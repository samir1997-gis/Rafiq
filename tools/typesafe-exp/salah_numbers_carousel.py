# Hook (slide 1) for the "20 words = over half your salah" carousel (owner, 11 Oct 2026): a Quran-difficulty hook, then the numbers.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/salah_numbers_carousel.py
# Result (11 Oct; swipe/share/trust, 3 viewers x 2): '20 words = over half of your salah' 7.81 (most trusted) · 'Think understanding
#   the Quran is too hard?' 7.42 (the owner's ask: the cover, with the 20-words cover as sn-1-alt) · combining the two 7.33 (trust drops:
#   it mixes up the Quran and the salah) · 'Do you understand what you're saying?' 7.28 · 'takes years… your salah says otherwise' 6.91.
# Caption (engage/spoil/trust): B_short 7.42 · C_honest 7.12 · A_hook 6.10 (giving the numbers away leaves no reason to swipe).
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 7-slide Instagram/TikTok carousel from Rafiq, a small Arabic-learning account. After slide 1, it shows: a four-rakah prayer is 425 words "
       "but only 90 different ones; 5 words are a third of it; the top 20 are over half, listed with how often each is said; you recite Al-Fatiha "
       "17 times a day; ends with 'save this, send it to someone who thinks Arabic is too hard'. Slide 1 is the hook on its own, with this text: ")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has wanted to understand the Quran for years",
       "revert": "a 30-year-old revert learning to pray"}
H = {"A_hard": "Think understanding the Quran is too hard? Swipe →",
     "B_most": "Most Muslims think understanding the Quran takes years. Your salah says otherwise →",
     "C_20": "20 words = over half of your salah. Swipe →",
     "D_dont": "You pray 5 times a day. Do you understand what you're saying? →",
     "E_combo": "Think the Quran is too hard to understand? 20 words are over half of your salah →"}
Q = {"swipe": {"type": "score", "instructions": "`ctx` `h`. Viewer: `who`. How likely are they to swipe to slide 2?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "share": {"type": "score", "instructions": "`ctx` `h`. Viewer: `who`. How likely are they to save or share the carousel?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` `h`. Viewer: `who`. Does the hook feel honest about what the carousel delivers (not clickbait)?", "criteria": ["Clickbait", "A bit misleading", "Mostly honest", "Honest"]}}
jobs = [(k, w) for k in H for w in WHO for _ in range(2)]
with ThreadPoolExecutor(15) as ex: res = list(ex.map(lambda j: (j[:2], ask({"ctx": CTX, "h": H[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>8}" for q in Q) + "   total")
for k in H:
    s = {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / (2 * len(WHO)) for q in Q}
    print(f"{k:10}" + "".join(f"{s[q]:8.2f}" for q in Q) + f"{sum(s.values()):8.2f}")

# Caption (same carousel, cover A). Result at the top.
CAP = {"A_hook": "Think understanding the Quran is too hard? 🤍 Start with the part you already recite 17 times a day. One four-rakʿah prayer is 425 words, but only 90 different ones, and 20 of them are over half of everything you say. Save this 📌 and send it to someone who thinks Arabic is too hard. #quran #salah #learnarabic #arabic #muslim #islam",
       "B_short": "Think understanding the Quran is too hard? Count the words in your salah first 👀 Swipe to the end, then save it 📌 for your next prayer. Which of the 20 did you already know? 👇 #quran #salah #learnarabic #arabic #muslim #islam",
       "C_honest": "Think understanding the Quran is too hard? 🤍 It's a big book, but your salah isn't. We counted every word of a four-rakʿah prayer: swipe to see how few words it really takes. Save it 📌 and send it to someone you pray with. #quran #salah #learnarabic #arabic #muslim #islam"}
QC = {"engage": {"type": "score", "instructions": "`ctx` Cover: Think understanding the Quran is too hard? Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
      "spoil": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. Does the caption give away so much that there's no reason to swipe?", "criteria": ["Gives it all away", "Gives a lot away", "A little", "Nothing, makes you swipe"]},
      "trust": Q["trust"]}
if __name__ == "__main__":
    jobs = [(k, w) for k in CAP for w in WHO for _ in range(2)]
    with ThreadPoolExecutor(15) as ex: res = list(ex.map(lambda j: (j[:2], ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, QC)["answers"]), jobs))
    for k in CAP:
        s = {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / (2 * len(WHO)) for q in QC}
        print(f"{k:10}" + "".join(f"{s[q]:8.2f}" for q in QC) + f"{sum(s.values()):8.2f}")
