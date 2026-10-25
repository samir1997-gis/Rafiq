#!/bin/bash
# Rebuild every version from the take: assemble → template base/plan → edit.py → zoom, masks, layers, mix (voice as recorded) →
# finish.sh (end card at his level). One at a time: each step already uses every core.   run_all.sh WORK [vN ...]
W=$1; shift; H=$(cd "$(dirname "$0")" && pwd); T=$H/../template; O=$H/../../out/tomorrow
declare -A NAME=([v1]=start-tomorrow [v2]=dajjal [v3]=sun [v4]=send-us-back [v5]=shaytan)
for v in ${@:-v1 v2 v3 v4 v5}; do
  rm -rf $W/$v; python3 $H/assemble.py $W $v || exit 1
  for st in "base nologo dark tight" plan; do (cd $T && python3 reel.py $W/$v $st > $W/$v/$(echo $st | cut -d' ' -f1).log 2>&1) || { echo "$v $st failed"; exit 1; }; done
  python3 $H/edit.py $W $v > $W/$v/edit.log 2>&1 || { echo "$v edit failed"; tail -3 $W/$v/edit.log; exit 1; }
  for st in zoom masks layers "mix keepvoice"; do (cd $T && python3 reel.py $W/$v $st >> $W/$v/render.log 2>&1) || { echo "$v $st failed"; exit 1; }; done
  $H/finish.sh $W/$v $O/tomorrow-$v-${NAME[$v]}.mp4; echo "$v finished $(date +%T)"
done
