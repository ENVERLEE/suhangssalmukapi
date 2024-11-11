import pytest
from datetime import datetime
from app.services import ResearchService
from app.models import Project, ResearchStep

def test_create_project(test_db):
   research_service = ResearchService(test_db)
   
   project_data = {
       "title": "Test Project",
       "description": "Test Description",
       "evaluation_plan": "Test Plan",
       "submission_format": "Test Format",
       "metadata1": {"test": "data"}
   }
   
   project = research_service.create_project(1, project_data)
   
   assert project.title == project_data["title"]
   assert project.description == project_data["description"]
   assert len(project.steps) > 0

async def test_execute_step(test_db):
   research_service = ResearchService(test_db)
   
   # 테스트용 프로젝트와 단계 생성
   project = Project(
       title="Test Project",
       user_id=1
   )
   test_db.add(project)
   test_db.commit()
   
   step = ResearchStep(
       project_id=project.id,
       step_number=1,
       description="Test Step",
       keywords=["test"],
       status="pending"
   )
   test_db.add(step)
   test_db.commit()
   
   result = await research_service.execute_step(project.id, 1)
   
   assert result is not None
   assert "step_analysis" in result
   assert "references" in result
