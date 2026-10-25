#!/usr/bin/env python3
"""The departure board (owner, 25 Oct 2026, #293: "something new that doesn't feel like AI", clear of what got m2-barik restricted, #289).
No voice at all and no reused audio: every sound is made here (station hall, split-flap clatter, chimes, the clock, a ticket punch).
The whole video is a split-flap departure board at night with a paper ticket in front of it. The root ذ ك ر, the unmade idea in IDEAS.md:
- hook: dhikr is hiding inside تَذْكِرَة, "ticket";
- the same three letters mean "to remember", and tadhkira literally means "a reminder";
- your turn: ذاكِرَة (memory, prayer mat or station?), 3-2-1 flipping on the board;
- فَاذْكُرُونِي أَذْكُرْكُمْ (al-Baqarah 2:152);
- ask: what dhikr do you say most?

  python3 brag-quiz/reels/board/build.py
  cd brag-quiz/reels/board/out/v && npx -y hyperframes@0.8.153 render --crf 10 -o ../board-raw.mp4
"""
import json, math, os, random, re, shutil, subprocess, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
V6 = os.path.join(ROOT, "brag-output-v6/composition/assets"); SFX = os.path.join(ROOT, "brag-quiz/sfx")
INK, CREAM, GOLD, GOLD2, RED, TEAL = "#17262b", "#f1ece0", "#a8842c", "#E9B949", "#B4322A", "#2e7263"
END, SR = 27.8, 48000
rnd = random.Random(7)

# ---- the board: 4 message lines of 13 tiles, then 3 departure rows (a platform tile and one wide flap each)
COLS, TW, TH, TG, RG = 13, 60, 92, 6, 12
GX = (1080 - (COLS * TW + (COLS - 1) * TG)) // 2                  # 114
GY = 352
ROW_Y, ROW_H, PLAT_W = [804, 940, 1076], 122, 76
FD_T, FD_R = 0.05, 0.085                                         # one flap falling: a tile, a row
LAT, ARL = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
CITIES = [("MAKKAH", "مَكَّة"), ("MADINAH", "المَدِينَة"), ("JEDDAH", "جُدَّة"), ("CAIRO", "القاهِرَة"), ("DUBAI", "دُبَي"), ("LONDON", "لَنْدَن"),
          ("AMMAN", "عَمّان"), ("ISTANBUL", "إِسْطَنْبُول"), ("DOHA", "الدَّوْحَة"), ("RIYADH", "الرِّياض")]

def tile(ch, cls=""):
    if ch == " ": return ""
    return f'<span class="{cls}{" a" if ch in ARL else ""}">{ch}</span>'

def line(s):
    """'WHY IS {DHIKR}' → 13 tile htmls: {gold} [red]; Arabic letters get the Arabic font."""
    out, cls = [], ""
    for ch in s:
        if ch in "{[": cls = "g" if ch == "{" else "rd"; continue
        if ch in "}]": cls = ""; continue
        out.append(tile(ch, cls))
    return (out + [""] * COLS)[:COLS]

def row(en="", tr="", ar=""):
    if not (en or ar): return ""
    return f'<div class="rc"><div class="en"><b>{en}</b><i>{tr}</i></div><div class="ar">{ar}</div></div>'

def verse(ar): return f'<div class="rc v"><div class="ar">{ar}</div></div>'
def plat(d): return f'<span class="g">{d}</span>' if d else ""
rt = lambda s: f'<span class="rt">{s}</span>'                     # root letters: gold on the board

TADHKIRA = "تَ" + rt("ذْكِرَ") + "ة"
DHIKR = rt("ذِكْر")
DHAKIRA = rt("ذ") + "ا" + rt("كِرَ") + "ة"

EL = {}                                                          # id → {"init", "fd", "ev": [(t, html)], "x", "kind"}
SND = []                                                         # (t, kind, pan) for each flap that lands
def el(eid, init, fd, x, kind): EL[eid] = {"init": init, "fd": fd, "ev": [], "x": x, "kind": kind}
def cur(eid): e = EL[eid]; return e["ev"][-1][1] if e["ev"] else e["init"]
def flip(eid, t0, new, k, pool):
    e = EL[eid]
    if cur(eid) == new: return t0
    steps = [pool() for _ in range(k)] + [new]
    for i, h in enumerate(steps):
        t = round(t0 + i * e["fd"], 3); e["ev"].append((t, h)); SND.append((t + e["fd"] * 0.85, e["kind"], (e["x"] - 540) / 540))
    return t0 + len(steps) * e["fd"]
