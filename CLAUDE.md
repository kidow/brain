# CLAUDE.md

## README 자동 연결 규칙

> **CRITICAL** — `notes/`, `sheets/`, `drills/` 또는 `vocab/`에 파일을 추가·삭제한 응답에서 반드시 같은 응답 안에 README 두 파일을 업데이트한다. 커밋 전 체크리스트:
> 1. `README.md` 해당 섹션에 링크 추가/삭제했는가?
> 2. `README.ko.md` 해당 섹션에 링크 추가/삭제했는가?
> 3. 두 파일 모두 같은 커밋에 포함했는가?
> 4. (notes/, sheets/) 그룹 내 나열 순서가 알파벳/추가순이 아니라 **배움의 흐름 순**인가?
> 5. (notes/) `_data/notes_order.yml`도 같은 순서로 함께 갱신했는가?

`notes/`, `sheets/`, `drills/` 또는 `vocab/` 폴더에 파일이 추가되거나 삭제되면 **반드시** `README.md`와 `README.ko.md` 양쪽의 해당 섹션을 동기화한다.

### notes/ 규칙

- 섹션: `README.md` → `## Notes`, `README.ko.md` → `## 노트`
- URL 패턴: `https://brain.dongwook.kim/notes/파일명` (`.md` 확장자 제거)
- 파일명의 `_`는 링크 표시 텍스트에서 공백으로 변환한다. 예: `일본어_문자의_특징` → `일본어 문자의 특징`
- 언어 계열 노트는 해당 언어 그룹 아래에 배치한다. 새 언어는 그룹을 신설한다.
- 언어 외 주제(음악, 예술, 과학 등)는 적절한 그룹 아래 배치하거나 새 그룹을 신설한다.
- **그룹 내 나열 순서는 알파벳순·추가된 순서가 아니라 실제 배움의 흐름(입문→기초→심화→응용) 순으로 정렬한다.** 새 노트를 끼워 넣을 위치는 "이 개념을 배우기 전에 뭘 알아야 하는가"로 판단한다. 순서를 바꾸면 같은 그룹의 기존 링크 순서도 재배치한다.

### sheets/ 규칙

- 섹션: `README.md` → `## Cheat Sheets`, `README.ko.md` → `## 치트시트`
- URL 패턴: `https://brain.dongwook.kim/sheets/파일명.html` (확장자 유지)
- 파일명의 `_`는 링크 표시 텍스트에서 공백으로 변환한다. 예: `러시아어_치트시트` → `러시아어 치트시트`
- 언어별 그룹으로 구분한다. 새 언어는 그룹을 신설한다.
- notes/ 규칙과 동일하게, 그룹 내 나열 순서는 배움의 흐름(입문→기초→심화→응용) 순으로 정렬한다.

### sheets/ head 태그 규칙

모든 치트시트 HTML 파일의 `<head>`에는 다음 태그를 반드시 포함한다. `<meta charset="UTF-8">` 바로 다음에 삽입한다.

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#ffffff">
```

### sheets/ 색상 규칙

- 모든 치트시트 HTML 파일은 **다크 모드 고정**으로 작성한다.
- 기본 색상: `background: #0f172a`, `color: #e2e8f0`, 보조 배경 `#1e293b`, 테두리 `#334155`, 흐린 텍스트 `#94a3b8`
- 강조색(accent): `#60a5fa` (파란색 계열)
- 라이트 배경(`#fff`, `#f8f8f8` 등) 사용 금지. 토글 버튼 없음.

### sheets/ 레이아웃 규칙

모든 치트시트 HTML 파일은 다음 레이아웃을 준수한다.

- `body`에 `max-width: 800px` + `margin: 0 auto` + `padding: 1.5rem 1.25rem` 적용
- 모바일/태블릿 우선: 좌우 여백으로 콘텐츠가 중앙 정렬되어 보임
- `@media (max-width: 600px)`에서 `padding: 1rem 1rem` 으로 축소
- `@media print`에서 `padding: 0.5cm` 으로 축소

