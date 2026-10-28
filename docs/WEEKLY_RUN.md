# 매주 금요일 자동 발행 절차 (예약 실행용)

예약된 Claude 세션이 매주 금요일 이 문서를 읽고 **사람 확인 없이** 끝까지 진행한다.
독자: Insu (LG에너지솔루션 전고체 R&D, 배터리공학 박사급). 결과물은 카카오톡 "나와의 채팅"으로 도착하는 카드 1장 + 웹 페이지.

## 0. 준비
1. 저장소 `SpaceInsu/battery-newsletter`를 clone (없으면 add_repo, access=push 후 clone). 이후 모든 경로는 저장소 기준.
2. 먼저 읽기: `docs/TEMPLATE.md`(카드 구성·설명 수준·라이선스·인용 규칙), `config/journals.json`(저널 화이트리스트), `issues/history.json`(이미 다룬 DOI), `site/issue-02/index.html`(최신 형식 견본).
3. 이번 호 번호 = history.json의 최대 issue + 1. 날짜 = 실행일(KST, YYYY.MM.DD).

## 1. 논문 고르기 (3편: 화제작 1 + 필독 2)
- 분야: 전고체전지(최우선) · Si-흑연/Si-C 음극 · Li 금속 전해질/SEI · Na 전해질 · ML 기반 LIB 수명 예측
- 범위: 최근 약 14일 안에 온라인 공개된 논문. `config/journals.json` 저널, 또는 그 밖의 오픈액세스 논문
- 제외: history.json에 있는 DOI
- 수준: 메커니즘·새 분석법·셀 레벨 실증 등 박사급 독자가 "몰랐던 것"을 얻는 논문. 단순 소재 성능 나열형은 피함
- 그림을 넣을 수 있는 **오픈액세스 우선**(Nature Communications, Science Advances, Advanced Science, Nature 계열 OA 등)
- 화제작 = 조회수·주목도가 가장 높은 1편(Nature 계열은 페이지의 Accesses 수 사용)
- 1·2주 안에 적당한 논문이 3편이 안 되면 2편으로 발행 (억지로 채우지 않음)

## 2. 원문·그림 가져오기
작업 공간에서 출판사 사이트가 막히는 경우가 많다. 순서대로 시도:
1. **Nature 계열**: `gh api -X POST repos/SpaceInsu/battery-newsletter/actions/workflows/fetch-papers.yml/dispatches -f ref=main -f 'inputs[ids]=<ID1>,<ID2>'` (ID = s41467-… 형태). 실행 완료 후 `git clone --depth 1 -b fetch/<run_id> …`로 받는다. 받은 뒤 `inputs[ids]=cleanup`으로 한 번 더 실행해 임시 브랜치 삭제.
2. 그 밖의 출판사: WebFetch로 논문 페이지를 직접 읽기(Wiley는 DOI 주소로 직접, Cell Press·AAAS는 기사 페이지). PDF나 그림 주소를 찾으면 fetch-papers에 **URL 그대로** 넣어 받을 수 있다(Wiley·ACS는 GitHub 서버도 차단됨 → WebFetch 텍스트로 진행).
3. Article in Press(웹에 그림 없음): PDF를 `pdftoppm -r 300`으로 렌더링해 **Figure 전체**를 잘라 사용.
4. 원문을 끝내 못 읽은 논문은 쓰지 않는다(초록만으로 카드 작성 금지) → 다른 후보로 교체.

## 3. 페이지 만들기
- `site/issue-NN/index.html`: `site/issue-02/index.html`을 복사해 머리말(title·og·description), 표지, 논문 섹션, 푸터, `var ISSUE='Battery Newsletter No.NN'`을 바꾼다. 스타일·스와이프·확대·질문 버튼 스크립트는 그대로.
- 카드 구성·설명 수준·"이 그림 읽는 법"·수치표·해석·결론("우리 셀에는?" + 한계 + 원문 버튼)은 TEMPLATE.md 그대로. 기본 정의(Nyquist, dQ/dV, CE, ICE, n/p 등)는 설명하지 않는다.
- 그림 라이선스: CC BY(자르기 허용, 변경 표시) / CC BY-NC-ND(원본 그대로, Figure 단위) / 구독 논문은 인용 규칙(논문당 최대 2개, 캡션에 `인용(저작권법 제28조)`).
- 그림은 `site/issue-NN/img/`에 1400px 폭 JPG. 카카오 썸네일 `thumb.jpg` = 화제작 대표 Figure 전체를 1200×600 흰 바탕 가운데 배치(자르지 않음).
- `site/index.html`: 새 호로 리다이렉트하고 목록 맨 위에 추가.
- `issues/history.json`: 이번 호 논문을 status "draft"로 추가(issue, date, slot, field, doi, title, license).

## 4. 검증 (보내기 전 필수)
- 모든 수치를 원문 텍스트와 대조. 그래프에서 읽은 값은 "근사치" 표기. 원문끼리 다른 값은 카드에 그대로 적기
- Playwright(`/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`, 375×740)로 열어 카드 수, 깨진 이미지, 가로 넘침, 콘솔 오류를 확인하고 표지·그림 카드 몇 장을 캡처해 직접 본다

## 5. 게시 → 발송
1. `site/`, `issues/history.json`을 커밋·푸시 → "Kakaotalk Battery Newsletter" 워크플로가 페이지만 게시. 성공(초록) 확인
2. `issues/latest.json`을 새 호로 덮어쓰기:
   `{"title": "🔋 Battery Newsletter No.NN (YYYY.MM.DD)", "description": "① … ② … ③ …"(200자 이내), "url": "https://spaceinsu.github.io/battery-newsletter/issue-NN/", "image_url": ".../issue-NN/img/thumb.jpg", "button": "NN호 읽기"}`
3. history.json의 이번 호 status를 "sent"로 바꿔 함께 커밋 "Issue NN: send" → 푸시 → 워크플로가 게시 후 카톡 발송
4. 실행이 decide·publish·deliver 모두 success인지 확인. 실패하면 로그를 보고 고칠 수 있는 것만 고쳐 한 번 재시도. 그래도 실패하면 세션 마지막 메시지에 원인을 남긴다
- 커밋 메시지 끝에는 세션이 안내하는 attribution 줄을 붙인다
- GraphQL은 막혀 있으므로 `gh` 대신 `gh api repos/...` REST만 사용
