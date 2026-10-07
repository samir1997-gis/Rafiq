import subprocess
E = [("whoosh",0.0,.5),("boom",0.04,.8),("swish",1.8,.4),("ping",2.44,.5),("whoosh",2.7,.45)] + [("tick",2.76+i*.06,.35) for i in range(6)] + [
 ("boom",4.86,.85),("whoosh",5.25,.5),("bell",6.38,.4),("swish",6.42,.4),("whoosh",6.55,.45),("whoosh",7.1,.45),("pop",8.38,.6),
 ("swish",8.9,.45),("ping",8.86,.4),("tick",8.88,.3),("swish",11.24,.45),("whoosh",13.88,.5),("ping",13.86,.35),("tick",13.9,.3),
 ("swish",14.9,.45),("pop",17.54,.6),("swish",17.6,.5),("ping",17.4,.35),("tick",17.42,.3),("swish",18.76,.45),("pop",20.95,.5),("ping",20.92,.35),
 ("whoosh",22.5,.5),("ping",22.5,.35),("tick",22.52,.3),("swish",23.54,.45),("swish",26.98,.5),("ping",26.9,.35),("tick",26.92,.3),("swish",28.22,.45),
 ("whoosh",28.5,.45),("boom",28.72,.6),("boom",30.98,.5),("ping",31.0,.35),("tick",31.02,.3),("swish",32.32,.45)] + [
 ("tick",32.4+i*.11,.45) for i in range(6)] + [("ping",32.96,.45),("boom",34.4,.6),("pop",35.0,.6),("ding",35.46,.55),("whoosh",35.95,.5),("ding",36.35,.45)]
args = ["ffmpeg","-v","error","-y","-i","base.mov","-framerate","30","-i","ov/%05d.png"]
for n,_,_ in E: args += ["-i", f"sfx/{n}.wav"]
fc = ["[0:v][1:v]overlay=0:0:format=auto:shortest=1,format=yuv420p[v]",
      "[0:a]aresample=48000,aformat=channel_layouts=stereo,highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=120:makeup=5dB,asplit=2[voice][sc]"]
lab = []
for i,(n,t,v) in enumerate(E):
    ms = int(t*1000); fc.append(f"[{i+2}:a]volume={v},adelay={ms}|{ms}[s{i}]"); lab.append(f"[s{i}]")
fc.append("".join(lab) + f"amix=inputs={len(lab)}:normalize=0,apad[sfx]")
fc.append("[sfx][sc]sidechaincompress=threshold=0.04:ratio=5:attack=8:release=250:makeup=1[duck]")
fc.append("[voice][duck]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,volume=3dB,alimiter=limit=0.89:level=false[a]")
args += ["-filter_complex", ";".join(fc), "-map","[v]","-map","[a]","-c:v","libx264","-crf","18","-preset","slow","-profile:v","high",
         "-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-movflags","+faststart","darasa-edit.mp4"]
subprocess.run(args, check=True); print("ok")
