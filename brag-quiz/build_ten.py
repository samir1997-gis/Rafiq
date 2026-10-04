#!/usr/bin/env python3
"""Ten TikToks / Reels (#219): five quizzes and five that teach one thing. The only sound is the app's own reading voice:
no fountain, no taps or chimes, no music.

  q1-guess-food     Guess the meaning: three food words, three meanings each, 3-2-1, the answer.
  q2-loanwords      "You already speak Arabic": سُكَّر قَهْوَة زَرافة صِفْر, guess the English word each became.
  q3-listen         Sound on: hear an animal's name, pick the picture.
  q4-salah-where    Where in the prayer do you say this? Rising, rukūʿ, sujūd (one word changes between the last two).
  q5-numbers        One to five, then two "what number is this?" rounds.
  i1-salam-reply    How to answer السَّلامُ عَلَيْكُم, and the vowel that changes "how are you" for a man or a woman.
  i2-sun-letters    Why it's as-salām, not al-salām: the sun letters, then "sun or moon?".
  i3-days           Arabic days of the week are numbers: Sunday "one" … Thursday "five", Friday the gathering.
  i4-ta-marbuta     One letter turns him into her: ة (جَدّ → جَدَّة, ابْن → ابْنَة, والِد → والِدَة), and أَخ → أُخْت.
  i5-salah-words    Three things you say in every prayer, word by word.

Same look and helpers as build_teach.py (and through it build_quiz.py). Every Arabic word and its meaning is the app's own
(vocab-data.js, salah-data.js) and is said with the app's recording; the notes in TEN.md list what isn't from the data.

  python3 brag-quiz/build_ten.py [id ...]            writes brag-quiz/out/<id>/composition
  then in each:  npx hyperframes render -o ../<id>.mp4
  python3 brag-quiz/build_ten.py --level [id ...]    levels each rendered video to -16 LUFS
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build_teach as T
from build_teach import Comp, e, mixed, GREEN, RED, INK
PAPER = "#f1ece0"

CSS = """
@font-face { font-family:"Noto Color Emoji"; src: local("Noto Color Emoji"); }   /* the picture answers (q3) and ☀️ 🌙 (i2) */
.ops { position:absolute; left:90px; right:90px; display:flex; flex-direction:column; gap:24px; }
.op { height:150px; border-radius:36px; background:var(--card); border:4px solid rgba(23,38,43,.13); display:flex; align-items:center;
  justify-content:center; box-shadow:0 12px 26px -16px rgba(23,38,43,.35); }
.op b { font-size:62px; font-weight:700; letter-spacing:-.01em; color:var(--ink); }
.op b .ar { font-family:var(--ar); }
.grid4 { position:absolute; left:90px; right:90px; display:grid; grid-template-columns:1fr 1fr; gap:24px; }
.grid4 .op { height:280px; flex-direction:column; gap:6px; }
.grid4 .op i { font-style:normal; font-size:130px; line-height:1.1; font-family:"Noto Color Emoji",sans-serif; }
.grid4 .op b { font-size:46px; }
.cnt { position:absolute; left:50%; width:150px; height:150px; margin-left:-75px; }
.cnt svg { position:absolute; inset:0; transform:rotate(-90deg); }
.cnt circle { fill:none; stroke-width:12; }
.cnt .bg { stroke:rgba(23,38,43,.12); }
.cnt .fg { stroke:var(--rubric); stroke-linecap:round; stroke-dasharray:408; stroke-dashoffset:0; }
.cnt span { position:absolute; inset:0; display:grid; place-items:center; font-size:74px; font-weight:700; opacity:0; }
.sub { position:absolute; left:80px; right:80px; text-align:center; font-size:48px; font-weight:700; color:var(--ink-soft); line-height:1.25; }
.sub .ar { font-family:var(--ar); color:var(--rubric); }
.wave { position:absolute; left:0; right:0; height:260px; display:flex; justify-content:center; align-items:center; gap:22px; }
.wave i { display:block; width:30px; height:220px; border-radius:15px; background:var(--verdigris); transform:scaleY(.25); }
.pill { position:absolute; left:50%; transform:translateX(-50%); white-space:nowrap; font-size:46px; font-weight:700; color:var(--paper);
  background:var(--ink); border-radius:999px; padding:16px 44px; }
.drows { position:absolute; left:70px; right:70px; display:flex; flex-direction:column; gap:20px; }
.drow { display:flex; align-items:center; justify-content:space-between; gap:20px; height:150px; padding:0 40px; background:var(--card);
  border:4px solid rgba(23,38,43,.13); border-radius:32px; box-shadow:0 12px 26px -16px rgba(23,38,43,.35); }
.drow .ar { font-family:var(--ar); font-weight:700; font-size:78px; line-height:1.45; }
.drow .en b { display:block; font-size:50px; font-weight:700; }
.drow .en span { display:block; font-size:36px; color:var(--ink-soft); font-weight:700; }
.drow .en span .ar { font-size:40px; color:var(--rubric); }
.pairs { position:absolute; left:70px; right:70px; display:flex; flex-direction:column; gap:26px; }
.pair { display:grid; grid-template-columns:1fr 90px 1fr; align-items:center; height:210px; background:var(--card); border:4px solid rgba(23,38,43,.13);
  border-radius:36px; box-shadow:0 12px 26px -16px rgba(23,38,43,.35); text-align:center; }
