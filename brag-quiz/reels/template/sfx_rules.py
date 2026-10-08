"""Where the sound effects go: the rules learned from the owner's reference (a creator's SFX breakdown, 8 Oct 2026).
Every visual change gets a short, crisp, high sound that sits above the voice instead of being buried under it:
  a title landing → shutter · a line of text appearing → tap · a stressed word popping → tap
  a punch-in zoom → short swoosh · a big transition → a ~1.3 s charge that lands on the cut, then swooshes as things slide in
  a flicker → flash flicker + flicker sounds · back to the speaker → shutter · the brand name → a sparkle (owner's n08)
Each sound is set by its peak (dBFS) against a voice at about -14 LUFS, so files of any loudness come out right.
No ducking: these sounds are high and short, so they don't cover words."""
import os, wave, array, math
LIB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "sfx")
R = lambda n: os.path.join(LIB, "ref", n + ".wav")
O = lambda n: os.path.join(LIB, "owner", n + ".wav")
DUR = {"charge-swoosh": 1.33}
PEAK = {"shutter": -12, "tap": -15, "short-swoosh": -8, "flicker": -10, "flash-flicker": -9, "charge-swoosh": -13, "sparkle": -17}

def _peak(f):
    w = wave.open(f); a = array.array("h", w.readframes(w.getnframes()))
    return 20 * math.log10(max(1, max(abs(x) for x in a)) / 32768)

def snd(f, kind, t):
    return (f, t, round(10 ** ((PEAK[kind] - _peak(f)) / 20), 3))

def events(C):
    """C: the reel's config (titles, punch, caps with stressed words, split, flick). Returns [(file, time, volume)]."""
    E = []
    for a, b, small, big, *_ in C["titles"]:
        if a > .2: E.append(snd(R("tap"), "tap", a))                        # the small line appears
        E.append(snd(R("shutter"), "shutter", a + .12))                      # the big word lands
        if big.upper() == "RAFIQ": E.append(snd(O("n08"), "sparkle", a + .2))
    punches = {round(a, 2) for a, _ in C.get("punch", [])}
    for a, _ in C.get("punch", []): E.append(snd(R("short-swoosh"), "short-swoosh", a - .03))
    for c in C["caps"]:                                                      # stressed words pop with a tap (a punch already has a sound)
        for w, s, em in c[2]:
            if em and round(s, 2) not in punches: E.append(snd(R("tap"), "tap", s))
    if C.get("split"):
        s0 = C["split"][0]
        E.append(snd(R("charge-swoosh"), "charge-swoosh", s0 - DUR["charge-swoosh"]))   # builds and lands on the cut
        for k in range(3): E.append(snd(R("short-swoosh"), "short-swoosh", s0 + k * .08))
    if C.get("flick"):
        f0, f1 = C["flick"][:2]
        E.append(snd(R("flash-flicker"), "flash-flicker", f0))
        for k, n in enumerate(["flicker-v1", "flicker-v3", "flicker-v2", "flicker-v1"]):
            if f0 + .3 + k * .35 < f1 - .1: E.append(snd(R(n), "flicker", f0 + .3 + k * .35))
        E.append(snd(R("shutter"), "shutter", f1))                           # back to the speaker
    return sorted(E, key=lambda e: e[1])
