#!/usr/bin/env python3
"""획순 쓰기 드릴 데이터(drills/일본어_문자_쓰기.json)를 만든다.

- 획 path: KanjiVG (CC BY-SA 3.0)
- 한자 뜻·읽기: KANJIDIC2 / EDRDG (CC BY-SA 4.0), kanjiapi.dev 경유
- 가나 romaji: 기존 drills/*.json (이미 검증된 데이터)

한자 목록은 notes/일본어/일본어_문자의_특징.md 에 실제로 등장한 글자에서 뽑는다.
(구 일본어_기본_한자 노트가 이 파일로 병합됨)
"""

import concurrent.futures as cf
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRILLS = ROOT / "drills"
NOTE = ROOT / "notes" / "일본어" / "일본어_문자의_특징.md"
OUT = DRILLS / "일본어_문자_쓰기.json"

SVG_URL = "https://raw.githubusercontent.com/KanjiVG/kanjivg/master/kanji/{:05x}.svg"
KANJI_API = "https://kanjiapi.dev/v1/kanji/{}"
UA = {"User-Agent": "Mozilla/5.0 (brain kanji-drill build script)"}
PATH_RE = re.compile(r'<path id="kvg:[0-9a-f]+-s(\d+)"[^>]*\sd="([^"]+)"')
CJK_RE = re.compile(r"[一-鿿]")

SMALL_HIRA = [
    ("ぁ", "작은 a"), ("ぃ", "작은 i"), ("ぅ", "작은 u"),
    ("ぇ", "작은 e"), ("ぉ", "작은 o"),
    ("ゃ", "작은 ya"), ("ゅ", "작은 yu"), ("ょ", "작은 yo"),
    ("っ", "촉음 (っ)"),
]
SMALL_KATA = [
    ("ァ", "작은 a"), ("ィ", "작은 i"), ("ゥ", "작은 u"),
    ("ェ", "작은 e"), ("ォ", "작은 o"),
    ("ャ", "작은 ya"), ("ュ", "작은 yu"), ("ョ", "작은 yo"),
    ("ッ", "촉음 (ッ)"),
]

KANA_SETS = [
    ("hira-basic", "히라가나 청음", "일본어_히라가나"),
    ("hira-daku", "히라가나 탁음·반탁음", "일본어_히라가나_탁음"),
    ("hira-small", "히라가나 작은 글자", SMALL_HIRA),
    ("kata-basic", "가타카나 청음", "일본어_가타카나"),
    ("kata-daku", "가타카나 탁음·반탁음", "일본어_가타카나_탁음"),
    ("kata-small", "가타카나 작은 글자", SMALL_KATA),
]

# 교육한자 학년 배정에 맞춘 묶음 (노트의 학년별 프레임을 그대로 따름)
KANJI_SETS = [
    ("kanji-g1", "한자 1학년", {1}),
    ("kanji-g2", "한자 2학년", {2}),
    ("kanji-g34", "한자 3·4학년", {3, 4}),
    ("kanji-g56", "한자 5·6학년", {5, 6}),
    ("kanji-adv", "한자 중학교 이상", None),  # 나머지 전부
]


def fetch(url, retries=3):
    for attempt in range(retries):
        try:
            return urllib.request.urlopen(
                urllib.request.Request(url, headers=UA), timeout=30
            ).read().decode("utf-8")
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt == retries - 1:
                raise RuntimeError(f"{url} 실패: {exc}") from exc
            time.sleep(1.5 * (attempt + 1))


def fetch_strokes(ch):
    raw = fetch(SVG_URL.format(ord(ch)))
    found = PATH_RE.findall(raw)
    if not found:
        raise RuntimeError(f"{ch} (U+{ord(ch):04X}): 획 path 없음")
    nums = sorted(int(n) for n, _ in found)
    if nums != list(range(1, len(nums) + 1)):
        raise RuntimeError(f"{ch}: 획 번호 불연속 {nums}")
    return [d for _, d in sorted(found, key=lambda p: int(p[0]))]


def fetch_kanji_meta(ch):
    return json.loads(fetch(KANJI_API.format(urllib.parse.quote(ch))))


# 부수 자체는 KANJIDIC 뜻이 "radical number 9" 식이라 학습에 쓸모없다.
# 노트(일본어_문자의_특징.md)가 직접 밝힌 우리말 이름으로 대체한다.
RADICAL_GLOSS = {
    "亻": "사람인변 (사람)",
    "扌": "재방변 (손)",
    "氵": "삼수변 (물)",
}


