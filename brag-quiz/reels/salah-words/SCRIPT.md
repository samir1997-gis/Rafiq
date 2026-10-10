# 5 words make up a third of your salah (talking to camera, about 40 s)

Edited with the reel template (`brag-quiz/reels/template/`): flicker hook, titles behind the head, the word-wall panel.
Numbers from the app's own data: every word of a four-rakah prayer (`salah-data.js`) times how often it's said (`salah.js` REPS),
not counting the surah you choose after al-Fatiha.

**1. Hook** *(flicker; on screen: "5 WORDS = ⅓ OF YOUR SALAH")*
Did you know **five** words make up a **third** of your salah?

**2. The objection** *(title behind the head: "NOT YEARS")*
Most people think understanding their salah means **years** of studying Arabic. It doesn't have to start that way.

**3. The numbers** *(word wall: 425 squares, the repeats light up)*
I counted every word of a four-rakah prayer. It's **425** words, but only **90** different ones.
The same words come back again and again.

**4. The five** *(the five words appear one by one, each with its meaning)*
سُبْحانَ, glory be to. رَبِّيَ, my Lord. اللَّهُ, Allah. الْأَعْلى, the Most High. أَكْبَرُ, is the Greatest.
Those five alone are **a third** of everything you say.

**5. The twenty** *(the wall fills to 56%)*
Learn the top **twenty**, and you understand **more than half** of your salah.

**6. Honest close**
It's not the whole language. But it's a real start, and you'll feel it in your very next prayer.

**7. Ending**
Follow, and I'll teach you those twenty words, **one at a time**.

---
TypeSafe (`tools/typesafe-exp/salah_words_talk.py`): the three hooks are close ("5 words make up a third" 9.61, "did you know you can
understand your salah without years" 9.53, "425 words, only 90 different" 9.47); a follow ending beats an app ending, which drops
trust (1.12 vs 1.52). Trust is the weak spot for all of them, so the script says where the numbers come from and that it's a start.

**Numbers** (four-rakah prayer, without the surah): 425 words, 90 different; top 5 = 34%, top 10 = 45%, top 20 = 56%.
Top 5 by count: سُبْحانَ 36, رَبِّيَ 36, اللَّهُ 28, الْأَعْلى 24, أَكْبَرُ 22.

**Follow-up series this sets up:** one short video per word of the top 20 (the generated "salah word by word" format).
