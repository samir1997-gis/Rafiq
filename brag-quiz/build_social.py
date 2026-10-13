#!/usr/bin/env python3
"""Ten TikToks (#222): five videos and five carousels. Words of the day, the app's real screens, and verbs from I to we.

  Videos (1080x1920, the reading voice only):
    w1-shukran     Word of the day: شُكْراً, then شُكْراً جَزِيلاً and the reply عَفْواً.
    a1-tour        The app in 20 seconds: real screens (home, a lesson, your salah, verb forms, practise).
    v1-go          ذَهَبَ "to go", I to we in the present: only the first letter changes (and "you" and "she" match).
    v2-write       كَتَبَ "to write", I to we in the past: only the ending changes.
    v3-drink       Quiz: أَشْرَبُ is "I drink"; what's "we drink"? Then the past.
  Carousels (1080x1350, TikTok photo mode):
    c1-sadiq       Word of the day: صَدِيق / صَدِيقَة, friend, in a real phrase.
    c2-rihla       Word of the day: رِحْلَة, journey, and رِحْلَة سَعِيدَة.
    c3-salah       Your salah, word by word: real screens.
    c4-inside      What's inside Rafiq: real screens.
    c5-study       دَرَسَ "to study", one slide per person, I to we.

Words, forms and meanings: vocab-data.js, drills-data.js, toolkit-data.js (VERBS). Screens: brag-social/screens/, captured
from the app running locally with a test account (no made-up progress). Notes and captions: brag-social/SOCIAL.md.

  python3 brag-quiz/build_social.py [id ...]          videos -> brag-quiz/out/<id>/composition, carousels -> brag-social/<id>/
  then for each video:  npx hyperframes render -o ../<id>.mp4   and   python3 brag-quiz/build_social.py --level [id ...]
"""
import html, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
import build_teach as T
from build_ten import comp, cnt, countdown, reveal, ops
from build_teach import e, mixed, GREEN, RED
SOC = os.path.join(ROOT, "brag-social"); SCREENS = os.path.join(SOC, "screens")
FONTS = "file://" + os.path.join(ROOT, "brag-output-v6/composition/assets/fonts")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

# the verb forms, as in toolkit-data.js VERBS (I, you m, you f, he, she, we), split so the part that changes can be coloured
PRON = [("أَنا", "I"), ("أَنْتَ", "you (m)"), ("أَنْتِ", "you (f)"), ("هُوَ", "he"), ("هِيَ", "she"), ("نَحْنُ", "we")]
GO = [[("أَ", 1), ("ذْهَبُ", 0)], [("تَ", 1), ("ذْهَبُ", 0)], [("تَ", 1), ("ذْهَبِ", 0), ("ينَ", 1)],
      [("يَ", 1), ("ذْهَبُ", 0)], [("تَ", 1), ("ذْهَبُ", 0)], [("نَ", 1), ("ذْهَبُ", 0)]]
WROTE = [[("كَتَبْ", 0), ("تُ", 1)], [("كَتَبْ", 0), ("تَ", 1)], [("كَتَبْ", 0), ("تِ", 1)],
         [("كَتَبَ", 0)], [("كَتَبَ", 0), ("تْ", 1)], [("كَتَبْ", 0), ("نا", 1)]]
STUDY = [[("أَ", 1), ("دْرُسُ", 0)], [("تَ", 1), ("دْرُسُ", 0)], [("تَ", 1), ("دْرُسِ", 0), ("ينَ", 1)],
         [("يَ", 1), ("دْرُسُ", 0)], [("تَ", 1), ("دْرُسُ", 0)], [("نَ", 1), ("دْرُسُ", 0)]]
flat = lambda ps: "".join(t for t, _ in ps)
paint = lambda ps: "".join(f'<em>{e(t)}</em>' if k else e(t) for t, k in ps)

