from openai import OpenAI
from typing import List, Dict
import json
from datetime import datetime

class PerplexityService:
    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.perplexity.ai"
        )
    
    async def search_references(self, query: str, max_results: int = 10) -> List[Dict]:
        """학술 참고문헌을 검색합니다."""
        messages = [
            {
                "role": "system",
                "content": "You are a research assistant helping to find academic references."
            },
            {
                "role": "user",
                "content": f"""Find academic references related to: {query}
                Please provide up to {max_results} references in JSON format with the following fields:
                - title
                - authors
                - abstract
                - publication_date
                - journal
                - doi
                - url
                - citations"""
            }
        ]
        
        response = await self.client.chat.completions.create(
            model="llama-3.1-sonar-small-128k-online",
            messages=messages,
            temperature=0.3
        )
        
        try:
            result = json.loads(response.choices[0].message.content)
            return self._normalize_references(result)
        except json.JSONDecodeError:
            return self._parse_text_response(response.choices[0].message.content)
        
    def _parse_search_results(self, data: Dict) -> List[Dict]:
        references = []
        for result in data.get("results", []):
            reference = {
                "title": result.get("title"),
                "authors": result.get("authors", []),
                "abstract": result.get("abstract"),
                "publication_date": result.get("publication_date"),
                "journal": result.get("journal"),
                "doi": result.get("doi"),
                "url": result.get("url"),
                "citations": result.get("citation_count", 0)
           }
            references.append(reference)
        return references
