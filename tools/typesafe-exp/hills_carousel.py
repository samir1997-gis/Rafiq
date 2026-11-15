# "Signs in the hills" carousel (#375, 15 Nov 2026): the owner's Kinder Scout photos, five verses, one Qur'an word per slide
# (آيات signs, الصِّراط the path, الجِبال the mountains, يُسْرًا ease, حَبْل rope). Which cover line, and which caption?
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 6-slide Instagram carousel from Rafiq, a small account teaching the Arabic of the Qur'an to Muslims in the UK. Real photos from the "
       "presenter's hike up Kinder Scout with friends (sunrise, fog, hail, a group at the summit). Each slide: a verse, one word in gold with its "
       "meaning (ayat signs 3:190, as-sirat the path 1:6, al-jibal the mountains 27:88, yusr ease 94:6, habl rope 3:103). Last slide: the five words, "
       "'which verse would you take up a mountain? 1-5', and the site.")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling", "learner": "a 34-year-old learning Arabic", "hiker": "a 28-year-old UK Muslim who likes the outdoors"}
COVER = {"climbed": "Climbed a mountain. Found these 5 words in the Qur'an.", "kinder": "5 Qur'an words I couldn't stop thinking about on Kinder Scout",
         "signs": "The Qur'an calls these hills 'signs'. Here are 5 words to see them.", "every": "Every step up this mountain was in the Qur'an."}
T = "#quran #learnarabic #hiking #peakdistrict #muslim"
CAP = {"which": f"Kinder Scout, sunrise to hail 🏔️ Five verses walked with us, and one word from each:\n\nآيات signs · الصِّراط the path · الجِبال the mountains · يُسْر ease · حَبْل rope\n\nWhich verse would you take up a mountain? Comment 1 to 5 👇\n\n{T}",
       "save": f"We climbed Kinder Scout in sun, fog and hail, and these five verses kept coming back 🏔️ Swipe for one Arabic word from each.\n\nSave it for your next walk, and tell me which one you'd take: 1 to 5 👇\n\n{T}"}
Q1 = {"stop": {"type": "score", "instructions": "`ctx` Cover slide line: `h`. Viewer: `who`. How likely are they to stop and swipe?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
      "fair": {"type": "score", "instructions": "`ctx` Cover slide line: `h`. Is it accurate, respectful and paid off by the slides?", "criteria": ["No", "Partly", "Mostly", "Fully"]}}
Q2 = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
      "fair": {"type": "score", "instructions": "`ctx` Caption: `h`. Is it accurate and respectful?", "criteria": ["No", "Partly", "Mostly", "Fully"]}}
import os
for D, Q, tag in (((COVER, Q1, "cover"), (CAP, Q2, "caption")) if not os.environ.get("PART2") else ()):
    jobs = [(k, w) for k in D for w in WHO for _ in range(2)]
    with ThreadPoolExecutor(18) as ex: r = list(ex.map(lambda j: (j, ask({"ctx": CTX, "h": D[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
    for k in D:
        s = {q: round(sum(a[q]["score"] for (kk, _), a in r if kk == k) / 6, 2) for q in Q}
        print(tag, k, s, round(sum(s.values()), 2))

# Part 2 (15 Nov 2026): water 21:30 (stream at sunset), hawnan 25:63 (walking the stone path), sahab 24:43 (clouds over the ridge),
# ash-shams 91:1 (sunrise over the valley), nawm 78:9 (sleeping under a rock at night).
CTX2 = CTX.replace("(sunrise, fog, hail, a group at the summit)", "(a stream at sunset, walking a stone path, clouds over the ridge, sunrise, sleeping out under a rock at night)").replace(
    "(ayat signs 3:190, as-sirat the path 1:6, al-jibal the mountains 27:88, yusr ease 94:6, habl rope 3:103)", "(al-ma' water 21:30, hawnan gently 25:63, sahab clouds 24:43, ash-shams the sun 91:1, nawm sleep 78:9)")
COVER2 = {"rock": "We slept under a rock on Kinder Scout. 5 Qur'an words from that night.", "more": "5 more Qur'an words from the top of Kinder Scout",
          "night": "One night on a mountain, 5 words from the Qur'an", "sleep": "Why the Qur'an calls your sleep a rest (and 4 more words from Kinder Scout)"}
CAP2 = {"night": f"Part 2 from Kinder Scout 🌄 A stream at sunset, clouds rolling over the ridge, and a night sleeping under a rock. Five verses, one Arabic word from each.\n\nWhich one is your favourite? 1 to 5 👇\n\n{T}",
        "save": f"We slept out under a rock on Kinder Scout, and woke to this 🌄 Swipe for five verses and one Arabic word from each.\n\nSave it, and tell me which word you didn't know: 1 to 5 👇\n\n{T}"}
for D, Q, tag in ((COVER2, Q1, "cover2"), (CAP2, Q2, "caption2")):
    jobs = [(k, w) for k in D for w in WHO for _ in range(2)]
    with ThreadPoolExecutor(18) as ex: r = list(ex.map(lambda j: (j, ask({"ctx": CTX2, "h": D[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
    for k in D:
        s = {q: round(sum(a[q]["score"] for (kk, _), a in r if kk == k) / 6, 2) for q in Q}
        print(tag, k, s, round(sum(s.values()), 2))