def check_forms():
    """every split above must put back together into the app's own form"""
    import re, subprocess, json
    src = open(os.path.join(ROOT, "toolkit-data.js")).read()
    data = json.loads(subprocess.check_output(["node", "-e", src.replace("const VERBS=", "global.VERBS=")
                                               + ";console.log(JSON.stringify(VERBS))"]).decode())
    V = {v["ar"]: v for v in data}
    for ar, key, forms in (("ذَهَبَ", "pr", GO), ("كَتَبَ", "past", WROTE), ("دَرَسَ", "pr", STUDY)):
        got = [flat(f) for f in forms]
        assert got == V[ar][key], (ar, got, V[ar][key])
    for f in V["شَرِبَ"]["pr"][::5] + V["شَرِبَ"]["past"][::5]: assert f in T.AUDIO, f
    return V

# ======================================================================== videos
VCSS = """
.vrows { position:absolute; left:80px; right:80px; display:flex; flex-direction:column; gap:16px; }
.vrow { display:flex; align-items:center; justify-content:space-between; height:156px; padding:0 44px; background:var(--card);
  border:4px solid rgba(23,38,43,.13); border-radius:32px; box-shadow:0 12px 26px -16px rgba(23,38,43,.35); }
.vrow .p { display:flex; flex-direction:column; align-items:flex-start; }
.vrow .p .ar { font-family:var(--ar); font-weight:700; font-size:56px; line-height:1.4; color:var(--ink-soft); }
.vrow .p .en { font-size:34px; font-weight:700; color:var(--ink-soft); margin-top:-6px; }
.vrow .f { font-family:var(--ar); font-weight:700; font-size:92px; line-height:1.4; }
.vrow .f em, .big em, .rule em { font-style:normal; color:var(--rubric); }
.vrow .g { font-size:40px; font-weight:700; color:var(--verdigris); }
.rule { position:absolute; left:80px; right:80px; text-align:center; font-size:56px; font-weight:700; line-height:1.3; }
.rule .ar { font-family:var(--ar); font-size:76px; }
.phone { position:absolute; left:50%; width:560px; margin-left:-280px; border-radius:64px; background:#17262b; padding:16px;
  box-sizing:border-box; box-shadow:0 40px 80px -30px rgba(23,38,43,.55); }
.phone .scr { border-radius:50px; overflow:hidden; }
.phone img { display:block; width:528px; border-radius:50px; }
.cap2 { position:absolute; left:60px; right:60px; text-align:center; font-size:60px; font-weight:700; line-height:1.15; letter-spacing:-.02em; }
.cap2 b { color:var(--verdigris); }
"""

def vcomp(vid, kicker):
    c = comp(vid, kicker); c.css += VCSS
    return c

def finish(c, body, E, line):
    body.append(c.end(E, line))
    c.write("\n".join("      " + b for b in body), round(E + 2.9, 2))

def bigin(c, sel, at):
    c.t(f'tl.fromTo("{sel}", {{opacity:0, scale:0.94}}, {{opacity:1, scale:1, duration:0.45, ease:"power3.out"}}, {at:.2f});')

