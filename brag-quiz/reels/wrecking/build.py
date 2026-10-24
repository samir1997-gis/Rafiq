#!/usr/bin/env python3
"""The wrecking-ball reel (owner, 23 Oct 2026), in the style of a reference he sent (@aperturemotion's "a wrecking ball that was never
there"): 8 s of a wrecking ball swinging at a wall, no voice, a FRAMES TO IMPACT counter and a building bed; it freezes before impact
and a calm narrator (George, a soft chuckle) says the reference's line; the scene turns to a blueprint. Then ours: "if you can watch
that for seven seconds, you can watch this for another fifteen"; Arabic is the key (a gold key unlocks a door onto light: every word
of your salah, the Qur'an in its own language (Yūsuf 12:2), your du'a); without Arabic, a book in the dark (the door slams); "so unlock
it, RafiqArabic.com". Our colours; the wall is rubric bricks with ر on it. Sounds made for this (brag-quiz/sfx/soft: drone, shimmer,
darkhum) plus our library. Voice: brag-quiz/voice/wrecking-lines.json (b1: Brian, the hook to compare).

  python3 brag-quiz/reels/wrecking/build.py [b1]   then  cd brag-quiz/reels/wrecking/out/v && npx hyperframes render -o ../wrecking.mp4
"""
import json, math, os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
V6 = os.path.join(ROOT, "brag-output-v6/composition/assets"); VO = os.path.join(ROOT, "brag-quiz/voice/wrecking")
INK, CREAM, GOLD, GOLD2, RED, TEAL, DARK = "#17262b", "#f1ece0", "#a8842c", "#E9B949", "#B4322A", "#2e7263", "#0c1214"
VOICE = sys.argv[1] if len(sys.argv) > 1 else "b"                                                # b: Brian (owner's pick), w: George
dur = lambda f: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
src = lambda n: os.path.join(VO, VOICE + n[1:])                                                    # line "w3" → its recording in this voice
words = lambda n: json.load(open(src(n) + ".words.json"))
FREEZE = 8.1
GAP = {"w2": .35, "w3": .21, "w4": .27, "w5": .31, "w6": .28}                                        # the pause before each line
L = {"w1": 8.2}
for n in GAP: p = f"w{int(n[1]) - 1}"; L[n] = round(L[p] + dur(src(p) + ".mp3") + GAP[n], 2)       # when each line starts
def at(n, key, last=False):                                                                         # when line n says the word with key in it
    hits = [s for w, s, e in words(n) if key in w.lower()]
    return L[n] + (hits[-1] if last else hits[0])
END = round(L["w6"] + dur(src("w6") + ".mp3") + 1.2, 2)
PIV, R, BR = (450, -900), 2150, 130                       # the pendulum: pivot high above, a long chain, so the ball arrives mid-wall
TH0, THC = -36.0, 1.07                                    # the ball comes in from far up-left (off screen); THC: where it would touch
N0, T0 = 204, 0.3                                         # as in the reference: 204 frames to impact, falling by ~12% every quarter second
KF = math.log(N0 / 6) / (FREEZE - T0)                     # (204 → 105 in 1.5 s, then a crawl down to 006 at the freeze)
WX0, WX1, WY = 620, 880, 900                              # the wall: left, right, top (11 rows of bricks below)
CAM0, CAM1 = (400, 1130, 0.45), (545, 1225, 1.35)         # the camera: wide on the wall, zooming in steadily the whole way

