"""The "level up as a Muslim" ad, first assembly (owner, 21 Oct 2026): his message from the eight DJI takes of 21 Oct (Drive,
DJI_20261021…_0045 to _0052), best take of each line, in the order of the message, no effects yet. Pauses inside a line are
tightened to 0.22 s; each piece starts and ends in a gap in his voice.
  python3 cut.py /tmp/ad1      (needs c00NN.mov and a00NN.wav: 1080x1920 copies and 16 kHz audio of each take) → /tmp/ad1/assembly.mp4"""
import json, os, subprocess, sys
import numpy as np
W = sys.argv[1]
# (take, from, to, what's said): times are the take's own, from the transcript
PIECES = [
 ("0045", 31.85, 71.65, "If you are a Muslim in 2026 … the sooner we can combat this."),   # the clean take (31.9 s; the first try stops at "the…")
 ("0045", 110.05, 124.05, "the reality is we have to level up as Muslims … It's really not enough anymore."),
 ("0045", 124.45, 127.75, "Look around you. Look what's happening in the world."),
 ("0046", 5.95, 11.30, "We have to start investing in ourselves, we have to start investing in our deen."),
 ("0046", 49.55, 55.40, "from my personal experience, the easiest way to do this is by studying the Arabic language."),
 ("0046", 61.15, 68.00, "The Quran was sent down to the Prophet Muhammad ﷺ in Arabic."),
 ("0046", 69.10, 76.95, "There is a reason why Allah revealed the Quran … upon the Arabic language"),
 ("0050", 0.65, 5.95, "Learning Arabic can change your life, and I know that's a big statement, but it's the truth"),
 ("0050", 12.00, 41.75, "because not only will you be able to understand what you say in your salah … all around the world."),
 ("0046", 90.35, 105.40, "I know, I know … learning the Arabic language is super duper difficult … But I have a solution for you"),
 ("0049", 0.00, 5.10, "I'm not here to sell you on something that I personally don't believe in"),
 ("0051", 0.00, 26.45, "Look, my proposal is very simple … I will give you a full refund."),
 ("0048", 0.65, 23.30, "Forget a full month … It's more personal."),
 ("0047", 0.00, 5.85, "1 month of Rafiq costs about the same as a cup of coffee does nowadays."),
 ("0052", 0.00, 9.00, "If you're ready to level up as a Muslim … sign up to RafiqArabic.com"),
 ("0052", 16.70, 26.70, "Everyone who signs up gets a 7 day free trial … you can just walk away")]
GAP, PAD, KEEP = 0.33, 0.07, 0.22        # a pause longer than GAP inside a piece becomes KEEP long; PAD of air around each spoken bit

def env(n):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(W, f"a{n}.wav"), "-f", "s16le", "-"], capture_output=True).stdout, np.int16).astype(float) / 32768
    e = 20 * np.log10(np.sqrt(np.convolve(x ** 2, np.ones(320) / 320, "same"))[::80] + 1e-7)   # 5 ms steps
    return e, np.percentile(e, 20)
E = {}
spans = []                                   # (take, from, to) after tightening the pauses
for n, a, b, _ in PIECES:
    if n not in E: E[n] = env(n)
    e, floor = E[n]; th = floor + 14
    i0, i1 = int(a * 200), min(len(e), int(b * 200))
    talk = e[i0:i1] > th
    runs, k = [], 0                                       # spoken runs inside the piece
    while k < len(talk):
        if talk[k]:
            j = k
            while j < len(talk) and talk[j]: j += 1
            runs.append([(i0 + k) / 200, (i0 + j) / 200]); k = j
        else: k += 1
    merged = []
    for r in runs:
        if merged and r[0] - merged[-1][1] < GAP: merged[-1][1] = r[1]
        else: merged.append(r)
    for r in merged:
        if r[1] - r[0] < 0.08: continue                   # a click, not a word
        s0, s1 = max(a, r[0] - PAD), min(b, r[1] + PAD)
        if spans and spans[-1][0] == n and s0 - spans[-1][2] < KEEP: s0 = spans[-1][2]
        spans.append([n, round(s0, 3), round(s1, 3)])
# each bit cut on its own (one input at a time keeps memory low), then joined and levelled
os.makedirs(os.path.join(W, "bits"), exist_ok=True); lst = []
for i, (n, s0, s1) in enumerate(spans):
    f = os.path.join(W, "bits", f"{i:03d}.mov"); lst.append(f"file '{f}'")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s0:.3f}", "-i", os.path.join(W, f"c{n}.mov"), "-t", f"{s1 - s0:.3f}",
                    "-vf", "fps=30,format=yuv420p,setsar=1", "-af", f"aformat=sample_rates=48000:channel_layouts=stereo,afade=t=in:d=0.012,afade=t=out:st={s1 - s0 - 0.015:.3f}:d=0.015",
                    "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-c:a", "pcm_s16le", f], check=True)
open(os.path.join(W, "bits", "list.txt"), "w").write("\n".join(lst))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(W, "bits", "list.txt"), "-af", "highpass=f=70,loudnorm=I=-16:TP=-1.5:LRA=11",
                "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", os.path.join(W, "assembly.mp4")], check=True)
json.dump(spans, open(os.path.join(W, "spans.json"), "w"))
print(len(spans), "bits,", round(sum(s1 - s0 for _, s0, s1 in spans), 1), "s")
