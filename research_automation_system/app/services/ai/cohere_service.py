import cohere
from typing import List, Dict
from datetime import datetime

class CohereService:
    def __init__(self, api_key: str):
        self.client = cohere.Client(api_key)
    
    async def generate_research_plan(self, context: str) -> Dict:
        """연구 계획을 생성합니다."""
        response = await self.client.chat(
            message=f"""Create a detailed research plan based on the following context:
            
            {context}
            
            Please provide:
            1. Research objectives
            2. Methodology
            3. Expected outcomes
            4. Required resources
            """,
            model="c4ai-aya-expanse-32b",
            temperature=0.3
        )
        
        return {
            "research_plan": response.text,
            "metadata": {
                "model": "command",
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    
    async def analyze_content(self, content: str) -> Dict:
        """문서 내용을 분석합니다."""
        response = await self.client.classify(
            inputs=[content],
            examples=[
                {"text": "This study explores machine learning.", "label": "methodology"},
                {"text": "The results show significant improvements.", "label": "findings"},
                {"text": "We propose a new approach.", "label": "proposal"}
            ],
            model="large"
        )
        
        return {
            "analysis": response.classifications[0],
            "confidence": response.confidences[0]
        }
    
    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """텍스트의 임베딩을 생성합니다."""
        response = await self.client.embed(
            texts=texts,
            model="embed-multilingual-v3.0"
        )
        
        return response.embeddings
