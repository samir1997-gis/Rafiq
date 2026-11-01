#!/usr/bin/env python3
"""If you speak Urdu, you already know these Arabic words: at the doctor's (owner, 1 Nov 2026, #313: "make me a video like this but in our
own style", after a reel set in a courtroom). Our own scene, colours and voices: a drawn clinic wider than the screen, the camera easing
from one thing to the next as each word is said, the word in Arabic with its Urdu spelling underneath, and a counter of the Arabic
words you already know that clicks up with every one:
  hook  "If you speak Urdu, you already know HUNDREDS of Arabic words!" (Callum; HUNDREDS shouted and slammed on: crash, boom, its echo, the shake)
  1 مَرِيض the patient · 2 طَبِيب the doctor · 3 دَواء the medicine · 4 عِلاج the treatment · 5 صِحَّة health · 6 شِفاء the cure
  then ash-Shuʿarāʾ 26:80 وَإِذا مَرِضْتُ فَهُوَ يَشْفِينِ, the six words together and the ask (comment your score). Then the cream end card.
Voices: brag-quiz/voice/urdu-doctor-lines.json (Callum; Rafiq says the Arabic, levelled with Callum). Figures are faceless (owner, 27 Oct).

  python3 brag-quiz/reels/urdu-doctor/build.py    then  cd brag-quiz/reels/urdu-doctor/out/v && npx hyperframes render -o ../raw.mp4
"""
import json, os, re, shutil, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
V6 = os.path.join(ROOT, "brag-output-v6/composition/assets"); VO = os.path.join(ROOT, "brag-quiz/voice/urdu-doctor")
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
    said = re.sub(r"\[[^]]*\]", "", SCRIPT.get(n, "")).replace("...", "… ").split()
    if len(said) == len(ws): ws = [[s, w[1], w[2]] for s, w in zip(said, ws)]   # the script's spelling (Urdu, ʿilāj), whisper's timing
    return [tuple(w) for w in ws]
SCRIPT = {l["file"]: l["text"] for l in json.load(open(os.path.join(ROOT, "brag-quiz/voice/urdu-doctor-lines.json")))}
WORDS = [   # file, Arabic, transliteration, meaning, Urdu spelling, Urdu said
    ("marid", "مَرِيض", "marīḍ", "patient", "مریض", "mareez"), ("tabib", "طَبِيب", "ṭabīb", "doctor", "طبیب", "tabeeb"),
    ("dawa", "دَواء", "dawā’", "medicine", "دوا", "dawa"), ("ilaj", "عِلاج", "‘ilāj", "treatment", "علاج", "ilaaj"),
    ("sihha", "صِحَّة", "ṣiḥḥa", "health", "صحت", "sehat"), ("shifa", "شِفاء", "shifā’", "cure", "شفا", "shifa")]
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
ORDER = [(HOOK, 0.25), ("s1", 0.5), ("marid", 0.25), ("s1b", 0.3), ("s2", 0.45), ("tabib", 0.25), ("s2b", 0.3), ("s3", 0.45), ("dawa", 0.25),
         ("s3b", 0.3), ("s4", 0.45), ("ilaj", 0.25), ("s4b", 0.3), ("s5", 0.45), ("sihha", 0.25), ("s5b", 0.3), ("s6", 0.45), ("shifa", 0.25),
         ("s6b", 0.3), ("ayah", 0.35), ("s7", 0.4)]
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

# ---- the clinic: 2160 wide, the camera shows 1080 of it ---------------------------------------------------------------------------
O = f'stroke="{INK}" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"'
def person(x, y, s, coat, cls="", extra="", head=None):           # faceless, flat, ink outline (as build_pop_carousel.py)
    return (f'<g transform="translate({x},{y}) scale({s})"><g class="{cls}">'
            f'<path d="M-70 0 L -60 -170 C -56 -210 56 -210 60 -170 L 70 0 Z" fill="{coat}" {O}/>'
            f'<rect x="-48" y="0" width="34" height="110" rx="10" fill="{INK}"/><rect x="14" y="0" width="34" height="110" rx="10" fill="{INK}"/>'
            f'<circle cx="0" cy="-250" r="52" fill="#C98E62" {O}/>{head or ""}{extra}</g></g>')   # animate the inner group: the outer one places it
