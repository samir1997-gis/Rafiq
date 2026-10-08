# the speaker cut out, only on frames where a title sits behind him; other frames get an empty mask
import json, os, subprocess
from rembg import remove, new_session
from PIL import Image
C = json.load(open("config.json")); os.makedirs("frames", exist_ok=True); os.makedirs("mask", exist_ok=True)
subprocess.run(["ffmpeg","-v","error","-y","-i","base.mov","-vf","scale=540:960","-q:v","3","frames/%05d.jpg"], check=True)
s = new_session("u2net_human_seg"); blank = Image.new("L", (1080, 1920), 0)
N = len(os.listdir("frames"))
for i in range(N):
    t = i / 30; out = f"mask/{i:05d}.png"
    if os.path.exists(out): continue
    if any(a - .05 <= t < b + .05 for a, b, *_ in C["titles"]):
        m = remove(Image.open(f"frames/{i+1:05d}.jpg"), session=s, only_mask=True).resize((1080, 1920), Image.BILINEAR)
        m.save(out)
    else: blank.save(out)
print("masks", N)
