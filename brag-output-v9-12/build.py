#!/usr/bin/env python3
"""Builds the four vertical videos (#155) as Hyperframes compositions, second cut:
brag-output-v9 (Your salah), v10 (What's in Complete), v11 (How Rafiq works), v12 (Meet Rafiq).

1080x1920. The spoken line as a caption at the top; below it the whole phone, always in frame, playing
clips of the real app working (capture.py: tapping, typing, words lighting up, with the app's own sounds);
designed scenes in the phone's place for the hook, Meet Rafiq, the review gaps and the ending.
Pace: every line is followed by a pause, and a demo that makes sounds plays after the line, so the
narration never talks over the app. Voice: Sara (ElevenLabs, vo-sara/, tools/v9-12-lines-sara.json).
Sound: v6's fountain and birdsong, no music.

  python3 brag-output-v9-12/capture.py (with the site served, see there), then python3 brag-output-v9-12/build.py,
  then per video: cd brag-output-vN/composition && npx hyperframes check && npx hyperframes render -o ../brag.mp4
"""
import html, json, os, re, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
V6 = os.path.join(ROOT, "brag-output-v6/composition/assets")
SW, SH = 390, 844                   # the app's CSS size in the captures
LEAD, GAP, TAIL = 0.9, 0.9, 0.35     # before the first line; after each line; after each demo

def dur(p): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode())
def ar(s): return html.escape(s)
# captions: Arabic inside English lines in the Arabic font
def cap(s):
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
# a line: (Sara's line id, visual). visual: ("scene", name or maker) | [demo, ...] | None (keep the last)
# a demo: (clip, how, start, end, zoom): how "with" plays it under the line, "after" holds its first frame
# under the line and plays it once the line is spoken (for demos with sound); start/end trim the clip (s);
# zoom "x,y,scale" eases in on that point (the app's CSS px) while it plays; an optional 6th value is the time of the
# frame held under the line in "after" mode (e.g. a settled screen, then the next word being said).
LINES = {l["file"]: l["text"] for l in json.load(open(os.path.join(ROOT, "tools/v9-12-lines-sara.json")))}
END = lambda t: ("scene", scene_outro("رَفِيق", t, "Free for a week · no card needed"))
VIDEOS = {
 "v12": ("Meet Rafiq", [
   ("v12-s1", ("scene", "forget")),
   ("v12-s2", ("scene", "meet")),
   ("v12-s3", [("words", "after", 3.3, 6.7, "", 3.2)]),
   ("v12-s4", [("mostsaid", "with", 0, 2.2, ""), ("prayalong", "after", 2.9, 7.2, "")]),
   ("v12-s5", [("tutor", "with", 0.4, 8.2, "")]),
   ("v12-s6", ("scene", "review")),
   ("v12-s7", END("Rafiq")),
 ]),
 "v9": ("Your salah", [
   ("v9-s1", ("scene", "prayer_words")),
   ("v9-s2", [("mostsaid", "with", 0, 4.6, "")]),
   ("v9-s3", [("mostsaid", "with", 0, 1.4, "195,300,1.3")]),
   ("v9-s4", [("quiz", "with", 0.9, 7.6, "")]),
   ("v9-s5", [("parts", "with", 0, 3.4, ""), ("part", "after", 5.9, 10.6, "", 5.0)]),
   ("v9-s6", [("count", "with", 0, 9.8, "")]),
   ("v9-s7", [("prayalong", "after", 2.9, 8.6, "")]),
   ("v9-s8", ("scene", scene_outro("صَلاتُكَ", "Your salah", "The words you say most are free on every plan"))),
 ]),
 "v10": ("What's in Complete", [
   ("v10-s1", [("plans", "with", 0, 3.7, "")]),
   ("v10-s2", [("prayalong", "with", 2.9, 8.6, "")]),
   ("v10-s3", [("tutor", "with", 0.4, 8.6, "")]),
   ("v10-s4", [("why", "with", 0.6, 7.6, "")]),
   ("v10-s5", [("scene", "with", 0.8, 9.2, "")]),
   ("v10-s6", [("weak", "with", 0, 5.7, "")]),
   ("v10-s7", END("Rafiq Complete")),
 ]),
 "v11": ("How Rafiq works", [
   ("v11-s1", [("home", "with", 0, 1.9, "")]),
   ("v11-s2", [("home", "with", 0.3, 5.9, "")]),
   ("v11-s3", [("letters", "with", 0.4, 6.2, "")]),
   ("v11-s4", [("words", "after", 3.3, 6.7, "", 3.2)]),
   ("v11-s5", [("listen", "after", 0.8, 3.6, ""), ("listen", "with", 8.2, 11.5, "")]),
   ("v11-s6", [("tiles", "with", 0.9, 5.8, "")]),
   ("v11-s7", ("scene", "review")),
   ("v11-s8", [("spelling", "with", 0.8, 5.6, "")]),
   ("v11-s9", [("mostsaid", "with", 0, 3.4, "")]),
   ("v11-s10", END("Rafiq")),
 ]),
}
# sounds the recorder missed or doubled, per clip: [seconds, file]
SOUNDS = {"listen": [[1.05, "audio/1u2523z.mp3"]]}

