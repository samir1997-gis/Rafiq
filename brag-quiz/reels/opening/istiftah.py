#!/usr/bin/env python3
"""Duʿāʾ al-istiftāḥ (owner, 9 Nov 2026; RAW/Opening Suplication/duaalistiftah.mp4, 28.7 s): "edit it similar to the last one; at the point
where I zoom into my monitor, overlay a phone screen, full screen, so you don't see any of the original screen anymore: Rafiq going through
the steps, subḥānaka… and then the word for word bit… with audio".
  - his part: as recorded, brought to 1080 x 1920, the same standard captions as build.py;
  - from his zoom into the monitor (26.4 s): the app full screen, a real recording of rafiq-arabic.com (stand-in learner, recorded in real
    time at the video's own size, 390 x 693 at 2.77): the opening supplication lesson, Listen, the duʿāʾ played with the app's own recording
    (audio/1fauxi5.mp3, at the app's speed, 0.95), then Word by word scrolled through all ten words; it comes in growing out of his zoom;
  - his sound fades as the app comes in; levelled to -14.5 LUFS.

  python3 istiftah.py WORK REC      (WORK/clip.mp4 his video; REC/log.json + frames from the app recording) → WORK/istiftah.mp4
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
W, REC = sys.argv[1:3]; FPS = 30; VW, VH = 1080, 1920; CUT = 26.4
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sh = lambda *a: subprocess.run(list(a), check=True)
def ttf(name):
    out = os.path.join(W, name + ".ttf")
    if not os.path.exists(out):
        from fontTools.ttLib import TTFont
        f = TTFont(os.path.join(ROOT, "brag-quiz", "fonts", name + ".woff2")); f.flavor = None; f.save(out)
    return out
fr = ImageFont.truetype(ttf("fredoka-latin-700-normal"), 66)
CAPS = [(0.0, 1.9, "Have you ever seen the imam do this before?"), (12.0, 14.4, "I always used to wonder what the imam was reciting"),
        (14.45, 16.5, "between Allahu akbar and the Fatiha,"), (16.55, 18.85, "and then I realised it's actually part of the Sunnah:"),
        (18.9, 20.85, "it's Du'a al-Istiftah,"), (20.9, 22.2, "the opening supplication,"), (22.25, 24.35, "and it's actually really easy to learn."),
        (24.4, 25.6, "Have a look.")]
def wrap(text, maxw=900):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if fr.getlength(t) > maxw and cur: lines.append(cur); cur = w
        else: cur = t
    return lines + [cur]
def caption(text):
    lines = wrap(text); img = Image.new("RGBA", (VW, 30 + 84 * len(lines) + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    for i, ln in enumerate(lines): d.text(((VW - fr.getlength(ln)) / 2, 20 + 84 * i), ln, font=fr, fill="white", stroke_width=7, stroke_fill=(10, 14, 16))
    return img
os.makedirs(os.path.join(W, "caps"), exist_ok=True); filt, ins = [], []
for i, (a, b, t) in enumerate(CAPS):
    f = os.path.join(W, "caps", f"c{i}.png"); caption(t).save(f); ins += ["-i", f]
    filt.append((a, b))

# the app: its frames, each held until the next one was taken (real time), then the last held a moment
L = json.load(open(os.path.join(REC, "log.json"))); app_len = L[-1][0] - L[0][0] + 1.2
lst = os.path.join(W, "app.txt")
with open(lst, "w") as fh:
    for (t, f, _), nxt in zip(L, L[1:] + [[L[-1][0] + 1.2]]): fh.write(f"file '{f}'\nduration {max(0.034, nxt[0] - t):.3f}\n")
    fh.write(f"file '{L[-1][1]}'\n")
sh("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-vf", f"fps={FPS},scale={VW}:{VH}:flags=lanczos,format=yuv420p",
   "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-t", f"{app_len:.3f}", os.path.join(W, "app.mp4"))
click = L[1][0] - L[0][0]                                   # Listen was pressed just before the first "playing" frame
total = CUT + app_len

# his part with its captions, then the app growing out of his zoom (0.4 s, eased out), the duʿāʾ's own audio under it
WORDS = ["9xm1rg", "bdqx1r", "1ab0u9p", "1q11ui", "zzjc1w", "1oziv6c", "7wrpdn", "y9vpsw", "cnwmz1", "vuziqi"]   # the ten words, the app's recordings
wbw = next(t for t, f, tag in L if tag == "wbw") - L[0][0]       # each word said as the list scrolls past it (owner: "with audio")
wins = sum((["-i", os.path.join(ROOT, "audio", w + ".mp3")] for w in WORDS), [])
cap_ov = "".join(f"[v{i}][{i + 2}:v]overlay=0:1500:enable='between(t,{a},{b})'[v{i + 1}];" for i, (a, b) in enumerate(filt))
fc = (f"[0:v]scale={VW}:{VH}:flags=lanczos,fps={FPS},format=yuv420p,trim=0:{CUT},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration={app_len:.3f}[v0];"
      + cap_ov +
      f"[1:v]setpts=PTS-STARTPTS+{CUT}/TB,scale=w='{VW}*(0.7+0.3*min(1,(t-{CUT})/0.4)*(2-min(1,(t-{CUT})/0.4)))':h=-2:eval=frame[app];"
      f"[v{len(filt)}][app]overlay=x='(W-w)/2':y='(H-h)/2':enable='gte(t,{CUT})':eval=frame,format=yuv420p[v];"
      f"[0:a]atrim=0:{CUT + 0.4},afade=t=out:st={CUT - 0.1}:d=0.5,apad=whole_dur={total:.3f}[his];"
      f"[{len(filt) + 2}:a]atempo=0.95,adelay={int((CUT + click) * 1000)}|{int((CUT + click) * 1000)},apad=whole_dur={total:.3f}[dua];"
      + "".join(f"[{len(filt) + 3 + i}:a]adelay={int((CUT + wbw + 0.3 + i * 0.95) * 1000)}|{int((CUT + wbw + 0.3 + i * 0.95) * 1000)},apad=whole_dur={total:.3f}[w{i}];" for i in range(len(WORDS))) +
      f"[his][dua]" + "".join(f"[w{i}]" for i in range(len(WORDS))) + f"amix=inputs={2 + len(WORDS)}:normalize=0:duration=longest,aresample=192000,loudnorm=I=-14.5:TP=-1.5:LRA=11,aresample=48000[a]")
sh("ffmpeg", "-v", "error", "-y", "-i", os.path.join(W, "clip.mp4"), "-i", os.path.join(W, "app.mp4"), *ins, "-i", os.path.join(ROOT, "audio", "1fauxi5.mp3"), *wins,
   "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", f"{total:.3f}", "-c:v", "libx264", "-crf", "19", "-preset", "slow",
   "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", os.path.join(W, "istiftah.mp4"))
print("istiftah.mp4", round(total, 1), "s")
