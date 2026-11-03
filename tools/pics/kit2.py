"""More of the drawing kit (#332): the scenes that many words share (number tiles, ordinals, calendars, the sky at each prayer
time, a ball and a box for the prepositions, people at work) and the extra objects the word list needs."""
import math
from kit import *

AR_DIG = "٠١٢٣٤٥٦٧٨٩"
def ar_num(n): return "".join(AR_DIG[int(c)] for c in str(n))

# ---- numbers -----------------------------------------------------------------------------------------------------------------
def numtile(n, c=ORANGE):
    """Arabic-Indic numeral big, the Western one small, and dots to count for one to ten."""
    s = rect(30, 26, 140, 148, WHITE, 22) + rect(30, 26, 140, 36, c, 22) + rect(30, 46, 140, 16, c, 0, "") + line(30, 62, 170, 62, O)
    s += text(100, 52, str(n), 26, WHITE)
    s += text(100, (128 if n <= 5 else 118) if 0 < n <= 10 else 140, ar_num(n), (64 if n <= 5 else 54) if n < 100 else 52, INK, "DejaVu Sans, Arial, sans-serif")
    if 0 < n <= 10:
        per = 5
        for i in range(n):
            r, k = divmod(i, per); cnt = min(per, n - r * per)
            x = 100 + (k - (cnt - 1) / 2) * 22
            s += A("p", circ(x, 138 + r * 18 if n > 5 else 152, 7, c, T), d=i % 4)
    return s
def ordinal(n):
    suf = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    c = {1: GOLD, 2: "#C9D1D6", 3: "#D08A4E"}.get(n, "#7FB3FF")
    return (path("M66 20L90 84L110 84L134 20L114 20L100 60L86 20Z", RED if n <= 3 else PURPLE) +
            A("j", circ(100, 120, 54, c) + circ(100, 120, 42, "none", T) + text(100, 136, f"{n}<tspan font-size='22'>{suf}</tspan>", 44, INK)))

# ---- calendars, clocks, the sky ----------------------------------------------------------------------------------------------
def cal(body="", hdr="", c=RED, x=100, y=108):
    return (rect(x - 66, y - 70, 132, 142, WHITE, 14) +
            path(f"M{x - 66} {y - 30}L{x - 66} {y - 56}Q{x - 66} {y - 70} {x - 52} {y - 70}L{x + 52} {y - 70}Q{x + 66} {y - 70} {x + 66} {y - 56}L{x + 66} {y - 30}Z", c) +
            rect(x - 36, y - 84, 12, 28, INK, 6, "") + rect(x + 24, y - 84, 12, 28, INK, 6, "") + (text(x, y - 40, hdr, 24, WHITE) if hdr else "") + body)
def grid(cols, rows, x0, y0, w, h, hi=(), hc=RED, fill="#EEF1F3"):
    s = ""
    for r in range(rows):
        for k in range(cols):
            i = r * cols + k
            cell = rect(x0 + k * w, y0 + r * h, w - 5, h - 5, hc if i in hi else fill, 3, T)
            s += A("p", cell, d=1) if i in hi else cell
    return s
def daycal(hdr, n=None, icon=""):
    body = (text(100, 128, ar_num(n), 58, INK, "DejaVu Sans, Arial") + text(100, 164, str(n), 22, "#6B7378")) if n else icon
    return cal(body, hdr, RED)
def hijri(n, name):
    return (cal(moon(68, 116, 18, YELLOW) + text(118, 136, ar_num(n), 54, INK, "DejaVu Sans, Arial") + text(100, 166, f"month {n}", 16, "#6B7378"), "", TEAL)
            + text(100, 75, name, 22 if len(name) <= 9 else 15, WHITE))
def ground(y=150, fill="#C9B08A"):
    dx = math.sqrt(94 ** 2 - (y - 100) ** 2)
    return f'<path d="M{100 - dx:.1f} {y}L{100 + dx:.1f} {y}A94 94 0 0 1 {100 - dx:.1f} {y}Z" fill="{fill}" {O}/>'
def skyline(fill="#7A5A3A"):  # a small mosque on the horizon
    return f'<g fill="{fill}">' + path("M112 150L112 128L152 128L152 150Z", fill, "") + path("M118 128C118 108 146 108 146 128Z", fill, "") + rect(156, 98, 9, 52, fill, 1, "") + path("M156 98L160.5 88L165 98Z", fill, "") + "</g>"
def sky(sun_at=None, moon_at=None, stars=False, ground_c="#C9B08A", mosque=True):
    s = ""
    if stars: s += sparks((48, 56, 7), (140, 44, 6), (96, 34, 5), (160, 84, 5))
    if moon_at: s += A("b", moon(*moon_at, 22, "#FFE08A"))
    if sun_at: s += A("p", sun(sun_at[0], sun_at[1], 22, True))
    return s + (skyline() if mosque else "") + ground(150, ground_c)
SKY = {"dawn": "#B9C6E8", "day": "#BFE3FF", "asr": "#FFE2B0", "dusk": "#F7B08A", "night": "#2D3A66"}

# ---- the ball and the box (prepositions) -------------------------------------------------------------------------------------
BOXC, BOXT, BALL = "#D8A86A", "#B98545", RED
def floor(): return line(30, 164, 170, 164, f'stroke="{INK}" stroke-width="5" stroke-linecap="round" opacity=".35"')
def boxfront(x=100, y=164, w=76, h=56): return rect(x - w / 2, y - h, w, h, BOXC, 6)
def boxtop(x=100, y=164, w=76, h=56): return path(f"M{x - w / 2} {y - h}L{x - w / 2 + 14} {y - h - 16}L{x + w / 2 + 14} {y - h - 16}L{x + w / 2} {y - h}Z", BOXT)
def boxside(x=100, y=164, w=76, h=56): return path(f"M{x + w / 2} {y - h}L{x + w / 2 + 14} {y - h - 16}L{x + w / 2 + 14} {y - 16}L{x + w / 2} {y}Z", "#C08A50")
def solidbox(x=100, y=164, w=76, h=56): return boxside(x, y, w, h) + boxtop(x, y, w, h) + boxfront(x, y, w, h)
def ball_(x, y, r=18): return circ(x, y, r, BALL) + path(f"M{x - r * .5} {y - r * .45}q{r * .3} {-r * .3} {r * .6} {-r * .2}", "none", f'stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".8"')
def prep(kind):
    f = floor()
    if kind == "in": return f + boxside() + path("M62 108L76 92L152 92L138 108Z", "#7A5232") + A("b", ball_(104, 104)) + boxfront()
    if kind == "on": return f + solidbox() + A("b", ball_(104, 74))
    if kind == "above": return f + solidbox() + A("u", ball_(104, 46)) + path("M90 72l28 0", "none", f'stroke="{INK}" stroke-width="4" stroke-dasharray="5 6" opacity=".4"')
    if kind == "under": return f + rect(44, 92, 112, 14, BROWN, 4) + line(54, 106, 54, 164) + line(146, 106, 146, 164) + A("b", ball_(100, 146))
    if kind == "behind": return f + A("x", ball_(134, 96, 20)) + solidbox(96, 166)
    if kind == "front": return f + solidbox(110, 150) + A("b", ball_(84, 146, 20))
    if kind == "next": return f + solidbox(86, 164) + A("b", ball_(150, 146))
    if kind == "between": return f + solidbox(52, 164, 50, 48) + solidbox(144, 164, 50, 48) + A("b", ball_(100, 146))
    if kind == "around": return f + solidbox(96, 150) + A("t", f'<circle cx="104" cy="112" r="70" fill="none"/>' + ball_(104, 42, 14))
    if kind == "outside": return f + boxside(84) + path("M46 108L60 92L136 92L122 108Z", "#7A5232") + boxfront(84) + A("h", ball_(156, 146))
    if kind == "near": return f + solidbox(76) + A("b", ball_(140, 146)) + arrow(120, 120, 132, 120, GREEN, 5)
    if kind == "far": return f + solidbox(60, 164, 60, 46) + ball_(162, 154, 10) + path("M100 138L148 138", "none", f'stroke="{INK}" stroke-width="4" stroke-dasharray="6 7"') + A("g", arrow(102, 120, 150, 120, RED, 5))
    raise KeyError(kind)

