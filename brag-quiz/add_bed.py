"""Put the fountain bed under a finished video that was built without it, then bring it to -16 LUFS.

The picture is copied as it is; the bed is mixed exactly as build_teach.Comp.write does it
(two copies crossfaded, from the first frame), at the level it sits at in those renders:
about -30 dB RMS in the gaps once levelled (r3-akbar, q3-sujood, w8-subhana-azim).

  python3 brag-quiz/add_bed.py i4-ta-marbuta m08-day1 m05-typing p2-ana
"""
import os, subprocess, sys
import build_teach as T

BED = 0.65  # linear gain on the +6 dB fountain; 0.1 (the composition's data-volume) comes out far too soft when mixed with ffmpeg

def add_bed(vid):
    src = os.path.join(T.HERE, "out", vid, vid + ".mp4"); tmp = src + ".bed.mp4"
    total = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                                 capture_output=True, text=True, check=True).stdout)
    f = os.path.join(T.V6, "sfx-gen/fountain.mp3")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-i", f, "-i", f, "-filter_complex",
                    f"[1][2]acrossfade=d=2:c1=tri:c2=tri,volume=6dB,atrim=0:{total:.2f},afade=t=in:d=0.3,"
                    f"afade=t=out:st={total - 1.4:.2f}:d=1.4,volume={BED}[bed];[0:a][bed]amix=inputs=2:normalize=0:duration=first[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", tmp], check=True)
    os.replace(tmp, src)
    for _ in range(3): gain(src)       # a plain gain to -16 LUFS (loudnorm's dynamic mode would lift the bed in the gaps), peaks limited

def lufs(f):
    m = subprocess.run(["ffmpeg", "-hide_banner", "-i", f, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(m[m.rindex("I:"):].split()[1])

def gain(src):
    d = -16.0 - lufs(src)
    if abs(d) < 0.3: return
    tmp = src + ".lvl.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-af", f"volume={d:.2f}dB,alimiter=limit=0.7:level=false",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, src)

if __name__ == "__main__":
    for vid in sys.argv[1:]: add_bed(vid)
