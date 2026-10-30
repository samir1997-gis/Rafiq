#!/usr/bin/env python3
"""The Arabic alphabet reel (owner, 26 Oct 2026): his own recording of the 28 letters (brag-quiz/voice/alphabet: his phone video's
audio, as recorded; the letters found by their level and checked by an Arabic transcription; ḍād and ṭā split at 21.33 s, a false
start at 23.9 s dropped; qāf re-recorded by the owner, 30 Oct 2026, and spliced in at 29.08 s at the same level), over a grid of the letters (rows of five, right to left, as the reference reel): each box lights up as he
says its letter and stays ticked, a progress bar with "n / 28" fills underneath, the Rafiq logo at the top and "Start your Arabic
journey · Try RafiqArabic.com" at the bottom (clear of Instagram's caption). Five colour schemes for trial reels.

  python3 brag-quiz/reels/alphabet/build.py SCHEME      (ink · paper · teal · rubric · night)
  then  cd brag-quiz/reels/alphabet/out/SCHEME && npx hyperframes render -o ../alphabet-SCHEME.mp4
"""
import json, os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
V6 = os.path.join(ROOT, "brag-output-v6/composition/assets"); VO = os.path.join(ROOT, "brag-quiz/voice/alphabet")
LETTERS = [("ا", "Alif"), ("ب", "Ba"), ("ت", "Ta"), ("ث", "Tha"), ("ج", "Jim"), ("ح", "Ha"), ("خ", "Kha"), ("د", "Dal"), ("ذ", "Dhal"),
           ("ر", "Ra"), ("ز", "Zay"), ("س", "Sin"), ("ش", "Shin"), ("ص", "Sad"), ("ض", "Dad"), ("ط", "Ta"), ("ظ", "Dha"), ("ع", "ʿAyn"),
           ("غ", "Ghayn"), ("ف", "Fa"), ("ق", "Qaf"), ("ك", "Kaf"), ("ل", "Lam"), ("م", "Mim"), ("ن", "Nun"), ("ه", "Ha"), ("و", "Waw"), ("ي", "Ya")]
SCHEMES = {   # background, letters, label, box, highlight fill, highlight text, accent (bar, logo dot), ticked tint
 "ink":    dict(bg="radial-gradient(ellipse at 50% 30%, #1d2f35 0%, #0f1a1d 70%)", fg="#F1ECE0", lab="#9fb0b2", box="rgba(241,236,224,.05)", hi="#E9B949", hit="#17262B", acc="#E9B949", done="rgba(233,185,73,.16)"),
 "paper":  dict(bg="radial-gradient(ellipse at 50% 30%, #fbf7ee 0%, #F1ECE0 65%, #e3d9c4 100%)", fg="#17262B", lab="#5c6e70", box="rgba(23,38,43,.04)", hi="#2E7263", hit="#F1ECE0", acc="#B4322A", done="rgba(46,114,99,.14)"),
 "teal":   dict(bg="radial-gradient(ellipse at 50% 30%, #3a8a78 0%, #2E7263 45%, #1d4d42 100%)", fg="#F1ECE0", lab="#cfe3dc", box="rgba(241,236,224,.07)", hi="#E9B949", hit="#17262B", acc="#E9B949", done="rgba(233,185,73,.2)"),
 "rubric": dict(bg="radial-gradient(ellipse at 50% 30%, #5a1a14 0%, #3a0f0c 60%, #240806 100%)", fg="#F1ECE0", lab="#e2b9b1", box="rgba(241,236,224,.06)", hi="#F1ECE0", hit="#B4322A", acc="#E9B949", done="rgba(241,236,224,.13)"),
 "night":  dict(bg="#050606", fg="#E9B949", lab="#a8842c", box="rgba(233,185,73,.05)", hi="#B4322A", hit="#F1ECE0", acc="#B4322A", done="rgba(180,50,42,.22)"),
}
SCHEME = sys.argv[1] if len(sys.argv) > 1 else "ink"; K = SCHEMES[SCHEME]
TIMES = json.load(open(os.path.join(VO, "owner-letters.times.json")))
END = round(TIMES[-1][1] + 1.6, 2)                                       # the last letter, then a beat on the full board
dur = lambda f: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))

