# battery-newsletter
BPM (Battery Paper Manager) — 월간 배터리 논문 뉴스레터를 카카오톡 "나에게 보내기"로 배달합니다.

## 구조 (비유)
| 파일 | 역할 |
|---|---|
| `issues/latest.json` | 우체통. Claude가 매달 새 호 정보를 넣으면 발송이 시작됨 |
| `scripts/send_kakao.py` | 우체부. 토큰 갱신 → 연결 유지 → 카톡 피드 카드 발송 |
| `.github/workflows/send-newsletter.yml` | 근무표. 언제 우체부가 출근할지 |
| `docs/PLAN.md` | 전체 계획 |
| `docs/KAKAO_API_SETUP.md` | 카카오 API 설정 기록 |

## 필요한 Secrets
- `KAKAO_REST_KEY`, `KAKAO_CLIENT_SECRET`, `KAKAO_REFRESH_TOKEN` (필수)
- `GH_PAT` (선택) — 카카오가 새 refresh_token을 주면 자동으로 교체하는 데 사용

## 수동 테스트
Actions 탭 → **Kakao newsletter** → Run workflow → mode = `test`

## 뉴스레터 JSON 형식
`issues/example.json` 참고 (`title`, `description`, `url`, `image_url`, `button`).
