#!/usr/bin/env python3
"""Three teaching TikToks / Reels (#218): each teaches one real thing and shows what Rafiq does with it.

  t1-masjid     "Why is a mosque called a masjid?"  The مَـ pattern: the place of …  (مَسْجِد, مَدْرَسَة, مَكْتَبَة, مَطْعَم, then
                your turn: مَطْبَخ).
  t2-subhana    "You say this word 36 times in every four-rakʿah prayer."  Where the 36 come from (salah.js REPS: 12 in rukūʿ,
                24 in sujūd), what it means word by word, and the app's own figure: the 20 words you say most are about 56%.
  t3-remember   Why a new word fades, and how Rafiq brings it back: the real gaps progress.js + fsrs.js give a word you keep
                remembering (3 days, 2 weeks, 57 days, 196 days); a missed word comes back sooner.

1080x1920, no narrator, the quiz videos' look (build_quiz.py's CSS and helpers), the app's own recordings for every Arabic word,
tap.mp3 / correct.mp3 on the frame that causes them, the courtyard fountain underneath, no music. Every word and number is
from the app's data (vocab-data.js, salah-data.js, salah.js, progress.js), except the plain-English glosses.

  python3 brag-quiz/build_teach.py [id ...]            writes brag-quiz/out/<id>/composition
  then in each:  npx hyperframes render -o ../<id>.mp4
  python3 brag-quiz/build_teach.py --level [id ...]    levels each rendered video: -16 LUFS for the voiced two (TikTok plays near -14),
                                                       -25 for t3, which is mostly the fountain
"""
import json, os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build_quiz as Q                                         # house CSS tokens, helpers, recordings, asset folders
ROOT, V6, e, mixed, dur, AUDIO = Q.ROOT, Q.V6, Q.e, Q.mixed, Q.dur, Q.AUDIO
LUFS = {"t1-masjid": -16.0, "t2-subhana": -16.0, "t3-remember": -25.0}   # t3 is mostly the fountain: levelled softer so the fountain stays as soft as in t1
GREEN, RED, INK = "#2e7263", "#b4322a", "#17262b"

