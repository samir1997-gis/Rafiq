# The aḥad script (owner to camera, 1 Nov 2026, #315; brag-quiz/reels/ahad/SCRIPT.md): Bilāl, aḥad vs wāḥid: version A (full) vs B (tight), and the three hooks.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/ahad_script.py
import re
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
md = open("brag-quiz/reels/ahad/SCRIPT.md").read()
def part(a, b):
    t = md[md.index(a):md.index(b)].split("\n", 1)[1]
    t = re.sub(r"🎬 \*[^*]*\*", "", t)                       # the graphics cues aren't said
    return re.sub(r"\s+", " ", t.replace(">", " ").replace("*", "")).strip()
S = {"A": part("## Version A", "## Version B"), "B": part("## Version B", "## Hook options")}
H = {f"hook{i}": h for i, h in enumerate(re.findall(r"^\d\. (.+?)(?: \*\(|$)", md[md.index("## Hook options"):], re.M), 1)}
CTX = ("A talking-head Reel from Rafiq, an account teaching the Arabic Muslims use; the presenter, a young British Muslim, to camera, with graphics: "
       "drawn scenes of Makkah and Bilāl, Arabic words, ayah cards. ")
WHO = {"young": "a 20-year-old UK Muslim who scrolls a lot", "practising": "a 30-year-old practising Muslim",
       "learner": "a 35-year-old learning Arabic for the Qur'an"}
Q = {"finish": {"type": "score", "instructions": "`ctx` Script: `s` Viewer: `who`. How likely are they to watch to the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "share": {"type": "score", "instructions": "`ctx` Script: `s` Viewer: `who`. How likely are they to share, save or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "fair": {"type": "score", "instructions": "`ctx` Script: `s` Viewer: `who`. Does it feel accurate, sincere and respectful, not preachy?", "criteria": ["No", "A bit", "Mostly", "Yes"]}}
HQ = {"stop": {"type": "score", "instructions": "`ctx` The first line said to camera: `s` Viewer: `who`, scrolling. How likely are they to stop and keep watching?",
               "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(k, w, S, Q) for k in S for w in WHO] + [(k, w, H, HQ) for k in H for w in WHO]
with ThreadPoolExecutor(12) as ex: res = list(ex.map(lambda j: ((j[0], j[1]), ask({"ctx": CTX, "s": j[2][j[0]], "who": WHO[j[1]]}, j[3])["answers"]), jobs))
for k in list(S) + list(H):
    rows = [a for (kk, w), a in res if kk == k]
    print(f"{k:6}", "  ".join(f"{q} {sum(a[q]['score'] for a in rows) / len(rows):.2f}" for q in rows[0]), "|", (S.get(k) or H.get(k))[:70])