### drills/ 규칙

- 섹션: `README.md` → `## Drills`, `README.ko.md` → `## 드릴`
- URL 패턴: `https://brain.dongwook.kim/drills/파일명.html` (확장자 유지)
- 파일명의 `_`는 링크 표시 텍스트에서 공백으로 변환한다.
- 언어별 그룹으로 구분한다. 새 언어는 그룹을 신설한다.
- 드릴 하나는 `파일명.html`(SM-2 복습 UI) + `파일명.json`(단어 데이터) 쌍으로 구성한다.
- 진행 상태(간격·난이도 등 SM-2 상태)는 **localStorage에만** 저장한다. 기기·브라우저 간 동기화는 하지 않는다 — 이 저장소는 어휘 원본(JSON)만 git으로 추적하고, 복습 진행률은 추적하지 않는다.
- 색상·레이아웃은 sheets/ 규칙(다크 모드 고정, `#0f172a`/`#1e293b`/`#334155`/`#94a3b8`/`#60a5fa`, `max-width: 800px`)을 그대로 따른다.
- head 태그는 sheets/ head 태그 규칙과 동일하게 포함한다.
- 단어 데이터는 날조하지 않는다 — 반드시 검증 가능한 출처(공개 데이터셋 등)에서 가져오고, 출처를 페이지 하단에 명시한다.

### vocab/ 규칙

- 섹션: `README.md` → `## Vocabulary`, `README.ko.md` → `## 단어장`
- URL 패턴: `https://brain.dongwook.kim/vocab/파일명.html` (확장자 유지)
- 카테고리 하나는 `카테고리.html`(껍데기) + `카테고리.json`(데이터) 쌍으로 구성한다.
- 렌더러는 `assets/js/vocab.js`, 스타일은 `assets/css/vocab.css` **각 한 벌을 공유한다**. 카테고리마다 인라인 `<script>`·`<style>`을 복제하지 않는다(`drills/`와 다른 점). 카테고리 HTML은 head 태그 + `<div id="vocab" data-src="...">` + 스크립트 두 줄이 전부다.
- 새 카테고리를 추가하면 `assets/js/vocab.js`의 `CATEGORIES` 배열에도 한 줄 넣는다. 이 배열이 상단 카테고리 네비게이션의 원본이며, **미완성 카테고리는 넣지 않는다**(비활성 표시가 아니라 아예 숨김).
- 대상 언어와 표시 순서는 전 카테고리 고정: **영 · 일 · 중 · 프 · 독 · 스 · 러 · 아** (`en ja zh fr de es ru ar`).
- 카테고리 나열 순서는 배움의 흐름 순으로 정렬한다(`notes/`·`sheets/` 규칙과 동일).
- 색상·레이아웃·head 태그는 `sheets/` 규칙을 그대로 따른다.

#### vocab/ 데이터 규칙

- **단어 데이터를 날조하지 않는다.** 개념 선정과 단어를 2층으로 나눠 출처를 남긴다.
  - 개념 선정 — Swadesh 207, Berlin & Kay(1969) 같은 표준 목록. `lists[]`에 기록한다.
    - 표준 목록에 없는 주제(스포츠 등)는 **표준화된 초급 교육과정**(중국어 HSK, 일본어 JLPT)을 근거로 쓴다. 그래도 빠지는 항목은 직접 선정하되 **선정 기준을 `sources.concepts`에 반드시 적는다**.
  - 단어 — English Wiktionary 등 검증 가능한 사전. 확인 못 한 단어는 넣지 않는다.
