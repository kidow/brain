# CLAUDE.md

## README 자동 연결 규칙

> **CRITICAL** — `notes/` 또는 `sheets/`에 파일을 추가·삭제한 응답에서 반드시 같은 응답 안에 README 두 파일을 업데이트한다. 커밋 전 체크리스트:
> 1. `README.md` 해당 섹션에 링크 추가/삭제했는가?
> 2. `README.ko.md` 해당 섹션에 링크 추가/삭제했는가?
> 3. 두 파일 모두 같은 커밋에 포함했는가?

`notes/` 또는 `sheets/` 폴더에 파일이 추가되거나 삭제되면 **반드시** `README.md`와 `README.ko.md` 양쪽의 해당 섹션을 동기화한다.

### notes/ 규칙

- 섹션: `README.md` → `## Notes`, `README.ko.md` → `## 노트`
- URL 패턴: `https://brain.dongwook.kim/notes/파일명` (`.md` 확장자 제거)
- 파일명의 `_`는 링크 표시 텍스트에서 공백으로 변환한다. 예: `일본어_문자의_특징` → `일본어 문자의 특징`
- 언어 계열 노트는 해당 언어 그룹 아래에 배치한다. 새 언어는 그룹을 신설한다.
- 언어 외 주제(음악, 예술, 과학 등)는 적절한 그룹 아래 배치하거나 새 그룹을 신설한다.

### sheets/ 규칙

- 섹션: `README.md` → `## Cheat Sheets`, `README.ko.md` → `## 치트시트`
- URL 패턴: `https://brain.dongwook.kim/sheets/파일명.html` (확장자 유지)
- 파일명의 `_`는 링크 표시 텍스트에서 공백으로 변환한다. 예: `러시아어_치트시트` → `러시아어 치트시트`
- 언어별 그룹으로 구분한다. 새 언어는 그룹을 신설한다.

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

### levels.md 규칙

- 섹션: `README.md` → `## Levels`, `README.ko.md` → `## 수준 기록`
- URL: `https://brain.dongwook.kim/levels` (단일 링크, 목록 아님)
- `levels.md` 내용이 변경되어도 README의 링크는 수정하지 않는다.

### notes/ 파일 내 섹션 정렬 규칙

- 새 레슨은 파일 **맨 아래에 추가(append)**한다.
- 섹션 구분자는 `---`이며, 파일 위→아래 = 처음 배운 것→최근 배운 것 순서를 유지한다.
- 덮어쓰기(전체 교체) 시에도 이 순서를 보존한다.

### 공통 규칙

- `.gitkeep` 파일은 목록에 포함하지 않는다.
- 파일 추가/삭제 후 README 수정을 커밋에 함께 포함한다.
- `README.md`(영문)와 `README.ko.md`(한국어) 양쪽 모두 업데이트한다.
