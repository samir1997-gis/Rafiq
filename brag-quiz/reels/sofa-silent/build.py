#!/usr/bin/env python3
"""The sofa story as a silent reel (#355), on the silent template (safari-silent, mattress-silent, magazine-silent): our colours,
Playfair Display, typed text with one word in italic serif, a fan of numbered cards, five numbered points with a wipe between them;
no voice, only sound effects. Every move eased (MOTION-STYLE.md). Figures are faceless.

  python3 brag-quiz/reels/sofa-silent/build.py
  then  python3 brag-quiz/framecap.py brag-quiz/reels/sofa-silent/out/v brag-quiz/reels/sofa-silent/out/raw.mp4
Facts: sofa from Turkish sofa, from Arabic صُفَّة, a raised bench or platform of stone or brick (Wiktionary, Wikipedia); English in
the 1620s for a raised floor with carpets and cushions, a long padded seat by 1717 (Etymonline via Dictionary.com); the people of the
ṣuffa lived on a platform in the Prophet's ﷺ mosque, Abū Hurayrah among them (al-Bukhārī 6452); صَفّ a row, سَوُّوا صُفُوفَكُمْ (al-Bukhārī 723).
Only "same letters" is claimed for صُفَّة and صَفّ: whether ṣuffa comes from the root ص ف ف is argued over."""
import html, os, shutil, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
V6 = os.path.join(ROOT, "brag-output-v6/composition/assets"); SFX = os.path.join(ROOT, "brag-quiz/sfx")
SR = 48000; END = 999                                             # set at the end, from the last line
INK, MAR, CREAM, GOLD, SKY, BONE = "#17262B", "#B4322A", "#F1ECE0", "#E9B949", "#2E7263", "#EADFC8"   # ink, rubric, paper, gold, verdigris, bone
TEAL = SKY

js, snd, body = [], [], []
T = js.append
def S(name, t, gain=1.0): snd.append((name, t, gain))

def typed(id, parts, t0, rate=0.032, tick=3):
    """Text that types out a character at a time (a key tick every few), from t0; parts: [(text, 'em'|None)]. Returns (html, end)."""
    out, n, t = "", 0, t0
    for txt, st in parts:
        span = ""
        for ch in txt:
            span += f'<span class="ch" id="{id}{n}">{html.escape(ch)}</span>'
            T(f'tl.set("#{id}{n}", {{opacity:1}}, {t:.3f});')
            if n % tick == 0 and ch != " ": S("soft/type.wav", t, 0.5 + 0.3 * ((n * 7) % 5) / 4)
            n += 1; t += rate
        out += f'<em>{span}</em>' if st == "em" else ("<br>" if st == "br" else span)
    return out, t

def words(id, ws, t0, gap=0.28):
    """Arabic, a word at a time (letters must stay joined, so never a letter at a time)."""
    out = ""
    for k, (w, cls) in enumerate(ws):
        out += f'<span class="aw {cls}" id="{id}{k}">{w}</span> '
        T(f'tl.fromTo("#{id}{k}", {{opacity:0, y:14}}, {{opacity:1, y:0, duration:0.25, ease:"power3.out"}}, {t0 + k * gap:.2f});')
        S("soft/tick.wav", t0 + k * gap, 0.7)
    return out

def pop(sel, t, s0=0.4, sound="ref/tap.wav", g=1.0):
    T(f'tl.fromTo("{sel}", {{opacity:0, scale:{s0}}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(1.4)", immediateRender:false}}, {t:.2f});')
    if sound: S(sound, t, g)

def scene(id, t0, t1):
    T(f'tl.set("#{id}", {{opacity:1}}, {t0:.2f});')
    if t1 < END: T(f'tl.set("#{id}", {{opacity:0}}, {t1:.2f});')

WIPES = []
def wipe(t, colour):
    """A panel sweeps across from the right (a low whoosh); the scenes swap while it covers the frame."""
    k = len(WIPES); WIPES.append(f'<div class="wipe" id="w{k}" style="background:{colour}"></div>')
    T(f'tl.fromTo("#w{k}", {{x:1100}}, {{x:0, duration:0.24, ease:"power3.out"}}, {t:.2f});')
    T(f'tl.to("#w{k}", {{x:-1100, duration:0.26, ease:"power3.in"}}, {t + 0.26:.2f});')
    S("ref/swoosh-low.wav", t, 1.0); S("soft/whoosh.wav", t + 0.05, 0.5)
    return t + 0.24

def head(id, num, parts, t0):
    """A point's number, its heading (types out) and returns the html and when the heading is done."""
    h, t = typed(id + "h", parts, t0 + 0.15, rate=0.045, tick=2)
    T(f'tl.fromTo("#{id}n", {{opacity:0}}, {{opacity:1, duration:0.25, ease:"power3.out"}}, {t0:.2f});')
    return f'<div class="num" id="{id}n">{num:02d} / 05</div><div class="hd">{h}</div>', t


