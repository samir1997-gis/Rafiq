#!/usr/bin/env python3
"""h11-jamil, "beautiful" (owner, 10 Nov 2026), as motion graphics in our dark colours (the pastel page is banned, FORMATS.md):
a desert at golden hour in deep teal and gold, lit and textured (sky gradient, a low sun with bloom, layered dunes with gold rim light,
film grain, drifting dust), camels walking in backlit silhouette, the camera moving through it in parallax.

  hook    "In Arabic, beautiful and camel are built from the SAME! three letters" (Callum, SAME shouted): SAME huge on frame 0, slams
          into the line on the shout (crash, shake, rings, sparks, flash); جَمِيل and جَمَل on their words; the three root tiles
  b1      جَمِيل big and glowing, a light sweep; its letters ج م ل lift into tiles, one on each name (Rafiq says جَمِيل)
  b2      the vowels change: جَمِيل → جَمَل; a camel walks across the sun (Rafiq says جَمَل)
  b3      a herd on the ridge, "beauty" and "wealth"; an-Naḥl 16:6 on a glass card, al-Ḥuṣarī reciting, then its meaning
  b4      words float like lanterns and gather into one line: جُمْلَة, a sentence (Rafiq says جُمْلَة)
  t1      your turn: the hadith (Muslim 91, Rafiq reads it), CAMELS or BEAUTY, 3-2-1 with a click each, BEAUTY revealed
  end     the comment ask, heard in full

  python3 brag-quiz/reels/jamil/build.py      then  cd brag-quiz/reels/jamil/out/v && npx -y hyperframes@0.9.30 render -o ../raw.mp4
"""
import json, math, os, random, re, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
V6 = os.path.join(ROOT, "brag-output-v6/composition/assets"); VO = os.path.join(ROOT, "brag-quiz/voice/jamil")
FONTS, SFX = os.path.join(ROOT, "brag-quiz/fonts"), os.path.join(ROOT, "brag-quiz/sfx")
TEAL, INK, GOLD, GOLD2, CREAM, RED = "#14232a", "#0b171b", "#E9B949", "#f6d27a", "#F1ECE0", "#e0574d"
HOOK = os.environ.get("HOOK", "hs1")
dur = lambda f: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
OUT = os.path.join(HERE, "out", "v"); A = os.path.join(OUT, "assets")

def words(n):
    """[(word, start)] for a line: the saved timings, or faster-whisper's (saved next to the line)"""
    f = os.path.join(VO, n + ".words.json")
    if not os.path.exists(f):
        from faster_whisper import WhisperModel
        s, _ = WhisperModel("base.en", compute_type="int8").transcribe(os.path.join(VO, n + ".mp3"), word_timestamps=True)
        json.dump([[w.word.strip(), round(float(w.start), 2)] for x in s for w in x.words], open(f, "w"))
    return [tuple(w[:2]) for w in json.load(open(f))]

# the lines in order: (name, audio file in assets, pause before it)
SEQ = [(HOOK, 0.1), ("b1", 0.45), ("jamil", 0.15), ("b2", 0.35), ("jamal", 0.15), ("b3", 0.5), ("nahl", 0.2), ("b3b", 0.25),
       ("b4", 0.5), ("jumla", 0.15), ("t1a", 0.5), ("hadith", 0.2), ("t1b", 0.25), ("b5", 3.4), ("end", 0.45)]
# the captions: the words as said, one token per spoken word ("+" glues a token to the next one); *gold
CAPS = {
 "b1": "This is *jamīl: *beautiful. Its three root letters: *jīm, *mīm, *lām.",
 "b2": "Keep those three letters, change the vowels, and you get *jamal: a *camel.",
 "b3": "To the Arabs, a herd of camels was *beauty and *wealth in one. Allah even says it about livestock:",
 "b3b": "“And for you there is *beauty in them.”",
 "b4": "The same letters give you *jumla, a *sentence: many words, gathered into one.",
 "t1a": "Your turn. The Prophet, peace be upon him, said: “Allah is *jamīl, and He loves al-+ *jamāl.”",
 "t1b": "Is al-+ *jamāl camels, or beauty?",
 "b5": "*Beauty. Allah is beautiful, and He loves *beauty.",
 "end": "*Tag someone beautiful. Just maybe don't call them a *camel.",
}
CHUNK = {"b1": [3, 1, 4, 3], "b2": [4, 3, 6], "b3": [3, 4, 6, 6], "b3b": [4, 4], "b4": [3, 3, 2, 5], "t1a": [2, 7, 3, 5],
         "t1b": [4, 2], "b5": [1, 3, 4], "end": [3, 7]}          # how many tokens each caption chunk holds

