#!/usr/bin/env python3
"""Short "show the website" promos for TikTok / Reels (#215): one entry in promos.json is one video.

1080x1920, 20-25s, no narrator: a hook card, a slot for the owner's screen recording (a labelled placeholder until one is
dropped in), lower-third captions, and the rafiq-arabic.com card. The look, fonts, motion and sound are build_quiz.py's: the
same CSS tokens (imported), calm critically-damped moves, one small spring on the key caption, and the quiet courtyard
fountain under everything, with tap.mp3 as each caption arrives and correct.mp3 on the key one, on the frame that causes them.

  python3 brag-quiz/build_promo.py [id ...]     then in each brag-quiz/out/<id>/composition: npx hyperframes render -o ../<id>.mp4
  python3 brag-quiz/build_promo.py --check       measures every caption and hook line (inside the frame, clear of TikTok's buttons)

Putting the recording in: save it as brag-quiz/screens/<id>.mp4 and build again. A portrait phone recording fills the panel from
the top (the lower part is under the captions: keep the action in the top 60% of the screen); a landscape one fits inside it.
Its own sound is used at "audio" in promos.json (0 = silent). Add "taps": [seconds, ...] to put a tap.mp3 on each tap in it.

Level: the quiz videos set the fountain at data-volume 0.12, which measures about -55 dB before any voice comes in (#217): nothing
to hear. Here the bed is lifted 6 dB when the long copy is made and played at 0.8, so it sits around -34 dB: soft, but there. The taps are
lifted 4 dB and the chime played at 0.5, so both are heard over the fountain without standing out.
"""
import html, json, os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build_quiz as Q                                        # the house CSS tokens, the helpers and the asset folders
ROOT, V6, e, dur = Q.ROOT, Q.V6, Q.e, Q.dur
import re
# Arabic in its own font (as the quiz does), and a hyphenated word like Al-Fātihah never split across two lines
mixed = lambda s: re.sub(r"(?<![\w>])([^\W\d_]+-[^\W\d_]+)(?![\w<])", r'<span style="white-space:nowrap">\1</span>', Q.mixed(s))
BED_GAIN_DB, BED_VOLUME = 6, 0.8
TAP_GAIN_DB = 4                                                # tap.mp3 is lifted a little so it clears the fountain's splashes
SFX_VOLUME = {"tap": 1.0, "correct": 0.5}
FRAME_SAFE_BOTTOM = 1500                                       # TikTok's caption and buttons live below this (and in the right 130px)

CSS = Q.CSS + """
#hook { position:absolute; inset:0; }
#hook .kick { position:absolute; top:200px; left:0; right:0; text-align:center; font-family:var(--ut); font-size:28px; letter-spacing:.16em; color:var(--ink-soft); }
#hook .hero { position:absolute; top:330px; left:0; right:0; text-align:center; font-family:var(--ar); font-weight:700; font-size:230px; line-height:1.3; }
#hook .hero i { display:block; margin:-10px auto 0; width:110px; height:8px; border-radius:4px; background:var(--verdigris); }
#hook .lines { position:absolute; left:80px; right:80px; display:flex; flex-direction:column; gap:34px; text-align:center; }
#hook .l { font-size:84px; font-weight:700; line-height:1.14; letter-spacing:-.02em; }
#hook .l .ar { font-family:var(--ar); color:var(--rubric); font-weight:700; }
#screen { position:absolute; left:90px; top:190px; width:900px; height:1200px; border-radius:44px; overflow:hidden; opacity:0;
  background:var(--card); border:4px solid rgba(23,38,43,.13); box-shadow:0 18px 40px -22px rgba(23,38,43,.4); }
#screen video { position:absolute; inset:0; width:100%; height:100%; object-position:top center; }
.ph { position:absolute; inset:26px; border:6px dashed rgba(23,38,43,.22); border-radius:30px; }
.ph .eb { position:absolute; top:44px; left:0; right:0; text-align:center; font-family:var(--ut); font-size:26px; letter-spacing:.16em; color:var(--rubric); }
.shot { position:absolute; left:60px; right:60px; top:0; bottom:0; display:flex; flex-direction:column; justify-content:center; gap:22px; text-align:center; opacity:0; }
.shot .tc { font-family:var(--ut); font-size:30px; letter-spacing:.08em; color:var(--verdigris); }
.shot .lb { font-size:50px; font-weight:700; line-height:1.22; letter-spacing:-.01em; }
.shot .lb .ar { font-family:var(--ar); color:var(--rubric); }
.cap { position:absolute; left:70px; right:70px; bottom:430px; padding:34px 48px 38px; border-radius:40px; text-align:center; opacity:0;
  background:var(--card); border:4px solid rgba(23,38,43,.13); box-shadow:0 14px 30px -16px rgba(23,38,43,.4);
  font-size:54px; font-weight:700; line-height:1.2; letter-spacing:-.015em; }
.cap .ar { font-family:var(--ar); color:var(--rubric); }
#end .wm { font-family:var(--ar); font-weight:700; font-size:150px; line-height:1.3; margin-top:-6px; }
"""