# ---- people at work and play -------------------------------------------------------------------------------------------------
def stetho(x, y, s=.62): return path(f"M{x - 16 * s} {y - 166 * s}C{x - 22 * s} {y - 120 * s} {x + 22 * s} {y - 120 * s} {x + 16 * s} {y - 166 * s}M{x} {y - 128 * s}L{x + 4 * s} {y - 100 * s}", "none", f'stroke="{INK}" stroke-width="4"') + circ(x + 4 * s, y - 94 * s, 6 * s, GREY, T)
def doctor(x=100, y=184, f=False, s=.62): return (woman(x, y, s, body=WHITE, top="hijab:#4D96FF") if f else man(x, y, s, body=WHITE, top=None, beard="#2a1d14")) + stetho(x, y, s)
def badge(x, y, c=GOLD, r=8): return star(x, y, r, c, T)
def uniform(x=100, y=184, cap="#1E3A5F", body="#2E4A8C", stars=1, s=.62, arm=None):
    st = "".join(badge(x - 14 * s + k * 14 * s, y - 150 * s, GOLD, 5) for k in range(stars))
    return person(x, y, s, SKIN[1], f"cap:{cap}", body, arm=arm) + st
def worker(x=100, y=184, s=.62, arm=None): return person(x, y, s, SKIN[2], f"helmet:{YELLOW}", ORANGE, arm=arm) + path(f"M{x - 26 * s} {y - 166 * s}L{x - 30 * s} {y - 70 * s}M{x + 26 * s} {y - 166 * s}L{x + 30 * s} {y - 70 * s}", "none", f'stroke="{YELLOW}" stroke-width="5"')
def suit(x=100, y=184, s=.62, f=False, arm=None):
    base = woman(x, y, s, body="#34495E", arm=arm) if f else man(x, y, s, body="#34495E", top=None, arm=arm)
    return base + ("" if f else path(f"M{x} {y - 168 * s}L{x - 6 * s} {y - 150 * s}L{x} {y - 110 * s}L{x + 6 * s} {y - 150 * s}Z", RED, T))
def grad(x=100, y=184, s=.62): return man(x, y, s, body="#2B2F36", top=None) + path(f"M{x - 52 * s} {y - 244 * s}L{x} {y - 266 * s}L{x + 52 * s} {y - 244 * s}L{x} {y - 222 * s}Z", "#2B2F36") + A("st", line(x + 40 * s, y - 248 * s, x + 44 * s, y - 214 * s, f'stroke="{GOLD}" stroke-width="4"'))
def seated(x=100, y=180, s=.6, skin=SKIN[1], top="kufi", body=TEAL, arm=None, chair=BROWN, beard="#2a1d14", prop=""):
    ch = f'<g transform="translate({x},{y}) scale({s})">' + rect(-56, -200, 112, 130, chair, 10) + rect(-70, -80, 140, 22, chair, 8) + rect(-64, -58, 14, 58, chair, 4) + rect(50, -58, 14, 58, chair, 4) + "</g>"
    return ch + person(x, y - 18 * s, s, skin, top, body, arm, beard, legs=True, prop=prop)
def wide_person(x=100, y=184, s=.62, k=1.6, **kw):
    """A rounder or slimmer body (k > 1 wider, k < 1 slimmer)."""
    p = person(x, y, s, kw.get("skin", SKIN[1]), kw.get("top", "kufi"), kw.get("body", TEAL), beard=kw.get("beard", "#2a1d14"))
    return p.replace("M-46 -60L-36 -168Q0 -190 36 -168L46 -60Z", f"M{-46 * k} -60C{-56 * k} -120 {-44 * k} -168 0 -176C{44 * k} -168 {56 * k} -120 {46 * k} -60Z" if k > 1 else f"M{-46 * k} -60L{-36 * k} -168Q0 -186 {36 * k} -168L{46 * k} -60Z")
