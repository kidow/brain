(function () {
  var KEY = 'brain:lastVisit';
  var RESTORE_KEY = 'brain:restoreScroll';
  var HOME_PATHS = ['/', '/index.html', '/README.html', '/README.ko.html'];
  var path = location.pathname;
  var isHome = HOME_PATHS.indexOf(path) !== -1;

  function read() {
    try { return JSON.parse(localStorage.getItem(KEY)); } catch (e) { return null; }
  }
  function save() {
    try { localStorage.setItem(KEY, JSON.stringify({ path: path, scrollY: window.scrollY })); } catch (e) {}
  }

  if (isHome) {
    var last = read();
    if (last && last.path && HOME_PATHS.indexOf(last.path) === -1) {
      if (window.confirm('마지막으로 보던 페이지로 이동할까요?\n' + last.path)) {
        try { sessionStorage.setItem(RESTORE_KEY, String(last.scrollY || 0)); } catch (e) {}
        location.href = last.path;
      }
    }
    return;
  }

  var restore = null;
  try { restore = sessionStorage.getItem(RESTORE_KEY); } catch (e) {}
  if (restore !== null) {
    try { sessionStorage.removeItem(RESTORE_KEY); } catch (e) {}
    window.addEventListener('load', function () {
      window.scrollTo(0, parseInt(restore, 10) || 0);
    });
  }

  var throttled = false;
  window.addEventListener('scroll', function () {
    if (throttled) return;
    throttled = true;
    setTimeout(function () {
      save();
      throttled = false;
    }, 300);
  });
  window.addEventListener('pagehide', save);
  save();
})();
