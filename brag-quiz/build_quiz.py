#!/usr/bin/env python3
"""Short salah quiz videos for regular posting (#197): one line of data in quizzes.json is one video.

1080x1920, 12-16s, no narrator: the question on screen, the app's native audio for the Arabic, four calm ticks of a
5-second countdown, the answer lighting up, one line of meaning, then rafiq-arabic.com. Formats chosen with TypeSafe
(tools/typesafe-exp/salah_quizzes.py); meanings from salah-data.js (teacher-checked). Motion follows the Apple-design
skill: critically damped moves, a small spring only when the answer lands, sound on the same frame as what causes it.

  python3 brag-quiz/build_quiz.py [id ...]     then in each brag-quiz/out/<id>/composition: npx hyperframes render -o ../<id>.mp4
"""
import html, json, os, re, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
V6 = os.path.join(ROOT, "brag-output-v6/composition/assets")
AUDIO = {x["text"]: x["id"] for x in json.load(open(os.path.join(ROOT, "audio-manifest.json")))}
dur = lambda p: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode())
e = html.escape
# Arabic inside an English line, in the Arabic font (as build.py's captions do)
mixed = lambda s: re.sub(r"([\u0600-\u06ff][\u0600-\u06ff\s]*[\u0600-\u06ff]|[\u0600-\u06ff])", lambda m: f'<bdi class="ar" lang="ar">{m.group(0)}</bdi>', e(s))

CSS = """
@font-face { font-family: "Plex Arabic"; src: url("assets/fonts/ibm-plex-sans-arabic-arabic-600-normal.woff2") format("woff2"); font-weight: 600; }
@font-face { font-family: "Plex Arabic"; src: url("assets/fonts/ibm-plex-sans-arabic-arabic-700-normal.woff2") format("woff2"); font-weight: 700; }
@font-face { font-family: "Karla"; src: url("assets/fonts/karla-latin-500-normal.woff2") format("woff2"); font-weight: 500; }
@font-face { font-family: "Karla"; src: url("assets/fonts/karla-latin-700-normal.woff2") format("woff2"); font-weight: 700; }
@font-face { font-family: "JetBrains Mono"; src: url("assets/fonts/jetbrains-mono-latin-500-normal.woff2") format("woff2"); font-weight: 500; }
:root { --paper:#f1ece0; --card:#f7f3ea; --ink:#17262b; --ink-soft:#4f6163; --rubric:#b4322a; --verdigris:#2e7263;
  --ar:"Plex Arabic","Karla",sans-serif; --la:"Karla",sans-serif; --ut:"JetBrains Mono",monospace; }
body { margin:0; background:var(--paper); font-family:var(--la); color:var(--ink); }
#root { position:relative; width:1080px; height:1920px; overflow:hidden; background:var(--paper); }
#glow { position:absolute; width:1500px; height:1500px; left:-210px; top:-640px; border-radius:50%;
  background:radial-gradient(circle, rgba(168,132,44,.20) 0%, rgba(168,132,44,.05) 45%, rgba(241,236,224,0) 70%); }
#brand { position:absolute; top:84px; left:0; right:0; display:flex; justify-content:center; align-items:center; gap:16px; }
#brand b { font-family:var(--ar); font-size:44px; font-weight:700; }
.tile { position:relative; width:60px; height:60px; border-radius:15px; background:var(--ink); display:grid; place-items:center; }
.tile span { font-family:var(--ar); font-weight:700; font-size:38px; color:var(--paper); margin-top:-6px; }
.tile em { position:absolute; right:10px; top:9px; width:10px; height:10px; border-radius:50%; background:var(--rubric); }
#kicker { position:absolute; top:200px; left:0; right:0; text-align:center; font-family:var(--ut); font-size:28px; letter-spacing:.16em; color:var(--ink-soft); }
#q { position:absolute; top:250px; left:80px; right:80px; text-align:center; font-size:72px; font-weight:700; line-height:1.14; letter-spacing:-.02em; }
#q .qar { display:inline-block; font-family:var(--ar); font-size:84px; color:var(--rubric); line-height:1.5; white-space:nowrap; }
#q .ar, .x .ar { font-family:var(--ar); color:var(--rubric); font-weight:700; }
#hero { position:absolute; top:500px; left:0; right:0; text-align:center; font-family:var(--ar); font-weight:700; font-size:210px; line-height:1.3; }
#hero i { display:block; margin:-10px auto 0; width:90px; height:8px; border-radius:4px; background:var(--verdigris); transform-origin:center; }
#opts { position:absolute; left:90px; right:90px; display:flex; flex-direction:column; gap:24px; }
.opt { position:relative; height:var(--oh,156px); border-radius:36px; background:var(--card); border:4px solid rgba(23,38,43,.13);
  display:flex; align-items:center; justify-content:center; box-shadow:0 12px 26px -16px rgba(23,38,43,.35); }
.opt b { font-size:64px; font-weight:700; letter-spacing:-.01em; }
.opt.arb b { font-family:var(--ar); font-size:86px; line-height:1.4; letter-spacing:0; }
.opt .tick { position:absolute; right:44px; font-size:56px; color:var(--verdigris); opacity:0; }
#count { position:absolute; left:50%; width:150px; height:150px; margin-left:-75px; }
#count svg { position:absolute; inset:0; transform:rotate(-90deg); }
#count circle { fill:none; stroke-width:12; }
#count .bg { stroke:rgba(23,38,43,.12); }
#count .fg { stroke:var(--rubric); stroke-linecap:round; stroke-dasharray:408; stroke-dashoffset:0; }
#count span { position:absolute; inset:0; display:grid; place-items:center; font-size:74px; font-weight:700; opacity:0; }
.x { position:absolute; left:90px; right:90px; text-align:center; }
#xar { font-family:var(--ar); font-weight:700; font-size:70px; color:var(--verdigris); line-height:1.5; }
#xen { font-size:46px; font-weight:700; line-height:1.3; color:var(--ink); }
#ask { font-size:52px; font-weight:700; line-height:1.25; color:var(--rubric); opacity:0; }
#end { position:absolute; top:620px; left:0; right:0; display:flex; flex-direction:column; align-items:center; gap:30px; opacity:0; text-align:center; }
#end .tile { width:170px; height:170px; border-radius:42px; }
#end .tile span { font-size:110px; margin-top:-16px; }
#end .tile em { width:26px; height:26px; right:28px; top:26px; }
#end h2 { margin:10px 60px 0; font-size:76px; line-height:1.12; letter-spacing:-.02em; }
#end .url { font-size:62px; font-weight:700; color:var(--paper); background:var(--verdigris); border-radius:999px; padding:26px 62px; }
#end p { margin:0; font-size:42px; color:var(--ink-soft); }
"""

