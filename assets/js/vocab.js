(() => {
  // 카테고리를 추가하면 여기에 한 줄 넣는다. 미완성 카테고리는 넣지 않는다.
  const CATEGORIES = [
    { name: '숫자', url: '/vocab/숫자.html' },
    { name: '색깔', url: '/vocab/색깔.html' },
    { name: '동물', url: '/vocab/동물.html' },
    { name: '신체', url: '/vocab/신체.html' },
    { name: '가족', url: '/vocab/가족.html' },
    { name: '음식', url: '/vocab/음식.html' },
    { name: '자연', url: '/vocab/자연.html' }
  ];

  const LANG_LABEL = {
    en: '영어', ja: '일본어', zh: '중국어', fr: '프랑스어',
    de: '독일어', es: '스페인어', ru: '러시아어', ar: '아랍어'
  };
  // 한중일 한자는 글꼴이 달라 lang 속성이 없으면 엉뚱한 자형으로 그려진다.
  const LANG_TAG = { en: 'en', ja: 'ja', zh: 'zh-Hans', fr: 'fr', de: 'de', es: 'es', ru: 'ru', ar: 'ar' };

  const root = document.getElementById('vocab');
  if (!root) return;

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

  // 언어 한 줄: 원어 + 로마자/현지표기 + 한글 음차, 그 아래 alt 들여쓰기
  const entryLine = (lang, entry, isAlt) => {
    const wrap = el('span', isAlt ? 'entry alt' : 'entry');
    const word = el('span', 'word', entry.word);
    word.lang = LANG_TAG[lang];
    if (lang === 'ar') word.dir = 'rtl';
    wrap.appendChild(word);
    const meta = el('span', 'meta');
    if (entry.rom) meta.appendChild(el('span', 'rom', entry.rom));
    if (entry.kor) meta.appendChild(el('span', 'kor', entry.kor));
    if (entry.label) meta.appendChild(el('span', 'tag', entry.label));
    if (meta.childNodes.length) wrap.appendChild(meta);
    return wrap;
  };

  const langRow = (lang, entry) => {
    const row = el('div', 'row');
    row.appendChild(el('span', 'lang', LANG_LABEL[lang] || lang));
    const body = el('span', 'body');
    body.appendChild(entryLine(lang, entry, false));
    (entry.alt || []).forEach((a) => body.appendChild(entryLine(lang, a, true)));
    row.appendChild(body);
    return row;
  };

  const conceptBody = (concept) => {
    const box = el('div', 'concept-body');
    data.languages.forEach((lang) => {
      const entry = concept.words[lang];
      if (entry) box.appendChild(langRow(lang, entry));
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
      const res = await fetch(src);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
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
  };

  boot();
})();
