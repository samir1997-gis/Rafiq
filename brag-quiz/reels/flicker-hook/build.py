"""The flicker hook (owner, 12 Oct 2026): a locked landscape take of the owner in different spots of the room, ending in front
of the camera with the hook line. The spots flicker inside a red-framed panel (the whole room, so it stays still while he
jumps), the panel opens out to the vertical frame on him, and the line plays with the house standard (FORMATS.md): the first
word slammed on with a crash and a shake, the rest word by word, a zoom step on each stressed word. Graded with the template.

  python3 build.py /tmp/reel-flick1      (needs clip.mp4 from `reel.py <W> fetch <id>`; writes <W>/hook.mp4)
Times below are for the first take (Drive 1qz_Vbkwp_7egQqQ0gBWILlkGM1VwDh3A); a new take needs new POSES/WORDS/CX.
"""
import os, sys, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
HERE = os.path.dirname(os.path.abspath(__file__)); BQ = os.path.join(HERE, "..", "..")
sys.path.insert(0, os.path.join(HERE, "..", "template")); import sfx_rules as SR
W = sys.argv[1]; SRC = os.path.join(W, "clip.mp4"); FPS, OW, OH = 30, 1080, 1920
GRADE = open(os.path.join(HERE, "..", "template", "grade.txt")).read().strip()
RED, GOLD, WHITE = (180, 50, 42), (233, 185, 73), (255, 255, 255)

# the take: where he holds still in each spot (s), and the line (s in the take)
POSES = {"door": 18.0, "near": 22.4, "room": 2.0, "sofa": 28.2, "cross": 32.8, "mid": 37.2, "walk": 38.3}
SEQ = [("door", 5), ("near", 4), ("room", 3), ("sofa", 4), ("cross", 4), ("mid", 3), ("door", 2), ("sofa", 2), ("cross", 2),
       ("near", 2), ("mid", 2), ("walk", 2), ("room", 1), ("sofa", 2), ("door", 1), ("mid", 1)]     # faster and faster
FRONT, S0 = 44.55, 45.22          # in front of the camera, and the take time where the panel starts to open
CX, CY_FACE = 2150, 420           # his centre (x) and face (y) in the 4K frame when he's in front
WORDS = [("pray", 45.98), ("another", 46.12), ("salah", 46.45), ("without", 47.08), ("doing", 47.78), ("this", 48.38), ("first.", 48.90)]
SLAM, SLAM_T, END = "DON'T", 45.65, 49.75
LINES = [[0, 1, 2], [3, 4], [5, 6]]; GOLDW = {5, 6}; STEPS = {5: 1.10, 6: 1.16}
TITLE = "BEFORE YOU PRAY"

o = lambda src_t: 2.0 + (src_t - S0)            # take time → output time
F_EXP, F_MAIN = 60, 71                          # the panel opens over frames 60-70, then the vertical frame
N = round(o(END) * FPS)
font = lambda n, s: ImageFont.truetype(os.path.join(W, n + ".ttf"), s)
for n in ("anton-latin-400-normal", "instrument-serif-latin-400-normal"):      # PIL can't read woff2
    if not os.path.exists(os.path.join(W, n + ".ttf")):
        from fontTools.ttLib import TTFont
        f = TTFont(os.path.join(BQ, "fonts", n + ".woff2")); f.flavor = None; f.save(os.path.join(W, n + ".ttf"))
ANTON, SERIF = (lambda s: font("anton-latin-400-normal", s)), (lambda s: font("instrument-serif-latin-400-normal", s))

def frames(t0, n, w, h):
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-i", SRC, "-frames:v", str(n), "-vf", f"scale={w}:{h},{GRADE}",
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    return [Image.fromarray(np.frombuffer(p, np.uint8)[k * w * h * 3:(k + 1) * w * h * 3].reshape(h, w, 3)) for k in range(len(p) // (w * h * 3))]

def text(s, f, fill, stroke=0, sc=None):
    b = f.getbbox(s, stroke_width=stroke); im = Image.new("RGBA", (b[2] - b[0] + 40, b[3] - b[1] + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im); d.text((20 - b[0], 20 - b[1]), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=sc); return im

def shadowed(im, r=10, a=150):
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.putalpha(im.getchannel("A").point(lambda v: v * a // 255))
    out = Image.new("RGBA", im.size, (0, 0, 0, 0)); out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(r)), (0, 6)); out.alpha_composite(im); return out

def paste_c(base, im, cx, cy, scale=1.0, rot=0, alpha=1.0):
    if scale != 1.0: im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.BICUBIC)
    if rot: im = im.rotate(rot, Image.BICUBIC, expand=True)
    if alpha < 1: im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * alpha)))
    base.alpha_composite(im, (round(cx - im.width / 2), round(cy - im.height / 2)))

