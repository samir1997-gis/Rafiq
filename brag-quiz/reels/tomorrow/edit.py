#!/usr/bin/env python3
"""The edit of the five tomorrow-people versions (SCRIPTS.md; owner, 25 Oct 2026, #292): fills in each version's config.json
after the template's `plan`. Every graphic (graphics.py, full screen while he keeps talking) is anchored to the word it belongs
to: its key beat (a slam, a stamp, a door shutting) lands on that word. Titles sit behind his head; the flicker is the hook.
V3 also gets the al-Ḥijr 15:3 screen (made here, its timings from his words) with al-Ḥuṣarī's recitation in his pause.
  python3 edit.py WORK vN       (WORK/vN has been through the template's base and plan; the graphics are rendered in out/)"""
import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); G = os.path.join(HERE, "out")
W, V = sys.argv[1], sys.argv[2]; D = os.path.join(W, V)
C = json.load(open(f"{D}/config.json")); ws = json.load(open(f"{D}/cutwords.json")); END = C["end"]
nz = lambda w: re.sub(r"[^a-z]", "", w.lower())

def at(phrase, after=0.0, end=False):
    """When the words of phrase are said (the first time after `after`): their start, or the end of the last one."""
    p = [nz(x) for x in phrase.split()]
    for i in range(len(ws) - len(p) + 1):
        if ws[i]["s"] >= after and all(nz(ws[i + k]["w"]) == p[k] for k in range(len(p))):
            return ws[i + len(p) - 1]["e"] if end else ws[i]["s"]
    raise SystemExit(f"{V}: not found: {phrase!r} after {after}")

panels, titles, flicks = [], [], []
def gfx(name, anchor, beat, lead=None, until=None, dur=None, after=0.0, slams=(), hits=(), **o):
    """A graphic whose moment `beat` (s into its clip) lands on the word(s) `anchor`; it comes in `lead` s before that word."""
    A = at(anchor, after); lead = beat if lead is None else lead; frm = max(0.0, beat - lead); s0 = A - lead
    s1 = (at(until, A, end=True) + 0.3) if until else (END if dur == "end" else s0 + dur)
    loc = lambda t: round(s0 + t - frm, 2)
    panels.append([round(s0, 2), round(min(s1, END), 2), "gfx", dict(src=f"{G}/{name}.mp4", **({"from": round(frm, 2)} if frm else {}),
                   slams=[loc(t) for t in slams if t >= frm], hits=[loc(t) for t in hits if t >= frm], **o)])
def title(phrase, small, big, size, until=None, dur=3.0, after=0.0):
    a = at(phrase, after); titles.append([round(a, 2), round(at(until, a, end=True) + 0.3 if until else a + dur, 2), small, big, size])
def flick(until, text, size=120):
    flicks.append([0, round(at(until, end=True) + 0.25, 2), text, size])

ENDING = lambda: (gfx("t9-today", "start today", 1.05, lead=1.05, dur=3.0, after=at("don't say"), slams=[2.2]),
                  gfx("p1-pack", "comment", 0.15, dur="end", slams=[0.15], hits=[0.9, 1.2, 1.5, 1.9]))
if V == "v1":
    flick("I'll start tomorrow", "I'LL START TOMORROW", 110)
    gfx("t1-tomorrow", "tomorrow people", 3.9, lead=1.2, until="people", slams=[3.9], hits=[3.35])
    title("Shaitan's biggest", "SHAYTAN'S BIGGEST", "PLOY", 300, until="ploys")
    gfx("c1-clock", "as long as", 2.8, until="win", hits=[0.7, 1.4, 2.1, 4.2])
    gfx("t7-graves", "grave", 0.3, until="tomorrow")
    title("little do they know", "THEY MIGHT NOT REACH", "TOMORROW", 230, until="reach tomorrow")
    title("biggest gift", "THE BIGGEST", "GIFT", 320, until="present")
    ENDING()
