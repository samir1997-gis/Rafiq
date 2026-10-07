# Synthesised sound effects, 48 kHz stereo WAV.
import numpy as np, wave
from scipy.signal import butter, sosfilt
SR = 48000
rng = np.random.default_rng(7)
def save(name, x, width=0.0):
    x = x / (np.max(np.abs(x)) + 1e-9) * 0.9
    l, r = x, x
    if width:  # a little stereo: delay one side
        d = int(width * SR); r = np.concatenate([np.zeros(d), x])[:len(x)]
    st = np.stack([l, r], 1)
    with wave.open(f"sfx/{name}.wav", "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
def t(d): return np.arange(int(d * SR)) / SR
def bp_sweep(noise, f0, f1, q=2.0, steps=60):
    out = np.zeros_like(noise); n = len(noise); seg = n // steps
    for i in range(steps):
        f = f0 * (f1 / f0) ** (i / (steps - 1)); bw = f / q
        sos = butter(2, [max(30, f - bw / 2), min(SR / 2 - 100, f + bw / 2)], btype="band", fs=SR, output="sos")
        a, b = i * seg, n if i == steps - 1 else (i + 1) * seg
        pad = min(a, 2000); out[a:b] = sosfilt(sos, noise[a - pad:b])[pad:]
    return out
# whoosh: noise through a rising-then-falling band, swelling then fading
d = 0.55; tt = t(d); n = rng.standard_normal(len(tt))
w = bp_sweep(n, 300, 3500, q=1.5); env = np.sin(np.pi * np.clip(tt / d, 0, 1)) ** 2.2
save("whoosh", w * env, 0.004)
# swish: short and bright
d = 0.28; tt = t(d); n = rng.standard_normal(len(tt))
save("swish", bp_sweep(n, 2500, 7000, q=1.2) * np.sin(np.pi * tt / d) ** 3, 0.003)
# ping: bright bell-like tone
d = 0.9; tt = t(d)
p = sum(a * np.sin(2 * np.pi * f * tt) * np.exp(-tt * k) for f, a, k in [(1760, 1, 5), (2637, .5, 7), (3520, .25, 9), (5274, .12, 12)])
save("ping", p * np.minimum(1, tt / 0.003))
# ding: lower, warmer
d = 1.2; tt = t(d)
save("ding", sum(a * np.sin(2 * np.pi * f * tt) * np.exp(-tt * k) for f, a, k in [(1046, 1, 3.5), (2093, .4, 5), (3136, .2, 7)]) * np.minimum(1, tt / 0.004))
# bell: school-bell style, inharmonic partials
d = 1.6; tt = t(d)
save("bell", sum(a * np.sin(2 * np.pi * f * tt) * np.exp(-tt * k) for f, a, k in [(880, 1, 2.2), (880 * 2.76, .6, 3), (880 * 5.4, .3, 4.5), (880 * 1.5, .3, 2.8)]) * (1 + .3 * np.sin(2 * np.pi * 9 * tt)))
# boom: punchy low hit with a pitch drop and a click on top
d = 0.9; tt = t(d)
f = 90 * np.exp(-tt * 4) + 38; ph = 2 * np.pi * np.cumsum(f) / SR
b = np.sin(ph) * np.exp(-tt * 5.5); click = rng.standard_normal(len(tt)) * np.exp(-tt * 120) * .4
save("boom", b + sosfilt(butter(2, 3000, btype="low", fs=SR, output="sos"), click))
# pop: quick bubbly blip with a falling pitch
d = 0.14; tt = t(d)
f = 900 * np.exp(-tt * 18) + 300; save("pop", np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 30))
# tick: tiny UI tick
d = 0.06; tt = t(d); save("tick", np.sin(2 * np.pi * 3200 * tt) * np.exp(-tt * 90))
# riser: rising noise into the hook
d = 0.8; tt = t(d); n = rng.standard_normal(len(tt))
save("riser", bp_sweep(n, 400, 6000, q=2.5) * (tt / d) ** 2.5, 0.004)
print("sfx ok")