.pair .ar { font-family:var(--ar); font-weight:700; font-size:92px; line-height:1.4; }
.pair .en { font-size:38px; font-weight:700; color:var(--ink-soft); margin-top:-10px; }
.pair .to { font-size:60px; font-weight:700; color:var(--ink-soft); }
.pair .ar em, .big em { font-style:normal; color:var(--rubric); }
.tr2 { position:absolute; left:80px; right:80px; text-align:center; font-family:var(--ut); font-size:50px; color:var(--verdigris); }
.tr2 s { color:var(--rubric); }
.letters { position:absolute; left:110px; right:110px; display:flex; flex-wrap:wrap; flex-direction:row-reverse; justify-content:center; gap:18px; }
.letters span { width:118px; height:118px; display:grid; place-items:center; font-family:var(--ar); font-weight:700; font-size:70px; color:var(--rubric);
  background:var(--card); border:4px solid rgba(23,38,43,.13); border-radius:26px; }
.sm { position:absolute; left:110px; right:110px; display:flex; gap:30px; }
.sm .op { flex:1; height:140px; }
.sm .op b { font-size:52px; }
.ques { position:absolute; left:80px; right:80px; text-align:center; font-size:84px; font-weight:700; line-height:1.15; letter-spacing:-.02em; }
.ques b { color:var(--verdigris); }
.digits { position:absolute; left:60px; right:60px; display:flex; justify-content:center; gap:18px; }
.digits div { flex:1; display:flex; flex-direction:column; align-items:center; background:var(--card); border:4px solid rgba(23,38,43,.13);
  border-radius:30px; padding:10px 0 18px; box-shadow:0 12px 26px -16px rgba(23,38,43,.35); }
.digits b { font-size:100px; font-weight:700; color:var(--verdigris); line-height:1.1; }
.digits i { font-style:normal; font-family:var(--ar); font-size:72px; font-weight:700; color:var(--rubric); line-height:1.3; }
.digits span { font-family:var(--ar); font-size:44px; font-weight:700; line-height:1.5; }
"""

def comp(vid, kicker):
    c = Comp(vid, kicker, bed=False); c.css = CSS
    return c

def cnt(cid, top):
    return (f'<div class="cnt" id="{cid}" style="top:{top}px"><svg viewBox="0 0 150 150"><circle class="bg" cx="75" cy="75" r="65"/>'
            f'<circle class="fg" cx="75" cy="75" r="65"/></svg>{"".join(f"<span>{k}</span>" for k in (3, 2, 1))}</div>')

def countdown(c, cid, at, n=3):
    """the ring empties over n seconds while n … 1 count down; returns when it's done"""
    c.t(f'tl.fromTo("#{cid}", {{opacity:0, scale:0.7}}, {{opacity:1, scale:1, duration:0.3, ease:"power3.out"}}, {at - 0.3:.2f});')
    c.t(f'tl.fromTo("#{cid} .fg", {{strokeDashoffset:0}}, {{strokeDashoffset:408, duration:{n}, ease:"none"}}, {at:.2f});')
    for k in range(n):
        sel = f"#{cid} span:nth-of-type({k + 1 + (3 - n)})"
        c.t(f'tl.fromTo("{sel}", {{opacity:0, scale:1.35}}, {{opacity:1, scale:1, duration:0.22, ease:"power3.out"}}, {at + k:.2f});')
        c.t(f'tl.to("{sel}", {{opacity:0, duration:0.15}}, {at + k + 0.82:.2f});')
    c.t(f'tl.to("#{cid}", {{opacity:0, scale:0.7, duration:0.25}}, {at + n - 0.1:.2f});')
    return at + n + 0.05

def reveal(c, right, wrong, at):
    """the right answer turns green, the others step back"""
    c.t(f'tl.to("{right}", {{backgroundColor:"{GREEN}", borderColor:"{GREEN}", duration:0.3}}, {at:.2f});')
    c.t(f'tl.to("{right} b", {{color:"{PAPER}", duration:0.3}}, {at:.2f});')
    c.t(f'tl.fromTo("{right}", {{scale:1}}, {{scale:1.04, duration:0.16, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {at + 0.1:.2f});')
    if wrong: c.t(f'tl.to([{", ".join(f"{chr(34)}{w}{chr(34)}" for w in wrong)}], {{opacity:0.3, duration:0.3}}, {at:.2f});')

def stagger(c, sels, at, gap=0.12, y=26):
    for i, s in enumerate(sels): c.inn(s, at + i * gap, y)
    return at + len(sels) * gap

def ops(sid, items, top):
    return f'<div class="ops" style="top:{top}px">' + "".join(f'<div class="op" id="{sid}o{i}"><b>{mixed(x)}</b></div>' for i, x in enumerate(items)) + '</div>'

