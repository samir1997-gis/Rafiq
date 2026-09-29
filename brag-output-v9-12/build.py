#!/usr/bin/env python3
"""Builds the four vertical videos (#155) as Hyperframes compositions:
brag-output-v9 (Your salah), v10 (What's in Complete), v11 (How Rafiq works), v12 (Meet Rafiq).

One layout for all four, 1080x1920: the voiceover line as a caption at the top and the real
app in a phone below (screens captured from the app at phone size, shots/), with a few designed
scenes in the phone's place (the hook, the review gaps, Meet Rafiq, the ending).
Voice: ElevenLabs (vo-el/, tools/v9-12-lines.json). Sound: v6's fountain and birdsong, no music.

  python3 brag-output-v9-12/build.py      then, per video:  cd brag-output-vN/composition && npx hyperframes check
"""
import html, json, os, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
V6 = os.path.join(ROOT, "brag-output-v6/composition/assets")
GAP, LEAD = 0.45, 0.9               # silence between lines; the opening ink stroke before the first line
SW, SH = 390, 844                   # the app's CSS size in the captures

def dur(p): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode())
def ar(s): return html.escape(s)
# captions: Arabic inside English lines in the Arabic font
def cap(s):
    import re
    t = re.sub(r"([؀-ۿ][؀-ۿ\s]*[؀-ۿ]|[؀-ۿ])", lambda m: f'<bdi class="ca" lang="ar">{m.group(0)}</bdi>', html.escape(s))
    return t.replace("rafiq-arabic.com", '<span class="nw">rafiq-arabic.com</span>')

# ---- designed scenes (shown where the phone is) -------------------------------------------
def scene_prayer_words(sid):
    words = [("سُبْحانَ", "Glory be to"), ("رَبِّيَ", "my Lord"), ("الْعَظِيمِ", "the Magnificent")]
    cells = "".join(f'<div class="pw" id="{sid}-w{i}"><b>{ar(a)}</b><i>{html.escape(e)}</i></div>' for i, (a, e) in enumerate(words))
    body = f'<div class="pwrow">{cells}</div><div class="kick" id="{sid}-k">IN RUKU, THREE TIMES</div>'
    def anim(t0, d):
        out = [f'tl.fromTo("#{sid} .pw b", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.6, ease:"power3.out", stagger:0.25}}, {t0+0.1:.2f});']
        out += [f'tl.fromTo("#{sid}-w{i} i", {{opacity:0, y:-10}}, {{opacity:1, y:0, duration:0.5, ease:"power2.out"}}, {t0+1.0+i*0.45:.2f});' for i in range(3)]
        out.append(f'tl.fromTo("#{sid}-k", {{opacity:0}}, {{opacity:1, duration:0.5}}, {t0+2.4:.2f});')
        return out
    return body, anim

def scene_forget(sid):
    words = [("كِتابٌ", "book"), ("مَدِينَةٌ", "city"), ("صَدِيقٌ", "friend")]
    cards = "".join(f'<div class="wcard" id="{sid}-c{i}"><b>{ar(a)}</b><i>{e}</i></div>' for i, (a, e) in enumerate(words))
    body = f'<div class="wstack">{cards}</div><div class="kick" id="{sid}-k">ONE WEEK LATER…</div>'
    def anim(t0, d):
        out = [f'tl.fromTo("#{sid}-c{i}", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.5, ease:"power3.out"}}, {t0+0.05+i*0.3:.2f});' for i in range(3)]
        out.append(f'tl.fromTo("#{sid}-k", {{opacity:0}}, {{opacity:1, duration:0.4}}, {t0+1.6:.2f});')
        out += [f'tl.to("#{sid}-c{i}", {{opacity:0.12, filter:"blur(12px)", y:-20, duration:1.0, ease:"power2.in"}}, {t0+1.9+j*0.25:.2f});' for j, i in enumerate([2, 0, 1])]
        return out
    return body, anim

