#!/usr/bin/env python3
"""'Salah word by word' TikTok series (#228): short (under 16s), hook and Arabic on screen from the first frame, each word said
as it appears, the meaning, then a question for the comments. No intro or end card; the reading voice only.

  s1-allahu-akbar        اللَّهُ أَكْبَرُ: 22 times in a four-rakʿah prayer (salah.js REPS.takbir)
  s2-subhana-rabbiyal    سُبْحانَ رَبِّيَ الْعَظِيمِ: 12 times (REPS.ruku)
  s3-samiallahu          سَمِعَ اللَّهُ لِمَنْ حَمِدَهُ: every time you rise from rukūʿ (REPS.rising: 4)

Words and meanings are salah-data.js's own. Never Quran: these are the prayer's own phrases.

  python3 brag-quiz/build_series.py [id ...]     then render each, then  --level
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build_teach as T
from build_teach import Comp, e

CSS = """
.hook { position:absolute; top:300px; left:70px; right:70px; text-align:center; font-size:74px; font-weight:700; line-height:1.12; letter-spacing:-.02em; }
.hook b { color:var(--rubric); }
.phrase { position:absolute; top:560px; left:40px; right:40px; text-align:center; font-family:var(--ar); font-weight:700; line-height:1.45; color:var(--ink); }
.wrow { position:absolute; top:880px; left:50px; right:50px; display:flex; flex-direction:row-reverse; justify-content:center; gap:18px; }
.wc { flex:1; display:flex; flex-direction:column; align-items:center; gap:2px; background:var(--card); border:4px solid rgba(23,38,43,.13); border-radius:30px;
  padding:14px 6px 20px; box-shadow:0 12px 26px -16px rgba(23,38,43,.35); }
.wc .ar { font-family:var(--ar); font-weight:700; line-height:1.5; color:var(--verdigris); }
.wc .en { font-size:40px; font-weight:700; text-align:center; line-height:1.15; }
.mean { position:absolute; top:1210px; left:70px; right:70px; text-align:center; font-size:56px; font-weight:700; line-height:1.2; color:var(--verdigris); }
.ask { position:absolute; top:1390px; left:70px; right:70px; text-align:center; font-size:46px; font-weight:700; line-height:1.25; color:var(--ink-soft); }
.url { position:absolute; top:150px; left:0; right:0; text-align:center; font-size:30px; font-weight:700; color:var(--verdigris); }
"""

S = [("s1-allahu-akbar", 1, 'You say this <b>22 times</b> in every four-rakʿah prayer', "اللَّهُ أَكْبَرُ", 150,
      [("اللَّهُ", "Allah"), ("أَكْبَرُ", "is the Greatest")], "“Allah is the Greatest.”", "Did you know it was 22? Tell me 👇"),
     ("s2-subhana-rabbiyal", 2, 'You say this <b>12 times</b> in every four-rakʿah prayer', "سُبْحانَ رَبِّيَ الْعَظِيمِ", 104,
      [("سُبْحانَ", "Glory be to"), ("رَبِّيَ", "my Lord"), ("الْعَظِيمِ", "the Magnificent")], "“Glory be to my Lord, the Magnificent.”",
      "Which line of salah should I do next? 👇"),
     ("s3-samiallahu", 3, 'You say this <b>every time</b> you rise from rukūʿ', "سَمِعَ اللَّهُ لِمَنْ حَمِدَهُ", 96,
      [("سَمِعَ", "hears"), ("اللَّهُ", "Allah"), ("لِمَنْ", "the one who"), ("حَمِدَهُ", "praises Him")], "“Allah hears the one who praises Him.”",
      "What do you reply? Comment it 👇")]

def build(vid, n, hook, phrase, size, words, mean, ask):
    c = Comp(vid, f"SALAH WORD BY WORD · #{n}", bed=False); c.css = CSS
    wsize = 70 if len(words) == 4 else 84
    # frame 0 already shows the hook and the phrase (the thumbnail and the first second)
    c.t('tl.fromTo(".phrase", {scale:0.96}, {scale:1, duration:0.5, ease:"power3.out"}, 0);')
    t = 0.35; d = c.say(phrase, t); t += d + 0.45
    c.t(f'tl.to(".hook", {{opacity:0.35, duration:0.3}}, {t - 0.2:.2f});')
    for i, (ar, _) in enumerate(words):
        c.inn(f"#w{i}", t, 30, 0.35); dw = c.say(ar, t + 0.05); t += max(dw, 0.6) + 0.25
    c.inn(".mean", t + 0.1); t += 2.0
    c.inn(".ask", t); t += 2.6
    cards = "".join(f'<div class="wc" id="w{i}"><div class="ar" lang="ar" style="font-size:{wsize}px">{e(a)}</div><div class="en">{e(m)}</div></div>'
                    for i, (a, m) in enumerate(words))
    body = (f'      <div class="url">rafiq-arabic.com</div><div class="hook">{hook}</div>'
            f'<div class="phrase" lang="ar" style="font-size:{size}px">{e(phrase)}</div>'
            f'<div class="wrow">{cards}</div><div class="mean">{e(mean)}</div><div class="ask">{e(ask)}</div>')
    c.write(body, round(t, 2))

ALL = {s[0]: s for s in S}
if __name__ == "__main__":
    ids = [a for a in sys.argv[1:] if not a.startswith("--")]
    T.LUFS.update({v: -16.0 for v in ALL})
    for vid, s in ALL.items():
        if ids and vid not in ids: continue
        T.level(vid) if "--level" in sys.argv else build(*s)
