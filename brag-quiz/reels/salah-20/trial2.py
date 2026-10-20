"""A second, shorter cut of the 20-words salah reel for a trial post (owner, 20 Oct 2026). The posted one (14 Oct) was our best
Instagram reel (4,727 views, 22.9 s average watch, 96 shares, 69 saves, 89.7 s long); this keeps its look and its hook and cuts it
from the posted master (Drive 1OAjJo3jxvq8jXhZ7fJ5G9CpdDz9D9rcN), so every graphic and sound stays as it was. Taken out:
"You wait in the Barzakh and then, all" · "you look around you, everybody is afraid. And" · "then I have a very simple solution for you."
· "They can take your salah … connect with your Lord. Is learning Arabic difficult? Maybe." · "Start from 20 words … And believe me
when I say this,". Each edge is on a frame where the burnt-in caption has cleared (checked frame by frame), the two talking-head jump
cuts get a slight punch-in, and each cut a quiet shutter. 66 s.
  python3 trial2.py <dir with master.mp4>   → <dir>/trial.mp4"""
import json, os, subprocess, sys
W = sys.argv[1]; SHUTTER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "sfx", "ref", "shutter.wav")
S = [(0.0, 12.47, 1), (14.97, 25.46, 1), (28.27, 42.09, 1), (45.46, 56.88, 1.08), (65.97, 70.98, 1), (76.85, 89.7, 1.08)]   # (from, to, zoom)
fc, n = [], len(S)
for i, (a, b, z) in enumerate(S):
    v = f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS"
    if z != 1: v += f",scale=iw*{z}:ih*{z}:flags=lanczos,crop=1080:1920:(iw-1080)/2:(ih-1920)*0.4"
    fc.append(v + f",fps=30,format=yuv420p,setsar=1[v{i}]")
    fc.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={b - a - 0.03:.3f}:d=0.03[a{i}]")
fc.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][a0]")
t, cuts = 0, []
for a, b, z in S[:-1]: t += b - a; cuts.append(t)
for k, c in enumerate(cuts): fc.append(f"[1:a]volume=0.25,adelay={int(c * 1000) - 20}|{int(c * 1000) - 20}[s{k}]")
fc.append("[a0]" + "".join(f"[s{k}]" for k in range(len(cuts))) + f"amix=inputs={len(cuts) + 1}:normalize=0:duration=first,loudnorm=I=-14.5:TP=-1.5:LRA=11[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(W, "master.mp4"), "-i", SHUTTER, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", os.path.join(W, "trial.mp4")], check=True)
