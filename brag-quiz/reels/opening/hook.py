#!/usr/bin/env python3
"""The salah hooks (owner, 9 Nov 2026; RAW/salah hook: "do not pray.mp4", "ghushu.mp4", 4-4.5 s each): "reduce the brightness, a darker
border around the video, make just my body outline flicker 3 times quite quickly with the flicker sound effect, and a very bold, in your face
caption in the upper third, yellow with a black outline: 'before you pray' or 'do not pray until'".
  - darker (0.8) and a soft dark vignette all round;
  - his outline: his body found in each frame (rembg, u2net_human_seg), a glowing white edge round it, on for 2 frames and off for 2, three
    times from 0.1 s, each flash with one of the flicker sounds (sfx/ref/flicker-v1..3);
  - the line in Anton, yellow (#FFD60A) with a thick black outline and a dark shadow, upper third, landing slightly big and settling;
  - his voice as recorded, levelled to -14.5 LUFS.

  python3 hook.py WORK "LINE ONE|LINE TWO" [TOP]     (WORK/clip.mp4) → WORK/hook.mp4
"""
import os, subprocess, sys
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont
W, TITLE = sys.argv[1], sys.argv[2].split("|"); TOP = int(sys.argv[3]) if len(sys.argv) > 3 else 470; FPS = 30; VW, VH = 1080, 1920   # TOP: just under his face (his head starts ~150 px down)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sh = lambda *a: subprocess.run(list(a), check=True)
os.makedirs(os.path.join(W, "fr"), exist_ok=True); os.makedirs(os.path.join(W, "out"), exist_ok=True)
if not os.listdir(os.path.join(W, "fr")):
    sh("ffmpeg", "-v", "error", "-i", os.path.join(W, "clip.mp4"), "-vf", f"scale={VW}:{VH}:flags=lanczos,fps={FPS}", os.path.join(W, "fr", "%04d.png"))
frames = sorted(os.listdir(os.path.join(W, "fr"))); N = len(frames)
FLASH = [3 + 4 * k + j for k in range(3) for j in range(2)]      # frames 3-4, 7-8, 11-12: on 2, off 2, three times (from 0.1 s)

from fontTools.ttLib import TTFont
anton = os.path.join(W, "anton.ttf")
if not os.path.exists(anton):
    f = TTFont(os.path.join(ROOT, "brag-quiz", "fonts", "anton-latin-400-normal.woff2")); f.flavor = None; f.save(anton)
an = ImageFont.truetype(anton, 190)
def title():
    img = Image.new("RGBA", (VW, 560), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    for i, ln in enumerate(TITLE):
        x = (VW - an.getlength(ln)) / 2; y = 30 + i * 230
        d.text((x + 8, y + 12), ln, font=an, fill=(0, 0, 0, 170), stroke_width=16, stroke_fill=(0, 0, 0, 170))
        d.text((x, y), ln, font=an, fill=(255, 214, 10), stroke_width=14, stroke_fill=(8, 8, 8))
    return img
TT = title()
yy, xx = np.mgrid[0:VH, 0:VW]
vig = np.clip(1.08 - 0.75 * (((xx - VW / 2) / (VW * 0.62)) ** 2 + ((yy - VH * 0.5) / (VH * 0.58)) ** 2), 0.22, 1)[..., None]

session = None
for n, name in enumerate(frames):
    im = Image.open(os.path.join(W, "fr", name)).convert("RGB")
    a = np.asarray(im, float) * 0.8 * vig                     # darker, and the dark border
    out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    if n in FLASH:                                            # his outline, glowing
        if session is None:
            from rembg import new_session, remove
            session = new_session("u2net_human_seg")
        m = remove(im.resize((540, 960)), session=session, only_mask=True).resize((VW, VH), Image.BILINEAR).point(lambda v: 255 if v > 128 else 0)
        edge = ImageChops.subtract(m.filter(ImageFilter.MaxFilter(17)), m)
        glow = edge.filter(ImageFilter.GaussianBlur(14)); core = edge.filter(ImageFilter.GaussianBlur(2))
        for layer, col in ((glow, (255, 240, 180)), (core, (255, 255, 255))):
            c = Image.new("RGBA", (VW, VH), col + (0,)); c.putalpha(layer.point(lambda v: min(255, v * 2))); out = Image.alpha_composite(out, c)
    t = n / FPS; s = 1 + 0.12 * (1 - min(1, t / 0.18)) ** 2      # the line lands slightly big and settles
    tt = TT.resize((int(VW * s), int(TT.size[1] * s)), Image.LANCZOS) if s > 1.001 else TT
    out.alpha_composite(tt, ((VW - tt.size[0]) // 2, TOP - (tt.size[1] - TT.size[1]) // 2))
    out.convert("RGB").save(os.path.join(W, "out", name))

SFX = os.path.join(ROOT, "brag-quiz", "sfx", "ref"); hits = [FLASH[0] / FPS, FLASH[2] / FPS, FLASH[4] / FPS]
ins = sum((["-i", os.path.join(SFX, f"flicker-v{k + 1}.wav")] for k in range(3)), [])
fc = "".join(f"[{k + 2}:a]aresample=48000,aformat=channel_layouts=stereo,volume=0.9,adelay={int(h * 1000)}|{int(h * 1000)}[f{k}];" for k, h in enumerate(hits))
fc += "[1:a]aresample=48000,aformat=channel_layouts=stereo[v];[v][f0][f1][f2]amix=inputs=4:normalize=0:duration=first,aresample=192000,loudnorm=I=-14.5:TP=-1.5:LRA=11,aresample=48000[a]"
sh("ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", os.path.join(W, "out", "%04d.png"), "-i", os.path.join(W, "clip.mp4"), *ins,
   "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-crf", "18", "-preset", "slow", "-pix_fmt", "yuv420p",
   "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", os.path.join(W, "hook.mp4"))
print("hook.mp4", N / FPS, "s")
