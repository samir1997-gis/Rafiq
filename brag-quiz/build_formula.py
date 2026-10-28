#!/usr/bin/env python3
"""Three videos in the winning formula (brag-quiz/IDEAS.md, "What our best videos do"; #238): a question about something they
already say in the first second, one "aha" pattern, the viewer plays along, 15-26 s, the app last or not at all.

  f1-sujood     "You say this every time you go into sujūd": سُبْحانَ رَبِّيَ الْأَعْلى word by word (salah-data.js),
                ending on a comment everyone can answer: what do you say in rukūʿ instead? (like s3-samiallahu)
  f2-root       "Why do school and teacher look alike?": مَدْرَسَة, مُدَرِّس, دَرَسَ share د ر س; your turn: كِتاب (كَتَبَ, to write),
                3-2-1, a book (like t1-masjid). Meanings: vocab-data.js (book, school, teacher (m)) and toolkit-data.js (to study, to write).
  f3-she-eats   Quiz: if يَأْكُلُ is "he eats", what's "she eats"? Then the past: أَكَلَ → أَكَلَتْ, with أَكَلْتُ "I ate" as the trap
                (like v3-drink). Forms: toolkit-data.js VERBS أَكَلَ.

Every Arabic word is the app's own recording (audio-manifest.json). Built on build_series.py, build_teach.py and build_social.py,
which live on the claude/teach-videos branch: run this from a checkout of that branch.

  python3 brag-quiz/build_formula.py [id ...]     then in each brag-quiz/out/<id>/composition: npx hyperframes render -o ../<id>.mp4
  python3 brag-quiz/build_formula.py --level [id ...]
"""
import json, os, re, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build_teach as T, build_series as S, build_social as SO
from build_teach import Comp, word, e
from build_ten import cnt, countdown, reveal

def f1():
    S.build("f1-sujood", 4, 'You say this <b>every time</b> you go into sujūd', "سُبْحانَ رَبِّيَ الْأَعْلى", 104,
            [("سُبْحانَ", "Glory be to"), ("رَبِّيَ", "my Lord"), ("الْأَعْلى", "the Most High")], "“Glory be to my Lord, the Most High.”",
            "What do you say in rukūʿ instead? Comment it 👇")

def f2():
    c = Comp("f2-root", "ARABIC · ONE ROOT")
    ROWS = [([("مَ", "v"), ("دْ", "r"), ("رَ", "r"), ("سَ", "r"), ("ة", "")], "مَدْرَسَة", "a school"),
            ([("مُ", "v"), ("دَ", "r"), ("رِّ", "r"), ("س", "r")], "مُدَرِّس", "a teacher"),
            ([("دَ", "r"), ("رَ", "r"), ("سَ", "r")], "دَرَسَ", "to study")]
    BOOK = [("كِ", "r"), ("ت", "r"), ("ا", "v"), ("ب", "r")]
    # 1. the hook: school and teacher, side by side, then the verb
    c.inn("#a .q2", 0.1); t = 0.6
    for i, (_, ar, _) in enumerate(ROWS):
        c.inn(f"#r{i}", t, 30); c.sfx("tap", t); c.say(ar, t + 0.35); t += 1.9 if i < 2 else 1.6
    for i in range(3): c.t(f'tl.fromTo("#r{i} .pr", {{color:"{T.INK}"}}, {{color:"{T.RED}", duration:0.35}}, {t + i * 0.2:.2f});')
    c.sfx("tap", t); t += 0.9
    c.inn("#e1", t); c.sfx("tap", t); t += 1.0
    c.inn("#a .say", t); c.sfx("correct", t)
    c.t(f'tl.fromTo("#a .say", {{scale:1}}, {{scale:1.04, duration:0.16, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {t + 0.45:.2f});')
    t += 2.2; c.out_("#a", t)
    # 2. your turn: كِتاب from كَتَبَ, a 3-2-1, then the answer and the ask
    K = t + 0.4
    c.inn("#k .q2", K); c.t(f'tl.fromTo("#k .big", {{opacity:0, scale:0.94}}, {{opacity:1, scale:1, duration:0.5, ease:"power3.out"}}, {K + 0.3:.2f});')
    c.say("كِتاب", K + 0.6)
    c.t(f'tl.fromTo("#k .big .pr", {{color:"{T.INK}"}}, {{color:"{T.RED}", duration:0.3}}, {K + 1.4:.2f});')
    c.inn("#k .hint", K + 1.5)
    cs = K + 2.4
    c.t(f'tl.fromTo("#count", {{opacity:0, scale:0.7}}, {{opacity:1, scale:1, duration:0.3, ease:"power3.out"}}, {cs - 0.3:.2f});')
    c.t(f'tl.fromTo("#count .fg", {{strokeDashoffset:0}}, {{strokeDashoffset:408, duration:3, ease:"none"}}, {cs:.2f});')
    for k in range(3):
        c.t(f'tl.fromTo("#n{3 - k}", {{opacity:0, scale:1.35}}, {{opacity:1, scale:1, duration:0.22, ease:"power3.out"}}, {cs + k:.2f});')
        c.t(f'tl.to("#n{3 - k}", {{opacity:0, duration:0.15}}, {cs + k + 0.82:.2f});'); c.sfx("tap", cs + k)
    R = cs + 3.05
    c.t(f'tl.to("#count", {{opacity:0, scale:0.7, duration:0.25}}, {R - 0.15:.2f});')
    c.t(f'tl.fromTo("#k .ans", {{opacity:0, scale:0.9}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(1.6)"}}, {R:.2f});')
    c.sfx("correct", R); c.say("كِتاب", R + 0.5)
    c.inn("#k .ask2", R + 1.4)
    c.out_("#k", R + 4.0)
    E = R + 4.4
    endc = c.end(E, "Learn the roots behind the words")
    body = f"""      <div class="sec" id="a">
        <div class="q2">Why do <b>school</b> and <b>teacher</b> look alike in Arabic?</div>
        <div class="rows" style="top:480px">{''.join(f'<div class="row" id="r{i}"><div class="en"><b>{e(en)}</b></div><div class="ar">{word(p)}</div></div>' for i, (p, _, en) in enumerate(ROWS))}</div>
        <div class="eqs" style="top:1240px"><div class="eq" id="e1"><span class="tag r" lang="ar">د ر س</span><span class="t">= studying</span></div></div>
        <div class="say" style="top:1470px">Three words, one root.</div>
      </div>
      <div class="sec" id="k">
        <div class="q2">Your turn. What is a <bdi class="ar" lang="ar">كِتاب</bdi>?</div>
        <div class="big" style="top:440px">{word(BOOK)}</div>
        <div class="hint" style="top:800px"><bdi lang="ar" style="font-family:var(--ar);color:var(--rubric)">كَتَبَ</bdi> = to write</div>
        <div id="count" style="top:960px"><svg viewBox="0 0 150 150"><circle class="bg" cx="75" cy="75" r="65"/><circle class="fg" cx="75" cy="75" r="65"/></svg>{''.join(f'<span id="n{k}">{k}</span>' for k in range(3, 0, -1))}</div>
        <div class="ans" style="top:980px">a book</div>
        <div class="ask2" style="position:absolute;left:80px;right:80px;text-align:center;font-size:52px;font-weight:700;color:var(--ink-soft);top:1220px">Which word’s root should I show next? 👇</div>
      </div>
      {endc}"""
    c.write(body, round(E + 2.9, 2))

HOOK_VOICE = "N2lVS1w4EtoT3dr4eOWO"   # Callum: the owner's pick for spoken hooks (12 Oct 2026); Rafiq's voice stays for the Arabic

def clip(c, rel, at, vol=1.0):
    """Any sound file (path from the repo root) on the timeline; returns its length."""
    src = os.path.join(T.ROOT, rel); name = os.path.basename(src); shutil.copy(src, os.path.join(c.a, "audio", name)); d = T.dur(src)
    if "/sfx/" in rel: vol = round(vol * getattr(c, "fx", 1.0), 3)       # c.fx: all the sound effects up or down, the voices as they are
    c.audio.append(f'<audio id="x{len(c.audio)}" src="assets/audio/{name}" data-start="{at:.2f}" data-duration="{d:.2f}" data-volume="{vol}" data-track-index="{16 + len(c.audio) % 3}"></audio>')
    return d

def words_at(rel):
    """Word timings of a spoken line, from the audio (faster-whisper); cached next to the mp3."""
    src = os.path.join(T.ROOT, rel); cache = src[:-4] + ".words.json"
    if not os.path.exists(cache):
        from faster_whisper import WhisperModel
        segs, _ = WhisperModel("small", device="cpu", compute_type="int8").transcribe(src, word_timestamps=True, language="en")
        json.dump([(w.word.strip(), float(w.start)) for sg in segs for w in sg.words], open(cache, "w"))
    return json.load(open(cache))

HOOK_NUMS = [  # numbers counting up all over the hook page: (left, top, size px, start, target, unit, colour, rotation)
    (60, 170, 54, 12, 365, "days", "verdigris", -6), (760, 150, 46, 40, 1200, "hours", "gold", 5), (840, 470, 40, 3, 52, "weeks", "rubric", 8),
    (40, 470, 44, 2, 120, "lessons", "gold", -4), (90, 1220, 64, 900, 10000, "words", "verdigris", -3), (700, 1240, 50, 100, 2555, "days", "rubric", 4),
    (400, 1400, 42, 2, 40, "apps", "gold", -7), (60, 1540, 48, 10, 500, "flashcards", "rubric", 3), (690, 1520, 56, 5, 365, "nights", "verdigris", -5),
    (420, 1730, 40, 2, 7, "years", "gold", 6)]

def hook_in(c, body, hook, bg=None):
    """An opening hook (owner, 12 Oct 2026) in the MOTION-STYLE moves. Each word swooshes in from alternating sides as the hook voice
    says it (the first is there at frame 0); a timer ring at the top counts the years up; numbers count up all over the page; the
    red word bumps, the circled word gets a gold hand-drawn circle, a flash and a shake; then a whip into the quiz.
    hook = (words, {word index: "red" | "circle"}, mp3 spoken with HOOK_VOICE[, (timer label, count)]); the timer counts YEARS to 7 unless given.
    The numbers and the years timer only fit hooks about time spent learning (g4). bg = (html, animate(c, at, d)) puts a background that
    fits this hook's own words in their place (owner, 17 Oct 2026), with no timer."""
    words, marks, mp3, (unit, n) = (*hook, ("YEARS", 7))[:4]
    W = words_at(mp3); d = clip(c, mp3, 0.05)
    at = lambda i: 0.05 + (W[i][1] if i < len(W) else d * i / len(words))
    red = next((i for i, m in marks.items() if m == "red"), 1)
    spans = "".join(f'<span class="hw{" " + marks[i] if i in marks else ""}" id="hw{i}">{w}</span> ' for i, w in enumerate(words))
    circle = '<svg class="hcirc" viewBox="0 0 520 200" preserveAspectRatio="none"><path d="M70 110 C 40 30, 470 15, 500 95 C 520 175, 110 200, 40 130 C 20 110, 70 50, 160 40" pathLength="1"/></svg>'
    nums = "".join(f'<div class="hn {col}" id="hn{k}" style="left:{x}px;top:{y}px;font-size:{sz}px;transform:rotate({r}deg)"><b>{a:,}</b> {u}</div>'
                   for k, (x, y, sz, a, b, u, col, r) in enumerate(HOOK_NUMS))
    timer = ('<div id="htimer"><svg viewBox="0 0 300 300"><circle class="bg" cx="150" cy="150" r="128"/><circle class="fg" cx="150" cy="150" r="128"/></svg>'
             f'<div class="tn"><b id="hty">0</b><span>{unit}</span></div></div>')
    if bg: nums, timer = bg[0], ""
    body.append(f'<div class="sec" id="hook">{nums}{timer}<div class="hookline" id="hl">{spans}</div><div id="hflash"></div></div>')
    os.makedirs(os.path.join(c.a, "fonts"), exist_ok=True)   # Fredoka, round and bubbly, for the hook page (owner, 12 Oct 2026)
    for wt in (600, 700): shutil.copy(os.path.join(T.ROOT, f"brag-quiz/fonts/fredoka-latin-{wt}-normal.woff2"), os.path.join(c.a, "fonts"))
    c.css = getattr(c, "css", "") + (
        "".join(f'@font-face {{ font-family:"Fredoka"; src:url("assets/fonts/fredoka-latin-{wt}-normal.woff2") format("woff2"); font-weight:{wt}; }}' for wt in (600, 700)) +
        "#hook .hookline, #hook .hn, #htimer .tn { font-family:\"Fredoka\", var(--la); }"
        ".hookline { position:absolute; left:60px; right:60px; top:640px; text-align:center; font-weight:700; font-size:112px; line-height:1.06; "
        "letter-spacing:-.01em; color:var(--ink); } .hw { display:inline-block; } .hw.red { color:var(--rubric); } .hw.loud { position:relative; font-size:1.4em; }"
        ".hring { position:absolute; left:50%; top:50%; width:300px; height:300px; margin:-150px; border-radius:50%; border:14px solid #E9B949; opacity:0; }"
        ".hring.r2 { border-color:var(--rubric); border-width:8px; } .hspark { position:absolute; left:50%; top:50%; width:110px; height:12px; margin-top:-6px; "
        "border-radius:6px; background:#E9B949; transform-origin:0 50%; opacity:0; }"
        ".hw.circle { position:relative; color:var(--verdigris); } .hcirc { position:absolute; left:-40px; top:-34px; width:calc(100% + 80px); "
        "height:180px; overflow:visible; } .hcirc path { fill:none; stroke:#E9B949; stroke-width:12; stroke-linecap:round; stroke-dasharray:1; stroke-dashoffset:1; }"
        ".hn { position:absolute; font-weight:700; opacity:.32; white-space:nowrap; letter-spacing:-.02em; } .hn b { font-weight:700; }"
        ".hn.verdigris { color:var(--verdigris); } .hn.gold { color:#a8842c; } .hn.rubric { color:var(--rubric); }"
        "#htimer { position:absolute; left:390px; top:250px; width:300px; height:300px; }"
        "#htimer svg { position:absolute; inset:0; transform:rotate(-90deg); } #htimer circle { fill:none; stroke-width:20; }"
        "#htimer .bg { stroke:rgba(23,38,43,.1); } #htimer .fg { stroke:var(--rubric); stroke-linecap:round; stroke-dasharray:805; stroke-dashoffset:805; }"
        "#htimer .tn { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; line-height:1; }"
        "#htimer .tn b { font-size:120px; color:var(--rubric); } #htimer .tn span { font-size:30px; letter-spacing:.2em; color:var(--ink); margin-top:4px; }"
        "#hflash { position:absolute; inset:0; background:#fff8e6; opacity:0; pointer-events:none; }")
    for i in range(1, len(words)):      # each word swooshes in from alternating sides, blurred (the loud word is already there, huge)
        if marks.get(i) == "loud": continue
        x = -560 if i % 2 else 560
        c.t(f'tl.fromTo("#hw{i}", {{opacity:0, x:{x}, scale:1.3, filter:"blur(16px)"}}, {{opacity:1, x:0, scale:1, filter:"blur(0px)", duration:0.32, ease:"expo.out"}}, {at(i) - 0.08:.2f});')
    for k, (x, y, sz, a, b, u, col, r) in enumerate([] if bg else HOOK_NUMS):   # the numbers count up and drift, from frame 0
        c.t(f'(() => {{ const o = {{v:{a}}}; tl.to(o, {{v:{b}, duration:{d + 0.2:.2f}, ease:"power2.in", onUpdate:() => {{ document.querySelector("#hn{k} b").textContent = '
            f'Math.round(o.v).toLocaleString("en-GB"); }}}}, 0); }})();')
        c.t(f'tl.fromTo("#hn{k}", {{y:0, scale:0.92}}, {{y:{-30 if k % 2 else 26}, scale:1.08, duration:{d + 0.2:.2f}, ease:"none"}}, 0);')
    tr = at(red)                        # the timer: years count up and the ring fills from "years" to the last word
    if bg: bg[1](c, at, d)
    if not bg:
        c.t(f'tl.fromTo("#htimer", {{scale:0.6, opacity:0.4}}, {{scale:1, opacity:1, duration:0.4, ease:"back.out(2)"}}, {tr - 0.1:.2f});')
        c.t(f'tl.fromTo("#htimer .fg", {{strokeDashoffset:805}}, {{strokeDashoffset:0, duration:{d - tr + 0.1:.2f}, ease:"power1.in"}}, {tr:.2f});')
        c.t(f'(() => {{ const o = {{v:0}}; tl.to(o, {{v:{n}, duration:{d - tr + 0.1:.2f}, ease:"power1.in", onUpdate:() => {{ document.getElementById("hty").textContent = Math.floor(o.v); }}}}, {tr:.2f}); }})();')
    c.t(f'tl.fromTo("#hw{red}", {{scale:1}}, {{scale:1.2, duration:0.16, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {tr + 0.25:.2f});')
    for k in range(1, 0 if bg else n + 1):   # a clear tick on every number the timer counts (power1.in: number k at sqrt(k/n) of the way)
        clip(c, "brag-quiz/sfx/ref/click.wav", tr + (d - tr + 0.1) * (k / n) ** 0.5, 0.7)
    for i, m in marks.items():
        if m == "loud":                 # the stressed word lands with force: huge at frame 0, slams down on the voice, crash, shockwave, screen shake
            hit = max(0.16, at(i) + 0.1)
            fx = '<i class="hring"></i><i class="hring r2"></i>' + "".join(f'<i class="hspark" style="transform:rotate({a}deg)"></i>' for a in range(0, 360, 36))
            body[-1] = body[-1].replace(f'id="hw{i}">{words[i]}</span>', f'id="hw{i}">{words[i]}{fx}</span>')
            c.t(f'tl.fromTo("#hw{i}", {{scale:1.9, rotation:-7, x:{getattr(c, "slam_x", 180)}}}, {{scale:1, rotation:0, x:0, duration:{hit:.2f}, ease:"power4.in"}}, 0);')   # c.slam_x: where it starts (a long word on its own line: 0)
            c.t(f'tl.to("#hw{i}", {{keyframes:[{{scaleX:1.18, scaleY:0.78, duration:0.06}}, {{scaleX:0.94, scaleY:1.08, duration:0.08}}, {{scaleX:1, scaleY:1, duration:0.12}}]}}, {hit:.2f});')
            c.t(f'tl.fromTo("#hw{i} .hring", {{scale:0.3, opacity:0.9}}, {{scale:3.2, opacity:0, duration:0.55, ease:"expo.out", stagger:0.07, immediateRender:false}}, {hit:.2f});')
            c.t(f'tl.fromTo("#hw{i} .hspark", {{opacity:1, scaleX:0.2, x:60}}, {{opacity:0, scaleX:1.4, x:260, duration:0.4, ease:"expo.out", immediateRender:false}}, {hit:.2f});')
            c.t(f'tl.fromTo("#hflash", {{opacity:0.85}}, {{opacity:0, duration:0.3, ease:"power2.out", immediateRender:false}}, {hit:.2f});')
            c.t(f'tl.to("#hook", {{keyframes:[{{x:-34, y:22, rotation:-1.4, duration:0.035}}, {{x:30, y:-18, rotation:1.2, duration:0.035}}, {{x:-22, y:14, rotation:-0.8, duration:0.04}}, '
                f'{{x:16, y:-10, rotation:0.6, duration:0.04}}, {{x:-8, y:6, rotation:-0.3, duration:0.05}}, {{x:0, y:0, rotation:0, duration:0.06}}]}}, {hit:.2f});')
            clip(c, "brag-quiz/sfx/crash.wav", hit - 0.02, 0.9)
        if m == "circle":
            body[-1] = body[-1].replace(f'id="hw{i}">{words[i]}</span>', f'id="hw{i}">{words[i]}{circle}</span>')
            c.t(f'tl.fromTo("#hw{i} .hcirc path", {{strokeDashoffset:1}}, {{strokeDashoffset:0, duration:0.45, ease:"power2.inOut"}}, {at(i) + 0.05:.2f});')
            c.t(f'tl.fromTo("#hflash", {{opacity:0.7}}, {{opacity:0, duration:0.35, ease:"power2.out", immediateRender:false}}, {at(i) + 0.05:.2f});')
            c.t(f'tl.fromTo("#hl", {{x:-14}}, {{x:14, duration:0.05, yoyo:true, repeat:5, ease:"none", immediateRender:false}}, {at(i) + 0.05:.2f});')
            c.t(f'tl.set("#hl", {{x:0}}, {at(i) + 0.36:.2f});')
            c.sfx("tap", at(i) + 0.05)
    c.t(f'tl.fromTo("#hl", {{scale:1}}, {{scale:1.06, duration:{d:.2f}, ease:"none"}}, 0);')          # a slow push-in while it's said
    w = d + 0.25                                                                                        # the whip into the quiz
    c.t(f'tl.to("#hook", {{x:-700, opacity:0, filter:"blur(18px)", duration:0.32, ease:"power3.in"}}, {w:.2f});')
    clip(c, "brag-quiz/sfx/ref/swoosh.wav", w - 0.05, 0.5)
    for i in (1, 3, 6): clip(c, "brag-quiz/sfx/ref/short-swoosh.wav", at(i) - 0.1, 0.18)
    return w + 0.25

def say_up(c, text, at, target=-19.0, src=None):
    """c.say, with the app's recording brought up to about the hook voice's level (owner, 12 Oct 2026: Rafiq was ~11 dB quieter).
    src: a retake (brag-quiz/voice/...) to use instead of the app's recording."""
    if src: src = os.path.join(T.ROOT, src); name = os.path.basename(src)[:-4] + "-up.mp3"
    else: src = os.path.join(T.ROOT, "audio", T.AUDIO[text] + ".mp3"); name = T.AUDIO[text] + "-up.mp3"
    m = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    gain = target - float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", m)[-1])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", f"volume={gain:.1f}dB,alimiter=limit=0.95", os.path.join(c.a, "audio", name)], check=True)
    d = T.dur(src)
    c.audio.append(f'<audio id="x{len(c.audio)}" src="assets/audio/{name}" data-start="{at:.2f}" data-duration="{d:.2f}" data-volume="1" data-track-index="{10 + len(c.audio) % 2}"></audio>')
    return d

def count_down(c, cid, at, n=3):
    """The 3-2-1 (or 5-4-3-2-1) ring, with a loud click on every number (owner, 12 Oct 2026)."""
    for k in range(n): clip(c, "brag-quiz/sfx/ref/click.wav", at + k, 1.0)
    if n == 3: return countdown(c, cid, at)
    c.t(f'tl.fromTo("#{cid}", {{opacity:0, scale:0.7}}, {{opacity:1, scale:1, duration:0.3, ease:"power3.out"}}, {at - 0.3:.2f});')
    c.t(f'tl.fromTo("#{cid} .fg", {{strokeDashoffset:0}}, {{strokeDashoffset:408, duration:{n}, ease:"none"}}, {at:.2f});')
    for k in range(n):
        sel = f"#{cid} span:nth-of-type({k + 1})"
        c.t(f'tl.fromTo("{sel}", {{opacity:0, scale:1.35}}, {{opacity:1, scale:1, duration:0.22, ease:"power3.out"}}, {at + k:.2f});')
        c.t(f'tl.to("{sel}", {{opacity:0, duration:0.15}}, {at + k + 0.82:.2f});')
    c.t(f'tl.to("#{cid}", {{opacity:0, scale:0.7, duration:0.25}}, {at + n - 0.1:.2f});')
    return at + n + 0.05

def change(vid, kicker, R, ask, hook=None, vo=None, count=3):
    """The Ashrabu format: "if this is X, what's the <she / we / past / plural> form?", a 3-2-1, the answer said, the rule.
    hook: optional spoken opening line (hook_in); then the first question comes in after it instead of being the cover.
    vo: optional hook-voice lines {"q": [(before the word, after it) per round], "rule": mp3, "end": mp3}: the question is spoken
    around the Arabic word (said in the Rafiq voice), its words appear as they're said, the trick and the closing ask are spoken."""
    c = SO.vcomp(vid, kicker); body, t = [], 0.1
    if vid != "f3-she-eats": c.bed = True              # the fountain under it, as in our other videos (f3 stays as posted)
    if hook: t = hook_in(c, body, hook)
    for k, (ar, en, ask_, opts, right, rule) in enumerate(R):
        s = f"r{k}"
        body.append(f'<div class="sec" id="{s}"><div class="q2">{k + 1}/{len(R)} · If this is “{en}” …</div>'
                    f'<div class="big" id="{s}b" style="top:380px;font-size:150px" lang="ar">{e(ar)}</div>'
                    f'<div class="ques" id="{s}q" style="top:680px">what’s <b>“{ask_}”</b>?</div>{cnt(s + "c", 800).replace("<span>3</span>", "".join(f"<span>{n}</span>" for n in range(count, 2, -1)))}'
                    f'<div class="ops" style="top:990px">' + "".join(f'<div class="op" id="{s}o{i}"><b><span class="ar" lang="ar" style="font-size:80px">{e(o)}</span></b></div>' for i, o in enumerate(opts))
                    + f'</div><div class="rule" id="{s}r" style="top:1500px;font-size:48px">the change: <span class="ar" style="font-size:64px">{rule}</span></div></div>')
        if hook and not k: c.t(f'tl.fromTo("#{s}", {{x:700, opacity:0, filter:"blur(18px)"}}, {{x:0, opacity:1, filter:"blur(0px)", duration:0.35, ease:"power3.out"}}, {t - 0.2:.2f});')
        if k or hook: c.inn(f"#{s} .q2", t); SO.bigin(c, f"#{s}b", t + 0.3)   # without a hook, the first question is the cover (frame 0)
        if vo:                                            # "If this means 'he wrote'..." [the word] "...what's 'I wrote'?"
            a = clip(c, vo["q"][k][0], t); d = say_up(c, ar, t + a + 0.05); tb = t + a + 0.05 + d + 0.15
            b = clip(c, vo["q"][k][1], tb)
            c.t(f'tl.fromTo("#{s}q", {{opacity:0, scale:1.5, filter:"blur(10px)"}}, {{opacity:1, scale:1, filter:"blur(0px)", duration:0.3, ease:"expo.out"}}, {tb:.2f});')
            for i in range(3): c.inn(f"#{s}o{i}", tb + 0.35 + i * 0.12)          # the options come in while the question is said
            done = count_down(c, f"{s}c", max(tb + b + 0.2, tb + 0.9), count)
        else:
            d = say_up(c, ar, t + 0.6)
            c.inn(f"#{s}q", t + 0.6 + d + 0.2)
            for i in range(3): c.inn(f"#{s}o{i}", t + 1.0 + d + i * 0.12)
            done = count_down(c, f"{s}c", t + 1.6 + d + 0.5, count)
        reveal(c, f"#{s}o{right}", [f"#{s}o{i}" for i in range(3) if i != right], done)
        d2 = say_up(c, opts[right], done + 0.3); c.inn(f"#{s}r", done + 0.3 + d2)
        hold = 2.4
        if vo and k == 0 and vo.get("rule"): hold = max(hold, clip(c, vo["rule"], done + 0.4 + d2) + 0.6)
        t = done + 0.3 + d2 + hold; c.out_(f"#{s}", t); t += 0.4
    end = clip(c, vo["end"], t + 0.4) if vo and vo.get("end") else 0
    body.append(c.end(t, ask))                          # SO.finish, but the end card stays until the closing line has been said
    c.write("\n".join("      " + b for b in body), round(max(t + 2.9, t + 0.4 + end + 0.8), 2))

def f3():
    change("f3-she-eats", "QUIZ · ARABIC VERBS",
           [("يَأْكُلُ", "he eats", "she eats", ["آكُلُ", "تَأْكُلُ", "نَأْكُلُ"], 1, '<bdi lang="ar"><em>يَ</em></bdi> → <bdi lang="ar"><em>تَ</em></bdi>'),
            ("أَكَلَ", "he ate", "she ate", ["أَكَلْتُ", "أَكَلَتْ", "أَكَلْنا"], 1, 'add <bdi lang="ar"><em>تْ</em></bdi> to the end')],
           "How many did you get? 0, 1 or 2? 👇")

def say_any(c, text, at, voice):
    """c.say, or an ElevenLabs line (brag-quiz/voice/) for a word the app has no recording of."""
    if text not in voice: return c.say(text, at)
    src = os.path.join(T.ROOT, voice[text]); name = os.path.basename(src)
    shutil.copy(src, os.path.join(c.a, "audio", name)); d = T.dur(src)
    c.audio.append(f'<audio id="s{len(c.audio)}" src="assets/audio/{name}" data-start="{at:.2f}" data-duration="{d:.2f}" data-volume="1.0" data-track-index="{10 + len(c.audio) % 2}"></audio>')
    return d