def glow(x, y, r=46, c="#FFE08A"): return A("p", f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity=".75"/>')
def talk(x, y, w=56, h=38, tail="left", c=WHITE): return bubble(x, y, w, h, c, tail) + "".join(A("g", circ(x + w / 2 + (k - 1) * 13, y + h / 2, 4.5, INK, ""), d=k) for k in range(3))
def think(x, y, w, h, inner=""): return thought(x, y, w, h) + inner
def qmark(x, y, size=40, c=PURPLE): return A("j", text(x, y, "?", size, c))
def hand_point(x=100, y=100, flip=False, s=1.0):   # a pointing hand coming from the left
    g = path("M-70 -14L-14 -14L-14 -26C-14 -34 0 -34 0 -26L0 -14L50 -14C60 -14 60 0 50 0L14 0C24 0 24 14 14 14L6 14C16 14 16 28 6 28L-4 28C6 28 6 40 -4 40L-70 40Z", SKIN[1])
    return f'<g transform="translate({x},{y}) scale({-s if flip else s},{s})">' + A("x", g) + "</g>"
def thumbs(x=100, y=104, up=True):
    g = path("M-36 -6L-14 -6L-2 -50C2 -64 22 -62 20 -44L16 -16L44 -16C58 -16 60 0 50 4C60 8 58 22 48 24C56 30 52 42 42 44C48 50 42 62 30 62L-14 62L-14 56L-36 56Z", SKIN[1]) + rect(-48, -10, 22, 74, BLUE, 5)
    return f'<g transform="translate({x},{y})' + ("" if up else " rotate(180)") + '">' + A("b", g) + "</g>"
def handshake(x=100, y=110): return A("j", path(f"M{x - 90} {y + 12}L{x - 44} {y - 14}L{x - 32} {y + 12}L{x - 78} {y + 38}Z", BLUE) + path(f"M{x + 90} {y + 12}L{x + 44} {y - 14}L{x + 32} {y + 12}L{x + 78} {y + 38}Z", TEAL) + ell(x - 6, y, 36, 22, SKIN[3], O, -12) + ell(x + 2, y - 20, 13, 7, SKIN[3], O, -24) + path(f"M{x + 40} {y - 12}C{x + 16} {y - 20} {x - 14} {y - 18} {x - 28} {y - 4}C{x - 34} {y + 4} {x - 26} {y + 12} {x - 16} {y + 10}L{x + 4} {y + 8}C{x - 4} {y + 16} {x} {y + 26} {x + 10} {y + 22}L{x + 36} {y + 12}Z", SKIN[1]) + path(f"M{x - 16} {y - 6}l18 -2M{x - 8} {y + 2}l18 -2", "none", T))
def lift(x=100, y=184): return person(x, y, .58, SKIN[1], "hair:#3a2a1c", RED, "up") + A("u", rect(x - 60, y - 150, 120, 10, INK, 4, "") + rect(x - 72, y - 166, 16, 42, GREY, 4) + rect(x + 56, y - 166, 16, 42, GREY, 4))
def waver(x=100, y=184, f=False, s=.62): return (woman(x, y, s, arm="wave") if f else man(x, y, s, arm="wave"))

# ---- objects -----------------------------------------------------------------------------------------------------------------
def snail(x=100, y=150): return A("x", path(f"M{x - 70} {y}C{x - 70} {y - 14} {x - 40} {y - 14} {x + 30} {y - 10}L{x + 52} {y - 40}C{x + 58} {y - 50} {x + 74} {y - 44} {x + 66} {y - 30}L{x + 50} {y}Z", "#F2C46B") + circ(x - 12, y - 44, 38, "#C26B3A") + path(f"M{x - 12} {y - 44}m0 -22a22 22 0 1 1 -20 30a12 12 0 1 1 14 -14", "none", T) + line(x + 56, y - 44, x + 50, y - 64, T) + line(x + 66, y - 40, x + 70, y - 60, T))
def broom(x=100, y=100): return A("s", line(x + 40, y - 80, x - 6, y + 30, f'stroke="{BROWN}" stroke-width="9" stroke-linecap="round"') + path(f"M{x - 20} {y + 20}L{x + 10} {y + 34}L{x - 4} {y + 76}L{x - 60} {y + 50}Z", YELLOW) + "".join(line(x - 50 + k * 12, y + 46 + k * 5, x - 30 + k * 10, y + 30 + k * 2, T) for k in range(4)), origin="70% 0%") + "".join(A("r", circ(x + dx, y + 70, 4, GREY, ""), d=i) for i, dx in enumerate((-70, -56, -40)))
def iron(x=100, y=128): return A("x", path(f"M{x - 60} {y}C{x - 60} {y - 30} {x + 10} {y - 46} {x + 60} {y - 30}L{x + 60} {y}Z", "#7FB3FF") + path(f"M{x - 30} {y - 36}C{x - 30} {y - 62} {x + 40} {y - 62} {x + 40} {y - 34}", "none", f'stroke="{INK}" stroke-width="9" stroke-linecap="round"') + rect(x - 66, y, 132, 12, GREY, 4)) + steam(x - 30, y - 50, 2, 20) + rect(x - 86, y + 16, 172, 10, "#E8DCC8", 4)
def rings(x=100, y=112): return circ(x - 20, y + 10, 34, "none", f'stroke="{INK}" stroke-width="17"') + circ(x - 20, y + 10, 34, "none", f'stroke="{GOLD}" stroke-width="9"') + circ(x + 22, y + 10, 34, "none", f'stroke="{INK}" stroke-width="17"') + circ(x + 22, y + 10, 34, "none", f'stroke="{GOLD}" stroke-width="9"') + A("g", path(f"M{x + 10} {y - 40}L{x + 22} {y - 56}L{x + 34} {y - 40}L{x + 22} {y - 26}Z", "#CDEBFF", T))
def chequer(x=100, y=100):
    cells = "".join(rect(x - 50 + k * 26, y - 66 + r * 22, 26, 22, INK if (r + k) % 2 else WHITE, 0, "") for r in range(3) for k in range(4))
    return line(x - 50, y - 70, x - 50, y + 84, f'stroke="{INK}" stroke-width="8" stroke-linecap="round"') + A("s", cells + rect(x - 50, y - 66, 104, 66, "none", 2), origin="0% 50%")
def play(x=100, y=100): return A("p", circ(x, y, 56, GREEN) + path(f"M{x - 16} {y - 26}L{x + 28} {y}L{x - 16} {y + 26}Z", WHITE, T))
def magnifier(x=100, y=100, inner=""): return inner + A("x", circ(x - 14, y - 14, 36, "#CDEBFF") + line(x + 12, y + 12, x + 50, y + 50, f'stroke="{INK}" stroke-width="15" stroke-linecap="round"') + line(x + 14, y + 14, x + 50, y + 50, f'stroke="{BROWN}" stroke-width="8" stroke-linecap="round"') + path(f"M{x - 34} {y - 22}C{x - 30} {y - 36} {x - 20} {y - 40} {x - 10} {y - 38}", "none", f'stroke="#fff" stroke-width="5" stroke-linecap="round"'))
def bag(x=100, y=164, c=PINK): return path(f"M{x - 50} {y}L{x - 44} {y - 90}L{x + 44} {y - 90}L{x + 50} {y}Z", c) + path(f"M{x - 22} {y - 90}C{x - 22} {y - 124} {x + 22} {y - 124} {x + 22} {y - 90}", "none")
def balloon(x=100, y=80, c=RED): return A("u", ell(x, y, 34, 42, c) + path(f"M{x - 6} {y + 44}L{x + 6} {y + 44}L{x} {y + 36}Z", c, T) + path(f"M{x} {y + 44}C{x - 10} {y + 70} {x + 10} {y + 80} {x} {y + 104}", "none", T) + path(f"M{x - 16} {y - 20}C{x - 12} {y - 30} {x - 4} {y - 34} {x + 4} {y - 34}", "none", f'stroke="#fff" stroke-width="5" stroke-linecap="round"'))
def razor(x=100, y=100): return A("s", rect(x - 10, y - 10, 20, 90, BLUE, 8) + rect(x - 40, y - 34, 80, 26, GREY, 6) + line(x - 36, y - 34, x + 36, y - 34, f'stroke="{INK}" stroke-width="3"'), origin="50% 100%")
def ruler(x=100, y=104): return A("x", rect(x - 80, y - 20, 160, 40, YELLOW, 4) + "".join(line(x - 70 + k * 14, y - 20, x - 70 + k * 14, y - (2 if k % 2 else -6), T) for k in range(11)))
def telescope(x=100, y=150): return line(x - 20, y + 20, x, y - 20) + line(x + 20, y + 20, x, y - 20) + A("j", path(f"M{x - 60} {y - 10}L{x + 50} {y - 70}L{x + 60} {y - 52}L{x - 50} {y + 8}Z", BLUE) + rect(x + 46, y - 84, 22, 40, BLUE, 4).replace("<rect", f'<rect transform="rotate(-28 {x + 57} {y - 64})"')) + A("g", star(x + 70, y - 116, 12))
def bow(x=100, y=104): return path(f"M{x - 30} {y - 76}C{x + 40} {y - 50} {x + 40} {y + 50} {x - 30} {y + 76}", "none", f'stroke="{BROWN}" stroke-width="10" stroke-linecap="round"') + line(x - 30, y - 76, x - 30, y + 76, T) + A("x", line(x - 70, y, x + 60, y, f'stroke="{INK}" stroke-width="5"') + path(f"M{x + 60} {y - 10}L{x + 80} {y}L{x + 60} {y + 10}Z", GREY, T) + path(f"M{x - 70} {y}L{x - 80} {y - 12}M{x - 70} {y}L{x - 80} {y + 12}", "none", f'stroke="{RED}" stroke-width="5"'))
def basket(x=100, y=164, fill=""): return fill + path(f"M{x - 60} {y - 60}L{x + 60} {y - 60}L{x + 46} {y}L{x - 46} {y}Z", "#D9A55B") + "".join(line(x - 50 + k * 20, y - 60, x - 40 + k * 16, y, T) for k in range(6)) + path(f"M{x - 50} {y - 60}C{x - 50} {y - 120} {x + 50} {y - 120} {x + 50} {y - 60}", "none", f'stroke="{INK}" stroke-width="7"')
def bricks(x=100, y=170): return "".join(rect(x - 78 + k * 52 + (26 if r % 2 else 0), y - 26 - r * 26, 50, 24, "#D9714A", 3, T) for r in range(3) for k in range(3 if r % 2 == 0 else 2)) + A("h", rect(x - 22, y - 130, 50, 24, "#D9714A", 3, T))
def wristwatch(x=100, y=104): return rect(x - 22, y - 80, 44, 160, "#7A5232", 10) + clockface(x, y, 40, 10, 10, WHITE) + rect(x + 40, y - 8, 10, 16, GREY, 3, T)
def sack(x=100, y=168, c="#D9C29A"): return path(f"M{x - 54} {y}C{x - 70} {y - 50} {x - 50} {y - 96} {x - 24} {y - 104}L{x + 24} {y - 104}C{x + 50} {y - 96} {x + 70} {y - 50} {x + 54} {y}Z", c) + path(f"M{x - 28} {y - 104}L{x + 28} {y - 104}", "none", f'stroke="{BROWN}" stroke-width="8"') + path(f"M{x - 24} {y - 108}C{x - 10} {y - 126} {x + 10} {y - 126} {x + 24} {y - 108}", GOLD, T)
def scroll(x=100, y=104): return rect(x - 56, y - 56, 112, 112, "#F2DFB4", 2) + rect(x - 66, y - 70, 132, 20, "#D9B26A", 10) + rect(x - 66, y + 50, 132, 20, "#D9B26A", 10) + "".join(line(x - 38, y - 30 + k * 18, x + 38, y - 30 + k * 18, f'stroke="#9C6B3E" stroke-width="5" stroke-linecap="round"') for k in range(4))
def camera(x=100, y=110): return rect(x - 70, y - 40, 140, 90, "#2B2F36", 12) + rect(x - 40, y - 58, 40, 22, "#2B2F36", 5) + circ(x, y + 6, 32, GREY) + circ(x, y + 6, 18, "#4D96FF", T) + A("g", rect(x + 40, y - 30, 20, 12, YELLOW, 3, T))
def photo(x=100, y=104): return rect(x - 66, y - 60, 132, 120, WHITE, 6) + rect(x - 54, y - 48, 108, 80, "#BFE3FF", 2, T) + path(f"M{x - 54} {y + 32}L{x - 20} {y - 10}L{x + 4} {y + 14}L{x + 22} {y - 4}L{x + 54} {y + 32}Z", GREEN, T) + A("p", circ(x + 30, y - 26, 10, YELLOW, T))
def warning(x=100, y=104): return A("j", path(f"M{x} {y - 70}L{x + 74} {y + 56}L{x - 74} {y + 56}Z", YELLOW) + rect(x - 7, y - 30, 14, 52, INK, 6, "") + circ(x, y + 36, 8, INK, ""))
def speaker(x=90, y=104, on=True): return path(f"M{x - 50} {y - 22}L{x - 24} {y - 22}L{x + 10} {y - 52}L{x + 10} {y + 52}L{x - 24} {y + 22}L{x - 50} {y + 22}Z", GREY) + (waves(x + 4, y, 3, 1.3) if on else cross(x + 50, y, 1.1))
def kettlebell(x=100, y=164, label="1kg"): return path(f"M{x - 30} {y - 90}C{x - 30} {y - 130} {x + 30} {y - 130} {x + 30} {y - 90}", "none", f'stroke="{INK}" stroke-width="16"') + path(f"M{x - 56} {y - 40}C{x - 56} {y - 100} {x + 56} {y - 100} {x + 56} {y - 40}C{x + 56} {y} {x - 56} {y} {x - 56} {y - 40}Z", "#3A3F47") + text(x, y - 28, label, 28, WHITE)
def signpost(x=100, y=176, dirs=("r", "l")):
    s = line(x, y, x, y - 150, f'stroke="{BROWN}" stroke-width="10" stroke-linecap="round"')
    for i, d in enumerate(dirs):
        yy = y - 140 + i * 44
        s += A("j" if i == 0 else "", path(f"M{x - 60} {yy}L{x + 50} {yy}L{x + 70} {yy + 16}L{x + 50} {yy + 32}L{x - 60} {yy + 32}Z" if d == "r" else f"M{x + 60} {yy}L{x - 50} {yy}L{x - 70} {yy + 16}L{x - 50} {yy + 32}L{x + 60} {yy + 32}Z", [ORANGE, BLUE, GREEN][i]))
    return s.replace('<g class="">', "<g>")
def cart(x=100, y=150): return path(f"M{x - 80} {y - 90}L{x - 60} {y - 90}L{x - 40} {y - 20}L{x + 50} {y - 20}L{x + 66} {y - 74}L{x - 52} {y - 74}", "none") + circ(x - 30, y, 10, INK, "") + circ(x + 40, y, 10, INK, "") + A("h", circ(x - 10, y - 56, 14, RED) + circ(x + 20, y - 54, 14, ORANGE))
def stall_seller(): return stall(100, 176) + person(100, 136, .34, SKIN[1], "kufi", TEAL, beard="#2a1d14", legs=False)
def pills(x=100, y=110): return A("j", rect(x - 60, y - 16, 70, 32, RED, 16) + line(x - 25, y - 16, x - 25, y + 16) + path(f"M{x - 25} {y - 16}L{x - 44} {y - 16}C{x - 66} {y - 16} {x - 66} {y + 16} {x - 44} {y + 16}L{x - 25} {y + 16}Z", WHITE, "")) + circ(x + 40, y + 20, 22, YELLOW) + line(x + 24, y + 20, x + 56, y + 20, T) + circ(x + 36, y - 34, 16, "#7FB3FF")
def pillbottle(x=100, y=168): return rect(x - 40, y - 110, 80, 110, ORANGE, 10) + rect(x - 46, y - 132, 92, 26, WHITE, 6) + rect(x - 30, y - 80, 60, 40, WHITE, 4) + path(f"M{x} {y - 74}L{x} {y - 46}M{x - 14} {y - 60}L{x + 14} {y - 60}", "none", f'stroke="{GREEN}" stroke-width="7"')
def cross_sign(x, y, r=18, c=RED): return path(f"M{x - r / 3} {y - r}L{x + r / 3} {y - r}L{x + r / 3} {y - r / 3}L{x + r} {y - r / 3}L{x + r} {y + r / 3}L{x + r / 3} {y + r / 3}L{x + r / 3} {y + r}L{x - r / 3} {y + r}L{x - r / 3} {y + r / 3}L{x - r} {y + r / 3}L{x - r} {y - r / 3}L{x - r / 3} {y - r / 3}Z", c, T)
def gauge(x=100, y=120): return path(f"M{x - 66} {y + 10}A66 66 0 0 1 {x + 66} {y + 10}Z", WHITE) + path(f"M{x + 30} {y - 46}A60 60 0 0 1 {x + 62} {y + 8}", "none", f'stroke="{RED}" stroke-width="8"') + A("w", line(x, y + 10, x - 20, y - 46, f'stroke="{INK}" stroke-width="6" stroke-linecap="round"'), origin="100% 100%") + circ(x, y + 10, 8, INK, "") + rect(x - 30, y + 26, 60, 30, GREY, 8) + path(f"M{x + 30} {y + 40}C{x + 60} {y + 40} {x + 60} {y + 70} {x + 80} {y + 70}", "none")
def blood(x=100, y=104, c=RED): return path(f"M{x} {y - 56}C{x + 30} {y - 14} {x + 40} {y + 10} {x + 40} {y + 22}C{x + 40} {y + 46} {x + 22} {y + 60} {x} {y + 60}C{x - 22} {y + 60} {x - 40} {y + 46} {x - 40} {y + 22}C{x - 40} {y + 10} {x - 30} {y - 14} {x} {y - 56}Z", c)
def jar(x=100, y=170, n=3, c=ORANGE):
    pts = [(-20, -20), (16, -24), (-2, -48), (-30, -54), (24, -56), (6, -80), (-24, -86), (28, -88), (-6, -112), (20, -116), (-28, -116)]
    return "".join(circ(x + dx, y + dy, 13, c, T) for dx, dy in pts[:n]) + path(f"M{x - 50} {y - 140}L{x - 50} {y - 10}Q{x - 50} {y} {x - 40} {y}L{x + 40} {y}Q{x + 50} {y} {x + 50} {y - 10}L{x + 50} {y - 140}", "none") + rect(x - 56, y - 152, 112, 14, BROWN, 5)
def factory(x=100, y=170): return path(f"M{x - 80} {y}L{x - 80} {y - 60}L{x - 46} {y - 80}L{x - 46} {y - 60}L{x - 12} {y - 80}L{x - 12} {y - 60}L{x + 22} {y - 80}L{x + 22} {y}Z", "#9AA4AC") + rect(x + 30, y - 130, 26, 130, "#7A848C", 3) + "".join(A("r", circ(x + 43 + dx, y - 146 - dy, 14, "#6B7378", T), d=i) for i, (dx, dy) in enumerate(((0, 0), (12, 18), (-6, 34)))) + "".join(rect(x - 70 + k * 30, y - 40, 16, 16, YELLOW, 2, T) for k in range(3))
def lightning(x, y, s=1.0, c=YELLOW): return A("g", path(f"M{x + 4 * s} {y - 30 * s}L{x - 14 * s} {y + 4 * s}L{x} {y + 4 * s}L{x - 6 * s} {y + 30 * s}L{x + 14 * s} {y - 6 * s}L{x} {y - 6 * s}Z", c, T))
def scribble(x, y): return A("t", path(f"M{x - 20} {y}C{x - 20} {y - 20} {x + 20} {y - 20} {x + 14} {y + 2}C{x + 8} {y + 18} {x - 14} {y + 12} {x - 8} {y - 4}C{x - 2} {y - 14} {x + 10} {y - 6} {x + 2} {y + 4}", "none", f'stroke="{INK}" stroke-width="4"'))
def circarrow(x=100, y=104, r=50, c=GREEN):
    return A("t", f'<circle cx="{x}" cy="{y}" r="{r}" fill="none"/>' + path(f"M{x + r} {y}A{r} {r} 0 1 1 {x + r * .5} {y - r * .87}", "none", f'stroke="{c}" stroke-width="13" stroke-linecap="round"') + path(f"M{x + r * .5 - 4} {y - r * .87 - 18}L{x + r * .5 + 22} {y - r * .87 + 2}L{x + r * .5 - 8} {y - r * .87 + 18}Z", c, ""))
def timeline(at="now"):
    s = line(26, 120, 174, 120, f'stroke="{INK}" stroke-width="8" stroke-linecap="round"') + "".join(line(40 + k * 30, 110, 40 + k * 30, 130, T) for k in range(5))
    if at == "past": return s + A("xl", arrow(100, 84, 36, 84, BLUE)) + circ(40, 120, 12, BLUE)
    if at == "future": return s + A("x", arrow(100, 84, 164, 84, GREEN)) + circ(160, 120, 12, GREEN)
    return s + A("p", circ(100, 120, 16, RED)) + path("M100 62L100 96", "none", f'stroke="{RED}" stroke-width="6" stroke-linecap="round"') + path("M88 70L100 96L112 70Z", RED, T)
def flag_pk(x=100, y=104): return line(x - 64, y - 64, x - 64, y + 84, f'stroke="{INK}" stroke-width="8" stroke-linecap="round"') + A("s", rect(x - 60, y - 60, 130, 88, "#01411C", 2) + rect(x - 60, y - 60, 32, 88, WHITE, 0, T) + moon(x + 18, y - 16, 26, WHITE).replace(O, "") + star(x + 36, y - 30, 11, WHITE, ""), origin="0% 50%")
def tray(x=100, y=120): return ell(x, y + 20, 74, 18, GOLD) + mini(cup(), x - 30, y - 8, .5) + mini(teaglass(), x + 30, y - 8, .5)
def bubbles(x, y): return "".join(A("r", circ(x + dx, y - dy, r, "#E4F4FF", T), d=i % 4) for i, (dx, dy, r) in enumerate(((-30, 0, 10), (-8, 14, 13), (18, 4, 9), (34, 20, 7))))
def tie_person(x=100, y=184, s=.62): return suit(x, y, s)
def plane_small(x, y, s=.4): return f'<g transform="translate({x},{y}) scale({s})">' + plane(0, 0) + "</g>"
def maqam(x=100, y=168): return rect(x - 46, y - 20, 92, 20, "#E8DCC8", 2) + path(f"M{x - 40} {y - 20}L{x - 40} {y - 90}C{x - 40} {y - 130} {x + 40} {y - 130} {x + 40} {y - 90}L{x + 40} {y - 20}Z", "#F7E7B5") + "".join(line(x - 40 + k * 16, y - 20, x - 40 + k * 16, y - 100 + abs(k - 2.5) * 6, f'stroke="{GOLD}" stroke-width="5"') for k in range(6)) + path(f"M{x - 40} {y - 90}C{x - 40} {y - 130} {x + 40} {y - 130} {x + 40} {y - 90}", "none", f'stroke="{GOLD}" stroke-width="7"') + line(x, y - 122, x, y - 140, T) + circ(x, y - 144, 5, GOLD, T)
def tents(x=100, y=170): return "".join(path(f"M{x + dx - 26} {y + dy}L{x + dx} {y + dy - 36}L{x + dx + 26} {y + dy}Z", WHITE) for dx, dy in ((-56, -40), (0, -46), (56, -40), (-28, -4), (28, -4), (-80, 0), (80, 0)))
def runners(): return rect(20, 140, 160, 30, "#E8743B", 4, "") + line(20, 155, 180, 155, f'stroke="#fff" stroke-width="3" stroke-dasharray="10 8"') + A("x", person(70, 150, .3, SKIN[1], "hair:#3a2a1c", BLUE) + person(110, 150, .3, SKIN[3], "cap:#E8574B", RED)) + chequer(160, 96).replace('stroke-width="8"', 'stroke-width="6"')
def swimmer(x=100, y=120): return A("x", circ(x + 10, y - 6, 18, SKIN[1]) + path(f"M{x - 4} {y - 4}C{x - 30} {y - 40} {x - 60} {y - 30} {x - 70} {y - 10}", "none", f'stroke="{INK}" stroke-width="16" stroke-linecap="round"') + path(f"M{x - 4} {y - 4}C{x - 30} {y - 40} {x - 60} {y - 30} {x - 70} {y - 10}", "none", f'stroke="{SKIN[1]}" stroke-width="8" stroke-linecap="round"') + path(f"M{x + 10} {y - 24}C{x + 2} {y - 34} {x + 20} {y - 40} {x + 28} {y - 16}", "#4D96FF", T)) + "".join(path(f"M10 {y + 8 + k * 22}q15 -12 30 0t30 0t30 0t30 0t30 0t30 0", "none", f'stroke="#4D96FF" stroke-width="8" stroke-linecap="round"') for k in range(3))
def checklist(x=100, y=104): return rect(x - 56, y - 70, 112, 140, WHITE, 8) + rect(x - 24, y - 80, 48, 20, GREY, 6) + "".join(rect(x - 40, y - 46 + k * 34, 20, 20, WHITE, 4, T) + line(x - 8, y - 36 + k * 34, x + 40, y - 36 + k * 34, f'stroke="{GREY}" stroke-width="6" stroke-linecap="round"') + A("p", check(x - 30, y - 38 + k * 34, .55), d=k) for k in range(3))
def form(x=100, y=104): return paper(x - 10, y, 110, 140, 4) + mini(pencil(), x + 34, y + 30, .6)
def report(x=100, y=104): return paper(x, y, 120, 146, 2) + A("p", circ(x + 30, y + 40, 22, GREEN)) + check(x + 30, y + 40, .7, WHITE)
def exam(x=100, y=104): return paper(x, y, 120, 150, 0) + "".join(check(x - 34, y - 42 + k * 34, .5) + line(x - 14, y - 42 + k * 34, x + 40, y - 42 + k * 34, f'stroke="{GREY}" stroke-width="6" stroke-linecap="round"') for k in range(3)) + A("p", text(x + 30, y + 66, "A+", 30, RED))
def atom(x=100, y=104): return "".join(ell(x, y, 62, 22, "none", f'stroke="{BLUE}" stroke-width="5"', a) for a in (0, 60, 120)) + A("p", circ(x, y, 13, RED))
def globe_(x=100, y=104, r=50): return earth(x, y, r) + rect(x - 8, y + r, 16, 20, BROWN, 3) + rect(x - 30, y + r + 18, 60, 10, BROWN, 4)
def letters(x=100, y=110): return "".join(A("b", rect(x + dx - 26, y + dy - 26, 52, 52, c, 10) + ar(x + dx, y + dy + 16, l, 40, WHITE), d=i) for i, (dx, dy, l, c) in enumerate(((-48, 10, "أ", RED), (0, -26, "ب", TEAL), (48, 10, "ت", PURPLE))))
def bilingual(): return bubble(24, 40, 80, 64, WHITE) + ar(64, 86, "ع", 40) + bubble(96, 86, 80, 64, "#FFE08A", "right") + text(136, 130, "Aa", 34)
def coinletter(l, c=GOLD): return A("j", circ(100, 104, 60, c) + circ(100, 104, 48, "none", T) + ar(100, 126, l, 60, "#7A5A10"))
def price(arrow_up=True): return tag(92, 100, "", YELLOW) + (A("u", arrow(150, 150, 150, 50, RED)) if arrow_up else A("u", arrow(150, 50, 150, 150, GREEN))) + text(80, 112, "$$$" if arrow_up else "$", 30)
def visa(out=True): return passport(84, 104) + (A("x", arrow(120, 150, 176, 150, GREEN)) if out else A("xl", arrow(176, 150, 124, 150, BLUE)))
def map_route(): return path("M24 46L74 30L126 46L176 30L176 160L126 176L74 160L24 176Z", "#E7F2D6") + line(74, 30, 74, 160, T) + line(126, 46, 126, 176, T) + path("M44 150C70 120 90 140 110 110C126 86 140 96 156 66", "none", f'stroke="{RED}" stroke-width="5" stroke-dasharray="8 7" stroke-linecap="round"') + pin_small(156, 58)
def pin_small(x, y, c=RED): return A("h", path(f"M{x} {y + 26}C{x - 10} {y + 10} {x - 20} {y} {x - 20} {y - 12}C{x - 20} {y - 26} {x - 10} {y - 34} {x} {y - 34}C{x + 10} {y - 34} {x + 20} {y - 26} {x + 20} {y - 12}C{x + 20} {y} {x + 10} {y + 10} {x} {y + 26}Z", c) + circ(x, y - 13, 7, WHITE, T))
def stack_plates(x=100, y=150): return "".join(ell(x, y - k * 16, 70, 18, WHITE) + ell(x, y - k * 16 - 2, 44, 9, "#F1F1F1", T) for k in range(4))
def menu_card(x=100, y=104): return rect(x - 46, y - 66, 92, 132, "#FFF8EC", 8) + fork(x - 16, y - 30, .34) + knife(x + 16, y - 30, .34) + "".join(line(x - 30, y + 14 + k * 16, x + 30, y + 14 + k * 16, f'stroke="{GREY}" stroke-width="5" stroke-linecap="round"') for k in range(3))
def heater(x=100, y=168): return rect(x - 40, y - 150, 80, 130, WHITE, 30) + gauge_small(x, y - 100) + line(x - 20, y - 20, x - 20, y) + line(x + 20, y - 20, x + 20, y) + A("g", path(f"M{x} {y - 66}C{x + 16} {y - 50} {x + 12} {y - 34} {x} {y - 30}C{x - 12} {y - 34} {x - 16} {y - 50} {x} {y - 66}Z", ORANGE, T))
def gauge_small(x, y): return circ(x, y, 18, "#CDEBFF", T) + line(x, y, x + 8, y - 10, T)
def milk(x=100, y=168): return path(f"M{x - 40} {y}L{x - 40} {y - 100}L{x - 20} {y - 130}L{x + 20} {y - 130}L{x + 40} {y - 100}L{x + 40} {y}Z", WHITE) + path(f"M{x - 40} {y - 100}L{x + 40} {y - 100}", "none", T) + rect(x - 14, y - 146, 28, 18, BLUE, 4) + path(f"M{x - 40} {y - 60}C{x - 20} {y - 70} {x + 10} {y - 50} {x + 40} {y - 62}L{x + 40} {y - 30}L{x - 40} {y - 30}Z", "#9FD8FF", T)
def meal(): return plate(100, 128, 66, 22) + circ(84, 120, 12, ORANGE, T) + ell(112, 122, 18, 9, "#C2453D", T) + circ(100, 112, 9, GREEN, T) + fork(26, 120, .42) + knife(174, 120, .42) + glass(160, 76, 40, 24, "#9fd8ff", .7).replace("stroke-width=\"6\"", "stroke-width=\"3\"")
def belly(x=100, y=184, s=.64): return person(x, y, s, SKIN[1], "hair:#3a2a1c", ORANGE, "fold") + A("g", text(x + 56, y - 110 * s, "~", 34, INK)) + A("j", plate(150, 160, 30, 9))
def team(): return "".join(person(46 + k * 54, 184, .48 if k == 1 else .42, SKIN[k], ["hair:#3a2a1c", "cap:#E8574B", "hair:#1d1d1d"][k], RED) for k in range(3)) + A("h", ball(100, 170, 13))
def hotel(x=100, y=176): return building(x, y, "#C9B6E4", 110, 150) + rect(x - 22, y - 170, 44, 28, RED, 6) + text(x, y - 148, "H", 26, WHITE)
def restaurant(x=100, y=176): return rect(x - 70, y - 90, 140, 90, "#FFD9A8", 2) + path(f"M{x - 80} {y - 90}L{x + 80} {y - 90}L{x + 70} {y - 116}L{x - 70} {y - 116}Z", RED) + rect(x - 54, y - 70, 44, 40, "#CDEBFF", 3, T) + rect(x + 10, y - 60, 34, 60, BROWN, 3) + A("j", circ(x, y - 140, 22, WHITE) + fork(x - 6, y - 128, .2) + spoon(x + 6, y - 128, .2))
def library(x=100, y=176): return rect(x - 76, y - 140, 152, 140, BROWN, 6) + "".join(rect(x - 64, y - 128 + r * 44, 128, 6, "#7A5232", 2, "") + "".join(rect(x - 62 + k * 18, y - 162 + r * 44 + 40 - (k % 3) * 4 - 26, 14, 30 + (k % 3) * 4, [RED, TEAL, YELLOW, PURPLE, BLUE, ORANGE, GREEN][k % 7], 2, T) for k in range(7)) for r in range(3))
def wardrobe_rack(): return line(30, 50, 170, 50, f'stroke="{INK}" stroke-width="7" stroke-linecap="round"') + A("st", mini(shirt(100, 110, BLUE), 62, 104, .55), origin="50% 0%") + A("st", mini(dress(100, 104, PINK), 138, 108, .55), d=1, origin="50% 0%")
def officeblock(n=1): return "".join(building(100 + (k - (n - 1) / 2) * 56, 176, ["#9FB4C8", "#8296AE", "#B6C6D6"][k % 3], 60 if n > 1 else 100, 140 - (k % 2) * 30) for k in range(n)) + (A("j", briefcase(100, 40)) if n == 1 else "")
def scene_room(inner=""): return rect(26, 40, 148, 130, "#FFF3DE", 4) + path("M26 140L174 140", "none", T) + rect(110, 58, 44, 40, "#CDEBFF", 3, T) + line(132, 58, 132, 98, T) + inner
def floorplan(): return rect(30, 34, 140, 132, WHITE, 4) + line(100, 34, 100, 166) + line(30, 100, 170, 100) + A("p", rect(104, 104, 62, 58, "#FFE08A", 2, ""), d=1) + rect(70, 96, 22, 8, WHITE, 0, "") + rect(122, 96, 22, 8, WHITE, 0, "")
def classroom(): return mini(board(100, 100, text(100, 116, "أ ب ت", 36, WHITE, "DejaVu Sans, Arial")), 100, 82, .8) + "".join(rect(32 + k * 52, 150, 36, 14, BROWN, 3) + circ(50 + k * 52, 140, 9, SKIN[k], T) for k in range(3))
def kitchen(): return rect(24, 40, 152, 36, "#C9935A", 6) + line(76, 40, 76, 76) + line(124, 40, 124, 76) + rect(24, 120, 152, 56, "#E8DCC8", 4) + rect(70, 128, 60, 40, GREY, 4) + pot(100, 120, RED) + steam(100, 52, 2, 18)
def dining(): return chair(36, 176) + chair(164, 176) + table(100, 170) + plate(74, 80, 22, 7) + plate(126, 80, 22, 7) + glass(100, 78, 30, 18, "#9fd8ff", .7)
def taxi_cars(): return car(64, 150, BLUE).replace('class="b"', 'class="x"') + car(132, 120, YELLOW).replace('class="b"', 'class="xl"')
def handwash(): return tap_water()
def ihram_walker(): return A("x", ihram(100, 184))
def rider(x=88, y=178): return horse(x, y) + person(x + 2, y - 70, .34, SKIN[1], "kufi", RED, beard="#2a1d14", legs=False) + rect(x - 12, y - 82, 26, 8, INK, 3, "")
def bike_rider(): return bike(100, 150) + person(96, 120, .36, SKIN[1], "helmet:#4D96FF", RED, legs=False)
def hammock_rest(): return sofa(100, 160, PURPLE) + person(100, 126, .3, SKIN[1], "kufi", TEAL, legs=False) + zzz(130, 70)

# ---- four-legged animals, each drawn in its own frame (feet on y = 0, facing right) and placed with beast() ------------------
def beast(inner, x=100, y=172, s=1.0): return f'<g transform="translate({x},{y}) scale({s})">{inner}</g>'
def legs(xs, h, w=12, c=BROWN): return "".join(rect(lx - w / 2, -h, w, h, c, 5) for lx in xs)
def thick(d, w, c): return path(d, "none", f'stroke="{INK}" stroke-width="{w + 9}" stroke-linecap="round" stroke-linejoin="round"') + path(d, "none", f'stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"')
def wag(d, w, c, cls="s"): return A(cls, thick(d, w, c))
def cat(x=96, y=172, c=ORANGE):
    return beast(wag("M-44 -48C-74 -58 -76 -96 -60 -104", 8, c) + legs((-34, -18, 18, 34), 28, 11, c) + ell(0, -46, 48, 20, c) +
                 path("M36 -80L38 -104L54 -88Z", c) + path("M56 -88L68 -104L70 -80Z", c) + circ(54, -70, 20, c), x, y, 1.1)
def dog(x=92, y=172, c="#C68B4B"):
    return beast(wag("M-46 -60L-64 -94", 8, c, "w") + legs((-36, -20, 20, 36), 34, 12, c) + ell(0, -54, 50, 22, c) + thick("M32 -64L52 -86", 18, c) +
                 ell(58, -92, 22, 18, c) + ell(80, -86, 12, 9, c) + circ(90, -88, 4, INK, "") + ell(46, -88, 8, 16, "#8C5A2B", T, 15), x, y, 1.05)
def lion(x=92, y=172, c="#E9A23B"):
    return beast(wag("M-48 -58C-70 -66 -78 -40 -70 -30", 6, c) + circ(-70, -28, 7, "#B5652A", T) + legs((-36, -20, 20, 36), 32, 12, c) + ell(0, -54, 52, 24, c) +
                 circ(56, -84, 34, "#B5652A") + circ(62, -82, 21, c) + ell(78, -76, 9, 7, "#F3D9A6", T), x, y, 1.0)
def fox(x=104, y=170, c="#E8743B"):
    return beast(A("s", path("M-40 -44C-90 -54 -104 -14 -74 -8C-62 -22 -54 -32 -40 -44Z", c) + path("M-84 -10C-94 -14 -100 -22 -98 -30C-90 -24 -86 -18 -78 -12Z", WHITE, T)) + legs((-30, -16, 16, 30), 24, 10, c) + ell(0, -38, 44, 17, c) +
                 path("M40 -66L42 -90L54 -72Z", c) + path("M54 -72L66 -90L68 -64Z", c) + ell(54, -58, 18, 15, c) + path("M66 -66L90 -56L66 -48Z", c) + circ(88, -56, 3.5, INK, ""), x, y, 1.05)
def bear(x=94, y=172, c="#7A5232"):
    return beast(legs((-40, -20, 20, 40), 36, 18, c) + ell(0, -62, 58, 32, c) + circ(42, -110, 10, c) + circ(70, -110, 10, c) + circ(56, -90, 24, c) + ell(76, -84, 11, 9, "#B88A5E", T), x, y, .95)
def pig(x=96, y=170, c="#F4A7B9"):
    return beast(A("j", path("M-56 -52c-14 -4 -16 -18 -6 -18c8 0 6 10 -2 8", "none", O)) + legs((-36, -20, 20, 36), 24, 13, c) + ell(0, -48, 56, 28, c) +
                 path("M42 -72L50 -92L60 -74Z", c) + circ(54, -56, 22, c) + ell(76, -52, 9, 12, "#E98AA3", T) + circ(76, -56, 2, INK, "") + circ(76, -48, 2, INK, ""), x, y, 1.05)
def cow(x=94, y=172, c=WHITE, horn=WHITE, spots=INK):
    sp = "".join(ell(dx, dy, r, r * .7, spots, "") for dx, dy, r in ((-22, -66, 12), (10, -54, 9), (-40, -50, 7), (24, -70, 6))) if spots else ""
    return beast(wag("M-56 -62L-64 -28", 5, c, "st") + legs((-40, -22, 22, 40), 34, 13, c) + ell(0, -58, 58, 26, c) + sp +
                 path("M52 -96C48 -110 40 -114 34 -112", "none", f'stroke="{INK}" stroke-width="9" stroke-linecap="round"') + path("M76 -96C80 -110 88 -114 94 -112", "none", f'stroke="{INK}" stroke-width="9" stroke-linecap="round"') +
                 path("M52 -96C48 -110 40 -114 34 -112M76 -96C80 -110 88 -114 94 -112", "none", f'stroke="{horn}" stroke-width="4" stroke-linecap="round"') +
                 ell(44, -88, 10, 5, c, T) + ell(84, -88, 10, 5, c, T) + ell(64, -80, 18, 22, c) + ell(64, -64, 15, 10, PINK, T), x, y, 1.0)
def bull(x=94, y=172): return cow(x, y, "#5A3A24", "#F3EBDD", None)
def sheep(x=98, y=172):
    wool = "".join(circ(dx, dy, 16, "#F7F3EA") for dx, dy in ((-36, -60), (-12, -70), (14, -70), (36, -60), (-24, -46), (0, -48), (24, -46)))
    return beast(legs((-30, -14, 14, 30), 32, 10, "#3A3A3A") + wool + ell(46, -76, 8, 4, "#3A3A3A", T, -20) + ell(58, -66, 14, 17, "#3A3A3A"), x, y, 1.1)
def goat(x=96, y=172, c="#CFC3B0"):
    return beast(A("j", path("M-46 -58l-8 -12", "none", O)) + legs((-32, -16, 16, 32), 34, 10, c) + ell(0, -56, 46, 20, c) + thick("M30 -64L46 -88", 14, c) +
                 path("M48 -104C44 -124 30 -128 24 -116", "none", f'stroke="{INK}" stroke-width="6" stroke-linecap="round"') + ell(54, -94, 13, 16, c) + path("M58 -80l2 16", "none", O), x, y, 1.15)
def horse(x=92, y=172, c="#8C5A2B"):
    return beast(wag("M-52 -76C-74 -64 -74 -34 -66 -22", 8, "#3A2414") + legs((-38, -22, 22, 38), 46, 12, c) + ell(0, -66, 54, 22, c) + thick("M32 -72L56 -112", 22, c) +
                 path("M28 -82C34 -100 42 -116 50 -128", "none", f'stroke="{INK}" stroke-width="10" stroke-linecap="round"') + path("M52 -126L54 -144L64 -130Z", c) +
                 ell(70, -116, 24, 13, c, O, 28) + circ(88, -104, 3, INK, ""), x, y, 1.0)
def camel(x=92, y=176, c="#D9A55B"):
    return beast(A("j", path("M-46 -78l-6 22", "none", O)) + legs((-32, -16, 18, 32), 56, 10, c) + path("M-30 -90C-24 -132 16 -132 22 -90Z", c) + ell(0, -78, 48, 20, c) +
                 thick("M36 -84C56 -92 50 -122 66 -128", 14, c) + ell(76, -128, 17, 11, c) + path("M64 -136l2 -8", "none", O), x, y, 1.0)
def gazelle(x=96, y=178, c="#D9A55B"):
    return beast(A("j", path("M-42 -80l-8 -10", "none", O)) + legs((-30, -16, 16, 30), 56, 8, c) + ell(0, -74, 44, 16, c) + path("M-34 -66C-10 -60 14 -60 34 -68", "none", f'stroke="#fff" stroke-width="5"') +
                 thick("M30 -80L46 -110", 12, c) + path("M48 -120C42 -144 50 -154 56 -158M56 -120C54 -142 62 -150 68 -154", "none", f'stroke="{INK}" stroke-width="5" stroke-linecap="round"') +
                 ell(42, -122, 7, 3.5, c, T, -20) + ell(56, -114, 15, 10, c, O, 20), x, y, 1.0)
def giraffe(x=86, y=184, c="#F2B544"):
    spots = "".join(circ(dx, dy, r, "#B5652A", "") for dx, dy, r in ((-18, -88, 7), (4, -80, 6), (-2, -96, 5), (22, -92, 6), (32, -116, 5), (38, -136, 5), (44, -156, 4)))
    return beast(legs((-28, -14, 16, 28), 70, 10, c) + ell(0, -86, 40, 18, c) + thick("M24 -94L50 -174", 14, c) + spots +
                 path("M52 -186L52 -200M62 -186L62 -200", "none", O) + circ(52, -202, 4, "#B5652A", T) + circ(62, -202, 4, "#B5652A", T) + ell(62, -178, 18, 10, c, O, 20), x, y, .82)
def elephant(x=88, y=172, c="#A7B2BC"):
    return beast(A("j", path("M-60 -72l-10 26", "none", O)) + legs((-42, -20, 18, 40), 42, 18, c) + ell(0, -72, 62, 34, c) + circ(62, -90, 28, c) +
                 A("s", thick("M82 -80C92 -52 88 -32 100 -20", 18, c)) + path("M76 -72l14 8", "none", f'stroke="#fff" stroke-width="5" stroke-linecap="round"') + ell(46, -88, 22, 30, "#8E9BA6"), x, y, .95)