- 출처는 JSON의 `sources` 객체에 적고, 렌더러가 페이지 하단에 그대로 표시한다.
- 한글 음차(`kor`)는 국립국어원 외래어 표기법을 적용한 값이지 등재 표기가 아니다. 이 사실을 `sources`에 반드시 명시한다.
- **아랍어는 `kor`를 생략한다** — 외래어 표기법에 아랍어 세칙이 없다.
- **프랑스어·스페인어는 `rom`을 생략한다** — 위키낱말사전이 발음을 템플릿으로 자동 생성해 원문에서 IPA를 못 긁는다. 영어·독일어는 원문에 IPA가 있어 수록한다.
- 중국어는 **간체자**로 적는다(`drills/중국어_HSK_어휘` 표기와 일치).
- 언어끼리 1:1로 안 맞는 경우:
  - `alt[]` — 같은 언어 줄 안에 보조어를 병기하고 `label`로 구분한다(성·수 변화, 의미 분화, 외래어 등).
  - `notes[]` — 줄 라벨로 안 담기는 배경은 카드 하단 메모로. **필요한 개념에만** 붙인다.
- 개념 `id`는 영어 슬러그다. URL 앵커(`vocab/색깔.html#black`)가 되고 표준 목록과 1:1로 대응된다. 파일명은 한국어를 유지한다.

#### vocab/ 발음 규칙

- 발화 텍스트 변환은 `assets/js/vocab.js`의 `speakText()`와 `scripts/build_vocab_audio.py`의 `speak_text()`에 **같은 로직이 두 벌 있다**. 일본어는 `rom`의 かな, 러시아어는 강세 기호 U+0301 제거, 아랍어는 모음부호 유지. **한쪽만 고치면 안 된다** — 파일명은 그대로인데 내용이 달라져 조용히 어긋난다.
- 직접 만든 mp3는 `audio/<언어>/<카테고리>/<개념>[-N].mp3`에 둔다. 존재 여부는 `audio/manifest.json`(언어 × 카테고리 단위)으로만 판단하고 404 폴백은 쓰지 않는다. 설계와 측정값은 [audio/PLAN.md](audio/PLAN.md)에 있다.

### levels.md 규칙

- 섹션: `README.md` → `## Levels`, `README.ko.md` → `## 수준 기록`
- URL: `https://brain.dongwook.kim/levels` (단일 링크, 목록 아님)
- `levels.md` 내용이 변경되어도 README의 링크는 수정하지 않는다.

### notes/ 파일 내 섹션 정렬 규칙

- 새 레슨은 파일 **맨 아래에 추가(append)**한다.
- 섹션 구분자는 `---`이며, 파일 위→아래 = 처음 배운 것→최근 배운 것 순서를 유지한다.
- 덮어쓰기(전체 교체) 시에도 이 순서를 보존한다.

### notes/ 페이지네이션 동기화 규칙

- 모든 notes/ 페이지 하단에는 `_layouts/note.html`이 렌더링하는 이전/다음 페이지네이션이 붙는다. 순서 데이터 원본은 `_data/notes_order.yml`이며, README.md `## Notes` 섹션과 **동일한 그룹·동일한 순서**를 유지해야 한다.
- notes/ 파일을 추가·삭제·재배치할 때는 README 두 파일과 함께 `_data/notes_order.yml`도 같은 커밋에서 갱신한다. 형식:
  ```yaml
  - name: "그룹명 (README 그룹명과 동일)"
    items:
      - title: "표시 제목 (README 링크 텍스트와 동일)"
        path: "notes/그룹폴더/파일명"  # .md 확장자 제외
  ```
- 페이지네이션은 **같은 그룹 안에서만 순환**한다(그룹 경계를 넘어가지 않음). 그룹에 항목이 1개뿐이면 네비게이션 자체가 표시되지 않는다 — 정상 동작이며 별도 처리 불필요.
- 새 언어/그룹 신설 시 `_data/notes_order.yml`에도 새 그룹 블록을 추가한다.

### 공통 규칙

- `.gitkeep` 파일은 목록에 포함하지 않는다.
- 파일 추가/삭제 후 README 수정을 커밋에 함께 포함한다.
- `README.md`(영문)와 `README.ko.md`(한국어) 양쪽 모두 업데이트한다.
