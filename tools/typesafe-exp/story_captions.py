# Captions for "the story of a word" (26 Oct 2026, #296; h3-lisan the Dune edition, 28 Oct, #303): h1-algebra and h2-coffee, the pastel doodle look, in the Callum standard.
# Each caption repeats the hook and keeps the quiz answer back (no "mend", no "café").
# Not run yet: no TYPE_SAFE_KEY in the session that made them (#262).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/story_captions.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = {
 "algebra": ("A TikTok/Instagram Reel from a small account teaching the Arabic Muslims use, on a pastel page with hand-drawn doodles. A voice says "
             "'Algebra is named after an Arabic word for setting broken BONES!'; al-jabr means putting broken pieces back together; al-Khwarizmi's "
             "book in Baghdad around 820; Europe turned it into algebra and his name into algorithm; then a quiz on a word from the dua between "
             "the two sujood (and forgive me / and mend me / and guide me?), 3-2-1. Ends: 'What do you say between the two sujood? Comment below!' "
             "Caption under it: "),
 "coffee": ("A TikTok/Instagram Reel from a small account teaching the Arabic Muslims use, on a pastel page with hand-drawn doodles. A voice says "
            "'The Arabic word for coffee used to mean WINE!'; old Arabic dictionaries say qahwa meant wine because it puts you off your food; Sufis "
            "in Yemen in the 1400s drank coffee to stay awake for night prayers and the name moved over; it travelled to Istanbul, the Dutch and "
            "English by 1582; then a quiz: masjid is the place of sujood, so what is a maqha (coffee pot / cafe / coffee bean?), 3-2-1. Ends: "
            "'How do you take yours? Comment below!' Caption under it: "),
 "lisan": ("A TikTok/Instagram Reel from a small account teaching the Arabic Muslims use, on a drawn desert page (dunes, sand blowing, a worm). "
           "A voice says 'Everyone in Dune chants Lisan al-Gaib... but what does it actually mean in Arabic?'; lisan means tongue and language "
           "(the Qur'an came down in a clear Arabic tongue); a quiz on al-ghayb from the first page of al-Baqarah (the desert / the unseen / "
           "the future?), 3-2-1; so it's 'the tongue of the unseen'; Frank Herbert didn't invent it: the Persian poet Hafez was called that over "
           "500 years earlier. Ends: 'Which Dune word should I do next: Muad'Dib, or Usul? Comment below!' Caption under it: "),
 "khutbah": ("A TikTok/Instagram Reel posted on a Friday from a small account teaching the Arabic Muslims use, pastel page with doodles. A voice says "
             "'The imam giving your Friday khutbah... and your fiancé... have the same name in Arabic' (khatib); both from khataba, to address; khutbah "
             "(sermon) and khitbah (marriage proposal) differ by one vowel mark; then a quiz on a phrase from al-Baqarah 2:235, sermon or proposal?, 3-2-1. "
             "Ends: 'Send this to someone who's getting married, and comment: did you spot it?' Caption under it: ")}
C = {
 "algebra/question": ("algebra", "Algebra is named after an Arabic word for setting broken bones 🦴 Can you guess what وَاجْبُرْنِي means before the 3-2-1? Then tell me: what do you say between the two sujood? 👇 #learnarabic #arabic #etymology #history #muslimtiktok"),
 "algebra/share": ("algebra", "Your maths teacher never told you this 🦴📐 Algebra comes from an Arabic word for setting broken bones. Send this to someone who hated maths 😅 #learnarabic #arabic #etymology #history #muslimtiktok"),
 "coffee/question": ("coffee", "The Arabic word for coffee used to mean… wine?! ☕ Guess what a مَقْهى is before the 3-2-1, then tell me how you take yours 👇 #learnarabic #arabic #coffee #etymology #muslimtiktok"),
 "khutbah/question": ("khutbah", "Your imam and your fiancé have the same name in Arabic 🕌💍 Can you spot the one mark that turns a sermon into a proposal? Guess before the 3-2-1 👇 #jumuah #learnarabic #arabic #khutbah #muslimtiktok"),
 "khutbah/share": ("khutbah", "Jumuʿah Mubarak 🤍 One tiny mark: a sermon or a marriage proposal? Send this to someone who's getting married 💍 #jumuah #learnarabic #arabic #khutbah #muslimtiktok"),
 "lisan/question": ("lisan", "Everyone chants Lisan al-Gaib… but what does it actually mean in Arabic? 🏜️ Guess before the 3-2-1, then tell me: Muad'Dib or Usul next? 👇 #dune #duneparttwo #learnarabic #arabic #lisanalgaib"),
 "lisan/fact": ("lisan", "Lisan al-Gaib is real Arabic, and it's older than Dune 🏜️ Did you know which part is from the Qur'an? Comment 👇 Send this to your Dune friend #dune #duneparttwo #learnarabic #arabic #lisanalgaib"),
 "coffee/share": ("coffee", "Every coffee you order is a little bit of Arabic ☕ Send this to your coffee-addict friend, and guess the last one before the 3-2-1 👇 #learnarabic #arabic #coffee #etymology #muslimtiktok"),
}
WHO = {"target": "a 27-year-old UK Muslim who prays but doesn't understand the Arabic", "revert": "a 31-year-old revert learning Arabic"}
Q = {"comment": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. How likely are they to comment?",
                 "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "share": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. How likely are they to send it to someone?",
               "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. Does the caption feel honest and interesting rather than clickbait?",
               "criteria": ["Clickbait", "A bit", "Mostly honest", "Honest and interesting"]}}
if __name__ == "__main__":
    jobs = [(k, w) for k in C for w in WHO for _ in range(2)]
    with ThreadPoolExecutor(20) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX[C[j[0]][0]], "c": C[j[0]][1], "who": WHO[j[1]]}, Q)["answers"]), jobs))
    for k in C:
        s = {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 4 for q in Q}
        print(f"{k:18} comment {s['comment']:.2f}  share {s['share']:.2f}  trust {s['trust']:.2f}  total {sum(s.values()):.2f}")