def w1():
    c = vcomp("w1-shukran", "WORD OF THE DAY"); body, t = [], 0.1
    body.append('<div class="sec" id="a"><div class="q2">The first word to learn in any language:</div>'
                '<div class="big" id="a1" style="top:520px" lang="ar">شُكْراً</div><div class="tr2" id="a2" style="top:880px">shukran</div>'
                '<div class="ques" id="a3" style="top:960px"><b>thank you</b></div></div>')
    c.inn("#a .q2", t); bigin(c, "#a1", t + 0.4); d = c.say("شُكْراً", t + 0.8)
    c.inn("#a2", t + 0.8 + d); c.inn("#a3", t + 1.2 + d); t = t + 1.2 + d + 2.2
    c.out_("#a", t); t += 0.4
    for k, (lab, ar, en) in enumerate([("Level up:", "شُكْراً جَزِيلاً.", "Thank you very much."),
                                       ("Say it at home:", "شُكْراً يا أُمِّي.", "Thank you, mother."),
                                       ("And the reply:", "عَفْواً", "you’re welcome")]):
        s = f"b{k}"
        body.append(f'<div class="sec" id="{s}"><div class="q2">{e(lab)}</div><div class="big" id="{s}1" style="top:520px;font-size:150px" lang="ar">{e(ar)}</div>'
                    f'<div class="ques" id="{s}2" style="top:900px"><b>{e(en)}</b></div></div>')
        c.inn(f"#{s} .q2", t); bigin(c, f"#{s}1", t + 0.3); d = c.say(ar, t + 0.6); c.inn(f"#{s}2", t + 0.6 + d)
        t = t + 0.6 + d + 2.0; c.out_(f"#{s}", t); t += 0.4
    finish(c, body, t, "A new word every day, with audio")

def a1():
    c = vcomp("a1-tour", "RAFIQ · THE APP"); body, t = [], 0.1
    import shutil
    S = [("lesson", "Short lessons. <b>Every word with audio.</b>", "السَّلامُ عَلَيْكُم"),
         ("salah-l1", "Your salah, <b>word by word</b>", "سُبْحانَ"), ("verbs-table", "Every verb, <b>I to we</b>", "ذَهَبَ"),
         ("practise-2", "Weak spots, spelling bee, <b>real-life scenes</b>", None),
         ("vocab", "Your words come back <b>just before you’d forget</b>", None)]
    os.makedirs(os.path.join(c.a, "img"), exist_ok=True)
    for k, (img, cap, say) in enumerate(S):
        shutil.copy(os.path.join(SCREENS, img + ".png"), os.path.join(c.a, "img"))
        s = f"sc{k}"                     # not s<k>: the audio clips use those ids
        body.append(f'<div class="sec" id="{s}"><div class="cap2" style="top:250px">{cap}</div>'
                    f'<div class="phone" style="top:420px"><div class="scr"><img src="assets/img/{img}.png" alt=""></div></div></div>')
        c.inn(f"#{s} .cap2", t)
        c.t(f'tl.fromTo("#{s} .phone", {{opacity:0, y:70}}, {{opacity:1, y:0, duration:0.55, ease:"power3.out"}}, {t + 0.1:.2f});')
        c.t(f'tl.fromTo("#{s} .phone img", {{scale:1}}, {{scale:1.04, duration:3.2, ease:"none", transformOrigin:"50% 30%"}}, {t + 0.1:.2f});')
        hold = 3.0
        if say: d = c.say(say, t + 0.8); hold = max(hold, 0.8 + d + 1.0)
        t += hold; c.out_(f"#{s}", t); t += 0.35
    finish(c, body, t, "Learn Arabic for your salah and for life")

def ladder(c, forms, ens, t, top=420):
    """six rows, one per person: pronoun, the form (changing part in red), English; each said as it appears"""
    rows = "".join(f'<div class="vrow" id="r{i}"><div class="p"><span class="ar" lang="ar">{e(p)}</span><span class="en">{ens[i]}</span></div>'
                   f'<span class="f" lang="ar">{paint(f)}</span></div>' for i, (f, (p, _)) in enumerate(zip(forms, PRON)))
    html_ = f'<div class="vrows" style="top:{top}px">{rows}</div>'
    for i, f in enumerate(forms):
        c.inn(f"#r{i}", t, 30); d1 = c.say(PRON[i][0], t + 0.15); d2 = c.say(flat(f), t + 0.15 + d1 + 0.15)
        t = t + 0.15 + d1 + 0.15 + d2 + 0.45
    return html_, t

