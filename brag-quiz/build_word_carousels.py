"""Five carousels in the question-words format (owner, 19 Oct 2026: "people like the simple ones they can relate to"):
I/you/he/she/we · today/tomorrow/yesterday/now/after that · here/there/this · how are you feeling · yes/no/of course/OK.
Same look as build_questions_carousel.py: slide 1 is the English words and "Can you say all N in Arabic?", one slide per word
with the course's own example sentence (word in red), the end asks for a score. Every word and sentence is the course's own
(vocab-data.js, drills-data.js, toolkit-data.js, scenes-data.js) except أَنا مَشْغُولٌ and أَنا سَعِيدٌ هُنا (trimmed from
"وَأَنا سَعِيدٌ هُنا"). Pure content (4 posts in 5): no app pitch.

  python3 brag-quiz/build_word_carousels.py [set ...]   ->  brag-quiz/stills/<set>/<set>-1.png ...
"""
import os, sys
from playwright.sync_api import sync_playwright
import build_salah_numbers as S
import build_questions_carousel as QC

# set id: (cover question, [(English, Arabic, transliteration, [(sentence, word to colour, transliteration, English)], note)])
SETS = {
 "pronouns": ("Can you say all 6<br>in Arabic? 👀", [
   ("I", "أَنا", "anā", [("أَنا مِنَ الْمَغْرِبِ. وَأَنْتَ؟", "أَنا", "anā mina l-maghribi. wa anta?", "I'm from Morocco. And you?")], ""),
   ("you (to a man)", "أَنْتَ", "anta", [("هَلْ أَنْتَ طالِبٌ؟", "أَنْتَ", "hal anta ṭālibun?", "Are you a student?")], ""),
   ("you (to a woman)", "أَنْتِ", "anti", [("نَعَمْ، أَنا طالِبَةٌ. وَأَنْتِ؟", "أَنْتِ", "naʿam, anā ṭālibatun. wa anti?", "Yes, I'm a student. And you?")],
    "Two words for “you”: one for a man, one for a woman."),
   ("he", "هُوَ", "huwa", [("جَدِّي فِي المَسْجِدِ. هُوَ يُصَلِّي.", "هُوَ", "jaddī fi l-masjidi. huwa yuṣallī.", "My grandfather is in the mosque. He's praying.")], ""),
   ("she", "هِيَ", "hiya", [("جَدَّتِي فِي الغُرْفَةِ. هِيَ تَقْرَأُ القُرْآنَ.", "هِيَ", "jaddatī fi l-ghurfati. hiya taqra'u l-qur'ān.", "My grandmother is in the room. She's reading the Qur'an.")], ""),
   ("we", "نَحْنُ", "naḥnu", [("نَحْنُ نُصَلِّي فِي الْمَسْجِدِ.", "نَحْنُ", "naḥnu nuṣallī fi l-masjid.", "We pray in the mosque.")],
    "You say “we” in every prayer: the نَـ in نَعْبُدُ (“we worship”).")]),
 "time": ("Can you say all 5<br>in Arabic? 👀", [
   ("today", "الْيَوْمَ", "al-yawma", [("كَيْفَ الْجَوُّ الْيَوْمَ؟", "الْيَوْمَ", "kayfa l-jawwu l-yawm?", "How's the weather today?")], ""),
   ("tomorrow", "غَدًا", "ghadan", [("إِنْ شاءَ اللهُ أَزُورُكَ غَدًا.", "غَدًا", "in shā' Allāhu azūruka ghadan.", "God willing, I'll visit you tomorrow.")], ""),
   ("yesterday", "أَمْسِ", "amsi", [("كانَ الْجَوُّ بارِدًا أَمْسِ.", "أَمْسِ", "kāna l-jawwu bāridan amsi.", "The weather was cold yesterday.")], ""),
   ("now", "الآنَ", "al-āna", [("صَحِيحٌ. أَتَوَضَّأُ الآنَ.", "الآنَ", "ṣaḥīḥ. atawaḍḍa'u l-āna.", "True. I'll do wudu now.")], ""),
   ("after that", "بَعْدَ ذَلِكَ", "baʿda dhālika", [("بَعْدَ ذَلِكَ أَذْهَبُ إِلى الْعَمَلِ.", "بَعْدَ ذَلِكَ", "baʿda dhālika adh-habu ila l-ʿamal.", "After that I go to work.")],
    "Answer in the comments: what do you do after Fajr? 👇")]),
 "here-this": ("Can you say all 4<br>in Arabic? 👀", [
   ("here", "هُنا", "hunā", [("أَنا طَبِيبٌ، وَبَيْتِي هُنا.", "هُنا", "anā ṭabībun, wa baytī hunā.", "I'm a doctor, and my house is here.")], ""),
   ("there", "هُناكَ", "hunāka", [("كَيْفَ الجَوُّ هُناكَ؟", "هُناكَ", "kayfa l-jawwu hunāk?", "How's the weather there?")], ""),
   ("this (for a man)", "هَذا", "hādhā", [("هَذا أَبِي. هُوَ مُهَنْدِسٌ.", "هَذا", "hādhā abī. huwa muhandis.", "This is my father. He's an engineer."),
                                          ("بِكَمْ هَذا الْقَمِيصُ؟", "هَذا", "bikam hādhā l-qamīṣ?", "How much is this shirt?")], ""),
   ("this (for a woman)", "هَذِهِ", "hādhihi", [("هَذِهِ أُمِّي. هِيَ مُعَلِّمَةٌ.", "هَذِهِ", "hādhihi ummī. hiya muʿallimah.", "This is my mother. She's a teacher.")],
    "Two words for “this”: one for a man, one for a woman.")]),
 "feelings": ("How are you feeling?<br>Say all 4 in Arabic 👀", [
   ("happy", "سَعِيد", "saʿīd", [("أَنا سَعِيدٌ هُنا.", "سَعِيدٌ", "anā saʿīdun hunā.", "I'm happy here.")], ""),
   ("hungry", "جَوْعان", "jawʿān", [("أَنا جَوْعانُ جِدّاً.", "جَوْعانُ", "anā jawʿānu jiddan.", "I'm very hungry."),
                                    ("لا يا أُمِّي. أَنا جَوْعانَةٌ.", "جَوْعانَةٌ", "lā yā ummī. anā jawʿānah.", "No, mum. I'm hungry. (a woman)")], ""),
   ("ill", "مَرِيض", "marīḍ", [("أَنا مَرِيضٌ قَلِيلاً.", "مَرِيضٌ", "anā marīḍun qalīlan.", "I'm a little ill.")], ""),
   ("busy", "مَشْغُول", "mashghūl", [("أَنا مَشْغُولٌ.", "مَشْغُولٌ", "anā mashghūl.", "I'm busy.")],
    "How are you feeling today? Answer in Arabic 👇")]),
 "yes-no": ("Can you say all 4<br>in Arabic? 👀", [
   ("yes", "نَعَمْ", "naʿam", [("نَعَمْ، هَذا أَخِي. وَهَذِهِ أُخْتِي.", "نَعَمْ", "naʿam, hādhā akhī. wa hādhihi ukhtī.", "Yes, this is my brother. And this is my sister.")], ""),
   ("no / not", "لا", "lā", [("لا يا أُمِّي. أَنا جَوْعانَةٌ.", "لا", "lā yā ummī. anā jawʿānah.", "No, mum. I'm hungry."),
                            ("فِي الْحَقِيقَةِ لا أَعْرِفُ.", "لا", "fi l-ḥaqīqati lā aʿrif.", "Actually, I don't know.")],
    "Before a verb, it means “not”."),
   ("of course", "طَبْعًا", "ṭabʿan", [("طَبْعًا! نَتَوَضَّأُ فِي الْبَيْتِ، ثُمَّ نَمْشِي مَعًا.", "طَبْعًا", "ṭabʿan! natawaḍḍa'u fi l-bayti, thumma namshī maʿan.", "Of course! We'll do wudu at home, then walk together.")], ""),
   ("OK / fine", "طَيِّب", "ṭayyib", [("طَيِّبٌ، أُرِيدُ كِيلُو بُرْتُقالٍ.", "طَيِّبٌ", "ṭayyib, urīdu kīlū burtuqāl.", "Fine, I'd like a kilo of oranges.")],
    "Yes or no? Reply in Arabic in the comments 👇")]),
 # numbers 1-10 with the salah link (IDEAS "next in the series"; owner 20 Oct 2026): the course's own words (vocab-data.js) and sentences
 # (drills-data.js; 10 from scenes-data.js); 2 shows the dual instead (Arabic says "two sisters" with an ending, not the number)
 "numbers": ("Can you count to 10<br>in Arabic? 👀", [
   ("1 · one", "واحِد", "wāḥid · ١", [("الشَّقَّةُ فِي الدَّوْرِ الأَوَّلِ، وَرَقْمُها واحِدٌ.", "واحِدٌ", "ash-shaqqatu fi d-dawri l-awwali, wa raqmuhā wāḥid.",
    "The flat is on the first floor, and its number is one.")], "Another “one”: أَحَد, in قُلْ هُوَ اللَّهُ أَحَدٌ."),
   ("2 · two", "اثْنانِ", "ithnān · ٢", [("عِنْدِي ثَلاثَةُ إِخْوَةٍ وَأُخْتانِ.", "أُخْتانِ", "ʿindī thalāthatu ikhwatin wa ukhtān.", "I have three brothers and two sisters.")],
    "For two, Arabic adds an ending instead: أُخْتانِ, two sisters. Fajr is رَكْعَتانِ, two rakʿahs."),
   ("3 · three", "ثَلاثَة", "thalātha · ٣", [("عِنْدِي ثَلاثَةُ دُرُوسٍ: الْقِراءَةُ، وَالنَّحْوُ، وَالْمُحادَثَةُ.", "ثَلاثَةُ", "ʿindī thalāthatu durūs: al-qirā'a, wa n-naḥw, wa l-muḥādatha.",
    "I have three lessons: reading, grammar and conversation.")], "Maghrib: three rakʿahs."),
   ("4 · four", "أَرْبَعَة", "arbaʿa · ٤", [("اسْأَلْنِي أَرْبَعَةَ أَسْئِلَةٍ عَنْ نَفْسِي.", "أَرْبَعَةَ", "is'alnī arbaʿata as'ilatin ʿan nafsī.", "Ask me four questions about myself.")],
    "Dhuhr, ʿAsr and ʿIshāʾ: four rakʿahs each."),
   ("5 · five", "خَمْسَة", "khamsa · ٥", [("رَقْمُ البَيْتِ خَمْسَةٌ.", "خَمْسَةٌ", "raqmu l-bayti khamsa.", "The house number is five.")], "Five prayers a day."),
   ("6 · six", "سِتَّة", "sitta · ٦", [("الْبُرْتُقالُ بِسِتَّةِ رِيالاتٍ لِلْكِيلُو، وَهُوَ طازَجٌ.", "سِتَّةِ", "al-burtuqālu bi-sittati riyālātin li-l-kīlū, wa huwa ṭāzaj.",
    "Oranges are six riyals a kilo, and they're fresh.")], ""),
   ("7 · seven", "سَبْعَة", "sabʿa · ٧", [("فِي أُسْرَتِي سَبْعَةُ أَوْلادٍ.", "سَبْعَةُ", "fī usratī sabʿatu awlād.", "In my family there are seven children.")],
    "al-Fātiḥah has seven verses."),
   ("8 · eight", "ثَمانِيَة", "thamāniya · ٨", [("أَعْمَلُ ثَمانِيَ ساعاتٍ فِي اليَوْمِ.", "ثَمانِيَ", "aʿmalu thamāniya sāʿātin fi l-yawm.", "I work eight hours a day.")],
    "Numbers 3 to 10 work backwards: with a feminine word like ساعَة (hour), the ة goes."),
   ("9 · nine", "تِسْعَة", "tisʿa · ٩", [("فِي أُسْرَتِي تِسْعَةُ أَوْلادٍ، وَكُلُّهُمْ طُلَّابٌ.", "تِسْعَةُ", "fī usratī tisʿatu awlādin, wa kulluhum ṭullāb.",
    "In my family there are nine children, and they're all students.")], ""),
   ("10 · ten", "عَشَرَة", "ʿashara · ١٠", [("بَعْدَ عَشْرِ دَقائِقَ.", "عَشْرِ", "baʿda ʿashri daqā'iq.", "In ten minutes.")],
    "The digits you write are called “Arabic numerals”. In Arabic: 1 = ١ · 2 = ٢ · 3 = ٣ · 10 = ١٠"),
 ]),
 # colours (IDEAS "next in the series"; owner 21 Oct 2026): the course's own words (vocab-data.js), sentences (drills-data.js: the
 # thobe/car templates, the "five things in your house" answer, the shop dialogue) and its rule (essentials-data.js: the second form
 # is for feminine nouns). Notes: the Green Dome, al-Baqarah 2:69, the Black Stone.
 "colours": ("Can you say all 6<br>in Arabic? 👀", [
   ("red", "أَحْمَر · حَمْراء", '<i class="sw" style="background:#c0392b"></i> aḥmar · ḥamrāʾ (f)', [("هَذا ثَوْبٌ أَحْمَرُ.", "أَحْمَرُ", "hādhā thawbun aḥmar.", "This is a red thobe."),
                                                    ("هَذِهِ سَيَّارَةٌ حَمْراءُ.", "حَمْراءُ", "hādhihi sayyāratun ḥamrā'.", "This is a red car.")],
    "Every colour has a second form for feminine words: حَمْراء, like سَيَّارَةٌ حَمْراءُ (a red car)."),
   ("blue", "أَزْرَق · زَرْقاء", '<i class="sw" style="background:#2f6fb5"></i> azraq · zarqāʾ (f)', [("وَهَلْ عِنْدَكَ قَمِيصٌ أَزْرَقُ؟", "أَزْرَقُ", "wa hal ʿindaka qamīṣun azraq?", "And do you have a blue shirt?"),
                                                      ("السَّيَّارَةُ زَرْقاءُ.", "زَرْقاءُ", "as-sayyāratu zarqā'.", "The car is blue.")], ""),
   ("green", "أَخْضَر · خَضْراء", '<i class="sw" style="background:#2e7d4f"></i> akhḍar · khaḍrāʾ (f)', [("الْقَمِيصُ أَخْضَرُ.", "أَخْضَرُ", "al-qamīṣu akhḍar.", "The shirt is green.")],
    "The Green Dome in Madinah: الْقُبَّةُ الْخَضْراءُ."),
   ("yellow", "أَصْفَر · صَفْراء", '<i class="sw" style="background:#e9b949"></i> aṣfar · ṣafrāʾ (f)', [("الثَّوْبُ أَصْفَرُ.", "أَصْفَرُ", "ath-thawbu aṣfar.", "The thobe is yellow.")],
    "In al-Baqarah (2:69), the cow is بَقَرَةٌ صَفْراءُ: a yellow cow."),
   ("white", "أَبْيَض · بَيْضاء", '<i class="sw" style="background:#ffffff"></i> abyaḍ · bayḍāʾ (f)', [("هَذا ثَوْبٌ أَبْيَضُ جَمِيلٌ.", "أَبْيَضُ", "hādhā thawbun abyaḍu jamīl.", "This is a beautiful white thobe."),
                                                       ("السَّيَّارَةُ بَيْضاءُ.", "بَيْضاءُ", "as-sayyāratu bayḍā'.", "The car is white.")], ""),
   ("black", "أَسْوَد · سَوْداء", '<i class="sw" style="background:#17262b"></i> aswad · sawdāʾ (f)', [("الْمِظَلَّةُ سَوْداءُ.", "سَوْداءُ", "al-miẓallatu sawdā'.", "The umbrella is black.")],
    "The Black Stone of the Kaaba: الْحَجَرُ الْأَسْوَدُ."),
 ]),
 # family (IDEAS "next in the series: family words", owner 28 Oct 2026, #305): the course's own words (vocab-data.js 50, 46, 32, 33, 52, 53) and
 # sentences (drills-data.js); notes: al-Bukhārī 5971, Maryam 19:42, al-Ḥujurāt 49:10, عَمّ / خال (as in f4-family), the ة for feminine
 "family": ("Can you say all 6<br>in Arabic? 👀", [
   ("mum", "أُمّ", "umm", [("شُكْراً يا أُمِّي.", "أُمِّي", "shukran yā ummī.", "Thank you, mum.")],
    "Who deserves your best company? «أُمُّكَ»: your mother, three times, then your father (al-Bukhārī 5971)."),
   ("dad", "أَب", "ab", [("نَعَمْ يا أَبِي. هَيَّا بِنا إِلى المَسْجِدِ.", "أَبِي", "naʿam yā abī. hayyā binā ila l-masjid.", "Yes, dad. Let's go to the mosque.")],
    "Ibrāhīm calls his father يا أَبَتِ: “O my father” (Maryam 19:42)."),
   ("brother", "أَخ", "akh", [("أَخِي فِي الحَمَّامِ. هُوَ يَتَوَضَّأُ.", "أَخِي", "akhī fi l-ḥammām. huwa yatawaḍḍa'.", "My brother is in the bathroom. He's doing wudu.")],
    "إِنَّمَا الْمُؤْمِنُونَ إِخْوَةٌ: “the believers are brothers” <b style=\"white-space:nowrap;font:inherit\">(al-Ḥujurāt 49:10)</b>."),
   ("sister", "أُخْت", "ukht", [("هَذا أَخِي الصَّغِيرُ، وَهَذِهِ أُخْتِي الْكَبِيرَةُ.", "أُخْتِي", "hādhā akhi ṣ-ṣaghīr, wa hādhihi ukhti l-kabīrah.",
    "That's my little brother, and this is my big sister.")], "أَخ → أُخْت: a ت on the end, and he's a she."),
   ("grandpa", "جَدّ", "jadd", [("جَدِّي فِي الْحَدِيقَةِ مَعَ عَمِّي.", "جَدِّي", "jaddī fi l-ḥadīqati maʿa ʿammī.", "My grandad is in the garden with my uncle.")],
    "عَمِّي is your dad's brother. Your mum's brother is خالِي."),
   ("grandma", "جَدَّة", "jadda", [("جَدَّتِي تَسْكُنُ قَرِيبًا مِنَّا.", "جَدَّتِي", "jaddatī taskunu qarīban minnā.", "My grandma lives near us.")],
    "جَدّ → جَدَّة: add ة and grandpa becomes grandma. Who do you call most? Comment in Arabic 👇"),
 ]),
 # the little words (IDEAS "next in the series: and/but/with/in", owner 30 Oct 2026, #308): the course's own words (vocab-data.js 39, 85, 244, 84;
 # toolkit-data.js لَكِنْ, مِنْ) and sentences (toolkit-data.js, drills-data.js); notes: al-Fātiḥah 1:5, the لَكِنْ / لَكِنَّ rule (toolkit-data.js),
 # al-Baqarah 2:153, 2:201, the taʿawwudh, 2:156
 "little": ("Can you say all 6<br>in Arabic? 👀", [
   ("and", "وَ", "wa", [("أَدْرُسُ الْعَرَبِيَّةَ وَالتَّارِيخَ.", "وَ", "adrusu l-ʿarabiyyata wa t-tārīkh.", "I study Arabic and history.")],
    "It joins onto the next word. You say it in every prayer: إِيّاكَ نَعْبُدُ وَإِيّاكَ نَسْتَعِينُ (1:5)."),
   ("but", "لَكِنْ", "lākin", [("أُحِبُّ الْقَهْوَةَ لَكِنْ لا أَشْرَبُها.", "لَكِنْ", "uḥibbu l-qahwata lākin lā ashrabuhā.", "I like coffee but I don't drink it.")],
    "لَكِنْ before a verb; لَكِنَّ before a noun."),
   ("with", "مَعَ", "maʿa", [("أَلْعَبُ كُرَةَ الْقَدَمِ مَعَ أَصْدِقائِي.", "مَعَ", "alʿabu kurata l-qadami maʿa aṣdiqā'ī.", "I play football with my friends.")],
    "إِنَّ اللَّهَ مَعَ الصّابِرِينَ: “Allah is with the patient” <b style=\"white-space:nowrap;font:inherit\">(al-Baqarah 2:153)</b>."),
   ("in", "فِي", "fī", [("نَجْلِسُ فِي الْبَيْتِ وَنَشْرَبُ الشَّايَ!", "فِي", "najlisu fi l-bayti wa nashrabu sh-shāy!", "We'll stay at home and drink tea!")],
    "رَبَّنا آتِنا فِي الدُّنْيا حَسَنَةً: “give us good in this world” <b style=\"white-space:nowrap;font:inherit\">(al-Baqarah 2:201)</b>."),
   ("from", "مِنْ", "min", [("اسْمِي حَمْزَةُ. مِنْ أَيْنَ أَنْتَ يا يُوسُفُ؟", "مِنْ", "ismī Ḥamza. min ayna anta yā Yūsuf?", "My name is Hamza. Where are you from, Yusuf?")],
    "Before الـ it becomes مِنَ: أَعُوذُ بِاللَّهِ مِنَ الشَّيْطانِ الرَّجِيمِ."),
   ("to", "إِلى", "ilā", [("الْيَوْمَ الْجُمُعَةُ. هَلْ تَذْهَبُ إِلى الْمَسْجِدِ؟", "إِلى", "al-yawma l-jumuʿah. hal tadh-habu ila l-masjid?", "Today is Friday. Are you going to the mosque?")],
    "إِلى + him = إِلَيْهِ: إِنّا لِلَّهِ وَإِنّا إِلَيْهِ راجِعُونَ (2:156). Which one did you know? 👇"),
 ]),
 "food": ("Can you order all 6<br>in Arabic? ☕", [
   ("water", "ماء", "māʾ", [("أُفَضِّلُ الْماءَ، مِنْ فَضْلِكَ.", "الْماءَ", "ufaḍḍilu l-māʾa, min faḍlik.", "I prefer water, please.")],
    "وَجَعَلْنا مِنَ الْماءِ كُلَّ شَيْءٍ حَيٍّ: “We made every living thing from water” <b style=\"white-space:nowrap;font:inherit\">(al-Anbiyāʾ 21:30)</b>."),
   ("bread", "خُبْز", "khubz", [("ماذا تُفَضِّلِينَ؟ خُبْزاً وَحَلِيباً؟", "خُبْزاً", "mādhā tufaḍḍilīn? khubzan wa ḥalīban?", "What would you like? Bread and milk?")],
    "In Egypt, bread is called عَيْش: “life”."),
   ("dates", "تَمْر", "tamr", [("نَعَمْ، عِنْدَنا تَمْرٌ وَكَعْكٌ.", "تَمْرٌ", "naʿam, ʿindanā tamrun wa kaʿk.", "Yes, we have dates and cake.")],
    "The Prophet ﷺ broke his fast with fresh dates, then dry dates, then sips of water <b style=\"white-space:nowrap;font:inherit\">(Abū Dāwūd 2356)</b>."),
   ("tea", "شاي", "shāy", [("أَشْرَبُ الشَّايَ وَأَقْرَأُ قَلِيلًا.", "الشَّايَ", "ashrabu sh-shāya wa aqraʾu qalīlan.", "I drink tea and read a little.")],
    "شاي and chai came from Chinese “chá” over land; English “tea” came from “tê” by sea."),
   ("milk", "حَلِيب", "ḥalīb", [("لا، أَشْرَبُ حَلِيباً. أَنا لا أُحِبُّ الشَّايَ.", "حَلِيباً", "lā, ashrabu ḥalīban. anā lā uḥibbu sh-shāy.", "No, I drink milk. I don't like tea.")],
    "The Qur'an says لَبَن: لَبَناً خالِصاً سائِغاً لِلشّارِبِينَ <b style=\"white-space:nowrap;font:inherit\">(an-Naḥl 16:66)</b>."),
   ("coffee", "قَهْوَة", "qahwa", [("وَماذا تَشْرَبُ؟ شاياً أَوْ قَهْوَةً؟", "قَهْوَةً", "wa mādhā tashrab? shāyan aw qahwa?", "And what will you drink? Tea or coffee?")],
    "قَهْوَة → Turkish kahve → Dutch koffie → coffee. So: tea or coffee? 👇"),
 ]),
 "days": ("The Arabic week is…<br>just numbers? 🤯", [
   ("Sunday", "الْأَحَد", "al-aḥad", [("أَحَد", "أَحَد", "aḥad", "one")],
    "Day one of the week. The same أَحَد as قُلْ هُوَ اللَّهُ أَحَدٌ <b style=\"white-space:nowrap;font:inherit\">(112:1)</b>."),
   ("Monday", "الِاثْنَيْن", "al-ithnayn", [("اِثْنانِ", "اِثْنانِ", "ithnān", "two")],
    "The Prophet ﷺ fasted Mondays: “the day I was born, and the day revelation came to me” <b style=\"white-space:nowrap;font:inherit\">(Muslim 1162)</b>."),
   ("Tuesday", "الثُّلاثاء", "ath-thulāthāʾ", [("ثَلاثَة", "ثَلاثَة", "thalātha", "three")],
    "Same letters ث ل ث as ثُلُث: a third."),
   ("Wednesday", "الْأَرْبِعاء", "al-arbiʿāʾ", [("أَرْبَعَة", "أَرْبَعَة", "arbaʿa", "four")],
    "Dhuhr, ʿAsr and ʿIshāʾ: أَرْبَعُ رَكَعاتٍ, four rakʿahs."),
   ("Thursday", "الْخَمِيس", "al-khamīs", [("خَمْسَة", "خَمْسَة", "khamsa", "five")],
    "Deeds are shown to Allah on Monday and Thursday, so the Prophet ﷺ fasted them <b style=\"white-space:nowrap;font:inherit\">(at-Tirmidhī 747)</b>."),
   ("Friday", "الْجُمُعَة", "al-jumuʿa", [("جَمَعَ", "جَمَعَ", "jamaʿa", "to gather: not six!")],
    "The pattern breaks: Friday is the day of gathering, مِنْ يَوْمِ الْجُمُعَةِ <b style=\"white-space:nowrap;font:inherit\">(al-Jumuʿa 62:9)</b>."),
   ("Saturday", "السَّبْت", "as-sabt", [("سُبات", "سُبات", "subāt", "rest")],
    "وَجَعَلْنا نَوْمَكُمْ سُباتاً: “We made your sleep for rest” <b style=\"white-space:nowrap;font:inherit\">(an-Nabaʾ 78:9)</b>. Which did you know? 👇"),
 ]),
 "months": ("What the Islamic months<br>actually mean 🤯", [
   ("Muḥarram", "مُحَرَّم", "month 1", [("حَرام", "حَرام", "ḥarām", "sacred, off-limits")],
    "One of the four sacred months: مِنْها أَرْبَعَةٌ حُرُمٌ <b style=\"white-space:nowrap;font:inherit\">(at-Tawbah 9:36)</b>."),
   ("Ṣafar", "صَفَر", "month 2", [("صِفْر", "صِفْر", "ṣifr", "empty")],
    "It's said the homes stood empty: everyone had gone off to travel or fight. Same letters as zero, صِفْر!"),
   ("Rabīʿ", "رَبِيع", "months 3 and 4", [("رَبِيع", "رَبِيع", "rabīʿ", "spring")],
    "There are two: رَبِيعُ الْأَوَّلِ, the first, and رَبِيعُ الْآخِرِ, the second."),
   ("Jumādā", "جُمادَى", "months 5 and 6", [("جَمَدَ", "جَمَدَ", "jamada", "to freeze")],
    "It's said the water froze. Two of these as well: الْأُولى, the first, and الْآخِرَة, the last."),
   ("Rajab", "رَجَب", "month 7", [("رَجَّبَ", "رَجَّبَ", "rajjaba", "to honour")],
    "A sacred month: “Rajab, which comes between Jumādā and Shaʿbān” <b style=\"white-space:nowrap;font:inherit\">(al-Bukhārī 4662)</b>."),
   ("Shaʿbān", "شَعْبان", "month 8", [("تَشَعَّبَ", "تَشَعَّبَ", "tashaʿʿaba", "to branch out")],
    "It's said the tribes split up and spread out. Same root: شُعُوباً, “nations” <b style=\"white-space:nowrap;font:inherit\">(al-Ḥujurāt 49:13)</b>."),
   ("Ramaḍān", "رَمَضان", "month 9", [("رَمْضاء", "رَمْضاء", "ramḍāʾ", "scorching heat")],
    "The only month named in the Qur'an: شَهْرُ رَمَضانَ الَّذِي أُنْزِلَ فِيهِ الْقُرْآنُ <b style=\"white-space:nowrap;font:inherit\">(2:185)</b>."),
   ("Shawwāl", "شَوّال", "month 10", [("عِيد", "عِيد", "ʿīd", "the 1st of Shawwāl is Eid!")],
    "Fast six days of Shawwāl after Ramadan: like fasting the whole year <b style=\"white-space:nowrap;font:inherit\">(Muslim 1164)</b>."),
   ("Dhū al-Qaʿdah", "ذُو الْقَعْدَة", "month 11", [("قَعَدَ", "قَعَدَ", "qaʿada", "to sit")],
    "It's said they sat at home: no fighting, no travel. ذُو means “the one of”."),
   ("Dhū al-Ḥijjah", "ذُو الْحِجَّة", "month 12", [("حَجّ", "حَجّ", "ḥajj", "pilgrimage")],
    "The month of Hajj: وَأَذِّنْ فِي النّاسِ بِالْحَجِّ <b style=\"white-space:nowrap;font:inherit\">(al-Ḥajj 22:27)</b>. Which did you know? 👇"),
 ]),
 "wudu": ("Can you do wudu<br>in Arabic? 💧", [
   ("hands", "يَد", "yad", [("أَغْسِلُ يَدَيَّ.", "يَدَيَّ", "aghsilu yadayya.", "I wash my hands.")],
    "Two hands: يَدانِ. My two hands: يَدَيَّ."),
   ("mouth", "فَم", "fam", [("أَغْسِلُ فَمِي.", "فَمِي", "aghsilu famī.", "I rinse my mouth.")],
    "Rinsing the mouth in wudu has its own word: الْمَضْمَضَة."),
   ("nose", "أَنْف", "anf", [("أَغْسِلُ أَنْفِي.", "أَنْفِي", "aghsilu anfī.", "I rinse my nose.")],
    "An ENT doctor in Arabic: طَبِيب أَنْف وَأُذُن وَحَنْجَرَة, a nose, ear and throat doctor."),
   ("face", "وَجْه", "wajh", [("أَغْسِلُ وَجْهِي.", "وَجْهِي", "aghsilu wajhī.", "I wash my face.")],
    "فَاغْسِلُوا وُجُوهَكُمْ: “wash your faces” <b style=\"white-space:nowrap;font:inherit\">(al-Māʾidah 5:6)</b>."),
   ("elbow", "مِرْفَق", "mirfaq", [("أَغْسِلُ يَدَيَّ إِلَى الْمِرْفَقَيْنِ.", "الْمِرْفَقَيْنِ", "aghsilu yadayya ila l-mirfaqayn.", "I wash my arms up to the elbows.")],
    "وَأَيْدِيَكُمْ إِلَى الْمَرافِقِ: “and your arms up to the elbows” <b style=\"white-space:nowrap;font:inherit\">(5:6)</b>."),
   ("head", "رَأْس", "raʾs", [("أَمْسَحُ رَأْسِي.", "رَأْسِي", "amsaḥu raʾsī.", "I wipe my head.")],
    "وَامْسَحُوا بِرُؤُوسِكُمْ: wipe, don't wash <b style=\"white-space:nowrap;font:inherit\">(5:6)</b>. One head رَأْس, many رُؤُوس."),
   ("ears", "أُذُن", "udhun", [("أَمْسَحُ أُذُنَيَّ.", "أُذُنَيَّ", "amsaḥu udhunayya.", "I wipe my ears.")],
    "Same letters ء ذ ن as أَذان, the call to prayer. It's for your ears!"),
   ("feet", "رِجْل", "rijl", [("أَغْسِلُ رِجْلَيَّ.", "رِجْلَيَّ", "aghsilu rijlayya.", "I wash my feet.")],
    "وَأَرْجُلَكُمْ إِلَى الْكَعْبَيْنِ: “and your feet up to the ankles” <b style=\"white-space:nowrap;font:inherit\">(5:6)</b>. Which did you know? 👇"),
 ]),
 "sun-moon": ("When do you NOT say<br>the L in “al-”? ☀️🌙", [
   ("the sun", "الشَّمْس", "ash-shams ☀️", [("وَالشَّمْسِ وَضُحاها", "وَالشَّمْسِ", "wash-shamsi wa ḍuḥāhā", "By the sun and its morning brightness (91:1)")],
    "ش is a sun letter: the ل goes silent and the ش doubles (that's the shadda ّ). Never “al-shams”."),
   ("the moon", "الْقَمَر", "al-qamar 🌙", [("وَالْقَمَرِ إِذا تَلاها", "وَالْقَمَرِ", "wal-qamari idhā talāhā", "And the moon when it follows it (91:2)")],
    "ق is a moon letter: you say the ل. Spot the sukūn on it: لْ."),
   ("peace", "السَّلام", "as-salām ☀️", [("السَّلامُ عَلَيْكُمْ", "السَّلامُ", "as-salāmu ʿalaykum", "Peace be upon you")],
    "You've said it right all along: as-salām, not al-salām. س is a sun letter."),
   ("the book", "الْكِتاب", "al-kitāb 🌙", [("ذٰلِكَ الْكِتابُ لا رَيْبَ فِيهِ", "الْكِتابُ", "dhālika l-kitābu lā rayba fīh", "This is the Book, without any doubt (2:2)")],
    "ك is a moon letter: you say the ل."),
   ("the Most Merciful", "الرَّحْمٰن", "ar-Raḥmān ☀️", [("الرَّحْمٰنِ الرَّحِيمِ", "الرَّحْمٰنِ", "ar-raḥmāni r-raḥīm", "The Most Merciful, the Most Kind (1:3)")],
    "ر is a sun letter, twice in one verse: ar-Raḥmān, ar-Raḥīm."),
   ("praise", "الْحَمْد", "al-ḥamd 🌙", [("الْحَمْدُ لِلَّهِ رَبِّ الْعالَمِينَ", "الْحَمْدُ", "al-ḥamdu lillāhi rabbi l-ʿālamīn", "All praise is for Allah, Lord of the worlds (1:2)")],
    "ح is a moon letter. The sukūn on لْ is your clue: say the L."),
   ("the light", "النُّور", "an-nūr ☀️", [("مِنَ الظُّلُماتِ إِلَى النُّورِ", "النُّورِ", "mina ẓ-ẓulumāti ila n-nūr", "Out of the darkness into the light (2:257)")],
    "ن and ظ are both sun letters: aẓ-ẓulumāt, an-nūr."),
   ("the House", "الْبَيْت", "al-bayt 🌙", [("فَلْيَعْبُدُوا رَبَّ هٰذَا الْبَيْتِ", "الْبَيْتِ", "fal-yaʿbudū rabba hādha l-bayt", "So let them worship the Lord of this House (106:3)")],
    "The 14 sun letters: ت ث د ذ ر ز س ش ص ض ط ظ ل ن. The other 14 are moon letters. Which did you know? 👇"),
 ]),
 "she": ("He → she in Arabic:<br>just one letter 👀", [
   ("teacher", "مُعَلِّمَ<i>ة</i>", "muʿallim → muʿallima", [("هُوَ مُعَلِّمٌ، وَهِيَ مُعَلِّمَةٌ.", "مُعَلِّمَةٌ", "huwa muʿallim, wa hiya muʿallima.", "He's a teacher, and she's a teacher.")],
    "Add ة (tāʾ marbūṭa) and he becomes she. At the end of a sentence it's just a soft “-a”."),
   ("student", "طالِبَ<i>ة</i>", "ṭālib → ṭāliba", [("أَنا طالِبٌ، وَأُخْتِي طالِبَةٌ.", "طالِبَةٌ", "anā ṭālib, wa ukhtī ṭāliba.", "I'm a student, and my sister's a student.")],
    "More than one female student: طالِبات (ṭālibāt). The ة becomes ات."),
   ("doctor", "طَبِيبَ<i>ة</i>", "ṭabīb → ṭabība", [("هِيَ طَبِيبَةٌ فِي الْمُسْتَشْفى.", "طَبِيبَةٌ", "hiya ṭabība fi l-mustashfā.", "She's a doctor at the hospital.")],
    "Before another word, the ة is said “t”: طَبِيبَةُ أَسْنانٍ, ṭabībatu asnān, a dentist (she)."),
   ("engineer", "مُهَنْدِسَ<i>ة</i>", "muhandis → muhandisa", [("أُمِّي مُهَنْدِسَةٌ.", "مُهَنْدِسَةٌ", "ummī muhandisa.", "My mum is an engineer.")],
    "Most jobs work the same way: add ة for a woman."),
   ("big", "كَبِيرَ<i>ة</i>", "kabīr → kabīra", [("الْبَيْتُ كَبِيرٌ، وَالسَّيّارَةُ كَبِيرَةٌ.", "كَبِيرَةٌ", "al-baytu kabīr, was-sayyāratu kabīra.", "The house is big, and the car is big.")],
    "Things have a gender too. سَيّارَة (car) ends in ة, so it's a she, and its adjective takes ة too."),
   ("new", "جَدِيدَ<i>ة</i>", "jadīd → jadīda", [("الْكِتابُ جَدِيدٌ، وَالْحَقِيبَةُ جَدِيدَةٌ.", "جَدِيدَةٌ", "al-kitābu jadīd, wal-ḥaqībatu jadīda.", "The book is new, and the bag is new.")],
    "حَقِيبَة (bag) ends in ة: a she. So the bag is جَدِيدَة."),
   ("watch out: mum", "أُمّ", "umm: a she, with no ة", [("أُمِّي فِي الْبَيْتِ.", "أُمِّي", "ummī fi l-bayt.", "My mum is at home.")],
    "Some words are feminine without ة: أُمّ mum, بِنْت girl, even شَمْس sun. Which did you know? 👇"),
 ]),
}

