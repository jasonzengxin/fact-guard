"""
Explanation generator for fact-checking results.

This module provides functionality to generate human-readable explanations
of fact-checking results using GPT or fallback to basic explanations.
"""

import logging
from typing import Dict
from openai import OpenAI

logger = logging.getLogger(__name__)

class ExplanationGenerator:
    """Generates human-readable explanations for fact-checking results."""
    
    def __init__(self, openai_client: OpenAI):
        """
        Initialize the explanation generator.
        
        Args:
            openai_client (OpenAI): OpenAI client instance
        """
        self.openai_client = openai_client
    
    async def generate_explanation(self, confidence: float, num_sources: int) -> str:
        """
        Generate a human-readable explanation using GPT or fallback.
        
        Args:
            confidence (float): Overall confidence score
            num_sources (int): Number of supporting sources
            
        Returns:
            str: Human-readable explanation in Chinese
        """
        try:
            return await self._generate_gpt_explanation(confidence, num_sources)
        except Exception as e:
            logger.error(f"Error in GPT explanation generation: {str(e)}")
            return self._generate_basic_explanation(confidence, num_sources)
    
    async def _generate_gpt_explanation(self, confidence: float, num_sources: int) -> str:
        """
        Generate explanation using GPT.
        
        Args:
            confidence (float): Overall confidence score
            num_sources (int): Number of supporting sources
            
        Returns:
            str: GPT-generated explanation in Chinese
        """
        prompt = f"""请用中文生成一个清晰简洁的事实核查结果说明。
        请包含以下信息：
        - 整体可靠性评估
        - 置信度
        - 支持来源数量
        
        请使用自然、易懂的中文表达。
        
        结果：
        - 置信度：{confidence:.2f}
        - 支持来源：{num_sources}
        
        请只返回说明文本，不要包含其他格式。"""

        response = await self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "你是一个事实核查助手。请用清晰简洁的中文生成事实核查结果说明。"
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        return response.choices[0].message.content.strip()
    
    def _generate_basic_explanation(self, confidence: float, num_sources: int) -> str:
        """
        Generate basic explanation as fallback.
        
        Args:
            confidence (float): Overall confidence score
            num_sources (int): Number of supporting sources
            
        Returns:
            str: Basic explanation in Chinese
        """
        if confidence > 0.8:
            base = "这条信息高度可靠"
        elif confidence > 0.6:
            base = "这条信息基本可靠"
        elif confidence > 0.4:
            base = "这条信息的可靠性存在争议"
        else:
            base = "这条信息不可靠"
        
        explanation = f"{base}，置信度为{confidence:.1%}。"
        explanation += f"有{num_sources}个来源支持"
        explanation += "。"
        
        return explanation 