def v1():
    c = vcomp("v1-go", "ARABIC VERBS · I TO WE"); body, t = [], 0.1
    body.append('<div class="ques" id="h1" style="top:600px">How does “to go” change</div><div class="ques" id="h2" style="top:820px"><b>from I to we?</b></div>'
                '<div class="big" id="h3" style="top:960px;font-size:170px" lang="ar">ذَهَبَ</div>')
    c.inn("#h1", t); c.inn("#h2", t + 0.4); bigin(c, "#h3", t + 0.8); d = c.say("ذَهَبَ", t + 1.1)
    t = t + 1.1 + d + 1.2; c.out_("#h1, #h2, #h3", t); t += 0.4
    rows, t2 = ladder(c, GO, ["I go", "you go", "you go", "he goes", "she goes", "we go"], t + 0.5)
    body.append(f'<div class="sec" id="a"><div class="q2" style="font-size:58px">Present tense: watch the red</div>{rows}</div>')
    c.inn("#a .q2", t); t = t2 + 0.8
    c.out_("#a", t); t += 0.4
    body.append('<div class="sec" id="b"><div class="rule" id="b1" style="top:420px">I go <span class="ar" lang="ar"><em>أَ</em>ذْهَبُ</span></div>'
                '<div class="rule" id="b2" style="top:600px">we go <span class="ar" lang="ar"><em>نَ</em>ذْهَبُ</span></div>'
                '<div class="sub" id="b3" style="top:830px">Only the first letter changes.</div>'
                '<div class="sub" id="b4" style="top:950px">And “you go” and “she goes” are the same word: <bdi class="ar" lang="ar">تَذْهَبُ</bdi>.</div></div>')
    c.inn("#b1", t); c.inn("#b2", t + 0.5); c.inn("#b3", t + 1.2); c.inn("#b4", t + 2.6)
    t += 5.4; c.out_("#b", t); t += 0.4
    finish(c, body, t, "21 verbs, every form, with audio")

def v2():
    c = vcomp("v2-write", "ARABIC VERBS · I TO WE"); body, t = [], 0.1
    body.append('<div class="ques" id="h1" style="top:600px">“I wrote” → “we wrote”</div><div class="ques" id="h2" style="top:720px"><b>Only the ending changes.</b></div>'
                '<div class="big" id="h3" style="top:960px;font-size:170px" lang="ar">كَتَبَ</div>')
    c.inn("#h1", t); c.inn("#h2", t + 0.4); bigin(c, "#h3", t + 0.8); d = c.say("كَتَبَ", t + 1.1)
    t = t + 1.1 + d + 1.2; c.out_("#h1, #h2, #h3", t); t += 0.4
    rows, t2 = ladder(c, WROTE, ["I wrote", "you wrote", "you wrote", "he wrote", "she wrote", "we wrote"], t + 0.5)
    body.append(f'<div class="sec" id="a"><div class="q2" style="font-size:58px">Past tense: watch the ending</div>{rows}</div>')
    c.inn("#a .q2", t); t = t2 + 0.8
    c.out_("#a", t); t += 0.4
    body.append('<div class="sec" id="b"><div class="rule" id="b1" style="top:420px">I wrote <span class="ar" lang="ar">كَتَبْ<em>تُ</em></span></div>'
                '<div class="rule" id="b2" style="top:600px">we wrote <span class="ar" lang="ar">كَتَبْ<em>نا</em></span></div>'
                '<div class="sub" id="b3" style="top:830px">“He wrote” has no ending at all: <bdi class="ar" lang="ar">كَتَبَ</bdi>. That’s the form the dictionary gives you.</div></div>')
    c.inn("#b1", t); c.inn("#b2", t + 0.5); c.inn("#b3", t + 1.4)
    t += 5.0; c.out_("#b", t); t += 0.4
    finish(c, body, t, "21 verbs, every form, with audio")

