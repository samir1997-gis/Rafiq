#!/usr/bin/env python3
"""A vocal pile-on of "hijab" (owner, 27 Oct 2026, #301): an old, chavvy English woman shouts "We need to ban the hijab!", then many
voices (American, Indian, English; men and women) say "hijab", one at a time at first, then faster and faster, overlapping, louder and
shouted, until they're all shouting over each other, and it cuts dead.

  python3 brag-quiz/reels/hijab-pileon/mix.py [OPENER]   (reads brag-quiz/voice/hijab/*.mp3, spoken from hijab-lines.json;
  OPENER = the take of the opening shout, ban5 by default: owner, 27 Oct, "louder and more animated", then "go for 5")
  → brag-quiz/out/hijab/hijab-pileon.wav and .mp3 (hijab-pileon-OPENER.* for another take)"""
import json, os, random, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
VO = os.path.join(ROOT, "brag-quiz/voice/hijab"); OUT = os.path.join(ROOT, "brag-quiz/out/hijab"); SR = 48000
random.seed(7)

def load(f):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
    e = np.sqrt(np.convolve(x ** 2, np.ones(480) / 480, "same")); on = np.where(e > 10 ** (-40 / 20))[0]   # trim the silence round it
    return x[max(0, on[0] - 240):on[-1] + 1200] if len(on) else x

lines = json.load(open(os.path.join(ROOT, "brag-quiz/voice/hijab-lines.json")))
takes = {k: [] for k in ("calm", "emph", "shout")}
for l in lines:
    if l["file"].startswith("ban") or not os.path.exists(os.path.join(VO, l["file"] + ".mp3")): continue   # a voice that failed is left out
    takes[l["file"].split("-")[-1]].append(load(os.path.join(VO, l["file"] + ".mp3")))
OPEN = sys.argv[1] if len(sys.argv) > 1 else "ban5"                    # the owner picked Charlotte's take (27 Oct)
ban = load(os.path.join(VO, OPEN + ".mp3"))

def place(buf, x, t, gain, pan, rate=1.0):
    if rate != 1.0: x = np.interp(np.arange(0, len(x) - 1, rate), np.arange(len(x)), x)   # a touch higher and quicker
    i = int(t * SR); x = x[:max(0, len(buf) - i)] * gain
    buf[i:i + len(x), 0] += x * np.sqrt((1 - pan) / 2); buf[i:i + len(x), 1] += x * np.sqrt((1 + pan) / 2)

# the calls: the gap between them shrinks every time (0.8 s → 0.03 s), the takes go calm → emphatic → shouted, louder as they go
t = len(ban) / SR + 0.45; calls, gap, k = [], 0.8, 0
while gap > 0.03 or len(calls) < 140:
    p = k / 150
    kind = "calm" if p < 0.07 else ("emph" if p < 0.3 else "shout")
    calls.append((t, kind, min(1.0, 0.85 + p * 0.3), random.uniform(-0.15, 0.15) if k < 6 else random.uniform(-0.85, 0.85), 1 + random.uniform(-0.04, 0.06) + p * 0.08))
    t += gap; gap = max(0.028, gap * 0.9); k += 1
    if k >= 150: break
END = calls[-1][0] + 0.9                                                  # the last ones land, then a dead cut
buf = np.zeros((int(END * SR), 2), np.float32)
pool = {k: list(range(len(v))) for k, v in takes.items()}
for i, (t0, kind, g, pan, rate) in enumerate(calls):
    if not pool[kind]: pool[kind] = list(range(len(takes[kind])))
    j = pool[kind].pop(random.randrange(len(pool[kind])))                 # every voice before any repeats
    place(buf, takes[kind][j], t0, g, pan, rate)
lvl = lambda y: np.percentile(np.sqrt(np.convolve(y ** 2, np.ones(480) / 480, "same")), 90)
peak = buf[int((END - 1.2) * SR):int((END - 0.2) * SR)].mean(axis=1) * 2
place(buf, ban, 0.0, 1.4 * lvl(peak) / lvl(ban), 0.0)                   # the shout as loud as the crowd at its peak, and a bit more
cut = int((END - 0.05) * SR); buf[cut:] = 0; buf[cut - 240:cut] *= np.linspace(1, 0, 240)[:, None]
os.makedirs(OUT, exist_ok=True); raw = os.path.join(OUT, "raw.f32")
buf.tofile(raw)
for ext, codec in (("wav", ["-c:a", "pcm_s16le"]), ("mp3", ["-c:a", "libmp3lame", "-b:a", "192k"])):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", raw, "-af",
                    "acompressor=threshold=-18dB:ratio=3:attack=5:release=80,loudnorm=I=-14:TP=-1.0:LRA=11,aresample=" + str(SR), *codec,
                    os.path.join(OUT, f"hijab-pileon{'' if OPEN == 'ban5' else '-' + OPEN}.{ext}")], check=True)
os.remove(raw)
print(f"{END:.1f} s, {len(calls)} calls, {sum(len(v) for v in takes.values())} takes")
