// 검색 페이지(search.js)와 전역 검색(cmdk.js)이 같이 쓰는 인덱스. 처음 load()가 불릴 때만 문서를 받아온다.
window.BrainSearch = window.BrainSearch || (() => {
  const CACHE_KEY = 'brain-search-index';
  const typeLabel = { note: '노트', sheet: '치트시트', drill: '드릴', vocab: '단어장' };
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
      if (source.type === 'vocab-data') {
        // 단어장은 개념 하나가 검색 단위다 — 8개 언어의 단어를 한 항목으로 묶고 해시로 바로 연결한다.
        const book = await response.json();
        const page = source.url.replace(/\.json$/i, '.html');
        return (book.concepts || []).map((concept) => {
          const words = Object.entries(concept.words || {}).flatMap(([, entry]) =>
            [entry, ...(entry.alt || [])].map((one) => `${one.word || ''} ${one.rom || ''} ${one.kor || ''} ${one.label || ''}`));
          return {
            type: 'vocab',
            title: `${book.category} · ${concept.ko}`,
            url: `${page}#${concept.id}`,
            content: `${concept.ko} ${concept.id} ${words.join(' ')} ${(concept.notes || []).join(' ')}`
          };
        });
      }
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

  // sessionStorage 캐시: 같은 탭에서 페이지를 옮겨도 다시 받지 않는다. 빌드 시각(version)이 바뀌면 버린다.
  // localStorage는 드릴 진행 상태와 용량을 나눠 쓰므로 일부러 피한다.
  const readCache = (version) => {
    try {
      const cached = JSON.parse(sessionStorage.getItem(CACHE_KEY));
      return cached && cached.version === version ? cached.entries : null;
    } catch { return null; }
  };
  const writeCache = (version, entries) => {
    try { sessionStorage.setItem(CACHE_KEY, JSON.stringify({ version, entries })); } catch { /* 용량 초과 — 캐시 없이 동작 */ }
  };

  let loading;
  const load = () => {
    loading = loading || (async () => {
      const response = await fetch('/search-sources.json');
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const { version, sources } = await response.json();
      let entries = readCache(version);
      if (!entries) {
        entries = (await mapWithConcurrency(sources, 8, readSource)).flat();
        writeCache(version, entries);
      }
      return entries.map((entry) => {
        const titleText = normalize(entry.title);
        const contentText = normalize(entry.content);
        return { ...entry, titleText, contentText, haystack: `${titleText} ${contentText}` };
      });
    })().catch((error) => { loading = null; throw error; });
    return loading;
  };

  const terms = (query) => normalize(query).split(' ').filter(Boolean);

  const search = (index, query, { filter = 'all', limit = 50 } = {}) => {
    const queryTerms = terms(query);
    if (!queryTerms.length) return [];
    return index.filter((entry) => (filter === 'all' || entry.type === filter) && queryTerms.every((term) => entry.haystack.includes(term)))
      .map((entry) => ({ entry, score: queryTerms.reduce((score, term) => score + (entry.titleText.includes(term) ? 20 : 0) + (entry.contentText.includes(term) ? 1 : 0), 0) }))
      .sort((a, b) => b.score - a.score || a.entry.title.localeCompare(b.entry.title, 'ko'))
      .slice(0, limit)
      .map(({ entry }) => entry);
  };

  const snippet = (entry, query, radius = 60) => {
    const [term] = terms(query);
    const original = plainText(entry.content);
    const position = term ? entry.contentText.indexOf(term) : -1;
    if (position < 0) return original.slice(0, radius * 3);
    return `${position > radius ? '…' : ''}${original.slice(Math.max(0, position - radius), position + radius * 2)}${original.length > position + radius * 2 ? '…' : ''}`;
  };

  return { typeLabel, load, search, snippet };
})();
