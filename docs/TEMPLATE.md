# 월간 카드뉴스 템플릿 (확정: 2026-10-22)

기준 시안: `templates/card-qna-v2.dc.html` (C2 · Q&A + 원본 Figure)

## 카드 구성 (화제작 1편 = 6장)
| # | 질문 | 내용 |
|---|---|---|
| 1 | Q1 표지 | 질문형 제목 + 비유 그림 + 핵심 숫자 3개 + 서지 |
| 2–5 | Q2~Q5 | 카드마다 **원본 Figure 1장** + 패널 표시(a, b, c…) 해설 + 실제 수치 표 |
| 6 | 그래서, 우리 셀에는? | 실무 연결 3가지 + 한계 + 원문 버튼 + 라이선스 |

나머지 논문(필독)은 1~2장으로 압축한다.

## 디자인 규칙
- 배경 #DDE5E0, 카드 #F4F7F5, 강조색 #1E6B52, 둥근 모서리 24px
- 제목 Gowun Dodum, 본문 Noto Sans KR, 숫자 IBM Plex Mono
- 그림을 누르면 확대 (원본 그대로 표시)

## 데이터 규칙
- 수치는 본문 문장을 우선 사용. 그래프에서 읽은 값은 "근사치"라고 표시
- 한계(Limitations)는 반드시 1줄 이상

## Figure 라이선스 규칙
| 라이선스 | 처리 |
|---|---|
| CC BY | 원본 삽입, 출처 표기 (자르기 허용, 변경 사실 표시) |
| CC BY-NC | 원본 삽입, 비상업, 출처 표기 |
| CC BY-NC-ND | **원본 그대로만** (자르기·덧그리기 금지), 해설은 그림 밖 |
| 구독 논문 | 원본 그림 사용 안 함 → Claude가 다시 그린 개념도 + 원문 Figure 링크 |

## 저널별 접근 테스트 (2026-10-22)
| 출판사 | 테스트 논문 | 라이선스 | 그림 가져오기 |
|---|---|---|---|
| Nature (Springer) | Nature 658, 636 (2026) | CC BY-NC-ND | ✅ 1200px |
| Cell Press | Joule 2026 (SSB cell database) | CC BY | ✅ 656px |
| Science / AAAS | Science adv1739 (2025.11) | 구독 | ❌ 그림 미노출 |
| Science / AAAS | Science Advances aat5383 | CC BY-NC | ✅ 1050px |
| ACS | JACS Au 2026 (generative electrolyte) | CC BY-NC-ND | ✅ 520px (CDN 경유) |
| ACS | Chem. Mater. 2026 perspective | 구독 | ⚠ 그래픽 초록만 |
| Wiley | AEM / Batteries & Supercaps 2026 | 구독 | ⚠ 그래픽 초록만 (394px) · OA 논문은 미검증 |
- Wiley 사이트 검색은 봇 확인 화면이 떠서 사용 불가 → DOI로 직접 접속
