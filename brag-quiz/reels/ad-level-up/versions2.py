"""The five trial cuts rebuilt from the original takes (owner, 21 Oct 2026: "you cut me off before I say .com"). The first build cut
from assembly.mp4, whose pieces ended where the loud part of a word stopped and so dropped soft endings (the "m" of .com, "refund",
"nowadays"). Here each sentence (the same units and order as versions.py) is mapped back to the spoken runs of the takes, and every
run's end is followed in the take's own audio until the voice has faded (and its start pulled back to just before the voice), then
joined. Each version's sentence endings are then measured: the voice must be below the room level at every edit.
  python3 versions2.py /tmp/ad1      (needs c00NN.mov, a00NN.wav, spans.json, bits/ from cut.py, and versions.py) → /tmp/ad1/w1.mp4 … w5.mp4 (add dry to print the runs only)"""
import json, os, re, subprocess, sys
import numpy as np
W = sys.argv[1]; HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "versions.py")).read()
U = {k: (float(a), float(b)) for k, a, b in re.findall(r'"(\w+)": \(([\d.]+), ([\d.]+)\)', src)}
V = dict(re.findall(r'"(v\d)": "([A-Z0-9 ]+)"', src))
S = json.load(open(os.path.join(W, "spans.json")))
dur = lambda f: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
B, t = [], 0.0                                           # each bit of the assembly: (start in assembly, take, from, to in the take)
for i, (n, s0, s1) in enumerate(S): B.append((t, n, s0, s1)); t += dur(os.path.join(W, "bits", f"{i:03d}.mov"))
E = {}
def env(n):                                              # voice level per 10 ms (20 ms window) and the room level
    if n not in E:
        x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(W, f"a{n}.wav"), "-f", "s16le", "-"], capture_output=True).stdout, np.int16).astype(float) / 32768
        e = 20 * np.log10(np.sqrt(np.convolve(x ** 2, np.ones(320) / 320, "same"))[::160] + 1e-7)
        E[n] = (e, np.percentile(e, 15))
    return E[n]
quiet = lambda n, i: (env(n)[0][max(0, i):i + 4] < env(n)[1] + 8).all()    # 40 ms at the room level (+8 dB)
def fade_end(n, t, lim):                                 # follow the voice until it fades (at most 0.45 s, not past lim);
    i = int(t * 100)                                     # if it never fades, the cut was inside flowing speech: keep it
    for k in range(i, int(min(t + .45, lim) * 100)):
        if quiet(n, k): return min(lim, max(t, k / 100 + .04))
    return t
def onset(n, t, lim):                                    # the same, backwards, for the start (at most 0.3 s, not before lim)
    i = int(t * 100)
    for k in range(i, int(max(t - .3, lim) * 100), -1):
        if quiet(n, k - 4): return max(lim, min(t, k / 100 - .03))
    return t
def unit_runs(a, b):                                     # the take runs that make up assembly time a..b
    out = []
    for k, (t0, n, s0, s1) in enumerate(B):
        t1 = t0 + (s1 - s0)
        if t1 <= a + 0.01 or t0 >= b - 0.01: continue
        r0 = s0 + max(0.0, a - t0); r1 = s0 + min(s1 - s0, b - t0)
        out.append([n, r0, r1, r1 >= s1 - 0.01, r0 <= s0 + 0.01])   # ends where the bit ends? starts where the bit starts?
    return out
for v, seq in V.items():
    R = []                                               # the take runs, as cut in the first build
    for u in seq.split():
        a, b = U[u]; b = min(b, B[-1][0] + B[-1][3] - B[-1][2])
        ur = unit_runs(a, b)
        for j, (n, r0, r1, at_end, at_start) in enumerate(ur):
            if r1 - r0 < 0.15: continue
            if j == 0 and not at_start and r1 - r0 < 0.3: continue     # the tail of the word before the sentence: not ours
            if j == len(ur) - 1 and j > 0 and not at_end and r1 - r0 < 0.3: continue   # the head of the word after it: not ours either
            if R and R[-1][0] == n and -0.5 < r0 - R[-1][2] < 0.15: R[-1][2] = max(r1, R[-1][2]); continue   # straight on in the same take: one run
            R.append([n, r0, r1])
    runs = []
    for j, (n, r0, r1) in enumerate(R):                  # each edge followed until the voice has faded (start: until it begins)
        nxt = [(r1 + x[1]) / 2 for x in R if x[0] == n and x[1] >= r1]     # never more than halfway to another piece of the same take
        prv = [(r0 + x[2]) / 2 for x in R if x[0] == n and x[2] <= r0]
        e1 = fade_end(n, r1, min(nxt + [99999])); e0 = onset(n, r0, max(prv + [0]))
        if "dry" in sys.argv and (e1 - r1 > .05 or r0 - e0 > .05): print(f"  {v} {n} {r0:.2f}-{r1:.2f}: start {e0 - r0:+.2f}, end {e1 - r1:+.2f}")
        runs.append([n, round(e0, 3), round(e1, 3)])
    loud = [(n, r1, int(env(n)[0][int(r1 * 100) - 3:int(r1 * 100)].max() - env(n)[1])) for n, r0, r1 in runs]   # dB above the room just before each cut
    if "dry" in sys.argv: print(v, json.dumps(runs), "\n   ends still loud:", [x for x in loud if x[2] > 12]); continue     # dry: only print the runs
    d = os.path.join(W, "w" + v[1:]); os.makedirs(d, exist_ok=True); os.makedirs(os.path.join(W, "runs"), exist_ok=True); lst = []
    for k, (n, r0, r1) in enumerate(runs):            # a quick seek to just before the run, then an exact trim on the take's own times (-copyts)
        f = os.path.join(W, "runs", f"{n}_{r0:.3f}_{r1:.3f}.mov"); lst.append(f"file '{f}'")
        if os.path.exists(f): continue                   # the same run in another version
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0, r0 - 3):.3f}", "-copyts", "-i", os.path.join(W, f"c{n}.mov"), "-vf", f"trim={r0}:{r1},setpts=PTS-STARTPTS,fps=30,format=yuv420p",
                        "-af", f"atrim={r0}:{r1},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo,afade=t=in:d=0.01,afade=t=out:st={r1 - r0 - 0.02:.3f}:d=0.02",
                        "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-c:a", "pcm_s16le", f], check=True)
    open(os.path.join(d, "list.txt"), "w").write("\n".join(lst))
    out = os.path.join(W, "w" + v[1:] + ".mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(d, "list.txt"), "-af", "highpass=f=70,loudnorm=I=-16:TP=-1.5:LRA=11",
                    "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", out], check=True)
    json.dump(runs, open(os.path.join(d, "runs.json"), "w"))
    print("w" + v[1:], round(dur(out), 1), "s,", len(runs), "runs, ends still loud:", [x for x in loud if x[2] > 12])