CSS = open(os.path.join(HERE, "style.css")).read()

def sounds_of(clip):
    s = SOUNDS.get(clip) or json.load(open(os.path.join(HERE, "clips", clip + ".json")))["sounds"]
    s = sorted(s)
    # the app has one shared player: a sound cut off by the next one within 0.3s never really played
    return [x for i, x in enumerate(s) if not (i + 1 < len(s) and s[i + 1][0] - x[0] < 0.3 and s[i + 1][1].startswith("audio/") and x[1].startswith("audio/"))]

def build(vid, title, lines):
    out = os.path.join(ROOT, f"brag-output-{vid}/composition"); a = os.path.join(out, "assets")
    if os.path.exists(out): shutil.rmtree(out)
    for d in ("fonts", "lib", "vo", "clips", "sfx", "app"): os.makedirs(os.path.join(a, d), exist_ok=True)
    for f in os.listdir(os.path.join(V6, "fonts")): shutil.copy(os.path.join(V6, "fonts", f), os.path.join(a, "fonts"))
    shutil.copy(os.path.join(V6, "lib/gsap.min.js"), os.path.join(a, "lib"))
    for f in ("fountain.mp3", "birds.mp3", "page-turn.mp3", "pen-stroke.mp3"): shutil.copy(os.path.join(V6, "sfx-gen", f), os.path.join(a, "sfx"))

    html_clips, scenes, js, audio, caps = [], [], [], [], []
    phone_on, t, n = [], LEAD, 0
    for i, (vo, vis) in enumerate(lines):
        src = os.path.join(HERE, "vo-sara", vo + ".mp3"); shutil.copy(src, os.path.join(a, "vo"))
        d = dur(src); s0 = t; vo_end = s0 + d
        audio.append(f'<audio id="a-{vo}" src="assets/vo/{vo}.mp3" data-start="{s0:.2f}" data-duration="{d:.2f}" data-track-index="20"></audio>')
        end = vo_end + GAP
        if isinstance(vis, list):                              # demos, one after another
            at = s0 - 0.3
            for j, (clip, how, c_in, c_out, zoom, *rest) in enumerate(vis):
                still_at = rest[0] if rest else c_in             # the frame held under the line (default: where the clip starts)
                n += 1; cid = f"c{n}"; L = c_out - c_in
                shutil.copy(os.path.join(HERE, "clips", clip + ".mp4"), os.path.join(a, "clips"))
                hold_until = max(at, vo_end + 0.15) if how == "after" else at
                show, play = at, hold_until
                if how == "after":                             # its first frame, still, while the line is spoken
                    still = f"{clip}-{still_at:.1f}.jpg"
                    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{still_at + 0.05:.2f}", "-i", os.path.join(HERE, "clips", clip + ".mp4"),
                                    "-frames:v", "1", "-q:v", "3", os.path.join(a, "clips", still)], check=True)
                    html_clips.append(f'<img class="cl" id="{cid}s" src="assets/clips/{still}">')
                    js.append(f'tl.fromTo("#{cid}s", {{opacity:0}}, {{opacity:1, duration:0.3}}, {show:.2f});')
                    js.append(f'tl.set("#{cid}s", {{opacity:0}}, {play + 0.1:.2f});')
                html_clips.append(f'<video class="cl" id="{cid}" src="assets/clips/{clip}.mp4" muted playsinline data-start="{play:.2f}" data-duration="{L:.2f}" data-media-start="{c_in:.2f}" data-track-index="{5 + n % 2}"></video>')
                js.append(f'tl.fromTo("#{cid}", {{opacity:0}}, {{opacity:1, duration:{0.3 if how != "after" else 0.01}}}, {play:.2f});')
                if zoom:
                    x, y, z = [float(v) for v in zoom.split(",")]
                    js.append(f'tl.set("#{cid}", {{transformOrigin:"{x / SW * 100:.1f}% {y / SH * 100:.1f}%"}}, 0);')
                    js.append(f'tl.fromTo("#{cid}", {{scale:1}}, {{scale:{z}, duration:{min(1.6, L * 0.6):.2f}, ease:"power2.inOut"}}, {play + 0.3:.2f});')
                for st, f in sounds_of(clip):
                    if c_in - 0.05 <= st < c_out:
                        shutil.copy(os.path.join(ROOT, f), os.path.join(a, "app"))
                        at_s = play + (st - c_in)
                        vol = 0.55 if f.startswith("sounds/") else 1.0
                        if s0 - 0.2 <= at_s <= vo_end: vol = round(vol * 0.35, 2)      # under Sara's line: quieter
                        audio.append(f'<audio id="s{len(audio)}" src="assets/app/{os.path.basename(f)}" data-start="{max(at_s, play):.2f}" data-duration="{dur(os.path.join(ROOT, f)):.2f}" data-volume="{vol}" data-track-index="12"></audio>')
                clip_end = play + L
                last = j + 1 == len(vis)
                if not last:
                    js.append(f'tl.to("#{cid}", {{opacity:0, duration:0.3}}, {clip_end - 0.05:.2f});')
                    at = clip_end - 0.05
                end = max(end, clip_end + TAIL)
            # the last demo's final frame stays on screen until the scene ends (a video shows only while it plays)
            held = f"{clip}-end-{c_out:.1f}.jpg"
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{max(c_in, c_out - 0.12):.2f}", "-i", os.path.join(HERE, "clips", clip + ".mp4"),
                            "-frames:v", "1", "-q:v", "3", os.path.join(a, "clips", held)], check=True)
            html_clips.append(f'<img class="cl" id="{cid}e" src="assets/clips/{held}"' + (f' style="transform-origin:{x / SW * 100:.1f}% {y / SH * 100:.1f}%;transform:scale({z})"' if zoom else '') + '>')
            js.append(f'tl.set("#{cid}e", {{opacity:1}}, {clip_end - 0.06:.2f});')
            lines[i] = (vo, vis, [f"#{cid}", f"#{cid}e"])      # faded at the scene's end below
            phone_on.append((s0 - 0.35, end))
        elif vis is not None:
            sid = f"s{i}"; make = SCENES[vis[1]] if isinstance(vis[1], str) else vis[1]
            body, anim = make(sid)
            scenes.append(f'<section id="{sid}" class="scene">{body}</section>')
            js.append(f'tl.fromTo("#{sid}", {{opacity:0}}, {{opacity:1, duration:0.35}}, {s0 - 0.3:.2f});')
            js += anim(s0, end - s0)
            lines[i] = (vo, vis, sid)
        caps.append((s0, end, LINES[vo]))
        if i + 1 == len(lines): end = vo_end + 1.8
        # the scene steps aside for the next one
        if i + 1 < len(lines):
            last = lines[i][2] if len(lines[i]) > 2 else None
            if isinstance(last, list): js.append(f'tl.to({json.dumps(last)}, {{opacity:0, duration:0.3}}, {end - 0.3:.2f});')
            elif isinstance(last, str): js.append(f'tl.to("#{last}", {{opacity:0, duration:0.3}}, {end - 0.3:.2f});')
        t = end
    total = round(t + 0.4, 2)
    for k, (s, e, text) in enumerate(caps):
        js.append(f'tl.fromTo("#cap{k}", {{opacity:0, y:14}}, {{opacity:1, y:0, duration:0.35, ease:"power2.out"}}, {s - 0.15:.2f});')
        if k + 1 < len(caps): js.append(f'tl.to("#cap{k}", {{opacity:0, duration:0.25}}, {e - 0.3:.2f});')
    # the phone rises in when a demo first shows, and steps aside for the designed scenes
    merged = []
    for s, e in phone_on:
        if merged and s - merged[-1][1] < 0.4: merged[-1][1] = e
        else: merged.append([s, e])
    turns = [s for s, _ in merged]
    for s, e in merged:
        js.append(f'tl.fromTo("#phone", {{opacity:0, y:70}}, {{opacity:1, y:0, duration:0.5, ease:"power3.out"}}, {s:.2f});')
        js.append(f'tl.to("#phone", {{opacity:0, y:40, duration:0.3, ease:"power2.in"}}, {e - 0.3:.2f});')
    turns += [s - 0.3 for s, e, _ in caps if not any(ms <= s <= me for ms, me in merged)]
    for k, s in enumerate(sorted(turns)[1:]):
        audio.append(f'<audio id="pt{k}" src="assets/sfx/page-turn.mp3" data-start="{max(0, s):.2f}" data-duration="1.0" data-volume="0.22" data-track-index="11"></audio>')
    audio += [f'<audio id="pen" src="assets/sfx/pen-stroke.mp3" data-start="0.00" data-duration="0.9" data-volume="0.6" data-track-index="10"></audio>',
              f'<audio id="amb1" src="assets/sfx/fountain.mp3" data-start="0.30" data-duration="{total - 0.3:.2f}" data-volume="0.12" data-fade-in="1" data-fade-out="1.2" data-track-index="8"></audio>',
              f'<audio id="amb2" src="assets/sfx/birds.mp3" data-start="0.60" data-duration="{min(total - 0.6, dur(os.path.join(V6, "sfx-gen/birds.mp3"))):.2f}" data-volume="0.08" data-fade-in="1.5" data-fade-out="1.5" data-track-index="9"></audio>']
    caps_html = "".join(f'<div class="cap" id="cap{k}"><p>{cap(text)}</p></div>' for k, (_, _, text) in enumerate(caps))

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
      <div id="caps">{caps_html}</div>
      <div id="phone"><div class="screen">{''.join(html_clips)}</div></div>
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
    print(f"{vid}: {title}, {total:.1f}s, {len(lines)} lines")

if __name__ == "__main__":
    import sys
    for vid, (title, lines) in VIDEOS.items():
        if len(sys.argv) < 2 or vid in sys.argv[1:]: build(vid, title, list(lines))
