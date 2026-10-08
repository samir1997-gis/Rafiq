import subprocess
PK = {2: .25, 3: .44, 11: .23, 10: .22}            # where each whoosh/impact peaks, so the peak lands on the moment
# (sound, moment, volume, take only this many seconds or None)
E = [(2,0.0,.35,None),(5,2.44,.3,None),(1,2.76,.18,1.6),(3,4.86,.45,None),(6,5.3,.22,1.0),(10,6.6,.25,None),(4,7.15,.35,None),
     (5,8.38,.3,None),(10,8.9,.25,None),(9,9.0,.25,.3),(8,9.02,.3,None),(10,11.24,.25,None)]
for t in (14.02, 17.54, 22.64, 27.0, 31.14):                   # each card: arrives, word sparkles, its tracker chip lights
    E += [(11,t,.3,None),(8,t+.06,.3,None),(9,t+.02,.25,.3)]
E += [(10,14.9,.25,None),(10,18.76,.25,None),(5,21.08,.3,None),(10,23.54,.25,None),(10,28.22,.25,None),(11,28.86,.35,None),
      (10,32.32,.25,None),(7,32.4,.3,None),(8,32.96,.3,None),(5,34.4,.3,None),(4,36.0,.35,None)]
args = ["ffmpeg","-v","error","-y","-i","base.mov","-framerate","30","-i","ov/%05d.png"]
for n,_,_,_ in E: args += ["-i", f"user_sfx/n{n:02d}.wav"]
fc = ["[0:v][1:v]overlay=0:0:format=auto:shortest=1,format=yuv420p[v]",
      "[0:a]aresample=48000,aformat=channel_layouts=stereo,highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=120:makeup=5dB,asplit=2[voice][sc]"]
lab = []
for i,(n,t,v,d) in enumerate(E):
    t0 = max(0, t - PK.get(n, 0)); ms = int(t0*1000)
    cut = f"atrim=0:{d},afade=t=out:st={d-.12:.2f}:d=0.12," if d else ""
    fc.append(f"[{i+2}:a]{cut}volume={v},adelay={ms}|{ms}[s{i}]"); lab.append(f"[s{i}]")
fc.append("".join(lab) + f"amix=inputs={len(lab)}:normalize=0,apad[sfx]")
fc.append("[sfx][sc]sidechaincompress=threshold=0.04:ratio=5:attack=8:release=250[duck]")
fc.append("[voice][duck]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,alimiter=limit=0.89:level=false[a]")
args += ["-filter_complex",";".join(fc),"-map","[v]","-map","[a]","-c:v","libx264","-crf","20","-preset","slow","-maxrate","6M","-bufsize","12M",
         "-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-movflags","+faststart","darasa-reel-A.mp4"]
subprocess.run(args, check=True); print("ok", len(E), "sounds")
