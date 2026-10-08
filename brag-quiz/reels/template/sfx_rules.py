"""Where the sound effects go: the rules learned from the owner's reference (a creator's SFX breakdown, 8 Oct 2026),
plus the owner's own sounds (n01-n11). Every visual change gets a short, crisp sound, and no two in a row are the same:
  a title landing → shutter / pop · a line of text → tap / tick · a stressed word popping → tap / tick / ping / click
  a punch-in → swoosh · stepped zoom ("these · three · things") → a hit on every step, the last one heaviest
  a big transition → a charge that lands on the cut + a boom, then swooshes as the strips slide in
  a flicker → flash + the owner's opening whoosh, a flicker sound on every clip switch, a swoosh + shutter on the wipe out
  the brand name → sparkle + ding
Each sound is levelled by its loudest 50 ms against the voice (which sits around -17 dBFS on the same measure at -14 LUFS),
and placed so that loudest moment lands on the visual. No ducking: the sounds are short and they should be heard."""
import os, wave, array, math
LIB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "sfx")
def F(n): return os.path.join(LIB, "owner" if n[0] == "n" and n[1:].isdigit() else "ref", n + ".wav")

# loudest 50 ms, in dBFS: 0 dB above means as loud as the voice's words
LEVEL = {"hit": -16, "boom": -17, "swoosh": -14, "tap": -19, "flicker": -19, "charge": -15, "sparkle": -19}
POOL = {   # rotated in order, so a sound never repeats back to back
    "small": ["tap", "n10", "click"],
    "title": ["shutter", "n05", "shutter-clicks", "shutter"],
    "emph": ["tap", "n10", "n09", "click", "digital", "click-x2"],
    "punch": ["short-swoosh", "n11", "swoosh-low", "swoosh"],
    "step": ["n10", "n05", "shutter"],
    "flick": ["flicker-v1", "flicker-v3", "digital", "flicker-v2", "click-x2"],
}
_info = {}
def info(f):   # (loudest 50 ms in dBFS, when it happens in s)
    if f not in _info:
        w = wave.open(f); sr, ch = w.getframerate(), w.getnchannels(); a = array.array("h", w.readframes(w.getnframes()))[::ch]
        n = int(sr * .05); best, at = 1e-9, 0
        for i in range(0, max(1, len(a) - n), n // 2):
            r = math.sqrt(sum(x * x for x in a[i:i + n]) / n)
            if r > best: best, at = r, i
        _info[f] = (20 * math.log10(best / 32768), (at + n / 2) / sr)
    return _info[f]

def events(C):
    """C: the reel's config. Returns [(file, start time, volume)], each sound's loudest moment on its visual."""
    E, turn = [], {k: 0 for k in POOL}
    def add(name, kind, t, db=0):
        f = F(name); lv, pk = info(f); E.append((f, round(t - pk, 3), round(10 ** ((LEVEL[kind] + db - lv) / 20), 3)))
    def pick(pool):
        n = POOL[pool][turn[pool] % len(POOL[pool])]; turn[pool] += 1; return n
    for a, b, small, big, *_ in C["titles"]:
        if small and a > .2: add(pick("small"), "tap", a)                    # the small line appears
        add(pick("title"), "hit", a + .2)                                     # the big word lands
    steps = C.get("steps", [])
    stepped = {round(s, 2) for ts, _ in steps for s in ts}
    for ts, _ in steps:                                                       # "these · three · things": a hit per step
        for k, s in enumerate(ts):
            add(POOL["step"][min(k, len(POOL["step"]) - 1)], "hit", s, -3 + 3 * k / max(1, len(ts) - 1))
            add(pick("punch"), "swoosh", s - .02, -4)
        add("n03", "boom", ts[-1], -2)                                        # weight under the last step
    punches = {round(a, 2) for a, _ in C.get("punch", [])}
    for a, _ in C.get("punch", []): add(pick("punch"), "swoosh", a)
    for c in C["caps"]:                                                       # other stressed words pop with a tap
        for w, s, em in c[2]:
            if em and round(s, 2) not in punches | stepped: add(pick("emph"), "tap", s)
    if C.get("split") and C["split"][0] >= 0:
        s0, s1 = C["split"]
        add("charge-swoosh", "charge", s0); add("n03", "boom", s0)            # builds and lands on the cut
        for k in range(3): add(pick("punch"), "swoosh", s0 + .05 + k * .08, -2)
        add("shutter", "hit", s1)                                             # back to the speaker
    for i, (f0, f1, title, *_) in enumerate(C.get("flicks", [])):
        add("flash-flicker", "hit", f0 + .02)
        if f0 < .1: add("n02", "swoosh", f0 + .25)                            # the hook opens with the owner's whoosh
        k = 1
        while f0 + k * 8 / 30 < f1 - .15:                                     # every clip switch (8 frames)
            add(pick("flick"), "flicker", f0 + k * 8 / 30); k += 1
        if title.upper().startswith("RAFIQ"): add("n08", "sparkle", f0 + .15); add("n04", "sparkle", f1 - .5)
        if f1 < C["end"] - .1: add(pick("punch"), "swoosh", f1 - .15); add("shutter", "hit", f1)   # circle wipe out
    return sorted(E, key=lambda e: e[1])
