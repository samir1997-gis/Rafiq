# Launch day review (1 Oct 2026, #185): what went live today, checked with TypeSafe the way earlier work was.
# The words people read (landing, emails, terms, cancel box), the fast Meet Rafiq cut, the vertical story film,
# and the idea of speaking replies in real-life scenes (#184).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/launch_day_review.py  (emails: node render to SCRATCH/emails.json first)
from concurrent.futures import ThreadPoolExecutor
import html, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from videos_v9 import ask, Q, VIEWERS
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FACTS = ("TRUE FACTS ABOUT RAFIQ (soft-launched 1 Oct 2026): a web app (rafiq-arabic.com) for learning Modern Standard Arabic, mostly for UK Muslims. "
 "Every new account gets 7 days of Complete free, no card. Essentials £6.99/month or £49.99/year; Complete £11.99/month or £79.99/year. "
 "Cancel any time in Settings. Cancelling within 14 days of the first payment, or of a yearly renewal, refunds it automatically, once per account. "
 "Course: letters, 'the basics', 12 units of 5-10 minute steps; fully vowelled with native audio; reviews timed by FSRS. "
 "Your salah: every word of the prayer and 10 short surahs, with Pray along (Complete); the 20 most-said words on every plan. "
 "Conversation partner and real-life scenes: the learner TYPES a reply in Arabic (or picks / builds it from tiles in early units) and AI checks it. "
 "Learners are told to say replies aloud, but nothing listens to them there; a microphone button exists only in some drills. "
 "The AI tutor and the 'Why?' button are NOT live yet (shown as coming soon). No music anywhere.")
READERS = {k: VIEWERS[k] for k in ("muslim", "revert", "parent", "general")}

def page(f, a, b=None):
    s = open(os.path.join(ROOT, f)).read(); s = s[s.index(a):s.index(b) if b else None]
    s = re.sub(r"<(script|style)[\s\S]*?</\1>", "", s); s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    return re.sub(r"\s+", " ", s).strip()

EMAILS = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else {}
TEXTS = {
 "landing": page("index.html", "<body", "Coming next"),
 "terms_short": page("terms.html", "The short version", '<ol class="toc">'),
 "cancel_box": "Cancel your plan? If this is within 14 days of your first payment (or of a yearly renewal), it's refunded in full and your plan ends now. "
               "Otherwise your plan stops on 8 November, the end of the period you've paid for, and you won't be charged again. We'll email you to confirm.",
 **{f"email_{k}": v for k, v in EMAILS.items()},
}
TQ = {
 "clear": Q("Facts: `facts` Reader: `reader`. Text they read from Rafiq: `text` How clear is it to this reader what it says and what to do next?",
            ["Confusing", "Some parts unclear", "Clear", "Completely clear"]),
 "trust": Q("Facts: `facts` Reader: `reader`. Text: `text` How much does it make this reader trust Rafiq with their money and time?",
            ["Puts them off", "Neutral", "Builds some trust", "Builds a lot of trust"]),
 "cheesy": Q("Reader: `reader`. Text: `text` How salesy, cheesy or pushy does it feel?",
             ["Not at all", "Slightly", "Noticeably", "Very"]),
 "true": Q("Facts: `facts` Text: `text` Does the text promise or describe anything that the facts say isn't so (a feature that isn't live, a feature that works differently, a wrong price or policy)?",
           ["Everything matches the facts", "One small overstatement", "A clear claim the facts contradict", "Several false claims"]),
}
# Which landing line overstates? Asked per line, so the answer points at the line
LANDING_LINES = ["🗣️ Speak your own replies, with feedback", "💬 Conversation partner: Reply in your own words. Answer the other speaker your way. Rafiq checks your reply fits and points out grammar slips.",
                 "✈️ Real-life scenes: The airport, the doctor, the masjid… Six everyday situations", "🧠 Smart review: Words come back just before you'd forget them",
                 "Start with a free week of everything, no card needed. Then pick a plan. Cancel any time.", "Coming soon: your AI tutor."]
LQ = {"true": Q("Facts: `facts` Landing-page line: `text` Would a new user who believed this line be surprised or misled by what the app actually does?",
                ["No, it's accurate", "Slightly", "Yes, misled"])}

