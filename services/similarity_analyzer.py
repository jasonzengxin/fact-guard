"""
Similarity analyzer for fact-checking.

This module provides functionality to analyze similarity between claims
and sources using GPT and basic text comparison methods.
"""

import logging
import jieba
from typing import Dict
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)

class SimilarityAnalyzer:
    """Analyzes similarity between claims and sources."""
    
    def __init__(self, openai_client: AsyncOpenAI):
        """
        Initialize the similarity analyzer.
        
        Args:
            openai_client (AsyncOpenAI): OpenAI client instance
        """
        self.openai_client = openai_client
        # Initialize jieba for Chinese text processing
        jieba.initialize()
    
    async def analyze_similarity(self, claim: str, source: 'Source') -> Dict:
        """
        Analyze similarity between a claim and a source using GPT.
        
        Args:
            claim (str): The claim to verify
            source (Source): The source to check against
            
        Returns:
            Dict: Analysis results including similarity score and explanation
        """
        try:
            return await self._analyze_with_gpt(claim, source)
        except Exception as e:
            logger.error(f"Error in GPT similarity analysis: {str(e)}")
            return self._analyze_with_basic_methods(claim, source)
    
    async def _analyze_with_gpt(self, claim: str, source: 'Source') -> Dict:
        """
        Analyze similarity using GPT.
        
        Args:
            claim (str): The claim to verify
            source (Source): The source to check against
            
        Returns:
            Dict: GPT analysis results
        """
        prompt = f"""请分析以下声明和来源文本之间的相似度和关系。
        请仔细分析以下几个方面：
        1. 核心信息是否相似（即使表达方式不同）
        2. 关键词和概念的重叠程度
        3. 语义上的关联性
        4. 是否存在支持或反驳关系
        
        请返回一个包含以下结构的JSON对象：
        {{
            "similarity_score": float (0-1),  // 基于以上所有方面的综合评分
            "is_supporting": boolean,         // 是否支持该声明
            "explanation": string             // 用中文解释相似度评分的原因
        }}

        声明：
        {claim}

        来源：
        {source.snippet}

        请只返回JSON对象，不要包含其他文本。"""

        response = await self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "你是一个事实核查助手。请仔细分析文本之间的相似度，即使表达方式不同，只要核心信息相似就应该给出较高的相似度分数。请用中文解释你的分析。"
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        content = response.choices[0].message.content.strip()
        logger.debug(f"GPT similarity analysis response: {content}")
        
        try:
            analysis = eval(content)  # 使用eval而不是json.loads，因为GPT可能返回Python字典格式
            if not isinstance(analysis, dict):
                raise ValueError("Response is not a dictionary")
        except Exception as e:
            logger.error(f"Failed to parse GPT response: {str(e)}")
            return self._analyze_with_basic_methods(claim, source)
        
        # 如果相似度分数过低，但确实存在相关表达，适当提高分数
        if analysis["similarity_score"] < 0.3:
            # 使用jieba分词检查关键词重叠
            claim_words = set(jieba.lcut(claim))
            source_words = set(jieba.lcut(source.snippet))
            overlap = len(claim_words.intersection(source_words))
            if overlap > 0:
                # 根据重叠词数量适当提高分数
                analysis["similarity_score"] = min(0.5, analysis["similarity_score"] + (overlap * 0.1))
                analysis["explanation"] += f"\n由于存在{overlap}个重叠关键词，相似度分数已适当调整。"
        
        # 根据相似度分数调整 is_supporting
        analysis["is_supporting"] = analysis["similarity_score"] > 0.3
        
        logger.info(f"相似度分析结果: 分数={analysis['similarity_score']:.2f}, 是否支持={analysis['is_supporting']}")
        logger.info(f"分析说明: {analysis['explanation']}")
        
        return analysis
    
    def _analyze_with_basic_methods(self, claim: str, source: 'Source') -> Dict:
        """
        Analyze similarity using basic text comparison methods.
        
        Args:
            claim (str): The claim to verify
            source (Source): The source to check against
            
        Returns:
            Dict: Basic analysis results
        """
        # 使用jieba分词检查关键词重叠
        claim_words = set(jieba.lcut(claim))
        source_words = set(jieba.lcut(source.snippet))
        overlap = len(claim_words.intersection(source_words))
        
        # 计算基本相似度分数
        similarity = min(0.5, overlap * 0.1)  # 每个重叠词贡献0.1分，最高0.5分
        
        result = {
            "similarity_score": similarity,
            "is_supporting": similarity > 0.3,
            "explanation": f"基本相似度得分：{similarity:.2f}，包含{overlap}个重叠关键词"
        }
        
        logger.info(f"使用基本相似度计算的结果: 分数={result['similarity_score']:.2f}, 是否支持={result['is_supporting']}")
        return result 