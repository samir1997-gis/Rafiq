"""A realistic open grave for the "remember" carousel's first slide (owner, 8 Nov 2026: "make the grave look more realistic, it looks too
Minecrafty"). Rendered, not drawn: fractal-noise soil lit from the top left (bump-mapped), the walls scraped in vertical strokes, clods on the
floor, shadow deepening down into the pit, dense turf blade by blade with blades hanging over the rim, a vignette and film grain.

  python3 brag-quiz/remember_grave.py   ->  brag-quiz/stills/remember/grave.png (1080 x 1350)
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 1080, 1350
rng = np.random.default_rng(7)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stills", "remember", "grave.png")

def noise(scale, sx=1.0, sy=1.0, octaves=5, seed=0):
    """fractal value noise in 0..1; sx, sy stretch it (sy > sx: vertical streaks)"""
    r = np.random.default_rng(seed); out = np.zeros((H, W)); amp, tot = 1.0, 0.0
    for o in range(octaves):
        f = scale * 2 ** o; gw, gh = max(2, int(W / f * sx) + 2), max(2, int(H / f * sy) + 2)
        g = Image.fromarray((r.random((gh, gw)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
        out += np.asarray(g, float) / 255 * amp; tot += amp; amp *= 0.5
    return out / tot

def lit(height, strength=6.0):
    """lambert light from the top left on a height field"""
    gy, gx = np.gradient(height * strength)
    n = np.dstack([-gx, -gy, np.ones_like(height)]); n /= np.linalg.norm(n, axis=2, keepdims=True)
    l = np.array([-0.55, -0.6, 0.58]); l /= np.linalg.norm(l)
    return np.clip((n * l).sum(2), 0, 1)

def mask(poly, blur=0):
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).polygon(poly, fill=255)
    if blur: m = m.filter(ImageFilter.GaussianBlur(blur))
    return np.asarray(m, float) / 255

def colorize(v, dark, light):
    v = v[..., None]; return np.array(dark) * (1 - v) + np.array(light) * v

# the pit: its opening, the floor seen far below, the walls between them (the near end runs off the bottom of the frame)
OPEN = [(222, 92), (520, 62), (860, 80), (944, 118), (996, 1350), (118, 1350)]
FLOOR = [(372, 318), (560, 302), (790, 322), (838, 1350), (318, 1350)]
LEFTW = [(222, 92), (372, 318), (318, 1350), (118, 1350)]
RIGHTW = [(944, 118), (790, 322), (838, 1350), (996, 1350)]
FARW = [(222, 92), (520, 62), (860, 80), (944, 118), (790, 322), (560, 302), (372, 318)]

def jag(poly, amp=7, step=14, seed=11):   # dug edges are never straight
    r = np.random.default_rng(seed); out = []
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        n = max(1, int(np.hypot(x1 - x0, y1 - y0) / step))
        for t in np.linspace(0, 1, n, endpoint=False):
            j = 0 if (y0 >= 1349 and y1 >= 1349) else r.normal(0, amp)
            out.append((x0 + (x1 - x0) * t + j, y0 + (y1 - y0) * t + r.normal(0, amp) * (0 if y0 >= 1349 and y1 >= 1349 else 1)))
    return out
OPEN, FLOOR, LEFTW, RIGHTW, FARW = jag(OPEN, 8), jag(FLOOR, 5, seed=12), jag(LEFTW, 3, seed=13), jag(RIGHTW, 3, seed=14), jag(FARW, 3, seed=15)
# soil
base = noise(160, seed=1); fine = noise(18, octaves=4, seed=2); streak = noise(34, sx=2.2, sy=0.6, octaves=5, seed=3); fine2 = noise(5, octaves=3, seed=8)
clods = noise(10, octaves=3, seed=4)
yy = np.linspace(0, 1, H)[:, None] * np.ones((1, W))
img = np.zeros((H, W, 3))
# floor: loose, crumbly, lit from above, lighter towards us
hf = 0.35 * base + 0.35 * fine + 0.3 * fine2
sf = lit(hf, 9) * 0.75 + 0.25
floor = colorize(np.clip(0.2 + 0.55 * hf, 0, 1), (30, 18, 10), (98, 66, 40)) * sf[..., None] * (0.55 + 0.45 * yy[..., None])
# walls: scraped in vertical strokes by the spade, darker deeper in, the right wall in shade
hw = 0.4 * streak + 0.3 * fine + 0.2 * fine2 + 0.1 * base
sw = lit(hw, 7) * 0.7 + 0.3
wallL = colorize(np.clip(0.2 + 0.55 * hw, 0, 1), (34, 20, 11), (118, 78, 46)) * sw[..., None]
wallR = wallL * 0.55
xs = np.linspace(0, 1, W)[None, :] * np.ones((H, 1))
farw = colorize(np.clip(0.2 + 0.5 * hw, 0, 1), (20, 12, 7), (70, 46, 28)) * sw[..., None] * 0.8
mL, mR, mF, mFar = mask(LEFTW, 2), mask(RIGHTW, 2), mask(FLOOR, 3), mask(FARW, 2)
img = floor * mF[..., None]
img = img * (1 - mL[..., None]) + wallL * (0.5 + 0.5 * (1 - (xs * 2.2).clip(0, 1)))[..., None] * mL[..., None]
img = img * (1 - mR[..., None]) + wallR * mR[..., None]
img = img * (1 - mFar[..., None]) + farw * mFar[..., None]
# the floor in the walls' shadow along its edges (contact shadow), and dark where it meets the far wall
edge = np.asarray(Image.fromarray((mF * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(40)), float) / 255
img *= (0.55 + 0.45 * edge)[..., None] ** 0.8 if False else 1
ao = np.asarray(Image.fromarray(((1 - mF) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(28)), float) / 255
img = img * (1 - 0.55 * ao * mF)[..., None]

# crumbs and clods on the floor: each lit from the top left, with its own shadow
cr = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)); cd = ImageDraw.Draw(cr, "RGBA"); fl = Image.fromarray((mF * 255).astype(np.uint8))
for _ in range(1400):
    x, y = rng.uniform(300, 860), rng.uniform(300, 1350)
    if fl.getpixel((int(min(W - 1, x)), int(min(H - 1, y)))) < 200: continue
    s0 = rng.uniform(1.5, 6) * (0.6 + 0.6 * y / H); v = rng.uniform(0.5, 1.0) * (0.5 + 0.4 * y / H)
    cd.ellipse([x - s0 + 2, y - s0 * 0.7 + 3, x + s0 + 2, y + s0 * 0.7 + 3], fill=(10, 6, 3, 120))
    cd.ellipse([x - s0, y - s0 * 0.7, x + s0, y + s0 * 0.7], fill=(int(96 * v), int(64 * v), int(38 * v), 255))
    cd.ellipse([x - s0 * 0.6, y - s0 * 0.6, x + s0 * 0.1, y - s0 * 0.05], fill=(int(140 * v), int(98 * v), int(62 * v), 160))
img = np.asarray(cr.filter(ImageFilter.GaussianBlur(0.7)), float)
# turf: a dense green base, then blade by blade
mOpen = mask(OPEN)
g0 = noise(60, seed=5); g1 = noise(8, octaves=3, seed=6)
turf = colorize(np.clip(0.3 * g0 + 0.7 * g1, 0, 1), (22, 48, 14), (78, 120, 40))
img = img * mOpen[..., None] + turf * (1 - mOpen[..., None])
im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")
blades = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(blades)
inside = Image.fromarray((mOpen * 255).astype(np.uint8))
for _ in range(230000):
    x, y = rng.uniform(-10, W + 10), rng.uniform(-10, H + 10)
    if inside.getpixel((min(W - 1, max(0, int(x))), min(H - 1, max(0, int(y))))) > 128: continue
    a = rng.normal(-1.57, 0.9); L = rng.uniform(6, 20); g = rng.uniform(0.4, 1.25)
    c = (int(np.clip(50 * g + rng.normal(0, 8), 0, 255)), int(np.clip(112 * g + rng.normal(0, 12), 0, 255)), int(np.clip(34 * g, 0, 255)), int(rng.uniform(150, 255)))
    d.line([(x, y), (x + L * np.cos(a), y + L * np.sin(a))], fill=c, width=1 if rng.random() < 0.7 else 2)
# blades hanging over the rim, into the pit, and the rim's shadow on the walls
rim = []
for (x0, y0), (x1, y1) in zip(OPEN, OPEN[1:] + OPEN[:1]):
    if y0 >= 1349 and y1 >= 1349: continue
    for t in np.linspace(0, 1, int(np.hypot(x1 - x0, y1 - y0) / 1.2)): rim.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
cx = sum(p[0] for p in OPEN) / len(OPEN); cy = 600
for x, y in rim:
    for _ in range(3):
        a = np.arctan2(cy - y, cx - x) + rng.normal(0, 0.6); L = rng.uniform(8, 26); g = rng.uniform(0.5, 1.2)
        d.line([(x, y), (x + L * np.cos(a), y + L * np.sin(a))], fill=(int(56 * g), int(118 * g), int(36 * g), 230), width=2 if rng.random() < 0.4 else 1)
shadow = Image.new("L", (W, H), 0); sd = ImageDraw.Draw(shadow)
for x, y in rim: sd.ellipse([x - 3, y - 3, x + 3, y + 30], fill=150)
shadow = shadow.filter(ImageFilter.GaussianBlur(16))
sh = np.asarray(shadow, float) / 255 * mOpen
base_rgb = np.asarray(im.convert("RGB"), float) * (1 - 0.6 * sh)[..., None]
im = Image.fromarray(np.clip(base_rgb, 0, 255).astype(np.uint8)).convert("RGBA")
im = Image.alpha_composite(im, blades.filter(ImageFilter.GaussianBlur(0.4)))
# grade: vignette, a touch of warmth, film grain
a = np.asarray(im.convert("RGB"), float)
yv, xv = np.mgrid[0:H, 0:W]; r = np.hypot((xv - W / 2) / (W * 0.62), (yv - H * 0.55) / (H * 0.62))
a *= np.clip(1.15 - 0.55 * r ** 2, 0.35, 1)[..., None]
a = a * np.array([1.04, 1.0, 0.94]) + rng.normal(0, 4.5, (H, W, 1))
Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(OUT)
print("grave.png")
