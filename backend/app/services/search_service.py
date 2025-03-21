from typing import List, Dict
import os
from googleapiclient.discovery import build
import wikipediaapi
from newsapi import NewsApiClient
from app.models.schemas import Source
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SearchService:
    def __init__(self):
        logger.info("Initializing SearchService...")
        try:
            self.google_service = build("customsearch", "v1", developerKey=os.getenv("GOOGLE_API_KEY"))
            logger.info("Google Custom Search API initialized successfully")
            
            self.wiki_wiki = wikipediaapi.Wikipedia(
                language='en',
                user_agent='FactGuard/1.0 (https://github.com/yourusername/fact-guard; your@email.com)'
            )
            logger.info("Wikipedia API initialized successfully")
            
            self.newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))
            logger.info("News API initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing search services: {str(e)}")
            raise

    def search_google(self, query: str, num_results: int = 5) -> List[Source]:
        """Search Google for relevant information"""
        logger.info(f"Starting Google search for query: '{query}'")
        try:
            result = self.google_service.cse().list(
                q=query,
                cx=os.getenv("GOOGLE_CSE_ID"),
                num=num_results
            ).execute()
            
            sources = [
                Source(
                    title=item["title"],
                    link=item["link"],
                    snippet=item["snippet"],
                    source_type="google"
                )
                for item in result.get("items", [])
            ]
            logger.info(f"Google search completed. Found {len(sources)} results")
            return sources
        except Exception as e:
            logger.error(f"Google search error: {str(e)}")
            return []

    def search_wikipedia(self, query: str) -> List[Source]:
        """Search Wikipedia for relevant information"""
        logger.info(f"Starting Wikipedia search for query: '{query}'")
        try:
            page = self.wiki_wiki.page(query)
            if page.exists():
                logger.info(f"Found Wikipedia page: '{page.title}'")
                sources = [Source(
                    title=page.title,
                    link=page.fullurl,
                    snippet=page.summary,
                    source_type="wikipedia"
                )]
                logger.info("Wikipedia search completed successfully")
                return sources
            logger.warning(f"No Wikipedia page found for query: '{query}'")
            return []
        except Exception as e:
            logger.error(f"Wikipedia search error: {str(e)}")
            return []

    def search_news(self, query: str) -> List[Source]:
        """Search news articles for relevant information"""
        logger.info(f"Starting news search for query: '{query}'")
        try:
            news = self.newsapi.get_everything(
                q=query,
                language='en',
                sort_by='relevancy',
                page_size=5
            )
            sources = [
                Source(
                    title=article["title"],
                    link=article["url"],
                    snippet=article["description"],
                    source_type="news"
                )
                for article in news.get("articles", [])
                if article["description"]
            ]
            logger.info(f"News search completed. Found {len(sources)} articles")
            return sources
        except Exception as e:
            logger.error(f"News search error: {str(e)}")
            return []

    def search_all_sources(self, query: str) -> List[Source]:
        """Search across all available sources"""
        logger.info(f"Starting comprehensive search across all sources for query: '{query}'")
        
        # Search Google
        logger.info("Initiating Google search...")
        google_results = self.search_google(query)
        logger.debug(f"Google search returned {len(google_results)} results")
        
        # Search Wikipedia
        logger.info("Initiating Wikipedia search...")
        wiki_results = self.search_wikipedia(query)
        logger.debug(f"Wikipedia search returned {len(wiki_results)} results")
        
        # Search News
        logger.info("Initiating News search...")
        news_results = self.search_news(query)
        logger.debug(f"News search returned {len(news_results)} results")
        
        # Combine results
        all_results = google_results + wiki_results + news_results
        logger.info(f"Search completed. Total results: {len(all_results)}")
        
        # Log source type breakdown
        source_types = {}
        for source in all_results:
            source_types[source.source_type] = source_types.get(source.source_type, 0) + 1
        
        logger.info("Source type breakdown:")
        for source_type, count in source_types.items():
            logger.info(f"- {source_type}: {count} sources")
        
        return all_results 