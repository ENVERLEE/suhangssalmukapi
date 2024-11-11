# Research Platform API Reference

## Overview

이 API는 연구 프로젝트 관리 및 참고 문헌 검색을 위한 엔드포인트를 제공합니다. 모든 API 요청은 인증이 필요하며, Bearer 토큰을 통해 인증됩니다.

## Base URL
```
https://api.example.com/api
```

## Authentication

### Register New User
```http
POST /register
```

새로운 사용자 계정을 생성합니다.

#### Request Body
| Field | Type | Description |
|-------|------|-------------|
| email | string | 사용자의 이메일 주소 |
| password | string | 사용자 비밀번호 |
| full_name | string | 사용자의 실명 |

#### Response
```json
{
    "access_token": "string",
    "token_type": "bearer"
}
```

### Login
```http
POST /token
```

기존 사용자 로그인을 위한 엔드포인트입니다.

#### Request Body
| Field | Type | Description |
|-------|------|-------------|
| username | string | 사용자 이메일 |
| password | string | 사용자 비밀번호 |

#### Response
```json
{
    "access_token": "string",
    "token_type": "bearer"
}
```

## Projects

### Create Project
```http
POST /projects/
```

새로운 연구 프로젝트를 생성합니다.

#### Request Body
| Field | Type | Description |
|-------|------|-------------|
| title | string | 프로젝트 제목 |
| description | string | 프로젝트 설명 |
| evaluation_plan | string | 평가 계획 |
| submission_format | string | 제출 형식 |
| metadata1 | object | 추가 메타데이터 (선택사항) |

#### Response
```json
{
    "id": 0,
    "title": "string",
    "description": "string",
    "created_at": "string",
    "status": "string"
}
```

### List Projects
```http
GET /projects/
```

현재 사용자의 모든 프로젝트를 조회합니다.

#### Response
```json
[
    {
        "id": 0,
        "title": "string",
        "description": "string",
        "created_at": "string",
        "status": "string"
    }
]
```

### Execute Project Step
```http
POST /projects/{project_id}/steps/{step_number}/execute
```

프로젝트의 특정 단계를 실행합니다.

#### Path Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| project_id | integer | 프로젝트 ID |
| step_number | integer | 실행할 단계 번호 |

## References

### Search References
```http
POST /references/search?project_id={project_id}
```

키워드를 기반으로 참고 문헌을 검색합니다.

#### Query Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| project_id | integer | 프로젝트 ID |

#### Request Body
| Field | Type | Description |
|-------|------|-------------|
| keywords | array[string] | 검색 키워드 목록 |

#### Response
```json
[
    {
        "id": 0,
        "title": "string",
        "authors": ["string"],
        "publication_date": "string",
        "content": "string",
        "metadata1": {}
    }
]
```

### Get Reference Summary
```http
GET /references/{reference_id}/summary
```

특정 참고 문헌의 요약을 조회합니다.

#### Path Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| reference_id | integer | 참고 문헌 ID |

## 오류 응답

이 API는 다음과 같은 HTTP 상태 코드를 반환할 수 있습니다:

| Status Code | Description |
|------------|-------------|
| 200 | 요청 성공 |
| 400 | 잘못된 요청 (예: 이미 등록된 이메일) |
| 401 | 인증 실패 |
| 404 | 리소스를 찾을 수 없음 |
| 500 | 서버 내부 오류 |

## Rate Limiting

모든 API 엔드포인트는 rate limiting이 적용됩니다:
- 인증된 사용자: 분당 100 요청
- 미인증 사용자: 분당 10 요청

## Security

- 모든 API 통신은 HTTPS를 통해 이루어집니다.
- 액세스 토큰은 발급 후 일정 시간이 지나면 만료됩니다.
- 민감한 데이터는 전송 시 항상 암호화됩니다.