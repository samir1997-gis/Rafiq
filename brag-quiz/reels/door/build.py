#!/usr/bin/env python3
"""The door reel (owner, 24 Oct 2026, #291), in the format of a reference he sent (@motiontheory, "a bullet that doesn't exist"): 8 s with
no voice of a gold key flying at a keyhole, a FRAMES TO UNLOCK counter falling from 204 to 006 (fast, then a crawl), the camera zooming
in; it freezes and Brian (soft chuckle) says it was "a key that doesn't exist… and you're still here, waiting for it to turn"; the
scene turns to a blueprint. Then: "if you can watch that for seven seconds, you can watch this for another fifteen" (a ring counts the
fifteen down); the camera pulls back from that keyhole to a giant arched door with a tiny person scratching at its foot ("you've only
ever scratched the surface, never knowing how deep it goes": the door turns see-through onto the words of the salah); on "Arabic" the
key finally turns and the door opens onto light; RafiqArabic.com and a comment ask. Captions as in the reference: the lead-in small
and grey, the rest of the sentence big and bold, one word at a time.

Built on the retention principles (an open loop from frame 0, a visible countdown, no exit points, a twist that calls the viewer
out, the commitment line with a second visible countdown, the first loop closed as the payoff, the comment ask heard in full).

Lines 4-6 are played 10% faster with two pauses trimmed (d5, d6), so the ring is a true fifteen seconds.

  python3 brag-quiz/reels/door/build.py   then  cd brag-quiz/reels/door/out/v && npx hyperframes render -o ../door-raw.mp4
"""
import json, math, os, re, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
V6 = os.path.join(ROOT, "brag-output-v6/composition/assets"); VO = os.path.join(ROOT, "brag-quiz/voice/door")
INK, CREAM, GOLD, GOLD2, RED, TEAL = "#17262b", "#f1ece0", "#a8842c", "#E9B949", "#B4322A", "#2e7263"
dur = lambda f: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
mp3 = lambda n: os.path.join(VO, n + ".mp3")
words = lambda n: json.load(open(os.path.join(VO, n + ".words.json")))
FREEZE = 8.1
GAP = {"d2": .3, "d3": .25, "d4": .3, "d5": .1, "d6": .1, "d7": 1.5}                      # d7: the door gets a beat to swing open                               # the pause before each line
L = {"d1": 8.2}
for n in GAP: p = f"d{int(n[1]) - 1}"; L[n] = round(L[p] + dur(mp3(p)) + GAP[n], 2)               # when each line starts
def at(n, key, last=False):                                                                         # when line n says the word with key in it
    hits = [s for w, s, e in words(n) if key in w.lower()]
    return L[n] + (hits[-1] if last else hits[0])
END = round(L["d7"] + dur(mp3("d7")) + 1.2, 2)
N0, T0 = 204, 0.3                                         # as in the reference: 204 frames, falling by ~12% every quarter second,
KF = math.log(N0 / 6) / (FREEZE - T0)                     # 204 → ~100 in 1.6 s, then a crawl down to 006 at the freeze
KX, KY = 640, 640                                         # the keyhole (world units; the door's foot is at GY, the person 170 tall)
G0 = 230                                                  # the key's tip starts this far left of the keyhole, just inside the frame
GY, DX0, DX1, DTOP = 1500, -300, 1380, -2000              # the door: ground, frame left/right, top of the arch
CAM_HOOK0, CAM_HOOK1, CAM_TALK = (560, 640, 3.2), (600, 645, 4.2), (585, 650, 2.5)
CAM_DOOR, CAM_DOOR2 = (540, 600, 0.32), (520, 760, 0.38)  # the whole door (person ~55 px), then a slow push towards the person
CAPS = {                                                   # (lead-in, punch, the word in red)
 "d1": [("You just watched a key", "for seven seconds.", "seven"), ("A key", "that doesn't exist.", "exist.")],
 "d2": [("And you're still here,", "waiting for it to turn.", "turn.")],
 "d3": [("So if you can watch that", "for seven seconds,", "seven"), ("you can watch this", "for another fifteen.", "fifteen.")],
 "d4": [("", "This is you.", "you."), ("At the foot of a door", "you've been scratching at your whole life.", "whole")],
 "d5": [("Every salah.", "Every ayah.", "ayah."), ("You've only", "scratched the surface.", "surface."), ("Never knowing", "how deep it goes.", "deep")],
 "d6": [("You can open it,", "if you're ready.", "ready."), ("And it's as simple as", "learning the language it speaks:", "language"), ("", "Arabic.", "Arabic.")],
 "d7": [("Start today at", "RafiqArabic.com", "RafiqArabic.com"), ("and tell me in the comments:", "what's the first thing you'd want to understand?", "understand?")],
}
norm = lambda w: {"7": "seven", "15": "fifteen"}.get(re.sub(r"[^a-z0-9]", "", w.lower()), re.sub(r"[^a-z0-9]", "", w.lower()))

