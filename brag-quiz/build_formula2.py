#!/usr/bin/env python3
"""Five more in the winning formula (brag-quiz/IDEAS.md, "What our best videos do"; #244): a question about something they
already say, on screen from the first frame (the cover) · one pattern that unlocks several words · a "your turn" round with a
3-second countdown · a comment anyone can answer · 18-22 s · the app card on one of the five only (4 posts in 5 pure content).

  p1-akbar    Why "Allāhu akbar", not "Allāhu kabīr"? كَبِير big → أَكْبَرُ the Greatest, الْأَعْلى the Most High; your turn: the name عَلِيّ
  p2-ana      The أَ at the start of أَشْهَدُ: أَشْهَدُ, أَعُوذُ, أَذْهَبُ = I…; your turn: أَكْتُبُ (كَتَبَ = to write). Ends on the app card.
  p3-li       The "li" in al-ḥamdu lillāh: لِلَّهِ for Allah, وَلَكَ and to You; your turn: لِي in رَبِّ اغْفِرْ لِي
  p4-hamd     Why Muhammad, Ahmad and al-ḥamdu sound alike: ح م د; your turn: مَحْمُود
  p5-insha    What in shā' Allāh actually says: إِنْ if, شاءَ willed, اللهُ Allah; your turn: ما شاءَ اللهُ

Sound: the app's reading voice, a soft tap as each piece appears and a chime on the answer; no fountain bed.
Meanings: salah-data.js, vocab-data.js (161 big, 233 God willing, 71 what God has willed), toolkit-data.js (أَذْهَبُ, أَكْتُبُ);
the names' meanings and "أَ = I", "لِ = for/to", "أَكْبَرُ from كَبِير" are general knowledge for the teacher to glance at.

  python3 brag-quiz/build_formula2.py [id ...]     then render each, then  --level
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build_teach as T
from build_teach import Comp, word, e

GREEN, RED, INK = T.GREEN, T.RED, T.INK
AR = lambda s: f'<bdi class="ar" lang="ar">{e(s)}</bdi>'

CSS = """
.q2 .ar, .hint .ar, .ask2 .ar { font-family:var(--ar); color:var(--rubric); }
.row .ar .pv, .big .pv { color:var(--ink); }
.row .ar { white-space:nowrap; }
.ask2 { position:absolute; left:70px; right:70px; text-align:center; font-size:52px; font-weight:700; line-height:1.2; color:var(--ink-soft); }
.ans { left:0; right:0; margin:0 auto; width:fit-content; padding:22px 56px; }
.exp { position:absolute; left:70px; right:70px; text-align:center; font-size:50px; font-weight:700; line-height:1.2; color:var(--ink); }
"""

V = [dict(id="p1-akbar", kicker="YOUR SALAH · ONE PATTERN",
          hook=f'Why do we say Allāhu <b>akbar</b>, not Allāhu <b>kabīr</b>?',
          rows=[([("كَ", "r"), ("بِ", "r"), ("ي", ""), ("ر", "r")], "كَبِير", "big", ""),
                ([("أَ", "v"), ("كْ", "r"), ("بَ", "r"), ("رُ", "r")], "أَكْبَرُ", "the Greatest", "Allāhu akbar"),
                ([("الْ", ""), ("أَ", "v"), ("عْ", "r"), ("ل", "r"), ("ى", "r")], "الْأَعْلى", "the Most High", "in sujūd")],
          tag="أَـ", eq="+ the root = <b>the most…</b>", say="Big → the Greatest.",
          turn=f'Your turn. If {AR("الْأَعْلى")} is “the Most High”, what does the name {AR("عَلِيّ")} mean?',
          big=[("عَ", "r"), ("لِ", "r"), ("يّ", "r")], big_audio="عَلِيّ", hint=f'same letters: {AR("ع ل ي")}',
          ans="high, exalted", ans_audio="عَلِيّ", exp="", ask="What do you say 33 times after salah? Comment it 👇", app=None),
     dict(id="p2-ana", kicker="ARABIC · ONE LETTER",
          hook=f'What’s the <b>{AR("أَ")}</b> at the start of {AR("أَشْهَدُ")}?',
          rows=[([("أَ", "v"), ("شْهَدُ", "")], "أَشْهَدُ", "I bear witness", "tashahhud"),
                ([("أَ", "v"), ("عُوذُ", "")], "أَعُوذُ", "I seek refuge", "aʿūdhu billāh"),
                ([("أَ", "v"), ("ذْهَبُ", "")], "أَذْهَبُ", "I go", "every day")],
          tag="أَـ", eq="at the start = <b>I</b>", say="One letter: “I”.",
          turn=f'Your turn. {AR("كَتَبَ")} = to write. So what is {AR("أَكْتُبُ")}?',
          big=[("أَ", "v"), ("كْتُبُ", "")], big_audio="أَكْتُبُ", hint="", ans="I write", ans_audio="أَكْتُبُ", exp="",
          ask="What do you say before you read the Quran? Comment it 👇", app="Every verb, from I to we"),
     dict(id="p3-li", kicker="YOUR SALAH · ONE LETTER",
          hook='You say al-ḥamdu <b>li</b>llāh every day. What does the <b>li</b> mean?',
          rows=[([("الْحَمْدُ ", ""), ("لِ", "v"), ("لَّهِ", "")], "الْحَمْدُ لِلَّهِ", "praise is for Allah", "", 80),
                ([("رَبَّنا وَ", ""), ("لَ", "v"), ("كَ الْحَمْدُ", "")], "رَبَّنا وَلَكَ الْحَمْدُ", "and to You", "rising from ruku", 64)],
          tag="لِ لَ", eq="= <b>for, to</b>", say="Praise is for Allah.",
          turn=f'Your turn. Between the sujūd you say {AR("رَبِّ اغْفِرْ لِي")}. What’s {AR("لِي")}?',
          big=[("لِ", "v"), ("ي", "")], big_audio="لِي", hint="", ans="(for) me", ans_audio="رَبِّ اغْفِرْ لِي",
          exp="“My Lord, forgive me.”", ask="Someone sneezes and says al-ḥamdu lillāh. What do you reply? 👇", app=None),
     dict(id="p4-hamd", kicker="ARABIC · ONE ROOT",
          hook='Why do <b>Muhammad</b>, <b>Ahmad</b> and al-<b>ḥamdu</b> sound alike?',
          rows=[([("الْ", ""), ("حَ", "r"), ("مْ", "r"), ("دُ", "r")], "الْحَمْدُ", "praise", ""),
                ([("مُ", "v"), ("حَ", "r"), ("مَّ", "r"), ("د", "r")], "مُحَمَّد", "the praised one", ""),
                ([("أَ", "v"), ("حْ", "r"), ("مَ", "r"), ("د", "r")], "أَحْمَد", "most praiseworthy", "")],
          tag="ح م د", eq="= <b>praise</b>", say="Three words, one root.",
          turn=f'Your turn. What does the name {AR("مَحْمُود")} mean?',
          big=[("مَ", "v"), ("حْ", "r"), ("مُ", "r"), ("و", "v"), ("د", "r")], big_audio="مَحْمُود", hint=f'{AR("ح م د")} = praise',
          ans="praised", ans_audio="مَحْمُود", exp="", ask="Tag a Muhammad, Ahmad or Mahmoud 👇", app=None),
     dict(id="p5-insha", kicker="ARABIC YOU ALREADY SAY",
          hook='What does in shā’ Allāh <b>actually</b> say?',
          rows=[([("إِنْ", "")], "إِنْ", "if", ""), ([("شاءَ", "r")], "شاءَ", "(He) willed", ""), ([("اللهُ", "")], "اللهُ", "Allah", "")],
          tag="إِنْ شاءَ اللهُ", eq="= <b>if Allah wills</b>", say="“God willing.”", say_audio="إِنْ شاءَ اللهُ",
          turn=f'Your turn. {AR("ما")} = what. So what is {AR("ما شاءَ اللهُ")}?',
          big=[("ما ", ""), ("شاءَ", "r"), (" اللهُ", "")], big_size=150, big_audio="ما شاءَ اللهُ", hint="",
          ans="what Allah has willed", ans_audio="ما شاءَ اللهُ", exp="", ask="When do you say mā shā’ Allāh? Comment it 👇", app=None)]

def build(v):
    c = Comp(v["id"], v["kicker"], bed=False); c.css = CSS
    rows, t = v["rows"], 0.85
    # 1. the hook fills the first frame (the cover), then moves up; the words arrive one by one, each said
    c.t('tl.fromTo("#a .q2", {y:520, scale:1.12}, {y:0, scale:1, duration:0.5, ease:"power3.inOut"}, 0.3);')
    for i, r in enumerate(rows):
        c.inn(f"#r{i}", t, 30); c.sfx("tap", t); d = c.say(r[1], t + 0.3); t += max(d, 0.9) + 0.75
    c.t(f'tl.to("#a .pr", {{color:"{RED}", duration:0.35, stagger:0.06}}, {t:.2f});')
    c.t(f'tl.to("#a .pv", {{color:"{GREEN}", duration:0.35, stagger:0.06}}, {t:.2f});'); c.sfx("tap", t); t += 0.9
    c.inn("#e1", t); c.sfx("tap", t); t += 1.0
    c.inn("#a .say", t); c.sfx("correct", t)
    if v.get("say_audio"): t += c.say(v["say_audio"], t + 0.3) + 0.3
    t += 1.9; c.out_("#a", t)
    # 2. your turn: the word, said; a 3-2-1; the answer; a comment anyone can answer
    K = t + 0.4
    c.inn("#k .q2", K)
    c.t(f'tl.fromTo("#k .big", {{opacity:0, scale:0.94}}, {{opacity:1, scale:1, duration:0.5, ease:"power3.out"}}, {K + 0.3:.2f});')
    c.say(v["big_audio"], K + 0.6)
    c.t(f'tl.to("#k .big .pr", {{color:"{RED}", duration:0.3}}, {K + 1.4:.2f}); tl.to("#k .big .pv", {{color:"{GREEN}", duration:0.3}}, {K + 1.4:.2f});')
    if v["hint"]: c.inn("#k .hint", K + 1.5)
    cs = K + 2.4
    c.t(f'tl.fromTo("#count", {{opacity:0, scale:0.7}}, {{opacity:1, scale:1, duration:0.3, ease:"power3.out"}}, {cs - 0.3:.2f});')
    c.t(f'tl.fromTo("#count .fg", {{strokeDashoffset:0}}, {{strokeDashoffset:408, duration:3, ease:"none"}}, {cs:.2f});')
    for k in range(3):
        c.t(f'tl.fromTo("#n{3 - k}", {{opacity:0, scale:1.35}}, {{opacity:1, scale:1, duration:0.22, ease:"power3.out"}}, {cs + k:.2f});')
        c.t(f'tl.to("#n{3 - k}", {{opacity:0, duration:0.15}}, {cs + k + 0.82:.2f});'); c.sfx("tap", cs + k)
    R = cs + 3.05
    c.t(f'tl.to("#count", {{opacity:0, scale:0.7, duration:0.25}}, {R - 0.15:.2f});')
    c.t(f'tl.fromTo("#k .ans", {{opacity:0, scale:0.9}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(1.6)"}}, {R:.2f});')
    c.sfx("correct", R); d = c.say(v["ans_audio"], R + 0.5)
    if v["exp"]: c.inn("#k .exp", R + 0.9)
    c.inn("#k .ask2", R + 1.5)
    E = R + max(4.0, d + 2.2)
    endc = ""
    if v["app"]:                                                   # one post in five: the app, after the payoff, briefly
        c.out_("#k", E); endc = c.end(E + 0.4, v["app"]); total = E + 2.6
    else:
        total = E + 0.4
    n = len(rows); top = 500 if n == 3 else 560
    def row(i, r):
        size = f' style="font-size:{r[4]}px"' if len(r) > 4 else ""
        sub = f"<span>{e(r[3])}</span>" if r[3] else ""
        return f'<div class="row" id="r{i}"><div class="en"><b>{e(r[2])}</b>{sub}</div><div class="ar"{size}>{word(r[0])}</div></div>'
    eq_top = top + n * 218 + (n - 1) * 26 + 54
    big_size = f' style="top:440px;font-size:{v["big_size"]}px"' if v.get("big_size") else ' style="top:440px"'
    body = f"""      <div class="sec" id="a">
        <div class="q2">{v["hook"]}</div>
        <div class="rows" style="top:{top}px">{''.join(row(i, r) for i, r in enumerate(rows))}</div>
        <div class="eqs" style="top:{eq_top}px"><div class="eq" id="e1"><span class="tag v" lang="ar">{e(v["tag"])}</span><span class="t">{v["eq"]}</span></div></div>
        <div class="say" style="top:{eq_top + 210}px">{e(v["say"])}</div>
      </div>
      <div class="sec" id="k">
        <div class="q2">{v["turn"]}</div>
        <div class="big"{big_size}>{word(v["big"])}</div>
        <div class="hint" style="top:800px">{v["hint"]}</div>
        <div id="count" style="top:960px"><svg viewBox="0 0 150 150"><circle class="bg" cx="75" cy="75" r="65"/><circle class="fg" cx="75" cy="75" r="65"/></svg>{''.join(f'<span id="n{k}">{k}</span>' for k in range(3, 0, -1))}</div>
        <div class="ans" style="top:980px">{e(v["ans"])}</div>
        <div class="exp" style="top:1150px">{e(v["exp"])}</div>
        <div class="ask2" style="top:{1320 if v["exp"] else 1200}px">{e(v["ask"])}</div>
      </div>
      {endc}"""
    c.write(body, round(total, 2))

ALL = {v["id"]: v for v in V}
if __name__ == "__main__":
    ids = [a for a in sys.argv[1:] if not a.startswith("--")]
    T.LUFS.update({k: -16.0 for k in ALL})
    for k, v in ALL.items():
        if ids and k not in ids: continue
        T.level(k) if "--level" in sys.argv else build(v)
