#!/usr/bin/env python3
"""Records the app working, live, for the videos (#155): drives the real pages in Chromium at phone size
and saves a sharp frame at every moment (with its real timing), plus every sound the app plays.
Each clip becomes clips/<name>.mp4 (30 fps) and clips/<name>.json ({"sounds": [[seconds, "audio/x.mp3"], ...]}).

Needs the site served on :8765:
  python3 .claude/skills/webapp-testing/scripts/with_server.py --server "python3 -m http.server 8765 >/dev/null 2>&1" \
    --port 8765 -- python3 brag-output-v9-12/capture.py [clip ...]
"""
import base64, json, os, subprocess, sys, time, datetime
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tests"))
from tutor import FAKE_SUPABASE, CHROME                                       # a signed-in stand-in for Supabase
B = "http://localhost:8765/"
OUT = os.path.join(HERE, "clips"); os.makedirs(OUT, exist_ok=True)
FONTS = next((open(p).read() for p in ["/tmp/claude-0/localfonts.css"] if os.path.exists(p)), None)
TODAY = datetime.date.today().isoformat()

# every sound the app plays (its one shared <audio> player, or Audio()), with the wall-clock time
HOOK = """(() => { window.__plays = [];
  const play = HTMLMediaElement.prototype.play;
  HTMLMediaElement.prototype.play = function(){ try{ if(this.src && !this.src.startsWith('data:')) window.__plays.push([Date.now(), this.src]); }catch(e){}
    return play.call(this); };
  // the right/wrong answer sounds go through Web Audio (sounds.js): note them too
  let rs; Object.defineProperty(window, 'RafiqSound', { configurable:true, get:() => rs, set:v => { rs = v; const a = v.answer;
    v.answer = ok => { window.__plays.push([Date.now(), ok ? 'sounds/correct.mp3' : 'sounds/wrong.mp3']); return a(ok); }; } });
})();"""
# the tutor streams its answer: stand in for the `tutor` function with the text from window.__tutorText, 3 characters every 30 ms
TUTOR = """(() => { const f = window.fetch;
  window.fetch = function(u, o){ if(String(u).includes('/functions/v1/tutor')){
    const body = JSON.parse((o && o.body) || '{}'); const t = (body.mode === 'why' ? window.__whyText : window.__tutorText) || '';
    const enc = new TextEncoder(); let i = 0;
    const s = new ReadableStream({ pull(c){ return new Promise(r => setTimeout(() => { if(i >= t.length){ c.close(); r(); return; }
      c.enqueue(enc.encode(t.slice(i, i + 3))); i += 3; r(); }, 30)); } });
    return Promise.resolve(new Response(s, { status:200, headers:{ 'Content-Type':'text/plain' } })); }
    return f.apply(this, arguments); }; })();"""
# the AI answer checker (judge.js → the rafiq-judge Worker): every answer is good
JUDGE = {"vocab": {"ok": 1}, "produce": {"ok": 0.95}, "build": {"ok": 0.95, "order": 0.9}, "rewrite": {"ok": 0.95, "changes": 0.95},
         "prompt": {"done": 2, "grammar": 0.9}, "reply": {"fits": 0.95, "grammar": 0.92, "follows": 0.9}}

