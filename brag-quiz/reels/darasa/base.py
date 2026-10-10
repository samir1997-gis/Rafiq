import json, subprocess, os
from zoom import ffexpr
ch = json.load(open("chunks.json"))
X0, Y0, CW, CH = 164, 560, 1400, 2489
GRADE = "eq=contrast=1.06:saturation=1.08:gamma=1.02"
os.makedirs("parts", exist_ok=True)
# 1: each piece on its own (seek, crop, grade, keep 1.3x of the final size so zooms stay sharp)
lst = []
for i, (_, a, b) in enumerate(ch):
    out = f"parts/p{i:02d}.mov"; lst.append(f"file 'p{i:02d}.mov'")
    if os.path.exists(out): continue
    n = round((b - a) * 30); d = n / 30             # whole frames, and the sound cut to exactly the same length
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a}", "-i", "clip.mp4", "-frames:v", str(n),
        "-vf", f"crop={CW}:{CH}:{X0}:{Y0},{GRADE},scale=1404:2496:flags=lanczos,fps=30,format=yuv420p",
        "-af", f"atrim=duration={d:.6f},asetpts=PTS-STARTPTS,afade=t=in:d=0.015,afade=t=out:st={d-0.03:.4f}:d=0.03",
        "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-c:a", "pcm_s16le", "-ar", "48000", out], check=True)
open("parts/list.txt", "w").write("\n".join(lst))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "parts/list.txt", "-c", "copy", "cut.mov"], check=True)
# 2: the zooms, and 1.4 s held at the end for the end card
Z = ffexpr().replace("T", "t")
vf = (f"tpad=stop_mode=clone:stop_duration=1.4,scale=w='trunc(1080*({Z})/2)*2':h='trunc(1920*({Z})/2)*2':eval=frame:flags=lanczos,"
      f"crop=1080:1920:'(iw-1080)*0.5':'(ih-1920)*0.26',unsharp=5:5:0.3,setsar=1,format=yuv420p")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "cut.mov", "-vf", vf, "-af", "apad=pad_dur=1.4", "-shortest",
                "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-c:a", "pcm_s16le", "base.mov"], check=True)
print("base ok")
