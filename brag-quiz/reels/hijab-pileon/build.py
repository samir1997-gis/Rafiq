#!/usr/bin/env python3
"""The animation for the hijab pile-on (owner, 27 Oct 2026, #302): a hijabi stands in the middle of a dark stage; an old woman shouts
"We need to ban the hijab!" (her mouth follows the shout); a spotlight clunks on over the hijabi and she looks distressed (brows up,
mouth down, hands clasp, she shrinks and trembles, a tear); then people join on their own "hijab" in the audio, one by one, then faster,
each shouting with a bubble, until a crowd surrounds her shouting over each other, the camera pushing in, and it cuts dead to black.
Every call is placed from the mixer's timings (brag-quiz/out/hijab/hijab-pileon.times.json, written by mix.py). Easing as
MOTION-STYLE.md: entrances ease out, exits ease in, pops spring with a slight overshoot, nothing linear.

  python3 brag-quiz/reels/hijab-pileon/mix.py && python3 brag-quiz/reels/hijab-pileon/build.py
  then  cd brag-quiz/reels/hijab-pileon/out/v && npx hyperframes render -o ../hijab-pileon-raw.mp4"""
import json, os, random, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
V6 = os.path.join(ROOT, "brag-output-v6/composition/assets"); OUTA = os.path.join(ROOT, "brag-quiz/out/hijab")
INK, CREAM, GOLD, RED, TEAL = "#17262B", "#F1ECE0", "#E9B949", "#B4322A", "#2E7263"
D = json.load(open(os.path.join(OUTA, "hijab-pileon.times.json"))); END, CALLS, BAN = D["end"], D["calls"], D["ban"]
rnd = random.Random(3)
js, T = [], None
T = js.append

def person(id, x, feet, s, d, body, face, hair, light):
    """A standing figure facing the middle (d = 1 faces right): its feet at (x, feet), s its scale, light its brightness."""
    w, h = 200 * s, 480 * s
    hairp = rnd.choice([f'<path d="M52 92 C 52 30, 148 30, 148 92 C 130 62, 70 62, 52 92 Z" fill="{hair}"/>',
                        f'<path d="M50 100 C 40 30, 160 30, 150 100 L 150 70 C 120 50, 80 50, 50 70 Z" fill="{hair}"/>',
                        f'<path d="M56 80 C 70 40, 130 40, 144 80 Z" fill="{hair}"/><circle cx="100" cy="42" r="14" fill="{hair}"/>'])
    ex = 8 * d
    return f'''<div class="p" id="{id}" style="left:{x - w / 2:.0f}px;top:{feet - h:.0f}px;width:{w:.0f}px;height:{h:.0f}px;filter:brightness({light})">
<svg viewBox="0 0 200 480" width="{w:.0f}" height="{h:.0f}"><g id="{id}g">
 <rect x="68" y="330" width="26" height="150" rx="10" fill="#141c20"/><rect x="106" y="330" width="26" height="150" rx="10" fill="#141c20"/>
 <path d="M48 345 L 60 172 Q 100 140 140 172 L 152 345 Z" fill="{body}"/>
 <g id="{id}a"><path d="M100 178 L {100 + 128 * d} 172" stroke="{body}" stroke-width="26" stroke-linecap="round"/><circle cx="{100 + 132 * d}" cy="172" r="14" fill="{face}"/></g>
 <circle cx="100" cy="95" r="48" fill="{face}"/>{hairp}
 <ellipse cx="{86 + ex}" cy="94" rx="5" ry="6" fill="#111"/><ellipse cx="{114 + ex}" cy="94" rx="5" ry="6" fill="#111"/>
 <path d="M{76 + ex} {80 + 4 * d} L {94 + ex} {84 - 4 * d} M {106 + ex} {84 + 4 * d} L {124 + ex} {80 - 4 * d}" stroke="#111" stroke-width="5" stroke-linecap="round"/>
 <ellipse id="{id}m" cx="{100 + ex}" cy="122" rx="13" ry="3" fill="#3a1010"/>
</g></svg></div>'''

