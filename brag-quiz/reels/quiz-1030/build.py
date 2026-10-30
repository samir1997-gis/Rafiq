#!/usr/bin/env python3
"""The owner's weekly Arabic quiz, "words frequently mentioned in the Qur'an" (30 Oct 2026, #309; Drive RAW 1030.mp4, his background already
removed to pure black). He sits small in the bottom half (keyed on the black, so his dark top stays); above him, each question as he asks it:
the word, four options, a countdown with a click on every tick, and the answer just before he moves on. Q4 is أَثاث, furnishings (an-Naḥl
16:80; owner: "it's athaath", the transcriber wrote "FF"). Sounds set against his voice as recorded and checked in the mix.
Easing as MOTION-STYLE.md.

  python3 brag-quiz/reels/quiz-1030/build.py WORK      (WORK/src.mp4 is his video) → brag-quiz/out/quiz/quiz-1030.mp4
"""
import json, os, re, shutil, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
W = sys.argv[1]; SRC = os.path.join(W, "src.mp4"); SFX = os.path.join(ROOT, "brag-quiz/sfx")
INK, PAPER, GOLD, TEAL, RED, GREEN = "#17262B", "#F1ECE0", "#E9B949", "#2E7263", "#B4322A", "#2EB67D"
END = 50.0                                                      # his video is 47.5 s; his last frame holds while the score ask lands
# (question, the word (or None), [(option, translit)], correct index, times: (shown, word pops, options, timer start, ticks, reveal, out))
Q = [("Which one means <b>“he said”</b>?", None, [("قالَ", "qāla"), ("ذَهَبَ", "dhahaba"), ("كَتَبَ", "kataba"), ("سَمِعَ", "samiʿa")], 0, (8.5, None, 10.8, 11.6, 3, 14.6, 16.4)),
     ("What does this mean?", ("كانَ", "kāna"), [("he said", ""), ("he was", ""), ("he came", ""), ("he made", "")], 1, (17.1, 17.9, 18.9, 19.4, 4, 23.4, 25.6)),
     ("What does this mean?", ("آمَنُوا", "āmanū"), [("they said", ""), ("they prayed", ""), ("they believed", ""), ("they knew", "")], 2, (26.2, 27.3, 28.5, 28.9, 4, 32.9, 34.0)),
     ("Tricky one ⚠️", ("أَثاث", "athāth"), [("clothes", ""), ("furnishings", ""), ("food", ""), ("gold", "")], 1, (34.3, 35.7, 36.4, 37.0, 4, 41.0, 41.9)),
     ("Which one means <b>“he made”</b>?", None, [("خَرَجَ", "kharaja"), ("كانَ", "kāna"), ("جَعَلَ", "jaʿala"), ("قالَ", "qāla")], 2, (42.0, None, 43.4, 43.9, 3, 46.9, None))]
NEXT = [15.1, 23.9, 33.5, 42.0, END - 2.5]                     # when he speaks again after each question (the score ask, for the last)
VO = os.path.join(ROOT, "brag-quiz/voice/quiz-1030")            # the answers read out (owner, 30 Oct): Rafiq for the Arabic, Callum for the English
def spoken(f):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout, np.int16) / 32768
    e = 20 * np.log10(np.sqrt(np.convolve(x ** 2, np.ones(160) / 160, "same")) + 1e-9); v = np.where(e > -40)[0]
    return v[0] / 16000, v[-1] / 16000                           # where the speech starts and ends in the file
NOTE = {3: "<i>athāth</i>: household goods, furnishings · an-Naḥl 16:80"}