# ---------------------------------------------------------------- q1: guess the meaning
def q1():
    c = comp("q1-guess-food", "QUIZ · GUESS THE MEANING")
    R = [("خُبْز", ["milk", "bread", "tea"], 1), ("تَمْر", ["dates", "fish", "water"], 0), ("حَلِيب", ["tea", "water", "milk"], 2)]
    body, t = [], 0.1
    body.append('<div class="ques" id="intro" style="top:700px">Three Arabic words.</div><div class="ques" id="intro2" style="top:810px"><b>Can you get 3 out of 3?</b></div>')
    c.inn("#intro", t); c.inn("#intro2", t + 0.4); c.out_("#intro, #intro2", t + 2.2); t += 2.6
    for k, (ar, opts, right) in enumerate(R):
        s = f"r{k}"
        c.inn(f"#{s} .q2", t); c.t(f'tl.fromTo("#{s} .big", {{opacity:0, scale:0.94}}, {{opacity:1, scale:1, duration:0.45, ease:"power3.out"}}, {t + 0.25:.2f});')
        d = c.say(ar, t + 0.55)
        stagger(c, [f"#{s}o{i}" for i in range(3)], t + 0.9)
        done = countdown(c, f"{s}c", max(t + 0.55 + d, t + 1.4) + 0.4)
        reveal(c, f"#{s}o{right}", [f"#{s}o{i}" for i in range(3) if i != right], done)
        c.say(ar, done + 0.3)
        c.out_(f"#{s}", done + 0.3 + d + 0.7)
        body.append(f'<div class="sec" id="{s}"><div class="q2">{k + 1}/3 · What does it mean?</div>'
                    f'<div class="big" style="top:400px" lang="ar">{e(ar)}</div>{cnt(s + "c", 760)}{ops(s, opts, 960)}</div>')
        t = done + 0.3 + d + 1.1
    body.append('<div class="ques" id="score" style="top:720px">How many did you get?</div><div class="ques" id="score2" style="top:830px"><b>Tell me in the comments</b></div>')
    c.inn("#score", t); c.inn("#score2", t + 0.3); c.out_("#score, #score2", t + 2.0)
    E = t + 2.4
    body.append(c.end(E, "Learn the words you'll use every day"))
    c.write("\n".join("      " + b for b in body), round(E + 2.9, 2))

# ---------------------------------------------------------------- q2: words English took from Arabic
def q2():
    c = comp("q2-loanwords", "QUIZ · YOU ALREADY SPEAK ARABIC")
    R = [("سُكَّر", "sukkar", "sugar", "via Latin and French"), ("قَهْوَة", "qahwa", "coffee", "via Turkish"),
         ("زَرافة", "zarāfa", "giraffe", "via Italian"), ("صِفْر", "ṣifr", "zero", "via Italian")]
    body, t = [], 0.1
    body.append('<div class="ques" id="intro" style="top:640px">These four English words</div>'
                '<div class="ques" id="intro2" style="top:860px"><b>came from Arabic.</b></div>'
                '<div class="sub" id="intro3" style="top:1010px">Guess each one before the timer ends.</div>')
    c.inn("#intro", t); c.inn("#intro2", t + 0.4); c.inn("#intro3", t + 1.0); c.out_("#intro, #intro2, #intro3", t + 2.6); t += 3.0
    for k, (ar, tr, en, via) in enumerate(R):
        s = f"r{k}"
        c.inn(f"#{s} .q2", t); c.t(f'tl.fromTo("#{s} .big", {{opacity:0, scale:0.94}}, {{opacity:1, scale:1, duration:0.45, ease:"power3.out"}}, {t + 0.2:.2f});')
        d = c.say(ar, t + 0.45); c.inn(f"#{s} .tr2", t + 0.6)
        done = countdown(c, f"{s}c", max(t + 0.45 + d, t + 1.2) + 0.3)
        c.t(f'tl.fromTo("#{s} .ans", {{opacity:0, scale:0.9}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(1.6)"}}, {done:.2f});')
        c.inn(f"#{s} .sub", done + 0.4)
        c.out_(f"#{s}", done + 1.9)
        body.append(f'<div class="sec" id="{s}"><div class="q2">{k + 1}/4 · Which English word?</div>'
                    f'<div class="big" style="top:420px" lang="ar">{e(ar)}</div><div class="tr2" style="top:770px">{e(tr)}</div>'
                    f'{cnt(s + "c", 920)}<div class="ans" style="top:930px">{e(en)}</div>'
                    f'<div class="sub" style="top:1090px">{e(en)} came into English from Arabic, {e(via)}</div></div>')
        t = done + 2.3
    body.append('<div class="ques" id="score" style="top:720px">How many did you get</div>'
                '<div class="ques" id="score2" style="top:830px"><b>before the timer?</b></div>')
    c.inn("#score", t); c.inn("#score2", t + 0.3); c.out_("#score, #score2", t + 2.0)
    E = t + 2.4
    body.append(c.end(E, "You know more Arabic than you think"))
    c.write("\n".join("      " + b for b in body), round(E + 2.9, 2))

