# Early units: teach first? (#156) Weighs the collaborator's grammar audit and the owner's idea (simpler first
# lessons that teach words before sentences) for Rafiq's learners.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/teaching_first.py
from concurrent.futures import ThreadPoolExecutor
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from videos_v9 import ask, Q, avg

LEARNERS = {
 "revert": "a new Muslim adult in the UK who can't read Arabic script yet and has never studied Arabic",
 "reader": "a UK Muslim adult who can read the Quran's script aloud but understands almost none of it, a total beginner in Arabic",
 "quitter": "a busy UK Muslim adult who tried Duolingo-style Arabic apps and quit after a week because it felt confusing",
 "student": "an adult at a weekend Arabic class who wants the grammar explained properly",
 "parent": "a Muslim parent with 10 minutes a day who wants to learn alongside their children",
}
NOW = ("TODAY, unit 1 (greetings) works like this: first, 'meet 10 words' — but all ten are greeting phrases (السَّلامُ عَلَيْكُم, كَيْفَ حالُكَ, ما اسْمُكَ؟ ...). "
       "Step 2 plays a full 10-line conversation where only about a quarter of the words have been met. Step 3 shows four grammar cards "
       "(no word for 'is', هذا/هذه, nationality endings, question words). Then 10 more words each, then a practice session "
       "where you pick missing endings, change sentences to the feminine or into questions, and build sentences from tiles; about half the words there are new.")

# ---- 1. which problems matter most
ISSUES = {
 "sentences_first": "Learners meet whole sentences and are asked to choose between endings and words before they know the words or the rule: in unit 1 only about 25% of the conversation's words have been taught when it plays",
 "past_untaught": "'Change to the past' is the most practised exercise (units 2-12) but past-tense endings are never explained; the future and 'you' (feminine) are also only practised, never taught",
 "case_scattered": "Case endings (-un/-an/-in) are taught as ten separate tricks across units instead of one simple 'three endings' idea",
 "agreement_missing": "No lesson explains noun-adjective agreement (بَيْتٌ كَبِيرٌ), 'this is a book' vs 'this book', verb-subject agreement, or 'who/which' (الذي/التي)",
 "no_escalation": "The sentence-changing exercises in unit 12 are no harder than in unit 4",
 "connectors": "53 joining words are listed but only about 5 are taught with the grammar they need",
 "no_contrast": "Grammar cards show one right example but never a common wrong one next to it",
 "endings_untested": "Typed answers ignore vowel marks, so wrong case endings are marked right, and word tiles give learners the endings ready-made",
}
QI = {"hurts": Q("A beginner Arabic app for Muslims learning Modern Standard Arabic. `now` A reviewer found this problem: `issue`. Learner: `learner`. How much does it hurt this learner in the first month (understanding, confidence, staying with it)?", ["Not at all", "A little", "Quite a lot", "Badly"]),
      "quit": {"type": "noul", "instructions": "A beginner Arabic app. `now` Problem: `issue`. Learner: `learner`. Is this likely to make this learner give up on the app?"}}

# ---- 2. what the first lessons should look like
DESIGNS = {
 "now": NOW,
 "words_first": ("Unit 1 starts with two short lessons of single words only (أَنا, أَنْتَ, هُوَ, هِيَ, اسْم, طالِب, بَيْت ...), each with a picture and a native voice, "
                 "and games: hear it and pick the picture, pick the meaning. Greeting phrases come next, taken apart word by word. The conversation comes at the end of the unit, "
                 "when almost every word in it has been taught."),
 "teach_then_do": ("Every step teaches before it asks: one idea shown with 3-4 examples and a common mistake crossed out, then guided practice (tap the right ending, with a hint), "
                   "then practice on your own, using only words already taught. Conversations play only once 80% of their words are known, with a tap on any word to see it."),
 "reorder_only": ("Same content as today, reordered: the grammar cards come before the conversation, every word in the conversation can be tapped for its meaning, "
                  "and practice uses only words already met."),
 "words_first_plus": ("Both: two words-only lessons to start (single words, pictures, native voice, hear-and-pick games), then every step teaches before it asks "
                      "(one idea, examples, a wrong example crossed out, guided then independent practice) using only words already taught; the conversation at the unit's end."),
}
QD = {"understand": Q("Arabic app, first week. `design` Learner: `learner`. How well would they understand what they're doing?", ["Lost", "Partly", "Mostly", "Fully"]),
      "confident": Q("Arabic app, first week. `design` Learner: `learner`. How confident and capable would they feel after the first lesson?", ["Discouraged", "Unsure", "Fairly confident", "Confident"]),
      "stay": Q("Arabic app, first week. `design` Learner: `learner`. How likely are they to still be using it after two weeks?", ["Unlikely", "Maybe", "Likely", "Very likely"]),
      "slow": {"type": "noul", "instructions": "Arabic app, first week. `design` Learner: `learner`. Would it feel too slow or too basic to them?"}}

if __name__ == "__main__":
    with ThreadPoolExecutor(8) as ex:
        ji = [(i, l) for i in ISSUES for l in LEARNERS]
        ri = dict(ex.map(lambda j: (j, ask({"now": NOW, "issue": ISSUES[j[0]], "learner": LEARNERS[j[1]]}, QI)["answers"]), ji))
        jd = [(d, l) for d in DESIGNS for l in LEARNERS]
        rd = dict(ex.map(lambda j: (j, ask({"design": DESIGNS[j[0]], "learner": LEARNERS[j[1]]}, QD)["answers"]), jd))
    print("=== 1. problems, by harm to beginners in the first month (0-3); quit = chance it makes them give up")
    for i in sorted(ISSUES, key=lambda i: -avg([ri[(i, l)] for l in LEARNERS], "hurts")):
        rs = [ri[(i, l)] for l in LEARNERS]
        print(f"  {avg(rs,'hurts'):.2f}  quit {avg(rs,'quit','noul'):.2f}  {i:18} " + " ".join(f"{l}:{ri[(i, l)]['hurts']['score']:.1f}" for l in LEARNERS))
    print("\n=== 2. the first lessons (0-3; slow = chance it feels too slow/basic)")
    print(f"  {'design':17} understand confident stay  slow")
    for d in DESIGNS:
        rs = [rd[(d, l)] for l in LEARNERS]
        print(f"  {d:17} {avg(rs,'understand'):.2f}       {avg(rs,'confident'):.2f}      {avg(rs,'stay'):.2f}  {avg(rs,'slow','noul'):.2f}")
    print("\n  stay, per learner:")
    for d in DESIGNS: print(f"  {d:17} " + " ".join(f"{l}:{rd[(d, l)]['stay']['score']:.2f}" for l in LEARNERS))
    print("  slow, per learner:")
    for d in DESIGNS: print(f"  {d:17} " + " ".join(f"{l}:{rd[(d, l)]['slow']['noul']:.2f}" for l in LEARNERS))
