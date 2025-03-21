"""
Confidence calculator for fact-checking results.

This module provides functionality to calculate confidence scores
based on various factors including claim similarity and source diversity.
"""

import logging
from typing import List, Dict
from models.schemas import Source

logger = logging.getLogger(__name__)

class ConfidenceCalculator:
    """Calculates confidence scores for fact-checking results."""
    
    def calculate_confidence(
        self,
        claims: List[str],
        verified_sources: List[Source],
        claim_scores: Dict[str, Dict],
        source_contributions: Dict[str, float]
    ) -> float:
        """
        Calculate overall confidence score based on multiple factors.
        
        Args:
            claims (List[str]): List of claims to verify
            verified_sources (List[Source]): List of verified sources
            claim_scores (Dict[str, Dict]): Scores for each claim
            source_contributions (Dict[str, float]): Contribution scores for each source
            
        Returns:
            float: Overall confidence score between 0 and 1
        """
        num_claims = len(claims)
        if num_claims == 0:
            logger.warning("没有声明可以计算置信度")
            return 0.0
            
        # Calculate average similarity per claim
        total_similarity = sum(score["total_score"] for score in claim_scores.values())
        avg_similarity = total_similarity / num_claims
        
        # Calculate source diversity bonus
        unique_sources = len(set(s.title for s in verified_sources))
        source_diversity = min(unique_sources / num_claims, 1.0)
        
        # Calculate source type bonus
        academic_count = sum(1 for s in verified_sources if s.source_type == "academic")
        gov_count = sum(1 for s in verified_sources if s.source_type == "government")
        source_type_bonus = min((academic_count * 0.1 + gov_count * 0.05) / num_claims, 0.2)
        
        # Combine all factors for final confidence
        confidence = min(1.0, avg_similarity * (1 + source_diversity * 0.2 + source_type_bonus))
        
        # Log detailed analysis
        self._log_analysis_details(
            num_claims,
            avg_similarity,
            source_diversity,
            source_type_bonus,
            confidence
        )
        
        return confidence
    
    def _log_analysis_details(
        self,
        num_claims: int,
        avg_similarity: float,
        source_diversity: float,
        source_type_bonus: float,
        confidence: float
    ) -> None:
        """Log detailed analysis information."""
        logger.info(f"\n{'='*50}")
        logger.info("最终分析结果:")
        logger.info(f"{'='*50}")
        logger.info(f"总声明数: {num_claims}")
        logger.info(f"平均相似度: {avg_similarity:.2f}")
        logger.info(f"来源多样性: {source_diversity:.2f}")
        logger.info(f"来源类型加成: {source_type_bonus:.2f}")
        logger.info(f"最终置信度: {confidence:.2f}")
    
    def log_claim_scores(self, claim_scores: Dict[str, Dict]) -> None:
        """Log detailed scores for each claim."""
        logger.info("\n各声明得分详情:")
        for claim, score_info in claim_scores.items():
            logger.info(f"\n声明: {claim}")
            logger.info(f"总分: {score_info['total_score']:.2f}")
            logger.info(f"支持来源数: {score_info['source_count']}")
            if score_info['source_details']:
                logger.info("来源详情:")
                for source_detail in score_info['source_details']:
                    logger.info(
                        f"- {source_detail['source']} "
                        f"({source_detail['type']}): {source_detail['score']:.2f}"
                    )
    
    def log_source_details(self, verified_sources: List[Source]) -> None:
        """Log details about verified sources."""
        logger.info("\n已验证的来源详情:")
        for source in verified_sources:
            logger.info(
                f"- {source.title} ({source.source_type}) - "
                f"贡献度: {source.contribution_score:.2f}"
            ) 