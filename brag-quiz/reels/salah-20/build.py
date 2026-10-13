"""The 20-words salah reel, last pass (owner, 12 Oct 2026). On top of the template's reel.mp4: the crash and shake on "the Day of
Judgement begins", a 0 → 50,000 YEARS counter, the hadith card, SALAH slammed on with a crash and an echo that lingers on a held
frame, the 20-words carousel (brag-quiz/stills/sn-*) sliding in, booms on "picture this … you pass away …", then the flicker
hook in front and the whole thing levelled.
  python3 build.py /tmp/reel-salah /tmp/reel-flick1/hook.mp4      → <W>/final.mp4"""
import json, os, re, subprocess, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
HERE = os.path.dirname(os.path.abspath(__file__)); BQ = os.path.join(HERE, "..", "..")
sys.path.insert(0, os.path.join(HERE, "..", "template")); import sfx_rules as SR
W, HOOK = sys.argv[1], sys.argv[2]; FPS, OW, OH = 30, 1080, 1920
sys.path.insert(0, HERE); from timemap import loader; m = loader(W)       # the take's times → after the silence cut
RED, GOLD, PAPER, INK = (180, 50, 42), (233, 185, 73), (241, 236, 224), (23, 38, 43)

CRASH = [19.82, 40.08]                                # loud crash, shake and flash (the take's own times)
BOOMS = [0.44, 2.38, 5.10, 7.56, 9.96, 12.36, 13.86]  # picture THIS · pass away · buried · wake up · Munkar · questioning · barzakh
COUNT = (23.24, 24.44, 26.0)                          # "50" … "years": the counter runs, YEARS slams, it leaves
SALAH = (39.95, 40.08, 41.3)                          # SALAH: appears, lands, leaves (after the held frame)
HOLD_AT, HOLD = 40.65, 1.3                            # the held frame after "salah", while the echo rings
HADITH = (37.7, 39.85)                                # in his pause before "your salah" (the graphic g7 is just before it)
PANELS = [(70.10, 77.05, "sn-7"), (77.05, 83.75, "sn-6")]   # the 56% ring · the top-20 list
# the Day of Judgement motion graphics made for this script (brag-quiz/reels/accountable/out, 10 Oct), cut in full screen over
# his talking shots: (from, to, clip). His face stays on the moments he leans on (picture THIS, 50 thousand years, the first thing, SALAH).
GFX = [(7.40, 12.40, "g1-grave"), (13.40, 16.00, "g2-barzakh"), (20.80, 23.10, "g3-resurrection"), (26.00, 29.60, "g5-sun"),
       (29.60, 32.70, "g6-crowd"), (35.50, 37.70, "g7-first-question"), (66.70, 70.10, "g9-twenty-words")]
CRASH, BOOMS = [m(x) for x in CRASH], [m(x) for x in BOOMS]
COUNT, SALAH, HOLD_AT, HADITH = tuple(m(x) for x in COUNT), tuple(m(x) for x in SALAH), m(HOLD_AT), tuple(m(x) for x in HADITH)
PANELS = [(m(a), m(b), k) for a, b, k in PANELS]; GFX = [(m(a), m(b), k) for a, b, k in GFX]
NH = round(HOLD * FPS)
sh = lambda t: t + HOLD if t > HOLD_AT else t       # take time → time in the reel with the hold inserted

font = lambda n, s: ImageFont.truetype(os.path.join(W, n + ".ttf"), s)
for n in ("anton-latin-400-normal", "instrument-serif-latin-400-normal"):
    if not os.path.exists(os.path.join(W, n + ".ttf")):
        from fontTools.ttLib import TTFont
        f = TTFont(os.path.join(BQ, "fonts", n + ".woff2")); f.flavor = None; f.save(os.path.join(W, n + ".ttf"))
ANTON, SERIF = (lambda s: font("anton-latin-400-normal", s)), (lambda s: font("instrument-serif-latin-400-normal", s))

def text(s, f, fill, stroke=0, sc=None):
    b = f.getbbox(s, stroke_width=stroke); im = Image.new("RGBA", (b[2] - b[0] + 40, b[3] - b[1] + 40), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((20 - b[0], 20 - b[1]), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=sc); return im
def shadowed(im, r=12, a=170):
    s = Image.new("RGBA", im.size, (0, 0, 0, 0)); s.putalpha(im.getchannel("A").point(lambda v: v * a // 255))
    o = Image.new("RGBA", im.size, (0, 0, 0, 0)); o.alpha_composite(s.filter(ImageFilter.GaussianBlur(r)), (0, 6)); o.alpha_composite(im); return o
def paste_c(base, im, cx, cy, scale=1.0, alpha=1.0, rot=0):
    if scale != 1.0: im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.BICUBIC)
    if rot: im = im.rotate(rot, Image.BICUBIC, expand=True)
    if alpha < 1: im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * alpha)))
    base.alpha_composite(im, (round(cx - im.width / 2), round(cy - im.height / 2)))
