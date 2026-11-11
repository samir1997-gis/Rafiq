#!/usr/bin/env python3
"""The owner's re-cut of the Aḥad video (#315, 8 Nov 2026; cLAUDE_eDITS/aaa5fccab0c241dcabf255254fb33279.mov, 1:55, opening on "deny
Muḥammad"; it already carries this edit's titles, captions and graphics). Owner: "add flicker effect, a bit of echo and bass to the hook,
zoom in about 5% across the whole video but make sure I'm centred, increase speed by 1.1, and add new graphics, more detailed, more
realistic, especially when I'm describing what's happening to Bilāl".
  - his footage is not graded again (it already is) and nothing is cut;
  - the zoom: 5% throughout, centred on his face frame by frame (OpenCV), the graphics he kept centred;
  - the flicker on the hook (his own moments, never a graphic), with the template's flicker sounds;
  - the hook's voice: an echo and some bass laid under it;
  - four new scenes over 8.7-36.2 s (scripts-gfx a_makkah, a_drag, a_burn, a_boulder), each beat on his word, with their sounds;
  - then everything 1.1x faster, levelled to -14.5 LUFS.

  python3 recut.py WORK prep      → cut.mov, cut.wav, config.json (WORK/clip.mp4 = his edit, reel.py WORK fetch …)
  python3 recut.py WORK config    → the graphics, sounds and flicker in config.json
  python3 recut.py WORK zoom      → base.mov, and the flicker's clips
  python3 reel.py WORK masks; python3 reel.py WORK layers; python3 reel.py WORK mix keepvoice
  python3 recut.py WORK finish    → WORK/ahad-recut.mp4 (1.1x, levelled)
"""
import json, os, re, subprocess, sys
import numpy as np
W, STEP = sys.argv[1:3]; HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
GFX = os.path.join(ROOT, "brag-quiz/reels/scripts-gfx"); SFX = os.path.join(ROOT, "brag-quiz/sfx")
sh = lambda *a: subprocess.run(list(a), check=True)
P = lambda f: os.path.join(W, f)
dur = lambda f: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
HOOK = (0.0, 6.9)                                   # "And they say to him, deny Muḥammad! Believe in al-Lāt and al-ʿUzzā!" (then "Now let me take you back" at 7.1)
# the new scenes: (graphic, from, to, [(planned s, his word's time)], sounds [(name, beat, dB)])
G = [("a_makkah", 8.65, 14.3, [(0.05, 8.8), (1.2, 11.1), (2.0, 12.2)], [("whoosh", 0, -8), ("wind", 0, -14), ("impact", 1, -4), ("shimmer", 2, -6)]),
     ("a_drag", 14.3, 20.95, [(0.05, 14.4), (1.0, 17.5), (2.5, 19.3)], [("scratch", 1, -6), ("rumble", 0, -12), ("thump", 2, -4)]),
     ("a_burn", 20.95, 28.8, [(0.05, 21.1), (1.5, 23.9), (2.6, 25.3), (3.8, 26.9)], [("whoosh", 0, -8), ("crackle", 2, -8), ("rumble", 2, -10), ("crackle", 3, -6)]),
     ("a_boulder", 28.8, 36.25, [(0.05, 28.9), (1.0, 30.2), (3.0, 32.8), (4.1, 34.4), (4.42, 34.7)], [("whoosh", 1, -8), ("thump", 2, -4), ("boom", 4, -2), ("impact", 4, 0)])]
SELF = [7.4, 15.0, 22.0, 37.6, 45.2, 50.0]          # his own moments for the flicker (on camera, no graphic)

if STEP == "prep":
    sh("ffmpeg", "-v", "error", "-y", "-i", P("clip.mp4"), "-vf", "scale=1404:2496:flags=lanczos,fps=30,format=yuv420p", "-c:v", "libx264", "-crf", "12",
       "-preset", "fast", "-c:a", "pcm_s16le", "-ar", "48000", P("cut.mov"))
    sh("ffmpeg", "-v", "error", "-y", "-i", P("cut.mov"), "-vn", "-ac", "1", "-ar", "16000", P("cut.wav"))
    end = round(dur(P("cut.mov")), 2)
    json.dump(dict(end=end, caps=[], titles=[], flicks=[], split=None, steps=[], punch=[], sections=[[0, end]], panels=[], audio=[],
                   broll={"split": [], "flick": ["self0", "self1", "self2", "self3", "self4", "self5"]}), open(P("config.json"), "w"), indent=1)
    print("end", end)

