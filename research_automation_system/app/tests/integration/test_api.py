from fastapi.testclient import TestClient
from research_automation_system.app.main import app

client = TestClient(app)

def test_create_project():
   response = client.post(
       "/api/projects/",
       json={
           "title": "Test Project",
           "description": "Test Description",
           "evaluation_plan": "Test Plan",
           "submission_format": "Test Format"
       },
       headers={"Authorization": "Bearer test-token"}
   )
   
   assert response.status_code == 200
   assert "id" in response.json()
   assert response.json()["title"] == "Test Project"

def test_search_references():
   response = client.post(
       "/api/references/search",
       params={"project_id": 1},
       json={
           "keywords": ["artificial intelligence", "machine learning"]
       },
       headers={"Authorization": "Bearer test-token"}
   )
   
   assert response.status_code == 200
   assert isinstance(response.json(), list)
   assert len(response.json()) > 0
