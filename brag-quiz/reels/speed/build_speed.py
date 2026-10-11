#!/usr/bin/env python3
"""Speed reading v2 (owner, 11 Oct 2026): the same five words as m09-speed, rebuilt for urgency after both TikTok posts
stalled at ~260-290 views (tools/typesafe-exp/speed_read_fix.py): the first word is on screen at frame 0 and its timer is
already running; a big stopwatch counts down; ticks speed up; a red flash and shake in the last half second; a buzzer and
TIME! when it runs out; then the word is said with its meaning, and the next one cuts in faster.

  python3 brag-quiz/reels/speed/build_speed.py      then in brag-quiz/reels/speed/out/s2-speed: npx hyperframes render -o ../s2-speed.mp4
"""
import json, os, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
FONTS = os.path.join(ROOT, "brag-quiz/fonts"); GSAP = os.path.join(ROOT, "brag-output-v6/composition/assets/lib/gsap.min.js")
AUDIO = {x["text"]: x["id"] for x in json.load(open(os.path.join(ROOT, "audio-manifest.json")))}
dur = lambda p: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode())

WORDS = [("باب", "door", "bāb", "#b3272f"), ("قَلَم", "pen", "qalam", "#2e7263"), ("شاي", "tea", "shāy", "#17262b"),
         ("بَحْر", "sea", "baḥr", "#6b3fa0"), ("سَيَّارَة", "car", "sayyāra", "#c4561d")]
TIMES = [2.4, 1.9, 1.5, 1.15, 0.85]          # each round faster
REVEAL = 1.15

def sounds(a):
    """A clock tick and a buzzer, made here so the reel needs nothing new in the sound library."""
    run = lambda *x: subprocess.run(["ffmpeg", "-v", "error", "-y", *x], check=True)
    run("-f", "lavfi", "-i", "sine=f=2400:d=0.04", "-af", "afade=t=out:st=0.004:d=0.036,volume=0.9", os.path.join(a, "tick.wav"))
    run("-f", "lavfi", "-i", "sine=f=150:d=0.5", "-f", "lavfi", "-i", "sine=f=223:d=0.5",
        "-filter_complex", "[0][1]amix=2,asoftclip=type=hard,volume=2.2,afade=t=out:st=0.38:d=0.12", os.path.join(a, "buzz.wav"))
    shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/ref/swoosh.wav"), os.path.join(a, "swoosh.wav"))

