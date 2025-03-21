"""
Academic search service for finding scholarly sources.

This module provides functionality to search academic papers and studies
from various academic sources including Google Scholar and Semantic Scholar.
"""

import os
import logging
from typing import List, Dict, Optional
from models.schemas import Source, SourceType
import httpx
from bs4 import BeautifulSoup
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AcademicSearchService:
    def __init__(self):
        """Initialize the academic search service"""
        self.semantic_scholar_api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        logger.info("Initializing AcademicSearchService...")

    def search_all_academic_sources(self, query: str) -> List[Source]:
        """
        Search for academic sources across multiple platforms.
        
        Args:
            query (str): The search query
            
        Returns:
            List[Source]: List of academic sources found
        """
        logger.info(f"Searching academic sources for query: {query}")
        sources = []
        
        try:
            # Search Google Scholar
            scholar_sources = self._search_google_scholar(query)
            sources.extend(scholar_sources)
            logger.info(f"Found {len(scholar_sources)} sources from Google Scholar")
            
            # Search Semantic Scholar if API key is available
            if self.semantic_scholar_api_key:
                semantic_sources = self._search_semantic_scholar(query)
                sources.extend(semantic_sources)
                logger.info(f"Found {len(semantic_sources)} sources from Semantic Scholar")
            
        except Exception as e:
            logger.error(f"Error in academic search: {str(e)}")
        
        return sources

    def _search_google_scholar(self, query: str) -> List[Source]:
        """
        Search Google Scholar for academic papers.
        
        Args:
            query (str): The search query
            
        Returns:
            List[Source]: List of academic sources from Google Scholar
        """
        logger.info("Starting Google Scholar search")
        sources = []
        
        try:
            # Construct the Google Scholar URL
            base_url = "https://scholar.google.com/scholar"
            params = {
                "q": query,
                "hl": "en",
                "as_sdt": "0,5"
            }
            
            # Make the request
            with httpx.Client(headers=self.headers) as client:
                response = client.get(base_url, params=params)
                response.raise_for_status()
                
                # Parse the response
                soup = BeautifulSoup(response.text, 'html.parser')
                results = soup.find_all('div', class_='gs_r gs_or gs_scl')
                
                for result in results:
                    try:
                        # Extract title and link
                        title_elem = result.find('h3', class_='gs_rt')
                        if not title_elem:
                            continue
                            
                        title = title_elem.get_text().strip()
                        link = title_elem.find('a')
                        if not link:
                            continue
                            
                        url = link.get('href', '')
                        if not url.startswith('http'):
                            url = 'https://scholar.google.com' + url
                        
                        # Extract snippet
                        snippet_elem = result.find('div', class_='gs_rs')
                        snippet = snippet_elem.get_text().strip() if snippet_elem else ""
                        
                        # Extract authors and year
                        authors_elem = result.find('div', class_='gs_a')
                        authors_text = authors_elem.get_text().strip() if authors_elem else ""
                        
                        # Parse authors and year using regex
                        authors_match = re.match(r'([^0-9]+)(\d{4})?', authors_text)
                        if authors_match:
                            authors = [author.strip() for author in authors_match.group(1).split(',')]
                            year = int(authors_match.group(2)) if authors_match.group(2) else None
                        else:
                            authors = []
                            year = None
                        
                        # Create source object
                        source = Source(
                            title=title,
                            snippet=snippet,
                            link=url,
                            source_type=SourceType.ACADEMIC,
                            authors=authors,
                            year=year
                        )
                        
                        sources.append(source)
                        logger.debug(f"Added source: {title}")
                        
                    except Exception as e:
                        logger.error(f"Error processing Google Scholar result: {str(e)}")
                        continue
                
        except Exception as e:
            logger.error(f"Error in Google Scholar search: {str(e)}")
        
        return sources

    def _search_semantic_scholar(self, query: str) -> List[Source]:
        """
        Search Semantic Scholar for academic papers.
        
        Args:
            query (str): The search query
            
        Returns:
            List[Source]: List of academic sources from Semantic Scholar
        """
        logger.info("Starting Semantic Scholar search")
        sources = []
        
        try:
            # Construct the Semantic Scholar API URL
            base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
            params = {
                "query": query,
                "limit": 10,
                "fields": "paperId,title,abstract,authors,year,citationCount,url"
            }
            
            # Make the request
            with httpx.Client(headers={"x-api-key": self.semantic_scholar_api_key}) as client:
                response = client.get(base_url, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                for paper in data.get("data", []):
                    try:
                        # Extract authors
                        authors = [author.get("name", "") for author in paper.get("authors", [])]
                        
                        # Create source object
                        source = Source(
                            title=paper.get("title", ""),
                            snippet=paper.get("abstract", ""),
                            link=paper.get("url", ""),
                            source_type=SourceType.ACADEMIC,
                            authors=authors,
                            year=paper.get("year"),
                            citations=paper.get("citationCount")
                        )
                        
                        sources.append(source)
                        logger.debug(f"Added source: {paper.get('title')}")
                        
                    except Exception as e:
                        logger.error(f"Error processing Semantic Scholar result: {str(e)}")
                        continue
                
        except Exception as e:
            logger.error(f"Error in Semantic Scholar search: {str(e)}")
        
        return sources 