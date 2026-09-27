/* pwa.js — Rafiq as an installed app (issue #31). Loaded early in <head> on every page.

   - Registers the service worker (sw.js): offline pages and audio, and the
     daily reminder notifications.
   - Adds the home-screen tags every page needs (manifest, icon, iPhone splash
     screens), so pages don't each have to carry them.
   - The install card: Home calls RafiqPWA.card(el); Settings gets a row. On
     Android and desktop Chrome/Edge it's an Install button (the browser's own
     prompt); on iPhone and iPad, which have no install prompt, it shows how:
     Share, then Add to Home Screen. Hidden once installed, or for 30 days
     after "Not now". */
(function(){
  const head = document.head;
  const add = (tag, attrs) => { const el = document.createElement(tag); Object.assign(el, attrs); head.appendChild(el); return el; };

  /* ---------- tags ---------- */
  if(!head.querySelector('link[rel="manifest"]')) add('link', { rel: 'manifest', href: 'manifest.json' });
  const touch = head.querySelector('link[rel="apple-touch-icon"]');
  if(touch) touch.href = 'apple-touch-icon.png'; else add('link', { rel: 'apple-touch-icon', href: 'apple-touch-icon.png' });
  const meta = (name, content) => { if(!head.querySelector(`meta[name="${name}"]`)) add('meta', { name, content }); };
  meta('apple-mobile-web-app-capable', 'yes');
  meta('mobile-web-app-capable', 'yes');
  meta('apple-mobile-web-app-title', 'رَفِيق');       // the label under the icon, as in manifest.json
  meta('apple-mobile-web-app-status-bar-style', 'default');
  // iPhone and iPad splash screens (icons/splash/, made from icon-512.png): [css width, css height, pixel ratio]
  [[440,956,3],[402,874,3],[430,932,3],[393,852,3],[428,926,3],[390,844,3],[375,812,3],[414,896,3],[414,896,2],[414,736,3],
   [375,667,2],[320,568,2],[820,1180,2],[1024,1366,2]].forEach(([w, h, r]) => ['light', 'dark'].forEach(mode => add('link', {
    rel: 'apple-touch-startup-image', href: `icons/splash/${w * r}x${h * r}-${mode}.png`,
    media: `(device-width: ${w}px) and (device-height: ${h}px) and (-webkit-device-pixel-ratio: ${r}) and (orientation: portrait) and (prefers-color-scheme: ${mode})` })));

  /* ---------- service worker ---------- */
  if('serviceWorker' in navigator && (location.protocol === 'https:' || location.hostname === 'localhost'))
    addEventListener('load', () => navigator.serviceWorker && navigator.serviceWorker.register('sw.js').catch(() => {}));

  /* ---------- installing ---------- */
  let prompt = null;
  const standalone = () => matchMedia('(display-mode: standalone)').matches || navigator.standalone === true;
  const ios = () => /iphone|ipad|ipod/i.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  const DISMISS = 'rafiq_install_later';
  const later = () => { try{ return Date.now() - (+localStorage.getItem(DISMISS) || 0) < 30 * 864e5; }catch(_){ return false; } };
  const mounted = [];
  addEventListener('beforeinstallprompt', e => { e.preventDefault(); prompt = e; mounted.forEach(f => f()); });
  addEventListener('appinstalled', () => { prompt = null; mounted.forEach(f => f()); });

  // 'prompt' (a button works) | 'ios' (show the steps) | null (installed, or this browser can't)
  const how = () => standalone() ? null : prompt ? 'prompt' : ios() ? 'ios' : null;
  async function install(){
    if(!prompt) return false;
    prompt.prompt();
    const { outcome } = await prompt.userChoice.catch(() => ({}));
    prompt = null; mounted.forEach(f => f());
    return outcome === 'accepted';
  }

  const SHARE = '<svg class="pwa-share" viewBox="0 0 24 24" aria-label="Share" role="img"><path d="M12 3v12M8 7l4-4 4 4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M7 10H5.5v10h13V10H17" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>';
  const css = document.createElement('style');
  css.textContent = `
    .pwa-card{background:var(--card);border:1px solid var(--rule);border-radius:12px;padding:14px 16px;margin:0 0 22px;display:flex;gap:14px;align-items:flex-start}
    .pwa-card .pwa-i{flex:0 0 auto;width:44px;height:44px;border-radius:10px;background:url(apple-touch-icon.png) center/cover}
    .pwa-card .pwa-t{font-weight:700;font-size:15.5px;color:var(--ink)}
    .pwa-card p{margin:4px 0 0;font-size:13.5px;line-height:1.5;color:var(--ink-soft)}
    .pwa-card .pwa-b{display:flex;gap:14px;align-items:center;margin-top:10px}
    .pwa-card .pwa-go{border:0;border-radius:10px;background:var(--verdigris);color:#fff;font:600 14px var(--la);padding:9px 18px;cursor:pointer}
    .pwa-card .pwa-no{border:0;background:none;color:var(--ink-soft);font:13px var(--la);text-decoration:underline;cursor:pointer;padding:0}
    .pwa-share{width:18px;height:18px;vertical-align:-3px;color:var(--verdigris)}`;
  head.appendChild(css);

  /* Home: a card inside el, kept up to date as the browser's prompt arrives or goes. */
  function card(el){
    if(!el) return;
    const paint = () => {
      const h = how();
      if(!h || later()){ el.innerHTML = ''; return; }
      el.innerHTML = `<div class="pwa-card"><span class="pwa-i" aria-hidden="true"></span><div>
        <div class="pwa-t">Put Rafiq on your home screen</div>
        <p>It opens like an app, full screen, and works without a connection.</p>
        ${h === 'ios' ? `<p>Tap ${SHARE} Share in the toolbar, then <b>Add to Home Screen</b>.</p>` : ''}
        <div class="pwa-b">${h === 'prompt' ? '<button type="button" class="pwa-go">Install</button>' : ''}<button type="button" class="pwa-no">Not now</button></div></div></div>`;
      const go = el.querySelector('.pwa-go'); if(go) go.onclick = () => install();
      el.querySelector('.pwa-no').onclick = () => { try{ localStorage.setItem(DISMISS, String(Date.now())); }catch(_){} paint(); };
    };
    mounted.push(paint); paint();
  }

  /* Settings → More: always there until installed ("Not now" on Home doesn't hide it). */
  function settingsRow(){
    const more = [...document.querySelectorAll('.group')].find(g => (g.querySelector('.glabel') || {}).textContent === 'More');
    if(!more) return;
    const row = document.createElement('div');
    row.className = 'row';
    more.appendChild(row);
    const paint = () => {
      const h = how();
      row.hidden = !h; row.style.display = h ? '' : 'none';
      row.innerHTML = `<div class="rl"><div class="rt">Install the app</div><div class="rs">${h === 'ios'
        ? `Tap ${SHARE} Share in Safari's toolbar, then Add to Home Screen.` : 'Rafiq on your home screen: full screen, and it works offline.'}</div></div>
        ${h === 'prompt' ? '<button type="button" class="btn small">Install</button>' : ''}`;
      const b = row.querySelector('button'); if(b) b.onclick = () => install();
    };
    mounted.push(paint); paint();
  }
  document.addEventListener('DOMContentLoaded', () => { if(/settings\.html$/.test(location.pathname)) settingsRow(); });

  window.RafiqPWA = { standalone, ios, how, install, card };
})();
