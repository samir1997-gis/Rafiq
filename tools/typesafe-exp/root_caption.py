# Caption for the ʿ-l-m root carousel. Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/root_caption.py
from concurrent.futures import ThreadPoolExecutor
import json, os, time, urllib.request
KEY = os.environ.get("TYPESAFE_API_KEY") or os.environ["TYPE_SAFE_KEY"]
def ask(state, qs):
    body = json.dumps({"state": state, "model": "jev-latest", "questions": qs}).encode()
    for a in range(5):
        try:
            r = urllib.request.Request("https://api.typesafe.ai/v1/systemone", body, {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
            with urllib.request.urlopen(r, timeout=60) as f: return json.load(f)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504, 529) and a < 4: time.sleep(2 ** a); continue
            raise
CTX = ("TikTok/Instagram photo carousel from Rafiq (Arabic for UK Muslim beginners): four words share the letters ع ل م, coloured in each "
       "(knowledge, a scholar, a teacher, a learner); it ends on رَبِّ زِدْنِي عِلْمًا, 'My Lord, increase me in knowledge' (Ta Ha 20:114).")
C = {
 "A_challenge": "4 words. 3 letters hiding in every one 👀 Can you spot them before you swipe?\n\nعِلْم knowledge · عالِم scholar · مُعَلِّم teacher · مُتَعَلِّم learner, all from ع ل م.\n\nAnd you'll find it in the duʿāʾ: رَبِّ زِدْنِي عِلْمًا, “My Lord, increase me in knowledge.” 🤲\n\nLearn the words you say → rafiq-arabic.com\n\n#arabic #learnarabic #quranicarabic #muslim #islam",
 "B_insight": "A scholar, a teacher, a learner. One family of words, from three letters: ع ل م 📖\n\nOnce you see the root, Arabic stops being a list to memorise and starts making sense.\n\nIt's even in the duʿāʾ: رَبِّ زِدْنِي عِلْمًا, “My Lord, increase me in knowledge.”\n\nFree for 7 days → rafiq-arabic.com\n\n#arabic #learnarabic #quranicarabic #muslim #islam",
 "C_duaa_first": "رَبِّ زِدْنِي عِلْمًا, “My Lord, increase me in knowledge.” 🤲\n\nThat word عِلْم shares its three letters with the scholar, the teacher and the learner. Swipe to see them light up.\n\nUnderstand the words you say → rafiq-arabic.com\n\n#arabic #learnarabic #quranicarabic #muslim #islam",
}
WHO = {"beginner": "a UK Muslim who can't read Arabic, scrolling TikTok", "some": "a UK Muslim who reads Quran letters but doesn't understand them", "parent": "a busy Muslim parent on Instagram"}
Q = {"stop": {"type": "score", "instructions": "`ctx` Caption: `c`. Viewer: `who`. How likely does it make them swipe through the carousel?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "visit": {"type": "score", "instructions": "`ctx` Caption: `c`. Viewer: `who`. How likely are they to visit the site?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "respect": {"type": "score", "instructions": "`ctx` Caption: `c`. Viewer: `who`. How respectful and sincere does it feel (not salesy)?", "criteria": ["Not at all", "A little", "Fairly", "Very"]}}
jobs = [(k, w) for k in C for w in WHO]
with ThreadPoolExecutor(9) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "c": C[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':14}" + "".join(f"{q:>9}" for q in Q) + "    total")
for k in sorted(C, key=lambda k: -sum(r[(k, w)][q]['score'] for w in WHO for q in Q)):
    s = [sum(r[(k, w)][q]['score'] for w in WHO) / 3 for q in Q]; print(f"{k:14}" + "".join(f"{x:9.2f}" for x in s) + f"    {sum(s):.2f}")
