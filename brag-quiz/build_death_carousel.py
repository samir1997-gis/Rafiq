"""Carousel: remember death (owner, 8 Nov 2026, from a reference post: an open grave, "REMEMBER", one line in a serif).
1 REMEMBER: "Your death will come on an ordinary day…" over a drawn open grave (grass edges, a spade) · 2 the only thing you take with you
is your deeds, and the hadith (al-Bukhārī 6514, Muslim 2960) · 3 so make the effort while you have time: learn Arabic, connect with Allah ·
4 rafiq-arabic.com, start your Arabic journey (a free week).
Style: the ghurabāʾ carousel's frame (brand, label, counter always in the same place), Instrument Serif for the lines, one accent colour.

  python3 brag-quiz/build_death_carousel.py   ->  brag-quiz/stills/remember/remember-1.png ... -4.png
"""
import os
from playwright.sync_api import sync_playwright
import build_salah_numbers as S
import build_ghurabaa_carousel as G

N = 4
GRAVE = """<svg class="bg" viewBox="0 0 1080 1350" preserveAspectRatio="xMidYMid slice"><defs>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.75" numOctaves="3" seed="7"/>
<feColorMatrix values="0 0 0 0 0.08  0 0 0 0 0.05  0 0 0 0 0.02  0 0 0 2.2 -0.85"/></filter>
<filter id="blades" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.035 0.45" numOctaves="3" seed="3"/>
<feColorMatrix values="0 0 0 0 0.62  0 0 0 0 0.80  0 0 0 0 0.35  0 0 0 2.4 -1.0"/></filter>
<filter id="dark" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.05 0.3" numOctaves="2" seed="9"/>
<feColorMatrix values="0 0 0 0 0.05  0 0 0 0 0.12  0 0 0 0 0.03  0 0 0 2 -0.8"/></filter>
<filter id="blur"><feGaussianBlur stdDeviation="14"/></filter>
<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3b2516"/><stop offset=".5" stop-color="#5a3b23"/><stop offset="1" stop-color="#6b4629"/></linearGradient>
<linearGradient id="wallL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6e4a2c"/><stop offset="1" stop-color="#2b1a0e"/></linearGradient>
<linearGradient id="wallR" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#5a3c22"/><stop offset="1" stop-color="#1f130a"/></linearGradient>
<linearGradient id="wallT" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a0f07"/><stop offset="1" stop-color="#3a2415"/></linearGradient>
<radialGradient id="vig" cx=".5" cy=".55" r=".8"><stop offset=".5" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".6"/></radialGradient>
<linearGradient id="steel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#cfc9be"/><stop offset=".5" stop-color="#8d877d"/><stop offset="1" stop-color="#4a463f"/></linearGradient>
<linearGradient id="wood" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#c49a66"/><stop offset="1" stop-color="#7d5a35"/></linearGradient></defs>
<rect width="1080" height="1350" fill="#4c7d2e"/><rect width="1080" height="1350" filter="url(#dark)"/><rect width="1080" height="1350" filter="url(#blades)"/>
<path d="M200 60 C 520 30 880 50 960 90 L 1010 1350 L 110 1350 Z" fill="#1a0f07" filter="url(#blur)" opacity=".8"/>
<path d="M230 80 C 520 52 860 70 930 104 L 980 1350 L 140 1350 Z" fill="url(#wallT)"/>
<path d="M230 80 L 380 300 L 330 1350 L 140 1350 Z" fill="url(#wallL)"/>
<path d="M930 104 L 790 310 L 830 1350 L 980 1350 Z" fill="url(#wallR)"/>
<path d="M380 300 C 520 288 690 292 790 310 L 830 1350 L 330 1350 Z" fill="url(#floor)"/>
<path d="M230 80 C 520 52 860 70 930 104 L 980 1350 L 140 1350 Z" filter="url(#grain)"/>
<path d="M230 80 C 520 52 860 70 930 104" stroke="#6f9f45" stroke-width="22" fill="none" stroke-linecap="round" opacity=".55"/>
<path d="M230 80 L 140 1350 M930 104 L 980 1350" stroke="#6f9f45" stroke-width="16" fill="none" opacity=".35"/>

<g transform="translate(800 -40) rotate(-4) scale(0.8)"><rect x="0" y="0" width="20" height="440" rx="8" fill="url(#wood)"/>
<path d="M-42 440 L 62 440 L 56 570 C 40 615 -20 615 -36 570 Z" fill="url(#steel)"/><ellipse cx="10" cy="610" rx="70" ry="14" fill="#000" opacity=".35"/></g>
<rect width="1080" height="1350" fill="url(#vig)"/><rect width="1080" height="1350" fill="#000" opacity=".18"/></svg>"""
CSS = G.CSS + f"""
.bg {{ position:absolute; inset:0; width:100%; height:100%; }}
.grave .lab, .grave .foot {{ color:{G.GOLD}; }}
.rem {{ font-family:"Anton"; font-size:150px; line-height:1; letter-spacing:.06em; color:{G.GOLD}; margin-bottom:-12px;
  text-shadow:0 0 40px rgba(233,185,73,.45), 0 6px 30px rgba(0,0,0,.8); }}
.bg {{ object-fit:cover; }}
.line {{ font-family:"Instrument Serif"; font-size:84px; line-height:1.12; letter-spacing:-.01em; color:#F1ECE0; text-shadow:0 4px 30px rgba(0,0,0,.6); }}
.goldrule {{ width:220px; height:4px; border-radius:2px; background:{G.GOLD}; }}
.big {{ font-family:"Instrument Serif"; line-height:1.04; letter-spacing:-.02em; }}
.stps {{ width:100%; display:flex; flex-direction:column; gap:14px; }} .stp {{ display:flex; align-items:center; gap:26px; padding:14px 26px; border-radius:28px; background:#fbf7ef; border:3px solid rgba(23,38,43,.08); text-align:left; }}
.sic svg {{ width:96px; height:96px; display:block; }} .stx {{ font-family:"Instrument Serif"; font-size:48px; line-height:1.05; }} .stx b {{ font-weight:400; color:{S.RED}; }}
.cta {{ display:inline-block; padding:22px 54px; border-radius:60px; background:{G.GOLD}; color:#17262B; font-family:"Karla"; font-weight:800; font-size:56px; }}
"""