HAIR = f'<path d="M-52 -258 C -56 -310 56 -310 52 -258 C 36 -280 -36 -280 -52 -258 Z" fill="{INK}"/>'
CAP = f'<path d="M-50 -268 C -50 -318 50 -318 50 -268 Z" fill="#ffffff" {O}/>'
STETH = f'<path d="M-30 -190 C -40 -120 40 -120 30 -190 M0 -134 L 0 -96" fill="none" stroke="{INK}" stroke-width="7"/><circle cx="0" cy="-90" r="12" fill="{GOLD}" {O}/>'
def chair(x, y): return f'<g transform="translate({x},{y})"><rect x="-90" y="-30" width="180" height="30" rx="8" fill="{TEAL}" {O}/><rect x="-90" y="-150" width="30" height="130" rx="8" fill="{TEAL}" {O}/><path d="M-80 0 L -80 70 M 80 0 L 80 70" {O}/></g>'
WORLD = (
    f'<rect x="0" y="0" width="2160" height="1180" fill="{SKY}"/>'
    + "".join(f'<rect x="{x}" y="0" width="70" height="1180" fill="#bfdcd5" opacity=".5"/>' for x in range(60, 2160, 220))   # wallpaper
    + f'<rect x="0" y="880" width="2160" height="300" fill="#E9D9B4"/><path d="M0 880 L 2160 880" {O}/>'
    + "".join(f'<path d="M{x} 900 L {x + 40} 1180" stroke="#d8c59a" stroke-width="4"/>' for x in range(0, 2160, 120))
    # the window, its sky and the light that comes in for شِفاء
    + f'<g id="win"><rect x="820" y="140" width="380" height="440" rx="24" fill="#9fd0f0" {O}/><path d="M1010 140 L 1010 580 M 820 360 L 1200 360" {O}/>'
      f'<circle id="sun" cx="1120" cy="230" r="44" fill="{GOLD}"/></g>'
    + f'<path id="beam" d="M820 580 L 1200 580 L 1500 1180 L 560 1180 Z" fill="{GOLD}" opacity="0"/>'
    # the sign on the wall: a teal cross
    + f'<g transform="translate(330,240)"><rect x="-90" y="-90" width="180" height="180" rx="30" fill="{PAPER}" {O}/><path d="M-22 -60 L 22 -60 L 22 -22 L 60 -22 L 60 22 L 22 22 L 22 60 L -22 60 L -22 22 L -60 22 L -60 -22 L -22 -22 Z" fill="{TEAL}" {O}/></g>'
    # the patient on his chair; feeling ill (the swirl and the ice pack), then well (stands, the sparkles)
    + chair(380, 900)
    + person(380, 820, 1.0, "#E2B04A", "pat", head=HAIR + f'<rect id="ice" x="-46" y="-330" width="92" height="34" rx="14" fill="#e8f6ff" {O}/>')
    + f'<g id="ill" transform="translate(380,480)">' + "".join(f'<path d="M{-40 + i * 40} 0 c 10 -20 -10 -30 0 -50" fill="none" stroke="#6aa86a" stroke-width="7" stroke-linecap="round"/>' for i in range(3)) + '</g>'
    # the doctor and the desk
    + person(1560, 790, 1.05, "#ffffff", "doc", head=CAP, extra=STETH)
    + f'<g transform="translate(1720,880)"><rect x="-260" y="-200" width="520" height="40" rx="10" fill="#c98a4a" {O}/><rect x="-240" y="-160" width="480" height="160" fill="#d9a066" {O}/></g>'
    # the medicine on the desk (pops on), the clipboard (the treatment)
    + f'<g transform="translate(1800,680)"><g id="bottle"><rect x="-40" y="-100" width="80" height="100" rx="14" fill="{RED}" {O}/><rect x="-32" y="-128" width="64" height="30" rx="8" fill="#ffffff" {O}/>'
      f'<rect x="-30" y="-74" width="60" height="40" rx="6" fill="{PAPER}"/><circle cx="64" cy="-12" r="14" fill="#ffffff" {O}/><circle cx="96" cy="-12" r="14" fill="{GOLD}" {O}/></g></g>'
    + f'<g id="clip" transform="translate(1900,420)"><rect x="-110" y="-150" width="220" height="300" rx="16" fill="{PAPER}" {O}/><rect x="-50" y="-170" width="100" height="40" rx="10" fill="{TEAL}" {O}/>'
      + "".join(f'<path class="tk" pathLength="1" d="M-80 {-80 + i * 70} l 18 18 l 30 -36" fill="none" stroke="{TEAL}" stroke-width="10" stroke-dasharray="1" stroke-dashoffset="1"/>'
                f'<rect x="-20" y="{-74 + i * 70}" width="100" height="12" rx="6" fill="#cdb991"/>' for i in range(4)) + '</g>'
    # health: a heart that beats over the patient
    + f'<g transform="translate(380,430)"><path id="heart" d="M0 30 C -60 -10 -50 -70 0 -40 C 50 -70 60 -10 0 30 Z" fill="{RED}" {O} opacity="0"/></g>'
    + "".join(f'<g transform="translate({x},{y})"><path class="spk" d="M0 -26 C 4 -6 6 -4 26 0 C 6 4 4 6 0 26 C -4 6 -6 4 -26 0 C -6 -4 -4 -6 0 -26 Z" fill="{GOLD}" opacity="0"/></g>'
              for x, y in ((260, 470), (520, 440), (230, 640), (540, 640))))
