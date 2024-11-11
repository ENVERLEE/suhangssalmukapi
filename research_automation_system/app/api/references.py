from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models import Reference
from app.services import ReferenceService
from app.utils.database import get_db
from app.utils.security import get_current_user
from pydantic import BaseModel

router = APIRouter()

class ReferenceSearch(BaseModel):
   keywords: List[str]

class ReferenceResponse(BaseModel):
   id: int
   title: str
   authors: List[str]
   publication_date: str
   content: str
   metadata1: dict

@router.post("/search", response_model=List[ReferenceResponse])
async def search_references(
   search: ReferenceSearch,
   project_id: int,
   db: Session = Depends(get_db),
   current_user: int = Depends(get_current_user)
):
   reference_service = ReferenceService(db)
   references = await reference_service.search_and_save_references(
       project_id,
       search.keywords
   )
   
   return [
       ReferenceResponse(
           id=ref.id,
           title=ref.title,
           authors=ref.authors,
           publication_date=ref.publication_date.isoformat(),
           content=ref.content,
           metadata1=ref.metadata1
       )
       for ref in references
   ]

@router.get("/{reference_id}/summary")
async def get_reference_summary(
   reference_id: int,
   db: Session = Depends(get_db),
   current_user: int = Depends(get_current_user)
):
   reference_service = ReferenceService(db)
   return await reference_service.get_reference_summary(reference_id)