VIDEOS = {
 "v12_43s": "Meet Rafiq, 43 seconds, vertical. A calm narrator; after each line about a 0.5s pause; each app demo waits as a still screenshot until her line ends, then plays. "
            "Scenes: word cards blurring ('one week later'), Meet Rafiq, new words with native audio, the salah words and Pray along, the AI tutor answering a question (8s), the review gaps, an 8-second ending card.",
 "v13_26s": "Meet Rafiq, 26 seconds, vertical. The same narrator 15% quicker, 0.1s between lines; the app demos play while she speaks; quick cuts, captions that pop in, a small push on the phone at each cut. "
            "Scenes: word cards blurring ('one week later'), Meet Rafiq, new words with native audio, the salah words and Pray along, the review gaps, a 6-second ending card. No tutor.",
 "story_88s_letterboxed": "Rafiq: the story, 88 seconds. A calm landscape explainer film placed in the middle of a vertical frame with a title above ('Why words stick with Rafiq') and 'Start free · rafiq-arabic.com' below; "
            "the film itself is small (about a third of the screen) and slightly soft. Three findings from memory research: spacing, testing, habit, each with app screens.",
}
VQ = {
 "watch": Q("Viewer: `reader`. Video seen on Instagram Reels or TikTok: `video` How likely are they to watch it to the end?", ["Scroll past", "Watch a bit", "Most of it", "To the end"]),
 "pace": Q("Viewer: `reader`. Video: `video` How does its pace feel to this viewer?", ["Slow and boring", "A bit slow", "Right", "Too fast to follow"]),
 "try": Q("Facts: `facts` Viewer: `reader`. Video: `video` How likely are they to try Rafiq's free week after it?", ["Unlikely", "Maybe", "Likely", "Very likely"]),
}
SPEAK = {
 "type_now": "In Complete's real-life scenes (airport, doctor, masjid, taxi…) you reply to the other person by typing Arabic on an Arabic keyboard; AI checks your reply fits.",
 "speak": "In Complete's real-life scenes (airport, doctor, masjid, taxi…) you can tap a microphone and SAY your reply in Arabic (or type it); your phone turns it into text and AI checks your reply fits. It doesn't grade pronunciation.",
}
SQ = {"want": Q("Facts: `facts` Learner: `reader`. Feature: `f` How much does it make them want to pay for Complete?", ["Not at all", "A little", "Quite a lot", "A lot"]),
      "use": Q("Learner: `reader`. Feature: `f` How likely are they to use it regularly?", ["Unlikely", "Maybe", "Likely", "Very likely"])}

def avg(rs, q): return sum(r[q]["score"] for r in rs) / len(rs)
if __name__ == "__main__":
    ex = ThreadPoolExecutor(8)
    runs = [(k, r) for k in TEXTS for r in READERS]
    res = list(ex.map(lambda x: ask({"facts": FACTS, "reader": READERS[x[1]], "text": TEXTS[x[0]]}, TQ)["answers"], runs))
    print("text                clear trust cheesy untrue   (0-3; cheesy and untrue: lower is better)")
    for k in TEXTS:
        rs = [a for (n, _), a in zip(runs, res) if n == k]
        print(f"{k:<20}{avg(rs,'clear'):.2f}  {avg(rs,'trust'):.2f}  {avg(rs,'cheesy'):.2f}   {avg(rs,'true'):.2f}")
    lr = list(ex.map(lambda l: ask({"facts": FACTS, "text": l}, LQ)["answers"]["true"]["score"], LANDING_LINES * 3))
    print("\nlanding line misleads (0-2)")
    for i, l in enumerate(LANDING_LINES): print(f"  {sum(lr[i::len(LANDING_LINES)])/3:.2f}  {l[:70]}")
    runs = [(k, r) for k in VIDEOS for r in VIEWERS]
    res = list(ex.map(lambda x: ask({"facts": FACTS, "reader": VIEWERS[x[1]], "video": VIDEOS[x[0]]}, VQ)["answers"], runs))
    print("\nvideo                  watch  pace(2=right) try")
    for k in VIDEOS:
        rs = [a for (n, _), a in zip(runs, res) if n == k]
        print(f"{k:<23}{avg(rs,'watch'):.2f}   {avg(rs,'pace'):.2f}          {avg(rs,'try'):.2f}")
    runs = [(k, r) for k in SPEAK for r in READERS for _ in range(2)]
    res = list(ex.map(lambda x: ask({"facts": FACTS, "reader": READERS[x[1]], "f": SPEAK[x[0]]}, SQ)["answers"], runs))
    print("\nscenes reply      want Complete  use")
    for k in SPEAK:
        rs = [a for (n, _, ), a in zip([(a, b) for a, b in runs], res) if n == k]
        print(f"{k:<18}{avg(rs,'want'):.2f}           {avg(rs,'use'):.2f}")

# Results (1 Oct 2026). Texts, averaged over 4 readers (0-3; cheesy and untrue: lower is better):
#   landing 2.12 clear / 2.26 trust / 1.42 cheesy / 1.79 untrue; terms 2.42/2.26/0.47/0.14; cancel box 1.89/2.17/0.04/0.14;
#   emails clear 2.20-2.32, trust 2.21-2.48, untrue <= 0.10 except welcome 0.84 and trial ended 1.41 (sentence probes
#   point at things these facts leave out, e.g. the videos and the Practise page, not at real errors).
# Landing lines that mislead (0-2): "🗣️ Speak your own replies, with feedback" 1.97 (replies are typed); conversation partner 1.29;
#   scenes 0.80; the rest <= 0.26.
# Videos (watch / pace, 2 = right / try): v12 43s 1.86/0.97/1.85; v13 26s 2.08/2.66/1.95; a 32s middle 2.05/2.48/1.93;
#   the story film letterboxed at 88s 1.49/1.18/1.83.
# Speaking replies in scenes (#184), want Complete / use: typing 1.49/1.43; a microphone 1.27-1.38/1.04-1.20. No lift.
