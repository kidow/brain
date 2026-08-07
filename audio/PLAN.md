# 단어장 발음 오디오 계획

> **이 문서는 `vocab/` 단어 하나짜리 mp3에 대한 것이다.** 노트를 통째로 읽어 주는
> 낭독 오디오는 [_notes_audio/PLAN.md](../_notes_audio/PLAN.md)에 따로 있다.
> 둘은 TTS 엔진(Grok)만 공유하고 저장 위치·길이·용도가 전부 다르다.

`vocab/` 단어장의 단어마다 직접 만든 mp3를 붙인다. 지금은 Web Speech API로 읽고 있고,
mp3가 준비된 (언어 × 카테고리)부터 하나씩 mp3로 갈아탄다.

## 결정 사항

| 항목 | 결정 | 근거 |
|---|---|---|
| 포맷 | **mp3 32kbps 모노 22.05kHz** | μ-law·A-law는 브라우저 `canPlayType`이 빈 문자열(미지원), raw PCM은 컨테이너가 없어 `<audio>` 불가. 실측으로 확인했다 |
| 총량 | 2,827개 · **약 9.0MB** | 실제 분할 결과 평균 3.25KB. GitHub Pages 1GB 한도의 1% |
| 위치 | **저장소 커밋** (R2 아님) | 9MB는 R2 셋업 비용을 정당화하지 못한다. `vocab/*.json`과 같은 커밋에서 움직여 데이터와 음성이 어긋나지 않는다 |
| 경로 | `audio/<언어>/<카테고리>/<개념>[-N].mp3` | 렌더러가 URL을 계산할 수 있다. 아랍어 모음부호(365개)·공백(28개)이 파일명에서 사라진다 |
| 존재 확인 | `audio/manifest.json` — (언어 × 카테고리) 단위 | 최대 88줄. 404 왕복이 없다 |
| 재생 우선순위 | mp3 → Web Speech → 버튼 미표시 | 점진적으로 채우는 동안에도 기능이 유지된다 |
| 생성 | xAI Grok TTS 플레이그라운드 (무료) | API는 유료다. 배치로 만들어 받고 스크립트가 잘라 배치한다 |

### 왜 404 폴백이 아니라 매니페스트인가

"mp3를 먼저 시도하고 없으면 Web Speech"는 `drills/`의 구글 TTS 분기와 같은 구조다.
그 분기는 로컬·배포 양쪽에서 실패하고 실패까지 144ms가 걸려 연속 재생을 망가뜨렸고,
그래서 단어장에는 가져오지 않았다. 같은 실패를 다시 들이지 않는다.

### 왜 음성인식으로 배치하지 않는가

이 데이터셋은 동음이의가 빽빽하다 — `ja|ひ` 하나가 `자연/sun`·`자연/fire`·`시간/day`
세 곳에 걸리고, 이런 중복이 61건이다. 인식기가 정확히 알아들어도 어느 칸인지 못 정한다.
게다가 고립된 단어는 문맥이 없어 인식률이 가장 나쁘다. **배치는 만들 때 정해져야지
만든 뒤에 되찾을 게 아니다.** 그래서 순서를 진실로 삼는다.

## 현재 상태 (2026-08-07)

```
154 / 2827 개 · audio/ 872KB
완성된 (언어 × 카테고리) — 색깔 8개 언어 전부 (141파일)
나머지 13개는 러시아어 시험 배치가 6개 카테고리에 흩어진 것이라 아직 아무것도 못 채운다
```

색깔 페이지는 8개 언어가 전부 직접 만든 mp3다. `▶ 8개 언어 순서대로`를 누르면
`en→ja→zh→fr→de→es→ru→ar` 순으로 6.6초에 재생된다.
141개 전부 아래 "분할이 어긋났는지 어떻게 아는가" 검사를 통과했다.

흩어진 13개는 파이프라인을 검증하려고 만든 시험 배치(`audio/_batches/ru-sample.*`)의
잔여다. 1음절 5개 + 두 단어 구 5개 + 대조군 4개를 **일부러 골라** 분할이 깨지는지 봤고,
사람이 귀로 들어 단어가 제 자리인지 확인했다. `script` 명령이 만든 게 아니라
손으로 고른 것이라 같은 배치는 재현되지 않는다 — 순서 기록은 json에 남아 있다.
(그 중 `색깔/black.mp3`은 `ru-색깔-0000` 배치와 합쳐져 색깔을 완성했다.)

