# The cut (frame-exact pieces so the sound stays in sync), watermark painted out, the grade, then gentle zooms.
import json, subprocess, os
ch = json.load(open("chunks.json")); G = open("grade.txt").read().strip()
os.makedirs("parts", exist_ok=True); lst = []
for i, (a, b) in enumerate(ch):
    out = f"parts/p{i:02d}.mov"; lst.append(f"file 'p{i:02d}.mov'")
    if os.path.exists(out): continue
    n = round((b - a) * 30); d = n / 30
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a}", "-i", "clip.mp4", "-frames:v", str(n),
        "-vf", f"delogo=x=90:y=600:w=780:h=110,{G},scale=1404:2496:flags=lanczos,fps=30,format=yuv420p",
        "-af", f"atrim=duration={d:.6f},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={d-0.025:.4f}:d=0.025",
        "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-c:a", "pcm_s16le", "-ar", "48000", out], check=True)
open("parts/list.txt", "w").write("\n".join(lst))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "parts/list.txt", "-c", "copy", "cut.mov"], check=True)
print("cut ok")
