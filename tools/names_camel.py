#!/usr/bin/env python3
"""The learner's name in Arabic (#169): does CAMeL Tools know each name, and do our vowel marks match
one of its readings? Run: python3 tools/names_camel.py"""
import json, subprocess, re
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer
from camel_tools.utils.dediac import dediac_ar
src = open("basics-data.js", encoding="utf8").read()
N = json.loads(subprocess.run(["node"], input=src + "\nprocess.stdout.write(JSON.stringify(BASICS_NAMES))", capture_output=True, text=True, check=True).stdout)
an = Analyzer(MorphologyDB.builtin_db(), backoff="NONE")
strip_end = lambda d: re.sub(r"[ً-ْ]+$", "", d)          # names at a pause: no case ending
unknown, differ = [], []
for ar in sorted(set(N.values())):
    words = ar.split()
    for w in words:
        a = an.analyze(dediac_ar(w))
        if not a: unknown.append(ar); break
        mine = strip_end(w.replace("َّ", "َّ").replace("ِّ", "ِّ"))
        forms = {strip_end(x["diac"].replace("َّ", "َّ").replace("ِّ", "ِّ")) for x in a}
        if len(words) == 1 and mine not in forms: differ.append((ar, sorted(forms)[:4])); break
print(f"{len(set(N.values()))} names; unknown to CAMeL: {len(unknown)}; vowels differ from all CAMeL readings: {len(differ)}")
for u in unknown: print("  unknown:", u)
for ar, f in differ: print("  differs:", ar, "  CAMeL:", " / ".join(f))
