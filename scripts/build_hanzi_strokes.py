#!/usr/bin/env python3
"""한자 획순 쓰기 드릴 데이터(drills/중국어_한자_쓰기.json)를 만든다.

- 획 데이터: makemeahanzi graphics.txt (Arphic Public License)
- 뜻·병음:   makemeahanzi dictionary.txt (LGPL v3+, Unihan/CJKlib 파생)
- 한글 훈음: 위키낱말사전 {{한자풀이}} 틀 (CC BY-SA 4.0), 음만 있을 땐 Unihan kHangul

대상 글자는 우리가 실제로 다룬 것만 — notes/중국어/*.md, sheets/중국어/*.html,
drills/중국어_HSK_어휘.json 에 등장한 한자의 합집합.

graphics.txt의 `strokes`는 채워 그리는 외곽선이라 획의 시작점·방향을 뽑을 수 없다.
드릴 채점기는 중심선을 요구하므로 `medians`(획 중심선 좌표열)를 폴리라인 path로 바꿔 쓴다.
좌표계도 다르다 — makemeahanzi는 Y축이 위로 향하고 기준선이 900이므로 y' = 900 - y 로
미리 뒤집어 0..1024 viewBox에 맞춘다(런타임 transform 불필요).
"""

import io
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRILLS = ROOT / "drills"
OUT = DRILLS / "중국어_한자_쓰기.json"

BASE = "https://raw.githubusercontent.com/skishore/makemeahanzi/master/"
UNIHAN = "https://www.unicode.org/Public/UCD/latest/ucd/Unihan.zip"
WIKT = "https://ko.wiktionary.org/w/api.php"
WIKT_EN = "https://en.wiktionary.org/w/api.php"
# 위키미디어는 연락처 없는 User-Agent를 차단한다 (User-Agent 정책)
UA = {"User-Agent": "brain-hanzi-drill/1.0 (https://brain.dongwook.kim; dongwook.kim@feedle.me)"}
CJK_RE = re.compile(r"[一-鿿]")
HANJA_TPL_RE = re.compile(r"\{\{한자풀이\s*(.*?)\}\}", re.S)
KO_SECTION_RE = re.compile(r"\n==Korean==(.*?)(?=\n==[^=]|\Z)", re.S)
KO_HANJA_RE = re.compile(r"\{\{ko-hanja(?:/new)?\|([^}]*)\}\}")
WIKILINK_RE = re.compile(r"\[\[(?:[^\]|]*\|)?([^\]|]*)\]\]")

VIEWBOX = 1024
FLIP_Y = 900  # makemeahanzi 기준선 — 렌더 시 transform="translate(0,900) scale(1,-1)"

# drills/중국어_HSK_어휘.json 의 구간(id 기준). 어휘 순서가 HSK1→2→3 이다.
HSK_SPANS = [("HSK 1급", 0, 150), ("HSK 2급", 150, 297), ("HSK 3급", 297, 595)]

BUILT_ON = "2026-08-01"


def fetch(url, binary=False, retries=6):
    """위키낱말사전은 연속 요청에 429를 준다 — Retry-After를 지키고 지수 백오프한다."""
    for attempt in range(retries):
        try:
            raw = urllib.request.urlopen(
                urllib.request.Request(url, headers=UA), timeout=180
            ).read()
            return raw if binary else raw.decode("utf-8")
        except urllib.error.HTTPError as exc:
            if exc.code != 429 or attempt == retries - 1:
                raise RuntimeError(f"{url[:80]} 실패: {exc}") from exc
            wait = int(exc.headers.get("Retry-After") or 0) or 5 * (2 ** attempt)
            print(f"  429 — {wait}초 대기 후 재시도", file=sys.stderr)
            time.sleep(wait)
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt == retries - 1:
                raise RuntimeError(f"{url[:80]} 실패: {exc}") from exc
            time.sleep(2 ** attempt)


def fetch_lines(name):
    return [json.loads(ln) for ln in fetch(BASE + name).strip().split("\n")]