# ---------------------------------------------------------------- q3: listen and pick the animal
def q3():
    c = comp("q3-listen", "QUIZ · SOUND ON")
    ANIMALS = {"cat": ("هِرّة", "🐱"), "dog": ("كَلْب", "🐶"), "horse": ("حِصان", "🐴"), "lion": ("أَسَد", "🦁"), "bird": ("طائِر", "🐦"), "fish": ("سَمَك", "🐟")}
    R = [("horse", ["cat", "horse", "lion", "dog"]), ("lion", ["bird", "dog", "lion", "fish"]), ("cat", ["cat", "fish", "horse", "bird"])]
    body, t = [], 0.1
    body.append('<div class="ques" id="intro" style="top:640px">🔊 Turn your sound on.</div>'
                '<div class="sub" id="intro2" style="top:790px">You’ll hear an animal in Arabic. Pick it before the timer ends.</div>')
    body[-1] = body[-1].replace('🔊 ', '<span style="font-family:\'Noto Color Emoji\'">🔊</span> ')
    c.inn("#intro", t); c.inn("#intro2", t + 0.5); c.out_("#intro, #intro2", t + 2.8); t += 3.2
    for k, (ans, opts) in enumerate(R):
        s, ar = f"r{k}", ANIMALS[ans][0]
        right = opts.index(ans)
        c.inn(f"#{s} .q2", t); c.inn(f"#{s} .wave", t + 0.2, 0)
        d = c.say(ar, t + 0.6); d2 = c.say(ar, t + 0.6 + d + 0.6)
        for j, a0 in enumerate((t + 0.6, t + 1.2 + d)):     # the bars move while the word is said
            for b in range(5):
                c.t(f'tl.fromTo("#{s} .wave i:nth-child({b + 1})", {{scaleY:0.25}}, {{scaleY:{[0.6, 0.9, 1, 0.8, 0.55][b]}, duration:{0.14 + b * 0.03:.2f}, yoyo:true, '
                    f'repeat:{max(1, int(d / (0.14 + b * 0.03)) // 2 * 2 - 1)}, ease:"sine.inOut", immediateRender:false}}, {a0:.2f});')
        stagger(c, [f"#{s}o{i}" for i in range(4)], t + 0.9, 0.1)
        done = countdown(c, f"{s}c", t + 1.2 + d + d2 + 0.3)
        reveal(c, f"#{s}o{right}", [f"#{s}o{i}" for i in range(4) if i != right], done)
        c.t(f'tl.to("#{s} .wave", {{opacity:0, duration:0.25}}, {done:.2f});')
        c.t(f'tl.fromTo("#{s} .pill", {{opacity:0, y:16}}, {{opacity:1, y:0, duration:0.35, ease:"power3.out"}}, {done + 0.15:.2f});')
        c.say(ar, done + 0.4)
        c.out_(f"#{s}", done + 0.4 + d + 0.8)
        cards = "".join(f'<div class="op" id="{s}o{i}"><i>{ANIMALS[o][1]}</i><b>{o}</b></div>' for i, o in enumerate(opts))
        body.append(f'<div class="sec" id="{s}"><div class="q2">{k + 1}/3 · Which animal did you hear?</div>'
                    f'<div class="wave" style="top:420px">{"<i></i>" * 5}</div>'
                    f'<div class="pill" style="top:500px"><bdi class="ar" lang="ar" style="font-family:var(--ar)">{e(ar)}</bdi> = {ans}</div>'
                    f'{cnt(s + "c", 700)}<div class="grid4" style="top:880px">{cards}</div></div>')
        t = done + 0.4 + d + 1.2
    body.append('<div class="ques" id="score" style="top:720px">3 out of 3?</div><div class="ques" id="score2" style="top:830px"><b>Your ears are learning.</b></div>')
    c.inn("#score", t); c.inn("#score2", t + 0.3); c.out_("#score, #score2", t + 2.0)
    E = t + 2.4
    body.append(c.end(E, "Hear every word, said by a real voice"))
    c.write("\n".join("      " + b for b in body), round(E + 2.9, 2))

# ---------------------------------------------------------------- q4: where in the prayer
def q4():
    c = comp("q4-salah-where", "QUIZ · YOUR SALAH")
    PLACES = ["Bowing (rukūʿ)", "Rising from bowing", "Prostration (sujūd)"]
    R = [("سَمِعَ اللَّهُ لِمَنْ حَمِدَهُ", 1, "Allah hears the one who praises Him."),
         ("سُبْحانَ رَبِّيَ الْعَظِيمِ", 0, "Glory be to my Lord, the Magnificent."),
         ("سُبْحانَ رَبِّيَ الْأَعْلى", 2, "Glory be to my Lord, the Most High.")]
    body, t = [], 0.1
    body.append('<div class="ques" id="intro" style="top:660px">You say these in every prayer.</div>'
                '<div class="ques" id="intro2" style="top:860px"><b>Do you know when?</b></div>')
    c.inn("#intro", t); c.inn("#intro2", t + 0.5); c.out_("#intro, #intro2", t + 2.4); t += 2.8
    for k, (ar, right, en) in enumerate(R):
        s = f"r{k}"
        c.inn(f"#{s} .q2", t)
        c.t(f'tl.fromTo("#{s} .big", {{opacity:0, scale:0.96}}, {{opacity:1, scale:1, duration:0.45, ease:"power3.out"}}, {t + 0.25:.2f});')
        d = c.say(ar, t + 0.55)
        if k == 2: c.inn(f"#{s} .hint", t + 0.55 + d)
        stagger(c, [f"#{s}o{i}" for i in range(3)], t + 0.9)
        done = countdown(c, f"{s}c", max(t + 0.55 + d, t + 1.4) + (0.9 if k == 2 else 0.4))
        reveal(c, f"#{s}o{right}", [f"#{s}o{i}" for i in range(3) if i != right], done)
        c.inn(f"#{s} .tr", done + 0.3)
        c.out_(f"#{s}", done + 2.6)
        hint = '<div class="hint" style="top:640px;font-size:44px">Careful: one word changed.</div>' if k == 2 else ""
        body.append(f'<div class="sec" id="{s}"><div class="q2">{k + 1}/3 · When do you say this?</div>'
                    f'<div class="big" style="top:400px;font-size:92px" lang="ar">{e(ar)}</div>{hint}'
                    f'{cnt(s + "c", 740)}{ops(s, PLACES, 940)}<div class="tr" style="top:1480px">“{e(en)}”</div></div>')
        t = done + 3.0
    E = t
    body.append(c.end(E, "Understand every word of your salah"))
    c.write("\n".join("      " + b for b in body), round(E + 2.9, 2))

