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

def hook_in(c, body, hook):
    """An opening hook (owner, 12 Oct 2026) in the MOTION-STYLE moves. Each word swooshes in from alternating sides as the hook voice
    says it (the first is there at frame 0); a timer ring at the top counts the years up; numbers count up all over the page; the
    red word bumps, the circled word gets a gold hand-drawn circle, a flash and a shake; then a whip into the quiz.
    hook = (words, {word index: "red" | "circle"}, mp3 spoken with HOOK_VOICE[, (timer label, count)]); the timer counts YEARS to 7 unless given."""
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
    for i in range(1, len(words)):      # each word swooshes in from alternating sides, blurred
        x = -560 if i % 2 else 560
        c.t(f'tl.fromTo("#hw{i}", {{opacity:0, x:{x}, scale:1.3, filter:"blur(16px)"}}, {{opacity:1, x:0, scale:1, filter:"blur(0px)", duration:0.32, ease:"expo.out"}}, {at(i) - 0.08:.2f});')
    for k, (x, y, sz, a, b, u, col, r) in enumerate(HOOK_NUMS):   # the numbers count up and drift, from frame 0
        c.t(f'(() => {{ const o = {{v:{a}}}; tl.to(o, {{v:{b}, duration:{d + 0.2:.2f}, ease:"power2.in", onUpdate:() => {{ document.querySelector("#hn{k} b").textContent = '
            f'Math.round(o.v).toLocaleString("en-GB"); }}}}, 0); }})();')
        c.t(f'tl.fromTo("#hn{k}", {{y:0, scale:0.92}}, {{y:{-30 if k % 2 else 26}, scale:1.08, duration:{d + 0.2:.2f}, ease:"none"}}, 0);')
    tr = at(red)                        # the timer: years count up and the ring fills from "years" to the last word
    c.t(f'tl.fromTo("#htimer", {{scale:0.6, opacity:0.4}}, {{scale:1, opacity:1, duration:0.4, ease:"back.out(2)"}}, {tr - 0.1:.2f});')
    c.t(f'tl.fromTo("#htimer .fg", {{strokeDashoffset:805}}, {{strokeDashoffset:0, duration:{d - tr + 0.1:.2f}, ease:"power1.in"}}, {tr:.2f});')
    c.t(f'(() => {{ const o = {{v:0}}; tl.to(o, {{v:{n}, duration:{d - tr + 0.1:.2f}, ease:"power1.in", onUpdate:() => {{ document.getElementById("hty").textContent = Math.floor(o.v); }}}}, {tr:.2f}); }})();')
    c.t(f'tl.fromTo("#hw{red}", {{scale:1}}, {{scale:1.2, duration:0.16, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {tr + 0.25:.2f});')
    for k in range(1, n + 1):           # a clear tick on every number the timer counts (power1.in: number k at sqrt(k/n) of the way)
        clip(c, "brag-quiz/sfx/ref/click.wav", tr + (d - tr + 0.1) * (k / n) ** 0.5, 0.7)
    for i, m in marks.items():
        if m == "loud":                 # the stressed word lands with force: huge at frame 0, slams down on the voice, crash, shockwave, screen shake
            hit = max(0.16, at(i) + 0.1)
            fx = '<i class="hring"></i><i class="hring r2"></i>' + "".join(f'<i class="hspark" style="transform:rotate({a}deg)"></i>' for a in range(0, 360, 36))
            body[-1] = body[-1].replace(f'id="hw{i}">{words[i]}</span>', f'id="hw{i}">{words[i]}{fx}</span>')
            c.t(f'tl.fromTo("#hw{i}", {{scale:1.9, rotation:-7, x:180}}, {{scale:1, rotation:0, x:0, duration:{hit:.2f}, ease:"power4.in"}}, 0);')
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

def say_up(c, text, at, target=-19.0):
    """c.say, with the app's recording brought up to about the hook voice's level (owner, 12 Oct 2026: Rafiq was ~11 dB quieter)."""
    src = os.path.join(T.ROOT, "audio", T.AUDIO[text] + ".mp3"); name = T.AUDIO[text] + "-up.mp3"
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

ALL = {"f1-sujood": f1, "f2-root": f2, "f3-she-eats": f3, "j1-jumuah": j1, "a1-adhan": a1, "a2-adhan": a2,
       "w5-rabbana": w5, "w6-salam": w6, "w7-tahiyyat": w7, "g1-plural": g1, "g2-female": g2, "g3-past": g3, "r2-muhammad": r2,
       "r3-akbar": r3, "r4-insha": r4, "g4-past-i": g4, "w8-subhana-azim": w8,
       "v1-go-quiz": v1q, "v2-write-quiz": v2q, "i4-she-quiz": i4q, "n1-jannah": n1}
if __name__ == "__main__":
    ids = [a for a in sys.argv[1:] if not a.startswith("--")]
    T.LUFS.update({v: -16.0 for v in ALL})
    for vid, fn in ALL.items():
        if ids and vid not in ids: continue
        T.level(vid) if "--level" in sys.argv else fn()