class Rec:
    """Frames and sounds for one clip. shot() saves a frame; hold(s) keeps saving frames for s seconds."""
    def __init__(self, page, name):
        self.p, self.name, self.frames, self.t0 = page, name, [], None
    def start(self):
        self.t0 = time.time(); self.shot(); return self
    def shot(self):
        try: self.frames.append((time.time(), self.p.screenshot(type="jpeg", quality=88)))
        except Exception: pass
    def hold(self, s):
        end = time.time() + s
        while time.time() < end: self.shot()
    def act(self, fn, after=0.0):                      # do something, then keep filming
        fn(); self.shot(); self.hold(after)
    def save(self):
        self.shot()
        d = os.path.join(OUT, self.name); os.makedirs(d, exist_ok=True)
        for f in os.listdir(d): os.remove(os.path.join(d, f))
        lst = []
        for i, (t, img) in enumerate(self.frames):
            open(os.path.join(d, f"{i:04d}.jpg"), "wb").write(img)
            if i: lst.append(f"duration {t - self.frames[i - 1][0]:.4f}")
            lst.append(f"file '{i:04d}.jpg'")
        lst += ["duration 0.1", f"file '{len(self.frames) - 1:04d}.jpg'"]
        open(os.path.join(d, "list.txt"), "w").write("\n".join(lst) + "\n")
        mp4 = os.path.join(OUT, self.name + ".mp4")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(d, "list.txt"),
                        "-vf", "fps=30,scale=780:-2", "-pix_fmt", "yuv420p", "-crf", "20", mp4], check=True)
        plays = self.p.evaluate("window.__plays || []")
        sounds = [[round(ms / 1000 - self.t0, 2), src.split(B)[-1].split("?")[0]] for ms, src in plays if ms / 1000 >= self.t0 - 2]     # a sound that began just before (negative) is trimmed in the video
        sounds = [x for i, x in enumerate(sounds) if x not in sounds[:i]]          # the answer sound is noted twice (tutor.js wraps it too)
        length = self.frames[-1][0] - self.t0
        json.dump({"length": round(length, 2), "sounds": sounds}, open(os.path.join(OUT, self.name + ".json"), "w"))
        for f in os.listdir(d): os.remove(os.path.join(d, f))
        os.rmdir(d)
        print(f"  {self.name}: {length:.1f}s, {len(self.frames)} frames, sounds {sounds}")

def context(b, mirror=None, signed=False, extra=None):
    c = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    if FONTS: c.route("https://fonts.googleapis.com/**", lambda r: r.fulfill(status=200, content_type="text/css", body=FONTS))
    c.route("**/@supabase/**", (lambda r: r.fulfill(status=200, content_type="application/javascript", body=FAKE_SUPABASE)) if signed else (lambda r: r.abort()))
    c.route("**/functions/v1/quran", lambda r: r.fulfill(status=503, content_type="application/json", body='{"error":"stub"}'))
    c.route("https://rafiq-judge.luq09.workers.dev/**", lambda r: r.fulfill(status=200, content_type="application/json",
        body=json.dumps(JUDGE.get(json.loads(r.request.post_data or "{}").get("kind"), {}))) if r.request.method == "POST" else r.fulfill(status=200, body="ok"))
    seed = {"rafiq_goal": "2", **(extra or {})}
    if mirror is not None: seed["rafiq_progress_mirror"] = json.dumps(mirror)
    c.add_init_script("if(!localStorage.getItem('__seeded')){" + "".join(f"localStorage.setItem({json.dumps(k)},{json.dumps(v)});" for k, v in seed.items())
                      + "localStorage.setItem('__seeded','1')}")
    c.add_init_script(HOOK); c.add_init_script(TUTOR)
    return c

def seen(*ks): return {k: {"box": 0, "seen": 1} for k in ks}

# RafiqTiles.create: keep each sentence's pieces in order, so a demo can build it right
TILES = """(() => { let t; Object.defineProperty(window, 'RafiqTiles', { configurable:true, get:() => t, set:v => { t = v; const c = v.create;
  v.create = o => { window.__tileParts = o.parts; return c(o); }; } }); })();"""
MISTAKES = json.dumps({"gender_agreement": [int(time.time() * 1000) - i * 3600000 for i in range(5)]})
UNIT1 = seen("p:00|placed", "p:01|words1", "p:01|listen", "p:01|grammar", "p:01|words2", "s:" + TODAY)
TUTOR_Q = "What's the difference between هَذا and هَذِهِ?"
TUTOR_A = ("The difference is **masculine and feminine**.\n\n- هَذا is for a man or a masculine word: هَذا بَيْتٌ, *this is a house*.\n"
           "- هَذِهِ is for a woman or a feminine word: هَذِهِ غُرْفَةٌ, *this is a room*.\n\nMost feminine words end in ة, so that's a good clue.")
