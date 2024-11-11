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
    
    def _normalize_references(self, references: List[Dict]) -> List[Dict]:
        """참고문헌 데이터를 표준 형식으로 변환합니다."""
        normalized = []
        for ref in references:
            normalized.append({
                "title": ref.get("title", ""),
                "authors": ref.get("authors", []),
                "abstract": ref.get("abstract", ""),
                "publication_date": ref.get("publication_date", ""),
                "journal": ref.get("journal", ""),
                "doi": ref.get("doi", ""),
                "url": ref.get("url", ""),
                "citations": int(ref.get("citations", 0))
            })
        return normalized
    
    def _parse_text_response(self, text: str) -> List[Dict]:
        """텍스트 응답을 구조화된 형식으로 변환합니다."""
        # 기본 구현
        references = []
        current_ref = {}
        
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('Title:'):
                if current_ref:
                    references.append(current_ref)
                current_ref = {"title": line[6:].strip()}
            elif line.startswith('Authors:'):
                current_ref['authors'] = [a.strip() for a in line[8:].split(',')]
            elif line.startswith('Abstract:'):
                current_ref['abstract'] = line[9:].strip()
            elif line.startswith('Journal:'):
                current_ref['journal'] = line[8:].strip()
            elif line.startswith('DOI:'):
                current_ref['doi'] = line[4:].strip()
            elif line.startswith('URL:'):
                current_ref['url'] = line[4:].strip()
            elif line.startswith('Citations:'):
                try:
                    current_ref['citations'] = int(line[10:].strip())
                except ValueError:
                    current_ref['citations'] = 0
        
        if current_ref:
            references.append(current_ref)
        
        return references