def root_video(vid, hook, big, root, root_mean, payoff, rows, turn_q, turn_big, turn_ar, ans, ask, voice={}):
    """THE root format (j1-jumuah, our best root video; the owner's rule, 11 Oct 2026: copy it exactly).
    1. hook question + the big word, root letters turn red, "root = meaning", the payoff line (the answer to the hook, by 4 s)
    2. "Once you see it, it's everywhere:" two related words, each with its meaning and why it matters
    3. "Your turn": one more word from the root, the hint, 3-2-1, the answer, then a "send this to ..." ask
    4. the end card. big / rows / turn_big: word() parts; rows: (parts, arabic, meaning, why)."""
    c = Comp(vid, "ARABIC · ONE ROOT")
    # the hook and its word are on screen from frame 0: the cover (FORMATS.md checklist, 11 Oct 2026)
    say_any(c, big[1], 1.0, voice)
    c.t(f'tl.fromTo("#a .big .pr", {{color:"{T.INK}"}}, {{color:"{T.RED}", duration:0.35}}, 2.6);'); c.sfx("tap", 2.6)
    c.inn("#e1", 3.1); c.sfx("tap", 3.1)
    c.inn("#a .say", 4.2); c.sfx("correct", 4.2)
    c.t('tl.fromTo("#a .say", {scale:1}, {scale:1.04, duration:0.16, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}, 4.65);')
    c.out_("#a", 6.4)
    c.inn("#b .q2", 6.8); t = 7.3
    for i, (_, ar, _, _) in enumerate(rows):
        c.inn(f"#r{i}", t, 30); c.sfx("tap", t); say_any(c, ar, t + 0.35, voice)
        c.t(f'tl.fromTo("#r{i} .pr", {{color:"{T.INK}"}}, {{color:"{T.RED}", duration:0.3}}, {t + 0.6:.2f});')
        t += 2.3
    c.out_("#b", t + 0.4)
    K = t + 0.8
    c.inn("#k .q2", K); c.t(f'tl.fromTo("#k .big", {{opacity:0, scale:0.94}}, {{opacity:1, scale:1, duration:0.5, ease:"power3.out"}}, {K + 0.3:.2f});')
    say_any(c, turn_ar, K + 0.6, voice)
    c.t(f'tl.fromTo("#k .big .pr", {{color:"{T.INK}"}}, {{color:"{T.RED}", duration:0.3}}, {K + 1.4:.2f});')
    c.inn("#k .hint", K + 1.5)
    cs = K + 2.4
    c.t(f'tl.fromTo("#count", {{opacity:0, scale:0.7}}, {{opacity:1, scale:1, duration:0.3, ease:"power3.out"}}, {cs - 0.3:.2f});')
    c.t(f'tl.fromTo("#count .fg", {{strokeDashoffset:0}}, {{strokeDashoffset:408, duration:3, ease:"none"}}, {cs:.2f});')
    for k in range(3):
        c.t(f'tl.fromTo("#n{3 - k}", {{opacity:0, scale:1.35}}, {{opacity:1, scale:1, duration:0.22, ease:"power3.out"}}, {cs + k:.2f});')
        c.t(f'tl.to("#n{3 - k}", {{opacity:0, duration:0.15}}, {cs + k + 0.82:.2f});'); c.sfx("tap", cs + k)
    R = cs + 3.05
    c.t(f'tl.to("#count", {{opacity:0, scale:0.7, duration:0.25}}, {R - 0.15:.2f});')
    c.t(f'tl.fromTo("#k .ans", {{opacity:0, scale:0.9}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(1.6)"}}, {R:.2f});')
    c.sfx("correct", R); say_any(c, turn_ar, R + 0.5, voice)
    c.inn("#k .ask2", R + 1.4)
    c.out_("#k", R + 4.0)
    E = R + 4.4
    endc = c.end(E, "Learn the roots behind the words")
    ASK = 'position:absolute;left:80px;right:80px;text-align:center;font-size:52px;font-weight:700;color:var(--ink-soft)'
    body = f"""      <div class="sec" id="a">
        <div class="q2">{hook}</div>
        <div class="big" style="top:470px">{word(big[0])}</div>
        <div class="eqs" style="top:850px"><div class="eq" id="e1"><span class="tag r" lang="ar">{root}</span><span class="t">= {root_mean}</span></div></div>
        <div class="say" style="top:1080px">{payoff}</div>
      </div>
      <div class="sec" id="b">
        <div class="q2">Once you see it, it’s everywhere:</div>
        <div class="rows" style="top:480px">{''.join(f'<div class="row" id="r{i}"><div class="en"><b>{e(en)}</b><span>{e(why)}</span></div><div class="ar">{word(p)}</div></div>' for i, (p, _, en, why) in enumerate(rows))}</div>
      </div>
      <div class="sec" id="k">
        <div class="q2">{turn_q}</div>
        <div class="big" style="top:440px">{word(turn_big)}</div>
        <div class="hint" style="top:800px"><bdi lang="ar" style="font-family:var(--ar);color:var(--rubric)">{root}</bdi> = {root_mean}</div>
        <div id="count" style="top:960px"><svg viewBox="0 0 150 150"><circle class="bg" cx="75" cy="75" r="65"/><circle class="fg" cx="75" cy="75" r="65"/></svg>{''.join(f'<span id="n{k}">{k}</span>' for k in range(3, 0, -1))}</div>
        <div class="ans" style="top:980px">{ans}</div>
        <div class="ask2" style="{ASK};top:1220px">{ask}</div>
      </div>
      {endc}"""
    c.write(body, round(E + 2.9, 2))

def j1():
    """Jumuʿah (9 Oct 2026): why Friday is الجُمُعَة, ج م ع "to gather" (brag-quiz/TEN.md's own source note), جَمْع, جامِعَة,
    your turn جَمِيع = all. Meanings: vocab-data.js (Friday, combining (of prayers), university, all)."""
    root_video("j1-jumuah", 'Why is Friday called <bdi class="ar" lang="ar">الجُمُعَة</bdi>?',
               ([("ال", ""), ("جُ", "r"), ("مُ", "r"), ("عَ", "r"), ("ة", "")], "الجُمُعَة"), "ج م ع", "to gather", "The day of gathering.",
               [([("جَ", "r"), ("مْ", "r"), ("ع", "r")], "جَمْع", "combining", "the prayers, done together"),
                ([("ج", "r"), ("ا", ""), ("مِ", "r"), ("عَ", "r"), ("ة", "")], "جامِعَة", "a university", "the same three letters")],
               'Your turn. What does <bdi class="ar" lang="ar">جَمِيع</bdi> mean?', [("جَ", "r"), ("مِ", "r"), ("ي", ""), ("ع", "r")], "جَمِيع",
               "all", "Send this to who you’re going to Jumuʿah with 🤍")

def a2():
    """Adhān v2 (11 Oct 2026), on the Jumuʿah template after a1 stalled: the payoff by 4 s, two relatives (مُؤَذِّن, which English
    borrowed as "muezzin", and إِذْن), your turn اِسْتَأْذَنَ. Meanings: vocab-data.js (call to prayer, ear); the three new words are
    spoken in the Rafiq voice (brag-quiz/voice/adhan-lines.json)."""
    V = "brag-quiz/voice/adhan/"
    root_video("a2-adhan", 'Why is the call to prayer called the <bdi class="ar" lang="ar">أَذان</bdi>?',
               ([("أَ", "r"), ("ذ", "r"), ("ا", ""), ("ن", "r")], "أَذان"), "أ ذ ن", "the ear", "The announcement made to your ears.",
               [([("مُ", ""), ("ؤَ", "r"), ("ذِّ", "r"), ("ن", "r")], "مُؤَذِّن", "the muʾadhdhin", "who calls it (English: “muezzin”)"),
                ([("إِ", "r"), ("ذْ", "r"), ("ن", "r")], "إِذْن", "permission", "as in “by Allah’s leave”")],
               'Your turn. What does <bdi class="ar" lang="ar">اِسْتَأْذَنَ</bdi> mean?', [("اِسْتَ", ""), ("أْ", "r"), ("ذَ", "r"), ("نَ", "r")], "اِسْتَأْذَنَ",
               "he asked permission", "Send this to whoever wakes you up for Fajr 🤍",
               voice={"مُؤَذِّن": V + "muadhdhin.mp3", "إِذْن": V + "idhn.mp3", "اِسْتَأْذَنَ": V + "istadhana.mp3"})

def a1():
    """Adhān (10 Oct 2026, after the Instagram analysis: short, a question in the first second, a share ask): why the call
    to prayer is the أَذان, أ ذ ن the root of hearing; your turn أُذُن = ear. Meanings: vocab-data.js (call to prayer, ear)."""
    c = Comp("a1-adhan", "ARABIC · ONE ROOT")
    ADHAN = [("أَ", "r"), ("ذا", "r"), ("ن", "r")]
    EAR = [("أُ", "r"), ("ذُ", "r"), ("ن", "r")]
    # the hook and its word are on screen from frame 0: the cover (FORMATS.md checklist, 11 Oct 2026)
    c.say("أَذان", 1.0)
    c.inn("#e1", 2.4); c.sfx("tap", 2.4)
    c.out_("#a", 4.0)
    K = 4.4
    c.inn("#k .q2", K); c.t(f'tl.fromTo("#k .big", {{opacity:0, scale:0.94}}, {{opacity:1, scale:1, duration:0.5, ease:"power3.out"}}, {K + 0.3:.2f});')
    c.say("أُذُن", K + 0.6)
    c.t(f'tl.fromTo("#k .big .pr", {{color:"{T.INK}"}}, {{color:"{T.RED}", duration:0.3}}, {K + 1.4:.2f});')
    c.inn("#k .hint", K + 1.5)
    cs = K + 2.4
    c.t(f'tl.fromTo("#count", {{opacity:0, scale:0.7}}, {{opacity:1, scale:1, duration:0.3, ease:"power3.out"}}, {cs - 0.3:.2f});')
    c.t(f'tl.fromTo("#count .fg", {{strokeDashoffset:0}}, {{strokeDashoffset:408, duration:3, ease:"none"}}, {cs:.2f});')
    for k in range(3):
        c.t(f'tl.fromTo("#n{3 - k}", {{opacity:0, scale:1.35}}, {{opacity:1, scale:1, duration:0.22, ease:"power3.out"}}, {cs + k:.2f});')
        c.t(f'tl.to("#n{3 - k}", {{opacity:0, duration:0.15}}, {cs + k + 0.82:.2f});'); c.sfx("tap", cs + k)
    R = cs + 3.05
    c.t(f'tl.to("#count", {{opacity:0, scale:0.7, duration:0.25}}, {R - 0.15:.2f});')
    c.t(f'tl.fromTo("#k .ans", {{opacity:0, scale:0.9}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(1.6)"}}, {R:.2f});')
    c.sfx("correct", R); c.say("أُذُن", R + 0.5)
    c.inn("#k .say", R + 1.2); c.inn("#k .ask2", R + 2.2)
    c.out_("#k", R + 5.0)
    E = R + 5.4
    endc = c.end(E, "Learn the roots behind the words")
    ASK = 'position:absolute;left:80px;right:80px;text-align:center;font-size:52px;font-weight:700;color:var(--ink-soft)'
    body = f"""      <div class="sec" id="a">
        <div class="q2">Why is the call to prayer called the <bdi class="ar" lang="ar">أَذان</bdi>?</div>
        <div class="big" style="top:470px">{word(ADHAN)}</div>
        <div class="eqs" style="top:850px"><div class="eq" id="e1"><span class="tag r" lang="ar">أ ذ ن</span><span class="t">= the root of hearing</span></div></div>
      </div>
      <div class="sec" id="k">
        <div class="q2">Your turn: what’s an <bdi class="ar" lang="ar">أُذُن</bdi>?</div>
        <div class="big" style="top:440px">{word(EAR)}</div>
        <div class="hint" style="top:800px"><bdi lang="ar" style="font-family:var(--ar);color:var(--rubric)">أ ذ ن</bdi> = hearing</div>
        <div id="count" style="top:960px"><svg viewBox="0 0 150 150"><circle class="bg" cx="75" cy="75" r="65"/><circle class="fg" cx="75" cy="75" r="65"/></svg>{''.join(f'<span id="n{k}">{k}</span>' for k in range(3, 0, -1))}</div>
        <div class="ans" style="top:980px">an ear 👂</div>
        <div class="say" style="top:1180px">The adhān is the call made for your ears.</div>
        <div class="ask2" style="{ASK};top:1420px">Send this to whoever wakes you up for Fajr 🤍</div>
      </div>
      {endc}"""
    c.write(body, round(E + 2.9, 2))

# 10 Oct 2026, the owner's read of what works: a salah line word by word, one root traced to its relatives, and the
# word-change quiz. Meanings: salah-data.js (the lines) and vocab-data.js / toolkit-data.js (the words).
def wbw(*a):
    """build_series.build with the fountain bed on (the series builder turns it off)."""
    comp = S.Comp; S.Comp = lambda *x, **k: comp(*x, **{**k, "bed": True})
    try: S.build(*a)
    finally: S.Comp = comp

def w5(): wbw("w5-rabbana", 5, 'You say this <b>every time</b> you stand up from rukūʿ', "رَبَّنا وَلَكَ الْحَمْدُ", 110,
                  [("رَبَّنا", "Our Lord"), ("وَلَكَ", "and to You"), ("الْحَمْدُ", "all praise")],
                  "“Our Lord, and to You belongs all praise.”", "What does the imam say just before it? Comment it 👇")
def w6(): wbw("w6-salam", 6, 'You say this to <b>end every prayer</b>', "السَّلامُ عَلَيْكُمْ وَرَحْمَةُ اللَّهِ", 84,
                  [("السَّلامُ", "Peace"), ("عَلَيْكُمْ", "be upon you"), ("وَرَحْمَةُ", "and the mercy"), ("اللَّهِ", "of Allah")],
                  "“Peace be upon you and the mercy of Allah.”", "Right side first, or left? Comment it 👇")
def w7(): wbw("w7-tahiyyat", 7, 'You say this <b>every time</b> you sit in salah', "التَّحِيّاتُ لِلَّهِ وَالصَّلَواتُ وَالطَّيِّباتُ", 76,
                  [("التَّحِيّاتُ", "All greetings"), ("لِلَّهِ", "are for Allah"), ("وَالصَّلَواتُ", "and the prayers"), ("وَالطَّيِّباتُ", "and the good things")],
                  "“All greetings are for Allah, and the prayers and the good things.”", "What’s the next line? Comment it 👇")

def g1(): change("g1-plural", "QUIZ · ONE BECOMES MANY",
                 [("كِتاب", "a book", "books", ["كِتابان", "كُتُب", "مَكْتَبَة"], 1, 'no ending: the inside changes'),
                  ("صَدِيق", "a friend", "friends", ["صَدِيقان", "أَصْدِقاء", "صَداقَة"], 1, 'a new shape: <bdi lang="ar"><em>أَ</em>…<em>اء</em></bdi>')],
                 "How many did you get? 0, 1 or 2? 👇")
def g2(): change("g2-female", "QUIZ · HE OR SHE",
                 [("مُعَلِّم", "teacher (m)", "teacher (f)", ["مُعَلِّمُون", "مُعَلِّمَة", "تَعْلِيم"], 1, 'add <bdi lang="ar"><em>ة</em></bdi> to the end'),
                  ("جَمِيلٌ", "beautiful (m)", "beautiful (f)", ["جَمِيلَة", "جَمال", "أَجْمَل"], 0, 'the same <bdi lang="ar"><em>ة</em></bdi>')],
                 "How many did you get? 0, 1 or 2? 👇")
def g3(): change("g3-past", "QUIZ · ARABIC VERBS",
                 [("يَشْرَبُ", "he drinks", "he drank", ["شَرِبَ", "شَرِبْتُ", "اشْرَبْ"], 0, 'the past starts on the root: <bdi lang="ar"><em>ش ر ب</em></bdi>'),
                  ("نَشْرَبُ", "we drink", "we drank", ["شَرِبُوا", "شَرِبْنا", "شَرِبْتُ"], 1, '<bdi lang="ar"><em>ـنا</em></bdi> on the end = we')],
                 "How many did you get? 0, 1 or 2? 👇")

# 11 Oct 2026: our three audited table videos (v1-go, v2-write, i4-ta-marbuta: no bed, blank first frame, nothing to play)
# rebuilt in the word-change format. Forms: toolkit-data.js VERBS (ذَهَبَ, كَتَبَ); nouns: vocab-data.js.
def v1q(): change("v1-go-quiz", "QUIZ · ARABIC VERBS",
                  [("أَذْهَبُ", "I go", "we go", ["تَذْهَبُ", "نَذْهَبُ", "يَذْهَبُ"], 1, '<bdi lang="ar"><em>أَ</em></bdi> → <bdi lang="ar"><em>نَ</em></bdi>'),
                   ("يَذْهَبُ", "he goes", "she goes", ["تَذْهَبُ", "نَذْهَبُ", "أَذْهَبُ"], 0, '<bdi lang="ar"><em>يَ</em></bdi> → <bdi lang="ar"><em>تَ</em></bdi>')],
                  "How many did you get? 0, 1 or 2? 👇")
def v2q(): change("v2-write-quiz", "QUIZ · ARABIC VERBS",
                  [("كَتَبْتُ", "I wrote", "we wrote", ["كَتَبَتْ", "كَتَبْنا", "كَتَبَ"], 1, '<bdi lang="ar"><em>ـتُ</em></bdi> → <bdi lang="ar"><em>ـنا</em></bdi>'),
                   ("كَتَبَ", "he wrote", "she wrote", ["كَتَبْتُ", "كَتَبْنا", "كَتَبَتْ"], 2, 'add <bdi lang="ar"><em>تْ</em></bdi> to the end')],
                  "How many did you get? 0, 1 or 2? 👇")
def i4q(): change("i4-she-quiz", "QUIZ · HE OR SHE",
                  [("جَدّ", "grandfather", "grandmother", ["جَدَّة", "أَجْداد", "جَدّان"], 0, 'add <bdi lang="ar"><em>ة</em></bdi> to the end'),
                   ("أَخ", "brother", "sister", ["أَخَة", "أُخْت", "إِخْوَة"], 1, 'not always <bdi lang="ar"><em>ة</em></bdi>: <bdi lang="ar"><em>أُخْت</em></bdi>')],
                  "How many did you get? 0, 1 or 2? Comment below 👇 and send this to your Arabic study buddy",
                  # the g4 standard (owner, 13 Oct 2026: it's retaining better): the same hook, Callum asks each question
                  hook=("MOST of you will get the second one WRONG!".split(), {0: "loud", 6: "red", 8: "circle"},   # owner, 13 Oct
                        "brag-quiz/voice/i4-hook4/i4-h4b.mp3", ("QUESTIONS", 2)),
                  vo={"q": [("brag-quiz/voice/i4-vo/q1a.mp3", "brag-quiz/voice/i4-vo/q1b.mp3"),
                            ("brag-quiz/voice/i4-vo/q2a.mp3", "brag-quiz/voice/i4-vo/q2b.mp3")],
                      "rule": "brag-quiz/voice/i4-vo/rule.mp3", "end": "brag-quiz/voice/g4-vo/end2.mp3"})

def r2():
    """Why the Prophet ﷺ is named مُحَمَّد: ح م د, praise, as in الْحَمْدُ and حَمِدَهُ; your turn أَحْمَد (his other name, Qurʾān 61:6)."""
    c = Comp("r2-muhammad", "ARABIC · ONE ROOT")
    MUH = [("مُ", ""), ("حَ", "r"), ("مَّ", "r"), ("د", "r")]
    ROWS = [([("الْ", ""), ("حَ", "r"), ("مْ", "r"), ("دُ", "r")], "الْحَمْدُ", "all praise", "al-ḥamdu lillāh, in every rakʿah"),
            ([("حَ", "r"), ("مِ", "r"), ("دَ", "r"), ("هُ", "")], "حَمِدَهُ", "praises Him", "samiʿa Allāhu liman ḥamidah")]
    AH = [("أَ", ""), ("حْ", "r"), ("مَ", "r"), ("د", "r")]
    # the hook and its word are on screen from frame 0: the cover (FORMATS.md checklist, 11 Oct 2026)
    c.say("مُحَمَّد", 1.0)
    c.t(f'tl.fromTo("#a .big .pr", {{color:"{T.INK}"}}, {{color:"{T.RED}", duration:0.35}}, 2.2);'); c.sfx("tap", 2.2)
    c.inn("#e1", 2.7); c.sfx("tap", 2.7)
    c.inn("#a .say", 3.8); c.sfx("correct", 3.8)
    c.out_("#a", 6.0)
    c.inn("#b .q2", 6.4); t = 6.9
    for i, (_, ar, _, _) in enumerate(ROWS):
        c.inn(f"#r{i}", t, 30); c.sfx("tap", t); c.say(ar, t + 0.35)
        c.t(f'tl.fromTo("#r{i} .pr", {{color:"{T.INK}"}}, {{color:"{T.RED}", duration:0.3}}, {t + 0.6:.2f});')
        t += 2.3
    c.out_("#b", t + 0.4)
    K = t + 0.8
    c.inn("#k .q2", K); c.t(f'tl.fromTo("#k .big", {{opacity:0, scale:0.94}}, {{opacity:1, scale:1, duration:0.5, ease:"power3.out"}}, {K + 0.3:.2f});')
    c.say("أَحْمَد", K + 0.6)
    c.t(f'tl.fromTo("#k .big .pr", {{color:"{T.INK}"}}, {{color:"{T.RED}", duration:0.3}}, {K + 1.4:.2f});')
    c.inn("#k .hint", K + 1.5)
    cs = K + 2.4
    c.t(f'tl.fromTo("#count", {{opacity:0, scale:0.7}}, {{opacity:1, scale:1, duration:0.3, ease:"power3.out"}}, {cs - 0.3:.2f});')
    c.t(f'tl.fromTo("#count .fg", {{strokeDashoffset:0}}, {{strokeDashoffset:408, duration:3, ease:"none"}}, {cs:.2f});')
    for k in range(3):
        c.t(f'tl.fromTo("#n{3 - k}", {{opacity:0, scale:1.35}}, {{opacity:1, scale:1, duration:0.22, ease:"power3.out"}}, {cs + k:.2f});')
        c.t(f'tl.to("#n{3 - k}", {{opacity:0, duration:0.15}}, {cs + k + 0.82:.2f});'); c.sfx("tap", cs + k)
    R = cs + 3.05
    c.t(f'tl.to("#count", {{opacity:0, scale:0.7, duration:0.25}}, {R - 0.15:.2f});')
    c.t(f'tl.fromTo("#k .ans", {{opacity:0, scale:0.9}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(1.6)"}}, {R:.2f});')
    c.sfx("correct", R); c.say("أَحْمَد", R + 0.5)
    c.inn("#k .say", R + 1.2); c.inn("#k .ask2", R + 2.2)
    c.out_("#k", R + 5.0)
    E = R + 5.4
    endc = c.end(E, "Learn the roots behind the words")
    ASK = 'position:absolute;left:80px;right:80px;text-align:center;font-size:52px;font-weight:700;color:var(--ink-soft)'
    body = f"""      <div class="sec" id="a">
        <div class="q2">Why is the Prophet <span style="font-family:var(--ar)">ﷺ</span> named <bdi class="ar" lang="ar">مُحَمَّد</bdi>?</div>
        <div class="big" style="top:470px">{word(MUH)}</div>
        <div class="eqs" style="top:850px"><div class="eq" id="e1"><span class="tag r" lang="ar">ح م د</span><span class="t">= praise</span></div></div>
        <div class="say" style="top:1080px">The one praised, again and again.</div>
      </div>
      <div class="sec" id="b">
        <div class="q2">You say this root in every prayer:</div>
        <div class="rows" style="top:480px">{''.join(f'<div class="row" id="r{i}"><div class="en"><b>{e(en)}</b><span>{e(why)}</span></div><div class="ar">{word(p)}</div></div>' for i, (p, _, en, why) in enumerate(ROWS))}</div>
      </div>
      <div class="sec" id="k">
        <div class="q2">Your turn: what does <bdi class="ar" lang="ar">أَحْمَد</bdi> mean?</div>
        <div class="big" style="top:440px">{word(AH)}</div>
        <div class="hint" style="top:800px"><bdi lang="ar" style="font-family:var(--ar);color:var(--rubric)">ح م د</bdi> = praise</div>
        <div id="count" style="top:960px"><svg viewBox="0 0 150 150"><circle class="bg" cx="75" cy="75" r="65"/><circle class="fg" cx="75" cy="75" r="65"/></svg>{''.join(f'<span id="n{k}">{k}</span>' for k in range(3, 0, -1))}</div>
        <div class="ans" style="top:980px">the most praised</div>
        <div class="say" style="top:1180px">His other name, in the Qurʾān (61:6).</div>
        <div class="ask2" style="{ASK};top:1420px">Send this to a Muhammad or an Ahmad you know 🤍</div>
      </div>
      {endc}"""
    c.write(body, round(E + 2.9, 2))

def r3():
    """Recreated from p1-akbar (#246) in the root format: أَكْبَرُ, ك ب ر "big, great"; كَبِير (vocab-data.js 161), تَكْبِير; your turn كِبار.
    أَكْبَرُ "is the Greatest" is salah-data.js's; تَكْبِير and كِبار are spoken in the Rafiq voice (brag-quiz/voice/recreate-lines.json)."""
    V = "brag-quiz/voice/recreate/"
    root_video("r3-akbar", 'What does <bdi class="ar" lang="ar">أَكْبَرُ</bdi> in Allāhu akbar really mean?',
               ([("أَ", ""), ("كْ", "r"), ("بَ", "r"), ("رُ", "r")], "أَكْبَرُ"), "ك ب ر", "big, great", "Greater than everything.",
               [([("كَ", "r"), ("بِ", "r"), ("ي", ""), ("ر", "r")], "كَبِير", "big", "the same three letters"),
                ([("تَ", ""), ("كْ", "r"), ("بِ", "r"), ("ي", ""), ("ر", "r")], "تَكْبِير", "the takbīr", "saying Allāhu akbar: how salah begins")],
               'Your turn. What does <bdi class="ar" lang="ar">كِبار</bdi> mean?', [("كِ", "r"), ("بَ", "r"), ("ا", ""), ("ر", "r")], "كِبار",
               "grown-ups", "Send this to whoever you pray with 🤍",
               voice={"تَكْبِير": V + "takbir.mp3", "كِبار": V + "kibar.mp3"})

def r4():
    """Recreated from p5-insha (#246) in the root format: شاءَ, ش ي ء "to will"; ما شاءَ اللهُ (vocab-data.js 71), مَشِيئَة; your turn شَيْء.
    مَشِيئَة is spoken in the Rafiq voice (brag-quiz/voice/recreate-lines.json)."""
    V = "brag-quiz/voice/recreate/"
    root_video("r4-insha", 'What does <bdi class="ar" lang="ar">إِنْ شاءَ اللهُ</bdi> actually say?',
               ([("ش", "r"), ("ا", ""), ("ءَ", "r")], "شاءَ"), "ش ي ء", "to will", "If Allah wills.",
               [([("ما\u00a0", ""), ("ش", "r"), ("ا", ""), ("ءَ", "r"), ("\u00a0اللهُ", "")], "ما شاءَ اللهُ", "what Allah has willed", "when you see something good"),
                ([("مَ", ""), ("شِ", "r"), ("ي", "r"), ("ئَ", "r"), ("ة", "")], "مَشِيئَة", "will", "Allah’s will: His mashīʾa")],
               'Your turn. What does <bdi class="ar" lang="ar">شَيْء</bdi> mean?', [("شَ", "r"), ("يْ", "r"), ("ء", "r")], "شَيْء",
               "a thing", "Send this to someone who says in shā’ Allāh every day 🤍",
               voice={"مَشِيئَة": V + "mashia.mp3"})

def g4(): change("g4-past-i", "QUIZ · ARABIC VERBS",            # recreated from v1-go and v2-write (#246)
                 [("كَتَبَ", "he wrote", "I wrote", ["كَتَبَتْ", "كَتَبْتُ", "كَتَبْنا"], 1, '<bdi lang="ar"><em>ـتُ</em></bdi> on the end = I'),
                  ("ذَهَبَ", "he went", "I went", ["ذَهَبْتُ", "ذَهَبَتْ", "ذَهَبْنا"], 0, 'the same <bdi lang="ar"><em>ـتُ</em></bdi>')],
                 "How many did you get? 0, 1 or 2? Comment below 👇 and send this to your Arabic study buddy",
                 hook=("MOST people learn Arabic for years before they notice this trick!".split(), {0: "loud", 5: "red", 10: "circle"},
                       "brag-quiz/voice/g4-hook3/g4-v3a.mp3"),
                 vo={"q": [("brag-quiz/voice/g4-vo/q1a.mp3", "brag-quiz/voice/g4-vo/q1b.mp3"),
                           ("brag-quiz/voice/g4-vo/q2a.mp3", "brag-quiz/voice/g4-vo/q2b.mp3")],
                     "rule": "brag-quiz/voice/g4-vo/rule.mp3", "end": "brag-quiz/voice/g4-vo/end2.mp3"})

