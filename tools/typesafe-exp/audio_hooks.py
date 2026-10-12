# What should the first 2 seconds SOUND like? (owner, 12 Oct 2026: "the hook isn't hooking; use ElevenLabs; a loud noise?")
# Same video for every option: a salah word quiz, the question and the big Arabic word on screen from frame 0.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/audio_hooks.py
# Result (12 Oct; stay past 3 s target / revert / non-Muslim, watch to the end, not annoying): E imam recitation then a voice 2.87 / 2.77 / 0.71,
#   end 2.81, 2.22 (best) · F owner's voice 2.81 / 2.78, end 2.77, 1.56 · C voice reads the question 2.77 / 2.48, end 2.73, 2.47 (least annoying)
#   · D "do you actually know?" 2.75 / 2.61, 1.62 · A today 2.78 / 2.38, end 2.63 · B loud bass hit 2.50 / 2.10, end 2.46, 1.17 (worst: cheap).
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A TikTok from a small account that teaches the Arabic of the daily prayer, seen in the For You feed with sound on. On screen from "
       "the first frame: 'What does this word in your salah mean?' and a big Arabic word (العَظِيم). What you hear in the first 2 seconds: ")
WHO = {"target": "a 27-year-old UK Muslim who prays but doesn't understand the Arabic",
       "revert": "a 31-year-old revert learning to pray",
       "nonmuslim": "a 24-year-old non-Muslim in the UK with no interest in Arabic or religion"}
A = {"A_now": "a soft fountain, then at 0.5 s the word said once, calmly",
     "B_bang": "a loud bass hit and whoosh at frame 0, then the word said",
     "C_vo_q": "a clear, warm British voice reading the question straight away: 'What does this word in your salah mean?'",
     "D_vo_you": "a warm British voice straight away: 'You say this word in every single rukūʿ. Do you actually know what it means?'",
     "E_imam": "an imam reciting 'subḥāna rabbiyal-ʿaẓīm' as in the prayer, then a voice: 'You say this every day. What does al-ʿaẓīm mean?'",
     "F_owner": "the account owner's own voice, casual, as if to a friend: 'Be honest, do you know what this word means? You say it every prayer.'"}
Q = {"stay": {"type": "score", "instructions": "`ctx` `a` Viewer: `who`. How likely are they to keep watching past 3 seconds?",
              "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "end": {"type": "score", "instructions": "`ctx` `a` Viewer: `who`. How likely are they to watch to the end (17 seconds) to see the answer?",
             "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "annoy": {"type": "score", "instructions": "`ctx` `a` Viewer: `who`. How cheap, annoying or clickbaity does the opening feel?",
               "criteria": ["Very", "Somewhat", "A little", "Not at all"]}}
if __name__ == "__main__":
    jobs = [(k, w) for k in A for w in WHO for _ in range(2)]
    with ThreadPoolExecutor(20) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "a": A[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
    print(f"{'':10}" + "".join(f"{'stay ' + w[:6]:>13}" for w in WHO) + "   end(t+r)  not-annoying(t+r)")
    for k in A:
        st = {w: sum(a["stay"]["score"] for (kk, ww), a in res if kk == k and ww == w) / 2 for w in WHO}
        en = sum(a["end"]["score"] for (kk, ww), a in res if kk == k and ww != "nonmuslim") / 4
        an = sum(a["annoy"]["score"] for (kk, ww), a in res if kk == k and ww != "nonmuslim") / 4
        print(f"{k:10}" + "".join(f"{st[w]:13.2f}" for w in WHO) + f"{en:11.2f}{an:12.2f}")
