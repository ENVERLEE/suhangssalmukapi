import cohere
from typing import List, Dict
from datetime import datetime
from langchain.llms import Cohere
from langchain.embeddings import CohereEmbeddings
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class CohereService:
    def __init__(self, api_key: str):
        self.client = cohere.Client(api_key)
        self.llm = Cohere(
            model="c4ai-aya-expanse-32b",
            cohere_api_key=api_key,
            temperature=0.7
        )
        self.embeddings = CohereEmbeddings(
            cohere_api_key=api_key,
            model="embed-multilingual-v3.0"
        )
    
    async def generate_research_plan(self, context: str) -> Dict:
        prompt = PromptTemplate(
            template="""
            당신은 전문 연구원입니다. 다음 컨텍스트를 바탕으로 연구 계획을 생성해주세요:
            
            컨텍스트: {context}
            
            다음 형식으로 응답해주세요:
            1. 연구 목표
            2. 연구 방법
            3. 예상 결과
            4. 필요한 자원
            """,
            input_variables=["context"]
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        result = await chain.arun(context=context)
        
        return {
            "research_plan": result,
            "metadata": {
                "model": "c4ai-aya-expanse-32b",
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    
    async def analyze_content(self, content: str) -> Dict:
        response = await self.client.analyze(
            texts=[content],
            model="c4ai-aya-expanse-32b",
            task_type="classification",
            output_indicators=["main_topics", "key_findings", "methodology"]
        )
        
        return {
            "analysis": response.classifications[0],
            "confidence": response.confidence
        }
    
    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        embeddings = await self.embeddings.aembed_documents(texts)
        return embeddings
