#!/usr/bin/env python3
"""Three videos in the winning formula (brag-quiz/IDEAS.md, "What our best videos do"; #238): a question about something they
already say in the first second, one "aha" pattern, the viewer plays along, 15-26 s, the app last or not at all.

  f1-sujood     "You say this every time you go into sujūd": سُبْحانَ رَبِّيَ الْأَعْلى word by word (salah-data.js),
                ending on a comment everyone can answer: what do you say in rukūʿ instead? (like s3-samiallahu)
  f2-root       "Why do school and teacher look alike?": مَدْرَسَة, مُدَرِّس, دَرَسَ share د ر س; your turn: كِتاب (كَتَبَ, to write),
                3-2-1, a book (like t1-masjid). Meanings: vocab-data.js (book, school, teacher (m)) and toolkit-data.js (to study, to write).
  f3-she-eats   Quiz: if يَأْكُلُ is "he eats", what's "she eats"? Then the past: أَكَلَ → أَكَلَتْ, with أَكَلْتُ "I ate" as the trap
                (like v3-drink). Forms: toolkit-data.js VERBS أَكَلَ.

Every Arabic word is the app's own recording (audio-manifest.json). Built on build_series.py, build_teach.py and build_social.py,
which live on the claude/teach-videos branch: run this from a checkout of that branch.

  python3 brag-quiz/build_formula.py [id ...]     then in each brag-quiz/out/<id>/composition: npx hyperframes render -o ../<id>.mp4
  python3 brag-quiz/build_formula.py --level [id ...]
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build_teach as T, build_series as S, build_social as SO
from build_teach import Comp, word, e
from build_ten import cnt, countdown, reveal

def f1():
    S.build("f1-sujood", 4, 'You say this <b>every time</b> you go into sujūd', "سُبْحانَ رَبِّيَ الْأَعْلى", 104,
            [("سُبْحانَ", "Glory be to"), ("رَبِّيَ", "my Lord"), ("الْأَعْلى", "the Most High")], "“Glory be to my Lord, the Most High.”",
            "What do you say in rukūʿ instead? Comment it 👇")

def f2():
    c = Comp("f2-root", "ARABIC · ONE ROOT")
    ROWS = [([("مَ", "v"), ("دْ", "r"), ("رَ", "r"), ("سَ", "r"), ("ة", "")], "مَدْرَسَة", "a school"),
            ([("مُ", "v"), ("دَ", "r"), ("رِّ", "r"), ("س", "r")], "مُدَرِّس", "a teacher"),
            ([("دَ", "r"), ("رَ", "r"), ("سَ", "r")], "دَرَسَ", "to study")]
    BOOK = [("كِ", "r"), ("ت", "r"), ("ا", "v"), ("ب", "r")]
    # 1. the hook: school and teacher, side by side, then the verb
    c.inn("#a .q2", 0.1); t = 0.6
    for i, (_, ar, _) in enumerate(ROWS):
        c.inn(f"#r{i}", t, 30); c.sfx("tap", t); c.say(ar, t + 0.35); t += 1.9 if i < 2 else 1.6
    for i in range(3): c.t(f'tl.fromTo("#r{i} .pr", {{color:"{T.INK}"}}, {{color:"{T.RED}", duration:0.35}}, {t + i * 0.2:.2f});')
    c.sfx("tap", t); t += 0.9
    c.inn("#e1", t); c.sfx("tap", t); t += 1.0
    c.inn("#a .say", t); c.sfx("correct", t)
    c.t(f'tl.fromTo("#a .say", {{scale:1}}, {{scale:1.04, duration:0.16, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {t + 0.45:.2f});')
    t += 2.2; c.out_("#a", t)
    # 2. your turn: كِتاب from كَتَبَ, a 3-2-1, then the answer and the ask
    K = t + 0.4
    c.inn("#k .q2", K); c.t(f'tl.fromTo("#k .big", {{opacity:0, scale:0.94}}, {{opacity:1, scale:1, duration:0.5, ease:"power3.out"}}, {K + 0.3:.2f});')
    c.say("كِتاب", K + 0.6)
    c.t(f'tl.fromTo("#k .big .pr", {{color:"{T.INK}"}}, {{color:"{T.RED}", duration:0.3}}, {K + 1.4:.2f});')
    c.inn("#k .hint", K + 1.5)
    cs = K + 2.4
    c.t(f'tl.fromTo("#count", {{opacity:0, scale:0.7}}, {{opacity:1, scale:1, duration:0.3, ease:"power3.out"}}, {cs - 0.3:.2f});')
    c.t(f'tl.fromTo("#count .fg", {{strokeDashoffset:0}}, {{strokeDashoffset:408, duration:3, ease:"none"}}, {cs:.2f});')
    for k in range(3):
        c.t(f'tl.fromTo("#n{3 - k}", {{opacity:0, scale:1.35}}, {{opacity:1, scale:1, duration:0.22, ease:"power3.out"}}, {cs + k:.2f});')
        c.t(f'tl.to("#n{3 - k}", {{opacity:0, duration:0.15}}, {cs + k + 0.82:.2f});'); c.sfx("tap", cs + k)
    R = cs + 3.05
    c.t(f'tl.to("#count", {{opacity:0, scale:0.7, duration:0.25}}, {R - 0.15:.2f});')
    c.t(f'tl.fromTo("#k .ans", {{opacity:0, scale:0.9}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(1.6)"}}, {R:.2f});')
    c.sfx("correct", R); c.say("كِتاب", R + 0.5)
    c.inn("#k .ask2", R + 1.4)
    c.out_("#k", R + 4.0)
    E = R + 4.4
    endc = c.end(E, "Learn the roots behind the words")
    body = f"""      <div class="sec" id="a">
        <div class="q2">Why do <b>school</b> and <b>teacher</b> look alike in Arabic?</div>
        <div class="rows" style="top:480px">{''.join(f'<div class="row" id="r{i}"><div class="en"><b>{e(en)}</b></div><div class="ar">{word(p)}</div></div>' for i, (p, _, en) in enumerate(ROWS))}</div>
        <div class="eqs" style="top:1240px"><div class="eq" id="e1"><span class="tag r" lang="ar">د ر س</span><span class="t">= studying</span></div></div>
        <div class="say" style="top:1470px">Three words, one root.</div>
      </div>
      <div class="sec" id="k">
        <div class="q2">Your turn. What is a <bdi class="ar" lang="ar">كِتاب</bdi>?</div>
        <div class="big" style="top:440px">{word(BOOK)}</div>
        <div class="hint" style="top:800px"><bdi lang="ar" style="font-family:var(--ar);color:var(--rubric)">كَتَبَ</bdi> = to write</div>
        <div id="count" style="top:960px"><svg viewBox="0 0 150 150"><circle class="bg" cx="75" cy="75" r="65"/><circle class="fg" cx="75" cy="75" r="65"/></svg>{''.join(f'<span id="n{k}">{k}</span>' for k in range(3, 0, -1))}</div>
        <div class="ans" style="top:980px">a book</div>
        <div class="ask2" style="position:absolute;left:80px;right:80px;text-align:center;font-size:52px;font-weight:700;color:var(--ink-soft);top:1220px">Which word’s root should I show next? 👇</div>
      </div>
      {endc}"""
    c.write(body, round(E + 2.9, 2))

def f3():
    c = SO.vcomp("f3-she-eats", "QUIZ · ARABIC VERBS"); body, t = [], 0.1
    R = [("يَأْكُلُ", "he eats", "she eats", ["آكُلُ", "تَأْكُلُ", "نَأْكُلُ"], 1, '<bdi lang="ar"><em>يَ</em></bdi> → <bdi lang="ar"><em>تَ</em></bdi>'),
         ("أَكَلَ", "he ate", "she ate", ["أَكَلْتُ", "أَكَلَتْ", "أَكَلْنا"], 1, 'add <bdi lang="ar"><em>تْ</em></bdi> to the end')]
    for k, (ar, en, ask, opts, right, rule) in enumerate(R):
        s = f"r{k}"
        body.append(f'<div class="sec" id="{s}"><div class="q2">{k + 1}/2 · If this is “{en}” …</div>'
                    f'<div class="big" id="{s}b" style="top:380px;font-size:150px" lang="ar">{e(ar)}</div>'
                    f'<div class="ques" id="{s}q" style="top:680px">what’s <b>“{ask}”</b>?</div>{cnt(s + "c", 800)}'
                    f'<div class="ops" style="top:990px">' + "".join(f'<div class="op" id="{s}o{i}"><b><span class="ar" lang="ar" style="font-size:80px">{e(o)}</span></b></div>' for i, o in enumerate(opts))
                    + f'</div><div class="rule" id="{s}r" style="top:1500px;font-size:48px">the change: <span class="ar" style="font-size:64px">{rule}</span></div></div>')
        c.inn(f"#{s} .q2", t); SO.bigin(c, f"#{s}b", t + 0.3); d = c.say(ar, t + 0.6)
        c.inn(f"#{s}q", t + 0.6 + d + 0.2)
        for i in range(3): c.inn(f"#{s}o{i}", t + 1.0 + d + i * 0.12)
        done = countdown(c, f"{s}c", t + 1.6 + d + 0.5)
        reveal(c, f"#{s}o{right}", [f"#{s}o{i}" for i in range(3) if i != right], done)
        d2 = c.say(opts[right], done + 0.3); c.inn(f"#{s}r", done + 0.3 + d2)
        t = done + 0.3 + d2 + 2.4; c.out_(f"#{s}", t); t += 0.4
    SO.finish(c, body, t, "How many did you get? 0, 1 or 2? 👇")

ALL = {"f1-sujood": f1, "f2-root": f2, "f3-she-eats": f3}
if __name__ == "__main__":
    ids = [a for a in sys.argv[1:] if not a.startswith("--")]
    T.LUFS.update({v: -16.0 for v in ALL})
    for vid, fn in ALL.items():
        if ids and vid not in ids: continue
        T.level(vid) if "--level" in sys.argv else fn()
