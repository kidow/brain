# CLAUDE.md

## README 자동 연결 규칙

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

### 공통 규칙

- `.gitkeep` 파일은 목록에 포함하지 않는다.
- 파일 추가/삭제 후 README 수정을 커밋에 함께 포함한다.
- `README.md`(영문)와 `README.ko.md`(한국어) 양쪽 모두 업데이트한다.
