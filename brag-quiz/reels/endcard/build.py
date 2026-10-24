#!/usr/bin/env python3
"""The end card for every video (owner, 20 Oct 2026): his line, since 24 Oct the clean one from the ad shoot (DJI take 0052 of
21 Oct, 2.57-9.40 s; owner: "it sounds a lot cleaner" than the first, phone-recorded "…invest in your Akhira"): "If you're ready to
finally invest in yourself and invest in your deen, then sign up to RafiqArabic.com" (voice.wav: low-cut and levelled to -16 LUFS;
it's all animation). The logo is there from the first frame; each word arrives from blur as he says it; "Deen" lands big in gold
with الدِّين; the line lifts away on "then"; the site pill types in on "RafiqArabic.com" and pops on ".com". Soft sounds from sfx/soft.
Two looks: cream (our usual videos) and dark (the quiet style).

  python3 brag-quiz/reels/endcard/build.py cream|dark   then  cd brag-quiz/reels/endcard/out/<look> && npx hyperframes render -o ../endcard-<look>.mp4
"""
import os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
V6 = os.path.join(ROOT, "brag-output-v6/composition/assets")
LOOK = sys.argv[1] if len(sys.argv) > 1 else "cream"
INK, CREAM, GOLD, GOLD2, RED, TEAL = "#17262b", "#f1ece0", "#a8842c", "#E9B949", "#b4322a", "#2e7263"
D = LOOK == "dark"
BG = "radial-gradient(ellipse at 50% 18%, #24393f 0%, #17262b 45%, #0d1619 100%)" if D else f"radial-gradient(circle at 50% 0%, rgba(168,132,44,.18) 0%, rgba(241,236,224,0) 55%), {CREAM}"
FG, ACC, MUTE = (CREAM, GOLD2, "rgba(241,236,224,.6)") if D else (INK, GOLD, "#5c6e70")
LEAD = 0.25; END = 7.8
# when each word is said (his recording, faster-whisper word times, + LEAD)
L1 = [("If", 0.07), ("you're", 0.19), ("ready", 0.49), ("to", 0.67), ("finally", 0.95), ("invest", 1.35), ("in", 1.85), ("yourself", 2.15),
      ("and", 2.53), ("invest", 2.81), ("in", 3.15), ("your", 3.45)]
AKH = 3.57; THEN = 4.59; L2 = [("then", 4.59), ("sign", 4.69), ("up", 4.95), ("to", 5.09)]; SITE = 5.25; NOW = 6.03   # NOW: ".com"