def build():
    out = os.path.join(HERE, "out", "v"); a = os.path.join(out, "assets")
    if os.path.exists(out): shutil.rmtree(out)
    os.makedirs(a)
    for f in ("fredoka-latin-700-normal.woff2", "fredoka-latin-600-normal.woff2", "ibm-plex-sans-arabic-arabic-700-normal.woff2", "anton-latin-400-normal.woff2"): shutil.copy(os.path.join(ROOT, "brag-quiz/fonts", f), a)
    shutil.copy(os.path.join(ROOT, "brag-output-v6/composition/assets/lib/gsap.min.js"), a)
    js, body, S = [], [], []; T = js.append
    def snd(name, t, db): S.append((name, t, db))
    IN = lambda sel, t, y=30, d=0.45: T(f'tl.fromTo("{sel}", {{opacity:0, y:{y}}}, {{opacity:1, y:0, duration:{d}, ease:"power3.out"}}, {t:.2f});')
    POP = lambda sel, t, s=0.6: T(f'tl.fromTo("{sel}", {{opacity:0, scale:{s}}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(1.4)"}}, {t:.2f});')
    OUT = lambda sel, t: T(f'tl.to("{sel}", {{opacity:0, y:-30, duration:0.3, ease:"power2.in"}}, {t:.2f});')
    # the hook: STOP slams on frame 0, then the title
    T('tl.fromTo("#stop", {scale:1.6}, {scale:1, duration:0.35, ease:"back.out(1.7)"}, 0);'); snd("crash", 0.02, -2)
    T('tl.fromTo("#cam", {x:-14}, {x:14, duration:0.05, yoyo:true, repeat:5, ease:"sine.inOut", immediateRender:false}, 0.02); tl.set("#cam", {x:0}, 0.34);')
    OUT("#stop", 1.0); POP("#title", 0.9); snd("whoosh", 0.9, -10)
    IN("#sub", 3.6, 20); snd("tap", 3.7, -8)
    for qi, (qtext, word, opts, ok, (t0, tw, to, tt, n, tr, tx)) in enumerate(Q):
        k = f"q{qi}"; af = os.path.join(VO, f"a{qi + 1}.mp3"); s0, s1 = spoken(af)
        tr = round(NEXT[qi] - (s1 - s0) - 0.45, 2)                 # the answer lands, is read out, and he goes on
        sp = (tr - tt) / n                                         # the ticks spread over the time there is
        wav = os.path.join(W, f"a{qi + 1}.wav"); subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", af, "-ar", "48000", "-ac", "2", wav], check=True)
        S.append((wav, tr + 0.12 - s0, 0))                          # the answer's voice just after it turns green, level with his peaks
        opt = "".join(f'<div class="op" id="{k}o{i}"><b class="{"ar" if tr_ else ""}">{o}</b>' + (f'<small>{tr_}</small>' if tr_ else "") + '</div>' for i, (o, tr_) in enumerate(opts))
        body.append(f'<div class="q" id="{k}"><div class="cnt">{qi + 1} / {len(Q)}</div><div class="qt">{qtext}</div>'
                    + (f'<div class="w ar" id="{k}w">{word[0]}<small>{word[1]}</small></div>' if word else "")
                    + f'<div class="ops{" big" if not word else ""}">{opt}</div><div class="tm" id="{k}t"><svg viewBox="0 0 120 120"><circle cx="60" cy="60" r="50" class="trk"/><circle cx="60" cy="60" r="50" class="arc" id="{k}a" pathLength="1"/></svg><b id="{k}n">{n}</b></div>'
                    + (f'<div class="note" id="{k}nt">{NOTE[qi]}</div>' if qi in NOTE else "") + '</div>')
        T(f'tl.set("#{k}", {{opacity:1}}, {t0 - 0.3:.2f});'); OUT("#title, #sub" if qi == 0 else f"#q{qi - 1}", t0 - 0.35)
        IN(f"#{k} .cnt", t0 - 0.2, 20); IN(f"#{k} .qt", t0, 30); snd("whoosh", t0 - 0.3, -10)
        if word: POP(f"#{k}w", tw - 0.05, 0.5); snd("tick-lo", tw, -6)
        for i in range(4): POP(f"#{k}o{i}", to + i * 0.12, 0.8); snd("tap", to + i * 0.12, -5)
        IN(f"#{k}t", tt - 0.25, 10)
        T(f'tl.fromTo("#{k}a", {{strokeDashoffset:0}}, {{strokeDashoffset:1, duration:{tr - tt:.2f}, ease:"power1.in"}}, {tt:.2f});')
        for j in range(n):
            T(f'tl.set("#{k}n", {{textContent:"{n - j}"}}, {tt + j * sp:.2f});'); T(f'tl.fromTo("#{k}n", {{scale:1.35}}, {{scale:1, duration:0.3, ease:"power3.out"}}, {tt + j * sp:.2f});')
            snd("click", tt + j * sp, 2)                           # louder ticks (owner, 30 Oct)
        T(f'tl.to("#{k}t", {{opacity:0, scale:0.6, duration:0.25, ease:"power2.in"}}, {tr - 0.05:.2f});')
        T(f'tl.to("#{k}o{ok}", {{backgroundColor:"{GREEN}", color:"#fff", scale:1.06, duration:0.3, ease:"back.out(1.4)"}}, {tr:.2f});')
        T(f'tl.to([{", ".join(f"{chr(34)}#{k}o{i}{chr(34)}" for i in range(4) if i != ok)}], {{opacity:0.3, duration:0.3, ease:"power2.in"}}, {tr:.2f});')
        snd("shimmer", tr, -10); snd("tick-lo", tr, -4)
        if qi in NOTE: IN(f"#{k}nt", tr + 0.2, 20)
        if tx is None: OUT(f"#{k}", END - 2.6)
    POP("#ask", END - 2.4, 0.6); snd("tap", END - 2.4, -6)
    css = f"""
@font-face {{ font-family:"FR"; src:url("assets/fredoka-latin-700-normal.woff2"); font-weight:700; }}
@font-face {{ font-family:"FR"; src:url("assets/fredoka-latin-600-normal.woff2"); font-weight:600; }}
@font-face {{ font-family:"AR"; src:url("assets/ibm-plex-sans-arabic-arabic-700-normal.woff2"); }}
@font-face {{ font-family:"AN"; src:url("assets/anton-latin-400-normal.woff2"); }}
* {{ margin:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; font-family:FR; font-weight:700; color:{PAPER};
  background:linear-gradient(#1d3b40 0%, #17262B 45%, #1a3a3c 100%); }}
#cam {{ position:absolute; inset:0; }}
.glow {{ position:absolute; border-radius:50%; filter:blur(70px); opacity:.45; }}
#logo {{ position:absolute; top:58px; left:0; right:0; display:flex; justify-content:center; gap:12px; align-items:center; }}
#logo .tile {{ position:relative; width:56px; height:56px; border-radius:16px; background:{PAPER}; display:grid; place-items:center; }}
#logo .tile span {{ font-family:AR; font-size:36px; color:{INK}; margin-top:-4px; }} #logo .tile em {{ position:absolute; right:9px; top:8px; width:9px; height:9px; border-radius:50%; background:{RED}; }}
#logo b {{ font-family:AR; font-size:42px; }}
#stop {{ position:absolute; top:330px; left:0; right:0; text-align:center; font-family:AN; font-size:220px; color:{RED}; text-shadow:0 10px 0 #5c1712; }}
#title {{ position:absolute; top:300px; left:0; right:0; text-align:center; font-size:110px; line-height:1.05; opacity:0; }}
#title span {{ color:{GOLD}; }}
#sub {{ position:absolute; top:560px; left:0; right:0; text-align:center; font-size:54px; color:#cfe3dc; opacity:0; }}
.q {{ position:absolute; inset:0; opacity:0; }}
.cnt {{ position:absolute; top:150px; left:0; right:0; text-align:center; }} .cnt {{ font-size:40px; color:{GOLD}; letter-spacing:.1em; }}
.qt {{ position:absolute; top:215px; left:60px; right:60px; text-align:center; font-size:66px; line-height:1.1; }} .qt b {{ color:{GOLD}; }}
.w {{ position:absolute; top:330px; left:0; right:0; text-align:center; font-size:190px; line-height:1.2; color:#fff; text-shadow:0 8px 0 {TEAL}; opacity:0; }}
.w small {{ display:block; font-family:FR; font-size:46px; color:#cfe3dc; text-shadow:none; margin-top:-10px; }}
.ar {{ font-family:AR; direction:rtl; }}
.ops {{ position:absolute; top:690px; left:60px; right:60px; display:grid; grid-template-columns:1fr 1fr; gap:22px; }}
.ops.big {{ top:430px; }}
.op {{ background:{PAPER}; color:{INK}; border-radius:28px; padding:18px 10px; text-align:center; font-size:50px; box-shadow:0 10px 0 rgba(0,0,0,.35); opacity:0; }}
.ops.big .op {{ padding:26px 10px 18px; }} .ops.big .op b {{ font-size:110px; line-height:1.2; }}
.op small {{ display:block; font-size:34px; color:#5c6e70; font-weight:600; }}
.tm {{ position:absolute; top:1030px; left:46px; width:130px; height:130px; opacity:0; }}
.tm svg {{ width:130px; height:130px; transform:rotate(-90deg); }} .trk {{ fill:rgba(0,0,0,.4); stroke:rgba(241,236,224,.2); stroke-width:10; }}
.arc {{ fill:none; stroke:{GOLD}; stroke-width:10; stroke-linecap:round; stroke-dasharray:1; }}
.tm b {{ position:absolute; inset:0; display:grid; place-items:center; font-size:62px; color:{GOLD}; }}
.note {{ position:absolute; top:636px; left:60px; right:60px; text-align:center; font-size:32px; font-weight:600; color:#cfe3dc; opacity:0; }}
.note i {{ color:{GOLD}; }}
#ask {{ position:absolute; top:430px; left:80px; right:80px; text-align:center; font-size:88px; line-height:1.1; background:{GOLD}; color:{INK}; border-radius:40px; padding:30px; opacity:0; box-shadow:0 14px 0 rgba(0,0,0,.35); }}
"""
    page = f"""<div id="cam"><i class="glow" style="left:-160px;top:-120px;width:620px;height:620px;background:{TEAL}"></i><i class="glow" style="right:-200px;top:200px;width:560px;height:560px;background:#5a3d7a"></i><i class="glow" style="left:240px;top:1180px;width:620px;height:620px;background:{TEAL};opacity:.5"></i><i class="glow" style="left:-220px;top:1500px;width:520px;height:520px;background:#5a3d7a;opacity:.35"></i>
<div id="logo"><span class="tile"><span>ر</span><em></em></span><b>رَفِيق</b></div>
<div id="stop">STOP!</div><div id="title">WEEKLY <span>ARABIC</span><br>QUIZ</div><div id="sub">Words you'll find all over the Qur'an</div>
{chr(10).join(body)}
<div id="ask">How many did you get?<br>Comment /5 👇</div></div>"""
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html><html><head><meta charset="UTF-8"><style>{css}</style><script src="assets/gsap.min.js"></script></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{END}">{page}</div>
<script>const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;</script></body></html>""")
    json.dump(S, open(os.path.join(W, "sfx.json"), "w"))
    return out

def mix():
    """His voice as recorded + the effects, each set against his voice's loudest 50 ms (VP), pre-mixed into one track."""
    sys.path.insert(0, os.path.join(ROOT, "brag-quiz/reels/template")); from sfx_rules import info
    rd = lambda f, sr=48000: np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "2", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout, np.float32).reshape(-1, 2)
    v = rd(SRC); m = v.mean(1)
    VP = float(np.percentile(20 * np.log10(np.sqrt(np.convolve(m ** 2, np.ones(2400) / 2400, "valid"))[::1200] + 1e-9), 90))
    out = np.zeros((int(END * 48000), 2), np.float32); out[:len(v)] += v[:len(out)]
    for name, t, db in json.load(open(os.path.join(W, "sfx.json"))):
        f = name if os.path.isabs(name) else next(os.path.join(SFX, d, name + ".wav") for d in ("soft", "ref", ".") if os.path.exists(os.path.join(SFX, d, name + ".wav")))
        pk_db, pk = info(f); x = rd(f) * 10 ** ((VP + db - pk_db) / 20)
        i = max(0, int((t - (0 if os.path.isabs(name) else pk)) * 48000)); j = min(len(out), i + len(x)); out[i:j] += x[:j - i]   # a voice starts at t; an effect peaks there
    out.tofile(os.path.join(W, "mix.f32"))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", "48000", "-ac", "2", "-i", os.path.join(W, "mix.f32"), "-af",
                    "lowpass=f=16000:poles=2,aresample=192000,alimiter=limit=0.8:attack=1:release=60:level=false,aresample=48000", os.path.join(W, "mix.wav")], check=True)
    return VP

