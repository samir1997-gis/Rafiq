# The owner's talking reel (10 Oct 2026): salah is the first thing we're asked about; 20 words make up 56% of what you say
# in salah (salah-data.js / salah.js, surah excluded); comment RAFIQ for the list. Hooks and the ask checked here.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/accountable_talk.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
from concurrent.futures import ThreadPoolExecutor
CTX = ("A 45-second talking-head reel by a young British Muslim who runs Rafiq, a small Arabic-learning account. Body: picture the Day of "
       "Judgement; the first thing you are asked about is your salah (Tirmidhi 413); are you content with yours? The easiest way to make it "
       "more meaningful is understanding its words; 20 words make up over half of what you say in salah. Then a call to action.")
HOOK = {"A_dont_pray": "Don't pray another salah without doing this first.",
        "B_first_asked": "The first thing you'll be asked about on the Day of Judgement is your salah.",
        "C_content": "If you stood before Allah today, would you be happy with your salah?",
        "D_twenty": "20 words make up more than half of everything you say in salah."}
ASK = {"a_comment": "Comment RAFIQ and I'll send you the 20 words.",
       "b_link": "The 20 words are free on rafiq-arabic.com, link in bio.",
       "c_save": "Save this and learn the first word before your next salah."}
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has wanted to learn Arabic for years",
       "imam": "a careful, knowledgeable Muslim who dislikes clickbait about religion"}
QH = {"stop": {"type": "score", "instructions": "`ctx` Opening line: `h`. Viewer: `who`. How likely are they to keep watching past 3 seconds?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
      "fair": {"type": "score", "instructions": "`ctx` Opening line: `h`. Viewer: `who`. Is the line accurate and respectful, not misleading about the religion?", "criteria": ["No", "Somewhat", "Mostly", "Yes"]}}
QA = {"act": {"type": "score", "instructions": "`ctx` Ending: `h`. Viewer: `who`. How likely are they to do what it asks?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [("h", k, w) for k in HOOK for w in WHO] + [("a", k, w) for k in ASK for w in WHO]
def run(j):
    t, k, w = j; src, q = (HOOK, QH) if t == "h" else (ASK, QA)
    return j, ask({"ctx": CTX, "h": src[k], "who": WHO[w]}, q)["answers"]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(run, jobs))
for t, src, q in (("h", HOOK, QH), ("a", ASK, QA)):
    for k in src: print(k, *(f"{n} {sum(r[(t, k, w)][n]['score'] for w in WHO) / 3:.2f}" for n in q), "| imam fair" if t == "h" else "", r[(t, k, "imam")]["fair"]["score"] if t == "h" else "")
