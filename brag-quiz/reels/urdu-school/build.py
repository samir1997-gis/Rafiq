#!/usr/bin/env python3
"""If you speak Urdu, you already know these Arabic words, part 2: in the classroom (#320, the series from #313). The same hook as part 1
(brag-quiz/voice/urdu-doctor/h1x.mp3, HUNDREDS shouted and slammed on), then a drawn classroom wider than the screen, the camera easing from
one thing to the next as each word is said, the word in Arabic with its Urdu spelling underneath, and the counter clicking up:
  1 طالِب the student · 2 عِلْم knowledge · 3 كِتاب the book · 4 قَلَم the pen · 5 حِساب maths · 6 اِمْتِحان the exam
  then the first verses ever revealed mention the pen: al-ʿAlaq 96:4 الَّذِي عَلَّمَ بِالْقَلَمِ, the six together and the ask. Then the cream end card.
Voices: brag-quiz/voice/urdu-school-lines.json (Callum; Rafiq says the Arabic, levelled with Callum). Figures are faceless (owner, 27 Oct).

  python3 brag-quiz/reels/urdu-school/build.py    then  cd brag-quiz/reels/urdu-school/out/v && npx hyperframes render -o ../raw.mp4
"""
import json, os, re, shutil, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
V6 = os.path.join(ROOT, "brag-output-v6/composition/assets"); VO = os.path.join(ROOT, "brag-quiz/voice/urdu-school")
INK, CREAM, GOLD, TEAL, RED, PAPER, SKY = "#17262B", "#F6EBD3", "#F2C46B", "#2E7263", "#B4322A", "#FBF6EA", "#CFE6E1"
dur = lambda f: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
mp3 = lambda n: os.path.join(VO, n + ".mp3")
def words(n):                                                       # word timings, made once from the audio (faster-whisper) and kept
    f = os.path.join(VO, n + ".words.json")
    if not os.path.exists(f):
        from faster_whisper import WhisperModel
        seg, _ = WhisperModel("small.en", device="cpu", compute_type="int8").transcribe(mp3(n), word_timestamps=True)
        json.dump([[w.word.strip(), round(w.start, 2), round(w.end, 2)] for s in seg for w in s.words], open(f, "w"))
    ws = json.load(open(f))
    ws = [[w[0], w[1], w[2] if len(w) > 2 else (ws[i + 1][1] if i + 1 < len(ws) else w[1] + 0.45)] for i, w in enumerate(ws)]   # align_words.py gives starts only
    said = re.sub(r"\[[^]]*\]", "", SCRIPT.get(n, "")).replace("...", "… ").split()
    if len(said) == len(ws): ws = [[s, w[1], w[2]] for s, w in zip(said, ws)]   # the script's spelling (Urdu, ʿilāj), whisper's timing
    return [tuple(w) for w in ws]
SCRIPT = {l["file"]: l["text"] for l in json.load(open(os.path.join(ROOT, "brag-quiz/voice/urdu-school-lines.json")))}
WORDS = [   # file, Arabic, transliteration, meaning, Urdu spelling, Urdu said
    ("talib", "طالِب", "ṭālib", "student", "طالب علم", "taalib-e-ilm"), ("ilm", "عِلْم", "ʿilm", "knowledge", "علم", "ilm"),
    ("kitab", "كِتاب", "kitāb", "book", "کتاب", "kitaab"), ("qalam", "قَلَم", "qalam", "pen", "قلم", "qalam"),
    ("hisab", "حِساب", "ḥisāb", "maths", "حساب", "hisaab"), ("imtihan", "اِمْتِحان", "imtiḥān", "exam", "امتحان", "imtihaan")]
def hook_voice():
    """The hook with HUNDREDS really shouted (owner, 1 Nov 2026: "a lot of emphasis, shouting"): eleven_v3 read it flat mid-line, so the
    loudest of three shouted takes (shout1-3) replaces it in h1b; it sits at least 4 dB above the rest. Writes h1x.mp3 and its word times."""
    out = os.path.join(VO, "h1x.mp3")
    if os.path.exists(out): return
    rd = lambda f: np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", "44100", "-f", "s16le", "-"], capture_output=True).stdout, np.int16).astype(float) / 32768
    db = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
    loud = lambda x: max(db(x[i:i + 2205]) for i in range(0, len(x) - 2205, 1100))
    takes = {n: rd(mp3(n)) for n in ("shout1", "shout2", "shout3")}
    best = max(takes, key=lambda n: loud(takes[n])); sh = takes[best]
    e = np.convolve(sh ** 2, np.ones(441) / 441, "same"); on = np.where(e > 10 ** (-45 / 10))[0]; sh = sh[max(0, on[0] - 441):on[-1] + 2205]
    line = rd(mp3("h1b")); ws = words("h1b"); k = next(i for i, w in enumerate(ws) if "hundred" in w[0].lower())
    a_, b_ = int(ws[k][1] * 44100), int(ws[k + 1][1] * 44100)
    rest = np.concatenate([line[:a_], line[b_:]])
    sh = sh * 10 ** (max(0, loud(rest) + 4 - loud(sh)) / 20)
    gap = np.zeros(int(0.08 * 44100))
    x = np.concatenate([line[:a_], gap, sh, gap, line[b_:] * 10 ** (3 / 20)])   # "of Arabic words!" came out quieter: up 3 dB
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", "44100", "-ac", "1", "-i", "-", "-af", "alimiter=limit=0.97", "-c:a", "libmp3lame", "-q:a", "2", out],
                   input=(np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes(), check=True)
    d = 0.08 * 2 + len(sh) / 44100 - (ws[k + 1][1] - ws[k][1])
    nw = ws[:k] + [("HUNDREDS!", round(ws[k][1] + 0.08, 2), round(ws[k][1] + 0.08 + len(sh) / 44100, 2))] + [(w, round(s + d, 2), round(e_ + d, 2)) for w, s, e_ in ws[k + 1:]]
    json.dump([list(w) for w in nw], open(os.path.join(VO, "h1x.words.json"), "w"))
    print("hook: shout from", best, f"{loud(sh) - loud(rest):+.1f} dB over the line")