렌더러(`assets/js/vocab.js`)는 **mp3를 쓸 줄 안다** (2026-08-07). 색깔 페이지는 8개 언어가
전부 mp3로 나가고, 아직 안 채운 카테고리는 Web Speech로 떨어진다.

## 파이프라인

```
vocab/*.json
  ↓ ① scripts/build_vocab_audio.py script <언어>
audio/_batches/<태그>.txt   ← [long-pause]로 이어붙인 배치 대본
audio/_batches/<태그>.json  ← 순서(경로 + 읽을 텍스트) 기록
  ↓ ② 플레이그라운드에 붙여넣고 생성 → 다운로드
  ↓ ③ scripts/build_vocab_audio.py split <태그> <받은파일>
audio/<언어>/<카테고리>/<개념>.mp3
audio/manifest.json  ← 스캔 결과로만 쓴다. 손으로 적지 않는다
```

### 명령어

```bash
# 배치 대본 만들기. 이미 파일이 있는 항목은 자동으로 건너뛴다
python3 scripts/build_vocab_audio.py script ru --category 숫자 --size 7            # 앞에서 7개
python3 scripts/build_vocab_audio.py script ru --category 숫자 --size 7 --offset 7 # 7개 건너뛰고
python3 scripts/build_vocab_audio.py script ru --category 숫자 --size 1            # 한 단어만
python3 scripts/build_vocab_audio.py script ru --all                              # 이미 있는 것도 다시

# 받은 파일 잘라 배치. 태그는 script 가 출력한 것을 그대로 쓴다
python3 scripts/build_vocab_audio.py split ru-숫자-0000 ~/Downloads/tts-....mp3

# 진행 상황 + 매니페스트 다시 쓰기
python3 scripts/build_vocab_audio.py status
```

태그는 `<언어>-<카테고리>-<offset 4자리>`다(`--category` 없이 뽑으면 카테고리 자리가 `all`).
**카테고리를 태그에 넣는 이유** — `<언어>-<offset>`만 쓰던 때, 색깔을 끝내고 숫자를 뽑자
`ja-0004`가 두 카테고리에 각각 존재해 어느 대본인지 알 수 없었다. 잘못 split 하면
색깔 mp3 자리에 숫자 소리가 덮인다.

같은 (언어·카테고리·offset)으로 두 번 만들면 덮어쓴다. 한 카테고리의 배치를
**먼저 다 뽑아 둔 뒤** 순서대로 생성한다 — `--offset`이 "아직 파일이 없는 목록" 기준이라
하나를 split 하고 나면 뒤 배치의 offset이 밀리기 때문이다.

### manifest.json 규칙

```json
{ "ru": ["색깔", "숫자"], "ja": [], "ar": [] }
```

**그 (언어 × 카테고리)의 파일이 하나도 빠짐없이 있을 때만 카테고리 이름이 들어간다.**
하나라도 없으면 배열에서 빠진다. 렌더러는 이 목록만 보고 mp3를 쓸지 정하므로,
파일 하나가 비어 있는데 카테고리가 등재되면 그 자리에서 소리가 안 난다.
`status`와 `split`이 끝날 때 스캔해서 다시 쓴다 — 손으로 고치지 않는다.

플레이그라운드 설정 — Output format `MP3`, Streaming optimization `Quality`,
Text normalization `ON`(숫자 카테고리 아랍어 보조어가 `٠`·`١٠٠` 같은 숫자 글자다).

Sample rate와 Bit rate는 **수치가 아니라 골라 놓은 등급**이다.
Sample rate `Telephony · Wideband · Broadcast · High quality · CD quality · Studio`,
Bit rate `Low · Standard · High · Very high · Max`. **가장 높은 쪽으로 둔다** —
`split`이 어차피 22.05kHz·32kbps 모노로 재인코딩하므로 원본이 좋을수록 손해가 없다.

**언어는 고를 수 없다 — 자동 감지다.** 키릴·아랍·한자는 안전하지만 **라틴 문자 언어
(en·fr·de·es)는 고립된 단어 목록이라 오판 여지가 있어 결과를 확인해야 한다.**

## 러시아어 14개 시험에서 측정한 것 (2026-08-07)

파일: 18.5초, mp3 96kbps 모노 24kHz, 217KB. 1음절 단어와 두 단어 구를 일부러 섞었다.