elif V == "v2":
    flick("too late", "IT'S TOO LATE", 140)
    gfx("t5-sun-west", "west", 2.3, lead=1.4, until="too late", slams=[2.3])
    gfx("t6-too-late", "shut", 1.9, lead=1.5, until="anyone", slams=[1.9])
    title("who are the tomorrow", "WHO ARE THE", "TOMORROW PEOPLE", 170, until="people")
    gfx("t1-tomorrow", "tomorrow people", 3.9, lead=1.2, until="people", after=at("these are"), slams=[3.9], hits=[3.35])
    gfx("t7-graves", "grave", 0.3, until="tomorrow")
    title("little do they know", "THEY MIGHT NOT REACH", "TOMORROW", 230, until="reach tomorrow")
    ENDING()
elif V == "v3":
    flick("from the west", "FROM THE WEST", 130)
    title("it's too late", "IT'S", "TOO LATE", 300, until="late")
    gfx("t6-too-late", "shut", 1.9, lead=1.5, until="anyone", slams=[1.9])
    title("there's even an arabic", "THERE'S A", "WORD FOR IT", 230, until="for it")
    tz = ws[[nz(w["w"]) for w in ws].index("it", [i for i, w in enumerate(ws) if nz(w["w"]) == "for"][0]) + 1]["s"]   # the Arabic word after "for it"
    panels.append([round(tz - 0.2, 2), round(at("later", tz, end=True) + 0.4 if any(nz(w["w"]) == "later" for w in ws) else tz + 5.5, 2), "gfx",
                   dict(src=f"{G}/t2-taswif.mp4", **{"from": 2.1}, slams=[], hits=[round(tz - 0.2 + 0.7, 2), round(tz - 0.2 + 1.1, 2)])])
    title("describes people like this", "ALLAH DESCRIBES", "THEM", 320, until="quran")
    # the ayah screen: from "he says" through his translation; the recitation plays in his held pause
    mp = json.load(open(f"{D}/map.json")); hold = [m for m in mp if m[3] == "hold"][0]; rec = hold[0] + 0.15
    q0 = at("says", at("hijr") if any(nz(w["w"]) == "hijr" for w in ws) else 0, end=True) + 0.1
    tr = [at("let them"), at("distracted"), at("they will come")]
    q1 = at("know", tr[2], end=True) + 0.9
    subprocess.run([sys.executable, os.path.join(HERE, "graphics.py"), "q1-hijr", json.dumps([round(rec - q0, 2), [round(t - q0, 2) for t in tr]])], check=True)
    subprocess.run(["npx", "hyperframes", "render", "-o", "../q1-hijr.mp4"], cwd=f"{G}/q1-hijr", check=True, capture_output=True)
    panels.append([round(q0, 2), round(q1, 2), "gfx", dict(src=f"{G}/q1-hijr.mp4", slams=[], hits=[round(t, 2) for t in tr])])
    r = os.path.join(W, "015003.mp3"); trim = os.path.join(D, "hijr-15-3.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", r, "-t", "15.2", "-af", "afade=t=out:st=14.9:d=0.3", "-ar", "48000", "-ac", "2", trim], check=True)
    lv = lambda f: float(re.findall(r"I:\s+(-?[\d.]+) LUFS", subprocess.run(["ffmpeg", "-i", f, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr)[-1])
    C["audio"] = [[trim, round(rec, 2), round(10 ** ((lv(f"{D}/cut.wav") - lv(trim) - 1.0) / 20), 3)]]   # the recitation a touch under his voice
    ENDING()
elif V == "v4":
    flick("they will say", "SEND US BACK", 150)
    gfx("s1-sajdah", "send us back", 1.9, lead=2.2, until="your worship", hits=[0.4, 1.1, 1.9, 2.4])
    gfx("t6-too-late", "too late", 1.9, lead=1.5, dur=3.2, after=at("but it'll"), slams=[1.9])
    title("problem with being", "THE PROBLEM WITH", "TOMORROW", 230, until="person")
    gfx("c1-clock", "as long as they can keep delaying", 2.8, dur=7.0, hits=[0.7, 1.4, 2.1, 4.2])
    title("winding down your clock", "UNTIL TOMORROW", "NEVER COMES", 220, until="comes")
    gfx("t7-graves", "grave", 0.3, until="tomorrow")
    title("little do they know", "THEY MIGHT NOT REACH", "TOMORROW", 230, until="reach tomorrow")
    ENDING()
elif V == "v5":
    flick("biggest ploys", "SHAYTAN'S BIGGEST PLOY", 100)
    gfx("c1-clock", "as long as", 2.8, until="win", hits=[0.7, 1.4, 2.1, 4.2])
    gfx("t1-tomorrow", "tomorrow people", 3.9, lead=1.2, until="people", slams=[3.9], hits=[3.35])
    gfx("t4-dajjal", "has come out", 0.9, lead=0.45, until="too late", hits=[1.2, 2.2])
    gfx("t5-sun-west", "west", 2.3, lead=1.4, until="too late", after=at("sun"), slams=[2.3])
    gfx("t6-too-late", "shut", 1.9, lead=1.5, until="anyone", slams=[1.9])
    title("winding down your clock", "UNTIL TOMORROW", "NEVER COMES", 220, until="comes")
    ENDING()

FIX = {"niyama": "ni'mah", "shaitans": "Shaytan's", "shaitan": "Shaytan", "jail": "Dajjal", "akhira": "akhirah",
       "shayateen": "shayatin", "sulfa": "fa-sawfa", "yaalamun": "ya'lamun", "yeah": "Ya"}
EM = set("ploys guaranteed delaying win grave full reach gift present waste today now pack late west dajjal shut repentance benefit "
         "jahannam back chance worship never comes clock know hopes taswif sawfa later promise smoking arabic quran".split())
for c in C["caps"]:
    for w in c[2]:
        k, tail = nz(w[0]), re.sub(r"^[\w'-]+", "", w[0])
        if re.search(r"[\u0600-\u06FF]", w[0]): w[0] = "at-taswif" if "ط" in w[0] or "ت" in w[0][:2] else "sawfa"
        elif k in FIX: w[0] = FIX[k] + tail
        nx = [v for v in c[2] if v[1] > w[1]] or [n for n in C["caps"] if n[0] > c[0]][:1] and [n for n in C["caps"] if n[0] > c[0]][0][2]
        if k == "now" and nx and nz(nx[0][0]) in ("im", "ill"): w[0] = "No,"            # the skit's "No, I'm gonna…", heard as "now"
        w[2] = nz(w[0]) in EM                                                     # the script's key words land gold
C["title_top"] = 470
C["titles"] = sorted(titles); C["flicks"] = flicks; C["split"] = None; C["steps"] = []
for f in flicks: f[1] = min([f[1]] + [p[0] for p in panels if p[0] > f[0]])   # the hook hands straight to a graphic
busy = [(p[0], p[1]) for p in panels] + [(f[0], f[1]) for f in flicks]
PANELS = sorted(panels)
for p, q in zip(PANELS, PANELS[1:]): p[1] = min(p[1], q[0])                   # one graphic hands straight to the next
C["panels"] = PANELS
em = [w for c in C["caps"] for w in c[2] if w[2] and not any(a - .4 <= w[1] < b + .4 for a, b in busy)]
nxt = lambda s: min([x["e"] for x in ws if abs(x["s"] - s) < .01] or [s + .35])
C["punch"] = [[w[1], nxt(w[1])] for w in em[::2]][:8]                         # every other gold word outside a graphic punches in
cuts = sorted({0, END} | {x for t in titles for x in t[:2]} | {x for a, b in busy for x in (a, b)})
C["sections"] = [[a, b] for a, b in zip(cuts, cuts[1:]) if b - a > .3]
for (a0, a1, *_), (b0, *_) in zip(sorted(panels + [f[:2] + [0, 0] for f in flicks]), sorted(panels + [f[:2] + [0, 0] for f in flicks])[1:]):
    if b0 < a1 - 0.01: print(f"{V}: overlap {a0}-{a1} with {b0}")
json.dump(C, open(f"{D}/config.json", "w"), indent=1, ensure_ascii=False)
print(V, "end", END, "| flicks", flicks, "\n titles", [(t[0], t[1], t[3]) for t in titles], "\n panels", [(p[0], p[1], os.path.basename(p[3]["src"])) for p in sorted(panels)])
