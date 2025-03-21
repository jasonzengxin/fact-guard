"""
Analysis service for fact-checking

This module provides the core analysis functionality for fact-checking,
including claim extraction, similarity calculation, and result generation.
"""

import logging
import os
import httpx
from openai import AsyncOpenAI
from typing import List
from ..models.schemas import Source, FactCheckResponse

from .claim_extractor import ClaimExtractor
from .similarity_analyzer import SimilarityAnalyzer
from .confidence_calculator import ConfidenceCalculator
from .explanation_generator import ExplanationGenerator

logger = logging.getLogger(__name__)

class AnalysisService:
    def __init__(self):
        """Initialize the analysis service with required components."""
        try:
            # Initialize OpenAI client
            self.openai_client = AsyncOpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                http_client=httpx.AsyncClient(
                    timeout=httpx.Timeout(30.0, connect=10.0),
                    limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
                )
            )
            
            # Initialize specialized services
            self.claim_extractor = ClaimExtractor(self.openai_client)
            self.similarity_analyzer = SimilarityAnalyzer(self.openai_client)
            self.confidence_calculator = ConfidenceCalculator()
            self.explanation_generator = ExplanationGenerator(self.openai_client)
            
            logger.info("Initializing AnalysisService...")
        except Exception as e:
            logger.error(f"初始化 AnalysisService 失败: {str(e)}")
            raise

    async def analyze_text(self, text: str, sources: List[Source]) -> FactCheckResponse:
        """
        Analyze text against sources using specialized services.
        
        Args:
            text (str): Text to analyze
            sources (List[Source]): List of sources to check against
            
        Returns:
            FactCheckResponse: Analysis results including factuality and confidence
        """
        try:
            logger.info("开始使用GPT进行全面分析")
            logger.info(f"收到 {len(sources)} 个来源进行分析")
            
            if not sources:
                logger.warning("没有提供任何来源进行分析")
                return FactCheckResponse(
                    is_fact=False,
                    confidence=0.0,
                    explanation="没有提供任何来源进行验证。",
                    sources=[],
                    academic_sources=[]
                )
            
            # Extract claims using specialized service
            try:
                claims = await self.claim_extractor.extract_claims(text)
                logger.info(f"提取出 {len(claims)} 个声明: {claims}")
            except Exception as e:
                logger.error(f"提取声明时出错: {str(e)}")
                return FactCheckResponse(
                    is_fact=False,
                    confidence=0.0,
                    explanation="提取声明时发生错误，请稍后重试。",
                    sources=[],
                    academic_sources=[]
                )
            
            if not claims:
                logger.warning("文本中没有找到可验证的声明")
                return FactCheckResponse(
                    is_fact=False,
                    confidence=0.0,
                    explanation="文本中没有找到可验证的声明。",
                    sources=[],
                    academic_sources=[]
                )
            
            # Analyze each claim against sources
            verified_sources = []
            source_contributions = {}
            claim_scores = {}
            
            for claim in claims:
                try:
                    logger.info(f"\n{'='*50}")
                    logger.info(f"开始分析声明: {claim}")
                    logger.info(f"{'='*50}")
                    
                    claim_similarity = 0
                    claim_sources = []
                    claim_source_scores = []
                    
                    for source in sources:
                        logger.info(f"\n检查来源: {source.title}")
                        try:
                            analysis = await self.similarity_analyzer.analyze_similarity(claim, source)
                            similarity = analysis["similarity_score"]
                            logger.info(f"来源 '{source.title}' 的相似度得分: {similarity:.2f}")
                            
                            if analysis["is_supporting"]:
                                # Calculate source contribution based on similarity and source type
                                base_contribution = similarity
                                if source.source_type == "academic":
                                    base_contribution *= 1.2
                                    logger.info(f"学术来源加成: 基础分数 {similarity:.2f} -> {base_contribution:.2f}")
                                elif source.source_type == "government":
                                    base_contribution *= 1.1
                                    logger.info(f"政府来源加成: 基础分数 {similarity:.2f} -> {base_contribution:.2f}")
                                
                                # Update source contribution score
                                if source.title not in source_contributions:
                                    source_contributions[source.title] = 0
                                source_contributions[source.title] = max(
                                    source_contributions[source.title],
                                    base_contribution
                                )
                                
                                claim_similarity = max(claim_similarity, similarity)
                                if source not in claim_sources:
                                    claim_sources.append(source)
                                    claim_source_scores.append({
                                        "source": source.title,
                                        "score": base_contribution,
                                        "type": source.source_type
                                    })
                                    logger.info(f"添加支持来源: {source.title} (得分: {base_contribution:.2f})")
                        except Exception as e:
                            logger.error(f"分析来源 '{source.title}' 时出错: {str(e)}")
                            continue
                    
                    if claim_sources:
                        verified_sources.extend(claim_sources)
                        claim_scores[claim] = {
                            "total_score": claim_similarity,
                            "source_count": len(claim_sources),
                            "source_details": claim_source_scores
                        }
                        logger.info(f"\n声明 '{claim}' 的最终得分: {claim_similarity:.2f}")
                        logger.info(f"支持来源数量: {len(claim_sources)}")
                        logger.info("支持来源详情:")
                        for source_detail in claim_source_scores:
                            logger.info(f"- {source_detail['source']} ({source_detail['type']}): {source_detail['score']:.2f}")
                    else:
                        logger.warning(f"未找到支持声明 '{claim}' 的来源")
                        claim_scores[claim] = {
                            "total_score": 0,
                            "source_count": 0,
                            "source_details": []
                        }
                except Exception as e:
                    logger.error(f"处理声明 '{claim}' 时出错: {str(e)}")
                    continue
            
            # Calculate confidence using specialized service
            try:
                confidence = self.confidence_calculator.calculate_confidence(
                    claims, verified_sources, claim_scores, source_contributions
                )
            except Exception as e:
                logger.error(f"计算置信度时出错: {str(e)}")
                confidence = 0.0
            
            # Log detailed scores
            try:
                self.confidence_calculator.log_claim_scores(claim_scores)
                self.confidence_calculator.log_source_details(verified_sources)
            except Exception as e:
                logger.error(f"记录详细分数时出错: {str(e)}")
            
            # Add contribution scores to sources
            for source in verified_sources:
                source.contribution_score = source_contributions.get(source.title, 0)
            
            # Generate explanation using specialized service
            try:
                explanation = await self.explanation_generator.generate_explanation(
                    confidence, len(verified_sources)
                )
            except Exception as e:
                logger.error(f"生成解释时出错: {str(e)}")
                explanation = "分析过程中出现错误，无法生成详细解释。"
            
            logger.info(f"\n分析完成。最终置信度: {confidence:.2f}")
            logger.info(f"已验证的来源数量: {len(verified_sources)}")
            
            return FactCheckResponse(
                is_fact=confidence > 0.6,
                confidence=confidence,
                explanation=explanation,
                sources=verified_sources,
                academic_sources=[s for s in verified_sources if s.source_type == "academic"]
            )
        except Exception as e:
            logger.error(f"分析过程中发生严重错误: {str(e)}")
            return FactCheckResponse(
                is_fact=False,
                confidence=0.0,
                explanation="分析过程中发生错误，请稍后重试。",
                sources=[],
                academic_sources=[]
            ) 