def load_unihan():
    """간체→번체 후보와 한국 한자음(kHangul).

    kTraditionalVariant만 믿으면 안 된다 — 자기 자신을 포함하는 경우가 있고(这 → 这·這),
    아예 비어 있는 글자도 많다(电). 번체 쪽 kSimplifiedVariant를 뒤집어 함께 모은다.
    """
    z = zipfile.ZipFile(io.BytesIO(fetch(UNIHAN, binary=True)))
    hangul, trad, from_simp = {}, {}, {}
    for line in z.read("Unihan_Readings.txt").decode("utf-8").split("\n"):
        if "\tkHangul\t" in line:
            cp, _, val = line.split("\t")
            # "작:0E" 처럼 출처 코드가 붙는다 — 음절만 남긴다
            hangul[chr(int(cp[2:], 16))] = [v.split(":")[0] for v in val.split()]
    for line in z.read("Unihan_Variants.txt").decode("utf-8").split("\n"):
        if "\tkTraditionalVariant\t" in line:
            cp, _, val = line.split("\t")
            trad[chr(int(cp[2:], 16))] = [chr(int(v[2:], 16)) for v in val.split()]
        elif "\tkSimplifiedVariant\t" in line:
            cp, _, val = line.split("\t")
            src = chr(int(cp[2:], 16))
            for v in val.split():
                from_simp.setdefault(chr(int(v[2:], 16)), []).append(src)

    def candidates(ch):
        seen = []
        for t in trad.get(ch, []) + from_simp.get(ch, []):
            if t != ch and t not in seen:
                seen.append(t)
        return seen

    return hangul, candidates


def wiktionary_pages(titles, api=WIKT):
    """위키낱말사전 원문을 50개씩 묶어 받는다."""
    out = {}
    for i in range(0, len(titles), 50):
        query = urllib.parse.urlencode({
            "action": "query", "prop": "revisions", "rvprop": "content",
            "rvslots": "main", "format": "json", "formatversion": "2",
            "titles": "|".join(titles[i:i + 50]),
        })
        data = json.loads(fetch(f"{api}?{query}"))
        for page in data["query"]["pages"]:
            revs = page.get("revisions") or [{}]
            out[page["title"]] = revs[0].get("slots", {}).get("main", {}).get("content") or ""
        time.sleep(1.0)   # 익명 API는 초당 1회 정도로 자제한다
    return out


def parse_hunmeum(wikitext):
    """{{한자풀이|훈=어제|음=작}} → "어제 작". 틀이 없거나 불완전하면 None."""
    m = HANJA_TPL_RE.search(wikitext or "")
    if not m:
        return None
    fields = {}
    for part in m.group(1).split("|"):
        if "=" in part:
            key, val = part.split("=", 1)
            fields[key.strip()] = re.sub(r"[\[\]]", "", val.strip())
    hun, eum = fields.get("훈"), fields.get("음")
    return f"{hun} {eum}" if hun and eum else None


def parse_en_hunmeum(wikitext, eum_set):
    """en.wiktionary의 {{ko-hanja/new|…}}에서 훈음을 뽑는다.

    인자 형식이 제각각이다 — `한|일`(훈·음), `위|윗|상`(훈·관형형·음),
    `힘|력||역`(훈·음·공백·두음). 위치만 보고 고르면 틀린다.
    그래서 Unihan kHangul(권위 있는 한국 한자음)과 일치하는 자리를 음으로 확정하고,
    바로 앞자리를 훈으로 삼는다. 음이 첫 자리면 훈이 없는 것이므로 음만 반환한다.
    """
    section = KO_SECTION_RE.search(wikitext or "")
    if not section:
        return None
    m = KO_HANJA_RE.search(section.group(1))
    if not m:
        return None
    # [[빠르다|빠를]] 안에도 | 가 있다 — 인자를 쪼개기 전에 위키링크를 먼저 벗긴다
    args = [a.strip() for a in WIKILINK_RE.sub(r"\1", m.group(1)).split("|")]
    args = [a for a in args if "=" not in a]          # hangeul=… 같은 이름인자는 뺀다
    for i, a in enumerate(args):
        if a in eum_set:
            return f"{args[i - 1]} {a}" if i > 0 and args[i - 1] else a
    # Unihan에 음이 없는 글자(查·跑 등)는 대조할 기준이 없다. 인자 개수로 판단한다.
    #   2개 전부 채워짐 → |훈|음|
    #   3개 전부 채워짐 → |훈 기본형|훈 관형형|음|  (관형형이 훈음에 쓰는 형태)
    #   빈 칸이 낀 4개(힘|력||역)는 두음법칙 변형이 섞인 형태라 위에서 걸러진다
    if len(args) == 2 and all(args):
        return f"{args[0]} {args[1]}"
    if len(args) == 3 and all(args):
        return f"{args[1]} {args[2]}"
    if len(args) == 1 and args[0]:
        return args[0]                                 # 음만 실린 항목
    return None


