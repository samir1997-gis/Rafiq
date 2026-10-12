# Thought-provoking opening lines, one per video (owner, 12 Oct 2026: "ask more thought-provoking questions... 'if kitāb is a book,
# what is books?' is boring"). Each line is spoken in the first second and shown on screen. Every claim must be true:
# مُحَمَّد and الْحَمْدُ share ح م د; أَذان shares أ ذ ن with أُذُن (ear); أَكْبَرُ is "greater/greatest", not just "great";
# tā' marbūṭa makes many words feminine; the past and plural follow patterns. Current line first in each list.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/hook_lines.py
# Result (12 Oct; stay / honest, target + revert x2): the plain question mostly holds its own: bold claims ("most people can't", "a part of your
#   body", "doesn't just mean great") read as clickbait. Two new lines beat the current: r2 "Part of the Prophet's ﷺ name is in a word you say in
#   every rakʿah. Can you spot it?" (stay 2.71 vs 2.32) and r4 "You say in shā' Allāh every day. Have you ever wondered what each word means?"
#   (5.44 vs 5.35). "Have you ever wondered why the Prophet ﷺ was named Muhammad?" 4.74 vs 5.00 now. What wins: tie it to something they
#   already say (every rakʿah, every day), keep it a real question, no claims about other people.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A TikTok from a small account teaching the Arabic Muslims say every day. In the first second a warm voice asks this, and it's on screen "
       "with the big Arabic word. The video then answers it with the word's root or pattern, and a 3-2-1 'your turn'. Opening line: ")
WHO = {"target": "a 27-year-old UK Muslim who prays but doesn't understand the Arabic", "revert": "a 31-year-old revert learning to pray"}
V = {
 "r2-muhammad": ["Why is the Prophet ﷺ named Muhammad?",
                 "Have you ever wondered why the Prophet ﷺ was named Muhammad?",
                 "Part of the Prophet's ﷺ name is in a word you say in every rakʿah. Can you spot it?"],
 "a2-adhan": ["Why is the call to prayer called the adhān?",
              "Have you ever wondered why the call to prayer is called the adhān?",
              "The word adhān comes from a part of your body. Which one?"],
 "r3-akbar": ["What does akbar in Allāhu akbar really mean?",
              "You say Allāhu akbar dozens of times a day. Does akbar really just mean 'great'?",
              "Akbar doesn't just mean 'great'. Here's what you're really saying in every prayer."],
 "r4-insha": ["What does in shā' Allāh actually say?",
              "You say in shā' Allāh every day. Have you ever wondered what each word means?",
              "In shā' Allāh is three words. Most people can't say what even one of them means."],
 "g1-plural": ["If kitāb is 'a book', what's 'books'?",
               "Arabic plurals don't just add an 's'. Can you guess how 'book' becomes 'books'?",
               "In Arabic, words change from the inside to become plural. Can you see how?"],
 "g2-female": ["If muʿallim is a male teacher, what's a female teacher?",
               "In Arabic, one letter at the end turns 'he' into 'she'. Can you find it?",
               "Arabic has a letter that makes words feminine. Once you see it, you'll spot it everywhere."],
 "g3-past": ["If yashrabu is 'he drinks', what's 'he drank'?",
             "In Arabic, changing a few sounds sends a verb back in time. Can you hear it?",
             "Ashrabu, part 2: one small change turns 'he drinks' into 'he drank'. Can you guess it?"],
 "v1-go-quiz": ["If adhhabu is 'I go', what's 'we go'?",
                "Learn one letter and you can turn 'I' into 'we' on any Arabic verb. Can you guess it?",
                "Arabic verbs tell you who's doing them from the first letter. Can you work out 'we go'?"],
}
Q = {"stay": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How likely are they to keep watching past 3 seconds?",
              "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. Does it feel honest and interesting rather than clickbait?",
               "criteria": ["Clickbait", "A bit", "Mostly honest", "Honest and interesting"]}}
if __name__ == "__main__":
    jobs = [(v, i, w) for v in V for i in range(len(V[v])) for w in WHO for _ in range(2)]
    with ThreadPoolExecutor(20) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "h": V[j[0]][j[1]], "who": WHO[j[2]]}, Q)["answers"]), jobs))
    for v in V:
        print(v)
        for i, h in enumerate(V[v]):
            s = {q: sum(a[q]["score"] for (vv, ii, _), a in res if vv == v and ii == i) / 4 for q in Q}
            print(f"  {s['stay']:.2f} {s['trust']:.2f} {s['stay'] + s['trust']:.2f}  {'(now) ' if i == 0 else ''}{h}")
