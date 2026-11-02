#!/bin/bash
# A finished Dajjāl video (#316): the intro (A or B: the clones and the rush-in, intro.py) + the template's reel.mp4 + the cream end card.
# The intro and the end card are brought DOWN to his reel's level, never his voice up (owner, 25 Oct 2026). Checks: loudness, frame 0.
#   finish.sh WORK RAW A|B OUT.mp4
set -e
W=$1; RAW=$2; V=$3; O=$4; H=$(cd "$(dirname "$0")" && pwd); E=$H/../../out/endcard/endcard-cream.mp4; I=$RAW/intro-$V.mov; R=$W/reel.mp4
lv() { ffmpeg -i "$1" -af ebur128 -f null - 2>&1 | sed -n '/Summary/,$p' | grep " I:" | awk '{print $2}'; }
GI=$(python3 -c "print(min(0, $(lv $R) - ($(lv $I))))"); GE=$(python3 -c "print(min(0, $(lv $R) - ($(lv $E))))")
ffmpeg -v error -y -i $I -i $R -ss 0.15 -i $E -filter_complex "[0:v]fps=30,format=yuv420p,setsar=1,setpts=PTS-STARTPTS[v0];[0:a]aresample=48000,aformat=channel_layouts=stereo,volume=${GI}dB,asetpts=PTS-STARTPTS[a0];[1:v]fps=30,format=yuv420p,setsar=1,setpts=PTS-STARTPTS[v1];[1:a]aresample=48000,aformat=channel_layouts=stereo,asetpts=PTS-STARTPTS[a1];[2:v]fps=30,scale=1080:1920,format=yuv420p,setsar=1,setpts=PTS-STARTPTS[v2];[2:a]aresample=48000,aformat=channel_layouts=stereo,volume=${GE}dB,asetpts=PTS-STARTPTS[a2];[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[v][ac];[ac]lowpass=f=16000:poles=2,aresample=192000,alimiter=limit=0.8:attack=1:release=60:level=false,aresample=48000[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 19 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart $O
echo "$(basename $O): $(ffprobe -v error -show_entries format=duration -of csv=p=0 $O) s, intro ${GI} dB, end card ${GE} dB, $(ffmpeg -i $O -af ebur128=peak=true -f null - 2>&1 | sed -n '/Summary/,$p' | grep -E ' I:|Peak:' | tr -s ' ' | tr '\n' ' ')"
python3 $H/../../check_frame0.py $O