def tc(t): return f"{int(t) // 60}:{int(t) % 60:02d}"

def long_bed(total, dst):
    """fountain.mp3 played on past its 22s: two copies joined with a 2s crossfade, lifted BED_GAIN_DB, faded in and out"""
    src = os.path.join(V6, "sfx-gen/fountain.mp3")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-i", src, "-filter_complex",
                    f"[0][1]acrossfade=d=2:c1=tri:c2=tri,volume={BED_GAIN_DB}dB,atrim=0:{total + 0.5:.2f},afade=t=in:d=0.6,afade=t=out:st={total - 1.4:.2f}:d=1.4",
                    "-c:a", "libmp3lame", "-q:a", "3", dst], check=True)

def build(p):
    out = os.path.join(HERE, "out", p["id"], "composition"); a = os.path.join(out, "assets")
    if os.path.exists(out): shutil.rmtree(out)
    for d in ("fonts", "lib", "sfx", "screen"): os.makedirs(os.path.join(a, d))
    for f in os.listdir(os.path.join(V6, "fonts")): shutil.copy(os.path.join(V6, "fonts", f), os.path.join(a, "fonts"))
    shutil.copy(os.path.join(V6, "lib/gsap.min.js"), os.path.join(a, "lib"))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(V6, "sfx-gen/tap.mp3"), "-af", f"volume={TAP_GAIN_DB}dB", os.path.join(a, "sfx", "tap.mp3")], check=True)
    shutil.copy(os.path.join(ROOT, "sounds/correct.mp3"), os.path.join(a, "sfx"))
    hk, sc, caps, ou = p["hook"], p["screen"], p["captions"], p["outro"]
    total = round(ou["end"], 2)
    long_bed(total, os.path.join(a, "sfx", "fountain.mp3"))

    rec = os.path.join(HERE, "screens", p["id"] + ".mp4"); has_rec = os.path.exists(rec); fit = "contain"
    if has_rec:
        shutil.copy(rec, os.path.join(a, "screen", p["id"] + ".mp4"))
        w, h = map(int, subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                                                 "-of", "csv=p=0", rec]).decode().strip().split(","))
        fit = "cover" if h > w else "contain"                   # a phone recording fills the panel from the top; a wide one fits inside

    js, audio = [], []
    sfx = lambda f, at, vol: audio.append(f'<audio id="s{len(audio)}" src="assets/sfx/{f}" data-start="{at:.2f}" data-duration="{dur(os.path.join(a, "sfx", f)):.2f}" '
                                         f'data-volume="{vol}" data-track-index="{14 + len(audio) % 2}"></audio>')
    js += [f'tl.fromTo("#glow", {{scale:0.94}}, {{scale:1.08, duration:{total}, ease:"none"}}, 0);',
           'tl.fromTo("#brand", {opacity:0, y:-10}, {opacity:1, y:0, duration:0.4, ease:"power3.out"}, 0);',
           'tl.fromTo("#hook .kick", {opacity:0}, {opacity:1, duration:0.3}, 0.05);']
    if hk.get("hero"): js.append('tl.fromTo("#hook .hero", {opacity:0, scale:0.94}, {opacity:1, scale:1, duration:0.5, ease:"power3.out"}, 0.1);')
    for j, at in enumerate(hk["at"]):
        js.append(f'tl.fromTo("#hl{j}", {{opacity:0, y:24}}, {{opacity:1, y:0, duration:0.5, ease:"power3.out"}}, {at:.2f});')
    js.append(f'tl.to("#hook", {{opacity:0, y:-24, duration:0.35, ease:"power2.in"}}, {hk["end"] - 0.35:.2f});')
    # the screen slot: the panel arrives as the hook leaves, the shot notes (placeholder only) swap, the panel goes as the end card comes
    js.append(f'tl.fromTo("#screen", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.5, ease:"power3.out"}}, {sc["start"] - 0.1:.2f});')
    if not has_rec:
        for k, s in enumerate(sc["shots"]):
            js.append(f'tl.fromTo("#sh{k}", {{opacity:0}}, {{opacity:1, duration:0.3}}, {s["start"] + 0.1:.2f});')
            if k < len(sc["shots"]) - 1: js.append(f'tl.to("#sh{k}", {{opacity:0, duration:0.25}}, {s["end"] - 0.15:.2f});')
    js.append(f'tl.to("#screen", {{opacity:0, y:-24, duration:0.35, ease:"power2.in"}}, {sc["end"] - 0.35:.2f});')
    for i, c in enumerate(caps):
        js += [f'tl.fromTo("#c{i}", {{opacity:0, y:24}}, {{opacity:1, y:0, duration:0.45, ease:"power3.out"}}, {c["start"]:.2f});',
               f'tl.to("#c{i}", {{opacity:0, y:-12, duration:0.3, ease:"power2.in"}}, {c["end"] - 0.3:.2f});']
        if c["sfx"] == "correct":                                # the one small spring: the key line lands
            js.append(f'tl.fromTo("#c{i}", {{scale:1}}, {{scale:1.03, duration:0.16, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {c["start"] + 0.45:.2f});')
        sfx(c["sfx"] + ".mp3", c["start"], SFX_VOLUME[c["sfx"]])
    for t in sc.get("taps", []): sfx("tap.mp3", t, SFX_VOLUME["tap"])
    js += ['tl.to("#brand", {opacity:0, duration:0.3}, ' + f'{ou["start"]:.2f});',
           f'tl.fromTo("#end", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.5, ease:"power3.out"}}, {ou["start"] + 0.15:.2f});']
    audio.append(f'<audio id="bed" src="assets/sfx/fountain.mp3" data-start="0" data-duration="{total:.2f}" data-volume="{BED_VOLUME}" data-track-index="8"></audio>')
    if has_rec and sc.get("audio", 0) > 0:
        audio.append(f'<audio id="screen-audio" src="assets/screen/{p["id"]}.mp4" data-start="{sc["start"]:.2f}" data-duration="{sc["end"] - sc["start"]:.2f}" '
                     f'data-volume="{sc["audio"]}" data-track-index="12"></audio>')

    n = len(hk["lines"]); top = 700 if hk.get("hero") else 560
    lines = "".join(f'<div class="l" id="hl{j}">{mixed(l)}</div>' for j, l in enumerate(hk["lines"]))
    hero = f'<div class="hero" lang="ar">{e(hk["hero"])}<i></i></div>' if hk.get("hero") else ""
    if has_rec:
        panel = (f'<video id="rec" class="clip" src="assets/screen/{p["id"]}.mp4" data-start="{sc["start"]:.2f}" data-duration="{sc["end"] - sc["start"]:.2f}" '
                 f'data-track-index="2" muted playsinline style="object-fit:{fit}"></video>')
    else:
        shots = "".join(f'<div class="shot" id="sh{k}"><div class="tc">{tc(s["start"])} – {tc(s["end"])}</div><div class="lb">{mixed(s["label"])}</div></div>' for k, s in enumerate(sc["shots"]))
        panel = f'<div class="ph"><div class="eb">YOUR SCREEN RECORDING GOES HERE</div>{shots}</div>'
    capsh = "".join(f'<div class="cap" id="c{i}">{mixed(c["text"])}</div>' for i, c in enumerate(caps))
    note = f'<p>{e(ou["note"])}</p>' if ou.get("note") else ""
    doc = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
    <title>Rafiq promo: {e(p['id'])}</title>
    <script src="assets/lib/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{total}">
      <div id="glow"></div>
      <div id="brand"><div class="tile"><span>ر</span><em></em></div><b>رَفِيق</b></div>
      <div id="hook"><div class="kick">{e(p['kicker'])}</div>{hero}<div class="lines" style="top:{top}px">{lines}</div></div>
      <div id="screen">{panel}</div>
      {capsh}
      <div id="end"><div class="tile"><span>ر</span><em></em></div><div class="wm" lang="ar">رَفِيق</div><div class="url">rafiq-arabic.com</div>{note}</div>
{chr(10).join('      ' + x for x in audio)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join('      ' + x for x in js)}
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(out, "index.html"), "w").write(doc)
    print(f"{p['id']}: {total:.1f}s{' (with your recording, fit ' + fit + ')' if has_rec else ' (placeholder where the recording goes)'}")
    return out