CENTRE = {"marid": (380, 1.0), "tabib": (1560, 1.0), "dawa": (1800, 1.5), "ilaj": (1900, 1.35), "sihha": (380, 1.0), "shifa": (1010, 1.0)}
FOCUS_Y = {"dawa": 620, "ilaj": 420}

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
    target = lv(mp3("s7"))                                                   # Rafiq's Arabic level with Callum (the standard)
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
    CHIPS = [("كِتاب", "kitab"), ("وَقْت", "waqt"), ("دُنْيا", "duniya"), ("عِلْم", "ilm"), ("صَبْر", "sabr"), ("قَلَم", "qalam"), ("خَبَر", "khabar"),
             ("شُكْر", "shukr"), ("إِنْسان", "insaan"), ("حَال", "haal"), ("عَقْل", "aql"), ("فِكْر", "fikr")]
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
    T(f'tl.set("#world", {{x:{540 - 380:.0f}, y:0, scale:1, transformOrigin:"0 0"}}, 0);')
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
    T(f'tl.fromTo("#ill path", {{y:0, opacity:0.4}}, {{y:-16, opacity:1, duration:0.6, yoyo:true, repeat:9, stagger:0.15, ease:"sine.inOut"}}, {L["s1"]:.2f});')
    T(f'tl.fromTo(".pat", {{rotation:0}}, {{rotation:-3, duration:0.5, yoyo:true, repeat:7, ease:"sine.inOut", transformOrigin:"50% 100%", immediateRender:false}}, {L["s1"]:.2f});')
    T(f'tl.fromTo(".doc", {{y:0}}, {{y:-18, duration:0.2, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {L["tabib"]:.2f});')
    T(f'tl.fromTo("#bottle", {{opacity:0, y:-80}}, {{opacity:1, y:0, duration:0.45, ease:"back.out(1.4)"}}, {at("s3", "medicine") - 0.1:.2f});'); snd("thump.wav", at("s3", "medicine"), 0.4)
    T(f'tl.fromTo("#clip .tk", {{strokeDashoffset:1}}, {{strokeDashoffset:0, duration:0.25, stagger:0.18, ease:"power2.out"}}, {at("s4", "treatment"):.2f});')
    for k in range(4): snd("tap.wav", at("s4", "treatment") + k * 0.18, 0.25)
    hl_ = at("s5", "health")
    T(f'tl.to("#ill, #ice", {{opacity:0, duration:0.3, ease:"power2.in"}}, {L["s5"]:.2f});')
    T(f'tl.fromTo(".pat", {{y:0}}, {{y:-60, duration:0.35, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {hl_ - 0.2:.2f});')
    T(f'tl.fromTo("#heart", {{opacity:0, scale:0.4}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(1.4)", transformOrigin:"50% 50%"}}, {hl_:.2f});')
    T(f'tl.to("#heart", {{scale:1.15, duration:0.25, yoyo:true, repeat:5, ease:"sine.inOut"}}, {hl_ + 0.45:.2f});')
    T(f'tl.fromTo(".spk", {{opacity:0, scale:0}}, {{opacity:1, scale:1, duration:0.35, stagger:0.1, ease:"back.out(1.4)", transformOrigin:"50% 50%"}}, {hl_ + 0.1:.2f});'); snd("shimmer.wav", hl_, 0.3, 1.2)
    T(f'tl.to("#beam", {{opacity:0.35, duration:0.8, ease:"power3.out"}}, {L["shifa"]:.2f});'); snd("shimmer.wav", L["shifa"], 0.35, 1.2)
    T(f'tl.fromTo("#sun", {{scale:1}}, {{scale:1.4, duration:0.8, yoyo:true, repeat:3, ease:"sine.inOut", transformOrigin:"50% 50%"}}, {L["shifa"]:.2f});')

    # ---- the ayah: ash-Shuʿarāʾ 26:80, its two words lit as the line says them ------------------------------------------------------
    AY = L["ayah"] - 0.4
    T(f'tl.to("#card5", {{opacity:0, y:-40, duration:0.3, ease:"power2.in"}}, {AY - 0.1:.2f});')
    POP("#aya", AY, 0.85); snd("flip.wav", AY, 0.4)
    T(f'tl.to("#aya .w1", {{color:"{RED}", duration:0.3, ease:"power2.out"}}, {L["ayah"] + 0.5:.2f});')
    T(f'tl.to("#aya .w2", {{color:"{TEAL}", duration:0.3, ease:"power2.out"}}, {L["ayah"] + 1.4:.2f});')
    IN("#aya .ee", L["s7"], 16)
    T(f'tl.to("#aya .t1", {{color:"{RED}", duration:0.3}}, {at("s7", "ill"):.2f});'); T(f'tl.to("#aya .t2", {{color:"{TEAL}", duration:0.3}}, {at("s7", "cures"):.2f});')
    # ---- the six together, the score, the ask ------------------------------------------------------------------------------------
    SX = at("s7", "six") - 0.2
    T(f'tl.to("#aya, #count", {{opacity:0, y:-40, duration:0.3, ease:"power2.in"}}, {SX - 0.15:.2f});'); snd("whoosh.wav", SX - 0.15, 0.3)
    T(f'tl.to("#scene", {{opacity:0.25, duration:0.4, ease:"power2.in"}}, {SX - 0.15:.2f});')
    IN("#fin .ttl", SX, 30)
    for i in range(6):
        POP(f"#fin .g{i}", SX + 0.15 + i * 0.12, 0.6); snd("click.wav", SX + 0.15 + i * 0.12, 0.5)
    POP("#ask", at("s7", "how") - 0.1, 0.8); snd("tick-lo.wav", at("s7", "how"), 0.45)
    POP("#url", at("s7", "comment"), 0.8)
    T(f'tl.fromTo("#arr", {{opacity:0, y:0}}, {{opacity:1, y:18, duration:0.4, yoyo:true, repeat:3, ease:"sine.inOut"}}, {at("s7", "comment"):.2f});')

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
.card .tr {{ font-size:50px; color:{TEAL}; margin-top:-6px; opacity:0; }}
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
 <div id="aya"><div class="aa">وَإِذا <span class="w1">مَرِضْتُ</span> فَهُوَ <span class="w2">يَشْفِينِ</span></div>
  <div class="ee">“And when I am <span class="t1">ill</span>, it is He who <span class="t2">cures</span> me”</div><small>the Qur’an · ash-Shuʿarāʾ 26:80</small></div>
</div>
<div id="count"><div id="cn">0</div><span>Arabic words<br>you already know</span></div>
<div id="logo"><span class="tl"><span>ر</span><em></em></span><b>رَفِيق</b></div>
<div id="hook"><div class="hl" id="hl1">{hl[1]}</div><div id="big">HUNDREDS{fx}</div><div class="hl" id="hl2">{hl[2]}</div>{chips}<div id="flash"></div></div>
<div id="fin"><div class="ttl">You already knew<br><em>6 Arabic words!</em></div><div class="grid">{grid}</div></div>
<div id="ask">How many did you get? 👇</div><div id="url"><span>rafiq-arabic.com</span></div><div id="arr">👇</div>
{caps}</div>"""
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><title>urdu doctor</title>
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
