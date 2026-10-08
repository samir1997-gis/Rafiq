#!/usr/bin/env python3
"""Two TikToks that break the quiz-card mould (#236). The reading voice only; hook on screen from the first frame.

  f1-chat      POV: an Arabic speaker texts you. Each message arrives with typing dots, your reply bubble counts down 3-2-1,
               then the right reply pops in and is said. vocab-data.js 1/2, 3/6, 110/184.
  f2-letters   Arabic letters change shape when they hold hands: ك ت ا ب drop in on their own, slide together and become كِتاب (150).
               Pull ب away and nothing changes, because ا never joins the letter after it. Then the same root grows:
               مَكْتَبَة (279) and كَتَبَ (toolkit-data.js VERBS).

  python3 brag-quiz/build_fresh.py [id ...]     then render each, then  --level
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build_teach as T
from build_teach import Comp, e, word

GREEN, PAPER = T.GREEN, "#f1ece0"

# ---------------------------------------------------------------- f1: the chat
CHAT_CSS = """
.hook { position:absolute; top:258px; left:40px; right:40px; text-align:center; font-size:57px; font-weight:700; line-height:1.1; letter-spacing:-.02em; }
.hook b { color:var(--rubric); }
.hook div + div { margin-top:6px; }
.phone { position:absolute; top:430px; left:56px; right:56px; height:1370px; background:var(--card); border:4px solid rgba(23,38,43,.13); border-radius:48px;
  box-shadow:0 18px 40px -20px rgba(23,38,43,.45); overflow:hidden; }
