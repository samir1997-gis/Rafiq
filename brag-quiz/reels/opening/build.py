#!/usr/bin/env python3
"""The opening supplication video (owner, 9 Nov 2026; RAW/Opening Suplication/opening suplication1.mp4, 1:09). Owner: "add captions, not the
fancy ones behind my head, just standard captions; on the first frame, for the first couple of seconds, in very bold, like a warning,
'Don't pray like this', pulsating a little, a small haze around it, yellow; when I'm translating the opening supplication, overlay a screen of
how it looks in the app with the translation; when I talk about learning all the words in your salah in Rafiq, a screen recording of the
salah section and all the words you can learn there."
  - his footage as recorded (no cuts, no grade), brought to 1080 x 1920, the sound levelled to -14.5 LUFS;
  - captions: whole phrases, white with a dark outline, low in the frame, a small pop as each comes in; the transliteration simple;
  - the warning: DON'T PRAY LIKE THIS in Anton, yellow, a soft yellow haze behind it that breathes, the text pulsing, 0-2.8 s;
  - the app (real screens, captured from rafiq-arabic.com with a stand-in learner, as app/store/screenshots.py): the opening supplication
    lesson (Arabic and its translation) while he translates; the Your salah list scrolling, then the word-by-word screen, while he says you
    can learn every step in Rafiq. In a phone frame that slides up, eased.

  python3 build.py WORK SHOTS      (WORK/clip.mp4 his video; SHOTS: lesson-0.png, lesson-2.png, scroll-NNN.png) → WORK/opening.mp4
"""
import glob, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
W, SHOTS = sys.argv[1:3]; FPS = 30; VW, VH = 1080, 1920
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sh = lambda *a: subprocess.run(list(a), check=True)
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", os.path.join(W, "clip.mp4")], capture_output=True, text=True).stdout)
N = int(dur * FPS)

def ttf(name):                                           # the project's woff2 fonts, as TTF for Pillow
    out = os.path.join(W, name + ".ttf")
    if not os.path.exists(out):
        from fontTools.ttLib import TTFont
        f = TTFont(os.path.join(ROOT, "brag-quiz", "fonts", name + ".woff2")); f.flavor = None; f.save(out)
    return out
ANTON, FRED, AMIRI = ttf("anton-latin-400-normal"), ttf("fredoka-latin-700-normal"), ttf("amiri-arabic-700-normal")

CAPS = [  # (from, to, text) in his words; the Arabic in a simple spelling
    (1.3, 2.8, "Don't do this."), (2.85, 5.5, "Allahu akbar."), (5.55, 8.6, "Al-hamdu lillahi rabbil-'alamin."),
    (8.7, 11.4, "Do this instead."), (11.45, 12.75, "Allahu akbar."), (12.8, 18.2, "(quietly) Subhanaka Allahumma wa bihamdik..."),
    (18.3, 21.4, "Al-hamdu lillahi rabbil-'alamin."), (22.1, 24.1, "Did you see the difference?"),
    (24.15, 27.6, "In the second one, I'm reciting the opening supplication,"), (27.65, 31.0, "which is part of the Sunnah of the Prophet ﷺ"),
    (31.05, 32.5, "and it goes like this:"), (32.55, 35.5, "Subhanaka Allahumma wa bihamdika,"), (35.55, 38.4, "wa tabaraka-smuka, wa ta'ala jadduka,"),
    (38.45, 39.95, "wa la ilaha ghayruk."), (40.0, 41.5, "and it means:"), (41.55, 45.1, "Glory be to You, O Allah, and with Your praise."),
    (45.15, 48.45, "Blessed is Your name, exalted is Your majesty,"), (48.5, 51.5, "and there is no god other than You."),
    (51.7, 57.1, "You can learn this du'a and every single step in your salah in Rafiq."),
    (57.2, 60.4, "If you want to start understanding the words you say in your salah,"), (60.45, 62.3, "sign up to rafiq-arabic.com."),
    (62.35, 64.15, "It's free for 7 days,"), (64.2, 68.4, "and after that it costs less than a cup of coffee for the entire month.")]
PHONE = [(40.7, 51.4, "lesson"), (51.5, 57.2, "salah")]          # the app on screen (the slide in starts 0.3 s before)

fr = ImageFont.truetype(FRED, 66); am = ImageFont.truetype(AMIRI, 72)
def runs(text):                                          # the ﷺ in Amiri, the rest in Fredoka
    out, cur = [], ""
    for ch in text:
        if ch == "ﷺ":
            if cur: out.append((cur, fr)); cur = ""
            out.append((ch, am))
        else: cur += ch
    if cur: out.append((cur, fr))
    return out
def wrap(text, maxw=900):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if fr.getlength(t) > maxw and cur: lines.append(cur); cur = w
        else: cur = t
    lines.append(cur); return lines
