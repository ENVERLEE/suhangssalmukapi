from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class ResearchStep(Base):
    __tablename__ = 'research_steps'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    step_number = Column(Integer)
    description = Column(String(1000))
    keywords = Column(JSON)
    methodology = Column(String(500))
    output_format = Column(String(200))
    status = Column(String(50))
    result = Column(JSON)
    executed_at = Column(DateTime)
    
    project = relationship("Project", back_populates="steps")