SOFA = lambda w, c=MAR: f"""<svg width="{w}" viewBox="0 0 320 170"><rect x="30" y="20" width="260" height="80" rx="24" fill="{c}" stroke="{INK}" stroke-width="6"/>
<rect x="6" y="60" width="60" height="90" rx="22" fill="{c}" stroke="{INK}" stroke-width="6"/><rect x="254" y="60" width="60" height="90" rx="22" fill="{c}" stroke="{INK}" stroke-width="6"/>
<rect x="56" y="90" width="208" height="56" rx="14" fill="{BONE}" stroke="{INK}" stroke-width="6"/><path d="M160 92 L 160 144" stroke="{INK}" stroke-width="5"/>
<path d="M30 150 L 30 166 M 290 150 L 290 166" stroke="{INK}" stroke-width="10" stroke-linecap="round"/></svg>"""
BENCH = lambda w: f"""<svg width="{w}" viewBox="0 0 520 170"><rect x="6" y="40" width="508" height="124" rx="10" fill="#c9b9a0" stroke="{INK}" stroke-width="6"/>
<path d="M6 80 L 514 80 M 6 122 L 514 122 M 90 40 L 90 80 M 230 40 L 230 80 M 370 40 L 370 80 M 160 80 L 160 122 M 300 80 L 300 122 M 440 80 L 440 122 M 90 122 L 90 164 M 230 122 L 230 164 M 370 122 L 370 164" stroke="{INK}" stroke-width="4" opacity=".45"/>
<rect x="0" y="22" width="520" height="26" rx="8" fill="#e8dcc6" stroke="{INK}" stroke-width="6"/></svg>"""
CUSH = lambda w, c: f"""<svg width="{w}" viewBox="0 0 160 90"><rect x="6" y="10" width="148" height="72" rx="30" fill="{c}" stroke="{INK}" stroke-width="6"/></svg>"""

# ---- 0 · hook, then the title and the fan of cards ------------------------------------------------------------------------
hook, t = typed("k", [("", "br"), ("Arabic word.", "em")], 0.5, rate=0.07, tick=1); hook = "Your sofa is an" + hook   # the line on frame 0
TITLE_T = 2.2
T(f'tl.to("#hook", {{opacity:0, duration:0.15, ease:"power2.in"}}, {TITLE_T - 0.15:.2f});')
T(f'tl.fromTo("#title", {{opacity:0, scale:1.08}}, {{opacity:1, scale:1, duration:0.3, ease:"power3.out"}}, {TITLE_T:.2f});')
ICONS = [f'<svg viewBox="0 0 90 60" width="72"><rect x="4" y="14" width="82" height="36" rx="6" fill="{INK}"/></svg>',
 f'<svg viewBox="0 0 80 80" width="60"><path d="M10 70 L 10 40 C 10 14, 70 14, 70 40 L 70 70 Z" fill="{INK}"/></svg>',
 f'<svg viewBox="0 0 80 80" width="66"><path d="M14 70 C 30 50, 20 30, 40 22 C 56 16, 60 10, 66 8" fill="none" stroke="{INK}" stroke-width="6" stroke-dasharray="8 6"/><circle cx="14" cy="70" r="8" fill="{INK}"/><circle cx="66" cy="8" r="8" fill="{INK}"/></svg>',
 f'<svg viewBox="0 0 90 60" width="72"><rect x="10" y="10" width="70" height="28" rx="10" fill="{INK}"/><rect x="4" y="26" width="20" height="28" rx="8" fill="{INK}"/><rect x="66" y="26" width="20" height="28" rx="8" fill="{INK}"/></svg>',
 f'<svg viewBox="0 0 60 90" width="46"><path d="M12 26 C 12 6, 48 6, 48 26 C 48 42, 30 42, 30 58" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/><circle cx="30" cy="78" r="6" fill="{INK}"/></svg>']
cards = ""
for i in range(5):
    a = (i - 2) * 15; col = MAR if i == 2 else (CREAM if i % 2 == 0 else SKY)
    fg = CREAM if i in (1, 2, 3) else INK
    icon = ICONS[i] if fg == INK else ICONS[i].replace(f'fill="{INK}"', f'fill="{fg}"').replace(f'stroke="{INK}"', f'stroke="{fg}"')
    cards += f'<div class="card" id="cd{i}" style="background:{col};color:{fg}"><span>{i + 1}</span>{icon}</div>'
    if i == 2:
        T(f'tl.fromTo("#cd2", {{opacity:0, y:-260, rotation:0}}, {{opacity:1, y:0, duration:0.35, ease:"power3.out"}}, {TITLE_T:.2f});')
    else:
        k = [1, 3, 0, 4].index(i); tt = TITLE_T + 0.75 + k * 0.2
        T(f'tl.fromTo("#cd{i}", {{opacity:0, rotation:0}}, {{opacity:1, rotation:{a}, duration:0.35, ease:"back.out(1.4)"}}, {tt:.2f});')
        S("soft/tick-lo.wav", tt, 1.0); S("ref/click.wav", tt, 0.35)
