(() => {
  // 카테고리를 추가하면 여기에 한 줄 넣는다. 미완성 카테고리는 넣지 않는다.
  const CATEGORIES = [
    { name: '숫자', url: '/vocab/숫자.html' },
    { name: '색깔', url: '/vocab/색깔.html' },
    { name: '동물', url: '/vocab/동물.html' },
    { name: '신체', url: '/vocab/신체.html' },
    { name: '가족', url: '/vocab/가족.html' },
    { name: '음식', url: '/vocab/음식.html' },
    { name: '자연', url: '/vocab/자연.html' },
    { name: '시간', url: '/vocab/시간.html' },
    { name: '동작', url: '/vocab/동작.html' },
    { name: '기본 형용사', url: '/vocab/기본_형용사.html' },
    { name: '스포츠', url: '/vocab/스포츠.html' }
  ];

  const LANG_LABEL = {
    en: '영어', ja: '일본어', zh: '중국어', fr: '프랑스어',
    de: '독일어', es: '스페인어', ru: '러시아어', ar: '아랍어'
  };
  // 한중일 한자는 글꼴이 달라 lang 속성이 없으면 엉뚱한 자형으로 그려진다.
  const LANG_TAG = { en: 'en', ja: 'ja', zh: 'zh-Hans', fr: 'fr', de: 'de', es: 'es', ru: 'ru', ar: 'ar' };

  // 발음. drills/ 와 같은 Web Speech API를 쓰되 언어 코드는 여기서 매핑한다.
  const SPEAK_LANG = {
    en: 'en-US', ja: 'ja-JP', zh: 'zh-CN', fr: 'fr-FR',
    de: 'de-DE', es: 'es-ES', ru: 'ru-RU', ar: 'ar-SA'
  };
  const SPEAK_RATE = 0.9;
  const KANA_ONLY = /^[ぁ-ゖ゠-ヿー]+$/;
  const speakable = new Set();

  // 직접 만든 mp3가 (언어 × 카테고리) 단위로 전부 있는지. audio/manifest.json 이 원본이다.
  // 404 폴백을 쓰지 않는 이유는 audio/PLAN.md 참고 — 실패까지 걸리는 시간이 연속 재생을 망친다.
  let audioCats = {};

  const root = document.getElementById('vocab');
  if (!root) return;

  // 경로는 JSON의 category(공백 포함)가 아니라 파일명이다 — 기본_형용사 → "기본 형용사"로 어긋난다.
  const STEM = decodeURIComponent(String(root.dataset.src || '').split('/').pop()).replace(/\.json$/, '');
  const hasAudio = (lang) => (audioCats[lang] || []).includes(STEM);
  const audible = (lang) => hasAudio(lang) || speakable.has(lang);

  const el = (tag, cls, text) => {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  };

  const wide = window.matchMedia('(min-width: 768px)');
  let data = null;
  let selected = null;
  let coreOnly = false;

  const visible = () => data.concepts.filter((c) => !coreOnly || (c.lists || []).includes('swadesh'));

  // getVoices()는 첫 호출에서 빈 배열을 준다. 목록이 찰 때까지 기다렸다 첫 렌더를 해야
  // 버튼이 뒤늦게 나타났다 사라지는 깜빡임이 없다.
  const voicesReady = () => new Promise((done) => {
    if (!('speechSynthesis' in window)) return done([]);
    const now = speechSynthesis.getVoices();
    if (now.length) return done(now);
    let settled = false;
    const finish = () => { if (!settled) { settled = true; done(speechSynthesis.getVoices()); } };
    speechSynthesis.addEventListener('voiceschanged', finish, { once: true });
    setTimeout(finish, 2000);
  });

  const markSpeakable = (voices) => {
    speakable.clear();
    Object.entries(SPEAK_LANG).forEach(([lang, tag]) => {
      const prefix = tag.split('-')[0];
      if (voices.some((v) => v.lang.toLowerCase().replace('_', '-').startsWith(prefix))) speakable.add(lang);
    });
  };

  // 화면에 적어 둔 읽기 그대로 들리도록 언어별로 손본다.
  const speakText = (lang, entry) => {
    if (lang === 'ja') {
      // 한자만 있는 표기는 TTS가 음독으로 잘못 읽는다(青 → せい). rom의 かな를 넘긴다.
      const kana = String(entry.rom || '').split('·')[0].trim();
      if (KANA_ONLY.test(kana)) return kana;
    }
    if (lang === 'ru') {
      // 강세 기호(U+0301)는 사전 표기용이라 입력에서 뺀다. 아랍어는 반대로 모음부호를 남겨야 정확히 읽힌다.
      return entry.word.normalize('NFD').replace(/́/g, '').normalize('NFC');
    }
    return entry.word;
  };

  let seq = 0;
  let playing = null;
  const stopSpeaking = () => {
    seq += 1;
    if ('speechSynthesis' in window) speechSynthesis.cancel();
    if (playing) { playing.pause(); playing = null; }
    document.querySelectorAll('.playing').forEach((b) => b.classList.remove('playing'));
  };

  const utter = (lang, entry) => new Promise((done) => {
    const u = new SpeechSynthesisUtterance(speakText(lang, entry));
    u.lang = SPEAK_LANG[lang];
    u.rate = SPEAK_RATE;
    u.onend = done;
    u.onerror = done;
    speechSynthesis.speak(u);
  });

  // scripts/build_vocab_audio.py 가 쓰는 경로와 같은 규칙: <개념>[-alt번호].mp3
  const playFile = (lang, id, alt) => new Promise((done) => {
    const url = `/audio/${lang}/${encodeURIComponent(STEM)}/${encodeURIComponent(id)}${alt ? `-${alt}` : ''}.mp3`;
    const a = new Audio(url);
    playing = a;
    a.onended = done;
    a.onerror = done;
    a.play().catch(done);
  });

  // mp3가 있으면 mp3, 없으면 Web Speech. 둘 다 없는 언어는 애초에 버튼이 안 붙는다.
  const say = (lang, entry, id, alt) => (
    hasAudio(lang) ? playFile(lang, id, alt) : utter(lang, entry));

  const playOne = async (lang, entry, btn, id, alt) => {
    const already = btn.classList.contains('playing');
    stopSpeaking();
    if (already) return;
    const token = seq;
    btn.classList.add('playing');
    await say(lang, entry, id, alt);
    if (token === seq) btn.classList.remove('playing');
  };

  // 본항만 순서대로. alt는 각 줄의 버튼으로 따로 듣는다.
  const playAll = async (concept, btn) => {
    const already = btn.classList.contains('playing');
    stopSpeaking();
    if (already) return;
    const token = seq;
    btn.classList.add('playing');
    for (const lang of data.languages) {
      if (token !== seq) return;
      const entry = concept.words[lang];
      if (!entry || !audible(lang)) continue;
      await say(lang, entry, concept.id, 0);
    }
    if (token === seq) btn.classList.remove('playing');
  };

  const playBtn = (lang, entry, id, alt) => {
    const btn = el('button', 'play-btn', '🔊');
    btn.type = 'button';
    btn.setAttribute('aria-label', `${LANG_LABEL[lang]} 발음 듣기`);
    btn.addEventListener('click', (e) => { e.preventDefault(); playOne(lang, entry, btn, id, alt); });
    return btn;
  };

  // 언어 한 줄: 원어 + 로마자/현지표기 + 한글 음차, 그 아래 alt 들여쓰기
  const entryLine = (lang, entry, isAlt, id, alt) => {
    const wrap = el('span', isAlt ? 'entry alt' : 'entry');
    const line = el('span', 'wordline');
    const word = el('span', 'word', entry.word);
    word.lang = LANG_TAG[lang];
    if (lang === 'ar') word.dir = 'rtl';
    line.appendChild(word);
    // mp3도 없고 이 기기에 해당 언어 음성도 없으면 버튼 자체를 만들지 않는다.
    if (audible(lang)) line.appendChild(playBtn(lang, entry, id, alt));
    wrap.appendChild(line);
    const meta = el('span', 'meta');
    if (entry.rom) meta.appendChild(el('span', 'rom', entry.rom));
    if (entry.kor) meta.appendChild(el('span', 'kor', entry.kor));
    if (entry.label) meta.appendChild(el('span', 'tag', entry.label));
    if (meta.childNodes.length) wrap.appendChild(meta);
    return wrap;
  };

  const langRow = (lang, entry, id) => {
    const row = el('div', 'row');
    row.appendChild(el('span', 'lang', LANG_LABEL[lang] || lang));
    const body = el('span', 'body');
    body.appendChild(entryLine(lang, entry, false, id, 0));
    (entry.alt || []).forEach((a, i) => body.appendChild(entryLine(lang, a, true, id, i + 1)));
    row.appendChild(body);
    return row;
  };

  const conceptBody = (concept) => {
    const box = el('div', 'concept-body');
    const heard = data.languages.filter((l) => concept.words[l] && audible(l));
    if (heard.length > 1) {
      const bar = el('div', 'speak-bar');
      const all = el('button', 'listen-all', `▶ ${heard.length}개 언어 순서대로`);
      all.type = 'button';
      all.addEventListener('click', (e) => { e.preventDefault(); playAll(concept, all); });
      bar.appendChild(all);
      box.appendChild(bar);
    }
    data.languages.forEach((lang) => {
      const entry = concept.words[lang];
      if (entry) box.appendChild(langRow(lang, entry, concept.id));
    });
    (concept.notes || []).forEach((note) => {
      const memo = el('div', 'memo');
      memo.appendChild(el('b', null, '참고'));
      memo.appendChild(el('span', null, note));
      box.appendChild(memo);
    });
    return box;
  };

  // swatch는 색깔 카테고리 전용 선택 필드. 없는 카테고리에 빈 네모를 그리지 않는다.
  const titleOf = (concept) => {
    const t = el('span', 'concept-title');
    if (concept.swatch) {
      const dot = el('i', 'swatch');
      dot.style.background = concept.swatch;
      t.appendChild(dot);
    }
    t.appendChild(el('span', null, concept.ko));
    return t;
  };

  // 모바일: 아코디언. <details>를 그대로 쓴다 — 여닫기 JS가 필요 없다.
  const renderAccordion = (host) => {
    visible().forEach((concept) => {
      const item = el('details', 'acc');
      item.id = concept.id;
      const head = el('summary');
      head.appendChild(titleOf(concept));
      item.appendChild(head);
      item.appendChild(conceptBody(concept));
      item.addEventListener('toggle', () => {
        stopSpeaking();
        if (item.open) history.replaceState(null, '', '#' + concept.id);
      });
      if (concept.id === selected) item.open = true;
      host.appendChild(item);
    });
    // 링크로 들어온 개념이 화면 밖이면 직접 스크롤해야 하므로 끌어올린다.
    const opened = selected && document.getElementById(selected);
    if (opened) opened.scrollIntoView({ block: 'start' });
  };

  // 데스크탑: 마스터–디테일. 왼쪽 목록 고정, 오른쪽 패널만 교체.
  const renderMasterDetail = (host) => {
    const grid = el('div', 'md');
    const list = el('div', 'md-list');
    const panel = el('div', 'md-panel');
    const items = visible();

    const show = (concept) => {
      selected = concept.id;
      stopSpeaking();
      history.replaceState(null, '', '#' + concept.id);
      panel.textContent = '';
      const h = el('p', 'md-title');
      h.appendChild(titleOf(concept));
      panel.appendChild(h);
      panel.appendChild(conceptBody(concept));
      [...list.children].forEach((b) => b.setAttribute('aria-current', String(b.dataset.id === concept.id)));
    };

    items.forEach((concept) => {
      const btn = el('button', 'md-item');
      btn.type = 'button';
      btn.dataset.id = concept.id;
      btn.appendChild(titleOf(concept));
      btn.addEventListener('click', () => show(concept));
      list.appendChild(btn);
    });

    grid.appendChild(list);
    grid.appendChild(panel);
    host.appendChild(grid);
    const start = items.find((c) => c.id === selected) || items[0];
    if (start) show(start);
  };

  const renderView = () => {
    const host = document.getElementById('vocab-view');
    stopSpeaking();
    host.textContent = '';
    if (!visible().length) {
      host.appendChild(el('p', 'empty', '표시할 개념이 없습니다.'));
      return;
    }
    if (wide.matches) renderMasterDetail(host);
    else renderAccordion(host);
  };

  const renderShell = () => {
    root.textContent = '';

    const head = el('header');
    head.appendChild(el('p', 'eyebrow', 'brain · 단어장'));
    head.appendChild(el('h1', null, data.category));
    head.appendChild(el('p', 'sub', `${data.languages.length}개 언어 대조 · 개념 ${data.concepts.length}개`));
    root.appendChild(head);

    if (CATEGORIES.length > 1) {
      const nav = el('nav', 'catnav');
      CATEGORIES.forEach((c) => {
        const a = el('a', c.name === data.category ? 'on' : null, c.name);
        a.href = c.url;
        nav.appendChild(a);
      });
      root.appendChild(nav);
    }

    const coreCount = data.concepts.filter((c) => (c.lists || []).includes('swadesh')).length;
    if (coreCount && coreCount < data.concepts.length) {
      const bar = el('div', 'toolbar');
      const label = el('label');
      const box = document.createElement('input');
      box.type = 'checkbox';
      box.addEventListener('change', () => { coreOnly = box.checked; renderView(); });
      label.appendChild(box);
      label.appendChild(el('span', null, `Swadesh 코어만 보기 (${coreCount}개)`));
      bar.appendChild(label);
      root.appendChild(bar);
    }

    const view = el('div');
    view.id = 'vocab-view';
    root.appendChild(view);

    const foot = el('footer', 'sources');
    foot.appendChild(el('b', null, '출처'));
    const ul = el('ul');
    Object.entries(data.sources || {}).forEach(([key, value]) => {
      ul.appendChild(el('li', null, `${key} — ${value}`));
    });
    foot.appendChild(ul);
    root.appendChild(foot);
  };

  const boot = async () => {
    const src = root.dataset.src;
    try {
      // 데이터·음성 목록·매니페스트를 함께 기다린다 — 첫 렌더부터 버튼 유무가 확정된다.
      // 매니페스트는 없어도 Web Speech로 굴러가야 하므로 실패를 삼킨다.
      const [res, voices, cats] = await Promise.all([
        fetch(src),
        voicesReady(),
        fetch('/audio/manifest.json').then((r) => (r.ok ? r.json() : {})).catch(() => ({}))
      ]);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      markSpeakable(voices);
      audioCats = cats;
      data = await res.json();
    } catch (err) {
      root.textContent = '';
      root.appendChild(el('p', 'empty', `데이터를 불러오지 못했습니다 (${err.message})`));
      return;
    }
    const hash = decodeURIComponent(location.hash.replace('#', ''));
    if (data.concepts.some((c) => c.id === hash)) selected = hash;
    renderShell();
    renderView();
    wide.addEventListener('change', renderView);
    // 음성이 fetch보다 늦게 도착한 드문 경우만 한 번 더 반영한다.
    if ('speechSynthesis' in window) {
      speechSynthesis.addEventListener('voiceschanged', () => {
        const before = speakable.size;
        markSpeakable(speechSynthesis.getVoices());
        if (speakable.size !== before) renderView();
      });
    }
  };

  boot();
})();
