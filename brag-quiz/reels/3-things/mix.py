import subprocess, json
C = json.load(open("config.json")); S = "/tmp/claude-0/edit2/user_sfx/"
PK = {2: .25, 11: .23, 10: .22}
E = [(2, a + .05, .16) for a, *_ in C["titles"][1:]]                 # a soft whoosh as each title rises
E += [(11, C["split"][0] + .05, .2), (7, C["flick"][0], .16), (4, C["titles"][-1][0] + .1, .2)]
args = ["ffmpeg","-v","error","-y","-i","base.mov","-framerate","30","-i","back/%05d.png","-framerate","30","-i","mask/%05d.png","-framerate","30","-i","front/%05d.png"]
for n, _, _ in E: args += ["-i", f"{S}n{n:02d}.wav"]
fc = ["[0:v]split=2[v0][v1]", "[v0][1:v]overlay=0:0:format=auto[bb]", "[2:v]format=gray[m]", "[v1][m]alphamerge[fg]",
      "[bb][fg]overlay=0:0:format=auto[c]", "[c][3:v]overlay=0:0:format=auto,format=yuv420p[v]",
      "[0:a]aresample=48000,aformat=channel_layouts=stereo,highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=150:makeup=4dB,asplit=2[voice][sc]"]
lab = []
for i, (n, t, v) in enumerate(E):
    ms = int(max(0, t - PK.get(n, 0)) * 1000); fc.append(f"[{i+4}:a]volume={v},adelay={ms}|{ms}[s{i}]"); lab.append(f"[s{i}]")
fc.append("".join(lab) + f"amix=inputs={len(lab)}:normalize=0,apad[sfx]")
fc.append("[sfx][sc]sidechaincompress=threshold=0.04:ratio=5:attack=8:release=250[duck]")
fc.append("[voice][duck]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,alimiter=limit=0.89:level=false[a]")
args += ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "19", "-preset", "slow", "-maxrate", "8M", "-bufsize", "16M",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "learn-arabic-3-things.mp4"]
subprocess.run(args, check=True); print("ok")