def g5(): change("g5-endings", "QUIZ · MY, HIS, HER",           # IDEAS "one word, many endings" in the g4 standard (#261)
                 [("اسْمِي", "my name", "his name", ["اسْمُها", "اسْمُهُ", "اسْمُكَ"], 1, '<bdi lang="ar"><em>ـهُ</em></bdi> on the end = his'),
                  ("بَيْتُكَ", "your house", "her house", ["بَيْتُهُ", "بَيْتُكِ", "بَيْتُها"], 2, '<bdi lang="ar"><em>ـها</em></bdi> = her, not <bdi lang="ar"><em>ـهُ</em></bdi>')],
                 "How many did you get? 0, 1 or 2? Comment below 👇 and send this to your Arabic study buddy",
                 hook=("NOBODY tells you Arabic has no word for “my”!".split(), {0: "loud", 5: "red", 8: "circle"},
                       "brag-quiz/voice/g5-hook/g5-h1b.mp3", ("QUESTIONS", 2)),
                 vo={"q": [("brag-quiz/voice/g5-vo/q1a.mp3", "brag-quiz/voice/g5-vo/q1b.mp3"),
                           ("brag-quiz/voice/g5-vo/q2a.mp3", "brag-quiz/voice/g5-vo/q2b.mp3")],
                     "rule": "brag-quiz/voice/g5-vo/rule.mp3", "end": "brag-quiz/voice/g4-vo/end2.mp3"})

def w8(): wbw("w8-subhana-azim", 8, 'You say this <b>every time</b> you bow in rukūʿ', "سُبْحانَ رَبِّيَ الْعَظِيمِ", 104,   # recreated from t2-subhana (#246)
                  [("سُبْحانَ", "Glory be to"), ("رَبِّيَ", "my Lord"), ("الْعَظِيمِ", "the Magnificent")],
                  "“Glory be to my Lord, the Magnificent.”", "What do you say in sujūd instead? Comment it 👇")

def n1():
    """Root series part 3 (owner, 13 Oct 2026: a weekly series he stitches himself onto): why Paradise is الْجَنَّة. ج ن ن "to hide,
    to cover": a garden so thick its ground is hidden; جِنّ the hidden beings; مَجْنُون "mad", the mind covered (Layla and Majnūn);
    your turn جَنِين, the baby hidden in the womb. The four words are spoken in the Rafiq voice (brag-quiz/voice/jannah-lines.json;
    جِنّ written جِنْ so it isn't read "jinna")."""
    V = "brag-quiz/voice/jannah/"
    root_video("n1-jannah", 'Why is Paradise called <bdi class="ar" lang="ar">الْجَنَّة</bdi>?',
               ([("الْ", ""), ("جَ", "r"), ("نَّ", "r"), ("ة", "")], "الْجَنَّة"), "ج ن ن", "to hide, to cover",
               "A garden so full of trees, it hides the ground.",
               [([("جِ", "r"), ("نّ", "r")], "جِنّ", "the jinn", "beings hidden from our eyes"),
                ([("مَ", ""), ("جْ", "r"), ("نُ", "r"), ("و", ""), ("ن", "r")], "مَجْنُون", "mad", "the mind covered (Layla and Majnūn)")],
               'Your turn. What does <bdi class="ar" lang="ar">جَنِين</bdi> mean?', [("جَ", "r"), ("نِ", "r"), ("ي", ""), ("ن", "r")], "جَنِين",
               "a baby in the womb", "Send this to someone you want to meet in Jannah 🤍",
               voice={"الْجَنَّة": V + "jannah.mp3", "جِنّ": V + "jinn.mp3", "مَجْنُون": V + "majnun.mp3", "جَنِين": V + "janin.mp3"})

MASH_CSS = (
    ".chips { position:absolute; left:70px; right:70px; display:flex; flex-direction:row-reverse; justify-content:center; gap:26px; }"
    ".chip { width:290px; padding:18px 0 22px; text-align:center; background:var(--card); border:4px solid rgba(23,38,43,.13); border-radius:32px; "
    "box-shadow:0 12px 26px -16px rgba(23,38,43,.35); } .chip .ar { font-family:var(--ar); font-weight:700; font-size:84px; line-height:1.35; color:var(--rubric); }"
    ".chip b { display:block; font-size:42px; color:var(--ink); } .big .w { display:inline-block; }"
    ".stamp { position:absolute; left:50%; top:560px; transform:translateX(-50%) rotate(-8deg); padding:10px 34px; border:8px solid var(--rubric); border-radius:22px; "
    "font-family:\"Fredoka\", var(--la); font-size:76px; font-weight:700; letter-spacing:.04em; color:var(--rubric); white-space:nowrap; }"
    ".card2 { position:absolute; left:80px; right:80px; display:flex; align-items:center; gap:30px; padding:22px 36px; background:var(--card); "
    "border:4px solid rgba(23,38,43,.13); border-radius:32px; box-shadow:0 12px 26px -16px rgba(23,38,43,.35); }"
    ".card2 .ar { font-family:var(--ar); font-weight:700; font-size:70px; line-height:1.4; min-width:380px; text-align:center; }"
    ".card2 .t { font-size:44px; font-weight:700; line-height:1.15; } .card2 .t small { display:block; font-size:32px; color:var(--ink-soft); }"
    ".card2.ok { border-color:var(--verdigris); } .card2.ok .t { color:var(--verdigris); } .card2.fut .t { color:#a8842c; }"
    ".rootq { position:absolute; left:0; right:0; top:420px; text-align:center; font-family:var(--ar); font-weight:700; font-size:150px; color:var(--rubric); }"
    ".qr { position:absolute; left:60px; right:60px; top:440px; text-align:center; font-family:var(--ar); font-weight:700; font-size:104px; line-height:1.55; direction:rtl; }"
    ".qr .w { display:inline-block; color:rgba(23,38,43,.28); } .qref { position:absolute; left:0; right:0; top:330px; text-align:center; font-size:40px; "
    "font-weight:700; letter-spacing:.12em; color:#a8842c; margin-top:24px; } .qen { position:absolute; left:90px; right:90px; top:900px; text-align:center; "
    "font-family:\"Instrument Serif\", serif; font-style:italic; font-size:60px; line-height:1.2; color:var(--ink); }"
    ".bub { position:absolute; left:120px; right:120px; top:420px; padding:30px 40px; background:var(--card); border:4px solid rgba(23,38,43,.13); "
    "border-radius:40px 40px 40px 8px; font-size:60px; font-weight:700; line-height:1.15; text-align:center; box-shadow:0 12px 26px -16px rgba(23,38,43,.35); }"
    ".ops2 { position:absolute; left:80px; right:80px; top:1000px; display:flex; flex-direction:column; gap:28px; }"
    ".ops2 .op { height:170px; border-radius:36px; background:var(--card); border:4px solid rgba(23,38,43,.13); display:flex; align-items:center; justify-content:center; }"
    ".ops2 .op b { font-family:var(--ar); font-size:84px; line-height:1.4; color:var(--ink); }")

def m1():
    """Mashallah in the standard (owner, 17 Oct 2026; replaces r4-insha's mashallah half). Callum explains, Rafiq says the Arabic:
    ما شاءَ اللهُ word by word ("what Allah has willed"); شاءَ is past tense, so it's for good that's already there, and the future takes
    إِنْ شاءَ اللهُ; the root ش ي ء (مَشِيئَة, شَيْء); al-Kahf 18:39 in al-Husary's recitation (reciter 12, as in the app; word timings
    from api.quran.com, Saheeh International's translation); a quick test, 3-2-1. Hook tested: tools/typesafe-exp/mashallah_hook.py.
    Voices: brag-quiz/voice/mashallah-lines.json."""
    V, Q = "brag-quiz/voice/mashallah/", "brag-quiz/voice/mashallah-quran/kahf-18-39.mp3"
    c = SO.vcomp("m1-mashallah", "ARABIC · WHAT YOU REALLY SAY"); c.bed = True; body = []
    t = hook_in(c, body, ("MOST people don’t know mashallah is in the PAST tense!".split(), {0: "loud", 4: "red", 8: "circle"}, V + "hb.mp3"))
    c.css += MASH_CSS + "#hw8 { margin-right:22px; }"            # the circled PAST touched "tense"
    # 1. word by word: the chips come in as Callum names them; the matching word in the big line turns red
    body.append('<div class="sec" id="a"><div class="q2">Word by word:</div>'
                '<div class="big" style="top:330px;font-size:170px" lang="ar" dir="rtl"><span class="w" id="aw0">ما</span> <span class="w" id="aw1">شاءَ</span> <span class="w" id="aw2">اللهُ</span></div>'
                '<div class="chips" style="top:720px">' + "".join(f'<div class="chip" id="ac{i}"><div class="ar">{a}</div><b>{en}</b></div>'
                for i, (a, en) in enumerate([("ما", "what"), ("شاءَ", "has willed"), ("اللهُ", "Allah")])) + '</div>'
                '<div class="say" id="as" style="top:1110px">= what Allah has willed</div></div>')
    c.t(f'tl.fromTo("#a", {{x:700, opacity:0, filter:"blur(18px)"}}, {{x:0, opacity:1, filter:"blur(0px)", duration:0.35, ease:"power3.out"}}, {t - 0.2:.2f});')
    d = say_up(c, "ما شاءَ اللهُ", t + 0.1); t += d + 0.3
    W = words_at(V + "c1.mp3"); d = clip(c, V + "c1.mp3", t)
    for i, key in enumerate(("what", "willed", "allah")):
        at = t + next((s for w, s in W if key in w.lower()), d * (i + 1) / 4)
        c.inn(f"#ac{i}", at - 0.05, 30); c.sfx("tap", at)
        c.t(f'tl.to("#aw{i}", {{color:"{T.RED}", duration:0.2}}, {at:.2f});')
        c.t(f'tl.fromTo("#aw{i}", {{scale:1}}, {{scale:1.12, duration:0.15, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {at:.2f});')
    t += d; c.inn("#as", t - 0.1); c.sfx("correct", t)                 # the meaning lands as the last word is said
    c.t(f'tl.fromTo("#as", {{scale:1}}, {{scale:1.05, duration:0.16, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {t + 0.3:.2f});')
    t += 1.3; c.t(f'tl.to("#a", {{x:-700, opacity:0, filter:"blur(18px)", duration:0.3, ease:"power3.in"}}, {t:.2f});')
    clip(c, "brag-quiz/sfx/ref/swoosh.wav", t - 0.05, 0.5); t += 0.35
    # 2. past tense: the stamp slams on "past"; mashallah is for good that's already there, the future is in shā' Allāh
    body.append('<div class="sec" id="b"><div class="big" style="top:260px;font-size:200px" lang="ar">شاءَ</div><div class="stamp" id="bs">PAST TENSE</div>'
                '<div class="card2 ok" id="b1" style="top:820px"><div class="ar">ما شاءَ اللهُ</div><div class="t">something good<small>that’s already there ✓</small></div></div>'
                '<div class="card2 fut" id="b2" style="top:1090px"><div class="ar">إِنْ شاءَ اللهُ</div><div class="t" id="b2t">the future<small>if Allah wills</small></div></div></div>')
    c.t(f'tl.fromTo("#b", {{x:700, opacity:0, filter:"blur(18px)"}}, {{x:0, opacity:1, filter:"blur(0px)", duration:0.35, ease:"power3.out"}}, {t - 0.2:.2f});')
    W = words_at(V + "c3b.mp3"); d = clip(c, V + "c3b.mp3", t)
    hit = t + next((s for w, s in W if "past" in w.lower()), 1.2) + 0.1
    c.t(f'tl.fromTo("#bs", {{opacity:0, scale:2.6}}, {{opacity:1, scale:1, duration:0.18, ease:"power4.in"}}, {hit - 0.18:.2f});')
    c.t(f'tl.to("#b", {{keyframes:[{{x:-24, y:16, duration:0.04}}, {{x:20, y:-12, duration:0.04}}, {{x:-10, y:6, duration:0.05}}, {{x:0, y:0, duration:0.06}}]}}, {hit:.2f});')
    clip(c, "brag-quiz/sfx/crash.wav", hit - 0.02, 0.6)
    ok = t + next((s for w, s in W if "mashallah" in w.lower() or "masha" in w.lower()), d * 0.55)
    c.inn("#b1", ok, 30); c.sfx("tap", ok)
    t += d + 0.1; d = clip(c, V + "c4.mp3", t); c.inn("#b2", t + 0.2, 30); c.sfx("tap", t + 0.2)
    t += d + 0.1; d = say_up(c, "إِنْ شاءَ اللهُ", t); t += d + 0.15; d = clip(c, V + "c5.mp3", t)
    c.t(f'tl.fromTo("#b2t small", {{color:"{T.INK}"}}, {{color:"#a8842c", duration:0.3}}, {t:.2f});')
    t += d + 0.3; c.t(f'tl.to("#b", {{x:-700, opacity:0, filter:"blur(18px)", duration:0.3, ease:"power3.in"}}, {t:.2f});')
    clip(c, "brag-quiz/sfx/ref/swoosh.wav", t - 0.05, 0.5); t += 0.35
    # 3. the root: ش ي ء, then its will and "a thing"
    body.append('<div class="sec" id="r"><div class="q2">Same three letters:</div><div class="rootq" lang="ar">ش ي ء</div>'
                '<div class="card2" id="r1" style="top:780px"><div class="ar">' + word([("مَ", ""), ("شِ", "r"), ("ي", "r"), ("ئَ", "r"), ("ة", "")]) + '</div><div class="t">will<small>Allah’s will</small></div></div>'
                '<div class="card2" id="r2" style="top:1050px"><div class="ar">' + word([("شَ", "r"), ("يْ", "r"), ("ء", "r")]) + '</div><div class="t">a thing<small>the same root</small></div></div></div>')
    c.t(f'tl.fromTo("#r", {{x:700, opacity:0, filter:"blur(18px)"}}, {{x:0, opacity:1, filter:"blur(0px)", duration:0.35, ease:"power3.out"}}, {t - 0.2:.2f});')
    d = clip(c, V + "c6.mp3", t); c.inn("#r1", t + d - 0.3, 30); c.sfx("tap", t + d - 0.3)
    t += d; d = say_any(c, "مَشِيئَة", t, {"مَشِيئَة": "brag-quiz/voice/recreate/mashia.mp3"}); t += d + 0.1
    d = clip(c, V + "c7.mp3", t); c.inn("#r2", t + 0.3, 30); c.sfx("tap", t + 0.3)
    t += d + 0.05; d = say_up(c, "شَيْء", t); t += d + 0.3
    c.t(f'tl.to("#r", {{x:-700, opacity:0, filter:"blur(18px)", duration:0.3, ease:"power3.in"}}, {t:.2f});')
    clip(c, "brag-quiz/sfx/ref/swoosh.wav", t - 0.05, 0.5); t += 0.35
    # 4. al-Kahf 18:39: each word lights up gold as al-Husary recites it (api.quran.com segments, from 7.33 s into the verse)
    QW = [("ما", 0.04), ("شاءَ", 0.65), ("اللَّهُ", 2.80), ("لا", 4.17), ("قُوَّةَ", 4.72), ("إِلّا", 5.98), ("بِاللَّهِ", 7.32)]
    body.append('<div class="sec" id="k"><div class="q2">Straight from the Qur’an</div><div class="qref">AL-KAHF · 18:39</div><div class="qr">'
                + " ".join(f'<span class="w" id="kw{i}">{a}</span>' + ("<br>" if i == 2 else "") for i, (a, _) in enumerate(QW)) +
                '</div><div class="qen" id="ke">“What Allah willed; there is no power except in Allah.”</div></div>')
    c.t(f'tl.fromTo("#k", {{x:700, opacity:0, filter:"blur(18px)"}}, {{x:0, opacity:1, filter:"blur(0px)", duration:0.35, ease:"power3.out"}}, {t - 0.2:.2f});')
    d = clip(c, V + "c8b.mp3", t); t += d + 0.15
    dq = say_up(c, "", t, src=Q)
    for i, (_, s) in enumerate(QW):
        c.t(f'tl.to("#kw{i}", {{color:"#a8842c", duration:0.25}}, {t + s:.2f});')
        c.t(f'tl.fromTo("#kw{i}", {{scale:1}}, {{scale:1.1, duration:0.18, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {t + s:.2f});')
    c.inn("#ke", t + 4.2); t += dq + 0.3
    c.t(f'tl.to("#k", {{x:-700, opacity:0, filter:"blur(18px)", duration:0.3, ease:"power3.in"}}, {t:.2f});')
    clip(c, "brag-quiz/sfx/ref/swoosh.wav", t - 0.05, 0.5); t += 0.35
    # 5. the quick test: 3-2-1, in shā' Allāh turns green and Rafiq says it, then the closing ask is heard in full
    body.append('<div class="sec" id="z"><div class="q2">Quick test!</div><div class="bub" id="zb">“See you at Jumuʿah tomorrow!”</div>'
                + cnt("zc", 760) + '<div class="ops2"><div class="op" id="zo0"><b>ما شاءَ اللهُ</b></div><div class="op" id="zo1"><b>إِنْ شاءَ اللهُ</b></div></div></div>')
    c.t(f'tl.fromTo("#z", {{x:700, opacity:0, filter:"blur(18px)"}}, {{x:0, opacity:1, filter:"blur(0px)", duration:0.35, ease:"power3.out"}}, {t - 0.2:.2f});')
    W = words_at(V + "c9.mp3"); d = clip(c, V + "c9.mp3", t)
    c.inn("#zb", t + next((s for w, s in W if "see" in w.lower()), 1.0) - 0.1, 30)
    o = t + next((s for i, (w, s) in enumerate(W) if "mashallah" in w.lower() or "masha" in w.lower()), d - 1.6)
    c.inn("#zo0", o - 0.1, 30); c.inn("#zo1", o + 0.5, 30)
    done = count_down(c, "zc", t + d + 0.35)
    reveal(c, "#zo1", ["#zo0"], done); d = say_up(c, "إِنْ شاءَ اللهُ", done + 0.3)
    t = done + 0.3 + d + 0.2; end = clip(c, V + "c10b.mp3", t)
    E = t + 2.2; c.out_("#z", E - 0.4)
    body.append(c.end(E, "Comment below 👇 and send this to someone who says mashallah every day"))
    c.write("\n".join("      " + b for b in body), round(max(E + 2.9, t + end + 0.8), 2))

BUBBLES = [  # moments people say it, round the hook line: (left, top, text, side "a" = tagged on mashallah, "b" = on Allahumma barik)
    (70, 300, "new baby 👶", "a"), (620, 330, "new car 🚗", "a"), (330, 480, "wedding photos 💍", "a"),
    (60, 1420, "exam results 🎓", "b"), (620, 1470, "new house 🏡", "b"), (300, 1650, "her cooking 🍲", "b")]

def m2():
    """Mashallah vs Allahumma barik (owner, 17 Oct 2026; replaces m1, whose "past tense" angle was wrong: إِنْ شاءَ اللهُ has the same
    past form). ما شاءَ اللهُ word by word; al-Kahf 18:39 (a man told he should have said it over his own garden), al-Husary reciting;
    for someone else's blessing the Prophet ﷺ taught praying for blessing (Ibn Mājah 3509, ʿĀmir ibn Rabīʿah and Sahl ibn Ḥunayf, sahih);
    the root ب ر ك (بَرَكَة, عِيد مُبارَك); a "new baby" test, answer: both. Hook: tools/typesafe-exp/barik_hook.py; the hook's background
    is the moments people say it, tagged "mashallah?" / "Allahumma barik?" as each is said. Voices: brag-quiz/voice/barik-lines.json."""
    V, M, Q = "brag-quiz/voice/barik/", "brag-quiz/voice/mashallah/", "brag-quiz/voice/mashallah-quran/kahf-18-39.mp3"
    c = SO.vcomp("m2-barik", "ARABIC · WHAT YOU REALLY SAY"); c.bed = True; body = []
    words = "Do YOU know the difference between mashallah and Allahumma barik?".split()   # the stress on YOU (owner)
    bub = "".join(f'<div class="hb2" id="hb{k}" style="left:{x}px;top:{y}px">{t}<i>{"mashallah?" if g == "a" else "Allahumma barik?"}</i></div>'
                  for k, (x, y, t, g) in enumerate(BUBBLES))
    def anim(c, at, d):
        for k, (x, y, t, g) in enumerate(BUBBLES):
            c.t(f'tl.fromTo("#hb{k}", {{y:0, rotation:{-3 if k % 2 else 3}}}, {{y:{-26 if k % 2 else 22}, rotation:{2 if k % 2 else -2}, duration:{d + 0.3:.2f}, ease:"none"}}, 0);')
            tg = at(6 if g == "a" else 8) + 0.1 * (k % 3)
            c.t(f'tl.fromTo("#hb{k} i", {{opacity:0, scale:1.6}}, {{opacity:1, scale:1, duration:0.22, ease:"back.out(2)"}}, {tg:.2f});')
            if k % 3 == 0: c.sfx("tap", tg)
    t = hook_in(c, body, (words, {1: "loud", 6: "red", 9: "circle"}, V + "hy1.mp3"), bg=(bub, anim))
    c.css += MASH_CSS + (".hb2 { position:absolute; padding:22px 30px; background:var(--card); border:4px solid rgba(23,38,43,.12); border-radius:34px 34px 34px 8px; "
                         "font-family:\"Fredoka\", var(--la); font-weight:600; font-size:44px; color:var(--ink); white-space:nowrap; box-shadow:0 14px 30px -18px rgba(23,38,43,.4); }"
                         ".hb2 i { position:absolute; right:-18px; top:-34px; font-style:normal; font-size:30px; font-weight:700; padding:6px 16px; border-radius:20px; "
                         "background:#E9B949; color:var(--ink); white-space:nowrap; opacity:0; } .ref { position:absolute; left:0; right:0; text-align:center; "
                         "font-size:34px; font-weight:700; letter-spacing:.06em; color:var(--ink-soft); }")
    def whip_in(sec, at): c.t(f'tl.fromTo("#{sec}", {{x:700, opacity:0, filter:"blur(18px)"}}, {{x:0, opacity:1, filter:"blur(0px)", duration:0.35, ease:"power3.out"}}, {at - 0.2:.2f});')
    def whip_out(sec, at):
        c.t(f'tl.to("#{sec}", {{x:-700, opacity:0, filter:"blur(18px)", duration:0.3, ease:"power3.in"}}, {at:.2f});')
        clip(c, "brag-quiz/sfx/ref/swoosh.wav", at - 0.05, 0.5); return at + 0.35
    def chips(sec, pairs, top): return (f'<div class="chips" style="top:{top}px">' + "".join(f'<div class="chip" id="{sec}c{i}"><div class="ar">{a}</div><b>{en}</b></div>'
                                        for i, (a, en) in enumerate(pairs)) + '</div>')
    def light(sec, mp3, keys, t):         # each chip comes in, and its word in the big line turns red, as Callum names it
        W = words_at(mp3); d = clip(c, mp3, t)
        for i, key in enumerate(keys):
            at = t + next((s for w, s in W if key in w.lower()), d * (i + 1) / (len(keys) + 1))
            c.inn(f"#{sec}c{i}", at - 0.05, 30); c.sfx("tap", at)
            c.t(f'tl.to("#{sec}w{i}", {{color:"{T.RED}", duration:0.2}}, {at:.2f});')
            c.t(f'tl.fromTo("#{sec}w{i}", {{scale:1}}, {{scale:1.12, duration:0.15, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {at:.2f});')
        return d
    # 1. mashallah word by word
    body.append('<div class="sec" id="a"><div class="q2">Mashallah, word by word:</div>'
                '<div class="big" style="top:330px;font-size:170px" lang="ar" dir="rtl"><span class="w" id="aw0">ما</span> <span class="w" id="aw1">شاءَ</span> <span class="w" id="aw2">اللهُ</span></div>'
                + chips("a", [("ما", "what"), ("شاءَ", "has willed"), ("اللهُ", "Allah")], 720) + '<div class="say" id="as" style="top:1110px">= what Allah has willed</div></div>')
    whip_in("a", t); d = say_up(c, "ما شاءَ اللهُ", t + 0.1); t += d + 0.3
    t += light("a", M + "c1.mp3", ("what", "willed", "allah"), t); c.inn("#as", t - 0.1); c.sfx("correct", t)
    t = whip_out("a", t + 1.2)
    # 2. al-Kahf 18:39, said over his own garden: each word lights up as al-Husary recites it (api.quran.com segments)
    QW = [("ما", 0.04), ("شاءَ", 0.65), ("اللَّهُ", 2.80), ("لا", 4.17), ("قُوَّةَ", 4.72), ("إِلّا", 5.98), ("بِاللَّهِ", 7.32)]
    body.append('<div class="sec" id="k"><div class="q2">In the Qur’an</div><div class="qref">AL-KAHF · 18:39</div><div class="qr">'
                + " ".join(f'<span class="w" id="kw{i}">{a}</span>' + ("<br>" if i == 2 else "") for i, (a, _) in enumerate(QW)) +
                '</div><div class="qen" id="ke">“What Allah willed; there is no power except in Allah.”</div>'
                '<div class="ref" id="kr" style="top:1130px">said over <b>his own</b> garden 🌳</div></div>')
    whip_in("k", t); d = clip(c, V + "d2.mp3", t); c.inn("#kr", t + d - 1.2); t += d + 0.15
    dq = say_up(c, "", t, src=Q)
    for i, (_, s_) in enumerate(QW):
        c.t(f'tl.to("#kw{i}", {{color:"#a8842c", duration:0.25}}, {t + s_:.2f});')
        c.t(f'tl.fromTo("#kw{i}", {{scale:1}}, {{scale:1.1, duration:0.18, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {t + s_:.2f});')
    c.inn("#ke", t + 4.2); t = whip_out("k", t + dq + 0.3)
    # 3. someone else's blessing: Allahumma barik, word by word, with the hadith
    body.append('<div class="sec" id="b"><div class="q2">Someone <b style="color:var(--rubric)">else’s</b> blessing?</div>'
                '<div class="big" style="top:330px;font-size:170px" lang="ar" dir="rtl"><span class="w" id="bw0">اللَّهُمَّ</span> <span class="w" id="bw1">بارِكْ</span></div>'
                + chips("b", [("اللَّهُمَّ", "O Allah"), ("بارِكْ", "bless")], 720) +
                '<div class="ref" id="br" style="top:1130px">“Why didn’t you pray for blessing?”<br><span style="font-weight:500;letter-spacing:0">the Prophet ﷺ · Ibn Mājah 3509</span></div></div>')
    whip_in("b", t); d = clip(c, V + "d4b.mp3", t); c.inn("#br", t + d * 0.4); t += d + 0.1
    d = say_up(c, "", t, src=V + "allahumma-barik.mp3"); t += d + 0.2
    t += light("b", V + "d5.mp3", ("allah", "bless"), t); t = whip_out("b", t + 1.0)
    # 4. the root ب ر ك
    body.append('<div class="sec" id="r"><div class="q2">Same three letters:</div><div class="rootq" lang="ar">ب ر ك</div>'
                '<div class="card2" id="r1" style="top:780px"><div class="ar">' + word([("بَ", "r"), ("رَ", "r"), ("كَ", "r"), ("ة", "")]) + '</div><div class="t">barakah<small>blessing</small></div></div>'
                '<div class="card2" id="r2" style="top:1050px"><div class="ar">' + word([("عِيد مُ", ""), ("ب", "r"), ("ا", ""), ("رَ", "r"), ("ك", "r")]) + '</div><div class="t">Eid Mubarak<small>a blessed Eid</small></div></div></div>')
    whip_in("r", t); d = clip(c, V + "d7a.mp3", t); c.inn("#r1", t + d - 0.2, 30); c.sfx("tap", t + d - 0.2); t += d
    d = say_up(c, "", t, src=V + "barakah.mp3"); t += d + 0.1
    d = clip(c, V + "d7b.mp3", t); c.inn("#r2", t + 0.2, 30); c.sfx("tap", t + 0.2); t += d
    d = say_up(c, "مُبارَكٌ", t); t = whip_out("r", t + d + 0.3)
    # 5. the test: 3-2-1, "both" turns green and Rafiq says both, then the closing ask is heard in full
    body.append('<div class="sec" id="z"><div class="q2">Quick test!</div><div class="bub" id="zb" style="top:380px">“Look, my new baby!” 👶</div>'
                + cnt("zc", 640) + '<div class="ops2" style="top:860px">' + "".join(f'<div class="op" id="zo{i}"><b>{o}</b></div>' for i, o in
                enumerate(["ما شاءَ اللهُ", "اللَّهُمَّ بارِكْ", '<span style="font-family:var(--la)">Both</span>'])) + '</div></div>')
    whip_in("z", t); d = clip(c, V + "d8.mp3", t); c.inn("#zb", t + 0.9, 30)
    for i in range(3): c.inn(f"#zo{i}", t + d - 1.0 + i * 0.15, 30)
    done = count_down(c, "zc", t + d + 0.35)
    reveal(c, "#zo2", ["#zo0", "#zo1"], done); d = say_up(c, "", done + 0.3, src=V + "both.mp3")
    t = done + 0.3 + d + 0.2; end = clip(c, V + "d9b.mp3", t)
    E = t + 2.4; c.out_("#z", E - 0.4)
    body.append(c.end(E, "Comment below 👇 and send this to someone who says mashallah every day"))
    c.write("\n".join("      " + b for b in body), round(max(E + 2.9, t + end + 0.8), 2))

