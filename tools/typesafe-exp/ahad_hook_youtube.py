# YouTube title and description for the Aḥad video with the owner's stitched hook, "Do not pray another salah until you know this fact" (11 Nov 2026).
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A YouTube Short from Rafiq, a small account teaching the Arabic Muslims use. It opens with the presenter: 'Do not pray another salah until you know "
       "this fact.' Then: Bilal, a slave in Makkah, a boulder on his chest, told to deny Muhammad, answers with one word, ahad; why ahad and not wahid "
       "(wahid is a number with a second; ahad is the One with none); you say ahad in Surat al-Ikhlas in your salah; the whole of tawhid in one word.")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling YouTube", "learner": "a 34-year-old learning Arabic", "seerah": "a 30-year-old who loves seerah stories"}
CAP = {"t1": "Don't Pray Another Salah Until You Know This #shorts", "t2": "The Word You Say in Every Salah That Bilal Said Under a Rock #shorts",
       "t3": "Before Your Next Salah: Why Bilal Said “Ahad” #shorts"}
Q = {"click": {"type": "score", "instructions": "`ctx` YouTube title: `h`. Viewer: `who`. How likely are they to watch it to the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` YouTube title: `h`. Viewer: `who`. Does the video pay off the title fairly (not clickbait)?", "criteria": ["No", "A bit", "Mostly", "Yes"]}}
jobs = [(k, w) for k in CAP for w in WHO for _ in range(2)]
with ThreadPoolExecutor(18) as ex: r = list(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
for k in CAP:
    s = {q: round(sum(a[q]["score"] for (kk, _), a in r if kk == k) / 6, 2) for q in Q}
    print(k, s, round(sum(s.values()), 2), CAP[k])
