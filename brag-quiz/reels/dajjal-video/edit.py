#!/usr/bin/env python3
"""The owner's Dajjāl take (2 Nov 2026, #316): "edit all the mistakes out and all the spaces where I was reading the script on my phone".
clip.mp4 = 1059 (the first 103 s: "Let me explain", the root, the camels) + 1107 (the rest), joined. SPANS is the best take of each line
(times in the joined clip, from words.json); inside each, true silences (the phone pauses) come out as the template's cut does
(-40 dB, 0.4 s+, a 0.12 s breath kept). Dropped: restarts and stumbles, "like a verb" (dajjāl is an intensive noun form, not a verb),
the first "al-Masīḥ ibn ad-Dajjāl" (he corrects it), "Yeah", "making it look,".

  python3 edit.py WORK chunks     → WORK/chunks.json, then the template's base (reel.py WORK base nologo)
"""
import json, os, re, subprocess, sys
W = sys.argv[1]
SPANS = [
    (26.0, 28.4),     # Let me explain. (take 1, finger up)
    (40.1, 47.5),     # The word dajjāl comes from the root dāl, jīm, lām.
    (58.5, 62.95),    # Dajjala, which means to cover or coat something.
    (111.2, 115.07),  # The Arabs used it for coating a sick camel with tar
    (116.72, 117.92), # to hide what was underneath (his second go: the first "to hide what was" trailed off)
    (140.1, 144.3),   # and for painting gold over something cheap to make it look more precious
    (169.68, 172.15), # The dajjāl is the strongest form of the word (after a false start: "and the dajjāl is this… and the…")
    (173.45, 186.95), # so the dajjāl isn't just a liar, the dajjāl is a master liar … like a manipulator or a fraudster.
    (203.7, 210.85),  # Someone who covers the truth with something shiny to make it look appealing again and again and again.
    (226.2, 233.4),  # So, by that meaning, anyone could be a dajjāl, there could be hundreds, even thousands living amongst us.
    (241.5, 248.7),  # The Prophet ﷺ even said that the Hour will not pass until…
    (256.6, 261.9),  # 30 dajjāls appear, liars, each claiming to have prophethood,
    (282.5, 285.45),  # But there is one who is the greatest of them all,
    (288.45, 290.95), # al-Masīḥ ad-Dajjāl.
    (308.5, 327.85),  # And his lies … his fire is paradise and his paradise is fire.
    (359.7, 363.75),  # He literally paints Jahannam with gold,
    (365.25, 368.3), # making it appear like paradise.
    (409.65, 432.2),  # But Allah ﷻ did not leave us without clues … identify it. And that's the important thing here: … your faith.
    (460.2, 476.6),   # And the Prophet ﷺ said … the first 10 ayat of Sūrat al-Kahf … Send this to someone … from the dajjāl.
]
SLOW = [(44.0, 47.7)]                                  # "dāl… jīm… lām": his pauses between the letters are part of it (0.45 s, not 0.28)
os.chdir(W)
if not os.path.exists("audio.wav"):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "clip.mp4", "-vn", "-ac", "1", "-ar", "16000", "audio.wav"], check=True)
# Speech measured against this room (owner, 2 Nov 2026: "you cut my sentences too quickly… in some places too late… gaps of silence"): the room
# sits near -70 dB, his voice near -25, breaths near -50; speech is over -46 dB (10 ms steps), in word-sized runs. A run belongs to a span if
# its middle is inside it (the edges above only choose WHICH words); kept runs closer than 0.30 s stay joined with their real gap, and every
# other cut lands in silence: 0.08 s before a word (or half the gap), 0.20 s after its end for the tail (or half the gap).
import numpy as np
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", "audio.wav", "-f", "s16le", "-"], capture_output=True).stdout, np.int16) / 32768
e = 20 * np.log10(np.sqrt(np.convolve(x ** 2, np.ones(160) / 160, "same"))[::160] + 1e-9)
runs, cur = [], None
for k, v in enumerate(np.append(e > -46, False)):
    if v and cur is None: cur = k
    if not v and cur is not None:
        if runs and cur / 100 - runs[-1][1] < 0.06: runs[-1] = (runs[-1][0], k / 100)   # a stop consonant's tiny dip isn't a gap
        else: runs.append((cur / 100, k / 100))
        cur = None
runs = [r for r in runs if r[1] - r[0] >= 0.04]
keep = [i for i, (s0, s1) in enumerate(runs) if any(a <= (s0 + s1) / 2 <= b for a, b in SPANS)]
groups = []
for i in keep:
    gap = (runs[i - 1][1], runs[i][0]) if i else (0, 0)
    soft = 0 < gap[1] - gap[0] < 1.2 and (e[int(gap[0] * 100):int(gap[1] * 100)] > -52).sum() >= 8   # a softly said word in a short gap
                                                                                                          # ("that's the important thing here")
    if groups and groups[-1][-1] == i - 1 and (gap[1] - gap[0] < 0.30 or soft): groups[-1].append(i)
    else: groups.append([i])
chunks = []
for g in groups:
    s0, s1 = runs[g[0]][0], runs[g[-1]][1]
    pre = runs[g[0] - 1][1] if g[0] else 0.0; nxt = runs[g[-1] + 1][0] if g[-1] + 1 < len(runs) else s1 + 1
    slow = any(a <= s0 <= b for a, b in SLOW)          # the letters, said slowly on purpose: more room either side
    chunks.append((round(s0 - min(0.15 if slow else 0.08, (s0 - pre) / 2), 3), round(s1 + min(0.32 if slow else 0.20, (nxt - s1) / 2), 3)))
json.dump(chunks, open("chunks.json", "w"))
print(len(chunks), "pieces,", round(sum(round((b - a) * 30) / 30 for a, b in chunks), 1), "s")