def scene_meet(sid):
    body = f'<div class="meet"><div class="tile big" id="{sid}-t"><span>ر</span><em></em></div><div class="mname" id="{sid}-n">Rafiq</div><div class="mar" id="{sid}-a">رَفِيق</div><div class="msub" id="{sid}-s">Your companion for learning Arabic</div></div>'
    def anim(t0, d):
        return [f'tl.fromTo("#{sid}-t", {{opacity:0, scale:0.7, rotation:-8}}, {{opacity:1, scale:1, rotation:0, duration:0.6, ease:"back.out(1.7)"}}, {t0:.2f});',
                f'tl.fromTo("#{sid}-n", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.5, ease:"power3.out"}}, {t0+0.25:.2f});',
                f'tl.fromTo("#{sid}-a", {{clipPath:"inset(0% 0% 0% 100%)"}}, {{clipPath:"inset(0% 0% 0% 0%)", duration:0.8, ease:"power2.inOut"}}, {t0+0.45:.2f});',
                f'tl.fromTo("#{sid}-s", {{opacity:0}}, {{opacity:1, duration:0.5}}, {t0+1.0:.2f});']
    return body, anim

def scene_review(sid):
    # the real gaps from fsrs.js (progress.js settings) for a new word remembered every time: 3, 14, 57, 196 days
    chips = [("3 days", ""), ("2 weeks", ""), ("2 months", ""), ("6 months", "")]
    row = "".join(f'<div class="chip" id="{sid}-g{i}"><b>{a}</b></div>' + ('<div class="arr">→</div>' if i < 3 else '') for i, (a, _) in enumerate(chips))
    body = (f'<div class="rcard" id="{sid}-card"><b>بَيْت</b><i>house</i></div>'
            f'<div class="rlab" id="{sid}-l1">Remember it? It comes back in</div><div class="chips">{row}</div>'
            f'<div class="rlab small" id="{sid}-l2">Forget it? It’s back tomorrow.</div>')
    def anim(t0, d):
        out = [f'tl.fromTo("#{sid}-card", {{opacity:0, scale:0.9}}, {{opacity:1, scale:1, duration:0.5, ease:"back.out(1.6)"}}, {t0:.2f});',
               f'tl.fromTo("#{sid}-l1", {{opacity:0}}, {{opacity:1, duration:0.4}}, {t0+0.5:.2f});']
        out += [f'tl.fromTo("#{sid}-g{i}", {{opacity:0, y:16}}, {{opacity:1, y:0, duration:0.4, ease:"power3.out"}}, {t0+0.8+i*0.45:.2f});' for i in range(4)]
        out.append(f'tl.fromTo("#{sid} .arr", {{opacity:0}}, {{opacity:1, duration:0.3, stagger:0.45}}, {t0+1.0:.2f});')
        out.append(f'tl.fromTo("#{sid}-l2", {{opacity:0}}, {{opacity:1, duration:0.4}}, {t0+2.6:.2f});')
        return out
    return body, anim

def scene_outro(title_ar, title_en, note):
    def make(sid):
        body = (f'<div class="meet"><div class="tile big" id="{sid}-t"><span>ر</span><em></em></div>'
                f'<div class="mar" id="{sid}-a">{ar(title_ar)}</div><div class="mname" id="{sid}-n">{html.escape(title_en)}</div>'
                f'<div class="url" id="{sid}-u">rafiq-arabic.com</div><div class="msub" id="{sid}-s">{html.escape(note)}</div></div>')
        def anim(t0, d):
            return [f'tl.fromTo("#{sid}-t", {{opacity:0, scale:0.7}}, {{opacity:1, scale:1, duration:0.6, ease:"back.out(1.7)"}}, {t0:.2f});',
                    f'tl.fromTo("#{sid}-a", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.6, ease:"power3.out"}}, {t0+0.2:.2f});',
                    f'tl.fromTo("#{sid}-n", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.6, ease:"power3.out"}}, {t0+0.35:.2f});',
                    f'tl.fromTo("#{sid}-u", {{opacity:0, scale:0.9}}, {{opacity:1, scale:1, duration:0.5, ease:"back.out(1.6)"}}, {t0+0.8:.2f});',
                    f'tl.fromTo("#{sid}-s", {{opacity:0}}, {{opacity:1, duration:0.5}}, {t0+1.1:.2f});',
                    f'tl.fromTo("#{sid} .meet", {{scale:1}}, {{scale:1.04, duration:{max(1.0, d - 0.2):.2f}, ease:"sine.inOut"}}, {t0+0.2:.2f});']
        return body, anim
    return make

SCENES = {"prayer_words": scene_prayer_words, "forget": scene_forget, "meet": scene_meet, "review": scene_review}

