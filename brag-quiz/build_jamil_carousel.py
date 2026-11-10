"""Carousel: three things Allah calls beautiful (owner, 10 Nov 2026; built with the h11-jamil reel; no pastel, FORMATS.md): our dark
colours, lit desert scenes (deep teal sky, gold sun and rim light, grain), the Arabic in gold, the lines in Instrument Serif.
1 "Allah calls your patience beautiful. And 2 other things." (TypeSafe: 4.91 of 6) · 2 ṣabrun jamīl, Yūsuf 12:18 · 3 hajran jamīlā,
al-Muzzammil 73:10 · 4 aṣ-ṣafḥ al-jamīl, al-Ḥijr 15:85 · 5 why: "Allah is jamīl and He loves beauty" (Muslim 91) · 6 comment 1, 2 or 3.

  python3 brag-quiz/build_jamil_carousel.py   ->  brag-quiz/stills/jamil/jamil-1.png ... -6.png  (1080 x 1350)
"""
import math, os, random
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); F = os.path.join(HERE, "fonts"); OUT = os.path.join(HERE, "stills", "jamil")
GOLD, GOLD2, CREAM, TEAL = "#E9B949", "#f6d27a", "#F1ECE0", "#14232a"
N = 6

DEFS = """<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#07121a"/><stop offset=".4" stop-color="#14232a"/><stop offset=".62" stop-color="#2c3b3a"/>
  <stop offset=".72" stop-color="#7a5a2c"/><stop offset=".78" stop-color="#d79a3c"/><stop offset=".81" stop-color="#f3c86a"/></linearGradient>
<linearGradient id="night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#050c10"/><stop offset=".6" stop-color="#0f1d24"/><stop offset="1" stop-color="#1b2c31"/></linearGradient>
<radialGradient id="bloom"><stop offset="0" stop-color="#ffe3a0" stop-opacity=".85"/><stop offset=".25" stop-color="#f0b04a" stop-opacity=".45"/><stop offset="1" stop-color="#e9b949" stop-opacity="0"/></radialGradient>
<radialGradient id="moonglow"><stop offset="0" stop-color="#f6ecd0" stop-opacity=".5"/><stop offset="1" stop-color="#f6ecd0" stop-opacity="0"/></radialGradient>
<radialGradient id="sun" cx="50%" cy="45%" r="55%"><stop offset="0" stop-color="#fffbe9"/><stop offset=".6" stop-color="#ffe7a6"/><stop offset="1" stop-color="#f6c45c"/></radialGradient>
<linearGradient id="d1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a3838"/><stop offset=".4" stop-color="#1a2a2f"/></linearGradient>
<linearGradient id="d2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1d2e33"/><stop offset=".5" stop-color="#122127"/></linearGradient>
<linearGradient id="d3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#14252b"/><stop offset=".5" stop-color="#0b171b"/></linearGradient>
<linearGradient id="ray" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#ffe6a8" stop-opacity=".5"/><stop offset="1" stop-color="#ffe6a8" stop-opacity="0"/></linearGradient>
<filter id="bl2"><feGaussianBlur stdDeviation="1.6"/></filter><filter id="bl8"><feGaussianBlur stdDeviation="8"/></filter><filter id="haze" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="16"/></filter>
<filter id="rim" x="-20%" y="-20%" width="140%" height="140%"><feMorphology in="SourceAlpha" operator="dilate" radius="3" result="d"/><feOffset in="d" dy="-3" result="o"/>
  <feFlood flood-color="#f8cf6a"/><feComposite in2="o" operator="in" result="r"/><feGaussianBlur in="r" stdDeviation="2.2" result="rb"/>
  <feMerge><feMergeNode in="rb"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="3" seed="4"/>
  <feColorMatrix values="0 0 0 0 1  0 0 0 0 .95  0 0 0 0 .85  0 0 0 .09 0"/></filter>
<radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#02070a" stop-opacity=".7"/></radialGradient>
</defs>"""

def dune(y, amp, seed, fill, rim):
    r = random.Random(seed); pts = [(x, y + amp * math.sin(x / 230 + seed) + 0.5 * amp * math.sin(x / 90 + seed * 2) + r.uniform(-3, 3)) for x in range(-40, 1130, 30)]
    d = f"M{pts[0][0]} {pts[0][1]:.0f} " + " ".join(f"L{x} {yy:.0f}" for x, yy in pts[1:])
    return f'<path d="{d} L1130 1400 L-40 1400 Z" fill="{fill}"/><path d="{d}" fill="none" stroke="{rim}" stroke-width="3" opacity=".75" filter="url(#bl2)"/>'

