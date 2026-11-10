#!/usr/bin/env python3
"""Pack a week's schedule for Metricool (owner, 10 Nov 2026: "i will add these to metricool"): one folder per post, numbered in
posting order, each with its slides (4:5 JPEGs, 1080×1350, numbered in order: one Metricool post can go to TikTok and Instagram,
which only takes 4:5 to 1.91:1 in a carousel) or the video, and caption.txt (when, where, the caption). Then one zip.

  python3 brag-quiz/schedule/pack_metricool.py brag-quiz/schedule/2026-11-10.json <out dir> [--videos]   (--videos: the mp4s in the zip too)
"""
import json, os, re, shutil, sys, unicodedata, zipfile
from PIL import Image
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
plan, out = json.load(open(sys.argv[1])), sys.argv[2]
week = os.path.join(out, "Rafiq week " + os.path.basename(sys.argv[1])[:10]); shutil.rmtree(week, ignore_errors=True); os.makedirs(week)
safe = lambda s: re.sub(r" +", " ", re.sub(r"[^A-Za-z0-9,.-]+", " ", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode())).strip(" ,.-")
for n, p in enumerate(plan, 1):
    d = os.path.join(week, f"{n:02d} {p['day'][:3]} {p['day'][4:]} {p['time'].replace(':', '.')} - {safe(p['what'])}"[:90]); os.makedirs(d)
    if p["kind"].startswith("carousel"):
        src = os.path.join(HERE, "stills", p["id"] + "-pop")
        files = sorted((f for f in os.listdir(src) if f[0] != "_"), key=lambda f: int(re.findall(r"(\d+)\.\w+$", f)[0]))
        for k, f in enumerate(files, 1):
            Image.open(os.path.join(src, f)).convert("RGB").save(os.path.join(d, f"{n:02d}-{p['id']}-{k:02d}.jpg"), quality=92)
        what = f"Carousel, {len(files)} slides, in order (01 first). 4:5 JPEGs: post to TikTok and Instagram together."
    elif "--videos" in sys.argv:
        shutil.copy(os.path.join(HERE, p["file"]), os.path.join(d, f"{n:02d}-{p['id']}.mp4"))
        what = "Video, 9:16. Instagram takes it as a Reel."
    else:                                                        # the videos are big: they're sent on their own, so the zip stays small
        what = f"Video: {os.path.basename(p['file'])} (sent on its own). 9:16; Instagram takes it as a Reel."
    open(os.path.join(d, "caption.txt"), "w").write(f"{p['day']} 2026, {p['time']} UK time\n{what}\n" + ("Link post: free week, link in bio.\n" if p["link"] else "") + f"\n{p['caption']}\n")
z = week + ".zip"
with zipfile.ZipFile(z, "w", zipfile.ZIP_STORED) as zf:
    for root, _, fs in os.walk(week):
        for f in sorted(fs): zf.write(os.path.join(root, f), os.path.relpath(os.path.join(root, f), out))
print(z, round(os.path.getsize(z) / 1e6, 1), "MB"); print("\n".join(sorted(os.listdir(week))))
