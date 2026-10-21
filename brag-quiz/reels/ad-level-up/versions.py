"""Five trial cuts of the level-up message (owner, 21 Oct 2026): each opens on a different headline line, then the story; 30-90 s.
Built from the clean assembly (cut.py → assembly.mp4), sentence by sentence; each edge snaps to the quietest point near the sentence
boundary. The refund promise and the coffee line are in, at the owner's word (21 Oct); note the site's terms refund within 14 days
of the first payment and the monthly plan is £6.99.
  python3 versions.py /tmp/ad1   → /tmp/ad1/v1.mp4 … v5.mp4"""
import os, subprocess, sys
import numpy as np
W = sys.argv[1]
U = {   # sentence: (from, to) in assembly.mp4
 "A": (0.00, 11.60),    # If you are a Muslim in 2026, you need to realise the odds are already stacked against you, especially … in the West.
 "B": (12.15, 20.62),   # Everywhere you look, everywhere you turn, there is fitna, there is a war being waged against you,
 "C": (20.62, 32.00),   # there are forces that are secretly conspiring to act against you … they want to take you away from your deen.
 "D": (32.05, 37.60),   # It's a reality, and the sooner we realise that reality, the sooner we can combat this.
 "E": (37.65, 41.60),   # The reality is we have to level up as Muslims.
 "F": (41.95, 49.54),   # It's not enough to just be passive Muslims … it's really not enough anymore.
 "H": (52.35, 57.65),   # We have to start investing in ourselves, we have to start investing in our deen.
 "I": (57.65, 63.60),   # From my personal experience, the easiest way to do this is by studying the Arabic language.
 "J": (63.85, 70.08),   # The Quran was sent down to the Prophet Muhammad ﷺ in Arabic.
 "L": (77.88, 82.11),   # Learning Arabic can change your life, and I know that's a big statement, but it's the truth,
 "M": (82.11, 91.51),   # because not only will you be able to understand what you say in your salah … directly communicating with Allah.
 "P": (106.15, 113.60), # I know, I know you have heard all your life that learning the Arabic language is super duper difficult.
 "Q": (113.65, 119.95), # People start learning Arabic, they get nowhere and they quit, but I have a solution for you.
 "R": (120.21, 123.68), # I'm not here to sell you on something that I personally don't believe in.
 "S": (123.95, 137.45), # Look, my proposal is very simple. Sign up to Rafiq, try it for one month … and if you do not see a change in your life, in your salah,
 "S4": (143.35, 146.93),# cancel your subscription and I will give you a full refund.
 "T": (148.52, 154.20), # Within days you will start seeing a difference in your salah, you'll start seeing a difference in your duʿa.
 "X": (168.27, 173.44), # One month of Rafiq costs about the same as a cup of coffee does nowadays.
 "Y": (173.44, 181.81), # If you're ready to level up as a Muslim … then sign up to RafiqArabic.com.
 "Z": (181.81, 999)} # Everyone who signs up gets a 7-day free trial, no card details required … you can just walk away.
V = {"v1": "A B F E H I J R S S4 X Y Z",   # the odds are stacked against you (~86 s)
     "v2": "L A F E H I M X Y Z",            # learning Arabic can change your life (~60 s)
     "v3": "C D F E H I J X Y",              # forces want to take you away from your deen (~50 s)
     "v4": "T P Q R S S4 Y",             # within days, a difference in your salah (~49 s)
     "v5": "F E H I X Y"}                  # it's not enough to be passive Muslims (~31 s)
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(W, "assembly.mp4"), "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                                 capture_output=True).stdout, np.int16).astype(float) / 32768
e = np.sqrt(np.convolve(x ** 2, np.ones(320) / 320, "same"))
def snap(t, w=0.0):                                      # no snapping: the times above are measured (word edges from short transcripts, joins between takes)
    a, b = max(0, int((t - w) * 16000)), min(len(e) - 1, int((t + w) * 16000))
    return round((a + int(np.argmin(e[a:b]))) / 16000, 3) if b > a else round(t, 3)
for name, seq in V.items():
    d = os.path.join(W, name); os.makedirs(d, exist_ok=True); lst = []
    for k, u in enumerate(seq.split()):
        a, b = U[u]; a, b = (snap(a) if a > 0 else 0.0), (snap(b) if b < 999 else 999.0)   # 999: to the end of the file (trim stops there)
        f = os.path.join(d, f"{k:02d}.mov"); lst.append(f"file '{f}'")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(W, "assembly.mp4"),     # trim filters: exact, and the fades sit on the piece
                        "-vf", f"trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS,fps=30,format=yuv420p",
                        "-af", f"atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={(b if b < 999 else 190.88) - a - 0.02:.3f}:d=0.02",
                        "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-c:a", "pcm_s16le", f], check=True)
    open(os.path.join(d, "list.txt"), "w").write("\n".join(lst))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(d, "list.txt"), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                    "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", os.path.join(W, name + ".mp4")], check=True)
    print(name, round(float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", os.path.join(W, name + ".mp4")])), 1), "s")