def build():
    out = os.path.join(HERE, "out", SCHEME); a = os.path.join(out, "assets")
    if os.path.exists(out): shutil.rmtree(out)
    os.makedirs(a)
    for f in ("karla-latin-500-normal.woff2", "karla-latin-700-normal.woff2", "ibm-plex-sans-arabic-arabic-700-normal.woff2"): shutil.copy(os.path.join(V6, "fonts", f), a)
    shutil.copy(os.path.join(V6, "lib/gsap.min.js"), a); shutil.copy(os.path.join(VO, "owner-letters.wav"), a)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", os.path.join(V6, "sfx-gen/fountain.mp3"), "-af",
                    f"volume=6dB,atrim=0:{END},afade=t=in:d=0.6,afade=t=out:st={END - 0.4}:d=0.4", "-c:a", "libmp3lame", "-q:a", "3", os.path.join(a, "bed.mp3")], check=True)
    au = [f'<audio id="v" src="assets/owner-letters.wav" data-start="0" data-duration="{dur(os.path.join(a, "owner-letters.wav")):.3f}" data-volume="1" data-track-index="1"></audio>',
          f'<audio id="b" src="assets/bed.mp3" data-start="0" data-duration="{END}" data-volume="0.05" data-track-index="2"></audio>']   # his voice as recorded; a very quiet bed
    js = []; T = js.append
    for i, (s, e) in enumerate(TIMES):
        t0 = max(0.0, s - 0.06); t1 = TIMES[i + 1][0] - 0.06 if i + 1 < len(TIMES) else END - 1.0
        T(f'tl.to("#c{i}", {{backgroundColor:"{K["hi"]}", borderColor:"{K["hi"]}", scale:1.12, duration:0.12, ease:"back.out(3)"}}, {t0:.2f});')
        T(f'tl.to("#c{i} b, #c{i} span", {{color:"{K["hit"]}", duration:0.1}}, {t0:.2f});')
        T(f'tl.to("#c{i}", {{scale:1.04, duration:0.25, ease:"power2.out"}}, {t0 + 0.14:.2f});')
        T(f'tl.to("#c{i}", {{backgroundColor:"{K["done"]}", borderColor:"{K["acc"]}", scale:1, duration:0.25}}, {t1:.2f});')       # said: stays ticked
        T(f'tl.to("#c{i} b", {{color:"{K["fg"]}", duration:0.2}}, {t1:.2f});'); T(f'tl.to("#c{i} span", {{color:"{K["lab"]}", duration:0.2}}, {t1:.2f});')
        T(f'tl.set("#cnt", {{textContent:"{i + 1} / 28"}}, {t0:.2f});')
        T(f'tl.to("#bar i", {{scaleX:{(i + 1) / 28:.4f}, duration:0.3, ease:"power2.out"}}, {t0:.2f});')
    T(f'tl.to(".cell", {{scale:1.06, duration:0.18, yoyo:true, repeat:1, stagger:0.02, ease:"power2.out"}}, {END - 1.3:.2f});')   # the full board
    T(f'tl.fromTo("#cta b", {{scale:1}}, {{scale:1.08, duration:0.25, yoyo:true, repeat:1, ease:"power2.out"}}, {END - 1.0:.2f});')
    cells = ""
    for r in range(6):
        row = LETTERS[r * 5:(r + 1) * 5]
        for c, (ar, en) in enumerate(row):
            i = r * 5 + c; col = 4 - c if r < 5 else 3 - c                    # right to left; the last row of three sits in the middle
            cells += (f'<div class="cell" id="c{i}" style="left:{70 + col * 192}px;top:{330 + r * 182}px"><b>{ar}</b><span>{en}</span></div>')
    css = f"""
@font-face {{ font-family:"KA"; src:url("assets/karla-latin-500-normal.woff2"); font-weight:500; }}
@font-face {{ font-family:"KA"; src:url("assets/karla-latin-700-normal.woff2"); font-weight:700; }}
@font-face {{ font-family:"AR"; src:url("assets/ibm-plex-sans-arabic-arabic-700-normal.woff2"); }}
* {{ margin:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:{K["bg"]}; color:{K["fg"]}; font-family:KA; }}
#logo {{ position:absolute; top:90px; left:0; right:0; display:flex; justify-content:center; align-items:center; gap:18px; }}
#logo .tile {{ position:relative; width:84px; height:84px; border-radius:22px; background:{K["fg"]}; display:grid; place-items:center; }}
#logo .tile span {{ font-family:AR; font-size:52px; color:{"#17262B" if K["fg"] != "#17262B" else "#F1ECE0"}; margin-top:-6px; }}
#logo .tile em {{ position:absolute; right:13px; top:12px; width:13px; height:13px; border-radius:50%; background:{K["acc"]}; }}
#logo b {{ font-family:AR; font-size:64px; font-weight:700; }}
#title {{ position:absolute; top:212px; left:0; right:0; text-align:center; font-weight:700; font-size:70px; letter-spacing:-.01em; }}
.cell {{ position:absolute; width:172px; height:172px; border-radius:26px; background:{K["box"]}; border:4px solid transparent;
  display:flex; flex-direction:column; align-items:center; justify-content:center; transform-origin:50% 50%; }}
.cell b {{ font-family:AR; font-size:92px; line-height:1.15; color:{K["fg"]}; font-weight:700; }}
.cell span {{ font-size:30px; font-weight:700; color:{K["lab"]}; margin-top:-4px; }}
#bar {{ position:absolute; left:110px; right:110px; top:1500px; height:16px; border-radius:8px; background:{K["box"]}; overflow:hidden; box-shadow:inset 0 0 0 2px {K["done"]}; }}
#bar i {{ position:absolute; inset:0; background:{K["acc"]}; transform-origin:0 50%; transform:scaleX(0); border-radius:8px; }}
#cnt {{ position:absolute; top:1428px; left:0; right:0; text-align:center; font-weight:700; font-size:46px; color:{K["lab"]}; }}
#cta {{ position:absolute; top:1550px; left:0; right:0; text-align:center; font-size:42px; font-weight:500; line-height:1.35; }}
#cta b {{ display:inline-block; font-weight:700; color:{K["acc"]}; }}
"""
    body = f"""<div id="logo"><span class="tile"><span>ر</span><em></em></span><b>رَفِيق</b></div>
<div id="title">The Arabic Alphabet</div>{cells}
<div id="cnt">0 / 28</div><div id="bar"><i></i></div>
<div id="cta">Start your Arabic journey<br>Try <b>RafiqArabic.com</b></div>"""
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><title>alphabet-{SCHEME}</title>
<script src="assets/gsap.min.js"></script><style>{css}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{END}">
{body}
{chr(10).join(au)}
</div><script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;</script></body></html>
""")
    print("built", SCHEME, END, "s")

if __name__ == "__main__":
    build()