# ---- the four videos -----------------------------------------------------------------------
# each line: (voice file, caption or None to use the spoken text, visual)
# visual: ("scene", name) | ("phone", [(shot, fraction of the line, effect)]) | ("pa",) the Pray along frames
# effects: "" | "zoom:x,y,scale" (x, y in the app's CSS pixels) | "tap:x,y" | "y:N" scroll the app N CSS px up, since the
# phone runs off the bottom of the frame and shows about 680 of the app's 844 px; combine with ";"
LINES = {l["file"]: l["text"] for l in json.load(open(os.path.join(ROOT, "tools/v9-12-lines.json")))}
VIDEOS = {
 "v9": ("Your salah", [
   ("v9-n1", None, ("scene", "prayer_words")),
   ("v9-n2", None, ("phone", [("ruku", 0, "zoom:195,300,1.1"), ("quiz_q", 0.55, "y:70")])),
   ("v9-n3", None, ("phone", [("part_rising", 0, "y:70"), ("salah_map", 0.5, "")])),
   ("v9-n4", None, ("pa",)),
   ("v9-r5", "Your salah, in رَفِيق.", ("scene", scene_outro("صَلاتُكَ", "Your salah", "The words you say most are free on every plan"))),
   ("v9-n6", None, None),
 ]),
 "v10": ("What's in Complete", [
   ("v10-n1", None, ("phone", [("plans_complete", 0, "")])),
   ("v10-n2", None, ("pa",)),
   ("v10-n3", "Your own tutor: ask anything, or tap Why? after a mistake.", ("phone", [("tutor0", 0, "tap:150,250"), ("tutor1", 0.28, ""), ("quiz_wrong", 0.6, "tap:292,24"), ("why", 0.78, "y:164")])),
   ("v10-n4", None, ("phone", [("scenes", 0, ""), ("scene_masjid", 0.5, "")])),
   ("v10-n5", None, ("phone", [("practise", 0, "y:40;zoom:195,345,1.15")])),
   ("v10-n6", None, ("scene", scene_outro("رَفِيق", "Rafiq Complete", "Free for a week · no card needed"))),
 ]),
 "v11": ("How Rafiq works", [
   ("v11-n1", None, ("phone", [("home", 0, "")])),
   ("v11-n2", None, ("phone", [("home", 0, "tap:150,256")])),
   ("v11-n3", None, ("phone", [("alpha", 0, "y:40")])),
   ("v11-n4", None, ("phone", [("words1", 0, "y:80")])),
   ("v11-n5", None, ("phone", [("listen", 0, "y:70"), ("grammar", 0.5, "y:70")])),
   ("v11-n6", None, ("phone", [("tiles0", 0, "zoom:195,330,1.08")])),
   ("v11-n7", None, ("scene", "review")),
   ("v11-n8", None, ("phone", [("practise", 0, ""), ("salah_map", 0.55, "")])),
   ("v11-n9", None, ("scene", scene_outro("رَفِيق", "Rafiq", "Free for a week · no card needed"))),
 ]),
 "v12": ("Meet Rafiq", [
   ("v12-n1", None, ("scene", "forget")),
   ("v12-r2", "Meet رَفِيق.", ("scene", "meet")),
   ("v12-n3", None, ("phone", [("words1", 0, "y:80"), ("listen", 0.55, "y:70")])),
   ("v12-n4", None, ("scene", "review")),
   ("v12-n5", None, ("scene", scene_outro("رَفِيق", "Rafiq", "Free for a week · no card needed"))),
 ]),
}

CSS = open(os.path.join(HERE, "style.css")).read()