WHYS = json.load(open(os.path.join(HERE, "whys.json")))

def goto(pg, url, wait=1800, early=False):
    pg.goto(B + url, wait_until="domcontentloaded" if early else "load"); pg.wait_for_timeout(wait)
def click_text(pg, sel, text): pg.locator(sel, has_text=text).first.click()
def salah_ids(pg): return pg.evaluate("RafiqSalah.parts().map(p => p.id)")
def done_before(pg, part):
    ids = salah_ids(pg); pg.evaluate("ids => ids.forEach(i => Progress.touch('sp:' + i))", ids[:ids.index(part)]); pg.wait_for_timeout(300)

# ---- the demos -------------------------------------------------------------------------------
def d_mostsaid(b):          # Your salah: the most-said words, scrolled slowly
    pg = context(b, seen("p:00|placed")).new_page(); goto(pg, "learn.html?salah=common1", 2500)
    r = Rec(pg, "mostsaid").start(); r.hold(1.5)
    for _ in range(10): pg.mouse.wheel(0, 45); r.hold(0.12)
    r.hold(1.2); r.save()

def d_quiz(b):              # Pick the meaning (right), then Hear it, pick the word (right)
    pg = context(b, seen("p:00|placed")).new_page(); goto(pg, "learn.html?salah=quiz", 2500)
    r = Rec(pg, "quiz").start(); r.hold(1.2)
    right = pg.evaluate("""(() => { const ar = document.querySelector('#stage').innerText.split('\\n').find(l => /[\\u0600-\\u06FF]/.test(l)).trim();
      for (const p of RafiqSalah.parts()) for (const l of p.lines) for (const w of l.words) if (w.ar === ar) return w.en; return null; })()""")
    opts = pg.locator(".opt"); texts = [opts.nth(i).inner_text().strip() for i in range(opts.count())]
    r.act(lambda: opts.nth(texts.index(right) if right in texts else 0).click(), 1.6)
    goto(pg, "learn.html?salah=listen", 300); r.hold(2.2)
    src = pg.evaluate("(window.__plays.slice(-1)[0] || [0, ''])[1]").split("/")[-1].replace(".mp3", "")
    opts = pg.locator(".opt"); n = opts.count()
    pick = next((i for i in range(n) if pg.evaluate("t => RQ.clipId(t)", opts.nth(i).inner_text().strip()) == src), 0)
    r.act(lambda: opts.nth(pick).click(), 1.8); r.save()

def d_part(b):              # a part of the prayer word by word, playing (the tashahhud)
    c = context(b, seen("p:00|placed")); pg = c.new_page(); goto(pg, "salah.html", 1500); done_before(pg, "tashahhud")
    goto(pg, "learn.html?salah=tashahhud", 0, True)
    r = Rec(pg, "part").start(); r.hold(6.0)
    r.act(lambda: click_text(pg, "button", "Next line"), 5.0); r.save()

def d_parts_list(b):        # Your salah: the parts, scrolled
    c = context(b, seen("p:00|placed")); pg = c.new_page(); goto(pg, "salah.html", 1500); done_before(pg, "ruku"); goto(pg, "salah.html", 1500)
    pg.mouse.wheel(0, 380); pg.wait_for_timeout(400)
    r = Rec(pg, "parts").start(); r.hold(0.8)
    for _ in range(14): pg.mouse.wheel(0, 50); r.hold(0.1)
    r.hold(1.2); r.save()

def d_count(b):             # the words-understood count growing
    c = context(b, seen("p:00|placed")); pg = c.new_page(); goto(pg, "salah.html", 1500)
    ids = pg.evaluate("RafiqSalah.words().map(RafiqSalah.wid)")
    r = Rec(pg, "count").start(); r.hold(1.0)
    for n in (24, 61, 97, 138):
        pg.evaluate("ids => ids.forEach(i => { if (Progress.isNew(i)) Progress.grade(i, 'good'); })", ids[:n]); pg.wait_for_timeout(200)
        pg.reload(); pg.wait_for_timeout(700); r.hold(1.1)
    r.save()