def build():
    out = os.path.join(HERE, "out", "s2-speed"); a = os.path.join(out, "assets")
    if os.path.exists(out): shutil.rmtree(out)
    os.makedirs(a)
    for f in os.listdir(FONTS): shutil.copy(os.path.join(FONTS, f), a)
    shutil.copy(GSAP, a); sounds(a)
    au, js, secs, t = [], [], [], 0.0
    def snd(src, at, d, vol, track):
        au.append(f'<audio id="a{len(au)}" src="assets/{src}" data-start="{at:.2f}" data-duration="{d:.2f}" data-volume="{vol}" data-track-index="{track}"></audio>')
    for k, ((ar, en, tr, bg), T) in enumerate(zip(WORDS, TIMES)):
        s = f"w{k}"
        secs.append(f'<div class="sec" id="{s}" style="background:{bg}"><div class="stripes"></div>'
                    f'<div class="lvl">ROUND {k + 1}/5{"" if k == 0 else f" · X{TIMES[0] / T:.1f} FASTER"}</div>'
                    f'<div class="word" lang="ar">{ar}</div>'
                    f'<div class="clock"><svg viewBox="0 0 300 300"><circle class="bg" cx="150" cy="150" r="130"/><circle class="fg" cx="150" cy="150" r="130"/></svg><span id="{s}n">{T:.1f}</span></div>'
                    f'<div class="time">TIME!</div><div class="mean"><b>{en}</b> · {tr}</div><div class="red"></div></div>')
        if k: js.append(f'tl.set("#{s}", {{opacity:1}}, {t:.2f});'); snd("swoosh.wav", max(0, t - 0.08), 0.5, 0.5, 6)
        js.append(f'tl.set("#w{k - 1}", {{opacity:0}}, {t:.2f});' if k else 'tl.set("#w0", {opacity:1}, 0);')
        # the stopwatch: ring drains and the number counts down to 0.0
        js += [f'tl.fromTo("#{s} .fg", {{strokeDashoffset:0}}, {{strokeDashoffset:817, duration:{T}, ease:"none"}}, {t:.2f});',
               f'(() => {{ const o = {{v:{T}}}; tl.to(o, {{v:0, duration:{T}, ease:"none", onUpdate:() => {{ document.getElementById("{s}n").textContent = o.v.toFixed(1); }}}}, {t:.2f}); }})();']
        n = 8 + k * 2; step = T / n                    # ticks: more of them, closer together, every round
        for i in range(n): snd("tick.wav", t + i * step, 0.05, 0.55 + 0.35 * i / n, 10 + i % 2)
        w = min(0.5, T * 0.45)                         # the last half second: red pulse and a shake
        js += [f'tl.fromTo("#{s} .red", {{opacity:0}}, {{opacity:0.55, duration:{w / 2:.2f}, yoyo:true, repeat:1}}, {t + T - w:.2f});',
               f'tl.fromTo("#{s} .word", {{x:-10}}, {{x:10, duration:0.05, yoyo:true, repeat:{int(w / 0.05) - 1}, ease:"none"}}, {t + T - w:.2f});',
               f'tl.set("#{s} .word", {{x:0}}, {t + T:.2f});']
        E = t + T                                      # time's up: buzzer and TIME!, then the word said and its meaning
        snd("buzz.wav", E, 0.5, 0.75, 7)
        js += [f'tl.fromTo("#{s} .time", {{opacity:0, scale:1.6, rotation:-8}}, {{opacity:1, scale:1, rotation:-8, duration:0.18, ease:"power4.out"}}, {E:.2f});',
               f'tl.to("#{s} .clock", {{opacity:0, duration:0.15}}, {E:.2f});',
               f'tl.fromTo("#{s} .mean", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.25, ease:"power3.out"}}, {E + 0.2:.2f});']
        src = os.path.join(ROOT, "audio", AUDIO[ar] + ".mp3"); shutil.copy(src, a)
        snd(f"{AUDIO[ar]}.mp3", E + 0.3, dur(src), 1.0, 12 + k % 2)
        t = E + REVEAL
    js += [f'tl.set("#w4", {{opacity:0}}, {t:.2f});', f'tl.fromTo("#end", {{opacity:0}}, {{opacity:1, duration:0.2}}, {t:.2f});',
           f'tl.fromTo("#end .score", {{scale:1.4, opacity:0}}, {{scale:1, opacity:1, duration:0.3, ease:"power4.out"}}, {t + 0.1:.2f});',
           f'tl.fromTo("#end .ask", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.3}}, {t + 0.6:.2f});']
    snd("swoosh.wav", t - 0.08, 0.5, 0.5, 6)
    total = round(t + 2.6, 2)
    css = """
@font-face { font-family:"Anton"; src:url("assets/anton-latin-400-normal.woff2"); }
@font-face { font-family:"Ar"; src:url("assets/ibm-plex-sans-arabic-arabic-700-normal.woff2"); font-weight:700; }
body { margin:0; background:#000; } #root { position:relative; width:1080px; height:1920px; overflow:hidden; background:#111; }
.sec, #end { position:absolute; inset:0; opacity:0; }
.stripes { position:absolute; inset:0; background:repeating-linear-gradient(135deg, rgba(255,255,255,.06) 0 40px, rgba(255,255,255,0) 40px 80px); }
.lvl { position:absolute; top:150px; left:0; right:0; text-align:center; font-family:Anton; font-size:64px; color:#E9B949; letter-spacing:.04em; }
.word { position:absolute; top:430px; left:0; right:0; text-align:center; font-family:Ar; font-weight:700; font-size:330px; color:#fff; line-height:1.3; }
.clock { position:absolute; top:1050px; left:390px; width:300px; height:300px; }
.clock svg { position:absolute; inset:0; transform:rotate(-90deg); } .clock circle { fill:none; stroke-width:22; }
.clock .bg { stroke:rgba(255,255,255,.18); } .clock .fg { stroke:#fff; stroke-linecap:round; stroke-dasharray:817; }
.clock span { position:absolute; inset:0; display:grid; place-items:center; font-family:Anton; font-size:120px; color:#fff; }
.time { position:absolute; top:1070px; left:0; right:0; text-align:center; font-family:Anton; font-size:190px; color:#fff; opacity:0;
        text-shadow:0 8px 0 #C8372D; }
.mean { position:absolute; top:1330px; left:0; right:0; text-align:center; font-family:Anton; font-size:84px; color:rgba(255,255,255,.85); opacity:0; }
.mean b { color:#E9B949; font-weight:400; }
.red { position:absolute; inset:0; background:radial-gradient(ellipse at 50% 50%, rgba(200,0,0,0) 30%, rgba(220,0,0,.9) 100%); opacity:0; }
#end { background:#17262b; } #end .q { position:absolute; top:430px; left:60px; right:60px; text-align:center; font-family:Anton; font-size:120px; color:#fff; line-height:1.05; }
#end .score { position:absolute; top:760px; left:0; right:0; text-align:center; font-family:Anton; font-size:330px; color:#E9B949; }
#end .ask { position:absolute; top:1250px; left:60px; right:60px; text-align:center; font-family:Anton; font-size:72px; color:#fff; line-height:1.15; }
"""
    end = ('<div id="end"><div class="q">HOW MANY DID YOU READ IN TIME?</div><div class="score">?/5</div>'
           '<div class="ask">COMMENT YOUR SCORE 👇<br><span style="color:#E9B949">SEND IT TO SOMEONE WHO’D LOSE 😅</span></div></div>')
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><title>s2-speed</title>
<script src="assets/gsap.min.js"></script><style>{css}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{total}">
{''.join(secs)}{end}
{chr(10).join(au)}
</div><script>const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;</script></body></html>
""")
    print(f"s2-speed: {total}s")

if __name__ == "__main__":
    build()
