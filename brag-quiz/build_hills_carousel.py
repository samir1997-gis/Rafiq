"""Carousel: Signs in the hills (#375, owner 15 Nov 2026). The owner's own photos from Kinder Scout, five verses, one Qur'an word on each
slide in gold with its meaning (the Rafiq part). Cover line chosen with TypeSafe (tools/typesafe-exp/hills_carousel.py, 5.25 of 6).
The photos show the owner's friends and the repo is public: they're read from a folder outside it, and the slides go to Drive.

  python3 brag-quiz/build_hills_carousel.py PHOTOS OUT      (PHOTOS: sunrise, path, clouds, hail, group .jpg)  ->  OUT/hills-1..6.png
"""
import os, sys
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); F = os.path.join(HERE, "fonts")
PHOTOS, OUT = sys.argv[1:3]
GOLD, CREAM, INK, TEAL = "#E9B949", "#F1ECE0", "#17262B", "#14232a"

# (photo, focus (background-position), verse with the word in [[ ]], the word, its sound, its meaning, translation, source)
SLIDES = [
 ("sunrise", "60% 50%", "إِنَّ فِي خَلْقِ السَّمَاوَاتِ وَالْأَرْضِ وَاخْتِلَافِ اللَّيْلِ وَالنَّهَارِ [[لَآيَاتٍ]] لِأُولِي الْأَلْبَابِ",
  "آيات", "āyāt", "signs (and the verses of the Qur'an)",
  "In the creation of the heavens and the earth, and the alternation of night and day, are signs for people of understanding.", "ĀL ʿIMRĀN · 3:190"),
 ("path", "55% 40%", "اهْدِنَا [[الصِّرَاطَ]] الْمُسْتَقِيمَ", "الصِّراط", "aṣ-ṣirāṭ", "the path", "Guide us to the straight path.", "AL-FĀTIḤAH · 1:6"),
 ("clouds", "30% 40%", "وَتَرَى [[الْجِبَالَ]] تَحْسَبُهَا جَامِدَةً وَهِيَ تَمُرُّ مَرَّ السَّحَابِ", "الجِبال", "al-jibāl", "the mountains (one: جَبَل)",
  "You see the mountains and think them firmly fixed, while they move as the clouds move.", "AN-NAML · 27:88"),
 ("hail", "45% 45%", "إِنَّ مَعَ الْعُسْرِ [[يُسْرًا]]", "يُسْر", "yusr", "ease", "Indeed, with hardship comes ease.", "ASH-SHARḤ · 94:6"),
 ("group", "50% 60%", "وَاعْتَصِمُوا [[بِحَبْلِ]] اللَّهِ جَمِيعًا وَلَا تَفَرَّقُوا", "حَبْل", "ḥabl", "rope",
  "Hold firmly to the rope of Allah, all together, and do not be divided.", "ĀL ʿIMRĀN · 3:103"),
]
N = len(SLIDES) + 1
COVER = "5 Qur'an words I couldn't stop thinking about on <b>Kinder Scout</b>"

