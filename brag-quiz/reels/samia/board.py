import os
from playwright.sync_api import sync_playwright
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# word sequence of a 4-rakah prayer (lengths from salah-data.js), 'r' = the two rising lines
def rakah(first, sit, last):
    s = [("t",2)] + ([("o",15)] if first else []) + [("f",30),("t",2),("k",9),("r",7),("t",2),("s",9),("t",2),("g",3),("t",2),("s",9)]
    if sit: s += [("t",2),("h",28)]
    if last: s += [("w",34),("x",8)]
    return s
seq = rakah(1,0,0)+rakah(0,1,0)+rakah(0,0,0)+rakah(0,1,1)
cells = "".join(f'<i class="{"g" if k=="r" else ""}"></i>' * n for k, n in seq); N = sum(n for _, n in seq)
cap = lambda html, top=1290: f'<div class="cap" style="top:{top}px">{html}</div>'
em = lambda w: f'<b>{w}</b>'
F = {}
F["01-hook"] = f'''<div class="red"><div class="inset"><img src="a/sp2.png" style="object-position:50% 30%;transform:scale(1.5);filter:grayscale(1) contrast(1.3)"><div class="shade"></div></div>
<div class="flab">17 TIMES A DAY</div>{cap("every time you stand<br>up from "+em("RUKU"),1500)}<div class="flash"></div></div>'''
F["02-title"] = f'''<img class="bg" src="a/sp1.png"><div class="small" style="top:150px">YOU'RE HAVING A</div><div class="big" style="top:240px;font-size:160px">CONVERSATION</div>
<img class="bg person" src="a/sp1.png" style="-webkit-mask-image:url(a/m1.png);mask-image:url(a/m1.png);mask-mode:luminance">{cap("you're having a "+em("CONVERSATION"))}'''
w1 = [("سَمِعَ","hears",1),("اللَّهُ","Allah",0),("لِمَنْ","the one who",0),("حَمِدَهُ","praises Him",0)]
F["03-words"] = f'''<div class="ink" style="height:1130px"><div class="lab" style="top:120px">RISING FROM RUKU · YOU SAY</div>
<div class="ww">{"".join(f'<div class="w{" on" if o else ""}"><span class="ar">{a}</span><span>{e}</span></div>' for a,e,o in w1)}</div>
<div class="tr">“Allah hears the one who praises Him.”</div></div>
<div class="strip" style="top:1130px;height:790px"><img src="a/sp2.png" style="object-position:50% 35%"></div>{cap("Allah "+em("HEARS")+"<br>the one who praises Him",1200)}'''
F["04-chat"] = '''<div class="paper"><div class="lab" style="top:150px;color:#B4322A">THE CONVERSATION</div>
<div class="bub l"><div class="when">rising</div><div class="ar">سَمِعَ اللَّهُ لِمَنْ حَمِدَهُ</div><div class="en">Allah hears the one who praises Him.</div></div>
<div class="bub r"><div class="when">standing straight</div><div class="ar">رَبَّنا وَلَكَ الْحَمْدُ</div><div class="en">Our Lord, and to You belongs all praise.</div></div>
<div class="pip"><img src="a/sp3.png"></div></div>'''
F["05-wall"] = f'''<div class="ink"><div class="lab" style="top:130px">EVERY WORD OF A 4-RAKAH PRAYER</div><div class="wall">{cells}</div>
<div class="stat" style="top:1300px">1 IN 15</div><div class="sub" style="top:1600px">of the words you say are these two lines<br><small>{N} words · 28 of them · not counting the surah you add</small></div></div>'''
pr = [("FAJR",2),("DHUHR",4),("ASR",4),("MAGHRIB",3),("ISHA",4)]
F["06-count"] = f'''<div class="ink"><div class="lab" style="top:150px">ONCE EVERY RAKAH</div>
<div class="days">{"".join(f'<div class="d"><div class="dots">{"<i></i>"*n}</div><div class="dn">{p}</div></div>' for p,n in pr)}</div>
<div class="stat" style="top:960px;color:#C8372D;font-size:330px">17×</div><div class="sub" style="top:1400px">a day, every day</div>
<div class="stat" style="top:1560px;font-size:150px">6,205 A YEAR</div></div>'''
F["07-split"] = f'''<div class="split"><div class="s" style="top:0"><div class="ph">B-ROLL: YOU RISING FROM RUKU<br><small>side-on, low light, 2-3 s</small></div></div>
<div class="s" style="top:648px"><img src="a/parts.png" style="object-position:50% 84%;filter:grayscale(1) brightness(.35) contrast(1.3)"></div>
<div class="s" style="top:1296px"><img src="a/sp1.png" style="object-position:50% 40%;filter:brightness(.6)"></div></div>{cap("just "+em("7 WORDS")+", 17 times a day",920)}'''
F["08-root"] = f'''<img class="bg" src="a/sp3.png"><div class="small" style="top:150px">PRAISE · 21× IN ONE PRAYER</div><div class="big ar" style="top:270px;font-size:300px;letter-spacing:40px">ح م د</div>
<img class="bg person" src="a/sp3.png" style="-webkit-mask-image:url(a/m3.png);mask-image:url(a/m3.png);mask-mode:luminance">{cap("even "+em("MUHAMMAD")+"<br>means the praised one",1230)}'''
F["09-end"] = f'''<div class="red"><div class="inset"><img src="a/parts.png" style="object-position:50% 50%"><div class="shade"></div></div><div class="flab" style="font-size:260px;top:200px">RAFIQ</div>
{cap("learn every word<br>you say in "+em("SALAH"),1500)}</div>'''
css = open("board.css").read()
html = f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>' + "".join(f'<div class="fr" id="f{k}">{v}</div>' for k, v in F.items()) + "</body></html>"
open("board.html", "w").write(html)
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome"); p = b.new_page(viewport={"width": 1080, "height": 1920})
    p.goto("file://" + os.path.abspath("board.html")); p.evaluate("document.fonts.ready"); p.wait_for_timeout(800)
    os.makedirs("out", exist_ok=True)
    for k in F: p.locator(f"#f{k}").screenshot(path=f"out/{k}.png")
    b.close()
print(N, "words")