if os.path.exists(mp3("shout1")): hook_voice()
HOOK = "h1x" if os.path.exists(mp3("h1x")) else "h1b"
ORDER = [(HOOK, 0.25), ("s1", 0.5), ("talib", 0.25), ("s1b", 0.3), ("s2", 0.45), ("ilm", 0.25), ("s2b", 0.3), ("s3", 0.45), ("kitab", 0.25),
         ("s3b", 0.3), ("s4", 0.45), ("qalam", 0.25), ("s4b", 0.3), ("s5", 0.45), ("hisab", 0.25), ("s5b", 0.3), ("s6", 0.45), ("imtihan", 0.25),
         ("s6b", 0.3), ("s7", 0.45), ("ayah", 0.35), ("s8", 0.4)]
ARABIC = [w[0] for w in WORDS] + ["ayah"]
def spoken(n):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", mp3(n), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout, np.int16) / 32768
    e = 20 * np.log10(np.sqrt(np.convolve(x ** 2, np.ones(160) / 160, "same")) + 1e-9)
    return np.where(e > -45)[0][-1] / 16000 + 0.05
L, t = {}, 0.0
for n, g in ORDER: t += g; L[n] = round(t, 2); t += spoken(n)
END = round(t + 0.9, 2)
def at(n, key, last=False):
    hits = [s for w, s, e in words(n) if key in re.sub(r"[^a-z0-9']", "", w.lower())]
    return round(L[n] + (hits[-1] if last else hits[0]), 2)

# ---- the classroom: 2160 wide, the camera shows 1080 of it -----------------------------------------------------------------------
O = f'stroke="{INK}" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"'
def person(x, y, s, coat, cls="", extra="", head=None):           # faceless, flat, ink outline (as build_pop_carousel.py)
    return (f'<g transform="translate({x},{y}) scale({s})"><g class="{cls}">'
            f'<path d="M-70 0 L -60 -170 C -56 -210 56 -210 60 -170 L 70 0 Z" fill="{coat}" {O}/>'
            f'<rect x="-48" y="0" width="34" height="110" rx="10" fill="{INK}"/><rect x="14" y="0" width="34" height="110" rx="10" fill="{INK}"/>'
            f'<circle cx="0" cy="-250" r="52" fill="#C98E62" {O}/>{head or ""}{extra}</g></g>')   # animate the inner group: the outer one places it
CAP = f'<path d="M-50 -268 C -50 -318 50 -318 50 -268 Z" fill="#ffffff" {O}/>'
BOOKS = "".join(f'<rect x="{x}" y="{y - h}" width="{w}" height="{h}" rx="5" fill="{c}" {O}/>' for y, row in ((470, ((60, 34, 110, RED), (98, 30, 96, TEAL), (132, 38, 120, GOLD), (174, 30, 100, "#6f5bb5"))),
          (680, ((60, 40, 120, "#6f5bb5"), (104, 30, 100, RED), (138, 34, 110, TEAL), (176, 28, 90, GOLD))), (880, ((60, 34, 110, GOLD), (98, 38, 120, RED), (140, 30, 96, TEAL), (174, 34, 104, "#6f5bb5"))))
          for x, w, h, c in row)
