/* build-web.js — the pages that go inside the iPhone and Android app (#35), into app/www.
   The app is the website's own files (nothing rewritten by hand): every learner page, its scripts and styles, the
   pictures and all the audio, so lessons open and play with no connection. Two things the website loads from other
   sites are saved into the app instead: the Supabase library and the fonts. The landing page (index.html) and the
   owner's dashboard stay on the website; the app opens on Home (dashboard.html), which sends a signed-out learner
   to the sign-in page. Plans and Settings also get app-store.js: the stores' subscriptions instead of Stripe.
     node build-web.js          (then: npx cap sync) */
const fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, '..'), WWW = path.join(__dirname, 'www');
const SUPABASE = '2.119.0';                        // pinned: the website's @2 resolves to this today
const SKIP_PAGES = new Set(['index.html', 'admin.html']);
const SKIP_JS = new Set(['build-manifest.js', 'sw.js']);   // the website's offline helper: not used inside the app
const DIRS = ['audio', 'sounds', 'pics', 'icons'];
const FILES = ['site.css', 'manifest.json', 'audio-manifest.json', 'icon-192.png', 'icon-512.png', 'icon-maskable-512.png', 'badge-96.png',
               'apple-touch-icon.png', 'media/rafiq-how-it-works.mp4', 'media/rafiq-how-it-works.jpg', 'media/rafiq-how-it-works.en.vtt'];
const UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1';

const copy = (from, to) => { fs.mkdirSync(path.dirname(to), { recursive: true }); fs.copyFileSync(from, to); };
const copyDir = (d) => fs.cpSync(path.join(ROOT, d), path.join(WWW, d), { recursive: true });
async function get(url, bin) {
  const r = await fetch(url, { headers: { 'User-Agent': UA } });
  if (!r.ok) throw new Error(`${url}: ${r.status}`);
  return bin ? Buffer.from(await r.arrayBuffer()) : r.text();
}

(async () => {
  fs.rmSync(WWW, { recursive: true, force: true }); fs.mkdirSync(WWW);
  const pages = fs.readdirSync(ROOT).filter(f => f.endsWith('.html') && !SKIP_PAGES.has(f));
  fs.readdirSync(ROOT).filter(f => f.endsWith('.js') && !SKIP_JS.has(f)).forEach(f => copy(path.join(ROOT, f), path.join(WWW, f)));
  FILES.forEach(f => copy(path.join(ROOT, f), path.join(WWW, f)));
  DIRS.forEach(copyDir);

  // the Supabase library, saved into the app
  fs.mkdirSync(path.join(WWW, 'vendor/fonts'), { recursive: true });
  fs.writeFileSync(path.join(WWW, 'vendor/supabase.js'), await get(`https://cdn.jsdelivr.net/npm/@supabase/supabase-js@${SUPABASE}/dist/umd/supabase.js`));

  // the fonts: every Google Fonts sheet the pages ask for, with its font files saved alongside
  const sheets = new Map();                         // the page's href → the saved copy
  for (const f of pages) for (const m of fs.readFileSync(path.join(ROOT, f), 'utf8').matchAll(/href="(https:\/\/fonts\.googleapis\.com\/css2\?[^"]+)"/g)) sheets.set(m[1].replace(/&amp;/g, '&'), null);
  let n = 0, files = 0;
  for (const href of sheets.keys()) {
    let css = await get(href);
    for (const u of [...new Set(css.match(/https:\/\/fonts\.gstatic\.com\/[^)]+/g) || [])]) {
      const name = u.split('/').slice(-2).join('-');
      fs.writeFileSync(path.join(WWW, 'vendor/fonts', name), await get(u, true)); files++;
      css = css.split(u).join(`fonts/${name}`);
    }
    const out = `vendor/fonts-${++n}.css`;
    fs.writeFileSync(path.join(WWW, out), css); sheets.set(href, out);
  }

  // the pages, pointed at the saved copies
  for (const f of pages) {
    let h = fs.readFileSync(path.join(ROOT, f), 'utf8');
    h = h.replace(/https:\/\/cdn\.jsdelivr\.net\/npm\/@supabase\/supabase-js@2[^"]*/g, 'vendor/supabase.js');
    h = h.replace(/href="(https:\/\/fonts\.googleapis\.com\/css2\?[^"]+)"/g, (m, u) => `href="${sheets.get(u.replace(/&amp;/g, '&'))}"`);
    h = h.replace(/<link rel="preconnect" href="https:\/\/fonts\.(googleapis|gstatic)\.com"[^>]*>\n?/g, '');
    fs.writeFileSync(path.join(WWW, f), h);
  }
  // App Store / Google Play instead of Stripe (#352): app-store.js, only in the app's copies of Plans and Settings
  copy(path.join(__dirname, 'app-store.js'), path.join(WWW, 'app-store.js'));
  for (const f of ['plans.html', 'settings.html']) {
    const h = fs.readFileSync(path.join(WWW, f), 'utf8');
    if (!h.includes('</body>')) throw new Error(`${f}: no </body> to add app-store.js before`);
    fs.writeFileSync(path.join(WWW, f), h.replace('</body>', '<script src="app-store.js"></script>\n</body>'));
  }
  // the app opens on Home
  fs.writeFileSync(path.join(WWW, 'index.html'), '<!doctype html><meta charset="utf-8"><title>Rafiq</title><script>location.replace("dashboard.html")</script>\n');
  const size = d => fs.readdirSync(d, { withFileTypes: true }).reduce((a, e) => a + (e.isDirectory() ? size(path.join(d, e.name)) : fs.statSync(path.join(d, e.name)).size), 0);
  console.log(`www: ${pages.length} pages, ${sheets.size} font sheet(s) with ${files} font files, ${(size(WWW) / 1048576).toFixed(0)} MB`);
})().catch(e => { console.error(e); process.exit(1); });