```
[long-pause] 실제 길이     0.33 ~ 1.27초   ← 일정하지 않다. 4배 차이
단어 내부 최장 무음        0.171초
안전 임계 구간             0.18 ~ 0.32초   ← 약 2배 여유
분할 결과                  14조각 (기대와 일치)
묵음 제거 후 평균          3.25KB · 0.40~1.24초
```

**고정 임계는 쓰지 않는다.** 처음 잡은 0.5초로는 경계가 10개만 잡혀 실패했다.
스크립트가 0.60→0.10초를 훑어 기대 조각 수와 맞는 값을 스스로 고르고, 맞는 값이
없으면 멈춘다. 조용히 어긋나는 경우가 없다.

처음에는 배치 크기로 40개 안팎을 권했지만, 색깔 8개 언어를 받아 보고 **7개**로 내렸다.
아래 "무음이 짧은 언어"를 보라 — 40개였다면 어긋난 5건 때문에 매번 40개를 다시 만들어야 했다.

## 무음이 짧은 언어 — 배치를 쪼갠다 (2026-08-07)

색깔 카테고리를 8개 언어로 받아 보니 **조각 수가 맞아도 어긋난 배치가 있었다.**

| 언어 | 결과 |
|---|---|
| ru 14 · en 12 | 임계 범위 0.18~0.24초로 넉넉히 맞았다. 검사도 통과 |
| ja 23 | 맞는 임계가 **한 단계**(0.18초)뿐. 실제로 어긋났다 |
| fr 13 · es 16 | 맞는 임계 2단계. 한 조각이 두 단어를 물었다 |
| zh 21 | 경계가 19개에서 22개로 건너뛰어 **20개가 되는 임계가 없다** |
| de 14 · ar 26 | 12→14, 24→26. 딱 하나 차이로 비껴간다 |

원인은 `[long-pause]` 하나가 만드는 무음이 언어마다 다르다는 것이다. 중국어는 음절이
짧아 항목 사이 무음이 0.14~0.40초까지 줄고, 단어 내부 쉼과 겹친다.

### `[long-pause]`를 두 번 겹치면 안 된다

무음을 벌리려고 `[long-pause][long-pause]`로 바꿔 중국어 21개를 다시 받아 봤다.

```
길이   15.2초 → 37.6초   (2.5배)
경계   최대 24개 → 최대 17개   (오히려 줄었다)
```

늘어난 22초가 무음이 아니라 연속 발화다 — **태그로 인식되지 않고 글자로 읽힌다.**
`--pause` 옵션은 그래서 도로 뺐다.

### 배치를 쪼갠다 — 7개가 실용적인 크기다

남은 방법은 한 배치의 항목 수를 줄이는 것이다. 조각이 7개면 맞춰야 할 경계가 6개뿐이라
어긋날 여지가 그만큼 준다. 그래도 안 되면 `--size 1`로 한 단어씩 받는다 — 경계가
0개라 반드시 성공한다.

```bash
python3 scripts/build_vocab_audio.py script zh --category 색깔 --size 7 --offset 0
python3 scripts/build_vocab_audio.py script zh --category 색깔 --size 7 --offset 7
python3 scripts/build_vocab_audio.py script zh --category 색깔 --size 7 --offset 14
```

`--offset`은 **아직 파일이 없는 목록** 기준이라, 셋을 **먼저 다 뽑아 둔 뒤** 생성한다.
하나를 split 하고 나면 뒤 배치의 offset이 밀린다.

색깔 8개 언어를 7개씩 받은 실적 — **21배치 중 19개가 한 번에 통과**했다.
실패 2개는 일본어였고, 4·3·1·1로 더 잘게 쪼개 해결했다. 그 밖에 조각 수는 맞았지만
한 조각이 두 발화를 문 경우가 3건(de·es·ar 각 1개) 있었고 그 파일만 `--size 1`로 다시 받았다.
**배치가 40개였다면 이 5건 때문에 매번 40개를 통째로 다시 만들어야 했다.**

### `--rank` 는 최후수단이다

맞는 임계가 없을 때 무음이 긴 순으로 필요한 개수만 고르는 `split --rank`가 있다.
zh·de·ar에 써 봤더니 "남긴 무음 최소"와 "버린 무음 최대"의 차이가 +0.00~+0.01초였고,
**세 배치 모두 어긋났다.** 차이가 0.1초도 안 되면 쓰지 않는다. 기본값은 꺼져 있다.