def v3():
    c = vcomp("v3-drink", "QUIZ · ARABIC VERBS"); body, t = [], 0.1
    R = [("أَشْرَبُ", "I drink", "we drink", ["يَشْرَبُ", "نَشْرَبُ", "تَشْرَبُ"], 1, '<bdi lang="ar"><em>أَ</em></bdi> → <bdi lang="ar"><em>نَ</em></bdi>'),
         ("شَرِبْتُ", "I drank", "we drank", ["شَرِبْنا", "شَرِبَتْ", "شَرِبْتَ"], 0, '<bdi lang="ar">ـ<em>تُ</em></bdi> → <bdi lang="ar">ـ<em>نا</em></bdi>')]
    for k, (ar, en, ask, opts, right, rule) in enumerate(R):
        s = f"r{k}"
        body.append(f'<div class="sec" id="{s}"><div class="q2">{k + 1}/2 · If this is “{en}” …</div>'
                    f'<div class="big" id="{s}b" style="top:380px;font-size:150px" lang="ar">{e(ar)}</div>'
                    f'<div class="ques" id="{s}q" style="top:680px">what’s <b>“{ask}”</b>?</div>{cnt(s + "c", 800)}'
                    f'<div class="ops" style="top:990px">' + "".join(f'<div class="op" id="{s}o{i}"><b><span class="ar" lang="ar" style="font-size:80px">{e(o)}</span></b></div>' for i, o in enumerate(opts))
                    + f'</div><div class="rule" id="{s}r" style="top:1500px;font-size:48px">the change: <span class="ar" style="font-size:64px">{rule}</span></div></div>')
        c.inn(f"#{s} .q2", t); bigin(c, f"#{s}b", t + 0.3); d = c.say(ar, t + 0.6)
        c.inn(f"#{s}q", t + 0.6 + d + 0.2)
        for i in range(3): c.inn(f"#{s}o{i}", t + 1.0 + d + i * 0.12)
        done = countdown(c, f"{s}c", t + 1.6 + d + 0.5)
        reveal(c, f"#{s}o{right}", [f"#{s}o{i}" for i in range(3) if i != right], done)
        d2 = c.say(opts[right], done + 0.3); c.inn(f"#{s}r", done + 0.3 + d2)
        t = done + 0.3 + d2 + 2.4; c.out_(f"#{s}", t); t += 0.4
    finish(c, body, t, "Spot the pattern once, use it on every verb")

VIDEOS = {"w1-shukran": w1, "a1-tour": a1, "v1-go": v1, "v2-write": v2, "v3-drink": v3}

