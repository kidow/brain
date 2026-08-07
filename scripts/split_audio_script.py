#!/usr/bin/env python3
"""낭독 대본을 TTS 입력 한 번에 들어가는 크기로 쪼갠다.

빈 줄(문단 경계)에서만 자른다. 문단 하나가 한계를 넘으면 줄 단위로 내려가고,
줄 하나가 넘으면 멈춘다 — 문장 중간에서 자르면 발음과 억양이 깨진다.

    python3 scripts/split_audio_script.py _notes_audio/scripts/notes/중국어/중국어_회화.txt
    python3 scripts/split_audio_script.py --limit 5000 <대본>
    python3 scripts/split_audio_script.py --check          # 전체 대본 현황

쪼갠 결과는 <대본>.part1.txt … 로 나온다. 순서대로 생성해 받은 뒤 concat 한다.

    ffmpeg -f concat -safe 0 -i parts.txt -c copy 합본.mp3
"""

import argparse
import sys
from pathlib import Path

# 실측 근거: 3,577자 통과, 6,736자 실패 (Grok TTS, 2026-08-07).
# 통과 실적 3,577자 바로 위에 기본값을 둔다. 진짜 한계는 3,577~6,736 사이 어딘가이며,
# 이분 탐색으로 좁히면 --limit 으로 올려 생성 횟수를 줄일 수 있다.
# 주의: `wc -m`은 로케일에 따라 바이트를 세므로 믿지 말 것. 이 값은 파이썬 len() 기준이다.
DEFAULT_LIMIT = 3600

# 실측 낭독 속도. 2,891자→357초, 3,577자→473초.
CHARS_PER_SEC = 7.8


def chunks(text, limit):
    """빈 줄로 나눈 문단을 limit 이하로 묶는다."""
    paras = [p for p in text.strip().split("\n\n") if p.strip()]

    out, cur = [], ""
    for para in paras:
        if len(para) > limit:
            # 문단 하나가 한계를 넘는다. 줄 단위로 내려간다.
            if cur:
                out.append(cur)
                cur = ""
            for line in para.split("\n"):
                if len(line) > limit:
                    raise ValueError(
                        f"줄 하나가 {len(line)}자로 한계 {limit}자를 넘는다. "
                        f"대본을 손봐야 한다: {line[:40]}…"
                    )
                cur = f"{cur}\n{line}" if cur else line
                if len(cur) > limit:
                    out.append(cur[: -(len(line) + 1)])
                    cur = line
            continue

        candidate = f"{cur}\n\n{para}" if cur else para
        if len(candidate) > limit:
            out.append(cur)
            cur = para
        else:
            cur = candidate

    if cur:
        out.append(cur)
    return out


def balanced(text, limit):
    """같은 조각 수를 유지하면서 길이를 고르게 편다.

    limit로 그냥 자르면 마지막 조각이 46초짜리 꼬리로 남는다. 조각 수는 어차피
    ceil(전체/limit)로 정해지니, 그 수를 유지하는 가장 작은 목표치를 찾는다.
    """
    n = max(1, -(-len(text) // limit))
    for target in range(-(-len(text) // n), limit + 1):
        parts = chunks(text, target)
        if len(parts) <= n:
            return parts
    return chunks(text, limit)  # ponytail: 위 루프가 비면 원래 방식으로


def mmss(chars):
    sec = round(chars / CHARS_PER_SEC)
    return f"{sec // 60}분 {sec % 60:02d}초"


def split(path, limit):
    text = path.read_text(encoding="utf-8")
    parts = balanced(text, limit)

    if len(parts) == 1:
        print(f"{path.name}: {len(text)}자 · {mmss(len(text))} — 한 번에 들어간다")
        return

    for i, part in enumerate(parts, 1):
        out = path.with_suffix(f".part{i}.txt")
        out.write_text(part + "\n", encoding="utf-8")
        print(f"{out.name}: {len(part)}자 · {mmss(len(part))}")

    print(f"\n{len(parts)}개로 쪼갬. 순서대로 생성한 뒤 concat 한다.")


def check(limit):
    root = Path("_notes_audio/scripts")
    if not root.is_dir():
        sys.exit("_notes_audio/scripts 가 없다. 저장소 루트에서 실행한다.")

    total = 0
    for p in sorted(root.rglob("*.txt")):
        if ".part" in p.name:
            continue
        n = len(p.read_text(encoding="utf-8"))
        total += n
        flag = "" if n <= limit else f"  ← {len(balanced(p.read_text(encoding='utf-8'), limit))}개로 쪼개야 함"
        print(f"{n:7,}자  {mmss(n):>10}  {p.relative_to(root)}{flag}")

    print(f"\n합계 {total:,}자 · {mmss(total)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("script", nargs="?", type=Path)
    ap.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    ap.add_argument("--check", action="store_true", help="전체 대본 현황만 본다")
    args = ap.parse_args()

    if args.check:
        check(args.limit)
    elif args.script:
        split(args.script, args.limit)
    else:
        ap.error("대본 경로나 --check 중 하나가 필요하다")


def demo():
    """assert 자체 검사. python3 -c 'import scripts.split_audio_script as m; m.demo()'"""
    # 문단 경계에서만 자른다
    text = "가" * 100 + "\n\n" + "나" * 100 + "\n\n" + "다" * 100
    assert chunks(text, 250) == ["가" * 100 + "\n\n" + "나" * 100, "다" * 100]
    # 한 번에 들어가면 안 쪼갠다
    assert len(chunks(text, 9999)) == 1
    # 문단이 한계를 넘으면 줄 단위로 내려간다
    big = "\n".join(["라" * 90] * 5)
    assert all(len(c) <= 200 for c in chunks(big, 200))
    # 고르게 편다 — 조각 수를 늘리지 않으면서 꼬리를 줄인다
    tail = "\n\n".join(["바" * 100] * 7)
    greedy, even = chunks(tail, 250), balanced(tail, 250)
    assert all(len(p) <= 250 for p in even), even
    assert len(even) <= len(greedy), (len(even), len(greedy))
    # 꼬리가 실제로 줄어드는 입력
    tail2 = "\n\n".join(["사" * 100] * 6)
    assert min(len(p) for p in balanced(tail2, 500)) > min(len(p) for p in chunks(tail2, 500))
    # 줄 하나가 넘으면 멈춘다
    try:
        chunks("마" * 500, 100)
    except ValueError:
        pass
    else:
        raise AssertionError("긴 줄에서 멈추지 않았다")
    print("ok")


if __name__ == "__main__":
    main()