lat = lambda: tile(rnd.choice(LAT))
ara = lambda: tile(rnd.choice(ARL))
city = lambda: row(*(lambda c: (c[0], "", c[1]))(rnd.choice(CITIES)))
digit = lambda: plat(str(rnd.randint(0, 9)))

A = ["WHY IS {DHIKR}", "HIDING IN THE", "ARABIC WORD", "FOR [TICKET]?"]
for r in range(4):
    for c, h in enumerate(line(A[r])): el(f"t{r}_{c}", "" if (r, c) == (3, 10) else h, FD_T, GX + c * (TW + TG) + TW / 2, "tile")
for i in range(3):
    el(f"p{i}", plat("1") if i == 0 else "", FD_R, GX + PLAT_W / 2, "plat")
    el(f"r{i}", row("TICKET", "tadhkira", TADHKIRA) if i == 0 else "", FD_R, 600, "row")

def msg(lines, t0, k=(2, 5)):
    """Every tile that changes flips, in a wave from the top left; the board's own clatter."""
    end = t0
    for r in range(4):
        for c, h in enumerate(line(lines[r]) if isinstance(lines[r], str) else lines[r]):
            d = t0 + 0.022 * c + 0.05 * r + rnd.uniform(0, 0.04)
            end = max(end, flip(f"t{r}_{c}", d, h, rnd.randint(*k), ara if "a\"" in h else lat))
    return end

ROOT3 = [""] * 4 + [tile("ر", "g"), "", tile("ك", "g"), "", tile("ذ", "g")] + [""] * 4   # left to right, so it reads ذ ك ر from the right
T_Q, T_LIT = 0.2, 1.0
T_B, T_C, T_PUNCH, T_D, T_E, T_F1, T_F2 = 3.5, 7.3, 8.4, 10.9, 16.3, 19.4, 22.9
COUNT = [13.3, 14.3, 15.3]
flip("t3_10", T_Q, tile("?"), 5, lat)
msg(["SAME LETTERS:", ROOT3, "TO REMEMBER", ""], T_B)
flip("p1", T_B + 0.25, plat("2"), 3, digit); flip("r1", T_B + 0.3, row("REMEMBRANCE", "dhikr", DHIKR), 4, city)
msg(["TADHKIRA", "LITERALLY", "MEANS:", "A {REMINDER}"], T_C)
msg(["YOUR TURN:", "A  MEMORY", "B  PRAYER MAT", "C  STATION"], T_D)
flip("p2", T_D + 0.25, plat("3"), 3, digit); flip("r2", T_D + 0.3, row("???", "dhākira", DHAKIRA), 4, city)
for n, t in zip("321", COUNT): flip("t0_11", t - FD_T * 2, tile(n, "rd"), 1, lambda: tile(str(rnd.randint(4, 9))))
msg(["ANSWER:", "{A  MEMORY}", "", ""], T_E, k=(1, 3))
flip("r2", T_E + 0.1, row("MEMORY", "dhākira", DHAKIRA), 3, lambda: row(rnd.choice(["PRAYER MAT", "STATION"]), "dhākira", DHAKIRA))
REVEAL = EL["r2"]["ev"][-1][0] + FD_R
msg(["REMEMBER ME,", "AND I WILL", "REMEMBER YOU", ""], T_F1)
for i, h in enumerate([verse("فَا" + rt("ذْكُرُ") + "ونِي"), verse("أَ" + rt("ذْكُرْ") + "كُمْ"), row("AL-BAQARAH 2:152")]):
    flip(f"p{i}", T_F1 + 0.15 + 0.12 * i, "", 2, digit); flip(f"r{i}", T_F1 + 0.2 + 0.12 * i, h, 4, city)
msg(["WHAT {DHIKR} DO", "YOU SAY", "THE MOST?", "COMMENT IT"], T_F2)
INFO = [(REVEAL + 0.25, T_F1 - 0.1, "📱 your phone's memory is ذاكِرَة too"), (T_F2 + 0.9, END + 1, "send this to the friend who always reminds you 🤍")]
CHIMES = [(0.0, (392, 523.25, 659.25)), (REVEAL + 0.1, (659.25, 523.25))]

# ---- sound: all made here (numpy), mixed into one track
N = int((END + 1) * SR); rng = np.random.default_rng(7)
def bandpass(x, lo=None, hi=None, n=2):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); f[0] = 1e-3; H = np.ones_like(f)
    if lo: H /= np.sqrt(1 + (lo / f) ** (2 * n))
    if hi: H /= np.sqrt(1 + (f / hi) ** (2 * n))
    return np.fft.irfft(X * H, len(x))