CSS = QC.CSS + (".sw { display:inline-block; width:34px; height:34px; border-radius:50%; border:3px solid rgba(23,38,43,.25); vertical-align:-6px; margin-right:6px; }"
               ".cov.colours b:nth-child(1) { color:#c0392b; } .cov.colours b:nth-child(2) { color:#2f6fb5; } .cov.colours b:nth-child(3) { color:#2e7d4f; }"
               ".cov.colours b:nth-child(4) { color:#d9a514; } .cov.colours b:nth-child(5) { color:#fff; -webkit-text-stroke:2px #17262b; }"
               ".cov.colours b:nth-child(6) { color:#17262b; }") + ".en.long { font-size:80px; top:245px; } .ar.long { font-size:160px; top:390px; } .note span { unicode-bidi:isolate; } .cov.few b { font-size:150px; }"
# the cover: the short words only
COVER = {"pronouns": "I · You · He · She · We", "time": "Today · Tomorrow · Yesterday · Now · After that", "here-this": "Here · There · This",
         "feelings": "Happy · Hungry · Ill · Busy", "yes-no": "Yes · No · Of course · OK", "numbers": "1 · 2 · 3 · 4 · 5 · 6 · 7 · 8 · 9 · 10",
         "colours": "Red · Blue · Green · Yellow · White · Black", "family": "Mum · Dad · Brother · Sister · Grandpa · Grandma",
         "little": "And · But · With · In · From · To",
         "food": "Water · Bread · Dates · Tea · Milk · Coffee", "days": "Sun · Mon · Tue · Wed · Thu · Fri · Sat",
         "months": "Muḥarram · Ṣafar · Rajab · Ramaḍān · Shawwāl", "wudu": "Hands · Mouth · Face · Head · Feet",
         "sun-moon": "al- · ash- · as- · ar- · an-", "she": "Teacher · Student · Doctor · Big · New"}

