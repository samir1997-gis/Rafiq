# The landing page's top screen (owner, 22 Oct and 4 Nov 2026: "one promise, one button"): the current hero against three
# one-promise options. Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/landing_hero.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("rafiq-arabic.com on a phone, the first screen before scrolling. Rafiq is a web app that teaches UK Muslims the Arabic of the "
       "Qur'an and the salah, with a free week. The screen shows: ")
H = {"current": "the Arabic tagline 'your companion in learning Arabic'; 'Learn Arabic, and understand every word of your salah'; a 5-line "
                "paragraph (short daily lessons in Modern Standard Arabic, fully vowelled, from the first letter, what each word of your prayer "
                "means, audio and pictures, reviews timed for just before you'd forget); a 'Start your free week' button; '7 days free, no card. "
                "Nothing is charged when it ends.'",
     "L1_video": "the Arabic tagline small; big 'Understand every word of your salah'; a one-minute video with 'Watch in a minute'; a big "
                 "'Start your free week' button; '7 days free · no card'.",
     "L2_try": "big 'Understand every word of your salah'; 'You say it five times a day. Try one word now:'; a card with سُبْحانَ from the "
               "prayer, a sound button and three answers to tap (is the Greatest / Glory be to / my Lord); a big 'Start your free week' "
               "button; '7 days free · no card'.",
     "L3_line": "the Arabic tagline small; big 'Understand every word of your salah'; سُبْحانَ رَبِّيَ الْعَظِيمِ with each word's meaning "
                "under it (Glory be to · my Lord · the Magnificent), 'What you say in every rukūʿ, word by word'; a big 'Start your free week' "
                "button; '7 days free · no card'; '5 minutes a day · from the very first letter'.",
     "L4_line_sub": "the Arabic tagline small; big 'Understand every word of your salah'; one line 'Short daily Arabic lessons from the very first "
                    "letter, with audio, and reviews that make words stick'; سُبْحانَ رَبِّيَ الْعَظِيمِ with each word's meaning under it "
                    "(Glory be to · my Lord · the Magnificent), 'What you say in every rukūʿ, word by word'; a big 'Start your free week' "
                    "button; '7 days free · no card'."}
WHO = {"tiktok": "a 22-year-old UK Muslim who tapped the link after a Rafiq TikTok about salah",
       "search": "a 33-year-old who searched 'learn Quran Arabic online UK'",
       "parent": "a 41-year-old Muslim mum who prays but doesn't understand the words"}
Q = {"signup": {"type": "score", "instructions": "`ctx``h` Visitor: `who`. How likely are they to tap 'Start your free week'?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "clear": {"type": "score", "instructions": "`ctx``h` Visitor: `who`. How clear is it, within 5 seconds, what Rafiq is and what they'd get?", "criteria": ["Not clear", "Somewhat", "Clear", "Very clear"]},
     "trust": {"type": "score", "instructions": "`ctx``h` Visitor: `who`. How much do they trust it's worth their time?", "criteria": ["Not at all", "A little", "Quite", "Very"]}}
jobs = [(k, w) for k in H for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": H[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>8}" for q in Q) + "   total   " + "  ".join(f"{w:>7}" for w in WHO))
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in H]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())):
    print(f"{k:10}" + "".join(f"{s[q]:8.2f}" for q in Q) + f"   {sum(s.values()):.2f}   " + "  ".join(f"{sum(r[(k, w)][q]['score'] for q in Q):7.1f}" for w in WHO))
