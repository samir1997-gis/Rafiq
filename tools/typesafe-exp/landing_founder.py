# The founder video for the landing page (owner, 4 Nov 2026, #160/#210): the 30 Sep founder story against salah-led versions.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/landing_founder.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("On rafiq-arabic.com, under 'Understand every word of your salah', a video of the founder, a young British Muslim, sitting and talking to "
       "camera (about 45 seconds). He says: ")
S = {"sep30": "\"Two years ago, I decided it was time to learn Arabic. To understand what I say in my salah, to understand the Quran, in the language "
              "it was revealed in to the Prophet ﷺ. So I started studying with a teacher, and at first it went really well. But about a year in, I noticed "
              "something. The further I got, the more I was forgetting my early lessons. A lesson once or twice a week isn't the problem. It's what happens "
              "in between. That's why we built Rafiq. It brings back the words you've learned just before you'd forget them, so they stick. If you study with "
              "a teacher, use Rafiq on the days in between, so you're practising Arabic every day, not once a week. And if you're just starting out, it begins "
              "with the letters.\"",
     "salah": "\"For 26 years I prayed every day without understanding a single word I was saying in my salah. Two years ago I decided to change that, and "
              "started learning Arabic with a teacher. But between lessons, I kept forgetting what I'd learned. So I built Rafiq. It starts with the words you "
              "say most in your salah, and teaches Arabic from the very first letter, a few minutes a day. Then it brings each word back just before you'd "
              "forget it, so it sticks. Try it free for a week. No card needed.\"",
     "salah_short": "\"For 26 years I prayed without understanding a single word of my salah. So I built Rafiq. It starts with the words you say most in "
                    "your prayer, a few minutes a day, from the very first letter, and brings each word back just before you'd forget it. Try it free for a "
                    "week.\"",
     "salah_moment": "\"For 26 years I prayed every day without understanding a single word I was saying. The first time I said سُبْحانَ رَبِّيَ الْعَظِيمِ "
                     "and knew what it meant, glory be to my Lord, the Magnificent, my salah felt different. That's why I built Rafiq. It starts with the "
                     "words you say most in your prayer, from the very first letter, a few minutes a day, and brings each word back just before you'd "
                     "forget it. Try it free for a week.\""}
WHO = {"tiktok": "a 22-year-old UK Muslim who tapped the link after a Rafiq TikTok about salah",
       "search": "a 33-year-old who searched 'learn Quran Arabic online UK'",
       "parent": "a 41-year-old Muslim mum who prays but doesn't understand the words"}
Q = {"watch": {"type": "score", "instructions": "`ctx``s` Visitor: `who`. How likely are they to watch to the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "signup": {"type": "score", "instructions": "`ctx``s` Visitor: `who`. How likely are they to start the free week after it?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx``s` Visitor: `who`. How genuine and trustworthy does he feel?", "criteria": ["Not at all", "A little", "Quite", "Very"]}}
jobs = [(k, w) for k in S for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "s": S[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':13}" + "".join(f"{q:>8}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in S]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:13}" + "".join(f"{s[q]:8.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
