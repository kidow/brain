# brain

[English](README.md) · 한국어

배운 것을 쌓아 두는 개인 지식 베이스(knowledge base)입니다. 노트를 직접 손으로 채우는 저장소가 아니라, 학습용 에이전트 스킬 세 개가 자동으로 채우고 갱신하는 살아 있는 저장소입니다.

학습은 **PTR** (Place → Teach → Review)이라 부르는 사이클로 진행됩니다.

```
place-me  →  teach-me  →  review-me
 (진단)       (학습)        (복습)
   └──────────  levels.md  ──────────┘
```

**PTR**은 세 스킬로 이루어진 학습 루프의 이름입니다. 주제마다 한 번씩 돌립니다. 현재 수준을 진단하고, 조각조각 배우고, 익숙해질 때까지 복습합니다. 수준이 올라가면 다시 반복합니다.

## 세 가지 스킬

이 저장소는 [`kidow/skills`](https://github.com/kidow/skills) 레포지토리의 학습 스킬들과 함께 사용하도록 만들어졌습니다.

- **place-me** — 학습을 시작하기 전, 해당 주제를 얼마나 알고 있는지 짧은 적응형 진단으로 가늠합니다. `levels.md`에 기존 요약이 있으면 시작 추정치로 활용합니다. 한 번에 한 질문씩, 수준이 확인될 때까지 묻고, 결과를 서술형 수준 요약으로 `levels.md`에 기록한 뒤 teach-me에 넘깁니다.
- **teach-me** — 한 번에 지식 하나씩, 기초부터 심화 순으로 설명합니다. `levels.md`를 먼저 읽어 깊이를 조정합니다. "다음"이라고 할 때만 진행하고, 이미 배운 내용은 다시 가르치지 않으며, 모호한 용어는 즉시 교정합니다. 복잡한 개념은 모국어·문화에 빗대 설명하고, 이해가 어려우면 시각 자료를 제공합니다. 외국어 학습 시 발음이 필요하면 음성 자료도 재생합니다. 주제가 완전히 다루어지면 관련 주제 2–3개를 제안합니다. 설명한 지식은 `notes/topic_name.md`에 커밋하며, 노트가 쌓이면 도메인별 하위 폴더로 자동 정리합니다.
- **review-me** — 저장된 노트를 한 항목씩 퀴즈로 복습합니다. 간격 반복(Again / Hard / Good / Easy) 방식이며, 컨텍스트가 없으면 `levels.md`에서 수준이 낮은 주제부터 우선 복습합니다. `levels.md`가 없으면 place-me 실행을 먼저 제안합니다. 복습이 끝나면 그 결과를 토대로 `levels.md`의 수준을 갱신하고 `.review/` 폴더를 삭제합니다.

세 스킬은 `topic_name`이라는 공통 키로 연결됩니다. `notes/topic_name.md`의 파일 이름과 `levels.md`의 `## topic_name` 섹션이 같은 주제를 가리킵니다.

## 저장소 구조

```
brain/
├── notes/            # 배운 지식 (teach-me가 작성, review-me가 읽음)
│   ├── topic_name.md #  - 주제당 1파일, 날짜 없음(git 히스토리가 시점 추적)
│   └── <domain>/     #  - 주제가 쌓이면 도메인별 하위 폴더로 자동 정리
├── sheets/           # 빠른 참조용 치트시트 (HTML, GitHub Pages로 서빙)
├── levels.md         # 주제별 수준 메모리 (Blank/Glimpsed/Grounded/Fluent)
└── README.md
```

- `notes/` — 지식 노트입니다. frontmatter 없이 내용만 담습니다.
- `levels.md` — 주제별 수준을 네 단계 라벨 + 서술형 요약으로 기록합니다.
  - **Blank** — 개념 자체를 접한 적 없음
  - **Glimpsed** — 본 적은 있지만 스스로 재현·설명 불가
  - **Grounded** — 자기 말로 설명하고 새 맥락에 적용 가능
  - **Fluent** — 예외·뉘앙스·엣지케이스까지 막힘없이 처리
- `.review/` — 복습 세션 중에만 존재하는 휘발성 폴더입니다. 세션이 끝나면 삭제됩니다(git 추적 제외).

## 수준 기록

주제별 현재 수준 — [brain.dongwook.kim/levels](https://brain.dongwook.kim/levels)

## 노트

[brain.dongwook.kim](https://brain.dongwook.kim)에서 바로 열 수 있는 학습 노트입니다.

**언어 — 일본어**
- [히라가나](https://brain.dongwook.kim/notes/히라가나)
- [가타카나](https://brain.dongwook.kim/notes/가타카나)
- [일본어 문자의 특징](https://brain.dongwook.kim/notes/일본어/일본어_문자의_특징)
- [일본어 기본 한자](https://brain.dongwook.kim/notes/일본어/일본어_기본_한자)
- [일본어 동사](https://brain.dongwook.kim/notes/일본어/일본어_동사)
- [일본어 조사](https://brain.dongwook.kim/notes/일본어/일본어_조사)
- [일본어 부사](https://brain.dongwook.kim/notes/일본어/일본어_부사)
- [일본어 형용사](https://brain.dongwook.kim/notes/일본어/일본어_형용사)
- [일본어 지시대명사](https://brain.dongwook.kim/notes/일본어/일본어_지시대명사)
- [일본어 조수사](https://brain.dongwook.kim/notes/일본어/일본어_조수사)
- [일본어 비교 표현](https://brain.dongwook.kim/notes/일본어/일본어_비교_표현)

**언어 — 중국어**
- [중국어 문자](https://brain.dongwook.kim/notes/중국어_문자)
- [중국어 발음](https://brain.dongwook.kim/notes/중국어_발음)
- [중국어 기초 어휘](https://brain.dongwook.kim/notes/중국어_기초_어휘)
- [중국어 양사 심화](https://brain.dongwook.kim/notes/중국어_양사_심화)
- [중국어 문장 구조](https://brain.dongwook.kim/notes/중국어_문장_구조)
- [중국어 결과보어](https://brain.dongwook.kim/notes/중국어_결과보어)
- [중국어 비교문](https://brain.dongwook.kim/notes/중국어_비교문)
- [중국어 존재문](https://brain.dongwook.kim/notes/중국어_존재문)
- [중국어 연동문](https://brain.dongwook.kim/notes/중국어_연동문)
- [중국어 의문사 의문문](https://brain.dongwook.kim/notes/중국어_의문사_의문문)
- [중국어 연결어](https://brain.dongwook.kim/notes/중국어_연결어)

**언어 — 러시아어**
- [러시아어 문자의 특징](https://brain.dongwook.kim/notes/러시아어_문자의_특징)
- [러시아어 기초 어휘](https://brain.dongwook.kim/notes/러시아어_기초_어휘)
- [러시아어 격변화 기초](https://brain.dongwook.kim/notes/러시아어_격변화_기초)

**언어 — 스페인어**
- [스페인어 문자](https://brain.dongwook.kim/notes/스페인어_문자)
- [스페인어 명사와 성](https://brain.dongwook.kim/notes/스페인어_명사와_성)
- [스페인어 기초 어휘](https://brain.dongwook.kim/notes/스페인어_기초_어휘)

**언어 — 독일어**
- [독일어 문자](https://brain.dongwook.kim/notes/독일어_문자)
- [독일어 명사](https://brain.dongwook.kim/notes/독일어_명사)
- [독일어 동사](https://brain.dongwook.kim/notes/독일어_동사)
- [독일어 형용사](https://brain.dongwook.kim/notes/독일어_형용사)
- [독일어 기초 어휘](https://brain.dongwook.kim/notes/독일어_기초_어휘)

**언어 — 프랑스어**
- [프랑스어 문자](https://brain.dongwook.kim/notes/프랑스어_문자)
- [프랑스어 명사 성](https://brain.dongwook.kim/notes/프랑스어_명사_성)
- [프랑스어 동사 현재형](https://brain.dongwook.kim/notes/프랑스어_동사_현재형)
- [프랑스어 기초 어휘](https://brain.dongwook.kim/notes/프랑스어_기초_어휘)
- [프랑스어 부정문 의문문](https://brain.dongwook.kim/notes/프랑스어_부정문_의문문)
- [프랑스어 도치 의문문](https://brain.dongwook.kim/notes/프랑스어_도치_의문문)
- [프랑스어 회화](https://brain.dongwook.kim/notes/프랑스어_회화)
- [프랑스어 faire 동사](https://brain.dongwook.kim/notes/프랑스어_faire_동사)
- [프랑스어 근접과거](https://brain.dongwook.kim/notes/프랑스어_근접과거)
- [프랑스어 직접목적어 대명사](https://brain.dongwook.kim/notes/프랑스어_직접목적어_대명사)

**언어 — 아랍어**
- [아랍어 문자](https://brain.dongwook.kim/notes/아랍어_문자)
- [아랍어 기초 어휘](https://brain.dongwook.kim/notes/아랍어_기초_어휘)

**언어 — 영어**
- [영어](https://brain.dongwook.kim/notes/영어/영어)
- [영어 전치사](https://brain.dongwook.kim/notes/영어/영어_전치사)
- [영어 관사](https://brain.dongwook.kim/notes/영어/영어_관사)
- [영어 부사](https://brain.dongwook.kim/notes/영어/영어_부사)
- [영어 조동사](https://brain.dongwook.kim/notes/영어/영어_조동사)
- [영어 가정법](https://brain.dongwook.kim/notes/영어/영어_가정법)
- [영어 수동태](https://brain.dongwook.kim/notes/영어/영어_수동태)
- [영어 관계대명사](https://brain.dongwook.kim/notes/영어/영어_관계대명사)
- [영어 관계부사](https://brain.dongwook.kim/notes/영어/영어_관계부사)
- [영어 접속사](https://brain.dongwook.kim/notes/영어/영어_접속사)
- [영어 분사구문](https://brain.dongwook.kim/notes/영어/영어_분사구문)
- [영어 시제 심화](https://brain.dongwook.kim/notes/영어/영어_시제_심화)
- [영어 5형식](https://brain.dongwook.kim/notes/영어/영어_5형식)
- [영어 to부정사](https://brain.dongwook.kim/notes/영어/영어_to부정사)
- [영어 가산/불가산 명사](https://brain.dongwook.kim/notes/영어/영어_가산_불가산_명사)
- [영어 비교급 최상급](https://brain.dongwook.kim/notes/영어/영어_비교급_최상급)
- [영어 분사](https://brain.dongwook.kim/notes/영어/영어_분사)
- [영어 명사절](https://brain.dongwook.kim/notes/영어/영어_명사절)
- [영어 도치](https://brain.dongwook.kim/notes/영어/영어_도치)
- [영어 강조 구문](https://brain.dongwook.kim/notes/영어/영어_강조_구문)
- [영어 관계사 심화](https://brain.dongwook.kim/notes/영어/영어_관계사_심화)
- [영어 부사절 심화](https://brain.dongwook.kim/notes/영어/영어_부사절_심화)
- [영어 동사구 심화](https://brain.dongwook.kim/notes/영어/영어_동사구_심화)
- [영어 문장 구조 심화](https://brain.dongwook.kim/notes/영어/영어_문장_구조_심화)
- [영어 동명사](https://brain.dongwook.kim/notes/영어/영어_동명사)
- [영어 화법](https://brain.dongwook.kim/notes/영어/영어_화법)
- [영어 구두점](https://brain.dongwook.kim/notes/영어/영어_구두점)
- [영어 어휘 확장](https://brain.dongwook.kim/notes/영어/영어_어휘_확장)
- [영어 회화](https://brain.dongwook.kim/notes/영어/영어_회화)
- [영어 슬랭·관용어](https://brain.dongwook.kim/notes/영어/영어_슬랭·관용어)
- [영어 발음](https://brain.dongwook.kim/notes/영어/영어_발음)
- [영어 쓰기](https://brain.dongwook.kim/notes/영어/영어_쓰기)
- [영어 비즈니스 영어](https://brain.dongwook.kim/notes/영어/영어_비즈니스_영어)
- [영어 독해](https://brain.dongwook.kim/notes/영어/영어_독해)
- [영어 청취](https://brain.dongwook.kim/notes/영어/영어_청취)
- [영어 전치사 심화](https://brain.dongwook.kim/notes/영어/영어_전치사_심화)

**음악**
- [음악 이론 기초](https://brain.dongwook.kim/notes/음악_이론_기초)
- [AI 음악 프롬프팅](https://brain.dongwook.kim/notes/AI_음악_프롬프팅)

**예술**
- [미술 작품 교양](https://brain.dongwook.kim/notes/미술_작품_교양)

**경제/금융**
- [회계학](https://brain.dongwook.kim/notes/회계학)
- [세금 용어](https://brain.dongwook.kim/notes/세금_용어)
- [경제학](https://brain.dongwook.kim/notes/경제학)
- [투자 기초](https://brain.dongwook.kim/notes/투자_기초)
- [주식 용어](https://brain.dongwook.kim/notes/주식_용어)
- [부동산 기초](https://brain.dongwook.kim/notes/부동산_기초)

**실생활**
- [근로기준법](https://brain.dongwook.kim/notes/근로기준법)
- [자동차 상식](https://brain.dongwook.kim/notes/자동차_상식)

**과학**
- [화학](https://brain.dongwook.kim/notes/화학)

**기술**
- [컴퓨터 부품](https://brain.dongwook.kim/notes/컴퓨터_부품)

## 치트시트

[brain.dongwook.kim](https://brain.dongwook.kim)에서 바로 열 수 있는 빠른 참조 시트입니다.

**아랍어**
- [아랍어 문자 치트시트](https://brain.dongwook.kim/sheets/아랍어/아랍어_문자_치트시트.html)

**일본어**
- [히라가나 치트시트](https://brain.dongwook.kim/sheets/일본어/히라가나_치트시트.html)
- [가타카나 치트시트](https://brain.dongwook.kim/sheets/일본어/가타카나_치트시트.html)
- [일본어 문자의 특징 치트시트](https://brain.dongwook.kim/sheets/일본어/일본어_문자의_특징_치트시트.html)
- [일본어 기본 한자 치트시트](https://brain.dongwook.kim/sheets/일본어/일본어_기본_한자_치트시트.html)
- [일본어 동사 치트시트](https://brain.dongwook.kim/sheets/일본어/일본어_동사_치트시트.html)
- [일본어 형용사 치트시트](https://brain.dongwook.kim/sheets/일본어/일본어_형용사_치트시트.html)
- [일본어 조사 치트시트](https://brain.dongwook.kim/sheets/일본어/일본어_조사_치트시트.html)
- [일본어 부사 치트시트](https://brain.dongwook.kim/sheets/일본어/일본어_부사_치트시트.html)
- [일본어 지시대명사 치트시트](https://brain.dongwook.kim/sheets/일본어/일본어_지시대명사_치트시트.html)
- [일본어 조수사 치트시트](https://brain.dongwook.kim/sheets/일본어/일본어_조수사_치트시트.html)
- [일본어 비교 표현 치트시트](https://brain.dongwook.kim/sheets/일본어/일본어_비교_표현_치트시트.html)

**러시아어**
- [러시아어 치트시트](https://brain.dongwook.kim/sheets/러시아어/러시아어_치트시트.html)
- [러시아어 알파벳 이름](https://brain.dongwook.kim/sheets/러시아어/러시아어_알파벳_이름.html)
- [러시아어 모음 약화](https://brain.dongwook.kim/sheets/러시아어/러시아어_모음_약화.html)
- [러시아어 문자의 특징 치트시트](https://brain.dongwook.kim/sheets/러시아어/러시아어_문자의_특징_치트시트.html)

**중국어**
- [병음 표](https://brain.dongwook.kim/sheets/중국어/병음_표.html)
- [중국어 성모표](https://brain.dongwook.kim/sheets/중국어/중국어_성모표.html)
- [중국어 성조규칙](https://brain.dongwook.kim/sheets/중국어/중국어_성조규칙.html)
- [중국어 성조 연습](https://brain.dongwook.kim/sheets/중국어/중국어_성조_연습.html)
- [중국어 문자 치트시트](https://brain.dongwook.kim/sheets/중국어/중국어_문자_치트시트.html)

**독일어**
- [독일어 치트시트](https://brain.dongwook.kim/sheets/독일어/독일어_치트시트.html)
- [독일어 명사 치트시트](https://brain.dongwook.kim/sheets/독일어/독일어_명사_치트시트.html)
- [독일어 문자 치트시트](https://brain.dongwook.kim/sheets/독일어/독일어_문자_치트시트.html)

**프랑스어**
- [프랑스어 명사 치트시트](https://brain.dongwook.kim/sheets/프랑스어/프랑스어_명사_치트시트.html)
- [프랑스어 문자 치트시트](https://brain.dongwook.kim/sheets/프랑스어/프랑스어_문자_치트시트.html)
- [프랑스어 동사 현재형 치트시트](https://brain.dongwook.kim/sheets/프랑스어/프랑스어_동사_현재형_치트시트.html)

**스페인어**
- [스페인어 알파벳 이름](https://brain.dongwook.kim/sheets/스페인어/스페인어_알파벳_이름.html)
- [스페인어 발음 규칙](https://brain.dongwook.kim/sheets/스페인어/스페인어_발음_규칙.html)
- [스페인어 악센트 강세](https://brain.dongwook.kim/sheets/스페인어/스페인어_악센트_강세.html)
- [스페인어 특수부호 키보드](https://brain.dongwook.kim/sheets/스페인어/스페인어_특수부호_키보드.html)
- [스페인어 명사와 성 치트시트](https://brain.dongwook.kim/sheets/스페인어/스페인어_명사와_성_치트시트.html)

**영어**
- [영어 전치사 치트시트](https://brain.dongwook.kim/sheets/영어/영어_전치사_치트시트.html)
- [영어 관사 치트시트](https://brain.dongwook.kim/sheets/영어/영어_관사_치트시트.html)
- [영어 조동사 치트시트](https://brain.dongwook.kim/sheets/영어/영어_조동사_치트시트.html)
- [영어 부사 치트시트](https://brain.dongwook.kim/sheets/영어/영어_부사_치트시트.html)
- [영어 가정법 치트시트](https://brain.dongwook.kim/sheets/영어/영어_가정법_치트시트.html)
- [영어 수동태 치트시트](https://brain.dongwook.kim/sheets/영어/영어_수동태_치트시트.html)
- [영어 관계대명사 치트시트](https://brain.dongwook.kim/sheets/영어/영어_관계대명사_치트시트.html)
- [영어 관계부사 치트시트](https://brain.dongwook.kim/sheets/영어/영어_관계부사_치트시트.html)
- [영어 접속사 치트시트](https://brain.dongwook.kim/sheets/영어/영어_접속사_치트시트.html)
- [영어 분사구문 치트시트](https://brain.dongwook.kim/sheets/영어/영어_분사구문_치트시트.html)
- [영어 시제 심화 치트시트](https://brain.dongwook.kim/sheets/영어/영어_시제_심화_치트시트.html)
- [영어 가산/불가산 명사 치트시트](https://brain.dongwook.kim/sheets/영어/영어_가산_불가산_명사_치트시트.html)
- [영어 5형식 치트시트](https://brain.dongwook.kim/sheets/영어/영어_5형식_치트시트.html)
- [영어 to부정사 치트시트](https://brain.dongwook.kim/sheets/영어/영어_to부정사_치트시트.html)
- [영어 비교급 최상급 치트시트](https://brain.dongwook.kim/sheets/영어/영어_비교급_최상급_치트시트.html)
- [영어 강조 구문 치트시트](https://brain.dongwook.kim/sheets/영어/영어_강조_구문_치트시트.html)
- [영어 관계사 심화 치트시트](https://brain.dongwook.kim/sheets/영어/영어_관계사_심화_치트시트.html)
- [영어 구두점 치트시트](https://brain.dongwook.kim/sheets/영어/영어_구두점_치트시트.html)
- [영어 도치 치트시트](https://brain.dongwook.kim/sheets/영어/영어_도치_치트시트.html)
- [영어 동명사 치트시트](https://brain.dongwook.kim/sheets/영어/영어_동명사_치트시트.html)
- [영어 동사구 심화 치트시트](https://brain.dongwook.kim/sheets/영어/영어_동사구_심화_치트시트.html)
- [영어 명사절 치트시트](https://brain.dongwook.kim/sheets/영어/영어_명사절_치트시트.html)
- [영어 문장 구조 심화 치트시트](https://brain.dongwook.kim/sheets/영어/영어_문장_구조_심화_치트시트.html)
- [영어 부사절 심화 치트시트](https://brain.dongwook.kim/sheets/영어/영어_부사절_심화_치트시트.html)
- [영어 분사 치트시트](https://brain.dongwook.kim/sheets/영어/영어_분사_치트시트.html)
- [영어 회화 치트시트](https://brain.dongwook.kim/sheets/영어/영어_회화_치트시트.html)
- [영어 화법 치트시트](https://brain.dongwook.kim/sheets/영어/영어_화법_치트시트.html)
- [영어 어휘 확장 치트시트](https://brain.dongwook.kim/sheets/영어/영어_어휘_확장_치트시트.html)
- [영어 슬랭·관용어 치트시트](https://brain.dongwook.kim/sheets/영어/영어_슬랭·관용어_치트시트.html)
- [영어 발음 치트시트](https://brain.dongwook.kim/sheets/영어/영어_발음_치트시트.html)
- [영어 쓰기 치트시트](https://brain.dongwook.kim/sheets/영어/영어_쓰기_치트시트.html)
- [영어 비즈니스 영어 치트시트](https://brain.dongwook.kim/sheets/영어/영어_비즈니스_영어_치트시트.html)
- [영어 독해 치트시트](https://brain.dongwook.kim/sheets/영어/영어_독해_치트시트.html)

**음악**
- [음악 이론 기초 치트시트](https://brain.dongwook.kim/sheets/음악_이론_기초_치트시트.html)

**경제/금융**
- [세금 용어 치트시트](https://brain.dongwook.kim/sheets/세금_용어_치트시트.html)
- [경제학 치트시트](https://brain.dongwook.kim/sheets/경제학_치트시트.html)
- [회계학 치트시트](https://brain.dongwook.kim/sheets/회계학_치트시트.html)
- [투자 기초 치트시트](https://brain.dongwook.kim/sheets/투자_기초_치트시트.html)
- [주식 용어 치트시트](https://brain.dongwook.kim/sheets/주식_용어_치트시트.html)
- [부동산 기초 치트시트](https://brain.dongwook.kim/sheets/부동산_기초_치트시트.html)

**실생활**
- [근로기준법 치트시트](https://brain.dongwook.kim/sheets/근로기준법_치트시트.html)

**기술**
- [컴퓨터 부품](https://brain.dongwook.kim/sheets/컴퓨터_부품.html)

## 드릴

간격 반복(SM-2) 방식 어휘 복습 도구입니다. [brain.dongwook.kim](https://brain.dongwook.kim)에서 바로 열 수 있습니다. 복습 진행 상태는 브라우저 localStorage에만 저장되며, 기기 간 동기화는 되지 않습니다.

**일본어**
- [일본어 기초 어휘](https://brain.dongwook.kim/drills/일본어_기초_어휘.html)

**영어**
- [영어 GRE 어휘](https://brain.dongwook.kim/drills/영어_GRE_어휘.html)

**아랍어**
- [아랍어 기초 어휘](https://brain.dongwook.kim/drills/아랍어_기초_어휘.html)

**러시아어**
- [러시아어 기초 어휘](https://brain.dongwook.kim/drills/러시아어_기초_어휘.html)

## 스킬 설치

```bash
npx skills@latest add kidow/skills/place-me
npx skills@latest add kidow/skills/teach-me
npx skills@latest add kidow/skills/review-me
```

## 사용 예

이 저장소 안에서 학습 스킬을 실행하시면 됩니다.

```
/place-me 일본어 문자의 특징     # 수준 진단 → levels.md 기록
/teach-me 일본어 문자의 특징     # 한 조각씩 학습 → notes/ 커밋
/review-me                       # 약한 주제부터 복습 → levels.md 갱신
```

## 나만의 brain 만들기

아래 프롬프트를 복사해 AI 어시스턴트(Claude Code 권장)에게 붙여넣으세요:

```
PTR 학습 시스템(Place → Teach → Review)으로 개인 지식 베이스를 세팅해줘.

1. 새 git 저장소를 만들고 Claude Code로 열어줘.
2. 학습 스킬 세 개를 설치해줘:
   npx skills@latest add kidow/skills/place-me
   npx skills@latest add kidow/skills/teach-me
   npx skills@latest add kidow/skills/review-me
3. 다음 파일 구조를 만들어줘:
   - notes/      (빈 폴더 — git이 추적하도록 .gitkeep 파일 추가)
   - levels.md   (빈 파일)
   - README.md   (https://github.com/kidow/brain 에서 복사)

완료되면 /place-me <주제> 로 첫 번째 주제 수준 진단을 시작해줘.
```
