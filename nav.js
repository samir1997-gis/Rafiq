/* nav.js — the same five places on every page: Home (your path), Practise
   (scenes, verbs, joining words, your words), Tutor (the AI tutor), Progress and Settings. Rewrites the page's
   own .navlinks (desktop) and .tabbar (phone) so they can't drift apart. */
(function(){
  const page = (location.pathname.split('/').pop() || 'dashboard.html').replace(/\?.*/, '');
  const TAB = {'dashboard.html':'home','learn.html':'home','session.html':'home',
               'practise.html':'practise','vocab.html':'practise','drills.html':'practise',
               'verbs.html':'practise','connectors.html':'practise','tutor.html':'tutor','progress.html':'progress','settings.html':'settings'};
  const on = TAB[page] || 'home';
  const ITEMS = [['home','dashboard.html','الرَّئِيسَة','Home'],
                 ['practise','practise.html','تَدْرِيب','Practise'],
                 ['tutor','tutor.html','مُعَلِّم','Tutor'],
                 ['progress','progress.html','التَّقَدُّم','Progress'],
                 ['settings','settings.html','إِعْدادات','Settings']]
                .filter(([k]) => k !== 'tutor' || (typeof TUTOR_ON !== 'undefined' && TUTOR_ON));   // auth.js
  function draw(){
    const links = document.querySelector('.navlinks');
    if(links) links.innerHTML = ITEMS.map(([k,h,,en]) => `<a href="${h}"${k===on?' class="active"':''}>${en}</a>`).join('') +
      '<a href="login.html" class="logout-link" onclick="logout();return false;">Log out</a>';
    const bar = document.querySelector('.tabbar');
    if(bar) bar.innerHTML = ITEMS.map(([k,h,ar,en]) => `<a href="${h}"${k===on?' class="on"':''}><span class="ti">${ar}</span>${en}</a>`).join('');
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', draw); else draw();
})();
