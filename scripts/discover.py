#!/usr/bin/env python3
"""후보 논문 찾기 (Fetch papers 워크플로의 discover 모드에서 실행).

GitHub 서버(인터넷이 열려 있음)에서 돌아가므로, Claude 쪽에서 웹 페이지를 열 필요가 없다.
  1) Crossref: 화이트리스트 저널(+Nature Communications)의 최근 N일 논문 목록 → 제목 키워드로 배터리 분야만
  2) Europe PMC: DOI별 오픈액세스 여부·PMCID·라이선스
  3) Altmetric(무료 공개 API): 화제성 점수 (실패해도 계속)
  4) issues/history.json 에 있는 DOI는 제외
결과: out/discover/candidates.json, candidates.md
사용: python3 scripts/discover.py [일수=14]
"""
import json, re, sys, time, urllib.parse, urllib.request, datetime, pathlib

DAYS = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 14
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = pathlib.Path("out/discover"); OUT.mkdir(parents=True, exist_ok=True)
UA = "BatteryNewsletter/1.0 (https://github.com/SpaceInsu/battery-newsletter; mailto:noreply@users.noreply.github.com)"
SINCE = (datetime.date.today() - datetime.timedelta(days=DAYS)).isoformat()

# 분야 키워드(제목 기준). 너무 넓은 'battery' 하나만 쓰면 놓치는 글이 있어 몇 개를 함께 쓴다.
KEY = re.compile(r"batter|lithium|\bli[- ]?ion|\bli\b|sodium[- ]ion|\bna[- ]ion|potassium[- ]ion|zinc[- ]ion|"
                 r"electrolyte|cathode|anode|solid[- ]state|interphase|\bsei\b|\bcei\b|dendrite|"
                 r"li metal|lithium metal|anode[- ]free|sulfide|argyrodite|halide|garnet|llzo|"
                 r"nickel[- ]rich|layered oxide|lfp|lifepo|silicon anode|li[- ]s\b|lithium[- ]sulfur|"
                 r"electrode|intercalation|cycling|fast[- ]charg", re.I)
EXCLUDE = re.compile(r"\b(correction|erratum|retraction|author correction|publisher correction)\b", re.I)


def get(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as e:  # 잠깐 쉬고 재시도
            if i == tries - 1:
                print(f"  ! {url[:90]} → {e}")
                return None
            time.sleep(3 * (i + 1))


def issn_for(name):
    """저널 이름 → Crossref ISSN 목록 (이름이 정확히 같은 것 우선)."""
    j = get("https://api.crossref.org/journals?rows=20&query=" + urllib.parse.quote(name))
    items = (j or {}).get("message", {}).get("items", [])
    norm = lambda s: re.sub(r"[^a-z]", "", s.lower().replace("&", "and"))
    for it in items:
        if norm(it.get("title", "")) == norm(name):
            return it.get("ISSN", [])
    return items[0].get("ISSN", []) if items else []


def works(issns):
    out, cursor = [], "*"
    filt = ",".join([f"issn:{i}" for i in issns] + [f"from-pub-date:{SINCE}", "type:journal-article"])
    while cursor and len(out) < 3000:
        j = get("https://api.crossref.org/works?rows=500&select=DOI,title,container-title,published,license,author,is-referenced-by-count"
                f"&filter={filt}&cursor={urllib.parse.quote(cursor)}")
        m = (j or {}).get("message", {})
        items = m.get("items", [])
        out += items
        cursor = m.get("next-cursor") if len(items) == 500 else None
    return out


def epmc(dois):
    """DOI 묶음 → {doi: {pmcid, oa, license}}"""
    res = {}
    for k in range(0, len(dois), 40):
        q = " OR ".join(f'DOI:"{d}"' for d in dois[k:k + 40])
        j = get("https://www.ebi.ac.uk/europepmc/webservices/rest/search?format=json&resultType=core&pageSize=100&query="
                + urllib.parse.quote(q))
        for r in (j or {}).get("resultList", {}).get("result", []):
            d = (r.get("doi") or "").lower()
            if d:
                res[d] = {"pmcid": r.get("pmcid"), "oa": r.get("isOpenAccess") == "Y", "license": r.get("license")}
    return res


def altmetric(doi):
    j = get("https://api.altmetric.com/v1/doi/" + doi, tries=1)
    return round(j.get("score", 0), 1) if j else 0


def main():
    cfg = json.loads((ROOT / "config/journals.json").read_text())
    names = [x["name"] for x in cfg["journals"]] + ["Nature Communications"]
    pub = {x["name"]: x["publisher"] for x in cfg["journals"]}; pub["Nature Communications"] = "Springer Nature"
    seen = {(h.get("doi") or "").lower() for h in json.loads((ROOT / "issues/history.json").read_text())}

    cands = []
    for name in names:
        issns = issn_for(name)
        if not issns:
            print(f"- {name}: ISSN 못 찾음"); continue
        ws = works(issns)
        keep = 0
        for w in ws:
            title = " ".join(w.get("title") or [""]).strip()
            doi = w.get("DOI", "").lower()
            if not title or doi in seen or EXCLUDE.search(title) or not KEY.search(title):
                continue
            lic = [l.get("URL", "") for l in w.get("license", [])]
            date = "-".join(str(x) for x in (w.get("published", {}).get("date-parts", [[None]])[0] or []) if x)
            au = w.get("author") or []
            cands.append({"doi": doi, "title": re.sub(r"<[^>]+>", "", title), "journal": name, "publisher": pub[name],
                          "date": date, "first_author": (au[0].get("family") if au else ""),
                          "last_author": (au[-1].get("family") if au else ""),
                          "cc_license": next((u for u in lic if "creativecommons" in u), None)})
            keep += 1
        print(f"- {name}: {len(ws)}편 중 분야 후보 {keep}편")

    info = epmc([c["doi"] for c in cands])
    for c in cands:
        e = info.get(c["doi"], {})
        c["pmcid"] = e.get("pmcid"); c["epmc_license"] = e.get("license")
        c["open_access"] = bool(c["cc_license"] or e.get("oa"))
        c["altmetric"] = altmetric(c["doi"])
        # 다음 단계(Fetch papers)에 넣을 값: Nature는 기사 ID, 나머지는 DOI
        m = re.match(r"10\.1038/(s\d{5}-\d{3}-\d{5}-\w)", c["doi"])
        c["fetch_id"] = m.group(1) if m else c["doi"]
        time.sleep(0.2)
    cands.sort(key=lambda c: (-c["altmetric"], c["journal"]))

    (OUT / "candidates.json").write_text(json.dumps({"since": SINCE, "days": DAYS, "count": len(cands),
                                                     "candidates": cands}, ensure_ascii=False, indent=1))
    lines = [f"# 후보 논문 ({SINCE} 이후 {DAYS}일, {len(cands)}편) — Altmetric 높은 순",
             "", "| # | Altm. | 저널 | 날짜 | OA | PMCID | 제목 | fetch_id |", "|---|---|---|---|---|---|---|---|"]
    for i, c in enumerate(cands, 1):
        lines.append(f"| {i} | {c['altmetric']} | {c['journal']} | {c['date']} | {'OA' if c['open_access'] else '구독'} | "
                     f"{c['pmcid'] or ''} | {c['title'][:110].replace('|', '/')} | {c['fetch_id']} |")
    (OUT / "candidates.md").write_text("\n".join(lines) + "\n")
    print(f"총 후보 {len(cands)}편 → {OUT}/candidates.md")


if __name__ == "__main__":
    main()