def build_hunmeum(chars):
    """한글 훈음. 간체자 페이지는 번체를 가리키는 껍데기라 번체로 한 번 더 찾는다.
    훈을 못 구하면 Unihan의 음만이라도 쓰고, 그것도 없으면 비운다(지어내지 않는다)."""
    hangul, candidates = load_unihan()
    result = {c: parse_hunmeum(t) for c, t in wiktionary_pages(chars).items()}

    need = [c for c in chars if not result.get(c)]
    alts = {c: candidates(c) for c in need}
    pages = wiktionary_pages(sorted({t for v in alts.values() for t in v}))
    for c in need:
        for t in alts[c]:
            hit = parse_hunmeum(pages.get(t, ""))
            if hit:
                result[c] = hit
                break

    # ko.wiktionary가 {{한자풀이}} 대신 {{Han char}}만 쓰는 글자(一·人·十 등)가 꽤 있다.
    # 그런 글자는 en.wiktionary의 한국어 섹션이 훈음을 갖고 있는 경우가 많다.
    still = [c for c in chars if not result.get(c)]
    en_pages = wiktionary_pages(still, api=WIKT_EN)
    for c in still:
        eum_set = set(hangul.get(c, []))
        for alt in candidates(c):
            eum_set |= set(hangul.get(alt, []))
        hit = parse_en_hunmeum(en_pages.get(c, ""), eum_set)
        if hit:
            result[c] = hit

    eum_only = 0
    for c in chars:
        value = result.get(c)
        if value and " " in value:
            continue
        if not value:                       # 훈도 음도 못 구한 경우 Unihan 음이라도
            for src in [c] + candidates(c):
                if hangul.get(src):
                    result[c] = hangul[src][0]
                    break
        if result.get(c):
            eum_only += 1
    found = sum(1 for c in chars if result.get(c))
    print(f"한글 훈음 {found}/{len(chars)}자 (그중 음만 {eum_only}자)")
    return result


def median_path(median):
    """중심선 좌표열 → SVG 폴리라인 path (Y축 반전 포함)."""
    pts = [f"{x} {FLIP_Y - y}" for x, y in median]
    if len(pts) == 1:  # 점 하나짜리 획은 길이 0이라 채점이 불가능하다
        return None
    return "M " + " L ".join(pts)


def gloss(entry):
    """뜻 — 원문 정의를 앞 두 조각만. 지어내지 않는다."""
    text = (entry.get("definition") or "").strip()
    if not text:
        return entry["character"]
    return ", ".join(p.strip() for p in text.split(",")[:2])


def collect_targets():
    """우리가 실제로 다룬 한자 + HSK 급수별 최초 등장 순서."""
    notes = set()
    for f in sorted((ROOT / "notes" / "중국어").glob("*.md")):
        notes |= set(CJK_RE.findall(f.read_text(encoding="utf-8")))
    for f in sorted((ROOT / "sheets" / "중국어").glob("*.html")):
        notes |= set(CJK_RE.findall(f.read_text(encoding="utf-8")))

    rows = json.loads((DRILLS / "중국어_HSK_어휘.json").read_text(encoding="utf-8"))
    buckets, seen = [], set()
    for label, lo, hi in HSK_SPANS:
        chars = []
        for row in rows[lo:hi]:
            for ch in CJK_RE.findall(row["expression"]):
                if ch not in seen:
                    seen.add(ch)
                    chars.append(ch)
        buckets.append((label, chars))

    # HSK 어휘엔 없고 노트·시트에만 나온 글자
    buckets.append(("노트·시트 한자", sorted(notes - seen)))
    return buckets, notes | seen


