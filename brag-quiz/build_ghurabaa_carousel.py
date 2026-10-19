"""Carousel: the strangers hadith and the root غ ر ب (owner, 19 Oct 2026). Format "one important word traced to its root".
Hook (TypeSafe, tools/typesafe-exp/ghurabaa_hook.py: the three tied at 8.0/9; the question kept, question hooks hold best).
Hadith: Sahih Muslim 145 (the plain wording, without the later "who are the strangers?" additions); Bukhari 6416.
For the teacher: the word-by-word glosses and "غَرَبَ: to go away; the sun set".

  python3 brag-quiz/build_ghurabaa_carousel.py   ->  brag-quiz/stills/ghurabaa/ghurabaa-1.png ... -7.png
"""
import os
from playwright.sync_api import sync_playwright
import build_salah_numbers as S
import build_questions_carousel as QC

R, G, T = S.RED, S.GOLD, S.TEAL
CSS = QC.CSS + f"""
.hk {{ position:absolute; top:250px; left:60px; right:60px; text-align:center; font-family:"Instrument Serif"; font-size:104px; line-height:1.04; }}
.pair {{ position:absolute; top:760px; left:0; right:0; display:flex; justify-content:center; gap:90px; direction:rtl; }}
.pair div {{ text-align:center; }} .pair b {{ display:block; font-family:"Plex Arabic"; font-size:150px; line-height:1.25; color:{R}; }}
.pair span {{ display:block; margin-top:22px; font-family:"JetBrains Mono"; font-size:30px; color:#4f6163; }}
.lab {{ position:absolute; top:170px; left:0; right:0; text-align:center; font-family:"JetBrains Mono"; font-size:28px; letter-spacing:.16em; color:#4f6163; }}
.had {{ position:absolute; top:270px; left:70px; right:70px; text-align:center; font-family:"Plex Arabic"; font-weight:700; font-size:84px; line-height:1.6; direction:rtl; }}
.had i {{ font-style:normal; color:{R}; }}
.hen {{ position:absolute; top:850px; left:90px; right:90px; text-align:center; font-family:"Instrument Serif"; font-style:italic; font-size:56px; line-height:1.15; }}
.ref {{ position:absolute; top:1150px; left:0; right:0; text-align:center; font-family:"JetBrains Mono"; font-size:30px; letter-spacing:.12em; color:{T}; font-weight:700; }}
.wbw {{ position:absolute; top:260px; left:50px; right:50px; display:flex; flex-wrap:wrap; flex-direction:row-reverse; justify-content:center; gap:22px; }}
.wbw div {{ background:rgba(23,38,43,.05); border-radius:22px; padding:18px 22px; text-align:center; min-width:250px; }}
.wbw div.k {{ background:{R}; color:#fff; }} .wbw div.k span {{ color:#fde; }}
.wbw b {{ display:block; font-family:"Plex Arabic"; font-size:70px; line-height:1.45; direction:rtl; }}
.wbw span {{ font-family:"Instrument Serif"; font-size:40px; color:#4f6163; }}
.rt {{ position:absolute; top:300px; left:0; right:0; text-align:center; font-family:"Plex Arabic"; font-size:260px; color:{R}; direction:rtl; letter-spacing:.12em; }}
.rm {{ position:absolute; top:760px; left:80px; right:80px; text-align:center; font-family:"Instrument Serif"; font-size:78px; line-height:1.1; }}
.rs {{ position:absolute; top:1040px; left:110px; right:110px; text-align:center; font-size:36px; font-weight:700; color:{T}; }}
.fam {{ position:absolute; top:250px; left:70px; right:70px; display:grid; gap:20px; }}
.fam div {{ display:flex; align-items:center; justify-content:space-between; background:rgba(23,38,43,.05); border-radius:22px; padding:14px 34px; }}
.fam b {{ font-family:"Plex Arabic"; font-size:76px; line-height:1.4; color:{R}; direction:rtl; }}
.fam span {{ font-family:"Instrument Serif"; font-size:46px; text-align:left; }} .fam small {{ display:block; font-family:"JetBrains Mono"; font-size:24px; color:#6b7a7c; }}
.tie {{ position:absolute; top:1060px; left:80px; right:80px; text-align:center; font-family:"Instrument Serif"; font-size:60px; line-height:1.1; }}
"""
FAM = [("غَرَبَ", "the sun set", "gharaba"), ("الْمَغْرِب", "Maghrib, the sunset prayer", "al-maghrib"), ("غَرْب", "west", "gharb"),
       ("غَرِيب", "a stranger, far from home", "gharīb"), ("غُرْبَة", "being away from home", "ghurbah"), ("غُرَباء", "strangers", "ghurabā'")]