WORLD = (
    f'<rect x="0" y="0" width="2160" height="1180" fill="{SKY}"/>'
    + "".join(f'<rect x="{x}" y="0" width="70" height="1180" fill="#bfdcd5" opacity=".5"/>' for x in range(60, 2160, 220))   # wallpaper
    + f'<rect x="0" y="880" width="2160" height="300" fill="#E9D9B4"/><path d="M0 880 L 2160 880" {O}/>'
    + "".join(f'<path d="M{x} 900 L {x + 40} 1180" stroke="#d8c59a" stroke-width="4"/>' for x in range(0, 2160, 120))
    # the bookshelf (knowledge): its books glow for عِلْم
    + f'<rect x="40" y="250" width="190" height="640" rx="10" fill="#c98a4a" {O}/>' + "".join(f'<path d="M40 {y} L 230 {y}" {O}/>' for y in (470, 680)) + BOOKS
    + f'<rect id="glow" x="20" y="230" width="230" height="680" rx="30" fill="{GOLD}" opacity="0"/>'
    # the window and the light that comes in for the pen
    + f'<g id="win"><rect x="720" y="140" width="260" height="380" rx="24" fill="#9fd0f0" {O}/><path d="M850 140 L 850 520 M 720 330 L 980 330" {O}/>'
      f'<circle id="sun" cx="930" cy="210" r="34" fill="{GOLD}"/></g>'
    + f'<path id="beam" d="M720 520 L 980 520 L 640 760 L 420 760 Z" fill="{GOLD}" opacity="0"/>'
    # the student at his desk; the bulb over his head (knowledge); the book on the desk opens; he picks up the pen
    + person(470, 840, 1.0, "#E2B04A", "stu", head=CAP)
    + f'<g id="bulb" transform="translate(470,470)" opacity="0"><circle r="40" fill="#fff6c9" {O}/><rect x="-16" y="36" width="32" height="26" rx="6" fill="#bbb" {O}/>'
      + "".join(f'<path d="M0 -58 L 0 -84" stroke="{GOLD}" stroke-width="8" stroke-linecap="round" transform="rotate({a_})"/>' for a_ in (-60, -30, 0, 30, 60)) + '</g>'
    + f'<g transform="translate(470,700)"><rect x="-200" y="0" width="400" height="34" rx="8" fill="#c98a4a" {O}/><rect x="-180" y="34" width="26" height="146" fill="#c98a4a" {O}/><rect x="154" y="34" width="26" height="146" fill="#c98a4a" {O}/></g>'
    + f'<g id="bookC" transform="translate(400,700)"><rect x="-70" y="-26" width="140" height="26" rx="6" fill="{TEAL}" {O}/></g>'
    + f'<g id="bookO" transform="translate(400,700)" opacity="0"><path d="M0 -10 C -40 -40 -90 -36 -120 -20 L -120 0 C -90 -14 -40 -18 0 6 Z" fill="#fff" {O}/>'
      f'<path d="M0 -10 C 40 -40 90 -36 120 -20 L 120 0 C 90 -14 40 -18 0 6 Z" fill="#fff" {O}/>'
      + "".join(f'<path d="M{s_ * 30} {-14 - i * 7} C {s_ * 55} {-24 - i * 7} {s_ * 80} {-24 - i * 7} {s_ * 100} {-18 - i * 7}" fill="none" stroke="#9aa6a0" stroke-width="3"/>' for s_ in (-1, 1) for i in range(2)) + '</g>'
    + f'<g transform="translate(560,694)"><g id="pen"><rect x="-6" y="-70" width="12" height="70" rx="5" fill="{RED}" {O}/><path d="M-6 0 L 0 16 L 6 0 Z" fill="{INK}"/></g></g>'
    + "".join(f'<g transform="translate({x},{y})"><path class="spk" d="M0 -22 C 4 -6 6 -4 22 0 C 6 4 4 6 0 22 C -4 6 -6 4 -22 0 C -6 -4 -4 -6 0 -22 Z" fill="{GOLD}" opacity="0"/></g>'
              for x, y in ((520, 560), (610, 600), (500, 640), (640, 680)))
    # the blackboard (maths): chalk sums write themselves on
    + f'<rect x="1060" y="150" width="560" height="420" rx="16" fill="#8a5a2b" {O}/><rect x="1084" y="174" width="512" height="372" rx="8" fill="#1f4d45"/>'
    + f'<text id="sum1" x="1340" y="340" text-anchor="middle" font-family="FR" font-weight="600" font-size="84" fill="#f2f2e8" opacity="0">7 × 8 =</text>'
    + f'<text id="sum2" x="1340" y="480" text-anchor="middle" font-family="FR" font-weight="700" font-size="110" fill="{GOLD}" opacity="0">56</text>'
    + f'<rect x="1120" y="570" width="440" height="20" rx="6" fill="#8a5a2b" {O}/>'
    # the calendar and the alarm clock (the exam)
    + f'<g transform="translate(1720,330)"><g id="cal"><rect x="-110" y="-130" width="220" height="250" rx="20" fill="#fff" {O}/><rect x="-110" y="-130" width="220" height="60" rx="20" fill="{RED}" {O}/>'
      f'<text x="0" y="-10" text-anchor="middle" font-family="FR" font-weight="700" font-size="44" fill="{INK}">EXAM</text>'
      f'<text x="0" y="74" text-anchor="middle" font-family="FR" font-weight="600" font-size="34" fill="{TEAL}">tomorrow</text>'
      f'<circle id="ring" pathLength="1" cx="0" cy="-20" r="82" fill="none" stroke="{RED}" stroke-width="9" stroke-dasharray="1" stroke-dashoffset="1"/></g></g>'
    + f'<g transform="translate(1900,760)"><g id="clock"><circle r="70" fill="#fff" {O}/><path d="M0 0 L 0 -44 M 0 0 L 32 14" {O}/><circle cx="-56" cy="-62" r="22" fill="{GOLD}" {O}/><circle cx="56" cy="-62" r="22" fill="{GOLD}" {O}/></g></g>'
    + f'<g transform="translate(1720,880)"><rect x="-140" y="-120" width="280" height="30" rx="8" fill="#c98a4a" {O}/><rect x="-120" y="-90" width="24" height="90" fill="#c98a4a" {O}/><rect x="96" y="-90" width="24" height="90" fill="#c98a4a" {O}/></g>')
CENTRE = {"talib": (540, 1.0), "ilm": (540, 1.0), "kitab": (420, 1.5), "qalam": (540, 1.5), "hisab": (1340, 1.0), "imtihan": (1620, 1.0)}
FOCUS_Y = {"kitab": 640, "qalam": 640}

