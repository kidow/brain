(() => {
  const { typeLabel, load, search: findEntries, snippet } = window.BrainSearch;
  const form = document.getElementById('search-form');
  const input = document.getElementById('search-input');
  const status = document.getElementById('search-status');
  const results = document.getElementById('search-results');
  const filters = [...document.querySelectorAll('.filter')];
  let activeFilter = 'all';
  let index = [];

  const readyText = () => `${index.length.toLocaleString('ko-KR')}개 검색 항목 준비 완료`;

  const render = (query) => {
    results.replaceChildren();
    if (!query.trim()) { status.textContent = readyText(); return; }
    const matched = findEntries(index, query, { filter: activeFilter, limit: 50 });
    status.textContent = `${matched.length}${matched.length === 50 ? '+' : ''}개 결과`;
    for (const entry of matched) {
      const item = document.createElement('li');
      item.className = 'result';
      const link = document.createElement('a'); link.href = entry.url; link.textContent = entry.title;
      const label = document.createElement('span'); label.className = 'type'; label.textContent = typeLabel[entry.type];
      const excerpt = document.createElement('p'); excerpt.className = 'snippet'; excerpt.textContent = snippet(entry, query);
      item.append(link, label, excerpt); results.append(item);
    }
  };

  const search = async (query, updateUrl) => {
    status.textContent = '검색 인덱스를 준비하고 있습니다.';
    try {
      index = await load();
    } catch (error) {
      console.warn('Search index unavailable:', error);
      status.textContent = '검색 인덱스를 불러오지 못했습니다.';
      return;
    }
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