## 분할이 어긋났는지 어떻게 아는가

조각 수가 맞아도 어긋난다. 사람이 듣기 전에 두 가지로 걸러낼 수 있다.

```bash
# 조각마다 크기와 내부 무음을 본다. 정상이면 아무것도 안 나온다
python3 - <<'PY'
import json, subprocess, re
from pathlib import Path
tag = "zh-숫자-0000"
for it in json.load(open(f"audio/_batches/{tag}.json")):
    p = Path(it["path"]); size = p.stat().st_size
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(p),
                        "-af", "silencedetect=noise=-40dB:d=0.20", "-f", "null", "-"],
                       capture_output=True, text=True)
    gaps = re.findall(r"silence_duration: ([\d.]+)", r.stderr)
    if size < 600 or gaps:
        print(f"{p.name}({it['text']}) {size}B 무음{gaps}")
PY
```

- **600바이트 미만** = 무음 조각. 경계를 단어 한가운데서 잡았다는 뜻이다
- **내부 무음 0.20초 이상** = 그 조각이 두 단어를 물고 있다

`d`를 0.12초까지 낮추면 `gray`의 `/g/` 같은 파열음 무음까지 잡히므로 **0.20초를 쓴다.**
길이도 함께 본다 — 음절 수와 어긋나면(2음절이 3.1초) 의심한다.

## 남은 일

### 1. 러시아어 한 카테고리를 끝까지 채운다 — 완료 (2026-08-07)

색깔 11개념·**15파일**(alt 포함). `ru-색깔-0000` 배치 14개 + 기존 `black.mp3`.

```
임계 0.12초 선택 (맞는 범위 0.1~0.16초, 4단계)
항목 사이 무음 0.17~0.52초 · 조각 14개 (기대와 일치)
조각 길이 0.36~0.67초 · 전부 4.0KB
```

**임계 범위가 좁다** — 시험 배치는 0.18~0.32초로 2배 여유였는데 이번은 0.1~0.16초다.
항목 사이 최소 무음 0.17초가 시험에서 잰 단어 내부 최장 무음 0.171초와 거의 붙었다.
조각 수는 맞았고 길이가 음절 수와 어울리지만(коричневый 0.67 / карий 0.36),
**같은 여유로 40개짜리를 돌리면 깨질 수 있다.** 배치가 커지면 임계 범위를 먼저 본다.

받은 파일 이름이 `tts-ara-…`였다 — 플레이그라운드가 언어를 자동 감지하므로
러시아어를 제대로 읽었는지는 **사람이 들어야 안다.**

### 2. 렌더러가 mp3를 쓰게 한다 — 완료 (2026-08-07)

`assets/js/vocab.js`에 들어간 것:

| 이름 | 하는 일 |
|---|---|
| `audioCats` | `/audio/manifest.json` 내용. `boot()`에서 받고 실패하면 `{}` |
| `STEM` | `root.dataset.src`에서 꺼낸 파일명. 경로의 카테고리 조각 |
| `hasAudio(lang)` | 매니페스트에 그 언어의 `STEM`이 있는가 |
| `audible(lang)` | `hasAudio(lang) || speakable.has(lang)`. 버튼 유무·개수 기준 |
| `playFile(lang, id, alt)` | `/audio/<lang>/<STEM>/<id>[-N].mp3` 를 `new Audio`로 재생 |
| `say(lang, entry, id, alt)` | mp3가 있으면 `playFile`, 없으면 `utter` |
| `playing` | 재생 중인 `Audio`. `stopSpeaking()`이 `pause()` 한다 |

`entryLine`·`langRow`·`playBtn`·`playOne`은 개념 id와 alt 인덱스를 받도록 인자가 늘었다.
alt 인덱스는 `entry.alt` 배열 순서 + 1 — `build_vocab_audio.py`의 `enumerate([entry, *alt])`와 같다.

**경로에는 JSON의 `category` 값이 아니라 파일명(stem)을 쓴다.** 둘이 다른 카테고리가
하나 있다 — `기본_형용사.json`의 `category`는 `"기본 형용사"`(공백)인데 경로는
`audio/ru/기본_형용사/...`다. 스크립트가 `path.stem`을 쓰기 때문이다.

