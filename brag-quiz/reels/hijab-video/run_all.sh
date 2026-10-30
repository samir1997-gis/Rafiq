#!/bin/bash
# Every version: its pieces of the take → template base/plan → edit.py → zoom, masks, layers, mix (voice as recorded) → finish.sh (the pile-on
# in front, the end card) → check.py (the sound effects are there). One at a time.   run_all.sh WORK [vN ...]   (WORK/src.mov is the owner's video)
W=$1; shift; H=$(cd "$(dirname "$0")" && pwd); T=$H/../template; O=$H/../../out/hijab
declare -A PILE=([v1]=9.5 [v2]=7.5 [v3]=5.5) NAME=([v1]=full [v2]=short [v3]=shorter)
for v in ${@:-v1 v2 v3}; do
  rm -rf $W/$v; python3 $H/edit.py $W $v chunks || exit 1
  for st in "base nologo" plan; do (cd $T && python3 reel.py $W/$v $st > $W/$v/$(echo $st | cut -d' ' -f1).log 2>&1) || { echo "$v $st failed"; exit 1; }; done
  python3 $H/edit.py $W $v > $W/$v/edit.log 2>&1 || { echo "$v edit failed"; tail -5 $W/$v/edit.log; exit 1; }
  for st in zoom masks layers "mix keepvoice"; do (cd $T && python3 reel.py $W/$v $st >> $W/$v/render.log 2>&1) || { echo "$v $st failed"; tail -5 $W/$v/render.log; exit 1; }; done
  bash $H/finish.sh $W/$v ${PILE[$v]} $O/hijab-video-$v-${NAME[$v]}.mp4 && python3 $H/check.py $W/$v ${PILE[$v]} $O/hijab-video-$v-${NAME[$v]}.mp4; echo "$v finished $(date +%T)"
done
