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
# v2 (owner, 18 Oct 2026): one round, wrong then right, from the continuous take 2 (21-67 s: pick, frown, think again, pick, smile)
# source seconds → the cut: hook, swipe (take 3), think, reach + push (wrong), look up, frown, think again, reach + push (right), smile, look up
CUTS = [(10.5, 3.0), (82.2, 2.7), (17.5, 4.1), (21.6, 5.2), (26.8, 2.5), (37.5, 3.8), (46.0, 4.4), (50.4, 5.4), (56.4, 3.5), (63.0, 3.5)]   # 38.1 s
V = os.path.join(REPO, "brag-quiz/voice/orbit/")

def config():
    pose = json.load(open("pose.json")); N = len(pose)
    raw = [p["ri"][:2] for p in pose]                                    # his right index fingertip (screen left) does every move
    hand = [[round(sum(raw[j][a] for j in range(max(0, i - 1), min(N, i + 2))) / len(range(max(0, i - 1), min(N, i + 2))), 1) for a in (0, 1)] for i in range(N)]
    # hook take hs1: the shouted YOU is 0.55-0.75 s (loudness; whisper puts the words after it too early)
    hook = [["Can", 0, False], ["YOU", .5, True], ["finish", 1.25, False], ["this", 1.62, False], ["Arabic", 1.95, False], ["sentence?", 2.45, False]]
    # contact = the frame his reach is furthest out (pose.json): the tile is already waiting there
    return dict(N=N, hand=hand, cx=585, cy=1120, rx=480, ry=210, w0=.55, w1=6.0, fling=[3.45, 4.6],
        words=[["مَنْ", "who"], ["كَيْفَ", "how"], ["أَيْنَ", "where"], ["ما", "what"], ["مَتى", "when"], ["لِماذا", "why"], ["كَمْ", "how many"]],
        hook=hook, hookEnd=3.45, lab=[3.5, 5.65, "PICK THE MISSING WORD"], flashes=[3.0, 5.7],
        card=dict(c0=5.7, rest=["حالُكَ؟"], en="___ are you?", ans="How"),
        attempts=[dict(k=2, contact=10.9, rel=14.95, land=15.25, wrong=True, back=17.4, en="<s style='color:#C8372D'>Where</s> are you? ✗"),
                  dict(k=1, contact=27.3, rel=30.55, land=30.85)],
        cds=[7.6, 23.6], ask=[34.0, "Did you get it <b>first time?</b><br>Comment 👇"])

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
    C = json.load(open("orbit.json")); A = []
    def lufs(f):
        m = subprocess.run(["ffmpeg", "-i", f, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
        return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", m)[-1])
    dur = lambda f: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
    def say(f, at, target):                # a voice line, levelled to target LUFS; returns its end
        A.append((f, at, 10 ** ((target - lufs(f)) / 20))); return at + dur(f)
    SX = os.path.join(REPO, "brag-quiz/sfx"); fx = lambda n, at, v: A.append((f"{SX}/{n}", at, v))
    ar = lambda text: os.path.join(REPO, "audio", T.AUDIO[text] + ".mp3")
    say(V + "hs1.mp3", .05, -16); fx("crash.wav", .62, .8)
    fx("ref/swoosh.wav", 2.95, .45); fx("ref/charge-swoosh.wav", 3.3, .5); say(V + "o1.mp3", 3.6, -17)
    fx("ref/shutter.wav", 5.7, .6); say(V + "o2.mp3", 5.9, -17)
    for c in C["cds"]:
        for k in range(3): fx("ref/click.wav", c + k, .9)
    for a in C["attempts"]:
        fx("ref/tap.wav", a["contact"], .7); fx("ref/short-swoosh.wav", a["rel"] - .05, .6); fx("owner/n03.wav", a["land"], .7)
    w, r = C["attempts"]
    A.append((os.path.join(REPO, "sounds/wrong.mp3"), w["land"] + .03, .6)); say(V + "w1.mp3", w["land"] + .35, -17)
    fx("ref/swoosh.wav", w["back"], .45); say(V + "w2.mp3", 21.4, -17)
    A.append((os.path.join(REPO, "sounds/correct.mp3"), r["land"] + .03, .55))
    e = say(ar("كَيْفَ حالُكَ؟"), r["land"] + .3, -18); e = say(V + "o3.mp3", e + .15, -17); say(V + "e1.mp3", max(e + .2, 33.85), -17)
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
