# notes 오디오 파이프라인 계획

이동 시간에 이어폰으로 notes를 듣기 위한 설계. 이 문서는 계획만 담고 있으며, 구현은 아직 시작하지 않았다.

## 결정 사항

| 항목 | 결정 | 근거 |
|---|---|---|
| 소비 경로 | 노트 페이지 `<audio>` 재생기 **only** (팟캐스트 RSS 없음) | LTE로 스트리밍하면 지하철에서도 문제없음. 데이터는 시간당 약 14MB |
| 재생기 기능 | 자동 연속재생 + 이어듣기 + 잠금화면 컨트롤 | 이 셋이 없으면 6분마다 폰을 꺼내야 해서 출퇴근 청취가 성립하지 않음 |
| 연속재생 범위 | `_data/notes_order.yml` **그룹 안에서만**, 끝나면 정지 | 기존 페이지네이션 규칙과 동일. 러시아어 듣다 회계학으로 넘어가지 않음 |
| 대상 | `notes/` 239개만 | sheets는 표 위주라 낭독에 부적합하고 내용도 notes와 겹침. drills는 포맷이 완전히 다른 별개 제품 |
| 대본 생성 | LLM 재작성 (기계 변환 아님) | 표·별표·샤프를 그대로 읽으면 못 들음. 자연스러운 톤이 목표 |
| 대본 실행 | **로컬** mlx-lm (M5 24GB) | 비용 0, 외부 전송 없음. 클라우드 대비 5시간 정도 더 걸리지만 자고 일어나면 끝남 |
| 대본 저장 | `_audio/scripts/<노트경로>.txt`, **git 커밋** | 로컬 LLM은 출력이 매번 달라서 이게 유일한 재현 수단. 텍스트라 전체 1MB 안팎 |
| mp3 호스팅 | Cloudflare R2 + `audio.dongwook.kim` | `r2.dev`는 문서상 rate-limited·개발 전용. partial(CNAME) 셋업이면 네임서버 이전 불필요 |
| 첫 실행 | Languages — Russian 22개 파일럿 | 파이프라인 전체를 짧게 검증한 뒤 나머지 217개 확장 |

## 미결정 — 스파이크로 처리

두 가지를 샘플 청취로 함께 결정한다. 노트 3개(어학 표 위주 1 + 산문 1 + 코드블록 포함 1)를 후보 조합으로 돌려 비교한다.

**1. 대본 LLM (로컬)**
- `mlx-community/Qwen3.5-35B-A3B-MLX-4bit` — MoE, Q4에서 약 20GB, M4 Pro 기준 ~32 tok/s. MLX 변환본 존재 확인됨
- `mlx-community/Qwen3.5-9B-MLX-4bit` — 메모리 여유 크고 빠름. 표 풀어쓰기에 충분한지 확인 필요
- 한국어 특화 모델 (Kanana-2 / EXAONE) — **MLX 변환본 존재 여부 미확인**. 없으면 직접 변환하거나 llama.cpp

**2. TTS 엔진**
- **1순위: Chatterbox Multilingual V3** (https://github.com/resemble-ai/chatterbox, MIT, 25.8k★) — 지원 23개 언어에 이 저장소가 다루는 ko·ru·de·ja·zh·ar·fr·es·en이 **전부** 포함. 한 모델로 한국어 나레이션과 외국어 원어를 모두 처리 가능
  - 설치 전 청취: https://resemble-ai.github.io/chatterbox_demopage/ , https://huggingface.co/spaces/ResembleAI/Chatterbox-Multilingual-TTS
- 대안: mlx-audio + Qwen3-TTS (Apple Silicon 네이티브, ko 지원 명시, ru·ar 커버 불명), Higgs Audio v3 (100개 언어, 4B로 무거움)

## 파이프라인

```
notes/**/*.md (239개)
  ↓ ① 로컬 LLM 재작성
_audio/scripts/**/*.txt   ← git 커밋, 상단에 원문 md의 sha256 기록
  ↓ ② TTS
  ↓ ③ ffmpeg 인코딩 (32kbps 모노)
*.mp3 (약 400~700MB)
  ↓ ④ R2 업로드
https://audio.dongwook.kim/notes/<그룹>/<파일명>.mp3
  ↓ ⑤ _layouts/note.html이 page.path로 URL 계산
브라우저 재생기
```

### 증분 빌드

대본 파일 상단에 원문 md의 sha256을 기록한다. 빌드 시 현재 md 해시와 비교해 **다른 노트만** ①~④를 다시 돌린다. 노트 하나 고쳤을 때 전체 5시간을 다시 돌리지 않기 위한 장치이며, 없으면 파이프라인이 사실상 일회용이 된다.

### 예상 소요

- 원문 852,922자 / 노트 평균 3,569자
- 대본 생성: 노트당 출력 약 2,400토큰. 30 tok/s 기준 노트당 80초 → 전체 약 5시간 (M5가 더 빠르면 2~3시간)
- 낭독 분량: 40~57시간 (LLM이 표를 문장으로 풀면 더 늘어날 수 있음)
- mp3 용량: 32kbps 모노 기준 약 400~700MB

## 구현 순서

1. **스파이크** — 노트 3개로 LLM 후보 × TTS 후보 샘플 생성, 청취 후 조합 확정
2. **R2 셋업** — Cloudflare 계정, 도메인 partial(CNAME) 추가, 버킷 생성, `audio.dongwook.kim` 연결, 업로드용 API 토큰 발급
3. **빌드 스크립트** (`scripts/build_audio.py`) — 대본 생성 → TTS → ffmpeg → R2 업로드. 해시 기반 증분 처리
4. **재생기** (`_layouts/note.html` + `assets/js/audio-player.js`) — md 239개는 건드리지 않는다
   - `<h1>brain</h1>` 바로 아래에 `<audio>` 블록 삽입 (레이아웃 1곳만 수정)
   - 곡 종료 시 `_data/notes_order.yml` 기준 같은 그룹의 다음 노트 mp3로 `src` 교체 (페이지 이동 없음)
   - localStorage에 재생 위치 저장 — [assets/js/visit-tracker.js](../assets/js/visit-tracker.js)의 스크롤 위치 저장 패턴을 그대로 따른다
   - MediaSession API로 잠금화면에 제목·이전/다음 노출
5. **파일럿** — Languages — Russian 22개 생성·업로드, 실제 출퇴근에 청취
6. **전체 확장** — 나머지 217개

## 남은 작업

- `CLAUDE.md`에 오디오 규칙 추가: notes를 추가·삭제·재배치할 때 대본과 mp3도 함께 갱신해야 한다는 항목. 지금은 README 두 개와 `notes_order.yml`만 규칙에 걸려 있음
- `.gitignore`: `_audio/scripts/`는 커밋하되 중간 산출물(wav 등)은 제외
- Cloudflare partial(CNAME) 셋업의 플랜 요건 확인 — 문서상 가능하다고 되어 있으나 실제 셋업 시 확인 필요

## 검증하지 못한 것

- **토큰 수 추정치**: 이 환경에 `ANTHROPIC_API_KEY`도 `ant` CLI도 없어 `count_tokens`를 실행하지 못했다. 852,922자 → 50~70만 토큰은 한국어 토큰 밀도 가정에 기반한 추정
- **TTS·LLM 품질**: 저장소 문서와 벤치마크 기준이며 실제로 들어본 결과가 아니다. 스파이크에서 확인
- **한국어 특화 모델의 MLX 변환본 존재 여부**