# ---------------------------------------------------------------- q5: one to five, then two rounds
def q5():
    c = comp("q5-numbers", "ARABIC · ONE TO FIVE")
    N = [("1", "١", "واحِد"), ("2", "٢", "اثْنانِ"), ("3", "٣", "ثَلاثَة"), ("4", "٤", "أَرْبَعَة"), ("5", "٥", "خَمْسَة")]
    body, t = [], 0.1
    c.inn("#a .q2", t); t += 0.6
    for i, (_, _, ar) in enumerate(N):
        c.inn(f"#d{i}", t, 30); d = c.say(ar, t + 0.15); t += max(d, 0.9) + 0.35
    c.inn("#a .sub", t); c.out_("#a", t + 2.2); t += 2.6
    body.append('<div class="sec" id="a"><div class="q2">Count to five in Arabic</div><div class="digits" style="top:560px">'
                + "".join(f'<div id="d{i}"><b>{n}</b><i lang="ar">{a}</i><span lang="ar">{e(w)}</span></div>' for i, (n, a, w) in enumerate(N))
                + '</div><div class="sub" style="top:1000px">In red: the digits you’ll see in a lot of Arabic writing, <bdi class="ar" lang="ar" dir="ltr">١ ٢ ٣ ٤ ٥</bdi></div></div>')
    for k, (ar, opts, right) in enumerate([("أَرْبَعَة", ["2", "4", "5"], 1), ("ثَلاثَة", ["3", "1", "5"], 0)]):
        s = f"r{k}"
        c.inn(f"#{s} .q2", t); c.t(f'tl.fromTo("#{s} .big", {{opacity:0, scale:0.94}}, {{opacity:1, scale:1, duration:0.45, ease:"power3.out"}}, {t + 0.25:.2f});')
        d = c.say(ar, t + 0.55)
        stagger(c, [f"#{s}o{i}" for i in range(3)], t + 0.9)
        done = countdown(c, f"{s}c", max(t + 0.55 + d, t + 1.4) + 0.4)
        reveal(c, f"#{s}o{right}", [f"#{s}o{i}" for i in range(3) if i != right], done)
        c.say(ar, done + 0.3)
        c.out_(f"#{s}", done + 0.3 + d + 0.7)
        body.append(f'<div class="sec" id="{s}"><div class="q2">{k + 1}/2 · Which number is it?</div>'
                    f'<div class="big" style="top:400px" lang="ar">{e(ar)}</div>{cnt(s + "c", 760)}{ops(s, opts, 960)}</div>')
        t = done + 0.3 + d + 1.1
    E = t
    body.append(c.end(E, "Numbers, times and dates, one step at a time"))
    c.write("\n".join("      " + b for b in body), round(E + 2.9, 2))

# ---------------------------------------------------------------- i1: answering the salam
def i1():
    c = comp("i1-salam-reply", "ARABIC · GREETINGS")
    body, t = [], 0.1
    body.append('<div class="sec" id="a"><div class="q2" id="a0">Someone says this to you:</div>'
                '<div class="big" id="a1" style="top:400px;font-size:110px" lang="ar">السَّلامُ عَلَيْكُم</div>'
                '<div class="sub" id="a1s" style="top:640px">peace be upon you</div>'
                '<div class="q2" id="a2" style="top:860px">What do you say back?</div>'
                '<div class="big" id="a3" style="top:1000px;font-size:110px;color:var(--verdigris)" lang="ar">وَعَلَيْكُمُ السَّلام</div>'
                '<div class="sub" id="a4" style="top:1240px">and peace be upon you</div></div>')
    c.inn("#a0", t); c.t(f'tl.fromTo("#a1", {{opacity:0, scale:0.96}}, {{opacity:1, scale:1, duration:0.45, ease:"power3.out"}}, {t + 0.3:.2f});')
    d = c.say("السَّلامُ عَلَيْكُم", t + 0.6); c.inn("#a1s", t + 0.6 + d)
    t = t + 0.6 + d + 0.6
    c.inn("#a2", t); t += 1.6
    c.t(f'tl.fromTo("#a3", {{opacity:0, scale:0.96}}, {{opacity:1, scale:1, duration:0.45, ease:"power3.out"}}, {t:.2f});')
    d = c.say("وَعَلَيْكُمُ السَّلام", t + 0.3); c.inn("#a4", t + 0.3 + d)
    t = t + 0.3 + d + 1.6
    c.out_("#a", t); t += 0.4
    # how are you: one vowel for a man, another for a woman
    body.append('<div class="sec" id="b"><div class="q2" id="b0">Then: how are you?</div>'
                '<div class="pairs" style="top:440px">'
                '<div class="pair" id="h0" style="grid-template-columns:1fr 1fr"><div><div class="ar" lang="ar">كَيْفَ حالُ<em>كَ</em></div></div><div class="en"><div>to a man</div><div>kayfa ḥālu<b style="color:var(--rubric)">ka</b></div></div></div>'
                '<div class="pair" id="h1" style="grid-template-columns:1fr 1fr"><div><div class="ar" lang="ar">كَيْفَ حالُ<em>كِ</em></div></div><div class="en"><div>to a woman</div><div>kayfa ḥālu<b style="color:var(--rubric)">ki</b></div></div></div>'
                '</div><div class="sub" id="b1" style="top:960px">Only the last vowel changes.</div>'
                '<div class="q2" id="b2" style="top:1120px">The answer:</div>'
                '<div class="big" id="b3" style="top:1220px;font-size:110px;color:var(--verdigris)" lang="ar">الحَمْدُ لِلَّهِ</div>'
                '<div class="sub" id="b4" style="top:1450px">praise be to God</div></div>')
    c.inn("#b0", t)
    c.inn("#h0", t + 0.4, 30); d = c.say("كَيْفَ حالُكَ", t + 0.6); t = t + 0.6 + d + 0.4
    c.inn("#h1", t, 30); d = c.say("كَيْفَ حالُكِ", t + 0.2); t = t + 0.2 + d + 0.3
    c.inn("#b1", t); t += 1.8
    c.inn("#b2", t); c.t(f'tl.fromTo("#b3", {{opacity:0, scale:0.96}}, {{opacity:1, scale:1, duration:0.45, ease:"power3.out"}}, {t + 0.3:.2f});')
    d = c.say("الحَمْدُ لِلَّهِ", t + 0.6); c.inn("#b4", t + 0.6 + d)
    t = t + 0.6 + d + 1.8
    c.out_("#b", t)
    E = t + 0.4
    body.append(c.end(E, "Say it right from day one"))
    c.write("\n".join("      " + b for b in body), round(E + 2.9, 2))