elif STEP == "config":
    C = json.load(open(P("config.json"))); END = C["end"]
    os.makedirs(P("gfx"), exist_ok=True); panels, AUDIO = [], []
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", P("cut.wav"), "-f", "s16le", "-"], capture_output=True).stdout, np.int16) / 32768
    VP = float(np.percentile(20 * np.log10(np.sqrt(np.convolve(x ** 2, np.ones(800) / 800, "valid"))[::400] + 1e-9), 90))
    sys.path.insert(0, os.path.join(ROOT, "brag-quiz/reels/template")); from sfx_rules import info
    def snd(name, t, db):
        f = next(p for p in (os.path.join(SFX, d, name + ".wav") for d in ("soft", "ref", ".")) if os.path.exists(p))
        pk_db, pk = info(f); AUDIO.append([f, round(max(0, t - pk), 3), round(10 ** ((VP + db - pk_db) / 20), 3)])
    for gid, a, b, at, sounds in G:
        warp = {gid: {"at": [[p, round(t - a, 2)] for p, t in at], "d": round(b - a + 0.4, 2)}}; out = P(f"gfx/{gid}.mp4")
        if not os.path.exists(out) or os.environ.get("REGFX"):
            r = subprocess.run([sys.executable, os.path.join(GFX, "graphics.py"), gid], env=dict(os.environ, WARP=json.dumps(warp), OUT=P("gfx")), capture_output=True, text=True)
            print(r.stdout.strip(), r.stderr[-300:])
        panels.append([a, b, "gfx", dict(src=out, slams=[], hits=[])])
        for name, k, db in sounds: snd(name, at[k][1], db)
    for p, q in zip(panels, panels[1:]):            # back to back: hard cuts between them
        p[1] = q[0]; p[3]["cutout"] = True; q[3]["cutin"] = True
    # the hook's voice: an echo after it and some bass under it, from his own audio
    os.makedirs(P("fx"), exist_ok=True); a, b = HOOK
    sh("ffmpeg", "-v", "error", "-y", "-ss", str(a), "-t", str(b - a), "-i", P("cut.mov"), "-filter_complex",
       "[0:a]aformat=channel_layouts=mono,asplit=2[e][l];[e]apad=pad_dur=1.2,asplit=3[a][b][c];[a]adelay=280,volume=0.32[a2];[b]adelay=560,volume=0.18[b2];[c]adelay=840,volume=0.09[c2];"
       "[a2][b2][c2]amix=inputs=3:normalize=0,highpass=f=180,lowpass=f=6000[echo];[l]lowpass=f=160,volume=1.6,apad=pad_dur=1.2[bass];[echo][bass]amix=inputs=2:normalize=0[o]",
       "-map", "[o]", "-ar", "48000", P("fx/hook.wav"))
    AUDIO.append([P("fx/hook.wav"), a, 1.0])
    NOFLICK = os.environ.get("NOFLICK")              # owner, 11 Nov 2026: no flicker at all (and none of its face close-ups); a salah hook goes on the front instead
    if NOFLICK: C["broll"]["flick"] = []
    C.update(panels=panels, flicks=[] if NOFLICK else [[0, 2.2, "THEY SAID:", 200]], audio=AUDIO, sections=[[0, END]])
    json.dump(C, open(P("config.json"), "w"), indent=1, ensure_ascii=False)
    print("panels", [(p[0], p[1], os.path.basename(p[3]["src"])) for p in panels], "| sounds", len(AUDIO))

