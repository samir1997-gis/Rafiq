# What's missing or brushed over in the reading starter and units 1-3 (#163), ranked.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/early_gaps.py
from concurrent.futures import ThreadPoolExecutor
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from videos_v9 import ask, Q

LEARNER = "an adult UK Muslim beginner in Modern Standard Arabic on a phone app, who has just learned the letters and vowel marks"
# each: what it is, and what the app does now (checked in the code, 30 Sep 2026)
GAPS = {
 "the":        ("ال means 'the', and there is no word for 'a': the -un ending (tanwin) marks 'a'",
                "never explained as a lesson; units 1-3 use ال in almost every sentence; the vowel lesson says tanwin 'adds n' but not that it means 'a'"),
 "sun-moon":   ("sun and moon letters: in السَّلامُ the ل of ال is silent and the next letter doubles (as-salām), but in الْقَمَر it's said (al-qamar)",
                "never explained; the very first phrase, السَّلامُ عَلَيْكُم, and 24 other places in units 1-3 are like this"),
 "ta-marbuta": ("how ة is said: -a at the end of a word, -at when another word or ending follows (مَدْرَسَةُ الْبِنْتِ, madrasatu)",
                "only that ة becomes ت before 'my' (new card); how to say it is never taught"),
 "we-they":    ("the plural pronouns: نَحْنُ we, أَنْتُمْ you (plural), هُمْ they",
                "only I, you (m/f), he, she are taught in units 1-3; نَحْنُ isn't in the word list at all; هُمْ is used twice without being taught"),
 "have":       ("'I have' is عِنْدِي (literally 'with me'), not a verb: عِنْدِي أَخٌ, I have a brother",
                "عِنْدِي is used 3 times in units 1-3 (the family unit) but never explained"),
 "not":        ("'is not' / 'am not' with لَيْسَ: لَسْتُ طالِباً, I'm not a student",
                "the word لَيْسَ comes in unit 4 but is only explained in unit 10"),
 "plurals":    ("most plurals change the inside of the word (طالِب → طُلّاب, وَلَد → أَوْلاد, غُرْفَة → غُرَف), so each word is learned with its plural",
                "plurals like these appear in units 2-3 with no explanation; only the ـات ending is explained, in unit 12"),
 "things-pl":  ("plurals of things (not people) count as feminine singular: هَذِهِ غُرَفٌ كَبِيرَةٌ, 'these are big rooms'",
                "never explained anywhere in the course"),
 "roots":      ("most words are built from a three-letter root: ك ت ب gives كِتاب book, كاتِب writer, مَكْتَب desk",
                "never explained as a lesson, though the salah section shows each word's root"),
 "verb-pair":  ("why verbs are listed as two words, قَرَأَ / يَقْرَأُ: the past 'he read' is the dictionary form, and the present form",
                "verbs appear in the word list this way from unit 1 (كانَ / يَكُونُ) with no explanation"),
 "pause":      ("at the end of a sentence you don't say the -u/-a/-i ending: السَّلامُ عَلَيْكُمْ, but a pause says السَّلام",
                "not explained; the app shows the full endings but speakers drop them at a pause"),
 "that":       ("'that': ذَلِكَ (m) and تِلْكَ (f)",
                "taught only in unit 12"),
 "wasl":       ("the joining alif: in بِسْمِ اللهِ or فِي الْبَيْتِ the a- of ال is not said (fil-bayt)",
                "not explained"),
}
QS = {"need": Q("A beginner Arabic course, first three units (greetings, family, housing). Topic: `t`. Learner: `learner`. How important is it to teach this in the first three units?", ["Not needed yet", "Useful", "Important", "Essential"]),
      "hurt": Q("A beginner Arabic app. Topic: `t`. What the app does now: `now`. Learner: `learner`. How much does the gap confuse them or build a bad habit?", ["Not at all", "A little", "Clearly", "A lot"])}

if __name__ == "__main__":
    with ThreadPoolExecutor(8) as ex:
        r = dict(zip(GAPS, ex.map(lambda g: ask({"t": g[0], "now": g[1], "learner": LEARNER}, QS)["answers"], GAPS.values())))
    print("gap          need  hurt  total")
    for k, a in sorted(r.items(), key=lambda x: -(x[1]["need"]["score"] + x[1]["hurt"]["score"])):
        print(f"{k:<12} {a['need']['score']:.2f}  {a['hurt']['score']:.2f}  {a['need']['score'] + a['hurt']['score']:.2f}")

# Results (30 Sep 2026), need (0-3) + hurt (0-3):
#   sun/moon letters 5.14 · 'I have' عِنْدِي 5.08 · 'the' ال and no 'a' 4.70 · how ة is said 4.03 · dropping endings at a pause 3.93
#   · the joining alif 3.65 · plurals that change inside 3.64 · we/you (pl)/they 3.57 · plurals of things are feminine 3.56
#   · لَيْسَ 'is not' 3.17 · why verbs have two forms 3.10 · roots 2.77 · 'that' 1.68