# ---------------------------------------------------------------- i2: the sun letters
def i2():
    c = comp("i2-sun-letters", "ARABIC · READING")
    SUN = "ت ث د ذ ر ز س ش ص ض ط ظ ل ن".split()
    body, t = [], 0.1
    body.append('<div class="sec" id="a"><div class="q2">Why is it <i style="font-style:normal;color:var(--verdigris);white-space:nowrap">ash-shams</i>, not <s style="color:var(--rubric);white-space:nowrap">al-shams</s>?</div>'
                '<div class="big" style="top:470px" lang="ar">الشَّمْس</div><div class="sub" id="a1" style="top:820px">the sun</div>'
                '<div class="tr2" style="top:920px">a<s>l</s>-shams → ash-shams</div>'
                '<div class="sub" id="a2" style="top:1040px">The <bdi class="ar" lang="ar">ل</bdi> of <bdi class="ar" lang="ar">ال</bdi> (“the”) isn’t said. The next letter is doubled instead.</div></div>')
    c.inn("#a .q2", t); c.t(f'tl.fromTo("#a .big", {{opacity:0, scale:0.94}}, {{opacity:1, scale:1, duration:0.45, ease:"power3.out"}}, {t + 0.4:.2f});')
    d = c.say("الشَّمْس", t + 0.8); c.inn("#a1", t + 0.8 + d)
    c.inn("#a .tr2", t + 1.4 + d); c.inn("#a2", t + 2.4 + d)
    t = t + 2.4 + d + 3.0
    c.out_("#a", t); t += 0.4
    body.append('<div class="sec" id="b"><div class="q2">It happens before 14 letters, the “sun letters”:</div>'
                f'<div class="letters" style="top:500px">{"".join(f"<span id=l{i}>{x}</span>" for i, x in enumerate(SUN))}</div>'
                '<div class="sub" style="top:1000px">Before the other 14, the “moon letters”, you say the <bdi class="ar" lang="ar">ل</bdi>:</div>'
                '<div class="tr2" id="b2" style="top:1200px"><bdi lang="ar" style="font-family:var(--ar);color:var(--ink)">الخَمِيس</bdi> al-khamīs, Thursday</div></div>')
    c.inn("#b .q2", t)
    for i in range(len(SUN)): c.inn(f"#l{i}", t + 0.5 + i * 0.07, 16, 0.3)
    t += 0.5 + len(SUN) * 0.07 + 1.6
    c.inn("#b .sub", t); c.inn("#b2", t + 1.2); d = c.say("الخَمِيس", t + 1.4)
    t = t + 1.4 + d + 1.6
    c.out_("#b", t); t += 0.4
    # sun or moon? two quick ones
    for k, (ar, tr, sun) in enumerate([("السَّبْت", "as-sabt, Saturday", True), ("الجُمُعَة", "al-jumuʿa, Friday", False)]):
        s = f"r{k}"
        c.inn(f"#{s} .q2", t); c.t(f'tl.fromTo("#{s} .big", {{opacity:0, scale:0.94}}, {{opacity:1, scale:1, duration:0.45, ease:"power3.out"}}, {t + 0.25:.2f});')
        c.inn(f"#{s}o0", t + 0.6); c.inn(f"#{s}o1", t + 0.7)
        done = countdown(c, f"{s}c", t + 1.2)
        right = 0 if sun else 1
        reveal(c, f"#{s}o{right}", [f"#{s}o{1 - right}"], done)
        d = c.say(ar, done + 0.2); c.inn(f"#{s} .tr2", done + 0.2)
        c.out_(f"#{s}", done + 0.2 + d + 1.2)
        body.append(f'<div class="sec" id="{s}"><div class="q2">{k + 1}/2 · Sun or moon? Is the <bdi class="ar" lang="ar">ل</bdi> said?</div>'
                    f'<div class="big" style="top:420px" lang="ar">{e(ar)}</div>{cnt(s + "c", 790)}'
                    f'<div class="sm" style="top:1000px"><div class="op" id="{s}o0"><b>☀️ sun: no L</b></div><div class="op" id="{s}o1"><b>🌙 moon: L said</b></div></div>'
                    f'<div class="tr2" style="top:1200px">{e(tr)}</div></div>'.replace("☀️ ", '<span style="font-family:\'Noto Color Emoji\'">☀️</span> ').replace("🌙 ", '<span style="font-family:\'Noto Color Emoji\'">🌙</span> '))
        t = done + 0.2 + d + 1.6
    E = t
    body.append(c.end(E, "Read Arabic the way it's said"))
    c.write("\n".join("      " + b for b in body), round(E + 2.9, 2))