eo = lambda x: 1 - (1 - min(1, max(0, x))) ** 3
SHAKE = [(-34, 22), (30, -18), (-22, 14), (16, -10), (-8, 6), (0, 0)]

salah_im = shadowed(text("SALAH", ANTON(330), RED, 8, (255, 255, 255)), 14)
years_im = shadowed(text("YEARS", ANTON(230), RED, 7, (255, 255, 255)), 14)
pan = {k: Image.open(os.path.join(BQ, "stills", k + ".png")).convert("RGB") for _, _, k in PANELS}
card = Image.new("RGBA", (960, 400), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
d.rounded_rectangle((0, 0, 959, 399), 34, fill=INK + (225,))
q = "“The first thing a servant will be brought to account for on the Day of Resurrection is the prayer.”"
y, line, words = 40, "", q.split()
for w_ in words:                                          # wrap to the card
    if SERIF(56).getlength(line + " " + w_) > 860 and line: d.text((50, y), line, font=SERIF(56), fill=PAPER); y += 66; line = w_
    else: line = (line + " " + w_).strip()
d.text((50, y), line, font=SERIF(56), fill=PAPER); d.text((50, y + 90), "TIRMIDHI 413 · NASĀʾĪ 465".replace("Ā", "A").replace("ʾ", "'").replace("Ī", "I"), font=ANTON(40), fill=GOLD)
card = card.crop((0, 0, 960, min(400, y + 160)))

def overlay(fr, t, held=0.0):
    """Everything drawn on one frame at take time t (held: seconds into the held frame)."""
    for c in CRASH:                                       # white flash on the crash
        if 0 <= t - c < .3 and not held: fr.alpha_composite(Image.new("RGBA", fr.size, (255, 248, 230, round(200 * (1 - (t - c) / .3)))))
    a, b, e = COUNT                                       # 0 → 50,000, then YEARS slams in
    if a - .05 <= t < e:
        v = 50000 * min(1, max(0, (t - a) / (b - a)) ** 1.6); out = 1 - eo((t - (e - .3)) / .3)
        paste_c(fr, shadowed(text(f"{int(v):,}", ANTON(300), GOLD)), OW / 2, 1300, 1 + .06 * np.exp(-max(0, t - b) * 10), out)
        if t >= b - .12:
            ds = t - b; sc = 1 + 1.2 * (-ds / .12) ** 2 if ds < 0 else 1 + .1 * np.exp(-ds * 16) * np.cos(ds * 40)
            paste_c(fr, years_im, OW / 2, 1560, sc, out)
    a, e = HADITH                                         # the hadith card slides up from the bottom
    if a <= t < e:
        k = eo((t - a) / .35); out = 1 - eo((t - (e - .3)) / .3); cd = card.copy(); cd.putalpha(cd.getchannel("A").point(lambda v: int(v * k * out)))
        fr.alpha_composite(cd, (60, round(1440 + (1 - k) * 140)))
    a, l, e = SALAH                                       # SALAH: huge, slams down on the word, rings, stays through the hold
    if a <= t < e or held:
        ds = (t - l) if not held else 1
        sc = 1 + 1.2 * (-ds / .13) ** 2 if ds < 0 else 1 + .12 * np.exp(-ds * 18) * np.cos(ds * 40)
        if held: sc = 1 + .05 * held / HOLD
        out = 1 - eo((t - (e - .25)) / .25) if not held else 1
        if 0 <= ds < .55 and not held:
            ov = Image.new("RGBA", fr.size, (0, 0, 0, 0)); dd = ImageDraw.Draw(ov); qq = ds / .55
            for k, (col, wd) in enumerate([(GOLD, 14), (RED, 8)]):
                r = 60 + 620 * (1 - (1 - max(0, qq - k * .12)) ** 3); dd.ellipse((540 - r, 1250 - r, 540 + r, 1250 + r), outline=col + (round(230 * (1 - qq)),), width=wd)
            for k in range(10):
                g = k * np.pi / 5; r0, r1 = 200 + 300 * qq, 260 + 420 * qq
                dd.line((540 + r0 * np.cos(g), 1250 + r0 * np.sin(g), 540 + r1 * np.cos(g), 1250 + r1 * np.sin(g)), fill=GOLD + (round(255 * (1 - qq)),), width=12)
            fr.alpha_composite(ov)
        paste_c(fr, salah_im, OW / 2, 1250, sc, out, -7 * max(0, -ds / .13) if ds < 0 else 0)
    for p0, p1, k in PANELS:                              # the carousel: each graphic slides in from the right, out to the left
        if p0 <= t < p1:
            im = pan[k]; bg = Image.new("RGBA", (OW, OH), im.getpixel((4, 4)) + (255,)); bg.paste(im, (0, (OH - im.height) // 2))
            first, last = p0 == PANELS[0][0], p1 == PANELS[-1][1]; k_ = eo((t - p0) / .3)
            if not first:                                 # between graphics: the next one pushes the last one out
                prev = [p for p in PANELS if p[1] == p0][0][2]
                pb = Image.new("RGBA", (OW, OH), pan[prev].getpixel((4, 4)) + (255,)); pb.paste(pan[prev], (0, (OH - pan[prev].height) // 2))
                fr.alpha_composite(pb, (round(-k_ * OW), 0))
            x = (1 - k_) * OW
            if last: x -= eo((t - (p1 - .25)) / .25) * OW
            fr.alpha_composite(bg, (round(x), 0))
    return fr

def shake(fr, t):
    for c in CRASH:
        ds = t - c
        if 0 <= ds < .25:
            dx, dy = SHAKE[min(5, int(ds / .04))]
            z = fr.resize((round(OW * 1.04), round(OH * 1.04)), Image.BICUBIC)
            return z.crop((round(OW * .02 - dx), round(OH * .02 - dy), round(OW * .02 - dx) + OW, round(OH * .02 - dy) + OH))
    return fr

LOOK = open(os.path.join(HERE, "look.txt")).read().strip()      # darker, dark edges easing off towards him (owner, 13 Oct)
GDIR = os.path.join(BQ, "reels", "accountable", "out"); gdec = {}
def gfx_frame(t):
    """The graphic on screen at take time t, if any (decoded as it plays)."""
    for g0, g1, gid in GFX:
        if g0 <= t < g1:
            if gid not in gdec: gdec[gid] = subprocess.Popen(["ffmpeg", "-v", "error", "-i", os.path.join(GDIR, gid + ".mp4"), "-vf", f"scale={OW}:{OH},fps={FPS}",
                                                              "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
            raw = gdec[gid].stdout.read(OW * OH * 3)
            if len(raw) == OW * OH * 3: gdec[gid].last = raw
            return Image.frombytes("RGB", (OW, OH), getattr(gdec[gid], "last", raw)).convert("RGBA")
    return None

# 1. the picture
N = int(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", os.path.join(W, "reel.mp4")], capture_output=True, text=True).stdout) * FPS)
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", os.path.join(W, "reel.mp4"), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{OW}x{OH}", "-r", str(FPS), "-i", "-",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", os.path.join(W, "body-v.mp4")], stdin=subprocess.PIPE)
for i in range(N):
    raw = dec.stdout.read(OW * OH * 3)
    if len(raw) < OW * OH * 3: break
    t = i / FPS; fr = gfx_frame(t) or Image.frombytes("RGB", (OW, OH), raw).convert("RGBA")
    if any(a - .2 <= t < c for a, _, c in [COUNT, SALAH]) or any(a <= t < b for a, b in [HADITH] + [(p[0], p[1]) for p in PANELS]) or any(0 <= t - c < .3 for c in CRASH):
        fr = overlay(fr, t)
    enc.stdin.write(shake(fr, t).convert("RGB").tobytes())
    if i == round(HOLD_AT * FPS):                         # the held frame: a slow push in, colour draining a little, SALAH stays
        base = Image.frombytes("RGB", (OW, OH), raw)
        for k in range(NH):
            p = k / NH; z = 1 + .05 * p; im = base.resize((round(OW * z), round(OH * z)), Image.BICUBIC)
            im = im.crop(((im.width - OW) // 2, round((im.height - OH) * .4), (im.width - OW) // 2 + OW, round((im.height - OH) * .4) + OH))
            im = ImageEnhance.Color(im).enhance(1 - .45 * p).convert("RGBA")
            enc.stdin.write(overlay(im, t, held=k / FPS + 1e-3).convert("RGB").tobytes())
enc.stdin.close(); enc.wait(); dec.stdout.close(); dec.wait()

# 2. the sound: the reel's own mix with the hold inserted, then the crashes, the booms, the counter's clicks, the echo
def lv(name): f = os.path.join(BQ, "sfx", name + ".wav") if name in ("crash", "boom") else SR.F(name); return f, SR.info(f)
S = [("crash", "boom", c, 11) for c in CRASH] + [("boom", "boom", b, 9) for b in BOOMS]     # loud: the owner asked for them to hit
a, b, _ = COUNT; ticks = [a + (b - a) * (k / 14) ** (1 / 1.6) for k in range(14)]      # the counter clicks faster as it races
S += [("click", "tap", x, 2) for x in ticks] + [("boom", "boom", b, 9)]
S += [("swoosh", "swoosh", HADITH[0] + .05, -2)] + [("short-swoosh" if k % 2 else "swoosh", "swoosh", p0 + .05, 0) for k, (p0, _, _) in enumerate(PANELS)]
S += [("swoosh", "swoosh", PANELS[-1][1] - .15, 0)]
S += [("shutter", "hit", g0, -2) for g0, _, _ in GFX] + [("shutter", "hit", g1, -4) for _, g1, _ in GFX if g1 not in [g[0] for g in GFX] + [p[0] for p in PANELS]]
cmd = ["ffmpeg", "-v", "error", "-y", "-i", os.path.join(W, "reel.mp4"), "-i", os.path.join(W, "voice_clean.wav")]
fl = [f"[0:a]atrim=0:{HOLD_AT},asetpts=PTS-STARTPTS[a0]", f"[0:a]atrim={HOLD_AT},asetpts=PTS-STARTPTS[a1]",
      f"anullsrc=r=48000:cl=stereo,atrim=0:{HOLD}[gap]", "[a0][gap][a1]concat=n=3:v=0:a=1,aformat=sample_rates=48000:channel_layouts=stereo[mix]",
      # the echo: "salah" from the clean voice, repeated and fading, no dry copy (the reel already has the word)
      f"[1:a]atrim={SALAH[1] - .05}:{SALAH[1] + .62},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo,asplit=4[e1][e2][e3][e4]"]
for k, (dl, g) in enumerate([(330, .55), (660, .38), (990, .25), (1320, .15)]):
    ms = int((SALAH[1] - .05) * 1000) + dl
    fl.append(f"[e{k + 1}]lowpass=f={5000 - 900 * k},volume={g * 1.6},adelay={ms}|{ms}[ec{k}]")
for k, (name, kind, t, boost) in enumerate(S):
    f, (pk, pat) = lv(name); cmd += ["-i", f]; ms = int(max(0, sh(t) - pat) * 1000)
    fl.append(f"[{k + 2}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={SR.LEVEL[kind] + boost - pk:.1f}dB,adelay={ms}|{ms}[s{k}]")
fl.append("[mix]" + "".join(f"[ec{k}]" for k in range(4)) + "".join(f"[s{k}]" for k in range(len(S)))
          + f"amix=inputs={len(S) + 5}:normalize=0:duration=first,alimiter=limit=0.7:level=disabled[a]")
subprocess.run(cmd + ["-filter_complex", ";".join(fl), "-map", "[a]", "-c:a", "pcm_s16le", os.path.join(W, "body-a.wav")], check=True)

# 3. the hook in front, everything levelled: -14.5 LUFS, true peak under -1 dB after AAC
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", HOOK, "-i", os.path.join(W, "body-v.mp4"), "-i", os.path.join(W, "body-a.wav"), "-filter_complex",
                f"[0:v]fps=30,{LOOK},format=yuv420p,setsar=1[hv];"
                "[1:v]fps=30,format=yuv420p,setsar=1[bv];[0:a]aformat=sample_rates=48000:channel_layouts=stereo[ha];"
                "[2:a]aformat=sample_rates=48000:channel_layouts=stereo[ba];[hv][ha][bv][ba]concat=n=2:v=1:a=1[v][a]",
                "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-c:a", "pcm_s16le", os.path.join(W, "joined.mov")], check=True)
m = subprocess.run(["ffmpeg", "-hide_banner", "-i", os.path.join(W, "joined.mov"), "-af", "loudnorm=I=-14.5:TP=-2.5:LRA=11:print_format=json", "-f", "null", "-"],
                   capture_output=True, text=True).stderr; J = json.loads(re.search(r"\{[^{}]*\}", m).group())
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(W, "joined.mov"), "-c:v", "libx264", "-crf", "20", "-preset", "slow", "-maxrate", "6M", "-bufsize", "12M",
                "-pix_fmt", "yuv420p", "-af", f"loudnorm=I=-14.5:TP=-2.5:LRA=11:measured_I={J['input_i']}:measured_TP={J['input_tp']}:measured_LRA={J['input_lra']}:"
                f"measured_thresh={J['input_thresh']}:offset={J['target_offset']}:linear=true,aresample=192000,"     # limit at 4x: the template's sharp taps
                "alimiter=limit=0.75:level=disabled:attack=0.5:release=50,aresample=48000", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
                os.path.join(W, "final.mp4")], check=True)
print("final.mp4")
