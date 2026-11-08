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
.grave .lab, .grave .foot {{ color:{G.GOLD}; }} .grave .brand, .grave .brand * {{ color:#F1ECE0 !important; }}
.line {{ font-family:"Instrument Serif"; font-size:84px; line-height:1.12; letter-spacing:-.01em; color:#F1ECE0; text-shadow:0 4px 30px rgba(0,0,0,.6); }}
.goldrule {{ width:220px; height:4px; border-radius:2px; background:{G.GOLD}; }}
.big {{ font-family:"Instrument Serif"; line-height:1.04; letter-spacing:-.02em; }}
.cta {{ display:inline-block; padding:22px 54px; border-radius:60px; background:{G.GOLD}; color:#17262B; font-family:"Karla"; font-weight:800; font-size:56px; }}
"""

def slides():
    page = G.page
    G.N = N
    one = page(1, "Remember", '<div class="goldrule"></div><div class="line">Your death will come on an ordinary day, in the middle of unfinished plans, '
                              'and the world will carry on <span style="color:' + G.GOLD + '">without you.</span></div>', dark=True, foot="Swipe →")
    one = one.replace('<body class="dark">', '<body class="dark grave">' + GRAVE, 1)
    return {
     "1": one,
     "2": page(2, "What goes with you", '<div class="big" style="font-size:104px">The only thing you’ll take with you is your <span class="acc">deeds.</span></div>'
               '<div class="rule"></div>'
               '<div class="arb" style="font-size:54px;line-height:1.85">يَتْبَعُ الْمَيِّتَ ثَلاثَةٌ، فَيَرْجِعُ اثْنانِ وَيَبْقى مَعَهُ واحِدٌ: يَتْبَعُهُ أَهْلُهُ وَمالُهُ وَعَمَلُهُ، '
               'فَيَرْجِعُ أَهْلُهُ وَمالُهُ، وَيَبْقى <span class="acc">عَمَلُهُ</span></div>'
               '<div class="it" style="font-size:42px">“Three follow the dead: his family, his wealth and his deeds. Two return and one remains: '
               'his family and wealth return, and his <b style="font-style:normal;color:' + S.RED + '">deeds</b> remain.”</div>'
               '<div class="mono" style="color:#2e7263;font-weight:500">SAHIH AL-BUKHARI 6514 · SAHIH MUSLIM 2960</div>'),
     "3": page(3, "While you still have time", '<div class="big" style="font-size:118px">So make the effort while you still <span class="acc">have time.</span></div>'
               '<div class="rule"></div>'
               '<div class="it" style="font-size:58px;line-height:1.3">Learn Arabic.<br>Understand what you say to Allah.<br>Connect with Him.</div>'),
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