def build():
    out = os.path.join(HERE, "out", "v"); a = os.path.join(out, "assets")
    if os.path.exists(out): shutil.rmtree(out)
    os.makedirs(a)
    for f in ("fredoka-latin-600-normal.woff2", "fredoka-latin-700-normal.woff2", "amiri-arabic-700-normal.woff2"): shutil.copy(os.path.join(ROOT, "brag-quiz/fonts", f), a)
    shutil.copy(os.path.join(V6, "lib/gsap.min.js"), a)
    for f in ("shimmer.wav", "tick-lo.wav", "thump.wav", "whoosh.wav", "flip.wav", "drone.wav"): shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/soft", f), a)
    for f in ("click.wav", "swoosh.wav", "tap.wav"): shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/ref", f), a)
    for f in ("crash.wav", "boom.wav"): shutil.copy(os.path.join(ROOT, "brag-quiz/sfx", f), a)
    lv = lambda f: float(re.findall(r"I:\s+(-?[\d.]+) LUFS", subprocess.run(["ffmpeg", "-i", f, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr)[-1])
    target = lv(mp3("s8"))                                                   # Rafiq's Arabic level with Callum (the standard)
    for n in L:
        if n in ARABIC: subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3(n), "-af", f"volume={target - lv(mp3(n)):.1f}dB,alimiter=limit=0.95", os.path.join(a, n + ".mp3")], check=True)
        else: shutil.copy(mp3(n), a)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", os.path.join(a, "drone.wav"), "-af",
                    f"atrim=0:{END},afade=t=in:d=0.6,afade=t=out:st={END - 0.4}:d=0.4", "-c:a", "libmp3lame", "-q:a", "3", os.path.join(a, "bed.mp3")], check=True)
    au = []
    def snd(name, t0, vol, d=None, track=None):
        d = d or dur(os.path.join(a, name))
        au.append(f'<audio id="s{len(au)}" src="assets/{name}" data-start="{max(0, t0):.3f}" data-duration="{d:.3f}" data-volume="{vol:.3f}" data-track-index="{track or 3 + len(au)}"></audio>')
    for n, t0 in L.items(): snd(f"{n}.mp3", t0, 1.0, track=1)
    snd("bed.mp3", 0, 0.07, END, track=2)
    js = []; T = js.append
    IN = lambda sel, t, y=40, d=0.5: T(f'tl.fromTo("{sel}", {{opacity:0, y:{y}}}, {{opacity:1, y:0, duration:{d}, ease:"power3.out"}}, {t:.2f});')
    POP = lambda sel, t, s=0.6: T(f'tl.fromTo("{sel}", {{opacity:0, scale:{s}}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.4)", transformOrigin:"50% 50%"}}, {t:.2f});')
    OUT = lambda sel, t, y=-30: T(f'tl.to("{sel}", {{opacity:0, y:{y}, duration:0.3, ease:"power2.in"}}, {t:.2f});')

    # ---- the hook (owner, 1 Nov 2026): "If you speak Urdu, you already know HUNDREDS of Arabic words!" HUNDREDS is huge from frame 0 and
    # slams down on the shout as in g4's hook_in "loud": squash, shockwave rings, sparks, flash, the screen shake, a crash and a boom, and an
    # echo tail of the shout itself (its own reverb). The other words swoosh in one at a time; Arabic-in-Urdu word chips pop up behind.
    hw = words(HOOK); k = next(i for i, w in enumerate(hw) if "hundred" in w[0].lower())
    hd = round(L[HOOK] + hw[k][1] + 0.08, 2)
    T(f'tl.fromTo("#big", {{scale:1.22, rotation:-7, opacity:0.9}}, {{scale:1, rotation:0, opacity:1, duration:{hd:.2f}, ease:"power4.in"}}, 0);')   # the one slam
    T(f'tl.to("#big", {{keyframes:[{{scaleX:1.18, scaleY:0.78, duration:0.06}}, {{scaleX:0.94, scaleY:1.08, duration:0.08}}, {{scaleX:1, scaleY:1, duration:0.12}}]}}, {hd:.2f});')
    T(f'tl.fromTo("#big .ring", {{scale:0.3, opacity:0.9}}, {{scale:3.2, opacity:0, duration:0.55, ease:"expo.out", stagger:0.07, immediateRender:false}}, {hd:.2f});')
    T(f'tl.fromTo("#big .spark", {{opacity:1, scaleX:0.2, x:60}}, {{opacity:0, scaleX:1.4, x:300, duration:0.4, ease:"expo.out", immediateRender:false}}, {hd:.2f});')
    T(f'tl.fromTo("#flash", {{opacity:0.85}}, {{opacity:0, duration:0.3, ease:"power2.out", immediateRender:false}}, {hd:.2f});')
    T(f'tl.to("#hook", {{keyframes:[{{x:-34, y:22, rotation:-1.4, duration:0.035}}, {{x:30, y:-18, rotation:1.2, duration:0.035}}, {{x:-22, y:14, rotation:-0.8, duration:0.04}}, '
      f'{{x:16, y:-10, rotation:0.6, duration:0.04}}, {{x:-8, y:6, rotation:-0.3, duration:0.05}}, {{x:0, y:0, rotation:0, duration:0.06}}]}}, {hd:.2f});')
    snd("crash.wav", hd - 0.02, 0.9); snd("boom.wav", hd - 0.02, 0.6)
    w0, w1 = hw[k][1], (hw[k + 1][1] if k + 1 < len(hw) else hw[k][2] + 0.3)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{w0:.2f}", "-t", f"{w1 - w0 + 0.05:.2f}", "-i", mp3(HOOK), "-af",
                    "apad=pad_dur=2.2,aecho=in_gain=0:out_gain=1:delays=180|360|560|800|1080|1400:decays=0.8|0.65|0.5|0.38|0.27|0.18,afade=t=out:st=1.8:d=0.7",
                    os.path.join(a, "echo.wav")], check=True)
    snd("echo.wav", L[HOOK] + w0, 1.0)                    # the shout's own echo
    hl = {1: "", 2: ""}
    for j, (w, s0, e) in enumerate(hw):
        if j == k: continue
        line = 1 if j < k else 2
        cls = " class=em" if re.sub(r"[^a-z]", "", w.lower()) in ("urdu", "arabic") else ""
        hl[line] += f'<span id="hw{j}"{cls}>{w}</span> '
        T(f'tl.fromTo("#hw{j}", {{opacity:0, x:{-60 if j % 2 else 60}, filter:"blur(8px)"}}, {{opacity:1, x:0, filter:"blur(0px)", duration:0.3, ease:"power3.out"}}, {L[HOOK] + s0 - 0.05:.2f});')
        if j in (0, k + 1): snd("swoosh.wav", L[HOOK] + s0 - 0.05, 0.25)
    CHIPS = [("مَرِيض", "mareez"), ("وَقْت", "waqt"), ("دُنْيا", "duniya"), ("طَبِيب", "tabeeb"), ("صَبْر", "sabr"), ("دَواء", "dawa"), ("خَبَر", "khabar"),
             ("شُكْر", "shukr"), ("إِنْسان", "insaan"), ("حال", "haal"), ("عَقْل", "aql"), ("فِكْر", "fikr")]      # part 1's words and others, not this video's six
    fx = '<i class="ring"></i><i class="ring r2"></i>' + "".join(f'<i class="spark" style="transform:rotate({a_}deg)"></i>' for a_ in range(0, 360, 36))
    rng = np.random.default_rng(5); chips = ""
    for i, (ar, ur) in enumerate(CHIPS):
        x, y = (70 + (i % 3) * 330 + rng.uniform(-15, 15), 1000 + (i // 3) * 190 + rng.uniform(-10, 10))
        chips += f'<div class="chip" id="ch{i}" style="left:{x:.0f}px;top:{y:.0f}px"><b>{ar}</b><span>{ur}</span></div>'
        t0 = hd + 0.5 + i * 0.28
        T(f'tl.fromTo("#ch{i}", {{opacity:0, y:40, scale:0.7}}, {{opacity:1, y:0, scale:1, duration:0.4, ease:"back.out(1.4)"}}, {t0:.2f});')
        T(f'tl.to("#ch{i}", {{y:-14, duration:2.5, ease:"sine.inOut"}}, {t0 + 0.4:.2f});')
        snd("click.wav", t0, 0.35)
    S1 = L["s1"] - 0.3
    T(f'tl.to("#hook", {{opacity:0, y:-80, duration:0.35, ease:"power2.in"}}, {S1 - 0.1:.2f});'); snd("whoosh.wav", S1 - 0.15, 0.35)
    T(f'tl.fromTo("#scene", {{opacity:0, scale:1.08}}, {{opacity:1, scale:1, duration:0.5, ease:"power3.out"}}, {S1:.2f});')
    IN("#count", S1 + 0.3, -30)

    # ---- the six words: the camera moves to the thing, Rafiq says it, the card comes up, the Urdu under it, the counter clicks ------
    cam = lambda t, k: T(f'tl.to("#world", {{x:{540 - CENTRE[k][0] * CENTRE[k][1]:.0f}, y:{(300 - FOCUS_Y[k]) * CENTRE[k][1] if k in FOCUS_Y else 0:.0f}, scale:{CENTRE[k][1]}, '
                         f'duration:0.9, ease:"power2.inOut"}}, {t:.2f});')
    T(f'tl.set("#world", {{x:{540 - CENTRE["talib"][0]:.0f}, y:0, scale:1, transformOrigin:"0 0"}}, 0);')
    for i, (k, ar, tr, en, ur, urs) in enumerate(WORDS):
        intro, after = ORDER[[n for n, _ in ORDER].index(k) - 1][0], ORDER[[n for n, _ in ORDER].index(k) + 1][0]
        if i: cam(L[intro] - 0.2, k); snd("whoosh.wav", L[intro] - 0.15, 0.3)
        t0 = L[k] - 0.1
        if i: T(f'tl.to("#card{i - 1}", {{opacity:0, y:-40, duration:0.3, ease:"power2.in"}}, {L[intro] - 0.1:.2f});')
        T(f'tl.fromTo("#card{i} .ar", {{opacity:0, scale:0.6}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.4)", transformOrigin:"50% 50%"}}, {t0:.2f});')
        T(f'tl.set("#card{i}", {{opacity:1, y:0}}, {t0:.2f});'); snd("tap.wav", t0 + 0.05, 0.4)
        IN(f"#card{i} .tr", t0 + 0.35, 20)
        ut = L[after] + (words(after)[-2][1] if len(words(after)) > 2 else 0.3)
        T(f'tl.fromTo("#card{i} .ur", {{opacity:0, x:80}}, {{opacity:1, x:0, duration:0.4, ease:"back.out(1.4)"}}, {ut - 0.1:.2f});'); snd("tick-lo.wav", ut, 0.45)
        T(f'tl.set("#cn", {{textContent:"{i + 1}"}}, {ut:.2f});')
        T(f'tl.fromTo("#count", {{scale:1}}, {{scale:1.15, duration:0.15, yoyo:true, repeat:1, ease:"power2.out", transformOrigin:"0% 50%", immediateRender:false}}, {ut:.2f});')
        snd("click.wav", ut, 0.9)
    # what happens in the scene on each word
    st = at("s1", "student")
    T(f'tl.fromTo(".stu", {{y:0}}, {{y:-18, duration:0.2, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {st:.2f});')
    kn = at("s2", "knowledge")
    T(f'tl.fromTo("#bulb", {{opacity:0, scale:0.4}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(1.6)", transformOrigin:"50% 50%"}}, {kn - 0.1:.2f});'); snd("shimmer.wav", kn, 0.35, 1.2)
    T(f'tl.to("#glow", {{opacity:0.35, duration:0.5, yoyo:true, repeat:3, ease:"sine.inOut"}}, {kn:.2f});')
    bk = at("s3", "book")
    T(f'tl.to("#bookC", {{opacity:0, duration:0.15, ease:"power2.in"}}, {bk - 0.1:.2f});')
    T(f'tl.fromTo("#bookO", {{opacity:0, scaleX:0.2}}, {{opacity:1, scaleX:1, duration:0.4, ease:"back.out(1.4)", transformOrigin:"50% 100%"}}, {bk - 0.05:.2f});'); snd("flip.wav", bk, 0.45)
    pn = at("s4", "pen")
    T(f'tl.to("#pen", {{y:-60, rotation:-35, duration:0.5, ease:"back.out(1.6)", transformOrigin:"50% 100%"}}, {pn - 0.3:.2f});'); snd("tap.wav", pn, 0.4)
    ma = at("s5", "maths")
    T(f'tl.fromTo("#sum1", {{opacity:0, x:-30}}, {{opacity:1, x:0, duration:0.4, ease:"power3.out"}}, {ma - 0.2:.2f});'); snd("tick-lo.wav", ma - 0.2, 0.35)
    T(f'tl.fromTo("#sum2", {{opacity:0, scale:0.5}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(1.6)", transformOrigin:"50% 50%"}}, {L["hisab"] + 0.2:.2f});'); snd("tap.wav", L["hisab"] + 0.2, 0.4)
    ex = at("s6", "exam")
    T(f'tl.fromTo("#ring", {{strokeDashoffset:1}}, {{strokeDashoffset:0, duration:0.5, ease:"power2.inOut"}}, {ex - 0.1:.2f});'); snd("thump.wav", ex, 0.4)
    T(f'tl.fromTo("#clock", {{rotation:-8}}, {{rotation:8, duration:0.06, yoyo:true, repeat:13, ease:"sine.inOut", transformOrigin:"50% 50%", immediateRender:false}}, {at("s6", "tomorrow"):.2f});')
    T(f'tl.set("#clock", {{rotation:0}}, {at("s6", "tomorrow") + 0.85:.2f});')
    T(f'tl.fromTo("#cal", {{rotation:0}}, {{rotation:-4, duration:0.12, yoyo:true, repeat:5, ease:"sine.inOut", transformOrigin:"50% 0%", immediateRender:false}}, {at("s6b", "nerves") - 0.2:.2f});')
    # the first verses mention the pen: back to the desk, the light comes in on the pen
    T(f'tl.to("#card5", {{opacity:0, y:-40, duration:0.3, ease:"power2.in"}}, {L["s7"] - 0.2:.2f});')
    T(f'tl.to("#world", {{x:0, y:{(300 - 600) * 1.3:.0f}, scale:1.3, duration:0.9, ease:"power2.inOut"}}, {L["s7"] - 0.2:.2f});'); snd("whoosh.wav", L["s7"] - 0.15, 0.3)
    pq = at("s7", "pen")
    T(f'tl.to("#beam", {{opacity:0.35, duration:0.8, ease:"power3.out"}}, {pq - 0.3:.2f});'); snd("shimmer.wav", pq, 0.35, 1.2)
    T(f'tl.fromTo(".spk", {{opacity:0, scale:0}}, {{opacity:1, scale:1, duration:0.35, stagger:0.1, ease:"back.out(1.4)", transformOrigin:"50% 50%"}}, {pq:.2f});')
    T(f'tl.fromTo("#sun", {{scale:1}}, {{scale:1.4, duration:0.8, yoyo:true, repeat:3, ease:"sine.inOut", transformOrigin:"50% 50%"}}, {pq:.2f});')

    # ---- the ayah: ash-Shuʿarāʾ 26:80, its two words lit as the line says them ------------------------------------------------------
    AY = L["ayah"] - 0.4
    POP("#aya", AY, 0.85); snd("flip.wav", AY, 0.4)
    T(f'tl.to("#aya .w1", {{color:"{RED}", duration:0.3, ease:"power2.out"}}, {L["ayah"] + 0.5:.2f});')
    T(f'tl.to("#aya .w2", {{color:"{TEAL}", duration:0.3, ease:"power2.out"}}, {L["ayah"] + 1.4:.2f});')
    IN("#aya .ee", L["s8"], 16)
    T(f'tl.to("#aya .t1", {{color:"{RED}", duration:0.3}}, {at("s8", "taught"):.2f});'); T(f'tl.to("#aya .t2", {{color:"{TEAL}", duration:0.3}}, {at("s8", "pen"):.2f});')
    # ---- the six together, the score, the ask ------------------------------------------------------------------------------------
    SX = at("s8", "six") - 0.2
    T(f'tl.to("#aya, #count", {{opacity:0, y:-40, duration:0.3, ease:"power2.in"}}, {SX - 0.15:.2f});'); snd("whoosh.wav", SX - 0.15, 0.3)
    T(f'tl.to("#scene", {{opacity:0.25, duration:0.4, ease:"power2.in"}}, {SX - 0.15:.2f});')
    IN("#fin .ttl", SX, 30)
    for i in range(6):
        POP(f"#fin .g{i}", SX + 0.15 + i * 0.12, 0.6); snd("click.wav", SX + 0.15 + i * 0.12, 0.5)
    POP("#ask", at("s8", "how") - 0.1, 0.8); snd("tick-lo.wav", at("s8", "how"), 0.45)
    POP("#url", at("s8", "comment"), 0.8)
    T(f'tl.fromTo("#arr", {{opacity:0, y:0}}, {{opacity:1, y:18, duration:0.4, yoyo:true, repeat:3, ease:"sine.inOut"}}, {at("s8", "comment"):.2f});')

    # captions: Callum's lines, word by word, low in the frame
    caps = ""; k = 0
    for n in L:
        if n in ARABIC or n == HOOK: continue
        ws = words(n); chunk = []
        for i, (w, s, e) in enumerate(ws):
            chunk.append((w, s))
            if w[-1] in ",.:?!" or len(chunk) >= 6 or i + 1 == len(ws):
                nxt = L[n] + ws[i + 1][1] if i + 1 < len(ws) else L[n] + e + 0.4
                caps += f'<div class="cap" id="cp{k}">' + " ".join(f'<span id="cp{k}w{j}">{x}</span>' for j, (x, _) in enumerate(chunk)) + "</div>"
                T(f'tl.set("#cp{k}", {{opacity:1}}, {L[n] + chunk[0][1] - 0.02:.2f});')
                for j, (x, s0) in enumerate(chunk): T(f'tl.fromTo("#cp{k}w{j}", {{opacity:0, y:10}}, {{opacity:1, y:0, duration:0.2, ease:"power3.out"}}, {L[n] + s0:.2f});')
                T(f'tl.to("#cp{k}", {{opacity:0, duration:0.15, ease:"power2.in"}}, {nxt - 0.18:.2f});'); k += 1; chunk = []

    cards = "".join(f'<div class="card" id="card{i}"><div class="ar">{ar}</div><div class="tr">{tr} · {en}</div>'
                    f'<div class="ur"><span class="tag">Urdu</span><b>{ur}</b><i>{urs}</i></div></div>' for i, (k_, ar, tr, en, ur, urs) in enumerate(WORDS))
    grid = "".join(f'<div class="g g{i}"><b>{ar}</b><span>{en}</span></div>' for i, (k_, ar, tr, en, ur, urs) in enumerate(WORDS))
    css = f"""
@font-face {{ font-family:"FR"; src:url("assets/fredoka-latin-600-normal.woff2"); font-weight:600; }}
@font-face {{ font-family:"FR"; src:url("assets/fredoka-latin-700-normal.woff2"); font-weight:700; }}
@font-face {{ font-family:"AM"; src:url("assets/amiri-arabic-700-normal.woff2"); }}
* {{ margin:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:{PAPER}; font-family:FR; font-weight:600; color:{INK}; }}
#cam {{ position:absolute; inset:0; }}
#scene {{ position:absolute; inset:0; opacity:0; }}
#view {{ position:absolute; left:0; top:0; width:1080px; height:1180px; overflow:hidden; border-bottom:8px solid {INK}; }}
#world {{ position:absolute; left:0; top:0; width:2160px; height:1180px; }}
#world svg {{ width:2160px; height:1180px; }}
#panel {{ position:absolute; left:0; top:1188px; width:1080px; height:732px; background:{PAPER};
  background-image:repeating-linear-gradient(-45deg, rgba(23,38,43,.04) 0 14px, transparent 14px 28px); }}
.card {{ position:absolute; left:0; right:0; top:1215px; text-align:center; opacity:0; }}
.card .ar {{ font-family:AM; font-size:190px; line-height:1.25; direction:rtl; color:{INK}; opacity:0; }}
.card .tr {{ font-size:50px; color:{TEAL}; margin-top:34px; opacity:0; }}
.card .ur {{ display:inline-flex; align-items:center; gap:18px; margin-top:18px; padding:6px 26px 6px 8px; border-radius:999px; background:#fff; border:4px solid {INK};
  box-shadow:0 6px 0 {INK}; opacity:0; }}
.card .ur .tag {{ padding:4px 18px; border-radius:999px; background:{TEAL}; color:#fff; font-size:34px; }}
.card .ur b {{ font-family:AM; font-size:64px; color:{RED}; direction:rtl; line-height:1.3; }} .card .ur i {{ font-style:normal; font-size:40px; color:{INK}; }}
#count {{ position:absolute; left:40px; top:150px; display:flex; align-items:center; gap:14px; padding:8px 26px 8px 10px; border-radius:999px; background:{GOLD};
  border:5px solid {INK}; box-shadow:0 6px 0 {INK}; opacity:0; z-index:4; }}
#count #cn {{ display:grid; place-items:center; width:74px; height:74px; border-radius:50%; background:{INK}; color:{GOLD}; font-size:48px; font-weight:700; }}
#count span {{ font-size:30px; line-height:1.05; }}
#logo {{ position:absolute; top:56px; left:0; right:0; display:flex; justify-content:center; gap:12px; align-items:center; z-index:6; }}
#logo .tl {{ position:relative; width:58px; height:58px; border-radius:16px; background:{INK}; display:grid; place-items:center; }}
#logo .tl span {{ font-family:AM; font-size:38px; color:{CREAM}; margin-top:-6px; }} #logo .tl em {{ position:absolute; right:9px; top:8px; width:9px; height:9px; border-radius:50%; background:{RED}; }}
#logo b {{ font-family:AM; font-size:44px; color:{INK}; padding:0 14px; border-radius:14px; background:rgba(251,246,234,.85); }}
.cap {{ position:absolute; left:60px; right:60px; top:1660px; text-align:center; font-size:46px; line-height:1.2; color:{INK}; opacity:0; z-index:5; }}
.cap span {{ display:inline-block; opacity:0; }}
#hook {{ position:absolute; inset:0; background:radial-gradient(ellipse at 50% 30%, #fffaf0 0%, {PAPER} 60%, #efe3c6 100%); z-index:3; }}
#big {{ position:absolute; left:0; right:0; top:380px; text-align:center; font-size:165px; font-weight:700; color:{RED}; letter-spacing:.01em;
  text-shadow:0 10px 0 {INK}; }}
.hl {{ position:absolute; left:60px; right:60px; text-align:center; font-size:72px; line-height:1.15; }} #hl1 {{ top:190px; }} #hl2 {{ top:610px; }}
.hl span {{ display:inline-block; opacity:0; }} .hl .em {{ color:{TEAL}; }}
#big .ring {{ position:absolute; left:50%; top:50%; width:300px; height:300px; margin:-150px; border-radius:50%; border:14px solid {GOLD}; opacity:0; }}
#big .ring.r2 {{ border-color:{RED}; border-width:8px; }}
#big .spark {{ position:absolute; left:50%; top:50%; width:110px; height:12px; margin-top:-6px; border-radius:6px; background:{GOLD}; transform-origin:0 50%; opacity:0; }}
#flash {{ position:absolute; inset:0; background:#fff; opacity:0; }}
.chip {{ position:absolute; width:290px; padding:10px 0 12px; border-radius:26px; background:#fff; border:4px solid {INK}; box-shadow:0 6px 0 {INK}; text-align:center; opacity:0; }}
.chip b {{ display:block; font-family:AM; font-size:64px; line-height:1.25; color:{INK}; }} .chip span {{ font-size:32px; color:{TEAL}; }}
#aya {{ position:absolute; left:60px; right:60px; top:1205px; padding:16px 24px 18px; border-radius:28px; background:#fff; border:5px solid {INK}; box-shadow:0 8px 0 {INK};
  text-align:center; opacity:0; }}
#aya .aa {{ font-family:AM; font-size:84px; line-height:1.55; direction:rtl; }} #aya .ee {{ font-size:38px; line-height:1.25; opacity:0; }}
#aya small {{ display:block; font-size:28px; color:#6b5a44; margin-top:8px; }}
#fin {{ position:absolute; left:0; right:0; top:200px; text-align:center; z-index:4; }}
#fin .ttl {{ font-size:84px; font-weight:700; line-height:1.05; opacity:0; }} #fin .ttl em {{ font-style:normal; color:{RED}; }}
#fin .grid {{ display:grid; grid-template-columns:repeat(3, 300px); gap:22px; justify-content:center; margin-top:40px; }}
.g {{ padding:10px 0 14px; border-radius:24px; background:#fff; border:4px solid {INK}; box-shadow:0 6px 0 {INK}; opacity:0; }}
.g b {{ display:block; font-family:AM; font-size:76px; line-height:1.3; }} .g span {{ font-size:32px; color:{TEAL}; }}
#ask {{ position:absolute; left:0; right:0; top:1030px; text-align:center; font-size:66px; font-weight:700; opacity:0; z-index:4; }}
#url {{ position:absolute; left:0; right:0; top:1150px; text-align:center; opacity:0; z-index:4; }}
#url span {{ display:inline-block; padding:10px 34px; border-radius:999px; background:{TEAL}; color:#fff; font-size:48px; border:4px solid {INK}; box-shadow:0 6px 0 {INK}; }}
#arr {{ position:absolute; left:0; right:0; top:1250px; text-align:center; font-size:80px; opacity:0; z-index:4; }}
"""
    body = f"""<div id="cam">
<div id="scene"><div id="view"><div id="world"><svg viewBox="0 0 2160 1180">{WORLD}</svg></div></div><div id="panel"></div>
 {cards}
 <div id="aya"><div class="aa">الَّذِي <span class="w1">عَلَّمَ</span> <span class="w2">بِالْقَلَمِ</span></div>
  <div class="ee">“He who <span class="t1">taught</span> by the <span class="t2">pen</span>”</div><small>the Qur’an · al-ʿAlaq 96:4</small></div>
</div>
<div id="count"><div id="cn">0</div><span>Arabic words<br>you already know</span></div>
<div id="logo"><span class="tl"><span>ر</span><em></em></span><b>رَفِيق</b></div>
<div id="hook"><div class="hl" id="hl1">{hl[1]}</div><div id="big">HUNDREDS{fx}</div><div class="hl" id="hl2">{hl[2]}</div>{chips}<div id="flash"></div></div>
<div id="fin"><div class="ttl">You already knew<br><em>6 Arabic words!</em></div><div class="grid">{grid}</div></div>
<div id="ask">How many did you get? 👇</div><div id="url"><span>rafiq-arabic.com</span></div><div id="arr">👇</div>
{caps}</div>"""
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><title>urdu school</title>
<script src="assets/gsap.min.js"></script><style>{css}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{END}">
{body}
{chr(10).join(au)}
</div><script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;</script></body></html>
""")
    print("built", END, "s,", len(au), "sounds;", {k: float(v) for k, v in L.items()})

if __name__ == "__main__":
    build()