# ======================================================================== carousels
CCSS = f"""
@font-face {{ font-family:"Plex Arabic"; src:url("{FONTS}/ibm-plex-sans-arabic-arabic-700-normal.woff2"); font-weight:700; }}
@font-face {{ font-family:"Karla"; src:url("{FONTS}/karla-latin-500-normal.woff2"); font-weight:500; }}
@font-face {{ font-family:"Karla"; src:url("{FONTS}/karla-latin-700-normal.woff2"); font-weight:700; }}
@font-face {{ font-family:"JetBrains Mono"; src:url("{FONTS}/jetbrains-mono-latin-500-normal.woff2"); font-weight:500; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; width:1080px; height:1350px; overflow:hidden; position:relative; background:#f1ece0; color:#17262b; font-family:"Karla",sans-serif;
  background-image:radial-gradient(circle at 50% -10%, rgba(168,132,44,.22) 0%, rgba(168,132,44,.05) 40%, rgba(241,236,224,0) 62%); }}
.brand {{ position:absolute; top:62px; left:0; right:0; display:flex; justify-content:center; align-items:center; gap:14px; }}
.brand b {{ font-family:"Plex Arabic"; font-size:40px; font-weight:700; }}
.tile {{ position:relative; width:56px; height:56px; border-radius:14px; background:#17262b; display:grid; place-items:center; }}
.tile span {{ font-family:"Plex Arabic"; font-weight:700; font-size:34px; color:#f1ece0; margin-top:-5px; }}
.tile em {{ position:absolute; right:9px; top:8px; width:9px; height:9px; border-radius:50%; background:#b4322a; }}
.kicker {{ position:absolute; top:156px; left:0; right:0; text-align:center; font-family:"JetBrains Mono"; font-size:26px; letter-spacing:.16em; color:#4f6163; }}
.h {{ position:absolute; top:206px; left:80px; right:80px; text-align:center; font-size:60px; font-weight:700; line-height:1.14; letter-spacing:-.02em; }}
.h b {{ color:#2e7263; }}
.ar {{ font-family:"Plex Arabic"; font-weight:700; }}
.word {{ position:absolute; left:0; right:0; text-align:center; font-family:"Plex Arabic"; font-weight:700; font-size:200px; line-height:1.3; }}
.word em, .form em, .ar em {{ font-style:normal; color:#b4322a; }}
.tr {{ position:absolute; left:0; right:0; text-align:center; font-family:"JetBrains Mono"; font-size:46px; color:#2e7263; }}
.en {{ position:absolute; left:80px; right:80px; text-align:center; font-size:60px; font-weight:700; line-height:1.2; }}
.note {{ position:absolute; left:110px; right:110px; text-align:center; font-size:40px; font-weight:500; color:#4f6163; line-height:1.35; }}
.note .ar {{ color:#b4322a; font-size:46px; }}
.card {{ position:absolute; left:90px; right:90px; background:#f7f3ea; border:4px solid rgba(23,38,43,.13); border-radius:40px; padding:30px 40px 40px;
  text-align:center; box-shadow:0 14px 30px -18px rgba(23,38,43,.4); }}
.card .ar {{ font-size:80px; line-height:1.5; color:#2e7263; }}
.card .en2 {{ font-size:48px; font-weight:700; margin-top:4px; }}
.foot {{ position:absolute; bottom:70px; left:0; right:0; text-align:center; font-size:42px; font-weight:700; color:#2e7263; }}
.cta {{ position:absolute; left:50%; transform:translateX(-50%); white-space:nowrap; font-size:52px; font-weight:700; color:#f1ece0; background:#2e7263;
  border-radius:999px; padding:26px 60px; }}
.phone {{ position:absolute; left:50%; border-radius:56px; background:#17262b; padding:14px; box-shadow:0 40px 80px -30px rgba(23,38,43,.55); overflow:hidden; }}
.phone img {{ display:block; border-radius:44px; }}
.form {{ position:absolute; left:0; right:0; text-align:center; font-family:"Plex Arabic"; font-weight:700; font-size:220px; line-height:1.3; }}
.pron {{ position:absolute; left:0; right:0; text-align:center; font-family:"Plex Arabic"; font-weight:700; font-size:90px; color:#4f6163; line-height:1.4; }}
.tbl {{ position:absolute; left:110px; right:110px; display:flex; flex-direction:column; gap:12px; }}
.tbl div {{ display:flex; justify-content:space-between; align-items:center; background:#f7f3ea; border:3px solid rgba(23,38,43,.12); border-radius:26px; padding:0 40px; height:104px; }}
.tbl span {{ font-size:40px; font-weight:700; color:#4f6163; }}
.tbl .ar {{ font-size:66px; color:#17262b; }}
"""
BRAND = '<div class="brand"><div class="tile"><span>ر</span><em></em></div><b>رَفِيق</b></div>'

def phone(img, top, w):
    return f'<div class="phone" style="top:{top}px;width:{w + 28}px;margin-left:-{(w + 28) // 2}px"><img src="file://{SCREENS}/{img}.png" style="width:{w}px"></div>'

def ar(t): return f'<bdi class="ar" lang="ar">{e(t)}</bdi>'