S("soft/thump.wav", TITLE_T + 0.2, 1.0); S("boom.wav", TITLE_T + 0.2, 0.45)
SP = TITLE_T + 1.75
T(f'tl.fromTo("#cd2", {{scale:1}}, {{scale:1.1, duration:0.2, yoyo:true, repeat:1, ease:"power2.inOut"}}, {SP:.2f});')
T(f'tl.fromTo("#spark i", {{opacity:0, scale:0}}, {{opacity:1, scale:1, duration:0.3, stagger:0.04, ease:"back.out(1.4)"}}, {SP:.2f});')
S("ref/click-x2.wav", SP, 0.9); S("soft/shimmer.wav", SP, 0.35)
spark = "".join(f'<i style="left:{540 + 230 * np.cos(np.radians(200 + 28 * k)):.0f}px;top:{1035 + 150 * np.sin(np.radians(200 + 28 * k)):.0f}px"></i>' for k in range(6))
body.append(f'''<div class="sc" id="s0" style="opacity:1">
 <div class="tx big" id="hook" style="top:360px">{hook}</div>
 <div class="tx big" id="title" style="top:330px">How <em>ṣuffa</em><br>became <em>sofa</em></div>
 <div id="fan">{cards}</div><div id="spark">{spark}</div></div>''')

# ---- 1 · you sit on one every day -----------------------------------------------------------------------------------------------
t1 = wipe(SP + 1.6, TEAL); scene("s0", 0, t1); A = t1 + 0.25
l1, t = typed("a", [("You sit on one every day.", None)], A)
l2, t = typed("b", [("Nobody told you the ", None), ("word", "em"), (" is Arabic.", None)], t + 0.35)
pop("#sf1", A + 0.2, 0.6, "soft/thump.wav", 0.6)
QT = t + 0.15
pop("#sw1", QT, 0.5, "ref/click-x2.wav"); S("soft/shimmer.wav", QT + 0.1, 0.3)
body.append(f"""<div class="sc" id="s1"><div class="tx" style="top:420px">{l1}<br>{l2}</div>
 <div class="ar" id="sw1" style="top:740px;opacity:0">صُفَّة</div>
 <div id="sf1" class="obj" style="left:330px;top:1040px">{SOFA(420)}</div></div>""")

# ---- 01 · the word ṣuffa ------------------------------------------------------------------------------------------------------------
t2 = wipe(QT + 2.0, CREAM); scene("s1", t1, t2); A = t2 + 0.2
h, t = head("p1", 1, [("The word ", None), ("ṣuffa", "em")], A)
b, t = typed("p1b", [("A raised bench of stone or brick, long enough for a row of people to sit on.", None)], t + 0.2)
pop("#mt2", A + 0.5, 0.5, "soft/tick-lo.wav")
T(f'tl.fromTo("#bn", {{opacity:0, y:120}}, {{opacity:1, y:0, duration:0.5, ease:"power3.out"}}, {t - 2.0:.2f});'); S("soft/thump.wav", t - 1.6, 0.8)
for i in range(3):
    T(f'tl.fromTo("#cu{i}", {{opacity:0, y:-500, rotation:{(i - 1) * 25}}}, {{opacity:1, y:0, rotation:{(i - 1) * 4}, duration:0.55, ease:"power3.in"}}, {t - 1.4 + i * 0.35:.2f});')
    S("soft/thump.wav", t - 0.85 + i * 0.35, 0.7)
AW = t + 0.4
body.append(f"""<div class="sc" id="s2"><div class="hdw">{h}</div><div class="tx sm" style="top:560px">{b}</div>
 <div class="ar" id="mt2" style="top:760px;opacity:0">صُفَّة</div>
 <div id="bn" class="obj" style="left:280px;top:1160px">{BENCH(520)}</div>
 {''.join(f'<div id="cu{i}" class="obj" style="left:{300 + i * 165}px;top:1110px">{CUSH(150, (MAR, TEAL, GOLD)[i])}</div>' for i in range(3))}</div>""")

# ---- 02 · the people of the Ṣuffah --------------------------------------------------------------------------------------------------
t3 = wipe(AW + 1.6, TEAL); scene("s2", t2, t3); A = t3 + 0.2
h, t = head("p2", 2, [("The ", None), ("Ṣuffah", "em")], A)
b, t = typed("p2b", [("In the Prophet's ﷺ mosque, poor Companions with no homes lived on the ṣuffa. Abū Hurayrah was one of them.", None)], t + 0.2)
T(f'tl.fromTo("#box", {{opacity:0, scaleY:0.2}}, {{opacity:1, scaleY:1, duration:0.35, ease:"power3.out"}}, {t - 1.6:.2f});'); S("soft/thump.wav", t - 1.55, 0.8)
pop("#ahl", t - 1.2, 0.6, "soft/tick.wav"); pop("#src2", t - 0.3, 0.6, "ref/tap.wav")
t = t + 0.6
body.append(f"""<div class="sc" id="s3"><div class="hdw">{h}</div><div class="tx sm" style="top:560px">{b}</div>
 <div id="box" style="top:880px"><div class="aw2" id="ahl">أَهْلُ الصُّفَّة</div><div class="lg2">the people of the bench</div>
  <div id="src2" style="margin:24px auto 0;width:max-content;padding:10px 26px;border-radius:30px;background:{MAR};font-family:MO;font-size:28px;letter-spacing:.12em;color:{GOLD};opacity:0">AL-BUKHĀRĪ 6452</div></div></div>""")