def main():
    print("makemeahanzi 내려받는 중…")
    graphics = {e["character"]: e for e in fetch_lines("graphics.txt")}
    meanings = {e["character"]: e for e in fetch_lines("dictionary.txt")}
    print(f"  graphics {len(graphics)}자 / dictionary {len(meanings)}자")

    buckets, targets = collect_targets()
    print(f"우리 자료에 등장한 한자 {len(targets)}자")

    out = {
        "_license": [
            {
                "for": "획순 데이터 (medians)",
                "source": "makemeahanzi graphics.txt — https://github.com/skishore/makemeahanzi",
                "derived_from": "Arphic PL KaitiM GB / Arphic PL UKai",
                "copyright": "Copyright (C) 1999 Arphic Technology Co., Ltd.",
                "license": "Arphic Public License — /licenses/ARPHICPL.TXT",
            },
            {
                "for": "영문 뜻·병음",
                "source": "makemeahanzi dictionary.txt — https://github.com/skishore/makemeahanzi",
                "derived_from": "Unihan (Unicode Consortium), CJKlib",
                "license": "GNU LGPL v3 or later — /licenses/LGPL-3.0.txt",
            },
            {
                "for": "한글 훈음",
                "source": "위키낱말사전 {{한자풀이}} 틀 — https://ko.wiktionary.org",
                "license": "CC BY-SA 4.0 — https://creativecommons.org/licenses/by-sa/4.0/",
            },
            {
                "for": "한글 훈음 보조 (음만 아는 글자) · 간체→번체 매핑",
                "source": "Unihan Database kHangul / kTraditionalVariant — https://unicode.org/charts/unihan.html",
                "copyright": "Copyright © 1991-2025 Unicode, Inc.",
                "license": "Unicode License v3 — https://www.unicode.org/license.txt",
            },
        ],
        # Arphic Public License §2(a) — 수정 내역을 파일 안에 명시한다
        "_modifications": {
            "date": BUILT_ON,
            "by": "scripts/build_hanzi_strokes.py",
            "changes": [
                "graphics.txt에서 이 저장소의 노트·치트시트·HSK 어휘에 등장한 한자만 추출",
                "외곽선(strokes) 대신 획 중심선(medians)을 SVG 폴리라인 path로 변환",
                "좌표 Y축 반전 (y' = 900 - y) 후 1024×1024 viewBox 기준으로 저장",
                "정의(definition) 앞 두 조각만 남기고 절단",
                "위키낱말사전 {{한자풀이}}에서 뽑은 한글 훈음을 각 글자에 병기",
            ],
        },
        "viewBox": f"0 0 {VIEWBOX} {VIEWBOX}",
        "sets": [],
    }

    print("한글 훈음 조회 중 (위키낱말사전 + Unihan)…")
    hunmeum = build_hunmeum(sorted(targets))

    missing, degenerate = [], []
    for label, chars in buckets:
        entries = []
        for ch in chars:
            g = graphics.get(ch)
            if not g:
                missing.append(ch)
                continue
            paths = [median_path(m) for m in g["medians"]]
            if not paths or any(p is None for p in paths):
                degenerate.append(ch)
                continue
            en = gloss(meanings.get(ch, {"character": ch}))
            ko = hunmeum.get(ch)
            # 훈음이 있으면 그것을 앞세우고 영문 뜻은 보조로 내린다.
            # 없으면 영문 뜻만 — 훈음을 지어내지 않는다.
            entry = {"k": ch, "r": ko or en, "s": paths}
            pinyin = (meanings.get(ch, {}).get("pinyin") or [])
            if pinyin:
                entry["r2"] = " · ".join(pinyin[:2])
            if ko:
                entry["r3"] = en
            entries.append(entry)
        entries.sort(key=lambda e: len(e["s"]))  # 획수 적은 것부터 = 쓰기 쉬운 순
        out["sets"].append({"id": f"hanzi-{len(out['sets'])}", "label": label, "chars": entries})
        print(f"{label:16s} {len(entries):3d}자")

    OUT.write_text(
        json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
    )
    total = sum(len(s["chars"]) for s in out["sets"])
    print(f"\n{OUT.relative_to(ROOT)}  {OUT.stat().st_size / 1024:.0f} KB")
    print(f"총 {total}자 / {len(out['sets'])}세트")
    if missing:
        print(f"획 데이터 없음 {len(missing)}자: {''.join(missing)}", file=sys.stderr)
    if degenerate:
        print(f"중심선 이상 {len(degenerate)}자: {''.join(degenerate)}", file=sys.stderr)
    return 1 if (missing or degenerate) else 0


if __name__ == "__main__":
    sys.exit(main())
