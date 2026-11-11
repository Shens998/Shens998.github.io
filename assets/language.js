'use strict';
// Language is encoded in the URL. No cookies or browser storage are needed.
function syncLanguageLinks() {
  document.querySelectorAll('.language-switch a').forEach(link => { link.hash = window.location.hash; });
}
syncLanguageLinks();
window.addEventListener('hashchange', syncLanguageLinks);