def build(vid, title, lines):
    out = os.path.join(ROOT, f"brag-output-{vid}/composition"); a = os.path.join(out, "assets")
    if os.path.exists(out): shutil.rmtree(out)
    for d in ("fonts", "lib", "vo", "shots", "sfx"): os.makedirs(os.path.join(a, d), exist_ok=True)
    for f in os.listdir(os.path.join(V6, "fonts")): shutil.copy(os.path.join(V6, "fonts", f), os.path.join(a, "fonts"))
    shutil.copy(os.path.join(V6, "lib/gsap.min.js"), os.path.join(a, "lib"))
    for f in ("fountain.mp3", "birds.mp3", "page-turn.mp3", "pen-stroke.mp3"): shutil.copy(os.path.join(V6, "sfx-gen", f), os.path.join(a, "sfx"))
    shutil.copy(os.path.join(V6, "sfx/click_003.ogg"), os.path.join(a, "sfx"))

    # timing: each line's window runs from its voice's start to the next line's start
    t, rows = LEAD, []
    for i, (vo, caption, vis) in enumerate(lines):
        src = os.path.join(HERE, "vo-el", vo + ".mp3"); shutil.copy(src, os.path.join(a, "vo"))
        d = dur(src); rows.append([vo, caption or LINES[vo], vis, t, d]); t += d + GAP
    total = round(t + 1.2, 2)
    for i, r in enumerate(rows): r.append((rows[i + 1][3] if i + 1 < len(rows) else total) - r[3])   # window
    capwin = [r[5] for r in rows]                     # each caption keeps its own line's window
    # a line with no visual keeps the one before (the ending holds under the last line)
    for i, r in enumerate(rows):
        if r[2] is None: rows[i - 1][5] += r[5]

    shots, scenes, js, audio, sfx_at = [], [], [], [], []
    phone_on = []                                      # (start, end) the phone is showing
    for i, (vo, text, vis, t0, d, win) in enumerate(rows):
        audio.append(f'<audio id="a-{vo}" src="assets/vo/{vo}.mp3" data-start="{t0:.2f}" data-duration="{d:.2f}" data-track-index="{20 + i % 2}"></audio>')
        js.append(f'tl.fromTo("#cap{i}", {{opacity:0, y:14}}, {{opacity:1, y:0, duration:0.35, ease:"power2.out"}}, {t0 - 0.15:.2f});')
        if i + 1 < len(rows): js.append(f'tl.to("#cap{i}", {{opacity:0, duration:0.25}}, {t0 + capwin[i] - 0.3:.2f});')
        if vis is None: continue
        if vis[0] == "scene":
            sid = f"s{i}"; make = SCENES[vis[1]] if isinstance(vis[1], str) else vis[1]
            body, anim = make(sid)
            scenes.append(f'<section id="{sid}" class="scene">{body}</section>')
            js.append(f'tl.fromTo("#{sid}", {{opacity:0}}, {{opacity:1, duration:0.35}}, {t0 - 0.3:.2f});')
            js += anim(t0, win)
            if i + 1 < len(rows) and rows[i + 1][2] is not None: js.append(f'tl.to("#{sid}", {{opacity:0, duration:0.3}}, {t0 + win - 0.3:.2f});')
            sfx_at.append(t0 - 0.3)
        else:
            phone_on.append((t0, t0 + win))
            items = [("pa", 0, "")] if vis[0] == "pa" else vis[1]
            for j, (shot, frac, fx) in enumerate(items):
                s = t0 - 0.3 + frac * win; e = (t0 + frac * win + (items[j + 1][1] - frac) * win) if j + 1 < len(items) else t0 + win
                iid = f"i{i}_{j}"
                if shot == "pa":
                    frames = sorted(os.listdir(os.path.join(HERE, "shots/pa")))
                    for f in frames: shutil.copy(os.path.join(HERE, "shots/pa", f), os.path.join(a, "shots"))
                    shots.append(f'<div class="shot" id="{iid}" style="top:-84px">' + "".join(f'<img class="pf" id="{iid}f{k}" src="assets/shots/{f}">' for k, f in enumerate(frames)) + '</div>')
                    js.append(f'tl.fromTo("#{iid}", {{opacity:0}}, {{opacity:1, duration:0.3}}, {s:.2f});')
                    step = 0.14                                    # the frames were captured about every 0.14s
                    for k in range(len(frames)):
                        js.append(f'tl.set("#{iid}f{k}", {{opacity:1}}, {s + 0.3 + k * step:.2f});')
                        if k: js.append(f'tl.set("#{iid}f{k-1}", {{opacity:0}}, {s + 0.3 + k * step:.2f});')
                else:
                    shutil.copy(os.path.join(HERE, "shots", shot + ".jpg"), os.path.join(a, "shots"))
                    off = next((float(f[2:]) for f in fx.split(";") if f.startswith("y:")), 0) * 820 / SW
                    shots.append(f'<div class="shot" id="{iid}" style="top:{-off:.0f}px"><img src="assets/shots/{shot}.jpg"></div>')
                    fx = ";".join(f for f in fx.split(";") if not f.startswith("y:"))
                    js.append(f'tl.fromTo("#{iid}", {{opacity:0}}, {{opacity:1, duration:0.3}}, {s:.2f});')
                    if fx.startswith("zoom:"):
                        x, y, z = [float(v) for v in fx[5:].split(",")]
                        js.append(f'tl.set("#{iid} img", {{transformOrigin:"{x / SW * 100:.1f}% {y / SH * 100:.1f}%"}}, 0);')
                        js.append(f'tl.fromTo("#{iid} img", {{scale:1}}, {{scale:{z}, duration:{max(1.0, e - s - 0.6):.2f}, ease:"power1.inOut"}}, {s + 0.5:.2f});')
                    if fx.startswith("tap:"):
                        x, y = [float(v) for v in fx[4:].split(",")]
                        shots[-1] = shots[-1].replace("</div>", f'<i class="tap" id="{iid}t" style="left:{x / SW * 100:.1f}%;top:{y / SH * 100:.1f}%"></i></div>')
                        tt = s + 0.35 + min(0.9, (e - s) * 0.45)
                        js.append(f'tl.fromTo("#{iid}t", {{opacity:0.9, scale:0.3}}, {{opacity:0, scale:1.6, duration:0.6, ease:"power2.out"}}, {tt:.2f});')
                        audio.append(f'<audio src="assets/sfx/click_003.ogg" data-start="{tt:.2f}" data-duration="0.3" data-volume="0.5" data-track-index="12"></audio>')
                js.append(f'tl.to("#{iid}", {{opacity:0, duration:0.3}}, {e - 0.3:.2f});')
    # the phone rises in when it first appears, and steps aside for the designed scenes
    merged = []
    for s, e in phone_on:
        if merged and abs(merged[-1][1] - s) < 0.05: merged[-1][1] = e
        else: merged.append([s, e])
    for k, (s, e) in enumerate(merged):
        js.append(f'tl.fromTo("#phone", {{opacity:0, y:80}}, {{opacity:1, y:0, duration:0.5, ease:"power3.out"}}, {s - 0.35:.2f});')
        js.append(f'tl.to("#phone", {{opacity:0, y:40, duration:0.3, ease:"power2.in"}}, {e - 0.3:.2f});')
        sfx_at.append(s - 0.35)
    for t in sfx_at[1:]:
        audio.append(f'<audio src="assets/sfx/page-turn.mp3" data-start="{max(0, t):.2f}" data-duration="1.0" data-volume="0.28" data-track-index="11"></audio>')
    audio += [f'<audio src="assets/sfx/pen-stroke.mp3" data-start="0.00" data-duration="0.9" data-volume="0.6" data-track-index="10"></audio>',
              f'<audio src="assets/sfx/fountain.mp3" data-start="0.30" data-duration="{total - 0.3:.2f}" data-volume="0.16" data-fade-in="1" data-fade-out="1.2" data-track-index="8"></audio>',
              f'<audio src="assets/sfx/birds.mp3" data-start="0.60" data-duration="{min(total - 0.6, dur(os.path.join(V6, "sfx-gen/birds.mp3"))):.2f}" data-volume="0.10" data-fade-in="1.5" data-fade-out="1.5" data-track-index="9"></audio>']
    audio = [x if ' id="' in x else x.replace('<audio ', f'<audio id="sfx{k}" ', 1) for k, x in enumerate(audio)]
    caps = "".join(f'<div class="cap" id="cap{i}"><p>{cap(r[1])}</p></div>' for i, r in enumerate(rows))

    doc = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Rafiq — {html.escape(title)} ({vid})</title>
    <script src="assets/lib/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{total}">
      <div id="glow"></div>
      <div id="ink"></div>
      <div id="brand"><div class="tile"><span>ر</span><em></em></div><b>رَفِيق</b></div>
      <div id="caps">{caps}</div>
      <div id="phone"><div class="screen">{''.join(shots)}</div></div>
      {''.join(scenes)}
      {chr(10).join('      ' + x for x in audio)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      tl.fromTo("#ink", {{scaleX:0, opacity:1}}, {{scaleX:1, opacity:1, duration:0.42, ease:"power3.out"}}, 0.0);
      tl.to("#ink", {{opacity:0, duration:0.35, ease:"sine.in"}}, 0.55);
      tl.fromTo("#brand", {{opacity:0, y:-12}}, {{opacity:1, y:0, duration:0.6, ease:"power3.out"}}, 0.35);
      tl.fromTo("#glow", {{scale:0.92}}, {{scale:1.08, duration:{total}, ease:"none"}}, 0);
      {chr(10).join('      ' + x for x in js)}
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(out, "index.html"), "w").write(doc)
    print(f"{vid}: {title}, {total:.1f}s, {len(rows)} lines")

if __name__ == "__main__":
    for vid, (title, lines) in VIDEOS.items(): build(vid, title, lines)