검증한 것 — 색깔 페이지에서 러시아어 버튼을 누르면 서버 로그에
`GET /audio/ru/%EC%83%89%EA%B9%94/brown.mp3`, `…/brown-1.mp3`(alt)가 찍히고
재생이 끝나면 `playing` 표시가 풀린다. 매니페스트가 비어 있던 때는 같은 페이지에서
버튼 141개가 그대로 나오고 콘솔 오류가 없었다 — Web Speech 경로에 회귀가 없다.

### 3. 나머지 카테고리 ← 지금 여기

색깔은 8개 언어를 다 채웠다. 다음 카테고리도 같은 방식이다 — `--size 7`로 쪼개
필요한 offset을 **먼저 다 뽑아 둔 뒤** 순서대로 생성한다.

```bash
python3 scripts/build_vocab_audio.py status                  # 남은 개수 확인
python3 scripts/build_vocab_audio.py script ru --category 숫자 --size 7 --offset 0
```

카테고리별 남은 양(8개 언어 합계, `--size 7` 기준 배치 수):

| 카테고리 | 남은 개수 | 배치 |
|---|---:|---:|
| 숫자 | 140 | 20 |
| 가족 | 152 | 22 |
| 동물 | 184 | 27 |
| 시간 | 198 | 29 |
| 음식 | 250 | 36 |
| 스포츠 | 275 | 40 |
| 기본_형용사 | 294 | 42 |
| 신체 | 301 | 44 |
| 자연 | 361 | 52 |
| 동작 | 518 | 74 |
| **합계** | **2673** | **386** |

작은 것부터(숫자 → 가족 → 동물) 가면 카테고리가 하나씩 완성되어 매니페스트에 바로 뜬다.

**숫자 카테고리는 Text normalization을 켜야 한다** — 아랍어 보조어가 `٠`·`١٠٠` 같은
숫자 글자다.

#### 읽기가 틀리는 단어는 따로 뽑는다

스페인어 `blanco`를 목록 맨 앞에 두면 `b.l.blanco`처럼 철자를 읊는다. 이런 단어는
배치에서 떼어 혼자 생성한다. 조각이 1개인 배치도 `split`이 처리한다 — 경계 0개를 찾으면
되므로 오히려 임계 여유가 가장 넓다(실측 22단계).

```bash
python3 scripts/build_vocab_audio.py script es --category 색깔 --size 1     # blanco 만
python3 scripts/build_vocab_audio.py script es --category 색깔 --offset 1   # 나머지 16개
```

`--offset`은 **아직 파일이 없는 목록** 기준이다. blanco를 먼저 채우고 나면 offset 0이
negro로 밀리므로, 두 대본을 **먼저 다 뽑아 둔 뒤** 생성한다.

## 주의

발화 텍스트 규칙은 `assets/js/vocab.js`의 `speakText()`와
`scripts/build_vocab_audio.py`의 `speak_text()`가 **반드시 같아야 한다**.
일본어는 `rom`의 かな, 러시아어는 강세 기호 U+0301 제거, 아랍어는 모음부호 유지.
한쪽만 고치면 파일명은 그대로인데 내용이 달라져 조용히 어긋난다.

`vocab/*.json`에 개념을 추가·삭제하면 오디오 경로도 따라 바뀐다. 개념 `id`를 바꾸면
기존 mp3가 고아가 되므로, `status`로 개수가 맞는지 확인한다.

## 이어서 작업할 때 읽을 것

이 문서만으로 이어갈 수 있게 썼지만, 실제로 손대기 전에 확인할 파일들이다.

| 파일 | 왜 |
|---|---|
| `scripts/build_vocab_audio.py` | 세 명령의 실제 동작. 특히 `speak_text()`와 `pick_threshold()` |
| `assets/js/vocab.js` | 위 "렌더러가 mp3를 쓰게 한다"의 대상. 발음 관련 함수는 파일 앞쪽에 모여 있다 |
| `audio/manifest.json` | 지금 무엇이 완성됐는지 |
| `audio/_batches/*.json` | 과거 배치가 어떤 순서였는지 |
| `CLAUDE.md`의 `vocab/ 발음 규칙` | 두 곳 동기화 경고 |

**소리가 맞는지는 사람만 확인할 수 있다.** 스크립트는 조각 수만 검증한다.
새 언어의 첫 배치는 반드시 몇 개를 들어 보고 진행한다.