# ---- 03 · the road to English -----------------------------------------------------------------------------------------------------
t4 = wipe(t + 2.0, CREAM); scene("s3", t3, t4); A = t4 + 0.2
h, t = head("p3", 3, [("The road to ", None), ("English", "em")], A)
b, t = typed("p3b", [("Arabic ṣuffa, Turkish sofa, French sofa, and by the 1620s, English sofa.", None)], t + 0.2)
CH = [("ch0", "صُفَّة", "wa", "Arabic"), ("ch1", "sofa", "", "Turkish"), ("ch2", "sofa", "", "French"), ("ch3", "sofa", "", "")]
ct, chain = A + 1.0, ""
for i, (id, w, c, lang) in enumerate(CH):
    chain += f'<div class="wc {c}" id="{id}">{w}</div>' + (f'<div class="lg" id="lg{i}">{lang}</div>' if lang else "") + ('<div class="arw">↓</div>' if i < 3 else "")
    if i < 3: pop(f"#{id}", ct, 0.6, "soft/tick-lo.wav"); pop(f"#lg{i}", ct + 0.15, 0.8, None); ct += 0.9
T(f'tl.fromTo(".arw", {{opacity:0, y:-10}}, {{opacity:1, y:0, duration:0.3, stagger:0.9, ease:"power3.out"}}, {A + 1.45:.2f});')
CF = max(t, ct) + 0.2
T(f'tl.fromTo("#ch3", {{opacity:0, scale:1.8}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.7)"}}, {CF:.2f});')   # the one slam
S("soft/thump.wav", CF + 0.15, 1.0); S("boom.wav", CF + 0.15, 0.4); S("soft/shimmer.wav", CF + 0.1, 0.4)
pop("#yr", CF + 0.6, 0.5, "ref/tap.wav")
T(f'tl.fromTo("#yrn", {{innerText:1100}}, {{innerText:1620, duration:0.7, snap:{{innerText:1}}, ease:"power2.out"}}, {CF + 0.6:.2f});')
for k in range(4): S("soft/tick-lo.wav", CF + 0.6 + 0.7 * (1 - (1 - (k + 1) / 4) ** 2), 0.5)
body.append(f"""<div class="sc" id="s4"><div class="hdw">{h}</div><div class="tx sm" style="top:560px">{b}</div><div id="chain" style="top:790px">{chain}</div>
 <div id="yr" class="obj" style="left:470px;top:1690px"><span class="tagp" style="background:{MAR};color:{GOLD}"><span id="yrn">1620</span>s</span></div></div>""")
t = CF + 1.3

# ---- 04 · from a floor to a seat -----------------------------------------------------------------------------------------------------
t5 = wipe(t + 1.8, TEAL); scene("s4", t4, t5); A = t5 + 0.2
h, t = head("p4", 4, [("From a floor to a ", None), ("seat", "em")], A)
b, t = typed("p4b", [("At first, a raised floor with carpets and cushions. By 1717, a long padded seat.", None)], t + 0.2)
pop("#y7", A + 0.5, 0.5, "ref/tap.wav")
T(f'tl.fromTo("#y7n", {{innerText:1620}}, {{innerText:1717, duration:0.9, snap:{{innerText:1}}, ease:"power2.out"}}, {A + 0.5:.2f});')
for k in range(5): S("soft/tick-lo.wav", A + 0.5 + 0.9 * (1 - (1 - (k + 1) / 5) ** 2), 0.5)
GM = t - 1.6
T(f'tl.fromTo("#sf4", {{opacity:0, scale:0.5, rotation:-6}}, {{opacity:1, scale:1, rotation:0, duration:0.55, ease:"back.out(1.5)"}}, {GM:.2f});'); S("soft/thump.wav", GM + 0.1, 0.9); S("boom.wav", GM + 0.1, 0.3)
t = t + 0.4
body.append(f"""<div class="sc" id="s5"><div class="hdw">{h}</div><div class="tx sm" style="top:560px">{b}</div>
 <div id="y7" class="obj" style="left:420px;top:830px"><span class="tagp" style="background:{MAR};color:{GOLD}" id="y7n">1717</span></div>
 <div id="sf4" class="obj" style="left:290px;top:1020px">{SOFA(500, TEAL)}</div></div>""")