# ---------------------------------------------------------------- i3: the days are numbers
def i3():
    c = comp("i3-days", "ARABIC · DAYS OF THE WEEK")
    D = [("الأَحَد", "Sunday", "أَحَد", "one"), ("الاِثْنَيْن", "Monday", "اثْنانِ", "two"), ("الثُّلاثاء", "Tuesday", "ثَلاثَة", "three"),
         ("الأَرْبِعاء", "Wednesday", "أَرْبَعَة", "four"), ("الخَمِيس", "Thursday", "خَمْسَة", "five")]
    body, t = [], 0.1
    body.append('<div class="ques" id="intro" style="top:640px">In Arabic, most days of the week</div><div class="ques" id="intro2" style="top:840px"><b>are just numbers.</b></div>')
    c.inn("#intro", t); c.inn("#intro2", t + 0.6); c.out_("#intro, #intro2", t + 2.4); t += 2.8
    rows = "".join(f'<div class="drow" id="w{i}"><div class="en"><b>{en}</b><span>from <bdi class="ar" lang="ar">{e(n)}</bdi> · {ne}</span></div>'
                   f'<div class="ar" lang="ar">{e(ar)}</div></div>' for i, (ar, en, n, ne) in enumerate(D))
    body.append(f'<div class="sec" id="a"><div class="q2" style="font-size:60px">Day one, day two, day three …</div><div class="drows" style="top:400px">{rows}</div></div>')
    c.inn("#a .q2", t); t += 0.5
    for i, (ar, *_rest) in enumerate(D):
        c.inn(f"#w{i}", t, 30); d = c.say(ar, t + 0.2); t += max(d, 1.0) + 0.7
    t += 1.0
    c.out_("#a", t); t += 0.4
    body.append('<div class="sec" id="b"><div class="q2" id="b0">Friday is different:</div>'
                '<div class="big" id="b1" style="top:420px" lang="ar">الجُمُعَة</div>'
                '<div class="sub" style="top:780px">the day of gathering, from <bdi class="ar" lang="ar">ج م ع</bdi>, to gather. The day of Jumuʿah prayer.</div>'
                '<div class="q2" id="b2" style="top:1060px">And Saturday?</div>'
                '<div class="big" id="b3" style="top:1150px;font-size:150px" lang="ar">السَّبْت</div></div>')
    c.inn("#b0", t); c.t(f'tl.fromTo("#b1", {{opacity:0, scale:0.94}}, {{opacity:1, scale:1, duration:0.45, ease:"power3.out"}}, {t + 0.3:.2f});')
    d = c.say("الجُمُعَة", t + 0.6); c.inn("#b .sub", t + 0.6 + d); t = t + 0.6 + d + 3.2
    c.inn("#b2", t); c.t(f'tl.fromTo("#b3", {{opacity:0, scale:0.94}}, {{opacity:1, scale:1, duration:0.45, ease:"power3.out"}}, {t + 0.3:.2f});')
    d = c.say("السَّبْت", t + 0.6); t = t + 0.6 + d + 1.6
    c.out_("#b", t)
    E = t + 0.4
    body.append(c.end(E, "Learn the words behind the words"))
    c.write("\n".join("      " + b for b in body), round(E + 2.9, 2))