CSS = Q.CSS + """
.sec { position:absolute; inset:0; }
.q2 { position:absolute; top:250px; left:80px; right:80px; text-align:center; font-size:68px; font-weight:700; line-height:1.14; letter-spacing:-.02em; }
.q2 .ar { font-family:var(--ar); color:var(--rubric); }
.big { position:absolute; left:0; right:0; text-align:center; font-family:var(--ar); font-weight:700; font-size:210px; line-height:1.3; }
.pv { color:var(--ink); } .pr { color:var(--ink); }
.eqs { position:absolute; left:110px; right:110px; display:flex; flex-direction:column; gap:22px; }
.eq { display:flex; align-items:center; gap:30px; background:var(--card); border:4px solid rgba(23,38,43,.13); border-radius:32px; padding:18px 34px;
  box-shadow:0 12px 26px -16px rgba(23,38,43,.35); }
.eq .tag { min-width:190px; text-align:center; font-family:var(--ar); font-weight:700; font-size:72px; line-height:1.45; }
.eq .tag.v { color:var(--verdigris); } .eq .tag.r { color:var(--rubric); }
.eq .t { font-size:48px; font-weight:700; line-height:1.2; }
.eq .t .ar { font-family:var(--ar); color:var(--ink); }
.say { position:absolute; left:80px; right:80px; text-align:center; font-size:66px; font-weight:700; line-height:1.15; letter-spacing:-.02em; color:var(--verdigris); }
.rows { position:absolute; left:80px; right:80px; display:flex; flex-direction:column; gap:26px; }
.row { display:flex; align-items:center; justify-content:space-between; gap:24px; height:218px; padding:0 46px; background:var(--card);
  border:4px solid rgba(23,38,43,.13); border-radius:36px; box-shadow:0 12px 26px -16px rgba(23,38,43,.35); }
.row .ar { font-family:var(--ar); font-weight:700; font-size:104px; line-height:1.45; }
.row .en b { display:block; font-size:58px; font-weight:700; letter-spacing:-.01em; }
.row .en span { display:block; font-size:36px; color:var(--ink-soft); margin-top:6px; line-height:1.25; }
.row .en span .ar { font-size:40px; color:var(--rubric); font-weight:700; }
.hint { position:absolute; left:80px; right:80px; text-align:center; font-size:52px; font-weight:700; color:var(--ink-soft); }
.ans { position:absolute; left:50%; width:600px; margin-left:-300px; text-align:center; font-size:72px; font-weight:700; color:var(--paper);
  background:var(--verdigris); border-radius:999px; padding:22px 0; }
.roll { position:absolute; left:0; right:0; overflow:hidden; display:flex; justify-content:center; }
.roll .col { display:flex; flex-direction:column; }
.roll .col div { text-align:center; font-weight:700; color:var(--verdigris); letter-spacing:-.04em; }
.roll .pc { font-weight:700; color:var(--verdigris); }
.lbl { position:absolute; left:80px; right:80px; text-align:center; font-size:56px; font-weight:700; line-height:1.18; letter-spacing:-.015em; }
.lbl .ar { font-family:var(--ar); color:var(--rubric); }
.sum { display:flex; flex-direction:column; gap:10px; background:var(--card); border:4px solid rgba(23,38,43,.13); border-radius:36px; padding:26px 40px 30px;
  box-shadow:0 12px 26px -16px rgba(23,38,43,.35); }
.sum .top { display:flex; justify-content:space-between; align-items:baseline; font-size:40px; font-weight:700; color:var(--ink-soft); }
.sum .top b { font-size:76px; color:var(--verdigris); }
.sum .ar { font-family:var(--ar); font-weight:700; font-size:70px; line-height:1.5; text-align:right; direction:rtl; }
.sum .ar i { font-style:normal; color:var(--rubric); }
.total { position:absolute; left:80px; right:80px; text-align:center; font-size:96px; font-weight:700; letter-spacing:-.02em; }
.total b { color:var(--verdigris); }
.words { position:absolute; left:60px; right:60px; display:flex; flex-direction:row-reverse; justify-content:center; gap:22px; }
.w { flex:1; display:flex; flex-direction:column; align-items:center; gap:4px; background:var(--card); border:4px solid rgba(23,38,43,.13); border-radius:30px;
  padding:16px 8px 22px; box-shadow:0 12px 26px -16px rgba(23,38,43,.35); }
.w .ar { font-family:var(--ar); font-weight:700; font-size:78px; line-height:1.5; }
.w .en { font-size:40px; font-weight:700; color:var(--verdigris); text-align:center; line-height:1.15; }
.tr { position:absolute; left:80px; right:80px; text-align:center; font-size:46px; color:var(--ink-soft); line-height:1.3; }
.bar { position:absolute; left:140px; right:140px; height:34px; border-radius:17px; background:rgba(23,38,43,.10); overflow:hidden; }
.bar i { position:absolute; left:0; top:0; bottom:0; width:56%; border-radius:17px; background:var(--verdigris); transform-origin:left center; }
.card1 { position:absolute; left:50%; width:520px; margin-left:-260px; text-align:center; background:var(--card); border:4px solid rgba(23,38,43,.13);
  border-radius:40px; padding:10px 0 26px; box-shadow:0 12px 26px -16px rgba(23,38,43,.35); }
.card1 .ar { font-family:var(--ar); font-weight:700; font-size:150px; line-height:1.45; }
.card1 .en { font-size:52px; font-weight:700; color:var(--ink-soft); margin-top:-8px; }
#graph { position:absolute; left:60px; top:520px; width:960px; height:700px; }
#graph text { font-family:var(--ut); font-size:32px; fill:var(--ink-soft); }
#graph .ax { stroke:rgba(23,38,43,.35); stroke-width:4; fill:none; }
#graph .c { fill:none; stroke-width:10; stroke-linecap:round; stroke-linejoin:round; stroke-dasharray:1; stroke-dashoffset:1; }
#graph .dot { fill:var(--verdigris); }
.cap { position:absolute; left:70px; right:70px; top:1255px; text-align:center; font-size:54px; font-weight:700; line-height:1.18; letter-spacing:-.015em;
  background:var(--card); border:4px solid rgba(23,38,43,.13); border-radius:36px; padding:28px 40px 32px; box-shadow:0 14px 30px -16px rgba(23,38,43,.4); }
.cap em { font-style:normal; color:var(--rubric); } .cap b { color:var(--verdigris); }
"""