CSS = f"""
@font-face {{ font-family:AM; src:url("file://{F}/amiri-arabic-700-normal.woff2"); }}
@font-face {{ font-family:IS; src:url("file://{F}/instrument-serif-latin-400-normal.woff2"); }}
@font-face {{ font-family:FR; src:url("file://{F}/fredoka-latin-600-normal.woff2"); }}
* {{ margin:0; box-sizing:border-box; }} body {{ width:1080px; height:1350px; overflow:hidden; position:relative; background:{TEAL}; color:{CREAM}; }}
.ph {{ position:absolute; inset:0; background-size:cover; filter:saturate(1.05) contrast(1.04); }}
.shade {{ position:absolute; inset:0; background:linear-gradient(180deg, rgba(8,16,20,.72) 0%, rgba(8,16,20,.25) 34%, rgba(8,16,20,.1) 52%, rgba(8,16,20,.55) 74%, rgba(8,16,20,.88) 100%); }}
.grain {{ position:absolute; inset:0; opacity:.13; mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/></filter><rect width='300' height='300' filter='url(%23n)'/></svg>"); }}
.top, .foot {{ position:absolute; left:72px; right:72px; display:flex; justify-content:space-between; align-items:center;
  font-family:FR; font-size:25px; letter-spacing:.16em; color:rgba(241,236,224,.9); }}
.top {{ top:58px; padding-bottom:20px; border-bottom:1.5px solid rgba(241,236,224,.45); }} .top b {{ color:{GOLD}; font-weight:600; }}
.foot {{ bottom:56px; padding-top:20px; border-top:1.5px solid rgba(241,236,224,.45); }}
.ar {{ position:absolute; left:70px; right:70px; top:170px; text-align:center; font-family:AM; direction:rtl; font-size:66px; line-height:1.75;
  color:{CREAM}; text-shadow:0 4px 24px rgba(0,0,0,.55); }}
.ar .w {{ color:{GOLD}; text-shadow:0 0 30px rgba(233,185,73,.55), 0 4px 24px rgba(0,0,0,.55); }}
.ar.short {{ font-size:84px; }} .ar.low {{ top:480px; font-size:50px; line-height:1.7; opacity:.95; }}
.word {{ position:absolute; left:50%; transform:translateX(-50%); bottom:330px; display:flex; align-items:center; gap:18px; white-space:nowrap;
  padding:14px 30px 14px 26px; border-radius:999px; background:rgba(14,26,30,.62); border:1.5px solid rgba(233,185,73,.7); backdrop-filter:blur(8px); }}
.word .a {{ font-family:AM; font-size:46px; line-height:1; color:{GOLD}; direction:rtl; padding-top:6px; }}
.word .t {{ font-family:FR; font-size:26px; color:{CREAM}; }} .word .t i {{ font-style:normal; opacity:.75; }}
.en {{ position:absolute; left:110px; right:110px; bottom:150px; text-align:center; font-family:IS; font-style:italic; font-size:44px; line-height:1.22;
  color:{CREAM}; text-shadow:0 2px 16px rgba(0,0,0,.6); }}
.cover {{ position:absolute; left:80px; right:80px; top:150px; text-align:center; }}
.cover h1 {{ font-family:IS; font-weight:400; font-size:84px; line-height:1.04; text-shadow:0 4px 30px rgba(0,0,0,.6); }} .cover h1 b {{ font-weight:400; color:{GOLD}; font-style:italic; }}
.cover .ar5 {{ margin-top:34px; font-family:AM; font-size:44px; direction:rtl; color:{GOLD}; letter-spacing:.02em; text-shadow:0 2px 16px rgba(0,0,0,.6); }}
.end {{ position:absolute; left:80px; right:80px; top:190px; text-align:center; }}
.end h2 {{ font-family:IS; font-weight:400; font-size:72px; line-height:1.05; }}
.list {{ margin:44px auto 0; width:620px; }}
.row {{ display:flex; justify-content:space-between; align-items:center; padding:16px 6px; border-bottom:1px solid rgba(241,236,224,.25); }}
.row .n {{ font-family:FR; font-size:26px; color:{GOLD}; width:40px; text-align:left; }} .row .e {{ flex:1; text-align:left; font-family:IS; font-size:40px; }}
.row .a {{ font-family:AM; font-size:44px; color:{GOLD}; direction:rtl; }}
.ask {{ margin-top:46px; font-family:IS; font-style:italic; font-size:48px; }}
.site {{ display:inline-block; margin-top:28px; padding:16px 34px; border-radius:999px; background:{GOLD}; color:{INK}; font-family:FR; font-size:30px; }}
"""
def page(body, photo=None, pos="50% 50%", dark=False):
    bg = f'<div class="ph" style="background-image:url(\'file://{PHOTOS}/{photo}.jpg\');background-position:{pos}"></div>' if photo else ""
    shade = '<div class="shade" style="background:rgba(8,16,20,.78)"></div>' if dark else '<div class="shade"></div>'
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{bg}{shade}<div class="grain"></div>{body}</body></html>'
def frame(n, right="SIGNS IN THE HILLS", left_foot="", right_foot="SWIPE →"):
    return (f'<div class="top"><span><b>RAFIQ</b> · ARABIC</span><span>{n:02d} / {N:02d}</span></div>'
            f'<div class="foot"><span>{left_foot}</span><span>{right_foot}</span></div>')

def slides():
    out = []
    for i, (ph, pos, ar, w, tr, mean, en, src) in enumerate(SLIDES):     # the first is also the cover: the hook above its verse
        a = ar.replace("[[", '<span class="w">').replace("]]", "</span>")
        hook = f'<div class="cover"><h1>{COVER}</h1></div>' if i == 0 else ""
        body = (frame(i + 1, left_foot=src) + hook + f'<div class="ar{" short" if len(ar) < 40 else ""}{" low" if i == 0 else ""}">{a}</div>'
                f'<div class="word"><span class="a">{w}</span><span class="t">{tr} <i>· {mean}</i></span></div><div class="en">{en}</div>')
        out.append(page(body, ph, pos))
    rows = "".join(f'<div class="row"><span class="n">{i + 1}</span><span class="e">{s[5].split(" (")[0]}</span><span class="a">{s[3]}</span></div>' for i, s in enumerate(SLIDES))
    out.append(page(frame(N, left_foot="SIGNS IN THE HILLS", right_foot="SAVE FOR YOUR NEXT WALK") +
                    f'<div class="end"><h2>Five words from one hike</h2><div class="list">{rows}</div>'
                    f'<div class="ask">Which verse would you take up a mountain? 1 to 5 👇</div><div class="site">Learn the Qur\'an\'s words: rafiq-arabic.com</div></div>',
                    "group", "50% 50%", dark=True))
    return out

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium" if os.path.exists("/opt/pw-browsers/chromium") else None)
        p = b.new_page(viewport={"width": 1080, "height": 1350})
        for i, html in enumerate(slides(), 1):
            tmp = os.path.join(OUT, f".s{i}.html"); open(tmp, "w").write(html)
            p.goto("file://" + tmp); p.evaluate("document.fonts.ready.then(() => 0)"); p.wait_for_timeout(400)
            p.screenshot(path=os.path.join(OUT, f"hills-{i}.png")); os.remove(tmp)
        b.close()
    print(OUT)
