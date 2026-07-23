(() => {
  const link = document.createElement('a');
  link.href = '/search/';
  link.className = 'brain-search-link';
  link.setAttribute('aria-label', '문서 검색');
  link.textContent = '⌕ 검색';

  const style = document.createElement('style');
  style.textContent = '.brain-search-link{position:fixed;z-index:1000;top:1rem;right:1rem;padding:.5rem .7rem;border:1px solid #60a5fa;border-radius:999px;background:#0f172a;color:#e2e8f0;font:600 14px/1 system-ui,sans-serif;text-decoration:none;box-shadow:0 2px 8px #0004}.brain-search-link:hover,.brain-search-link:focus{background:#1e293b;outline:2px solid #60a5fa;outline-offset:2px}';
  document.head.append(style);
  document.body.append(link);
})();
