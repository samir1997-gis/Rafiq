# Round 2 (#230): the winner was the faceless logo tile. What makes it likeable and good on video without a face? And its voice.
exec(open("tools/typesafe-exp/rafiq_character.py").read().split("jobs = [")[0])   # the context, viewers and questions from round 1
from concurrent.futures import ThreadPoolExecutor
BASE = "The logo itself comes alive with NO face: the dark rounded square with ر moves with personality (bounces, leans in, nods, wobbles when thinking) and its small red dot glows and pulses in time with its voice."
CON = {
 "B0_base": BASE,
 "B1_bubbles": BASE + " When it teaches, the Arabic word pops out of it on a card with the meaning, and the changing letter glows red.",
 "B2_letter_mood": BASE + " The ر on it subtly reshapes with its mood: it stands taller when proud of you, curls when thinking, droops and bounces back when you get something wrong.",
 "B3_hands": BASE + " It has two small rounded hands (no face) to wave salam, point at words and give a thumbs up.",
 "B4_all": BASE + " The ر on it reshapes with its mood, the word it is teaching pops out of it on a card with the meaning, and it has two small rounded hands to wave salam and point at words (still no face).",
}
VOICE = {"V1_brother": "Its voice: a calm, warm young British Muslim man, like a kind older brother; short sentences, encouraging, a little gentle humour; says 'salam' and 'mashaAllah' naturally.",
         "V2_cheeky": "Its voice: a playful, cheeky, fast-talking young man who jokes a lot and teases learners when they get things wrong.",
         "V3_scholar": "Its voice: a formal, wise teacher, slow and serious, uses classical phrases.",
         "V4_friend_neutral": "Its voice: a friendly, upbeat, neutral-accent voice, polished like a voice assistant."}
def table(opts, qs, title, key):
    jobs = [(k, w) for k in opts for w in WHO]
    with ThreadPoolExecutor(12) as ex:
        r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, key: opts[j[0]], "who": WHO[j[1]]}, qs)["answers"]), jobs))
    print(f"\n{title}\n{'':18}" + "".join(f"{q:>8}" for q in qs) + "   total")
    rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / len(WHO) for q in qs}) for k in opts]
    for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:18}" + "".join(f"{s[q]:8.2f}" for q in qs) + f"   {sum(s.values()):.2f}")
table(CON, Q, "Round 2: making the faceless tile likeable", "h")
QV = {"like": {"type": "score", "instructions": "`ctx` The character is the faceless animated logo tile. `v` Viewer: `who`. How much would they like hearing Rafiq talk?", "criteria": ["Not at all", "A little", "Fairly", "A lot"]},
      "trust": {"type": "score", "instructions": "`ctx` The character is the faceless animated logo tile. `v` Viewer: `who`. As their AI tutor for Arabic and salah, how much would they trust it?", "criteria": ["Not at all", "A little", "Fairly", "A lot"]},
      "brand": {"type": "score", "instructions": "`ctx` `v` How well does this voice fit the brand?", "criteria": ["Poorly", "OK", "Well", "Perfectly"]}}
table(VOICE, QV, "Rafiq's voice", "v")
