"""Five carousels in the question-words format (owner, 19 Oct 2026: "people like the simple ones they can relate to"):
I/you/he/she/we · today/tomorrow/yesterday/now/after that · here/there/this · how are you feeling · yes/no/of course/OK.
Same look as build_questions_carousel.py: slide 1 is the English words and "Can you say all N in Arabic?", one slide per word
with the course's own example sentence (word in red), the end asks for a score. Every word and sentence is the course's own
(vocab-data.js, drills-data.js, toolkit-data.js, scenes-data.js) except أَنا مَشْغُولٌ and أَنا سَعِيدٌ هُنا (trimmed from
"وَأَنا سَعِيدٌ هُنا"). Pure content (4 posts in 5): no app pitch.

  python3 brag-quiz/build_word_carousels.py   ->  brag-quiz/stills/<set>/<set>-1.png ...
"""
import os
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
}

CSS = QC.CSS + ".en.long { font-size:80px; top:245px; } .ar.long { font-size:160px; top:390px; } .note span { unicode-bidi:isolate; } .cov.few b { font-size:150px; }"
# the cover: the short words only
COVER = {"pronouns": "I · You · He · She · We", "time": "Today · Tomorrow · Yesterday · Now · After that", "here-this": "Here · There · This",
         "feelings": "Happy · Hungry · Ill · Busy", "yes-no": "Yes · No · Of course · OK"}

def ar_spans(note):     # Arabic inside an English note gets the Arabic font
    import re
    return re.sub(r"([؀-ۿ][؀-ۿً-ْٰ ]*[؀-ۿً-ْٰ])", r"<span>\1</span>", note)

def slides(cover, W, sid):
    n = len(W); cw = COVER[sid].split(" · ")
    out = {"1": f'<body>{S.BRAND}<div class="cov{" few" if len(cw) < 6 else ""}">' + "".join(f"<b>{e}</b>" for e in cw) + '</div>'
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
            out = os.path.join(S.HERE, "stills", sid); os.makedirs(out, exist_ok=True)
            for k, body in slides(cover, W, sid).items():
                tmp = os.path.join(out, "_s.html"); open(tmp, "w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>{body}</html>')
                pg.goto("file://" + tmp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
                pg.screenshot(path=os.path.join(out, f"{sid}-{k}.png"))
            os.remove(os.path.join(out, "_s.html")); print(sid, len(W) + 2, "slides")
        b.close()
