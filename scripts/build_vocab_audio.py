#!/usr/bin/env python3
"""단어장 발음 mp3를 만들고 배치한다.

배경 — xAI Grok TTS 플레이그라운드는 무료로 생성·다운로드가 되지만 API는 유료다.
그래서 "여러 단어를 한 번에 생성해 받고, 무음을 기준으로 잘라 순서대로 배치"한다.
순서가 진실이므로 음성인식이 필요 없다. 이 데이터셋은 동음이의가 빽빽해서
(ja|ひ 하나가 자연/sun·자연/fire·시간/day 세 곳에 걸린다) 인식 기반 배치는 위험하다.

발화 텍스트 규칙은 assets/js/vocab.js 의 speakText() 와 반드시 같아야 한다.
  - 일본어: 한자 표기는 TTS가 음독으로 잘못 읽으므로 rom의 かな를 쓴다
  - 러시아어: 강세 기호 U+0301은 사전 표기용이라 뺀다
  - 아랍어: 모음부호가 있어야 정확히 읽히므로 그대로 둔다
한쪽만 고치면 조용히 어긋나므로 CLAUDE.md에도 이 사실을 적어 두었다.

사용법
  script  대상 언어의 배치 대본을 만든다. 플레이그라운드에 그대로 붙여 넣는다.
  split   받은 오디오를 잘라 mp3로 인코딩해 audio/ 아래 제 자리에 넣는다.
  status  무엇이 남았는지 세고 audio/manifest.json 을 다시 쓴다.

플레이그라운드 설정 — Output format=MP3, Sample rate·Bit rate는 고를 수 있는 가장 높은 값.
split 이 어차피 22.05kHz·32kbps 모노로 재인코딩하므로 원본이 좋을수록 손해가 없다.
**언어는 고를 수 없다 — 자동 감지다.** 라틴 문자 언어는 오판 여지가 있어 듣고 확인한다.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOCAB = ROOT / "vocab"
AUDIO = ROOT / "audio"

# vocab.js 의 SPEAK_LANG 과 같은 순서·같은 코드
LANGS = ["en", "ja", "zh", "fr", "de", "es", "ru", "ar"]

KANA_ONLY = re.compile(r"^[ぁ-ゖ゠-ヿー]+$")
COMBINING_ACUTE = "́"
PAUSE = "[long-pause]"

# 인코딩·분할 상수.
# [long-pause] 의 실제 길이는 일정하지 않다 — 러시아어 14개 시험에서 0.33~1.27초로
# 4배 가까이 흔들렸다. 반면 단어 내부 쉼은 최대 0.171초였다. 고정 임계를 쓰면
# 배치마다 깨지므로, 임계를 훑어 기대 개수와 맞는 값을 스스로 고른다.
SILENCE_DB = "-40dB"
SILENCE_SWEEP = [round(0.60 - 0.02 * i, 2) for i in range(26)]  # 0.60 → 0.10
MP3_ARGS = ["-codec:a", "libmp3lame", "-b:a", "32k", "-ac", "1", "-ar", "22050"]


def speak_text(lang: str, entry: dict) -> str:
    """assets/js/vocab.js 의 speakText() 와 같은 규칙."""
    if lang == "ja":
        kana = str(entry.get("rom") or "").split("·")[0].strip()
        if KANA_ONLY.match(kana):
            return kana
    if lang == "ru":
        return entry["word"].replace(COMBINING_ACUTE, "")
    return entry["word"]


def load_items():
    """(lang, category, concept_id, alt_index, text, rel_path) 를 정해진 순서로 낸다."""
    items = []
    for path in sorted(VOCAB.glob("*.json")):
        category = path.stem
        data = json.loads(path.read_text(encoding="utf-8"))
        for concept in data["concepts"]:
            for lang in data["languages"]:
                entry = concept["words"].get(lang)
                if not entry:
                    continue
                for idx, one in enumerate([entry, *entry.get("alt", [])]):
                    name = concept["id"] + (f"-{idx}" if idx else "")
                    items.append({
                        "lang": lang,
                        "category": category,
                        "concept": concept["id"],
                        "alt": idx,
                        "text": speak_text(lang, one),
                        "path": f"audio/{lang}/{category}/{name}.mp3",
                    })
    return items


def cmd_script(args):
    items = [i for i in load_items() if i["lang"] == args.lang]
    if args.category:
        items = [i for i in items if i["category"] == args.category]
    if not items:
        sys.exit(f"해당하는 항목이 없다: lang={args.lang} category={args.category}")

    todo = [i for i in items if args.all or not (ROOT / i["path"]).exists()]
    batch = todo[args.offset: args.offset + args.size]
    if not batch:
        print("남은 항목이 없다.")
        return

    out_dir = ROOT / "audio" / "_batches"
    out_dir.mkdir(parents=True, exist_ok=True)
    # 태그에 카테고리를 넣는다. <언어>-<offset> 만 쓰면 카테고리가 바뀔 때 같은 이름이
    # 다시 나와, 색깔 대본이 남아 있는 자리에 숫자 대본이 덮이거나 그 반대가 된다.
    tag = f"{args.lang}-{args.category or 'all'}-{args.offset:04d}"
    # [long-pause] 를 두 번 겹쳐 무음을 벌리려 해 봤지만 태그로 인식되지 않고 글자로 읽힌다
    # (중국어 21개 기준 15.2초 → 37.6초, 그런데 검출되는 무음은 오히려 줄었다).
    # 무음이 모자라면 --size 로 배치를 쪼개는 수밖에 없다.
    (out_dir / f"{tag}.txt").write_text(PAUSE.join(i["text"] for i in batch), encoding="utf-8")
    (out_dir / f"{tag}.json").write_text(
        json.dumps(batch, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"배치 {tag} — {len(batch)}개 (전체 남은 {len(todo)}개)")
    print(f"  대본: audio/_batches/{tag}.txt")
    print(f"  순서: audio/_batches/{tag}.json")
    print()
    print("플레이그라운드 설정 — Output format=MP3, Sample rate·Bit rate는 가장 높은 값.")
    print("언어 선택은 없다(자동 감지). 숫자 카테고리는 Text normalization 을 켠다.")
    print("대본을 그대로 붙여 넣고 생성한 뒤 받은 파일을 이렇게 넘긴다:")
    print(f"  python3 scripts/build_vocab_audio.py split {tag} ~/Downloads/받은파일.mp3")
    print()
    print("─" * 60)
    print(PAUSE.join(i["text"] for i in batch))
    print("─" * 60)


def detect_boundaries(src: Path, min_silence: float, total: float):
    """주어진 임계에서 항목 사이 무음 구간의 (시작, 끝) 목록. 앞뒤 여백은 뺀다."""
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(src),
         "-af", f"silencedetect=noise={SILENCE_DB}:d={min_silence}", "-f", "null", "-"],
        capture_output=True, text=True)
    starts = [float(m) for m in re.findall(r"silence_start: ([\d.]+)", proc.stderr)]
    ends = [float(m) for m in re.findall(r"silence_end: ([\d.]+)", proc.stderr)]
    pairs = list(zip(starts, ends))
    return [(s, e) for s, e in pairs if s > 0.05 and e < total - 0.05]


def pick_threshold(src: Path, expected: int, total: float):
    """기대 조각 수와 맞는 임계를 고른다. 맞는 구간의 한가운데를 쓴다.

    맞는 임계가 여러 개면 그 구간이 넓을수록 안전하다 — 단어 내부 쉼과
    항목 사이 쉼의 간격이 그만큼 벌어져 있다는 뜻이다.
    """
    ok = [d for d in SILENCE_SWEEP
          if len(detect_boundaries(src, d, total)) == expected - 1]
    if not ok:
        return None, []
    return ok[len(ok) // 2], ok


def rank_boundaries(src: Path, expected: int, total: float):
    """맞는 임계가 없을 때: 가장 낮은 임계로 후보를 다 모아 긴 순으로 필요한 만큼만 쓴다.

    임계 하나로는 못 가르는 배치가 있다 — 중국어 21개는 경계가 19개에서 22개로 건너뛰어
    20개가 되는 임계가 아예 없었고, 독일어·아랍어는 단어 내부 쉼 하나가 항목 사이 쉼
    하나보다 길어 겹쳤다. 순위로 고르면 그 겹침 하나만 잘못될 뿐 나머지는 살아난다.

    함께 내는 margin 은 (남긴 것 중 가장 짧은 무음, 버린 것 중 가장 긴 무음)이다.
    앞이 뒤보다 넉넉히 커야 안전하고, 붙어 있으면 그 경계가 뒤바뀌었을 수 있다.
    """
    cand = detect_boundaries(src, min(SILENCE_SWEEP), total)
    if len(cand) < expected - 1:
        return None, None
    ranked = sorted(cand, key=lambda p: p[1] - p[0], reverse=True)
    kept = sorted(ranked[:expected - 1])
    dropped = ranked[expected - 1:]
    return kept, (min((e - s for s, e in kept), default=0.0),
                  max((e - s for s, e in dropped), default=0.0))


def duration(src: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(src)], capture_output=True, text=True).stdout.strip()
    return float(out)


def cmd_split(args):
    meta = ROOT / "audio" / "_batches" / f"{args.tag}.json"
    if not meta.exists():
        sys.exit(f"배치 정보가 없다: {meta}")
    batch = json.loads(meta.read_text(encoding="utf-8"))
    src = Path(args.audio).expanduser()
    if not src.exists():
        sys.exit(f"오디오가 없다: {src}")

    total = duration(src)
    expected = len(batch)
    chosen, ok = pick_threshold(src, expected, total)
    if chosen is not None:
        inner = detect_boundaries(src, chosen, total)
        print(f"임계 {chosen}초 선택 (맞는 범위 {min(ok)}~{max(ok)}초, {len(ok)}단계)")
    else:
        inner, margin = (rank_boundaries(src, expected, total) if args.rank
                         else (None, None))
        if inner is None:
            print(f"조각 {expected}개로 나눌 임계를 찾지 못했다.", file=sys.stderr)
            for d in (0.5, 0.3, 0.2, 0.15, 0.10):
                print(f"  임계 {d}초 → 경계 {len(detect_boundaries(src, d, total))}개",
                      file=sys.stderr)
            print("script 를 --pause 2 로 다시 뽑아 생성하는 편이 낫다. "
                  "무음 길이만으로 밀어붙이려면 --rank 를 준다.", file=sys.stderr)
            sys.exit(1)
        print(f"!! 맞는 임계가 없어 무음이 긴 순으로 {expected - 1}개를 골랐다.")
        print(f"   남긴 무음 최소 {margin[0]:.2f}초 · 버린 무음 최대 {margin[1]:.2f}초"
              f"  (차이 {margin[0] - margin[1]:+.2f}초)")
        print("   차이가 작으면 경계가 뒤바뀌었을 수 있다 — 반드시 소리를 확인한다.")

    gaps = sorted(e - s for s, e in inner)
    # 조각이 1개면 자를 경계가 없다 — 읽기가 틀리는 단어를 혼자 다시 받을 때 생긴다.
    span = f"항목 사이 무음 {gaps[0]:.2f}~{gaps[-1]:.2f}초 · " if gaps else "경계 없음 · "
    print(f"  {span}조각 {expected}개\n")

    cuts = [0.0] + [(s + e) / 2 for s, e in inner] + [total]
    for i, item in enumerate(batch):
        dest = ROOT / item["path"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        start, end = cuts[i], cuts[i + 1]
        # -ss/-t 는 반드시 -i 앞에 둔다. 뒤에 두면 필터가 잘라낸 조각이 아니라
        # 원본 전체에 걸려서 조각별 앞뒤 묵음이 그대로 남는다.
        trim = "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.02"
        subprocess.run(
            ["ffmpeg", "-hide_banner", "-loglevel", "error",
             "-ss", f"{start:.3f}", "-t", f"{end - start:.3f}", "-i", str(src),
             # 앞을 자르고, 뒤집어 뒤쪽도 자른 뒤 되돌린다
             "-af", f"{trim},areverse,{trim},areverse",
             *MP3_ARGS, "-y", str(dest)], check=True)
        print(f"  {item['path']}  ←  {item['text']}")
    print(f"\n{len(batch)}개 배치 완료.")
    write_manifest()


def write_manifest():
    """(언어 × 카테고리)가 전부 채워졌는지만 기록한다. 최대 88줄이라 매 페이지에 얹어도 된다."""
    items = load_items()
    done = {}
    for lang in LANGS:
        cats = sorted({i["category"] for i in items if i["lang"] == lang})
        full = [c for c in cats
                if all((ROOT / i["path"]).exists()
                       for i in items if i["lang"] == lang and i["category"] == c)]
        done[lang] = full
    AUDIO.mkdir(exist_ok=True)
    (AUDIO / "manifest.json").write_text(
        json.dumps(done, ensure_ascii=False, indent=1), encoding="utf-8")
    print("audio/manifest.json 갱신")


def cmd_status(args):
    items = load_items()
    print(f"{'언어':<6}{'있음':>7}{'전체':>7}   미완성 카테고리")
    for lang in LANGS:
        mine = [i for i in items if i["lang"] == lang]
        have = [i for i in mine if (ROOT / i["path"]).exists()]
        cats = sorted({i["category"] for i in mine})
        missing = [c for c in cats
                   if any(not (ROOT / i["path"]).exists()
                          for i in mine if i["category"] == c)]
        print(f"{lang:<6}{len(have):>7}{len(mine):>7}   {', '.join(missing) if missing else '—'}")
    print(f"\n총 {sum(1 for i in items if (ROOT / i['path']).exists())} / {len(items)}")
    write_manifest()


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("script", help="배치 대본을 만든다")
    s.add_argument("lang", choices=LANGS)
    s.add_argument("--category", help="특정 카테고리만")
    s.add_argument("--size", type=int, default=40, help="한 배치 단어 수 (기본 40)")
    s.add_argument("--offset", type=int, default=0, help="남은 목록에서 건너뛸 개수")
    s.add_argument("--all", action="store_true", help="이미 있는 파일도 포함")
    s.set_defaults(func=cmd_script)

    s = sub.add_parser("split", help="받은 오디오를 잘라 배치한다")
    s.add_argument("tag", help="배치 태그 (예: ru-색깔-0000)")
    s.add_argument("audio", help="다운로드한 오디오 경로")
    s.add_argument("--rank", action="store_true",
                   help="맞는 임계가 없어도 무음이 긴 순으로 밀어붙인다 (어긋날 수 있다)")
    s.set_defaults(func=cmd_split)

    s = sub.add_parser("status", help="진행 상황과 매니페스트")
    s.set_defaults(func=cmd_status)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