# ---------------------------------------------------------------- i4: ة makes it feminine
def i4():
    c = comp("i4-ta-marbuta", "ARABIC · ONE LETTER")
    P = [("جَدّ", "grandfather", "جَدَّ", "grandmother", "جَدَّة"), ("ابْن", "son", "ابْنَ", "daughter", "ابْنَة"), ("والِد", "father", "والِدَ", "mother", "والِدَة")]
    body, t = [], 0.1
    body.append('<div class="sec" id="a"><div class="q2">Add one letter, and <i style="font-style:normal;color:var(--verdigris)">he</i> becomes <i style="font-style:normal;color:var(--rubric)">she</i>:</div>'
                '<div class="big" style="top:420px;color:var(--rubric)" lang="ar">ة</div>'
                '<div class="sub" style="top:780px">tāʾ marbūṭa: at the end of a word, it’s usually feminine</div>'
                '<div class="pairs" style="top:900px">'
                + "".join(f'<div class="pair" id="p{i}"><div><div class="ar" lang="ar">{e(m)}</div><div class="en">{en_m}</div></div><div class="to">←</div>'
                          f'<div><div class="ar" lang="ar">{e(stem)}<em>ة</em></div><div class="en">{en_f}</div></div></div>'
                          for i, (m, en_m, stem, en_f, _) in enumerate(P)).replace('<div class="pair"', '<div class="pair" dir="rtl"')
                + '</div></div>')
    c.inn("#a .q2", t); c.t(f'tl.fromTo("#a .big", {{opacity:0, scale:0.8}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.6)"}}, {t + 0.5:.2f});')
    c.inn("#a .sub", t + 1.2); t += 2.4
    for i, (m, _, _, _, f) in enumerate(P):
        c.inn(f"#p{i}", t, 30); d = c.say(m, t + 0.2); d2 = c.say(f, t + 0.2 + d + 0.35)
        t = t + 0.2 + d + 0.35 + d2 + 0.6
    t += 0.8
    c.out_("#a", t); t += 0.4
    body.append('<div class="sec" id="b"><div class="q2">But not always:</div>'
                '<div class="pairs" style="top:460px"><div class="pair" dir="rtl" id="p9"><div><div class="ar" lang="ar">أَخ</div><div class="en">brother</div></div>'
                '<div class="to">←</div><div><div class="ar" lang="ar">أُخْ<em>ت</em></div><div class="en">sister</div></div></div></div>'
                '<div class="sub" style="top:760px">Sister ends in a plain <bdi class="ar" lang="ar">ت</bdi>, with no <bdi class="ar" lang="ar">ة</bdi>.</div></div>')
    c.inn("#b .q2", t); c.inn("#p9", t + 0.4, 30); d = c.say("أَخ", t + 0.6); d2 = c.say("أُخْت", t + 0.6 + d + 0.35)
    c.inn("#b .sub", t + 0.6 + d + 0.35 + d2 + 0.2); t = t + 0.6 + d + 0.35 + d2 + 3.0
    c.out_("#b", t)
    E = t + 0.4
    body.append(c.end(E, "Spot the patterns, learn faster"))
    c.write("\n".join("      " + b for b in body), round(E + 2.9, 2))

# ---------------------------------------------------------------- i5: three things you say in every prayer, word by word
def i5():
    c = comp("i5-salah-words", "YOUR SALAH · WORD BY WORD")
    PH = [("اللَّهُ أَكْبَرُ", [("اللَّهُ", "Allah"), ("أَكْبَرُ", "is the Greatest")], "Allah is the Greatest."),
          ("سَمِعَ اللَّهُ لِمَنْ حَمِدَهُ", [("سَمِعَ", "hears"), ("اللَّهُ", "Allah"), ("لِمَنْ", "the one who"), ("حَمِدَهُ", "praises Him")], "Allah hears the one who praises Him."),
          ("رَبَّنا وَلَكَ الْحَمْدُ", [("رَبَّنا", "Our Lord"), ("وَلَكَ", "and to You (belongs)"), ("الْحَمْدُ", "all praise")], "Our Lord, and to You belongs all praise.")]
    body, t = [], 0.1
    body.append('<div class="ques" id="intro" style="top:640px">You say these in every prayer.</div><div class="ques" id="intro2" style="top:840px"><b>Here’s what each word means.</b></div>')
    c.inn("#intro", t); c.inn("#intro2", t + 0.6); c.out_("#intro, #intro2", t + 2.4); t += 2.8
    for k, (ar, ws, en) in enumerate(PH):
        s = f"p{k}"
        c.inn(f"#{s} .q2", t); d = c.say(ar, t + 0.4)
        stagger(c, [f"#{s}w{i}" for i in range(len(ws))], t + 0.5, 0.35, 30)
        c.inn(f"#{s} .tr", t + 0.5 + len(ws) * 0.35 + 0.4)
        t = max(t + 0.4 + d, t + 0.5 + len(ws) * 0.35) + 2.8
        c.out_(f"#{s}", t); t += 0.4
        size = 64 if len(ws) == 4 else 78
        body.append(f'<div class="sec" id="{s}"><div class="q2">{["When you start", "When you rise from bowing", "Then you say"][k]}</div>'
                    f'<div class="words" style="top:520px">' + "".join(f'<div class="w" id="{s}w{i}"><div class="ar" lang="ar" style="font-size:{size}px">{e(a)}</div><div class="en">{e(m)}</div></div>' for i, (a, m) in enumerate(ws))
                    + f'</div><div class="tr" style="top:900px">“{e(en)}”</div></div>')
    E = t
    body.append(c.end(E, "Understand every word of your salah"))
    c.write("\n".join("      " + b for b in body), round(E + 2.9, 2))

ALL = {"q1-guess-food": q1, "q2-loanwords": q2, "q3-listen": q3, "q4-salah-where": q4, "q5-numbers": q5,
       "i1-salam-reply": i1, "i2-sun-letters": i2, "i3-days": i3, "i4-ta-marbuta": i4, "i5-salah-words": i5}

if __name__ == "__main__":
    ids = [a for a in sys.argv[1:] if not a.startswith("--")]
    T.LUFS.update({vid: -16.0 for vid in ALL})          # voice only: all at a normal TikTok loudness
    for vid, fn in ALL.items():
        if ids and vid not in ids: continue
        T.level(vid) if "--level" in sys.argv else fn()