# slide 2: the hadith drawn: a janāzah carried to the grave; behind it his family, his wealth and his deeds; two turn back, one goes on
INK, CREAM = "#17262B", "#F1ECE0"
def person(x, y, s, c, back=False):          # faceless, standing; back: turned, walking away
    return (f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="4" rx="34" ry="7" fill="#000" opacity=".12"/>'
            f'<path d="M-28 0 L-22 -88 C-20 -112 20 -112 22 -88 L28 0 Z" fill="{c}"/><circle cx="0" cy="-126" r="22" fill="{c}"/>'
            + (f'<path d="M-6 -60 L-40 -40" stroke="{c}" stroke-width="12" stroke-linecap="round"/>' if back else "") + '</g>')
FOLLOW = f"""<svg viewBox="0 0 1000 520" style="width:940px;height:489px">
<defs><radialGradient id="lg"><stop offset="0" stop-color="#ffe9a8"/><stop offset=".45" stop-color="#E9B949" stop-opacity=".55"/><stop offset="1" stop-color="#E9B949" stop-opacity="0"/></radialGradient>
<linearGradient id="mound" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a6a4a"/><stop offset="1" stop-color="#5e4530"/></linearGradient>
<marker id="ah" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="#9aa5a6"/></marker></defs>
<path d="M0 420 C 260 404 640 414 1000 396" stroke="#d8cfbd" stroke-width="7" fill="none"/>
<path d="M830 414 C 852 320 978 320 1000 414 Z" fill="url(#mound)"/><rect x="905" y="292" width="18" height="80" rx="7" fill="#6b5a48"/>
<g transform="translate(690 404)">{person(-62, 6, 1.0, INK)}{person(62, 6, 1.0, INK)}
<path d="M-80 -86 L-70 -176 M-44 -86 L-54 -176 M44 -86 L54 -176 M80 -86 L70 -176" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>
<rect x="-120" y="-196" width="240" height="26" rx="12" fill="#efe8d8" stroke="{INK}" stroke-width="4"/>
<path d="M-104 -196 C -70 -250 70 -250 104 -196 Z" fill="#fbf7ef" stroke="{INK}" stroke-width="4"/></g>
<circle cx="510" cy="300" r="140" fill="url(#lg)"/>
<g transform="translate(510 360) scale(1.5)"><path d="M-20 -70 H20 M-12 -70 V-82 H12 V-70" stroke="#a8842c" stroke-width="5" fill="none"/>
<path d="M-26 -70 L-32 -10 H32 L26 -70 Z" fill="#E9B949" stroke="#a8842c" stroke-width="4"/><path d="M-14 -58 L-17 -20 H17 L14 -58 Z" fill="#fff6d6"/>
<path d="M-34 -10 H34 V0 H-34 Z" fill="#a8842c"/></g>
<text x="510" y="478" text-anchor="middle" font-family="Instrument Serif" font-size="50" fill="{S.RED}">his deeds</text>
<text x="690" y="478" text-anchor="middle" font-family="Instrument Serif" font-size="40" fill="{INK}">the janāzah</text>
<g opacity=".4">{person(300, 414, 1.05, INK, True)}{person(366, 416, 0.85, INK, True)}
<g transform="translate(120 404) scale(1.3)"><ellipse cx="0" cy="0" rx="46" ry="12" fill="#a8842c"/><path d="M-40 0 C -46 -60 46 -60 40 0 Z" fill="#c9a24a"/>
<path d="M-12 -46 C -6 -60 6 -60 12 -46" stroke="#7d6020" stroke-width="5" fill="none"/><text x="0" y="-12" text-anchor="middle" font-family="Karla" font-weight="800" font-size="30" fill="#7d6020">£</text>
<circle cx="54" cy="-6" r="12" fill="#E9B949"/><circle cx="70" cy="0" r="10" fill="#E9B949"/></g></g>
<path d="M380 200 C 340 150 270 150 240 200" stroke="#9aa5a6" stroke-width="6" fill="none" marker-end="url(#ah)" stroke-dasharray="12 9"/>
<path d="M190 230 C 160 185 100 185 70 230" stroke="#9aa5a6" stroke-width="6" fill="none" marker-end="url(#ah)" stroke-dasharray="12 9"/>
<text x="330" y="478" text-anchor="middle" font-family="Instrument Serif" font-size="40" fill="#7f8b8c">his family</text>
<text x="130" y="478" text-anchor="middle" font-family="Instrument Serif" font-size="40" fill="#7f8b8c">his wealth</text>
<text x="225" y="130" text-anchor="middle" font-family="JetBrains Mono" font-size="24" letter-spacing="3" fill="#9aa5a6">TWO TURN BACK</text>
<text x="530" y="150" text-anchor="middle" font-family="JetBrains Mono" font-size="24" letter-spacing="3" fill="#a8842c">ONE STAYS</text></svg>"""