CAMEL = ("M-175 -300 C-150 -360 -90 -405 -30 -405 C30 -405 70 -360 100 -322 C140 -300 175 -310 200 -335 C220 -360 228 -395 240 -410 "
         "C255 -428 285 -422 300 -405 C312 -393 316 -382 305 -376 C285 -372 262 -378 252 -372 C238 -355 232 -325 220 -295 C205 -265 170 -245 140 -240 "
         "C120 -230 110 -210 100 -200 C40 -185 -60 -185 -120 -200 C-150 -210 -170 -240 -175 -300 Z")
LEG = "M-19 0 L19 0 L13 95 Q19 104 13 116 L10 188 L20 200 L-12 200 L-8 188 L-12 116 Q-19 104 -13 95 Z"
def camel(x, y, s, stride=0):
    leg = lambda lx, a, c: f'<path d="{LEG}" fill="{c}" transform="translate({lx} -200) rotate({a})"/>'
    far = leg(105, stride, "#16262c") + leg(-118, stride, "#16262c"); near = leg(88, -stride, "#0a1418") + leg(-100, -stride, "#0a1418")
    return (f'<g transform="translate({x} {y}) scale({s})" filter="url(#rim)">{far}<path d="{CAMEL}" fill="#0a1418"/>'
            f'<path d="M-174 -290 C-185 -260 -186 -230 -180 -205" stroke="#0a1418" stroke-width="9" fill="none"/>{near}<path d="M268 -402 l6 -14 l6 12 Z" fill="#0a1418"/></g>')

def stars(seed, n=110, ymax=900):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(0, 1080):.0f}" cy="{r.uniform(0, ymax):.0f}" r="{r.uniform(.8, 2.4):.1f}" fill="#fff6dd" opacity="{r.uniform(.25, .9):.2f}"/>' for _ in range(n))

def sunset(sy=1010, herd=True, hero=None):
    s = f'<rect width="1080" height="1350" fill="url(#sky)"/><g opacity=".5">{stars(1, 70, 600)}</g><circle cx="540" cy="{sy}" r="700" fill="url(#bloom)"/>'
    s += f'<circle cx="540" cy="{sy}" r="170" fill="url(#sun)"/><rect x="-100" y="{sy - 40}" width="1280" height="80" fill="#ffd98a" opacity=".2" filter="url(#haze)"/>'
    s += dune(sy + 40, 16, 1, "url(#d1)", "#f3c86a")
    if herd: s += "".join(camel(x, sy + 58, sc, 10 * (-1) ** k) for k, (x, sc) in enumerate(((120, .22), (230, .25), (760, .23), (880, .26), (990, .21))))
    s += dune(sy + 140, 34, 3, "url(#d2)", "#e9b949")
    if hero: s += camel(*hero)
    s += dune(sy + 270, 46, 5, "url(#d3)", "#c99a3a")
    return s

def seated(x, y, s):                       # a faceless figure sitting on a dune, his back to us, knees up, a shawl over the head
    return (f'<g transform="translate({x} {y}) scale({s}) rotate(-4)" filter="url(#rim)"><path d="M-80 0 C-84 -50 -78 -120 -62 -152 C-50 -172 -28 -178 0 -178 '
            f'C28 -178 50 -172 62 -152 C78 -120 84 -50 80 0 Z" fill="#0a1418"/><rect x="-13" y="-196" width="26" height="24" fill="#0a1418"/>'
            f'<ellipse cx="0" cy="-222" rx="31" ry="35" fill="#0a1418"/></g>')
def walker(x, y, s):                       # a faceless figure walking away, robe and head-wrap
    return (f'<g transform="translate({x} {y}) scale({s})" filter="url(#rim)"><path d="M-34 0 L-26 -120 C-30 -160 -22 -190 0 -196 C22 -190 30 -160 26 -120 L34 0 L8 0 L4 -60 L-4 -60 L-8 0 Z" fill="#0a1418"/>'
            f'<circle cx="0" cy="-214" r="22" fill="#0a1418"/></g>')

def foot(x, y, s, a):
    return f'<ellipse cx="{x}" cy="{y}" rx="{9 * s:.1f}" ry="{18 * s:.1f}" transform="rotate({a} {x} {y})" fill="#08121a" opacity=".55"/>'