def word(pieces, cls=""):
    """an Arabic word in coloured parts: 'v' the pattern (green), 'r' the root letters (red), '' plain"""
    return f'<span class="{cls}" lang="ar" dir="rtl">' + "".join(f'<span class="p{k}">{e(t)}</span>' if k else e(t) for t, k in pieces) + '</span>'

class Comp:
    def __init__(self, vid, kicker, bed=True):
        self.id, self.kicker, self.bed = vid, kicker, bed       # bed=False: no fountain (build_ten.py: the reading voice only)
        self.out = os.path.join(HERE, "out", vid, "composition"); self.a = os.path.join(self.out, "assets")
        if os.path.exists(self.out): shutil.rmtree(self.out)
        for d in ("fonts", "lib", "sfx", "audio"): os.makedirs(os.path.join(self.a, d))
        for f in os.listdir(os.path.join(V6, "fonts")): shutil.copy(os.path.join(V6, "fonts", f), os.path.join(self.a, "fonts"))
        shutil.copy(os.path.join(V6, "lib/gsap.min.js"), os.path.join(self.a, "lib"))
        shutil.copy(os.path.join(V6, "sfx-gen/tap.mp3"), os.path.join(self.a, "sfx")); shutil.copy(os.path.join(ROOT, "sounds/correct.mp3"), os.path.join(self.a, "sfx"))
        self.js, self.audio = [], []
    def t(self, s): self.js.append(s)
    def say(self, text, at, vol=1.0):
        """the app's own recording of this Arabic (audio-manifest.json), at time `at`; returns its length"""
        src = os.path.join(ROOT, "audio", AUDIO[text] + ".mp3"); shutil.copy(src, os.path.join(self.a, "audio"))
        d = dur(src)
        self.audio.append(f'<audio id="s{len(self.audio)}" src="assets/audio/{AUDIO[text]}.mp3" data-start="{at:.2f}" data-duration="{d:.2f}" data-volume="{vol}" data-track-index="{10 + len(self.audio) % 2}"></audio>')
        return d
    def sfx(self, name, at, vol=None):
        f = os.path.join(self.a, "sfx", name + ".mp3"); v = vol if vol is not None else {"tap": 0.45, "correct": 0.55}[name]
        self.audio.append(f'<audio id="s{len(self.audio)}" src="assets/sfx/{name}.mp3" data-start="{at:.2f}" data-duration="{dur(f):.2f}" data-volume="{v}" data-track-index="{14 + len(self.audio) % 2}"></audio>')
    def inn(self, sel, at, y=24, d=0.45):
        self.t(f'tl.fromTo("{sel}", {{opacity:0, y:{y}}}, {{opacity:1, y:0, duration:{d}, ease:"power3.out"}}, {at:.2f});')
    def out_(self, sel, at):
        self.t(f'tl.to("{sel}", {{opacity:0, y:-24, duration:0.35, ease:"power2.in"}}, {at:.2f});')
    def end(self, at, line):
        self.t(f'tl.to(["#brand", "#kicker"], {{opacity:0, duration:0.3}}, {at - 0.3:.2f});')
        self.t(f'tl.fromTo("#end", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.5, ease:"power3.out"}}, {at:.2f});')
        return f'<div id="end"><div class="tile"><span>ر</span><em></em></div><h2>{mixed(line)}</h2><div class="url">rafiq-arabic.com</div><p>Free for a week · no card needed</p></div>'
    def write(self, body, total):
        # the fountain, played on past its 22s if needed (two copies crossfaded): a soft bed, heard but well under the words
        if self.bed:
            bed = os.path.join(self.a, "sfx", "fountain.mp3"); src = os.path.join(V6, "sfx-gen/fountain.mp3")
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-i", src, "-filter_complex",
                            f"[0][1]acrossfade=d=2:c1=tri:c2=tri,volume=6dB,atrim=0:{total + 0.5:.2f},afade=t=in:d=0.6,afade=t=out:st={total - 1.4:.2f}:d=1.4",
                            "-c:a", "libmp3lame", "-q:a", "3", bed], check=True)
            self.audio.append(f'<audio id="bed" src="assets/sfx/fountain.mp3" data-start="0" data-duration="{total:.2f}" data-volume="0.1" data-track-index="8"></audio>')
        head = ['tl.fromTo("#glow", {scale:0.94}, {scale:1.08, duration:' + f'{total}' + ', ease:"none"}, 0);',
                'tl.fromTo("#brand", {opacity:0, y:-10}, {opacity:1, y:0, duration:0.4, ease:"power3.out"}, 0);',
                'tl.fromTo("#kicker", {opacity:0}, {opacity:1, duration:0.3}, 0.05);']
        css = CSS + getattr(self, "css", "")
        doc = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
    <title>Rafiq: {e(self.id)}</title>
    <script src="assets/lib/gsap.min.js"></script>
    <style>{css}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{total}">
      <div id="glow"></div>
      <div id="brand"><div class="tile"><span>ر</span><em></em></div><b>رَفِيق</b></div>
      <div id="kicker">{e(self.kicker)}</div>
{body}
{chr(10).join('      ' + x for x in self.audio)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join('      ' + x for x in head + self.js)}
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
        open(os.path.join(self.out, "index.html"), "w").write(doc)
        print(f"{self.id}: {total:.1f}s")