def matte(w=660, h=1174):
    """His cut-out with alpha. Only the black joined to the frame's edges is background (his own removal left it pure black); dark
    parts inside his outline (pupils, nostrils, beard, the shadows on his top) stay solid, which a plain black key punched through."""
    from scipy import ndimage
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", SRC, "-vf", f"fps=30,scale={w}:{h}", "-pix_fmt", "rgb24", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{w}x{h}", "-r", "30", "-i", "-",
                            "-c:v", "qtrle", os.path.join(W, "me.mov")], stdin=subprocess.PIPE)
    n = w * h * 3
    x = np.arange(w); RAMP = np.clip(np.minimum(x, w - 1 - x) / 70, 0, 1)[None, :] ** 1.5
    while True:
        buf = dec.stdout.read(n)
        if len(buf) < n: break
        f = np.frombuffer(buf, np.uint8).reshape(h, w, 3)
        dark = f.astype(np.int16).sum(2) < 24
        lab, _ = ndimage.label(dark)
        edge = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])); edge = edge[edge > 0]
        bg = np.isin(lab, edge)
        fg = ndimage.binary_erosion(~bg, iterations=2)                    # in by 2 px: the light fringe his removal left round his hair goes
        a = ndimage.gaussian_filter(fg.astype(np.float32), 1.2) * RAMP     # a soft edge; his shoulders fade where his camera's frame cut them
        enc.stdin.write(np.dstack([f, (a * 255).clip(0, 255).astype(np.uint8)]).tobytes())
    enc.stdin.close(); enc.wait(); dec.wait()

