# Five in the formula (#244)

Built by `brag-quiz/build_formula2.py`, following `IDEAS.md` ("What our best videos do"):
- a question about something they already say, big in the middle of the first frame (use it as the cover)
- one pattern that unlocks several words
- a "your turn" round with a 3-2-1
- a comment anyone can answer
- 20-23 s
- the app card on one of the five only

Sound: the app's reading voice, a soft tap as things appear and a chime on the answer, no fountain bed.
Levelled to about -16 LUFS.

| # | Video | Hook | Pattern | Your turn | Ends on |
|---|---|---|---|---|---|
| 1 | `out/p4-hamd/p4-hamd.mp4` | Why do Muhammad, Ahmad and al-ḥamdu sound alike? | ح م د = praise | مَحْمُود → praised | Tag a Muhammad, Ahmad or Mahmoud |
| 2 | `out/p1-akbar/p1-akbar.mp4` | Why "Allāhu akbar", not "Allāhu kabīr"? | أَـ + root = the most… | عَلِيّ → high, exalted | What do you say 33 times after salah? |
| 3 | `out/p5-insha/p5-insha.mp4` | What does in shā' Allāh actually say? | إِنْ if · شاءَ willed · اللهُ | ما شاءَ اللهُ → what Allah has willed | When do you say mā shā' Allāh? |
| 4 | `out/p2-ana/p2-ana.mp4` | What's the أَ at the start of أَشْهَدُ? | أَـ at the start = I | أَكْتُبُ → I write | What do you say before you read the Quran? **+ app card** |
| 5 | `out/p3-li/p3-li.mp4` | What's the "li" in al-ḥamdu lillāh? | لِ / لَ = for, to | لِي in رَبِّ اغْفِرْ لِي → (for) me | Someone sneezes and says al-ḥamdu lillāh: what do you reply? |

Post in that order: the one app post sits fourth.

## Where it comes from
- **salah-data.js:**
  - أَكْبَرُ "is the Greatest", الْأَعْلى "the Most High"
  - أَشْهَدُ "I bear witness", أَعُوذُ "I seek refuge"
  - لِلَّهِ "are for Allah", وَلَكَ "and to You (belongs)", لِي "me" in رَبِّ اغْفِرْ لِي
- **vocab-data.js:** كَبِير 161 "big", إِنْ شاءَ اللهُ 233 "God willing", ما شاءَ اللهُ 71 "what God has willed".
- **toolkit-data.js:** أَذْهَبُ "I go", أَكْتُبُ "I write", كَتَبَ "to write".
- Every Arabic word is the app's own recording; nothing from the Quran is voiced.
- **Worth a glance from the teacher (general knowledge, written for these):**
  - أَكْبَرُ is كَبِير in the "most" pattern (أَفْعَل).
  - عَلِيّ "high, exalted", from ع ل ي like الْأَعْلى.
  - أَـ at the start of a present verb = "I".
  - لِـ / لَـ = "for, to", and لِي "(for) me".
  - The names: مُحَمَّد "the praised one", أَحْمَد "most praiseworthy", مَحْمُود "praised", all from ح م د "praise".
  - إِنْ "if", شاءَ "(He) willed".

Not checked with TypeSafe (no key in this session): check the captions with it before posting (CLAUDE.md).

## Captions (say the question; the ask is the last line)

**1 · p4-hamd**: *Why do Muhammad, Ahmad and al-ḥamdu lillāh sound alike? ✨*
They share three letters, ḥ-m-d: praise. Al-ḥamd is praise, Muḥammad the praised one, Aḥmad the most praiseworthy. So what does Maḥmūd mean? Tag a Muhammad, Ahmad or Mahmoud 👇 Follow for a new Arabic word every week. #arabicnames #muhammad #learnarabic #arabic #islam #muslim

**2 · p1-akbar**: *Why "Allāhu akbar" and not "Allāhu kabīr"? 🤔*
Kabīr means big. Akbar means the Greatest: the same letters with أَ in front. You hear it again in sujūd: al-aʿlā, the Most High… and in the name ʿAlī, high, exalted. What do you say 33 times after salah? Comment it 👇 Follow for a new word from your salah every week. #salah #allahuakbar #learnarabic #arabic #islam #muslim

**3 · p5-insha**: *What does "in shā' Allāh" actually say? 🤲*
In is "if", shā'a is "willed": "if Allah wills." And mā shā' Allāh? Mā is "what": "what Allah has willed." When do you say mā shā' Allāh? Comment it 👇 Send this to someone learning Arabic. #inshallah #mashallah #learnarabic #arabic #islam #muslim

**4 · p2-ana** (the app post): *What's the أَ at the start of ashhadu? ☝️*
Ashhadu, I bear witness. Aʿūdhu, I seek refuge. Adhhabu, I go. One letter at the start means "I". So what's aktubu? 👀 What do you say before you read the Quran? Comment it 👇 Every verb from I to we is in Rafiq: free week, link in bio. #learnarabic #arabic #arabicgrammar #salah #muslim #arabicforbeginners

**5 · p3-li**: *What's the "li" in al-ḥamdu lillāh? 🤲*
Li means "for": al-ḥamdu lillāh, all praise is for Allah. Rabbanā wa laka l-ḥamd: and to You belongs the praise. So in rabbi-ghfir lī, lī is "(for) me": "My Lord, forgive me." Someone sneezes and says al-ḥamdu lillāh: what do you reply? 👇 Send this to someone who says it every day. #alhamdulillah #salah #learnarabic #arabic #islam #muslim
