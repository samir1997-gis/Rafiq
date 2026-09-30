/* sw.js — the service worker (issue #31): lets the installed app open and work
   offline, and shows the daily reminder notifications.

   - Pages, scripts and styles: from the network first, so every change to the
     site shows up straight away; the cached copy is used when there's no
     connection (or the network takes more than 4 seconds).
   - Audio clips never change (their names are content hashes): from the cache
     first, saved the first time each one plays.
   - Fonts and the Supabase library (other sites): the cached copy at once,
     refreshed in the background.
   - Nothing else is touched: sign-in, progress and answer checking always go
     to the network.
   Bump VERSION when the list below changes. */
const VERSION = 'rafiq-2026-09-30-goal';
const SHELL = VERSION + '-shell', RUNTIME = 'rafiq-runtime', AUDIO = 'rafiq-audio';
const PAGES = ['dashboard.html', 'login.html', 'onboarding.html', 'learn.html', 'session.html', 'practise.html', 'tutor.html', 'progress.html',
  'settings.html', 'vocab.html', 'drills.html', 'verbs.html', 'connectors.html', 'index.html', 'reset-password.html',
  'plans.html', 'help.html', 'privacy.html', 'salah.html'];
const FILES = ['site.css', 'theme.js', 'pwa.js', 'auth.js', 'nav.js', 'plan.js', 'fsrs.js', 'progress.js', 'path.js', 'basics-data.js', 'path-data.js', 'audio.js',
  'sounds.js', 'judge.js', 'mistakes.js', 'arkb.js', 'tiles.js', 'spelling.js', 'translations.js', 'reminders.js',
  'alphabet-data.js', 'vocab-data.js', 'drills-data.js', 'toolkit-data.js', 'scenes-data.js', 'essentials.js', 'essentials-data.js',
  'item-tags.js', 'report.js', 'tutor.js', 'teach.js', 'salah.js', 'salah-data.js', 'salah-timings.js', 'manifest.json', 'icon-192.png', 'icon-512.png', 'apple-touch-icon.png', 'badge-96.png',
  'sounds/correct.mp3', 'sounds/wrong.mp3'];
const REMOTE = ['https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2',
  'https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Karla:wght@400;500;700&family=JetBrains+Mono:wght@400;600&display=swap'];

self.addEventListener('install', e => {
  e.waitUntil((async () => {
    const c = await caches.open(SHELL);
    // one missing file mustn't stop the rest being saved
    await Promise.all([...PAGES, ...FILES].map(u => c.add(new Request(u, { cache: 'reload' })).catch(() => {})));
    const r = await caches.open(RUNTIME);
    await Promise.all(REMOTE.map(u => r.add(u).catch(() => {})));
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    for (const k of await caches.keys()) if (![SHELL, RUNTIME, AUDIO].includes(k)) await caches.delete(k);
    await self.clients.claim();
  })());
});

const REMOTE_HOSTS = ['fonts.googleapis.com', 'fonts.gstatic.com', 'cdn.jsdelivr.net'];

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  const scope = self.registration.scope;                    // the site's folder: '/' on rafiq-arabic.com, deeper on a preview host
  if (url.href.startsWith(scope)) {
    const rel = url.pathname.slice(new URL(scope).pathname.length);
    if (/^(audio|sounds)\/[^/]+\.mp3$/.test(rel)) return e.respondWith(cacheFirst(req, AUDIO));
    if (rel.startsWith('media/')) return;                     // videos stream with range requests: leave them alone
    return e.respondWith(networkFirst(req, e));
  }
  if (REMOTE_HOSTS.includes(url.hostname)) e.respondWith(staleWhileRevalidate(req, e));
});

async function cacheFirst(req, name) {
  const hit = await caches.match(req);
  if (hit) return hit;
  const res = await fetch(req);
  if (res.ok) (await caches.open(name)).put(req, res.clone());
  return res;
}

async function networkFirst(req, e) {
  const net = fetch(req).then(async res => {
    // saved without its query (?v=…, ?t=…): one copy per file, the newest
    if (res.ok && res.type === 'basic') { const c = await caches.open(RUNTIME); await c.put(stripped(req), res.clone()); }
    return res;
  });
  e.waitUntil(net.catch(() => {}));
  const slow = new Promise(r => setTimeout(r, 4000, 'slow'));
  try {
    const res = await Promise.race([net, slow]);
    if (res !== 'slow') return res;
    return (await cached(req)) || await net;
  } catch (_) {
    const hit = await cached(req);
    if (hit) return hit;
    if (req.mode === 'navigate') return (await caches.match('dashboard.html', { ignoreSearch: true })) || Response.error();
    return Response.error();
  }
}
const stripped = req => { const u = new URL(req.url); return u.origin + u.pathname; };
// the newest copy of this file, whatever its ?v= (the pages load scripts as auth.js?v=6 and so on)
const cached = async req => (await (await caches.open(RUNTIME)).match(stripped(req))) || caches.match(req, { ignoreSearch: true });

async function staleWhileRevalidate(req, e) {
  const hit = await caches.match(req);
  const net = fetch(req).then(async res => {
    if (res.ok || res.type === 'opaque') { const c = await caches.open(RUNTIME); await c.put(req, res.clone()); }
    return res;
  });
  e.waitUntil(net.catch(() => {}));
  return hit || net;
}

/* ---------- the daily reminder (sent by tools/send-reminders.js) ---------- */
self.addEventListener('push', e => {
  let d = {};
  try { d = e.data ? e.data.json() : {}; } catch (_) { d = { body: e.data && e.data.text() }; }
  e.waitUntil(self.registration.showNotification(d.title || 'Rafiq', {
    body: d.body || 'A few minutes of Arabic today.',
    icon: 'icon-192.png', badge: 'badge-96.png', tag: 'daily-reminder', renotify: true,
    data: { url: d.url || 'dashboard.html' } }));
});

self.addEventListener('notificationclick', e => {
  e.notification.close();
  const url = new URL((e.notification.data && e.notification.data.url) || 'dashboard.html', self.registration.scope).href;   // relative to the site
  e.waitUntil((async () => {
    const open = await self.clients.matchAll({ type: 'window', includeUncontrolled: true });
    const tab = open.find(c => c.url.startsWith(self.registration.scope));
    if (tab) { await tab.focus(); return tab.navigate(url).catch(() => {}); }
    return self.clients.openWindow(url);
  })());
});