def blurred_bg(img):              # the frame behind the panel: the same picture, cover-cropped, blurred and dark
    w, h = img.size; cw = h * OW // OH; bg = img.crop(((w - cw) // 2, 0, (w + cw) // 2, h)).resize((OW // 4, OH // 4))
    return ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(8))).enhance(0.42).resize((OW, OH)).convert("RGBA")

def ease(p): return 4 * p ** 3 if p < .5 else 1 - (-2 * p + 2) ** 3 / 2
out = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{OW}x{OH}", "-r", str(FPS), "-i", "-",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", os.path.join(W, "hook-v.mp4")], stdin=subprocess.PIPE)
title = shadowed(text(TITLE, ANTON(132), WHITE))
PX, PY, PW, PH = 40, 679, 1000, 562                                     # the panel
sounds = [("flash-flicker", "hit", 0.02, 0), ("n02", "swoosh", 0.25, 0)]

# 1. the flicker
clips = {k: frames(t, 16, 1280, 720) for k, t in POSES.items()}; clips["front"] = frames(FRONT, F_EXP - sum(n for _, n in SEQ), 1280, 720)
seq = SEQ + [("front", len(clips["front"]))]; head = {k: 0 for k in clips}; i = 0; prev = None
for si, (k, n) in enumerate(seq):
    for j in range(n):
        img = clips[k][head[k]]; head[k] += 1
        if j == 0 and prev and si % 3 == 2 and n > 1: img = clips[prev][max(0, head[prev] - 1)]      # one frame flicks back
        fr = blurred_bg(img); pnl = img.resize((PW, PH))
        if j == 0 and si: pnl = Image.blend(pnl, Image.new("RGB", pnl.size, WHITE), 0.45)            # a white flash on each switch
        fr.paste(pnl, (PX, PY)); ImageDraw.Draw(fr).rectangle((PX - 14, PY - 14, PX + PW + 13, PY + PH + 13), outline=RED, width=14)
        paste_c(fr, title, OW / 2, 520, 1.0 + 0.03 * (i % 2))
        out.stdin.write(fr.convert("RGB").tobytes()); i += 1
    prev = k