def roll(cid, top, n, h, size, pct=False):
    """a counter that rolls from 0 up to n: one column of numbers slid up (deterministic, no callbacks)"""
    nums = "".join(f'<div style="height:{h}px;line-height:{h}px;font-size:{size}px">{k}</div>' for k in range(n + 1))
    pc = f'<span class="pc" style="font-size:{int(size * 0.6)}px;line-height:{h}px">%</span>' if pct else ""
    return f'<div class="roll" id="{cid}" style="top:{top}px;height:{h}px"><div class="col" id="{cid}c" data-layout-allow-overflow>{nums}</div>{pc}</div>'

# ---------------------------------------------------------------- t1: the مَـ pattern
def t1():
    c = Comp("t1-masjid", "ARABIC · ONE PATTERN")
    MASJID = [("مَ", "v"), ("سْ", "r"), ("جِ", "r"), ("د", "r")]
    ROWS = [([("مَ", "v"), ("دْ", "r"), ("رَ", "r"), ("سَ", "r"), ("ة", "")], "مَدْرَسَة", "a school", "the place of studying · دَرَسَ"),
            ([("مَ", "v"), ("كْ", "r"), ("تَ", "r"), ("بَ", "r"), ("ة", "")], "مَكْتَبَة", "a library", "the place of books · كِتاب"),
            ([("مَ", "v"), ("طْ", "r"), ("عَ", "r"), ("م", "r")], "مَطْعَم", "a restaurant", "the place of food · طَعام")]
    KITCHEN = [("مَ", "v"), ("طْ", "r"), ("بَ", "r"), ("خ", "r")]
    # 1. the hook, and the split
    c.inn("#a .q2", 0.1); c.t('tl.fromTo("#a .big", {opacity:0, scale:0.94}, {opacity:1, scale:1, duration:0.5, ease:"power3.out"}, 0.45);')
    c.say("مَسْجِد", 1.0)
    c.t(f'tl.fromTo("#a .big .pv", {{color:"{INK}"}}, {{color:"{GREEN}", duration:0.35}}, 2.5);'); c.sfx("tap", 2.5)
    c.t(f'tl.fromTo("#a .big .pr", {{color:"{INK}"}}, {{color:"{RED}", duration:0.35}}, 2.9);')
    c.inn("#e1", 3.0); c.inn("#e2", 3.8); c.sfx("tap", 3.8)
    c.inn("#a .say", 4.8); c.sfx("correct", 4.8)
    c.t('tl.fromTo("#a .say", {scale:1}, {scale:1.04, duration:0.16, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}, 5.25);')
    c.out_("#a", 6.9)
    # 2. everywhere
    c.inn("#b .q2", 7.3); t = 7.8
    for i, (_, ar, _, _) in enumerate(ROWS):
        c.inn(f"#r{i}", t, 30); c.sfx("tap", t); c.say(ar, t + 0.35)
        c.t(f'tl.fromTo("#r{i} .pv", {{color:"{INK}"}}, {{color:"{GREEN}", duration:0.3}}, {t + 0.35:.2f});')
        c.t(f'tl.fromTo("#r{i} .pr", {{color:"{INK}"}}, {{color:"{RED}", duration:0.3}}, {t + 0.6:.2f});')
        t += 2.3
    c.out_("#b", t + 0.4)
    # 3. your turn: the place of cooking, a 3-2-1, then the answer
    T = t + 0.8
    c.inn("#k .q2", T); c.t(f'tl.fromTo("#k .big", {{opacity:0, scale:0.94}}, {{opacity:1, scale:1, duration:0.5, ease:"power3.out"}}, {T + 0.3:.2f});')
    c.t(f'tl.fromTo("#k .big .pv", {{color:"{INK}"}}, {{color:"{GREEN}", duration:0.3}}, {T + 0.9:.2f});')
    c.t(f'tl.fromTo("#k .big .pr", {{color:"{INK}"}}, {{color:"{RED}", duration:0.3}}, {T + 1.1:.2f});')
    c.inn("#k .hint", T + 1.2)
    cs = T + 2.0
    c.t(f'tl.fromTo("#count", {{opacity:0, scale:0.7}}, {{opacity:1, scale:1, duration:0.3, ease:"power3.out"}}, {cs - 0.3:.2f});')
    c.t(f'tl.fromTo("#count .fg", {{strokeDashoffset:0}}, {{strokeDashoffset:408, duration:3, ease:"none"}}, {cs:.2f});')
    for k in range(3):
        c.t(f'tl.fromTo("#n{3 - k}", {{opacity:0, scale:1.35}}, {{opacity:1, scale:1, duration:0.22, ease:"power3.out"}}, {cs + k:.2f});')
        c.t(f'tl.to("#n{3 - k}", {{opacity:0, duration:0.15}}, {cs + k + 0.82:.2f});'); c.sfx("tap", cs + k)
    R = cs + 3.05
    c.t(f'tl.to("#count", {{opacity:0, scale:0.7, duration:0.25}}, {R - 0.15:.2f});')
    c.t(f'tl.fromTo("#k .ans", {{opacity:0, scale:0.9}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(1.6)"}}, {R:.2f});')   # the one spring: the answer
    c.sfx("correct", R); c.say("مَطْبَخ", R + 0.5)
    c.out_("#k", R + 2.4)
    E = R + 2.8
    endc = c.end(E, "Learn the patterns behind the words")
    body = f"""      <div class="sec" id="a">
        <div class="q2">Why is a mosque called a <bdi class="ar" lang="ar">مَسْجِد</bdi>?</div>
        <div class="big" style="top:470px">{word(MASJID)}</div>
        <div class="eqs" style="top:850px">
          <div class="eq" id="e1"><span class="tag v" lang="ar">مَـ</span><span class="t">= the place of …</span></div>
          <div class="eq" id="e2"><span class="tag r" lang="ar">س ج د</span><span class="t">= <bdi class="ar" lang="ar">السُّجُودُ</bdi>, prostration</span></div>
        </div>
        <div class="say" style="top:1250px">The place of prostration.</div>
      </div>
      <div class="sec" id="b">
        <div class="q2">Once you see it, it’s everywhere:</div>
        <div class="rows" style="top:480px">{''.join(f'<div class="row" id="r{i}"><div class="en"><b>{e(en)}</b><span>{mixed(why)}</span></div><div class="ar">{word(p)}</div></div>' for i, (p, _, en, why) in enumerate(ROWS))}</div>
      </div>
      <div class="sec" id="k">
        <div class="q2">Your turn. What is this place?</div>
        <div class="big" style="top:440px">{word(KITCHEN)}</div>
        <div class="hint" style="top:800px">the place of cooking</div>
        <div id="count" style="top:960px"><svg viewBox="0 0 150 150"><circle class="bg" cx="75" cy="75" r="65"/><circle class="fg" cx="75" cy="75" r="65"/></svg>{''.join(f'<span id="n{k}">{k}</span>' for k in range(3, 0, -1))}</div>
        <div class="ans" style="top:980px">a kitchen</div>
      </div>
      {endc}"""
    c.write(body, round(E + 2.9, 2))

