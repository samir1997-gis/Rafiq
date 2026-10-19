# Simple image ads (#266, 19 Oct 2026)

Three 1080x1350 feed ads (Instagram/Facebook 4:5). Edit `ads.html`, then `python3 brag-social/ads/render.py`.

| File | Idea |
|---|---|
| `ad-news.png` | Breaking-news front page: "Rafiq is now live". Our own masthead, not a real paper's name or logo. |
| `ad-time.png` | Your salah, 30 days from now: Day 0 → 1 → 14 → 30. |
| `ad-ba.png` | Before / after on one line: سُبْحانَ رَبِّيَ الْأَعْلى without and with its meaning. |

## Where the claims come from
- Every word of the prayer plus 10 short surahs: `salah-data.js` (21 parts: 11 of the prayer, 10 surahs; 331 words), live (`salah.js` LIVE).
- One part is about 5 minutes (`salah.js` header); "5–10 minutes a day" and "free for 7 days, no card" are on `index.html`.
- Day 1, "5 words, a third of your prayer": the first salah lesson says the first 5 most-said words are 34% of a four-rakah prayer.
- Day 14, the whole prayer: the 11 prayer parts at one part a day. Day 30: the 10 surahs after that, with time to review.
- The timeline is the pace at one part a day, not a promise; the small print says "one 5-minute part a day".
- Photo: the owner's own B-roll (DJI_20261018181326_0042_D, 11.5 s), graded with `brag-quiz/reels/template/grade.txt`.

## The before/after video (for the owner to film)
Keep it honest: a real before (now) and a real after, or play it clearly as a sketch. UK ad rules (ASA) don't allow a
staged result shown as typical.
1. **Before, 3-4 s.** Mid-prayer or just after: "I've said this every day for years…" then try to explain سُبْحانَ رَبِّيَ الْأَعْلى and stall.
2. **Card, 1 s.** "DAY 1" with the app open on the first salah lesson.
3. **After, 5-6 s.** Same spot, same top: say the line slowly and translate each word as you say it.
4. **End, 2 s.** "Every word of your salah. Free for 7 days." + the logo.
Send the clips and I'll cut it with the reel template.