def kanji_label(meta):
    """뜻과 읽기를 프롬프트용 두 줄로. 원문 그대로만 쓰고 지어내지 않는다."""
    ch = meta.get("kanji", "")
    if ch in RADICAL_GLOSS:
        return RADICAL_GLOSS[ch], ""

    # "one radical (no.1)" 같은 부수 번호 설명은 뜻이 아니라 사전 메타데이터다
    meanings = [m for m in (meta.get("meanings") or []) if "radical" not in m.lower()]
    kun = (meta.get("kun_readings") or [])[:1]
    on = (meta.get("on_readings") or [])[:1]
    main = ", ".join(meanings[:2]) if meanings else ch
    sub = " · ".join(kun + on)
    return main, sub


def load_kana_pairs(source):
    if isinstance(source, list):
        return source
    data = json.loads((DRILLS / f"{source}.json").read_text(encoding="utf-8"))
    return [(row["kana"], row["romaji"]) for row in data]


def main():
    out = {
        "_license": [
            {
                "for": "획순 path 데이터",
                "source": "KanjiVG — https://github.com/KanjiVG/kanjivg",
                "copyright": "Copyright (C) 2009-2011 Ulrich Apel",
                "license": "CC BY-SA 3.0 — http://creativecommons.org/licenses/by-sa/3.0/",
            },
            {
                "for": "한자 뜻·읽기",
                "source": "KANJIDIC2 / EDRDG — http://www.edrdg.org/wiki/index.php/KANJIDIC_Project",
                "copyright": "Copyright (C) Electronic Dictionary Research and Development Group",
                "license": "CC BY-SA 4.0 — https://creativecommons.org/licenses/by-sa/4.0/",
            },
        ],
        "note": "획 데이터는 KanjiVG의 파생물이며 동일 조건으로 배포된다.",
        "viewBox": "0 0 109 109",
        "sets": [],
    }

    failed = []

    # ── 가나 ──────────────────────────────────────────────────
    for set_id, label, source in KANA_SETS:
        chars = []
        for kana, romaji in load_kana_pairs(source):
            try:
                chars.append({"k": kana, "r": romaji, "s": fetch_strokes(kana)})
            except RuntimeError as exc:
                print(f"  ! {exc}", file=sys.stderr)
                failed.append(kana)
        out["sets"].append({"id": set_id, "label": label, "chars": chars})
        print(f"{label:22s} {len(chars):3d}자")

    # ── 한자 (노트에 등장한 글자) ────────────────────────────────
    kanji = sorted(set(CJK_RE.findall(NOTE.read_text(encoding="utf-8"))))
    print(f"\n노트에서 추출한 한자 {len(kanji)}자 — 획순·뜻 조회 중")

    def build_kanji(ch):
        return ch, fetch_strokes(ch), fetch_kanji_meta(ch)

    built = {}
    with cf.ThreadPoolExecutor(max_workers=12) as ex:
        for fut in cf.as_completed([ex.submit(build_kanji, c) for c in kanji]):
            try:
                ch, strokes, meta = fut.result()
                built[ch] = (strokes, meta)
            except Exception as exc:
                print(f"  ! {exc}", file=sys.stderr)
                failed.append("?")

    used = set()
    for set_id, label, grades in KANJI_SETS:
        chars = []
        for ch in kanji:
            if ch not in built or ch in used:
                continue
            grade = built[ch][1].get("grade")
            if grades is None or grade in grades:
                strokes, meta = built[ch]
                main, sub = kanji_label(meta)
                entry = {"k": ch, "r": main, "s": strokes}
                if sub:
                    entry["r2"] = sub
                chars.append(entry)
                used.add(ch)
        # 획수 적은 것부터 = 배우기 쉬운 순
        chars.sort(key=lambda c: len(c["s"]))
        out["sets"].append({"id": set_id, "label": label, "chars": chars})
        print(f"{label:22s} {len(chars):3d}자")

    OUT.write_text(
        json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
    )
    total = sum(len(s["chars"]) for s in out["sets"])
    print(f"\n{OUT.relative_to(ROOT)}  {OUT.stat().st_size / 1024:.1f} KB")
    print(f"총 {total}자 / {len(out['sets'])}세트, 실패 {len(failed)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
