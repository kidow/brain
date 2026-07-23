(() => {
  const documentSources = JSON.parse(document.getElementById('document-sources').textContent);
  const form = document.getElementById('search-form');
  const input = document.getElementById('search-input');
  const status = document.getElementById('search-status');
  const results = document.getElementById('search-results');
  const filters = [...document.querySelectorAll('.filter')];
  let activeFilter = 'all';
  let index = [];
  let loading;

  const typeLabel = { note: '노트', sheet: '치트시트', drill: '드릴' };
  const normalize = (text) => String(text || '')
    .normalize('NFKC').toLocaleLowerCase()
    .replace(/[\p{P}\p{S}]+/gu, ' ')
    .replace(/\s+/g, ' ').trim();
  const plainText = (text) => String(text || '')
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/!?(\[[^\]]*\])\([^)]*\)/g, '$1')
    .replace(/[#>*_`~|]/g, ' ')
    .replace(/\s+/g, ' ').trim();
  const htmlText = (html) => {
    const documentFragment = new DOMParser().parseFromString(html, 'text/html');
    documentFragment.querySelectorAll('script, style, noscript, template').forEach((node) => node.remove());
    return plainText(documentFragment.body.textContent);
  };

  const mapWithConcurrency = async (items, limit, mapper) => {
    const output = new Array(items.length);
    let cursor = 0;
    const worker = async () => {
      while (cursor < items.length) {
        const current = cursor++;
        output[current] = await mapper(items[current]);
      }
    };
    await Promise.all(Array.from({ length: Math.min(limit, items.length) }, worker));
    return output;
  };

  const readSource = async (source) => {
    try {
      const response = await fetch(source.url);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      if (source.type === 'drill-data') {
        const words = await response.json();
        return Array.isArray(words) ? words.map((word) => ({
          type: 'drill', title: source.title, url: source.url.replace(/\.json$/i, '.html'),
          content: `${word.word || ''} ${word.meaning || ''} ${word.pos || ''}`
        })) : [];
      }
      return [{ type: source.type, title: source.title, url: source.url, content: htmlText(await response.text()) }];
    } catch (error) {
      console.warn('Search source unavailable:', source.url, error);
      return [];
    }
  };

  const ensureIndex = () => {
    if (loading) return loading;
    loading = (async () => {
      const loaded = await mapWithConcurrency(documentSources, 8, readSource);
      index = loaded.flat().map((entry) => ({
        ...entry, titleText: normalize(entry.title), contentText: normalize(entry.content)
      }));
      status.textContent = `${index.length.toLocaleString('ko-KR')}개 검색 항목 준비 완료`;
    })();
    return loading;
  };

  const createSnippet = (entry, term) => {
    const position = entry.contentText.indexOf(term);
    if (position < 0) return plainText(entry.content).slice(0, 170);
    const original = plainText(entry.content);
    return `${position > 60 ? '…' : ''}${original.slice(Math.max(0, position - 60), position + 120)}${original.length > position + 120 ? '…' : ''}`;
  };

  const render = (query) => {
    const terms = normalize(query).split(' ').filter(Boolean);
    results.replaceChildren();
    if (!terms.length) { status.textContent = `${index.length.toLocaleString('ko-KR')}개 검색 항목 준비 완료`; return; }
    const matched = index.filter((entry) => (activeFilter === 'all' || entry.type === activeFilter) && terms.every((term) => `${entry.titleText} ${entry.contentText}`.includes(term)))
      .map((entry) => ({ entry, score: terms.reduce((score, term) => score + (entry.titleText.includes(term) ? 20 : 0) + (entry.contentText.includes(term) ? 1 : 0), 0) }))
      .sort((a, b) => b.score - a.score || a.entry.title.localeCompare(b.entry.title, 'ko'))
      .slice(0, 50);
    status.textContent = `${matched.length}${matched.length === 50 ? '+' : ''}개 결과`;
    for (const { entry } of matched) {
      const item = document.createElement('li');
      item.className = 'result';
      const link = document.createElement('a'); link.href = entry.url; link.textContent = entry.title;
      const label = document.createElement('span'); label.className = 'type'; label.textContent = typeLabel[entry.type];
      const snippet = document.createElement('p'); snippet.className = 'snippet'; snippet.textContent = createSnippet(entry, terms[0]);
      item.append(link, label, snippet); results.append(item);
    }
  };

  const search = async (query, updateUrl) => {
    status.textContent = '검색 인덱스를 준비하고 있습니다.';
    await ensureIndex();
    if (updateUrl) {
      const url = new URL(location.href); query ? url.searchParams.set('q', query) : url.searchParams.delete('q');
      history.replaceState({}, '', url);
    }
    render(query);
  };

  form.addEventListener('submit', (event) => { event.preventDefault(); search(input.value, true); });
  filters.forEach((filter) => filter.addEventListener('click', () => {
    activeFilter = filter.dataset.filter;
    filters.forEach((button) => { const active = button === filter; button.classList.toggle('is-active', active); button.setAttribute('aria-pressed', String(active)); });
    search(input.value, false);
  }));

  const initialQuery = new URLSearchParams(location.search).get('q') || '';
  input.value = initialQuery;
  search(initialQuery, false);
})();