# ---- 05 · your turn: صَفّ, a row ---------------------------------------------------------------------------------------------------
t6 = wipe(t + 1.8, CREAM); scene("s5", t5, t6); A = t6 + 0.2
h, t = head("p5", 5, [("Your ", None), ("turn", "em")], A)
b, t = typed("p5b", [("Same letters, ص ف ف. Before the prayer, the Prophet ﷺ said: straighten your ___.", None)], t + 0.2)
T(f'tl.fromTo("#box2", {{opacity:0, scaleY:0.2}}, {{opacity:1, scaleY:1, duration:0.35, ease:"power3.out"}}, {A + 0.5:.2f});'); S("soft/thump.wav", A + 0.55, 0.8)
du = words("du", [("سَوُّوا", ""), ("صُفُوفَكُمْ", "gold")], A + 0.9, gap=0.35)
o0 = t + 0.3
for i in range(3): pop(f"#op{i}", o0 + i * 0.25, 0.8, "ref/tap.wav", 0.6)
c0 = o0 + 1.1
for k, nm in enumerate(("3", "2", "1")):
    T(f'tl.set("#cd", {{textContent:"{nm}", opacity:1}}, {c0 + k:.2f});'); T(f'tl.fromTo("#cd", {{scale:1.4}}, {{scale:1, duration:0.35, ease:"power3.out"}}, {c0 + k:.2f});')
    S("ref/click.wav", c0 + k, 1.0)
AN = c0 + 3
T(f'tl.to("#cd", {{opacity:0, duration:0.2, ease:"power2.in"}}, {AN - 0.1:.2f});')
T(f'tl.to("#op2", {{backgroundColor:"{GOLD}", color:"{INK}", scale:1.06, duration:0.35, ease:"back.out(1.4)"}}, {AN:.2f});'); S("ref/click-x2.wav", AN, 1.0); S("soft/shimmer.wav", AN, 0.4)
T(f'tl.to(["#op0", "#op1"], {{opacity:0.3, duration:0.3, ease:"power2.in"}}, {AN:.2f});')
an, t = typed("p5a", [("Rows", "em"), (": “Straighten your rows.” صَفّ is a row.", None)], AN + 0.4)
pop("#src", AN + 0.5, 0.6, None)
body.append(f"""<div class="sc" id="s6"><div class="hdw">{h}</div><div class="tx sm" style="top:560px">{b}</div>
 <div id="box2"><div class="du">{du}</div>
  {''.join(f'<div class="op2" id="op{i}">{x}</div>' for i, x in enumerate(("your hands", "your backs", "your rows")))}
  <div class="ans">{an}</div><div id="src">AL-BUKHĀRĪ 723</div></div><div id="cd">3</div></div>""")

# ---- the end ---------------------------------------------------------------------------------------------------------------------
t7 = wipe(t + 2.2, TEAL); scene("s6", t6, t7); A = t7 + 0.25
e1, t = typed("e1", [("Which word should", None), ("", "br"), ("we ", None), ("trace", "em"), (" next?", None)], A, rate=0.04, tick=2)
pop("#logo", A, 0.6, "soft/tick-lo.wav")
pop("#site", t + 0.2, 0.4, "ref/click-x2.wav"); S("soft/thump.wav", t + 0.2, 0.7)
e2, t = typed("e2", [("Comment it.", None)], t + 0.9, rate=0.03)
scene("s7", t7, END)
END = round(t + 1.6, 2)
body.append(f'''<div class="sc" id="s7"><div id="logo"><span class="tile"><span>ر</span><em></em></span><b>رَفِيق</b></div>
 <div class="tx big" style="top:520px;font-size:76px">{e1}</div><div id="site">rafiq-arabic.com</div><div class="tx sm" style="top:1080px">{e2}</div></div>''')

# ---- sounds: one track, mixed here, plus a low room tone under it ---------------------------------------------------------------
def load(f):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(SFX, f), "-f", "s16le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True).stdout, np.int16)
    return x.reshape(-1, 2).astype(np.float32) / 32768
def mix(path):
    n = int(END * SR); out = np.zeros((n, 2), np.float32); cache = {}
    room = load("soft/drone.wav"); reps = int(np.ceil(n / len(room))) + 1
    tone = np.concatenate([room] * reps)[:n] * 0.06
    fade = np.minimum(1, np.minimum(np.arange(n) / (0.8 * SR), (n - np.arange(n)) / (0.6 * SR)))[:, None]
    out += tone * fade
    for f, t, g in snd:
        if f not in cache:
            x = load(f)
            if f == "soft/shimmer.wav": x = x[:int(1.2 * SR)] * np.linspace(1, 0, int(1.2 * SR))[:, None] ** 2
            cache[f] = x / (np.abs(x).max() + 1e-9)
        x = cache[f] * g; i = int(t * SR); j = min(n, i + len(x))
        if i < n: out[i:j] += x[:j - i]
    out *= 0.89 / np.abs(out).max()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", path], input=out.tobytes(), check=True)