SCENES = {
 1: sunset(1000, herd=True, hero=(470, 1090, .6, 12)),
 2: (f'<rect width="1080" height="1350" fill="url(#night)"/>{stars(2)}<circle cx="900" cy="250" r="260" fill="url(#moonglow)"/><mask id="cres"><rect width="1080" height="1350" fill="#fff"/><circle cx="924" cy="236" r="52" fill="#000"/></mask>'
     f'<circle cx="900" cy="250" r="58" fill="#f6ecd0" mask="url(#cres)"/>' + dune(1060, 30, 2, "url(#d2)", "#bfae80") + seated(380, 1078, 0.9) + dune(1200, 40, 4, "url(#d3)", "#8f8460")),
 3: (sunset(930, herd=False) + "".join(foot(540 + (-1) ** k * 14 + k * 9, 1340 - k * 46, 1.4 - k * 0.09, 20 - k) for k in range(12)) + walker(650, 1060, 0.62)),
 4: (sunset(1040, herd=False) + "".join(f'<path d="M540 1040 L{540 + 1500 * math.cos(a):.0f} {1040 - 1500 * math.sin(a):.0f} L{540 + 1500 * math.cos(a + .05):.0f} {1040 - 1500 * math.sin(a + .05):.0f} Z" fill="url(#ray)" opacity=".35"/>'
     for a in [math.pi * (0.12 + 0.11 * k) for k in range(7)])),
 5: (f'<rect width="1080" height="1350" fill="url(#night)"/>{stars(5, 220, 1100)}<circle cx="540" cy="560" r="520" fill="url(#bloom)" opacity=".35"/>' + dune(1100, 30, 6, "url(#d2)", "#c99a3a") + dune(1220, 40, 7, "url(#d3)", "#8f7a45")),
 6: sunset(1060, herd=True),
}
SLIDES = {
 1: '''<div class="ar1">جَمِيل</div><div class="h1">Allah calls your<br><b>patience</b> beautiful.</div><div class="h2">And 2 other things.</div><div class="swipe">swipe →</div>''',
 2: '''<div class="n">1</div><div class="ar">فَصَبْرٌ <b>جَمِيلٌ</b></div><div class="en">“So: <b>beautiful</b> patience.”</div><div class="ref">YŪSUF 12:18</div>
<div class="p">Yaʿqūb’s words when his son was taken from him. Beautiful patience: <b>no complaint to people</b>, only to Allah.</div>''',
 3: '''<div class="n">2</div><div class="ar">وَاهْجُرْهُمْ هَجْرًا <b>جَمِيلًا</b></div><div class="en">“And leave them, a <b>beautiful</b> leaving.”</div><div class="ref">AL-MUZZAMMIL 73:10</div>
<div class="p">Walking away from those who hurt you, <b>without insult</b> and without revenge.</div>''',
 4: '''<div class="n">3</div><div class="ar">فَاصْفَحِ الصَّفْحَ <b>الْجَمِيلَ</b></div><div class="en">“So forgive, a <b>beautiful</b> forgiving.”</div><div class="ref">AL-ḤIJR 15:85</div>
<div class="p">Forgiveness with <b>no blame</b> after it.</div>''',
 5: '''<div class="why">Why “beautiful”?</div><div class="ar big">إِنَّ اللَّهَ <b>جَمِيلٌ</b><br>يُحِبُّ <b>الْجَمَالَ</b></div><div class="en">“Allah is <b>beautiful</b>, and He loves beauty.”</div>
<div class="ref">MUSLIM 91</div><div class="p">One root in all of them: <bdi dir="rtl" class="rt">ج م ل</bdi>, <i>beauty</i>.</div>''',
 6: '''<div class="h1 q">Which one do you<br>need <b>most</b> right now?</div><div class="opts"><span>1 <i>patience</i></span><span>2 <i>leaving</i></span><span>3 <i>forgiving</i></span></div>
<div class="h2">Comment 1, 2 or 3 👇</div>''',
}
CSS = f"""
@font-face {{ font-family:IS; src:url("file://{F}/instrument-serif-latin-400-normal.woff2"); }}
@font-face {{ font-family:FR; src:url("file://{F}/fredoka-latin-700-normal.woff2"); }}
@font-face {{ font-family:AM; src:url("file://{F}/amiri-arabic-700-normal.woff2"); }}
* {{ margin:0; box-sizing:border-box; }} body {{ width:1080px; height:1350px; overflow:hidden; background:{TEAL}; position:relative; color:{CREAM}; }}
svg.bg {{ position:absolute; inset:0; width:1080px; height:1350px; }}
.top {{ position:absolute; left:64px; right:64px; top:54px; display:flex; justify-content:space-between; font-family:FR; font-size:28px; letter-spacing:.14em; color:rgba(241,236,224,.7); }}
.top b {{ color:{GOLD}; }}
.c {{ position:absolute; left:70px; right:70px; top:150px; text-align:center; }}
.ar1 {{ font-family:AM; font-size:250px; line-height:1.3; color:{GOLD}; text-shadow:0 0 70px rgba(233,185,73,.55), 0 12px 0 #6d4f12, 0 24px 50px rgba(0,0,0,.6); }}
.h1 {{ font-family:IS; font-size:96px; line-height:1.02; margin-top:6px; text-shadow:0 6px 30px rgba(0,0,0,.6); }} .h1 b {{ font-weight:400; color:{GOLD}; font-style:italic; }}
.h2 {{ font-family:IS; font-style:italic; font-size:66px; color:{GOLD2}; margin-top:24px; }}
.rt {{ font-family:AM; color:{GOLD}; }}
.swipe {{ position:absolute; right:0; top:1100px; padding:14px 34px; border-radius:999px; border:2px solid rgba(233,185,73,.6); font-family:FR; font-size:30px; letter-spacing:.1em; color:{GOLD2}; }}
.n {{ display:inline-block; width:96px; height:96px; border-radius:50%; font-family:FR; font-size:56px; line-height:96px; color:#0b171b;
  background:linear-gradient(160deg, #fbe3a1, {GOLD} 55%, #b8891f); box-shadow:0 0 40px rgba(233,185,73,.45), 0 12px 30px rgba(0,0,0,.5); }}
.ar {{ font-family:AM; direction:rtl; font-size:104px; line-height:1.6; margin-top:14px; color:{CREAM}; text-shadow:0 8px 30px rgba(0,0,0,.6); }}
.ar b {{ color:{GOLD}; text-shadow:0 0 40px rgba(233,185,73,.6); }} .ar.big {{ font-size:118px; line-height:1.55; }}
.en {{ font-family:IS; font-size:62px; line-height:1.1; }} .en b {{ font-weight:400; color:{GOLD}; font-style:italic; }}
.ref {{ font-family:FR; font-size:26px; letter-spacing:.2em; color:{GOLD2}; margin-top:18px; }}
.p {{ margin:34px auto 0; max-width:860px; padding:28px 36px; border-radius:30px; font-family:IS; font-size:46px; line-height:1.18; color:rgba(241,236,224,.92);
  background:linear-gradient(165deg, rgba(11,23,27,.72), rgba(11,23,27,.5)); border:1.5px solid rgba(233,185,73,.35); backdrop-filter:blur(6px); }}
.p b {{ font-weight:400; color:{GOLD}; }} .p i {{ color:{GOLD2}; }}
.why {{ font-family:IS; font-style:italic; font-size:84px; color:{GOLD2}; }}
.q {{ margin-top:60px; }} .opts {{ display:flex; justify-content:center; gap:22px; margin-top:54px; }}
.opts span {{ padding:20px 30px; border-radius:26px; font-family:FR; font-size:44px; color:#0b171b; background:linear-gradient(160deg, #fbe3a1, {GOLD});
  box-shadow:0 14px 34px rgba(0,0,0,.45); }} .opts i {{ font-style:normal; font-family:IS; font-size:44px; }}
"""
def page(n):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<svg class="bg" viewBox="0 0 1080 1350">{DEFS}{SCENES[n]}<rect width="1080" height="1350" fill="url(#vig)"/><rect width="1080" height="1350" filter="url(#grain)"/></svg>
<div class="top"><span><b>RAFIQ</b> · ARABIC</span><span>{n} / {N}</span></div><div class="c">{SLIDES[n]}</div></body></html>"""

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium" if os.path.exists("/opt/pw-browsers/chromium") else None)
        p = b.new_page(viewport={"width": 1080, "height": 1350})
        for n in range(1, N + 1):
            tmp = os.path.join(OUT, f".s{n}.html"); open(tmp, "w").write(page(n))
            p.goto("file://" + tmp); p.evaluate("document.fonts.ready.then(() => 0)"); p.wait_for_timeout(300)
            p.screenshot(path=os.path.join(OUT, f"jamil-{n}.png")); os.remove(tmp)
        b.close()
    print(OUT)
