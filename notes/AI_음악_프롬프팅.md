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