def build():
    out = os.path.join(HERE, "out", LOOK); a = os.path.join(out, "assets")
    if os.path.exists(out): shutil.rmtree(out)
    os.makedirs(a)
    for f in ("ibm-plex-sans-arabic-arabic-700-normal.woff2", "karla-latin-500-normal.woff2", "karla-latin-700-normal.woff2"): shutil.copy(os.path.join(V6, "fonts", f), a)
    shutil.copy(os.path.join(ROOT, "brag-quiz/fonts/instrument-serif-latin-400-normal.woff2"), a); shutil.copy(os.path.join(V6, "lib/gsap.min.js"), a)
    shutil.copy(os.path.join(HERE, "voice.wav"), a)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", os.path.join(V6, "sfx-gen/fountain.mp3"), "-af",       # the quiet bed: the clean take
                    f"volume=6dB,atrim=0:{END},afade=t=out:st={END - 0.25}:d=0.25", "-c:a", "libmp3lame", "-q:a", "3", os.path.join(a, "bed.mp3")], check=True)   # is silent between words
    for f in ("whoosh.wav", "tick.wav", "tick-lo.wav", "type.wav", "thump.wav"): shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/soft", f), a)
    au = [f'<audio id="voice" src="assets/voice.wav" data-start="{LEAD}" data-duration="6.83" data-volume="1" data-track-index="1"></audio>',
          f'<audio id="bed" src="assets/bed.mp3" data-start="0" data-duration="{END}" data-volume="0.06" data-track-index="7"></audio>']
    LEN = {"whoosh.wav": .55, "tick.wav": .05, "tick-lo.wav": .05, "type.wav": .025, "thump.wav": .7}
    def fx(n, t, v): au.append(f'<audio id="s{len(au)}" src="assets/{n}" data-start="{t:.3f}" data-duration="{LEN[n]}" data-volume="{v}" data-track-index="{2 + len(au) % 5}"></audio>')
    js = []; T = js.append
    def word(sel, t, d=0.45): T(f'tl.fromTo("{sel}", {{opacity:0, y:14, filter:"blur(12px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:{d}, ease:"power2.out"}}, {t:.2f});')
    T('tl.fromTo("#logo", {scale:0.96}, {scale:1, duration:0.6, ease:"power2.out"}, 0);')
    for i, (w, t) in enumerate(L1): word(f"#w{i}", LEAD + t - 0.05)
    t = LEAD + AKH - 0.06                                                     # Akhira lands big, gold, with its Arabic
    T(f'tl.fromTo("#akh", {{opacity:0, scale:1.35, filter:"blur(20px)"}}, {{opacity:1, scale:1, filter:"blur(0px)", duration:0.6, ease:"expo.out"}}, {t:.2f});')
    T(f'tl.fromTo("#akhAr", {{opacity:0, y:16}}, {{opacity:1, y:0, duration:0.5, ease:"power2.out"}}, {t + 0.35:.2f});')
    T(f'tl.fromTo("#glow", {{opacity:0, scale:0.6}}, {{opacity:1, scale:1, duration:0.9, ease:"power2.out"}}, {t:.2f});'); fx("thump.wav", t + 0.05, 0.35)
    t = LEAD + THEN - 0.3                                                     # the line lifts away, clear by "then"
    T(f'tl.to(["#part1", "#glow"], {{y:-260, opacity:0, filter:"blur(14px)", duration:0.4, ease:"power3.in"}}, {t:.2f});'); fx("whoosh.wav", t - 0.05, 0.3)
    for i, (w, tt) in enumerate(L2): word(f"#v{i}", LEAD + tt - 0.05)
    t = LEAD + SITE - 0.08                                                    # the pill, then the site types in
    T(f'tl.fromTo("#pill", {{opacity:0, scale:0.8, y:30}}, {{opacity:1, scale:1, y:0, duration:0.5, ease:"back.out(2)"}}, {t:.2f});'); fx("tick-lo.wav", t + 0.05, 0.25)
    site = "rafiq-arabic.com"; dt = (LEAD + NOW - 0.25 - (t + 0.2)) / len(site)
    for k in range(len(site)): T(f'tl.set("#site span:nth-child({k + 1})", {{opacity:1}}, {t + 0.2 + dt * k:.3f});')
    for k in range(0, len(site), 2): fx("type.wav", t + 0.2 + dt * k, 0.08)
    t = LEAD + NOW - 0.05
    fx("tick.wav", t + 0.03, 0.25)
    T(f'tl.fromTo("#pill", {{scale:1}}, {{scale:1.05, duration:0.18, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {t:.2f});')
    T(f'tl.fromTo("#free", {{opacity:0, y:14}}, {{opacity:1, y:0, duration:0.4, ease:"power2.out"}}, {t + 0.3:.2f});')

    body = f"""
<div id="logo"><span class="tile"><span>ر</span><em></em></span><b>رَفِيق</b></div>
<div id="glow"></div>
<div id="part1"><div class="line">{" ".join(f'<span class="w" id="w{i}">{w}</span>' for i, (w, _) in enumerate(L1))}</div>
  <div id="akh">Deen,</div><div id="akhAr">الدِّين</div></div>
<div id="part2"><div class="line">{" ".join(f'<span class="w" id="v{i}">{w}</span>' for i, (w, _) in enumerate(L2))}</div>
  <div id="pill"><span class="tile sm"><span>ر</span><em></em></span><span id="site">{"".join(f"<span>{c}</span>" for c in site)}</span></div>
  <div id="free">Free for 7 days · no card needed</div></div>"""
    css = f"""
@font-face {{ font-family:"Ar"; src:url("assets/ibm-plex-sans-arabic-arabic-700-normal.woff2"); font-weight:700; }}
@font-face {{ font-family:"Karla"; src:url("assets/karla-latin-500-normal.woff2"); font-weight:500; }}
@font-face {{ font-family:"Karla"; src:url("assets/karla-latin-700-normal.woff2"); font-weight:700; }}
@font-face {{ font-family:"InstrumentSerif"; src:url("assets/instrument-serif-latin-400-normal.woff2"); }}
body {{ margin:0; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:{BG}; color:{FG}; font-family:"Karla"; }}
#logo {{ position:absolute; top:420px; left:0; right:0; display:flex; justify-content:center; align-items:center; gap:22px; }}
#logo b {{ font-family:"Ar"; font-size:76px; font-weight:700; }}
.tile {{ position:relative; width:104px; height:104px; border-radius:26px; background:{FG}; display:grid; place-items:center; }}
.tile span {{ font-family:"Ar"; font-weight:700; font-size:64px; color:{CREAM if not D else INK}; margin-top:-8px; }}
.tile em {{ position:absolute; right:16px; top:14px; width:16px; height:16px; border-radius:50%; background:{RED}; }}
.tile.sm {{ width:76px; height:76px; border-radius:20px; background:{CREAM if not D else INK}; }} .tile.sm span {{ font-size:46px; color:{INK if not D else CREAM}; margin-top:-6px; }}
.tile.sm em {{ right:11px; top:10px; width:12px; height:12px; }}
#part1, #part2 {{ position:absolute; left:70px; right:70px; top:800px; text-align:center; }}
.line {{ font-family:"InstrumentSerif"; font-style:italic; font-size:84px; line-height:1.12; letter-spacing:-.01em; }}
.w {{ display:inline-block; opacity:0; }}
#akh {{ font-family:"InstrumentSerif"; font-size:230px; line-height:1; letter-spacing:-.025em; color:{ACC}; margin-top:40px; opacity:0; }}
#akhAr {{ font-family:"Ar"; font-weight:700; font-size:96px; direction:rtl; color:{ACC}; opacity:0; margin-top:10px; }}
#glow {{ position:absolute; left:140px; top:800px; width:800px; height:640px; border-radius:50%; background:radial-gradient(circle, rgba(233,185,73,{.28 if D else .22}) 0%, rgba(233,185,73,0) 65%); opacity:0; }}
#pill {{ display:inline-flex; align-items:center; gap:22px; margin-top:70px; padding:26px 46px 26px 30px; border-radius:999px; background:{TEAL}; color:{CREAM};
  font-weight:700; font-size:64px; opacity:0; box-shadow:0 24px 50px -24px rgba(46,114,99,.9); }}
#site span {{ opacity:0; }}
#free {{ font-size:40px; font-weight:500; color:{MUTE}; margin-top:40px; opacity:0; }}
"""
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><title>endcard-{LOOK}</title>
<script src="assets/gsap.min.js"></script><style>{css}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{END}">
{body}
{chr(10).join(au)}
</div><script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;</script></body></html>
""")
    print("built", LOOK, END, "s")

if __name__ == "__main__":
    build()
