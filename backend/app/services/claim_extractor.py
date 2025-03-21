"""
Claim extractor for fact-checking.

This module provides functionality to extract verifiable claims
from text using GPT and basic text processing methods.
"""

import logging
import json
import re
import jieba
from typing import List
from openai import AsyncOpenAI
import asyncio
from ..core.config import get_settings

logger = logging.getLogger(__name__)

class ClaimExtractor:
    """Extracts verifiable claims from text."""
    
    def __init__(self, openai_client: AsyncOpenAI):
        """
        Initialize the claim extractor.
        
        Args:
            openai_client (AsyncOpenAI): OpenAI client instance
        """
        self.openai_client = openai_client
        # Initialize jieba for Chinese text processing
        jieba.initialize()
    
    async def extract_claims(self, text: str) -> List[dict]:
        """
        Extract verifiable claims from text using GPT or fallback methods.
        
        Args:
            text (str): Text to extract claims from
            
        Returns:
            List[dict]: List of dictionaries containing claims, uncommonness scores, and tags
        """
        try:
            results = await self._extract_with_gpt(text)
            # Add tags based on uncommonness scores
            for result in results:
                if result['uncommonness'] <= 30:
                    result['tag'] = "非常常见"
                elif result['uncommonness'] <= 60:
                    result['tag'] = "存疑待考"
                elif result['uncommonness'] < 75:
                    result['tag'] = "可能性较低"
                else:
                    result['tag'] = "几乎不可能"
            return results
        except Exception as e:
            logger.error(f"Error in GPT claim extraction: {str(e)}")
            basic_results = self._extract_with_basic_methods(text)
            return [{"claim": claim, "uncommonness": 50, "tag": "存疑待考"} for claim in basic_results]
    
    async def _extract_with_gpt(self, text: str) -> List[dict]:
        """
        Extract claims using GPT with streaming response.
        
        Args:
            text (str): Text to extract claims from
            
        Returns:
            List[dict]: List of dictionaries containing claims and their uncommonness scores
        """
        settings = get_settings()
        prompt = f"""请分析以下文本并提取可以验证的关键事实声明。
        对于每个声明，请专注于具体的、可验证的陈述，而不是观点或一般性陈述。
        如果有代词请根据上下文进行替换，比如这类儿童需要替代为具体的人群。
        返回的声明要有具体的意义，不要是一些没有意义的名词或标点。
        对于每个声明，请评估其不常见程度（0-100的整数），其中：
        - 0-30: 非常常见的事实
        - 31-60: 一般常见的事实
        - 61-100: 不常见或独特的事实
        请以JSON数组的形式返回，每个元素是一个对象，包含claim（声明）和uncommonness（不常见程度）两个字段。

        要分析的文本：
        {text}

        请只返回JSON数组，不要包含其他文本。"""

        try:
            # 使用流式响应
            response = await self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个事实核查助手。请从给定文本中提取可验证的事实声明，并评估每个声明的不常见程度。"
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500,
                stream=True  # 启用流式响应
            )
            
            # 收集完整的响应内容
            full_content = ""
            is_complete = False
            max_retries = 3
            retry_count = 0
            
            while not is_complete and retry_count < max_retries:
                try:
                    async for chunk in response:
                        if chunk.choices[0].delta.content is not None:
                            full_content += chunk.choices[0].delta.content
                            logger.debug(f"Received chunk: {chunk.choices[0].delta.content}")
                        
                        # 检查是否是最后一个chunk
                        if chunk.choices[0].finish_reason is not None:
                            is_complete = True
                            logger.debug("Stream completed successfully")
                            break
                            
                except asyncio.CancelledError:
                    logger.warning("Stream processing was cancelled")
                    raise
                except Exception as e:
                    logger.error(f"Error during stream processing: {str(e)}")
                    if retry_count < max_retries - 1:
                        retry_count += 1
                        logger.info(f"Retrying stream processing (attempt {retry_count + 1}/{max_retries})")
                        # 重新创建流式响应
                        response = await self.openai_client.chat.completions.create(
                            model=settings.OPENAI_MODEL_NAME,
                            messages=[
                                {
                                    "role": "system",
                                    "content": "你是一个事实核查助手。请从给定文本中提取可验证的事实声明，并评估每个声明的不常见程度。"
                                },
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.3,
                            max_tokens=500,
                            stream=True
                        )
                        continue
                    raise
            
            if not is_complete:
                logger.warning(f"Stream did not complete after {max_retries} attempts")
                raise Exception("Failed to get complete response after maximum retries")
                
            logger.debug(f"GPT response content: {full_content}")
            
            try:
                # 处理 markdown 代码块格式
                if full_content.startswith('```'):
                    # 移除开头的 ```json 和结尾的 ```
                    full_content = full_content.replace('```json\n', '').replace('\n```', '')
                
                results = json.loads(full_content)
                if not isinstance(results, list):
                    raise ValueError("Response is not a JSON array")
                
                # 验证每个结果的结构
                for result in results:
                    if not isinstance(result, dict) or 'claim' not in result or 'uncommonness' not in result:
                        raise ValueError("Each result must be a dict with 'claim' and 'uncommonness' fields")
                    if not isinstance(result['uncommonness'], (int, float)) or not 0 <= result['uncommonness'] <= 100:
                        raise ValueError("Uncommonness must be a number between 0 and 100")
                
                claims = results
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing error: {str(e)}")
                # 如果解析失败，返回空列表
                claims = []
            
            # 验证结果
            if not claims:
                logger.warning("No claims extracted from GPT response")
                return self._extract_with_basic_methods(text)
            
            logger.info(f"Extracted {len(claims)} key claims using GPT")
            return claims
            
        except asyncio.CancelledError:
            logger.warning("GPT claim extraction was cancelled")
            return self._extract_with_basic_methods(text)
        except Exception as e:
            logger.error(f"Error in GPT claim extraction: {str(e)}")
            return self._extract_with_basic_methods(text)
    
    def _extract_with_basic_methods(self, text: str) -> List[str]:
        """
        Extract claims using basic text processing methods.
        
        Args:
            text (str): Text to extract claims from
            
        Returns:
            List[str]: Basic extracted claims
        """
        # 根据语言选择分词方法
        if self._is_chinese_text(text):
            sentences = re.split(r'[。！？]', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            # 过滤掉太短的句子和疑问句
            claims = [
                s for s in sentences
                if len(jieba.lcut(s)) > 3 and not s.endswith('?')
            ]
        else:
            sentences = re.split(r'[.!?]', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            # 过滤掉太短的句子和疑问句
            claims = [
                s for s in sentences
                if len(s.split()) > 5 and not s.endswith('?')
            ]
        
        logger.info(f"Extracted {len(claims)} claims using basic methods")
        return claims
    
    def _is_chinese_text(self, text: str) -> bool:
        """
        Check if the text is Chinese by looking for Chinese characters.
        
        Args:
            text (str): Text to check
            
        Returns:
            bool: True if text contains Chinese characters
        """
        chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
        return bool(chinese_pattern.search(text)) 