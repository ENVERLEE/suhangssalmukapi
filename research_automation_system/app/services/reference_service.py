from typing import List, Dict
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Reference
from .perplexity_service import PerplexityService
from .cohere_service import CohereService

class ReferenceService:
   def __init__(self,
                db: Session,
                perplexity_service: PerplexityService,
                cohere_service: CohereService):
       self.db = db
       self.perplexity = perplexity_service
       self.cohere = cohere_service
   
   async def search_and_save_references(self,
                                      project_id: int,
                                      keywords: List[str]) -> List[Reference]:
       # Perplexity API로 참고문헌 검색
       query = " AND ".join(keywords)
       references = await self.perplexity.search_references(query)
       
       # 검색된 참고문헌 저장
       saved_references = []
       for ref_data in references:
           # 임베딩 생성
           embedding = await self.cohere.generate_embeddings([ref_data["abstract"]])
           
           reference = Reference(
               project_id=project_id,
               title=ref_data["title"],
               authors=ref_data["authors"],
               publication_date=datetime.fromisoformat(ref_data["publication_date"]),
               content=ref_data["abstract"],
               metadata={
                   "journal": ref_data["journal"],
                   "doi": ref_data["doi"],
                   "url": ref_data["url"],
                   "citations": ref_data["citations"]
               },
               embedding=embedding[0]
           )
           
           self.db.add(reference)
           saved_references.append(reference)
       
       self.db.commit()
       return saved_references
   
   async def get_reference_summary(self, reference_id: int) -> Dict:
       reference = self.db.query(Reference).get(reference_id)
       if not reference:
           raise ValueError("참고문헌을 찾을 수 없습니다.")
       
       # Cohere를 사용하여 요약 생성
       analysis = await self.cohere.analyze_content(reference.content)
       
       return {
           "title": reference.title,
           "authors": reference.authors,
           "summary": analysis["analysis"],
           "metadata": reference.metadata
       }
