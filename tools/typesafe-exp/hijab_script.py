# The "what does hijab actually mean" script (owner to camera, 30 Oct 2026; brag-quiz/reels/hijab-pileon/SCRIPT.md), opening on the pile-on.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/hijab_script.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 75-second talking-head Reel from Rafiq, an account teaching the Arabic Muslims use. It opens on an animation: a woman shouts 'We need to ban "
       "the hijab!' and a crowd shouts 'hijab' faster and faster at a hijabi under a spotlight; dead cut; the presenter walks in. Script: ")
S = {"A": "Hijab. Everybody seems to have an opinion on it… but what does the word actually mean? It comes from ḥ-j-b: to screen something off. "
          "From the same root, ḥājib: the doorkeeper, and your eyebrow, because it shields the eye. Every time ḥijāb comes up in the Qur'an it means a "
          "screen: between Paradise and the Fire (7:46); the sun hides behind the ḥijāb (38:32); Allah spoke to Musa from behind a ḥijāb (42:51); ask the "
          "Prophet's wives from behind a ḥijāb (33:53), revealed at Zaynab's wedding (Bukhari 4791). The headscarf words are khimar (24:31; Aisha: the women "
          "tore their cloaks and covered themselves straight away, Bukhari 4758) and jilbab (33:59), and the verse before is for men: lower your gaze (24:30). "
          "So hijab is a screen that protects something precious, like your eyebrow protects your eye; it goes with haya, and haya is part of faith (Bukhari 24). "
          "Next time everyone has an opinion on the hijab, now you know what it means. Which word next? Comment below."}
WHO = {"hijabi": "a 23-year-old UK hijabi", "brother": "a 28-year-old Muslim man", "curious": "a 30-year-old non-Muslim who's curious"}
Q = {"finish": {"type": "score", "instructions": "`ctx` `s` Viewer: `who`. How likely are they to watch to the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "share": {"type": "score", "instructions": "`ctx` `s` Viewer: `who`. How likely are they to share or save it?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "fair": {"type": "score", "instructions": "`ctx` `s` Viewer: `who`. Does it feel accurate and respectful, not preachy?", "criteria": ["No", "A bit", "Mostly", "Yes"]}}
if __name__ == "__main__":
    jobs = [(k, w) for k in S for w in WHO for _ in range(2)]
    with ThreadPoolExecutor(12) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "s": S[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
    for k in S:
        for w in WHO:
            s = {q: sum(a[q]["score"] for (kk, ww), a in res if kk == k and ww == w) / 2 for q in Q}
            print(k, f"{w:8}", "  ".join(f"{q} {v:.2f}" for q, v in s.items()))
