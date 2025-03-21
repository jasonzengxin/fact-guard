"""
DeepSeek API integration service

This module provides integration with the DeepSeek API for text analysis and fact-checking.
"""

import os
import logging
from typing import Dict, Any, List, AsyncGenerator
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)

class DeepSeekService:
    def __init__(self):
        """Initialize the DeepSeek service with API key."""
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable is not set")
        
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com"
        )

    async def analyze_text_stream(self, text: str, task: str = "fact_check") -> AsyncGenerator[str, None]:
        """
        Analyze text using DeepSeek API with streaming response.
        
        Args:
            text (str): Text to analyze
            task (str): Type of analysis to perform
            
        Yields:
            str: Chunks of the response
        """
        try:
            messages = [
                {
                    "role": "system", 
                    "content": "你是一个事实核查助手。请从给定文本中提取可验证的事实声明，并评估每个声明的不常见程度。"
                },
                {
                    "role": "user", 
                    "content": f"""请分析以下文本并提取可以验证的关键事实声明。
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
                }
            ]
            
            response = await self.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                temperature=0.3,
                max_tokens=1000,
                stream=True
            )
            
            async for chunk in response:
                if content := chunk.choices[0].delta.content:
                    yield content
                            
        except Exception as e:
            logger.error(f"Error in DeepSeek API stream call: {str(e)}")
            raise

    async def analyze_text(self, text: str, task: str = "fact_check") -> Dict[str, Any]:
        """
        Analyze text using DeepSeek API.
        
        Args:
            text (str): Text to analyze
            task (str): Type of analysis to perform
            
        Returns:
            Dict[str, Any]: Analysis results
        """
        try:
            messages = [
                {
                    "role": "system", 
                    "content": "你是一个事实核查助手。请从给定文本中提取可验证的事实声明，并评估每个声明的不常见程度。"
                },
                {
                    "role": "user", 
                    "content": f"""请分析以下文本并提取可以验证的关键事实声明。
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
                }
            ]
            
            response = await self.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                temperature=0.3,
                max_tokens=1000,
                stream=False
            )
            
            return {
                "choices": [{
                    "message": {
                        "content": response.choices[0].message.content
                    }
                }]
            }
            
        except Exception as e:
            logger.error(f"Error in DeepSeek API call: {str(e)}")
            raise

    async def extract_claims(self, text: str) -> List[dict]:
        """
        Extract claims from text using DeepSeek API.
        
        Args:
            text (str): Text to extract claims from
            
        Returns:
            List[dict]: List of dictionaries containing claims, uncommonness scores, and tags
        """
        try:
            result = await self.analyze_text(text, task="extract_claims")
            # Parse the response and extract claims
            claims = result.get("choices", [{}])[0].get("message", {}).get("content", "").split("\n")
            #claims = ['```json', '[', '    {', '        "claim": "腺样体肥大患儿中约65%存在颌面骨骼发育异常，表现为上颌前突或下颌后缩。",', '        "uncommonness": 40', '    },', '    {', '        "claim": "北京协和医院2023年研究证实，持续口呼吸6个月以上的儿童，骨缝闭合前（通常12岁前）进行干预可降低60%不可逆面容损伤风险。",', '        "uncommonness": 70', '    },', '    {', '        "claim": "腺样体肥大患儿夜间血氧饱和度常低于90%（正常值95%-100%）。",', '        "uncommonness": 50', '    },', '    {', '        "claim": "持续缺氧直接损伤海马体，导致记忆容量缩减30%，注意力持续时间缩短50%。",', '        "uncommonness": 65', '    },', '    {', '        "claim": "腺样体肥大患儿出现学习障碍的概率是健康儿童的4.6倍。",', '        "uncommonness": 60', '    },', '    {', '        "claim": "肥大的腺样体成为细菌培养皿，脓性分泌物倒流引发中耳炎（发病率68%）、鼻窦炎（52%）。",', '        "uncommonness": 55', '    },', '    {', '        "claim": "长期炎症刺激会改写免疫系统编码，使过敏性疾病发生率提升3.8倍，哮喘风险增加2.4倍。",', '        "uncommonness": 70', '    },', '    {', '        "claim": "儿童期腺样体肥大者，成年后罹患高血压的风险提升27%。",', '        "uncommonness": 75', '    },', '    {', '        "claim": "因面容异常导致的校园歧视率高达43%。",', '        "uncommonness": 60', '    },', '    {', '        "claim": "睡眠障碍引发的情绪失控发生率61%。",', '        "uncommonness": 55', '    },', '    {', '        "claim": "腺样体肥大患儿的抑郁倾向是同龄人的5.2倍。",', '        "uncommonness": 65', '    },', '    {', '        "claim": "腺样体肥大患儿的社交恐惧症发生率高出3.8倍。",', '        "uncommonness": 65', '    }', ']', '```']
            
            # Join the array elements and remove markdown code block markers
            json_str = ''.join(claims).replace('```json', '').replace('```', '').strip()
            
            # Parse the JSON string and extract claims with uncommonness
            import json
            claims_data = json.loads(json_str)
            
            # Add tags based on uncommonness scores
            results = []
            for item in claims_data:
                uncommonness = item['uncommonness']
                if uncommonness <= 30:
                    tag = "非常常见"
                elif uncommonness <= 60:
                    tag = "存疑待考"
                elif uncommonness < 75:
                    tag = "可能性较低"
                else:
                    tag = "几乎不可能"
                    
                results.append({
                    "claim": item['claim'],
                    "uncommonness": uncommonness,
                    "tag": tag
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error extracting claims: {str(e)}")
            return []

    async def check_factuality(self, claim: str, context: str = "") -> Dict[str, Any]:
        """
        Check the factuality of a claim using DeepSeek API.
        
        Args:
            claim (str): Claim to check
            context (str): Additional context for fact-checking
            
        Returns:
            Dict[str, Any]: Fact-checking results
        """
        try:
            prompt = f"Claim: {claim}\nContext: {context}\nPlease analyze the factuality of this claim."
            result = await self.analyze_text(prompt, task="fact_check")
            
            # Parse the response and extract fact-checking results
            return {
                "is_fact": True,  # This should be determined from the API response
                "confidence": 0.8,  # This should be calculated from the API response
                "explanation": result.get("choices", [{}])[0].get("message", {}).get("content", ""),
                "sources": []  # This should be extracted from the API response
            }
            
        except Exception as e:
            logger.error(f"Error checking factuality: {str(e)}")
            return {
                "is_fact": False,
                "confidence": 0.0,
                "explanation": "Error occurred during fact-checking",
                "sources": []
            } 