(() => {
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'brain-copy-link';
  button.textContent = '링크 복사';
  button.setAttribute('aria-label', '현재 페이지 링크 복사');

  const style = document.createElement('style');
  style.textContent = '.brain-copy-link{position:fixed;z-index:1000;top:3.75rem;right:1rem;padding:.5rem .7rem;border:1px solid #60a5fa;border-radius:999px;background:#0f172a;color:#e2e8f0;font:600 14px/1 system-ui,sans-serif;cursor:pointer;box-shadow:0 2px 8px #0004}.brain-copy-link:hover,.brain-copy-link:focus{background:#1e293b;outline:2px solid #60a5fa;outline-offset:2px}';
  document.head.append(style);

  const copy = async () => {
    const url = location.href;
    try {
      await navigator.clipboard.writeText(url);
    } catch {
      const textarea = document.createElement('textarea');
      textarea.value = url;
      textarea.setAttribute('readonly', '');
      textarea.style.position = 'fixed';
      textarea.style.opacity = '0';
      document.body.append(textarea);
      textarea.select();
      document.execCommand('copy');
      textarea.remove();
    }
    button.textContent = '복사됨';
    setTimeout(() => { button.textContent = '링크 복사'; }, 1600);
  };

  button.addEventListener('click', copy);
  document.body.append(button);
})();