def build():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(A)
    for f in ("fredoka-latin-700-normal.woff2", "amiri-arabic-700-normal.woff2", "anton-latin-400-normal.woff2"): shutil.copy(os.path.join(FONTS, f), A)
    shutil.copy(os.path.join(V6, "lib/gsap.min.js"), A)
    for f in ("swoosh.wav", "swoosh-low.wav", "short-swoosh.wav", "click.wav", "tap.wav", "flash-flicker.wav"): shutil.copy(os.path.join(SFX, "ref", f), A)
    for f in ("shimmer.wav", "impact.wav", "thump.wav", "rumble.wav", "chalk.wav"): shutil.copy(os.path.join(SFX, "soft", f), A)
    for f in ("crash.wav", "boom.wav"): shutil.copy(os.path.join(SFX, f), A)
    # the voices, levelled: Callum and Rafiq level with each other (-19 LUFS each; the whole mix goes to -16 after the render)
    src = {n: os.path.join(VO, n + ".mp3") for n, _ in SEQ}
    src["nahl"] = os.path.join(VO, "nahl-16-6-part.mp3")
    T1CUT = 7.3                                                  # t1 split before "Is al-jamāl…", so Rafiq reads the hadith in between
    for part, args in (("t1a", ["-t", str(T1CUT)]), ("t1b", ["-ss", str(T1CUT)])):
        src[part] = os.path.join(A, part + "-raw.wav")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(VO, "t1.mp3"), *args, src[part]], check=True)
    for n, f in src.items():
        tgt = -19.0
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f, "-af", f"aresample=48000,loudnorm=I={tgt}:TP=-2:LRA=11,aresample=48000", "-ar", "48000", os.path.join(A, n + ".wav")], check=True)
    for part in ("t1a", "t1b"): os.remove(src[part])
    W = {n: words(n) for n in CAPS if n not in ("t1a", "t1b")}
    t1 = words("t1"); W["t1a"] = [(w, s) for w, s in t1 if s < T1CUT]; W["t1b"] = [(w, s - T1CUT) for w, s in t1 if s >= T1CUT]
    W[HOOK] = words(HOOK)

    L, t = {}, 0.0                                               # when each line starts
    for n, gap in SEQ:
        t += gap; L[n] = round(t, 2); t += dur(os.path.join(A, n + ".wav"))
    END = round(t + 1.4, 2)
    def at(n, key, k=0):
        hits = [s for w, s in W[n] if key in w.lower()]
        return L[n] + hits[k]

    au = []
    def snd(name, t0, vol, d=None, track=None):
        d = d or dur(os.path.join(A, name))
        au.append(f'<audio id="s{len(au)}" src="assets/{name}" data-start="{max(0, t0):.3f}" data-duration="{d:.3f}" data-volume="{vol:.3f}" data-track-index="{track or 4 + len(au)}"></audio>')
    for n, _ in SEQ: snd(n + ".wav", L[n], 1.0, track=1)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", os.path.join(V6, "sfx-gen/fountain.mp3"), "-af",
                    f"atrim=0:{END},afade=t=in:d=0.6,afade=t=out:st={END - 1.5}:d=1.5", "-c:a", "libmp3lame", "-q:a", "3", os.path.join(A, "bed.mp3")], check=True)
    snd("bed.mp3", 0, 0.1, END, track=2)                         # the fountain bed, so nothing is ever silent
    js = []; T = js.append
    fro = lambda sel, a, b, t0, ir=False: T(f'tl.fromTo("{sel}", {a}, {b[:-1] + ("" if ir else ", immediateRender:false")}}}, {t0:.2f});')   # the from state only once it starts
    to = lambda sel, b, t0: T(f'tl.to("{sel}", {b}, {t0:.2f});')
    cam = lambda x, y, s, d, t0, ease="power2.inOut": T(f'tl.to(CAM, {{x:{x}, y:{y}, s:{s}, duration:{d}, ease:"{ease}", onUpdate:camSet}}, {t0:.2f});')
    def whip(t0):                                                 # between sections: a quick blur whip and a swoosh
        fro("#whip", "{opacity:0}", "{opacity:1, duration:0.12, yoyo:true, repeat:1, ease:\"power2.in\"}", t0 - 0.12)
        fro("#fg", "{filter:\"blur(0px)\"}", "{filter:\"blur(14px)\", duration:0.12, yoyo:true, repeat:1, ease:\"power2.in\"}", t0 - 0.12)
        snd("swoosh.wav", t0 - 0.2, 0.45)

    # ---- the hook: the line word by word at the top, SAME huge from frame 0, slamming on the shout ----
    hw = W[HOOK]; same_i = next(i for i, (w, s) in enumerate(hw) if "same" in w.lower())
    hook_tokens = [re.sub(r"[^A-Za-z',.]", "", w) for w, s in hw]
    hl = "".join((f'<br><span class="hw same" id="hw{i}">{w.upper()}</span><br>' if i == same_i else f'<span class="hw" id="hw{i}">{w}</span> ') for i, w in enumerate(hook_tokens))
    SAME = L[HOOK] + hw[same_i][1]
    for i, (w, s) in enumerate(hw):
        if i == same_i: continue
        side = -50 if i % 2 else 50
        fro(f"#hw{i}", "{opacity:0, x:%d, filter:\"blur(8px)\"}" % side, "{opacity:1, x:0, filter:\"blur(0px)\", duration:0.22, ease:\"power3.out\"}", L[HOOK] + s)
    T(f'tl.set("#hw{same_i}", {{opacity:1, scale:2.5, y:780, x:0, color:"{GOLD}"}}, 0);')     # frame 0: huge in the middle
    fro(f"#hw{same_i}", "{scale:2.5}", "{scale:2.7, duration:%.2f, ease:\"sine.inOut\"}" % max(0.3, SAME - 0.25), 0.01)   # it swells, waiting
    fro(f"#hw{same_i}", "{scale:2.7, y:780}", "{scale:1, y:0, duration:0.2, ease:\"power4.in\", immediateRender:false}", SAME - 0.18)
    snd("crash.wav", SAME, 0.75); snd("boom.wav", SAME, 0.5)
    T(f'tl.to("#world", {{keyframes:[{{x:-26, y:14}}, {{x:22, y:-18}}, {{x:-14, y:10}}, {{x:8, y:-6}}, {{x:0, y:0}}], duration:0.42, ease:"power1.out"}}, {SAME + 0.02:.2f});')
    fro(f"#hw{same_i}", "{scaleY:0.78, scaleX:1.18}", "{scaleY:1, scaleX:1, duration:0.4, ease:\"elastic.out(1.2,0.4)\", immediateRender:false}", SAME + 0.02)
    fro(".ring", "{scale:0.2, opacity:0.9}", "{scale:3.2, opacity:0, duration:0.7, ease:\"power2.out\", stagger:0.08}", SAME + 0.02)
    fro(".spark", "{x:0, y:0, opacity:1, scale:1}", "{x:(i, el) => +el.dataset.dx, y:(i, el) => +el.dataset.dy, opacity:0, scale:0.3, duration:0.6, ease:\"power3.out\"}", SAME + 0.02)
    fro("#flash", "{opacity:0.75}", "{opacity:0, duration:0.35, ease:\"power2.out\"}", SAME + 0.02)
    # the two words on their words, the three tiles on "three letters"
    bw, cw, th = at(HOOK, "beaut"), at(HOOK, "camel"), at(HOOK, "three")
    fro("#hjamil", "{opacity:0, y:40, scale:0.8}", "{opacity:1, y:0, scale:1, duration:0.45, ease:\"back.out(1.7)\"}", bw); snd("short-swoosh.wav", bw, 0.3)
    fro("#hjamal", "{opacity:0, y:40, scale:0.8}", "{opacity:1, y:0, scale:1, duration:0.45, ease:\"back.out(1.7)\"}", cw); snd("short-swoosh.wav", cw, 0.3)
    fro(".htile", "{opacity:0, y:60, rotationX:-70}", "{opacity:1, y:0, rotationX:0, duration:0.5, ease:\"back.out(1.6)\", stagger:0.12}", th)
    for k in range(3): snd("click.wav", th + 0.12 * k, 0.35)
    fro("#hjamil .ar b, #hjamal .ar b", "{color:\"%s\"}" % CREAM, "{color:\"%s\", duration:0.3, stagger:0.04}" % RED, th + 0.4)
    cam(560, 0, 1.06, L["b1"] - 0.2, 0.0, "sine.inOut")            # a slow push from frame 0
    T(f'tl.to("#hook, #hjamil, #hjamal, #htiles", {{opacity:0, y:-40, duration:0.35, ease:"power2.in"}}, {L["b1"] - 0.3:.2f});')
    whip(L["b1"])

    # ---- b1: jamīl, its three letters lifting into tiles ----
    fro("#big", "{opacity:0, scale:0.7, filter:\"blur(20px)\"}", "{opacity:1, scale:1, filter:\"blur(0px)\", duration:0.6, ease:\"power3.out\"}", L["b1"] - 0.05)
    T(f'tl.set("#bigA", {{opacity:1}}, {L["b1"] - 0.05:.2f});')
    fro("#sweep", "{x:-900}", "{x:900, duration:1.1, ease:\"power2.inOut\"}", at("b1", "jamil") + 0.1); snd("shimmer.wav", at("b1", "jamil"), 0.35)
    fro("#bigEn", "{opacity:0, y:20}", "{opacity:1, y:0, duration:0.4, ease:\"power3.out\"}", at("b1", "beaut"))
    rt = at("b1", "root")
    to("#bigA", "{opacity:0.28, scale:0.9, duration:0.5, ease:\"power2.inOut\"}", rt)
    for k, key in enumerate(("jeam", "meme", "larm")):
        tk = at("b1", key)
        fro(f"#t{k}", "{opacity:0, y:-140, scale:0.6}", "{opacity:1, y:0, scale:1, duration:0.5, ease:\"back.out(1.8)\"}", tk - 0.1)
        fro(f"#t{k} .glow", "{opacity:1}", "{opacity:0.35, duration:0.8, ease:\"power2.out\"}", tk + 0.3)
        snd("click.wav", tk, 0.45); snd("chalk.wav", tk - 0.05, 0.12)
    cam(520, -20, 1.12, 3, L["b1"] + 1, "sine.inOut")
    fro("#bigA", "{opacity:0.28, scale:0.9}", "{opacity:1, scale:1.06, duration:0.35, ease:\"back.out(2)\", immediateRender:false}", L["jamil"] - 0.05)  # Rafiq says it
    to("#bigA", "{scale:1, duration:0.5, ease:\"power2.out\"}", L["jamil"] + 0.35)

    # ---- b2: change the vowels: jamīl → jamal; a camel walks across the sun ----
    cv = at("b2", "chang")
    fro(".tile .mk", "{opacity:0, y:-20}", "{opacity:1, y:0, duration:0.3, ease:\"back.out(2)\", stagger:0.08}", cv)
    to(".tile .mk", "{opacity:0, y:20, duration:0.25, ease:\"power2.in\", stagger:0.08}", cv + 0.9)
    snd("tap.wav", cv, 0.3); snd("tap.wav", cv + 0.9, 0.3)
    jm = at("b2", "jamal")
    to("#bigA", "{opacity:0, scale:0.8, filter:\"blur(14px)\", duration:0.3, ease:\"power2.in\"}", jm - 0.3)
    to("#bigEn", "{opacity:0, duration:0.25, ease:\"power2.in\"}", jm - 0.3)
    fro("#bigB", "{opacity:0, scale:1.3, filter:\"blur(14px)\"}", "{opacity:1, scale:1, filter:\"blur(0px)\", duration:0.4, ease:\"power3.out\"}", jm - 0.02)
    snd("impact.wav", jm, 0.4)
    fro("#bigEn2", "{opacity:0, y:20}", "{opacity:1, y:0, duration:0.4, ease:\"power3.out\"}", at("b2", "camel"))
    hc = at("b2", "change") + 0.3                                     # the hero camel walks in from the right, across the sun
    T(f'tl.fromTo("#hero", {{x:1500}}, {{x:620, duration:{L["b3"] + 0.5 - hc:.2f}, ease:"power1.out"}}, {hc:.2f});')
    cam(540, 120, 1.0, 1.6, at("b2", "camel") - 0.4, "power2.inOut")
    fro("#bigB", "{scale:1}", "{scale:1.08, duration:0.35, ease:\"back.out(2)\", yoyo:true, repeat:1}", L["jamal"])
    to("#word", "{opacity:0, y:-60, duration:0.4, ease:\"power2.in\"}", L["b3"] - 0.35)
    whip(L["b3"])

    # ---- b3: the herd on the ridge, beauty and wealth; an-Naḥl 16:6 ----
    cam(540, 260, 0.82, 2.2, L["b3"] - 0.2, "power3.inOut")         # pull back to the wide desert
    to("#hero", "{x:-500, duration:9, ease:\"none\"}", L["b3"] + 0.3)
    fro("#herd", "{x:900}", "{x:-700, duration:%.2f, ease:\"none\"}" % (L["b4"] - L["b3"] + 1.5), L["b3"] - 0.2, ir=True)
    for key, sel in (("beauty", "#chipB"), ("wealth", "#chipW")):
        tk = at("b3", key)
        fro(sel, "{opacity:0, scale:0.6, y:30}", "{opacity:1, scale:1, y:0, duration:0.45, ease:\"back.out(2)\"}", tk - 0.05); snd("tap.wav", tk, 0.4)
    to("#chipB, #chipW", "{opacity:0, y:-30, duration:0.35, ease:\"power2.in\"}", at("b3", "allah") - 0.1)
    lv = at("b3", "allah")
    fro("#ayah", "{opacity:0, y:120, rotationX:25}", "{opacity:1, y:0, rotationX:0, duration:0.7, ease:\"power3.out\"}", lv); snd("swoosh-low.wav", lv, 0.35)
    fro("#ayah .ar span", "{opacity:0, y:20}", "{opacity:1, y:0, duration:0.4, ease:\"power2.out\", stagger:0.55}", L["nahl"] + 0.15, ir=True)
    fro("#ayah .ul", "{scaleX:0}", "{scaleX:1, duration:0.5, ease:\"power3.out\"}", L["nahl"] + 1.4, ir=True); snd("shimmer.wav", L["nahl"] + 1.4, 0.3)
    fro("#ayah .en", "{opacity:0}", "{opacity:1, duration:0.4, ease:\"power2.out\"}", L["b3b"], ir=True)
    to("#ayah", "{opacity:0, y:-80, duration:0.4, ease:\"power2.in\"}", L["b4"] - 0.35)
    whip(L["b4"])

    # ---- b4: night: words float like lanterns, then gather into one sentence (jumla) ----
    to("#night", "{opacity:1, duration:1.6, ease:\"power2.inOut\"}", L["b4"] - 0.3)
    cam(540, -120, 1.0, 2, L["b4"] - 0.2, "power2.inOut")
    fro("#jumla", "{opacity:0, scale:0.8, filter:\"blur(16px)\"}", "{opacity:1, scale:1, filter:\"blur(0px)\", duration:0.55, ease:\"power3.out\"}", at("b4", "jumla") - 0.05)
    snd("impact.wav", at("b4", "jumla"), 0.35)
    fro("#jumlaEn", "{opacity:0, y:20}", "{opacity:1, y:0, duration:0.4, ease:\"power3.out\"}", at("b4", "sentence"))
    mw = at("b4", "many")
    fro(".lw", "{opacity:0, scale:0.4}", "{opacity:1, scale:1, duration:0.5, ease:\"back.out(1.7)\", stagger:0.1}", L["b4"] + 0.3)
    T(f'tl.to(".lw", {{y:"+=28", duration:1.4, ease:"sine.inOut", yoyo:true, repeat:1, stagger:0.15}}, {L["b4"] + 0.8:.2f});')
    gt = at("b4", "gather")
    T(f'tl.to(".lw", {{left:(i, el) => el.dataset.gx + "px", top:"1180px", rotation:0, scale:1, y:0, duration:0.8, ease:"power3.inOut", stagger:0.06}}, {gt - 0.15:.2f});')
    T(f'tl.to(".lw", {{background:"rgba(233,185,73,.0)", borderColor:"rgba(233,185,73,0)", duration:0.4, ease:"power2.out"}}, {gt + 0.75:.2f});')
    fro("#jline", "{scaleX:0}", "{scaleX:1, duration:0.6, ease:\"power3.out\"}", gt + 0.7); snd("shimmer.wav", gt + 0.6, 0.4); snd("swoosh-low.wav", gt - 0.15, 0.4)
    fro("#jumla", "{scale:1}", "{scale:1.08, duration:0.35, ease:\"back.out(2)\", yoyo:true, repeat:1}", L["jumla"])
    to("#jscene", "{opacity:0, y:-60, duration:0.4, ease:\"power2.in\"}", L["t1a"] - 0.35)
    whip(L["t1a"])

    # ---- t1: your turn: the hadith, CAMELS or BEAUTY, 3-2-1, BEAUTY ----
    to("#night", "{opacity:0.55, duration:1, ease:\"power2.inOut\"}", L["t1a"])
    fro("#turn", "{opacity:0, scale:1.6}", "{opacity:1, scale:1, duration:0.35, ease:\"back.out(2)\"}", L["t1a"]); snd("impact.wav", L["t1a"], 0.45)
    to("#turn", "{opacity:0, y:-40, duration:0.3, ease:\"power2.in\"}", at("t1a", "prophet") - 0.2)
    fro("#hadith", "{opacity:0, y:100}", "{opacity:1, y:0, duration:0.6, ease:\"power3.out\"}", at("t1a", "prophet") - 0.1); snd("swoosh-low.wav", at("t1a", "prophet") - 0.1, 0.3)
    fro("#hadith .ar span", "{opacity:0, y:16}", "{opacity:1, y:0, duration:0.35, ease:\"power2.out\", stagger:0.45}", L["hadith"] + 0.1, ir=True)
    fro("#hadith .q", "{color:\"%s\"}" % CREAM, "{color:\"%s\", duration:0.3, ease:\"power2.out\"}" % GOLD, L["hadith"] + 1.9)
    q = L["t1b"]
    for k, sel in enumerate(("#optC", "#optB")):
        tk = at("t1b", "camel") if k == 0 else at("t1b", "beauty")
        fro(sel, "{opacity:0, x:%d, scale:0.85}" % (-160 if k == 0 else 160), "{opacity:1, x:0, scale:1, duration:0.45, ease:\"back.out(1.8)\"}", tk - 0.1)
        snd("tap.wav", tk, 0.4)
    cd = L["t1b"] + dur(os.path.join(A, "t1b.wav")) + 0.2
    fro("#ring3", "{opacity:0, scale:0.6}", "{opacity:1, scale:1, duration:0.3, ease:\"back.out(2)\"}", cd - 0.1)
    fro("#ring3 .fg", "{strokeDashoffset:0}", "{strokeDashoffset:339, duration:3, ease:\"power1.inOut\"}", cd)
    for k in range(3):
        T(f'tl.set("#rnum", {{textContent:"{3 - k}"}}, {cd + k:.2f});'); snd("click.wav", cd + k, 0.6)
        fro("#rnum", "{scale:1.4}", "{scale:1, duration:0.4, ease:\"back.out(2)\", immediateRender:false}", cd + k)
    rv = L["b5"] - 0.1
    to("#ring3", "{opacity:0, scale:1.4, duration:0.35, ease:\"power2.in\"}", rv - 0.15)
    to("#optC", "{opacity:0.25, scale:0.92, filter:\"grayscale(1)\", duration:0.35, ease:\"power2.out\"}", rv)
    fro("#optB", "{scale:1}", "{scale:1.12, boxShadow:\"0 0 90px rgba(233,185,73,.8)\", borderColor:\"%s\", duration:0.4, ease:\"back.out(2.2)\"}" % GOLD, rv)
    fro("#flash", "{opacity:0.5}", "{opacity:0, duration:0.4, ease:\"power2.out\"}", rv); snd("shimmer.wav", rv, 0.55); snd("impact.wav", rv, 0.45)
    fro("#optB .tick", "{opacity:0, scale:0.3}", "{opacity:1, scale:1, duration:0.4, ease:\"back.out(2.5)\"}", rv + 0.1)
    to("#quiz", "{opacity:0, y:-60, duration:0.4, ease:\"power2.in\"}", L["end"] - 0.35)
    whip(L["end"])

    # ---- end: the comment ask ----
    to("#night", "{opacity:0, duration:1.2, ease:\"power2.inOut\"}", L["end"] - 0.3)
    cam(540, 180, 1.1, 2.5, L["end"] - 0.2, "power2.inOut")
    fro("#endc", "{opacity:0, scale:0.85}", "{opacity:1, scale:1, duration:0.5, ease:\"back.out(1.8)\"}", L["end"] - 0.05)
    T(f'tl.fromTo("#hero", {{x:-450}}, {{x:950, duration:6.5, ease:"none", immediateRender:false}}, {L["end"] - 0.4:.2f});')   # a camel walks across the sun at a steady pace
    snd("short-swoosh.wav", at("end", "camel") - 0.5, 0.3)
    T(f'tl.set("#endc", {{opacity:1}}, {END - 0.01:.2f});')

    # ---- the captions: word by word from alternating sides, with a blur; gold on the key words ----
    cap_html = ""
    for n, text in CAPS.items():
        toks = text.split(); ws = W[n]
        if len(toks) != len(ws): raise SystemExit(f"{n}: {len(toks)} caption tokens for {len(ws)} spoken words: {[w for w, _ in ws]}")
        sizes = CHUNK[n]; assert sum(sizes) == len(toks), (n, sum(sizes), len(toks))
        i = 0
        for c, size in enumerate(sizes):
            cid = f"c{n}{c}"; spans = ""
            for k in range(i, i + size):
                tok = toks[k]; glue = tok.endswith("+"); tok = tok.rstrip("+"); gold = "*" in tok; tok = tok.replace("*", "")
                spans += f'<span class="cw{" g" if gold else ""}" id="{cid}w{k - i}">{tok}</span>' + ("" if glue else " ")
            cap_html += f'<div class="cap" id="{cid}">{spans}</div>'
            start = L[n] + ws[i][1]
            nxt = L[n] + ws[i + size][1] if i + size < len(ws) else L[n] + dur(os.path.join(A, n + ".wav")) + 0.25
            T(f'tl.set("#{cid}", {{opacity:1}}, {start - 0.02:.2f});')
            for k in range(size):
                side = -40 if (k % 2) else 40
                fro(f"#{cid}w{k}", "{opacity:0, x:%d, filter:\"blur(6px)\"}" % side, "{opacity:1, x:0, filter:\"blur(0px)\", duration:0.2, ease:\"power3.out\"}", L[n] + ws[i + k][1])
            T(f'tl.to("#{cid}", {{opacity:0, duration:0.12, ease:"power2.in"}}, {nxt - 0.06:.2f});')
            i += size

    # ---- the scene ----
    rnd = random.Random(7)
    stars = "".join(f'<circle cx="{rnd.uniform(0, 1080):.0f}" cy="{rnd.uniform(0, 900):.0f}" r="{rnd.uniform(0.8, 2.4):.1f}" fill="#fff6dd" opacity="{rnd.uniform(.3, .9):.2f}"/>' for _ in range(90))
    dust = "".join(f'<circle class="dst" cx="{rnd.uniform(0, 1080):.0f}" cy="{rnd.uniform(900, 1800):.0f}" r="{rnd.uniform(1.5, 4.5):.1f}" fill="#ffe7b0" opacity="{rnd.uniform(.15, .5):.2f}"/>' for _ in range(40))
    T(f'tl.fromTo(".dst", {{x:0, y:0}}, {{x:() => -120 - Math.random() * 120, y:() => -60 - Math.random() * 80, duration:{END}, ease:"none"}}, 0);')
    sparks = "".join(f'<div class="spark" data-dx="{math.cos(a) * r:.0f}" data-dy="{math.sin(a) * r:.0f}" style="transform:rotate({math.degrees(a):.0f}deg)"></div>'
                     for a, r in ((k * math.tau / 16 + 0.2, 300 + (k % 3) * 90) for k in range(16)))
    def dune(y, amp, seed, fill, rim, op=1):
        r = random.Random(seed); pts = [(x, y + amp * math.sin(x / 260 + seed) + 0.5 * amp * math.sin(x / 97 + seed * 2) + r.uniform(-4, 4)) for x in range(-600, 1700, 40)]
        d = f"M{pts[0][0]} {pts[0][1]:.0f} " + " ".join(f"L{x} {yy:.0f}" for x, yy in pts[1:])
        return (f'<path d="{d} L1700 2600 L-600 2600 Z" fill="{fill}" opacity="{op}"/>'
                f'<path d="{d}" fill="none" stroke="{rim}" stroke-width="3" opacity=".75" filter="url(#bl2)"/>')

    def camel(cid, flip=False, tone="#0a1418"):
        """a dromedary in backlit silhouette (feet at 0,0, facing right, ~420 tall); legs swing as it walks (a pacing gait)"""
        body = ("M-175 -300 C-150 -360 -90 -405 -30 -405 C30 -405 70 -360 100 -322 C140 -300 175 -310 200 -335 "
                "C220 -360 228 -395 240 -410 C255 -428 285 -422 300 -405 C312 -393 316 -382 305 -376 C285 -372 262 -378 252 -372 "
                "C238 -355 232 -325 220 -295 C205 -265 170 -245 140 -240 C120 -230 110 -210 100 -200 "
                "C40 -185 -60 -185 -120 -200 C-150 -210 -170 -240 -175 -300 Z")
        leg = "M-19 0 L19 0 L13 95 Q19 104 13 116 L10 188 L20 200 L-12 200 L-8 188 L-12 116 Q-19 104 -13 95 Z"
        far, near = "#16262c", tone
        legs = ""
        for k, (x, ph, col) in enumerate(((105, 0, far), (-118, 0, far), (88, math.pi, near), (-100, math.pi, near))):
            legs += f'<g class="leg" data-ph="{ph:.2f}" data-x="{x}" transform="translate({x} -200)"><path d="{leg}" fill="{col}"/></g>'
            if k == 1: legs += f'<path d="{body}" fill="{near}"/><path d="M-174 -290 C-185 -260 -186 -230 -180 -205" stroke="{near}" stroke-width="9" fill="none" stroke-linecap="round"/>'
        legs += '<path d="M268 -402 l6 -14 l6 12 Z" fill="%s"/>' % near             # the ear
        fl = ' transform="scale(-1,1)"' if flip else ""
        return f'<g id="{cid}" class="camel"{fl}><g class="bob" filter="url(#rim)">{legs}</g></g>'

    herd = "".join(f'<g transform="translate({x} {y}) scale({s})">{camel(f"h{k}")}</g>' for k, (x, y, s) in enumerate(((0, 1218, .26), (130, 1222, .3), (290, 1216, .24), (420, 1221, .28), (560, 1219, .25), (700, 1224, .31))))
    tiles = "".join(f'<div class="tile" id="t{k}"><div class="glow"></div><span class="l">{ch}</span><span class="mk">{mk}</span></div>' for k, (ch, mk) in enumerate((("ج", "َ"), ("م", "ِ ← َ"), ("ل", "ـ"))))
    htiles = "".join(f'<div class="htile">{ch}</div>' for ch in ("ج", "م", "ل"))
    lw = [("بِسْمِ", 760, 620, -8), ("اللَّهِ", 300, 520, 6), ("الرَّحْمَنِ", 640, 860, 5), ("الرَّحِيمِ", 200, 960, -6)]
    gx = [800, 590, 300, 40]                                        # right to left, as the line reads
    lwh = "".join(f'<div class="lw" data-gx="{g}" style="left:{x}px;top:{y}px;transform:rotate({r}deg)">{w}</div>' for (w, x, y, r), g in zip(lw, gx))
    css = f"""
@font-face {{ font-family:"FR"; src:url("assets/fredoka-latin-700-normal.woff2"); }}
@font-face {{ font-family:"AM"; src:url("assets/amiri-arabic-700-normal.woff2"); }}
* {{ margin:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:{TEAL}; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:{TEAL}; }}
#world, #fg {{ position:absolute; inset:0; }}
.lay {{ position:absolute; left:0; top:0; width:1080px; height:1920px; transform-origin:540px 960px; will-change:transform; }}
svg.full {{ position:absolute; left:0; top:0; width:1080px; height:1920px; overflow:visible; }}
#night {{ position:absolute; inset:0; opacity:0; background:linear-gradient(#050c0f 0%, rgba(8,18,22,.85) 45%, rgba(10,20,24,.55) 75%, rgba(10,20,24,.3)); }}
#grain {{ position:absolute; inset:-50px; opacity:.11; mix-blend-mode:overlay; pointer-events:none;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/></filter><rect width='300' height='300' filter='url(%23n)'/></svg>"); }}
#vig {{ position:absolute; inset:0; pointer-events:none; background:radial-gradient(ellipse at 50% 48%, rgba(0,0,0,0) 52%, rgba(3,8,10,.7) 100%); }}
#whip {{ position:absolute; inset:0; opacity:0; background:linear-gradient(90deg, rgba(233,185,73,0), rgba(246,210,122,.35), rgba(233,185,73,0)); }}
#flash {{ position:absolute; inset:0; opacity:0; background:#fff4d6; mix-blend-mode:screen; }}
.ar {{ font-family:AM; direction:rtl; }}
#hook {{ position:absolute; left:60px; right:60px; top:150px; text-align:center; }}
#hl {{ font-family:FR; font-size:78px; line-height:1.14; color:{CREAM}; text-shadow:0 6px 24px rgba(0,0,0,.55); }}
.hw {{ display:inline-block; opacity:0; }} .hw.same {{ opacity:1; color:{GOLD}; font-size:108px; transform-origin:50% 50%;
  text-shadow:0 0 40px rgba(233,185,73,.75), 0 8px 0 #7a5a14, 0 12px 30px rgba(0,0,0,.6); }}
.ring {{ position:absolute; left:440px; top:430px; width:200px; height:200px; border-radius:50%; border:10px solid {GOLD2}; opacity:0; }}
.spark {{ position:absolute; left:520px; top:520px; width:44px; height:8px; border-radius:4px; background:{GOLD2}; opacity:0; box-shadow:0 0 14px {GOLD}; }}
.pair {{ position:absolute; top:720px; width:440px; text-align:center; opacity:0; }}
.pair .ar {{ font-size:150px; line-height:1.3; color:{CREAM}; text-shadow:0 0 30px rgba(233,185,73,.45), 0 10px 30px rgba(0,0,0,.6); }}
.pair .ar b {{ font-weight:700; }} .pair .en {{ font-family:FR; font-size:46px; color:{GOLD2}; letter-spacing:.04em; }}
#hjamil {{ left:560px; }} #hjamal {{ left:80px; }}
#htiles {{ position:absolute; left:0; right:0; top:1060px; display:flex; justify-content:center; gap:28px; direction:rtl; perspective:800px; }}
.htile {{ width:150px; height:150px; border-radius:30px; font-family:AM; font-size:100px; line-height:150px; text-align:center; color:{INK};
  background:linear-gradient(160deg, #fbe3a1, {GOLD} 55%, #b8891f); box-shadow:inset 0 2px 0 rgba(255,255,255,.6), 0 18px 40px rgba(0,0,0,.5), 0 0 40px rgba(233,185,73,.35); opacity:0; }}
#word {{ position:absolute; left:0; right:0; top:420px; height:900px; }}
#big {{ position:absolute; left:0; right:0; top:0; height:520px; opacity:0; }}
.bigw {{ position:absolute; left:0; right:0; top:0; text-align:center; font-size:330px; line-height:1.4; color:{GOLD};
  text-shadow:0 0 60px rgba(233,185,73,.55), 0 14px 0 #6d4f12, 0 24px 50px rgba(0,0,0,.6); }}
#bigA {{ opacity:0; }} #bigB {{ opacity:0; }}
#sweepw {{ position:absolute; left:0; right:0; top:40px; height:440px; overflow:hidden; mix-blend-mode:screen; -webkit-mask-image:linear-gradient(#000,#000); }}
#sweep {{ position:absolute; top:-100px; left:440px; width:200px; height:640px; transform:rotate(18deg); background:linear-gradient(90deg, rgba(255,255,255,0), rgba(255,248,220,.55), rgba(255,255,255,0)); }}
.en1 {{ position:absolute; left:0; right:0; top:450px; text-align:center; font-family:FR; font-size:64px; color:{CREAM}; opacity:0; letter-spacing:.06em; }}
#tiles {{ position:absolute; left:0; right:0; top:590px; display:flex; justify-content:center; gap:34px; direction:rtl; }}
.tile {{ position:relative; width:170px; height:190px; border-radius:34px; opacity:0;
  background:linear-gradient(160deg, rgba(255,255,255,.16), rgba(255,255,255,.04)); border:2px solid rgba(246,210,122,.65);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.35), 0 20px 50px rgba(0,0,0,.45); backdrop-filter:blur(6px); }}
.tile .glow {{ position:absolute; inset:-20px; border-radius:50px; background:radial-gradient(circle, rgba(233,185,73,.6), rgba(233,185,73,0) 70%); opacity:0; }}
.tile .l {{ position:absolute; inset:0; text-align:center; font-family:AM; font-size:120px; line-height:180px; color:{GOLD2}; text-shadow:0 0 24px rgba(233,185,73,.6); }}
.tile .mk {{ position:absolute; left:0; right:0; top:-70px; text-align:center; font-family:AM; font-size:54px; color:{RED}; opacity:0; direction:ltr; }}
#hero {{ position:absolute; left:0; top:0; }}
.chip {{ position:absolute; top:560px; padding:22px 46px; border-radius:999px; font-family:FR; font-size:64px; color:{INK};
  background:linear-gradient(160deg, #fbe3a1, {GOLD}); box-shadow:0 16px 40px rgba(0,0,0,.45), 0 0 40px rgba(233,185,73,.4); opacity:0; }}
#chipB {{ left:120px; }} #chipW {{ right:120px; }}
.card {{ position:absolute; left:70px; right:70px; border-radius:44px; padding:50px 50px 46px; text-align:center;
  background:linear-gradient(165deg, rgba(20,35,42,.78), rgba(11,23,27,.88)); border:2px solid rgba(233,185,73,.55);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.12), 0 40px 90px rgba(0,0,0,.55); backdrop-filter:blur(10px); opacity:0; }}
.card .ar {{ font-size:96px; line-height:1.55; color:{CREAM}; }} .card .ar span {{ display:inline-block; }}
.card .src {{ font-family:FR; font-size:36px; color:{GOLD2}; letter-spacing:.12em; margin-bottom:6px; }}
.card .en {{ font-family:FR; font-size:46px; color:rgba(241,236,224,.85); margin-top:14px; }}
#ayah {{ top:480px; perspective:900px; }} #ayah .g {{ color:{GOLD}; position:relative; text-shadow:0 0 30px rgba(233,185,73,.6); }}
#ayah .ul {{ position:absolute; left:6%; right:6%; bottom:14px; height:7px; border-radius:4px; background:{GOLD}; transform-origin:100% 50%; }}
#jscene {{ position:absolute; inset:0; }}
#jumla {{ position:absolute; left:0; right:0; top:340px; text-align:center; font-size:250px; line-height:1.4; color:{GOLD}; opacity:0;
  text-shadow:0 0 60px rgba(233,185,73,.55), 0 12px 0 #6d4f12, 0 22px 50px rgba(0,0,0,.6); }}
#jumlaEn {{ position:absolute; left:0; right:0; top:700px; text-align:center; font-family:FR; font-size:60px; color:{CREAM}; opacity:0; letter-spacing:.06em; }}
.lw {{ position:absolute; width:240px; text-align:center; font-family:AM; font-size:76px; line-height:120px; color:{GOLD2}; opacity:0; border-radius:28px;
  background:rgba(233,185,73,.1); border:2px solid rgba(233,185,73,.5); box-shadow:0 0 40px rgba(233,185,73,.25); text-shadow:0 0 20px rgba(233,185,73,.6); }}
#jline {{ position:absolute; left:90px; right:90px; top:1320px; height:6px; border-radius:3px; background:linear-gradient(90deg, rgba(233,185,73,0), {GOLD}, rgba(233,185,73,0)); transform:scaleX(0); }}
#turn {{ position:absolute; left:0; right:0; top:560px; text-align:center; font-family:FR; font-size:150px; color:{GOLD}; opacity:0;
  text-shadow:0 0 40px rgba(233,185,73,.6), 0 10px 0 #6d4f12, 0 18px 40px rgba(0,0,0,.6); }}
#hadith {{ top:300px; }} #hadith .ar {{ font-size:84px; }}
.opt {{ position:absolute; top:880px; width:420px; height:360px; border-radius:44px; text-align:center; opacity:0;
  background:linear-gradient(165deg, rgba(20,35,42,.8), rgba(11,23,27,.9)); border:3px solid rgba(241,236,224,.35); box-shadow:0 30px 70px rgba(0,0,0,.5); }}
#optC {{ left:80px; }} #optB {{ right:80px; }}
.opt svg {{ position:absolute; left:110px; top:40px; width:200px; height:190px; }}
.opt b {{ position:absolute; left:0; right:0; top:250px; font-family:FR; font-size:66px; color:{CREAM}; }}
.opt .tick {{ position:absolute; right:-24px; top:-24px; width:96px; height:96px; border-radius:50%; background:{GOLD}; color:{INK}; font-family:FR; font-size:64px; line-height:96px; opacity:0; box-shadow:0 0 40px rgba(233,185,73,.7); }}
#ring3 {{ position:absolute; left:440px; top:1290px; width:200px; height:200px; opacity:0; }} #ring3 svg {{ position:absolute; inset:0; transform:rotate(-90deg); }}
#ring3 circle {{ fill:none; stroke-width:12; }} #ring3 .bg {{ stroke:rgba(241,236,224,.15); }} #ring3 .fg {{ stroke:{GOLD}; stroke-linecap:round; stroke-dasharray:339; }}
#rnum {{ position:absolute; inset:0; text-align:center; line-height:200px; font-family:FR; font-size:100px; color:{CREAM}; }}
#endc {{ position:absolute; left:60px; right:60px; top:380px; text-align:center; opacity:0; }}
#endc .a {{ font-family:FR; font-size:110px; line-height:1.1; color:{GOLD}; text-shadow:0 0 40px rgba(233,185,73,.5), 0 10px 0 #6d4f12, 0 18px 40px rgba(0,0,0,.55); }}
#endc .b {{ font-family:FR; font-size:56px; line-height:1.25; color:{CREAM}; margin-top:30px; }}
#endc .c {{ display:inline-block; margin-top:44px; padding:18px 40px; border-radius:999px; border:2px solid rgba(233,185,73,.6); font-family:FR; font-size:40px; color:{GOLD2}; }}
.cap {{ position:absolute; left:70px; right:70px; top:1560px; text-align:center; font-family:FR; font-size:68px; line-height:1.18; color:{CREAM}; opacity:0;
  text-shadow:0 4px 0 rgba(0,0,0,.45), 0 8px 30px rgba(0,0,0,.6); }}
.cw {{ display:inline-block; opacity:0; }} .cw.g {{ color:{GOLD}; }}
"""
    defs = f"""<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#07121a"/><stop offset=".35" stop-color="{TEAL}"/><stop offset=".55" stop-color="#2a3a3a"/>
  <stop offset=".64" stop-color="#7a5a2c"/><stop offset=".69" stop-color="#d79a3c"/><stop offset=".72" stop-color="#f3c86a"/></linearGradient>
<radialGradient id="bloom" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#ffe3a0" stop-opacity=".85"/><stop offset=".25" stop-color="#f0b04a" stop-opacity=".45"/><stop offset="1" stop-color="#e9b949" stop-opacity="0"/></radialGradient>
<radialGradient id="sun" cx="50%" cy="45%" r="55%"><stop offset="0" stop-color="#fffbe9"/><stop offset=".6" stop-color="#ffe7a6"/><stop offset="1" stop-color="#f6c45c"/></radialGradient>
<linearGradient id="d1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a3838"/><stop offset=".4" stop-color="#1a2a2f"/></linearGradient>
<linearGradient id="d2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1d2e33"/><stop offset=".5" stop-color="#122127"/></linearGradient>
<linearGradient id="d3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#14252b"/><stop offset=".5" stop-color="#0b171b"/></linearGradient>
<filter id="bl2"><feGaussianBlur stdDeviation="1.6"/></filter><filter id="haze" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="14"/></filter>
<filter id="rim" x="-20%" y="-20%" width="140%" height="140%"><feMorphology in="SourceAlpha" operator="dilate" radius="3" result="d"/><feOffset in="d" dy="-3" result="o"/>
  <feFlood flood-color="#f8cf6a"/><feComposite in2="o" operator="in" result="r"/><feGaussianBlur in="r" stdDeviation="2.2" result="rb"/>
  <feMerge><feMergeNode in="rb"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>"""
    icon = camel("ic", tone="#1b2c32").replace('class="leg"', 'class="leg2"')
    camel_icon = f'<svg viewBox="-200 -440 520 450"><g filter="url(#rim)">{icon}</g></svg>'
    body = f"""
<svg width="0" height="0" style="position:absolute">{defs}</svg>
<div id="world">
 <div class="lay" data-k="0.1"><svg class="full" viewBox="0 0 1080 1920"><rect x="-600" y="-600" width="2280" height="3100" fill="url(#sky)"/><g opacity=".55">{stars}</g></svg></div>
 <div class="lay" data-k="0.2"><svg class="full" viewBox="0 0 1080 1920"><circle cx="540" cy="1200" r="760" fill="url(#bloom)"/><circle cx="540" cy="1200" r="190" fill="url(#sun)"/>
   <rect x="-600" y="1150" width="2280" height="90" fill="#ffd98a" opacity=".22" filter="url(#haze)"/></svg></div>
 <div class="lay" data-k="0.35"><svg class="full" viewBox="0 0 1080 1920">{dune(1235, 18, 1, "url(#d1)", "#f3c86a")}<g id="herd">{herd}</g></svg></div>
 <div class="lay" data-k="0.6"><svg class="full" viewBox="0 0 1080 1920">{dune(1340, 40, 3, "url(#d2)", "#e9b949")}</svg></div>
 <div class="lay" data-k="1"><svg class="full" viewBox="0 0 1080 1920"><g id="hero" transform="translate(1500 1520) scale(1.05)">{camel("hc")}</g>
   {dune(1500, 55, 5, "url(#d3)", "#c99a3a")}<g>{dust}</g></svg></div>
</div>
<div id="night"></div>
<div id="fg">
 <div id="hook"><div id="hl">{hl}</div></div>
 <div class="pair" id="hjamil"><div class="ar"><b>ج</b>َ<b>م</b>ِي<b>ل</b></div><div class="en">beautiful</div></div>
 <div class="pair" id="hjamal"><div class="ar"><b>ج</b>َ<b>م</b>َ<b>ل</b></div><div class="en">camel</div></div>
 <div id="htiles">{htiles}</div>
 <div class="ring"></div><div class="ring"></div>{sparks}
 <div id="word"><div id="big"><div class="bigw ar" id="bigA">جَمِيل</div><div class="bigw ar" id="bigB">جَمَل</div><div id="sweepw"><div id="sweep"></div></div></div>
   <div class="en1" id="bigEn">beautiful</div><div class="en1" id="bigEn2">a camel</div><div id="tiles">{tiles}</div></div>
 <div class="chip" id="chipB">beauty</div><div class="chip" id="chipW">wealth</div>
 <div class="card" id="ayah"><div class="src">AN-NAḤL 16:6</div><div class="ar"><span>وَلَكُمْ</span> <span>فِيهَا</span> <span class="g">جَمَالٌ<i class="ul"></i></span></div>
   <div class="en">“And for you there is beauty in them.”</div></div>
 <div id="jscene"><div class="ar" id="jumla">جُمْلَة</div><div id="jumlaEn">a sentence</div>{lwh}<div id="jline"></div></div>
 <div id="quiz"><div id="turn">YOUR TURN</div>
   <div class="card" id="hadith"><div class="src">THE PROPHET ﷺ · MUSLIM 91</div><div class="ar"><span>إِنَّ</span> <span>اللَّهَ</span> <span>جَمِيلٌ</span> <span>يُحِبُّ</span> <span class="q">الْجَمَالَ</span></div>
     <div class="en">“Allah is jamīl, and He loves <span style="color:{GOLD}">al-jamāl</span>”</div></div>
   <div class="opt" id="optC">{camel_icon}<b>CAMELS</b></div>
   <div class="opt" id="optB"><svg viewBox="-100 -100 200 200"><g fill="{GOLD}" filter="url(#rim)"><path d="M0 -80 C8 -20 20 -8 80 0 C20 8 8 20 0 80 C-8 20 -20 8 -80 0 C-20 -8 -8 -20 0 -80 Z"/>
     <path d="M52 -62 C55 -46 60 -42 74 -40 C60 -37 55 -33 52 -18 C49 -33 44 -37 30 -40 C44 -42 49 -46 52 -62 Z" opacity=".8"/></g></svg><b>BEAUTY</b><div class="tick">✓</div></div>
   <div id="ring3"><svg viewBox="0 0 200 200" width="200" height="200"><circle class="bg" cx="100" cy="100" r="54"/><circle class="fg" cx="100" cy="100" r="54"/></svg><div id="rnum">3</div></div></div>
 <div id="endc"><div class="a">Tag someone<br>beautiful</div><div class="b">Just maybe don't<br>call them a camel.</div><div class="c">comment below 👇</div></div>
 {cap_html}
</div>
<div id="whip"></div><div id="flash"></div><div id="grain"></div><div id="vig"></div>"""
    open(os.path.join(OUT, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><title>jamil</title>
<script src="assets/gsap.min.js"></script><style>{css}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{END}">
{body}
{chr(10).join(au)}
</div><script>
const tl = gsap.timeline({{ paused: true }});
const CAM = {{x:540, y:0, s:1.0}}, lays = [...document.querySelectorAll(".lay")];
function camSet() {{ for (const l of lays) {{ const k = +l.dataset.k; l.style.transform = `translate(${{(540 - CAM.x) * k}}px, ${{-CAM.y * k * 0.5}}px) scale(${{1 + (CAM.s - 1) * k}})`; }} }}
camSet();
const legs = [...document.querySelectorAll(".leg")], bobs = [...document.querySelectorAll(".bob")], W = {{t:0}};
function walk() {{ const t = W.t;                       // the pacing gait: both legs on a side together; the body rises and falls
  for (const g of legs) {{ const a = 16 * Math.sin(t * 2 * Math.PI * 0.9 + +g.dataset.ph); g.setAttribute("transform", `translate(${{g.dataset.x}} -200) rotate(${{a.toFixed(2)}})`); }}
  for (const b of bobs) b.setAttribute("transform", `translate(0 ${{(4 * Math.sin(t * 4 * Math.PI * 0.9)).toFixed(2)}})`); }}
walk();
tl.to(W, {{t:{END}, duration:{END}, ease:"none", onUpdate:walk}}, 0);
{chr(10).join(js)}
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;</script></body></html>
""")
    print("built", END, "s,", len(au), "sounds;", {k: v for k, v in L.items()})
    return END

if __name__ == "__main__":
    build()