if __name__ == "__main__":
    out = build()
    if os.environ.get("BUILD_ONLY"): sys.exit()
    subprocess.run(["npx", "-y", "hyperframes", "render", "-o", os.path.join(W, "bg.mp4")], cwd=out, check=True, capture_output=True)
    mix()
    dst = os.path.join(ROOT, "brag-quiz/out/quiz"); os.makedirs(dst, exist_ok=True)
    matte()
    # him: a cut-out floating over the full-screen quiz page (owner, 30 Oct: "one thing, and I'm just an overlay"), in the bottom half;
    # his last frame holds to the end
    fc = (f"[1:v]tpad=stop_mode=clone:stop_duration={END:.2f},trim=0:{END},setpts=PTS-STARTPTS[me];[0:v][me]overlay=x=(W-w)/2:y=H-h+10:format=auto,format=yuv420p[v]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(W, "bg.mp4"), "-i", os.path.join(W, "me.mov"), "-i", os.path.join(W, "mix.wav"), "-filter_complex", fc,
                    "-map", "[v]", "-map", "2:a", "-t", str(END), "-c:v", "libx264", "-crf", "17", "-preset", "slow", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
                    os.path.join(dst, "quiz-1030.mp4")], check=True)
    print("done", os.path.join(dst, "quiz-1030.mp4"))
