#!/usr/bin/env python3
"""The orbit video (owner, 18 Oct 2026): question-word tiles circle the owner; he swipes them faster, a sentence with a gap
appears above him, he reaches out, picks a tile and pushes it up into the gap. Two rounds. No sound from him: Callum's voice
and Rafiq's Arabic are added.

  W=/tmp/orbit: clip.mp4 (Drive 1-96UWHRVdaTtbricTcpAh4LjZMemyvVq), cut.mp4 (CUTS below, graded), pose.json (MediaPipe pose per frame
  of cut.mp4), mask/ (rembg person masks) → python3 render.py W frames → back/ front/ → python3 render.py W mix → orbit.mp4
"""
import json, os, re, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"; FPS = 30
W = sys.argv[1]; STEP = sys.argv[2]; os.chdir(W)
# source seconds (take 1 10-29, take 2 30-67, take 3 68-89) → the cut: hook, swipe, think, grab+push, look up; think, grab+push, look up
CUTS = [(30.5, 3.0), (82.2, 2.7), (77.0, 2.6), (72.5, 4.2), (56.4, 2.4), (46.0, 3.5), (50.5, 5.2), (57.5, 3.3), (63.0, 4.3)]   # 31.2 s, 936 frames
V = os.path.join(REPO, "brag-quiz/voice/orbit/")

def config():
    pose = json.load(open("pose.json")); N = len(pose)
    raw = [p["ri"][:2] for p in pose]                                    # his right hand (screen left) does every move
    hand = [[round(sum(raw[j][a] for j in range(max(0, i - 2), min(N, i + 3))) / len(range(max(0, i - 2), min(N, i + 3))), 1) for a in (0, 1)] for i in range(N)]
    # hook take A (ha.mp3): the shouted YOU is 0.45-0.75 s (loudness; whisper puts the words after it too early)
    hook = [["Can", 0, False], ["YOU", .42, True], ["finish", 1.22, False], ["these", 1.6, False], ["Arabic", 1.85, False], ["sentences?", 2.3, False]]
    return dict(N=N, hand=hand, cx=585, cy=1120, rx=480, ry=210, w0=.55, w1=6.0, fling=[3.45, 4.6],
        words=[["مَنْ", "who"], ["كَيْفَ", "how"], ["أَيْنَ", "where"], ["ما", "what"], ["مَتى", "when"], ["لِماذا", "why"], ["كَمْ", "how many"]],
        hook=hook, hookEnd=3.45, lab=[3.5, 5.65, "PICK THE MISSING WORD"], flashes=[3.0, 5.7, 14.9],
        rounds=[dict(n="1/2", k=1, rest=["حالُكَ؟"], en="___ are you?", ans="How", c0=5.7, c1=14.9, cd=7.5, g0=8.75, g1=9.35, rel=11.3, land=11.62),
                dict(n="2/2", k=3, rest=["اسْمُكَ؟"], en="___ is your name?", ans="What", c0=14.9, c1=99, cd=17.7, g0=19.25, g1=19.8, rel=22.35, land=22.68, last=True)],
        ask=[26.0, "How many did you get?<br><b>0, 1 or 2?</b> Comment 👇"])

if STEP == "frames":
    from playwright.sync_api import sync_playwright
    C = config(); json.dump(C, open("orbit.json", "w"), ensure_ascii=False)
    if not os.path.exists("fonts"): shutil.copytree(os.path.join(REPO, "brag-quiz", "fonts"), "fonts")
    shutil.copy(os.path.join(HERE, "orbit.html"), "orbit.html")
    for L in ("back", "front"): os.makedirs(L, exist_ok=True)
    K = os.cpu_count() or 1
    only = sys.argv[3:]                               # optional frame numbers, for stills
    for p in [subprocess.Popen([sys.executable, __file__, W, "worker", str(k), str(K)] + only) for k in range(K)]: assert p.wait() == 0

elif STEP == "worker":
    from playwright.sync_api import sync_playwright
    C = json.load(open("orbit.json")); k, K = int(sys.argv[3]), int(sys.argv[4]); only = [int(x) for x in sys.argv[5:]]
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME); p = b.new_page(viewport={"width": 1080, "height": 1920})
        p.goto("file://" + os.path.abspath("orbit.html")); p.evaluate(f"C = {json.dumps(C, ensure_ascii=False)}"); p.evaluate("document.fonts.ready"); p.wait_for_timeout(500)
        for i in (only or range(C["N"]))[k::K]:
            if not only and os.path.exists(f"front/{i:05d}.png"): continue
            for L in ("back", "front"):
                p.evaluate(f"update({i / FPS}, '{L}')"); p.screenshot(path=f"{L}/{i:05d}.png", omit_background=True)
        b.close()