def whip_in(c, sec, at): c.t(f'tl.fromTo("#{sec}", {{x:700, opacity:0, filter:"blur(18px)"}}, {{x:0, opacity:1, filter:"blur(0px)", duration:0.35, ease:"power3.out"}}, {at - 0.2:.2f});')
def whip_out(c, sec, at):
    c.t(f'tl.to("#{sec}", {{x:-700, opacity:0, filter:"blur(18px)", duration:0.3, ease:"power3.in"}}, {at:.2f});')
    clip(c, "brag-quiz/sfx/ref/swoosh.wav", at - 0.05, 0.5); return at + 0.35
def key_at(mp3, key, fallback):
    """When Callum says the first word containing key, in seconds from the start of his line."""
    return next((s for w, s in words_at(mp3) if key in w.lower()), fallback)
def serif(c):
    """A quoted source (a hadith, a tafsir) in a card, in Instrument Serif; the reference line darker gold, for contrast."""
    shutil.copy(os.path.join(T.ROOT, "brag-quiz/fonts/instrument-serif-latin-400-normal.woff2"), os.path.join(c.a, "fonts"))
    c.css += ('@font-face { font-family:"Instrument Serif"; src:url("assets/fonts/instrument-serif-latin-400-normal.woff2") format("woff2"); }'
              ".quote { position:absolute; left:70px; right:70px; padding:26px 40px 30px; text-align:center; background:var(--card); border:4px solid rgba(23,38,43,.13); "
              "border-radius:36px; box-shadow:0 14px 30px -16px rgba(23,38,43,.4); } .quote q { display:block; font-family:\"Instrument Serif\", serif; font-style:italic; "
              "font-size:66px; line-height:1.12; color:var(--ink); quotes:\"\\201C\" \"\\201D\"; } .quote small { display:block; margin-top:14px; font-size:32px; "
              "font-weight:700; letter-spacing:.04em; color:var(--ink-soft); } .quote .pbuh { font-family:var(--ar); font-size:46px; vertical-align:-6px; }")

GROW_CSS = (
    ".soil { position:absolute; left:180px; top:1600px; width:720px; height:92px; border-radius:50%; background:#e3d6b8; }"
    ".seed { position:absolute; left:50%; top:1560px; transform:translateX(-50%); padding:4px 34px 10px; border-radius:40px; background:#E9B949; "
    "font-family:var(--ar); font-weight:700; font-size:66px; line-height:1.35; color:var(--rubric); white-space:nowrap; box-shadow:0 14px 30px -14px rgba(23,38,43,.45); }"
    ".seed small { font-family:var(--la); font-size:38px; color:var(--ink); margin-right:14px; }"
    ".tree { position:absolute; inset:0; overflow:visible; } .tree path { fill:none; stroke:var(--verdigris); stroke-linecap:round; stroke-dasharray:1; stroke-dashoffset:1; }"
    ".leaf { position:absolute; width:58px; height:30px; border-radius:0 100%; background:#3f8f7d; transform-origin:0 50%; }"
    ".leaf.b { background:#2e7263; } .bloom { position:absolute; padding:14px 18px 22px; text-align:center; background:var(--card); border:6px solid var(--verdigris); "
    "border-radius:56px; box-shadow:0 18px 34px -18px rgba(23,38,43,.5); } .bloom .ar { font-family:var(--ar); font-weight:700; font-size:84px; line-height:1.45; color:var(--rubric); }"
    ".bloom b { display:block; font-size:42px; line-height:1.1; color:var(--ink); } .bloom.crown { border-color:#E9B949; border-width:10px; }"
    ".bloom.crown .ar { font-size:110px; } .bloom .lab { position:relative; } .bloom.crown .lab { height:64px; } .bloom.crown .lab b { position:absolute; left:0; right:0; top:0; }"
    ".bloom .qm { color:var(--rubric); font-size:56px; } .bloom.crown .lab b { font-size:54px; }"
    ".pet { position:absolute; left:50%; top:50%; width:26px; height:26px; margin:-13px; border-radius:50%; background:#E9B949; opacity:0; }"
    ".pet:nth-child(odd) { background:var(--rubric); width:18px; height:18px; margin:-9px; }"
    "#wc { position:absolute; left:830px; top:590px; width:190px; height:190px; } #wc svg { position:absolute; inset:0; transform:rotate(-90deg); }"
    "#wc circle { fill:none; stroke-width:16; } #wc .bg { stroke:rgba(23,38,43,.1); } #wc .fg { stroke:var(--rubric); stroke-linecap:round; stroke-dasharray:503; stroke-dashoffset:503; }"
    "#wc span { position:absolute; inset:0; display:grid; place-items:center; font-family:\"Fredoka\", var(--la); font-weight:700; font-size:96px; color:var(--rubric); opacity:0; }"
    "#wc small { position:absolute; left:-70px; right:-70px; top:196px; text-align:center; font-weight:700; font-size:23px; letter-spacing:.12em; color:var(--ink-soft); white-space:nowrap; }"
    ".opts { position:absolute; left:50px; right:50px; display:flex; gap:22px; } .opts .op2 { flex:1; height:128px; border-radius:64px; background:var(--card); "
    "border:4px solid rgba(23,38,43,.13); display:flex; align-items:center; justify-content:center; } .opts .op2 b { font-size:50px; font-weight:700; color:var(--ink); }"
    "#tflash { position:absolute; inset:0; background:#fff8e6; opacity:0; pointer-events:none; }"
    ".hb3 { position:absolute; padding:20px 30px; background:var(--card); border:4px solid rgba(23,38,43,.12); border-radius:34px; font-family:\"Fredoka\", var(--la); "
    "font-weight:600; font-size:46px; color:var(--ink); white-space:nowrap; box-shadow:0 14px 30px -18px rgba(23,38,43,.4); } .vine { position:absolute; inset:0; overflow:visible; }"
    ".vine path { fill:none; stroke:#3f8f7d; stroke-width:9; stroke-linecap:round; stroke-dasharray:1; stroke-dashoffset:1; opacity:.8; }")

FAMILY = [(70, 290, "mum 🤍", 250), (650, 320, "dad", 150), (330, 470, "grandma", 250),     # the hook's "family", round the hook line:
          (70, 1400, "my sister", 280), (660, 1430, "cousins", 250), (330, 1610, "my brother", 320)]   # (left, top, text, width)
TRUNK = "M540,1615 C548,1470 512,1340 532,1190 S562,930 538,770 S526,610 540,540"
GROW = [  # the blooms, bottom to top: (branch path, left, top, width, Arabic, meaning, Rafiq's recording or None for the app's, Callum's line)
    ("M534,1330 C480,1300 450,1250 440,1205", 60, 1110, 380, "رَحْمَة", "mercy", None, "b1"),
    ("M545,1070 C580,1040 596,990 604,955", 600, 830, 420, "رَحِمَهُ اللهُ", "may Allah have mercy on him", "rahimahu", "b3")]
LEAVES = [(560, 1500, -40), (476, 1440, 210), (560, 1300, -30), (470, 1120, 200), (566, 1010, -35), (480, 900, 205), (562, 690, -30),
          (484, 620, 210), (470, 1265, 160), (590, 1020, -60), (466, 790, 150)]   # (x, y, rotation) along the trunk

def word_tree(c, body, t, cf):
    """The word tree after its hook (n2-rahma, n3-ilm): the verse in al-Husary's recitation, its root letters turn red and drop in as
    a seed, a trunk grows and a word blooms on each branch (cf["grow"]) with a counter clicking up, then the tree pulls back for
    "your turn" on the crown (3-2-1, its meaning slams on), the source in a quote card, and the closing ask on the end card."""
    V = cf["V"]
    c.css += MASH_CSS + GROW_CSS + ".qref { color:#9a7826; }"
    # 1. al-Fātiḥah 1:3: each word lights up as al-Husary recites it (from the audio: the ḥ of each word, minus its r-ra), then the root
    body.append(f'<div class="sec" id="a"><div class="q2">{cf.get("intro", "You say it in al-Fātiḥah:")}</div><div class="qref" style="top:350px">{cf["ref"]}</div>'
                '<div class="big" style="top:470px;font-size:140px" dir="rtl">' + " ".join(f'<span class="w" id="aw{i}">{word(w)}</span>' for i, w in enumerate(cf["verse"])) + '</div></div>')
    whip_in(c, "a", t); d = clip(c, cf["c1"], t + 0.1); t += 0.1 + d + 0.1
    dq = say_up(c, "", t, src=cf["recite"])
    for i, s in enumerate(cf["times"]):
        c.t(f'tl.fromTo("#aw{i}", {{scale:1}}, {{scale:1.1, duration:0.18, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {t + s:.2f});')
    t += dq + 0.1; c.t(f'tl.to("#a .pr", {{color:"{T.RED}", duration:0.3, stagger:0.08}}, {t:.2f});'); c.sfx("tap", t)
    t = whip_out(c, "a", t + 0.8)
    # 2. the tree: the three letters drop into the soil as a seed, the trunk grows, a word blooms on each branch as it's said
    pets = "".join('<i class="pet"></i>' for _ in range(8))
    blooms = "".join(f'<div class="bloom" id="bl{k}" style="left:{x}px;top:{y}px;width:{w}px"><div class="ar">{ar}</div><div class="lab"><b id="bl{k}e">{en}</b></div>{pets}</div>'
                     for k, (_, x, y, w, ar, en, _, _) in enumerate(cf["grow"]))
    n = len(cf["grow"])                              # the crown is bloom n
    crown = (f'<div class="bloom crown" id="bl{n}" style="left:260px;top:290px;width:560px"><div class="ar">{cf["crown"][0]}</div><div class="lab"><b class="qm" id="bl{n}q">?</b>'
             f'<b id="bl{n}e" style="color:var(--rubric)">{cf["crown"][1]}</b></div>{pets}</div>')
    paths = (f'<path id="trunk" d="{TRUNK}" pathLength="1" style="stroke-width:30"/>' + "".join(f'<path id="br{k}" d="{p}" pathLength="1" style="stroke-width:18"/>'
             for k, (p, *_ ) in enumerate(cf["grow"])) + '<path id="br3" d="M540,560 C540,548 540,536 540,522" pathLength="1" style="stroke-width:22"/>')
    lv = "".join(f'<i class="leaf{" b" if k % 2 else ""}" id="lv{k}" style="left:{x}px;top:{y}px;transform:rotate({r}deg)"></i>' for k, (x, y, r) in enumerate(LEAVES))
    ring = ('<div id="wc"><svg viewBox="0 0 190 190"><circle class="bg" cx="95" cy="95" r="80"/><circle class="fg" cx="95" cy="95" r="80"/></svg>'
            + "".join(f'<span id="wc{k}">{k}</span>' for k in range(n + 2)) + '<small>WORDS, ONE ROOT</small></div>')
    opts = '<div class="opts" id="qo" style="top:1450px">' + "".join(f'<div class="op2" id="qo{i}"><b>{o}</b></div>' for i, o in enumerate(cf["opts"])) + '</div>'
    body.append(f'<div class="sec" id="tr"><div id="tv"><div class="soil"></div><svg class="tree" viewBox="0 0 1080 1920">{paths}</svg>{lv}'
                f'<div class="seed" id="seed"><small>{cf["seed"][0]}</small>{cf["seed"][1]}</div>{blooms}{crown}{ring}</div>'
                f'{cnt("qc", 1270)}{opts}<div class="quote" id="hq" style="top:1290px">{cf["quote"]}</div><div class="say" id="hs" style="top:1640px">{cf["say"]}</div><div id="tflash"></div></div>')
    whip_in(c, "tr", t)
    c.t(f'tl.fromTo("#seed", {{y:-760, scale:0.3, opacity:0}}, {{scale:2.1, opacity:1, duration:0.45, ease:"back.out(2)"}}, {t:.2f});'); c.sfx("tap", t + 0.1)
    c.t(f'tl.fromTo(".soil", {{scaleX:0, opacity:0}}, {{scaleX:1, opacity:1, duration:0.4, ease:"power3.out"}}, {t + 0.3:.2f});')
    d = clip(c, cf["c2"], t + 0.1); m = t + 0.1 + key_at(cf["c2"], cf["c2key"], 2.2)
    c.t(f'tl.fromTo("#seed", {{scale:2.1}}, {{scale:2.35, duration:0.14, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {m:.2f});')
    c.t(f'tl.to("#seed", {{y:0, scale:1, duration:0.45, ease:"power2.in"}}, {m + 0.45:.2f});'); c.sfx("tap", m + 0.9)   # it drops into the soil
    g = m + 1.0; t += 0.1 + d
    c.t(f'tl.to("#trunk", {{strokeDashoffset:0, duration:1.3, ease:"power2.inOut"}}, {g - 0.2:.2f});'); clip(c, "brag-quiz/sfx/ref/swoosh.wav", g - 0.2, 0.35)
    for k, (x, y, r) in enumerate(LEAVES):           # the leaves open as the trunk passes them
        c.t(f'tl.fromTo("#lv{k}", {{scale:0}}, {{scale:1, duration:0.35, ease:"back.out(2.5)"}}, {g - 0.2 + 1.3 * (1615 - y) / 1075:.2f});')
    c.t(f'tl.fromTo("#wc", {{opacity:0, scale:0.6}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, {g:.2f});'); c.t(f'tl.set("#wc0", {{opacity:1}}, {g:.2f});')
    t = max(t, g + 1.1)
    def pop(k, at):                                  # a bloom opens: petals burst, a tap, and the counter clicks up
        c.t(f'tl.fromTo("#bl{k}", {{opacity:0, scale:0.15, rotation:{-14 if k % 2 else 14}}}, {{opacity:1, scale:1, rotation:0, duration:0.5, ease:"back.out(2.2)"}}, {at:.2f});')
        c.t(f'tl.fromTo("#bl{k} .pet", {{opacity:1, x:0, y:0}}, {{opacity:0, x:(i) => Math.cos(i * Math.PI / 4) * 230, y:(i) => Math.sin(i * Math.PI / 4) * 150, '
            f'duration:0.6, ease:"expo.out", immediateRender:false}}, {at + 0.05:.2f});')
        c.t(f'tl.to("#wc{k}", {{opacity:0, duration:0.1}}, {at:.2f});')
        c.t(f'tl.fromTo("#wc{k + 1}", {{opacity:0, scale:1.6}}, {{opacity:1, scale:1, duration:0.25, ease:"back.out(2)"}}, {at:.2f});')
        c.t(f'tl.to("#wc .fg", {{strokeDashoffset:{503 * (1 - (k + 1) / (n + 1)):.0f}, duration:0.3, ease:"power2.out"}}, {at:.2f});')
        clip(c, "brag-quiz/sfx/ref/click.wav", at, 0.8); c.sfx("tap", at + 0.05)
    for k, (_, x, y, w, ar, en, rec, line) in enumerate(cf["grow"]):
        c.t(f'tl.to("#br{k}", {{strokeDashoffset:0, duration:0.4, ease:"power2.out"}}, {t:.2f});'); clip(c, "brag-quiz/sfx/ref/short-swoosh.wav", t, 0.25)
        pop(k, t + 0.3)
        d = say_up(c, ar, t + 0.4) if rec is None else say_up(c, "", t + 0.4, src=V + rec + ".mp3"); t += 0.4 + d + 0.1
        c.t(f'tl.fromTo("#bl{k}e", {{opacity:0, y:16}}, {{opacity:1, y:0, duration:0.3, ease:"power3.out"}}, {t:.2f});')
        d = clip(c, V + line + ".mp3", t); t += d
    # 3. your turn: the tree pulls back, the crown buds, 3-2-1, its meaning slams on, then the source
    c.t(f'tl.to("#tv", {{scale:0.7, y:-20, transformOrigin:"540px 240px", duration:0.7, ease:"power3.inOut"}}, {t:.2f});')
    d = clip(c, cf["t1"], t + 0.1)
    c.t(f'tl.to("#br3", {{strokeDashoffset:0, duration:0.3}}, {t + 0.5:.2f});'); pop(n, t + 0.7)
    c.t(f'tl.set("#bl{n}e", {{opacity:0}}, 0);'); t += 0.1 + d + 0.05
    d = say_up(c, "", t, src=cf["crown_say"])
    for i in range(3): c.inn(f"#qo{i}", t + 0.1 + i * 0.12, 30)
    done = count_down(c, "qc", t + d + 0.3)
    reveal(c, f"#qo{cf['right']}", [f"#qo{i}" for i in range(3) if i != cf["right"]], done)
    d = clip(c, cf["slam"], done); hit = done + key_at(cf["slam"], cf["slam_key"], 0.14) + 0.05
    c.t(f'tl.to("#bl{n}q", {{opacity:0, duration:0.1}}, {hit - 0.1:.2f});')
    c.t(f'tl.fromTo("#bl{n}e", {{opacity:0, scale:2.6}}, {{opacity:1, scale:1, duration:0.2, ease:"power4.in"}}, {hit - 0.2:.2f});')
    c.t(f'tl.fromTo("#tflash", {{opacity:0.8}}, {{opacity:0, duration:0.3, ease:"power2.out", immediateRender:false}}, {hit:.2f});')
    c.t(f'tl.to("#tr", {{keyframes:[{{x:-26, y:16, duration:0.04}}, {{x:22, y:-12, duration:0.04}}, {{x:-12, y:8, duration:0.05}}, {{x:0, y:0, duration:0.06}}]}}, {hit:.2f});')
    clip(c, "brag-quiz/sfx/crash.wav", hit - 0.02, 0.7); c.sfx("correct", hit + 0.1)
    t = done + d + 0.5
    c.t(f'tl.to(["#qo"], {{opacity:0, y:30, duration:0.3}}, {t - 0.3:.2f});')
    d = clip(c, cf["c5"], t)
    c.t(f'tl.fromTo("#hq", {{opacity:0, y:40, scale:0.96}}, {{opacity:1, y:0, scale:1, duration:0.45, ease:"power3.out"}}, {t + key_at(cf["c5"], cf["quote_key"], 1.6) - 0.1:.2f});')
    f = t + key_at(cf["c5"], cf["say_key"], 4.8); c.inn("#hs", f - 0.05); c.sfx("correct", f + 0.3)
    t += d + 0.5
    # 4. the closing ask, heard in full on the end card
    c.out_("#tr", t - 0.4); end = clip(c, cf["end"], t)
    body.append(c.end(t, cf["end_line"]))
    c.write("\n".join("      " + b for b in body), round(t + end + 0.9, 2))


def n2():
    """The word tree (IDEAS "a word tree", owner 18 Oct 2026: "be more creative"), root series part 4: ر ح م. The hook's family,
    round the line, gets hidden under leaves as the vine creeps in ("FAMILY is hiding inside a word you say in every prayer!");
    al-Fātiḥah 1:3 in al-Husary's recitation (reciter 12, as in the app), the three letters turn red and drop into the soil as a
    seed; a trunk grows and words bloom on its branches (رَحْمَة mercy, رَحِمَهُ اللهُ "may Allah have mercy on him"), a counter clicking
    up the words; then the tree pulls back for "your turn": the crown, رَحِم, 3-2-1, the WOMB. The Prophet ﷺ: the womb takes its
    name from ar-Raḥmān (al-Bukhārī 5988, Abu Hurayrah, sahih). Voices: brag-quiz/voice/rahma-lines.json (Rafiq for رَحِمَهُ اللهُ and رَحِم;
    the app's recording for رَحْمَة). Cut for length: the رَحِيم bloom, c3 and the أَرْحام round (their recordings stay unused)."""
    V = "brag-quiz/voice/rahma/"
    c = SO.vcomp("n2-rahma", "ARABIC · ONE ROOT"); c.bed = True; body = []; serif(c)
    bub = "".join(f'<div class="hb3" id="fb{k}" style="left:{x}px;top:{y}px">{t}</div>' for k, (x, y, t, w) in enumerate(FAMILY))
    vines, leaves = [], ""
    for k, (x, y, t, w) in enumerate(FAMILY):       # a vine from the nearest edge to each of them, and leaves that grow over them
        cx, cy = x + w / 2, y + 45; sx = 0 if cx < 540 else 1080
        vines.append(f'<path d="M{sx},{cy + 170} Q{(sx + cx) / 2:.0f},{cy + 230} {cx:.0f},{cy + 30}" pathLength="1"/>')
        for j, (dx, dy, r) in enumerate([(-24, 40, -30), (w * 0.35, 58, 20), (w * 0.62, -8, -150), (w - 20, 46, 35)]):
            leaves += f'<i class="leaf{" b" if j % 2 else ""}" id="fl{k}{j}" style="left:{x + dx:.0f}px;top:{y + dy:.0f}px;transform:rotate({r}deg)"></i>'
    bg = f'<svg class="vine" viewBox="0 0 1080 1920">{"".join(vines)}</svg>{bub}{leaves}'
    def anim(c, at, d):
        c.t(f'tl.fromTo(".vine path", {{strokeDashoffset:1}}, {{strokeDashoffset:0, duration:{at(3) - 0.1:.2f}, ease:"power1.inOut", stagger:0.06}}, 0.05);')
        for k in range(len(FAMILY)):
            c.t(f'tl.fromTo("#fb{k}", {{y:0, rotation:{-3 if k % 2 else 3}}}, {{y:{-24 if k % 2 else 20}, rotation:{2 if k % 2 else -2}, duration:{d + 0.3:.2f}, ease:"none"}}, 0);')
            for j in range(4):                       # "hiding inside": the leaves cover them
                c.t(f'tl.fromTo("#fl{k}{j}", {{scale:0, opacity:0}}, {{scale:1.25, opacity:1, duration:0.3, ease:"back.out(2.4)"}}, {at(2) + 0.08 * k + 0.05 * j:.2f});')
            c.t(f'tl.to("#fb{k}", {{opacity:0.55, filter:"blur(2px)", duration:0.4}}, {at(3) + 0.05 * k:.2f});')
        for k in (0, 3): c.sfx("tap", at(2) + 0.08 * k)
    words = "FAMILY is hiding inside a word you say in every prayer!".split()
    t = hook_in(c, body, (words, {0: "loud", 2: "red", 10: "circle"}, V + "h1a.mp3"), bg=(bg, anim))
    word_tree(c, body, t, dict(V=V, grow=GROW, ref="AL-FĀTIḤAH · 1:3", c1=V + "c1.mp3", recite=V + "fatiha-1-3t.mp3",
        verse=[[("ال", ""), ("رَّ", "r"), ("حْ", "r"), ("مَٰ", "r"), ("نِ", "")], [("ال", ""), ("رَّ", "r"), ("حِ", "r"), ("ي", ""), ("مِ", "r")]],
        times=(0.22, 1.55), seed=("mercy =", "ر ح م"), c2=V + "c2.mp3", c2key="mercy",
        crown=("رَحِم", "the womb"), opts=["mercy", "the womb", "a family"], right=1, crown_say=V + "rahim-womb.mp3", t1=V + "t1.mp3",
        slam=V + "b4b.mp3", slam_key="womb", c5=V + "c5.mp3", quote_key="said", say_key="family",
        quote='<q>The womb takes its name from <span style="font-style:normal;white-space:nowrap">ar-Raḥmān</span>.</q>'
              '<small>the Prophet <span class="pbuh">ﷺ</span> · al-Bukhārī 5988</small>',
        say="Family is built on mercy.", end=V + "end.mp3", end_line="Who in your family needs a call today? Comment below 👇 and send this to them 🤍"))

WORLD = [(70, 290, "☀️ the sun", 260), (640, 320, "🌙 the moon", 290), (330, 470, "✨ the stars", 280),   # the hook's world, round the line:
         (60, 1400, "⛰️ mountains", 300), (650, 1430, "🌊 the sea", 260), (330, 1610, "🌳 trees", 220)]   # each gets "a sign" on "sign"
GROW_ILM = [("M534,1330 C480,1300 450,1250 440,1205", 60, 1110, 380, "عِلْم", "knowledge", "ilm", "b1"),
            ("M545,1070 C580,1040 596,990 604,955", 600, 830, 420, "مُعَلِّم", "a teacher", None, "b2")]

def n3():
    """The word tree, part 2 (owner 21 Oct 2026, after n2-rahma): ع ل م "to know". Hook "The WORLD is a sign, and you say it in every
    prayer!" over the sun, moon, stars, mountains, sea and trees, each tagged "a sign" as Callum says it; al-Fātiḥah 1:2 in al-Husary's
    recitation (reciter 12, as in the app), رَبِّ الْعالَمِينَ; the root grows عِلْم knowledge and مُعَلِّم teacher (vocab-data.js); your turn:
    عَلامَة, 3-2-1, a SIGN; Ibn Kathīr on 1:2: ʿālam is derived from ʿalāma, a sign testifying to its Creator (quran.com, the English
    abridgement). Voices: brag-quiz/voice/ilm-lines.json (Rafiq for عِلْم and عَلامَة; the app's recording for مُعَلِّم; c1 and t1 from n2)."""
    V, VR = "brag-quiz/voice/ilm/", "brag-quiz/voice/rahma/"
    c = SO.vcomp("n3-ilm", "ARABIC · ONE ROOT"); c.bed = True; body = []; serif(c)
    bub = "".join(f'<div class="hb3" id="wb{k}" style="left:{x}px;top:{y}px">{t}<i>a sign</i></div>' for k, (x, y, t, w) in enumerate(WORLD))
    def anim(c, at, d):
        for k in range(len(WORLD)):
            c.t(f'tl.fromTo("#wb{k}", {{y:0, rotation:{-3 if k % 2 else 3}}}, {{y:{-24 if k % 2 else 20}, rotation:{2 if k % 2 else -2}, duration:{d + 0.3:.2f}, ease:"none"}}, 0);')
            s = at(4) + 0.1 * k                      # "sign": each of them is tagged
            c.t(f'tl.fromTo("#wb{k} i", {{opacity:0, scale:1.7}}, {{opacity:1, scale:1, duration:0.22, ease:"back.out(2.4)"}}, {s:.2f});')
            clip(c, "brag-quiz/sfx/ref/click.wav", s, 0.5)
    words = "The WORLD is a sign, and you say it in every prayer!".split()
    t = hook_in(c, body, (words, {1: "loud", 4: "red", 11: "circle"}, V + "h1c.mp3"), bg=(bub, anim))
    c.css += ("#hw1 { font-size:0.9em; } "                  # WORLD, shouted: small enough to fit the cover at its slam-in size
              ".hb3 i { position:absolute; right:-16px; top:-30px; font-style:normal; font-family:var(--la); font-size:28px; font-weight:700; "
              "padding:5px 14px; border-radius:18px; background:#E9B949; color:var(--ink); white-space:nowrap; opacity:0; }")
    word_tree(c, body, t, dict(V=V, grow=GROW_ILM, ref="AL-FĀTIḤAH · 1:2", c1=VR + "c1.mp3", recite=V + "fatiha-1-2t.mp3",
        verse=[[("الْحَمْدُ", "")], [("لِلَّهِ", "")], [("رَبِّ", "")], [("الْ", ""), ("عَ", "r"), ("ا", ""), ("لَ", "r"), ("مِ", "r"), ("ينَ", "")]],
        times=(0.2, 0.92, 1.43, 2.45), seed=("to know =", "ع ل م"), c2=V + "c2.mp3", c2key="know",
        crown=("عَلامَة", "a sign"), opts=["a world", "a sign", "a teacher"], right=1, crown_say=V + "alama.mp3", t1=VR + "t1.mp3",
        slam=V + "b4b.mp3", slam_key="sign", c5=V + "c5.mp3", quote_key="explains", say_key="pointing",
        quote='<q style="font-size:54px">ʿĀlam is derived from ʿalāma, because it is a sign testifying to the existence of its Creator…</q>'
              '<small>Ibn Kathīr on al-Fātiḥah 1:2</small>',
        say="The whole world is a sign 🌍", end=V + "end.mp3", end_line="What sign of Allah did you notice today? Comment below 👇"))

HIDDEN = [(70, 290, "🌴 gardens", 250), (650, 320, "🌙 the night", 270), (330, 470, "🛡️ a shield", 260),   # the hook: things from the root,
          (70, 1400, "👶 a baby", 230), (640, 1430, "👁️ the unseen", 290), (330, 1610, "🔥 the jinn", 250)]   # hidden by leaves on "same root"
