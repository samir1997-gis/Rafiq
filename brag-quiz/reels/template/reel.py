#!/usr/bin/env python3
"""The Rafiq reel template (VIDEO-STYLE.md): one talking-head clip in, a finished reel out.

  python3 reel.py WORK fetch <google-drive-file-id>   download the clip to WORK/clip.mp4
  python3 reel.py WORK words      transcribe (WORK/words.json)
  python3 reel.py WORK cut        cut only true silences, keep a breath; prints the cut's transcript to check no word is clipped
  python3 reel.py WORK base [nologo]   frame-exact pieces (sound stays in sync), DJI watermark out (nologo: footage without one), the grade → WORK/cut.mov; word times
  python3 reel.py WORK plan       draft WORK/config.json: captions, stressed words (gold pops), punch-ins. Then fill in by hand,
                                  from the transcript: "titles" [start, end, small line, BIG WORD, size], "split" [start, end],
                                  "flicks" [[start, end, TITLE], ...] (the hook at 0, the ending, camera changes),
                                  "steps" [[[word starts], end], ...] (a zoom step per word: "these · three · things"),
                                  "sections" (where each slow push restarts)
  python3 reel.py WORK zoom       the slow push per section → WORK/base.mov
  python3 reel.py WORK masks      the speaker cut out wherever a title sits behind him (rembg; about a second a frame)
  python3 reel.py WORK layers     titles (behind) and captions, split frame, flicker (in front)
  python3 reel.py WORK mix        clean the voice before the gain, -14 LUFS, sound effects by sfx_rules.py, punch-ins → WORK/reel.mp4
"""
import json, os, re, subprocess, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"; FPS = 30
W = sys.argv[1]; STEP = sys.argv[2]; os.makedirs(W, exist_ok=True); os.chdir(W)
sh = lambda *a: subprocess.run(list(a), check=True)
J = lambda f: json.load(open(f)); P = lambda f, o: json.dump(o, open(f, "w"), ensure_ascii=False, indent=1)

def transcribe(src, out):
    from faster_whisper import WhisperModel
    m = WhisperModel("small.en", compute_type="int8"); segs, _ = m.transcribe(src, word_timestamps=True, condition_on_previous_text=False)
    ws = [dict(w=w.word.strip(), s=round(w.start, 2), e=round(w.end, 2)) for s in segs for w in s.words]; P(out, ws)
    print(" ".join(w["w"] for w in ws)); return ws

if STEP == "fetch":
    sh("curl", "-sSL", "-o", "clip.mp4", f"https://drive.usercontent.google.com/download?id={sys.argv[3]}&export=download&confirm=t")
    sh("ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate:format=duration", "-of", "compact", "clip.mp4")

elif STEP == "words":
    sh("ffmpeg", "-v", "error", "-y", "-i", "clip.mp4", "-vn", "-ac", "1", "-ar", "16000", "audio.wav"); transcribe("audio.wav", "words.json")