def ar_spans(note):     # Arabic inside an English note gets the Arabic font
    import re
    return re.sub(r"([؀-ۿ][؀-ۿً-ْٰ ]*[؀-ۿً-ْٰ])", r"<span>\1</span>", note)

def slides(cover, W, sid):
    n = len(W); cw = COVER[sid].split(" · ")
    out = {"1": f'<body>{S.BRAND}<div class="cov{" few" if len(cw) < 6 else ""} {sid}">' + "".join(f"<b>{e}</b>" for e in cw) + '</div>'
                f'<div class="cq">{cover}</div><div class="cs">SWIPE AND COUNT YOUR SCORE →</div></body>'}
    for k, (en, ar, tr, ex, note) in enumerate(W, 2):
        top = 760 if len(ex) == 1 else 690
        boxes = "".join(f'<div class="e"><div class="s">{s.replace(h, f"<i>{h}</i>", 1)}</div><div class="t">{t}</div><div class="m">{m}</div></div>'
                        for s, h, t, m in ex)
        lg = " long" if len(en) > 10 or len(ar) > 8 else ""
        out[str(k)] = (f'<body>{S.BRAND}<div class="n">{k - 1} / {n}</div><div class="q en{lg}">{en[0].upper() + en[1:]}</div>'
                       f'<div class="q ar{lg}">{ar}</div><div class="q tr">{tr}</div><div class="ex" style="top:{top}px">{boxes}</div>'
                       + (f'<div class="note">{ar_spans(note)}</div>' if note else "") + '</body>')
    out[str(n + 2)] = (f'<body class="dark">{S.BRAND}<div class="endq">How many<br>did you know?<br><i>Comment /{n} 👇</i></div>'
                       '<div class="ends"><div>Save this 📌 for later</div><div>Send it to someone learning Arabic with you</div></div></body>')
    return out

if __name__ == "__main__":
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=S.CHROME if os.path.exists(S.CHROME) else None)
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for sid, (cover, W) in SETS.items():
            if sys.argv[1:] and sid not in sys.argv[1:]: continue      # python3 brag-quiz/build_word_carousels.py numbers
            out = os.path.join(S.HERE, "stills", sid); os.makedirs(out, exist_ok=True)
            for k, body in slides(cover, W, sid).items():
                tmp = os.path.join(out, "_s.html"); open(tmp, "w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>{body}</html>')
                pg.goto("file://" + tmp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
                pg.screenshot(path=os.path.join(out, f"{sid}-{k}.png"))
            os.remove(os.path.join(out, "_s.html")); print(sid, len(W) + 2, "slides")
        b.close()