TIMES_6_76 = (0.11, 1.05, 2.39, 3.40)   # فَلَمَّا · جَنَّ · عَلَيْهِ · اللَّيْلُ in anam-6-76t.mp3 (al-Husary, 0.40-4.62 s of 6:76: "when the night covered him")
GROW_JANNA = [("M534,1330 C480,1300 450,1250 440,1205", 60, 1110, 380, "جَنَّة", "a garden", "jannah", "b1"),
              ("M545,1070 C580,1040 596,990 604,955", 600, 830, 420, "جِنّ", "the jinn", "jinn", "b2")]

def n4():
    """The word tree, part 3 (owner 22 Oct 2026, #281): "Why does JANNAH share the same root as the jinn?" over things from the root
    (gardens, the night, a shield, a baby, the unseen, the jinn) that leaves grow over and hide; al-Anʿām 6:76 in al-Husary's
    recitation, فَلَمَّا جَنَّ عَلَيْهِ اللَّيْلُ "when the night covered him": ج ن ن = to cover; the root grows جَنَّة (a garden so thick its
    trees cover the ground) and جِنّ (beings hidden from our eyes); your turn: جُنَّة, 3-2-1, a SHIELD; then why Jannah: hidden from you for
    now. Ibn Fāris, Maqāyīs al-Lugha (ج ن): Jannah is "a reward hidden from them today"; Allah in a ḥadīth qudsī (al-Bukhārī 3244,
    Muslim 2824). n1-jannah (13 Oct) did the root in the old format. Voices: brag-quiz/voice/jannah2-lines.json (Rafiq for جُنَّة; جَنَّة
    and جِنّ are n1's recordings)."""
    V = "brag-quiz/voice/jannah2/"
    c = SO.vcomp("n4-jannah", "ARABIC · ONE ROOT"); c.bed = True; body = []; serif(c)
    bub = "".join(f'<div class="hb3" id="fb{k}" style="left:{x}px;top:{y}px">{t}</div>' for k, (x, y, t, w) in enumerate(HIDDEN))
    leaves = "".join(f'<i class="leaf{" b" if j % 2 else ""}" id="fl{k}{j}" style="left:{x + dx:.0f}px;top:{y + dy:.0f}px;transform:rotate({r}deg)"></i>'
                     for k, (x, y, t, w) in enumerate(HIDDEN) for j, (dx, dy, r) in enumerate([(-24, 40, -30), (w * 0.35, 58, 20), (w * 0.62, -8, -150), (w - 20, 46, 35)]))
    def anim(c, at, d):
        for k in range(len(HIDDEN)):
            c.t(f'tl.fromTo("#fb{k}", {{y:0, rotation:{-3 if k % 2 else 3}}}, {{y:{-24 if k % 2 else 20}, rotation:{2 if k % 2 else -2}, duration:{d + 0.3:.2f}, ease:"none"}}, 0);')
            for j in range(4):                       # "the same root": leaves grow over each of them and hide it
                c.t(f'tl.fromTo("#fl{k}{j}", {{scale:0, opacity:0}}, {{scale:1.3, opacity:1, duration:0.3, ease:"back.out(2.4)"}}, {at(5) + 0.08 * k + 0.05 * j:.2f});')
            c.t(f'tl.to("#fb{k}", {{opacity:0.45, filter:"blur(3px)", duration:0.4}}, {at(6) + 0.05 * k:.2f});')
        for k in (0, 3): c.sfx("tap", at(5) + 0.08 * k)
    words = "Why does JANNAH share the same root as the jinn?".split()
    c.slam_x = 0                                         # JANNAH slams in on its own line, centred, so it fits the cover
    t = hook_in(c, body, (words, {2: "loud", 6: "circle", 9: "red"}, V + "h1a.mp3"), bg=(bub + leaves, anim))
    c.css += "#hw2 { display:block; width:max-content; margin:0 auto; font-size:1.05em; } "
    word_tree(c, body, t, dict(V=V, grow=GROW_JANNA, intro="In the Qur’an:", ref="AL-ANʿĀM · 6:76", c1=V + "c1.mp3", recite=V + "anam-6-76t.mp3",
        verse=[[("فَلَمَّا", "")], [("جَ", "r"), ("نَّ", "r")], [("عَلَيْهِ", "")], [("اللَّيْلُ", "")]],
        times=TIMES_6_76, seed=("to cover =", "ج ن ن"), c2=V + "c2.mp3", c2key="cover",
        crown=("جُنَّة", "a shield"), opts=["a garden", "a shield", "a jinn"], right=1, crown_say=V + "junna.mp3", t1=V + "t1.mp3",
        slam=V + "b4b.mp3", slam_key="shield", c5=V + "c5.mp3", quote_key="prepared", say_key="hidden",
        quote='<q style="font-size:54px">I have prepared for My righteous servants what no eye has seen, no ear has heard, and no heart has ever imagined.</q>'
              '<small>Allah, in a ḥadīth qudsī · al-Bukhārī 3244</small>',
        say='Hidden from you… for now 🤍<small style="display:block;font-size:30px;font-weight:700;color:var(--ink-soft);margin-top:10px">'
            'Jannah: “a reward hidden from them today” · Ibn Fāris, Maqāyīs al-Lugha</small>',
        end=V + "end.mp3", end_line="Send this to someone you want to meet in Jannah 🤍 What will you ask for first? 👇"))

PRAYERS = [(70, 290, "🌅 Fajr"), (640, 320, "☀️ Dhuhr"), (330, 470, "🌤️ ʿAsr"),   # the hook's five prayers round the line,
           (60, 1400, "🌇 Maghrib"), (650, 1430, "🌙 ʿIshāʾ")]                     # numbered 1 to 5 as FIVE lands
TIMES_HAYYA = (0.06, 0.60, 0.88)   # حَيَّ · عَلَى · الصَّلاةِ in hayya.mp3 (Rafiq), from the dips in its loudness
GROW_SALAH = [("M534,1330 C480,1300 450,1250 440,1205", 60, 1110, 380, "الصَّلاة", "the prayer", None, "b1"),
              ("M545,1070 C580,1040 596,990 604,955", 600, 830, 420, "مُصَلَّى", "a place of prayer", None, "b2")]

def n5():
    """The word tree, part 4 (IDEAS "root series part 6", 24 Oct 2026, #290): ص ل و. Hook "You do it FIVE times a day… but what does
    salah really mean?" over the five prayers, numbered 1 to 5 with a click each as FIVE lands; حَيَّ عَلَى الصَّلاةِ from the adhān in
    Rafiq's voice (no Qur'an recitation this time: #289, reused recitation audio may be why TikTok kept m2-barik off the For You
    feed); the root grows الصَّلاة the prayer and مُصَلَّى a place of prayer (the app's recordings); your turn: فَلْيُصَلِّ, 3-2-1, make
    DUʿĀʾ: invited to a meal while fasting, "let him pray" (Muslim 1431, Abū Hurayrah), and al-Tirmidhī 780 adds "meaning duʿāʾ";
    so in Arabic ṣalāh is duʿāʾ, calling on Allah. Voices: brag-quiz/voice/salah5-lines.json."""
    V = "brag-quiz/voice/salah5/"
    c = SO.vcomp("n5-salah", "ARABIC · ONE ROOT"); c.bed = True; body = []; serif(c)
    bub = "".join(f'<div class="hb3" id="pb{k}" style="left:{x}px;top:{y}px">{t}<i>{k + 1}</i></div>' for k, (x, y, t) in enumerate(PRAYERS))
    def anim(c, at, d):
        for k in range(len(PRAYERS)):
            c.t(f'tl.fromTo("#pb{k}", {{y:0, rotation:{-3 if k % 2 else 3}}}, {{y:{-24 if k % 2 else 20}, rotation:{2 if k % 2 else -2}, duration:{d + 0.3:.2f}, ease:"none"}}, 0);')
            s = at(3) + 0.2 + 0.14 * k                # FIVE: they're counted, 1 to 5, a click on each
            c.t(f'tl.fromTo("#pb{k} i", {{opacity:0, scale:1.8}}, {{opacity:1, scale:1, duration:0.22, ease:"back.out(2.4)"}}, {s:.2f});')
            clip(c, "brag-quiz/sfx/ref/click.wav", s, 0.6)
    words = "You do it FIVE times a day… but what does salah really mean?".split()
    c.slam_x = 0                                         # FIVE slams in on its own line, centred, so it fits the cover
    t = hook_in(c, body, (words, {3: "loud", 10: "red", 12: "circle"}, V + "h1a.mp3"), bg=(bub, anim))
    c.css += ("#hw3 { display:block; width:max-content; margin:0 auto; letter-spacing:.1em; transform-origin:50% 8%; } "
              ".hb3 i { position:absolute; right:-16px; top:-30px; font-style:normal; font-family:\"Fredoka\", var(--la); font-size:34px; font-weight:700; "
              "width:52px; height:52px; line-height:52px; text-align:center; border-radius:50%; background:#E9B949; color:var(--ink); opacity:0; }")
    word_tree(c, body, t, dict(V=V, grow=GROW_SALAH, intro="You hear it in every adhān:", ref="THE ADHĀN", c1=V + "c1.mp3", recite=V + "hayya.mp3",
        verse=[[("حَيَّ", "")], [("عَلَى", "")], [("ال", ""), ("صَّ", "r"), ("لا", "r"), ("ةِ", "")]],
        times=TIMES_HAYYA, seed=("to pray =", "ص ل و"), c2=V + "c2.mp3", c2key="pray",
        crown=("فَلْيُصَلِّ", "make duʿāʾ"), opts=["ṣalāh", "duʿāʾ", "eat"], right=1, crown_say=V + "falyusalli.mp3", t1=V + "t1.mp3",
        slam=V + "b4b.mp3", slam_key="dua", c5=V + "c5.mp3", quote_key="narration", say_key="every",
        quote='<q style="font-size:54px">If one of you is invited to a meal… and he is fasting, let him pray.</q>'
              '<small>the Prophet <span class="pbuh">ﷺ</span> · Muslim 1431</small>'
              '<small style="margin-top:6px">“meaning: duʿāʾ” · al-Tirmidhī 780</small>',
        say="Every ṣalāh is a duʿāʾ 🤲", end=V + "end.mp3", end_line="Who do you make duʿāʾ for first? Comment below 👇 and send this to them 🤲"))

TALLY = [("Fajr", 2, 70, 300), ("Dhuhr", 4, 590, 300), ("ʿAsr", 4, 330, 460), ("Maghrib", 3, 60, 1320), ("ʿIshāʾ", 4, 600, 1320)]   # 17 rakʿahs

DIN_CSS = (
    ".tp { position:absolute; display:flex; align-items:center; gap:14px; padding:16px 26px; background:var(--card); border:4px solid rgba(23,38,43,.12); "
    "border-radius:34px; box-shadow:0 14px 30px -18px rgba(23,38,43,.4); } .tp span { font-family:\"Fredoka\", var(--la); font-weight:600; font-size:46px; "
    "margin-right:8px; } .tp i { width:34px; height:34px; border-radius:50%; border:5px solid rgba(23,38,43,.22); box-sizing:border-box; }"
    "#dring { position:absolute; left:400px; top:1490px; width:280px; height:280px; } #dring svg { position:absolute; inset:0; transform:rotate(-90deg); }"
    "#dring circle { fill:none; stroke-width:20; } #dring .bg { stroke:rgba(23,38,43,.1); } #dring .fg { stroke:var(--rubric); stroke-linecap:round; "
    "stroke-dasharray:741; stroke-dashoffset:741; } #dring .tn { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; "
    "justify-content:center; line-height:1; font-family:\"Fredoka\", var(--la); } #dring b { font-size:120px; color:var(--rubric); } #dring span { position:absolute; "
    "left:-80px; right:-80px; top:294px; text-align:center; font-size:30px; letter-spacing:.14em; font-weight:700; } .chip .q { font-family:\"Fredoka\", var(--la); font-size:84px; line-height:1.35; color:var(--rubric); }"
    ".ops2 .op b.en { font-family:var(--la); font-size:62px; line-height:1.2; } .ref { position:absolute; left:70px; right:70px; text-align:center; font-size:34px; "
    "font-weight:700; letter-spacing:.03em; color:var(--ink-soft); line-height:1.3; } .yrow { position:absolute; left:0; right:0; top:330px; text-align:center; "
    "font-family:\"Fredoka\", var(--la); font-weight:700; color:var(--rubric); } .yrow b { font-size:190px; letter-spacing:-.02em; } .yrow span { display:block; "
    "font-size:60px; color:var(--ink); margin-top:-10px; } .yu { position:relative; height:80px; } .yu em { position:absolute; left:0; right:0; font-style:normal; } .grid { position:absolute; left:80px; top:680px; width:920px; display:grid; grid-template-columns:repeat(20, 1fr); "
    "gap:8px; } .grid i { height:38px; border-radius:9px; background:rgba(23,38,43,.08); }")

def d1():
    """Seventeen times a day (owner 18 Oct 2026: "be more creative"): the hook's background is the day's prayers, a dot for each
    rakʿah, clicking up to 17 on a ring as Callum says it; al-Fātiḥah 1:4 in al-Husary's recitation (reciter 12, as in the app);
    مالِكِ "Master" · يَوْمِ "of the Day" · الدِّينِ "?"; the quiz: you know دِين as "religion", but here? 3-2-1: repayment. Ibn Kathīr on
    1:4, from Ibn ʿAbbās: "the Day of Recompense for the creatures, the Day of Judgement". Then a year of it: 365 squares fill as the
    count rolls 17 → 6,205. Voices: brag-quiz/voice/din-lines.json."""
    V = "brag-quiz/voice/din/"
    c = SO.vcomp("d1-din", "ARABIC · WHAT YOU REALLY SAY"); c.bed = True; body = []; serif(c)
    pills = "".join(f'<div class="tp" id="tp{k}" style="left:{x}px;top:{y}px"><span>{n}</span>' + "".join(f'<i id="td{k}{j}"></i>' for j in range(r)) + '</div>'
                    for k, (n, r, x, y) in enumerate(TALLY))
    ring = ('<div id="dring"><svg viewBox="0 0 280 280"><circle class="bg" cx="140" cy="140" r="118"/><circle class="fg" cx="140" cy="140" r="118"/></svg>'
            '<div class="tn"><b id="dn">0</b><span>RAKʿAHS A DAY</span></div></div>')
    def anim(c, at, d):
        a, b = at(1) - 0.1, at(10) - 0.35          # from "times" to just before "MEANS": a dot fills and the ring clicks for every rakʿah
        dots = [(k, j) for k, (_, r, _, _) in enumerate(TALLY) for j in range(r)]
        for n, (k, j) in enumerate(dots):
            s = a + (b - a) * n / 17
            c.t(f'tl.to("#td{k}{j}", {{backgroundColor:"{T.RED}", borderColor:"{T.RED}", duration:0.08}}, {s:.2f});')
            c.t(f'tl.fromTo("#td{k}{j}", {{scale:1.7}}, {{scale:1, duration:0.2, ease:"back.out(3)", immediateRender:false}}, {s:.2f});')
            clip(c, "brag-quiz/sfx/ref/click.wav", s, 0.55)
            if j == TALLY[k][1] - 1: c.t(f'tl.to("#tp{k}", {{borderColor:"{T.RED}", duration:0.2}}, {s:.2f});')
        c.t(f'(() => {{ const o = {{v:0}}; tl.to(o, {{v:17, duration:{b - a + (b - a) / 17:.2f}, ease:"none", onUpdate:() => {{ document.getElementById("dn").textContent = Math.min(17, Math.floor(o.v)); }}}}, {a:.2f}); }})();')
        c.t(f'tl.to("#dring .fg", {{strokeDashoffset:0, duration:{b - a:.2f}, ease:"none"}}, {a:.2f});')
        c.t(f'tl.fromTo("#dring", {{scale:1}}, {{scale:1.12, duration:0.16, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {b:.2f});')
        for k in range(len(TALLY)): c.t(f'tl.fromTo("#tp{k}", {{y:0}}, {{y:{-18 if k % 2 else 16}, duration:{d + 0.3:.2f}, ease:"none"}}, 0);')
    words = "17 times a day… do you know what this word MEANS?".split()   # SEVENTEEN, said; 17 fits the cover
    t = hook_in(c, body, (words, {0: "loud", 6: "red", 10: "circle"}, V + "h1b.mp3"), bg=(pills + ring, anim))
    c.css += MASH_CSS + DIN_CSS + ".qref { color:#9a7826; } #hw0 { font-size:2.1em; color:var(--rubric); }"
    # 1. al-Fātiḥah 1:4: each word lights up as al-Husary recites it (from the audio), then Master · of the Day · ?
    QW = [("مَالِكِ", 0.25), ("يَوْمِ", 0.95), ("الدِّينِ", 1.95)]
    body.append('<div class="sec" id="a"><div class="q2">In every rakʿah you say:</div><div class="qref" style="top:350px">AL-FĀTIḤAH · 1:4</div>'
                '<div class="qr" style="top:470px;font-size:124px">' + " ".join(f'<span class="w" id="aw{i}">{w}</span>' for i, (w, _) in enumerate(QW)) + '</div>'
                '<div class="chips" style="top:860px">' + "".join(f'<div class="chip" id="ac{i}"><div class="ar">{a}</div><b>{en}</b></div>' for i, (a, en) in
                enumerate([("مَالِكِ", "Master"), ("يَوْمِ", "of the Day")])) + '<div class="chip" id="ac2"><div class="ar">الدِّينِ</div><b class="q" id="acq">?</b></div></div></div>')
    whip_in(c, "a", t); t += 0.3                       # the line on screen says "In every rakʿah you say:", so no c1
    dq = say_up(c, "", t, src=V + "fatiha-1-4t.mp3")
    for i, (_, s) in enumerate(QW):
        c.t(f'tl.to("#aw{i}", {{color:"#a8842c", duration:0.25}}, {t + s:.2f});')
        c.t(f'tl.fromTo("#aw{i}", {{scale:1}}, {{scale:1.1, duration:0.18, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {t + s:.2f});')
    t += dq; d = clip(c, V + "c2.mp3", t)
    for i, key in enumerate(("master", "day", "what")):
        s = t + key_at(V + "c2.mp3", key, d * i / 3); c.inn(f"#ac{i}", s - 0.05, 30); c.sfx("tap", s)
    w = t + key_at(V + "c2.mp3", "what", d - 0.5)
    c.t(f'tl.fromTo("#acq", {{rotation:0, scale:1}}, {{keyframes:[{{rotation:-14, scale:1.3, duration:0.12}}, {{rotation:12, duration:0.12}}, {{rotation:0, scale:1, duration:0.16}}]}}, {w + 0.1:.2f});')
    t = whip_out(c, "a", t + d + 0.4)
    # 2. the quiz: 3-2-1, repayment, with Ibn Kathīr's source on screen
    body.append('<div class="sec" id="q"><div class="q2">You know <bdi class="ar" lang="ar">دِين</bdi> as “religion”…</div>'
                '<div class="big" id="qb" style="top:430px;font-size:170px;color:var(--rubric)" lang="ar">الدِّينِ</div>'
                f'<div class="ques" id="qq" style="top:720px;font-size:70px">but here, it means…?</div>{cnt("qc", 830)}'
                '<div class="ops2" style="top:1000px">' + "".join(f'<div class="op" id="qo{i}"><b class="en">{o}</b></div>' for i, o in enumerate(["religion", "repayment", "faith"])) + '</div>'
                '<div class="quote" id="qs" style="top:1230px"><q>The Day of Recompense for the creatures: the Day of Judgement.</q><small>Ibn ʿAbbās, in Tafsīr Ibn Kathīr on 1:4</small></div></div>')
    whip_in(c, "q", t); c.inn("#q .q2", t); SO.bigin(c, "#qb", t + 0.3)
    d = clip(c, V + "q1.mp3", t + 0.1)
    c.inn("#qq", t + 0.1 + key_at(V + "q1.mp3", "here", 2.1) - 0.05)
    o = t + 0.1 + key_at(V + "q1.mp3", "what", 2.4)
    for i in range(3): c.inn(f"#qo{i}", o + i * 0.12, 30)
    done = count_down(c, "qc", t + 0.1 + d + 0.3)
    reveal(c, "#qo1", ["#qo0", "#qo2"], done); c.sfx("correct", done)
    d = clip(c, V + "r1.mp3", done + 0.3)
    j = done + 0.3 + key_at(V + "r1.mp3", "that's", 4.1)
    c.t(f'tl.to(["#qo0", "#qo2"], {{opacity:0, duration:0.25}}, {j - 0.3:.2f});'); c.t(f'tl.to("#qo1", {{y:-198, duration:0.4, ease:"power3.inOut"}}, {j - 0.3:.2f});')
    c.t(f'tl.fromTo("#qs", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.45, ease:"power3.out"}}, {j - 0.1:.2f});')
    t = whip_out(c, "q", done + 0.3 + d + 0.5)
    # 3. a year of it: 365 squares fill row by row, a click on every row, as the count rolls 17 → 6,205
    body.append('<div class="sec" id="y"><div class="yrow"><b id="yn">17</b><span class="yu"><em id="yd">times a day</em><em id="yy">times a year</em></span></div><div class="grid">'
                + '<i></i>' * 365 + '</div><div class="say" id="ys" style="top:1620px">Now you’ll know what you’re saying.</div></div>')
    whip_in(c, "y", t); d = clip(c, V + "n1.mp3", t + 0.1)
    a = t + 0.1 + key_at(V + "n1.mp3", "is", 1.46); b = t + 0.1 + key_at(V + "n1.mp3", "year", 3.09) + 0.1
    c.t(f'tl.to(".grid i", {{backgroundColor:"{T.GREEN}", duration:0.05, stagger:{(b - a) / 365:.4f}}}, {a:.2f});')
    for r in range(19): clip(c, "brag-quiz/sfx/ref/click.wav", a + (b - a) * r / 19, 0.5)
    c.t(f'(() => {{ const o = {{v:17}}; tl.to(o, {{v:6205, duration:{b - a:.2f}, ease:"none", onUpdate:() => {{ document.getElementById("yn").textContent = Math.round(o.v).toLocaleString("en-GB"); }}}}, {a:.2f}); }})();')
    c.t(f'tl.to("#yd", {{opacity:0, duration:0.15}}, {a:.2f});')
    c.t(f'tl.fromTo("#yy", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.25, ease:"back.out(2)"}}, {b:.2f});')
    c.t(f'tl.fromTo("#yn", {{scale:1}}, {{scale:1.12, duration:0.16, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {b:.2f});'); c.sfx("correct", b)
    c.inn("#ys", t + 0.1 + key_at(V + "n1.mp3", "now", 4.2) - 0.05)
    t += 0.1 + d + 0.6
    c.out_("#y", t - 0.4); end = clip(c, V + "end.mp3", t)
    body.append(c.end(t, "Did you know this one? Comment yes or no 👇 and send this to someone you pray with"))
    c.write("\n".join("      " + b for b in body), round(t + end + 0.9, 2))

FT = [  # the family tree: (id, centre x, centre y, emoji, English, Arabic, side: "d" dad's, "m" mum's, "" you)
    ("g1", 150, 480, "👴🏽", "Grandpa", "جَدّ", "d"), ("g2", 360, 480, "👵🏽", "Grandma", "جَدَّة", "d"),
    ("g3", 720, 480, "👴🏽", "Grandpa", "جَدّ", "m"), ("g4", 930, 480, "👵🏽", "Grandma", "جَدَّة", "m"),
    ("u1", 95, 830, "🧔🏽", "Uncle", "عَمّ", "d"), ("a1", 270, 830, "🧕🏽", "Aunty", "عَمَّة", "d"), ("fa", 445, 830, "🧔🏽", "Dad", "أَب", "d"),
    ("mo", 635, 830, "🧕🏽", "Mum", "أُمّ", "m"), ("a2", 810, 830, "🧕🏽", "Aunty", "خالَة", "m"), ("u2", 985, 830, "🧔🏽", "Uncle", "خال", "m"),
    ("me", 540, 1180, "🧒🏽", "You", "أَنا", "")]
FT_LINES = ("M150,480 H360 M255,480 V700 M95,700 H445 M95,700 V770 M270,700 V770 M445,700 V770"
            " M720,480 H930 M825,480 V700 M635,700 H985 M635,700 V770 M810,700 V770 M985,700 V770 M445,830 H635 M540,830 V1120")
HFAM = [(70, 290, "👴🏽", "Grandpa", ""), (310, 260, "👵🏽", "Grandma", ""), (580, 290, "🧔🏽", "Dad", ""), (820, 260, "🧕🏽", "Mum", "mum"),
        (50, 1330, "🧕🏽", "Aunty", "a"), (300, 1400, "🧔🏽", "Uncle", ""), (570, 1330, "🧕🏽", "Aunty", "a"), (820, 1400, "🧔🏽", "Uncle", "")]

FAM_CSS = (
    "#ft { position:absolute; left:0; top:0; width:1080px; height:1920px; transform-origin:0 0; } #ft svg { position:absolute; inset:0; overflow:visible; }"
    "#ft path { fill:none; stroke:rgba(23,38,43,.32); stroke-width:6; stroke-linecap:round; stroke-dasharray:1; stroke-dashoffset:1; }"
    ".fn { position:absolute; width:170px; text-align:center; } .fc { position:relative; width:132px; height:132px; margin:0 auto; border-radius:50%; "
    "background:var(--card); border:7px solid rgba(23,38,43,.25); display:grid; place-items:center; font-family:\"Noto Color Emoji\", sans-serif; font-size:74px; "
    "line-height:1; box-shadow:0 14px 28px -16px rgba(23,38,43,.5); } .fn.d .fc { border-color:var(--verdigris); } .fn.m .fc { border-color:#E9B949; }"
    ".fn b { display:block; margin-top:6px; font-family:\"Fredoka\", var(--la); font-weight:600; font-size:32px; color:var(--ink); }"
    ".fn i { position:relative; display:block; height:64px; font-style:normal; } .fn i span { position:absolute; left:-20px; right:-20px; top:0; font-family:var(--ar); "
    "font-weight:700; font-size:48px; line-height:1.3; color:var(--rubric); opacity:0; } .fn i .q { font-family:\"Fredoka\", var(--la); color:#7f611b; }"
    ".badge { position:absolute; right:-12px; top:-12px; width:52px; height:52px; border-radius:50%; background:var(--rubric); color:#fff; font-family:\"Fredoka\", var(--la); "
    "font-weight:700; font-size:34px; display:grid; place-items:center; opacity:0; } .side { position:absolute; top:330px; font-weight:700; font-size:28px; letter-spacing:.16em; }"
    ".side.d { left:70px; color:var(--verdigris); } .side.m { right:70px; color:#9a7826; } .heart { position:absolute; font-family:\"Noto Color Emoji\", sans-serif; font-size:70px; opacity:0; }"
    ".rp { position:absolute; left:50%; top:1290px; transform:translateX(-50%); padding:14px 40px; border-radius:50px; font-size:48px; font-weight:700; color:#fff; white-space:nowrap; }"
    ".rp.d { background:var(--verdigris); } .rp.m { background:#a8842c; } .rp em { font-style:normal; opacity:.75; font-weight:500; }"
    ".hp { position:absolute; text-align:center; width:200px; } .hp .fc { width:120px; height:120px; font-size:66px; } .hp b { display:block; margin-top:6px; "
    "font-family:\"Fredoka\", var(--la); font-weight:600; font-size:34px; color:var(--ink); } .hp.a .fc { border-color:var(--rubric); }"
    ".opts .op2 .ar { font-family:var(--ar); font-size:62px; line-height:1.3; } .sum { position:absolute; left:70px; right:70px; display:flex; gap:20px; }"
    ".sum div { flex:1; padding:14px 0 18px; border-radius:30px; text-align:center; font-weight:700; font-size:30px; letter-spacing:.06em; color:#fff; }"
    ".sum .d { background:var(--verdigris); } .sum .m { background:#a8842c; } .sum span { display:block; font-family:var(--ar); font-size:54px; letter-spacing:0; line-height:1.35; }")

