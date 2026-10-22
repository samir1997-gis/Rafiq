"""The Ramadan 100-days video (owner, 22 Oct 2026): two takes from RAW (dji_mimo_20261022_1933 and _1936) cut to the message, in order.
Each piece is given roughly (take, from, to, what's said); its edges then follow the voice in the take's own audio (yesterday's lesson,
the level-up ad: never trust word times at a sentence's end): the start steps back to just before the voice begins, the end runs on
until the voice has faded (40 ms at the room level + 8 dB), never into the next piece's words. Every piece is transcribed on its own
to check it starts and ends on whole words, then they're joined → WORK/clip.mp4 for the reel template (reels/template).
  python3 cut.py WORK      (WORK has c1.mov, c2.mov: 1080x1920 30 fps working copies, and a1.wav, a2.wav: 16 kHz mono)"""
import os, subprocess, sys
import numpy as np
W = sys.argv[1]
P = [  # (take, from, to, limit: never past this (the next words we don't keep), what's said)
    ("1", 5.3, 15.0, 15.4, "Ramadan is less than a hundred days away. I know that came up really quickly, didn't it, SubhanAllah."),
    ("1", 15.45, 16.6, 17.8, "But listen,"),
    ("1", 41.5, 45.75, 46.3, "The Salaf used to prepare for Ramadan when it was six months out."),
    ("1", 46.3, 66.6, 67.4, "Imagine that. After Ramadan ... they'd be preparing for it. Now we have a hundred days left till Ramadan."),
    ("2", 0.0, 6.9, 7.6, "If you want to have the best Ramadan you've ever had in your life, then I would suggest you start preparing from now."),
    ("2", 7.6, 14.3, 15.5, "Start reading Quran daily now. Start getting into the routine of waking up in the middle of the night worshipping Allah."),
    ("2", 15.5, 22.0, 22.7, "And one thing you can do that will really, really, really help you with your Ramadan is studying the Arabic language."),
    ("2", 38.9, 49.6, 50.1, "If you start learning the Arabic language now, by the time we reach Ramadan in sha Allah, you will understand every word you say in your salah,"),
    ("2", 57.0, 65.7, 66.3, "you'll also be able to understand the majority of the smaller surahs ... Don't underestimate the difference that can make to your worship."),
    ("2", 76.1, 84.5, 85.0, "If you want to have the best Ramadan you've ever had in your life, then sign up to RafiqArabic.com now. Do your daily tasks."),
    ("2", 87.6, 90.6, 90.9, "Study consistently for the next 100 days,"),          # "and believe me" said twice: the second take runs on
    ("2", 95.2, 98.2, 99.5, "and believe me, you'll have the best Ramadan you've ever had."),
]
E = {}
def env(n):                                              # voice level per 10 ms (20 ms window) and the room level
    if n not in E:
        x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f"{W}/a{n}.wav", "-f", "s16le", "-"], capture_output=True).stdout, np.int16) / 32768
        e = 20 * np.log10(np.sqrt(np.convolve(x ** 2, np.ones(320) / 320, "same"))[::160] + 1e-7)
        E[n] = (e, np.percentile(e, 15))
    return E[n]
quiet = lambda n, i: (env(n)[0][max(0, i):i + 4] < env(n)[1] + 8).all()
def end_at(n, t, lim):                                   # the voice has faded: the first quiet 40 ms after t (else the quietest point before lim)
    for k in range(int(t * 100), int(lim * 100)):
        if quiet(n, k): return k / 100 + .06
    e = env(n)[0]; return (int(t * 100) + int(np.argmin(e[int(t * 100):int(lim * 100)]))) / 100
def start_at(n, t):                                      # just before the voice begins: step back to quiet (at most 0.4 s)
    k = int(t * 100)
    while k > int((t - .4) * 100) and not quiet(n, k - 4): k -= 1
    return max(0, k / 100 - .05)
os.makedirs(f"{W}/pieces", exist_ok=True); lst = []
for k, (n, a, b, lim, said) in enumerate(P):
    a, b = start_at(n, a), end_at(n, b, lim); P[k] = (n, a, b, lim, said)
    f = f"{W}/pieces/{k:02d}.mov"; lst.append(f"file '{f}'")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0, a - 3):.3f}", "-copyts", "-i", f"{W}/c{n}.mov",
                    "-vf", f"trim={a}:{b},setpts=PTS-STARTPTS,fps=30,format=yuv420p",
                    "-af", f"atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={b - a - 0.02:.3f}:d=0.02",
                    "-c:v", "libx264", "-crf", "14", "-preset", "fast", "-c:a", "pcm_s16le", "-ar", "48000", f], check=True)
open(f"{W}/pieces/list.txt", "w").write("\n".join(lst))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{W}/pieces/list.txt", "-c", "copy", f"{W}/joined.mov"], check=True)
from faster_whisper import WhisperModel                  # the check: every piece on its own, first and last words
m = WhisperModel("small.en", compute_type="int8")
for k, (n, a, b, lim, said) in enumerate(P):
    segs, _ = m.transcribe(f"{W}/pieces/{k:02d}.mov", condition_on_previous_text=False)
    e, fl = env(n); lv = int(e[int(b * 100) - 3:int(b * 100)].max() - fl)
    print(f"{k:02d} take {n} {a:6.2f}-{b:6.2f}  end +{lv:2d} dB | {' '.join(s.text.strip() for s in segs)}")
