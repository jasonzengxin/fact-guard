import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException

def extract_text_from_url(url: str) -> str:
    """Extract text content from a URL"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        return soup.get_text()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to extract text from URL: {str(e)}") 