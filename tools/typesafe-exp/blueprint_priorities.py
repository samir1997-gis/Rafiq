# Which ideas from the owner's teaching-science PDF ("How to Teach Arabic: The Science and the Blueprint", 3 Nov 2026, #333) to build first.
# Each feature is described as the learner would meet it in Rafiq; three learners say how much it would make them keep coming back,
# learn more, and pay. Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/blueprint_priorities.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("Rafiq is a web app that teaches UK Muslims the Arabic of the Qur'an and the salah: short daily lessons, words that come back for review "
       "on a schedule, a 'Your salah' section that teaches the prayer word by word, a streak, and (paid) an AI tutor and spoken conversation scenes. "
       "A new feature: ")
WHO = {"beginner": "a 26-year-old UK Muslim who can't read Arabic yet and wants to understand their salah",
       "reader": "a 38-year-old who reads the Qur'an fluently but doesn't understand it",
       "lapsed": "a 31-year-old who has started and quit several Arabic apps"}
F = {"salah_meter": "a meter on the home screen: 'You understand 61% of your salah', rising as you learn each word of the prayer.",
     "shape_letters": "the alphabet taught in families of letters that share a shape (ب ت ث ن ي, then ج ح خ), always contrasting the dots.",
     "sound_gym": "a 'sound gym': a few minutes a day of hearing pairs that English speakers mix up (ح/ه, ع/ء, ق/ك, ص/س) in many voices and tapping which one you heard.",
     "vowel_fade": "vowel marks that gradually disappear from words you know well, with a tap to bring them back.",
     "one_queue": "one daily review list that brings back letters, sounds and grammar patterns as well as words, all on the same schedule.",
     "quran_curve": "a Qur'an meter: 'the words you know cover 34% of the Qur'an', from a word count of the whole Qur'an.",
     "stories": "a short story every day written only with words you already know, plus two or three new ones, read aloud.",
     "voice_score": "say a word into the mic and the app tells you exactly which sound was off ('your ع sounded like ء: from lower in the throat').",
     "root_toy": "a word-building toy: put a 3-letter root into a pattern (like ma__a__ = 'the place of') and see and hear the real word it makes.",
     "khutbah": "Friday khutbah recordings with Arabic captions you can tap to learn the words."}
Q = {"return": {"type": "score", "instructions": "`ctx``f` Learner: `who`. How much would this make them come back every day?", "criteria": ["Not at all", "A little", "Quite a lot", "A lot"]},
     "learn": {"type": "score", "instructions": "`ctx``f` Learner: `who`. How much would this help them actually learn?", "criteria": ["Not at all", "A little", "Quite a lot", "A lot"]},
     "pay": {"type": "score", "instructions": "`ctx``f` Learner: `who`. How much would this make them want to pay for Rafiq?", "criteria": ["Not at all", "A little", "Quite a lot", "A lot"]}}
jobs = [(k, w) for k in F for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "f": F[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':14}" + "".join(f"{q:>8}" for q in Q) + "   total   " + "  ".join(f"{w[:8]:>8}" for w in WHO))
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in F]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())):
    print(f"{k:14}" + "".join(f"{s[q]:8.2f}" for q in Q) + f"   {sum(s.values()):.2f}   " + "  ".join(f"{sum(r[(k, w)][q]['score'] for q in Q):8.1f}" for w in WHO))
