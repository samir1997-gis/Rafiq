#!/bin/bash
# The finished version: the template's reel.mp4 + the owner's end card, the end card brought DOWN to the reel's own level
# (a peak catch at -1 dBFS, nothing raised; the owner's voice is never raised: "don't increase the audio", 25 Oct 2026). Checks: loudness, frame 0, silences.
#   finish.sh WORK/vN OUT.mp4
set -e
R=$1/reel.mp4; O=$2; E=$(dirname "$0")/../../out/endcard/endcard-cream.mp4
lv() { ffmpeg -i "$1" -af ebur128 -f null - 2>&1 | sed -n '/Summary/,$p' | grep " I:" | awk '{print $2}'; }
G=$(python3 -c "print(min(0, $(lv $R) - ($(lv $E))))")
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $R)
ffmpeg -v error -y -i $R -ss 0.15 -i $E -filter_complex "[0:v]fps=30,format=yuv420p,setpts=PTS-STARTPTS[v0];[0:a]aresample=48000,asetpts=PTS-STARTPTS[a0];[1:v]fps=30,format=yuv420p,setpts=PTS-STARTPTS[v1];[1:a]aresample=48000,volume=${G}dB,asetpts=PTS-STARTPTS[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][ac];[ac]aresample=192000,alimiter=limit=0.89:attack=1:release=60:level=false,aresample=48000[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 19 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart $O
echo "$(basename $O): $(ffprobe -v error -show_entries format=duration -of csv=p=0 $O) s, end card ${G} dB, $(ffmpeg -i $O -af ebur128=peak=true -f null - 2>&1 | sed -n '/Summary/,$p' | grep -E ' I:|Peak:' | tr -s ' ' | tr '\n' ' ')"
python3 $(dirname "$0")/../../check_frame0.py $O
