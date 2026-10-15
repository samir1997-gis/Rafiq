"""The 20 words card (owner, 15 Oct 2026): what the salah reel promised in the DMs ("drop a comment and I'll DM you"). The app's own
top 20 (build_salah_numbers.TOP: 56% of a four-rakah prayer), grouped by where you say them, with how often. One phone-sized
image to send as a picture, and the same page as a PDF.

  python3 brag-quiz/build_twenty_card.py   ->  brag-quiz/stills/twenty-words.png, twenty-words.pdf
"""
import os
from playwright.sync_api import sync_playwright
import build_salah_numbers as S

TOP = S.TOP                                                          # the app's own words (its vowel-mark order), by rank
TR = ["subḥāna", "rabbiya", "Allāhu", "al-aʿlā", "akbar", "al-ʿaẓīm", "Allāhi", "ar-Raḥmān", "ar-Raḥīm", "al-ḥamdu", "rabbi", "lillāhi",
      "as-salāmu", "bismi", "al-ʿālamīn", "māliki", "yawmi", "ad-dīn", "naʿbudu", "nastaʿīn"]
assert [w["en"] for w in TOP[:3]] == ["Glory be to", "my Lord", "Allah"] and TOP[19]["en"] == "we ask for help", "the ranking changed"
GROUPS = [("In rukūʿ and sujūd", [0, 1, 5, 3]),                         # where you say them, in prayer order
          ("Every takbīr", [2, 4]),
          ("Al-Fātiḥah", [13, 6, 7, 8, 9, 11, 10, 14, 15, 16, 17, 18, 19]),
          ("Ending the prayer", [12])]
assert sorted(i for _, ws in GROUPS for i in ws) == list(range(20)), "every top-20 word once"

CSS = S.CSS.replace("height:1350px", "height:1920px") + f"""
h1 {{ position:absolute; top:150px; left:60px; right:60px; margin:0; text-align:center; font-family:"Instrument Serif"; font-weight:400;
  font-size:76px; line-height:1.02; }} h1 i {{ color:{S.GOLD}; }}
.wsub {{ position:absolute; top:330px; left:60px; right:60px; text-align:center; font-size:30px; color:#4f6163; }}
.wl {{ position:absolute; top:395px; left:56px; right:56px; }}
.wg {{ font-family:"JetBrains Mono"; font-size:22px; letter-spacing:.14em; text-transform:uppercase; color:{S.TEAL}; margin:14px 0 2px; }}
.wr {{ display:flex; align-items:center; height:50px; border-bottom:1.5px solid rgba(23,38,43,.08); }}
.wr .n {{ width:46px; font-family:"JetBrains Mono"; font-size:22px; color:#8a9698; }}
.wr .en {{ flex:1; white-space:nowrap; font-size:29px; font-weight:700; line-height:1; }} .wr .en small {{ display:block; font-size:21px; font-weight:500; color:#6b7a7c; margin-top:3px; }}
.wr .x {{ width:84px; text-align:center; font-family:"JetBrains Mono"; font-size:21px; color:{S.RED}; }}
.wr .ar {{ width:250px; text-align:right; font-family:"Plex Arabic"; font-weight:700; font-size:42px; line-height:1; direction:rtl; }}
.wtip {{ position:absolute; bottom:172px; left:56px; right:56px; padding:22px 28px; border-radius:22px; background:rgba(46,114,99,.12);
  font-size:27px; line-height:1.3; }} .wtip b {{ color:{S.TEAL}; }}
.wcta {{ position:absolute; bottom:34px; left:56px; right:56px; text-align:center; font-size:26px; line-height:1.35; }} .wcta b {{ color:{S.RED}; }}
.wcta span {{ font-family:"JetBrains Mono"; font-size:23px; color:#4f6163; }}
"""

def page():
    rows, k = "", 0
    for g, ws in GROUPS:
        rows += f'<div class="wg">{g}</div>'
        for i in ws:
            k += 1; w = TOP[i]
            rows += (f'<div class="wr"><div class="n">{k:02d}</div><div class="en">{S.e(w["en"])}<small>{TR[i]}</small></div>'
                     f'<div class="x">×{w["n"]}</div><div class="ar">{w["ar"]}</div></div>')
    return (f'<body>{S.BRAND}<h1>The 20 words that make up<br><i>over half of your salah</i></h1>'
            f'<div class="wsub">{S.pct(S.TOP)}% of every word in a 4-rakʿah prayer · ×N = times you say it</div>'
            f'<div class="wl">{rows}</div>'
            '<div class="wtip"><b>Start with the first four.</b> Think of their meaning in your next rukūʿ and sujūd: '
            'subḥāna rabbiya alone comes 36 times in one prayer, so you’ll feel it straight away, in shā’ Allāh 🤲</div>'
            '<div class="wcta"><b>Learn it properly with Rafiq:</b> your whole salah, every short surah, and everyday Arabic.<br>'
            '<span>rafiq-arabic.com · free for a week, no card needed</span></div></body>')

if __name__ == "__main__":
    out = os.path.join(S.HERE, "stills"); os.makedirs(out, exist_ok=True)
    tmp = os.path.join(out, "_twenty.html")
    open(tmp, "w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>{page()}</html>')
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=S.CHROME if os.path.exists(S.CHROME) else None)
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto("file://" + tmp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
        pg.screenshot(path=os.path.join(out, "twenty-words.png"))
        pg.pdf(path=os.path.join(out, "twenty-words.pdf"), width="1080px", height="1920px", print_background=True)
        b.close()
    os.remove(tmp); print("twenty-words.png, twenty-words.pdf")