# ---------------------------------------------------------------- t2: 36 times
def t2():
    c = Comp("t2-subhana", "YOUR SALAH · BY THE NUMBERS")
    c.t('tl.fromTo("#a .big", {opacity:0, scale:0.94}, {opacity:1, scale:1, duration:0.5, ease:"power3.out"}, 0.15);')
    c.say("سُبْحانَ", 0.6)
    c.inn("#a .l1", 1.3)
    c.t('tl.fromTo("#n36", {opacity:0}, {opacity:1, duration:0.2}, 1.6);')
    c.t('tl.fromTo("#n36c", {y:0}, {y:-36*330, duration:1.7, ease:"power3.out"}, 1.6);')     # 0 → 36
    c.sfx("tap", 3.25)
    c.inn("#a .l2", 3.0)
    c.out_("#a", 5.6)
    # where they come from
    c.inn("#b .q2", 6.0)
    c.inn("#sa", 6.6, 30); c.sfx("tap", 6.6); da = c.say("سُبْحانَ رَبِّيَ الْعَظِيمِ", 7.0)
    c.inn("#sb", 9.4, 30); c.sfx("tap", 9.4); db = c.say("سُبْحانَ رَبِّيَ الْأَعْلى", 9.8)
    c.inn("#b .total", 12.2); c.sfx("correct", 12.2)
    c.t('tl.fromTo("#b .total", {scale:1}, {scale:1.04, duration:0.16, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}, 12.65);')
    c.out_("#b", 14.2)
    # what it means, word by word
    c.inn("#m .q2", 14.6)
    for i in range(3): c.inn(f"#w{i}", 15.1 + i * 0.45, 30); c.sfx("tap", 15.1 + i * 0.45)
    c.inn("#m .tr", 16.6)
    c.out_("#m", 19.0)
    # the 56%
    c.inn("#p .lbl.t", 19.4)
    c.t('tl.fromTo("#n56", {opacity:0}, {opacity:1, duration:0.2}, 19.8);')
    c.t('tl.fromTo("#n56c", {y:0}, {y:-56*300, duration:1.6, ease:"power3.out"}, 19.8);')
    c.inn("#p .bar", 19.8, 0, 0.3); c.t('tl.fromTo("#p .bar i", {scaleX:0}, {scaleX:1, duration:1.6, ease:"power3.out"}, 19.8);')
    c.sfx("correct", 21.4)
    c.inn("#p .lbl.b", 21.0)
    c.out_("#p", 23.4)
    E = 23.8
    endc = c.end(E, "Learn those 20 words first")
    row = lambda rid, where, calc, n, ar: (f'<div class="sum" id="{rid}"><div class="top"><span>{e(where)} · {e(calc)}</span><b>{n}</b></div>'
                                          f'<div class="ar" lang="ar"><i>سُبْحانَ</i> {e(ar)}</div></div>')
    words = [("سُبْحانَ", "Glory be to"), ("رَبِّيَ", "my Lord"), ("الْعَظِيمِ", "the Magnificent")]
    body = f"""      <div class="sec" id="a">
        <div class="big" style="top:300px;color:var(--rubric)" lang="ar">سُبْحانَ</div>
        <div class="lbl l1" style="top:700px">You say this word</div>
        {roll("n36", 790, 36, 330, 300)}
        <div class="lbl l2" style="top:1150px">times in every four-rakʿah prayer.</div>
      </div>
      <div class="sec" id="b">
        <div class="q2">Where the 36 come from:</div>
        <div class="rows" style="top:470px">
          {row("sa", "Rukūʿ", "3 times × 4 rakʿahs", 12, "رَبِّيَ الْعَظِيمِ")}
          {row("sb", "Sujūd", "3 times × 2 × 4", 24, "رَبِّيَ الْأَعْلى")}
        </div>
        <div class="total" style="top:1130px">12 + 24 = <b>36</b></div>
      </div>
      <div class="sec" id="m">
        <div class="q2">And what it means:</div>
        <div class="words" style="top:520px">{''.join(f'<div class="w" id="w{i}"><div class="ar" lang="ar">{e(a)}</div><div class="en">{e(en)}</div></div>' for i, (a, en) in enumerate(words))}</div>
        <div class="tr" style="top:870px">“Glory be to my Lord, the Magnificent.”</div>
        <div class="tr" style="top:940px">In sujūd: “… my Lord, the Most High.”</div>
      </div>
      <div class="sec" id="p">
        <div class="lbl t" style="top:420px;left:50px;right:50px;font-size:50px">The 20 words you say most are about</div>
        {roll("n56", 580, 56, 300, 260, pct=True)}
        <div class="bar" style="top:930px"><i></i></div>
        <div class="lbl b" style="top:1030px">of everything you say in a four-rakʿah prayer.</div>
      </div>
      {endc}"""
    c.write(body, round(E + 2.9, 2))

