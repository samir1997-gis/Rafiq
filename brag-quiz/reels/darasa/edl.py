# Keep the best take of each line; inside each, keep only the speech (silences over 0.4 s cut to a breath).
import re, subprocess, json
log = subprocess.run(["ffmpeg","-i","audio.wav","-af","silencedetect=noise=-35dB:d=0.4","-f","null","-"],capture_output=True,text=True).stderr
ends = [(float(a), float(b)) for a, b in re.findall(r"silence_end: ([\d.]+) \| silence_duration: ([\d.]+)", log)]
sil = [(e - d, e) for e, d in ends]
RANGES = [("intro", 14.20, 20.55), ("pay", 21.00, 22.78), ("darasa", 23.85, 27.25), ("adrusu", 28.35, 30.60),
          ("man", 55.05, 59.70), ("female", 60.05, 64.55), ("he", 79.85, 85.05), ("she", 101.75, 106.85),
          ("we", 116.78, 121.55), ("outro", 130.05, 133.85)]
PAD = 0.12
chunks = []
for name, a, b in RANGES:
    cur = a
    for s, e in sil:
        if e <= a or s >= b: continue
        s2, e2 = max(s, a), min(e, b)
        if s2 + PAD < e2 - PAD and s2 > cur:
            chunks.append((name, round(cur, 3), round(s2 + PAD, 3)))
            cur = e2 - PAD
        elif s2 <= cur:
            cur = max(cur, e2 - PAD)
    if cur < b: chunks.append((name, round(cur, 3), b))
chunks = [c for c in chunks if c[2] - c[1] > 0.12]
t = 0
for c in chunks:
    print(f"{c[0]:7} src {c[1]:7.2f}-{c[2]:7.2f}  out {t:6.2f}"); t += c[2] - c[1]
print("total", round(t, 2))
json.dump(chunks, open("chunks.json", "w"))