WBW = [("بَدَأَ", "began"), ("الإِسْلامُ", "Islam"), ("غَرِيبًا", "as a stranger", 1), ("وَسَيَعُودُ", "and it will return"),
       ("كَما بَدَأَ", "as it began"), ("غَرِيبًا", "a stranger", 1), ("فَطُوبى", "so glad tidings"), ("لِلْغُرَباءِ", "to the strangers", 1)]

def slides():
    B = S.BRAND
    return {
     "1": f'<body>{B}<div class="hk">What does a <i style="color:{R};font-style:normal">stranger</i><br>have to do with<br>Maghrib? 🌅</div>'
          '<div class="pair"><div><b>غَرِيب</b><span>gharīb · stranger</span></div><div><b>الْمَغْرِب</b><span>al-maghrib · sunset</span></div></div>'
          '<div class="cs" style="top:1180px">SWIPE →</div></body>',
     "2": f'<body>{B}<div class="lab">THE PROPHET (PBUH) SAID</div><div class="had">بَدَأَ الإِسْلامُ <i>غَرِيبًا</i>، وَسَيَعُودُ كَما بَدَأَ <i>غَرِيبًا</i>، فَطُوبى <i>لِلْغُرَباءِ</i></div>'
          '<div class="hen">“Islam began as something strange, and it will return to being strange as it began, so glad tidings to the strangers.”</div>'
          '<div class="ref">SAHIH MUSLIM 145</div></body>',
     "3": f'<body>{B}<div class="lab">WORD BY WORD</div><div class="wbw">' +
          "".join(f'<div class="{"k" if len(w) > 2 else ""}"><b>{w[0]}</b><span>{w[1]}</span></div>' for w in WBW) + '</div></body>',
     "4": f'<body>{B}<div class="lab">THE ROOT</div><div class="rt">غ ر ب</div>'
          '<div class="rm">to go away,<br>like the sun when it <i style="color:#C8372D">sets</i></div>'
          '<div class="rs">A غَرِيب is someone who has gone far from home.</div></body>',
     "5": f'<body>{B}<div class="lab">ONE ROOT, ONE FAMILY</div><div class="fam">' +
          "".join(f'<div><span>{e}<small>{t}</small></span><b>{a}</b></div>' for a, e, t in FAM) + '</div></body>',
     "6": f'<body>{B}<div class="lab">AND HE (PBUH) SAID</div><div class="had" style="top:300px">كُنْ فِي الدُّنْيا كَأَنَّكَ <i>غَرِيبٌ</i> أَوْ عابِرُ سَبِيلٍ</div>'
          '<div class="hen" style="top:640px">“Be in this world as if you were a stranger or a traveller.”</div>'
          '<div class="ref" style="top:860px">SAHIH AL-BUKHARI 6416</div>'
          '<div class="tie">A stranger is far from home.<br>Our home is somewhere else. 🤍</div></body>',
     "7": f'<body class="dark">{B}<div class="endq">Did you know<br>Maghrib and <i>stranger</i><br>were family? 👇</div>'
          '<div class="ends"><div>Save this 📌 for later</div><div>Send it to someone who feels like a stranger</div></div></body>'}

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
    print("7 slides")
