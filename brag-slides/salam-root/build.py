#!/usr/bin/env python3
"""A TikTok slideshow from the owner's seven slides, "One root · five words" (س ل م) (#211).

1080x1920, about 22s. Each slide (1080x1350) sits in the middle of the frame with its own paper background carried up and
down, so TikTok's buttons and caption fall on plain paper. A slow 3% push-in on every slide, a swipe between them, and the
sound the earlier TikTok videos used (brag-quiz, v9-v12): no music, a quiet courtyard fountain with a little birdsong, a
reed-pen stroke on the first frame and a page turn on every swipe. Levelled to about -22 LUFS (ambience alone, so softer
than the -15 the voiced videos use; true peak under -1.5).

  python3 brag-slides/salam-root/build.py        ->  brag-slides/salam-root/out/salam-root.mp4
Needs ffmpeg 5+ and the repo's brag-output-v6 sound files.
"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
SFX = os.path.join(ROOT, "brag-output-v6/composition/assets/sfx-gen")
OUT = os.path.join(HERE, "out"); FRAMES = os.path.join(OUT, "frames")

# how long each slide is on (seconds, from when it starts arriving to when the next starts arriving)
SLIDES = [("01.jpg", 3.4), ("02.jpg", 2.9), ("03.jpg", 2.9), ("04.jpg", 2.9), ("05.jpg", 2.9), ("06.jpg", 2.9), ("07.jpg", 4.0)]
SWIPE = 0.45                      # the swipe between slides
FPS, W, H = 30, 1080, 1920
SLIDE_H = 1350; PAD = (H - SLIDE_H) // 2          # 285 above and below
ZOOM = 0.03
TARGET_LUFS = -22.0
# the slide's own "Swipe to find out →" has nothing to swipe in a video: paint it out with paper from just above it
HIDE_SWIPE = {"01.jpg": (320, 1170, 440, 80, 1070)}   # x, y, w, h, and the y to copy the paper from

def run(*a, **k):
    r = subprocess.run(list(a), capture_output=True, text=True, **k)
    if r.returncode: sys.exit("FAILED: " + " ".join(a)[:300] + "\n" + r.stderr[-1500:])
    return r

def frame(name):
    """slide -> 1080x1920: paper rows copied up and down to fill the frame"""
    src = os.path.join(HERE, "slides", name); dst = os.path.join(FRAMES, name.replace(".jpg", ".png"))
    # the paper above and below: the slide's own top and bottom rows, stretched and softened so there's no streaking
    top = f"crop={W}:8:0:0,scale={W}:{PAD}:flags=bilinear,gblur=sigma=45:steps=3[t]"
    bot = f"crop={W}:8:0:{SLIDE_H - 8},scale={W}:{PAD}:flags=bilinear,gblur=sigma=45:steps=3[u]"
    if name in HIDE_SWIPE:
        x, y, w, h, sy = HIDE_SWIPE[name]
        fc = f"[0:v]format=rgb24,split=4[a0][b][c][pp];[pp]crop={w}:{h}:{x}:{sy}[p];[a0][p]overlay={x}:{y}[a];[b]{top};[c]{bot};[t][a][u]vstack=inputs=3"
    else:
        fc = f"[0:v]format=rgb24,split=3[a][b][c];[b]{top};[c]{bot};[t][a][u]vstack=inputs=3"
    run("ffmpeg", "-y", "-v", "error", "-i", src, "-filter_complex", fc, "-frames:v", "1", dst)
    return dst

def main():
    os.makedirs(FRAMES, exist_ok=True)
    frames = [frame(n) for n, _ in SLIDES]
    starts = []; t = 0.0                                   # when each swipe starts
    for _, d in SLIDES[:-1]: t += d; starts.append(round(t, 3))
    total = round(sum(d for _, d in SLIDES), 3)

    # ---- picture
    ins, parts = [], []
    for i, ((_, d), f) in enumerate(zip(SLIDES, frames)):
        length = d + (SWIPE if i < len(SLIDES) - 1 else 0)      # the end of each slide is under the next swipe
        n = round(length * FPS)
        ins += ["-loop", "1", "-framerate", str(FPS), "-t", f"{length:.3f}", "-i", f]
        parts.append(f"[{i}:v]scale={W*2}:{H*2}:flags=lanczos,zoompan=z='1+{ZOOM}*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                     f":d=1:s={W}x{H}:fps={FPS},setsar=1,format=yuv420p[v{i}]")
    prev = "v0"
    for i in range(1, len(SLIDES)):
        parts.append(f"[{prev}][v{i}]xfade=transition=slideleft:duration={SWIPE}:offset={starts[i-1]}[x{i}]"); prev = f"x{i}"
    video = os.path.join(OUT, "video.mp4")
    run("ffmpeg", "-y", "-v", "error", *ins, "-filter_complex", ";".join(parts), "-map", f"[{prev}]", "-t", f"{total}",
        "-c:v", "libx264", "-crf", "17", "-preset", "slow", "-pix_fmt", "yuv420p", "-r", str(FPS), video)

    # ---- sound: fountain + a little birdsong, a pen stroke at the start, a page turn on every swipe
    cue = lambda n: os.path.join(SFX, n + ".mp3")
    ain = ["-i", cue("fountain"), "-i", cue("birds"), "-i", cue("opener")] + sum((["-i", cue("page-turn")] for _ in starts), [])
    # the fountain's splashes are levelled out first, so the page turns and the pen stroke stand clear of it
    g = [f"[0:a]atrim=0:{total},afade=t=in:d=0.8,afade=t=out:st={total-1.4:.2f}:d=1.4,acompressor=threshold=0.03:ratio=4:attack=20:release=250,volume=3dB[fo]",
         f"[1:a]atrim=0:{total-3.5:.2f},afade=t=in:d=1.5,afade=t=out:st={total-3.5-1.5:.2f}:d=1.5,adelay=2500|2500,volume=-17dB[bi]",
         f"[2:a]volume=11dB,adelay=150|150[op]"]
    mix = ["[fo]", "[bi]", "[op]"]
    for k, s in enumerate(starts):
        ms = int((s - 0.08) * 1000)
        g.append(f"[{3+k}:a]volume=9dB,adelay={ms}|{ms}[pt{k}]"); mix.append(f"[pt{k}]")
    g.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0:duration=longest,atrim=0:{total},aformat=sample_rates=48000:channel_layouts=stereo[mx]")
    raw = os.path.join(OUT, "mix.wav")
    run("ffmpeg", "-y", "-v", "error", *ain, "-filter_complex", ";".join(g), "-map", "[mx]", raw)
    # two passes of loudnorm: measure, then apply linearly
    m = run("ffmpeg", "-hide_banner", "-i", raw, "-af", f"loudnorm=I={TARGET_LUFS}:TP=-1.5:LRA=7:print_format=json", "-f", "null", "-").stderr
    st = json.loads(m[m.rindex("{"):])
    af = (f"loudnorm=I={TARGET_LUFS}:TP=-1.5:LRA=7:measured_I={st['input_i']}:measured_TP={st['input_tp']}:measured_LRA={st['input_lra']}"
          f":measured_thresh={st['input_thresh']}:offset={st['target_offset']}:linear=true")
    final = os.path.join(OUT, "salam-root.mp4")
    run("ffmpeg", "-y", "-v", "error", "-i", video, "-i", raw, "-af", af, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-t", f"{total}", final)
    os.remove(video); os.remove(raw)
    print(f"{final}: {total}s, swipes at {starts}")

if __name__ == "__main__":
    main()