def build():
    out = os.path.join(HERE, "out", "v"); a = os.path.join(out, "assets")
    if os.path.exists(out): shutil.rmtree(out)
    os.makedirs(a)
    for f in ("karla-latin-500-normal.woff2", "karla-latin-700-normal.woff2", "jetbrains-mono-latin-500-normal.woff2", "ibm-plex-sans-arabic-arabic-700-normal.woff2"): shutil.copy(os.path.join(V6, "fonts", f), a)
    for f in ("playfair-display-latin-700-normal.woff2", "playfair-display-latin-700-italic.woff2", "playfair-display-latin-500-italic.woff2"): shutil.copy(os.path.join(ROOT, "brag-quiz/fonts", f), a); shutil.copy(os.path.join(V6, "lib/gsap.min.js"), a)
    mix(os.path.join(a, "sfx.wav"))
    css = f"""
@font-face {{ font-family:"KA"; src:url("assets/karla-latin-500-normal.woff2"); font-weight:500; }}
@font-face {{ font-family:"KA"; src:url("assets/karla-latin-700-normal.woff2"); font-weight:700; }}
@font-face {{ font-family:"MO"; src:url("assets/jetbrains-mono-latin-500-normal.woff2"); }}
@font-face {{ font-family:"SE"; src:url("assets/playfair-display-latin-700-normal.woff2"); font-weight:700; }}
@font-face {{ font-family:"SE"; src:url("assets/playfair-display-latin-700-italic.woff2"); font-weight:700; font-style:italic; }}
@font-face {{ font-family:"SE"; src:url("assets/playfair-display-latin-500-italic.woff2"); font-weight:500; font-style:italic; }}
@font-face {{ font-family:"AR"; src:url("assets/ibm-plex-sans-arabic-arabic-700-normal.woff2"); }}
* {{ margin:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:{INK}; color:{CREAM}; font-family:SE; font-weight:700; font-variant-numeric:lining-nums; }}
#wall {{ position:absolute; inset:0 0 auto 0; height:1180px; background:
  linear-gradient(rgba(241,236,224,.035) 2px, transparent 2px) 0 0/90px 90px, linear-gradient(90deg, rgba(241,236,224,.035) 2px, transparent 2px) 0 0/90px 90px,
  radial-gradient(ellipse at 50% 60%, #22393f 0%, {INK} 75%); }}
#floorw {{ position:absolute; left:0; right:0; top:1180px; bottom:0; perspective:700px; perspective-origin:50% 0; overflow:hidden; }}
#floor {{ position:absolute; left:-1400px; right:-1400px; top:0; height:2600px; transform:rotateX(68deg); transform-origin:50% 0;
  background:repeating-conic-gradient(#245a4e 0 25%, #1a3d37 0 50%) 0 0/180px 180px; }}
#floorw::after {{ content:""; position:absolute; inset:0; background:linear-gradient({INK} 0%, rgba(23,38,43,.2) 30%, rgba(23,38,43,.55) 100%); }}
.sc {{ position:absolute; inset:0; opacity:0; }}
.tx {{ position:absolute; left:70px; right:70px; text-align:center; font-size:62px; line-height:1.25; }}
.tx.big {{ font-size:90px; line-height:1.12; }} .tx.sm {{ font-size:54px; font-weight:700; line-height:1.3; color:#dfe6e3; }}
.ch {{ opacity:0; }} #title .ch, #title {{ opacity:1; }} #title {{ opacity:0; }}
em {{ font-family:SE; font-style:italic; font-weight:700; color:{GOLD}; }}
#hook em {{ border-bottom:3px solid {GOLD}; }}
.num {{ position:absolute; top:330px; left:0; right:0; text-align:center; font-family:MO; font-size:34px; letter-spacing:.3em; color:#8fb3a9; opacity:0; }}
.hdw .hd, .hd {{ position:absolute; top:390px; left:60px; right:60px; text-align:center; font-size:96px; line-height:1.05; }}
#fan {{ position:absolute; left:0; right:0; top:860px; height:400px; }}
.card {{ position:absolute; left:450px; top:0; width:180px; height:250px; border-radius:20px; transform-origin:50% 230%; border:5px solid {INK};
  display:flex; flex-direction:column; align-items:center; justify-content:space-around; padding:14px 0 30px; box-shadow:0 18px 30px rgba(0,0,0,.45); opacity:0; }}
.card span {{ font-family:SE; font-style:italic; font-size:70px; font-weight:700; line-height:1; }} #cd2 {{ z-index:2; }}
#spark i {{ position:absolute; width:16px; height:16px; border-radius:50%; background:{GOLD}; opacity:0; }}
.fig {{ position:absolute; top:960px; width:100px; height:250px; }}
.fig i {{ position:absolute; left:22px; top:0; width:56px; height:56px; border-radius:50%; background:{BONE}; }}
.fig b {{ position:absolute; left:10px; top:66px; width:80px; height:184px; border-radius:40px 40px 10px 10px; background:{BONE}; }}
.obj {{ position:absolute; opacity:0; }}
#board {{ padding:28px 34px; border-radius:14px; background:#0f1a1d; border:8px solid {GOLD}; font-family:SE; font-style:italic; font-weight:700; font-size:62px; color:{CREAM}; }}
.book {{ width:240px; height:170px; }} .book > i {{ position:absolute; top:20px; width:116px; height:150px; background:{BONE}; border:6px solid {INK};
  background-image:repeating-linear-gradient(transparent 0 26px, rgba(23,38,43,.5) 26px 31px); background-position:0 30px; }}
.book > i:nth-of-type(1) {{ left:2px; border-radius:12px 2px 2px 12px; transform:skewY(6deg); }} .book > i:nth-of-type(2) {{ left:122px; border-radius:2px 12px 12px 2px; transform:skewY(-6deg); }}
#rays1, #rays2 {{ position:absolute; left:120px; top:90px; }} #rays1 i, #rays2 i {{ position:absolute; left:-4px; top:-30px; width:8px; height:56px; border-radius:4px; background:{BONE}; transform-origin:50% 100%; opacity:0; }}
.ar {{ position:absolute; left:0; right:0; text-align:center; font-family:AR; font-size:150px; color:{GOLD}; direction:rtl; }} .ar.sm {{ font-size:70px; color:{CREAM}; }}
#jabr, #ktitle {{ opacity:0; }}
.eq {{ position:absolute; top:715px; left:0; right:0; text-align:center; font-family:SE; font-style:italic; font-weight:700; font-size:104px; color:{CREAM}; opacity:0; }}
.eq.gold {{ color:{GOLD}; font-size:130px; }}
#dia {{ position:absolute; left:215px; top:880px; width:650px; height:400px; }}
.blk {{ position:absolute; display:grid; place-items:center; background:{TEAL}; color:{CREAM}; border:5px solid {INK}; font-family:SE; font-style:italic; font-weight:700; font-size:58px; border-radius:6px; opacity:0; }}
#sq {{ background:{CREAM}; color:{INK}; }} .blk.dash {{ background:transparent; border:5px dashed {GOLD}; }} .blk.dash b {{ font-family:SE; font-weight:700; font-size:84px; color:{INK}; opacity:0; }}
.eight {{ position:absolute; font-family:SE; font-style:italic; font-size:72px; color:{GOLD}; font-weight:700; opacity:0; }}
.step {{ position:absolute; top:1320px; left:60px; right:60px; text-align:center; font-size:54px; font-weight:700; line-height:1.2; }}
#ms {{ position:absolute; left:290px; top:900px; width:500px; height:300px; border-radius:14px; background:{CREAM}; box-shadow:0 20px 40px rgba(0,0,0,.5); opacity:0; }}
#ms .ar {{ top:40px; font-size:130px; color:{MAR}; }} #ms .la {{ position:absolute; top:70px; left:0; right:0; text-align:center; font-family:SE; font-style:italic; font-weight:700; font-size:120px; color:{MAR}; opacity:0; }}
#ms small {{ position:absolute; bottom:22px; left:0; right:0; text-align:center; font-family:SE; font-style:italic; font-weight:500; font-size:32px; color:#5c6e70; }}
#sign {{ position:absolute; left:340px; top:1220px; width:400px; transform-origin:50% 0; opacity:0; }} .rope {{ margin:0 auto; width:8px; height:50px; background:{BONE}; }}
.plate {{ padding:18px 0 10px; border-radius:16px; background:{CREAM}; border:6px solid {INK}; text-align:center; font-size:52px; color:{TEAL}; letter-spacing:.04em; font-family:KA; }}
#box {{ position:absolute; left:70px; right:70px; top:720px; padding:30px 40px 40px; border-radius:18px; background:#0f1a1d; border:3px solid {TEAL}; opacity:0; transform-origin:50% 0; }}
.du {{ text-align:center; direction:rtl; font-family:AR; font-size:74px; line-height:1.6; }} .aw {{ display:inline-block; opacity:0; }} .aw.gold {{ color:{GOLD}; }}
.tr {{ margin-top:24px; text-align:center; font-size:52px; font-weight:700; line-height:1.3; }}
#src {{ margin:30px auto 0; width:max-content; padding:10px 26px; border-radius:30px; background:{MAR}; font-family:MO; font-size:28px; letter-spacing:.12em; color:{GOLD}; opacity:0; }}
#logo {{ position:absolute; top:330px; left:0; right:0; display:flex; justify-content:center; align-items:center; gap:18px; opacity:0; }}
#logo .tile {{ position:relative; width:84px; height:84px; border-radius:22px; background:{CREAM}; display:grid; place-items:center; }}
#logo .tile span {{ font-family:AR; font-size:52px; color:{INK}; margin-top:-6px; }} #logo .tile em {{ position:absolute; right:13px; top:12px; width:13px; height:13px; border-radius:50%; background:{GOLD}; }}
#logo b {{ font-family:AR; font-size:64px; }}
#site {{ position:absolute; top:860px; left:50%; margin-left:-340px; width:680px; font-family:KA; padding:24px 0; text-align:center; border-radius:60px; background:{GOLD}; color:{INK}; font-size:58px; opacity:0; }}
.tagp {{ display:inline-block; padding:8px 30px; border-radius:40px; background:{CREAM}; color:{MAR}; font-size:56px; box-shadow:0 12px 24px rgba(0,0,0,.4); }}
.tagp.tar {{ font-family:AR; direction:rtl; }}
#stars2 i {{ position:absolute; width:14px; height:14px; border-radius:50%; background:#fff6d8; opacity:0; }}
.bean {{ position:absolute; top:980px; width:34px; height:46px; border-radius:50%; background:#6B4226; border:4px solid {INK}; opacity:0; }}
#map {{ position:absolute; left:70px; top:850px; width:940px; height:680px; border-radius:24px; background:#0f1a1d; border:3px solid {TEAL}; overflow:hidden; opacity:0; transform-origin:50% 0; }}
#map text {{ font-family:KA; font-weight:700; font-size:40px; fill:{CREAM}; }}
#chain {{ position:absolute; left:0; right:0; top:800px; text-align:center; }}
.wc {{ display:block; width:max-content; margin:0 auto; padding:6px 44px; border-radius:60px; background:{CREAM}; color:{INK}; font-family:SE; font-style:italic; font-size:76px; line-height:1.3; opacity:0; }}
.wc.wa {{ font-family:AR; direction:rtl; font-style:normal; color:{MAR}; font-size:66px; line-height:1.6; }} #ch3 {{ background:{GOLD}; font-size:110px; }}
.arw {{ font-family:KA; font-size:50px; color:{GOLD}; line-height:70px; height:70px; opacity:0; }}
.aw2 {{ text-align:center; font-family:AR; font-size:120px; line-height:1.4; direction:rtl; opacity:0; }}
#mq {{ margin-top:-30px; }}
.op2 {{ width:600px; margin:16px auto 0; padding:14px; border-radius:40px; background:#22393f; text-align:center; font-family:KA; font-size:48px; color:{CREAM}; opacity:0; }}
.ans {{ margin-top:30px; text-align:center; font-size:56px; }}
#cd {{ position:absolute; left:0; right:0; top:1330px; text-align:center; font-size:130px; color:{GOLD}; opacity:0; }}
.lg {{ font-family:MO; font-size:30px; letter-spacing:.2em; color:#8fb3a9; text-transform:uppercase; margin-top:6px; opacity:0; }}
#dawnbox {{ position:absolute; left:70px; top:820px; width:940px; height:620px; border-radius:24px; overflow:hidden; background:#0f1a1d; border:3px solid {TEAL}; }}
#sky {{ position:absolute; inset:0; background:linear-gradient(#2a4a6b 0%, #e9a35a 70%, {GOLD} 100%); opacity:0; }}
#sun {{ position:absolute; left:380px; top:330px; width:180px; height:180px; border-radius:50%; background:#FFD27A; box-shadow:0 0 80px 30px rgba(255,200,110,.55); }}
.cl {{ position:absolute; top:150px; width:360px; height:150px; border-radius:80px; background:#3a4f57; box-shadow:60px 40px 0 -10px #33474f; }}
#hzn {{ position:absolute; left:0; right:0; top:450px; bottom:0; background:#1a3d37; border-top:6px solid #245a4e; }}
#lets {{ position:absolute; left:0; right:0; top:470px; text-align:center; direction:rtl; }} .lt {{ position:relative; display:inline-block; font-family:AR; font-size:110px; color:{CREAM}; margin:0 26px; }}
#lets {{ position:absolute; left:0; right:0; top:820px; text-align:center; direction:rtl; }} .lt {{ position:relative; display:inline-block; font-family:AR; font-size:150px; color:{GOLD}; margin:0 30px; }}
.lg2 {{ text-align:center; font-family:SE; font-style:italic; font-weight:500; font-size:40px; color:#8fb3a9; margin-top:-10px; }}
#box2 {{ position:absolute; left:70px; right:70px; top:830px; padding:30px 40px 40px; border-radius:18px; background:#0f1a1d; border:3px solid {TEAL}; opacity:0; transform-origin:50% 0; }}
#box2 .du {{ font-size:64px; }}
.wipe {{ position:absolute; inset:0; z-index:50; transform:translateX(1100px); }}
"""
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><title>sofa-silent</title>
<script src="assets/gsap.min.js"></script><style>{css}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{END}">
<div id="wall"></div><div id="floorw"><div id="floor"></div></div>
{chr(10).join(body)}
{chr(10).join(WIPES)}
<audio id="fx" src="assets/sfx.wav" data-start="0" data-duration="{END}" data-volume="1" data-track-index="1"></audio>
</div><script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;</script></body></html>
""")
    print("built", END, "s,", len(snd), "sounds")

if __name__ == "__main__":
    build()
