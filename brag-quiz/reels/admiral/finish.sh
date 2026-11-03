#!/bin/bash
# The finished h8-admiral: the render + the cream end card (brought DOWN to the reel's level, never the reel up), levelled to -16 LUFS
# (two-pass loudnorm), then checked: frame 0, loudness, silences.   finish.sh  →  brag-quiz/out/h8-admiral/h8-admiral-master.mp4
set -e
H=$(cd "$(dirname "$0")" && pwd); R=$H/out/raw.mp4; E=$H/../../out/endcard/endcard-cream.mp4; O=$H/../../out/h8-admiral; mkdir -p $O
lv() { ffmpeg -i "$1" -af ebur128 -f null - 2>&1 | sed -n '/Summary/,$p' | grep " I:" | awk '{print $2}'; }
GE=$(python3 -c "print(min(0, $(lv $R) - ($(lv $E))))")
ffmpeg -v error -y -i $R -ss 0.15 -i $E -filter_complex "[0:v]fps=30,format=yuv420p,setsar=1,setpts=PTS-STARTPTS[v0];[0:a]aresample=48000,aformat=channel_layouts=stereo,asetpts=PTS-STARTPTS[a0];[1:v]fps=30,scale=1080:1920,format=yuv420p,setsar=1,setpts=PTS-STARTPTS[v1];[1:a]aresample=48000,aformat=channel_layouts=stereo,volume=${GE}dB,asetpts=PTS-STARTPTS[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 12 -preset slow -pix_fmt yuv420p -c:a pcm_s16le $O/joined.mov
J=$(ffmpeg -i $O/joined.mov -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g() { echo "$J" | python3 -c "import json,sys; print(json.load(sys.stdin)['$1'])"; }
ffmpeg -v error -y -i $O/joined.mov -af "loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aresample=48000" \
  -c:v copy -c:a aac -b:a 192k -movflags +faststart $O/h8-admiral-master.mp4
rm $O/joined.mov
F=$O/h8-admiral-master.mp4
echo "end card ${GE} dB; $(ffprobe -v error -show_entries format=duration -of csv=p=0 $F) s; $(ffmpeg -i $F -af ebur128=peak=true -f null - 2>&1 | sed -n '/Summary/,$p' | grep -E ' I:|Peak:' | tr -s ' ' | tr '\n' ' ')"
echo "silences: $(ffmpeg -i $F -af silencedetect=n=-50dB:d=0.25 -f null - 2>&1 | grep -c silence_start)"
python3 $H/../../check_frame0.py $F
