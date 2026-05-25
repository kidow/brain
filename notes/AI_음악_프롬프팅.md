# AI 음악 프롬프팅

## 메타태그란 무엇인가

대괄호 `[]` 안에 쓰는 특수 지시어. 일반 프롬프트 텍스트와 달리 모델에게 음악의 구조·형식에 관한 명령임을 알린다.

두 종류:

| 종류 | 예시 | 역할 |
|------|------|------|
| 보컬 제어 | `[instrumental]`, `[no vocals]` | 보컬 완전 제거 |
| 섹션 구조 | `[Verse]`, `[Chorus]`, `[Bridge]`, `[Outro]` | 해당 위치에서 곡 구조 전환 |

예시:
```
[instrumental]
electronic dance, 129 BPM, synth layers, driving energy
```
→ 맨 앞에 `[instrumental]` 하나만 추가하면 보컬 없는 순수 기악 트랙 생성.

## 섹션 태그로 곡 구조 설계하기

가사 안에 삽입해서 곡의 흐름을 직접 지정. Suno 기준:

```
[Verse]
(가사 1절)

[Chorus]
(후렴 가사)

[Verse]
(가사 2절)

[Chorus]
(후렴 반복)

[Bridge]
(브릿지 가사)

[Outro]
```

핵심:
- 태그 없으면 AI가 구조 알아서 결정 → 매번 달라짐
- 태그 있으면 전환점 고정 → `[Chorus]` 직후 에너지·멜로디 후렴 패턴으로 전환

입력란 분리: Style 칸 = 무드/장르 텍스트, Lyrics 칸 = `[Verse]/[Chorus]` 구조.

## 스타일 레퍼런스 프롬프팅

특정 아티스트의 사운드 스타일을 참고시키는 기법. 직접 방식과 우회 방식 두 가지.

**직접 방식** (Udio에서 주로 작동):
```
style of Daft Punk, electronic dance, 129 BPM, driving energy
```

**우회 방식** (저작권 이슈 회피, Suno 권장):
아티스트 이름 대신 그 특징을 묘사.
```
vocoded robotic vocals, vintage analog synths, four-on-the-floor kick,
french house filter sweep, 128 BPM
```

Suno는 실존 아티스트 이름을 쓰면 거부하거나 결과물 희석. 이름 대신 **소리의 특징으로 번역**하는 능력이 핵심.

## 네거티브 프롬프팅의 정밀화

`avoiding direct artist imitation`은 범용 면책 문구 — 사운드 제어력 약함.

**효과 약한 방식:**
```
avoiding direct artist imitation, song cloning, or replication
```

**효과 강한 방식 — 원하지 않는 소리를 구체적으로 명시:**
```
no distorted guitar, no acoustic instruments, no jazz chords,
no slow tempo, no ambient pads
```

Suno는 네거티브 프롬프트를 소리 단위로 처리. "아티스트 모방 금지"는 모호하지만 "no acoustic drums"는 즉각 반영.

조합 예시:
```
electronic dance, 129 BPM, synth layers, driving energy,
no acoustic instruments, no vocals, no jazz harmony, no reverb-heavy pads
```

## 에너지 곡선 설계

단일 프롬프트는 곡 전체에 동일한 에너지 적용. 인트로→드롭 구조를 만들려면 섹션별 에너지를 다르게 지시.

**방법: 섹션 태그 + 소괄호 지시어 조합**

```
[Intro]
(soft, minimal synth, no drums, building tension)

[Verse]
(mid-energy, kick drum enters, synth melody)

[Chorus]
(full energy, heavy bass drop, layered synths, driving beat)

[Bridge]
(stripped back, only pads and melody, anticipation)

[Chorus]
(maximum energy, distorted synth, euphoric)

[Outro]
(gradual fadeout, reverb tail)
```

소괄호 `()` 안 = 해당 섹션에만 적용되는 사운드 지시.

**전역 프롬프트(Style 칸) = 전체 색깔, 섹션 지시(Lyrics 칸 소괄호) = 구간별 명암.**

## 음악 이론 용어로 사운드 고정하기

무드·에너지 형용사는 AI가 넓게 해석. 음악 이론 용어를 쓰면 좁고 정확하게 고정.

| 모호한 표현 | 정밀한 표현 |
|------------|------------|
| `dark mood` | `minor key, diminished chords` |
| `happy feel` | `major key, bright chord voicings` |
| `groovy` | `syncopated rhythm, off-beat hi-hat` |
| `epic` | `orchestral swell, rising fifth interval` |
| `tense` | `tritone harmony, unresolved chord progression` |

