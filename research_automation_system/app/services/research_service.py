from typing import List, Dict
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Project, ResearchStep
from .cohere_service import CohereService
from .perplexity_service import PerplexityService

class ResearchService:
   def __init__(self, 
                db: Session, 
                cohere_service: CohereService,
                perplexity_service: PerplexityService):
       self.db = db
       self.cohere = cohere_service
       self.perplexity = perplexity_service
   
   async def create_project(self, user_id: int, project_data: Dict) -> Project:
       # 프로젝트 생성
       project = Project(
           user_id=user_id,
           title=project_data['title'],
           description=project_data['description'],
           evaluation_plan=project_data['evaluation_plan'],
           submission_format=project_data['submission_format'],
           metadata=project_data.get('metadata', {})
       )
       
       self.db.add(project)
       self.db.commit()
       
       # 연구 계획 생성
       plan_result = await self.cohere.generate_research_plan(
           f"{project.description}\n\n평가 계획: {project.evaluation_plan}"
       )
       
       # 연구 단계 생성
       steps = self._parse_research_plan(plan_result['research_plan'])
       for step_number, step_data in enumerate(steps, 1):
           step = ResearchStep(
               project_id=project.id,
               step_number=step_number,
               description=step_data['description'],
               keywords=step_data.get('keywords', []),
               methodology=step_data.get('methodology', ''),
               output_format=step_data.get('output_format', ''),
               status='pending'
           )
           self.db.add(step)
       
       self.db.commit()
       return project
   
   async def execute_step(self, project_id: int, step_number: int) -> Dict:
       step = self.db.query(ResearchStep).filter_by(
           project_id=project_id,
           step_number=step_number
       ).first()
       
       if not step:
           raise ValueError("연구 단계를 찾을 수 없습니다.")
       
       try:
           # 관련 참고문헌 검색
           references = await self.perplexity.search_references(
               " ".join(step.keywords)
           )
           
           # 내용 분석
           analysis = await self.cohere.analyze_content(
               f"""
               연구 단계: {step.description}
               방법론: {step.methodology}
               참고문헌: {[ref['title'] for ref in references]}
               """
           )
           
           result = {
               "step_analysis": analysis,
               "references": references,
               "execution_time": datetime.utcnow().isoformat()
           }
           
           # 결과 저장
           step.status = 'completed'
           step.result = result
           step.executed_at = datetime.utcnow()
           
           self.db.commit()
           return result
           
       except Exception as e:
           step.status = 'failed'
           self.db.commit()
           raise e
   
   def _parse_research_plan(self, plan_text: str) -> List[Dict]:
       # 연구 계획 파싱 로직 구현
       # 예시 구현:
       steps = []
       sections = plan_text.split('\n\n')
       for section in sections:
           if not section.strip():
               continue
           
           lines = section.split('\n')
           step = {
               "description": lines[0].strip(),
               "keywords": [],
               "methodology": "",
               "output_format": ""
           }
           
           for line in lines[1:]:
               line = line.strip()
               if line.startswith('키워드:'):
                   step['keywords'] = [k.strip() for k in line[4:].split(',')]
               elif line.startswith('방법론:'):
                   step['methodology'] = line[4:].strip()
               elif line.startswith('결과물:'):
                   step['output_format'] = line[4:].strip()
           
           steps.append(step)
       
       return steps
