# 주간 카드뉴스 템플릿 (확정: 2026-10-22)

기준 시안: `templates/card-qna-v2.dc.html` (C2 · Q&A + 원본 Figure)

## 한 호 구성 (주 3편)
- 화제작 1편 = 카드 6장 (아래 구성)
- 필독 2편 = 각 4~5장, 순서 고정 (2026-10-22 개정: "그림만 있어 이해 어려움" 피드백)
  1. **배경** — 왜 이 문제가 중요한가, 무엇이 병목인가, 기존 해법의 한계 (개념도 포함)
  2. **아이디어** — 이 논문의 해법과 작동 원리 (단계별 + 비유)
  3~4. **그림 카드** — 원본 Figure + "이 그림 읽는 법"(축·색·비교 포인트) + 수치표 + 해석
  5. **결론** — 논리 정리 한 줄 + 읽을 때 주의(한계) + 우리 셀에는?

## 화제작 카드 구성 (6장)
| # | 질문 | 내용 |
|---|---|---|
| 1 | Q1 표지 | 질문형 제목 + 비유 그림 + 핵심 숫자 3개 + 서지 |
| 2–5 | Q2~Q5 | 카드마다 **원본 Figure 1장** + 패널 표시(a, b, c…) 해설 + 실제 수치 표 |
| 6 | 그래서, 우리 셀에는? | 실무 연결 3가지 + 한계 + 원문 버튼 + 라이선스 |


## 디자인 규칙
- 배경 #DDE5E0, 카드 #F4F7F5, 강조색 #1E6B52, 둥근 모서리 24px
- 제목 Gowun Dodum, 본문 Noto Sans KR, 숫자 IBM Plex Mono
- 그림을 누르면 확대 (원본 그대로 표시)

## 설명 수준 (Insu 피드백 2026-10-23)
- 독자는 배터리 박사급: Nyquist plot, dQ/dV, CE, ICE, n/p 같은 **기본 정의는 생략**
- 설명은 **논문 고유·고급 개념**에 집중 (예: redox mediation, 과리튬화 계산, NMR 피크 귀속, MLFF 등)

## 데이터 규칙
- 수치는 본문 문장을 우선 사용. 그래프에서 읽은 값은 "근사치"라고 표시
- 한계(Limitations)는 반드시 1줄 이상

## Figure 라이선스 규칙
| 라이선스 | 처리 |
|---|---|
| CC BY | 원본 삽입, 출처 표기 (자르기 허용, 변경 사실 표시) |
| CC BY-NC | 원본 삽입, 비상업, 출처 표기 |
| CC BY-NC-ND | **원본 그대로만** (자르기·덧그리기 금지), 해설은 그림 밖 |
| 구독 논문 | **인용형(A안)** — 아래 "구독 논문 인용 규칙" 적용 |

## 구독 논문 인용 규칙 (A안 확정: 2026-10-28)
근거: 저작권법 제28조(공표된 저작물의 인용) — 비평·연구 목적, 정당한 범위, 공정한 관행. 법률 자문 아님, 운영 판단은 Insu.
비유: **해설이 주인공, 그림은 증거 사진 한 장.**

| 항목 | 규칙 |
|---|---|
| 그림 수 | 논문당 **최대 2개** (화제작도 동일). 나머지 결과는 수치표·직접 그린 도식으로 |
| 주종관계 | 그림 카드마다 "이 그림 읽는 법" + 수치표 + 해석이 그림보다 분량이 많아야 함 |
| 변형 | 원본 그대로. 패널 일부만 쓸 때는 캡션에 "Fig. 3b 발췌"로 표기, 덧그리기 금지 |
| 출처 표기 | 캡션: `Fig. N · 저자 et al., 저널 (연도) · DOI · 인용(저작권법 제28조)` |
| 원문 버튼 | 결론 카드에 DOI 링크 "원문 읽기 (구독)" |
| 그림 원본 | 출판사 논문 페이지·PDF(회사 구독으로 열람)에서 가져옴. 구글 이미지 등 2차 출처 사용 안 함 |
| 가져오는 방법 | 공개 페이지에 그림이 보이면 Claude가 직접 / 안 보이면 Insu가 PDF 또는 그림 파일을 업로드 |
| 삭제 요청 | 저자·출판사 요청이 오면 즉시 해당 그림 내리고 도식으로 교체 |

## 대상 저널 (화이트리스트, 2026-10-28)
목록 원본: `config/journals.json` — 후보는 이 저널 + 오픈액세스 논문에서만 선정.
Nature · Science · Nature Energy · Nature Materials · Joule · Nature Nanotechnology · Energy & Environmental Science · Advanced Materials · Advanced Energy Materials · Nature Sustainability · Chem · ACS Energy Letters · Nature Chemistry · Advanced Functional Materials · Matter · ACS Nano · Angewandte Chemie International Edition · Advanced Science · Journal of the American Chemical Society · Science Advances · Small · ACS Materials Letters · PNAS · Chemistry of Materials

## 저널별 접근 테스트 (2026-10-22)
| 출판사 | 테스트 논문 | 라이선스 | 그림 가져오기 |
|---|---|---|---|
| Nature (Springer) | Nature 658, 636 (2026) | CC BY-NC-ND | ✅ 1200px |
| Cell Press | Joule 2026 (SSB cell database) | CC BY | ✅ 656px |
| Science / AAAS | Science adv1739 (2025.11) | 구독 | ❌ 그림 미노출 |
| Science / AAAS | Science Advances aat5383 | CC BY-NC | ✅ 1050px |
| ACS | JACS Au 2026 (generative electrolyte) | CC BY-NC-ND | ✅ 520px (CDN 경유) |
| ACS | Chem. Mater. 2026 perspective | 구독 | ⚠ 그래픽 초록만 |
| Wiley | AEM / Batteries & Supercaps 2026 | 구독 | ⚠ 그래픽 초록만 (394px) |
| Wiley | Batteries & Supercaps batt.70409 (OA) | CC BY | ✅ 892–1096px |
- Wiley 사이트 검색은 봇 확인 화면이 떠서 사용 불가 → DOI로 직접 접속

## 운영 메모
- Nature 계열은 페이지에 조회수(Accesses)가 표시됨 → 표지에 "조회" 수로 활용
- Nature Communications "Article in Press"는 HTML에 그림이 없음 → PDF에서 Figure 전체를 잘라 사용 (ND 라이선스: Figure 단위로 통째로만)

## 웹 페이지 형식 (2026-10-26 추가)
- 카드 한 장 = 화면 한 장, 좌우 스와이프로 넘김 (표지 → 논문별 배경·아이디어·결과·결론 카드)
- HTML은 기존처럼 `section.paper` 안에 `.card` / `.so`를 순서대로 쓰면 되고, 페이지 하단 스크립트가 자동으로 카드 덱으로 재배치
- 하단 "💬 이 카드 Claude에게 질문" 버튼: 논문 제목·출처·원문 링크·보고 있던 카드를 채운 채 claude.ai 새 대화를 엶