def rms_to(x, r): return x * (r / (np.sqrt(np.mean(x ** 2)) + 1e-12))
def load(path):
    w = wave.open(path); a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
    if w.getnchannels() == 2: a = a.reshape(-1, 2).mean(axis=1)
    return a
DRY, WET = np.zeros((2, N)), np.zeros(N)
def put(sig, t, gain=1.0, pan=0.0, wet=0.25):
    i = int(t * SR); j = min(N, i + len(sig))
    if j <= i or i < 0: return
    s = sig[:j - i] * gain; a = (max(-1, min(1, pan)) + 1) * math.pi / 4
    DRY[0, i:j] += s * math.cos(a); DRY[1, i:j] += s * math.sin(a); WET[i:j] += s * wet

def flap_sound(pitch, big):
    n = int(0.05 * SR); t = np.arange(n) / SR
    nb = bandpass(rng.standard_normal(n) * np.exp(-t / 0.0022), 1400 * pitch, 7000 * pitch)
    body = np.sin(2 * np.pi * (520 if big else 840) * pitch * t) * np.exp(-t / (0.014 if big else 0.009)) * (0.5 if big else 0.3)
    k = int(0.008 * SR); s2 = np.zeros(n); s2[k:] = nb[:n - k] * 0.3
    out = nb / (np.abs(nb).max() + 1e-9) + body + s2
    return out / np.abs(out).max()
FLAPS = {False: [flap_sound(rng.uniform(.9, 1.12), False) for _ in range(14)], True: [flap_sound(rng.uniform(.9, 1.1), True) for _ in range(8)]}
for t, kind, pan in SND:
    big = kind != "tile"
    put(FLAPS[big][rng.integers(len(FLAPS[big]))], t + rng.uniform(-0.004, 0.004), (0.55 if big else 0.32) * rng.uniform(.7, 1), pan * 0.7, 0.3)

def bell(f, d=2.4):
    t = np.arange(int(d * SR)) / SR
    s = sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t / dd) for m, a, dd in ((1, 1, 1.5), (2.0, .45, .8), (2.76, .3, .5), (5.4, .12, .25), (.5, .2, 2.0)))
    return s * np.minimum(1, t / 0.003)
for t0, notes in CHIMES:
    for i, f in enumerate(notes): put(bell(f), t0 + i * 0.36, 0.12, 0.0, 0.6)

n = int(0.25 * SR); t = np.arange(n) / SR                                                     # the ticket punch: a click, a ring, paper
punch = (bandpass(rng.standard_normal(n) * np.exp(-t / 0.004), 2000, 9000) * 1.2 + (np.sin(2 * np.pi * 2870 * t) + .6 * np.sin(2 * np.pi * 4630 * t)) * np.exp(-t / 0.05) * .25
         + np.sin(2 * np.pi * 170 * t) * np.exp(-t / 0.025) * .6)
rustle = np.zeros(n); k = int(0.015 * SR); rustle[k:] = bandpass(rng.standard_normal(n - k), 3000, 11000) * np.exp(-t[:n - k] / 0.03) * .5
put(punch + rustle, T_PUNCH, 0.7, 0.1, 0.35)

TICK, CLICK, SHIM, THUMP = (load(os.path.join(SFX, p)) for p in ("soft/tick.wav", "ref/click.wav", "soft/shimmer.wav", "soft/thump.wav"))
for s in range(int(END)):                                                                     # the station clock, every second
    put(TICK, s + 0.3, 0.5 if round(s + 0.3, 2) in COUNT else 0.09, 0.55, 0.2)
for t0 in COUNT: put(CLICK, t0, 0.55, 0.0, 0.2)
put(SHIM, T_LIT, 0.22, 0.0, 0.2); put(THUMP, T_LIT, 0.35, 0.0, 0.1); put(SHIM, REVEAL, 0.25, 0.0, 0.2)

