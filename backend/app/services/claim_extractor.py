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
    
    async def extract_claims(self, text: str) -> List[str]:
        """
        Extract verifiable claims from text using GPT or fallback methods.
        
        Args:
            text (str): Text to extract claims from
            
        Returns:
            List[str]: List of extracted claims
        """
        try:
            return await self._extract_with_gpt(text)
        except Exception as e:
            logger.error(f"Error in GPT claim extraction: {str(e)}")
            return self._extract_with_basic_methods(text)
    
    async def _extract_with_gpt(self, text: str) -> List[str]:
        """
        Extract claims using GPT with streaming response.
        
        Args:
            text (str): Text to extract claims from
            
        Returns:
            List[str]: GPT-extracted claims
        """
        settings = get_settings()
        prompt = f"""请分析以下文本并提取可以验证的关键事实声明。
        对于每个声明，请专注于具体的、可验证的陈述，而不是观点或一般性陈述。
        如果有代词请根据上下文进行替换，比如这类儿童需要替代为具体的人群。
        返回的声明要有具体的意义，不要是一些没有意义的名词或标点。
        请以JSON数组的形式返回声明，每个元素是一个字符串。

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
                        "content": "你是一个事实核查助手。请只从给定文本中提取可验证的事实声明。"
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500,
                stream=True  # 启用流式响应
            )
            
            # 收集完整的响应内容
            full_content = ""
            total_chunks = 0
            chunks_received = 0
            
            # 首先计算总块数
            async for _ in response:
                total_chunks += 1
            
            # 重新创建流式响应
            response = await self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个事实核查助手。请只从给定文本中提取可验证的事实声明。"
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500,
                stream=True
            )
            
            try:
                async for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        full_content += chunk.choices[0].delta.content
                        chunks_received += 1
                        # 计算并发送进度
                        progress = int((chunks_received / total_chunks) * 100)
                        logger.debug(f"Extraction progress: {progress}%")
                        # 这里可以通过某种方式（如 WebSocket）发送进度到前端
            except asyncio.CancelledError:
                logger.warning("Stream processing was cancelled")
                raise
            except Exception as e:
                logger.error(f"Error during stream processing: {str(e)}")
                raise
            
            logger.debug(f"GPT response content: {full_content}")
            
            try:
                claims = json.loads(full_content)
                if not isinstance(claims, list):
                    raise ValueError("Response is not a JSON array")
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing error: {str(e)}")
                # 尝试从文本中提取数组
                full_content = full_content.replace("'", '"')  # 替换单引号为双引号
                try:
                    claims = json.loads(full_content)
                except:
                    # 如果还是失败，尝试手动提取数组
                    matches = re.findall(r'"([^"]+)"', full_content)
                    if not matches:
                        matches = re.findall(r"'([^']+)'", full_content)
                    claims = matches if matches else []
            
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