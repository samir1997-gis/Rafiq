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

# the pit, seen from above at an angle (owner's reference): turf top left, the pit running off to the right and the bottom, its long side
# wall lit and going down from the rim, the far wall at the top, the floor below
OPEN = [(430, -30), (960, -30), (1010, 1380), (90, 1380), (120, 1120), (230, 760), (340, 360)]
FLOOR = [(640, 250), (900, 232), (950, 1380), (480, 1380), (530, 820)]
LEFTW = [(430, -30), (640, 250), (530, 820), (480, 1380), (90, 1380), (120, 1120), (230, 760), (340, 360)]
RIGHTW = [(960, -30), (1010, 1380), (950, 1380), (900, 232)]
FARW = [(430, -30), (960, -30), (900, 232), (640, 250)]
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
floor = colorize(np.clip(0.2 + 0.55 * hf, 0, 1), (40, 25, 14), (120, 82, 50)) * sf[..., None] * (0.55 + 0.45 * yy[..., None])
# walls: scraped in vertical strokes by the spade, darker deeper in, the right wall in shade
hw = 0.4 * streak + 0.3 * fine + 0.2 * fine2 + 0.1 * base
sw = lit(hw, 7) * 0.7 + 0.3
wallL = colorize(np.clip(0.2 + 0.55 * hw, 0, 1), (52, 32, 18), (150, 102, 62)) * sw[..., None]
wallR = wallL * 0.55
xs = np.linspace(0, 1, W)[None, :] * np.ones((H, 1))
farw = colorize(np.clip(0.2 + 0.5 * hw, 0, 1), (20, 12, 7), (70, 46, 28)) * sw[..., None] * 0.8
mL, mR, mF, mFar = mask(LEFTW, 2), mask(RIGHTW, 2), mask(FLOOR, 3), mask(FARW, 2)
img = floor * mF[..., None]
img = img * (1 - mL[..., None]) + wallL * (0.95 - 0.55 * yy)[..., None] * mL[..., None]
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
    x, y = rng.uniform(470, 960), rng.uniform(220, 1350)
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
# the spoil from the dig: mud trodden into the grass along the rim and in patches, darker and wetter where it's thick
near = np.asarray(Image.fromarray((mOpen * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(55)), float) / 255
mud = np.clip((near * 2.8 - 0.25) + (noise(90, seed=21) - 0.62) * 2.2, 0, 1) * (1 - mOpen)
mud = np.clip(mud + np.clip((noise(110, seed=22) - 0.6) * 4, 0, 0.9), 0, 1) * (1 - mOpen)
mudc = colorize(np.clip(0.3 * noise(30, seed=23) + 0.5 * fine + 0.2 * fine2, 0, 1), (34, 22, 12), (104, 74, 46)) * (lit(0.5 * fine + 0.5 * fine2, 8) * 0.6 + 0.4)[..., None]
turf = turf * (1 - mud[..., None]) + mudc * mud[..., None]
img = img * mOpen[..., None] + turf * (1 - mOpen[..., None])
MUD = Image.fromarray((mud * 255).astype(np.uint8))
im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")
blades = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(blades)
inside = Image.fromarray((mOpen * 255).astype(np.uint8))
for _ in range(230000):
    x, y = rng.uniform(-10, W + 10), rng.uniform(-10, H + 10)
    px = (min(W - 1, max(0, int(x))), min(H - 1, max(0, int(y))))
    if inside.getpixel(px) > 128 or rng.random() < MUD.getpixel(px) / 255 * 1.1: continue     # no grass where the mud lies
    a = rng.normal(-1.57, 1.1); L = rng.uniform(5, 24); g = rng.uniform(0.35, 1.3) * (0.75 if rng.random() < 0.15 else 1)
    c = (int(np.clip(50 * g + rng.normal(0, 8), 0, 255)), int(np.clip(112 * g + rng.normal(0, 12), 0, 255)), int(np.clip(34 * g, 0, 255)), int(rng.uniform(150, 255)))
    d.line([(x, y), (x + L * np.cos(a), y + L * np.sin(a))], fill=c, width=1 if rng.random() < 0.7 else 2)
# blades hanging over the rim, into the pit, and the rim's shadow on the walls
rim = []
for (x0, y0), (x1, y1) in zip(OPEN, OPEN[1:] + OPEN[:1]):
    if y0 >= 1349 and y1 >= 1349: continue
    for t in np.linspace(0, 1, int(np.hypot(x1 - x0, y1 - y0) / 1.2)): rim.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
cx, cy = 900, 700
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
# clods of the spoil lying on the grass, then the two shovels: one dropped on the turf, one stuck upright in the floor of the pit
cd = ImageDraw.Draw(im, "RGBA")
for _ in range(2600):
    x, y = rng.uniform(0, 1080), rng.uniform(0, 1350)
    if MUD.getpixel((int(min(W - 1, x)), int(min(H - 1, y)))) < 90: continue
    s0 = rng.uniform(3, 12); v = rng.uniform(0.6, 1.1)
    cd.ellipse([x - s0 + 3, y - s0 * .7 + 4, x + s0 + 3, y + s0 * .7 + 4], fill=(8, 5, 2, 130))
    cd.ellipse([x - s0, y - s0 * .7, x + s0, y + s0 * .7], fill=(int(92 * v), int(62 * v), int(36 * v), 255))
    cd.ellipse([x - s0 * .6, y - s0 * .6, x, y - s0 * .1], fill=(int(130 * v), int(92 * v), int(58 * v), 150))
def shovel(L, angle, at, blade_down=True, scale=1.0):
    """a long-handled shovel drawn on its own layer, rotated and placed: wood with a highlight, a dark D-grip, a steel blade with dirt on it"""
    w, h = int(300 * scale), int(L * scale) + int(300 * scale); lay = Image.new("RGBA", (w, h), (0, 0, 0, 0)); g = ImageDraw.Draw(lay)
    cx = w // 2; hw = max(7, int(13 * scale)); top = int(110 * scale); bot = int(L * scale)
    for i in range(-hw, hw + 1):                                     # the handle, lit along one side
        t = (i + hw) / (2 * hw); c = int(150 + 70 * np.exp(-((t - 0.3) / 0.18) ** 2) - 60 * t)
        g.line([(cx + i, top), (cx + i, bot)], fill=(c, int(c * 0.72), int(c * 0.45), 255))
    gr = int(46 * scale); g.rounded_rectangle([cx - gr, top - int(70 * scale), cx + gr, top + int(6 * scale)], radius=int(18 * scale), outline=(28, 28, 28, 255), width=max(6, int(12 * scale)))
    g.rectangle([cx - int(12 * scale), bot - int(6 * scale), cx + int(12 * scale), bot + int(40 * scale)], fill=(70, 70, 66, 255))
    bw, bh = int(96 * scale), int(200 * scale); y0 = bot + int(36 * scale)
    blade = [(cx - bw, y0), (cx + bw, y0), (cx + int(bw * .92), y0 + int(bh * .7)), (cx, y0 + bh), (cx - int(bw * .92), y0 + int(bh * .7))]
    bm = Image.new("L", lay.size, 0); ImageDraw.Draw(bm).polygon(blade, fill=255)
    yy2, xx2 = np.mgrid[0:lay.size[1], 0:lay.size[0]]
    steel = 92 + 62 * np.cos((xx2 - cx) / bw * 1.6 - 0.5) - 30 * ((yy2 - y0) / bh).clip(0, 1) + rng.normal(0, 9, xx2.shape)
    dirt = ((noise_small(lay.size, 0.2) > 0.6) & (((yy2 - y0) / bh) > 0.3)) | (((yy2 - y0) / bh) > 0.78)
    rgb = np.dstack([steel, steel * 0.98, steel * 0.94]); rgb[dirt] = rgb[dirt] * 0.25 + np.array([70, 48, 30]) * 0.75
    bl = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert("RGBA"); bl.putalpha(bm)
    lay = Image.alpha_composite(lay, bl)
    lay = lay.rotate(angle, resample=Image.BICUBIC, expand=True)
    sh = Image.new("RGBA", lay.size, (0, 0, 0, 0)); sh.putalpha(lay.getchannel("A").point(lambda v: v * 0.55)); sh = sh.filter(ImageFilter.GaussianBlur(10))
    return lay, sh
def noise_small(size, f):
    gw, gh = max(2, int(size[0] * f)), max(2, int(size[1] * f))
    return np.asarray(Image.fromarray((rng.random((gh, gw)) * 255).astype(np.uint8)).resize(size, Image.BICUBIC), float) / 255
def place(lay, sh, cx, cy):                                           # the layer's centre at (cx, cy), its shadow down and right of it
    x, y = int(cx - lay.size[0] / 2), int(cy - lay.size[1] / 2); im.alpha_composite(sh, (x + 22, y + 26)); im.alpha_composite(lay, (x, y))
lay, sh = shovel(640, 128, None, scale=0.8); place(lay, sh, 170, 210)   # dropped on the grass, top left: blade up by the rim, grip down to the left
lay, sh = shovel(820, -4, None, scale=0.62); place(lay, sh, 760, 70)   # upright in the floor of the pit, its handle running off the top
# grade: vignette, a touch of warmth, film grain
a = np.asarray(im.convert("RGB"), float)
yv, xv = np.mgrid[0:H, 0:W]; r = np.hypot((xv - W * 0.55) / (W * 0.7), (yv - H * 0.55) / (H * 0.7))
a *= np.clip(1.15 - 0.55 * r ** 2, 0.35, 1)[..., None]
a = a * np.array([1.04, 1.0, 0.94]) + rng.normal(0, 4.5, (H, W, 1))
Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(OUT)
print("grave.png")
