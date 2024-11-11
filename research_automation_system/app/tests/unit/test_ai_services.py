import pytest
from app.services.ai import PerplexityService, CohereService
import os

@pytest.fixture
def perplexity_service():
    return PerplexityService(os.getenv("PERPLEXITY_API_KEY"))

@pytest.fixture
def cohere_service():
    return CohereService(os.getenv("COHERE_API_KEY"))

async def test_perplexity_search(perplexity_service):
    query = "machine learning applications in healthcare"
    results = await perplexity_service.search_references(query, max_results=5)
    
    assert len(results) > 0
    assert all(isinstance(ref, dict) for ref in results)
    assert all("title" in ref for ref in results)
    assert all("authors" in ref for ref in results)

async def test_cohere_research_plan(cohere_service):
    context = "Developing a new machine learning model for medical diagnosis"
    result = await cohere_service.generate_research_plan(context)
    
    assert "research_plan" in result
    assert "metadata" in result
    assert isinstance(result["research_plan"], str)

async def test_cohere_content_analysis(cohere_service):
    content = "This research introduces a novel approach to deep learning"
    result = await cohere_service.analyze_content(content)
    
    assert "analysis" in result
    assert "confidence" in result
    assert isinstance(result["confidence"], float)

async def test_cohere_embeddings(cohere_service):
    texts = ["machine learning", "artificial intelligence"]
    embeddings = await cohere_service.generate_embeddings(texts)
    
    assert len(embeddings) == len(texts)
    assert all(isinstance(emb, list) for emb in embeddings)