def timed(n):
    """[(chunk index, is punch, word, start)] for line n: the caption's own words, each given the start of the matching spoken word."""
    ws, j, out, t = words(n), 0, [], 0.0
    for c, (lead, punch, _) in enumerate(CAPS[n]):
        for part, text in ((0, lead), (1, punch)):
            for w in text.split():
                a = norm(w)
                for k in range(j, min(j + 4, len(ws))):
                    b = norm(ws[k][0])
                    if b and (a[:3] == b[:3] or a.startswith(b) or b.startswith(a)): t, j = ws[k][1], k + 1; break
                else: t += 0.12
                out.append((c, part, w, L[n] + t))
    return out

def build():
    out = os.path.join(HERE, "out", "v"); a = os.path.join(out, "assets")
    if os.path.exists(out): shutil.rmtree(out)
    os.makedirs(a)
    for f in ("ibm-plex-sans-arabic-arabic-700-normal.woff2", "karla-latin-500-normal.woff2", "karla-latin-700-normal.woff2"): shutil.copy(os.path.join(V6, "fonts", f), a)
    shutil.copy(os.path.join(V6, "lib/gsap.min.js"), a)
    for f in os.listdir(os.path.join(ROOT, "brag-quiz/sfx/soft")): shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/soft", f), a)
    for f in ("swoosh.wav", "swoosh-low.wav", "click.wav", "tap.wav"): shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/ref", f), a)
    shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/boom.wav"), a)
    for n in L: shutil.copy(mp3(n), a)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", os.path.join(V6, "sfx-gen/fountain.mp3"), "-af",
                    f"volume=6dB,atrim=0:{END - FREEZE},afade=t=in:d=1.0,afade=t=out:st={END - FREEZE - 1.5}:d=1.5", "-c:a", "libmp3lame", "-q:a", "3", os.path.join(a, "bed.mp3")], check=True)
    au = []
    def snd(name, t0, vol, d=None, track=None):
        d = d or dur(os.path.join(a, name))
        au.append(f'<audio id="s{len(au)}" src="assets/{name}" data-start="{max(0, t0):.3f}" data-duration="{d:.3f}" data-volume="{vol:.3f}" data-track-index="{track or 3 + len(au)}"></audio>')
    for n, t0 in L.items(): snd(f"{n}.mp3", t0, 1.0, track=1)
    snd("bed.mp3", FREEZE, 0.06, END - FREEZE, track=2)                                    # a very quiet bed under the voice, so nothing is ever silent
    js = []; T = js.append
    cam = lambda c, d, t, ease="power2.inOut": T(f'tl.to(CAM, {{cx:{c[0]}, cy:{c[1]}, s:{c[2]}, duration:{d}, ease:"{ease}", onUpdate:camSet}}, {t:.2f});')

    # 1 · the key (0-8.1), timed like the reference: already moving at the left edge on frame 0, it covers most of the way at once, then
    # crawls, the gap shrinking by the same share every moment (the counter falls fast, then barely); the camera zooms in steadily
    T(f'''(() => {{ const o = {{t:0}}, k = document.getElementById("keyw"), n = document.getElementById("cnum");
      const draw = (t) => {{ const f = Math.exp(-{KF:.4f} * Math.max(0, t - {T0})), g = {G0 - 100} * Math.pow(f, 3) + 100 * f;   // the gap, world px
        k.setAttribute("transform", `translate(${{{KX} - g}},{KY})`);
        const u = Math.min(1, t / {FREEZE}); CAM.cx = {CAM_HOOK0[0]} + {CAM_HOOK1[0] - CAM_HOOK0[0]} * u; CAM.cy = {CAM_HOOK0[1]} + {CAM_HOOK1[1] - CAM_HOOK0[1]} * u;
        CAM.s = {CAM_HOOK0[2]} + {CAM_HOOK1[2] - CAM_HOOK0[2]} * u; camSet();
        const v = Math.max(6, Math.round({N0} * f)); n.textContent = String(v).padStart(3, "0"); n.style.color = v <= 30 ? "#e0574d" : "{CREAM}"; }};
      draw(0); tl.to(o, {{t:{FREEZE}, duration:{FREEZE}, ease:"none", onUpdate:() => draw(o.t)}}, 0); }})();''')
    snd("drone.wav", 0, 0.55, FREEZE)
    snd("swoosh.wav", T0 - 0.05, 0.55); snd("swoosh-low.wav", T0 + 0.35, 0.4)
    last = -1                                                                                        # a tick each time the counter drops,
    for m in range(N0 - 1, 5, -1):                                                                   # as fast as a buzz at first
        t = T0 + math.log(N0 / (m + 0.5)) / KF
        if t - last >= 0.07 and t < FREEZE: snd("tick.wav", t, 0.09); last = t
    T(f'tl.to("#counter", {{opacity:0, y:-20, duration:0.3}}, {L["d1"] - 0.1:.2f});')
    cam(CAM_TALK, 0.9, L["d1"] - 0.05)                                                               # it eases back out as he talks (as in the reference)

    # 2 · the twist: the blueprint on "doesn't", colour again on "And you're still here"
    nv = at("d1", "doesn")
    T(f'tl.to(["#wood", "#leaves"], {{opacity:0, duration:0.5}}, {nv:.2f});'); T(f'tl.to("#keyfill", {{opacity:0, duration:0.5}}, {nv:.2f});')
    T(f'tl.fromTo(["#bp", "#grid", "#keybp"], {{opacity:0}}, {{opacity:1, duration:0.5}}, {nv:.2f});')
    T(f'tl.fromTo(".note", {{opacity:0, x:-14}}, {{opacity:1, x:0, duration:0.4, stagger:0.25}}, {nv + 0.3:.2f});'); snd("tap.wav", nv, 0.25); snd("tap.wav", nv + 0.3, 0.2)
    T(f'tl.to(["#bp", "#grid", "#keybp", ".note"], {{opacity:0, duration:0.4}}, {L["d2"] - 0.1:.2f});')
    T(f'tl.to(["#wood", "#leaves", "#keyfill"], {{opacity:1, duration:0.4}}, {L["d2"] - 0.1:.2f});'); snd("swoosh-low.wav", L["d2"] - 0.15, 0.2)

    # 3 · "…another fifteen": a ring shows 15 on "fifteen" and counts down from "this" (the start of the next line) to the moment the
    # door opens; the key that doesn't exist fades
    ff, OPEN = at("d3", "", last=True), at("d6", "arabic")
    secs = math.ceil(OPEN - L["d4"] - 0.05)
    T(f'tl.fromTo("#ring", {{opacity:0, scale:0.6}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, {ff:.2f});'); snd("click.wav", ff, 0.4)
    T(f'tl.set("#rnum", {{textContent:"{secs}"}}, {ff:.2f});')
    T(f'tl.fromTo("#ring .fg", {{strokeDashoffset:0}}, {{strokeDashoffset:251, duration:{OPEN - L["d4"]:.2f}, ease:"none"}}, {L["d4"]:.2f});')
    for i in range(1, secs + 1):                                                                     # the seconds left, a click on each
        t = OPEN - (secs - i)
        T(f'tl.set("#rnum", {{textContent:"{secs - i}"}}, {t:.2f});'); snd("click.wav", t, 0.18)
    T(f'tl.to("#ring", {{scale:1.4, opacity:0, duration:0.5}}, {OPEN + 0.1:.2f});')
    T(f'tl.to("#key", {{opacity:0, duration:0.4}}, {ff + 0.1:.2f});')

    # 4 · the pull back: that keyhole is high up a giant door; a tiny person at its foot, scratching at it
    PB = ff + 0.25                                                                                   # the pull back, straight after "fifteen"
    cam(CAM_DOOR, 1.5, PB, "power3.inOut"); snd("swoosh-low.wav", PB, 0.5); snd("whoosh.wav", PB + 0.2, 0.3)
    cam(CAM_DOOR2, OPEN - L["d4"] - 1.6, L["d4"] + 1.4, "sine.inOut")                              # never still: a slow push towards the person
    scr = []; t = L["d4"] + 0.9
    while t < OPEN - 2.4: scr.append(t); t += 1.25
    for i, t in enumerate(scr):
        snd("scratch.wav", t, 0.5)
        T(f'tl.fromTo("#arm", {{rotation:0}}, {{rotation:7, duration:0.12, yoyo:true, repeat:5, ease:"sine.inOut", svgOrigin:"488 1368", immediateRender:{"true" if i == 0 else "false"}}}, {t:.2f});')
        if i < 10: T(f'tl.fromTo("#nm{i}", {{opacity:0}}, {{opacity:1, duration:0.2}}, {t + 0.1:.2f});')
    yu = max(at("d4", "you"), PB + 1.4)                                                                             # "This is you": a gold circle round the person
    T(f'tl.fromTo("#you", {{opacity:0, scale:1.6, transformOrigin:"50% 50%"}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, {yu:.2f});')
    T(f'tl.to("#you", {{opacity:0, duration:0.4}}, {yu + 1.6:.2f});'); snd("tick-lo.wav", yu, 0.5)
    sf, dp = at("d5", "surface"), at("d5", "deep")
    T(f'tl.fromTo(".mk", {{stroke:"rgba(241,236,224,.35)"}}, {{stroke:"{GOLD2}", duration:0.3, yoyo:true, repeat:1}}, {sf:.2f});'); snd("shimmer.wav", sf, 0.25, 1.2)
    # 5 · "how deep it goes": the door turns see-through onto the words of the salah, receding into the light
    T(f'tl.to(".leaf", {{opacity:0.08, duration:0.6}}, {dp - 0.1:.2f});'); T(f'tl.fromTo("#depth", {{opacity:0}}, {{opacity:1, duration:0.6}}, {dp - 0.1:.2f});')
    T(f'tl.fromTo(".dl", {{scale:0.85}}, {{scale:1.05, duration:2.6, ease:"sine.out", stagger:0.08}}, {dp - 0.1:.2f});'); snd("shimmer.wav", dp, 0.5); snd("darkhum.wav", dp, 0.2, 2.4)
    T(f'tl.to(".leaf", {{opacity:1, duration:0.5}}, {L["d6"] - 0.2:.2f});'); T(f'tl.to("#depth", {{opacity:0, duration:0.5}}, {L["d6"] - 0.2:.2f});')
    # 6 · "you can open it, if you're ready": the key appears at the person's hand, rises to the keyhole; on "Arabic" it goes in and turns
    op, rd = at("d6", "open"), at("d6", "ready")
    T(f'tl.fromTo("#key", {{opacity:0, x:{560 - KX + 3}, y:{1300 - KY}, scale:1.6, transformOrigin:"100% 50%"}}, {{opacity:1, duration:0.5, immediateRender:false}}, {op:.2f});'); snd("shimmer.wav", op, 0.45, 1.5)
    T(f'tl.set("#keyglow", {{opacity:1}}, {op:.2f});')
    T(f'tl.to("#key", {{x:-20, y:0, scale:1, duration:{max(0.8, OPEN - rd - 0.6):.2f}, ease:"power2.inOut"}}, {rd:.2f});'); snd("swoosh-low.wav", rd, 0.3)
    T(f'tl.to("#key", {{x:3, duration:0.25, ease:"power2.in"}}, {OPEN - 0.25:.2f});')
    T(f'tl.to("#key", {{scaleY:-1, duration:0.3, ease:"back.out(2)"}}, {OPEN:.2f});'); snd("click.wav", OPEN + 0.02, 1.0); snd("tick-lo.wav", OPEN + 0.1, 0.7)
    T(f'tl.to("#key", {{opacity:0, duration:0.3}}, {OPEN + 0.5:.2f});')
    T(f'tl.to("#leafL", {{scaleX:0.07, duration:1.2, ease:"power2.inOut"}}, {OPEN + 0.3:.2f});'); T(f'tl.to("#leafR", {{scaleX:0.07, duration:1.2, ease:"power2.inOut"}}, {OPEN + 0.3:.2f});')
    snd("creak.wav", OPEN + 0.3, 0.55); snd("boom.wav", OPEN + 0.35, 0.35); snd("shimmer.wav", OPEN + 0.5, 0.9)
    T(f'tl.fromTo("#beyond", {{opacity:0}}, {{opacity:1, duration:1.0}}, {OPEN + 0.4:.2f});')
    # 7 · into the light: RafiqArabic.com, then the comment ask, heard in full
    cam((540, 300, 1.6), 1.2, L["d7"] - 0.6, "power2.in"); T(f'tl.fromTo("#light", {{opacity:0}}, {{opacity:1, duration:0.8}}, {L["d7"] - 0.4:.2f});'); snd("swoosh.wav", L["d7"] - 0.5, 0.3)
    url = at("d7", "raf")
    T(f'tl.fromTo("#cta", {{opacity:0, scale:0.9}}, {{opacity:1, scale:1, duration:0.5, ease:"back.out(1.8)"}}, {url - 0.15:.2f});'); snd("tick-lo.wav", url, 0.6)
    T(f'tl.set("#cta", {{opacity:1}}, {END - 0.01:.2f});')

    # the captions, as in the reference: lead-in small and grey, punch big and bold, word by word
    cap_html, chunks = "", []
    for n in L:
        tw = timed(n)
        for c in range(len(CAPS[n])):
            ws = [x for x in tw if x[0] == c]
            if ws: chunks.append((n, c, ws))
    for j, (n, c, ws) in enumerate(chunks):
        red, start = CAPS[n][c][2], ws[0][3]
        nxt = chunks[j + 1][2][0][3] if j + 1 < len(chunks) else END
        lead = " ".join(f'<span class="cw" id="c{j}w{i}">{w}</span>' for i, (_, p, w, s) in enumerate(ws) if p == 0)
        punch = " ".join(f'<span class="cw{" red" if w == red else ""}" id="c{j}w{i}">{w}</span>' for i, (_, p, w, s) in enumerate(ws) if p == 1)
        cap_html += f'<div class="cap" id="c{j}">' + (f'<div class="lead">{lead}</div>' if lead else "") + f'<div class="punch">{punch}</div></div>'
        T(f'tl.set("#c{j}", {{opacity:1}}, {start - 0.02:.2f});')
        for i, (_, p, w, s) in enumerate(ws): T(f'tl.fromTo("#c{j}w{i}", {{opacity:0, y:10, filter:"blur(6px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.25}}, {s:.2f});')
        T(f'tl.to("#c{j}", {{opacity:0, duration:0.15}}, {min(nxt - 0.05, ws[-1][3] + 2.6):.2f});')

    # the door, in world units (the camera moves over it)
    plank = lambda x0, x1: "".join(f'<line x1="{x}" y1="{DTOP}" x2="{x}" y2="{GY}" stroke="#22363d" stroke-width="5"/>' for x in range(x0 + 110, x1, 110))
    archL = f"M{DX0 + 70} {GY} V{DTOP + 840} A770 770 0 0 1 540 {DTOP + 70} V{GY} Z"
    archR = f"M540 {GY} V{DTOP + 70} A770 770 0 0 1 {DX1 - 70} {DTOP + 840} V{GY} Z"
    marks = "".join(f'<line class="mk" x1="{470 + (i * 37) % 80}" y1="{1215 + (i * 53) % 120}" x2="{476 + (i * 37) % 80}" y2="{1250 + (i * 53) % 120}" stroke-width="3"/>' for i in range(26))
    newm = "".join(f'<line class="mk" id="nm{i}" x1="{492 + (i * 13) % 40}" y1="{1262 + (i * 29) % 70}" x2="{498 + (i * 13) % 40}" y2="{1298 + (i * 29) % 70}" stroke-width="3" opacity="0"/>' for i in range(10))
    lines = ["الْحَمْدُ لِلَّهِ رَبِّ الْعالَمِينَ", "إِيّاكَ نَعْبُدُ وَإِيّاكَ نَسْتَعِينُ", "اهْدِنا الصِّراطَ الْمُسْتَقِيمَ", "سُبْحانَ رَبِّيَ الْعَظِيمِ",
             "سَمِعَ اللَّهُ لِمَنْ حَمِدَهُ", "سُبْحانَ رَبِّيَ الْأَعْلى", "رَبَّنا آتِنا فِي الدُّنْيا حَسَنَةً"]
    depth = "".join(f'<div class="dl" style="top:{1180 - i * 330}px;font-size:{200 - i * 18}px;opacity:{1 - i * 0.11:.2f}">{t}</div>' for i, t in enumerate(lines))
    keysvg = (f'<g id="keyfill"><circle cx="-128" cy="0" r="22" fill="none" stroke="{GOLD2}" stroke-width="11"/>'
              f'<rect x="-108" y="-6" width="108" height="12" rx="4" fill="{GOLD2}"/><rect x="-34" y="6" width="9" height="18" rx="2" fill="{GOLD2}"/>'
              f'<rect x="-17" y="6" width="9" height="13" rx="2" fill="{GOLD2}"/></g>'
              f'<g id="keybp" opacity="0"><circle cx="-128" cy="0" r="22" fill="none" stroke="#5f7d86" stroke-width="2" stroke-dasharray="6 5"/>'
              f'<rect x="-108" y="-6" width="108" height="12" rx="4" fill="none" stroke="#5f7d86" stroke-width="2" stroke-dasharray="6 5"/></g>')
    keyhole = (f'<rect x="{KX - 42}" y="{KY - 90}" width="84" height="190" rx="40" fill="{GOLD}"/><rect x="{KX - 34}" y="{KY - 82}" width="68" height="174" rx="34" fill="{GOLD2}"/>'
               f'<circle cx="{KX}" cy="{KY - 6}" r="15" fill="#0c1214"/><path d="M{KX - 9} {KY} L{KX - 15} {KY + 52} H{KX + 15} L{KX + 9} {KY} Z" fill="#0c1214"/>')
    grid = "".join(f'<line x1="{x}" y1="-2400" x2="{x}" y2="2400"/>' for x in range(-1200, 2401, 30)) + "".join(f'<line x1="-1200" y1="{y}" x2="2400" y2="{y}"/>' for y in range(-2400, 2401, 30))
    stone = "".join(f'<rect x="{x + (90 if (y // 180) % 2 else 0)}" y="{y}" width="180" height="180" fill="none" stroke="#d8cfbd" stroke-width="4"/>' for y in range(-2600, GY, 180) for x in range(-1800, 2600, 180))
    css = f"""
@font-face {{ font-family:"KA"; src:url("assets/karla-latin-500-normal.woff2"); font-weight:500; }}
@font-face {{ font-family:"KA"; src:url("assets/karla-latin-700-normal.woff2"); font-weight:700; }}
@font-face {{ font-family:"AR"; src:url("assets/ibm-plex-sans-arabic-arabic-700-normal.woff2"); }}
* {{ margin:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:{CREAM}; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:{CREAM}; }}
.sc {{ position:absolute; inset:0; }} #cam {{ position:absolute; left:0; top:0; width:1080px; height:1920px; transform-origin:0 0; }}
svg.full {{ position:absolute; left:0; top:0; width:1080px; height:1920px; overflow:visible; }}
#grid {{ opacity:0; }} #grid line {{ stroke:#c9d3d4; stroke-width:0.6; }} #bp {{ opacity:0; }}
#counter {{ position:absolute; left:0; right:0; top:1440px; text-align:center; font-family:KA; color:{CREAM}; }}
#counter small {{ display:block; font-size:24px; letter-spacing:.32em; font-weight:700; opacity:.55; }} #cnum {{ display:block; font-size:120px; font-weight:500; letter-spacing:.04em; }}
.note {{ position:absolute; font-family:KA; font-size:28px; letter-spacing:.06em; color:#5f7d86; opacity:0; }}
.cap {{ position:absolute; left:90px; right:90px; top:1360px; text-align:center; font-family:KA; color:{INK}; opacity:0; }}
.cap .lead {{ font-size:42px; font-weight:500; color:#6b7173; line-height:1.2; margin-bottom:6px; }}
.cap .punch {{ font-size:66px; font-weight:700; line-height:1.12; letter-spacing:-.01em; }} .cw {{ display:inline-block; opacity:0; }} .red {{ color:{RED}; }}
#ring {{ position:absolute; right:56px; top:120px; width:110px; height:110px; opacity:0; }} #ring svg {{ position:absolute; inset:0; transform:rotate(-90deg); }}
#ring circle {{ fill:none; stroke-width:7; }} #ring .bg {{ stroke:rgba(23,38,43,.15); }} #ring .fg {{ stroke:{RED}; stroke-linecap:round; stroke-dasharray:251; }}
#rnum {{ position:absolute; inset:0; text-align:center; line-height:110px; font-family:KA; font-weight:700; font-size:40px; color:{INK}; }}
#leaves {{ position:absolute; left:0; top:0; width:1080px; height:1920px; }}
.leaf {{ position:absolute; left:0; top:0; width:1080px; height:1920px; overflow:visible; }} #leafL {{ transform-origin:{DX0 + 70}px 0px; }} #leafR {{ transform-origin:{DX1 - 70}px 0px; }}
#depth {{ position:absolute; left:0; top:0; width:1080px; height:1920px; opacity:0; }}
.dl {{ position:absolute; left:-600px; width:2280px; text-align:center; font-family:AR; color:{GOLD2}; direction:rtl; text-shadow:0 0 30px rgba(233,185,73,.6); }}
#beyond {{ position:absolute; left:0; top:0; width:1080px; height:1920px; opacity:0; }}
#light {{ position:absolute; inset:0; opacity:0; background:radial-gradient(circle at 50% 40%, #fffef8, #fff6da 55%, #f6e3a8); }}
#cta {{ position:absolute; left:0; right:0; top:560px; text-align:center; opacity:0; }} #cta .logo {{ display:inline-block; width:160px; height:160px; border-radius:38px; background:{INK};
  color:{CREAM}; font-family:AR; font-size:100px; line-height:160px; position:relative; }} #cta .logo i {{ position:absolute; right:24px; top:22px; width:18px; height:18px; border-radius:50%; background:{RED}; }}
#cta .url {{ display:inline-block; margin-top:44px; padding:24px 58px; border-radius:999px; background:{TEAL}; color:{CREAM}; font-family:KA; font-weight:700; font-size:64px; }}
#cta small {{ display:block; margin-top:22px; font-family:KA; font-size:34px; color:{INK}; opacity:.7; }}
"""
    body = f"""
<div class="sc" id="s1"><div id="cam">
  <svg class="full" viewBox="0 0 1080 1920"><g id="grid">{grid}</g></svg>
  <svg class="full" viewBox="0 0 1080 1920" id="wood">
    <g>{stone}</g><rect x="-2000" y="{GY}" width="5000" height="3000" fill="#e3dac7"/><line x1="-2000" y1="{GY}" x2="3000" y2="{GY}" stroke="#c9bea7" stroke-width="6"/>
    <path d="M{DX0} {GY} V{DTOP + 840} A840 840 0 0 1 {DX1} {DTOP + 840} V{GY} Z" fill="#c4b69a"/>
    <path d="{archL}" fill="#0c1214"/><path d="{archR}" fill="#0c1214"/>
  </svg>
  <svg class="full" viewBox="0 0 1080 1920" id="beyond"><defs><radialGradient id="lg" cx="50%" cy="55%" r="60%"><stop offset="0" stop-color="#fffef8"/><stop offset=".5" stop-color="#fff3c9"/><stop offset="1" stop-color="#f3d98f"/></radialGradient></defs>
    <path d="{archL}" fill="url(#lg)"/><path d="{archR}" fill="url(#lg)"/></svg>
  <div id="depth"><svg class="full" viewBox="0 0 1080 1920"><path d="{archL}" fill="#0f1a1e"/><path d="{archR}" fill="#0f1a1e"/></svg>{depth}</div>
  <div id="leaves">
    <svg class="full leaf" id="leafL" viewBox="0 0 1080 1920"><defs><clipPath id="cpL"><path d="{archL}"/></clipPath><clipPath id="cpR"><path d="{archR}"/></clipPath></defs>
      <path d="{archL}" fill="{INK}"/><g clip-path="url(#cpL)">{plank(DX0 + 70, 540)}</g><line x1="530" y1="{DTOP}" x2="530" y2="{GY}" stroke="#0c1214" stroke-width="12"/>
      <g stroke="rgba(241,236,224,.35)">{marks}{newm}</g></svg>
    <svg class="full leaf" id="leafR" viewBox="0 0 1080 1920"><path d="{archR}" fill="{INK}"/><g clip-path="url(#cpR)">{plank(540, DX1 - 70)}</g>{keyhole}</svg>
  </div>
  <svg class="full" viewBox="0 0 1080 1920" id="bp"><path d="M{DX0 + 70} {GY} V{DTOP + 840} A770 770 0 0 1 {DX1 - 70} {DTOP + 840} V{GY} Z" fill="none" stroke="#5f7d86" stroke-width="3"/>
    <line x1="540" y1="{DTOP}" x2="540" y2="{GY}" stroke="#5f7d86" stroke-width="2"/>
    <rect x="{KX - 42}" y="{KY - 90}" width="84" height="190" rx="40" fill="none" stroke="#5f7d86" stroke-width="2"/><circle cx="{KX}" cy="{KY - 6}" r="15" fill="none" stroke="#5f7d86" stroke-width="2"/>
    <line x1="{KX - 200}" y1="{KY}" x2="{KX - 20}" y2="{KY}" stroke="#5f7d86" stroke-width="1.2" stroke-dasharray="4 4"/></svg>
  <svg class="full" viewBox="0 0 1080 1920" id="person"><ellipse id="you" cx="476" cy="1415" rx="70" ry="120" fill="none" stroke="{GOLD2}" stroke-width="9" opacity="0" transform="rotate(-8 476 1415)"/><ellipse cx="478" cy="{GY + 4}" rx="40" ry="7" fill="rgba(23,38,43,.18)"/>
    <g fill="{CREAM}" style="filter:drop-shadow(0 0 6px rgba(0,0,0,.35))"><circle cx="476" cy="1340" r="14"/><path d="M458 1360 Q476 1352 494 1360 L497 1448 H455 Z"/><rect x="458" y="1440" width="15" height="60" rx="6"/><rect x="479" y="1440" width="15" height="60" rx="6"/>
      <path d="M458 1366 L446 1430" stroke="{CREAM}" stroke-width="10" stroke-linecap="round"/>
      <g id="arm"><path d="M488 1368 L500 1300" stroke="{CREAM}" stroke-width="10" stroke-linecap="round"/></g></g></svg>
  <svg class="full" viewBox="0 0 1080 1920"><g id="keyw" transform="translate({KX - G0},{KY})"><g id="key"><circle id="keyglow" cx="-60" cy="0" r="70" fill="rgba(233,185,73,.25)" opacity="0"/>{keysvg}</g></g></svg>
</div>
  <div class="note" style="left:80px;top:250px">distance to keyhole = ∞</div><div class="note" style="left:80px;top:300px">turns = 0</div>
  <div class="note" style="left:640px;top:250px">attention = held</div>
  <div id="counter"><small>FRAMES TO UNLOCK</small><b id="cnum">204</b></div>
</div>
<div id="light"></div>
<div id="cta"><div class="logo">ر<i></i></div><br><div class="url">rafiqarabic.com</div><small>7 days free · no card needed</small></div>
<div id="ring"><svg viewBox="0 0 110 110" width="110" height="110"><circle class="bg" cx="55" cy="55" r="40"/><circle class="fg" cx="55" cy="55" r="40"/></svg><div id="rnum">15</div></div>
{cap_html}"""
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><title>door</title>
<script src="assets/gsap.min.js"></script><style>{css}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{END}">
{body}
{chr(10).join(au)}
</div><script>
const tl = gsap.timeline({{ paused: true }});
const CAM = {{cx:{CAM_HOOK0[0]}, cy:{CAM_HOOK0[1]}, s:{CAM_HOOK0[2]}}}, camEl = document.getElementById("cam");
function camSet() {{ camEl.style.transform = `translate(${{540 - CAM.cx * CAM.s}}px, ${{960 - CAM.cy * CAM.s}}px) scale(${{CAM.s}})`; }}
camSet();
{chr(10).join(js)}
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;</script></body></html>
""")
    print("built", END, "s,", len(au), "sounds;", L, f"ring {OPEN - L['d4']:.1f} s")

if __name__ == "__main__":
    build()
