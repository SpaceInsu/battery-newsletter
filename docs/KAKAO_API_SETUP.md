# 카카오톡 "나에게 보내기" API 설정 기록 (STEP 1)

> 완료일: 2026-10-22 · 결과: "나와의 채팅"에 테스트 메시지 수신 ✅
> 비유: **번호표(인가 코드)를 뽑아서 → 창구에서 출입증(토큰)으로 교환 → 시험 편지 1통 발송**

---

## 1. Kakao Developers 앱 설정

| 항목 | 위치 | 설정값 |
|---|---|---|
| 앱 생성 | [내 애플리케이션] → [애플리케이션 추가하기] | 앱 이름은 카톡 메시지 하단에 출처로 표시됨 |
| REST API 키 | [앱] > [일반] > [플랫폼 키] | 값은 GitHub Secrets에만 보관 |
| Redirect URI | [플랫폼 키] → REST API 키 상세 | **`https://example.com/oauth`** |
| 카카오 로그인 | [카카오 로그인] → 활성화 설정 | ON |
| 동의항목 | [카카오 로그인] > [동의항목] | 카카오톡 메시지 전송(talk_message) = 선택 동의 |
| 클라이언트 시크릿 | [플랫폼 키] → REST API 키 상세 → 아래쪽 | **"카카오 로그인"용 코드 사용, 상태 ON** ("비즈니스 인증"용 아님) |

---

## 2. 번호표(인가 코드) 받기

브라우저 주소창에 입력합니다. `REST키` 부분만 교체하세요.

```
https://kauth.kakao.com/oauth/authorize?client_id=REST키&redirect_uri=https://example.com/oauth&response_type=code&scope=talk_message
```

- 동의 후 "Example Domain" 페이지가 열립니다.
- 주소창의 `?code=` 뒤 값이 인가 코드입니다. `&`가 있으면 그 앞까지만 복사하세요.
- ⏱ **약 10분 안에, 1회만** 사용할 수 있습니다.

---

## 3. 출입증(토큰) 교환 + 테스트 메시지 (Windows PowerShell)

따옴표는 남겨두고 `REST키` / `시크릿` / `인가코드` 안의 글자만 교체합니다. 값 앞뒤에 공백이 들어가지 않게 주의하세요.

```powershell
try {
  $t = Invoke-RestMethod -Method Post -Uri "https://kauth.kakao.com/oauth/token" -Body @{grant_type="authorization_code"; client_id="REST키"; client_secret="시크릿"; redirect_uri="https://example.com/oauth"; code="인가코드"}
  $t | Format-List
  $tpl = '{"object_type":"text","text":"Newsletter test OK","link":{"web_url":"https://developers.kakao.com"}}'
  Invoke-RestMethod -Method Post -Uri "https://kapi.kakao.com/v2/api/talk/memo/default/send" -Headers @{Authorization="Bearer $($t.access_token)"} -Body @{template_object=$tpl}
} catch { $_.ErrorDetails.Message }
```

- 출력된 `refresh_token` → GitHub Secrets `KAKAO_REFRESH_TOKEN`에 저장한 뒤 메모장에서 삭제
- 메시지 본문을 한글로 쓰면 PowerShell에서 글자가 깨질 수 있어 테스트는 영문으로 진행

### 토큰 재발급 (refresh)
```powershell
Invoke-RestMethod -Method Post -Uri "https://kauth.kakao.com/oauth/token" -Body @{grant_type="refresh_token"; client_id="REST키"; client_secret="시크릿"; refresh_token="리프레시토큰"}
```
- 만료 1개월 이내에 재발급하면 응답에 **새 refresh_token**이 함께 옵니다. 이 경우 Secrets 값을 교체해야 합니다.

---

## 4. 토큰 수명 (열쇠 비유)

| 토큰 | 비유 | 유효기간 |
|---|---|---|
| access_token | 임시 출입증 | 약 6시간 |
| refresh_token | 출입증 재발급권 | 약 60일 |

- 장기간 미사용 시 연결이 끊길 수 있으므로 **월 1회 이상 재발급 + 사용자 정보 API 호출**을 권장합니다.

---

## 5. 겪었던 문제와 해결

| 증상 | 원인 | 해결 |
|---|---|---|
| 동의 후 화면에 반응이 없음 | Redirect가 `https://localhost`로 가는데 그 주소에서 응답하는 프로그램이 없음 | Redirect URI를 `https://example.com/oauth`로 변경 |
| `(401) 권한이 없음` | 클라이언트 시크릿이 ON인데 요청에 `client_secret`이 빠짐 | "카카오 로그인"용 시크릿을 추가 |
| 오류 원인이 안 보임 | PowerShell 기본 출력이 응답 본문을 숨김 | `try { ... } catch { $_.ErrorDetails.Message }`로 감싸서 KOE 코드 확인 |

---

## 6. 보안 규칙
- REST 키, 시크릿, 토큰은 **채팅에 붙여넣지 않는다.** 저장은 GitHub Secrets에만 한다.
- GitHub Secrets 이름: `KAKAO_REST_KEY`, `KAKAO_CLIENT_SECRET`, `KAKAO_REFRESH_TOKEN`

## 참고
- [Kakao Developers – 카카오톡 메시지 REST API](https://developers.kakao.com/docs/latest/ko/message/rest-api)