def f4():
    """The family tree (owner, 18 Oct 2026: "a family tree, then zoom in to one and explain the background, aunty, uncle, grandma or
    grandpa; a fun fact would be nice"). Hook "TWO words for 'aunty' in Arabic, and one's like your MUM!" over the family's faces popping
    in with a click each, the two aunties turning red; the tree, dad's side green and mum's side gold, its words in Arabic (vocab-data.js:
    عَمّ paternal uncle, عَمَّة paternal aunt); the camera zooms into dad's sister, عَمَّة, then pans to mum's sister, خالَة; the fun fact:
    Ḥamza's daughter given to her khala, "the maternal aunt is in the place of the mother" (al-Bukhārī 2699, also 4251; Tirmidhī 1904);
    your turn: mum's brother, 3-2-1, خال. Voices: brag-quiz/voice/family-lines.json (Rafiq for خالَة and خال; the app's recordings for
    the rest)."""
    V = "brag-quiz/voice/family/"
    c = SO.vcomp("f4-family", "ARABIC · YOUR FAMILY"); c.bed = True; body = []; serif(c)
    c.css += MASH_CSS + GROW_CSS + FAM_CSS
    hp = "".join(f'<div class="hp{" a" if r == "a" else ""}" id="hp{k}" style="left:{x}px;top:{y}px"><div class="fc">{em}</div><b>{en}</b></div>' for k, (x, y, em, en, r) in enumerate(HFAM))
    hearts = ('<div class="heart" id="hh0" data-layout-allow-overlap style="left:930px;top:250px">❤️</div>'
              '<div class="heart" id="hh1" data-layout-allow-overlap style="left:680px;top:1320px">❤️</div>')
    def anim(c, at, d):                              # the family pops in, a click each; the aunties last, red, as "aunty" is said; hearts on MUM
        rest = [k for k, h in enumerate(HFAM) if h[4] != "a"]
        for n, k in enumerate(rest):
            s = 0.1 + (at(3) - 0.5) * n / len(rest)
            c.t(f'tl.fromTo("#hp{k}", {{scale:0, opacity:0}}, {{scale:1, opacity:1, duration:0.3, ease:"back.out(2.2)"}}, {s:.2f});')
            clip(c, "brag-quiz/sfx/ref/click.wav", s, 0.55)
        for j, k in enumerate(k for k, h in enumerate(HFAM) if h[4] == "a"):
            s = at(3) + 0.12 * j
            c.t(f'tl.fromTo("#hp{k}", {{scale:0, opacity:0}}, {{scale:1, opacity:1, duration:0.32, ease:"back.out(2.6)"}}, {s:.2f});')
            c.t(f'tl.fromTo("#hp{k}", {{scale:1}}, {{scale:1.18, duration:0.16, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {s + 0.35:.2f});')
            c.t(f'tl.to("#hp{k} b", {{color:"{T.RED}", duration:0.2}}, {s:.2f});'); clip(c, "brag-quiz/sfx/ref/click.wav", s, 0.8)
        for k in range(len(HFAM)): c.t(f'tl.to("#hp{k}", {{y:{-18 if k % 2 else 16}, duration:{d:.2f}, ease:"none"}}, 0.4);')
        for j in range(2): c.t(f'tl.fromTo("#hh{j}", {{opacity:0, scale:0.2, y:30}}, {{opacity:1, scale:1, y:0, duration:0.35, ease:"back.out(3)"}}, {at(10) + 0.1 * j:.2f});')
    words = "TWO words for “aunty” in Arabic, and one’s like your MUM!".split()
    t = hook_in(c, body, (words, {0: "loud", 3: "red", 10: "circle"}, V + "h1a.mp3"), bg=(hp + hearts, anim))
    # 1. the tree: lines draw, the family pops in, then their words turn Arabic
    nodes = "".join(f'<div class="fn {sd}" id="n{i}" style="left:{x - 85}px;top:{y - 66}px"><div class="fc">{em}'
                    + (f'<span class="badge" id="bd{i}">{1 if i == "a1" else 2}</span>' if i in ("a1", "a2") else "")
                    + f'</div><b>{en}</b><i><span id="n{i}a" lang="ar">{ar}</span>' + ('<span class="q" id="nu2q">?</span>' if i == "u2" else "") + '</i></div>'
                    for i, x, y, em, en, ar, sd in FT)
    body.append(f'<div class="sec" id="t"><div id="ft" data-layout-allow-overflow data-layout-allow-occlusion><svg viewBox="0 0 1080 1920"><path d="{FT_LINES}" pathLength="1"/></svg>'
                f'<div class="side d" id="sd">DAD’S SIDE</div><div class="side m" id="sm">MUM’S SIDE</div>{nodes}'
                '<div class="heart" id="th" data-layout-allow-overlap style="left:688px;top:770px">❤️</div></div>'
                '<div class="rp d" id="rp1">ʿamma <em>· dad’s sister</em></div><div class="rp m" id="rp2">khāla <em>· mum’s sister</em></div>'
                '<div class="quote" id="tq" style="top:1440px"><small id="tqs" style="margin:0 0 12px">Ḥamza’s daughter needed a home. She went to her khala:</small>'
                '<q>The maternal aunt is in the place of the mother.</q><small>the Prophet <span class="pbuh">ﷺ</span> · al-Bukhārī 2699</small></div>'
                f'{cnt("tc", 1365)}<div class="opts" id="to" style="top:1545px">' + "".join(f'<div class="op2" id="to{k}"><b class="ar">{a}</b></div>' for k, a in enumerate(["عَمّ", "خال", "جَدّ"]))
                + '</div><div class="sum" id="ts" style="top:1440px"><div class="d">DAD’S SIDE<span>عَمّ · عَمَّة</span></div><div class="m">MUM’S SIDE<span>خال · خالَة</span></div></div></div>')
    whip_in(c, "t", t); c.t('tl.set("#ft", {transformOrigin:"0 0"}, 0);')
    c.t(f'tl.to("#ft path", {{strokeDashoffset:0, duration:0.9, ease:"power2.inOut"}}, {t:.2f});')
    for n, (i, x, y, *_ ) in enumerate(FT):
        c.t(f'tl.fromTo("#n{i}", {{scale:0, opacity:0}}, {{scale:1, opacity:1, duration:0.3, ease:"back.out(2.2)"}}, {t + 0.1 + 0.07 * n:.2f});')
    for i in ("sd", "sm"): c.inn(f"#{i}", t + 0.5)
    clip(c, "brag-quiz/sfx/ref/short-swoosh.wav", t, 0.3)
    d = clip(c, V + "v1.mp3", t + 0.3); a = t + 0.3 + key_at(V + "v1.mp3", "arabic", d - 0.6)
    for n, (i, *_ ) in enumerate(FT):               # the words turn Arabic, a click each (mum's brother stays a "?" for the quiz)
        s = a + 0.06 * n; sel = "#nu2q" if i == "u2" else f"#n{i}a"
        c.t(f'tl.fromTo("{sel}", {{opacity:0, rotationX:90}}, {{opacity:1, rotationX:0, duration:0.25, ease:"power2.out"}}, {s:.2f});')
        if n % 2 == 0: clip(c, "brag-quiz/sfx/ref/click.wav", s, 0.45)
    t = max(t + 0.3 + d, a + 0.8) + 0.1
    # 2. two aunties: a badge and a click each, then the camera zooms into dad's sister and pans to mum's sister
    d = clip(c, V + "v2.mp3", t); b = t + key_at(V + "v2.mp3", "both", 0.9)
    for j, i in enumerate(("a1", "a2")):
        s = b + 0.35 * j
        c.t(f'tl.fromTo("#bd{i}", {{opacity:0, scale:2}}, {{opacity:1, scale:1, duration:0.25, ease:"back.out(2.5)"}}, {s:.2f});'); clip(c, "brag-quiz/sfx/ref/click.wav", s, 0.9)
        c.t(f'tl.fromTo("#n{i} .fc", {{scale:1}}, {{scale:1.15, duration:0.16, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {s:.2f});')
    t += d + 0.1
    def cam(s, cx, cy, at, dur=0.8):                 # point (cx, cy) of the tree to (540, 700) on screen, at scale s
        c.t(f'tl.to("#ft", {{scale:{s}, x:{540 - s * cx:.0f}, y:{700 - s * cy:.0f}, duration:{dur}, ease:"power3.inOut"}}, {at:.2f});')
        clip(c, "brag-quiz/sfx/ref/short-swoosh.wav", at, 0.3)
    cam(2.1, 270, 830, t); c.t(f'tl.to("#bda1, #bda2", {{opacity:0, duration:0.2}}, {t:.2f});')
    c.t(f'tl.to(["#brand", "#kicker", "#nme"], {{autoAlpha:0, duration:0.25}}, {t:.2f});')   # out of the camera's way until the quiz
    d = clip(c, V + "v3.mp3", t + 0.1); t += 0.1 + d
    c.inn("#rp1", t); d = say_up(c, "عَمَّة", t + 0.05); t += 0.05 + d + 0.3
    c.t(f'tl.to("#rp1", {{opacity:0, duration:0.25}}, {t:.2f});'); cam(2.1, 810, 830, t)
    d = clip(c, V + "v4.mp3", t + 0.1); t += 0.1 + d
    c.inn("#rp2", t); d = say_up(c, "", t + 0.05, src=V + "khala.mp3")
    c.t(f'tl.fromTo("#na2 .fc", {{scale:1}}, {{scale:1.12, duration:0.18, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {t + 0.1:.2f});'); c.sfx("tap", t + 0.1)
    t += 0.05 + d + 0.4
    # 3. the fun fact: back out to khala and mum side by side, the story, the hadith, a heart between them
    c.t(f'tl.to("#rp2", {{opacity:0, duration:0.25}}, {t - 0.1:.2f});'); cam(1.45, 722, 830, t)
    d = clip(c, V + "v5.mp3", t + 0.2); v = t + 0.2
    c.t(f'tl.fromTo("#tq", {{autoAlpha:0, y:40}}, {{autoAlpha:1, y:0, duration:0.45, ease:"power3.out"}}, {v + key_at(V + "v5.mp3", "hamza", 0.3) - 0.1:.2f});')
    c.t(f'tl.set("#tq q, #tq small:last-child", {{opacity:0}}, 0);')
    q = v + key_at(V + "v5.mp3", "maternal", d - 3.0) - 0.4
    c.t(f'tl.fromTo("#tq q, #tq small:last-child", {{opacity:0, y:14}}, {{opacity:1, y:0, duration:0.35, ease:"power3.out", immediateRender:false}}, {q:.2f});')
    h = v + key_at(V + "v5.mp3", "mother", d - 0.6)
    c.t(f'tl.fromTo("#th", {{opacity:0, scale:0.2}}, {{opacity:1, scale:1.3, duration:0.35, ease:"back.out(3)"}}, {h:.2f});')
    c.t(f'tl.to("#th", {{scale:1.1, duration:0.3, yoyo:true, repeat:3, ease:"sine.inOut"}}, {h + 0.35:.2f});'); c.sfx("correct", h)
    t = v + d + 0.6
    # 4. your turn: back to the whole tree, mum's brother, 3-2-1, خال; then the two sides side by side
    c.t(f'tl.to("#tq", {{autoAlpha:0, y:30, duration:0.3}}, {t - 0.3:.2f});'); cam(1, 540, 700, t)
    c.t(f'tl.to(["#brand", "#kicker", "#nme"], {{autoAlpha:1, duration:0.3}}, {t + 0.6:.2f});')
    d = clip(c, V + "q1.mp3", t + 0.3)
    c.t(f'tl.to("#nu2 .fc", {{scale:1.15, duration:0.3, yoyo:true, repeat:5, ease:"sine.inOut"}}, {t + 0.6:.2f});')
    for k in range(3): c.inn(f"#to{k}", t + 0.3 + d - 0.6 + 0.12 * k, 30)
    done = count_down(c, "tc", t + 0.3 + d + 0.3)
    reveal(c, "#to1", ["#to0", "#to2"], done)
    c.t(f'tl.to("#nu2q", {{opacity:0, duration:0.1}}, {done:.2f});')
    c.t(f'tl.fromTo("#nu2a", {{opacity:0, scale:2.4}}, {{opacity:1, scale:1, duration:0.2, ease:"power4.in"}}, {done:.2f});'); clip(c, "brag-quiz/sfx/crash.wav", done + 0.18, 0.5)
    d = say_up(c, "", done + 0.3, src=V + "khal.mp3"); t = done + 0.3 + d + 0.1
    d = clip(c, V + "r1.mp3", t)
    c.t(f'tl.to(["#to", "#tc"], {{opacity:0, duration:0.25}}, {t + 0.4:.2f});')
    c.t('tl.set("#ts", {autoAlpha:0}, 0);'); c.t(f'tl.set("#ts", {{autoAlpha:1}}, {t + 0.6:.2f});')
    c.t(f'tl.fromTo("#ts div", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.4, stagger:0.15, ease:"power3.out"}}, {t + 0.6:.2f});')
    c.t(f'tl.to(".fn.m .fc", {{scale:1.1, duration:0.2, yoyo:true, repeat:1, stagger:0.06}}, {t + 0.6:.2f});'); c.sfx("tap", t + 0.6)
    t += d + 0.9
    # 5. the closing ask, heard in full on the end card
    c.out_("#t", t - 0.4); end = clip(c, V + "end.mp3", t)
    body.append(c.end(t, "Tag your khala 👇 and tell her she’s basically your mum 🤍"))
    c.write("\n".join("      " + b for b in body), round(t + end + 0.9, 2))

LADDER_CSS = (
    # one page that moves (MOTION-STYLE rule 6, the owner's reference reel): the rounds sit one under another and the page slides up
    # to the next; a rail on the left keeps the share of people still in the game, its marker dropping a rung each round
    "#view { position:absolute; left:0; right:0; top:170px; height:990px; overflow:hidden; "
    "-webkit-mask-image:linear-gradient(#000 82%, transparent); mask-image:linear-gradient(#000 82%, transparent); }"
    "#page { position:absolute; left:190px; right:40px; top:0; } .blk { position:absolute; left:0; right:0; height:900px; }"
    ".lq { position:absolute; left:0; right:0; top:60px; text-align:center; font-size:62px; font-weight:700; line-height:1.15; color:var(--ink); }"
    ".lq .ar, .lbig .ar { font-family:var(--ar); color:var(--rubric); } .lbig { position:absolute; left:0; right:0; top:230px; text-align:center; font-size:150px; line-height:1.2; }"
    ".blk .cnt { top:470px !important; } .lans { position:absolute; left:50%; top:470px; transform:translateX(-50%); padding:16px 50px; "
    "border-radius:60px; background:var(--card,#fff); border:4px solid rgba(23,38,43,.12); white-space:nowrap; } .lans b { font-size:66px; font-weight:800; color:var(--ink); }"
    ".lans .ar { font-family:var(--ar); font-size:92px; } .lcom { position:absolute; left:0; right:0; top:660px; text-align:center; font-size:44px; font-weight:700; color:var(--verdigris); }"
    "#rail { position:absolute; left:34px; top:230px; width:130px; height:860px; } #rail .trk { position:absolute; left:58px; top:10px; bottom:10px; width:10px; "
    "border-radius:5px; background:rgba(23,38,43,.1); } #rail .fill { position:absolute; left:58px; top:10px; width:10px; height:0; border-radius:5px; background:var(--rubric); }"
    ".rung { position:absolute; left:0; width:126px; text-align:center; font-weight:800; font-size:30px; color:rgba(23,38,43,.3); transform:translateY(-50%); }"
    ".rung i { position:absolute; left:52px; top:50%; width:22px; height:22px; margin-top:-11px; border-radius:50%; background:#efe8d8; border:4px solid rgba(23,38,43,.18); }"
    ".rung span { position:relative; top:-34px; } #mark { position:absolute; left:0; width:126px; transform:translateY(-50%); text-align:center; }"
    "#mark b { display:inline-block; padding:8px 14px; border-radius:30px; background:var(--rubric); color:#fff; font-size:38px; font-weight:800; box-shadow:0 8px 24px rgba(180,50,42,.35); }"
    "#mark small { display:block; font-size:19px; letter-spacing:.12em; font-weight:800; color:var(--rubric); margin-top:6px; }")

def ladder(vid, R, ask, voice={}, kicker="QUIZ · HOW FAR CAN YOU GET?"):
    """The difficulty ladder (owner, 14 Oct 2026). The owner says each line, stitched under the video, so it all sits in the top
    ~1,150 px. One page: each round sits under the last and the page slides up to it; the rail on the left drops its marker a rung
    (the share counts down, a click per 10%); the question, a 3-2-1 with clicks, the answer pops green and Rafiq says it.
    R: (percent, question html, big html or "", answer html, Arabic said, "big" | "ans" (when Rafiq says it), extra line or "")."""
    c = SO.vcomp(vid, kicker); c.bed = True; c.css += LADDER_CSS
    n, H, GAP = len(R), 860, 760
    ry = lambda k: 20 + k * (H - 40) / (n - 1)                    # rung k's height on the rail
    rungs = "".join(f'<div class="rung" id="g{k}" style="top:{ry(k):.0f}px"><i></i><span>{p}%</span></div>' for k, (p, *_ ) in enumerate(R))
    blocks = ""
    for k, (pct, q, big, ans, ar, when, extra) in enumerate(R):
        s = f"l{k}"
        blocks += (f'<div class="blk" id="{s}" style="top:{k * GAP}px"><div class="lq" id="{s}q">{q}</div>' + (f'<div class="lbig" id="{s}b">{big}</div>' if big else "")
                   + cnt(s + "c", 470) + f'<div class="lans" id="{s}a">{ans}</div>' + (f'<div class="lcom" id="{s}x">{extra}</div>' if extra else "") + '</div>')
    body = [f'<div id="view"><div id="page">{blocks}</div></div>',
            f'<div id="rail"><div class="trk"></div><div class="fill" id="fill"></div>{rungs}'
            f'<div id="mark" style="top:{ry(0):.0f}px"><b id="markn">{R[0][0]}%</b><small>STILL IN</small></div></div>']
    t, prev = 0.1, R[0][0]
    for k, (pct, q, big, ans, ar, when, extra) in enumerate(R):
        s = f"l{k}"
        if k:                                                     # the page slides up to the next round, the marker drops a rung
            c.t(f'tl.to("#page", {{y:{-k * GAP}, duration:0.6, ease:"power3.inOut"}}, {t - 0.45:.2f});')
            c.t(f'tl.fromTo("#page", {{filter:"blur(0px)"}}, {{filter:"blur(6px)", duration:0.25, yoyo:true, repeat:1, ease:"power1.in", immediateRender:false}}, {t - 0.4:.2f});')
            clip(c, "brag-quiz/sfx/ref/short-swoosh.wav", t - 0.45, 0.35)
            c.t(f'tl.to("#mark", {{top:{ry(k):.0f}, duration:0.7, ease:"back.out(1.4)"}}, {t + 0.1:.2f});')
            c.t(f'tl.to("#fill", {{height:{ry(k) - 10:.0f}, duration:0.7, ease:"power2.out"}}, {t + 0.1:.2f});')
            c.t(f'(() => {{ const o = {{v:{prev}}}; tl.to(o, {{v:{pct}, duration:0.7, ease:"power2.out", onUpdate:() => {{ document.getElementById("markn").textContent = Math.round(o.v) + "%"; }}}}, {t + 0.1:.2f}); }})();')
            steps = max(1, round((prev - pct) / 10))              # a click per 10% the share drops
            for i in range(steps): clip(c, "brag-quiz/sfx/ref/click.wav", t + 0.1 + 0.6 * (i + 1) / steps, 0.6)
            c.t(f'tl.fromTo("#mark b", {{scale:1}}, {{scale:1.18, duration:0.14, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {t + 0.8:.2f});')
            c.t(f'tl.to("#g{k - 1}", {{opacity:0.45, duration:0.3}}, {t + 0.1:.2f});')
            c.t(f'tl.fromTo("#{s}q", {{opacity:0, y:40, filter:"blur(10px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.4, ease:"expo.out"}}, {t + 0.2:.2f});')
            if big: SO.bigin(c, f"#{s}b", t + 0.5)
        if when == "big": say_up(c, ar, t + 1.2, src=voice.get(ar))
        if extra: c.inn(f"#{s}x", t + 1.0)
        done = count_down(c, f"{s}c", t + 3.2)
        c.t(f'tl.fromTo("#{s}a", {{opacity:0, scale:0.6}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(1.8)"}}, {done:.2f});')
        reveal(c, f"#{s}a", [], done + 0.05); c.sfx("correct", done)
        d = say_up(c, ar, done + 0.3, src=voice.get(ar)) if when == "ans" else 0
        t = done + 0.3 + d + 1.5; prev = pct
    c.out_("#view", t); c.out_("#rail", t); t += 0.4
    body.append(c.end(t, ask))
    c.write("\n".join("      " + b for b in body), round(t + 2.9, 2))

def l1():
    """The difficulty ladder #1 (owner, 14 Oct 2026), ordered by the Kelly list's CEFR levels for Arabic (Kilgarriff et al. 2014;
    ssharoff.github.io/kelly): far, near A1 → cold A2 → hot, fat, thin B1 → the final boss خائِن "traitor" C1, the opposite of
    أَمِين "trustworthy" (A2). Meanings: vocab-data.js; حارّ, أَمِين and خائِن spoken for this video (brag-quiz/voice/ladder-lines.json)."""
    A = lambda w: f'<span class="ar" lang="ar">{w}</span>'
    V = "brag-quiz/voice/ladder/"
    ladder("l1-ladder", [
        (90, "What does this mean?", A("بَعِيد"), "<b>far</b>", "بَعِيد", "big", ""),
        (80, f"What’s the opposite of {A('بَعِيد')} (far)?", "", f"<b>{A('قَرِيب')}</b> &nbsp;<b>near</b>", "قَرِيب", "ans", ""),
        (50, "How do you say <b>“cold”</b> in Arabic?", "", f"<b>{A('بارِد')}</b>", "بارِد", "ans", ""),
        (30, f"And the opposite of {A('بارِد')} (cold)?", "", f"<b>{A('حارّ')}</b> &nbsp;<b>hot</b>", "حارّ", "ans", ""),
        (20, "How do you say <b>“fat”</b> in Arabic?", "", f"<b>{A('سَمِين')}</b>", "سَمِين", "ans", "Got this far? Comment below 👇"),
        (10, f"What’s the opposite of {A('سَمِين')} (fat)?", "", f"<b>{A('نَحِيف')}</b> &nbsp;<b>thin</b>", "نَحِيف", "ans", ""),
        (5, f"The final boss 😈 What’s the opposite of {A('أَمِين')} (trustworthy)?", "", f"<b>{A('خائِن')}</b> &nbsp;<b>a traitor</b>", "خائِن", "ans", ""),
    ], "How far did you get? Comment your score 👇",
           voice={"حارّ": V + "har.mp3", "أَمِين": V + "amin.mp3", "خائِن": V + "khain.mp3"})

def l2():
    """The difficulty ladder #2, Jumuʿah edition (owner, 23 Oct 2026; he films himself saying each line, 3 s to answer, stitched under
    it): غُسْل ghusl 90% → جَماعَة congregation 70% → عِطْر perfume 45% → لِباس clothes 20% → the final boss أَنْصِتْ "be quiet and listen!" 1%
    (the khutbah hadith, al-Bukhārī 934). The percentages are a game device, not data. Spoken: brag-quiz/voice/ladder2-lines.json."""
    A = lambda w: f'<span class="ar" lang="ar">{w}</span>'
    V = "brag-quiz/voice/ladder2/"
    ladder("l2-jumuah", [
        (90, "What does this mean?", A("غُسْل"), "<b>a full bath</b>", "غُسْل", "ans", ""),
        (70, "What does this mean?", A("جَماعَة"), "<b>congregation</b>", "جَماعَة", "ans", ""),
        (45, "What does this mean?", A("عِطْر"), "<b>perfume</b>", "عِطْر", "ans", ""),
        (20, "What does this mean?", A("لِباس"), "<b>clothes</b>", "لِباس", "ans", "Got this far? Comment below 👇"),
        (1, "The final boss 😈 What does this mean?", A("أَنْصِتْ"), "<b>Be quiet and listen!</b>", "أَنْصِتْ", "ans", ""),
    ], "How far did you get? Comment your score 👇 Send this to who you’re going to Jumuʿah with 🤍",
           voice={"غُسْل": V + "ghusl.mp3", "جَماعَة": V + "jamaa.mp3", "عِطْر": V + "itr.mp3", "لِباس": V + "libas.mp3", "أَنْصِتْ": V + "ansit.mp3"},
           kicker="QUIZ · JUMUʿAH EDITION")

# ---------------------------------------------------------------- the story of a word (owner 26 Oct 2026, #296): a light pastel page,
# hand-drawn doodles behind it, in the Callum standard (spoken hook, every move on its word, captions word by word, a 3-2-1, Rafiq for the Arabic)
PASTEL = [(-260, -160, 820, "#cfe8dc"), (560, 200, 720, "#f9dcc6"), (-220, 860, 760, "#f7e8b8"), (600, 1180, 820, "#f5d3cf"), (40, 1600, 720, "#d5e8ec")]
DCOL = {"sage": ("#6aa893", "#dcefe6"), "peach": ("#e09868", "#fbe3d2"), "butter": ("#d1a63c", "#f8ebc4"), "blush": ("#d6807b", "#f7d9d6"),
        "sky": ("#6fa5b5", "#d9ebf0"), "ink": ("#2b3a3e", "#fbf7ef"), "red": ("#b4322a", "none")}
DOODLE = {  # hand-drawn shapes in a 100 x 100 box: [(path, filled)]
    "bone": [("M30 43 H70 A10 10 0 1 1 80 50 A10 10 0 1 1 70 57 H30 A10 10 0 1 1 20 50 A10 10 0 1 1 30 43 Z", 1)],
    "boneL": [("M50 43 H30 A10 10 0 1 0 20 50 A10 10 0 1 0 30 57 H50 L47 54 L52 51 L47 47 Z", 1)],
    "boneR": [("M50 43 H70 A10 10 0 1 1 80 50 A10 10 0 1 1 70 57 H50 L47 54 L52 51 L47 47 Z", 1)],
    "cup": [("M22 40 H70 V58 C70 74 60 82 46 82 C32 82 22 74 22 58 Z", 1), ("M70 46 C84 46 84 64 70 64", 0), ("M14 88 H78", 0),
            ("M36 32 C30 24 42 20 36 12", 0), ("M52 32 C46 24 58 20 52 12", 0)],
    "bean": [("M50 18 C72 18 82 40 78 58 C74 78 56 86 44 82 C24 76 18 54 24 38 C28 26 38 18 50 18 Z", 1), ("M52 22 C40 40 62 58 46 80", 0)],
    "dallah": [("M40 30 C30 40 30 62 36 78 H64 C70 62 70 40 60 30 Z", 1), ("M44 30 C44 22 56 22 56 30", 0), ("M50 22 V14 M46 14 H54", 0),
               ("M36 46 C24 42 18 32 10 24", 0), ("M64 38 C80 40 82 64 66 70", 0), ("M32 84 H68", 0)],
    "moon": [("M60 14 A36 36 0 1 0 86 70 A28 28 0 1 1 60 14 Z", 1)],
    "star": [("M50 12 L57 43 L88 50 L57 57 L50 88 L43 57 L12 50 L43 43 Z", 1)],
    "lantern": [("M50 6 V14 M40 14 H60", 0), ("M34 26 L40 14 H60 L66 26 Z", 1), ("M34 26 L28 66 H72 L66 26 Z", 1), ("M28 66 L38 82 H62 L72 66", 0), ("M50 26 V66", 0)],
    "book": [("M50 26 C38 18 22 18 12 24 V80 C22 74 38 74 50 82 C62 74 78 74 88 80 V24 C78 18 62 18 50 26 Z", 1), ("M50 26 V82", 0),
             ("M20 36 C28 33 36 33 42 36 M20 48 C28 45 36 45 42 48 M58 36 C64 33 72 33 80 36 M58 48 C64 45 72 45 80 48", 0)],
    "dome": [("M18 92 V62 H76 V92 Z", 1), ("M24 62 C24 34 70 34 70 62", 1), ("M47 38 V24 M43 24 H51", 0), ("M86 92 V40 M82 40 H90 M86 40 V30", 0)],
    "palm": [("M52 92 C50 72 48 52 52 32", 0), ("M52 32 C40 20 26 22 16 30 M52 32 C46 18 50 10 60 8 M52 32 C64 20 78 22 86 32 M52 32 C66 30 74 40 76 52", 0)],
    "compass": [("M50 12 V22 M50 22 L30 88 M50 22 L70 88 M38 60 H62", 0), ("M46 22 A4 4 0 1 0 54 22 A4 4 0 1 0 46 22", 1)],
    "phone": [("M32 8 H68 A8 8 0 0 1 76 16 V84 A8 8 0 0 1 68 92 H32 A8 8 0 0 1 24 84 V16 A8 8 0 0 1 32 8 Z", 1), ("M44 84 H56", 0)],
    "plate": [("M28 52 A22 22 0 1 0 72 52 A22 22 0 1 0 28 52 Z", 1), ("M38 52 A12 12 0 1 0 62 52 A12 12 0 1 0 38 52", 0),
              ("M14 30 V76 M10 30 V42 C10 47 18 47 18 42 V30", 0), ("M88 30 C80 40 80 52 88 55 V76", 0)],
    "cross": [("M18 22 L82 82 M82 22 L18 82", 0)],
    "pin": [("M50 88 C40 68 26 58 26 40 A24 24 0 1 1 74 40 C74 58 60 68 50 88 Z", 1), ("M42 40 A8 8 0 1 0 58 40 A8 8 0 1 0 42 40", 0)],
    "arrow": [("M50 8 V82 M32 64 L50 86 L68 64", 0)],
}
STORY_CSS = (
    "#root { background:#fbf7ef; } #glow { display:none; } #pastel, #doodles { position:absolute; inset:0; overflow:hidden; pointer-events:none; }"
    "#pastel { z-index:0; } #doodles { z-index:1; } .sec { z-index:2; } #brand, #kicker, #end, #pflash { z-index:3; }"
    "#pastel i { position:absolute; border-radius:50%; filter:blur(70px); opacity:.85; } .dd { position:absolute; overflow:visible; }"
    ".dd path { stroke-linecap:round; stroke-linejoin:round; } .drw { visibility:hidden; } .drw .dr { stroke-dasharray:1; stroke-dashoffset:1; fill-opacity:0; }"
    ".tdd { position:absolute; font-family:\"Fredoka\", var(--la); font-weight:600; white-space:nowrap; }"
    ".cc { position:absolute; left:100px; right:100px; top:1300px; text-align:center; font-family:\"Fredoka\", var(--la); font-weight:600; font-size:58px; "
    "line-height:1.16; color:var(--ink); } .cc.ccs { font-size:48px; } .cw { display:inline-block; opacity:0; } .cw.r { color:var(--rubric); } "
    ".cw.g { color:var(--verdigris); } .cw.y { color:#8f6f1d; }"
    ".bigw { position:absolute; left:0; right:0; text-align:center; font-family:var(--ar); font-weight:700; line-height:1.4; color:var(--ink); }"
    ".bigw .pr { color:var(--rubric); } .bigw .pv { color:var(--verdigris); }"
    ".sp { position:absolute; padding:12px 34px 16px; border-radius:46px; background:#fffdf8; border:4px solid rgba(23,38,43,.12); "
    "font-family:\"Fredoka\", var(--la); font-weight:600; font-size:50px; color:var(--ink); white-space:nowrap; box-shadow:0 14px 28px -18px rgba(23,38,43,.45); }"
    ".sp.mid { left:0; right:0; margin:0 auto; width:max-content; } .sp .ar { font-family:var(--ar); font-weight:700; } .sp .pr { color:var(--rubric); } .sp .pv { color:var(--verdigris); }"
    ".yr { position:absolute; left:0; right:0; text-align:center; font-family:\"Fredoka\", var(--la); font-weight:700; color:#8f6f1d; line-height:1; }"
    ".yr small { display:block; font-size:30px; letter-spacing:.2em; color:var(--ink-soft); margin-bottom:8px; } .yr b { font-size:190px; }"
    ".slamw { position:absolute; left:40px; right:40px; text-align:center; font-family:\"Fredoka\", var(--la); font-weight:700; font-size:120px; line-height:1.05; color:var(--ink); }"
    ".slamw em { font-style:normal; color:var(--rubric); } .opts.col { flex-direction:column; gap:18px; left:150px; right:150px; } .opts.col .op2 { flex:none; height:112px; }"
    ".burst { position:absolute; width:0; height:0; } .burst i { position:absolute; left:-11px; top:-11px; width:22px; height:22px; border-radius:50%; background:#E9B949; opacity:0; }"
    ".burst i:nth-child(odd) { background:#e09868; width:16px; height:16px; left:-8px; top:-8px; }"
    "#pflash { position:absolute; inset:0; background:#fffaf0; opacity:0; pointer-events:none; }")

