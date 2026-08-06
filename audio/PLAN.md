# 단어장 발음 오디오 계획

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
14 / 2827 개 — 전부 러시아어, 6개 카테고리에 흩어져 있다
완성된 (언어 × 카테고리) 없음 → manifest.json 은 8개 언어 모두 빈 배열
```

이 14개는 파이프라인을 검증하려고 만든 시험 배치(`audio/_batches/ru-sample.*`)다.
1음절 5개 + 두 단어 구 5개 + 대조군 4개를 **일부러 골라** 분할이 깨지는지 봤고,
사람이 귀로 들어 단어가 제 자리인지 확인했다. `script` 명령이 만든 게 아니라
손으로 고른 것이라 같은 배치는 재현되지 않는다 — 순서 기록은 json에 남아 있다.

렌더러(`assets/js/vocab.js`)는 **아직 mp3를 모른다.** Web Speech만 쓴다.

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
python3 scripts/build_vocab_audio.py script ru                    # 남은 것 앞에서 40개
python3 scripts/build_vocab_audio.py script ru --size 20          # 20개씩
python3 scripts/build_vocab_audio.py script ru --category 색깔     # 특정 카테고리만
python3 scripts/build_vocab_audio.py script ru --offset 40        # 남은 목록에서 40개 건너뛰고
python3 scripts/build_vocab_audio.py script ru --all              # 이미 있는 것도 다시

# 받은 파일 잘라 배치. 태그는 script 가 출력한 것을 그대로 쓴다 (예: ru-0000)
python3 scripts/build_vocab_audio.py split ru-0000 ~/Downloads/tts-....mp3

# 진행 상황 + 매니페스트 다시 쓰기
python3 scripts/build_vocab_audio.py status
```

태그는 `<언어>-<offset 4자리>` 형식으로 자동 생성된다. 같은 offset으로 두 번 만들면
덮어쓰므로, 한 배치를 끝내고 다음 배치를 뽑는 순서로 쓴다.

### manifest.json 규칙

```json
{ "ru": ["색깔", "숫자"], "ja": [], "ar": [] }
```

**그 (언어 × 카테고리)의 파일이 하나도 빠짐없이 있을 때만 카테고리 이름이 들어간다.**
하나라도 없으면 배열에서 빠진다. 렌더러는 이 목록만 보고 mp3를 쓸지 정하므로,
파일 하나가 비어 있는데 카테고리가 등재되면 그 자리에서 소리가 안 난다.
`status`와 `split`이 끝날 때 스캔해서 다시 쓴다 — 손으로 고치지 않는다.

플레이그라운드 설정 — Output format `MP3`, Streaming optimization `Quality`,
Text normalization `ON`(숫자 카테고리 아랍어 보조어가 `٠`·`١٠٠` 같은 숫자 글자다),
Sample rate·Bit rate는 높게 둔다(스크립트가 어차피 재인코딩하므로 원본이 좋을수록 낫다).
언어 선택은 없고 자동 감지다 — 키릴·아랍·한자는 안전하지만 **라틴 문자 언어
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

배치 크기는 **40개 안팎**을 권한다. 14개가 18.5초였으니 40개면 약 1분이다.
한 언어(약 350개)를 통째로 넣으면 10분짜리가 되어 하나만 어긋나도 전체를 다시 만들어야 한다.

## 남은 일

### 1. 러시아어 한 카테고리를 끝까지 채운다

색깔이 11개념·**15파일**(alt 포함)로 가장 작다. 지금 1개(`black.mp3`)만 있다.

```bash
python3 scripts/build_vocab_audio.py script ru --category 색깔
```

끝나면 `manifest.json`에 `"ru": ["색깔"]`이 떠야 한다. 이게 떠야 2번을 검증할 수 있다.

### 2. 렌더러가 mp3를 쓰게 한다

`assets/js/vocab.js`의 현재 구조 — 발음 관련은 이렇게 돼 있다.

| 이름 | 하는 일 |
|---|---|
| `SPEAK_LANG` | 언어 → BCP-47 (`ru` → `ru-RU`) |
| `speakable` (Set) | 이 기기에 음성이 있는 언어. `markSpeakable()`이 채운다 |
| `voicesReady()` | `getVoices()`가 빌 수 있어 목록이 찰 때까지 기다린다 |
| `speakText(lang, entry)` | 읽을 텍스트 (일본어 かな·러시아어 강세 제거) |
| `utter(lang, entry)` | `SpeechSynthesisUtterance` 하나를 재생하는 Promise |
| `playOne(lang, entry, btn)` | 버튼 하나 재생. 누르면 `stopSpeaking()` 후 시작 |
| `playAll(concept, btn)` | 본항만 순서대로. `alt`는 제외 |
| `playBtn(lang, entry)` | 🔊 버튼 생성 |
| `entryLine()` | `speakable.has(lang)`일 때만 버튼을 붙인다 |
| `stopSpeaking()` | `seq += 1` 로 진행 중인 연속 재생을 끊고 `cancel()` |

고칠 지점은 넷이다.

1. `boot()`의 `Promise.all([fetch(src), voicesReady()])`에 `fetch('/audio/manifest.json')`을 더한다.
   매니페스트를 못 받아도 실패하지 않게 `.catch(() => ({}))`로 감싼다.
2. `entryLine()`이 버튼을 붙이는 조건을 `speakable.has(lang) || hasAudio(lang)`로 넓힌다.
   `hasAudio(lang)` = 매니페스트에 그 언어의 현재 카테고리가 들어 있는가.
   **mp3가 있으면 기기에 음성이 없어도 버튼이 나와야 한다** — 지금은 안 나온다.
3. `utter()` 옆에 `playFile(lang, entry, altIndex)`를 만든다. 경로는
   `audio/<lang>/<data.category>/<concept.id>[-N].mp3`이고 `new Audio(url)`로 재생한다.
   `onended`/`onerror`를 같은 Promise로 감싸 `utter()`와 자리를 바꿔 쓸 수 있게 한다.
   이 때문에 `playOne`·`playAll`은 개념·alt 인덱스를 알아야 하므로 인자를 늘려야 한다.
4. `playAll()`의 건너뛰기 조건도 `speakable` 대신 "mp3 또는 음성이 있는가"로 바꾼다.
   버튼 라벨(`▶ N개 언어 순서대로`)의 N도 같은 기준으로 센다.

**경로에는 JSON의 `category` 값이 아니라 파일명(stem)을 쓴다.** 둘이 다른 카테고리가
하나 있다 — `기본_형용사.json`의 `category`는 `"기본 형용사"`(공백)인데 경로는
`audio/ru/기본_형용사/...`다. 스크립트가 `path.stem`을 쓰기 때문이다. 렌더러도
`root.dataset.src`(`/vocab/기본_형용사.json`)에서 파일명을 꺼내 써야 어긋나지 않는다.

### 3. 나머지 언어·카테고리 확장

라틴 문자 언어(en·fr·de·es)는 자동 감지 오판 여지가 있어 첫 배치를 듣고 확인한 뒤 진행한다.

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
