import pytest
from app.services import ReferenceService
from app.models import Reference

async def test_search_and_save_references(test_db):
   reference_service = ReferenceService(test_db)
   
   keywords = ["artificial intelligence", "machine learning"]
   references = await reference_service.search_and_save_references(1, keywords)
   
   assert len(references) > 0
   assert all(isinstance(ref, Reference) for ref in references)
   assert all(ref.project_id == 1 for ref in references)

async def test_get_reference_summary(test_db):
   reference_service = ReferenceService(test_db)
   
   # 테스트용 참고문헌 생성
   reference = Reference(
       project_id=1,
       title="Test Reference",
       authors=["Test Author"],
       content="Test Content",
       metadata1={"test": "data"}
   )
   test_db.add(reference)
   test_db.commit()
   
   summary = await reference_service.get_reference_summary(reference.id)
   
   assert summary is not None
   assert "title" in summary
   assert "authors" in summary
   assert "summary" in summary