def d_prayalong(b):         # Pray along: the takbir, then the opening supplication, words lighting up
    pg = context(b, seen("p:00|placed")).new_page(); goto(pg, "learn.html?salah=prayalong&surah=ikhlas", 0, True)
    r = Rec(pg, "prayalong").start(); r.hold(3.0)
    r.act(lambda: click_text(pg, "button", "Next"), 7.5); r.save()

def d_tutor(b):             # the Tutor tab: a question typed, the answer streaming in
    pg = context(b, seen("p:00|placed"), signed=True).new_page()
    goto(pg, "tutor.html", 1800); pg.evaluate("t => window.__tutorText = t", TUTOR_A)
    r = Rec(pg, "tutor").start(); r.hold(0.8)
    pg.click("#q")
    for ch in TUTOR_Q: pg.keyboard.insert_text(ch); r.shot()
    r.hold(0.5); r.act(lambda: pg.click("#send"), 4.5); r.save()

def d_why(b):               # a wrong answer, Why?, the explanation
    for attempt in range(12):
        pg = context(b, seen("p:00|placed"), signed=True).new_page(); goto(pg, "learn.html?salah=quiz", 2500)
        ar = pg.evaluate("document.querySelector('#stage').innerText.split('\\n').find(l => /[\\u0600-\\u06FF]/.test(l)).trim()")
        right = pg.evaluate("""ar => { for (const p of RafiqSalah.parts()) for (const l of p.lines) for (const w of l.words) if (w.ar === ar) return w.en; return null; }""", ar)
        if right in WHYS: break
        pg.context.close()
    opts = pg.locator(".opt"); texts = [opts.nth(i).inner_text().strip() for i in range(opts.count())]
    wrong = next(i for i, t in enumerate(texts) if t != right)
    pg.evaluate("t => window.__whyText = t", WHYS[right])
    r = Rec(pg, "why").start(); r.hold(1.0)
    r.act(lambda: opts.nth(wrong).click(), 1.3)
    r.act(lambda: pg.click(".tu-why"), 5.0); r.save()

def d_scene(b):             # a real-life scene: reply in your own words, feedback
    pg = context(b, seen("p:00|placed")).new_page(); goto(pg, "learn.html?scene=masjid", 2500)
    r = Rec(pg, "scene").start(); r.hold(1.5)
    pg.click("textarea.ar-in")
    for ch in "وَعَلَيْكُمُ السَّلامُ. نَعَمْ، أَنا جَدِيدٌ هُنا.": pg.keyboard.insert_text(ch); r.shot()
    r.hold(0.4); r.act(lambda: click_text(pg, "button", "Send"), 3.5); r.save()

def d_weak(b):              # Home's weak-spot card, then the weak-spots review
    pg = context(b, UNIT1, extra={"rafiq_mistakes": MISTAKES}).new_page(); goto(pg, "dashboard.html", 2000)
    card = pg.locator("text=Masculine and feminine").first
    if card.count(): card.scroll_into_view_if_needed(); pg.mouse.wheel(0, -120); pg.wait_for_timeout(300)
    r = Rec(pg, "weak").start(); r.hold(2.0)
    goto(pg, "session.html?focus=weak", 900); r.hold(2.5); r.save()

def d_home(b):              # Home, Continue
    pg = context(b, seen("p:00|placed", "p:01|words1", "s:" + TODAY)).new_page(); goto(pg, "dashboard.html", 2000)
    r = Rec(pg, "home").start(); r.hold(2.0)
    r.act(lambda: pg.click("a.cont"), 3.5); r.save()

def d_letters(b):           # the alphabet: tap letters, hear them
    pg = context(b, {}).new_page(); goto(pg, "learn.html?u=00&s=letters1", 2000)
    r = Rec(pg, "letters").start(); r.hold(1.0)
    for ch in ("ب", "ت", "ث", "ج"): r.act(lambda ch=ch: click_text(pg, ".abc-l", ch), 1.1)
    r.save()