def build():
    out = os.path.join(HERE, "out", "v"); a = os.path.join(out, "assets")
    if os.path.exists(out): shutil.rmtree(out)
    os.makedirs(a)
    for f in ("ibm-plex-sans-arabic-arabic-700-normal.woff2", "karla-latin-500-normal.woff2", "karla-latin-700-normal.woff2"): shutil.copy(os.path.join(V6, "fonts", f), a)
    shutil.copy(os.path.join(ROOT, "brag-quiz/fonts/instrument-serif-latin-400-normal.woff2"), a); shutil.copy(os.path.join(V6, "lib/gsap.min.js"), a)
    for f in os.listdir(os.path.join(ROOT, "brag-quiz/sfx/soft")): shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/soft", f), a)
    for f in ("swoosh.wav", "swoosh-low.wav", "click.wav", "tap.wav"): shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/ref", f), a)
    shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/boom.wav"), a)
    for n in L: shutil.copy(src(n) + ".mp3", os.path.join(a, n + ".mp3"))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", os.path.join(V6, "sfx-gen/fountain.mp3"), "-af",
                    f"volume=6dB,atrim=0:{END - FREEZE},afade=t=in:d=1.0,afade=t=out:st={END - FREEZE - 1.5}:d=1.5", "-c:a", "libmp3lame", "-q:a", "3", os.path.join(a, "bed.mp3")], check=True)
    au = []
    def snd(name, t0, vol, d=None, track=None):
        d = d or dur(os.path.join(a, name))
        au.append(f'<audio id="s{len(au)}" src="assets/{name}" data-start="{max(0, t0):.3f}" data-duration="{d:.3f}" data-volume="{vol:.3f}" data-track-index="{track or 3 + len(au)}"></audio>')
    for n, t0 in L.items(): snd(f"{n}.mp3", t0, 1.0, track=1)
    snd("bed.mp3", FREEZE, 0.06, END - FREEZE, track=2)                                    # a very quiet bed under the voice, so nothing is ever silent
    js = []; T = js.append

    # 1 · the swing (0-8.1), timed like the reference: the wall alone, then the ball rushes in from off screen and covers most of the
    # way at once; it then crawls, the gap shrinking by the same share every moment (so the counter falls fast, then barely), and it
    # stops just short of touching. The camera zooms in steadily throughout.
    T(f'''(() => {{ const o = {{t:0}}, ch = document.getElementById("chain"), ch2 = document.getElementById("chain2"), b = document.getElementById("ball"),
        sh = document.getElementById("bshadow"), n = document.getElementById("cnum"), cam = document.getElementById("cam");
      const draw = (t) => {{ const f = Math.exp(-{KF:.4f} * Math.max(0, t - {T0})), g = {THC - TH0 - 8} * Math.pow(f, 3) + 8 * f;   // the gap, in degrees
        const th = ({THC} - g) * Math.PI / 180, x = {PIV[0]} + {R} * Math.sin(th), y = {PIV[1]} + {R} * Math.cos(th);
        for (const c of [ch, ch2]) {{ c.setAttribute("x2", x); c.setAttribute("y2", y - {BR}); }}
        b.setAttribute("transform", `translate(${{x}},${{y}})`); sh.setAttribute("cx", x);
        const u = Math.min(1, t / {FREEZE}), k = u, cx = {CAM0[0]} + ({CAM1[0]} - {CAM0[0]}) * k, cy = {CAM0[1]} + ({CAM1[1]} - {CAM0[1]}) * k, sc = {CAM0[2]} + ({CAM1[2]} - {CAM0[2]}) * k;
        cam.style.transform = `translate(${{540 - cx * sc}}px, ${{960 - cy * sc}}px) scale(${{sc}})`;
        const v = Math.max(6, Math.round({N0} * f)); n.textContent = String(v).padStart(3, "0"); n.style.color = v <= 30 ? "{RED}" : "{INK}"; }};
      draw(0); tl.to(o, {{t:{FREEZE}, duration:{FREEZE}, ease:"none", onUpdate:() => draw(o.t)}}, 0); }})();''')
    snd("drone.wav", 0, 0.55, FREEZE)
    snd("swoosh.wav", T0 - 0.05, 0.55); snd("swoosh-low.wav", T0 + 0.35, 0.4)                          # it rushes in, then slows
    last = -1                                                                                        # a tick each time the counter drops,
    for m in range(N0 - 1, 5, -1):                                                                   # as fast as a buzz at first
        t = T0 + math.log(N0 / (m + 0.5)) / KF
        if t - last >= 0.07 and t < FREEZE: snd("tick.wav", t, 0.09); last = t
    T(f'tl.to("#counter", {{opacity:0, y:-20, duration:0.3}}, {L["w1"] - 0.1:.2f});')
    # 2 · the line (the reference's), and the blueprint on "never"
    nv = at("w1", "never")
    T(f'tl.to(["#wall", "#ballfill", "#chainfill"], {{opacity:0, duration:0.5}}, {nv:.2f});')
    T(f'tl.fromTo(["#bp", "#grid"], {{opacity:0}}, {{opacity:1, duration:0.5}}, {nv:.2f});')
    T(f'tl.fromTo(".note", {{opacity:0, x:-14}}, {{opacity:1, x:0, duration:0.4, stagger:0.25}}, {nv + 0.3:.2f});'); snd("tap.wav", nv, 0.25); snd("tap.wav", nv + 0.3, 0.2)
    # 3 · "…another fifteen": a thin ring starts filling to the end, the blueprint whips away
    ff = at("w2", "", last=True)
    T(f'tl.fromTo("#ring", {{opacity:0, scale:0.6}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, {ff:.2f});')
    T(f'tl.fromTo("#ring .fg", {{strokeDashoffset:251}}, {{strokeDashoffset:0, duration:{END - ff - 0.3:.2f}, ease:"none"}}, {ff:.2f});'); snd("click.wav", ff, 0.4)
    T(f'tl.to("#s1", {{x:-700, opacity:0, filter:"blur(18px)", duration:0.35, ease:"power3.in"}}, {L["w3"] - 0.4:.2f});'); snd("swoosh.wav", L["w3"] - 0.45, 0.35)
    # 4 · the key and the door
    T(f'tl.fromTo("#s2", {{opacity:0, x:700, filter:"blur(18px)"}}, {{opacity:1, x:0, filter:"blur(0px)", duration:0.4, ease:"power3.out"}}, {L["w3"] - 0.1:.2f});')
    ky, un = at("w3", "key"), at("w3", "unlock")
    T(f'tl.fromTo("#key", {{x:380, y:560, rotation:-35, opacity:0}}, {{x:0, y:0, rotation:0, opacity:1, duration:0.6, ease:"power3.out"}}, {ky - 0.45:.2f});'); snd("swoosh-low.wav", ky - 0.45, 0.3)
    T(f'tl.to("#key", {{rotation:90, duration:0.3, ease:"back.out(2)"}}, {un:.2f});'); snd("click.wav", un + 0.05, 0.9); snd("tick-lo.wav", un + 0.12, 0.6)
    T(f'tl.to("#leaf", {{rotationY:-105, duration:1.1, ease:"power2.inOut"}}, {un + 0.4:.2f});'); T(f'tl.to("#key", {{opacity:0, duration:0.3}}, {un + 0.4:.2f});')
    T(f'tl.fromTo("#glow", {{opacity:0, scale:0.6}}, {{opacity:1, scale:1.25, duration:1.4, ease:"power2.out"}}, {un + 0.5:.2f});'); snd("shimmer.wav", un + 0.45, 0.9)
    # 5 · through the door into the light: salah, the Qur'an (12:2), your du'a
    T(f'tl.to("#door", {{scale:7, duration:1.1, ease:"power2.in", transformOrigin:"540px 900px"}}, {L["w4"]:.2f});'); snd("swoosh.wav", L["w4"] + 0.4, 0.35)
    T(f'tl.fromTo("#light", {{opacity:0}}, {{opacity:1, duration:0.6}}, {L["w4"] + 0.6:.2f});')
    for i, k in enumerate(("salah", "qur", "du")):                                   # salah · Qur'an · du'a
        t0 = at("w4", k) - 0.1
        T(f'tl.fromTo("#c{i}", {{opacity:0, y:60, scale:0.92, filter:"blur(10px)"}}, {{opacity:1, y:0, scale:1, filter:"blur(0px)", duration:0.6, ease:"power3.out"}}, {t0:.2f});')
        snd("tick.wav", t0 + 0.05, 0.35); snd("shimmer.wav", t0, 0.25, 1.4)
    # 6 · the door slams: the dark, a book you can barely see; its last glow goes out on "dark"
    T(f'tl.set("#s3", {{opacity:1}}, {L["w5"] - 0.05:.2f});'); T(f'tl.set(["#s2", "#light"], {{opacity:0}}, {L["w5"] - 0.05:.2f});')
    snd("boom.wav", L["w5"] - 0.05, 0.7); snd("thump.wav", L["w5"] - 0.05, 0.8); snd("darkhum.wav", L["w5"], 0.35)
    T(f'tl.fromTo("#s3", {{x:-18}}, {{x:0, duration:0.3, ease:"elastic.out(1, 0.3)"}}, {L["w5"]:.2f});')
    T(f'tl.fromTo("#lamp", {{opacity:0.9, scale:1}}, {{opacity:0.35, scale:0.7, duration:{at("w5", "dark") - L["w5"]:.2f}, ease:"power1.in"}}, {L["w5"]:.2f});')
    T(f'tl.to("#lamp", {{opacity:0, duration:0.4}}, {at("w5", "dark"):.2f});'); T(f'tl.to("#book", {{opacity:0.25, duration:0.5}}, {at("w5", "dark"):.2f});')
    # 7 · "so… unlock it": the key glows in the dark, turns; a line of light opens onto RafiqArabic.com
    T(f'tl.fromTo("#key2", {{opacity:0, scale:0.6}}, {{opacity:1, scale:1, duration:0.5, ease:"back.out(2)"}}, {L["w6"] + 0.1:.2f});'); snd("shimmer.wav", L["w6"] + 0.1, 0.4, 1.5)
    u2, url = at("w6", "unlock"), at("w6", "raf")
    T(f'tl.to("#key2", {{rotation:90, duration:0.3, ease:"back.out(2)"}}, {u2:.2f});'); snd("click.wav", u2 + 0.05, 0.9)
    T(f'tl.fromTo("#crack", {{scaleX:0, opacity:0}}, {{scaleX:1, opacity:1, duration:0.5, ease:"power3.out"}}, {u2 + 0.35:.2f});')
    T(f'tl.to("#crack", {{scaleY:520, duration:0.7, ease:"power2.in"}}, {u2 + 0.85:.2f});'); T(f'tl.to("#key2", {{opacity:0, duration:0.3}}, {u2 + 0.9:.2f});')
    snd("swoosh.wav", u2 + 0.8, 0.35)
    T(f'tl.fromTo("#cta", {{opacity:0, scale:0.9}}, {{opacity:1, scale:1, duration:0.5, ease:"back.out(1.8)"}}, {url - 0.1:.2f});'); snd("tick-lo.wav", url, 0.6)
    # the narration, word by word, small and quiet under the picture (as in the reference)
    caps = []
    for n in L:
        for i, (w, s, e) in enumerate(words(n)):
            w = {"7": "seven", "15.": "fifteen.", "dua,": "du'a,", "Qur": "Qur'an,", "'an,": "", "du": "du'a,", "'a,": "", "Quran": "Qur'an,", "rafigarabic": "RafiqArabic.com", ".com": "", "Salah,": "salah,"}.get(w, w)
            if w: caps.append((n, w, L[n] + s))
    lines, cur = [], []
    for k, (n, w, s) in enumerate(caps):                               # lines break at punctuation, each line replaces the last
        cur.append((w, s))
        if w[-1] in ",.:?" or len(cur) >= 6 or k + 1 == len(caps) or caps[k + 1][0] != n: lines.append(cur); cur = []
    cap_html = ""
    for j, ln in enumerate(lines):
        nxt = lines[j + 1][0][1] if j + 1 < len(lines) else END
        cap_html += f'<div class="cap" id="l{j}">' + " ".join(f'<span class="cw" id="l{j}w{i}">{w}</span>' for i, (w, s) in enumerate(ln)) + "</div>"
        for i, (w, s) in enumerate(ln): T(f'tl.fromTo("#l{j}w{i}", {{opacity:0, y:8, filter:"blur(6px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.3}}, {s:.2f});')
        T(f'tl.to("#l{j}", {{opacity:0, duration:0.2}}, {min(nxt, ln[-1][1] + 2.5) - 0.05:.2f});')
    T(f'tl.set(".cap", {{color:"{CREAM}"}}, {L["w5"] - 0.05:.2f});')    # in the dark, the words go light
    T(f'tl.set(".cap", {{color:"#5a5f60"}}, {at("w6", "unlock") + 1.0:.2f});')      # and dark again once the light floods back in

    bricks = ""
    for r in range(11):
        for c in range(-1, 3):
            x = WX0 + c * 128 + (64 if r % 2 else 0); col = ("#B4322A", "#c8473d", "#a32c25", "#bd3a30")[(r * 3 + c) % 4]
            x0, x1 = max(x, WX0), min(x + 120, WX1)
            if x1 - x0 > 8: bricks += f'<rect x="{x0}" y="{WY + r * 56}" width="{x1 - x0}" height="50" rx="4" fill="{col}"/>'
    bp_bricks = bricks.replace('fill="#', 'fill="none" stroke="#5f7d86" stroke-width="2.5" data-c="#')
    grid = "".join(f'<line x1="{x}" y1="-1200" x2="{x}" y2="3200"/>' for x in range(-1800, 2401, 60)) + "".join(f'<line x1="-1800" y1="{y}" x2="2400" y2="{y}"/>' for y in range(-1200, 3201, 60))
    css = f"""
@font-face {{ font-family:"SE"; src:url("assets/instrument-serif-latin-400-normal.woff2"); }}
@font-face {{ font-family:"KA"; src:url("assets/karla-latin-500-normal.woff2"); font-weight:500; }}
@font-face {{ font-family:"KA"; src:url("assets/karla-latin-700-normal.woff2"); font-weight:700; }}
@font-face {{ font-family:"AR"; src:url("assets/ibm-plex-sans-arabic-arabic-700-normal.woff2"); }}
* {{ margin:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:{CREAM}; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:{CREAM}; }}
.sc {{ position:absolute; inset:0; }} #cam {{ transform-origin:0 0; }} svg.full {{ position:absolute; inset:0; width:1080px; height:1920px; overflow:visible; }}
#grid line {{ stroke:#c9d3d4; stroke-width:1.2; }} #bp {{ opacity:0; }}
#counter {{ position:absolute; left:0; right:0; top:1440px; text-align:center; font-family:KA; color:{INK}; }}
#counter small {{ display:block; font-size:24px; letter-spacing:.32em; font-weight:700; opacity:.55; }} #cnum {{ display:block; font-size:120px; font-weight:500; letter-spacing:.04em; }}
.note {{ position:absolute; font-family:KA; font-size:28px; letter-spacing:.06em; color:#5f7d86; }}
.cap {{ position:absolute; left:110px; right:110px; top:1500px; text-align:center; font-family:SE; font-size:52px; line-height:1.15; color:#5a5f60; }}
.cw {{ display:inline-block; opacity:0; }}
#ring {{ position:absolute; right:56px; top:120px; width:90px; height:90px; opacity:0; }} #ring svg {{ transform:rotate(-90deg); }}
#ring circle {{ fill:none; stroke-width:7; }} #ring .bg {{ stroke:rgba(23,38,43,.15); }} #ring .fg {{ stroke:{RED}; stroke-linecap:round; stroke-dasharray:251; }}
#s2 {{ opacity:0; }} #door {{ position:absolute; inset:0; perspective:1600px; }}
#frame {{ position:absolute; left:290px; top:470px; width:500px; height:860px; border-radius:250px 250px 14px 14px; background:#d9cfb8; border:14px solid #c4b69a; overflow:hidden; }}
#glow {{ position:absolute; inset:-200px; background:radial-gradient(circle at 50% 55%, #fffdf4 0 22%, #fff3c9 38%, rgba(233,185,73,.0) 70%); opacity:0; }}
#leaf {{ position:absolute; left:0; top:0; width:100%; height:100%; background:{INK}; border-radius:236px 236px 0 0; transform-origin:0 50%; }}
#leaf i {{ position:absolute; left:50px; right:50px; height:280px; border:5px solid #2c4048; border-radius:120px 120px 8px 8px; }} #leaf i + i {{ border-radius:8px; }}
#hole {{ position:absolute; right:52px; top:440px; width:30px; height:30px; border-radius:50%; background:{GOLD2}; box-shadow:0 0 18px rgba(233,185,73,.6); }}
#key, #key2 {{ position:absolute; width:260px; height:90px; transform-origin:30px 45px; }} #key {{ left:735px; top:868px; opacity:0; }}
#light {{ position:absolute; inset:0; opacity:0; background:radial-gradient(circle at 50% 40%, #fffef8, #fff6da 55%, #f6e3a8); }}
.card {{ position:absolute; left:90px; right:90px; padding:28px 34px; border-radius:36px; background:rgba(255,255,255,.75); border:4px solid {GOLD2}; text-align:center; opacity:0;
  box-shadow:0 20px 50px -24px rgba(168,132,44,.6); }} .card .ar {{ font-family:AR; font-size:60px; line-height:1.6; color:{INK}; direction:rtl; }}
.card .en {{ font-family:SE; font-style:italic; font-size:48px; color:{INK}; line-height:1.15; }} .card small {{ display:block; font-family:KA; font-weight:700; font-size:26px; letter-spacing:.12em; color:{GOLD}; margin-top:10px; }}
#s3 {{ background:{DARK}; opacity:0; }} #lamp {{ position:absolute; left:240px; top:620px; width:600px; height:600px; border-radius:50%; background:radial-gradient(circle, rgba(233,185,73,.28), rgba(233,185,73,0) 65%); }}
#book {{ position:absolute; left:250px; top:760px; width:580px; height:360px; opacity:.6; }}
#key2 {{ left:410px; top:860px; filter:drop-shadow(0 0 22px rgba(233,185,73,.9)); opacity:0; }}
#crack {{ position:absolute; left:0; right:0; top:958px; height:4px; background:#fff3c9; box-shadow:0 0 30px 8px rgba(233,185,73,.8); opacity:0; }}
#cta {{ position:absolute; left:0; right:0; top:760px; text-align:center; opacity:0; }} #cta .logo {{ display:inline-block; width:150px; height:150px; border-radius:36px; background:{INK};
  color:{CREAM}; font-family:AR; font-size:96px; line-height:150px; position:relative; }} #cta .logo i {{ position:absolute; right:22px; top:20px; width:18px; height:18px; border-radius:50%; background:{RED}; }}
#cta .url {{ display:inline-block; margin-top:44px; padding:22px 54px; border-radius:999px; background:{TEAL}; color:{CREAM}; font-family:KA; font-weight:700; font-size:60px; }}
#cta small {{ display:block; margin-top:22px; font-family:KA; font-size:34px; color:{INK}; opacity:.7; }}
"""
    keysvg = (f'<svg viewBox="0 0 260 90" width="260" height="90"><circle cx="40" cy="45" r="32" fill="none" stroke="{GOLD2}" stroke-width="16"/>'
              f'<rect x="70" y="37" width="180" height="16" rx="6" fill="{GOLD2}"/><rect x="200" y="53" width="14" height="28" rx="3" fill="{GOLD2}"/>'
              f'<rect x="226" y="53" width="14" height="20" rx="3" fill="{GOLD2}"/></svg>')
    body = f"""
<div class="sc" id="s1"><div class="sc" id="cam">
  <svg class="full" viewBox="0 0 1080 1920"><g id="grid">{grid}</g></svg>
  <svg class="full" viewBox="0 0 1080 1920" id="wall"><ellipse cx="{(WX0 + WX1) // 2}" cy="{WY + 625}" rx="230" ry="22" fill="rgba(23,38,43,.16)"/>{bricks}
    <text x="{(WX0 + WX1) // 2}" y="{WY + 360}" text-anchor="middle" font-family="AR" font-size="230" fill="rgba(241,236,224,.82)">ر</text></svg>
  <svg class="full" viewBox="0 0 1080 1920"><ellipse id="bshadow" cx="300" cy="{WY + 628}" rx="120" ry="16" fill="rgba(23,38,43,.14)"/>
    <g id="chainfill"><line id="chain" x1="{PIV[0]}" y1="{PIV[1]}" x2="300" y2="500" stroke="#2b2f31" stroke-width="16" stroke-dasharray="30 12"/>
      <line id="chain2" x1="{PIV[0]}" y1="{PIV[1]}" x2="300" y2="500" stroke="#454a4c" stroke-width="8" stroke-dasharray="12 30" stroke-dashoffset="21"/></g>
    <g id="ball"><g id="ballfill"><defs><radialGradient id="bg1" cx="35%" cy="30%" r="75%"><stop offset="0" stop-color="#5a6063"/><stop offset=".45" stop-color="#1d2224"/><stop offset="1" stop-color="#050707"/></radialGradient></defs>
      <rect x="-22" y="-{BR + 26}" width="44" height="40" rx="8" fill="#2b2f31"/><circle r="{BR}" fill="url(#bg1)"/><ellipse cx="-44" cy="-56" rx="30" ry="18" fill="rgba(255,255,255,.18)" transform="rotate(-30)"/></g>
      <circle r="{BR}" fill="none" stroke="#5f7d86" stroke-width="3" class="bpo" opacity="0"/><path d="M-{BR} 0 H{BR} M0 -{BR} V{BR}" stroke="#5f7d86" stroke-width="1.5" stroke-dasharray="8 8" class="bpo" opacity="0"/></g></svg>
  <svg class="full" viewBox="0 0 1080 1920" id="bp"><g>{bp_bricks}</g><line x1="-1800" y1="{WY + 630}" x2="2400" y2="{WY + 630}" stroke="#5f7d86" stroke-width="2"/></svg>
</div>
  <div class="note" style="left:80px;top:250px">time to impact = never</div><div class="note" style="left:80px;top:300px">distance to impact = ∞</div>
  <div class="note" style="left:640px;top:250px">attention = held</div>
  <div id="counter"><small>FRAMES TO IMPACT</small><b id="cnum">204</b></div>
</div>
<div class="sc" id="s2"><div id="door"><div id="frame"><div id="glow"></div><div id="leaf"><i style="top:60px"></i><i style="top:400px;height:330px"></i><div id="hole"></div></div></div></div>
  <div id="key">{keysvg}</div>
  <div id="light"></div>
  <div class="card" id="c0" style="top:330px"><div class="ar">سُبْحانَ رَبِّيَ الْأَعْلى</div><div class="en">every word of your salah</div></div>
  <div class="card" id="c1" style="top:720px"><div class="ar">إِنّا أَنْزَلْناهُ قُرْآنًا عَرَبِيًّا لَعَلَّكُمْ تَعْقِلُونَ</div><div class="en">“We sent it down as an Arabic Qur’an so that you may understand”</div><small>YŪSUF 12:2</small></div>
  <div class="card" id="c2" style="top:1180px"><div class="ar">رَبَّنا آتِنا فِي الدُّنْيا حَسَنَةً</div><div class="en">your du’a, finally understood</div></div>
</div>
<div class="sc" id="s3"><div id="lamp"></div>
  <svg id="book" viewBox="0 0 580 360"><path d="M290 40 C200 10 90 10 20 40 V330 C90 300 200 300 290 330 Z" fill="#1d2629" stroke="#2c3a3e" stroke-width="4"/>
    <path d="M290 40 C380 10 490 10 560 40 V330 C490 300 380 300 290 330 Z" fill="#1d2629" stroke="#2c3a3e" stroke-width="4"/>
    {''.join(f'<rect x="{x}" y="{80 + k * 34}" width="{w}" height="10" rx="5" fill="#2f3d41"/>' for k in range(7) for x, w in ((60, 190 - (k * 17) % 50), (330, 190 - (k * 23) % 60)))}</svg>
  <div id="key2">{keysvg}</div><div id="crack"></div>
  <div id="cta"><div class="logo">ر<i></i></div><br><div class="url">rafiqarabic.com</div><small>7 days free · no card needed</small></div>
</div>
<div id="ring"><svg viewBox="0 0 90 90" width="90" height="90"><circle class="bg" cx="45" cy="45" r="40"/><circle class="fg" cx="45" cy="45" r="40"/></svg></div>
{cap_html}"""
    js.append(f'tl.to(".bpo", {{opacity:1, duration:0.5}}, {nv:.2f});')
    js.append(f'tl.set("#cta", {{opacity:1}}, {END - 0.01:.2f});')
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><title>wrecking</title>
<script src="assets/gsap.min.js"></script><style>{css}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{END}">
{body}
{chr(10).join(au)}
</div><script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;</script></body></html>
""")
    print("built", END, "s,", len(au), "sounds; voice", VOICE, L)

if __name__ == "__main__":
    build()
