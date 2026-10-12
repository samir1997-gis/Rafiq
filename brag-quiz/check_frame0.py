#!/usr/bin/env python3
"""Fail any video whose first frame is (nearly) empty: the first frame is the cover and what stops the scroll.
q4-azim opened on a blank screen and most TikTok viewers left at 0:01 (12 Oct 2026); 12 of 23 scheduled videos did the same.

  python3 brag-quiz/check_frame0.py video.mp4 [...]     exit 1 if any first frame is blank
"""
import subprocess, sys
from PIL import Image, ImageStat

def ink(path):
    """Share of the first frame that differs clearly from the background (text, a word, a face)."""
    png = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-frames:v", "1", "-vf", "scale=270:-1,format=gray", "-f", "image2pipe",
                          "-vcodec", "png", "-"], capture_output=True, check=True).stdout
    from io import BytesIO
    im = Image.open(BytesIO(png)); bg = ImageStat.Stat(im).median[0]
    px = im.tobytes(); return sum(abs(p - bg) > 60 for p in px) / len(px)

bad = 0
for f in sys.argv[1:]:
    s = ink(f); ok = s >= 0.004
    print(f"{'ok  ' if ok else 'BLANK'} {s * 100:5.2f}% ink  {f}"); bad += not ok
sys.exit(1 if bad else 0)