def doodle(shape, x, y, size, col, did="", draw=False, sw=5, rot=0):
    """One of DOODLE's shapes, drawn by hand: a pastel line and fill, with a second faint line just off it (a sketch). draw: it starts
    undrawn and draw_on() draws it."""
    s, f = DCOL[col]; kl = ' class="dr"' if draw else ""; w = sw * 100 / size           # sw: the line's width on screen, in px
    one = lambda dx, op: "".join(f'<path{kl} d="{d}" pathLength="1" fill="{f if fill else "none"}" stroke="{s}" stroke-width="{w:.2f}" '
                                 f'opacity="{op}" transform="translate({dx:.2f},{dx * .7:.2f})"/>' for d, fill in DOODLE[shape])
    return (f'<svg class="dd{" drw" if draw else ""}"{f" id={chr(34)}{did}{chr(34)}" if did else ""} viewBox="0 0 100 100" '
            f'style="left:{x}px;top:{y}px;width:{size}px;height:{size}px;transform:rotate({rot}deg)">{one(1.6 * 100 / size, .3)}{one(0, 1)}</svg>')

def pastel(c, body, items):
    """The pastel page: soft blobs of colour that drift, and doodles round the edges that bob (items: (shape or "txt:…", x, y, size, rotation,
    colour)). Returns finish(total), which adds their movement once the length is known."""
    c.css += STORY_CSS
    blobs = "".join(f'<i style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;background:{col}"></i>' for x, y, s, col in PASTEL)
    dd = "".join(f'<div class="tdd" data-layout-ignore id="dd{k}" style="left:{x}px;top:{y}px;font-size:{s}px;color:{DCOL[col][0]}">{sh[4:]}</div>' if sh.startswith("txt:")
                 else doodle(sh, x, y, s, col, f"dd{k}") for k, (sh, x, y, s, r, col) in enumerate(items))
    body.insert(0, f'<div id="pastel" data-layout-ignore>{blobs}</div><div id="doodles" data-layout-ignore>{dd.replace("<svg class=", "<svg data-layout-ignore class=")}</div>')
    def finish(total):
        c.t(f'tl.fromTo("#pastel i", {{x:0, y:0}}, {{x:(i) => [60, -50, 40, -60, 50][i], y:(i) => [40, 60, -50, 30, -40][i], duration:{total:.2f}, ease:"none"}}, 0);')
        for k, (sh, x, y, s, r, col) in enumerate(items):
            p = 2.2 + 0.37 * (k % 4)
            c.t(f'tl.fromTo("#dd{k}", {{y:0, rotation:{r}}}, {{y:{-14 if k % 2 else 12}, rotation:{r + (4 if k % 2 else -4)}, duration:{p:.2f}, '
                f'yoyo:true, repeat:{int(total / p) + 1}, ease:"sine.inOut"}}, 0);')
    return finish

def cap(c, cid, mp3, at, keys=(), cls=""):
    """Callum's line as a caption, each word coming in as he says it; keys: (lowercase piece of a word, "r" | "g" | "y") to colour it."""
    W = words_at(mp3)
    col = lambda w: next((" " + k for p, k in keys if p in w.lower()), "")
    for i, (w, s) in enumerate(W):
        c.t(f'tl.fromTo("#{cid}w{i}", {{opacity:0, y:18, filter:"blur(8px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.22, ease:"power3.out"}}, {at + s - 0.03:.2f});')
    return f'<div class="cc {cls}" id="{cid}">' + " ".join(f'<span class="cw{col(w)}" id="{cid}w{i}">{e(w)}</span>' for i, (w, s) in enumerate(W)) + '</div>'

def cap_out(c, cid, at): c.t(f'tl.to("#{cid}", {{opacity:0, y:-18, duration:0.25, ease:"power2.in"}}, {at:.2f});')
def key_last(mp3, key, fallback):
    return next((s for w, s in reversed(words_at(mp3)) if key in w.lower()), fallback)
def zoom_in(c, sel, at):
    c.t(f'tl.fromTo("{sel}", {{opacity:0, scale:1.6, filter:"blur(14px)"}}, {{opacity:1, scale:1, filter:"blur(0px)", duration:0.38, ease:"expo.out"}}, {at - 0.05:.2f});')
def pop(c, sel, at, tap=True):
    c.t(f'tl.fromTo("{sel}", {{opacity:0, scale:0.3}}, {{opacity:1, scale:1, duration:0.42, ease:"back.out(2.2)"}}, {at:.2f});')
    if tap: c.sfx("tap", at)
def draw_on(c, did, at, d=0.8):
    c.t(f'tl.set("#{did}", {{visibility:"visible"}}, {at:.2f});')         # hidden till then: an undrawn round-capped line still shows a dot
    c.t(f'tl.to("#{did} .dr", {{strokeDashoffset:0, duration:{d}, ease:"power2.inOut", stagger:{d / 5:.2f}}}, {at:.2f});')
    c.t(f'tl.to("#{did} .dr", {{fillOpacity:1, duration:0.4}}, {at + d * 0.7:.2f});')
    clip(c, "brag-quiz/sfx/soft/scratch.wav", at, 0.18)
def burst(c, bid, x, y, at, n=8):
    c.t(f'tl.fromTo("#{bid} i", {{opacity:1, x:0, y:0, scale:1}}, {{opacity:0, x:(i) => Math.cos(i * {6.283 / n:.3f}) * 170, y:(i) => Math.sin(i * {6.283 / n:.3f}) * 170, '
        f'scale:0.4, duration:0.6, ease:"expo.out", immediateRender:false}}, {at:.2f});')
    return f'<div class="burst" id="{bid}" style="left:{x}px;top:{y}px">' + "<i></i>" * n + '</div>'
def year(c, cid, frm, to, at, d, ticks=8, suffix=""):
    """A year that rolls up, a click on each step of the way (they bunch at the start: it slows as it lands)."""
    c.t(f'(() => {{ const o = {{v:{frm}}}, el = document.getElementById("{cid}"); tl.fromTo(o, {{v:{frm}}}, {{v:{to}, duration:{d:.2f}, ease:"power2.out", '
        f'immediateRender:false, onUpdate:() => {{ el.textContent = Math.round(o.v) + "{suffix}"; }}}}, {at:.2f}); }})();')
    for k in range(1, ticks + 1): clip(c, "brag-quiz/sfx/ref/click.wav", at + d * (1 - (1 - k / ticks) ** 0.5), 0.45)
def slam(c, sel, sec, at, snd="brag-quiz/sfx/crash.wav"):
    c.t(f'tl.fromTo("{sel}", {{opacity:0, scale:2.6}}, {{opacity:1, scale:1, duration:0.2, ease:"power4.in"}}, {at - 0.2:.2f});')
    c.t(f'tl.fromTo("#pflash", {{opacity:0.8}}, {{opacity:0, duration:0.3, ease:"power2.out", immediateRender:false}}, {at:.2f});')
    c.t(f'tl.to("#{sec}", {{keyframes:[{{x:-26, y:16, duration:0.04}}, {{x:22, y:-12, duration:0.04}}, {{x:-12, y:8, duration:0.05}}, {{x:0, y:0, duration:0.06}}]}}, {at:.2f});')
    clip(c, snd, at - 0.02, 0.7); c.sfx("correct", at + 0.1)

ALG_DOODLES = [("txt:x + 2 = 5", 50, 1560, 54, -8, "sage"), ("txt:√49 = 7", 780, 1540, 52, 9, "peach"), ("star", 120, 540, 64, 0, "butter"),
               ("txt:÷", 960, 560, 84, 0, "blush"), ("txt:×", 50, 1120, 80, 0, "sky"), ("star", 930, 1180, 56, 0, "sage"), ("book", 850, 1400, 130, -10, "peach"),
               ("compass", 915, 1200, 110, 12, "sky"), ("bone", 360, 1700, 170, -16, "butter"), ("txt:2x = 10", 720, 1760, 50, 6, "blush")]
JABR = [("الْ", ""), ("جَ", "r"), ("بْ", "r"), ("ر", "r")]
WAJBURNI = [("وَا", ""), ("جْ", "r"), ("بُ", "r"), ("رْ", "r"), ("نِي", "")]

def h1():
    """The story of a word #1 (owner 26 Oct 2026, #296: "the history of a word… a light background with a pastel feel, drawings"): ALGEBRA.
    Hook "Algebra is named after an Arabic word for setting broken BONES!" (the bone at the bottom snaps on "broken"); الْجَبْر "putting broken
    pieces back together" (the bone is set); al-Khwārizmī's book, Baghdad, about 820 (x² + 10x = 39 is his own example); Europe turned al-jabr
    into "algebra" and his name into "algorithm"; your turn: وَاجْبُرْنِي, from the duʿāʾ between the two sujood (al-Tirmidhī 284, Ibn ʿAbbās),
    3-2-1, "and MEND me". Sources: Wiktionary and American Heritage, "algebra" (al-jabr "reunion of broken parts", bone-setting).
    Voices: brag-quiz/voice/algebra-lines.json (b1, b4, b5 and t1 were cut for length; b3s and t1s replace b3 and t1)."""
    V = "brag-quiz/voice/algebra/"
    c = SO.vcomp("h1-algebra", "THE STORY OF A WORD"); c.bed = True; body = []; serif(c); c.css += GROW_CSS
    finish = pastel(c, body, ALG_DOODLES)
    def anim(c, at, d):                                  # "broken": the bone snaps in two
        b = at(9) + 0.15
        c.t(f'tl.to("#hbL", {{x:-46, y:10, rotation:-16, duration:0.25, ease:"back.out(3)"}}, {b:.2f});')
        c.t(f'tl.to("#hbR", {{x:46, y:10, rotation:16, duration:0.25, ease:"back.out(3)"}}, {b:.2f});')
        clip(c, "brag-quiz/sfx/soft/thump.wav", b, 0.5); c.sfx("tap", b)
    words = "Algebra is named after an Arabic word for setting broken BONES!".split()
    c.slam_x = 0
    hb = doodle("boneL", 290, 1250, 500, "butter", "hbL", sw=7) + doodle("boneR", 290, 1250, 500, "butter", "hbR", sw=7)
    t = hook_in(c, body, (words, {0: "red", 5: "circle", 10: "loud"}, V + "h1c.mp3"), bg=(hb, anim))   # h1c: no shouting (owner, 26 Oct)
    c.css += "#hw10 { display:block; width:max-content; margin:0 auto; } #hook .hookline { top:560px; }"
    # 1. الْجَبْر: putting broken pieces back together, and the bone is set
    B = V + "b1b.mp3"
    whip_in(c, "s1", t); dj = say_up(c, "", t + 0.15, src=V + "jabr.mp3"); zoom_in(c, "#s1w", t + 0.15); pop(c, "#s1t", t + 0.15 + dj, False)
    t3 = t + 0.15 + dj + 0.25; db = clip(c, B, t3); h = cap(c, "s1b", B, t3, (("broken", "r"), ("together", "g"), ("bone", "r")))
    br = t3 + key_at(B, "broken", 0.3); draw_on(c, "s1L", br); draw_on(c, "s1R", br + 0.1)
    tog = t3 + key_at(B, "together", 2.5)
    for k in "LR": c.t(f'tl.to("#s1{k}", {{x:0, rotation:0, duration:0.3, ease:"back.out(2)"}}, {tog:.2f});')
    bu = burst(c, "s1x", 540, 950, tog + 0.25); clip(c, "brag-quiz/sfx/ref/click.wav", tog + 0.25, 0.9)
    c.t(f'tl.fromTo("#s1bone", {{scale:1}}, {{scale:1.1, duration:0.16, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {t3 + key_at(B, "bone.", 4.0):.2f});')
    c.t('tl.set("#s1L", {x:-60, rotation:-14}, 0); tl.set("#s1R", {x:60, rotation:14}, 0);')
    body.append(f'<div class="sec" id="s1"><div class="bigw" id="s1w" style="top:330px;font-size:200px">{word(JABR)}</div>'
                f'<div class="sp mid" id="s1t" style="top:640px">al-jabr</div><div id="s1bone" style="position:absolute;left:290px;top:700px;width:500px;height:500px">'
                + doodle("boneL", 0, 0, 500, "butter", "s1L", True, 7) + doodle("boneR", 0, 0, 500, "butter", "s1R", True, 7) + f'</div>{bu}{h}</div>')
    t = whip_out(c, "s1", t3 + db + 0.35)
    # 2. Baghdad, about 820: al-Khwārizmī's book (the year rolls up; the city and the book are drawn; his own equation is written out)
    B = V + "b2.mp3"; whip_in(c, "s2", t); d = clip(c, B, t + 0.1); s = t + 0.1
    h = cap(c, "s2a", B, s, (("820", "y"), ("baghdad", "g"), ("khwarizmi", "g"), ("al-jabr", "r")))
    year(c, "s2y", 0, 820, s + key_at(B, "year", 0.4), max(0.6, key_at(B, "820", 0.8) - key_at(B, "year", 0.4) + 0.5))
    bg = s + key_at(B, "baghdad", 2.0); draw_on(c, "s2d", bg - 0.1); draw_on(c, "s2p", bg); pop(c, "#s2bl", bg + 0.2)
    pop(c, "#s2k", s + key_at(B, "khwarizmi", 2.9)); bk = s + key_at(B, "book", 4.1); draw_on(c, "s2b", bk - 0.1)
    eq = s + key_at(B, "equations", 5.1)
    c.t(f'tl.fromTo("#s2e", {{opacity:1, clipPath:"inset(0 100% 0 0)"}}, {{opacity:1, clipPath:"inset(0 0% 0 0)", duration:0.7, ease:"steps(13)"}}, {eq - 0.3:.2f});')
    for k in range(5): clip(c, "brag-quiz/sfx/soft/type.wav", eq - 0.3 + k * 0.14, 0.3)
    pop(c, "#s2j", s + key_at(B, "al-jabr", 5.9))
    body.append('<div class="sec" id="s2"><div class="yr" style="top:250px"><small>AROUND THE YEAR</small><b id="s2y">0</b></div>'
                + doodle("dome", 70, 560, 380, "sage", "s2d", True, 6) + doodle("palm", 300, 600, 240, "sage", "s2p", True, 6)
                + '<div class="sp" id="s2bl" style="left:120px;top:960px">Baghdad</div>'
                + doodle("book", 590, 560, 360, "peach", "s2b", True, 6) + '<div class="sp" id="s2j" style="left:660px;top:690px;font-size:44px;color:var(--rubric)">al-jabr</div>'
                + '<div class="tdd" id="s2e" style="left:600px;top:930px;font-size:56px;color:var(--ink);opacity:0">x² + 10x = 39</div>'
                + f'<div class="sp mid" id="s2k" style="top:1110px">al-Khwarizmi</div>{h}</div>')
    t = whip_out(c, "s2", s + d + 0.4)
    # 3. Europe: al-jabr → ALGEBRA, and al-Khwārizmī → ALGORITHM
    B = V + "b3s.mp3"; whip_in(c, "s3", t); d = clip(c, B, t + 0.1); s = t + 0.1
    h = cap(c, "s3a", B, s, (("algebra", "y"), ("khwarizmi", "g"), ("algorithm", "g")))
    pop(c, "#s3a1", s + 0.15); c.inn("#s3r1", s + key_at(B, "turned", 0.4))
    al = s + key_at(B, "algebra", 1.4); zoom_in(c, "#s3a3", al); bu = burst(c, "s3x", 540, 560, al + 0.1); c.sfx("correct", al)
    pop(c, "#s3k", s + key_at(B, "khwarizmi", 2.6)); c.inn("#s3r2", s + key_at(B, "name", 3.3))
    ag = s + key_at(B, "algorithm", 4.0); zoom_in(c, "#s3w", ag); draw_on(c, "s3p", ag - 0.3, 0.6)
    body.append('<div class="sec" id="s3"><div class="sp mid" id="s3a1" style="top:290px"><span class="ar">' + word(JABR) + '</span></div>'
                + doodle("arrow", 490, 400, 100, "ink", "s3r1", sw=6) + '<div class="slamw" id="s3a3" style="top:500px;color:#8f6f1d">ALGEBRA</div>'
                + '<div class="sp mid" id="s3k" style="top:700px">al-Khwarizmi</div>' + doodle("arrow", 490, 810, 100, "ink", "s3r2", sw=6)
                + '<div class="slamw" id="s3w" style="top:910px;font-size:110px;color:var(--verdigris)">ALGORITHM</div>'
                + doodle("phone", 820, 640, 170, "sky", "s3p", True, 6) + f'{bu}{h}</div>')
    t = whip_out(c, "s3", s + d + 0.5)
    # 4. your turn: وَاجْبُرْنِي, from the duʿāʾ between the two sujood; 3-2-1; "and MEND me"; the source
    B, Q, S = V + "t1s.mp3", V + "t1b.mp3", V + "b6.mp3"
    whip_in(c, "s5", t); d = clip(c, B, t + 0.1); h = cap(c, "s5a", B, t + 0.1, (("turn", "r"), ("sujood", "g")), "ccs")
    t2 = t + 0.1 + d + 0.05; dw = say_up(c, "", t2, src=V + "wajburni.mp3"); zoom_in(c, "#s5w", t2)
    t3 = t2 + dw + 0.15; dq = clip(c, Q, t3); h2 = cap(c, "s5b", Q, t3, (("mean", "r"),))
    for i in range(3): c.inn(f"#qo{i}", t3 + 0.1 + i * 0.12, 30)
    done = count_down(c, "qc", t3 + dq + 0.3)
    reveal(c, "#qo1", ["#qo0", "#qo2"], done)
    d6 = clip(c, S, done); hit = done + key_at(S, "mend", 0.2) + 0.05
    c.t(f'tl.to(["#qo0", "#qo2", "#s5b"], {{opacity:0, duration:0.25}}, {hit - 0.3:.2f});')
    slam(c, "#s5s", "s5", hit); bu = burst(c, "s5x", 540, 1290, hit + 0.05)
    c.t(f'tl.to("#qo", {{opacity:0, y:30, duration:0.3}}, {hit + 1.2:.2f});')
    c.t(f'tl.fromTo("#s5q", {{opacity:0, y:40, scale:0.96}}, {{opacity:1, y:0, scale:1, duration:0.45, ease:"power3.out"}}, {hit + 1.4:.2f});')
    opts = '<div class="opts col" id="qo" style="top:800px">' + "".join(f'<div class="op2" id="qo{i}"><b>{o}</b></div>' for i, o in enumerate(["and forgive me", "and mend me", "and guide me"])) + '</div>'
    body.append(f'<div class="sec" id="s5">{h}<div class="bigw" id="s5w" style="top:430px;font-size:170px">{word(WAJBURNI)}</div>{h2}'
                f'{opts}{cnt("qc", 1230)}<div class="slamw" id="s5s" style="top:1240px;font-size:104px">and <em>MEND</em> me</div>{bu}'
                '<div class="quote" id="s5q" style="top:820px"><q style="font-size:50px">O Allah, forgive me, have mercy on me, mend me, guide me and provide for me.</q>'
                '<small>between the two sujood · al-Tirmidhī 284</small></div></div>')
    c.css += "#s5a { top:270px; } #s5b { top:720px; }"
    t = done + d6 + 1.2
    # the closing ask, heard in full on the end card
    c.out_("#s5", t - 0.4); end = clip(c, V + "end.mp3", t)
    body.append('<div id="pflash"></div>' + c.end(t, "What do you say between the two sujood? Comment below 👇"))
    total = round(t + end + 0.9, 2); finish(total)
    c.write("\n".join("      " + b for b in body), total)

COF_DOODLES = [("cup", 30, 1380, 140, -10, "peach"), ("bean", 900, 1300, 100, 25, "butter"), ("moon", 60, 600, 110, -12, "sky"), ("star", 940, 620, 60, 0, "sage"),
               ("bean", 50, 1150, 90, -30, "peach"), ("star", 140, 900, 50, 0, "butter"), ("dallah", 850, 1420, 160, 8, "sage"), ("lantern", 60, 1640, 130, 6, "blush"),
               ("bean", 720, 1760, 100, 60, "blush")]
QAHWA = [("قَ", "r"), ("هْ", "r"), ("وَ", "r"), ("ة", "")]
MAQHA = [("مَ", "v"), ("قْ", "r"), ("هى", "r")]
ROUTE = [("Yemen", 720, 1120, "", 770), ("Istanbul · kahve", 600, 790, "kahve", 650), ("Dutch · koffie", 400, 570, "koffie", 450),
         ("English · coffee", 220, 450, "coffee.", 270)]   # (label, x, y, the word it's reached on, label left)

