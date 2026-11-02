#!/usr/bin/env python3
"""The Dajjāl video's two intros (owner, 2 Nov 2026, #316: "I filmed myself in several different positions… have me appear several
times… from a wide angle… zooms into me quite rapidly… use while I'm holding my finger up as a reference point. Do that for both hooks"):
  the whole room, wide (1048, him on the sofa saying the hook), framed in the middle of the vertical video over a blurred, darkened copy of
  itself, the hook as a title in the band above; clones of him (from 1044, the same locked-off framing) pop in on his words; then a push
  into him that fills the screen, the real camera move (1052, sped up), and the cut onto his raised finger in the talking take (1059),
  where the main edit starts ("Let me explain").
  A  "Did you know there is more than one Dajjāl?"  the clones land on "more", "than", "one", "Dajjāl"
  B  "The Prophet ﷺ spoke about 30 dajjāls, but most people only know the one."  all on "30 dajjāls", gone again on "only know the one"
Each clone is cut out against the empty room (1044 at 39.5 s, same take, same light), only inside a box round where he stands (the sun
moved during the take), and brought to the hook shot's light by matching the background. Sounds as sfx_rules: against his voice.

  python3 intro.py RAW A|B      (RAW holds 1044.mp4 1048.mp4 1052.mp4 1059.mp4)  → RAW/intro-A.mov
"""
import os, subprocess, sys
import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont, ImageFilter
RAW, V = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE))); SFX = os.path.join(ROOT, "brag-quiz/sfx")
W, H, FPS = 1080, 1920, 30
WX0, WW = 480, 2880                                   # the room: 4K x 480..3360, all of it high (2160) → 4:3
CW, CH = 2160, 1620                                   # worked at twice the size it shows, so the push-in stays sharp
SHOW = (W, round(W * CH / CW))                        # 1080 x 810 on screen
TOP = (H - SHOW[1]) // 2 - 60                         # a little above the middle: the title band above, captions below
FACE = (1920 - WX0) / WW * CW, 760 / 2160 * CH        # his face in the worked frame (sitting in the middle of the sofa)
GRADE = "eq=contrast=1.06:saturation=1.08:gamma=1.02" # as the template's base
src = lambda n: os.path.join(RAW, n + ".mp4")
def reader(f, t0, vf, w, h):                           # frames one at a time (a 4K take doesn't fit in memory)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{t0}", "-i", f, "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    while True:
        b = p.stdout.read(w * h * 3)
        if len(b) < w * h * 3: p.kill(); return
        yield np.frombuffer(b, np.uint8).reshape(h, w, 3)
ROOM = f"crop={WW}:2160:{WX0}:0,fps={FPS},scale={CW}:{CH}"
room_frames = lambda f, t0: reader(src(f), t0, ROOM, CW, CH)
take = lambda f, t0, n: [fr.copy() for _, fr in zip(range(n), room_frames(f, t0))]

HOOK = {"A": (18.35, 22.05, [20.04, 20.28, 20.56], None, ("MORE THAN", "ONE?")),
        "B": (7.05, 14.5, [10.32, 10.62, 10.94], 13.32, ("30", "DAJJĀLS"))}[V]
t0, t1, ins, outs, title = HOOK
n = round((t1 - t0) * FPS)
plate = take("1044", 39.5, 1)[0].astype(np.float32)
# the clones: (time in 1044, ping-pong span, where he is in 4K x): standing on the left, sitting on the right end, standing on the right
# (the ones close to the lens covered him or were cut off by the frame's edge)
CLONES = [(8.05, 0.2, 1430), (18.0, 0.8, 2640), (21.8, 0.8, 2470)]
def clone(tc, span, x4k):
    fr = take("1044", tc, max(2, round(span * FPS)))
    cx = (x4k - WX0) / WW * CW; box = np.zeros((CH, CW), bool); box[:, max(0, int(cx - 420)):int(cx + 420)] = True
    ms = []
    for f in fr:                                       # the person, cut out as the template does (rembg), only in his box
        m = np.asarray(remove(Image.fromarray(f), session=SEG, only_mask=True)).astype(np.float32) / 255 * box
        lab, k = ndimage.label(m > 0.5)
        if k: m = m * ndimage.binary_dilation(lab == (1 + int(np.argmax(ndimage.sum(m > 0.5, lab, range(1, k + 1))))), iterations=6)
        ms.append((np.clip(ndimage.gaussian_filter(m, 1.5), 0, 1) * 255).astype(np.uint8))
    return fr + fr[::-1], ms + ms[::-1]                # ping-pong, so a short still moment can loop
