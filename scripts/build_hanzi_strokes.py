#!/usr/bin/env python3
"""한자 획순 쓰기 드릴 데이터(drills/중국어_한자_쓰기.json)를 만든다.

- 획 데이터: makemeahanzi graphics.txt (Arphic Public License)
- 뜻·병음:   makemeahanzi dictionary.txt (LGPL v3+, Unihan/CJKlib 파생)

대상 글자는 우리가 실제로 다룬 것만 — notes/중국어/*.md, sheets/중국어/*.html,
drills/중국어_HSK_어휘.json 에 등장한 한자의 합집합.

graphics.txt의 `strokes`는 채워 그리는 외곽선이라 획의 시작점·방향을 뽑을 수 없다.
드릴 채점기는 중심선을 요구하므로 `medians`(획 중심선 좌표열)를 폴리라인 path로 바꿔 쓴다.
좌표계도 다르다 — makemeahanzi는 Y축이 위로 향하고 기준선이 900이므로 y' = 900 - y 로
미리 뒤집어 0..1024 viewBox에 맞춘다(런타임 transform 불필요).
"""

import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRILLS = ROOT / "drills"
OUT = DRILLS / "중국어_한자_쓰기.json"

BASE = "https://raw.githubusercontent.com/skishore/makemeahanzi/master/"
UA = {"User-Agent": "Mozilla/5.0 (brain hanzi-drill build script)"}
CJK_RE = re.compile(r"[一-鿿]")

VIEWBOX = 1024
FLIP_Y = 900  # makemeahanzi 기준선 — 렌더 시 transform="translate(0,900) scale(1,-1)"

# drills/중국어_HSK_어휘.json 의 구간(id 기준). 어휘 순서가 HSK1→2→3 이다.
HSK_SPANS = [("HSK 1급", 0, 150), ("HSK 2급", 150, 297), ("HSK 3급", 297, 595)]

BUILT_ON = "2026-08-01"


def fetch_lines(name):
    raw = urllib.request.urlopen(
        urllib.request.Request(BASE + name, headers=UA), timeout=180
    ).read().decode("utf-8")
    return [json.loads(ln) for ln in raw.strip().split("\n")]


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
                "for": "뜻·병음",
                "source": "makemeahanzi dictionary.txt — https://github.com/skishore/makemeahanzi",
                "derived_from": "Unihan (Unicode Consortium), CJKlib",
                "license": "GNU LGPL v3 or later — /licenses/LGPL-3.0.txt",
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
            ],
        },
        "viewBox": f"0 0 {VIEWBOX} {VIEWBOX}",
        "sets": [],
    }

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
            entry = {"k": ch, "r": gloss(meanings.get(ch, {"character": ch})), "s": paths}
            pinyin = (meanings.get(ch, {}).get("pinyin") or [])
            if pinyin:
                entry["r2"] = " · ".join(pinyin[:2])
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
