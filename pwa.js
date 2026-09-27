/* pwa.js — Rafiq as an installed app (issue #31). Loaded early in <head> on every page.

   - Registers the service worker (sw.js): offline pages and audio, and the
     daily reminder notifications.
   - Adds the home-screen tags every page needs (manifest, icon, iPhone splash
     screens), so pages don't each have to carry them.
   - The install card: Home calls RafiqPWA.card(el, {ready}) once the learner
     has finished a first lesson step; Settings gets a row. On Android and
     desktop Chrome/Edge it's an Install button (the browser's own prompt); on
     iPhone and iPad, which have no install prompt, "Show me how" opens a
     picture guide (RafiqPWA.guide()): Share, then Add to Home Screen, or
     "open this in Safari first" from an app's built-in browser. It's framed
     around the daily reminder: on iPhone, notifications only reach a
     home-screen app. Hidden once installed, or for 30 days after "Not now".
     Approach scored with TypeSafe: tools/typesafe-exp/install_prompt.py. */
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
  /* On iPhone, which browser is this? 'safari' | 'other' (Chrome, Firefox, Edge: since iOS 16.4
     their Share menu can add to the home screen too) | 'inapp' (Instagram, Facebook and similar
     built-in browsers, which can't: open in Safari first) */
  function iosBrowser(){
    const ua = navigator.userAgent;
    if(/FBAN|FBAV|Instagram|Line\/|MicroMessenger|Snapchat|TikTok|musical_ly|GSA\//.test(ua) || !/Safari\//.test(ua)) return 'inapp';
    if(/CriOS|FxiOS|EdgiOS|OPiOS/.test(ua)) return 'other';
    return 'safari';
  }
  async function install(){
    if(!prompt) return false;
    prompt.prompt();
    const { outcome } = await prompt.userChoice.catch(() => ({}));
    prompt = null; mounted.forEach(f => f());
    return outcome === 'accepted';
  }

  const css = document.createElement('style');
  css.textContent = `
    .pwa-card{background:var(--card);border:1px solid var(--rule);border-radius:12px;padding:14px 16px;margin:0 0 22px;display:flex;gap:14px;align-items:flex-start}
    .pwa-card .pwa-i{flex:0 0 auto;width:44px;height:44px;border-radius:10px;background:url(apple-touch-icon.png) center/cover}
    .pwa-card .pwa-t{font-weight:700;font-size:15.5px;color:var(--ink)}
    .pwa-card p{margin:4px 0 0;font-size:13.5px;line-height:1.5;color:var(--ink-soft)}
    .pwa-card .pwa-b{display:flex;gap:14px;align-items:center;margin-top:10px}
    .pwa-card .pwa-go{border:0;border-radius:10px;background:var(--verdigris);color:#fff;font:600 14px var(--la);padding:9px 18px;cursor:pointer}
    .pwa-card .pwa-no{border:0;background:none;color:var(--ink-soft);font:13px var(--la);text-decoration:underline;cursor:pointer;padding:0}
`;
  head.appendChild(css);

  /* ---------- the iPhone guide: pictures of each step, as a sheet ---------- */
  const gcss = document.createElement('style');
  gcss.textContent = `
    .pwa-scrim{position:fixed;inset:0;z-index:400;background:rgba(0,0,0,.4);opacity:0;transition:opacity .22s ease}
    .pwa-scrim.on{opacity:1}
    .pwa-sheet{position:fixed;left:0;right:0;bottom:0;z-index:401;max-width:520px;margin:0 auto;max-height:94vh;overflow:auto;background:var(--paper);
      border-radius:16px 16px 0 0;box-shadow:0 -10px 40px -12px rgba(0,0,0,.4);padding:10px 20px calc(20px + env(safe-area-inset-bottom));
      transform:translateY(100%);transition:transform .34s var(--ease-out,cubic-bezier(.16,1,.3,1))}
    .pwa-sheet.on{transform:none}
    .pwa-grab{width:40px;height:5px;border-radius:3px;background:var(--rule);margin:0 auto 12px}
    .pwa-sheet h2{font-size:21px;letter-spacing:-.01em;margin:0 0 4px}
    .pwa-sheet .pwa-lead{font-size:14.5px;color:var(--ink-soft);margin:0 0 16px;line-height:1.5}
    .pwa-step{display:flex;gap:12px;align-items:flex-start;margin:0 0 16px}
    .pwa-n{flex:0 0 26px;height:26px;border-radius:50%;background:var(--verdigris);color:var(--paper);font:700 13px/26px var(--la);text-align:center}
    .pwa-step p{margin:2px 0 8px;font-size:15px;line-height:1.45;color:var(--ink)}
    .pwa-step small{display:block;font-size:12.5px;color:var(--ink-soft);margin-top:2px}
    .pwa-pic{background:var(--card);border:1px solid var(--rule);border-radius:12px;padding:10px 12px;position:relative}
    .pwa-bar{display:flex;justify-content:space-around;align-items:center;height:34px;color:var(--ink-soft)}
    .pwa-bar svg{width:22px;height:22px}
    .pwa-bar .hl{color:var(--verdigris);position:relative}
    .pwa-bar .hl::after{content:'';position:absolute;inset:-7px;border:2px solid var(--verdigris);border-radius:10px}
    .pwa-arrow{position:absolute;left:50%;top:-30px;transform:translateX(-50%);color:var(--verdigris);font-size:22px;animation:pwaBob 1.1s ease-in-out infinite}
    @keyframes pwaBob{50%{transform:translate(-50%,5px)}}
    .pwa-menu div{display:flex;justify-content:space-between;align-items:center;padding:8px 2px;font-size:14px;color:var(--ink-soft);border-bottom:1px solid var(--rule)}
    .pwa-menu div:last-child{border:0}
    .pwa-menu .hl{color:var(--ink);font-weight:700;background:color-mix(in srgb,var(--verdigris) 12%,transparent);border-radius:8px;padding:8px 8px;border:0}
    .pwa-menu .hl span{font-size:17px;color:var(--verdigris)}
    .pwa-add{display:flex;justify-content:space-between;align-items:center;font-size:14px}
    .pwa-add b{color:var(--verdigris)}
    .pwa-warn{background:color-mix(in srgb,var(--gold) 14%,var(--card));border:1px solid var(--gold);border-radius:10px;padding:12px 14px;font-size:14px;line-height:1.5;margin:0 0 16px}
    .pwa-copy{margin-top:8px;border:1px solid var(--rule);background:var(--card);color:var(--ink);border-radius:8px;padding:8px 12px;font:600 13.5px var(--la);cursor:pointer}
    .pwa-sheet .pwa-done{width:100%;min-height:48px;border:0;border-radius:10px;background:var(--verdigris);color:#fff;font:600 15px var(--la);cursor:pointer}
    @media (prefers-reduced-motion:reduce){.pwa-sheet{transition:opacity .2s ease;transform:none;opacity:0}.pwa-sheet.on{opacity:1}.pwa-arrow{animation:none}}`;
  head.appendChild(gcss);
  const ICON = {
    back:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M15 5l-7 7 7 7"/></svg>',
    fwd:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M9 5l7 7-7 7"/></svg>',
    share:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12M8 7l4-4 4 4"/><path d="M7 10H5.5v10h13V10H17"/></svg>',
    book:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M4 5h6a2 2 0 0 1 2 2v12a2 2 0 0 0-2-2H4zM20 5h-6a2 2 0 0 0-2 2v12a2 2 0 0 1 2-2h6z"/></svg>',
    tabs:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><rect x="4" y="7" width="12" height="12" rx="2"/><path d="M8 4h10a2 2 0 0 1 2 2v10"/></svg>',
  };
  function guide(){
    if(document.querySelector('.pwa-sheet')) return;
    const b = iosBrowser();
    const scrim = document.createElement('div'); scrim.className = 'pwa-scrim';
    const sheet = document.createElement('div'); sheet.className = 'pwa-sheet';
    sheet.setAttribute('role','dialog'); sheet.setAttribute('aria-modal','true'); sheet.setAttribute('aria-labelledby','pwaTitle');
    const warn = b === 'inapp'
      ? `<div class="pwa-warn"><b>First, open Rafiq in Safari.</b> You're in another app's built-in browser, which can't add to the home screen. Look for <b>Open in Safari</b> (often under ••• or the compass icon), or copy the link and paste it into Safari.<br><button type="button" class="pwa-copy">Copy the link</button></div>`
      : b === 'other' ? `<div class="pwa-warn">This works in Chrome and other browsers on iPhone too: use their Share button. If you can't find <b>Add to Home Screen</b>, open Rafiq in Safari.</div>` : '';
    sheet.innerHTML = `<div class="pwa-grab" aria-hidden="true"></div>
      <h2 id="pwaTitle">Put Rafiq on your home screen</h2>
      <p class="pwa-lead">Three taps. Then Rafiq opens like an app, works offline, and can send your daily reminder.</p>${warn}
      <div class="pwa-step"><span class="pwa-n">1</span><div style="flex:1"><p>Tap the <b>Share</b> button.<small>At the bottom of Safari (at the top on iPad). On some iPhones it's inside the ••• menu.</small></p>
        <div class="pwa-pic" aria-hidden="true" style="margin-top:34px"><span class="pwa-arrow">↓</span><div class="pwa-bar">${ICON.back}${ICON.fwd}<span class="hl">${ICON.share}</span>${ICON.book}${ICON.tabs}</div></div></div></div>
      <div class="pwa-step"><span class="pwa-n">2</span><div style="flex:1"><p>Scroll down and tap <b>Add to Home Screen</b>.</p>
        <div class="pwa-pic pwa-menu" aria-hidden="true"><div>Copy</div><div>Add to Reading List</div><div class="hl">Add to Home Screen <span>⊞</span></div></div></div></div>
      <div class="pwa-step"><span class="pwa-n">3</span><div style="flex:1"><p>Tap <b>Add</b>, then open Rafiq from its new icon.</p>
        <div class="pwa-pic pwa-add" aria-hidden="true"><span>Cancel</span><span>Add to Home Screen</span><b>Add</b></div></div></div>
      <button type="button" class="pwa-done">Got it</button>`;
    document.body.append(scrim, sheet);
    const last = document.activeElement;
    const close = () => { scrim.classList.remove('on'); sheet.classList.remove('on'); document.removeEventListener('keydown', key);
      setTimeout(() => { scrim.remove(); sheet.remove(); if(last && last.focus) last.focus(); }, 300); };
    const key = e => { if(e.key === 'Escape') close(); };
    document.addEventListener('keydown', key);
    scrim.onclick = close; sheet.querySelector('.pwa-done').onclick = close;
    const copy = sheet.querySelector('.pwa-copy');
    if(copy) copy.onclick = async () => { try{ await navigator.clipboard.writeText(location.origin + '/login.html'); copy.textContent = 'Copied. Now paste it into Safari'; }catch(_){ copy.textContent = location.origin; } };
    requestAnimationFrame(() => { scrim.classList.add('on'); sheet.classList.add('on'); });
    setTimeout(() => sheet.querySelector('.pwa-done').focus({ preventScroll:true }), 360);
  }

  /* Home: a card inside el, kept up to date as the browser's prompt arrives or goes.
     opts.ready = false keeps it hidden (Home passes whether a first lesson step is done). */
  function card(el, opts = {}){
    if(!el) return;
    const paint = () => {
      const h = how();
      if(!h || later() || opts.ready === false){ el.innerHTML = ''; return; }
      el.innerHTML = `<div class="pwa-card"><span class="pwa-i" aria-hidden="true"></span><div>
        <div class="pwa-t">${h === 'ios' ? 'Get a daily reminder' : 'Keep Rafiq one tap away'}</div>
        <p>${h === 'ios' ? 'Put Rafiq on your home screen: it opens like an app, works offline, and on iPhone that’s how your daily reminder reaches you.'
          : 'Install Rafiq: it opens like an app, full screen, and works without a connection.'}</p>
        <div class="pwa-b"><button type="button" class="pwa-go">${h === 'ios' ? 'Show me how' : 'Install'}</button><button type="button" class="pwa-no">Not now</button></div></div></div>`;
      el.querySelector('.pwa-go').onclick = () => h === 'ios' ? guide() : install();
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
        ? 'Put Rafiq on your home screen. On iPhone, that’s how notifications reach you.' : 'Rafiq on your home screen: full screen, and it works offline.'}</div></div>
        ${h ? `<button type="button" class="btn small">${h === 'ios' ? 'Show me how' : 'Install'}</button>` : ''}`;
      const b = row.querySelector('button'); if(b) b.onclick = () => h === 'ios' ? guide() : install();
    };
    mounted.push(paint); paint();
  }
  document.addEventListener('DOMContentLoaded', () => { if(/settings\.html$/.test(location.pathname)) settingsRow(); });

  window.RafiqPWA = { standalone, ios, iosBrowser, how, install, card, guide };
})();
