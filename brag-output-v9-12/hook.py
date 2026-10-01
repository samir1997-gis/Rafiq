"""Put the owner's filmed hook in front of a demo video, for the ads (#160).

  python3 brag-output-v9-12/hook.py HOOK.mov[,MORE.mov,...] DEMO.mp4 OUT.mp4 CUTS.json

Several clips (comma-separated) are joined in that order first; the times in CUTS.json are then on the
joined timeline (clip 2 starts where clip 1 ends).

CUTS.json says which parts of the hook to keep and the captions:
  {"keep": [[0.62, 9.25], [10.40, 18.20]],     # seconds in the hook; every other part is punched in a little
   "zoom": 1.08,
   "demo_from": 0.5,                             # optional: skip the demo's first moments (its blank opening frame)
   "captions": [[0.70, 2.26, "I spent {26 years}"], ...]}   # hook times; {braces} are highlighted

The hook's phone footage (4K, any rotation) becomes 1080x1920 at 30 fps like the demos, its sound is
brought to the demos' loudness, the captions are burned in (Karla, like the app), and the demo follows
straight on. Also writes OUT-hook.mp4, the hook on its own. The filmed clips themselves aren't committed
(the repo is public).
"""
import json, os, re, subprocess, sys, tempfile

FONTS = os.environ.get("HOOK_FONTS", os.path.join(os.path.dirname(__file__), "fonts"))

def ass(captions, keep):
    def out(t):                                   # hook time -> time in the cut hook
        done = 0.0
        for a, b in keep:
            if t < b: return done + max(0.0, t - a)
            done += b - a
        return done
    ts = lambda s: "%d:%02d:%05.2f" % (s // 3600, s % 3600 // 60, s % 60)
    lines = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "",
             "[V4+ Styles]",
             "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
             "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
             # white, with a dark ink outline and soft shadow; bottom centre, low on the screen but just above the
             # strip Reels and TikTok cover with the username and caption; CAP_BOTTOM moves it (pixels up from the bottom)
             "Style: Cap,Karla ExtraBold,96,&H00FFFFFF,&H00FFFFFF,&H002B2617,&H64000000,0,0,0,0,100,100,0,0,1,7,3,2,80,80,%d,1"
             % int(os.environ.get("CAP_BOTTOM", 260)),
             "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    for a, b, text in captions:
        text = re.sub(r"\{([^}]*)\}", r"{\\c&H4CB6E8&}\1{\\c&HFFFFFF&}", text)   # highlight: warm gold
        lines.append("Dialogue: 0,%s,%s,Cap,,0,0,0,,{\\fscx86\\fscy86\\t(0,140,\\fscx100\\fscy100)}%s"
                     % (ts(out(a)), ts(out(b)), text))
    return "\n".join(lines) + "\n"

def main(hook, demo, out, cuts):
    c = json.load(open(cuts))
    keep, zoom = c["keep"], c.get("zoom", 1.0)
    tmp = tempfile.mkdtemp()
    # first, one pass down from 4K (a little above 1080p, so the punch-in stays sharp): editing 4K directly runs out of memory
    mezz = os.path.join(tmp, "hook.mp4")
    clips = hook.split(",")
    join = "".join(f"[{i}:v]scale=1296:2304:flags=lanczos,fps=30,setsar=1[v{i}];[{i}:a]aresample=48000[a{i}];" for i in range(len(clips)))
    join += "".join(f"[v{i}][a{i}]" for i in range(len(clips))) + f"concat=n={len(clips)}:v=1:a=1[v][a]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *sum((["-i", c] for c in clips), []), "-filter_complex", join,
                    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "fast", "-crf", "14", "-c:a", "pcm_s16le", "-f", "mov", mezz],
                   check=True)
    hook = mezz
    open(os.path.join(tmp, "caps.ass"), "w").write(ass(c["captions"], keep))
    parts, f = [], []
    for i, (a, b) in enumerate(keep):
        z = zoom if i % 2 else 1.0                # in, out, in: each jump cut changes the framing
        f.append(f"[s{i}]trim={a}:{b},setpts=PTS-STARTPTS,crop=iw/{z}:ih/{z}:(iw-iw/{z})/2:(ih-ih/{z})*0.4,"
                 f"scale=1080:1920:flags=lanczos,fps=30,setsar=1[v{i}];"
                 f"[t{i}]atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000[a{i}];")
        parts.append(f"[v{i}][a{i}]")
    n = len(keep)
    f.insert(0, f"[0:v]split={len(keep)}" + "".join(f"[s{i}]" for i in range(len(keep))) + ";"
                + f"[0:a]asplit={len(keep)}" + "".join(f"[t{i}]" for i in range(len(keep))) + ";")
    f.append("".join(parts) + f"concat=n={n}:v=1:a=1[hv][ha0];")
    f.append(f"[hv]subtitles={tmp}/caps.ass:fontsdir={FONTS}[hvc];")
    total = sum(b - a for a, b in keep)
    f.append(f"[ha0]highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,afade=t=out:st={total - 0.12:.2f}:d=0.12[ha];")
    hook_only = out.replace(".mp4", "-hook.mp4")
    enc = ["-c:v", "libx264", "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", hook, "-filter_complex", "".join(f).rstrip(";"),
                    "-map", "[hvc]", "-map", "[ha]", *enc, hook_only], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", hook_only, "-ss", str(c.get("demo_from", 0)), "-i", demo, "-filter_complex",
                    "[0:v]fps=30,setsar=1[a];[1:v]fps=30,scale=1080:1920,setsar=1[b];[1:a]aresample=48000[ba];"
                    "[a][0:a][b][ba]concat=n=2:v=1:a=1[v][au]", "-map", "[v]", "-map", "[au]", *enc, out], check=True)
    print(out, "and", hook_only)

if __name__ == "__main__":
    main(*sys.argv[1:5])