# slide 3: an hourglass running low, then the three steps, each drawn
HOURGLASS = f"""<svg viewBox="0 0 300 330" style="width:250px;height:275px">
<defs><linearGradient id="gl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset=".5" stop-color="#fff" stop-opacity=".15"/><stop offset="1" stop-color="#fff" stop-opacity=".45"/></linearGradient>
<linearGradient id="sand" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E9B949"/><stop offset="1" stop-color="#c9902e"/></linearGradient></defs>
<rect x="40" y="10" width="220" height="22" rx="10" fill="#6b4a2a"/><rect x="40" y="298" width="220" height="22" rx="10" fill="#6b4a2a"/>
<rect x="52" y="30" width="12" height="270" fill="#8a6a44"/><rect x="236" y="30" width="12" height="270" fill="#8a6a44"/>
<path d="M78 34 H222 C 222 110 160 140 156 165 C 160 190 222 220 222 296 H78 C 78 220 140 190 144 165 C 140 140 78 110 78 34 Z" fill="#e9eef0" stroke="{INK}" stroke-width="4"/>
<path d="M118 120 H182 C 172 140 158 150 152 162 H148 C 142 150 128 140 118 120 Z" fill="url(#sand)"/>
<rect x="148" y="162" width="4" height="110" fill="#E9B949"/>
<path d="M84 294 C 96 240 130 228 150 226 C 170 228 204 240 216 294 Z" fill="url(#sand)"/>
<path d="M78 34 H222 C 222 110 160 140 156 165 C 160 190 222 220 222 296 H78 C 78 220 140 190 144 165 C 140 140 78 110 78 34 Z" fill="url(#gl)"/></svg>"""
def step(icon, line, n):
    return (f'<div class="stp"><div class="sic">{icon}</div><div class="stx"><span class="mono" style="font-size:22px">STEP {n}</span><br>{line}</div></div>')