from rembg import remove, new_session
SEG = new_session("u2net_human_seg")
cl = [clone(*c) for c in CLONES]
# the light: the hook shot against the empty room, per channel, on what no one covers
first = take("1048", t0, 1)[0].astype(np.float32)
bg = ~ndimage.binary_dilation(ndimage.gaussian_filter(np.abs(first - plate).mean(2), 2) > 40, iterations=40)
gain = np.array([np.median(first[..., c][bg]) / max(1, np.median(plate[..., c][bg])) for c in range(3)])
print("light gain", gain.round(3))

# the title in the band above (Anton, the house title font), drawn once
def ttf():
    out = os.path.join(RAW, "anton.ttf")
    if not os.path.exists(out):
        from fontTools.ttLib import TTFont
        f = TTFont(os.path.join(ROOT, "brag-quiz/fonts/anton-latin-400-normal.woff2")); f.flavor = None; f.save(out)
    return out
def title_img(small, big):
    im = Image.new("RGBA", (W, 330), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for txt, size, y, col in ((small, 92, 20, (241, 236, 224, 255)), (big, 150, 120, (233, 185, 73, 255))):
        f = ImageFont.truetype(ttf(), size); w = d.textlength(txt, font=f)
        d.text(((W - w) / 2 + 4, y + 6), txt, font=f, fill=(0, 0, 0, 160)); d.text(((W - w) / 2, y), txt, font=f, fill=col)
    return np.asarray(im).astype(np.float32)
TITLE = title_img(*title)

def frame_out(room, i, zoom=1.0):
    """the vertical frame: the room in the middle over its own blurred, darkened copy, the title above; zoom > 1 pushes into his face"""
    t = i / FPS
    if zoom > 1.0:                                    # the push: the window shrinks round his face
        sw, sh = CW / zoom, CH / zoom
        x = min(max(0, FACE[0] - sw / 2), CW - sw); y = min(max(0, FACE[1] - sh / 2), CH - sh)
        room = np.asarray(Image.fromarray(room).crop((int(x), int(y), int(x + sw), int(y + sh))).resize((CW, CH), Image.BILINEAR))
    fill = min(1.0, (zoom - 1) / 1.6)                 # and the room grows to fill the height as it does
    hh = round(SHOW[1] + (H - SHOW[1]) * fill); ww = round(W * hh / SHOW[1])
    big = np.asarray(Image.fromarray(room).resize((ww, hh), Image.LANCZOS)).astype(np.float32)
    small = Image.fromarray(room).resize((W // 4, SHOW[1] // 4))
    back = np.asarray(small.resize((round(W * H / SHOW[1]) // 4, H // 4)).filter(ImageFilter.GaussianBlur(7)).resize((round(W * H / SHOW[1]), H))).astype(np.float32)
    bx = (back.shape[1] - W) // 2; out = back[:, bx:bx + W] * 0.42
    top = round(TOP * (1 - fill)); x0 = (ww - W) // 2
    out[top:top + hh] = big[:H - top, x0:x0 + W]
    if fill < 0.5:                                    # the title, gone as the push starts
        a = TITLE[..., 3:] / 255 * (1 - fill * 2) * min(1, t / 0.25)
        y = max(0, top - 320); out[y:y + 330] = out[y:y + 330] * (1 - a) + TITLE[..., :3] * a
    return out

frames_out = []
push = 0.42                                            # the last 0.42 s of the hook: the push into his face (eases in)
for i, room in zip(range(n), room_frames("1048", t0)):
    t = t0 + i / FPS; o = room.astype(np.float32)
    for k, (fr, ms) in enumerate(cl):
        a = ins[k]
        if t < a: continue
        p = 1 - (1 - min(1.0, (t - a) / 0.14)) ** 3                     # pops on, easing out
        if outs and t >= outs + k * 0.12: p *= max(0.0, 1 - (t - outs - k * 0.12) / 0.14) ** 2   # and off, easing in
        if p <= 0: continue
        j = int((t - a) * FPS) % len(fr)
        al = (ms[j].astype(np.float32) / 255 * p)[..., None]
        o = o * (1 - al) + np.clip(fr[j].astype(np.float32) * gain, 0, 255) * al
    for a in ins:                                                      # a flash as each one lands
        if 0 <= t - a < 0.12: o = o + (255 - o) * 0.22 * (1 - (t - a) / 0.12)
    u = (t - (t1 - push)) / push
    z = 1.0 + 1.6 * u ** 2 if u > 0 else 1.0                          # eases in (power2.in)
    frames_out.append(np.clip(frame_out(np.clip(o, 0, 255).astype(np.uint8), i, z), 0, 255).astype(np.uint8))
# the real camera move, 2.5x, him centred (a vertical window on the 4K move), a light blend for motion
RUSH = f"crop=1215:2160:1312:0,setpts=PTS/2.5,fps={FPS},scale={W}:{H}"
rush = [f.copy() for _, f in zip(range(20), reader(src("1052"), 2.5, RUSH, W, H))]
for k in range(len(rush)):
    a = rush[k].astype(np.float32); b = rush[min(len(rush) - 1, k + 1)].astype(np.float32)
    frames_out.append(np.clip(a * 0.75 + b * 0.25, 0, 255).astype(np.uint8))
tmp = os.path.join(RAW, f"intro-{V}-v.mov")
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                      "-vf", f"{GRADE},format=yuv420p", "-c:v", "libx264", "-crf", "14", "-preset", "medium", tmp], stdin=subprocess.PIPE)
for f in frames_out: p.stdin.write(f.tobytes())
p.stdin.close(); p.wait()
D = len(frames_out) / FPS
# sound: his hook as recorded, a pop on each clone, a whoosh into the push, a hit as the move lands
sys.path.insert(0, os.path.join(HERE, "..", "template")); from sfx_rules import info
voice = os.path.join(RAW, f"intro-{V}-voice.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0}", "-t", f"{t1 - t0:.3f}", "-i", src("1048"), "-vn", "-ac", "2", "-ar", "48000",
                "-af", f"afade=t=out:st={t1 - t0 - 0.12:.3f}:d=0.12,apad=whole_dur={D:.3f}", voice], check=True)
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", voice, "-ac", "1", "-f", "s16le", "-"], capture_output=True).stdout, np.int16) / 32768
VP = float(np.percentile(20 * np.log10(np.sqrt(np.convolve(x ** 2, np.ones(2400) / 2400, "valid"))[::1200] + 1e-9), 90))
fx = [("tap", a - t0, -2) for a in ins] + [("whoosh", (t1 - t0) - push, 0), ("impact", D - 0.05, -4)]
if outs: fx += [("swoosh", outs - t0 + 0.05, -6)]
ins_, flt = ["-i", voice], []
for k, (name, at, db) in enumerate(fx):
    f = next(os.path.join(SFX, d, name + ".wav") for d in ("soft", "ref", ".") if os.path.exists(os.path.join(SFX, d, name + ".wav")))
    pk_db, pk = info(f)
    ins_ += ["-i", f]                                  # input 0 is the picture, 1 his voice, the effects from 2
    flt.append(f"[{k + 2}:a]aresample=48000,aformat=channel_layouts=stereo,volume={10 ** ((VP + db - pk_db) / 20):.3f},adelay={max(0, int((at - pk) * 1000))}:all=1[s{k}]")
flt.append("[1:a]" + "".join(f"[s{k}]" for k in range(len(fx))) + f"amix=inputs={len(fx) + 1}:normalize=0:duration=first[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, *ins_, "-filter_complex", ";".join(flt), "-map", "0:v", "-map", "[a]",
                "-c:v", "copy", "-c:a", "pcm_s16le", os.path.join(RAW, f"intro-{V}.mov")], check=True)
print(V, "intro", round(D, 2), "s")