walk = np.cumsum(rng.standard_normal(N)); walk -= np.linspace(walk[0], walk[-1], N)
hall = rms_to(bandpass(walk, 25, 170), 0.045)                    # the station: a low room rumble,
env = np.interp(np.arange(N), np.arange(0, N, SR // 4), 0.55 + 0.45 * rng.random(len(range(0, N, SR // 4))))
murmur = rms_to(bandpass(rng.standard_normal(N), 280, 1400) * bandpass(env, None, 1.5), 0.02)  # a distant crowd
ir_t = np.arange(int(1.9 * SR)) / SR                                                          # a big hall reverb for everything else
ir = bandpass(rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 6.9 / 1.9), 120, 4500); ir /= np.sqrt(np.sum(ir ** 2))
m = 1 << int(math.ceil(math.log2(N + len(ir))))
wet = np.fft.irfft(np.fft.rfft(WET, m) * np.fft.rfft(ir, m), m)[:N] * 0.5
fade = np.minimum(1, np.arange(N) / (0.02 * SR)) * np.clip((END - np.arange(N) / SR) / 0.6, 0, 1)
mix = (DRY + wet + hall + murmur * np.array([[1.0], [0.85]])) * fade
mix = np.tanh(mix / (np.abs(mix).max() * 0.8)) * 0.89                                           # gentle limit, peaks under -1 dBFS

def build():
    out = os.path.join(HERE, "out", "v"); a = os.path.join(out, "assets")
    if os.path.exists(out): shutil.rmtree(out)
    os.makedirs(a)
    for f in ("ibm-plex-sans-arabic-arabic-700-normal.woff2", "karla-latin-500-normal.woff2", "karla-latin-700-normal.woff2"): shutil.copy(os.path.join(V6, "fonts", f), a)
    shutil.copy(os.path.join(ROOT, "brag-quiz/fonts/anton-latin-400-normal.woff2"), a); shutil.copy(os.path.join(V6, "lib/gsap.min.js"), a)
    w = wave.open(os.path.join(a, "sound.wav"), "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix.T * 32767).astype(np.int16).tobytes()); w.close()
    from PIL import Image                                                                     # film grain, four frames cycled
    for i in range(4):
        g = np.random.default_rng(100 + i).normal(128, 40, (960, 540)).clip(0, 255).astype(np.uint8)
        Image.fromarray(g, "L").save(os.path.join(a, f"grain{i}.png"))

    tiles = "".join(f'<div class="fl t" data-layout-allow-occlusion id="t{r}_{c}" style="left:{GX + c * (TW + TG)}px;top:{GY + r * (TH + RG)}px"></div>' for r in range(4) for c in range(COLS))
    rows = "".join(f'<div class="fl p" data-layout-allow-occlusion id="p{i}" style="top:{y}px"></div><div class="fl rw" data-layout-allow-occlusion id="r{i}" style="top:{y}px"></div>' for i, y in enumerate(ROW_Y))
    bokeh = "".join(f'<i style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;background:{c}" data-p="{p}"></i>' for x, y, s, c, p in [
        (-60, 420, 260, "rgba(233,185,73,.20)", .3), (860, 300, 200, "rgba(241,236,224,.13)", .5), (760, 1180, 320, "rgba(233,185,73,.16)", .35),
        (40, 1300, 180, "rgba(241,236,224,.10)", .6), (420, 90, 150, "rgba(233,185,73,.14)", .45), (980, 760, 240, "rgba(233,185,73,.12)", .25),
        (-40, 860, 140, "rgba(46,114,99,.25)", .5), (600, 1500, 220, "rgba(46,114,99,.22)", .4)])
    ribs = "".join(f'<path d="M{x0} 1900 C{x0} {420 - k * 40} {1080 - x0} {420 - k * 40} {1080 - x0} 1900" />' for k, x0 in enumerate((-260, -120, 20, 140)))
    ribs += "".join(f'<line x1="{x}" y1="0" x2="{540 + (x - 540) * 1.6}" y2="1920"/>' for x in range(-200, 1300, 150))
    cticks = "".join(f'<line x1="0" y1="-60" x2="0" y2="{-50 if i % 5 else -44}" stroke-width="{3 if i % 5 else 6}" transform="rotate({i * 6})"/>' for i in range(60))
    bits = "".join(f'<i class="bit" id="bit{i}"></i>' for i in range(7))
    info = "".join(f'<div class="info" id="info{i}">{s}</div>' for i, (_, _, s) in enumerate(INFO))
    css = f"""
@font-face {{ font-family:"AN"; src:url("assets/anton-latin-400-normal.woff2"); }}
@font-face {{ font-family:"KA"; src:url("assets/karla-latin-500-normal.woff2"); font-weight:500; }}
@font-face {{ font-family:"KA"; src:url("assets/karla-latin-700-normal.woff2"); font-weight:700; }}
@font-face {{ font-family:"AR"; src:url("assets/ibm-plex-sans-arabic-arabic-700-normal.woff2"); }}
* {{ margin:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:#0c1518; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:linear-gradient(#0b1417, #132428 55%, #0e1b1e); }}
#bg {{ position:absolute; inset:-80px; }} #bg svg {{ position:absolute; inset:0; width:100%; height:100%; }} #bg path, #bg line {{ fill:none; stroke:rgba(241,236,224,.045); stroke-width:6; }}
#bokeh i {{ position:absolute; border-radius:50%; filter:blur(26px); }}
#cam {{ position:absolute; inset:0; transform-origin:540px 800px; }}
#board {{ position:absolute; left:64px; top:196px; width:952px; height:1090px; border-radius:22px;
  background:linear-gradient(#20292c, #161d20); box-shadow:0 40px 90px rgba(0,0,0,.6), inset 0 2px 0 rgba(255,255,255,.07), inset 0 -3px 0 rgba(0,0,0,.5); }}
#board:before {{ content:""; position:absolute; inset:12px; border-radius:14px; background:#0f1416; box-shadow:inset 0 6px 18px rgba(0,0,0,.7); }}
.rod {{ position:absolute; top:-40px; width:12px; height:236px; background:linear-gradient(90deg,#2a3336,#4a5458,#2a3336); }}
.screw {{ position:absolute; width:14px; height:14px; border-radius:50%; background:radial-gradient(circle at 35% 35%, #5d686c, #22292b); }}
#hdr {{ position:absolute; left:{GX}px; right:{GX}px; top:226px; height:90px; display:flex; align-items:center; justify-content:space-between; color:{CREAM}; }}
#hdr b {{ font-family:KA; font-weight:700; font-size:38px; letter-spacing:.34em; }} #hdr span {{ font-family:AR; font-size:44px; color:{GOLD2}; }}
#hdr:after {{ content:""; position:absolute; left:0; right:0; bottom:-8px; height:3px; background:rgba(233,185,73,.35); }}
.fl {{ position:absolute; perspective:500px; }} .fl .h {{ position:absolute; left:0; right:0; height:50%; overflow:hidden; border-radius:7px; backface-visibility:hidden; }}
.fl .top {{ top:0; border-bottom-left-radius:0; border-bottom-right-radius:0; background:linear-gradient(#2a3236, #20272a); transform-origin:50% 100%; }}
.fl .bot {{ top:50%; border-top-left-radius:0; border-top-right-radius:0; background:linear-gradient(#1c2225, #171c1e); transform-origin:50% 0%; }}
.fl .c {{ position:absolute; left:0; right:0; height:200%; display:flex; align-items:center; justify-content:center; color:{CREAM}; }} .fl .bot .c {{ top:-100%; }}
.fl:after {{ content:""; position:absolute; left:0; right:0; top:calc(50% - 1.5px); height:3px; background:#07090a; box-shadow:0 1px 0 rgba(255,255,255,.05); }}
.t {{ width:{TW}px; height:{TH}px; }} .t .c {{ font-family:AN; font-size:70px; line-height:1; letter-spacing:0; }} .t .c .a {{ font-family:AR; font-size:86px; line-height:1; transform:translateY(-10px); }}
.p {{ left:{GX}px; width:{PLAT_W}px; height:{ROW_H}px; }} .p .c {{ font-family:AN; font-size:76px; }}
.rw {{ left:{GX + PLAT_W + 10}px; width:{1080 - 2 * GX - PLAT_W - 10}px; height:{ROW_H}px; }}
.g {{ color:{GOLD2}; text-shadow:0 0 18px rgba(233,185,73,.45); }} .rw .c .rt {{ color:var(--root, {CREAM}); text-shadow:0 0 calc(var(--rootg, 0) * 20px) rgba(233,185,73,.55); }}
.t .c .rd {{ color:#ec6a5e; text-shadow:0 0 18px rgba(224,87,77,.4); }}
.rc {{ position:absolute; inset:0 24px; display:flex; align-items:center; justify-content:space-between; }} .rc.v {{ justify-content:center; }}
.rc .en {{ display:flex; flex-direction:column; justify-content:center; }} .rc .en b {{ font-family:AN; font-weight:400; font-size:54px; line-height:1.05; letter-spacing:.02em; }}
.rc .en i {{ font-family:KA; font-style:normal; font-weight:500; font-size:27px; color:rgba(241,236,224,.62); letter-spacing:.06em; }}
.rc .ar {{ font-family:AR; font-size:80px; line-height:1; direction:rtl; padding-top:6px; }} .rc.v .ar {{ font-size:76px; padding-top:0; margin-top:-22px; }}
#strip {{ position:absolute; left:{GX}px; right:{GX}px; top:1214px; height:52px; border-radius:8px; background:#0a0e0f; overflow:hidden; }}
.info {{ position:absolute; inset:0; display:flex; align-items:center; justify-content:center; font-family:KA; font-weight:700; font-size:31px; color:#f3c25a;
  text-shadow:0 0 12px rgba(243,194,90,.5); opacity:0; white-space:nowrap; }} .info span, .info {{ unicode-bidi:plaintext; }}
#plate {{ position:absolute; right:84px; top:1272px; font-family:KA; font-weight:700; font-size:15px; letter-spacing:.3em; color:rgba(241,236,224,.6); }}
#clock {{ position:absolute; left:802px; top:58px; width:150px; height:150px; }} #clock svg {{ overflow:visible; }}
#ticket {{ position:absolute; left:126px; top:1330px; width:830px; height:410px; transform-origin:50% 0%; filter:drop-shadow(0 26px 30px rgba(0,0,0,.55)); }}
#paper {{ position:absolute; inset:0; border-radius:16px; background:linear-gradient(170deg, #f8f1de, #efe4c8);
  -webkit-mask:radial-gradient(circle at 0 50%, transparent 26px, #000 27px) left/51% 100% no-repeat, radial-gradient(circle at 100% 50%, transparent 26px, #000 27px) right/51% 100% no-repeat; }}
#paper:before {{ content:""; position:absolute; inset:0; border-radius:16px; background:url(assets/grain0.png) center/540px 960px; opacity:.13; mix-blend-mode:multiply; }}
.tk {{ position:absolute; color:{INK}; }} .tk.lbl {{ font-family:KA; font-weight:700; font-size:21px; letter-spacing:.24em; color:rgba(23,38,43,.72); }}
.tk.big {{ left:56px; top:76px; width:520px; text-align:center; font-family:AR; font-size:128px; line-height:1.08; direction:rtl; }}
.tk.big .rt {{ color:var(--rootp, {INK}); }}
.tk.sub {{ left:56px; top:232px; width:520px; text-align:center; font-family:KA; font-weight:500; font-size:30px; color:rgba(23,38,43,.75); }}
.tk.route {{ font-family:AN; font-size:36px; letter-spacing:.04em; }}
#perf {{ position:absolute; left:624px; top:20px; bottom:20px; border-left:4px dashed rgba(23,38,43,.25); }}
#hole {{ position:absolute; left:706px; top:262px; width:46px; height:46px; border-radius:50%; background:#0f1b1e; box-shadow:inset 0 3px 6px rgba(0,0,0,.6); opacity:0; }}
.bit {{ position:absolute; left:722px; top:278px; width:14px; height:14px; border-radius:50%; background:#f3ead2; opacity:0; }}
#vig {{ position:absolute; inset:0; pointer-events:none; background:radial-gradient(ellipse at 50% 45%, transparent 55%, rgba(0,0,0,.55)); }}
#glow {{ position:absolute; inset:0; pointer-events:none; background:radial-gradient(ellipse at 50% 30%, rgba(255,214,140,.10), transparent 60%); mix-blend-mode:screen; }}
.grain {{ position:absolute; inset:0; background-size:540px 960px; background-repeat:repeat; opacity:0; mix-blend-mode:overlay; pointer-events:none; }}
"""
    body = f"""
<div id="bg"><svg viewBox="-80 -80 1240 2080">{ribs}</svg><div id="bokeh">{bokeh}</div></div>
<div id="cam">
  <div class="rod" style="left:200px"></div><div class="rod" style="left:868px"></div>
  <div id="board"></div>
  <div class="screw" style="left:82px;top:212px"></div><div class="screw" style="left:984px;top:212px"></div>
  <div class="screw" style="left:82px;top:1256px"></div><div class="screw" style="left:984px;top:1256px"></div>
  <div id="hdr"><b>DEPARTURES</b><span>المُغادَرَة</span></div>
  {tiles}{rows}
  <div id="strip">{info}</div><div id="plate">RAFIQ &amp; CO.</div>
  <div id="clock"><svg width="150" height="150" viewBox="-75 -75 150 150"><line x1="0" y1="-140" x2="0" y2="-70" stroke="#3a4448" stroke-width="8"/>
    <circle r="72" fill="#2a3336"/><circle r="64" fill="{CREAM}"/><g stroke="{INK}">{cticks}</g>
    <line id="hh" x1="0" y1="8" x2="0" y2="-30" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>
    <line id="mh" x1="0" y1="10" x2="0" y2="-46" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>
    <g id="sh"><line x1="0" y1="14" x2="0" y2="-52" stroke="{RED}" stroke-width="2.5"/></g><circle r="4.5" fill="{RED}"/></svg></div>
  <div id="ticket"><div id="paper"></div>
    <div class="tk lbl" style="left:56px;top:34px">ONE WAY · ADULT</div>
    <div class="tk big">{TADHKIRA}</div>
    <div class="tk sub">tadhkira · a ticket</div>
    <div id="perf"></div>
    <div class="tk lbl" style="left:668px;top:34px">FROM</div><div class="tk route" style="left:668px;top:62px">JEDDAH</div>
    <div class="tk lbl" style="left:668px;top:124px">TO</div><div class="tk route" style="left:668px;top:150px">MAKKAH</div>
    <div class="tk lbl" style="left:668px;top:330px">No. 2152</div>
    <div id="hole"></div>{bits}
  </div>
</div>
<div id="glow"></div><div id="vig"></div>
{''.join(f'<div class="grain" id="g{i}" style="background-image:url(assets/grain{i}.png)"></div>' for i in range(4))}"""
    occ = lambda h: re.sub(r"<(span|b|i|div)([ >])", r"<\1 data-layout-allow-occlusion data-layout-allow-overlap data-layout-allow-overflow\2", h)  # flaps cover letters by design
    data = {k: {"init": occ(v["init"]), "fd": v["fd"], "ev": [(t, occ(h)) for t, h in v["ev"]]} for k, v in EL.items()}
    js = f"""
const EL = {json.dumps(data, ensure_ascii=False)};
const INFO = {json.dumps([(a, b) for a, b, _ in INFO])}, T_LIT = {T_LIT}, T_PUNCH = {T_PUNCH}, REVEAL = {REVEAL:.3f}, COUNT = {json.dumps(COUNT)};
const D = {{}};
for (const id in EL) {{
  const e = document.getElementById(id); e.innerHTML = ["top st", "bot sb", "top ft", "bot fb"].map((k) => `<div class="h ${{k}}" data-layout-allow-occlusion><div class="c" data-layout-allow-occlusion></div></div>`).join("");
  const q = (s) => e.querySelector(s + " .c");
  D[id] = {{ e, s: EL[id], st:q(".st"), sb:q(".sb"), ft:q(".ft"), fb:q(".fb"), ftw:e.querySelector(".ft"), fbw:e.querySelector(".fb"), last:{{}} }};
}}
function put(d, k, h) {{ if (d.last[k] !== h) {{ d[k].innerHTML = h; d.last[k] = h; }} }}
function at(s, t) {{
  let lo = 0, hi = s.ev.length - 1, i = -1;
  while (lo <= hi) {{ const m = (lo + hi) >> 1; if (s.ev[m][0] <= t) {{ i = m; lo = m + 1; }} else hi = m - 1; }}
  if (i < 0) return [s.init, s.init, 1];
  const prev = i > 0 ? s.ev[i - 1][1] : s.init, p = (t - s.ev[i][0]) / s.fd;
  return p >= 1 ? [s.ev[i][1], s.ev[i][1], 1] : [prev, s.ev[i][1], p];
}}
const mix = (a, b, u) => {{ const h = (x) => [1, 3, 5].map((i) => parseInt(x.slice(i, i + 2), 16)); const A = h(a), B = h(b);
  return "rgb(" + A.map((v, i) => Math.round(v + (B[i] - v) * u)).join(",") + ")"; }};
const ease = (u) => u <= 0 ? 0 : u >= 1 ? 1 : 1 - Math.pow(1 - u, 3);
const cam = document.getElementById("cam"), bg = document.getElementById("bg"), bok = [...document.querySelectorAll("#bokeh i")];
const tk = document.getElementById("ticket"), hole = document.getElementById("hole"), bits = [...document.querySelectorAll(".bit")];
const sh = document.getElementById("sh"), mh = document.getElementById("mh"), hh = document.getElementById("hh"), clock = document.getElementById("clock");
const infos = INFO.map((_, i) => document.getElementById("info" + i)), grains = [0, 1, 2, 3].map((i) => document.getElementById("g" + i));
function draw(t) {{
  for (const id in D) {{
    const d = D[id], [o, n, p] = at(d.s, t);
    put(d, "st", n); put(d, "sb", p >= 1 ? n : o);
    if (p >= 1) {{ d.ftw.style.visibility = "hidden"; d.fbw.style.visibility = "hidden"; }}
    else if (p < 0.5) {{ put(d, "ft", o); d.ftw.style.visibility = "visible"; d.fbw.style.visibility = "hidden";
      d.ftw.style.transform = `rotateX(${{-180 * p}}deg)`; d.ftw.style.filter = `brightness(${{1 - 0.8 * p}})`; }}
    else {{ put(d, "fb", n); d.fbw.style.visibility = "visible"; d.ftw.style.visibility = "hidden";
      d.fbw.style.transform = `rotateX(${{180 * (1 - p)}}deg)`; d.fbw.style.filter = `brightness(${{0.6 + 0.8 * (p - 0.5)}})`; }}
  }}
  const lit = ease((t - T_LIT) / 0.3);                                       // the root letters light up
  document.documentElement.style.setProperty("--root", mix("{CREAM}", "{GOLD2}", lit));
  document.documentElement.style.setProperty("--rootg", lit.toFixed(3));
  document.documentElement.style.setProperty("--rootp", mix("{INK}", "{RED}", lit));
  const bump = (c, a) => {{ const u = t - c; return u < 0 ? 0 : a * Math.exp(-u * 5) * Math.sin(Math.min(u * 18, Math.PI)); }};   // a quick nudge in
  const s = 1 + 0.045 * (t / {END}) + bump(T_LIT, 0.02) + bump(REVEAL, 0.022) + bump(T_PUNCH, 0.008);
  const dx = 5 * Math.sin(1.3 * t) + 2.6 * Math.sin(2.9 * t + 1), dy = 4 * Math.sin(1.7 * t + 0.5) + 2.2 * Math.sin(3.7 * t), r = 0.22 * Math.sin(0.9 * t + 0.3);
  cam.style.transform = `translate(${{dx}}px, ${{dy}}px) rotate(${{r}}deg) scale(${{s}})`;
  bg.style.transform = `translate(${{dx * 0.4}}px, ${{dy * 0.4}}px) scale(${{1 + 0.02 * t / {END}}})`;
  bok.forEach((b, i) => {{ const k = +b.dataset.p; b.style.transform = `translate(${{18 * Math.sin(0.21 * t * (1 + k) + i)}}px, ${{-14 * t * k}}px)`; }});
  const pu = t - T_PUNCH;                                                    // the ticket: it breathes, and jolts when it's punched
  const jolt = pu < 0 ? 0 : 16 * Math.exp(-pu * 7) * Math.cos(pu * 26);
  tk.style.transform = `translateY(${{jolt}}px) rotate(${{-3.2 + 0.5 * Math.sin(0.8 * t) + (pu < 0 ? 0 : 0.8 * Math.exp(-pu * 5) * Math.sin(pu * 22))}}deg)`;
  hole.style.opacity = pu < 0 ? 0 : 1;
  bits.forEach((b, i) => {{ const a = i * 0.9 + 0.3, v = 380 + 90 * (i % 3);
    if (pu < 0 || pu > 1.2) {{ b.style.opacity = 0; return; }}
    b.style.opacity = Math.max(0, 1 - pu / 1.2); b.style.transform = `translate(${{Math.cos(a) * v * pu}}px, ${{-Math.abs(Math.sin(a)) * v * pu + 900 * pu * pu}}px) rotate(${{pu * 400}}deg)`; }});
  const sec = Math.floor(t - 0.3 + 1e-6), u = t - 0.3 - sec, over = u < 0.12 ? 2.4 * Math.sin(u / 0.12 * Math.PI) : 0;   // the clock ticks each second
  sh.setAttribute("transform", `rotate(${{(sec + 1) * 6 + over}})`); mh.setAttribute("transform", `rotate(${{48 + t * 0.1}})`); hh.setAttribute("transform", `rotate(${{304 + t * 0.008}})`);
  const cd = COUNT.reduce((m, c) => m + (t >= c && t < c + 0.5 ? Math.exp(-(t - c) * 6) : 0), 0);
  clock.style.transform = `scale(${{1 + 0.12 * cd}})`;
  infos.forEach((el, i) => {{ const [a, b] = INFO[i]; el.style.opacity = Math.max(0, Math.min(1, (t - a) / 0.25, (b - t) / 0.2)); }});
  const gi = Math.floor(t * 24) % 4; grains.forEach((g, i) => g.style.opacity = i === gi ? 0.09 : 0);
}}
const tl = gsap.timeline({{ paused: true }}), o = {{ t: 0 }};
draw(0);
tl.to(o, {{ t: {END}, duration: {END}, ease: "none", onUpdate: () => draw(o.t) }}, 0);
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;"""
    body = body.replace('class="tk ', 'data-layout-allow-occlusion class="tk ').replace('<span class="rt">', '<span data-layout-allow-occlusion class="rt">')  # the ticket's print sits on its paper
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><title>board</title>
<script src="assets/gsap.min.js"></script><style>{css}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{END}">
{body}
<audio id="snd" src="assets/sound.wav" data-start="0" data-duration="{END}" data-volume="1" data-track-index="1"></audio>
</div><script>{js}
</script></body></html>
""")
    print(f"built {END} s, {len(SND)} flaps, reveal at {REVEAL:.2f} s")

if __name__ == "__main__":
    build()
