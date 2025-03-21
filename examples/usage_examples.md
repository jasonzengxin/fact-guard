# Fact Guard API Usage Examples

This document provides detailed examples of how to use the Fact Guard API for fact-checking.

## Text-Based Fact Checking

### Using curl

1. Basic single claim check:
```bash
curl -X POST "http://localhost:8000/check" \
     -H "Content-Type: application/json" \
     -d '{"text": "COVID-19 vaccines are effective in preventing severe illness."}'
```

2. Check multiple claims in one text:
```bash
curl -X POST "http://localhost:8000/check" \
     -H "Content-Type: application/json" \
     -d '{"text": "The Earth is round and orbits around the Sun. The Moon orbits around the Earth."}'
```

3. Check a longer article or statement:
```bash
curl -X POST "http://localhost:8000/check" \
     -H "Content-Type: application/json" \
     -d '{"text": "Global warming is caused by increased greenhouse gas emissions. This has led to rising global temperatures and more extreme weather events."}'
```

### Using Python requests

1. Basic single claim check:
```python
import requests

url = "http://localhost:8000/check"
data = {
    "text": "COVID-19 vaccines are effective in preventing severe illness."
}
response = requests.post(url, json=data)
result = response.json()
```

2. Check multiple claims:
```python
data = {
    "text": """
    The Earth is round and orbits around the Sun.
    The Moon orbits around the Earth.
    The Earth's rotation causes day and night.
    """
}
response = requests.post(url, json=data)
result = response.json()
```

3. Check a longer article:
```python
data = {
    "text": """
    Global warming is caused by increased greenhouse gas emissions.
    This has led to rising global temperatures and more extreme weather events.
    The main contributors are carbon dioxide and methane emissions.
    """
}
response = requests.post(url, json=data)
result = response.json()
```

## URL-Based Fact Checking

### Using curl
```bash
curl -X POST "http://localhost:8000/check" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com/article"}'
```

### Using Python requests
```python
import requests

url = "http://localhost:8000/check"
data = {
    "url": "https://example.com/article"
}
response = requests.post(url, json=data)
result = response.json()
```

## API Response Format

The API will return a response in this format:
```json
{
    "is_fact": true,
    "confidence": 0.85,
    "explanation": "Analysis of 3 key claims...",
    "sources": [
        {
            "title": "Source Title",
            "url": "https://example.com/source",
            "snippet": "Relevant text from the source",
            "reliability": 0.9
        }
    ],
    "discrepancies": [
        {
            "claim": "The specific claim that has discrepancies",
            "contradicting_sources": ["Source 1", "Source 2"],
            "explanation": "Why there are discrepancies"
        }
    ],
    "academic_sources": [
        {
            "title": "Academic Paper Title",
            "authors": ["Author 1", "Author 2"],
            "year": 2023,
            "url": "https://example.com/paper",
            "reliability": 0.95
        }
    ]
}
```

## Response Fields Explanation

- `is_fact`: Boolean indicating whether the content is factual
- `confidence`: Float between 0 and 1 indicating the confidence level of the analysis
- `explanation`: Detailed analysis of the claims
- `sources`: List of general web sources used for verification
- `discrepancies`: List of any contradictions found in the sources
- `academic_sources`: List of academic papers used for verification

Each source in the response includes:
- `title`: The title of the source
- `url`: The URL where the source can be found
- `snippet`: Relevant text excerpt from the source
- `reliability`: Confidence score for the source (0-1)

Academic sources include additional fields:
- `authors`: List of paper authors
- `year`: Publication year 