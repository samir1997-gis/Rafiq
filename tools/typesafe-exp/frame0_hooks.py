# Which first frame stops the right people? (owner, 12 Oct 2026: q4-azim lost most viewers at 0:01; TikTok shows new accounts'
# videos to a broad first audience, so the first frame has to stop the target viewer and tell everyone else it's not for them.)
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/frame0_hooks.py
# Result (12 Oct; stop past 3 s for target / revert / non-Muslim, then trust): A plain quiz shown at once 2.17 / 2.61 / 0.14, trust 2.20 (most
#   trusted, and it lets uninterested people go) · B "Muslims: you say this 17 times a day" 2.58 / 1.88 / 0.70, trust 0.42 · C a face mid-sentence
#   2.36 / 1.66 / 0.62, trust 1.41 · D "10,000 times and never understood it" 2.58 / 2.55 / 0.73, trust 0.28 · E "only 1 in 10" 2.22 / 2.23, trust 0.06.
#   Loud claims stop a few more people but read as clickbait; the honest quiz, actually on screen, is the base. Add relevance ("you say this in
#   every rukūʿ"), bigger type, and the owner's face for some, never invented stats.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A TikTok from a small account that teaches the Arabic of the daily prayer. The viewer sees only the first second, "
       "scrolling the For You feed, nothing else. On screen: ")
WHO = {"target": "a 27-year-old UK Muslim who prays but doesn't understand the Arabic",
       "revert": "a 31-year-old revert learning to pray",
       "nonmuslim": "a 24-year-old non-Muslim in the UK with no interest in Arabic or religion"}
F0 = {"A_quiz": "small text 'What does this word in your salah mean?' and a big Arabic word, plain cream background (today's quiz)",
      "B_callout": "huge bold text 'Muslims: you say this 17 times a day. Do you know what it means?' over a big Arabic phrase",
      "C_face": "a young Muslim man looking straight at the camera, mid-sentence, caption 'I prayed for 26 years without understanding a word'",
      "D_stakes": "huge text 'You've said this 10,000 times and never understood it' with سُبْحانَ رَبِّيَ الْعَظِيمِ glowing underneath",
      "E_challenge": "huge text 'Only 1 in 10 Muslims gets this right' and a big Arabic word with a timer already running"}
Q = {"stop": {"type": "score", "instructions": "`ctx` `f` Viewer: `who`. How likely are they to stop scrolling and keep watching past 3 seconds?",
              "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` `f` Viewer: `who`. Does it feel genuine rather than clickbait?",
               "criteria": ["Clickbait", "A bit", "Mostly genuine", "Genuine"]}}
if __name__ == "__main__":
    jobs = [(k, w) for k in F0 for w in WHO for _ in range(2)]
    with ThreadPoolExecutor(20) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "f": F0[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
    print(f"{'':12}" + "".join(f"{w[:8]:>9}" for w in WHO) + "    trust")
    for k in F0:
        st = {w: sum(a["stop"]["score"] for (kk, ww), a in res if kk == k and ww == w) / 2 for w in WHO}
        tr = sum(a["trust"]["score"] for (kk, ww), a in res if kk == k and ww != "nonmuslim") / 4
        print(f"{k:12}" + "".join(f"{st[w]:9.2f}" for w in WHO) + f"{tr:9.2f}")
