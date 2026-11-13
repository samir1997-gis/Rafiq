"""More of the drawing kit (#371, 13 Nov 2026): what the new units (13 Ramadan & Eid, 14 Health, 15 Travel, 16 Stories) and the last
words without a picture need. Same rules as kit.py: flat shapes, an ink outline, faceless figures, a gentle loop that eases."""
from kit2 import *

NIGHT = "#2D3A66"
def night(stars=True): return (sparks((40, 60, 6), (150, 40, 5), (96, 30, 4), (168, 96, 5), (30, 110, 4)) if stars else "")
def eye(x=100, y=104, s=1.0):
    return (path(f"M{x - 70 * s} {y}C{x - 40 * s} {y - 46 * s} {x + 40 * s} {y - 46 * s} {x + 70 * s} {y}C{x + 40 * s} {y + 46 * s} {x - 40 * s} {y + 46 * s} {x - 70 * s} {y}Z", WHITE)
            + circ(x, y, 28 * s, "#6B8E5A") + A("p", circ(x, y, 12 * s, INK, "")) + circ(x + 8 * s, y - 8 * s, 5 * s, WHITE, ""))
def leg(x=100, y=100): return (path(f"M{x - 20} {y - 80}L{x + 14} {y - 80}L{x + 12} {y + 40}L{x + 50} {y + 52}C{x + 60} {y + 56} {x + 58} {y + 72} {x + 46} {y + 72}L{x - 18} {y + 72}Z", SKIN[1])
                               + A("g", circ(x - 2, y - 10, 10, "#FFFFFF66", "")))
def foot(x=100, y=120): return (path(f"M{x - 60} {y + 20}C{x - 70} {y - 10} {x - 40} {y - 34} {x} {y - 30}C{x + 40} {y - 26} {x + 70} {y - 20} {x + 70} {y + 4}C{x + 70} {y + 26} {x + 40} {y + 34} {x} {y + 32}Z", SKIN[1])
                                + "".join(A("b", circ(x + 60 - k * 13, y - 26 + k * 2, 8 - k * .8, SKIN[1], T), d=k % 4) for k in range(5)))
def side(x=100, y=184, s=.62, body=TEAL, skin=SKIN[1], ache=False):
    """a faceless figure seen from the side (facing right); ache: a red pulse on the back"""
    g = rect(-14, -70, 26, 70, INK, 10, "") + path("M-30 -64L-26 -168Q2 -184 26 -166L30 -64Z", body) + circ(0, -210, 36, skin) + path("M-36 -214C-40 -256 30 -258 34 -222C10 -232 -16 -232 -36 -214Z", "#3a2a1c")
    if ache: g += A("p", circ(-30, -120, 20, "#E8574B88", "")) + A("g", lightning(-58, -120, .8, RED))
    return f'<g transform="translate({x},{y}) scale({s})">{g}</g>'
def tear(x, y): return A("f", path(f"M{x} {y - 10}C{x + 8} {y} {x + 7} {y + 9} {x} {y + 9}C{x - 7} {y + 9} {x - 8} {y} {x} {y - 10}Z", "#4D96FF", T))
def sweat(x, y): return A("f", path(f"M{x} {y - 8}C{x + 6} {y} {x + 5} {y + 7} {x} {y + 7}C{x - 5} {y + 7} {x - 6} {y} {x} {y - 8}Z", "#9FD8FF", T))
def road(c="#5B6770"):
    return (path("M70 196L92 70L108 70L130 196Z", c, "") + "".join(A("r", rect(97, 80 + k * 30, 6, 16, WHITE, 2, ""), d=k % 4) for k in range(4)))
def zebra(y=150): return rect(16, y - 30, 168, 60, "#5B6770", 4, "") + "".join(rect(24 + k * 30, y - 26, 18, 52, WHITE, 2, "") for k in range(6))
def walker(x=100, y=184, s=.6, body=TEAL, skin=SKIN[1], top="kufi"):
    g = (A("w", rect(-6, -70, 22, 72, INK, 10, "")) + A("wr", rect(-16, -70, 22, 72, INK, 10, "")) +
         path("M-30 -64L-26 -168Q2 -184 26 -166L30 -64Z", body) + circ(0, -210, 36, skin) + (path("M-34 -222C-32 -254 32 -254 34 -222Z", WHITE) if top == "kufi" else ""))
    return f'<g transform="translate({x},{y}) scale({s})">' + A("x", g) + "</g>"
def speedlines(x, y, n=3): return "".join(A("xl", line(x - 10 - k * 6, y + k * 16, x - 46 - k * 6, y + k * 16, f'stroke="{INK}" stroke-width="5" stroke-linecap="round" opacity=".5"'), d=k) for k in range(n))
def wordcard(arabic, c=TEAL, icon=""):
    """a grammar word on a card, for words that are only grammar (who/which, will not): the word itself, and what it points to"""
    return rect(28, 46, 144, 84, WHITE, 18) + rect(28, 46, 144, 16, c, 8, "") + ar(100, 114, arabic, 46, INK) + icon
def stepnums(a="1", b="2", c=GREEN):
    return (circ(54, 100, 30, WHITE) + text(54, 114, a, 36, INK) + A("x", arrow(92, 100, 116, 100, c)) + A("p", circ(146, 100, 30, c)) + text(146, 114, b, 36, WHITE))
def burst(x=100, y=104, r=60, c=YELLOW):
    import math
    pts = " ".join(f"{x + (r if i % 2 == 0 else r * .62) * math.cos(math.pi * i / 8):.1f},{y + (r if i % 2 == 0 else r * .62) * math.sin(math.pi * i / 8):.1f}" for i in range(16))
    return A("p", f'<polygon points="{pts}" fill="{c}" {O}/>')
def tower(x=150, y=176): return rect(x - 8, y - 110, 16, 110, "#C9D1D6", 2) + path(f"M{x - 24} {y - 110}L{x + 24} {y - 110}L{x + 18} {y - 136}L{x - 18} {y - 136}Z", "#9FD8FF") + A("g", circ(x, y - 146, 6, RED, ""))
def platform(): return rect(14, 160, 172, 18, "#C9B6A0", 2) + path("M20 56L180 56L170 76L30 76Z", "#9B6BFF") + line(40, 76, 40, 160) + line(160, 76, 160, 160)
def legsplit(x=100, y=184, s=.6, body=ORANGE, skin=SKIN[0], arms="up"):
    return person(x, y, s, skin, "hair:#3a2a1c", body, arms)
def cough_puffs(x, y): return "".join(A("r", circ(x + k * 16, y - k * 6, 8 + k * 3, "#E4EEF2", T), d=k) for k in range(3))
def wing(x=100, y=104): return A("s", path(f"M{x - 70} {y + 40}C{x - 60} {y - 40} {x + 10} {y - 70} {x + 70} {y - 60}C{x + 40} {y - 40} {x + 50} {y - 20} {x + 20} {y - 10}C{x + 40} {y} {x + 40} {y + 16} {x + 10} {y + 20}C{x + 24} {y + 30} {x + 16} {y + 44} {x - 10} {y + 44}Z", "#E9E4DA")
                                  + path(f"M{x - 50} {y + 30}C{x - 20} {y - 10} {x + 20} {y - 40} {x + 54} {y - 54}", "none", T))
def dominoes(): return rect(40, 70, 30, 80, WHITE, 4) + circ(55, 92, 5, INK, "") + circ(55, 128, 5, INK, "") + A("s", rect(96, 70, 30, 80, WHITE, 4) + circ(111, 92, 5, INK, "") + circ(111, 128, 5, INK, "")) + A("x", arrow(72, 60, 100, 60, RED))