def d_words(b):             # meet new words: the word card and its native voice, then the next word
    pg = context(b, seen("p:00|placed")).new_page(); goto(pg, "learn.html?u=01&s=words1", 0, True)
    r = Rec(pg, "words").start(); r.hold(3.2)
    r.act(lambda: click_text(pg, "button", "Next word"), 3.2); r.save()

def d_listen(b):            # the conversation, line by line, then a grammar note
    pg = context(b, seen("p:00|placed", "p:01|words1")).new_page(); goto(pg, "learn.html?u=01&s=listen", 0, True)
    r = Rec(pg, "listen").start(); r.hold(1.0)
    r.act(lambda: click_text(pg, "button", "Again"), 3.5)
    r.act(lambda: click_text(pg, "button", "Next line"), 3.5)
    goto(pg, "learn.html?u=01&s=grammar", 900); r.hold(3.0); r.save()

def d_tiles(b):             # word tiles: build the sentence, check, right
    c = context(b, UNIT1); c.add_init_script(TILES); pg = c.new_page(); goto(pg, "learn.html?u=01&s=practise", 2000)
    for _ in range(12):     # answer until a tiles question comes up
        if pg.evaluate("!!window.__tileParts && !!document.querySelector('.tl-pool, .tiles, [class*=tile]')"): break
        o = pg.locator(".opt"); 
        if o.count(): o.first.click(); pg.wait_for_timeout(500)
        nx = pg.locator("button", has_text="Next"); 
        if nx.count(): nx.first.click(); pg.wait_for_timeout(600)
        else: pg.locator("button", has_text="Skip").first.click() if pg.locator("button", has_text="Skip").count() else None; pg.wait_for_timeout(600)
    parts = pg.evaluate("window.__tileParts")
    r = Rec(pg, "tiles").start(); r.hold(1.5)
    for part in parts:
        r.act(lambda part=part: pg.locator("button", has_text=part).filter(has_not=pg.locator(".placed")).first.click(), 0.6)
    r.act(lambda: pg.locator("button", has_text="Check").first.click(), 2.2); r.save()

def d_spelling(b):          # the spelling bee: see the word, type it on the Arabic keyboard, check
    pg = context(b, UNIT1).new_page(); goto(pg, "practise.html#spelling", 2000)
    en = pg.locator("text=Type this word in Arabic").locator("xpath=preceding-sibling::*[1]").inner_text().strip()
    ar = pg.evaluate("en => { const w = VOCAB.find(v => v.en === en); return w ? w.ar : null }", en)
    bare = "".join(ch for ch in (ar or "") if not ("ً" <= ch <= "ْ" or ch == "ٰ"))
    r = Rec(pg, "spelling").start(); r.hold(1.5)
    for ch in bare: r.act(lambda ch=ch: pg.locator("button.arkb-key", has_text=ch).first.click(), 0.25)
    r.act(lambda: click_text(pg, "button", "Check"), 2.5); r.save()

def d_plans(b):             # Plans: the Complete card
    pg = context(b, {}).new_page(); goto(pg, "plans.html", 1500)
    pg.evaluate("(()=>{const h=[...document.querySelectorAll('h2,h3,b,div')].find(e=>e.textContent.trim()==='Complete'); if(h) h.scrollIntoView({block:'start'}); window.scrollBy(0,-120);})()")
    pg.wait_for_timeout(400)
    r = Rec(pg, "plans").start(); r.hold(1.0)
    for _ in range(8): pg.mouse.wheel(0, 30); r.hold(0.1)
    r.hold(1.5); r.save()

DEMOS = {k[2:]: v for k, v in list(globals().items()) if k.startswith("d_")}
if __name__ == "__main__":
    todo = sys.argv[1:] or list(DEMOS)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, args=["--autoplay-policy=no-user-gesture-required"])
        for name in todo:
            try: DEMOS[name](b)
            except Exception as e: print(f"  {name}: FAILED {str(e)[:300]}")
        b.close()
