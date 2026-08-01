#!/usr/bin/env python3
"""KanjiVG에서 가나 획순 데이터를 받아 drills/일본어_가나_쓰기.json 을 만든다.

romaji는 기존 drills/*.json(검증된 데이터)에서 재사용하고, 획 path만 새로 받는다.
출처: https://github.com/KanjiVG/kanjivg (CC BY-SA 3.0)
"""

import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRILLS = ROOT / "drills"
OUT = DRILLS / "일본어_가나_쓰기.json"

SVG_URL = "https://raw.githubusercontent.com/KanjiVG/kanjivg/master/kanji/{:05x}.svg"
PATH_RE = re.compile(r'<path id="kvg:[0-9a-f]+-s(\d+)"[^>]*\sd="([^"]+)"')

# 소문자(요음·촉음·외래어용)는 기존 드릴에 단독 항목이 없어 여기서 정의한다.
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

SETS = [
    ("hira-basic", "히라가나 청음", "일본어_히라가나"),
    ("hira-daku", "히라가나 탁음·반탁음", "일본어_히라가나_탁음"),
    ("hira-small", "히라가나 작은 글자", SMALL_HIRA),
    ("kata-basic", "가타카나 청음", "일본어_가타카나"),
    ("kata-daku", "가타카나 탁음·반탁음", "일본어_가타카나_탁음"),
    ("kata-small", "가타카나 작은 글자", SMALL_KATA),
]


def load_pairs(source):
    """(kana, romaji) 목록을 만든다. source는 기존 드릴 파일명 또는 직접 정의한 리스트."""
    if isinstance(source, list):
        return source
    data = json.loads((DRILLS / f"{source}.json").read_text(encoding="utf-8"))
    return [(row["kana"], row["romaji"]) for row in data]


def fetch_strokes(ch, retries=3):
    """한 글자의 획 path를 획순대로 반환."""
    url = SVG_URL.format(ord(ch))
    for attempt in range(retries):
        try:
            raw = urllib.request.urlopen(url, timeout=30).read().decode("utf-8")
            break
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt == retries - 1:
                raise RuntimeError(f"{ch} (U+{ord(ch):04X}) 실패: {exc}") from exc
            time.sleep(1.5 * (attempt + 1))
    found = PATH_RE.findall(raw)
    if not found:
        raise RuntimeError(f"{ch} (U+{ord(ch):04X}): 획 path를 찾지 못함")
    return [d for _, d in sorted(found, key=lambda p: int(p[0]))]


def main():
    out = {
        "_license": {
            "data": "KanjiVG stroke order data",
            "source": "https://github.com/KanjiVG/kanjivg",
            "site": "http://kanjivg.tagaini.net",
            "copyright": "Copyright (C) 2009-2011 Ulrich Apel",
            "license": "CC BY-SA 3.0",
            "url": "http://creativecommons.org/licenses/by-sa/3.0/",
            "note": "획 path는 KanjiVG에서 추출한 파생물이며 동일 조건(CC BY-SA 3.0)으로 배포된다.",
        },
        "viewBox": "0 0 109 109",
        "sets": [],
    }

    total = failed = 0
    for set_id, label, source in SETS:
        chars = []
        for kana, romaji in load_pairs(source):
            try:
                chars.append({"k": kana, "r": romaji, "s": fetch_strokes(kana)})
                total += 1
            except RuntimeError as exc:
                print(f"  ! {exc}", file=sys.stderr)
                failed += 1
        out["sets"].append({"id": set_id, "label": label, "chars": chars})
        strokes = sum(len(c["s"]) for c in chars)
        print(f"{label:22s} {len(chars):3d}자 / {strokes:4d}획")

    OUT.write_text(
        json.dumps(out, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    print(f"\n{OUT.relative_to(ROOT)}  {OUT.stat().st_size / 1024:.1f} KB")
    print(f"총 {total}자, 실패 {failed}자")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