# ---------------------------------------------------------------- t3: why words fade
def t3():
    import math
    c = Comp("t3-remember", "WHY NEW WORDS FADE")
    X0, X1, Y0, Y1 = 90, 920, 100, 560         # plot area in the 960x700 svg: top = remembered well, bottom = forgotten
    # reviews where the app's gaps fall (3 days, 2 weeks, 57 days, 196 days), spaced to read, not to scale
    R = [90, 230, 400, 610, 880]
    def decay(xa, xb, k, steps=24):
        pts = []
        for i in range(steps + 1):
            x = xa + (xb - xa) * i / steps; y = Y0 + (Y1 - Y0) * (1 - math.exp(-k * (x - xa) / (xb - xa)))
            pts.append(f"{x:.1f},{y:.1f}")
        return pts
    red = "M " + " L ".join(decay(X0, X1, 6.5))
    segs = []                                    # each gap fades to the same point, just before you'd forget, then the review lifts it
    for i in range(4):
        pts = decay(R[i], R[i + 1], 0.38, 18)
        segs.append("M " + " L ".join(pts) + f" L {R[i + 1]},{Y0}")
    tail = "M " + " L ".join(decay(R[4], X1 + 10, 0.38 * (X1 + 10 - R[4]) / (R[4] - R[3]), 8))
    labels = ["3 days", "2 weeks", "2 months", "6 months"]
    c.inn("#a .q2", 0.1)
    c.t('tl.fromTo("#a .card1", {opacity:0, scale:0.94}, {opacity:1, scale:1, duration:0.5, ease:"power3.out"}, 0.5);')
    c.say("كِتاب", 1.0)
    c.out_("#a .card1", 3.0)
    c.inn("#graph", 3.3, 20)
    c.t('tl.fromTo("#red", {strokeDashoffset:1}, {strokeDashoffset:0, duration:1.6, ease:"power1.inOut"}, 3.6);')
    c.inn("#c1", 3.8)
    c.t('tl.to("#red", {opacity:0.25, duration:0.4}, 6.4);'); c.out_("#c1", 6.4)
    c.inn("#c2", 6.8); t = 7.0
    for i in range(4):
        c.t(f'tl.fromTo("#g{i}", {{strokeDashoffset:1}}, {{strokeDashoffset:0, duration:1.1, ease:"none"}}, {t:.2f});')
        c.t(f'tl.fromTo("#d{i}", {{opacity:0}}, {{opacity:1, duration:0.25}}, {t + 1.1:.2f});')
        c.inn(f"#l{i}", t + 1.1, 10, 0.3); c.sfx("tap", t + 1.1)
        t += 1.35
    c.t(f'tl.fromTo("#gt", {{strokeDashoffset:1}}, {{strokeDashoffset:0, duration:0.6, ease:"none"}}, {t:.2f});')
    c.out_("#c2", t + 0.3)
    c.inn("#c3", t + 0.7); c.sfx("correct", t + 0.7)
    c.out_("#c3", t + 3.6)
    c.inn("#c4", t + 4.0); c.sfx("tap", t + 4.0)
    c.out_("#c4, #graph, #a .q2", t + 6.2)
    E = t + 6.6
    endc = c.end(E, "Words that come back until they stay")
    svg = f"""<svg id="graph" viewBox="0 0 960 700">
          <path class="ax" d="M {X0},{Y0 - 30} L {X0},{Y1 + 20} L {X1 + 20},{Y1 + 20}"/>
          <text x="{X0 + 14}" y="{Y0 - 46}">remembered</text><text x="{X1 + 20}" y="{Y1 + 110}" text-anchor="end">time →</text>
          <path id="red" class="c" pathLength="1" style="stroke:{RED}" d="{red}"/>
          {''.join(f'<path id="g{i}" class="c" pathLength="1" style="stroke:{GREEN}" d="{s}"/>' for i, s in enumerate(segs))}
          <path id="gt" class="c" pathLength="1" style="stroke:{GREEN}" d="{tail}"/>
          {''.join(f'<circle id="d{i}" class="dot" cx="{R[i + 1]}" cy="{Y0}" r="15"/>' for i in range(4))}
          {''.join(f'<text id="l{i}" x="{R[i + 1]}" y="{Y1 + 64}" text-anchor="middle" style="fill:{GREEN};font-weight:500">{labels[i]}</text>' for i in range(4))}
          <text x="{X0 + 10}" y="{Y1 + 110}" style="font-size:22px">not to scale</text>
        </svg>"""
    body = f"""      <div class="sec" id="a">
        <div class="q2">Learnt a new Arabic word yesterday? It’s already fading.</div>
        <div class="card1" style="top:620px"><div class="ar" lang="ar">كِتاب</div><div class="en">book</div></div>
      </div>
      {svg}
      <div class="cap" id="c1">Without review, a new word <em>fades fast</em>.</div>
      <div class="cap" id="c2">Rafiq brings it back <b>just before you’d forget it</b>.</div>
      <div class="cap" id="c3">Each time you remember it, the gap grows: <b>3 days → 2 weeks → 2 months → 6 months</b>.</div>
      <div class="cap" id="c4">Miss one? It comes back sooner.</div>
      {endc}"""
    c.write(body, round(E + 2.9, 2))

def level(vid):
    """two-pass loudnorm to LUFS[vid] (-16 for the voiced ones), peaks under -1.5 dBTP; the picture is copied as it is"""
    I = LUFS[vid]
    src = os.path.join(HERE, "out", vid, vid + ".mp4"); tmp = src + ".lvl.mp4"
    m = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af", f"loudnorm=I={I}:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    s = json.loads(m[m.rindex("{"):])
    af = (f"loudnorm=I={I}:TP=-1.5:LRA=11:measured_I={s['input_i']}:measured_TP={s['input_tp']}:measured_LRA={s['input_lra']}"
          f":measured_thresh={s['input_thresh']}:offset={s['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-af", af, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, src); print(f"{vid}: levelled from {s['input_i']} LUFS")

if __name__ == "__main__":
    ids = [a for a in sys.argv[1:] if not a.startswith("--")]
    ALL = {"t1-masjid": t1, "t2-subhana": t2, "t3-remember": t3}
    for vid, fn in ALL.items():
        if ids and vid not in ids: continue
        level(vid) if "--level" in sys.argv else fn()
