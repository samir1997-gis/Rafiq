"""Carousel: the strangers hadith and the root غ ر ب (owner, 19 Oct 2026; v2 in the owner's order and hook).
1 ISLAM IS SO STRANGE! · 2 the hadith (Sahih Muslim 145, plain wording) · 3 غُرَباء = strangers · 4 the root · 5 other words from it ·
6 Bukhari 6416 above "Comment below if you're a stranger".
Hook: tools/typesafe-exp/ghurabaa_hook2.py (alone: respect 1.62/3; with the line pointing to the hadith 2.10, swipe up too, so kept).
Layout (the apple-design skill): one focal element per slide, centred in one frame that every slide shares (brand, label, counter
always in the same place); hierarchy from size and weight; tight leading and slight negative tracking on display text, open tracking
on small labels; one accent colour, only on the word that matters; spacing on an 8 px grid.
For the teacher: the glosses and "غ ر ب: to go away; the sun set".

  python3 brag-quiz/build_ghurabaa_carousel.py   ->  brag-quiz/stills/ghurabaa/ghurabaa-1.png ... -6.png
"""
import os
from playwright.sync_api import sync_playwright
import build_salah_numbers as S

GOLD, MUTE = "#E9B949", "#5c6e70"
CSS = S.CSS + f"""
@font-face {{ font-family:"Anton"; src:url("file://{os.path.join(S.HERE, "fonts", "anton-latin-400-normal.woff2")}"); }}
.frame {{ position:absolute; inset:0; padding:160px 96px 88px; display:flex; flex-direction:column; align-items:center; text-align:center; }}
.lab {{ font-family:"JetBrains Mono"; font-size:26px; letter-spacing:.18em; color:{MUTE}; text-transform:uppercase; height:40px; }}
.dark .lab {{ color:rgba(241,236,224,.55); }}
.main {{ flex:1; width:100%; display:flex; flex-direction:column; justify-content:center; align-items:center; gap:40px; }}
.foot {{ font-family:"JetBrains Mono"; font-size:24px; letter-spacing:.18em; color:{MUTE}; height:32px; }}
.dark .foot {{ color:{GOLD}; font-family:"Karla"; font-weight:700; font-size:36px; letter-spacing:0; }}
.arb {{ font-family:"Plex Arabic"; font-weight:700; direction:rtl; }}
.acc {{ color:{S.RED}; }} .dark .acc {{ color:{GOLD}; }}
.disp {{ font-family:"Instrument Serif"; line-height:1.0; letter-spacing:-.02em; }}
.it {{ font-family:"Instrument Serif"; font-style:italic; line-height:1.2; }}
.mono {{ font-family:"JetBrains Mono"; font-size:30px; letter-spacing:.06em; color:{MUTE}; }}
.rule {{ width:64px; height:4px; border-radius:2px; background:{S.RED}; opacity:.8; }}
.hook {{ font-family:"Anton"; font-size:184px; line-height:.92; letter-spacing:-.005em; text-transform:uppercase; }}
.rows {{ width:100%; display:flex; flex-direction:column; }}
.row {{ display:flex; align-items:center; justify-content:space-between; padding:22px 8px; border-bottom:2px solid rgba(23,38,43,.10); }}
.row:last-child {{ border-bottom:0; }}
.row .l {{ text-align:left; }} .row .l b {{ display:block; font-family:"Instrument Serif"; font-weight:400; font-size:50px; line-height:1.1; letter-spacing:-.01em; }}
.row .l span {{ font-family:"JetBrains Mono"; font-size:24px; letter-spacing:.06em; color:{MUTE}; }}
.row .arb {{ font-size:84px; line-height:1.45; color:{S.RED}; }}
"""
FAM = [("غَرَبَ", "the sun set", "gharaba"), ("الْمَغْرِب", "Maghrib, the sunset prayer", "al-maghrib"), ("غَرْب", "the west", "gharb"),
       ("غَرِيب", "a stranger", "gharīb"), ("غُرْبَة", "being far from home", "ghurbah")]
