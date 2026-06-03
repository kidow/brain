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

## Notes

All knowledge notes served live at [brain.dongwook.kim](https://brain.dongwook.kim).

**Languages — Japanese**
- [히라가나](https://brain.dongwook.kim/notes/히라가나)
- [가타카나](https://brain.dongwook.kim/notes/가타카나)
- [일본어 문자의 특징](https://brain.dongwook.kim/notes/일본어_문자의_특징)
- [일본어 기본 한자](https://brain.dongwook.kim/notes/일본어_기본_한자)

**Languages — Chinese**
- [중국어 문자](https://brain.dongwook.kim/notes/중국어_문자)

**Languages — Russian**
- [러시아어 문자의 특징](https://brain.dongwook.kim/notes/러시아어_문자의_특징)

**Languages — Spanish**
- [스페인어 문자](https://brain.dongwook.kim/notes/스페인어_문자)

**Languages — German**
- [독일어 문자](https://brain.dongwook.kim/notes/독일어_문자)

**Languages — French**
- [프랑스어 문자](https://brain.dongwook.kim/notes/프랑스어_문자)

**Languages — Arabic**
- [아랍어 문자](https://brain.dongwook.kim/notes/아랍어_문자)

**Languages — English**
- [영어](https://brain.dongwook.kim/notes/영어)

**Music**
- [음악 이론 기초](https://brain.dongwook.kim/notes/음악_이론_기초)
- [AI 음악 프롬프팅](https://brain.dongwook.kim/notes/AI_음악_프롬프팅)

**Art**
- [미술 작품 교양](https://brain.dongwook.kim/notes/미술_작품_교양)

**Science**
- [화학](https://brain.dongwook.kim/notes/화학)

## Cheat Sheets

Quick-reference sheets served live at [brain.dongwook.kim](https://brain.dongwook.kim).

**Japanese**
- [히라가나 치트시트](https://brain.dongwook.kim/sheets/히라가나_치트시트.html)
- [가타카나 치트시트](https://brain.dongwook.kim/sheets/가타카나_치트시트.html)

**Russian**
- [러시아어 치트시트](https://brain.dongwook.kim/sheets/러시아어_치트시트.html)
- [러시아어 알파벳 이름](https://brain.dongwook.kim/sheets/러시아어_알파벳_이름.html)
- [러시아어 모음 약화](https://brain.dongwook.kim/sheets/러시아어_모음_약화.html)

**Chinese**
- [병음 표](https://brain.dongwook.kim/sheets/병음_표.html)

**German**
- [독일어 치트시트](https://brain.dongwook.kim/sheets/독일어_치트시트.html)

**Spanish**
- [스페인어 알파벳 이름](https://brain.dongwook.kim/sheets/스페인어_알파벳_이름.html)

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
