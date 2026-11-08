#!/usr/bin/env python3
"""Render a hyperframes composition without `hyperframes render`, which restarted this machine four times in a row on 8 Nov 2026 (#354): seek the GSAP timeline
frame by frame in one Chromium page (as `hyperframes snapshot` does), pipe JPEG screenshots to ffmpeg, then mix the
<audio> elements (data-start / data-duration / data-volume) with numpy and mux.

  python3 brag-quiz/framecap.py <composition dir> <out.mp4> [--fps 30] [--frames N]   (N: only the first N frames, for a speed test)
"""
import os, re, subprocess, sys, time
import numpy as np
from playwright.sync_api import sync_playwright

comp, out = sys.argv[1], sys.argv[2]
FPS = int(sys.argv[sys.argv.index("--fps") + 1]) if "--fps" in sys.argv else 30
LIMIT = int(sys.argv[sys.argv.index("--frames") + 1]) if "--frames" in sys.argv else None
html = open(os.path.join(comp, "index.html")).read()
DUR = float(re.search(r'data-composition-id="main"[^>]*data-duration="([\d.]+)"', html).group(1))
N = int(round(DUR * FPS)); N = min(N, LIMIT) if LIMIT else N
SR = 48000

def mix(path):
    n = int(DUR * SR) + SR; buf = np.zeros((n, 2), np.float32)
    for m in re.finditer(r'<audio[^>]*>', html):
        tag = m.group(0); g = lambda k: re.search(k + r'="([^"]*)"', tag)
        src, t0, d, v = g("src").group(1), float(g("data-start").group(1)), float(g("data-duration").group(1)), float(g("data-volume").group(1)) if g("data-volume") else 1.0
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(comp, src), "-t", f"{d:.3f}", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True).stdout
        x = np.frombuffer(raw, np.float32).reshape(-1, 2) * v; i = int(t0 * SR); j = min(n, i + len(x))
        if i < n: buf[i:j] += x[:j - i]
    buf = buf[:int(DUR * SR)]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_f32le", path], input=buf.tobytes(), check=True)

vid = out + ".video.mp4"
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                        "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-pix_fmt", "yuv420p", vid], stdin=subprocess.PIPE)
t_start = time.time()
with sync_playwright() as p:
    b = p.chromium.launch(args=["--disable-gpu"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.goto("file://" + os.path.abspath(os.path.join(comp, "index.html")))
    pg.wait_for_timeout(1500); assert pg.evaluate("!!(window.__timelines && window.__timelines.main) && document.fonts.status === 'loaded'")
    pg.evaluate("document.querySelectorAll('audio').forEach(a => a.muted = true)")
    for k in range(N):
        pg.evaluate(f"void window.__timelines.main.seek({k / FPS:.5f}, false)")
        enc.stdin.write(pg.screenshot(type="jpeg", quality=93))
        if k % 150 == 0: print(f"frame {k}/{N}  {time.time() - t_start:.0f}s", flush=True)
    b.close()
enc.stdin.close(); enc.wait()
print(f"video done: {N} frames in {time.time() - t_start:.0f}s", flush=True)
if LIMIT: sys.exit(0)
wav = out + ".audio.wav"; mix(wav)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vid, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", out], check=True)
os.remove(vid); os.remove(wav); print("done", out)