elif STEP == "cut":     # only true silence (-40 dB, 0.4 s+), a 0.12 s breath kept either side: never clips a soft word ending
    log = subprocess.run(["ffmpeg", "-i", "audio.wav", "-af", "silencedetect=noise=-40dB:d=0.4", "-f", "null", "-"], capture_output=True, text=True).stderr
    sil = [(float(e) - float(d), float(e)) for e, d in re.findall(r"silence_end: ([\d.]+) \| silence_duration: ([\d.]+)", log)]
    end = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "clip.mp4"], capture_output=True, text=True).stdout)
    chunks, cur = [], 0.0
    for s, e in sil:
        a, b = s + .12, e - .12
        if b - a > .12 and a > cur: chunks.append((round(cur, 3), round(a, 3))); cur = b
    chunks.append((round(cur, 3), round(end - .05, 3))); P("chunks.json", chunks)
    print(len(chunks), "pieces,", round(sum(round((b - a) * FPS) / FPS for a, b in chunks), 1), "s")
    fc = "".join(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS[a{i}];" for i, (a, b) in enumerate(chunks)) + "".join(f"[a{i}]" for i in range(len(chunks))) + f"concat=n={len(chunks)}:v=0:a=1[a]"
    sh("ffmpeg", "-v", "error", "-y", "-i", "audio.wav", "-filter_complex", fc, "-map", "[a]", "cutcheck.wav"); transcribe("cutcheck.wav", "cutcheck.json")

elif STEP == "base":
    G = open(os.path.join(HERE, "grade.txt")).read().strip(); os.makedirs("parts", exist_ok=True); lst = []
    w, h = map(int, subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-of", "csv=p=0", "clip.mp4"], capture_output=True, text=True).stdout.strip().split(","))
    logo = f"delogo=x={int(90*w/2160)}:y={int(600*h/3840)}:w={int(780*w/2160)}:h={int(110*h/3840)}," if w * 16 == h * 9 and "nologo" not in sys.argv else ""
    for i, (a, b) in enumerate(J("chunks.json")):
        out = f"parts/p{i:02d}.mov"; lst.append(f"file 'p{i:02d}.mov'")
        if os.path.exists(out): continue
        n = round((b - a) * FPS); d = n / FPS
        sh("ffmpeg", "-v", "error", "-y", "-ss", f"{a}", "-i", "clip.mp4", "-frames:v", str(n),
           "-vf", f"{logo}{G},scale=1404:2496:flags=lanczos,fps={FPS},format=yuv420p",
           "-af", f"atrim=duration={d:.6f},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={d-0.025:.4f}:d=0.025",
           "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-c:a", "pcm_s16le", "-ar", "48000", out)
    open("parts/list.txt", "w").write("\n".join(lst))
    sh("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "parts/list.txt", "-c", "copy", "cut.mov")
    sh("ffmpeg", "-v", "error", "-y", "-i", "cut.mov", "-vn", "-ac", "1", "-ar", "16000", "cut.wav"); transcribe("cut.wav", "cutwords.json")

elif STEP == "plan":    # captions, stressed words (loud against their neighbours), punch-ins on the strongest; titles are filled in by hand
    import numpy as np
    ws = J("cutwords.json"); end = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "cut.mov"], capture_output=True, text=True).stdout)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", "cut.wav", "-f", "s16le", "-"], capture_output=True).stdout; x = np.frombuffer(raw, np.int16) / 32768
    lv = lambda a, b: 20 * np.log10(np.sqrt(np.mean(x[int(a*16000):int(b*16000)] ** 2)) + 1e-9)
    for w in ws: w["lv"] = lv(w["s"], min(w["e"], w["s"] + .5))
    for w in ws:
        near = [v["lv"] for v in ws if abs(v["s"] - w["s"]) < 3 and v is not w]; w["z"] = (w["lv"] - np.median(near)) / (np.std(near) + 1e-6)
    STOP = set("the a an to of you in is be that and or it it's if i what with your from which do need this so just like okay".split())
    cand = sorted([w for w in ws if w["w"].strip(",.?!").lower() not in STOP and len(w["w"].strip(",.?!")) > 2], key=lambda w: -w["z"])
    emph = sorted(cand[:max(6, len(ws) // 12)], key=lambda w: w["s"]); E = {round(w["s"], 2) for w in emph}
    punch = sorted(emph, key=lambda w: -w["z"])[:max(4, len(emph) // 2)]
    caps, cur = [], []
    for i, w in enumerate(ws):
        cur.append(w); nxt = ws[i + 1]["s"] if i + 1 < len(ws) else end
        if len(cur) >= 4 or w["w"][-1] in ",.?" or (len(cur) >= 2 and nxt - w["e"] > .35) or i + 1 == len(ws):
            caps.append([cur[0]["s"], nxt if nxt - cur[-1]["e"] < .6 else cur[-1]["e"] + .3,
                         [[v["w"].rstrip(",") if j == len(cur) - 1 else v["w"], v["s"], round(v["s"], 2) in E] for j, v in enumerate(cur)]]); cur = []
    C = J("config.json") if os.path.exists("config.json") else {}
    C.update(caps=caps, punch=sorted([[w["s"], w["e"]] for w in punch]), end=round(end, 2))
    C.setdefault("titles", []); C.setdefault("split", None); C.setdefault("flicks", [[0, 2.5, "HOOK TITLE"]]); C.setdefault("steps", []); C.setdefault("sections", [])
    C.setdefault("broll", {"split": ["words", "tiles", "prayalong"], "flick": ["self0", "home", "self1", "quiz", "self2", "mostsaid", "self3", "weak"]})
    P("config.json", C); print("stressed:", " ".join(w["w"] for w in emph)); print("punch-ins:", " ".join(w["w"] for w in sorted(punch, key=lambda w: w["s"])))

elif STEP == "zoom":    # a slow push in each section (restarts at each section start)
    C = J("config.json"); S = C["sections"] or [[0, C["end"]]]
    z = "1+0.055*(" + "+".join(f"between(t,{a},{b})*(t-{a})/{b-a:.3f}" for a, b in S) + ")"
    sh("ffmpeg", "-v", "error", "-y", "-i", "cut.mov", "-vf", f"scale=w='trunc(1080*({z})/2)*2':h='trunc(1920*({z})/2)*2':eval=frame:flags=lanczos,crop=1080:1920:'(iw-1080)*0.5':'(ih-1920)*0.35',setsar=1,format=yuv420p",
       "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-c:a", "pcm_s16le", "base.mov")

elif STEP == "masks":
    from rembg import remove, new_session
    from PIL import Image
    C = J("config.json"); os.makedirs("frames", exist_ok=True); os.makedirs("mask", exist_ok=True)
    sh("ffmpeg", "-v", "error", "-y", "-i", "base.mov", "-vf", "scale=540:960", "-q:v", "3", "frames/%05d.jpg")
    s = new_session("u2net_human_seg"); blank = Image.new("L", (1080, 1920), 0); N = len(os.listdir("frames"))
    for i in range(N):
        out = f"mask/{i:05d}.png"
        if os.path.exists(out): continue
        if any(a - .05 <= i / FPS < b + .05 for a, b, *_ in C["titles"]):
            remove(Image.open(f"frames/{i+1:05d}.jpg"), session=s, only_mask=True).resize((1080, 1920), Image.BILINEAR).save(out)
        else: blank.save(out)

elif STEP == "layers":
    from playwright.sync_api import sync_playwright
    C = J("config.json"); clips = os.path.join(REPO, "brag-output-v9-12", "clips")
    if not os.path.exists("fonts"):
        shutil.copytree(os.path.join(REPO, "brag-quiz", "fonts"), "fonts")
    shutil.copy(os.path.join(HERE, "layers.html"), "layers.html")
    for c in C["broll"]["split"]:      # B-roll: the app's own screen recordings until the owner films some
        if not os.path.exists(f"broll/{c}"):
            os.makedirs(f"broll/{c}"); sh("ffmpeg", "-v", "error", "-y", "-i", f"{clips}/{c}.mp4", "-t", "6", "-vf", "fps=30,scale=1080:-2,crop=1080:640:0:(ih-640)*0.45", "-q:v", "3", f"broll/{c}/%04d.jpg")
    LOOK = ["crop=iw*.5:ih*.5:iw*.25:ih*.22", "hue=s=0,eq=contrast=1.35:brightness=-.03", "crop=iw*.7:ih*.7:iw*.15:ih*.12", "hue=s=0,crop=iw*.42:ih*.42:iw*.29:ih*.24"]
    for k in range(4):   # the speaker's own footage for the flicker: four other moments, tight / black-and-white / medium crops
        if not os.path.exists(f"broll/self{k}"):
            os.makedirs(f"broll/self{k}"); sh("ffmpeg", "-v", "error", "-y", "-ss", f"{C['end'] * (.15 + .2 * k):.2f}", "-i", "base.mov", "-t", "1",
               "-vf", f"{LOOK[k]},scale=960:1640:force_original_aspect_ratio=increase,crop=960:1640", "-q:v", "3", f"broll/self{k}/%04d.jpg")
    for c in C["broll"]["flick"]:
        if not os.path.exists(f"broll/{c}"):
            os.makedirs(f"broll/{c}"); sh("ffmpeg", "-v", "error", "-y", "-i", f"{clips}/{c}.mp4", "-t", "3", "-vf", "fps=30,scale=920:-2,crop=920:1500:0:(ih-1500)*0.3", "-q:v", "3", f"broll/{c}/%04d.jpg")
    C["n"] = {c: len(os.listdir(f"broll/{c}")) for c in os.listdir("broll")}
    C["split"] = C["split"] or [-1, -1]
    for L in ("back", "front"): os.makedirs(L, exist_ok=True)
    P("layers.json", C); K = os.cpu_count() or 1        # one browser per core, each takes every K-th frame
    for p in [subprocess.Popen([sys.executable, os.path.join(HERE, "reel.py"), os.path.abspath("."), "render", str(k), str(K)]) for k in range(K)]: assert p.wait() == 0

elif STEP == "render":
    from playwright.sync_api import sync_playwright
    C = J("layers.json"); k, K = int(sys.argv[3]), int(sys.argv[4]); N = round(C["end"] * FPS)
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME); p = b.new_page(viewport={"width": 1080, "height": 1920})
        p.goto("file://" + os.path.abspath("layers.html")); p.evaluate(f"C = {json.dumps(C)}"); p.evaluate("document.fonts.ready"); p.wait_for_timeout(500)
        for i in range(k, N, K):
            if os.path.exists(f"front/{i:05d}.png"): continue
            for L in ("back", "front"):
                p.evaluate(f"update({i / FPS}, '{L}')")
                if L == "front": p.evaluate("Promise.all([...document.images].filter(i => i.offsetParent).map(i => i.decode().catch(() => 0)))")
                p.screenshot(path=f"{L}/{i:05d}.png", omit_background=True)
        b.close()

elif STEP == "mix":
    sys.path.insert(0, HERE); from sfx_rules import events
    C = J("config.json")
    CLEAN = "highpass=f=80,lowpass=f=13000,afftdn=nr=18:nf=-66:tn=1,agate=threshold=0.003:ratio=2.5:range=0.15:attack=6:release=220,acompressor=threshold=-28dB:ratio=2:attack=12:release=220"
    sh("ffmpeg", "-v", "error", "-y", "-i", "base.mov", "-vn", "-af", CLEAN, "-ar", "48000", "-ac", "2", "voice_clean.wav")
    m = subprocess.run(["ffmpeg", "-i", "voice_clean.wav", "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    gain = -14.5 - float(re.findall(r"I:\s+(-?[\d.]+) LUFS", m)[-1])
    # zoom builds through a section: each emphasis (punch or step word) goes one level deeper (slow, eased),
    # and it only eases back out as the section ends (next title, split, flicker or the end): in, in, in, out
    sm = lambda u: f"({u})*({u})*(3-2*({u}))"
    cuts = sorted({x[0] for x in C["titles"]} | {x for f in C.get("flicks", []) for x in f[:2]} |
                  (set(C["split"]) if C.get("split") else set()) | {x for p in C.get("panels", []) for x in p[:2]} | {C["end"]})
    hits = sorted([a for a, _ in C["punch"]] + [s for ts, _ in C.get("steps", []) for s in ts])
    Z = "1"
    for s1 in cuts:
        ps = [p for p in hits if p < s1 - .3 and not any(p < c < s1 for c in cuts)]
        if ps: Z += f"+min(0.3,0.08*({'+'.join(sm(f'clip((t-{p})/0.45,0,1)') for p in ps)}))*{sm(f'clip(({s1}-t)/0.5,0,1)')}"
    E = events(C)
    args = ["ffmpeg", "-v", "error", "-y", "-i", "base.mov", "-framerate", "30", "-i", "back/%05d.png", "-framerate", "30", "-i", "mask/%05d.png",
            "-framerate", "30", "-i", "front/%05d.png", "-i", "voice_clean.wav"]
    for f, _, _ in E: args += ["-i", f]
    fc = ["[0:v]split=2[v0][v1]", "[v0][1:v]overlay=0:0:format=auto[bb]", "[2:v]format=gray[m]", "[v1][m]alphamerge[fg]",
          "[bb][fg]overlay=0:0:format=auto,format=yuv420p[sc]",
          f"[sc]scale=w='trunc(1080*({Z})/2)*2':h='trunc(1920*({Z})/2)*2':eval=frame:flags=bicubic,crop=1080:1920:'(1080*({Z})-1080)/2':'(1920*({Z})-1920)*0.4'[zs]",
          "[zs][3:v]overlay=0:0:format=auto,format=yuv420p[v]", f"[4:a]volume={gain:.2f}dB[voice]"]
    for i, (f, t, v) in enumerate(E):
        ms = int(max(0, t) * 1000); fc.append(f"[{i+5}:a]aresample=48000,aformat=channel_layouts=stereo,volume={v},adelay={ms}|{ms}[s{i}]")
    fc.append("".join(f"[s{i}]" for i in range(len(E))) + f"amix=inputs={len(E)}:normalize=0,apad[sfx]")
    fc.append("[voice][sfx]amix=inputs=2:normalize=0:duration=first,lowpass=f=16000:poles=2,alimiter=limit=0.8:level=false[a]")
    sh(*args, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "21", "-preset", "slow", "-maxrate", "4.2M", "-bufsize", "8M",
       "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "reel.mp4")
    print("reel.mp4 ready")