def build():
    out = os.path.join(HERE, "out", "v"); a = os.path.join(out, "assets")
    if os.path.exists(out): shutil.rmtree(out)
    os.makedirs(a)
    shutil.copy(os.path.join(ROOT, "brag-quiz/fonts/anton-latin-400-normal.woff2"), a); shutil.copy(os.path.join(V6, "lib/gsap.min.js"), a)
    shutil.copy(os.path.join(OUTA, "hijab-pileon.wav"), os.path.join(a, "pile.wav")); shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/soft/thump.wav"), a)
    people, bubbles = [], []

    # 0-2.6 s · the old woman: lunges in, points, her mouth follows the shout; her words come up in a bubble
    people.append(person("ow", 300, 1440, 1.0, 1, "#8f2a24", "#e3bca2", "#cfcfcf", 0.8))
    T('tl.fromTo("#ow", {x:-40}, {x:0, duration:0.35, ease:"power3.out"}, 0.05);')
    T('tl.to("#owa", {rotation:-14, duration:0.25, ease:"back.out(1.4)", svgOrigin:"100 178"}, 0.15);')
    for i, v in enumerate(BAN): T(f'tl.set("#owm", {{attr:{{ry:{3 + 13 * v:.1f}}}}}, {i * 0.04:.2f});')
    T(f'tl.set("#owm", {{attr:{{ry:3}}}}, {len(BAN) * 0.04:.2f});')
    voiced = [i * 0.04 for i, v in enumerate(BAN) if v > 0.25]
    W = ["WE", "NEED", "TO", "BAN", "THE", "HIJAB!"]
    bw = ""
    for k, w in enumerate(W):
        tk = voiced[int(k * len(voiced) / len(W))]
        bw += f'<span id="bw{k}"{" class=r" if w in ("BAN", "HIJAB!") else ""}>{w}</span> '
        T(f'tl.fromTo("#bw{k}", {{opacity:0, scale:1.4}}, {{opacity:1, scale:1, duration:0.18, ease:"power3.out"}}, {tk:.2f});')
    T('tl.fromTo("#bigb", {opacity:0, scale:0.7}, {opacity:1, scale:1, duration:0.3, ease:"back.out(1.4)"}, 0.0);')
    T(f'tl.to("#bigb", {{opacity:0, y:-30, duration:0.3, ease:"power2.in"}}, {voiced[-1] + 0.35:.2f});')

    # 2.7 s · the spotlight clunks on; the room goes dark round her; she's distressed
    L0 = round(len(BAN) * 0.04 + 0.06, 2)
    for dt, o in ((0, 1), (0.06, 0.25), (0.12, 1)): T(f'tl.set("#spot", {{opacity:{o}}}, {L0 + dt:.2f});')
    T(f'tl.to("#dim", {{opacity:0.72, duration:0.15, ease:"power3.out"}}, {L0:.2f});')
    T(f'tl.to("#ow", {{filter:"brightness(0.45)", duration:0.2, ease:"power3.out"}}, {L0:.2f});')
    T(f'tl.to("#hjw", {{filter:"brightness(1.12)", duration:0.15, ease:"power3.out"}}, {L0:.2f});')
    dz = L0 + 0.25
    T(f'tl.to("#brL", {{rotation:-16, duration:0.35, ease:"power3.out", svgOrigin:"122 146"}}, {dz:.2f});')
    T(f'tl.to("#brR", {{rotation:16, duration:0.35, ease:"power3.out", svgOrigin:"178 146"}}, {dz:.2f});')
    T(f'tl.to("#mo1", {{opacity:0, duration:0.2, ease:"power2.in"}}, {dz:.2f});'); T(f'tl.to("#mo2", {{opacity:1, duration:0.25, ease:"power3.out"}}, {dz + 0.1:.2f});')
    T(f'tl.fromTo("#hands", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.45, ease:"power3.out"}}, {dz + 0.3:.2f});')
    T(f'tl.to("#hj", {{scale:0.92, y:10, duration:{END - dz - 1:.2f}, ease:"power2.inOut", transformOrigin:"50% 100%"}}, {dz:.2f});')   # she shrinks as it builds
    T(f'tl.fromTo("#tear", {{opacity:0, y:0}}, {{opacity:1, y:46, duration:1.4, ease:"power2.in"}}, {CALLS[18][0]:.2f});')
    for t0, t1, amp, per in ((CALLS[4][0], CALLS[30][0], 2, 0.11), (CALLS[30][0], END - 0.1, 4, 0.05)):   # she trembles, harder later
        T(f'tl.fromTo("#hjt", {{x:-{amp}}}, {{x:{amp}, duration:{per}, yoyo:true, repeat:{int((t1 - t0) / per) | 1}, ease:"sine.inOut", immediateRender:false}}, {t0:.2f});')

    # 3.1 s → · people join: one per call at first (40 of them, three rows), then the calls go round them all
    ROWS = [dict(n=10, feet=1440, s=0.95, light=0.6, xs=[110, 210, 300, 40, 160]),
            dict(n=12, feet=1265, s=0.7, light=0.42, xs=[400, 320, 230, 140, 60, 360]),
            dict(n=18, feet=1830, s=1.35, light=0.22, xs=[290, 140, 0, 380, 210, 60, 330, -40, 160])]
    BODY = ["#3d4a52", "#5a3d3d", "#3b4f45", "#4c4660", "#5b5340", "#2f3d4a", "#614a3a", "#45545c"]
    FACE = ["#d9b08c", "#a8784f", "#7a5236", "#e8c4a6", "#c48f66", "#8d5f3e"]
    HAIR = ["#1d1611", "#3a2a1c", "#7d6a55", "#111", "#b9a27c", "#5b3a22"]
    used, figs, side_alt = {}, [("ow", 300, 1440 - 480 * 0.8, -1, 1.0)], 1
    for k, (t0, kind, pan) in enumerate(CALLS):
        if k < 40:                                                       # a new person
            r = 0 if k < 10 else (1 if k < 22 else 2); R = ROWS[r]
            side = -1 if pan < -0.05 else (1 if pan > 0.05 else side_alt); side_alt = -side_alt
            n = used.get((r, side), 0)
            if n >= len(R["xs"]): side = -side; n = used.get((r, side), 0)
            used[(r, side)] = n + 1
            xl = R["xs"][n % len(R["xs"])]; x = xl if side < 0 else 1080 - xl
            id = f"p{k}"; d = -side
            people.append(person(id, x, R["feet"], R["s"], d, rnd.choice(BODY), rnd.choice(FACE), rnd.choice(HAIR), R["light"]))
            ent = t0 - (0.3 if k < 12 else 0.12)
            if r == 0: T(f'tl.fromTo("#{id}", {{opacity:0, x:{side * 160}}}, {{opacity:1, x:0, duration:0.35, ease:"power3.out"}}, {ent:.2f});')
            elif r == 1: T(f'tl.fromTo("#{id}", {{opacity:0, y:50}}, {{opacity:1, y:0, duration:0.3, ease:"power3.out"}}, {ent:.2f});')
            else: T(f'tl.fromTo("#{id}", {{opacity:0, y:320}}, {{opacity:1, y:0, duration:0.3, ease:"power3.out"}}, {ent:.2f});')
            figs.append((id, x, R["feet"] - 480 * R["s"], d, R["s"]))
            f = figs[-1]
        else:                                                            # the calls go round the crowd, on the side they're heard
            cand = [g for g in figs if (g[1] - 540) * pan >= 0] or figs
            f = rnd.choice(cand)
        id, x, top, d, s = f
        T(f'tl.to("#{id}m", {{attr:{{ry:15}}, duration:0.06, ease:"power3.out"}}, {t0:.2f});')
        T(f'tl.to("#{id}m", {{attr:{{ry:3}}, duration:0.2, ease:"power2.in"}}, {t0 + 0.24:.2f});')
        T(f'tl.fromTo("#{id}g", {{y:0}}, {{y:-10, duration:0.07, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {t0:.2f});')
        if k < 70: T(f'tl.to("#{id}a", {{rotation:{-18 * d}, duration:0.12, ease:"back.out(1.4)", svgOrigin:"100 178"}}, {t0:.2f});')
        if k < 60: T(f'tl.to("#{id}a", {{rotation:{30 * d}, duration:0.25, ease:"power2.in", svgOrigin:"100 178"}}, {t0 + 0.4:.2f});')
        if k < 8: T(f'tl.to("#eyes", {{x:{-5 if x < 540 else 5}, duration:0.2, ease:"power3.out"}}, {t0 + 0.05:.2f});')   # she looks at each one
        txt, cls = {"calm": ("hijab.", "b0"), "emph": ("Hijab!", "b1"), "shout": ("HIJAB!", "b2")}[kind]
        bx = x + d * 60 * s + rnd.uniform(-40, 40); by = top - 20 + rnd.uniform(-60, 30)
        if 400 < bx < 680 and 740 < by < 1130: bx = 390 if bx < 540 else 690   # never over her face
        bubbles.append(f'<div class="bub {cls}" id="b{k}" style="left:{bx:.0f}px;top:{by:.0f}px;font-size:{(44 if kind == "calm" else 56) * max(0.8, s):.0f}px;transform:translateX(-50%)"><i style="transform:rotate({rnd.uniform(-10, 10):.0f}deg)">{txt}</i></div>')
        T(f'tl.fromTo("#b{k} i", {{opacity:0, scale:0.4}}, {{opacity:1, scale:1, duration:0.18, ease:"back.out(1.4)"}}, {t0:.2f});')
        if k < 50: T(f'tl.to("#b{k} i", {{opacity:0, y:-20, duration:0.25, ease:"power2.in"}}, {t0 + (0.55 if k < 20 else 0.4):.2f});')   # later ones pile up
    # the camera pushes in on her as it builds, shaking at the end; a dead cut to black with the audio
    T(f'tl.fromTo("#cam", {{scale:1.45}}, {{scale:1.75, duration:{END - CALLS[0][0]:.2f}, ease:"power2.inOut", immediateRender:false}}, {CALLS[0][0]:.2f});')
    T(f'tl.fromTo("#cam", {{x:-5, y:3}}, {{x:5, y:-3, duration:0.05, yoyo:true, repeat:{int(2.4 / 0.05) | 1}, ease:"sine.inOut", immediateRender:false}}, {END - 2.6:.2f});')
    T(f'tl.set("#black", {{opacity:1}}, {END - 0.05:.2f});')

    css = f"""
@font-face {{ font-family:"AN"; src:url("assets/anton-latin-400-normal.woff2"); }}
* {{ margin:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:#0c1316; }}
#cam {{ position:absolute; inset:0; transform-origin:540px 1120px; transform:scale(1.45); }}
#wall {{ position:absolute; inset:0 0 auto 0; height:1300px; background:radial-gradient(ellipse at 50% 70%, #24363c 0%, #121c20 70%); }}
#floor {{ position:absolute; left:0; right:0; top:1300px; bottom:0; background:linear-gradient(#1a272b, #0b1012); }}
#dim {{ position:absolute; inset:0; background:#05080a; opacity:0; }}
#spot {{ position:absolute; inset:0; opacity:0; }}
#cone {{ position:absolute; left:0; top:0; width:1080px; height:1500px; background:linear-gradient(rgba(255,244,214,.38), rgba(255,244,214,.12));
  clip-path:polygon(470px 0, 610px 0, 800px 1460px, 280px 1460px); filter:blur(6px); }}
#pool {{ position:absolute; left:250px; top:1380px; width:580px; height:150px; border-radius:50%; background:radial-gradient(rgba(255,244,214,.5), rgba(255,244,214,0) 70%); }}
.p {{ position:absolute; opacity:1; }}
#hjw {{ position:absolute; left:390px; top:780px; width:300px; height:660px; filter:brightness(0.75); }}
#bigb {{ position:absolute; left:215px; top:600px; width:600px; padding:26px 30px; border-radius:40px; background:{CREAM}; font-family:AN; font-size:84px; line-height:1.05; color:{INK}; text-align:center; opacity:0; }}
#bigb::after {{ content:""; position:absolute; left:60px; bottom:-40px; border:24px solid transparent; border-top:30px solid {CREAM}; }}
#bigb span {{ display:inline-block; opacity:0; }} #bigb .r {{ color:{RED}; }}
.bub {{ position:absolute; font-family:AN; white-space:nowrap; }}
.bub i {{ display:inline-block; font-style:normal; padding:4px 22px; border-radius:30px; opacity:0; box-shadow:0 10px 24px rgba(0,0,0,.45); }}
.b0 i {{ background:#d9d4c8; color:#3a3a3a; }} .b1 i {{ background:{CREAM}; color:{RED}; }} .b2 i {{ background:{RED}; color:#fff; }}
#black {{ position:absolute; inset:0; background:#000; opacity:0; z-index:99; }}
"""
    hijabi = f'''<div id="hjw"><div id="hjt"><svg id="hj" viewBox="0 0 300 660" width="300" height="660" style="overflow:visible">
 <path d="M78 650 L 96 300 Q 150 250 204 300 L 222 650 Z" fill="#1f3b40"/>
 <path d="M150 58 C 88 58 66 122 72 178 C 76 232 58 300 70 336 L 230 336 C 242 300 224 232 228 178 C 234 122 212 58 150 58 Z" fill="{TEAL}"/>
 <path d="M150 58 C 88 58 66 122 72 178 C 90 120 210 120 228 178 C 234 122 212 58 150 58 Z" fill="#256356"/>
 <ellipse cx="150" cy="168" rx="46" ry="56" fill="#c99a73"/>
 <g id="eyes"><ellipse cx="132" cy="163" rx="6" ry="7" fill="#1a1a1a"/><ellipse cx="168" cy="163" rx="6" ry="7" fill="#1a1a1a"/></g>
 <path id="brL" d="M122 146 L 140 144" stroke="#2a1d14" stroke-width="5" stroke-linecap="round"/><path id="brR" d="M160 144 L 178 146" stroke="#2a1d14" stroke-width="5" stroke-linecap="round"/>
 <path id="mo1" d="M138 196 Q 150 201 162 196" stroke="#6b2f24" stroke-width="5" fill="none" stroke-linecap="round"/>
 <path id="mo2" d="M138 201 Q 150 191 162 201" stroke="#6b2f24" stroke-width="5" fill="none" stroke-linecap="round" opacity="0"/>
 <ellipse id="tear" cx="172" cy="178" rx="4" ry="6" fill="#bfe3ff" opacity="0"/>
 <g id="hands" opacity="0"><ellipse cx="136" cy="372" rx="20" ry="16" fill="#c99a73"/><ellipse cx="162" cy="376" rx="20" ry="16" fill="#c99a73"/></g>
</svg></div></div>'''
    back = [p for p in people if 'id="p' in p and int(p.split('id="p')[1].split('"')[0]) in range(10, 22)]
    front = [p for p in people if 'id="p' in p and int(p.split('id="p')[1].split('"')[0]) >= 22]
    mid = [p for p in people if p not in back and p not in front]
    body = f"""<div id="cam"><div id="wall"></div><div id="floor"></div><div id="dim"></div>
<div id="spot"><div id="cone"></div><div id="pool"></div></div>
{chr(10).join(back)}
{hijabi}
{chr(10).join(mid)}
{chr(10).join(front)}
{chr(10).join(bubbles)}
<div id="bigb">{bw}</div></div><div id="black"></div>"""
    au = [f'<audio id="a0" src="assets/pile.wav" data-start="0" data-duration="{END}" data-volume="1" data-track-index="1"></audio>',
          f'<audio id="a1" src="assets/thump.wav" data-start="{L0}" data-duration="0.7" data-volume="0.45" data-track-index="2"></audio>']   # the spotlight's clunk
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><title>hijab-pileon</title>
<script src="assets/gsap.min.js"></script><style>{css}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{END}">
{body}
{chr(10).join(au)}
</div><script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;</script></body></html>
""")
    print("built", END, "s,", len(people), "people,", len(bubbles), "bubbles")

if __name__ == "__main__":
    build()
