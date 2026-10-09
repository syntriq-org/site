const header = document.querySelector('#header');
const updateHeader = () => header.classList.toggle('compact', window.scrollY > 35);
window.addEventListener('scroll', updateHeader, { passive: true });
updateHeader();
const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('#navigation');
function closeMenu() { toggle.setAttribute('aria-expanded', 'false'); nav.classList.remove('open'); }
toggle.addEventListener('click', () => { const open = toggle.getAttribute('aria-expanded') !== 'true'; toggle.setAttribute('aria-expanded', String(open)); nav.classList.toggle('open', open); });
nav.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
document.addEventListener('keydown', event => { if (event.key === 'Escape' && nav.classList.contains('open')) { closeMenu(); toggle.focus(); } });
if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const observer = new IntersectionObserver(entries => { entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('visible'); observer.unobserve(entry.target); } }); }, { threshold: 0.08 });
  document.querySelectorAll('.reveal').forEach(element => observer.observe(element));
  document.documentElement.classList.add('motion');
}
const views = {
  data: '<div class="model-row"><div class="entity"><h4><span>◇</span> Customer</h4><p>id <span>ID</span><br>name <span>String</span><br>agreements <span>[Agreement]</span></p></div><div class="connector"></div><div class="entity"><h4><span>◇</span> Agreement</h4><p>id <span>ID</span><br>status <span>String</span><br>customer <span>Customer</span></p></div></div><div class="model-caption">BUSINESS ENTITIES. MEANINGFUL RELATIONSHIPS.</div>',
  process: '<div class="process-stack"><span>Customer created</span><i></i><span>Review agreement</span><i></i><span>Activate customer</span></div><div class="model-caption">AN EXPLICIT PATH FROM EVENT TO ACTION.</div>',
  query: '<pre><span class="token">query</span> {\n  customers {\n    id\n    name\n    agreements {\n      id\n      status\n    }\n  }\n}</pre>'
};
const tabs = [...document.querySelectorAll('[role="tab"]')];
function selectTab(tab) { tabs.forEach(item => { item.setAttribute('aria-selected', String(item === tab)); item.tabIndex = item === tab ? 0 : -1; }); const panel = document.querySelector('#demo-panel'); panel.innerHTML = views[tab.dataset.view]; panel.setAttribute('aria-labelledby', tab.id); }
tabs.forEach((tab, index) => { tab.addEventListener('click', () => selectTab(tab)); tab.addEventListener('keydown', event => { let next; if(event.key === 'ArrowRight') next = (index + 1) % tabs.length; if(event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length; if(event.key === 'Home') next = 0; if(event.key === 'End') next = tabs.length - 1; if(next !== undefined) { event.preventDefault(); tabs[next].focus(); selectTab(tabs[next]); } }); });
selectTab(tabs[0]);
document.querySelector('#year').textContent = new Date().getFullYear();