def caption(text):
    img = Image.new("RGBA", (VW, 400), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    lines = wrap(text); y = 20
    for ln in lines:
        rs = runs(ln); tw = sum(f.getlength(s) for s, f in rs); x = (VW - tw) / 2
        for s, f in rs:
            d.text((x, y + (8 if f is am else 0)), s, font=f, fill="white", stroke_width=7, stroke_fill=(10, 14, 16))
            x += f.getlength(s)
        y += 84
    return img.crop((0, 0, VW, y + 30))
CAPIMG = [caption(t) for _, _, t in CAPS]

an = ImageFont.truetype(ANTON, 168)
def warning(t):
    """DON'T PRAY LIKE THIS: yellow, a dark outline, a haze behind it that breathes, the text pulsing a little"""
    img = Image.new("RGBA", (VW, 620), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    lines = ["DON'T PRAY", "LIKE THIS"]; pulse = float(1 + 0.035 * np.sin(t * 2 * np.pi * 1.6))
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    for i, ln in enumerate(lines):
        x = (VW - an.getlength(ln)) / 2; y = 60 + i * 200
        gd.text((x, y), ln, font=an, fill=(255, 214, 10, int(200 + 40 * np.sin(t * 2 * np.pi * 1.6))))
        d.text((x, y), ln, font=an, fill=(255, 214, 10), stroke_width=9, stroke_fill=(20, 16, 4))
    glow = glow.filter(ImageFilter.GaussianBlur(float(18 + 6 * np.sin(t * 2 * np.pi * 1.6))))
    out = Image.alpha_composite(glow, img)
    w, h = out.size; s = pulse * (1.25 - 0.25 * min(1, t / 0.25) ** 0.5 if t < 0.25 else pulse)   # it lands from a little bigger, then breathes
    return out.resize((int(w * s), int(h * s)), Image.LANCZOS)

def phone(screen, scale=1.0):
    """a phone: dark body, rounded screen, a soft shadow; screen: an app screenshot (1170 x 2532)"""
    sw = int(600 * scale); shh = int(sw * screen.size[1] / screen.size[0]); pad = int(22 * scale); r = int(70 * scale)
    body = Image.new("RGBA", (sw + 2 * pad + 80, shh + 2 * pad + 80), (0, 0, 0, 0))
    sh_ = Image.new("L", body.size, 0); ImageDraw.Draw(sh_).rounded_rectangle([40, 52, 40 + sw + 2 * pad, 52 + shh + 2 * pad], r + pad, fill=150)
    body.putalpha(0); shadow = Image.new("RGBA", body.size, (0, 0, 0, 255)); shadow.putalpha(sh_.filter(ImageFilter.GaussianBlur(24)))
    body = Image.alpha_composite(body, shadow)
    ImageDraw.Draw(body).rounded_rectangle([40, 40, 40 + sw + 2 * pad, 40 + shh + 2 * pad], r + pad, fill=(18, 22, 24, 255))
    scr = screen.convert("RGBA").resize((sw, shh), Image.LANCZOS); m = Image.new("L", (sw, shh), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, sw, shh], r, fill=255)
    body.paste(scr, (40 + pad, 40 + pad), m)
    return body
LESSON = Image.open(os.path.join(SHOTS, "lesson-0.png")).crop((0, 0, 1170, 2000))          # the duʿāʾ and its translation, Word by word cut off
WBW = Image.open(os.path.join(SHOTS, "lesson-2.png")).crop((0, 0, 1170, 2000))
SCROLL = sorted(glob.glob(os.path.join(SHOTS, "scroll-*.png")))
ease = lambda u: 1 - (1 - min(1, max(0, u))) ** 3

os.makedirs(os.path.join(W, "ov"), exist_ok=True)
for n in range(N):
    t = n / FPS; out = os.path.join(W, "ov", f"{n:05d}.png")
    if os.path.exists(out): continue
    frame = Image.new("RGBA", (VW, VH), (0, 0, 0, 0))
    for a, b, kind in PHONE:                               # the app, sliding up (eased out), then down and away (eased in)
        if a - 0.3 <= t < b + 0.3:
            if kind == "lesson": scr = LESSON
            else:
                k = (t - a) / (b - a - 1.6)
                scr = WBW if k >= 1 else Image.open(SCROLL[min(len(SCROLL) - 1, int(k * len(SCROLL)))]).crop((0, 0, 1170, 2000))
            ph = phone(scr, 1.05)
            u = ease((t - (a - 0.3)) / 0.45); v = 1 - (1 - max(0, min(1, (t - b) / 0.3))) ** 3 if t > b else 0
            y = int(170 + (1 - u) * 1500 + v * 1500)
            frame.alpha_composite(ph, ((VW - ph.size[0]) // 2, y))
    for (a, b, _), img in zip(CAPS, CAPIMG):
        if a <= t < b:
            s = 1 + 0.08 * (1 - ease((t - a) / 0.12))
            im = img.resize((int(img.size[0] * s), int(img.size[1] * s)), Image.LANCZOS) if s > 1.001 else img
            frame.alpha_composite(im, ((VW - im.size[0]) // 2, 1500 - (im.size[1] - img.size[1]) // 2))
    if t < 2.8:
        wimg = warning(t); fade = 1 - max(0, (t - 2.5) / 0.3)
        if fade < 1: wimg.putalpha(wimg.getchannel("A").point(lambda v: int(v * fade)))
        frame.alpha_composite(wimg, ((VW - wimg.size[0]) // 2, 300 - (wimg.size[1] - 620) // 2))
    frame.save(out, optimize=False, compress_level=1)

m = subprocess.run(["ffmpeg", "-i", os.path.join(W, "clip.mp4"), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
sh("ffmpeg", "-v", "error", "-y", "-i", os.path.join(W, "clip.mp4"), "-framerate", str(FPS), "-i", os.path.join(W, "ov", "%05d.png"),
   "-filter_complex", f"[0:v]scale={VW}:{VH}:flags=lanczos,fps={FPS},format=yuv420p[b];[b][1:v]overlay=0:0:format=auto,format=yuv420p[v];"
   "[0:a]aresample=192000,loudnorm=I=-14.5:TP=-1.5:LRA=11,aresample=48000[a]",
   "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "19", "-preset", "slow", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
   "-t", f"{dur:.3f}", os.path.join(W, "opening.mp4"))
print("opening.mp4", round(dur, 1), "s")
