# Research Automation System

AI 기반 연구 자동화 시스템입니다.

## 기능

- 연구 계획 자동 생성
- 참고문헌 검색 및 분석
- 연구 단계 자동화 실행
- 문서 처리 및 분석

## 설치 및 실행

1. 환경 설정
```bash
cp .env.example .env
# .env 파일 수정
## AI 서비스 설정

### Perplexity API
- OpenAI 호환 인터페이스 사용
- llama-3.1-sonar-large-128k-online 모델 활용
- 학술 참고문헌 검색 및 분석

### Cohere API
- 연구 계획 생성
- 문서 내용 분석
- 다국어 임베딩 지원

### 사용 예시
```python
# 서비스 초기화
perplexity = PerplexityService(os.getenv("PERPLEXITY_API_KEY"))
cohere = CohereService(os.getenv("COHERE_API_KEY"))

# 참고문헌 검색
references = await perplexity.search_references("AI research")

# 연구 계획 생성
plan = await cohere.generate_research_plan("AI project")
```