I_BOOK = f'<svg viewBox="0 0 100 100"><path d="M50 26 C38 18 22 18 12 24 V80 C22 74 38 74 50 82 C62 74 78 74 88 80 V24 C78 18 62 18 50 26 Z" fill="#fbe3d2" stroke="#e09868" stroke-width="5"/><path d="M50 26 V82" stroke="#e09868" stroke-width="5"/><text x="69" y="58" text-anchor="middle" font-family="Plex Arabic" font-weight="700" font-size="24" fill="{S.RED}">ع</text><text x="31" y="58" text-anchor="middle" font-family="Plex Arabic" font-weight="700" font-size="24" fill="{INK}">ا ب</text></svg>'
I_HANDS = '<svg viewBox="0 0 100 100"><path d="M22 92 V30 C 22 12 78 12 78 30 V92 Z" fill="#dcefe6" stroke="#6aa893" stroke-width="5" stroke-linejoin="round"/><path d="M34 82 V36 C 34 24 66 24 66 36 V82" fill="none" stroke="#6aa893" stroke-width="4"/><path d="M22 92 H78 M28 97 V92 M40 97 V92 M52 97 V92 M64 97 V92 M74 97 V92" stroke="#6aa893" stroke-width="4" stroke-linecap="round"/><circle cx="50" cy="42" r="5" fill="#6aa893"/></svg>'
I_LIGHT = '<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="18" fill="#f8ebc4" stroke="#d1a63c" stroke-width="5"/>' + "".join(f'<path d="M50 50 m{__import__("math").cos(a)*26:.1f} {__import__("math").sin(a)*26:.1f} l{__import__("math").cos(a)*14:.1f} {__import__("math").sin(a)*14:.1f}" stroke="#d1a63c" stroke-width="5" stroke-linecap="round"/>' for a in [k * 0.785 for k in range(8)]) + '</svg>'
STEPS = ('<div class="stps">' + step(I_BOOK, "Learn <b>Arabic</b>.", 1) + step(I_HANDS, "Understand what you say to <b>Allah</b>.", 2)
         + step(I_LIGHT, "Connect with <b>Him</b>.", 3) + '</div>')

def slides():
    page = G.page
    G.N = N
    one = page(1, "", '<div class="rem">REMEMBER</div><div class="goldrule"></div><div class="line">Your death will come on an ordinary day, in the middle of unfinished plans, '
                              'and the world will carry on <span style="color:' + G.GOLD + '">without you.</span></div>', dark=True, foot="Swipe →")
    one = one.replace('<body class="dark">', '<body class="dark grave"><img class="bg" src="file://' + os.path.join(S.HERE, "stills", "remember", "grave.png") + '">', 1)   # remember_grave.py
    return {
     "1": one,
     "2": page(2, "What goes with you", '<div class="big" style="font-size:88px">The only thing you’ll take with you is your <span class="acc">deeds.</span></div>'
               + FOLLOW +
               '<div class="arb" style="font-size:44px;line-height:1.8">يَتْبَعُ الْمَيِّتَ ثَلاثَةٌ… فَيَرْجِعُ أَهْلُهُ وَمالُهُ، وَيَبْقى <span class="acc">عَمَلُهُ</span></div>'
               '<div class="it" style="font-size:38px">“Three follow the dead: his family, his wealth and his deeds. His family and wealth return, and his '
               '<b style="font-style:normal;color:' + S.RED + '">deeds</b> remain.”</div><div class="mono" style="font-size:24px;color:#2e7263;margin-top:-24px">SAHIH AL-BUKHARI 6514 · SAHIH MUSLIM 2960</div>'),
     "3": page(3, "While you still have time", '<div class="big" style="font-size:96px">So make the effort while you still <span class="acc">have time.</span></div>'
               + HOURGLASS + STEPS),
     "4": page(4, "Start today", '<div class="big" style="font-size:112px;color:#F1ECE0">Kick-start your <span class="acc">Arabic</span> journey</div>'
               '<div class="it" style="font-size:52px;color:rgba(241,236,224,.85)">Understand every word of your salah, a few minutes a day.</div>'
               '<div class="cta">rafiq-arabic.com</div><div class="mono" style="color:rgba(241,236,224,.6)">FREE FOR A WEEK · LINK IN BIO</div>', dark=True, foot="")}

if __name__ == "__main__":
    out = os.path.join(S.HERE, "stills", "remember"); os.makedirs(out, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=S.CHROME if os.path.exists(S.CHROME) else None)
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for k, body in slides().items():
            tmp = os.path.join(out, "_s.html"); open(tmp, "w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>{body}</html>')
            pg.goto("file://" + tmp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
            pg.screenshot(path=os.path.join(out, f"remember-{k}.png"))
        os.remove(os.path.join(out, "_s.html")); b.close()
    print(N, "slides")