for k in range(0, F_EXP - 6, 8): sounds.append((SR.POOL["flick"][(k // 8) % 3], "flicker", k / FPS, 0))
sounds += [("swoosh", "swoosh", (F_EXP - 2) / FPS, 0), ("shutter", "hit", F_EXP / FPS, 0)]

# 2. the panel opens out to the vertical frame, then the line
s0, s1 = PW / 3840, OH / 2160; X0 = CX - OW / s1 / 2                 # the vertical crop: centred on him, full height
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{S0:.3f}", "-i", SRC, "-frames:v", str(N - F_EXP), "-vf", GRADE,
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
slam = shadowed(text(SLAM, ANTON(330), RED, 8, WHITE), 14, 170)
wim = [shadowed(text(w, SERIF(150 if k in GOLDW else 128), GOLD if k in GOLDW else WHITE), 8, 170) for k, (w, _) in enumerate(WORDS)]
def zoom_at(t):
    z = 1.0 + 0.012 * max(0, t - o(SLAM_T))                                 # a slow push
    if t >= o(SLAM_T): z += 0.05 * min(1, (t - o(SLAM_T)) / 0.12)
    for k, zz in STEPS.items():
        a = o(WORDS[k][1])
        if t >= a: r = min(1, (t - a) / 0.1); z = max(z, zz * r + z * (1 - r))
    return z
SHAKE = [(-34, 22, -1.4), (30, -18, 1.2), (-22, 14, -.8), (16, -10, .6), (-8, 6, -.3), (0, 0, 0)]
for i in range(F_EXP, N):
    raw = dec.stdout.read(3840 * 2160 * 3)
    if len(raw) < 3840 * 2160 * 3: break
    src = Image.fromarray(np.frombuffer(raw, np.uint8).reshape(2160, 3840, 3)); t = i / FPS
    if i < F_MAIN:                                                          # the opening: panel rect → full frame
        p = ease((i - F_EXP + 1) / (F_MAIN - F_EXP)); s = s0 * (s1 / s0) ** p
        R = [PX + (0 - PX) * p, PY + (0 - PY) * p, PX + PW + (OW - PX - PW) * p, PY + PH + (OH - PY - PH) * p]
        ax, ay = (PX + CX * s0) * (1 - p) + ((CX - X0) * s1) * p, (PY + 1080 * s0) * (1 - p) + 1080 * s1 * p
        box = [CX + (R[0] - ax) / s, 1080 + (R[1] - ay) / s, CX + (R[2] - ax) / s, 1080 + (R[3] - ay) / s]
        fr = blurred_bg(src.resize((1280, 720)))
        cb = [max(0, box[0]), max(0, box[1]), min(3840, box[2]), min(2160, box[3])]
        pc = src.crop(tuple(round(v) for v in cb)).resize((max(1, round((cb[2] - cb[0]) * s)), max(1, round((cb[3] - cb[1]) * s))))
        fr.paste(pc, (round(R[0] + (cb[0] - box[0]) * s), round(R[1] + (cb[1] - box[1]) * s)))
        if p < 1:
            ov = Image.new("RGBA", (OW, OH), (0, 0, 0, 0)); ImageDraw.Draw(ov).rectangle((R[0] - 14, R[1] - 14, R[2] + 13, R[3] + 13), outline=RED + (round(255 * (1 - p)),), width=14); fr.alpha_composite(ov)
        paste_c(fr, title, OW / 2, 520 - 300 * p, 1.0, 0, max(0, 1 - 2 * p))
    else:                                                                   # the vertical frame, with zoom steps and the shake
        z = zoom_at(t); ds = t - o(SLAM_T); dx = dy = rot = 0
        if 0 <= ds < 0.25: dx, dy, rot = SHAKE[min(5, int(ds / 0.04))]
        sc = s1 * z * (1.04 if rot else 1); ax, ay = (CX - X0) * s1, CY_FACE * s1
        box = (CX + (0 - ax - dx) / sc, CY_FACE + (0 - ay - dy) / sc, CX + (OW - ax - dx) / sc, CY_FACE + (OH - ay - dy) / sc)
        fr = src.resize((OW, OH), Image.BICUBIC, box=box).convert("RGBA")
        if rot: fr = fr.rotate(rot, Image.BICUBIC)
    if i >= F_MAIN:
        ds = t - o(SLAM_T); end = o(WORDS[0][1])
        if -0.13 <= ds and t < end + 0.12:                                   # "DON'T": huge, slams down, squash, then gone as "pray" comes
            if ds < 0: sc_, rot_ = 1 + 1.2 * (-ds / 0.13) ** 2, -7 * (-ds / 0.13)
            else: sc_, rot_ = 1 + 0.12 * np.exp(-ds * 18) * np.cos(ds * 40), 0
            a = 1 if t < end else max(0, 1 - (t - end) / 0.12)
            if 0 <= ds < 0.55:                                                # shockwave rings and sparks
                q = ds / 0.55; ov = Image.new("RGBA", (OW, OH), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
                for k, (col, wd) in enumerate([(GOLD, 14), (RED, 8)]):
                    r = 60 + 620 * (1 - (1 - max(0, q - k * .12)) ** 3); al = round(230 * max(0, 1 - q))
                    d.ellipse((540 - r, 1250 - r, 540 + r, 1250 + r), outline=col + (al,), width=wd)
                for k in range(10):
                    ang = k * np.pi / 5; r0, r1 = 200 + 300 * q, 260 + 420 * q
                    d.line((540 + r0 * np.cos(ang), 1250 + r0 * np.sin(ang), 540 + r1 * np.cos(ang), 1250 + r1 * np.sin(ang)), fill=GOLD + (round(255 * (1 - q)),), width=12)
                fr.alpha_composite(ov)
            paste_c(fr, slam, OW / 2, 1250, sc_ * (1.08 if 0 <= ds < .06 else 1), rot_, a)
        if 0 <= ds < 0.3: fr.alpha_composite(Image.new("RGBA", (OW, OH), (255, 248, 230, round(215 * (1 - ds / 0.3)))))
        for line in LINES:                                                  # the rest of the line, word by word
            t0 = o(WORDS[line[0]][1]); nxt = [l for l in LINES if WORDS[l[0]][1] > WORDS[line[0]][1]]
            t1 = o(WORDS[nxt[0][0]][1]) - 0.05 if nxt else 99
            if not t0 - 0.05 <= t < t1: continue
            ims = [wim[k] for k in line]; gap = 4; tot = sum(m.width for m in ims) + gap * (len(ims) - 1); x = OW / 2 - tot / 2
            for k, m in zip(line, ims):
                dt = t - o(WORDS[k][1])
                if dt >= -0.03:
                    pop = 1 + (0.45 if k in GOLDW else 0.25) * max(0, 1 - dt / 0.14)
                    paste_c(fr, m, x + m.width / 2, 1290, pop, 0, min(1, (dt + 0.03) / 0.08))
                x += m.width + gap
    out.stdin.write(fr.convert("RGB").tobytes())
out.stdin.close(); out.wait(); dec.stdout.close(); dec.wait()

# 3. sound: the take's own audio (cleaned), the crash on the slam, a tap per caption line, a hit on each zoom step
sounds += [("crash", "boom", o(SLAM_T), 5)]
for line in LINES: sounds.append((SR.POOL["text"][LINES.index(line) % 3], "text", o(WORDS[line[0]][1]), 0))
for n, k in enumerate(sorted(STEPS)): sounds.append((["n10", "shutter"][n], "hit", o(WORDS[k][1]), 2 * n))
dur = N / FPS; a0 = S0 - 2.0
cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{a0:.3f}", "-t", f"{dur:.3f}", "-i", SRC]; fl = [
    "[0:a]highpass=f=80,lowpass=f=13000,afftdn=nr=18:nf=-66,acompressor=threshold=-24dB:ratio=3:attack=8:release=120,loudnorm=I=-15:TP=-2:LRA=9[v]"]
for k, (name, kind, at, boost) in enumerate(sounds):
    f = os.path.join(BQ, "sfx", "crash.wav") if name == "crash" else SR.F(name); pk, pat = SR.info(f)
    cmd += ["-i", f]; d = max(0, at - pat)
    fl.append(f"[{k + 1}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={SR.LEVEL[kind] + boost - pk:.1f}dB,adelay={int(d * 1000)}:all=1[s{k}]")
fl.append("[v]aformat=sample_rates=48000:channel_layouts=stereo[vv];[vv]" + "".join(f"[s{k}]" for k in range(len(sounds)))
          + f"amix=inputs={len(sounds) + 1}:normalize=0:duration=first,alimiter=limit=0.7:level=disabled[a]")
subprocess.run(cmd + ["-filter_complex", ";".join(fl), "-map", "[a]", "-c:a", "pcm_s16le", os.path.join(W, "hook-mix.wav")], check=True)
import json, re                                                         # level the mix: -14.5 LUFS, true peak under -1 dB after AAC (-2.5 before)
m = subprocess.run(["ffmpeg", "-hide_banner", "-i", os.path.join(W, "hook-mix.wav"), "-af", "loudnorm=I=-14.5:TP=-2.5:LRA=11:print_format=json",
                    "-f", "null", "-"], capture_output=True, text=True).stderr; J = json.loads(re.search(r"\{[^{}]*\}", m).group())
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(W, "hook-mix.wav"), "-af", f"loudnorm=I=-14.5:TP=-2.5:LRA=11:measured_I={J['input_i']}:"
                f"measured_TP={J['input_tp']}:measured_LRA={J['input_lra']}:measured_thresh={J['input_thresh']}:offset={J['target_offset']}:linear=true",
                "-ar", "48000", "-c:a", "pcm_s16le", os.path.join(W, "hook-a.wav")], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(W, "hook-v.mp4"), "-i", os.path.join(W, "hook-a.wav"), "-c:v", "copy",
                "-c:a", "aac", "-b:a", "192k", "-shortest", os.path.join(W, "hook.mp4")], check=True)
print("hook.mp4", round(dur, 2), "s")
