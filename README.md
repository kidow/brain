# brain

English · [한국어](README.ko.md)

A personal knowledge base of everything I learn. Not a repo I fill by hand — three learning agent skills populate and keep it up to date automatically. It's a living store.

Learning runs as a cycle called **PTR** (Place → Teach → Review):

```
place-me  →  teach-me  →  review-me
 (assess)     (learn)      (review)
   └──────────  levels.md  ──────────┘
```

**PTR** is the name for this three-skill loop. Run it once per topic: assess where you stand, learn piece by piece, then review until it sticks. Repeat as the level rises.

## The three skills

This repo is built to work with the learning skills from the [`kidow/skills`](https://github.com/kidow/skills) repository.

- **place-me** — Before learning a topic, a short adaptive diagnostic gauges how much I already know. Reads any existing `levels.md` entry for the topic as a starting guess. One question at a time until the level is clear, then it writes a prose level summary to `levels.md` and hands off to teach-me calibrated to the result.
- **teach-me** — Explains one piece of knowledge at a time, always progressing from foundational to advanced. Reads `levels.md` first to calibrate depth. Advances only when I say "next", never re-teaches covered pieces, and flags imprecise vocabulary for correction. Complex concepts are grounded in analogies to my native language and culture. A visual aid is drawn when something is hard to grasp, and an audio aid plays pronunciation when learning a foreign language. When all pieces are covered, suggests 2–3 related topics. Each piece is committed to `notes/topic_name.md`; notes auto-organize into domain subfolders as they grow.
- **review-me** — Quizzes me on the saved notes one item at a time using spaced repetition (Again / Hard / Good / Easy). With no context given, it prioritizes the weakest topics from `levels.md`; offers to run place-me first if `levels.md` is missing. When the session ends, it updates the level in `levels.md` and deletes the ephemeral `.review/` folder.

The three skills are tied together by a shared `topic_name` key: the `notes/topic_name.md` filename and the `## topic_name` section in `levels.md` point to the same topic.

## Repository layout

```
brain/
├── notes/            # learned knowledge (written by teach-me, read by review-me)
│   ├── topic_name.md #  - one file per topic, no date (git history tracks time)
│   └── <domain>/     #  - notes auto-organize into domain subfolders as they grow
├── sheets/           # quick-reference cheat sheets (HTML, served via GitHub Pages)
├── levels.md         # per-topic level memory (Blank/Glimpsed/Grounded/Fluent)
└── README.md
```

- `notes/` — knowledge notes, content only, no frontmatter.
- `levels.md` — each topic's level as a four-stage label plus a prose summary.
  - **Blank** — no prior exposure to the concept
  - **Glimpsed** — seen it before but cannot reproduce or explain it reliably
  - **Grounded** — explains it independently and applies it in new contexts
  - **Fluent** — handles exceptions, nuance, and edge cases without hesitation
- `.review/` — an ephemeral folder that exists only during a review session and is deleted when it ends (excluded from git).

## Levels

Current level per topic — [brain.dongwook.kim/levels](https://brain.dongwook.kim/levels)

## Notes

All knowledge notes served live at [brain.dongwook.kim](https://brain.dongwook.kim).

**Languages — Japanese**
- [히라가나](https://brain.dongwook.kim/notes/일본어/히라가나)
- [가타카나](https://brain.dongwook.kim/notes/일본어/가타카나)
- [일본어 문자의 특징](https://brain.dongwook.kim/notes/일본어/일본어_문자의_특징)
- [일본어 기본 한자](https://brain.dongwook.kim/notes/일본어/일본어_기본_한자)
- [일본어 동사](https://brain.dongwook.kim/notes/일본어/일본어_동사)
- [일본어 조사](https://brain.dongwook.kim/notes/일본어/일본어_조사)
- [일본어 부사](https://brain.dongwook.kim/notes/일본어/일본어_부사)
- [일본어 형용사](https://brain.dongwook.kim/notes/일본어/일본어_형용사)
- [일본어 지시대명사](https://brain.dongwook.kim/notes/일본어/일본어_지시대명사)
- [일본어 조수사](https://brain.dongwook.kim/notes/일본어/일본어_조수사)
- [일본어 비교 표현](https://brain.dongwook.kim/notes/일본어/일본어_비교_표현)
- [일본어 관용구](https://brain.dongwook.kim/notes/일본어/일본어_관용구)

**Languages — Chinese**
- [중국어 문자](https://brain.dongwook.kim/notes/중국어/중국어_문자)
- [중국어 발음](https://brain.dongwook.kim/notes/중국어/중국어_발음)
- [중국어 기초 어휘](https://brain.dongwook.kim/notes/중국어/중국어_기초_어휘)
- [중국어 양사](https://brain.dongwook.kim/notes/중국어/중국어_양사)
- [중국어 문장 구조](https://brain.dongwook.kim/notes/중국어/중국어_문장_구조)
- [중국어 결과보어](https://brain.dongwook.kim/notes/중국어/중국어_결과보어)
- [중국어 비교문](https://brain.dongwook.kim/notes/중국어/중국어_비교문)
- [중국어 존재문](https://brain.dongwook.kim/notes/중국어/중국어_존재문)
- [중국어 연동문](https://brain.dongwook.kim/notes/중국어/중국어_연동문)
- [중국어 의문사 의문문](https://brain.dongwook.kim/notes/중국어/중국어_의문사_의문문)
- [중국어 연결어](https://brain.dongwook.kim/notes/중국어/중국어_연결어)
- [중국어 정반의문문](https://brain.dongwook.kim/notes/중국어/중국어_정반의문문)
- [중국어 的地得 구별](https://brain.dongwook.kim/notes/중국어/중국어_的地得_구별)
- [중국어 시량보어](https://brain.dongwook.kim/notes/중국어/중국어_시량보어)
- [중국어 연쇄·병렬 표현](https://brain.dongwook.kim/notes/중국어/중국어_연쇄_병렬_표현)
- [중국어 회화](https://brain.dongwook.kim/notes/중국어/중국어_회화)
- [중국어 동시진행·순서 표현](https://brain.dongwook.kim/notes/중국어/중국어_동시진행_순서_표현)
- [중국어 관용어](https://brain.dongwook.kim/notes/중국어/중국어_관용어)

**Languages — Russian**
- [러시아어 문자의 특징](https://brain.dongwook.kim/notes/러시아어/러시아어_문자의_특징)
- [러시아어 기초 어휘](https://brain.dongwook.kim/notes/러시아어/러시아어_기초_어휘)
- [러시아어 격변화 기초](https://brain.dongwook.kim/notes/러시아어/러시아어_격변화_기초)
- [러시아어 명사의 성](https://brain.dongwook.kim/notes/러시아어/러시아어_명사의_성)
- [러시아어 형용사 격변화](https://brain.dongwook.kim/notes/러시아어/러시아어_형용사_격변화)
- [러시아어 동사 현재형](https://brain.dongwook.kim/notes/러시아어/러시아어_동사_현재형)
- [러시아어 명사 복수형](https://brain.dongwook.kim/notes/러시아어/러시아어_명사_복수형)
- [러시아어 동사 과거형](https://brain.dongwook.kim/notes/러시아어/러시아어_동사_과거형)
- [러시아어 부정문](https://brain.dongwook.kim/notes/러시아어/러시아어_부정문)
- [러시아어 동사 미래형](https://brain.dongwook.kim/notes/러시아어/러시아어_동사_미래형)
- [러시아어 동사상](https://brain.dongwook.kim/notes/러시아어/러시아어_동사상)
- [러시아어 이동동사](https://brain.dongwook.kim/notes/러시아어/러시아어_이동동사)
- [러시아어 소유대명사 격변화](https://brain.dongwook.kim/notes/러시아어/러시아어_소유대명사_격변화)
- [러시아어 지시대명사](https://brain.dongwook.kim/notes/러시아어/러시아어_지시대명사)
- [러시아어 의문문 심화](https://brain.dongwook.kim/notes/러시아어/러시아어_의문문_심화)
- [러시아어 형용사 비교급 최상급](https://brain.dongwook.kim/notes/러시아어/러시아어_형용사_비교급_최상급)
- [러시아어 인칭대명사 격변화](https://brain.dongwook.kim/notes/러시아어/러시아어_인칭대명사_격변화)
- [러시아어 존댓말](https://brain.dongwook.kim/notes/러시아어/러시아어_존댓말)
- [러시아어 시간 표현](https://brain.dongwook.kim/notes/러시아어/러시아어_시간_표현)
- [러시아어 서수사](https://brain.dongwook.kim/notes/러시아어/러시아어_서수사)
- [러시아어 명사 격변화 심화](https://brain.dongwook.kim/notes/러시아어/러시아어_명사_격변화_심화)
- [러시아어 감정·상태 형용사](https://brain.dongwook.kim/notes/러시아어/러시아어_감정_상태_형용사)
- [러시아어 날씨 표현](https://brain.dongwook.kim/notes/러시아어/러시아어_날씨_표현)
- [러시아어 회화](https://brain.dongwook.kim/notes/러시아어/러시아어_회화)
- [러시아어 숫자](https://brain.dongwook.kim/notes/러시아어/러시아어_숫자)
- [러시아어 재귀동사](https://brain.dongwook.kim/notes/러시아어/러시아어_재귀동사)
- [러시아어 접속사 종속절](https://brain.dongwook.kim/notes/러시아어/러시아어_접속사_종속절)

**Languages — Spanish**
- [스페인어 문자](https://brain.dongwook.kim/notes/스페인어/스페인어_문자)
- [스페인어 명사와 성](https://brain.dongwook.kim/notes/스페인어/스페인어_명사와_성)
- [스페인어 기초 어휘](https://brain.dongwook.kim/notes/스페인어/스페인어_기초_어휘)
- [스페인어 동사 현재형](https://brain.dongwook.kim/notes/스페인어/스페인어_동사_현재형)
- [스페인어 부정문 의문문](https://brain.dongwook.kim/notes/스페인어/스페인어_부정문_의문문)
- [스페인어 목적어 대명사](https://brain.dongwook.kim/notes/스페인어/스페인어_목적어_대명사)
- [스페인어 명령문](https://brain.dongwook.kim/notes/스페인어/스페인어_명령문)
- [스페인어 재귀동사](https://brain.dongwook.kim/notes/스페인어/스페인어_재귀동사)
- [스페인어 과거시제](https://brain.dongwook.kim/notes/스페인어/스페인어_과거시제)
- [스페인어 현재완료](https://brain.dongwook.kim/notes/스페인어/스페인어_현재완료)
- [스페인어 미래시제](https://brain.dongwook.kim/notes/스페인어/스페인어_미래시제)
- [스페인어 비교급 최상급](https://brain.dongwook.kim/notes/스페인어/스페인어_비교급_최상급)
- [스페인어 접속법](https://brain.dongwook.kim/notes/스페인어/스페인어_접속법)
- [스페인어 관계대명사](https://brain.dongwook.kim/notes/스페인어/스페인어_관계대명사)
- [스페인어 진행형](https://brain.dongwook.kim/notes/스페인어/스페인어_진행형)
- [스페인어 회화](https://brain.dongwook.kim/notes/스페인어/스페인어_회화)
- [스페인어 부사절 접속사](https://brain.dongwook.kim/notes/스페인어/스페인어_부사절_접속사)
- [스페인어 접속법 과거](https://brain.dongwook.kim/notes/스페인어/스페인어_접속법_과거)
- [스페인어 관용구](https://brain.dongwook.kim/notes/스페인어/스페인어_관용구)
- [스페인어 슬랭 관용어](https://brain.dongwook.kim/notes/스페인어/스페인어_슬랭_관용어)
- [스페인어 완료 시제 심화](https://brain.dongwook.kim/notes/스페인어/스페인어_완료_시제_심화)

**Languages — German**
- [독일어 문자](https://brain.dongwook.kim/notes/독일어/독일어_문자)
- [독일어 명사](https://brain.dongwook.kim/notes/독일어/독일어_명사)
- [독일어 동사](https://brain.dongwook.kim/notes/독일어/독일어_동사)
- [독일어 형용사](https://brain.dongwook.kim/notes/독일어/독일어_형용사)
- [독일어 기초 어휘](https://brain.dongwook.kim/notes/독일어/독일어_기초_어휘)
- [독일어 대명사](https://brain.dongwook.kim/notes/독일어/독일어_대명사)
- [독일어 회화](https://brain.dongwook.kim/notes/독일어/독일어_회화)
- [독일어 접속법](https://brain.dongwook.kim/notes/독일어/독일어_접속법)
- [독일어 전치사](https://brain.dongwook.kim/notes/독일어/독일어_전치사)
- [독일어 관계문](https://brain.dongwook.kim/notes/독일어/독일어_관계문)
- [독일어 수동태](https://brain.dongwook.kim/notes/독일어/독일어_수동태)
- [독일어 부사](https://brain.dongwook.kim/notes/독일어/독일어_부사)
- [독일어 명사화](https://brain.dongwook.kim/notes/독일어/독일어_명사화)
- [독일어 접속사](https://brain.dongwook.kim/notes/독일어/독일어_접속사)
- [독일어 복합어 심화](https://brain.dongwook.kim/notes/독일어/독일어_복합어_심화)
- [독일어 동사 격지배](https://brain.dongwook.kim/notes/독일어/독일어_동사_격지배)
- [독일어 형용사 전치사 지배](https://brain.dongwook.kim/notes/독일어/독일어_형용사_전치사_지배)
- [독일어 명사 전치사 지배](https://brain.dongwook.kim/notes/독일어/독일어_명사_전치사_지배)
- [독일어 존댓말과 격식체](https://brain.dongwook.kim/notes/독일어/독일어_존댓말과_격식체)
- [독일어 숫자와 시간](https://brain.dongwook.kim/notes/독일어/독일어_숫자와_시간)
- [독일어 요일 시간대 표현](https://brain.dongwook.kim/notes/독일어/독일어_요일_시간대_표현)
- [독일어 시제](https://brain.dongwook.kim/notes/독일어/독일어_시제)

**Languages — French**
- [프랑스어 문자](https://brain.dongwook.kim/notes/프랑스어/프랑스어_문자)
- [프랑스어 명사 성](https://brain.dongwook.kim/notes/프랑스어/프랑스어_명사_성)
- [프랑스어 동사 현재형](https://brain.dongwook.kim/notes/프랑스어/프랑스어_동사_현재형)
- [프랑스어 기초 어휘](https://brain.dongwook.kim/notes/프랑스어/프랑스어_기초_어휘)
- [프랑스어 부정문 의문문](https://brain.dongwook.kim/notes/프랑스어/프랑스어_부정문_의문문)
- [프랑스어 도치 의문문](https://brain.dongwook.kim/notes/프랑스어/프랑스어_도치_의문문)
- [프랑스어 회화](https://brain.dongwook.kim/notes/프랑스어/프랑스어_회화)
- [프랑스어 faire 동사](https://brain.dongwook.kim/notes/프랑스어/프랑스어_faire_동사)
- [프랑스어 근접과거](https://brain.dongwook.kim/notes/프랑스어/프랑스어_근접과거)
- [프랑스어 직접목적어 대명사](https://brain.dongwook.kim/notes/프랑스어/프랑스어_직접목적어_대명사)
- [프랑스어 명령문](https://brain.dongwook.kim/notes/프랑스어/프랑스어_명령문)
- [프랑스어 명령문 목적어 대명사 위치](https://brain.dongwook.kim/notes/프랑스어/프랑스어_명령문_목적어_대명사_위치)
- [프랑스어 재귀동사](https://brain.dongwook.kim/notes/프랑스어/프랑스어_재귀동사)
- [프랑스어 복합과거](https://brain.dongwook.kim/notes/프랑스어/프랑스어_복합과거)
- [프랑스어 재귀동사 복합과거](https://brain.dongwook.kim/notes/프랑스어/프랑스어_재귀동사_복합과거)
- [프랑스어 반과거](https://brain.dongwook.kim/notes/프랑스어/프랑스어_반과거)
- [프랑스어 대과거](https://brain.dongwook.kim/notes/프랑스어/프랑스어_대과거)
- [프랑스어 단순미래](https://brain.dongwook.kim/notes/프랑스어/프랑스어_단순미래)
- [프랑스어 조건법](https://brain.dongwook.kim/notes/프랑스어/프랑스어_조건법)
- [프랑스어 접속법](https://brain.dongwook.kim/notes/프랑스어/프랑스어_접속법)
- [프랑스어 가족 일상 어휘](https://brain.dongwook.kim/notes/프랑스어/프랑스어_가족_일상_어휘)
- [프랑스어 관용구](https://brain.dongwook.kim/notes/프랑스어/프랑스어_관용구)

**Languages — Arabic**
- [아랍어 문자](https://brain.dongwook.kim/notes/아랍어/아랍어_문자)
- [아랍어 기초 어휘](https://brain.dongwook.kim/notes/아랍어/아랍어_기초_어휘)
- [아랍어 회화](https://brain.dongwook.kim/notes/아랍어/아랍어_회화)
- [아랍어 동사 활용](https://brain.dongwook.kim/notes/아랍어/아랍어_동사_활용)
- [아랍어 관계대명사](https://brain.dongwook.kim/notes/아랍어/아랍어_관계대명사)
- [아랍어 조건문](https://brain.dongwook.kim/notes/아랍어/아랍어_조건문)
- [아랍어 수동태](https://brain.dongwook.kim/notes/아랍어/아랍어_수동태)
- [아랍어 비교급](https://brain.dongwook.kim/notes/아랍어/아랍어_비교급)
- [아랍어 시간절](https://brain.dongwook.kim/notes/아랍어/아랍어_시간절)
- [아랍어 방언 입문](https://brain.dongwook.kim/notes/아랍어/아랍어_방언_입문)
- [아랍어 등위접속사](https://brain.dongwook.kim/notes/아랍어/아랍어_등위접속사)
- [아랍어 호격 감탄문](https://brain.dongwook.kim/notes/아랍어/아랍어_호격_감탄문)

**Languages — English**
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
- [영어 동사구](https://brain.dongwook.kim/notes/영어/영어_동사구)
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
- [영어 한정사](https://brain.dongwook.kim/notes/영어/영어_한정사)
- [영어 수 일치](https://brain.dongwook.kim/notes/영어/영어_수_일치)
- [영어 뉴스·시사 어휘](https://brain.dongwook.kim/notes/영어/영어_뉴스·시사_어휘)
- [영어 프레젠테이션](https://brain.dongwook.kim/notes/영어/영어_프레젠테이션)
- [영어 이력서·자소서 작성](https://brain.dongwook.kim/notes/영어/영어_이력서·자소서_작성)
- [영어 인터넷 밈·은어](https://brain.dongwook.kim/notes/영어/영어_인터넷_밈·은어)

**Music**
- [음악 이론 기초](https://brain.dongwook.kim/notes/음악_이론_기초)
- [AI 음악 프롬프팅](https://brain.dongwook.kim/notes/AI_음악_프롬프팅)

**Art**
- [미술 작품 교양](https://brain.dongwook.kim/notes/미술_작품_교양)

**Economics / Finance**
- [회계학](https://brain.dongwook.kim/notes/회계학)
- [세금 용어](https://brain.dongwook.kim/notes/세금_용어)
- [경제학](https://brain.dongwook.kim/notes/경제학)
- [투자 기초](https://brain.dongwook.kim/notes/투자_기초)
- [주식 용어](https://brain.dongwook.kim/notes/주식_용어)
- [부동산 기초](https://brain.dongwook.kim/notes/부동산_기초)

**Daily Life**
- [근로기준법](https://brain.dongwook.kim/notes/근로기준법)
- [자동차 상식](https://brain.dongwook.kim/notes/자동차_상식)

**Science**
- [화학](https://brain.dongwook.kim/notes/화학)

**Technology**
- [컴퓨터 부품](https://brain.dongwook.kim/notes/컴퓨터_부품)

## Cheat Sheets

Quick-reference sheets served live at [brain.dongwook.kim](https://brain.dongwook.kim).

**Arabic**
- [아랍어 문자 치트시트](https://brain.dongwook.kim/sheets/아랍어/아랍어_문자_치트시트.html)
- [아랍어 기초 어휘 치트시트](https://brain.dongwook.kim/sheets/아랍어/아랍어_기초_어휘_치트시트.html)
- [아랍어 동사 활용 치트시트](https://brain.dongwook.kim/sheets/아랍어/아랍어_동사_활용_치트시트.html)

**Japanese**
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
- [일본어 존댓말 치트시트](https://brain.dongwook.kim/sheets/일본어/일본어_존댓말_치트시트.html)
- [일본어 조건 표현 치트시트](https://brain.dongwook.kim/sheets/일본어/일본어_조건_표현_치트시트.html)
- [일본어 자동사·타동사 치트시트](https://brain.dongwook.kim/sheets/일본어/일본어_자동사_타동사_치트시트.html)
- [일본어 숫자 체계 치트시트](https://brain.dongwook.kim/sheets/일본어/일본어_숫자_체계_치트시트.html)

**Russian**
- [러시아어 치트시트](https://brain.dongwook.kim/sheets/러시아어/러시아어_치트시트.html)
- [러시아어 알파벳 이름](https://brain.dongwook.kim/sheets/러시아어/러시아어_알파벳_이름.html)
- [러시아어 모음 약화](https://brain.dongwook.kim/sheets/러시아어/러시아어_모음_약화.html)
- [러시아어 문자의 특징 치트시트](https://brain.dongwook.kim/sheets/러시아어/러시아어_문자의_특징_치트시트.html)
- [러시아어 격변화 치트시트](https://brain.dongwook.kim/sheets/러시아어/러시아어_격변화_치트시트.html)
- [러시아어 인칭대명사 치트시트](https://brain.dongwook.kim/sheets/러시아어/러시아어_인칭대명사_치트시트.html)
- [러시아어 동사 현재형 치트시트](https://brain.dongwook.kim/sheets/러시아어/러시아어_동사_현재형_치트시트.html)
- [러시아어 시간 표현 치트시트](https://brain.dongwook.kim/sheets/러시아어/러시아어_시간_표현_치트시트.html)
- [러시아어 소유대명사 치트시트](https://brain.dongwook.kim/sheets/러시아어/러시아어_소유대명사_치트시트.html)

**Chinese**
- [병음 표](https://brain.dongwook.kim/sheets/중국어/병음_표.html)
- [중국어 성모표](https://brain.dongwook.kim/sheets/중국어/중국어_성모표.html)
- [중국어 성조규칙](https://brain.dongwook.kim/sheets/중국어/중국어_성조규칙.html)
- [중국어 성조 연습](https://brain.dongwook.kim/sheets/중국어/중국어_성조_연습.html)
- [중국어 문자 치트시트](https://brain.dongwook.kim/sheets/중국어/중국어_문자_치트시트.html)
- [중국어 보어 총정리](https://brain.dongwook.kim/sheets/중국어/중국어_보어_총정리.html)
- [중국어 상관접속사 총정리](https://brain.dongwook.kim/sheets/중국어/중국어_상관접속사_총정리.html)
- [중국어 문장구조 핵심표](https://brain.dongwook.kim/sheets/중국어/중국어_문장구조_핵심표.html)
- [중국어 양사 빠른참조표](https://brain.dongwook.kim/sheets/중국어/중국어_양사_빠른참조표.html)
- [중국어 회화 표현모음](https://brain.dongwook.kim/sheets/중국어/중국어_회화_표현모음.html)

**German**
- [독일어 치트시트](https://brain.dongwook.kim/sheets/독일어/독일어_치트시트.html)
- [독일어 명사 치트시트](https://brain.dongwook.kim/sheets/독일어/독일어_명사_치트시트.html)
- [독일어 문자 치트시트](https://brain.dongwook.kim/sheets/독일어/독일어_문자_치트시트.html)
- [독일어 동사 치트시트](https://brain.dongwook.kim/sheets/독일어/독일어_동사_치트시트.html)
- [독일어 형용사 치트시트](https://brain.dongwook.kim/sheets/독일어/독일어_형용사_치트시트.html)
- [독일어 대명사 치트시트](https://brain.dongwook.kim/sheets/독일어/독일어_대명사_치트시트.html)
- [독일어 접속법 치트시트](https://brain.dongwook.kim/sheets/독일어/독일어_접속법_치트시트.html)
- [독일어 전치사 치트시트](https://brain.dongwook.kim/sheets/독일어/독일어_전치사_치트시트.html)
- [독일어 명사화 치트시트](https://brain.dongwook.kim/sheets/독일어/독일어_명사화_치트시트.html)

**French**
- [프랑스어 명사 치트시트](https://brain.dongwook.kim/sheets/프랑스어/프랑스어_명사_치트시트.html)
- [프랑스어 문자 치트시트](https://brain.dongwook.kim/sheets/프랑스어/프랑스어_문자_치트시트.html)
- [프랑스어 동사 현재형 치트시트](https://brain.dongwook.kim/sheets/프랑스어/프랑스어_동사_현재형_치트시트.html)
- [프랑스어 시제 마스터 치트시트](https://brain.dongwook.kim/sheets/프랑스어/프랑스어_시제_마스터_치트시트.html)
- [프랑스어 부정문 의문문 치트시트](https://brain.dongwook.kim/sheets/프랑스어/프랑스어_부정문_의문문_치트시트.html)
- [프랑스어 명령문 치트시트](https://brain.dongwook.kim/sheets/프랑스어/프랑스어_명령문_치트시트.html)
- [프랑스어 대명사 치트시트](https://brain.dongwook.kim/sheets/프랑스어/프랑스어_대명사_치트시트.html)
- [프랑스어 faire 동사 치트시트](https://brain.dongwook.kim/sheets/프랑스어/프랑스어_faire_동사_치트시트.html)

**Spanish**
- [스페인어 알파벳 이름](https://brain.dongwook.kim/sheets/스페인어/스페인어_알파벳_이름.html)
- [스페인어 발음 규칙](https://brain.dongwook.kim/sheets/스페인어/스페인어_발음_규칙.html)
- [스페인어 악센트 강세](https://brain.dongwook.kim/sheets/스페인어/스페인어_악센트_강세.html)
- [스페인어 특수부호 키보드](https://brain.dongwook.kim/sheets/스페인어/스페인어_특수부호_키보드.html)
- [스페인어 명사와 성 치트시트](https://brain.dongwook.kim/sheets/스페인어/스페인어_명사와_성_치트시트.html)

**English**
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
- [영어 동사구 치트시트](https://brain.dongwook.kim/sheets/영어/영어_동사구_치트시트.html)
- [영어 명사절 치트시트](https://brain.dongwook.kim/sheets/영어/영어_명사절_치트시트.html)
- [영어 문장 구조 심화 치트시트](https://brain.dongwook.kim/sheets/영어/영어_문장_구조_심화_치트시트.html)
- [영어 분사 치트시트](https://brain.dongwook.kim/sheets/영어/영어_분사_치트시트.html)
- [영어 회화 치트시트](https://brain.dongwook.kim/sheets/영어/영어_회화_치트시트.html)
- [영어 화법 치트시트](https://brain.dongwook.kim/sheets/영어/영어_화법_치트시트.html)
- [영어 한정사 치트시트](https://brain.dongwook.kim/sheets/영어/영어_한정사_치트시트.html)
- [영어 수 일치 치트시트](https://brain.dongwook.kim/sheets/영어/영어_수_일치_치트시트.html)
- [영어 청취 치트시트](https://brain.dongwook.kim/sheets/영어/영어_청취_치트시트.html)
- [영어 뉴스·시사 어휘 치트시트](https://brain.dongwook.kim/sheets/영어/영어_뉴스·시사_어휘_치트시트.html)
- [영어 프레젠테이션 치트시트](https://brain.dongwook.kim/sheets/영어/영어_프레젠테이션_치트시트.html)
- [영어 이력서·자소서 작성 치트시트](https://brain.dongwook.kim/sheets/영어/영어_이력서·자소서_작성_치트시트.html)
- [영어 인터넷 밈·은어 치트시트](https://brain.dongwook.kim/sheets/영어/영어_인터넷_밈·은어_치트시트.html)
- [영어 어휘 확장 치트시트](https://brain.dongwook.kim/sheets/영어/영어_어휘_확장_치트시트.html)
- [영어 슬랭·관용어 치트시트](https://brain.dongwook.kim/sheets/영어/영어_슬랭·관용어_치트시트.html)
- [영어 발음 치트시트](https://brain.dongwook.kim/sheets/영어/영어_발음_치트시트.html)
- [영어 쓰기 치트시트](https://brain.dongwook.kim/sheets/영어/영어_쓰기_치트시트.html)
- [영어 비즈니스 영어 치트시트](https://brain.dongwook.kim/sheets/영어/영어_비즈니스_영어_치트시트.html)
- [영어 독해 치트시트](https://brain.dongwook.kim/sheets/영어/영어_독해_치트시트.html)

**Music**
- [음악 이론 기초 치트시트](https://brain.dongwook.kim/sheets/음악_이론_기초_치트시트.html)

**Economics / Finance**
- [세금 용어 치트시트](https://brain.dongwook.kim/sheets/세금_용어_치트시트.html)
- [경제학 치트시트](https://brain.dongwook.kim/sheets/경제학_치트시트.html)
- [회계학 치트시트](https://brain.dongwook.kim/sheets/회계학_치트시트.html)
- [투자 기초 치트시트](https://brain.dongwook.kim/sheets/투자_기초_치트시트.html)
- [주식 용어 치트시트](https://brain.dongwook.kim/sheets/주식_용어_치트시트.html)
- [부동산 기초 치트시트](https://brain.dongwook.kim/sheets/부동산_기초_치트시트.html)

**Daily Life**
- [근로기준법 치트시트](https://brain.dongwook.kim/sheets/근로기준법_치트시트.html)

**Technology**
- [컴퓨터 부품](https://brain.dongwook.kim/sheets/컴퓨터_부품.html)

## Drills

Spaced-repetition (SM-2) vocabulary drills, served live at [brain.dongwook.kim](https://brain.dongwook.kim). Review progress is stored in your browser's localStorage only — it is not synced across devices.

**Japanese**
- [일본어 기초 어휘](https://brain.dongwook.kim/drills/일본어_기초_어휘.html)

**Chinese**
- [중국어 HSK 어휘](https://brain.dongwook.kim/drills/중국어_HSK_어휘.html)

**English**
- [영어 GRE 어휘](https://brain.dongwook.kim/drills/영어_GRE_어휘.html)

**French**
- [프랑스어 빈도 어휘](https://brain.dongwook.kim/drills/프랑스어_빈도_어휘.html)

**Arabic**
- [아랍어 기초 어휘](https://brain.dongwook.kim/drills/아랍어_기초_어휘.html)

**Russian**
- [러시아어 기초 어휘](https://brain.dongwook.kim/drills/러시아어_기초_어휘.html)

**Spanish**
- [스페인어 기초 어휘](https://brain.dongwook.kim/drills/스페인어_기초_어휘.html)

**German**
- [독일어 기초 어휘](https://brain.dongwook.kim/drills/독일어_기초_어휘.html)

## Installing the skills

```bash
npx skills@latest add kidow/skills/place-me
npx skills@latest add kidow/skills/teach-me
npx skills@latest add kidow/skills/review-me
```

## Usage

Run the learning skills from inside this repository.

```
/place-me Japanese writing system   # assess level → record in levels.md
/teach-me Japanese writing system   # learn piece by piece → commit to notes/
/review-me                          # review weakest topics → update levels.md
```

## Start your own brain

Copy the prompt below and paste it to your AI assistant (Claude Code recommended):

```
Set up a personal knowledge base using the PTR learning system (Place → Teach → Review).

1. Create a new git repository and open it in Claude Code.
2. Install the three learning skills:
   npx skills@latest add kidow/skills/place-me
   npx skills@latest add kidow/skills/teach-me
   npx skills@latest add kidow/skills/review-me
3. Create this file structure:
   - notes/      (empty folder — add a .gitkeep file so git tracks it)
   - levels.md   (empty file)
   - README.md   (copy from https://github.com/kidow/brain)

Once done, start with /place-me <topic> to assess your first topic.
```