def h2():
    """The story of a word #2 (owner 26 Oct 2026, #296): COFFEE. Hook "The Arabic word for coffee used to mean WINE!"; قَهْوَة (the app's
    recording): old Arabic dictionaries say it meant wine, "so named because it puts the drinker off his food" (Hattox, Coffee and
    Coffeehouses, quoting the lexicographers; modern scholars doubt it, so it's said as the dictionaries' view); the Sufis of Yemen, mid-1400s,
    drank coffee to stay awake for their night devotions (the earliest credible evidence of coffee drinking) and the name moved over;
    Istanbul (kahve), the Dutch (koffie), English "coffee" by 1582 (Wikipedia, Coffee and History of coffee); your turn: مَقْهى,
    masjid's مَـ "the place of", 3-2-1, a CAFÉ. Voices: brag-quiz/voice/coffee-lines.json (b1 cut; b2s and b3s replace b2 and b3, for length)."""
    V = "brag-quiz/voice/coffee/"
    c = SO.vcomp("h2-coffee", "THE STORY OF A WORD"); c.bed = True; body = []; c.css += GROW_CSS
    finish = pastel(c, body, COF_DOODLES)
    def anim(c, at, d):                                  # "coffee": the cup steams; WINE: it wobbles
        c.t(f'tl.set("#hcup .dr", {{visibility:"visible"}}, {at(4) - 0.1:.2f});')
        c.t(f'tl.to("#hcup .dr", {{strokeDashoffset:0, duration:0.6, ease:"power2.out", stagger:0.08}}, {at(4) - 0.1:.2f});')
        c.t(f'tl.fromTo("#hcup", {{rotation:0}}, {{rotation:7, duration:0.08, yoyo:true, repeat:5, ease:"sine.inOut", immediateRender:false}}, {at(8) + 0.12:.2f});')
    words = "The Arabic word for coffee used to mean WINE!".split()
    c.slam_x = 0
    hc = doodle("cup", 330, 1240, 420, "peach", "hcup", sw=7)          # the steam is undrawn until "coffee"
    hc = hc.replace('<path d="M36 32', '<path class="dr" style="stroke-dasharray:1;stroke-dashoffset:1;visibility:hidden" d="M36 32').replace('<path d="M52 32', '<path class="dr" style="stroke-dasharray:1;stroke-dashoffset:1;visibility:hidden" d="M52 32')
    t = hook_in(c, body, (words, {1: "circle", 4: "red", 8: "loud"}, V + "h1c.mp3"), bg=(hc, anim))   # h1c: no shouting (owner, 26 Oct)
    c.css += "#hw8 { display:block; width:max-content; margin:0 auto; } #hook .hookline { top:560px; }"
    # 1. قَهْوَة: old dictionaries say it meant wine, because it puts you off your food
    B = V + "b1b.mp3"
    whip_in(c, "s1", t); dq = say_up(c, "قَهْوَة", t + 0.15); zoom_in(c, "#s1w", t + 0.15); pop(c, "#s1t", t + 0.15 + dq, False)
    t3 = t + 0.15 + dq + 0.25; db = clip(c, B, t3); h = cap(c, "s1b", B, t3, (("wine", "r"), ("dictionaries", "g"), ("food", "g")))
    draw_on(c, "s1d", t3 + key_at(B, "dictionaries", 1.2) - 0.1); draw_on(c, "s1f", t3 + key_at(B, "puts", 3.2) - 0.2)
    draw_on(c, "s1x", t3 + key_at(B, "food", 4.0), 0.35); c.sfx("tap", t3 + key_at(B, "food", 4.0) + 0.3)
    body.append(f'<div class="sec" id="s1"><div class="bigw" id="s1w" style="top:330px;font-size:200px">{word(QAHWA)}</div>'
                f'<div class="sp mid" id="s1t" style="top:640px">qahwa</div>' + doodle("book", 110, 760, 360, "peach", "s1d", True, 6)
                + doodle("plate", 590, 760, 360, "sage", "s1f", True, 6) + doodle("cross", 610, 780, 320, "red", "s1x", True, 9) + f'{h}</div>')
    t = whip_out(c, "s1", t3 + db + 0.35)
    # 2. Yemen, the 1400s: Sufis drink it to stay awake for night prayers (the night is drawn), and the name moves over
    B = V + "b2s.mp3"; whip_in(c, "s2", t); d = clip(c, B, t + 0.1); s = t + 0.1
    h = cap(c, "s2a", B, s, (("1400s", "y"), ("yemen", "g"), ("up", "r"), ("night", "g"), ("qahwa", "r")))
    year(c, "s2y", 1000, 1400, s + key_at(B, "1400s", 0.3) - 0.2, 0.8, suffix="s")
    pop(c, "#s2yl", s + key_at(B, "yemen", 1.6)); draw_on(c, "s2l", s + key_at(B, "sufis", 1.2) - 0.1)
    br = s + key_at(B, "drank", 2.2); draw_on(c, "s2p", br - 0.1); draw_on(c, "s2c", br + 0.2)
    for k in range(3): pop(c, f"#s2b{k}", s + key_at(B, "coffee", 2.6) + 0.1 * k, k == 0)
    ni = s + key_at(B, "night", 5.0); draw_on(c, "s2m", ni - 0.15); [pop(c, f"#s2s{k}", ni + 0.15 + 0.12 * k, False) for k in range(3)]
    pop(c, "#s2q", s + key_last(B, "qahwa", d - 0.8))
    body.append('<div class="sec" id="s2"><div class="yr" style="top:250px"><small>IN THE</small><b id="s2y">1000s</b></div>'
                + doodle("moon", 760, 470, 200, "sky", "s2m", True, 6) + "".join(doodle("star", x, y, 60, "butter", f"s2s{k}") for k, (x, y) in enumerate([(690, 470), (930, 640), (700, 650)]))
                + doodle("lantern", 110, 500, 260, "butter", "s2l", True, 6) + doodle("dallah", 260, 760, 330, "sage", "s2p", True, 6)
                + doodle("cup", 600, 820, 260, "peach", "s2c", True, 6)
                + "".join(doodle("bean", x, y, 90, "butter", f"s2b{k}") for k, (x, y) in enumerate([(560, 1060), (670, 1090), (790, 1050)]))
                + '<div class="sp" id="s2yl" style="left:120px;top:1110px">Yemen</div>'
                + f'<div class="sp" id="s2q" style="left:640px;top:740px"><span class="ar">{word(QAHWA)}</span></div>{h}</div>')
    c.t("".join(f'tl.set("#s2s{k}, #s2b{k}", {{opacity:0}}, 0);' for k in range(3)))
    t = whip_out(c, "s2", s + d + 0.4)
    # 3. the route: Makkah, Cairo, Istanbul (kahve), the Dutch (koffie), English (coffee, 1582); a cup travels the line as each is said
    B = V + "b3s.mp3"; whip_in(c, "s3", t); d = clip(c, B, t + 0.1); s = t + 0.1
    h = cap(c, "s3a", B, s, (("istanbul", "g"), ("kahve", "r"), ("dutch", "g"), ("koffie", "r"), ("1582", "y"), ("coffee.", "r")))
    P = [(x, y) for _, x, y, _, _ in ROUTE]
    segs = []
    for i in range(len(P) - 1):                          # a smooth line through the stops (Catmull-Rom as cubic Béziers)
        p0, p1, p2 = P[max(i - 1, 0)], P[i], P[i + 1]; p3 = P[min(i + 2, len(P) - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6); c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        segs.append(f"M{p1[0]} {p1[1]} C{c1[0]:.0f} {c1[1]:.0f} {c2[0]:.0f} {c2[1]:.0f} {p2[0]} {p2[1]}")
    pop(c, "#s3n0", s + 0.1); pop(c, "#s3l0", s + 0.2, False)
    prev = s + 0.3
    for i in range(1, len(ROUTE)):
        at = s + key_at(B, ROUTE[i][3], prev - s + 0.8)
        c.t(f'(() => {{ const P = document.getElementById("s3g{i - 1}"), L = P.getTotalLength(), cup = document.getElementById("s3cup"), o = {{p:0}}; '
            f'tl.fromTo(o, {{p:0}}, {{p:1, duration:{max(0.3, at - prev - 0.05):.2f}, ease:"power1.inOut", immediateRender:false, onUpdate:() => {{ const q = P.getPointAtLength(o.p * L); '
            f'cup.style.transform = `translate(${{q.x - 45}}px, ${{q.y - 60}}px)`; }}}}, {prev:.2f}); }})();')
        c.t(f'tl.fromTo("#s3g{i - 1}", {{strokeDashoffset:1}}, {{strokeDashoffset:0, duration:{max(0.3, at - prev - 0.05):.2f}, ease:"power1.inOut", immediateRender:false}}, {prev:.2f});')
        pop(c, f"#s3n{i}", at); pop(c, f"#s3l{i}", at + 0.08, False); prev = at
    yc = s + key_at(B, "1582", d - 1.6); year(c, "s3y", 1450, 1582, yc - 0.3, 0.7)
    c.t(f'tl.fromTo("#s3cupi", {{opacity:0, scale:0.4}}, {{opacity:1, scale:1, duration:0.3, ease:"back.out(2)"}}, {s + 0.2:.2f});')
    c.t(f'document.getElementById("s3cup").style.transform = "translate({P[0][0] - 45}px, {P[0][1] - 60}px)";')
    lab = "".join(f'<div class="sp" id="s3l{i}" style="left:{lx}px;top:{y - 40}px;font-size:40px">{n}</div>' for i, (n, x, y, _, lx) in enumerate(ROUTE))
    pins = "".join(doodle("pin", x - 35, y - 62, 70, "blush", f"s3n{i}", sw=5) for i, (n, x, y, _, _) in enumerate(ROUTE))
    body.append('<div class="sec" id="s3"><svg class="dd" viewBox="0 0 1080 1920" style="left:0;top:0;width:1080px;height:1920px">'
                + "".join(f'<path id="s3g{i}" d="{g}" pathLength="1" fill="none" stroke="#e09868" stroke-width="9" stroke-linecap="round" style="stroke-dasharray:1;stroke-dashoffset:1"/>' for i, g in enumerate(segs))
                + f'</svg>{pins}{lab}<div id="s3cup" style="position:absolute;left:0;top:0;width:90px;height:90px">' + doodle("cup", 0, 0, 90, "peach", "s3cupi", sw=5) + '</div>'
                + f'<div class="yr" style="top:250px;left:560px;right:40px"><small>BY</small><b id="s3y" style="font-size:130px">1450</b></div>{h}</div>')
    c.t("".join(f'tl.set("#s3n{i}, #s3l{i}", {{opacity:0}}, 0);' for i in range(len(ROUTE))))
    t = whip_out(c, "s3", s + d + 0.5)
    # 4. your turn: masjid is the place of sujood, so what's a مَقْهى? 3-2-1, a CAFÉ
    B, S = V + "t1.mp3", V + "b6.mp3"
    whip_in(c, "s4", t); d = clip(c, B, t + 0.1); h = cap(c, "s4a", B, t + 0.1, (("turn", "r"), ("masjid", "g"), ("place", "g")), "ccs")
    pop(c, "#s4m", t + 0.1 + key_at(B, "masjid", 1.0))
    t2 = t + 0.1 + d + 0.05; dw = say_up(c, "", t2, src=V + "maqha.mp3"); zoom_in(c, "#s4w", t2)
    for i in range(3): c.inn(f"#qo{i}", t2 + 0.2 + i * 0.12, 30)
    done = count_down(c, "qc", t2 + dw + 0.4)
    reveal(c, "#qo1", ["#qo0", "#qo2"], done)
    d6 = clip(c, S, done); hit = done + key_at(S, "cafe", 0.1) + 0.05
    c.t(f'tl.to(["#qo0", "#qo2"], {{opacity:0, duration:0.25}}, {hit - 0.3:.2f});')
    slam(c, "#s4s", "s4", hit); bu = burst(c, "s4x", 540, 1300, hit + 0.05); draw_on(c, "s4c", hit + 0.2, 0.6)
    opts = '<div class="opts col" id="qo" style="top:860px">' + "".join(f'<div class="op2" id="qo{i}"><b>{o}</b></div>' for i, o in enumerate(["a coffee pot", "a café", "a coffee bean"])) + '</div>'
    body.append(f'<div class="sec" id="s4">{h}<div class="sp mid" id="s4m" style="top:400px;font-size:44px"><span class="ar">{word([("مَ", "v"), ("سْجِد", "")])}</span>'
                f' = the place of sujood</div><div class="bigw" id="s4w" style="top:520px;font-size:180px">{word(MAQHA)}</div>'
                f'{opts}{cnt("qc", 1270)}<div class="slamw" id="s4s" style="top:1260px;font-size:110px">a <em>CAFÉ</em>!</div>{bu}'
                + doodle("cup", 800, 1220, 170, "peach", "s4c", True, 6) + '</div>')
    c.css += "#s4a { top:270px; }"
    t = done + d6 + 0.9
    c.out_("#s4", t - 0.4); end = clip(c, V + "end.mp3", t)
    body.append('<div id="pflash"></div>' + c.end(t, "How do you take your coffee? Comment below 👇 Send this to your coffee-addict friend ☕"))
    total = round(t + end + 0.9, 2); finish(total)
    c.write("\n".join("      " + b for b in body), total)

# ---------------------------------------------------------------- the story of a word #3, the Dune edition (owner 28 Oct 2026, #303)
DUNES = [(1040, "M0 260 C150 200 300 170 460 210 S760 290 900 230 S1120 160 1200 190 V760 H0 Z", "#ecc093", 12),   # (top, path, colour, drift px)
         (1140, "M0 380 C180 300 360 330 520 380 S820 450 980 360 S1150 320 1200 340 V760 H0 Z", "#dfa36d", 26),
         (1260, "M0 520 C200 440 420 470 600 530 S900 600 1200 500 V760 H0 Z", "#cb8852", 44)]
DESERT_CSS = (
    "#root { background:linear-gradient(#f7e9d4 0%, #f5d4ac 36%, #f0bb86 60%, #e9a96f 100%); } #glow { display:none; }"
    "#desert { position:absolute; inset:0; overflow:hidden; pointer-events:none; z-index:0; } #desert svg.dn { position:absolute; left:-60px; width:1200px; height:760px; }"
    "#sun { position:absolute; left:600px; top:470px; width:300px; height:300px; border-radius:50%; "
    "background:radial-gradient(circle, #fff7e2 0 50%, rgba(255,242,214,.6) 58%, rgba(255,232,196,0) 71%); }"
    ".sand { position:absolute; left:0; border-radius:50%; } .gust { position:absolute; left:0; height:3px; width:240px; border-radius:2px; "
    "background:linear-gradient(90deg, rgba(255,246,228,0), rgba(255,246,228,.85), rgba(255,246,228,0)); }"
    "#worm { position:absolute; left:0; top:0; width:1080px; height:1920px; overflow:visible; }"
    ".sec { z-index:2; } #brand, #kicker, #end, #pflash { z-index:3; }"
    ".title { position:absolute; left:0; right:0; text-align:center; font-family:\"Anton\", var(--la); font-size:128px; line-height:1; letter-spacing:.12em; color:#6b3a17; "
    "text-shadow:0 6px 0 rgba(255,236,206,.7); } .title small { display:block; font-family:var(--la); font-size:30px; letter-spacing:.3em; color:#7a4d2a; margin-top:14px; text-shadow:none; }")

def desert(c, body):
    """The desert page: a dusk sky, a low sun, two moons, three layers of dunes that drift at different speeds, sand blowing through on the
    wind, and a worm (#worm) behind the nearest dune for worm_rise(). Returns finish(total), which adds the movement once the length is known."""
    c.css += STORY_CSS + DESERT_CSS                     # the story look; the desert's own sky replaces the pastel page
    os.makedirs(os.path.join(c.a, "fonts"), exist_ok=True)
    shutil.copy(os.path.join(T.ROOT, "brag-quiz/fonts/anton-latin-400-normal.woff2"), os.path.join(c.a, "fonts"))
    c.css += '@font-face { font-family:"Anton"; src:url("assets/fonts/anton-latin-400-normal.woff2") format("woff2"); }'
    rnd = __import__("random").Random(9)
    dn = lambda k: (f'<svg class="dn" id="dn{k}" viewBox="0 0 1200 760" style="top:{DUNES[k][0]}px"><path d="{DUNES[k][1]}" fill="{DUNES[k][2]}"/>'
                    f'<path d="{DUNES[k][1].split(" V")[0]}" fill="none" stroke="#f9dfba" stroke-width="5" opacity=".55"/></svg>')
    W = "M1000 2010 C990 1640 1075 1290 850 1050"          # the worm arches up out of the sand on the right and leans over the page
    worm = ('<svg id="worm" viewBox="0 0 1080 1920"><g id="wormg">'
            f'<path d="{W}" fill="none" stroke="#8d5b36" stroke-width="170" stroke-linecap="round"/>'
            f'<path d="{W}" fill="none" stroke="#a87048" stroke-width="120" stroke-linecap="round" opacity=".55"/>'
            f'<path d="{W}" fill="none" stroke="#6a4024" stroke-width="172" stroke-dasharray="5 36"/>'
            '<ellipse cx="846" cy="1050" rx="92" ry="44" fill="#d39a64" transform="rotate(-38 846 1050)"/>'
            '<ellipse cx="846" cy="1050" rx="74" ry="32" fill="#2f1b0f" transform="rotate(-38 846 1050)"/></g></svg>')
    sand = []
    for k in range(40):
        y, s = rnd.randint(860, 1900), rnd.choice([3, 4, 5, 6])
        sand.append((k, rnd.randint(-60, 1140), y, s, rnd.uniform(160, 420), rnd.choice(["#fff4e0", "#fbe2bd", "#b8743f"])))
    gusts = [(k, rnd.randint(0, 1080), rnd.randint(980, 1800), rnd.uniform(700, 1100)) for k in range(6)]
    body.insert(0, '<div id="desert" data-layout-ignore><div id="sun"></div>' + doodle("moon", 70, 470, 84, "sky", "moon1", rot=-14) + doodle("moon", 175, 420, 44, "sky", "moon2", rot=8)
                + dn(0) + dn(1) + worm + dn(2)
                + "".join(f'<i class="sand" id="sd{k}" style="top:{y}px;width:{s}px;height:{s}px;background:{col};opacity:.75"></i>' for k, x, y, s, v, col in sand)
                + "".join(f'<i class="gust" id="gs{k}" style="top:{y}px"></i>' for k, x, y, v in gusts)
                + '<div id="wspray" style="position:absolute;left:1000px;top:1560px">' + "".join(f'<i class="sand" style="left:0;top:0;width:{8 + k % 3 * 4}px;height:{8 + k % 3 * 4}px;'
                  f'background:{["#f3cf9f", "#d9a46e", "#fbe6c4"][k % 3]};opacity:0"></i>' for k in range(12)) + '</div></div>')
    c.t('tl.set("#wormg", {y:1000}, 0);')
    def finish(total):
        for k, (top, p, col, dr) in enumerate(DUNES):
            c.t(f'tl.fromTo("#dn{k}", {{x:0}}, {{x:{-dr}, duration:{total:.2f}, ease:"none"}}, 0);')
        c.t(f'tl.fromTo("#sun", {{y:0}}, {{y:60, duration:{total:.2f}, ease:"none"}}, 0);')
        for k, x, y, s, v, col in sand:
            c.t(f'tl.fromTo("#sd{k}", {{x:{x}}}, {{x:{x + v * total:.0f}, duration:{total:.2f}, ease:"none", modifiers:{{x:gsap.utils.unitize(gsap.utils.wrap(-60, 1140))}}}}, 0);')
        for k, x, y, v in gusts:
            c.t(f'tl.fromTo("#gs{k}", {{x:{x}}}, {{x:{x + v * total:.0f}, duration:{total:.2f}, ease:"none", modifiers:{{x:gsap.utils.unitize(gsap.utils.wrap(-300, 1300))}}}}, 0);')
        for k in range(1, int(total / 7.5) + 1): clip(c, "brag-quiz/sfx/soft/wind.wav", (k - 1) * 7.5, 0.22)
    return finish

def worm_rise(c, at, hold=1.8):
    """The worm bursts up out of the sand behind the page, a rumble under it, and sinks again."""
    c.t(f'tl.to("#wormg", {{y:0, duration:0.9, ease:"power3.out"}}, {at:.2f});')
    c.t(f'tl.to("#wormg", {{y:1000, duration:1.1, ease:"power2.in"}}, {at + 0.9 + hold:.2f});')
    c.t(f'tl.fromTo("#dn2", {{y:0}}, {{y:0, keyframes:[{{y:-10, duration:0.06}}, {{y:8, duration:0.06}}, {{y:-5, duration:0.06}}, {{y:0, duration:0.08}}], immediateRender:false}}, {at:.2f});')
    clip(c, "brag-quiz/sfx/soft/rumble.wav", at - 0.3, 0.6)
    c.t(f'tl.fromTo("#wspray i", {{opacity:1, x:0, y:0, scale:1}}, {{opacity:0, x:(i) => (i % 2 ? 1 : -1) * (60 + 22 * i), y:(i) => -120 - 30 * (i % 4), '
        f'scale:0.5, duration:0.8, ease:"power2.out", immediateRender:false}}, {at + 0.05:.2f});')

GHAYB = [("الْ", ""), ("غَ", "r"), ("يْ", "r"), ("ب", "r")]
LISAN = [("لِ", "r"), ("سا", "r"), ("ن", "r")]

def h3():
    """The story of a word #3, the Dune edition (owner 28 Oct 2026, #303: "a Dune themed Arabic video which explains the history and context of one
    of the Arabic words"): LISAN AL-GAIB, on a desert page. Hook "Everyone in Dune chants Lisan al-Gaib… but what does it actually mean in Arabic?"
    (said calmly: the owner took the shouting out on #296); لِسان tongue, language, and the Qur'an "in a clear Arabic tongue" (ash-Shuʿarāʾ 26:195,
    text only, no recitation); your turn الْغَيْب from the first page of al-Baqarah (2:3): the desert, the unseen or the future? 3-2-1, the UNSEEN
    (the worm rises out of the sand), and it's ghayb with a gh; together "the tongue of the unseen"; Herbert didn't invent it: the Persian poet
    Hafez (d. 1390) was called Lisān al-Ghayb (Dune's glossary: "the Voice from the Outer World"). No clip from the film (copyright, and reused
    clips are what TikTok flags as unoriginal, #289); no Dune logo or the film's font. Voices: brag-quiz/voice/lisan-lines.json."""
    V = "brag-quiz/voice/lisan/"
    c = SO.vcomp("h3-lisan", "THE ARABIC IN DUNE"); c.bed = True; body = []; serif(c); c.css += GROW_CSS
    c.fx = 0.5                                           # the background sounds about 30% down in the finished mix (owner, 28 Oct 2026; the render compresses, so 0.7 only gave ~1.7 dB)
    finish = desert(c, body)
    def anim(c, at, d):                                  # "Lisan al-Gaib": the title glows as it's said, and the wind gusts
        c.t(f'tl.fromTo("#htitle", {{scale:1}}, {{scale:1.06, duration:0.25, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {at(4):.2f});')
        c.t(f'tl.to("#htitle", {{color:"#a8531f", duration:0.3}}, {at(4):.2f});'); clip(c, "brag-quiz/sfx/soft/whoosh.wav", at(4) - 0.1, 0.5)
    words = "Everyone in Dune chants Lisan al-Gaib… but what does it actually mean in Arabic?".split()
    t = hook_in(c, body, (words, {2: "red", 11: "circle"}, V + "h1.mp3"), bg=('<div class="title" id="htitle" style="top:300px">LISAN AL-GAIB<small>لِسانُ الْغَيْب</small></div>', anim))
    c.css += "#hook .hookline { top:600px; font-size:96px; } #hw4, #hw5 { color:#a8531f; } #htitle small { font-family:var(--ar); font-size:44px; letter-spacing:0; }"
    # 1. لِسان: tongue, and language; the Qur'an "in a clear Arabic tongue"
    A, B = V + "b1.mp3", V + "b1b.mp3"
    whip_in(c, "s1", t); dl = say_up(c, "", t + 0.15, src=V + "lisan.mp3"); zoom_in(c, "#s1w", t + 0.15); pop(c, "#s1t", t + 0.15 + dl, False)
    t2 = t + 0.15 + dl + 0.2; da = clip(c, A, t2); h = cap(c, "s1a", A, t2, (("tongue", "r"), ("language", "g")))
    pop(c, "#s1m0", t2 + key_at(A, "tongue", 0.6)); pop(c, "#s1m1", t2 + key_at(A, "language", 1.5))
    t3 = t2 + da + 0.15; cap_out(c, "s1a", t3 - 0.1); db = clip(c, B, t3); h2 = cap(c, "s1b", B, t3, (("qur'an", "g"), ("lisan", "r"), ("tongue", "r")))
    c.t(f'tl.fromTo("#s1q", {{opacity:0, y:40, scale:0.96}}, {{opacity:1, y:0, scale:1, duration:0.45, ease:"power3.out"}}, {t3 + key_at(B, "qur", 0.3):.2f});')
    body.append(f'<div class="sec" id="s1"><div class="bigw" id="s1w" style="top:330px;font-size:200px">{word(LISAN)}</div>'
                f'<div class="sp mid" id="s1t" style="top:640px">lisān</div>'
                '<div class="sp" id="s1m0" style="left:250px;top:770px;color:var(--rubric)">tongue</div><div class="sp" id="s1m1" style="left:560px;top:770px;color:var(--verdigris)">language</div>'
                '<div class="quote" id="s1q" style="top:900px"><q style="font-size:50px;quotes:none"><span style="font-family:var(--ar);font-style:normal;font-size:64px">بِلِسانٍ عَرَبِيٍّ مُبِينٍ</span>'
                '<br>in a clear Arabic tongue</q><small>the Qur’an · ash-Shuʿarāʾ 26:195</small></div>' + f'{h}{h2}</div>')
    t = whip_out(c, "s1", t3 + db + 0.35)
    # 2. your turn: الْغَيْب (al-Baqarah 2:3): the desert, the unseen or the future? 3-2-1, the UNSEEN, and the worm rises out of the sand
    B, Q, S = V + "t1.mp3", V + "t1b.mp3", V + "b2t.mp3"      # b2t, b3t: the lines' last sentences cut for length
    whip_in(c, "s2", t); d = clip(c, B, t + 0.1); h = cap(c, "s2a", B, t + 0.1, (("turn", "r"), ("baqarah", "g")), "ccs")
    t2 = t + 0.1 + d + 0.05; dw = say_up(c, "", t2, src=V + "ghayb.mp3"); zoom_in(c, "#s2w", t2)
    t3 = t2 + dw + 0.15; dq = clip(c, Q, t3); h2 = cap(c, "s2b", Q, t3, (("it?", "r"),))
    for i in range(3): c.inn(f"#qo{i}", t3 + 0.1 + i * 0.12, 30)
    done = count_down(c, "qc", t3 + dq + 0.3)
    reveal(c, "#qo1", ["#qo0", "#qo2"], done)
    d2 = clip(c, S, done); hit = done + key_at(S, "unseen", 0.15) + 0.05
    c.t(f'tl.to(["#qo0", "#qo2", "#s2b"], {{opacity:0, duration:0.25}}, {hit - 0.3:.2f});')
    slam(c, "#s2s", "s2", hit, "brag-quiz/sfx/soft/impact.wav"); worm_rise(c, hit - 0.1)
    c.t(f'tl.to("#qo", {{opacity:0, y:30, duration:0.3}}, {hit + 1.0:.2f});')
    c.t(f'tl.fromTo("#s2q", {{opacity:0, y:40, scale:0.96}}, {{opacity:1, y:0, scale:1, duration:0.45, ease:"power3.out"}}, {done + key_at(S, "hidden", 1.4):.2f});')
    pop(c, "#s2g", done + key_at(S, "hidden", 1.4) + 0.8)
    opts = '<div class="opts col" id="qo" style="top:800px">' + "".join(f'<div class="op2" id="qo{i}"><b>{o}</b></div>' for i, o in enumerate(["the desert", "the unseen", "the future"])) + '</div>'
    body.append(f'<div class="sec" id="s2">{h}<div class="bigw" id="s2w" style="top:430px;font-size:170px">{word(GHAYB)}</div>{h2}'
                f'{opts}{cnt("qc", 1230)}<div class="slamw" id="s2s" style="top:1240px;font-size:110px">the <em>UNSEEN</em></div>'
                '<div class="quote" id="s2q" style="top:810px"><q style="font-size:50px;quotes:none"><span style="font-family:var(--ar);font-style:normal;font-size:60px">الَّذِينَ يُؤْمِنُونَ بِالْغَيْبِ</span>'
                '<br>those who believe in the unseen</q><small>the Qur’an · al-Baqarah 2:3</small></div>'
                f'<div class="sp mid" id="s2g" style="top:1110px"><span class="ar" style="color:var(--rubric)">غ</span> = gh, not g</div></div>')
    c.css += "#s2a { top:270px; } #s2b { top:720px; }"
    t = whip_out(c, "s2", done + d2 + 1.0)
    # 3. together: لِسانُ الْغَيْب, "the tongue of the unseen"
    B = V + "b3t.mp3"
    whip_in(c, "s3", t); dp = say_up(c, "", t + 0.15, src=V + "lisanghayb.mp3"); zoom_in(c, "#s3w", t + 0.15)
    pop(c, "#s3l0", t + 0.25, False); pop(c, "#s3l1", t + 0.15 + dp * 0.55, False)
    t2 = t + 0.15 + dp + 0.2; d = clip(c, B, t2); h = cap(c, "s3a", B, t2, (("tongue", "r"), ("unseen", "g")))
    tg = t2 + key_at(B, "tongue", 1.8); zoom_in(c, "#s3m", tg); c.sfx("correct", tg)
    body.append(f'<div class="sec" id="s3"><div class="bigw" id="s3w" dir="rtl" style="top:360px;font-size:150px;direction:rtl">{word(LISAN + [("ُ", "")])} {word(GHAYB)}</div>'
                '<div class="sp" id="s3l0" style="left:600px;top:640px;color:var(--rubric)">tongue</div><div class="sp" id="s3l1" style="left:170px;top:640px;color:var(--verdigris)">the unseen</div>'
                f'<div class="slamw" id="s3m" style="top:820px;font-size:92px;color:#8a4316">the tongue<br>of the unseen</div>{h}</div>')
    t = whip_out(c, "s3", t2 + d + 0.4)
    # 4. the history: Herbert didn't invent it; the years roll back from Dune (1965) to Hafez of Shiraz (d. 1390)
    B = V + "b4.mp3"; whip_in(c, "s4", t); d = clip(c, B, t + 0.1); s = t + 0.1
    h = cap(c, "s4a", B, s, (("herbert", "g"), ("five", "y"), ("hundred", "y"), ("hafez", "r")))
    pop(c, "#s4d", s + key_at(B, "herbert", 0.6))
    rb = s + key_at(B, "five", 2.0); year(c, "s4y", 1965, 1390, rb - 0.1, 1.3, 10)
    c.t(f'tl.to("#s4d", {{opacity:0.25, duration:0.3}}, {rb:.2f});')
    hz = s + key_at(B, "hafez", 4.6); pop(c, "#s4h", hz); draw_on(c, "s4b", hz - 0.3, 0.7); pop(c, "#s4n", hz + 0.5, False)
    body.append('<div class="sec" id="s4"><div class="yr" style="top:250px"><small>THE YEAR</small><b id="s4y">1965</b></div>'
                '<div class="sp mid" id="s4d" style="top:520px">Dune · 1965</div>' + doodle("book", 380, 590, 320, "peach", "s4b", True, 6)
                + '<div class="sp mid" id="s4h" style="top:930px;font-size:56px">Hafez of Shiraz · d. 1390</div>'
                '<div class="sp mid" id="s4n" style="top:1060px;font-size:38px"><span class="ar">حافِظ</span> = one who knows the Qur’an by heart</div>' + f'{h}</div>')
    c.css += "#s4y { color:#8a4316; }"
    t = s + d + 0.6
    c.out_("#s4", t - 0.4); end = clip(c, V + "end.mp3", t)
    body.append('<div id="pflash"></div>' + c.end(t, "Which Dune word next: Muad’Dib or Usul? Comment below 👇"))
    total = round(t + end + 0.9, 2); finish(total)
    c.write("\n".join("      " + b for b in body), total)

ALL = {"f1-sujood": f1, "f2-root": f2, "f3-she-eats": f3, "j1-jumuah": j1, "a1-adhan": a1, "a2-adhan": a2,
       "w5-rabbana": w5, "w6-salam": w6, "w7-tahiyyat": w7, "g1-plural": g1, "g2-female": g2, "g3-past": g3, "r2-muhammad": r2,
       "r3-akbar": r3, "r4-insha": r4, "g4-past-i": g4, "g5-endings": g5, "w8-subhana-azim": w8,
       "v1-go-quiz": v1q, "v2-write-quiz": v2q, "i4-she-quiz": i4q, "n1-jannah": n1, "m1-mashallah": m1, "m2-barik": m2, "l1-ladder": l1,
       "n2-rahma": n2, "d1-din": d1, "f4-family": f4, "n3-ilm": n3, "n4-jannah": n4, "l2-jumuah": l2, "n5-salah": n5, "h1-algebra": h1, "h2-coffee": h2, "h3-lisan": h3}
if __name__ == "__main__":
    ids = [a for a in sys.argv[1:] if not a.startswith("--")]
    T.LUFS.update({v: -16.0 for v in ALL})
    for vid, fn in ALL.items():
        if ids and vid not in ids: continue
        T.level(vid) if "--level" in sys.argv else fn()
