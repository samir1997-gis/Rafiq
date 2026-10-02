# Should the owner post videos of an AI avatar of themselves (cloned face and voice) instead of filming daily?
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/ai_avatar.py
from concurrent.futures import ThreadPoolExecutor
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from videos_v9 import ask, Q, VIEWERS
BASE = "A 15-second vertical TikTok/Reel for Rafiq, an app teaching Arabic to UK Muslims: a quick Arabic word quiz ('which of these means brother?'), then the answer and rafiq-arabic.com. "
FORMATS = {
 "founder_real": BASE + "The young British Muslim founder films himself on his phone, talking to camera.",
 "ai_avatar_labelled": BASE + "The presenter is a hyper-realistic AI avatar of the founder with a cloned voice; TikTok shows its 'AI-generated' label. Arabic words are spoken by the cloned voice.",
 "ai_avatar_spotted": BASE + "The presenter is a hyper-realistic AI avatar of the founder with a cloned voice; some viewers notice it's AI from the lip movements, and a comment says 'this is AI'.",
 "app_screen_voice": BASE + "No face: the real app on screen with a narrator's voice and a native Arabic speaker saying the words.",
}
QS = {"watch": Q("Viewer: `viewer`. Video: `v` How likely are they to watch to the end?", ["Scroll past", "Watch a bit", "Most of it", "To the end"]),
      "trust": Q("Viewer: `viewer`. Video: `v` How much do they trust this app to teach Arabic (and the words of the prayer) correctly?", ["Not at all", "A little", "Quite a lot", "A lot"]),
      "try": Q("Viewer: `viewer`. Video: `v` How likely are they to visit the website?", ["Unlikely", "Maybe", "Likely", "Very likely"])}
if __name__ == "__main__":
    runs = [(k, v) for k in FORMATS for v in VIEWERS for _ in range(2)]
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(lambda r: ask({"viewer": VIEWERS[r[1]], "v": FORMATS[r[0]]}, QS)["answers"], runs))
    for k in FORMATS:
        rs = [a for (n, _), a in zip(runs, res) if n == k]
        print(f"{k:<20}", "  ".join(f"{q} {sum(a[q]['score'] for a in rs)/len(rs):.2f}" for q in QS))

# Results (2 Oct 2026), 5 viewers x 2 runs — watch / trust / visit site:
#   founder filmed for real        1.98 / 1.14 / 1.50
#   AI avatar, labelled AI         1.69 / 0.84 / 1.19   <- lowest on all three
#   AI avatar, spotted as AI       1.88 / 0.96 / 1.26
#   app screen + voice, no face    2.14 / 1.39 / 1.65   <- highest on all three
