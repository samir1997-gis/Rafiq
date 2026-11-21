#!/usr/bin/env python3
"""The four videos for the week of 21 Nov 2026 (#395), all in the every-video standard (FORMATS.md): Callum's spoken hook with one
shouted word slammed on, a background that fits the hook's own words, words one at a time, a click on every count, Rafiq's Arabic
level with Callum, the closing ask heard in full, the fountain bed, the cream page (never the pastel one).

  a9-letters   The 9 Arabic letters with no real match in English: the winning alphabet board (29 Oct, 378,000 views) cut down to
               nine, each lit as the owner says it (his own recording, voice/alphabet), Callum's tip for each
  l5-letters   Name the letter, each one harder (the weekly ladder): ب, ج, ق, then ع and ه in the middle of a word
  g13-not      "I don't…": لا in front of the verb (rule_quiz, g6's hook)
  w9-istiftah  The opening duʿāʾ word by word: five of its words end in ـكَ, "You": you speak to Allah directly
               (salah-data.js and the app's recordings; Abū Dāwūd 775, at-Tirmidhī 242)

  python3 brag-quiz/build_nov21.py [id ...]          then  python3 brag-quiz/framecap.py brag-quiz/out/<id>/composition brag-quiz/out/<id>/<id>.mp4
  python3 brag-quiz/build_nov21.py --level [id ...]
Voices: brag-quiz/voice/nov21-lines.json (one ElevenLabs run); word timings from align_words.py (pocketsphinx)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build_formula as BF, build_teach as T, build_social as SO
from build_formula import clip, say_up, hook_in, count_down, cap, cap_out, whip_in, whip_out, pop
from build_ten import cnt, reveal
from build_teach import e

V = "brag-quiz/voice/nov21/"
CLICK = "brag-quiz/sfx/ref/click.wav"

def letters_bg(letters, label, n, red=()):
    """A hook background that fits a hook about letters: the letters scattered faintly round the page, drifting; a counter that
    clicks up to n on the shouted number (at frame 0), its letters ticking in one by one; then they ripple when "letters" is said."""
    spots = [(70, 180, 150, -8), (820, 150, 170, 7), (60, 1180, 190, 6), (800, 1150, 160, -6), (420, 1290, 130, 4), (90, 1500, 140, -4),
             (760, 1470, 180, 8), (430, 140, 120, -5), (880, 420, 110, 9), (40, 430, 120, -7), (600, 1640, 120, 5), (250, 1680, 110, -9)]
    html = "".join(f'<div class="lbg{" r" if l in red else ""}" id="lb{k}" style="left:{x}px;top:{y}px;font-size:{sz}px;transform:rotate({r}deg)">{l}</div>'
                   for k, (l, (x, y, sz, r)) in enumerate(zip(letters, spots)))
    html += f'<div class="lcnt" id="lcnt"><b id="lcn">0</b><small>{label}</small></div>'
    def anim(c, at, d):
        c.css += (".hw.loud { letter-spacing:.05em; } .lbg { position:absolute; font-family:var(--ar); font-weight:700; color:var(--ink); opacity:.12; line-height:1; }"
                  ".lbg.r { color:var(--rubric); opacity:.2; }"
                  ".lcnt { position:absolute; left:340px; right:340px; top:330px; height:220px; border-radius:40px; background:var(--card); "
                  "border:5px solid var(--rubric); box-shadow:0 18px 40px -18px rgba(23,38,43,.4); display:flex; flex-direction:column; align-items:center; justify-content:center; }"
                  ".lcnt b { font-family:\"Fredoka\", var(--la); font-size:130px; line-height:1; color:var(--rubric); } .lcnt small { font-weight:700; font-size:30px; letter-spacing:.2em; color:var(--ink); }")
        for k in range(len(letters)):
            c.t(f'tl.fromTo("#lb{k}", {{y:0}}, {{y:{-40 if k % 2 else 34}, duration:{d + 0.3:.2f}, ease:"none"}}, 0);')
        c.t(f'tl.fromTo("#lcnt", {{scale:0.6, opacity:0.4}}, {{scale:1, opacity:1, duration:0.35, ease:"back.out(2)"}}, 0.05);')
        for k in range(1, n + 1):                                          # the count runs while the number is shouted
            tk = 0.12 + 0.95 * k / n
            c.t(f'tl.set("#lcn", {{textContent:"{k}"}}, {tk:.2f});'); clip(c, CLICK, tk, 0.8)
            c.t(f'tl.fromTo("#lcn", {{scale:1.25}}, {{scale:1, duration:0.12, ease:"power2.out", immediateRender:false}}, {tk:.2f});')
        r = at(2)                                                          # "letters": they ripple
        c.t(f'tl.to(".lbg", {{opacity:.3, scale:1.15, duration:0.18, yoyo:true, repeat:1, stagger:0.04, ease:"power2.out"}}, {r - 0.05:.2f});')
    return html, anim

# ------------------------------------------------------------------------------------------------ a9-letters
NINE = [("ح", "ḥāʾ", "ha", "t1"), ("خ", "khāʾ", "kha", "t2"), ("ص", "ṣād", "sad", "t3"), ("ض", "ḍād", "dad", "t4"), ("ط", "ṭāʾ", "ta", "t5"),
        ("ظ", "ẓāʾ", "dha", "t6"), ("ع", "ʿayn", "ayn", "t7"), ("غ", "ghayn", "ghayn", "t8"), ("ق", "qāf", "qaf", "t9")]
def a9():
    """The winning alphabet board (#297, 29 Oct: 378,000 views) cut down to the nine letters English has no real match for, in the
    standard: Callum's hook (NINE shouted), then each card lights up as the owner says the letter (his own recording) and Callum gives
    the tip; the board stays ticked and "n / 9" fills underneath, as on the original."""
    c = SO.vcomp("a9-letters", "THE ALPHABET"); c.bed = True; body = []
    t = hook_in(c, body, ("NINE Arabic letters have no real match in English. Can you say them all?".split(), {0: "loud", 4: "red", 8: "circle"}, V + "a9-h1.mp3"),
                bg=letters_bg([l for l, *_ in NINE] + ["ح", "ع", "ق"], "LETTERS", 9, red=("ع", "ض", "ق")))
    W, Hc, G, X0, Y0 = 280, 280, 24, 98, 420
    cards = ""
    for i, (l, nm, _, _) in enumerate(NINE):
        r, col = divmod(i, 3); x = X0 + (2 - col) * (W + G); y = Y0 + r * (Hc + G)     # right to left, as the alphabet reads
        cards += f'<div class="a9c" id="a9c{i}" style="left:{x}px;top:{y}px"><b>{l}</b><span>{nm}</span><i>✓</i></div>'
    body.append(f'<div class="sec" id="brd"><div class="q2" id="bq" style="top:285px">SAY EACH ONE OUT LOUD</div>{cards}'
                '<div id="a9bar"><i></i></div><div id="a9n">0 / 9</div></div>')
    c.css += (".a9c { position:absolute; width:280px; height:280px; border-radius:36px; background:var(--card); border:4px solid rgba(23,38,43,.12); "
              "box-shadow:0 14px 30px -18px rgba(23,38,43,.4); display:flex; flex-direction:column; align-items:center; justify-content:center; }"
              ".a9c b { font-family:var(--ar); font-weight:700; font-size:150px; line-height:1.15; color:var(--ink); }"
              ".a9c span { font-weight:700; font-size:40px; color:var(--ink-soft); margin-top:-6px; }"
              ".a9c i { position:absolute; top:14px; right:20px; font-style:normal; font-weight:700; font-size:40px; color:var(--verdigris); opacity:0; }"
              "#a9bar { position:absolute; left:120px; right:120px; top:1345px; height:22px; border-radius:11px; background:rgba(23,38,43,.1); overflow:hidden; }"
              "#a9bar i { position:absolute; inset:0; background:var(--rubric); transform-origin:0 50%; transform:scaleX(0); border-radius:11px; }"
              "#a9n { position:absolute; left:0; right:0; top:1385px; text-align:center; font-weight:700; font-size:52px; color:var(--ink); }"
              ".cc { position:absolute; left:70px; right:70px; top:1480px; text-align:center; font-weight:700; font-size:60px; line-height:1.18; color:var(--ink); }"
              ".cw { display:inline-block; opacity:0; } .cw.r { color:var(--rubric); } .cw.g { color:var(--verdigris); }")
    whip_in(c, "brd", t)
    di = clip(c, V + "a9-intro.mp3", t + 0.1); body.append(cap(c, "ci", V + "a9-intro.mp3", t + 0.1, (("loud", "r"),)))
    t += 0.1 + di + 0.35; cap_out(c, "ci", t - 0.25)
    for i, (l, nm, clipname, tip) in enumerate(NINE):
        s = f"#a9c{i}"
        c.t(f'tl.to("{s}", {{backgroundColor:"#E9B949", borderColor:"#E9B949", scale:1.12, duration:0.14, ease:"back.out(3)"}}, {t:.2f});')
        c.t(f'tl.to("{s}", {{scale:1.05, duration:0.25, ease:"power2.out"}}, {t + 0.16:.2f});')
        c.t(f'tl.set("#a9n", {{textContent:"{i + 1} / 9"}}, {t:.2f});'); clip(c, CLICK, t, 0.7)
        c.t(f'tl.to("#a9bar i", {{scaleX:{(i + 1) / 9:.4f}, duration:0.3, ease:"power2.out"}}, {t:.2f});')
        d1 = say_up(c, "", t + 0.05, src=V + f"owner-{clipname}.mp3")       # the owner says the letter, as on the original reel
        u = t + 0.05 + d1 + 0.15; mp3 = V + f"a9-{tip}.mp3"
        d2 = clip(c, mp3, u); body.append(cap(c, f"c{i}", mp3, u, (("heavy", "r"), ("throat", "g"), ("loch", "g"), ("french", "g"), ("back", "g"), ("nicknamed", "r"))))
        done = u + d2 + 0.25
        c.t(f'tl.to("{s}", {{backgroundColor:"rgba(46,114,99,.12)", borderColor:"#2E7263", scale:1, duration:0.3, ease:"power2.out"}}, {done:.2f});')
        c.t(f'tl.to("{s} i", {{opacity:1, duration:0.2}}, {done:.2f});')
        cap_out(c, f"c{i}", done + 0.15)
        t = done + 0.45                                                    # a beat to say it out loud
    c.t(f'tl.to(".a9c", {{scale:1.06, duration:0.18, yoyo:true, repeat:1, stagger:0.04, ease:"power2.out"}}, {t:.2f});')
    t += 0.8; c.out_("#brd", t); t += 0.4
    end = clip(c, V + "a9-end.mp3", t + 0.4)
    body.append(c.end(t, "Which one is the hardest for you? Comment it 👇 and save this to practise later"))
    c.write("\n".join("      " + b for b in body), round(t + 0.4 + end + 0.9, 2))

# ------------------------------------------------------------------------------------------------ l5-letters
def l5():
    """The weekly ladder #5, the alphabet: name the letter, each one harder: ب 90% → ج 70% → ق 45% → ع in the middle of a word 20% →
    the final boss ه in the middle of a word 3%. The owner says each letter's name (his recording). The percentages are a game device."""
    A = lambda w: f'<span class="ar" lang="ar" style="font-size:165px">{w}</span>'
    a = lambda w: f'<span class="ar" lang="ar">{w}</span>'
    BF.ladder("l5-letters", [
        (90, "Easy one first. What’s this letter called?", A("ب"), "<b>bāʾ</b>", "ب", "ans", ""),
        (70, "Next one. What’s it called?", A("ج"), "<b>jīm</b>", "ج", "ans", ""),
        (45, "Two dots on top. Which letter is it?", A("ق"), "<b>qāf</b>", "ق", "ans", ""),
        (20, "In the middle of a word. Which one?", A("ـعـ"), f"<b>ʿayn</b> &nbsp;{a('ع')}", "ـعـ", "ans", "Got this far? Comment below 👇"),
        (3, "The final boss 😈 Also in the middle of a word:", A("ـهـ"), f"<b>hāʾ</b> &nbsp;{a('ه')}", "ـهـ", "ans", ""),
    ], "How far did you get? Comment your level 👇 and send this to someone learning to read Arabic",
        voice={"ب": V + "owner-ba.mp3", "ج": V + "owner-jim.mp3", "ق": V + "owner-qaf.mp3", "ـعـ": V + "owner-ayn.mp3", "ـهـ": V + "owner-haa.mp3"},
        kicker="QUIZ · THE ALPHABET",
        hook=("FIVE Arabic letters, each one harder to spot. How far can you get?".split(), {0: "loud", 5: "red", 7: "circle"}, V + "l5-h1.mp3"),
        vo=[V + f"l5-q{k}.mp3" for k in range(1, 6)], end="brag-quiz/voice/ladder3/end.mp3",
        bg=letters_bg(["ب", "ج", "ق", "ع", "ه", "ـعـ", "ـهـ", "ف", "ح", "ت", "خ", "غ"], "LETTERS", 5, red=("ـعـ", "ـهـ")))

# ------------------------------------------------------------------------------------------------ g13-not
def g13():
    """rule_quiz (g6's shape and hook): أَعْرِفُ I know → لا أَعْرِفُ I don't know → لا نَعْرِفُ we don't know; لا in front, the verb unchanged.
    Quiz: يَشْرَبُ → he doesn't drink? (traps ما شَرِبَ he didn't drink, لا تَشْرَبُ she doesn't drink); نَذْهَبُ → we don't go? (traps لَنْ نَذْهَبَ
    we won't go, لا يَذْهَبُونَ they don't go)."""
    W = V + "g13-"
    BF.rule_quiz("g13-not", W,
        [("أَعْرِفُ", 'أَعْرِفُ', "I know", "", W + "t1"), ("لا أَعْرِفُ", '<em>لا</em> أَعْرِفُ', "I don’t know", "", W + "t2"),
         ("لا نَعْرِفُ", '<em>لا</em> نَعْرِفُ', "we don’t know", "", W + "t3")],
        'one word in front: <bdi lang="ar" dir="rtl">لا</bdi> = don’t',
        ('don’t = <span class="ar" lang="ar"><em>لا</em></span> in front', 'and the verb stays exactly the same'),
        [("يَشْرَبُ", "he drinks", "he doesn’t drink", ["ما شَرِبَ", "لا يَشْرَبُ", "لا تَشْرَبُ"], 1, '<bdi lang="ar"><em>لا</em></bdi> in front = don’t'),
         ("نَذْهَبُ", "we go", "we don’t go", ["لَنْ نَذْهَبَ", "لا يَذْهَبُونَ", "لا نَذْهَبُ"], 2, '<bdi lang="ar"><em>لا</em></bdi> in front = don’t')],
        "How many did you get? 0, 1 or 2? Comment below 👇 and send this to your Arabic study buddy",
        words={"لا نَعْرِفُ": W + "la-narif.mp3", "لا يَشْرَبُ": W + "la-yashrab.mp3", "لا نَذْهَبُ": W + "la-nadhhab.mp3"})

# ------------------------------------------------------------------------------------------------ w9-istiftah
LINE = "سُبْحانَكَ اللَّهُمَّ وَبِحَمْدِكَ وَتَبارَكَ اسْمُكَ وَتَعالى جَدُّكَ وَلا إِلٰهَ غَيْرُكَ"
ROWS = [  # (the words, with the ـكَ "You" ending marked by |, as said; Callum's meaning line)
    (["سُبْحانَ|كَ", "اللَّهُمَّ"], "m1", "Glory be to You, O Allah"),
    (["وَبِحَمْدِ|كَ"], "m2", "and with Your praise"),
    (["وَتَبارَكَ", "اسْمُ|كَ"], "m3", "Blessed is Your name"),
    (["وَتَعالى", "جَدُّ|كَ"], "m4", "exalted is Your majesty"),
    (["وَلا", "إِلٰهَ", "غَيْرُ|كَ"], "m5", "and there is no god other than You")]
def w9():
    """The opening duʿāʾ (duʿāʾ al-istiftāḥ) word by word, after the owner's "A Sunnah most of us skip" (10,000 views): Callum's hook
    (FIVE shouted: five times you say "You" to Allah), the line said whole (the app's recording), then row by row: Rafiq says the
    words (the app's recordings), Callum says what they mean; then the pattern: five words end in ـكَ "You / Your" (the ك of تَبارَكَ
    is the word's own, ب ر ك); your turn رَبُّكَ (my Lord / your Lord / our Lord?), 3-2-1; ask: what do you say straight after it?
    Meanings: salah-data.js. Source: Abū Dāwūd 775, at-Tirmidhī 242 (Abū Saʿīd al-Khudrī)."""
    c = SO.vcomp("w9-istiftah", "SALAH WORD BY WORD"); c.bed = True; body = []
    ka = lambda w: w.replace("|كَ", '<em class="ka">كَ</em>').replace("|", "")
    faint = " ".join(ka(w) for ws, _, _ in ROWS for w in ws)
    def bg_anim(c, at, d):
        c.css += (".hw.loud { letter-spacing:.05em; } #w9bg { position:absolute; left:60px; right:60px; top:1420px; text-align:center; direction:rtl; font-family:var(--ar); font-weight:700; "
                  "font-size:76px; line-height:1.75; color:var(--ink); opacity:.16; } #w9bg .ka { font-style:normal; }"
                  ".lcnt { position:absolute; left:340px; right:340px; top:330px; height:220px; border-radius:40px; background:var(--card); "
                  "border:5px solid var(--rubric); box-shadow:0 18px 40px -18px rgba(23,38,43,.4); display:flex; flex-direction:column; align-items:center; justify-content:center; }"
                  ".lcnt b { font-family:\"Fredoka\", var(--la); font-size:130px; line-height:1; color:var(--rubric); } .lcnt small { font-weight:700; font-size:30px; letter-spacing:.2em; color:var(--ink); }")
        c.t('tl.fromTo("#lcnt", {scale:0.6, opacity:0.4}, {scale:1, opacity:1, duration:0.35, ease:"back.out(2)"}, 0.05);')
        for k in range(1, 6):                                              # FIVE: the count clicks up, and each "You" in the duʿāʾ lights red
            tk = 0.12 + 0.95 * k / 5
            c.t(f'tl.set("#lcn", {{textContent:"{k}"}}, {tk:.2f});'); clip(c, CLICK, tk, 0.8)
            c.t(f'tl.fromTo("#lcn", {{scale:1.25}}, {{scale:1, duration:0.12, ease:"power2.out", immediateRender:false}}, {tk:.2f});')
            c.t(f'tl.to("#w9bg .ka:nth-of-type({k})", {{color:"#B4322A", duration:0.15}}, {tk:.2f});')
        c.t(f'tl.to("#w9bg", {{opacity:.34, duration:0.4}}, {at(9):.2f});')   # "...to Allah": the duʿāʾ comes up a little
    bg = (f'<div id="w9bg">{faint}</div><div class="lcnt" id="lcnt"><b id="lcn">0</b><small>TIMES “YOU”</small></div>', bg_anim)
    t = hook_in(c, body, ("FIVE times in this one line, you say ‘You’ to Allah. Most people never notice.".split(), {0: "loud", 8: "red", 13: "circle"}, V + "w9-h1.mp3"), bg=bg)
    c.css += (".cc { position:absolute; left:70px; right:70px; text-align:center; font-weight:700; font-size:58px; line-height:1.2; color:var(--ink); }"
              ".cw { display:inline-block; opacity:0; } .cw.r { color:var(--rubric); } .cw.g { color:var(--verdigris); }"
              ".w9line { position:absolute; left:60px; right:60px; text-align:center; direction:rtl; font-family:var(--ar); font-weight:700; line-height:1.7; color:var(--ink); }"
              ".w9line .ka, .w9row .ka { font-style:normal; } .w9rows { position:absolute; left:60px; right:60px; top:410px; display:flex; flex-direction:column; gap:18px; }"
              ".w9row { display:flex; align-items:center; justify-content:space-between; min-height:150px; padding:6px 36px; background:var(--card); "
              "border:4px solid rgba(23,38,43,.12); border-radius:30px; box-shadow:0 12px 26px -16px rgba(23,38,43,.35); }"
              ".w9row .en { font-weight:700; font-size:40px; color:var(--ink); max-width:440px; text-align:left; line-height:1.15; }"
              ".w9row .ar { font-family:var(--ar); font-weight:700; font-size:78px; line-height:1.5; direction:rtl; }"
              ".w9row .ar span { display:inline-block; } .w9note { position:absolute; left:80px; right:80px; top:1345px; text-align:center; font-size:34px; color:var(--ink-soft); }"
              ".w9q { position:absolute; left:0; right:0; text-align:center; font-family:var(--ar); font-weight:700; font-size:220px; line-height:1.3; color:var(--ink); }"
              ".w9ops { position:absolute; left:90px; right:90px; top:1010px; display:flex; flex-direction:column; gap:22px; }"
              ".w9ops .op { height:120px; display:flex; align-items:center; justify-content:center; border-radius:28px; background:var(--card); "
              "border:4px solid rgba(23,38,43,.13); } .w9ops .op b { font-size:56px; font-weight:700; color:var(--ink); }")
    # 1. the line, said whole
    body.append(f'<div class="sec" id="ln"><div class="q2" style="top:300px">THE OPENING DUʿĀʾ</div>'
                f'<div class="w9line" id="lnar" style="top:470px;font-size:96px">{" ".join(ka(w) for ws, _, _ in ROWS for w in ws)}</div></div>')
    whip_in(c, "ln", t)
    dl = clip(c, V + "w9-l1.mp3", t + 0.1); body.append(cap(c, "c0", V + "w9-l1.mp3", t + 0.1, (("allahu", "g"), ("akbar", "g"), ("fatiha", "g"))))
    c.css += "#c0 { top:1250px; }"
    c.t(f'tl.fromTo("#lnar", {{opacity:0, scale:0.95}}, {{opacity:1, scale:1, duration:0.5, ease:"power3.out"}}, {t + 0.2:.2f});')
    u = t + 0.1 + dl + 0.25; cap_out(c, "c0", u)
    d = say_up(c, LINE, u)                                                 # the app's own recording of the whole line
    c.t(f'tl.fromTo("#lnar", {{scale:1}}, {{scale:1.03, duration:{d:.2f}, ease:"none", immediateRender:false}}, {u:.2f});')
    t = whip_out(c, "ln", u + d + 0.4)
    # 2. word by word: Rafiq says the words, Callum says what they mean
    rows = "".join(f'<div class="w9row" id="wr{k}"><div class="en" id="wr{k}e">{en}</div><div class="ar">'
                   + " ".join(f'<span id="wr{k}a{j}">{ka(w)}</span>' for j, w in enumerate(ws)) + '</div></div>'
                   for k, (ws, _, en) in enumerate(ROWS))
    body.append(f'<div class="sec" id="wb"><div class="q2" style="top:300px">WORD BY WORD</div><div class="w9rows">{rows}</div>'
                '<div class="w9note" id="wnote">The ك of <bdi lang="ar" style="font-family:var(--ar)">تَبارَكَ</bdi> is part of the word itself: <bdi lang="ar" style="font-family:var(--ar)">ب ر ك</bdi>, blessing.</div></div>')
    whip_in(c, "wb", t); t += 0.25
    for k, (ws, m, en) in enumerate(ROWS):
        c.inn(f"#wr{k}", t, 30); c.t(f'tl.set("#wr{k}e", {{opacity:0}}, 0);')
        for j, w in enumerate(ws):
            c.t(f'tl.fromTo("#wr{k}a{j}", {{opacity:0.25}}, {{opacity:1, duration:0.2}}, {t + 0.1:.2f});')
            dw = say_up(c, w.replace("|", ""), t + 0.1); c.sfx("tap", t + 0.1); t += dw + 0.05
        mp3 = V + f"w9-{m}.mp3"; dm = clip(c, mp3, t + 0.1)
        c.t(f'tl.fromTo("#wr{k}e", {{opacity:0, x:-30}}, {{opacity:1, x:0, duration:0.35, ease:"power3.out"}}, {t + 0.12:.2f});')
        t += 0.1 + dm + 0.35
    # 3. the pattern: five words end in ـكَ
    mp3 = V + "w9-rule.mp3"; dr = clip(c, mp3, t + 0.1)
    body.append(cap(c, "c1", mp3, t + 0.1, (("ka", "r"), ("you", "r"), ("allah", "g"))))
    c.css += "#c1 { top:1430px; font-size:52px; }"
    hit = t + 0.1 + BF.key_at(mp3, "five", 0.8)
    for k in range(5):                                                     # the five "You"s light up, a click each
        c.t(f'tl.to("#wr{k} .ka", {{color:"#B4322A", scale:1.3, duration:0.18, ease:"back.out(3)"}}, {hit + k * 0.3:.2f});')
        c.t(f'tl.to("#wr{k} .ka", {{scale:1, duration:0.2}}, {hit + k * 0.3 + 0.2:.2f});'); clip(c, CLICK, hit + k * 0.3, 0.8)
    c.inn("#wnote", hit + 1.8)
    cap_out(c, "c1", t + 0.1 + dr + 0.3); t = whip_out(c, "wb", t + 0.1 + dr + 0.5)
    # 4. your turn: رَبُّكَ
    body.append('<div class="sec" id="yq"><div class="q2" style="top:300px">YOUR TURN</div>'
                f'<div class="w9q" id="yqa" style="top:400px">رَبُّ<em class="ka" style="font-style:normal;color:var(--rubric)">كَ</em></div>'
                + cnt("yqc", 790) + '<div class="w9ops">' + "".join(f'<div class="op" id="yo{i}"><b>{o}</b></div>' for i, o in enumerate(["my Lord", "your Lord", "our Lord"]))
                + '</div></div>')
    whip_in(c, "yq", t)
    da = clip(c, V + "w9-q1a.mp3", t + 0.1); c.t(f'tl.fromTo("#yqa", {{opacity:0, scale:0.9}}, {{opacity:1, scale:1, duration:0.4, ease:"power3.out"}}, {t + 0.2:.2f});')
    dq = say_up(c, "", t + 0.1 + da + 0.1, src=V + "w9-rabbuka.mp3")
    tb = t + 0.1 + da + 0.1 + dq + 0.15; db = clip(c, V + "w9-q1b.mp3", tb)
    for i in range(3): c.inn(f"#yo{i}", tb + BF.key_at(V + "w9-q1b.mp3", ["my", "your", "our"][i], 0.4 + i * 0.6) - 0.05)
    done = count_down(c, "yqc", tb + db + 0.25)
    reveal(c, "#yo1", ["#yo0", "#yo2"], done); c.sfx("correct", done)
    d2 = say_up(c, "", done + 0.3, src=V + "w9-rabbuka.mp3")
    t = done + 0.3 + d2 + 1.4; c.out_("#yq", t); t += 0.4
    end = clip(c, V + "w9-end.mp3", t + 0.4)
    body.append(c.end(t, "What do you say straight after it? Comment it 👇 and send this to someone you pray with"))
    c.write("\n".join("      " + b for b in body), round(t + 0.4 + end + 0.9, 2))

ALL = {"a9-letters": a9, "l5-letters": l5, "g13-not": g13, "w9-istiftah": w9}
if __name__ == "__main__":
    ids = [a for a in sys.argv[1:] if not a.startswith("--")]
    T.LUFS.update({v: -16.0 for v in ALL})
    for vid, fn in ALL.items():
        if ids and vid not in ids: continue
        T.level(vid) if "--level" in sys.argv else fn()