def check(p, out):
    """every caption and hook line measured on the real layout: inside the frame, clear of TikTok's buttons, not clipped"""
    from playwright.sync_api import sync_playwright
    bad = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome" if os.path.exists("/opt/pw-browsers/chromium-1194/chrome-linux/chrome") else None)
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto("file://" + os.path.join(out, "index.html"), wait_until="domcontentloaded", timeout=20000); pg.evaluate("document.fonts.ready.then(() => 0)"); pg.wait_for_timeout(500)
        def rect(sel, t):
            pg.evaluate(f'window.__timelines["main"].seek({t}); 0')
            return pg.evaluate("""s => { const n = document.querySelector(s), r = n.getBoundingClientRect(); return { l: r.left, r: r.right, t: r.top, b: r.bottom, over: n.scrollWidth > n.clientWidth + 1 }; }""", sel)
        for i, c in enumerate(p["captions"]):
            r = rect(f"#c{i}", (c["start"] + c["end"]) / 2 + 0.1)
            ok = r["l"] >= 60 and r["r"] <= 1020 and r["b"] <= FRAME_SAFE_BOTTOM and r["t"] >= 1150 and not r["over"]
            print(f"  caption {i + 1}: x {r['l']:.0f}-{r['r']:.0f}, y {r['t']:.0f}-{r['b']:.0f}  {'ok' if ok else 'CHECK THIS'}")
            if not ok: bad.append(f"caption {i + 1}")
        for j in range(len(p["hook"]["lines"])):
            r = rect(f"#hl{j}", p["hook"]["end"] - 0.5)
            ok = r["l"] >= 60 and r["r"] <= 1020 and r["b"] <= 1400 and not r["over"]
            print(f"  hook line {j + 1}: x {r['l']:.0f}-{r['r']:.0f}, y {r['t']:.0f}-{r['b']:.0f}  {'ok' if ok else 'CHECK THIS'}")
            if not ok: bad.append(f"hook line {j + 1}")
        for k, s in enumerate(p["screen"]["shots"]):
            if os.path.exists(os.path.join(HERE, "screens", p["id"] + ".mp4")): break
            r = rect(f"#sh{k} .lb", s["start"] + 0.6)
            ok = r["l"] >= 150 and r["r"] <= 930 and r["b"] <= 1330
            print(f"  shot note {k + 1}: y {r['t']:.0f}-{r['b']:.0f}  {'ok' if ok else 'CHECK THIS'}")
            if not ok: bad.append(f"shot note {k + 1}")
        b.close()
    return bad

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]; run_check = "--check" in sys.argv
    problems = []
    for p in json.load(open(os.path.join(HERE, "promos.json"))):
        if args and p["id"] not in args: continue
        out = build(p)
        if run_check: problems += [(p["id"], x) for x in check(p, out)]
    if run_check:
        print("all inside the frame and clear of TikTok's buttons" if not problems else f"{len(problems)} to look at: {problems}")
        sys.exit(1 if problems else 0)
