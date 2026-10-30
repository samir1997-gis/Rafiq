#!/bin/bash
# A finished version: the pile-on (its first P seconds, cut dead while it builds) + the template's reel.mp4 + the owner's end card.
# The pile-on and the end card are brought DOWN to his reel's level (his voice is never raised: owner, 25 Oct 2026). Checks: loudness, frame 0.
#   finish.sh WORK/vN P OUT.mp4
set -e
R=$1/reel.mp4; P=$2; O=$3; H=$(cd "$(dirname "$0")" && pwd); A=$H/../../out/hijab/hijab-pileon-anim.mp4; E=$H/../../out/endcard/endcard-cream.mp4
lv() { ffmpeg -i "$1" -af ebur128 -f null - 2>&1 | sed -n '/Summary/,$p' | grep " I:" | awk '{print $2}'; }
ffmpeg -v error -y -i $A -t $P -c:v libx264 -crf 16 -c:a pcm_s16le $1/pile.mov
GP=$(python3 -c "print(min(0, $(lv $R) + 1 - ($(lv $1/pile.mov))))"); GE=$(python3 -c "print(min(0, $(lv $R) - ($(lv $E))))")
ffmpeg -v error -y -i $1/pile.mov -i $R -ss 0.15 -i $E -filter_complex "[0:v]fps=30,format=yuv420p,setsar=1,setpts=PTS-STARTPTS[v0];[0:a]aresample=48000,aformat=channel_layouts=stereo,volume=${GP}dB,asetpts=PTS-STARTPTS[a0];[1:v]fps=30,format=yuv420p,setsar=1,setpts=PTS-STARTPTS[v1];[1:a]aresample=48000,aformat=channel_layouts=stereo,asetpts=PTS-STARTPTS[a1];[2:v]fps=30,scale=1080:1920,format=yuv420p,setsar=1,setpts=PTS-STARTPTS[v2];[2:a]aresample=48000,aformat=channel_layouts=stereo,volume=${GE}dB,asetpts=PTS-STARTPTS[a2];[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[v][ac];[ac]lowpass=f=16000:poles=2,aresample=192000,alimiter=limit=0.8:attack=1:release=60:level=false,aresample=48000[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 19 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart $O
echo "$(basename $O): $(ffprobe -v error -show_entries format=duration -of csv=p=0 $O) s, pile-on ${GP} dB, end card ${GE} dB, $(ffmpeg -i $O -af ebur128=peak=true -f null - 2>&1 | sed -n '/Summary/,$p' | grep -E ' I:|Peak:' | tr -s ' ' | tr '\n' ' ')"
python3 $H/../../check_frame0.py $O
