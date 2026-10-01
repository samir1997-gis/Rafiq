/* source.js — where someone first came from (#186), so the funnel can show which post or ad brings
   sign-ups. Kept once, on the first visit: a link's ?utm_source= (and utm_campaign), else the site
   that linked here, else "direct". auth.js saves it with a new account. No cookies; nothing is sent. */
(function(){
  try {
    if (localStorage.getItem('rafiq_src')) return;
    const q = new URLSearchParams(location.search);
    let src = (q.get('utm_source') || '').toLowerCase().slice(0, 40);
    if (!src && document.referrer) {
      const h = new URL(document.referrer).hostname.replace(/^(www|l|lm|m)\./, '');
      if (h !== location.hostname) src = h;
    }
    localStorage.setItem('rafiq_src', JSON.stringify({ src: src || 'direct',
      campaign: (q.get('utm_campaign') || '').slice(0, 60) || undefined, at: new Date().toISOString().slice(0, 10) }));
  } catch(_) {}
})();