def build(q):
    out = os.path.join(HERE, "out", q["id"], "composition"); a = os.path.join(out, "assets")
    if os.path.exists(out): shutil.rmtree(out)
    for d in ("fonts", "lib", "sfx", "audio"): os.makedirs(os.path.join(a, d))
    for f in os.listdir(os.path.join(V6, "fonts")): shutil.copy(os.path.join(V6, "fonts", f), os.path.join(a, "fonts"))
    shutil.copy(os.path.join(V6, "lib/gsap.min.js"), os.path.join(a, "lib"))
    for f in ("tap.mp3", "fountain.mp3"): shutil.copy(os.path.join(V6, "sfx-gen", f), os.path.join(a, "sfx"))
    for f in ("correct.mp3",): shutil.copy(os.path.join(ROOT, "sounds", f), os.path.join(a, "sfx"))
    audio, js = [], []
    def say(text, at, vol=1.0):                       # the app's own recording of this Arabic, at time `at`
        src = os.path.join(ROOT, "audio", AUDIO[text] + ".mp3"); shutil.copy(src, os.path.join(a, "audio"))
        d = dur(src); audio.append(f'<audio id="s{len(audio)}" src="assets/audio/{AUDIO[text]}.mp3" data-start="{at:.2f}" data-duration="{d:.2f}" data-volume="{vol}" data-track-index="{10 + len(audio) % 2}"></audio>')
        return d
    def sfx(f, at, d, vol):
        audio.append(f'<audio id="s{len(audio)}" src="assets/sfx/{f}" data-start="{at:.2f}" data-duration="{d:.2f}" data-volume="{vol}" data-track-index="{14 + len(audio) % 2}"></audio>')

    n = len(q["options"]); has_hero = "word" in q
    # where things sit: question at the top; the hero word (if any); options; the countdown under them
    qlines = q["question"].count(chr(10)) + 1 if chr(10) in q["question"] else (3 if len(q["question"]) > 44 else 2)
    OH = 140 if n > 3 else 156                      # option height
    opts_top = 880 if has_hero else 260 + qlines * 84 + 120
    opts_h = n * OH + (n - 1) * 24
    count_top = opts_top + opts_h + 60
    x_top = opts_top + OH + 60                      # after the reveal only the answer is left, in the top slot

    # timeline: question at once (the hook), then the word or the lead phrase, the options, 5-4-3-2-1, the answer
    js += ['tl.fromTo("#brand", {opacity:0, y:-10}, {opacity:1, y:0, duration:0.4, ease:"power3.out"}, 0);',
           'tl.fromTo("#kicker", {opacity:0}, {opacity:1, duration:0.3}, 0.05);',
           'tl.fromTo("#q", {opacity:0, y:24}, {opacity:1, y:0, duration:0.45, ease:"power3.out"}, 0.1);']
    t = 1.0
    if has_hero:
        js += [f'tl.fromTo("#hero", {{opacity:0, scale:0.94}}, {{opacity:1, scale:1, duration:0.5, ease:"power3.out"}}, {t - 0.2:.2f});',
               f'tl.fromTo("#hero i", {{scaleX:0}}, {{scaleX:1, duration:0.5, ease:"power3.out"}}, {t:.2f});']
        d = say(q["word_audio"], t); t += d + 0.35
        js.append(f'tl.fromTo("#hero i", {{scaleX:1}}, {{scaleX:0.4, duration:0.4, ease:"power2.inOut", immediateRender:false}}, {t - 0.4:.2f});')
    if "lead_audio" in q:
        t += say(q["lead_audio"], t, 0.9) + 0.3
    for i in range(n):                                  # each option settles in; voiced ones are said as they arrive
        js.append(f'tl.fromTo("#o{i}", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.4, ease:"power3.out"}}, {t:.2f});')
        if q.get("option_audio"): t += say(q["option_audio"][i], t + 0.15) + 0.4
        else: t += 0.18
    cs = t + 0.5
    js += [f'tl.fromTo("#count", {{opacity:0, scale:0.7}}, {{opacity:1, scale:1, duration:0.3, ease:"power3.out"}}, {cs - 0.3:.2f});',
           f'tl.fromTo("#count .fg", {{strokeDashoffset:0}}, {{strokeDashoffset:408, duration:5, ease:"none"}}, {cs:.2f});']
    for k in range(5):
        js += [f'tl.fromTo("#n{5 - k}", {{opacity:0, scale:1.35}}, {{opacity:1, scale:1, duration:0.22, ease:"power3.out"}}, {cs + k:.2f});',
               f'tl.to("#n{5 - k}", {{opacity:0, duration:0.15}}, {cs + k + 0.82:.2f});']
        sfx("tap.mp3", cs + k, 0.4, 0.45)
    R = cs + 5.05
    js.append(f'tl.to("#count", {{opacity:0, scale:0.7, duration:0.25}}, {R - 0.15:.2f});')
    ans = q["answer"]
    js += [f'tl.to("#o{ans}", {{backgroundColor:"#e3efe9", borderColor:"#2e7263", duration:0.12}}, {R:.2f});',
           f'tl.fromTo("#o{ans}", {{scale:1}}, {{scale:1.05, duration:0.16, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {R:.2f});',   # the one small spring: the answer lands
           f'tl.to("#o{ans} .tick", {{opacity:1, duration:0.2}}, {R:.2f});',
           f'tl.to("{", ".join(f"#o{i}" for i in range(n) if i != ans)}", {{opacity:0.3, duration:0.35}}, {R + 0.1:.2f});',
           # then the wrong ones go, and the answer glides up to the top slot with its meaning under it
           f'tl.to("{", ".join(f"#o{i}" for i in range(n) if i != ans)}", {{opacity:0, duration:0.3}}, {R + 0.9:.2f});',
           f'tl.to("#o{ans}", {{y:{-ans * (OH + 24)}, duration:0.5, ease:"power3.inOut"}}, {R + 1.0:.2f});']
    sfx("correct.mp3", R, 0.6, 0.55)
    rd = say(q["reveal_audio"], R + 0.55)
    if q.get("explain_ar"): js.append(f'tl.fromTo("#xar", {{opacity:0, y:16}}, {{opacity:1, y:0, duration:0.4, ease:"power3.out"}}, {R + 1.4:.2f});')
    js.append(f'tl.fromTo("#xen", {{opacity:0, y:16}}, {{opacity:1, y:0, duration:0.4, ease:"power3.out"}}, {R + 1.6:.2f});')
    E = R + max(4.0, rd + 2.2)
    if q.get("ask"):                                   # a share ask under the meaning, before the end card (#243 findings)
        js.append(f'tl.fromTo("#ask", {{opacity:0, y:16}}, {{opacity:1, y:0, duration:0.4, ease:"power3.out"}}, {R + 2.6:.2f});')
        E = max(E, R + 5.2)
    js += [f'tl.to(["#kicker", "#q", "#hero", "#opts", "#xar", "#xen", "#ask"], {{opacity:0, y:-24, duration:0.35, ease:"power2.in"}}, {E:.2f});',
           f'tl.fromTo("#end", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.5, ease:"power3.out"}}, {E + 0.3:.2f});']
    total = round(E + 2.7, 2)
    audio.append(f'<audio id="bed" src="assets/sfx/fountain.mp3" data-start="0" data-duration="{total:.2f}" data-volume="0.12" data-track-index="8"></audio>')
    js.insert(0, f'tl.fromTo("#glow", {{scale:0.94}}, {{scale:1.08, duration:{total}, ease:"none"}}, 0);')

    # the question: a line that's all Arabic stands on its own, larger and unbroken
    qhtml = "<br>".join(f'<span class="qar" lang="ar">{e(l)}</span>' if re.fullmatch(r"[\u0600-\u06ff\s]+", l) else mixed(l) for l in q["question"].split("\n"))
    cls = "opt arb" if q["rtl"] else "opt"
    opts = "".join(f'<div class="{cls}" id="o{i}"><b{" lang=ar dir=rtl" if q["rtl"] else ""}>{e(o)}</b><span class="tick">✓</span></div>' for i, o in enumerate(q["options"]))
    hero = f'<div id="hero" lang="ar">{e(q["word"])}<i></i></div>' if has_hero else ""
    xar = f'<div class="x" id="xar" style="top:{x_top}px" lang="ar">{e(q["explain_ar"])}</div>' if q.get("explain_ar") else ""
    xen_top = x_top + (120 if q.get("explain_ar") else 0)
    doc = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
    <title>Rafiq quiz: {e(q['id'])}</title>
    <script src="assets/lib/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{total}">
      <div id="glow"></div>
      <div id="brand"><div class="tile"><span>ر</span><em></em></div><b>رَفِيق</b></div>
      <div id="kicker">{e(q['kicker'])}</div>
      <div id="q">{qhtml}</div>
      {hero}
      <div id="opts" style="top:{opts_top}px;--oh:{OH}px">{opts}</div>
      <div id="count" style="top:{count_top}px"><svg viewBox="0 0 150 150"><circle class="bg" cx="75" cy="75" r="65"/><circle class="fg" cx="75" cy="75" r="65"/></svg>{''.join(f'<span id="n{k}">{k}</span>' for k in range(5, 0, -1))}</div>
      {xar}
      <div class="x" id="xen" style="top:{xen_top}px">{mixed(q['explain'])}</div>
      {f'<div class="x" id="ask" style="top:{xen_top + 200}px">{e(q["ask"])}</div>' if q.get("ask") else ""}
      <div id="end"><div class="tile"><span>ر</span><em></em></div><h2>Learn every word of your salah</h2><div class="url">rafiq-arabic.com</div><p>Free for a week · no card needed</p></div>
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
    print(f"{q['id']}: {total:.1f}s")

if __name__ == "__main__":
    for q in json.load(open(os.path.join(HERE, "quizzes.json"))):
        if len(sys.argv) < 2 or q["id"] in sys.argv[1:]: build(q)
