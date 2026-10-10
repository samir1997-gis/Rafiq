# Shared zoom curve (base video and overlay use the same one, so hand-tied pops follow the picture).
ZOOMS = [  # (start, end, extra zoom, ramp seconds)
    (0.00, 0.70, 0.14, 0.01),    # open tight, ease out
    (2.90, 4.55, 0.12, 0.20),    # "can CHANGE"
    (4.86, 6.55, 0.28, 0.08),    # "PAY ATTENTION" snap
    (9.00, 11.15, 0.08, 0.25),   # adrusu
    (13.38, 14.85, 0.14, 0.12),  # tadrusu
    (16.92, 18.70, 0.14, 0.12),  # tadrusina
    (21.96, 23.50, 0.14, 0.12),  # yadrusu
    (26.36, 28.15, 0.14, 0.12),  # tadrusu (she)
    (28.60, 29.40, 0.10, 0.06),  # "WE" punch
    (30.10, 32.25, 0.16, 0.12),  # nadrusu
    (32.32, 37.40, 0.10, 2.50),  # slow push into the ending
]
AX, AY = 0.5, 0.26   # zoom anchor: the face
def z(t):
    v = 1.0
    for a, b, k, r in ZOOMS:
        if a == 0.0 and r < 0.05:   # opening: starts zoomed, eases out over the range
            if t < b: v += k * (1 - (t / b)) ** 2
            continue
        up = min(1, max(0, (t - a) / r)); dn = min(1, max(0, (b - t) / r))
        e = lambda x: x * x * (3 - 2 * x)
        v += k * e(min(up, dn))
    return v
def ffexpr():
    parts = ["1"]
    for a, b, k, r in ZOOMS:
        if a == 0.0 and r < 0.05: parts.append(f"{k}*pow(max(0,1-T/{b}),2)"); continue
        m = f"min(clip((T-{a})/{r},0,1),clip(({b}-T)/{r},0,1))"
        parts.append(f"{k}*({m})*({m})*(3-2*({m}))")
    return "+".join(parts)