elif STEP == "mix":
    sys.path.insert(0, os.path.join(REPO, "brag-quiz")); import build_teach as T
    C = json.load(open("orbit.json")); A, R = [], C["rounds"]
    def lufs(f):
        m = subprocess.run(["ffmpeg", "-i", f, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
        return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", m)[-1])
    dur = lambda f: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
    def say(f, at, target):                # a voice line, levelled to target LUFS; returns its end
        A.append((f, at, 10 ** ((target - lufs(f)) / 20))); return at + dur(f)
    SX = os.path.join(REPO, "brag-quiz/sfx"); fx = lambda n, at, v: A.append((f"{SX}/{n}", at, v))
    ar = lambda text: os.path.join(REPO, "audio", T.AUDIO[text] + ".mp3")
    say(V + "ha.mp3", .05, -16); fx("crash.wav", .52, .8)
    fx("ref/swoosh.wav", 2.95, .45); fx("ref/charge-swoosh.wav", 3.3, .5); say(V + "o1.mp3", 3.6, -17)
    for r, line, arabic, after in ((R[0], "o2", "كَيْفَ حالُكَ؟", "o3"), (R[1], "o4", "ما اسْمُكَ؟", "o5")):
        fx("ref/shutter.wav", r["c0"], .6); say(V + line + ".mp3", r["c0"] + .2, -17)
        for k in range(3): fx("ref/click.wav", r["cd"] + k, .9)
        fx("ref/tap.wav", r["g1"], .7); fx("ref/short-swoosh.wav", r["rel"] - .05, .6)
        fx("owner/n03.wav", r["land"], .7); A.append((os.path.join(REPO, "sounds/correct.mp3"), r["land"] + .03, .5))
        e = say(ar(arabic), r["land"] + .3, -18); say(V + after + ".mp3", e + .2, -17)
    end = round(C["N"] / 30, 2)
    bed = os.path.join(REPO, "brag-output-v6/composition/assets/sfx-gen/fountain.mp3")
    args = ["ffmpeg", "-v", "error", "-y", "-i", "cut.mp4", "-framerate", "30", "-i", "back/%05d.png", "-framerate", "30", "-i", "mask/%05d.png",
            "-framerate", "30", "-i", "front/%05d.png", "-stream_loop", "-1", "-i", bed]
    for f, _, _ in A: args += ["-i", f]
    # each jump cut between takes alternates the framing (1.0 / 1.07), so the cuts read as intended
    edges, t = [], 0
    for _, d in CUTS: edges.append((round(t, 3), round(t + d, 3))); t += d
    z = "+".join(f"between(t,{a},{b - .001})*{1.07 if k % 2 else 1}" for k, (a, b) in enumerate(edges))
    fc = ["[0:v]split=2[v0][v1]", "[v0][1:v]overlay=0:0:format=auto[bb]", "[2:v]format=gray[m]", "[v1][m]alphamerge[fg]",
          "[bb][fg]overlay=0:0:format=auto[sc]", "[sc][3:v]overlay=0:0:format=auto,format=yuv420p[all]",
          f"[all]scale=w='trunc(1080*({z})/2)*2':h='trunc(1920*({z})/2)*2':eval=frame:flags=bicubic,crop=1080:1920:'(iw-1080)/2':'(ih-1920)*0.4',setsar=1[v]",
          f"[4:a]atrim=0:{end},volume=0.1,aformat=channel_layouts=stereo,aresample=48000[bed]"]
    for i, (f, at, v) in enumerate(A):
        ms = int(max(0, at) * 1000); fc.append(f"[{i+5}:a]aresample=48000,aformat=channel_layouts=stereo,volume={v:.3f},adelay={ms}|{ms}[s{i}]")
    fc.append("[bed]" + "".join(f"[s{i}]" for i in range(len(A))) + f"amix=inputs={len(A) + 1}:normalize=0:duration=first,alimiter=limit=0.89:level=false[a]")
    subprocess.run(args + ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-t", str(end), "-c:v", "libx264", "-crf", "16", "-preset", "slow",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", "orbit.mp4"], check=True)
    print("orbit.mp4", end, "s")
