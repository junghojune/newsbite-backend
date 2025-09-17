# 기여 가이드

## 커밋 컨벤션 (Conventional Commits)

형식: `<type>(scope?): <subject>`

주요 타입:
- feat: 새로운 기능
- fix: 버그 수정
- docs: 문서 수정
- chore: 빌드/도구/잡 작업
- refactor: 리팩토링
- test: 테스트 추가/수정
- style: 포맷/스타일(동작 변경 없음)

예시:
- `feat(api): add /news/today endpoint`
- `fix(crawler): handle timeout error`

## 브랜치 전략
- main: 안정 배포용
- feature/*: 기능 개발 브랜치

## PR 가이드
- 작은 단위로 제출하고, 설명/체크리스트 작성
- 리뷰 반영 시 `fixup!` 커밋 후 스쿼시 머지 권장

