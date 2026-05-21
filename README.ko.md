# brain

[English](README.md) · 한국어

내가 배운 것을 쌓아 두는 개인 지식 베이스(knowledge base)다. 노트를 직접 손으로 쓰는 저장소가 아니라, 학습용 에이전트 스킬 세 개가 자동으로 채우고 갱신하는 살아 있는 저장소다.

학습은 다음 사이클로 돈다.

```
place-me  →  teach-me  →  review-me
 (진단)       (학습)        (복습)
   └──────────  levels.md  ──────────┘
```

## 세 가지 스킬

이 저장소는 [`kidow/skills`](https://github.com/kidow/skills) 레포지토리의 학습 스킬들과 함께 쓰도록 만들어졌다.

- **place-me** — 학습을 시작하기 전, 해당 주제를 내가 얼마나 아는지 짧은 적응형 진단으로 가늠한다. 한 번에 한 질문씩, 수준이 확신될 때까지 묻고, 결과를 서술형 수준 요약으로 `levels.md`에 기록한다.
- **teach-me** — 한 번에 지식 하나씩 설명한다. "다음"이라고 할 때만 진행하고, 이미 배운 내용은 다시 가르치지 않는다. 복잡한 개념은 내 모국어·문화에 빗대 설명하고, 이해가 어려우면 시각 자료를 띄운다. 설명한 지식은 `notes/topic_name.md`에 커밋한다.
- **review-me** — 저장된 노트를 한 항목씩 퀴즈로 복습한다. 간격 반복(spaced-repetition) 방식이며, 컨텍스트가 없으면 `levels.md`에서 수준이 낮은 주제부터 우선 복습한다. 복습이 끝나면 그 결과를 토대로 `levels.md`의 수준을 갱신한다.

세 스킬은 `topic_name`이라는 공통 키로 묶인다. `notes/topic_name.md`의 파일 이름과 `levels.md`의 `## topic_name` 섹션이 같은 주제를 가리킨다.

## 저장소 구조

```
brain/
├── notes/            # 배운 지식 (teach-me가 작성, review-me가 읽음)
│   ├── topic_name.md #  - 주제당 1파일, 날짜 없음(git 히스토리가 시점 추적)
│   └── <domain>/     #  - 주제가 쌓이면 도메인별 하위 폴더로 자동 정리
├── levels.md         # 주제별 수준 메모리 (Blank/Glimpsed/Grounded/Fluent)
└── README.md
```

- `notes/` — 지식 노트. frontmatter 없이 내용만 담는다.
- `levels.md` — 주제별 수준을 네 단계 라벨 + 서술형 요약으로 기록한다.
  - **Blank** — 개념 자체를 접한 적 없음
  - **Glimpsed** — 본 적은 있지만 스스로 재현·설명 불가
  - **Grounded** — 자기 말로 설명하고 새 맥락에 적용 가능
  - **Fluent** — 예외·뉘앙스·엣지케이스까지 막힘없이 처리
- `.review/` — 복습 세션 중에만 존재하는 휘발성 폴더. 세션이 끝나면 삭제된다(git 추적 제외).

## 스킬 설치

```bash
npx skills@latest add kidow/skills/place-me
npx skills@latest add kidow/skills/teach-me
npx skills@latest add kidow/skills/review-me
```

## 사용 예

이 저장소 안에서 학습 스킬을 실행하면 된다.

```
/place-me 일본어 문자의 특징     # 수준 진단 → levels.md 기록
/teach-me 일본어 문자의 특징     # 한 조각씩 학습 → notes/ 커밋
/review-me                       # 약한 주제부터 복습 → levels.md 갱신
```