elif STEP == "zoom":    # 5% in, his face centred every frame; where there's no face (his graphics), the middle
    import cv2
    C = json.load(open(P("config.json"))); END = C["end"]
    SW, SH = map(int, subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-of", "csv=p=0", P("cut.mov")],
                                     capture_output=True, text=True).stdout.strip().split(","))
    fp = P("faces.json")
    if not os.path.exists(fp):
        w, h = SW // 4, SH // 4; out = []
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", P("cut.mov"), "-vf", f"select='not(mod(n\\,3))',scale={w}:{h}", "-vsync", "0", "-f", "rawvideo", "-pix_fmt", "gray", "-"], stdout=subprocess.PIPE)
        cas = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml"); i = 0
        while len(b := p.stdout.read(w * h)) == w * h:
            fs = cas.detectMultiScale(np.frombuffer(b, np.uint8).reshape(h, w), 1.1, 5, minSize=(30, 30))
            if len(fs): x, y, fw, fh = max(fs, key=lambda r: r[2] * r[3]); out.append([i * 3, (x + fw / 2) / w, (y + fh / 2) / h])
            i += 1
        json.dump(out, open(fp, "w"))
    F = np.array(json.load(open(fp))); F = F[(abs(F[:, 2] - np.median(F[:, 2])) < 0.06) & (abs(F[:, 1] - np.median(F[:, 1])) < 0.12)]
    N = round(END * 30); fr = np.arange(N)
    near = np.array([np.min(np.abs(F[:, 0] - n)) <= 15 for n in fr])          # his face within half a second: he's on camera
    fx = np.where(near, np.interp(fr, F[:, 0], F[:, 1]), 0.5); fy = np.where(near, np.interp(fr, F[:, 0], F[:, 2]), 0.5)
    ker = np.ones(31) / 31; sm = lambda a: np.convolve(np.pad(a, 15, mode="edge"), ker, "valid")[:N]
    fx, fy = sm(fx), sm(fy)
    Z = 1.05; cw, ch = SW / Z, SH / Z
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", P("cut.mov"), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920", "-r", "30", "-i", "-", "-i", P("cut.mov"),
                            "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", "-shortest", P("base.mov")], stdin=subprocess.PIPE)
    off = []
    for n in range(N):
        b = dec.stdout.read(SW * SH * 3)
        if len(b) < SW * SH * 3: break
        x0 = min(max(fx[n] * SW - cw / 2, 0), SW - cw); y0 = min(max(fy[n] * SH - (0.36 if near[n] else 0.5) * ch, 0), SH - ch)
        M = np.float32([[1080 / cw, 0, -x0 * 1080 / cw], [0, 1920 / ch, -y0 * 1920 / ch]])
        enc.stdin.write(cv2.warpAffine(np.frombuffer(b, np.uint8).reshape(SH, SW, 3), M, (1080, 1920), flags=cv2.INTER_LANCZOS4).tobytes())
        if near[n]: off.append(round((fx[n] * SW - x0) / cw, 3))
    enc.stdin.close(); enc.wait(); dec.stdout.close()
    print("his face across the screen:", min(off), "to", max(off), "(0.5 = centre)")
if STEP in ("zoom", "selfs") and not os.environ.get("NOFLICK"):   # the flicker's clips: tight on his face only (his edit's captions and titles sit lower and behind him)
    LOOK = ["crop=iw*.42:ih*.3:iw*.29:ih*.2", "hue=s=0,eq=contrast=1.35:brightness=-.03,crop=iw*.46:ih*.32:iw*.27:ih*.19", "crop=iw*.38:ih*.27:iw*.31:ih*.21",
            "hue=s=0,crop=iw*.34:ih*.24:iw*.33:ih*.22", "crop=iw*.44:ih*.31:iw*.28:ih*.2", "hue=s=0,crop=iw*.4:ih*.28:iw*.3:ih*.2"]
    for k, t in enumerate(SELF):
        os.makedirs(P(f"broll/self{k}"), exist_ok=True)
        sh("ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", P("base.mov"), "-t", "1", "-vf", f"{LOOK[k]},scale=960:1640:force_original_aspect_ratio=increase,crop=960:1640",
           "-q:v", "3", P(f"broll/self{k}/%04d.jpg"))

if STEP == "finish":  # 1.1x, then levelled to -14.5 LUFS with true peaks under -1.5 dB (the mix can go over full scale: kept in float, never clipped)
    tmp = P("fast.mp4")
    sh("ffmpeg", "-v", "error", "-y", "-i", P("reel.mp4"), "-filter_complex", "[0:v]setpts=PTS/1.1[v];[0:a]atempo=1.1[a]", "-map", "[v]", "-map", "[a]",
       "-c:v", "libx264", "-crf", "19", "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "pcm_f32le", tmp.replace(".mp4", ".mov"))
    sh("ffmpeg", "-v", "error", "-y", "-i", tmp.replace(".mp4", ".mov"), "-c:v", "copy", "-af", "acompressor=threshold=0.35:ratio=20:attack=0.1:release=60:makeup=1,aresample=192000,loudnorm=I=-14.5:TP=-1.5:LRA=11,aresample=48000",
       "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", P("ahad-recut.mp4"))
    os.remove(tmp.replace(".mp4", ".mov")); print("ahad-recut.mp4", round(dur(P("ahad-recut.mp4")), 1), "s")