N = 6

def page(k, lab, main, dark=False, foot=None):
    foot = foot if foot is not None else f"{k} / {N}"
    return f'<body class="{"dark" if dark else ""}">{S.BRAND}<div class="frame"><div class="lab">{lab}</div><div class="main">{main}</div><div class="foot">{foot}</div></div></body>'

def slides():
    return {
     "1": page(1, "", '<div class="hook">Islam is<br>so <span class="acc">strange!</span></div>'
                      '<div class="it" style="font-size:56px;opacity:.85">…and the Prophet <span class="arb" style="font-style:normal">ﷺ</span> said it would be.</div>',
               dark=True, foot="Swipe →"),
     "2": page(2, "The Prophet ﷺ said".replace("ﷺ", "(pbuh)"),
               '<div class="arb" style="font-size:80px;line-height:1.75">بَدَأَ الإِسْلامُ <span class="acc">غَرِيبًا</span>، وَسَيَعُودُ كَما بَدَأَ <span class="acc">غَرِيبًا</span>، فَطُوبى <span class="acc">لِلْغُرَباءِ</span></div>'
               '<div class="rule"></div>'
               '<div class="it" style="font-size:52px">“Islam began as something strange, and it will return to being strange as it began, so glad tidings to the strangers.”</div>'
               '<div class="mono" style="color:#2e7263;font-weight:500">SAHIH MUSLIM 145</div>'),
     "3": page(3, "The word", '<div class="arb acc" style="font-size:300px;line-height:1.3">غُرَباء</div>'
                              '<div class="mono">ghurabāʾ</div><div class="disp" style="font-size:150px">strangers</div>'
                              '<div class="it" style="font-size:44px;color:#5c6e70">One stranger: <span class="arb" style="font-style:normal">غَرِيب</span> · gharīb</div>'),
     "4": page(4, "The root", '<div class="arb acc" style="font-size:280px;line-height:1.3;letter-spacing:.14em">غ ر ب</div>'
                              '<div class="disp" style="font-size:132px">to go away</div>'
                              '<div class="it" style="font-size:52px;color:#5c6e70">like the sun when it sets 🌅<br>A stranger is someone far from home.</div>'),
     "5": page(5, "Same root", '<div class="rows">' + "".join(f'<div class="row"><div class="l"><b>{e}</b><span>{t}</span></div><div class="arb">{a}</div></div>' for a, e, t in FAM) + '</div>'),
     "6": page(6, "And he (pbuh) said",
               '<div class="arb" style="font-size:60px;line-height:1.7;white-space:nowrap">كُنْ فِي الدُّنْيا كَأَنَّكَ <span class="acc">غَرِيبٌ</span> أَوْ عابِرُ سَبِيلٍ</div>'
               '<div class="it" style="font-size:46px;opacity:.85">“Be in this world as if you were a stranger or a traveller.”</div>'
               '<div class="mono" style="color:rgba(241,236,224,.55)">SAHIH AL-BUKHARI 6416</div>'
               '<div style="height:24px"></div>'
               '<div class="hook" style="font-size:112px;line-height:.98">Comment below<br>if you’re a <span class="acc">stranger</span> 👇</div>',
               dark=True, foot="")}

if __name__ == "__main__":
    out = os.path.join(S.HERE, "stills", "ghurabaa"); os.makedirs(out, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=S.CHROME if os.path.exists(S.CHROME) else None)
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for k, body in slides().items():
            tmp = os.path.join(out, "_s.html"); open(tmp, "w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>{body}</html>')
            pg.goto("file://" + tmp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
            pg.screenshot(path=os.path.join(out, f"ghurabaa-{k}.png"))
        os.remove(os.path.join(out, "_s.html")); b.close()
    print(N, "slides")