.head { position:absolute; top:0; left:0; right:0; height:130px; display:flex; align-items:center; gap:24px; padding:0 36px;
  border-bottom:3px solid rgba(23,38,43,.10); background:#efe9dc; }
.av { width:84px; height:84px; border-radius:50%; background:var(--verdigris); display:grid; place-items:center; }
.av span { font-family:var(--ar); font-weight:700; font-size:50px; color:var(--paper); margin-top:-6px; }
.who b { display:block; font-size:44px; font-weight:700; }
.who i { position:relative; display:block; height:40px; font-style:normal; font-size:32px; }
.who i span { position:absolute; left:0; top:0; white-space:nowrap; }
.st1 { color:var(--ink-soft); } .st2 { color:var(--verdigris); opacity:0; }
.feedw { position:absolute; top:130px; left:0; right:0; bottom:0; overflow:hidden; }
.feed { position:absolute; top:0; left:0; right:0; height:1200px; }
.b { position:absolute; height:176px; box-sizing:border-box; padding:12px 40px 0; border-radius:40px; display:flex; flex-direction:column; justify-content:center; }
.b .ar { font-family:var(--ar); font-weight:700; font-size:64px; line-height:1.45; direction:rtl; white-space:nowrap; }
.b .en { font-size:34px; font-weight:700; line-height:1.2; margin-top:-4px; }
.in { left:34px; background:#fff; border:3px solid rgba(23,38,43,.12); border-bottom-left-radius:10px; }
.in .ar { text-align:left; } .in .en { color:var(--ink-soft); }
.me { right:34px; background:var(--verdigris); border-bottom-right-radius:10px; color:var(--paper); }
.me .ar { text-align:right; } .me .en { text-align:right; opacity:.85; }
.wait { position:absolute; right:34px; width:330px; height:176px; box-sizing:border-box; border:5px dashed rgba(46,114,99,.55); border-radius:40px;
  border-bottom-right-radius:10px; display:flex; align-items:center; justify-content:center; gap:22px; }
.wait em { font-style:normal; font-size:40px; font-weight:700; color:var(--verdigris); }
.wait .n { position:relative; width:60px; height:80px; }
.wait .n span { position:absolute; inset:0; display:grid; place-items:center; font-size:70px; font-weight:700; color:var(--rubric); opacity:0; }
.dots { position:absolute; left:34px; width:190px; height:110px; background:#fff; border:3px solid rgba(23,38,43,.12); border-radius:40px;
  border-bottom-left-radius:10px; display:flex; align-items:center; justify-content:center; gap:16px; }
.dots i { width:22px; height:22px; border-radius:50%; background:var(--ink-soft); }
.score { position:absolute; left:110px; right:110px; top:880px; text-align:center; background:var(--ink); color:var(--paper); border-radius:40px;
  padding:34px 40px 40px; box-shadow:0 20px 40px -18px rgba(23,38,43,.6); }
.score b { display:block; font-size:62px; line-height:1.12; letter-spacing:-.02em; }
.score span { display:block; margin-top:14px; font-size:40px; font-weight:700; color:#bcd8cf; }
"""

CHAT = [("السَّلامُ عَلَيْكُم", "peace be upon you", "وَعَلَيْكُمُ السَّلام", "and peace be upon you"),
        ("كَيْفَ حالُكَ", "how are you?", "الحَمْدُ لِلَّهِ", "praise be to God (I'm well)"),
        ("شُكْراً", "thank you", "عَفْواً", "you're welcome")]
STEP = 205                                                       # one bubble (176px) and the gap under it

def f1():
    c = Comp("f1-chat", "POV · REPLY IN ARABIC", bed=False); c.css = CHAT_CSS
    feed, t = [], 0.3
    for k, (q, qe, a, ae) in enumerate(CHAT):
        yi, ya = 30 + 2 * k * STEP, 30 + (2 * k + 1) * STEP
        if k == 2:                                               # the third pair would run off the bottom: the chat scrolls up one bubble
            c.t(f'tl.to(".feed", {{y:-{STEP}, duration:0.45, ease:"power2.inOut"}}, {t:.2f});')
            c.t(f'tl.to("#m0", {{opacity:0, duration:0.3}}, {t:.2f});'); t += 0.3
        # Yusuf is typing…
        feed.append(f'<div class="dots" id="d{k}" style="top:{yi + 33}px"><i></i><i></i><i></i></div>')
        c.t(f'tl.fromTo("#d{k}", {{opacity:0, scale:0.8}}, {{opacity:1, scale:1, duration:0.2}}, {t:.2f});')
        c.t(f'tl.to([".st1"], {{opacity:0, duration:0.15}}, {t:.2f}); tl.to([".st2"], {{opacity:1, duration:0.15}}, {t:.2f});')
        for j in range(3):
            c.t(f'tl.fromTo("#d{k} i:nth-child({j + 1})", {{y:0}}, {{y:-14, duration:0.15, yoyo:true, repeat:3, ease:"sine.inOut"}}, {t + 0.1 + j * 0.1:.2f});')
        t += 0.75
        c.t(f'tl.to("#d{k}", {{opacity:0, duration:0.1}}, {t:.2f});')
        c.t(f'tl.to([".st2"], {{opacity:0, duration:0.15}}, {t:.2f}); tl.to([".st1"], {{opacity:1, duration:0.15}}, {t:.2f});')
        # his message, said
        feed.append(f'<div class="b in" id="m{k}" style="top:{yi}px"><div class="ar" lang="ar">{e(q)}</div><div class="en">{e(qe)}</div></div>')
        c.t(f'tl.fromTo("#m{k}", {{opacity:0, scale:0.85, transformOrigin:"0% 100%"}}, {{opacity:1, scale:1, duration:0.3, ease:"back.out(1.6)"}}, {t:.2f});')
        t += c.say(q, t + 0.1) + 0.35
        # your turn: 3, 2, 1
        feed.append(f'<div class="wait" id="w{k}" style="top:{ya}px"><em>you?</em><div class="n">{"".join(f"<span>{n}</span>" for n in (3, 2, 1))}</div></div>')
        c.t(f'tl.fromTo("#w{k}", {{opacity:0, scale:0.85, transformOrigin:"100% 100%"}}, {{opacity:1, scale:1, duration:0.25, ease:"back.out(1.6)"}}, {t:.2f});')
        for n in range(3):
            sel = f"#w{k} .n span:nth-child({n + 1})"
            c.t(f'tl.fromTo("{sel}", {{opacity:0, scale:1.4}}, {{opacity:1, scale:1, duration:0.2, ease:"power3.out"}}, {t + 0.15 + n:.2f});')
            c.t(f'tl.to("{sel}", {{opacity:0, duration:0.12}}, {t + 0.95 + n:.2f});')
        t += 3.1
        # the reply, said
        feed.append(f'<div class="b me" id="r{k}" style="top:{ya}px"><div class="ar" lang="ar">{e(a)}</div><div class="en">{e(ae)}</div></div>')
        c.t(f'tl.to("#w{k}", {{opacity:0, duration:0.15}}, {t:.2f});')
        c.t(f'tl.fromTo("#r{k}", {{opacity:0, scale:0.85, transformOrigin:"100% 100%"}}, {{opacity:1, scale:1, duration:0.3, ease:"back.out(1.6)"}}, {t:.2f});')
        t += c.say(a, t + 0.1) + 0.35
    c.t(f'tl.to(".feed", {{opacity:0, duration:0.3}}, {t:.2f});')
    c.t(f'tl.fromTo(".score", {{opacity:0, y:40, scale:0.92}}, {{opacity:1, y:0, scale:1, duration:0.4, ease:"back.out(1.5)"}}, {t:.2f});')
    t += 2.8
    body = ('      <div class="hook"><div>POV: an Arabic speaker texts you.</div><div><b>Can you reply in time?</b> ⏱️</div></div>'
            '<div class="phone"><div class="head"><div class="av"><span lang="ar">ي</span></div>'
            '<div class="who"><b>Yusuf</b><i><span class="st1" data-layout-allow-overlap>online</span><span class="st2" data-layout-allow-overlap>typing…</span></i></div></div>'
            f'<div class="feedw"><div class="feed" data-layout-allow-overflow>{"".join(feed)}</div></div>'
            '<div class="score" data-layout-allow-overlap data-layout-allow-occlusion><b>3 out of 3? You just had your first Arabic chat 💬</b><span>Your score in the comments 👇</span></div></div>')
    c.write(body, round(t, 2))

# ---------------------------------------------------------------- f2: letters hold hands
LET_CSS = """
.hook { position:absolute; top:262px; left:60px; right:60px; text-align:center; font-size:70px; font-weight:700; line-height:1.12; letter-spacing:-.02em; }
.hook b { color:var(--rubric); }
.stage { position:absolute; top:560px; left:0; right:0; height:380px; }
.iso { position:absolute; inset:0; display:flex; flex-direction:row-reverse; justify-content:center; align-items:center; gap:56px; }
.iso div { width:170px; height:230px; display:grid; place-items:center; background:var(--card); border:4px solid rgba(23,38,43,.13); border-radius:34px;
  box-shadow:0 12px 26px -16px rgba(23,38,43,.35); }
.iso span { font-family:var(--ar); font-weight:700; font-size:150px; line-height:1; margin-top:-30px; color:var(--ink); }
.join { position:absolute; inset:0; display:flex; flex-direction:row-reverse; justify-content:center; align-items:center; }
.join span { font-family:var(--ar); font-weight:700; font-size:230px; line-height:1.5; color:var(--ink); }
.join .bb { color:var(--rubric); }
.gl { position:absolute; top:960px; left:60px; right:60px; text-align:center; font-size:58px; font-weight:700; line-height:1.2; }
.gl em { font-style:normal; color:var(--ink-soft); font-weight:500; }
.note { position:absolute; top:1110px; left:60px; right:60px; text-align:center; font-size:50px; font-weight:700; line-height:1.18; letter-spacing:-.015em; }
.note .ar { font-family:var(--ar); color:var(--rubric); }
.six { position:absolute; top:1290px; left:110px; right:110px; display:flex; flex-direction:row-reverse; justify-content:space-between; }
.six span { width:118px; height:138px; display:grid; place-items:center; font-family:var(--ar); font-weight:700; font-size:86px; line-height:1; color:var(--rubric);
  background:var(--card); border:4px solid rgba(23,38,43,.13); border-radius:26px; }
.sixl { position:absolute; top:1460px; left:70px; right:70px; text-align:center; font-size:42px; font-weight:700; color:var(--ink-soft); }
.rt { position:absolute; top:520px; left:70px; right:70px; text-align:center; font-size:64px; font-weight:700; line-height:1.15; letter-spacing:-.02em; }
.rt .ar { font-family:var(--ar); color:var(--rubric); }
.fam { position:absolute; top:700px; left:90px; right:90px; display:flex; flex-direction:column; gap:28px; }
.fr { display:flex; align-items:center; justify-content:space-between; height:220px; padding:0 50px; background:var(--card); border:4px solid rgba(23,38,43,.13);
  border-radius:36px; box-shadow:0 12px 26px -16px rgba(23,38,43,.35); }
.fr .ar { font-family:var(--ar); font-weight:700; font-size:110px; line-height:1.45; color:var(--ink); }
.fr .ar .pr { color:var(--rubric); }
.fr .en b { display:block; font-size:58px; font-weight:700; }
.fr .en span { display:block; font-size:38px; color:var(--ink-soft); }
.root { position:absolute; top:1460px; left:70px; right:70px; text-align:center; font-size:66px; font-weight:700; letter-spacing:-.02em; }
.root .ar { font-family:var(--ar); color:var(--rubric); }
.ask { position:absolute; top:1610px; left:70px; right:70px; text-align:center; font-size:46px; font-weight:700; line-height:1.25; color:var(--ink-soft); }
"""

FAM = [("كِتاب", [("كِ", "r"), ("ت", "r"), ("ا", ""), ("ب", "r")], "book", "kitāb"),
       ("مَكْتَبَة", [("مَ", ""), ("كْ", "r"), ("تَ", "r"), ("بَ", "r"), ("ة", "")], "library", "maktaba"),
       ("كَتَبَ", [("كَ", "r"), ("تَ", "r"), ("بَ", "r")], "he wrote", "kataba")]

def f2():
    c = Comp("f2-letters", "HOW ARABIC IS WRITTEN", bed=False); c.css = LET_CSS
    # the four letters drop in on their own, right to left
    for i in range(4):
        c.t(f'tl.fromTo("#l{i}", {{opacity:0, y:-160}}, {{opacity:1, y:0, duration:0.4, ease:"bounce.out"}}, {0.3 + i * 0.3:.2f});')
    # …slide together (each card moves to the middle) and turn into one word
    for i, x in enumerate((-339, -113, 113, 339)):
        c.t(f'tl.to("#l{i}", {{x:{x // 3}, scale:0.8, duration:0.5, ease:"power2.in"}}, 1.9);')
    c.t('tl.to(".iso", {opacity:0, duration:0.2}, 2.3);')
    c.t('tl.fromTo(".join", {opacity:0, scale:0.85}, {opacity:1, scale:1, duration:0.4, ease:"back.out(1.7)"}, 2.35);')
    t = 2.5 + c.say("كِتاب", 2.5) + 0.2
    c.inn(".gl", 2.75)
    t = max(t, 4.3)
    # the twist: pull ب away and nothing changes
    c.inn("#n1", t); t += 0.7
    c.t(f'tl.to(".join .bb", {{x:-150, duration:0.5, ease:"power2.inOut"}}, {t:.2f});')
    c.t(f'tl.to(".join .bb", {{x:0, duration:0.5, ease:"power2.inOut"}}, {t + 1.3:.2f});')
    t += 2.0
    c.out_("#n1", t - 0.4); c.inn("#n2", t); t += 0.6
    for i in range(6): c.inn(f"#x{i}", t + i * 0.12, 30, 0.35)
    c.inn(".sixl", t + 0.8); t += 3.4
    # the same three letters make more words
    c.t(f'tl.to([".hook", ".stage", ".gl", "#n1", "#n2", ".six", ".sixl"], {{opacity:0, duration:0.35}}, {t:.2f});'); t += 0.4
    c.inn(".rt", t); t += 0.5
    for i, (ar, _, _, _) in enumerate(FAM):
        c.inn(f"#f{i}", t, 30); t += max(c.say(ar, t + 0.1), 0.8) + 0.45
    c.inn(".root", t); t += 1.2
    c.inn(".ask", t); t += 2.6
    rows = "".join(f'<div class="fr" id="f{i}">{word(p, "ar")}<div class="en"><b>{e(en)}</b><span>{e(tr)}</span></div></div>'
                   for i, (_, p, en, tr) in enumerate(FAM))
    body = ('      <div class="hook">Arabic letters <b>change shape</b> when they hold hands 🤝</div>'
            '<div class="stage"><div class="iso">' + "".join(f'<div id="l{i}"><span lang="ar">{x}</span></div>' for i, x in enumerate("كتاب")) + '</div>'
            '<div class="join" lang="ar"><span>كِتا</span><span class="bb">ب</span></div></div>'
            '<div class="gl">kitāb <em>·</em> book</div>'
            '<div class="note" id="n1">Pull <span class="ar">ب</span> away… and nothing changes 👀</div>'
            '<div class="note" id="n2" style="top:1110px">because <span class="ar">ا</span> never holds the next letter’s hand. These 6 never do:</div>'
            '<div class="six">' + "".join(f'<span id="x{i}" lang="ar">{x}</span>' for i, x in enumerate("ادذرزو")) + '</div>'
            '<div class="sixl">Every other letter joins the one after it.</div>'
            '<div class="rt">Same 3 letters, <span class="ar">ك ت ب</span>, more words:</div>'
            f'<div class="fam">{rows}</div>'
            '<div class="root"><span class="ar">ك ت ب</span> = writing ✍️</div>'
            '<div class="ask">Which root should I do next? 👇</div>')
    c.write(body, round(t, 2))

ALL = {"f1-chat": f1, "f2-letters": f2}
if __name__ == "__main__":
    ids = [a for a in sys.argv[1:] if not a.startswith("--")]
    T.LUFS.update({v: -16.0 for v in ALL})
    for vid, fn in ALL.items():
        if ids and vid not in ids: continue
        T.level(vid) if "--level" in sys.argv else fn()
