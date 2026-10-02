# The owner's three trimmed ads (#195): the talking-head voice made crisper and both parts levelled to -15 LUFS.
# Run in the folder with a-trim.mp4, b-trim.mp4, c-trim.mp4 (the intro ends at 14.67, 14.23 and 15.87 s).
# Measured: voice 75-83% of energy at 150-500 Hz and under 1% at 2-5 kHz, 8-12 LU quieter than the app part.
# Owner's voice (the intro) made crisper; the app part untouched apart from level. Picture copied as it is.
import subprocess, json, sys
VOICE = ("highpass=f=90,afftdn=nr=10:nf=-40,"
         "equalizer=f=250:t=o:w=1.2:g=-5,equalizer=f=450:t=o:w=1:g=-2,"   # less boxy
         "equalizer=f=3200:t=o:w=1.2:g=5,equalizer=f=6500:t=o:w=1:g=3,"   # clarity and a little air
         "acompressor=threshold=-24dB:ratio=3:attack=5:release=90:makeup=3") # evens out the level
def lufs(f, af):
    out = subprocess.run(["ffmpeg","-hide_banner","-i",f,"-vn","-af",af+",loudnorm=print_format=json","-f","null","-"],capture_output=True,text=True).stderr
    return float(json.loads(out[out.rindex("{"):])["input_i"])
TARGET = -15.0     # where Instagram and TikTok play things (about -14), with room for the limiter
for n, T in [("a", 14.67), ("b", 14.23), ("c", 15.87)]:
    f = f"{n}-trim.mp4"
    gi = TARGET - lufs(f, f"atrim=0:{T},{VOICE}")
    ga = TARGET - lufs(f, f"atrim={T}")
    fc = (f"[0:a]atrim=0:{T},asetpts=PTS-STARTPTS,{VOICE},volume={gi:.2f}dB[i];"
          f"[0:a]atrim={T},asetpts=PTS-STARTPTS,volume={ga:.2f}dB[r];"
          f"[i][r]acrossfade=d=0.03:c1=tri:c2=tri,alimiter=limit=0.84:level=false[a]")
    subprocess.run(["ffmpeg","-loglevel","error","-y","-i",f,"-filter_complex",fc,"-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","192k","-movflags","+faststart",f"{n}-crisp.mp4"],check=True)
    print(n, f"voice {gi:+.1f} dB, app {ga:+.1f} dB")
