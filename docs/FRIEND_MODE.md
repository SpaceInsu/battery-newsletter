# 친구 계정(B)에게서 받기 — 나중에 켜는 스위치

지금은 **나와의 채팅**(memo 모드)으로 받습니다. 아래를 마치면 "🔋 배터리 위클리" 같은 다른 계정(B)이 Insu 계정으로 1:1 카톡을 보내는 방식(friends 모드)으로 바뀝니다. 코드는 이미 준비되어 있어 **설정만** 하면 됩니다.

## 준비물
1. 두 번째 카카오톡 계정 B (두 번째 전화번호 필요)
2. B와 Insu 본 계정이 **서로 카톡 친구**

## Kakao Developers 설정
1. [앱] > [멤버(팀원)]에 **B 계정과 Insu 계정을 팀원으로 추가** — 심사 없이 개인용으로 쓰기 위한 조건
2. [카카오 로그인] > [동의항목]에서 **카카오톡 친구 목록(friends)** 을 선택 동의로 켜기 (talk_message는 이미 켜져 있음)

## 토큰 발급
1. **B 계정**으로 아래 주소에 로그인 (`REST키` 교체)
   `https://kauth.kakao.com/oauth/authorize?client_id=REST키&redirect_uri=https://example.com/oauth&response_type=code&scope=talk_message,friends`
2. `KAKAO_API_SETUP.md` 3번 PowerShell 명령으로 토큰 교환 → B의 refresh_token 확보
3. **Insu 계정**도 같은 주소로 한 번 로그인해 friends·talk_message에 동의 (받는 쪽도 앱 사용자여야 함)

## GitHub 설정 (battery-newsletter 저장소)
1. Secrets: `KAKAO_SENDER_REFRESH_TOKEN` = B의 refresh_token
2. Variables: `KAKAO_SEND_TARGET` = `friends`
3. Actions → Kakao newsletter → Run workflow → **list-friends** 실행 → 로그에서 Insu 계정의 uuid 확인
4. Variables: `KAKAO_RECEIVER_UUIDS` = 확인한 uuid
5. Run workflow → **test** 로 발송 확인

## 되돌리기
Variables의 `KAKAO_SEND_TARGET`을 지우거나 `memo`로 바꾸면 다시 나와의 채팅으로 받습니다.

## 제약
- 친구 메시지 API는 "서비스 이용자끼리"의 용도라 정식 심사는 통과가 어려울 수 있음 → 팀원끼리 쓰는 개인용으로 운영
- 일일 발송 한도 있음 (주 1회 발송에는 영향 없음)