def carousels():
    swipe = '<div class="foot">Swipe →</div>'
    end = lambda h: (f'<div class="kicker">RAFIQ</div><div class="h" style="top:330px">{h}</div>'
                     f'<div class="cta" style="top:660px">rafiq-arabic.com</div><div class="note" style="top:830px">Free for a week · no card needed</div>')
    C = {}
    C["c1-sadiq"] = [
        f'<div class="kicker">WORD OF THE DAY</div><div class="h">Do you know this one?</div><div class="word" style="top:470px">صَدِيق</div>{swipe}',
        f'<div class="kicker">WORD OF THE DAY</div><div class="word" style="top:300px">صَدِيق</div><div class="tr" style="top:700px">ṣadīq</div>'
        f'<div class="en" style="top:790px">a friend</div><div class="note" style="top:920px">for a man or a boy</div>',
        f'<div class="kicker">WORD OF THE DAY</div><div class="word" style="top:300px">صَدِيقَ<em>ة</em></div><div class="tr" style="top:700px">ṣadīqa</div>'
        f'<div class="en" style="top:790px">a friend</div><div class="note" style="top:920px">for a woman or a girl: add {ar("ة")} at the end</div>',
        f'<div class="kicker">USE IT</div><div class="h">Say it when you say goodbye:</div>'
        f'<div class="card" style="top:470px"><div class="ar" lang="ar">مَعَ السَّلامَةِ يا صَدِيقِي.</div><div class="en2">Goodbye, my friend.</div></div>'
        f'<div class="note" style="top:960px">{ar("صَدِيقِي")} is “my friend”: the {ar("ي")} on the end means “my”.</div>',
        end("Learn a word a day <b>with audio and review</b>")]
    C["c2-rihla"] = [
        f'<div class="kicker">WORD OF THE DAY</div><div class="h">Going somewhere? ✈️</div><div class="word" style="top:470px">رِحْلَة</div>{swipe}',
        f'<div class="kicker">WORD OF THE DAY</div><div class="word" style="top:300px">رِحْلَة</div><div class="tr" style="top:700px">riḥla</div>'
        f'<div class="en" style="top:790px">a journey, a trip</div>',
        f'<div class="kicker">USE IT</div><div class="h">Say it to someone who’s travelling:</div>'
        f'<div class="card" style="top:470px"><div class="ar" lang="ar">رِحْلَة سَعِيدَة</div><div class="en2">Have a good trip</div></div>'
        f'<div class="note" style="top:850px">riḥla saʿīda</div>',
        end("A new word every day, <b>with audio</b>")]
    C["c3-salah"] = [
        f'<div class="kicker">YOUR SALAH</div><div class="h">Do you know what you’re <b>saying</b> in your prayer?</div>{phone("salah", 400, 400)}',
        f'<div class="kicker">WORD BY WORD</div><div class="h">Every word, its meaning, and <b>how often you say it</b></div>{phone("salah-l1", 400, 400)}',
        f'<div class="kicker">START WITH THE MOST-SAID</div><div class="h" style="top:280px">The 20 words you say most are about</div>'
        f'<div class="word" style="top:420px;font-family:\'Karla\';color:#2e7263">56%</div>'
        f'<div class="en" style="top:760px">of everything you say in a four-rakʿah prayer</div>'
        f'<div class="note" style="top:950px">So Rafiq starts there, five words at a time.</div>',
        end("Understand <b>every word</b> of your salah")]
    C["c4-inside"] = [
        f'<div class="kicker">WHAT’S INSIDE · SWIPE →</div><div class="h">Learning Arabic? Here’s <b>what’s inside Rafiq</b></div>'
        f'<div class="note" style="top:350px">1 · Short lessons, every word with audio</div>{phone("lesson", 440, 380)}',
        f'<div class="kicker">2 · VERB FORMS</div><div class="h">21 verbs, <b>every form</b>, from I to we</div>{phone("verbs-table", 400, 400)}',
        f'<div class="kicker">3 · PRACTISE</div><div class="h">Weak-spots review, spelling bee, <b>real-life scenes</b></div>{phone("practise-2", 400, 400)}',
        f'<div class="kicker">4 · REVIEW</div><div class="h">Your words come back <b>just before you’d forget them</b></div>{phone("vocab", 400, 400)}',
        end("Try it all <b>free for a week</b>")]
    ens = ["I study", "you study (to a man)", "you study (to a woman)", "he studies", "she studies", "we study"]
    C["c5-study"] = ([f'<div class="kicker">ARABIC VERBS · I TO WE</div><div class="h">How “to study” changes, <b>person by person</b></div>'
                      f'<div class="word" style="top:470px">دَرَسَ</div><div class="tr" style="top:870px">darasa</div>{swipe}']
                     + [f'<div class="kicker">{i + 1} OF 6</div><div class="pron" style="top:250px">{e(PRON[i][0])}</div>'
                        f'<div class="form" style="top:400px">{paint(STUDY[i])}</div><div class="en" style="top:820px">{ens[i]}</div>'
                        + ('<div class="note" style="top:950px">Same word as “you study (to a man)”. You tell them apart from the sentence.</div>' if i == 4 else "")
                        + ('<div class="note" style="top:950px">The front letter tells you who: <span class="ar">أَ</span> I, <span class="ar">نَ</span> we.</div>' if i == 5 else "")
                        for i in range(6)]
                     + [f'<div class="kicker">ALL SIX</div><div class="tbl" style="top:230px">'
                        + "".join(f'<div><span>{ens[i].split(" (")[0]}{" (m)" if i == 1 else " (f)" if i == 2 else ""}</span><span class="ar" lang="ar">{paint(STUDY[i])}</span></div>' for i in range(6))
                        + '</div><div class="note" style="top:1000px">Learn the pattern once, and it works for every verb like it.</div>',
                        end("21 verbs, <b>every form</b>, with audio")])
    return C

