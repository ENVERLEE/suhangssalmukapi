from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models import Project
from app.services import ResearchService
from app.utils.database import get_db
from app.utils.security import get_current_user
from pydantic import BaseModel

router = APIRouter()

class ProjectCreate(BaseModel):
   title: str
   description: str
   evaluation_plan: str
   submission_format: str
   metadata1: dict = {}

class ProjectResponse(BaseModel):
   id: int
   title: str
   description: str
   created_at: str
   status: str

@router.post("/", response_model=ProjectResponse)
async def create_project(
   project: ProjectCreate,
   db: Session = Depends(get_db),
   current_user: int = Depends(get_current_user)
):
   research_service = ResearchService(db)
   new_project = await research_service.create_project(current_user, project.dict())
   
   return ProjectResponse(
       id=new_project.id,
       title=new_project.title,
       description=new_project.description,
       created_at=new_project.created_at.isoformat(),
       status="created"
   )

@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
   db: Session = Depends(get_db),
   current_user: int = Depends(get_current_user)
):
   projects = db.query(Project).filter(Project.user_id == current_user).all()
   return [
       ProjectResponse(
           id=project.id,
           title=project.title,
           description=project.description,
           created_at=project.created_at.isoformat(),
           status="completed" if project.steps[-1].status == "completed" else "in_progress"
       )
       for project in projects
   ]

@router.post("/{project_id}/steps/{step_number}/execute")
async def execute_step(
   project_id: int,
   step_number: int,
   db: Session = Depends(get_db),
   current_user: int = Depends(get_current_user)
):
   project = db.query(Project).filter(
       Project.id == project_id,
       Project.user_id == current_user
   ).first()
   
   if not project:
       raise HTTPException(status_code=404, detail="Project not found")
   
   research_service = ResearchService(db)
   result = await research_service.execute_step(project_id, step_number)
   
   return result
