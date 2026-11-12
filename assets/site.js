'use strict';
const menu = document.querySelector('.menu-toggle'), nav = document.querySelector('#nav');
menu?.addEventListener('click', () => { const open = menu.getAttribute('aria-expanded') !== 'true'; menu.setAttribute('aria-expanded', String(open)); nav.classList.toggle('is-open', open); });
nav?.querySelectorAll('a').forEach(a => a.addEventListener('click', () => { menu.setAttribute('aria-expanded', 'false'); nav.classList.remove('is-open'); }));
const isEnglish = document.documentElement.lang === 'en';
const publications = [...document.querySelectorAll('.publication')];
const search = document.querySelector('#paper-search'), year = document.querySelector('#paper-year');
const more = document.querySelector('#show-more'), count = document.querySelector('#result-count');
let topic = 'all', limit = 6;
[...new Set(publications.map(p => p.dataset.year))].sort((a,b) => Number(b)-Number(a)).forEach(y => { const option = document.createElement('option'); option.value = y; option.textContent = y; year.append(option); });
function update() {
  const term = search.value.trim().toLocaleLowerCase();
  const matches = publications.filter(p => (topic === 'all' || p.dataset.group === topic) && (year.value === 'all' || p.dataset.year === year.value) && p.textContent.toLocaleLowerCase().includes(term));
  const shown = new Set(matches.slice(0, limit));
  publications.forEach(p => { p.hidden = !shown.has(p); });
  count.textContent = isEnglish ? `${matches.length} publications` : `${matches.length} 篇论文`;
  document.querySelector('#empty-state').hidden = matches.length !== 0;
  more.hidden = matches.length <= limit;
  more.textContent = isEnglish ? `Show more (${Math.max(0,matches.length-limit)} remaining) ↓` : `展开更多论文（还有 ${Math.max(0,matches.length-limit)} 篇） ↓`;
  document.querySelectorAll('[data-filter]').forEach(b => { const active = b.dataset.filter === topic; b.classList.toggle('active', active); b.setAttribute('aria-pressed', String(active)); });
}
document.querySelector('.pub-controls').hidden = false;
document.querySelectorAll('[data-filter]').forEach(b => b.addEventListener('click', () => { topic = b.dataset.filter; limit = 6; update(); }));
document.querySelectorAll('[data-topic]').forEach(a => a.addEventListener('click', () => { topic = a.dataset.topic; search.value = ''; year.value = 'all'; limit = 6; update(); }));
search.addEventListener('input', () => { limit = 6; update(); }); year.addEventListener('change', () => { limit = 6; update(); });
more.addEventListener('click', () => { limit += 12; update(); }); update();
const dialog = document.querySelector('#privacy-dialog');
document.querySelector('#privacy-button').addEventListener('click', () => dialog.showModal());
document.querySelector('#privacy-close').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', e => { if (e.target === dialog) { const r=dialog.getBoundingClientRect(); if (e.clientX<r.left || e.clientX>r.right || e.clientY<r.top || e.clientY>r.bottom) dialog.close(); } });
document.querySelector('#copyright-year').textContent = new Date().getFullYear();
if ('IntersectionObserver' in window) {
 const observer = new IntersectionObserver(entries => { entries.forEach(entry => { if (entry.isIntersecting) { nav.querySelectorAll('a').forEach(a => { if (a.hash === '#'+entry.target.id) a.setAttribute('aria-current','location'); else a.removeAttribute('aria-current'); }); } }); }, {rootMargin:'-15% 0px -65% 0px'});
 document.querySelectorAll('main section[id]').forEach(s => observer.observe(s));
}