def render_carousels(ids):
    from playwright.sync_api import sync_playwright
    C = {k: v for k, v in carousels().items() if not ids or k in ids}
    if not C: return
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME); p = b.new_page(viewport={"width": 1080, "height": 1350})
        for cid, slides in C.items():
            out = os.path.join(SOC, cid); os.makedirs(out, exist_ok=True)
            for f in os.listdir(out):
                if f.startswith("slide-"): os.remove(os.path.join(out, f))
            for i, s in enumerate(slides):
                page = os.path.join(out, "_slide.html")      # a real file, so the local fonts and screens load
                open(page, "w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CCSS}</style></head><body>{BRAND}{s}</body></html>')
                p.goto("file://" + page); p.evaluate("document.fonts.ready.then(() => 0)"); p.wait_for_timeout(300)
                bad = p.evaluate("[...document.images].filter(i => !i.naturalWidth).length + [...document.fonts].filter(f => f.status === 'error').length")
                if bad: print(f"  ! {cid} slide {i + 1}: {bad} image(s) or font(s) didn't load")
                over = p.evaluate("""[...document.body.querySelectorAll('*')].filter(el => { const r = el.getBoundingClientRect();
                    return r.width && (r.right > 1081 || r.left < -1 || r.bottom > 1351); }).map(el => el.className || el.tagName)""")
                if over: print(f"  ! {cid} slide {i + 1} runs off the edge: {over[:4]}")
                p.screenshot(path=os.path.join(out, f"slide-{i + 1:02d}.png")); os.remove(page)
            print(f"{cid}: {len(slides)} slides")
        b.close()

if __name__ == "__main__":
    ids = [a for a in sys.argv[1:] if not a.startswith("--")]
    check_forms()
    if "--level" in sys.argv:
        T.LUFS.update({v: -16.0 for v in VIDEOS})
        for vid in VIDEOS:
            if not ids or vid in ids: T.level(vid)
        sys.exit()
    for vid, fn in VIDEOS.items():
        if not ids or vid in ids: fn()
    cids = [i for i in ids if i.startswith("c")]
    if cids or not ids: render_carousels(cids)
