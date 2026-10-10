import subprocess, json, re
C = json.load(open("config.json")); S = "/tmp/claude-0/edit2/user_sfx/"
# 1. the voice: noise out first, then a gentle compressor, pauses kept quiet; measure, then set to -14 LUFS without pumping
CLEAN = "highpass=f=80,lowpass=f=13000,afftdn=nr=18:nf=-66:tn=1,agate=threshold=0.003:ratio=2.5:range=0.15:attack=6:release=220,acompressor=threshold=-28dB:ratio=2:attack=12:release=220"
subprocess.run(["ffmpeg","-v","error","-y","-i","base.mov","-vn","-af",CLEAN,"-ar","48000","-ac","2","voice_clean.wav"], check=True)
m = subprocess.run(["ffmpeg","-i","voice_clean.wav","-af","ebur128","-f","null","-"],capture_output=True,text=True).stderr
I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", m)[-1]); gain = -14.5 - I; print("voice", I, "LUFS -> gain", round(gain, 1), "dB")
# 2. the picture: on each stressed word the scene (you + the titles) punches in, holds, and eases back; captions stay put
def env(a, b):
    u = f"clip((t-{a})/0.1,0,1)"; d = f"clip(({b}+0.6-t)/0.35,0,1)"; m = f"min({u},{d})"
    return f"({m})*({m})*(3-2*({m}))"
Z = "1+0.1*(" + "+".join(env(a, b) for a, b in C["punch"]) + ")"
PK = {2: .25, 11: .23}
E = [(2, a + .05, .1) for a, *_ in C["titles"][1:]] + [(11, C["split"][0] + .05, .12), (7, C["flick"][0], .1), (4, C["titles"][-1][0] + .1, .12)]
args = ["ffmpeg","-v","error","-y","-i","base.mov","-framerate","30","-i","back/%05d.png","-framerate","30","-i","mask/%05d.png","-framerate","30","-i","front/%05d.png","-i","voice_clean.wav"]
for n, _, _ in E: args += ["-i", f"{S}n{n:02d}.wav"]
fc = ["[0:v]split=2[v0][v1]", "[v0][1:v]overlay=0:0:format=auto[bb]", "[2:v]format=gray[m]", "[v1][m]alphamerge[fg]",
      "[bb][fg]overlay=0:0:format=auto,format=yuv420p[sc]",
      f"[sc]scale=w='trunc(1080*({Z})/2)*2':h='trunc(1920*({Z})/2)*2':eval=frame:flags=lanczos,crop=1080:1920:'(iw-1080)*0.5':'(ih-1920)*0.33'[zs]",
      "[zs][3:v]overlay=0:0:format=auto,format=yuv420p[v]",
      f"[4:a]volume={gain:.2f}dB,asplit=2[voice][sc2]"]
lab = []
for i, (n, t, v) in enumerate(E):
    ms = int(max(0, t - PK.get(n, 0)) * 1000); fc.append(f"[{i+5}:a]volume={v},adelay={ms}|{ms}[s{i}]"); lab.append(f"[s{i}]")
fc.append("".join(lab) + f"amix=inputs={len(lab)}:normalize=0,apad[sfx]")
fc.append("[sfx][sc2]sidechaincompress=threshold=0.03:ratio=6:attack=8:release=300[duck]")
fc.append("[voice][duck]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.85:level=false[a]")
args += ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "21", "-preset", "slow", "-maxrate", "4.2M", "-bufsize", "8M",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "learn-arabic-3-things-v2.mp4"]
subprocess.run(args, check=True); print("ok")
