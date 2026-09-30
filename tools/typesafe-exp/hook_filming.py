# How to film the 5-second founder hook in front of the demo videos (#160).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/hook_filming.py
from concurrent.futures import ThreadPoolExecutor
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from videos_v9 import ask, Q
from social_videos import APP, VIEWER

LINE = "\"I prayed for 28 years without understanding a single word of my salah.\""
STYLES = {
    "desk-tripod": "sat at a desk, phone on a tripod at eye level, looking into the lens, tidy room behind",
    "desk-selfie": "sat at a desk, holding the phone as a selfie, looking into the lens",
    "prayer-mat":  "sitting on a prayer mat at home just after praying, phone propped up at eye level, looking into the lens",
    "walk-out":    "walking outside on a UK street, holding the phone as a selfie, talking as they walk",
    "masjid":      "standing outside a masjid, selfie, looking into the lens",
    "car":         "sitting in a parked car, phone on the dashboard, looking into the lens",
}
ENDS = {
    "cut":      "straight after the line, a hard cut to the app demo",
    "sobuilt":  "they add 'So I built this.' and hold up the phone to the camera, then it cuts to the app demo on that phone",
    "question": "they add 'Here's what changed that.' then it cuts to the app demo",
}
QS = {"stop": Q("The first 5 seconds of a vertical video ad for `app`: a man says `line`, filmed `s`. Viewer: `viewer`. How likely are they to keep watching?", ["Not at all", "A little", "Clearly", "Very"]),
      "real": Q("The opening of an ad for `app`: a man says `line`, filmed `s`. Viewer: `viewer`. How genuine and relatable does it feel (not staged or salesy)?", ["Not at all", "A little", "Clearly", "Very"])}
QE = {"flow": Q("A video ad for `app` opens with a man saying `line` to camera; then `e`. Viewer: `viewer`. How natural and compelling is that move from him to the app?", ["Not at all", "A little", "Clearly", "Very"]),
      "want": Q("A video ad for `app` opens with a man saying `line` to camera; then `e`, and 40s of the app working. Viewer: `viewer`. How much does it make them want to try the app?", ["Not at all", "A little", "Clearly", "A lot"])}

if __name__ == "__main__":
    with ThreadPoolExecutor(8) as ex:
        rs = dict(zip(STYLES, ex.map(lambda s: ask({"app": APP, "viewer": VIEWER, "line": LINE, "s": s}, QS)["answers"], STYLES.values())))
        re_ = dict(zip(ENDS, ex.map(lambda e: ask({"app": APP, "viewer": VIEWER, "line": LINE, "e": e}, QE)["answers"], ENDS.values())))
    print("style        stop  real  total")
    for k, a in sorted(rs.items(), key=lambda x: -(x[1]["stop"]["score"] + x[1]["real"]["score"])):
        print(f"{k:<12} {a['stop']['score']:.2f}  {a['real']['score']:.2f}  {a['stop']['score'] + a['real']['score']:.2f}")
    print("\nthen         flow  want  total")
    for k, a in sorted(re_.items(), key=lambda x: -(x[1]["flow"]["score"] + x[1]["want"]["score"])):
        print(f"{k:<12} {a['flow']['score']:.2f}  {a['want']['score']:.2f}  {a['flow']['score'] + a['want']['score']:.2f}")

# Results (30 Sep 2026), stop + real: prayer mat at home 5.42 · outside a masjid 5.15 · walking outside 5.04
#   · parked car 5.04 · desk on a tripod 4.65 · desk selfie 4.59.
# Then: "So I built this." + phone held up 5.68 · "Here's what changed that." 5.56 · straight cut 5.24.
