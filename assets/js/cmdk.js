// 전역 검색 팔레트(⌘K / Ctrl+K). 인덱스는 처음 열 때 search-index.js를 불러와서 만든다.
(() => {
  const LIMIT = 20;
  const isMac = /Mac|iPhone|iPad/.test(navigator.userAgentData?.platform || navigator.platform);
  const shortcut = isMac ? '⌘K' : 'Ctrl K';
  const searchPageInput = document.getElementById('search-input');

  const style = document.createElement('style');
  style.textContent = `
.brain-page-actions{display:flex;justify-content:flex-end;gap:.5rem;padding:1rem 1rem 0}
.brain-cmdk-open{display:inline-flex;align-items:center;gap:.45rem;padding:.5rem .7rem;border:1px solid #60a5fa;border-radius:999px;background:#0f172a;color:#e2e8f0;font:600 14px/1 system-ui,sans-serif;cursor:pointer}
.brain-cmdk-open:hover,.brain-cmdk-open:focus{background:#1e293b;outline:2px solid #60a5fa;outline-offset:2px}
.brain-cmdk-open kbd,.brain-cmdk-foot kbd{padding:.1rem .3rem;border:1px solid #334155;border-radius:.25rem;background:#1e293b;color:#94a3b8;font:500 12px/1.2 system-ui,sans-serif}
.brain-cmdk{width:min(640px,calc(100vw - 2rem));max-height:min(560px,calc(100vh - 4rem));margin:10vh auto auto;padding:0;border:1px solid #334155;border-radius:.75rem;background:#0f172a;color:#e2e8f0;font:15px/1.5 system-ui,-apple-system,sans-serif;box-shadow:0 20px 50px rgba(0,0,0,.5);overflow:hidden}
.brain-cmdk[open]{display:flex;flex-direction:column}
.brain-cmdk::backdrop{background:rgba(2,6,23,.6)}
.brain-cmdk-input{box-sizing:border-box;width:100%;margin:0;padding:1rem 1.1rem;border:0;border-bottom:1px solid #334155;background:transparent;color:#e2e8f0;font:inherit;font-size:1.05rem;outline:none}
.brain-cmdk-input::placeholder{color:#94a3b8}
.brain-cmdk-list{flex:1;overflow-y:auto;margin:0;padding:.4rem;list-style:none}
.brain-cmdk-list li{margin:0;padding:.6rem .75rem;border-radius:.5rem;cursor:pointer}
.brain-cmdk-list li[aria-selected="true"]{background:#1e293b;box-shadow:inset 3px 0 0 #60a5fa}
.brain-cmdk-title{display:flex;align-items:baseline;gap:.5rem;color:#e2e8f0;font-weight:600}
.brain-cmdk-type{flex:none;color:#60a5fa;font-size:.78rem;font-weight:500}
.brain-cmdk-snippet{margin-top:.15rem;overflow:hidden;color:#94a3b8;font-size:.85rem;white-space:nowrap;text-overflow:ellipsis}
.brain-cmdk-foot{display:flex;justify-content:space-between;gap:1rem;margin:0;padding:.55rem 1rem;border-top:1px solid #334155;color:#94a3b8;font-size:.8rem}
@media (max-width:600px){.brain-cmdk{margin-top:1rem;max-height:calc(100vh - 2rem)}.brain-cmdk-keys{display:none}}
@media print{.brain-page-actions{display:none}}`;
  document.head.append(style);

  // 검색 페이지에서는 팔레트 대신 페이지 검색창으로 보낸다.
  if (searchPageInput) {
    document.addEventListener('keydown', (event) => {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') { event.preventDefault(); searchPageInput.focus(); searchPageInput.select(); }
    });
    return;
  }

  const dialog = document.createElement('dialog');
  dialog.className = 'brain-cmdk';
  dialog.setAttribute('aria-label', '문서 검색');
  dialog.innerHTML = `
<input class="brain-cmdk-input" type="text" placeholder="노트·치트시트·드릴·단어장 검색" autocomplete="off" spellcheck="false"
  role="combobox" aria-expanded="true" aria-controls="brain-cmdk-list" aria-autocomplete="list">
<ul class="brain-cmdk-list" id="brain-cmdk-list" role="listbox" aria-label="검색 결과"></ul>
<p class="brain-cmdk-foot"><span class="brain-cmdk-status" role="status"></span><span class="brain-cmdk-keys"><kbd>↑</kbd> <kbd>↓</kbd> 이동 · <kbd>Enter</kbd> 열기 · <kbd>Esc</kbd> 닫기</span></p>`;
  const input = dialog.querySelector('.brain-cmdk-input');
  const list = dialog.querySelector('.brain-cmdk-list');
  const status = dialog.querySelector('.brain-cmdk-status');

  let index = null;
  let items = [];
  let active = 0;

  let scriptLoading;
  const loadIndex = () => {
    scriptLoading = scriptLoading || (window.BrainSearch ? Promise.resolve() : new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = '/assets/js/search-index.js';
      script.onload = resolve;
      script.onerror = () => { scriptLoading = null; script.remove(); reject(new Error('search-index.js unavailable')); };
      document.head.append(script);
    }));
    return scriptLoading.then(() => window.BrainSearch.load());
  };

  const select = (next) => {
    if (!items.length) return;
    active = (next + items.length) % items.length;
    [...list.children].forEach((node, position) => node.setAttribute('aria-selected', String(position === active)));
    const current = list.children[active];
    input.setAttribute('aria-activedescendant', current.id);
    current.scrollIntoView({ block: 'nearest' });
  };

  const render = () => {
    const query = input.value;
    list.replaceChildren();
    input.removeAttribute('aria-activedescendant');
    items = [];
    if (!index) return;
    if (!query.trim()) { status.textContent = `${index.length.toLocaleString('ko-KR')}개 항목에서 검색`; return; }

    const { typeLabel, search, snippet } = window.BrainSearch;
    const matched = search(index, query, { limit: LIMIT });
    items = [
      ...matched.map((entry) => ({ url: entry.url, title: entry.title, type: typeLabel[entry.type], text: snippet(entry, query, 30) })),
      { url: `/search/?q=${encodeURIComponent(query)}`, title: `‘${query}’ 전체 결과 보기`, type: '검색', text: '유형 필터와 함께 모든 결과를 봅니다' }
    ];
    items.forEach((item, position) => {
      const node = document.createElement('li');
      node.id = `brain-cmdk-item-${position}`;
      node.setAttribute('role', 'option');
      const title = document.createElement('div'); title.className = 'brain-cmdk-title';
      const name = document.createElement('span'); name.textContent = item.title;
      const type = document.createElement('span'); type.className = 'brain-cmdk-type'; type.textContent = item.type;
      const text = document.createElement('div'); text.className = 'brain-cmdk-snippet'; text.textContent = item.text;
      title.append(name, type); node.append(title, text);
      node.addEventListener('mousemove', () => { if (active !== position) select(position); });
      node.addEventListener('click', (event) => go(position, event.metaKey || event.ctrlKey));
      list.append(node);
    });
    status.textContent = matched.length ? `${matched.length}${matched.length === LIMIT ? '+' : ''}개 결과` : '결과 없음';
    select(0);
  };

  const go = (position, newTab) => {
    const item = items[position];
    if (!item) return;
    if (newTab) { window.open(item.url, '_blank', 'noopener'); return; }
    dialog.close();
    location.href = item.url;
  };

  const open = () => {
    if (dialog.open) { input.select(); return; }
    dialog.showModal();
    input.select();
    if (index) { render(); return; }
    status.textContent = '검색 인덱스를 불러오는 중…';
    loadIndex().then((loaded) => { index = loaded; render(); }).catch((error) => {
      console.warn('Search index unavailable:', error);
      status.textContent = '검색 인덱스를 불러오지 못했습니다. 다시 열어 주세요.';
    });
  };

  input.addEventListener('input', render);
  input.addEventListener('keydown', (event) => {
    if (event.isComposing) return; // 한글 조합 중 Enter·화살표는 IME 몫
    if (event.key === 'ArrowDown') { event.preventDefault(); select(active + 1); }
    else if (event.key === 'ArrowUp') { event.preventDefault(); select(active - 1); }
    else if (event.key === 'Enter') { event.preventDefault(); go(active, event.metaKey || event.ctrlKey); }
  });
  // 바깥(backdrop) 클릭은 dialog 자신이 target이 된다.
  dialog.addEventListener('click', (event) => { if (event.target === dialog) dialog.close(); });
  document.addEventListener('keydown', (event) => {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
      event.preventDefault();
      dialog.open ? dialog.close() : open();
    }
  });

  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'brain-cmdk-open';
  button.setAttribute('aria-label', `문서 검색 (${shortcut})`);
  button.innerHTML = `검색 <kbd>${shortcut}</kbd>`;
  button.addEventListener('click', open);

  const mount = () => {
    // copy-link.js와 같은 버튼 줄을 쓴다. 먼저 실행된 쪽이 줄을 만든다.
    let actions = document.querySelector('.brain-page-actions');
    if (!actions) {
      actions = document.createElement('div');
      actions.className = 'brain-page-actions';
      document.body.prepend(actions);
    }
    actions.prepend(button);
    document.body.append(dialog);
  };
  document.body ? mount() : document.addEventListener('DOMContentLoaded', mount);
})();
