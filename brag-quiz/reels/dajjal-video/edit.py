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
    (173.15, 186.95), # so the dajjāl isn't just a liar, the dajjāl is a master liar … like a manipulator or a fraudster.
    (203.7, 210.85),  # Someone who covers the truth with something shiny to make it look appealing again and again and again.
    (226.2, 233.4),  # So, by that meaning, anyone could be a dajjāl, there could be hundreds, even thousands living amongst us.
    (241.5, 248.7),  # The Prophet ﷺ even said that the Hour will not pass until…
    (256.6, 261.9),  # 30 dajjāls appear, liars, each claiming to have prophethood,
    (282.5, 285.45),  # But there is one who is the greatest of them all,
    (288.45, 290.95), # al-Masīḥ ad-Dajjāl.
    (308.5, 327.85),  # And his lies … his fire is paradise and his paradise is fire.
    (359.7, 363.75),  # He literally paints Jahannam with gold,
    (365.25, 368.3), # making it appear like paradise.
    (409.65, 424.05), # But Allah ﷻ did not leave us without clues … will be able to identify it.
    (425.9, 432.2),   # It has nothing to do with your ability to read, it has everything to do with your faith. ("and that's the important thing
                      #  here" dropped: said too quietly, the silence cut took half of it)
    (460.2, 476.6),   # And the Prophet ﷺ said … the first 10 ayat of Sūrat al-Kahf … Send this to someone … from the dajjāl.
]
os.chdir(W)
if not os.path.exists("audio.wav"):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "clip.mp4", "-vn", "-ac", "1", "-ar", "16000", "audio.wav"], check=True)
log = subprocess.run(["ffmpeg", "-i", "audio.wav", "-af", "silencedetect=noise=-40dB:d=0.4", "-f", "null", "-"], capture_output=True, text=True).stderr
sil = [(float(e) - float(d) + .12, float(e) - .12) for e, d in re.findall(r"silence_end: ([\d.]+) \| silence_duration: ([\d.]+)", log)]
chunks = []
for a, b in SPANS:                                    # each span minus the silences inside it
    cur = a
    for s, e in sil:
        if e <= cur or s >= b: continue
        if s > cur and s - cur > .12: chunks.append((round(cur, 3), round(min(s, b), 3)))
        cur = max(cur, e)
    if b - cur > .12: chunks.append((round(cur, 3), round(b, 3)))
json.dump(chunks, open("chunks.json", "w"))
print(len(chunks), "pieces,", round(sum(round((b - a) * 30) / 30 for a, b in chunks), 1), "s")