키·스케일·코드 진행 직접 명시:
```
A minor, i-VI-III-VII chord progression, 129 BPM,
synth lead melody, four-on-the-floor kick
```

**형용사 = 느낌 전달, 이론 용어 = 소리 고정.** 조합하면 재현 가능성 높아짐.

## Extend & Remaster 전략

**Extend (곡 연장):** 생성된 트랙의 특정 구간 이후를 이어서 생성.
- Suno: 트랙 선택 → Extend 버튼 → 타임스탬프 지정
- 새 섹션 태그/가사 추가로 방향 제어

**Remaster:** 동일 구조·멜로디 유지, 음질·믹스 개선. 프롬프트 변경 없이 더 나은 버전 추출.

**실전 워크플로우:**
1. 같은 프롬프트로 3~4회 생성
2. 가장 좋은 것 선택
3. Extend로 구조 완성
4. Remaster로 품질 개선

생성은 확률적 — 한 번에 완성하려 하지 말고 **선택 → 연장 → 개선** 흐름 사용.

## Custom Mode vs Simple Mode

**Simple Mode:** 텍스트 하나 입력 → AI가 가사·구조·스타일 전부 결정. 빠르지만 제어 불가.

**Custom Mode 입력란:**
- Style 칸: 장르·악기·무드·BPM 등 사운드 지시
- Lyrics 칸: 실제 가사 + 섹션 태그
- Title 칸: 곡 제목 (품질에 미묘하게 영향)

Lyrics 칸 전략:

| 입력 | 결과 |
|------|------|
| 비워둠 | AI가 보컬 없는 기악 트랙 생성 경향 |
| `[instrumental]` | 명시적으로 보컬 제거 |
| 섹션 태그 + 가사 | 구조·가사 고정 |

**Simple Mode = 탐색용, Custom Mode = 완성용.**


## 보컬 스타일 프롬프팅

보컬이 있는 트랙에서 성질 제어 가능.

**성별·음역:** `female vocalist, soprano range` / `male vocalist, deep baritone` / `androgynous vocals`

**창법·질감:**
```
breathy vocals        # 숨 섞인 목소리
raspy vocals          # 거친 목소리
falsetto              # 팔세토
vocoded               # 보코더 처리
auto-tuned, robotic   # 오토튠 강하게
choir, layered vocals # 합창 레이어
```

**언어 지정:** `Korean lyrics` / `Japanese vocals` / `English rap verses`

주의: 한국어·일본어는 언어 지정만으로 부족 → Lyrics 칸에 직접 해당 언어로 가사 입력해야 확실.

## 프롬프트 A/B 테스트 전략

좋은 프롬프트는 한 번에 나오지 않음. **변수를 하나씩 바꾸면서** 무엇이 결과를 바꾸는지 추적.

원칙: 한 번에 하나만 변경.
```
# 기준
electronic dance, 129 BPM, synth layers, driving energy, minor key

# 테스트 A — BPM만 변경
electronic dance, 140 BPM, synth layers, driving energy, minor key

# 테스트 B — 키만 변경
electronic dance, 129 BPM, synth layers, driving energy, major key
```

**변수 영향력 순위:**
1. 장르 키워드 (가장 큰 영향)
2. BPM
3. 키(major/minor)
4. 악기 조합
5. 에너지 형용사 (가장 작은 영향)

마음에 드는 트랙이 나왔을 때 프롬프트를 그대로 저장. AI는 같은 프롬프트도 매번 다른 결과 → **프롬프트 + 운**의 조합.

## 구간 재생성 (Inpainting)

트랙 전체는 괜찮은데 특정 구간만 문제일 때 사용.

**Suno 기준:**
1. 트랙 재생 중 문제 구간 드래그 선택
2. Recut → 해당 부분만 재생성
3. 나머지 구간 그대로 유지

활용 케이스:
- 브릿지만 어색함 → 브릿지 구간만 재생성
- 인트로 드럼 너무 강함 → 인트로만 다시 뽑음
- 후렴 멜로디는 좋은데 2절 가사 발음 이상 → 2절만 재생성

한계: 재생성 구간이 앞뒤와 이음새에서 어색해질 수 있음. 기악 트랙이 보컬 트랙보다 결과 자연스러움.

Extend = 앞에서 뒤로 이어가기. Inpainting = 중간 구간 교체.
