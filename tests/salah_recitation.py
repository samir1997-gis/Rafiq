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
STUB = """
(() => {
  let rp;
  Object.defineProperty(window, 'RafiqPlan', { configurable: true, get: () => rp, set: v => {
    rp = v;
    rp.call = async (fn, body) => {
      window.__asked = (window.__asked || []).concat(body.verses || []);
      if (fn !== 'quran') return { error: 'stub' };
      const verses = {};
      (body.verses || []).forEach(k => {
        // four words, 250 ms each, in QF's [position, start, end] form; 1:7 in quran-align's form
        verses[k] = { url: 'CLIP', segments: k === '1:7'
          ? [[0, 9, 0, 900]]
          : [[1, 0, 250], [2, 250, 500], [3, 500, 750], [4, 750, 1000], [5, 1000, 1250], [6, 1250, 1500]] };
      });
      return { verses, credit: 'Recitation: Quran Foundation (Quran.com)' };
    };
  }});
})();
""".replace("CLIP", CLIP)

def main():
    proxy = os.environ.get("HTTPS_PROXY")
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None,
                              args=["--autoplay-policy=no-user-gesture-required"] +
                                   (["--proxy-server=" + proxy, "--proxy-bypass-list=localhost,127.0.0.1"] if proxy else []))
        ctx = b.new_context(ignore_https_errors=bool(proxy))
        ctx.add_init_script(STUB)
        ctx.add_init_script("""(() => { const A = window.Audio; window.__played = [];
          window.Audio = function(src){ const a = new A(src); window.__played.push(src); return a; }; })();""")
        # no Supabase: the app then runs signed out without sending us to login (auth.js)
        ctx.route("**/@supabase/**", lambda r: r.abort())
        page = ctx.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(BASE + "learn.html?salah=prayalong&surah=ikhlas", wait_until="domcontentloaded")
        page.wait_for_timeout(1500)
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
        seen = set()
        for _ in range(30):                                    # watch the highlight move with the audio
            k = page.evaluate("[...document.querySelectorAll('.pw')].findIndex(w => w.classList.contains('on'))")
            seen.add(k)
            page.wait_for_timeout(50)
        ok.append(("played the recitation", any(CLIP in s for s in page.evaluate("window.__played"))))
        ok.append(("highlight moved across words", len({k for k in seen if k >= 0}) >= 3))
        ok.append(("no page errors", not errors))
        for name, good in ok:
            print(("ok   " if good else "FAIL ") + name)
        for e in errors:
            print("    " + e)
        b.close()
        sys.exit(0 if all(g for _, g in ok) else 1)

if __name__ == "__main__":
    main()
