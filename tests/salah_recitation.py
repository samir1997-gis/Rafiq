"""Salah recitation check (#135/#140): with the quran function answering (stubbed
here, since the real one needs Quran Foundation keys), Pray along plays the
recitation for Al-Fatiha and lights each word from its word timings.

  python3 .claude/skills/webapp-testing/scripts/with_server.py \
    --server "python3 -m http.server 8765 >/dev/null 2>&1" --port 8765 -- python3 tests/salah_recitation.py
"""
import os, sys, glob
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8765/"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
CLIP = max(glob.glob("audio/*.mp3"), key=os.path.getsize)          # any real mp3 stands in for the reciter
import json as _json
try:
    REAL = _json.load(open("/tmp/claude-0/health.json"))["verses"]      # live QF answer, if captured
except Exception:
    REAL = {}
STUB = """
(() => {
  let rp;
  Object.defineProperty(window, 'RafiqPlan', { configurable: true, get: () => rp, set: v => {
    rp = v;
    rp.call = async (fn, body) => {
      window.__asked = (window.__asked || []).concat(body.verses || []);
      if (fn !== 'quran') return { error: 'stub' };
      const verses = {};
      const REAL = __REAL__;
      (body.verses || []).forEach(k => {
        if (REAL[k] && REAL[k].url) { verses[k] = REAL[k]; return; }
        // four words, 250 ms each, in QF's [position, start, end] form; 1:7 in quran-align's form
        verses[k] = { url: 'CLIP', segments: k === '1:7'
          ? [[0, 9, 0, 900]]
          : [[1, 0, 250], [2, 250, 500], [3, 500, 750], [4, 750, 1000], [5, 1000, 1250], [6, 1250, 1500]] };
      });
      return { verses, credit: 'Recitation: Quran Foundation (Quran.com)' };
    };
  }});
})();
""".replace("CLIP", CLIP).replace("__REAL__", _json.dumps({k: v for k, v in REAL.items() if k.startswith("1:")}))


def sync_errors(page, seconds=6):
    """Sample the page: the lit word must be the one being said at that moment
    (a word's own timing, or the last one said in a gap), give or take 120 ms."""
    bad, n = [], 0
    for _ in range(int(seconds / 0.05)):
        v = page.evaluate("""(() => {
          const a = window.__audios && window.__audios[window.__audios.length - 1];
          const ws = [...document.querySelectorAll('.pw, #f span')]; if (!a || a.paused || !ws.length) return null;
          const txt = ws.map(w => (w.querySelector('b') || w).textContent).join(' ');
          const S = window.RafiqSalah, parts = S.parts ? S.parts() : [];
          let line = null; parts.forEach(p => p.lines.forEach(l => { if (l.words.map(w => w.ar).join(' ') === txt) line = l; }));
          const t = line && S.timings(line); if (!t) return null;
          return { ms: a.currentTime * 1000, lit: ws.findIndex(w => w.classList.contains('on')), t };
        })()""")
        page.wait_for_timeout(50)
        if not v: continue
        n += 1
        ms, lit, t = v["ms"], v["lit"], v["t"]
        said = max([i for i, (s0, e0) in enumerate(t) if s0 <= ms] or [0])
        near = any(abs(ms - x) < 120 for se in t for x in se)
        if lit != said and not near: bad.append((round(ms), lit, said))
    return n, bad

def main():
    proxy = os.environ.get("HTTPS_PROXY")
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None,
                              args=["--autoplay-policy=no-user-gesture-required"] +
                                   (["--proxy-server=" + proxy, "--proxy-bypass-list=localhost,127.0.0.1"] if proxy else []))
        ctx = b.new_context(ignore_https_errors=bool(proxy))
        ctx.add_init_script(STUB)
        ctx.add_init_script("""(() => { const A = window.Audio; window.__played = [];
          window.__audios = [];
          window.Audio = function(src){ const a = new A(src); window.__played.push(src); window.__audios.push(a); return a; }; })();""")
        # no Supabase: the app then runs signed out without sending us to login (auth.js)
        ctx.route("**/@supabase/**", lambda r: r.abort())
        page = ctx.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(BASE + "learn.html?salah=prayalong&surah=ikhlas", wait_until="domcontentloaded")
        page.wait_for_timeout(1500)
        # the opening supplication (10 words, the app's voice): lit word = word being said
        page.evaluate("(() => { const b = [...document.querySelectorAll('button')].find(b => b.textContent.trim() === 'Next'); if (b) b.click(); })()")
        page.wait_for_timeout(200)
        n_pr, bad_pr = sync_errors(page, 6)
        for _ in range(40):                                    # step through to Al-Fatiha
            if "al-fatiha" in page.inner_text("body").lower():
                break
            page.evaluate("(() => { const b = [...document.querySelectorAll('button')].find(b => b.textContent.trim() === 'Next'); if (b) b.click(); })()")
            page.wait_for_timeout(200)
        text = page.inner_text("body")
        if "al-fatiha" not in text.lower():
            print(text[:600])
        ok = []
        ok.append(("reached Al-Fatiha", "al-fatiha" in text.lower()))
        ok.append(("asked for the Quran verses once", "1:1" in page.evaluate("window.__asked || []")))
        ok.append(("shows the QF credit", "Quran Foundation" in text))
        ok.append(("says listen, not read-only", "Listen and read along" in text))
        page.wait_for_timeout(300)
        n_q, bad_q = sync_errors(page, 5)                      # Al-Fatiha 1:1, the real recitation
        played = page.evaluate("window.__played")
        ok.append(("played the recitation", any("quran.foundation" in s or CLIP in s for s in played)))
        ok.append(("prayer phrase: lit word is the word being said (%d samples, %d wrong %s)" % (n_pr, len(bad_pr), bad_pr[:3]), n_pr > 20 and not bad_pr))
        ok.append(("Quran: lit word is the word being recited (%d samples, %d wrong %s)" % (n_q, len(bad_q), bad_q[:3]), n_q > 20 and not bad_q))
        ok.append(("no page errors", not errors))
        for name, good in ok:
            print(("ok   " if good else "FAIL ") + name)
        for e in errors:
            print("    " + e)
        b.close()
        sys.exit(0 if all(g for _, g in ok) else 1)

if __name__ == "__main__":
    main()
