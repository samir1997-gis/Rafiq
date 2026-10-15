"""Carousel: the question words (owner, 15 Oct 2026): who, what, where, when, why, how, how many. Slide 1 is the English words and
"Can you say all 7 in Arabic?"; then one slide per word with an example sentence, the word in red; the end asks for a score.
Words and most sentences are the course's own (toolkit-data.js "Asking"); the faith ones (مَنْ رَبُّكَ؟, the mosque, Jumuʿah, Fajr)
are written to the same pattern. Pure content (4 posts in 5): no app pitch.

  python3 brag-quiz/build_questions_carousel.py   ->  brag-quiz/stills/qw-1.png ... qw-9.png
"""
import os
from playwright.sync_api import sync_playwright
import build_salah_numbers as S

# (English, Arabic, transliteration, [(sentence, transliteration, English)], note)
W = [("who", "مَنْ", "man", [("مَنْ رَبُّكَ؟", "man rabbuka?", "Who is your Lord?")], "The first question in the grave."),
     ("what", "ما · ماذا", "mā · mādhā", [("ما اسْمُكَ؟", "mā smuka?", "What’s your name?"), ("ماذا تَفْعَلُ؟", "mādhā tafʿalu?", "What are you doing?")],
      "Two words for “what”: ما before a noun, ماذا before a verb."),
     ("where", "أَيْنَ", "ayna", [("أَيْنَ المَسْجِدُ؟", "ayna l-masjidu?", "Where is the mosque?")], ""),
     ("when", "مَتى", "matā", [("مَتى صَلاةُ الجُمُعَةِ؟", "matā ṣalātu l-jumuʿah?", "When is the Jumuʿah prayer?")], ""),
     ("why", "لِماذا", "limādhā", [("لِماذا تَدْرُسُ العَرَبِيَّةَ؟", "limādhā tadrusu l-ʿarabiyyah?", "Why do you study Arabic?")], ""),
     ("how", "كَيْفَ", "kayfa", [("كَيْفَ حالُكَ؟", "kayfa ḥāluka?", "How are you?")], ""),
     ("how many", "كَمْ", "kam", [("كَمْ رَكْعَةً فِي الفَجْرِ؟", "kam rakʿatan fi l-fajr?", "How many rakʿahs are in Fajr?")],
      "Answer it in the comments 👇")]

CSS = S.CSS + f"""
.q {{ position:absolute; left:0; right:0; text-align:center; font-weight:700; }}
.cov {{ position:absolute; top:250px; left:70px; right:70px; display:flex; flex-wrap:wrap; justify-content:center; gap:18px 30px; }}
.cov b {{ font-family:"Instrument Serif"; font-weight:400; font-size:118px; line-height:1; }} .cov b:nth-child(odd) {{ color:{S.RED}; }}
.cq {{ position:absolute; top:960px; left:60px; right:60px; text-align:center; font-family:"Instrument Serif"; font-size:84px; line-height:1.05; }}
.cs {{ position:absolute; top:1180px; left:0; right:0; text-align:center; font-family:"JetBrains Mono"; font-size:26px; letter-spacing:.14em; color:#4f6163; }}
.n {{ position:absolute; top:170px; left:0; right:0; text-align:center; font-family:"JetBrains Mono"; font-size:26px; letter-spacing:.16em; color:#4f6163; }}
.en {{ top:230px; font-family:"Instrument Serif"; font-weight:400; font-size:96px; }}
.ar {{ top:360px; font-family:"Plex Arabic"; font-size:200px; line-height:1.2; color:{S.RED}; direction:rtl; }}
.tr {{ top:610px; font-family:"JetBrains Mono"; font-weight:500; font-size:36px; color:#4f6163; }}
.ex {{ position:absolute; left:80px; right:80px; display:flex; flex-direction:column; gap:30px; }}
.e {{ background:rgba(23,38,43,.05); border-radius:26px; padding:24px 30px; text-align:center; }}
.e .s {{ font-family:"Plex Arabic"; font-weight:700; font-size:66px; direction:rtl; line-height:1.35; }} .e .s i {{ font-style:normal; color:{S.RED}; }}
.e .t {{ font-family:"JetBrains Mono"; font-size:25px; color:#6b7a7c; margin-top:4px; }} .e .m {{ font-size:34px; font-weight:700; margin-top:6px; }}
.note {{ position:absolute; bottom:90px; left:80px; right:80px; text-align:center; font-size:34px; font-weight:700; color:{S.TEAL}; }}
.note span {{ font-family:"Plex Arabic"; }}
.endq {{ position:absolute; top:330px; left:70px; right:70px; text-align:center; font-family:"Instrument Serif"; font-size:110px; line-height:1.02; }}
.endq i {{ color:{S.GOLD}; }} .ends {{ position:absolute; top:820px; left:90px; right:90px; display:grid; gap:24px; }}
.ends div {{ border-radius:22px; padding:24px; text-align:center; font-size:38px; font-weight:700; background:rgba(46,114,99,.12); }}
"""

def hi(sentence, word):          # the question word in red: ماذا is a word on its own, ما is its own word too
    first, _, rest = sentence.partition(" ")
    return f'<i>{first}</i> {rest}' if first in word.replace(" ", "").split("·") else sentence

def slides():
    out = {"1": f'<body>{S.BRAND}<div class="cov">' + "".join(f"<b>{e.capitalize()}?</b>" for e, *_ in W) + '</div>'
                f'<div class="cq">Can you say all 7<br>in Arabic? 👀</div><div class="cs">SWIPE AND COUNT YOUR SCORE →</div></body>'}
    for k, (en, ar, tr, ex, note) in enumerate(W, 2):
        top = 760 if len(ex) == 1 else 700
        boxes = "".join(f'<div class="e"><div class="s">{hi(s, ar)}</div><div class="t">{t}</div><div class="m">{m}</div></div>' for s, t, m in ex)
        nt = note.replace("ما ", '<span>ما</span> ').replace("ماذا ", '<span>ماذا</span> ')
        out[str(k)] = (f'<body>{S.BRAND}<div class="n">{k - 1} / 7</div><div class="q en">{en.capitalize()}?</div>'
                       f'<div class="q ar">{ar}</div><div class="q tr">{tr}</div><div class="ex" style="top:{top}px">{boxes}</div>'
                       + (f'<div class="note">{nt}</div>' if nt else "") + '</body>')
    out["9"] = (f'<body class="dark">{S.BRAND}<div class="endq">How many<br>did you know?<br><i>Comment /7 👇</i></div>'
                '<div class="ends"><div>Save this 📌 for later</div><div>Send it to someone learning Arabic with you</div></div></body>')
    return out

if __name__ == "__main__":
    out = os.path.join(S.HERE, "stills"); os.makedirs(out, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=S.CHROME if os.path.exists(S.CHROME) else None)
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for k, body in slides().items():
            tmp = os.path.join(out, "_qw.html"); open(tmp, "w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>{body}</html>')
            pg.goto("file://" + tmp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
            pg.screenshot(path=os.path.join(out, f"qw-{k}.png")); print(f"qw-{k}.png")
        b.close()
    os.remove(os.path.join(out, "_qw.html"))
