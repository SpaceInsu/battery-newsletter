"""카카오톡 우체부 스크립트 ('나에게 보내기' 기본, '친구에게 보내기' 스위치 지원).

흐름 (비유):
  1) 재발급권(refresh_token)으로 임시 출입증(access_token)을 새로 받는다.
  2) 사용자 정보 API를 한 번 호출해 연결을 유지한다.
  3) 뉴스레터 정보(issues/latest.json)를 피드 카드로 만들어 발송한다.

환경변수 (GitHub Secrets / Variables에서 주입):
  KAKAO_REST_KEY, KAKAO_CLIENT_SECRET, KAKAO_REFRESH_TOKEN
  KAKAO_SEND_TARGET   : "memo"(기본, 나와의 채팅) 또는 "friends"(다른 계정이 나에게 보냄)
  KAKAO_RECEIVER_UUIDS: friends 모드일 때 받는 사람 uuid (쉼표 구분)
    - friends 모드에서는 KAKAO_REFRESH_TOKEN이 "보내는 계정(B)"의 토큰이어야 한다.
    - uuid는 B 계정 토큰으로 --list-friends 를 실행하면 확인할 수 있다.

옵션:
  --issue PATH     발송할 뉴스레터 JSON (기본 issues/latest.json)
  --keepalive      메시지는 보내지 않고 토큰 갱신·연결 유지만 수행
  --test           간단한 테스트 문구 1통 발송

카카오가 새 refresh_token을 주면 new_refresh_token.txt 에 저장한다.
(워크플로가 이 파일을 보고 GitHub Secrets 값을 교체한다.)
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

TOKEN_URL = "https://kauth.kakao.com/oauth/token"
ME_URL = "https://kapi.kakao.com/v2/user/me"
SEND_URL = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
FRIEND_SEND_URL = "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
FRIENDS_URL = "https://kapi.kakao.com/v1/api/talk/friends"
NEW_TOKEN_FILE = "new_refresh_token.txt"


def post(url, data, headers=None):
    body = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded;charset=utf-8")
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    return _open(req)


def get(url, headers):
    req = urllib.request.Request(url, method="GET")
    for k, v in headers.items():
        req.add_header(k, v)
    return _open(req)


def _open(req):
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        # 오류 원인(KOE 코드 등)이 로그에 보이도록 본문을 출력한다. 토큰 값은 포함되지 않는다.
        sys.exit(f"[카카오 오류] HTTP {e.code} {req.full_url}\n{detail}")


def refresh_access_token():
    data = {
        "grant_type": "refresh_token",
        "client_id": os.environ["KAKAO_REST_KEY"],
        "refresh_token": os.environ["KAKAO_REFRESH_TOKEN"],
    }
    secret = os.environ.get("KAKAO_CLIENT_SECRET", "").strip()
    if secret:
        data["client_secret"] = secret
    res = post(TOKEN_URL, data)

    new_rt = res.get("refresh_token")
    if new_rt:
        with open(NEW_TOKEN_FILE, "w", encoding="utf-8") as f:
            f.write(new_rt)
        print("새 refresh_token을 받았습니다 → Secrets 교체 대상")
    else:
        print("refresh_token은 아직 유효 기간이 넉넉해 교체 불필요")
    return res["access_token"]


def keep_alive(access_token):
    get(ME_URL, {"Authorization": f"Bearer {access_token}"})
    print("사용자 정보 API 호출 완료 (연결 유지)")


def send(access_token, template):
    target = os.environ.get("KAKAO_SEND_TARGET", "memo").strip() or "memo"
    auth = {"Authorization": f"Bearer {access_token}"}
    body = {"template_object": json.dumps(template, ensure_ascii=False)}

    if target == "friends":
        uuids = [u.strip() for u in os.environ.get("KAKAO_RECEIVER_UUIDS", "").split(",") if u.strip()]
        if not uuids:
            sys.exit("[설정 오류] friends 모드인데 KAKAO_RECEIVER_UUIDS가 비어 있습니다.")
        body["receiver_uuids"] = json.dumps(uuids)
        res = post(FRIEND_SEND_URL, body, auth)
        ok = res.get("successful_receiver_uuids", [])
        if len(ok) != len(uuids):
            sys.exit(f"[일부/전체 발송 실패] {res}")
        print(f"카카오톡 친구 발송 완료 ✅ ({len(ok)}명)")
        return

    res = post(SEND_URL, body, auth)
    if res.get("result_code") != 0:
        sys.exit(f"[발송 실패] {res}")
    print("카카오톡 발송 완료 ✅ (나와의 채팅)")


def list_friends(access_token):
    """friends 모드 준비용: 보내는 계정의 친구 목록(이름·uuid) 출력."""
    res = get(FRIENDS_URL, {"Authorization": f"Bearer {access_token}"})
    for f in res.get("elements", []):
        print(f"{f.get('profile_nickname', '?')}\t{f.get('uuid')}")
    if not res.get("elements"):
        print("친구 목록이 비어 있습니다. (동의항목 friends, 앱 팀원 등록, 카톡 친구 여부 확인)")


def feed_template(issue):
    """뉴스레터 JSON → 카카오 피드 카드(제목 + 썸네일 + 버튼)."""
    url = issue["url"]
    link = {"web_url": url, "mobile_web_url": url}
    content = {
        "title": issue["title"][:200],
        "description": issue.get("description", "")[:200],
        "link": link,
    }
    if issue.get("image_url"):
        content["image_url"] = issue["image_url"]
    return {
        "object_type": "feed",
        "content": content,
        "buttons": [{"title": issue.get("button", "뉴스레터 열기")[:14], "link": link}],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--issue", default="issues/latest.json")
    p.add_argument("--keepalive", action="store_true")
    p.add_argument("--test", action="store_true")
    p.add_argument("--list-friends", action="store_true")
    args = p.parse_args()

    token = refresh_access_token()
    keep_alive(token)

    if args.keepalive:
        return
    if args.list_friends:
        list_friends(token)
        return
    if args.test:
        send(token, {
            "object_type": "text",
            "text": "🔋 GitHub 우체부 테스트 성공!\n매월 논문 뉴스레터가 이 방으로 배달됩니다.",
            "link": {"web_url": "https://github.com", "mobile_web_url": "https://github.com"},
        })
        return

    with open(args.issue, encoding="utf-8") as f:
        issue = json.load(f)
    send(token, feed_template(issue))


if __name__ == "__main__":
    main()
