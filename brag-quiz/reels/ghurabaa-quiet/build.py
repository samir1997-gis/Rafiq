#!/usr/bin/env python3
"""The strangers video, no voice (owner, 20 Oct 2026; #269), in the style of a reference reel the owner sent (analysed 20 Oct):
dark page, a short italic serif headline per beat whose words arrive left to right from blur; a glowing card in the middle; text that
types in with a cursor; list lines and tiles that tick in; a highlight that hops across a grid and lands; bubbles that stack; one big
gold reveal that materialises over the fading scene, small lines under it. Scenes change by a blur cross-fade (no camera moves).
Sound, measured on the reference's music-only stem: a quiet bed (~40 dB down), one soft airy whoosh per scene change, tiny pitched
ticks per thing that appears, typing clicks, one low thump on the big reveal; all well under where a voice would sit.
Our colours: ink #17262B, cream, gold, rubric red. Sounds: brag-quiz/sfx/soft/ (made for this, not copied).

  python3 brag-quiz/reels/ghurabaa-quiet/build.py   then  cd brag-quiz/reels/ghurabaa-quiet/out/v && npx hyperframes render -o ../quiet.mp4
"""
import os, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
V6 = os.path.join(ROOT, "brag-output-v6/composition/assets")
INK, CREAM, GOLD, GOLD2, RED, TEAL = "#17262b", "#f1ece0", "#a8842c", "#E9B949", "#c8473d", "#2e7263"
END = 31.0

def build():
    out = os.path.join(HERE, "out", "v"); a = os.path.join(out, "assets")
    if os.path.exists(out): shutil.rmtree(out)
    os.makedirs(a)
    for f in ("ibm-plex-sans-arabic-arabic-700-normal.woff2", "karla-latin-500-normal.woff2", "karla-latin-700-normal.woff2"): shutil.copy(os.path.join(V6, "fonts", f), a)
    shutil.copy(os.path.join(ROOT, "brag-quiz/fonts/instrument-serif-latin-400-normal.woff2"), a); shutil.copy(os.path.join(V6, "lib/gsap.min.js"), a)
    for f in os.listdir(os.path.join(ROOT, "brag-quiz/sfx/soft")): shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/soft", f), a)
    src = os.path.join(V6, "sfx-gen/fountain.mp3")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", src, "-af", f"volume=6dB,atrim=0:{END + .3},afade=t=in:d=0.3,afade=t=out:st={END - 1.5}:d=1.5",
                    "-c:a", "libmp3lame", "-q:a", "3", os.path.join(a, "fountain.mp3")], check=True)
    au = [f'<audio id="bed" src="assets/fountain.mp3" data-start="0" data-duration="{END}" data-volume="0.1" data-track-index="1"></audio>']
    VOL = {"whoosh.wav": .38, "tick.wav": .16, "tick-lo.wav": .16, "type.wav": .07, "count.wav": .06, "thump.wav": .55}
    LEN = {"whoosh.wav": .55, "tick.wav": .05, "tick-lo.wav": .05, "type.wav": .025, "count.wav": .03, "thump.wav": .7}
    def fx(name, t0, k=1.0): au.append(f'<audio id="s{len(au)}" src="assets/{name}" data-start="{max(0, t0):.3f}" data-duration="{LEN[name]}" data-volume="{VOL[name] * k:.3f}" data-track-index="{2 + len(au) % 6}"></audio>')
    js = []
    def T(s): js.append(s)
    def head(sid, words, t0, gap=0.11):                         # the headline: words arrive left to right, each from blur
        T(f'tl.fromTo("#{sid} .hw", {{opacity:0, y:10, filter:"blur(12px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.5, ease:"power2.out", stagger:{gap}}}, {t0:.2f});')
    def scene_out(sid, t0):                                      # blur cross-fade out, with the whoosh
        T(f'tl.to("#{sid}", {{opacity:0, filter:"blur(16px)", scale:0.985, duration:0.55, ease:"power2.in"}}, {t0:.2f});'); fx("whoosh.wav", t0 - 0.1)
    def scene_in(sid, t0): T(f'tl.fromTo("#{sid}", {{opacity:0, filter:"blur(16px)"}}, {{opacity:1, filter:"blur(0px)", duration:0.55, ease:"power2.out"}}, {t0:.2f});')
    def rise(sel, t0, snd="tick.wav", d=0.42):                  # a line, tile or bubble ticks in
        T(f'tl.fromTo("{sel}", {{opacity:0, y:24, filter:"blur(8px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:{d}, ease:"power3.out"}}, {t0:.2f});')
        if snd: fx(snd, t0 + 0.02)
    def typed(sel, text, t0, cps=22, snd=True):                  # types in with a cursor, a soft click every few letters
        n = len(text); d = n / cps
        T(f'(() => {{ const o = {{n:0}}, el = document.querySelector("{sel}"); tl.to(o, {{n:{n}, duration:{d:.2f}, ease:"none", onUpdate:() => {{ el.textContent = {text!r}.slice(0, Math.round(o.n)); }}}}, {t0:.2f}); }})();')
        if snd:
            for k in range(0, n, 3): fx("type.wav", t0 + k / cps, 0.8 + 0.4 * ((k * 7) % 5) / 5)
        return t0 + d
    words = lambda sid, s: f'<div class="head" id="{sid}h">' + " ".join(f'<span class="hw">{w}</span>' for w in s.split()) + "</div>"

    # 1 · the hook (frame 0, the cover): the headline is whole from the first frame; the glowing card with the word; the line under it
    T(f'tl.fromTo("#card1", {{boxShadow:"0 0 0px 0px rgba(233,185,73,.0)"}}, {{boxShadow:"0 0 70px 6px rgba(233,185,73,.35)", duration:1.2, yoyo:true, repeat:2, ease:"sine.inOut"}}, 0);')
    T('tl.fromTo("#c1w", {scale:1.08}, {scale:1, duration:3.2, ease:"power2.out"}, 0);')
    T('tl.fromTo("#sub1 .hw", {opacity:0, y:10, filter:"blur(10px)"}, {opacity:1, y:0, filter:"blur(0px)", duration:0.5, stagger:0.12, ease:"power2.out"}, 1.3);')
    for k in range(9): fx("count.wav", 1.32 + 0.12 * k, 0.8)
    # 2 · the hadith: the card types the Arabic, then four English lines tick in, then the source checks
    scene_out("s1", 4.0); scene_in("s2", 4.35); head("s2h", "", 4.4)
    t = typed("#ar2", "بَدَأَ الإِسْلامُ غَرِيبًا، وَسَيَعُودُ كَما بَدَأَ غَرِيبًا، فَطُوبى لِلْغُرَباءِ", 5.0, 34)
    for k, t0 in enumerate([t + 0.25, t + 0.7, t + 1.15, t + 1.6]): rise(f"#l{k}", t0)
    T(f'tl.fromTo("#chk", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.4, ease:"power3.out"}}, {t + 2.2:.2f});')
    T(f'tl.fromTo("#tickmark", {{scale:0, rotation:-30}}, {{scale:1, rotation:0, duration:0.45, ease:"back.out(3)"}}, {t + 2.45:.2f});'); fx("tick-lo.wav", t + 2.45); fx("tick.wav", t + 2.52)
    # 3 · the last word: the hadith's words as tiles, a highlight hops across and lands on لِلْغُرَباءِ
    s3 = t + 3.6; scene_out("s2", s3 - 0.35); scene_in("s3", s3); head("s3h", "", s3 + 0.05)
    for k in range(9): rise(f"#g{k}", s3 + 0.5 + 0.075 * k, "tick.wav" if k % 2 == 0 else "tick-lo.wav", 0.35)
    hops = [0, 3, 6, 8]; h0 = s3 + 1.6
    for i, k in enumerate(hops):
        T(f'tl.to("#hl", {{left:() => document.getElementById("g{k}").offsetLeft - 8, top:() => document.getElementById("g{k}").offsetTop - 8, opacity:1, duration:{0.01 if i == 0 else 0.32}, ease:"power3.inOut"}}, {h0 + 0.42 * i:.2f});')
        fx("tick-lo.wav" if i < len(hops) - 1 else "tick.wav", h0 + 0.42 * i + 0.25)
    land = h0 + 0.42 * (len(hops) - 1) + 0.3
    T(f'tl.to("#g8", {{scale:1.12, background:"{GOLD2}", color:"{INK}", duration:0.3, ease:"back.out(2)"}}, {land:.2f});')
    T(f'tl.to("#hl", {{scale:1.12, borderColor:"{GOLD2}", duration:0.3, ease:"back.out(2)"}}, {land:.2f});')
    # 4 · what it means: the word in a card, three bubbles stack
    s4 = land + 1.5; scene_out("s3", s4 - 0.35); scene_in("s4", s4); head("s4h", "", s4 + 0.05)
    rise("#w4", s4 + 0.6, "tick-lo.wav", 0.5)
    for k in range(3): rise(f"#b{k}", s4 + 1.7 + 1.1 * k)
    # 5 · the big reveal: THE ROOT, غ ر ب materialises in gold with a low thump, its family ticks in underneath
    s5 = s4 + 5.6; scene_out("s4", s5 - 0.3)
    T(f'tl.fromTo("#s5", {{opacity:0}}, {{opacity:1, duration:0.01}}, {s5:.2f});')
    T(f'tl.fromTo("#lab5", {{opacity:0, y:12}}, {{opacity:1, y:0, duration:0.4, ease:"power2.out"}}, {s5:.2f});')
    T(f'tl.fromTo("#root5", {{opacity:0, scale:1.25, filter:"blur(22px)"}}, {{opacity:1, scale:1, filter:"blur(0px)", duration:0.7, ease:"expo.out"}}, {s5 + 0.15:.2f});'); fx("thump.wav", s5 + 0.15)
    T(f'tl.fromTo("#mean5 .hw", {{opacity:0, y:10, filter:"blur(10px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.5, stagger:0.12, ease:"power2.out"}}, {s5 + 0.9:.2f});')
    for k in range(3): rise(f"#r{k}", s5 + 1.8 + 0.75 * k)
    # 6 · the end: Bukhari 6416 as the headline, then the ask in gold
    s6 = s5 + 5.0; scene_out("s5", s6 - 0.35); scene_in("s6", s6); head("s6h", "", s6 + 0.05, 0.1)
    T(f'tl.fromTo("#ref6", {{opacity:0}}, {{opacity:1, duration:0.5}}, {s6 + 1.4:.2f});')
    rise("#ask6", s6 + 2.6, "tick-lo.wav", 0.6)
    T(f'tl.fromTo("#arrow6", {{y:-14}}, {{y:14, duration:0.45, yoyo:true, repeat:9, ease:"sine.inOut"}}, {s6 + 3.0:.2f});'); rise("#arrow6", s6 + 3.0, "tick.wav")
    rise("#send6", s6 + 3.6, None)
    T(f'tl.fromTo("#grain", {{backgroundPosition:"0px 0px"}}, {{backgroundPosition:"0px 240px", duration:{END}, ease:"none"}}, 0);')

    HA = ["بَدَأَ", "الإِسْلامُ", "غَرِيبًا،", "وَسَيَعُودُ", "كَما بَدَأَ", "غَرِيبًا،", "فَطُوبى", "لِلْغُرَباءِ"]
    HA = HA[:4] + ["كَما", "بَدَأَ"] + HA[5:]
    body = f"""
<div id="grain"></div>
<section id="s1">{words("s1", "Islam is so strange.").replace('class="hw"', 'class="hw on"')}
  <div class="card" id="card1"><div id="c1w"><div class="lab">THE WORD</div><div class="ar big">غُرَباء</div><div class="tr">ghurabāʾ · strangers</div></div></div>
  <div class="sub" id="sub1">{" ".join(f'<span class="hw">{w}</span>' for w in "…and the Prophet (pbuh) told us it would be.".split())}</div></section>
<section id="s2">{words("s2", "The Prophet (pbuh) said:")}
  <div class="box" style="top:520px"><div class="lab">SAHIH MUSLIM 145</div><div class="ar typ" id="ar2"></div></div>
  <div class="box" style="top:930px"><div class="lab">IN ENGLISH</div>
    <div class="li" id="l0"><b>01</b> Islam began as something strange,</div><div class="li" id="l1"><b>02</b> and it will return to being strange</div>
    <div class="li" id="l2"><b>03</b> as it began.</div><div class="li" id="l3"><b>04</b> So glad tidings to the <i>strangers.</i></div></div>
  <div class="box row" id="chk" style="top:1470px"><div><div class="lab">SOURCE</div><div class="src">Sahih Muslim 145 · Kitab al-Iman</div></div><div id="tickmark">✓</div></div></section>
<section id="s3">{words("s3", "Look at the last word.")}
  <div id="grid">{"".join(f'<div class="tile" id="g{k}">{w}</div>' for k, w in enumerate(HA))}<div id="hl"></div></div></section>
<section id="s4">{words("s4", "It means strangers.")}
  <div class="card small" id="w4"><div class="ar mid">غُرَباء</div><div class="tr">ghurabāʾ</div></div>
  <div class="bub" id="b0" style="top:1040px">Just one stranger: <span class="ar in">غَرِيب</span></div>
  <div class="bub" id="b1" style="top:1230px">Its root: <span class="ar in red">غ ر ب</span> to go away</div>
  <div class="bub" id="b2" style="top:1420px">like the sun when it sets 🌅</div></section>
<section id="s5"><div class="lab big" id="lab5">THE ROOT</div><div class="ar huge" id="root5">غ ر ب</div>
  <div class="sub" id="mean5" style="top:900px">{" ".join(f'<span class="hw">{w}</span>' for w in "to go away".split())}</div>
  <div class="fam" id="r0" style="top:1120px"><span class="ar">الْمَغْرِب</span><span>Maghrib · <i>the sunset prayer</i></span></div>
  <div class="fam" id="r1" style="top:1300px"><span class="ar">غَرْب</span><span>gharb · <i>the west</i></span></div>
  <div class="fam" id="r2" style="top:1480px"><span class="ar">غُرْبَة</span><span>ghurba · <i>far from home</i></span></div></section>
<section id="s6">{words("s6", "“Be in this world as if you were a stranger or a traveller.”")}
  <div class="lab" id="ref6" style="position:absolute;left:0;right:0;top:760px;text-align:center">THE PROPHET (PBUH) · SAHIH AL-BUKHARI 6416</div>
  <div id="ask6">Are you one of<br>the <i>strangers?</i></div><div id="arrow6">👇</div>
  <div id="send6">Comment below · send this to someone who feels like a stranger</div></section>"""
    css = f"""
@font-face {{ font-family:"Ar"; src:url("assets/ibm-plex-sans-arabic-arabic-700-normal.woff2"); font-weight:700; }}
@font-face {{ font-family:"Karla"; src:url("assets/karla-latin-500-normal.woff2"); font-weight:500; }}
@font-face {{ font-family:"Karla"; src:url("assets/karla-latin-700-normal.woff2"); font-weight:700; }}
@font-face {{ font-family:"InstrumentSerif"; src:url("assets/instrument-serif-latin-400-normal.woff2"); }}
body {{ margin:0; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; color:{CREAM}; font-family:"Karla";
  background:radial-gradient(ellipse at 50% 18%, #24393f 0%, #17262b 45%, #0d1619 100%); }}
#grain {{ position:absolute; inset:-20px; opacity:.05; background-image:radial-gradient(rgba(255,255,255,.9) 1px, transparent 1.4px); background-size:6px 6px; }}
section {{ position:absolute; inset:0; opacity:0; }} #s1 {{ opacity:1; }}
i {{ font-family:"InstrumentSerif"; font-style:italic; font-weight:400; color:{GOLD2}; }}
.head {{ position:absolute; left:80px; right:80px; top:250px; text-align:center; font-family:"InstrumentSerif"; font-style:italic; font-size:96px; line-height:1.08; letter-spacing:-.015em; }}
.hw {{ display:inline-block; opacity:0; }} .hw.on {{ opacity:1; }}
.lab {{ font-weight:700; font-size:26px; letter-spacing:.22em; color:rgba(241,236,224,.55); }} .lab.big {{ position:absolute; left:0; right:0; top:420px; text-align:center; font-size:34px; color:{GOLD2}; }}
.ar {{ font-family:"Ar"; font-weight:700; direction:rtl; }}
.card {{ position:absolute; left:250px; width:580px; top:560px; height:760px; border-radius:46px; border:3px solid rgba(233,185,73,.75);
  background:linear-gradient(160deg, #22363c, #142125); display:flex; align-items:center; justify-content:center; text-align:center; }}
.card .lab {{ margin-bottom:30px; }} .ar.big {{ font-size:190px; line-height:1.3; color:{GOLD2}; }} .tr {{ font-size:34px; color:rgba(241,236,224,.7); margin-top:14px; letter-spacing:.04em; }}
.sub {{ position:absolute; left:60px; right:60px; top:1420px; text-align:center; font-family:"InstrumentSerif"; font-style:italic; font-size:56px; line-height:1.15; color:rgba(241,236,224,.85); }}
.box {{ position:absolute; left:70px; right:70px; border-radius:30px; background:rgba(241,236,224,.06); border:2px solid rgba(241,236,224,.10); padding:30px 38px; }}
.typ {{ font-size:66px; line-height:1.65; min-height:220px; margin-top:12px; }} .typ::after {{ content:"|"; color:{GOLD2}; font-family:"Karla"; font-weight:500; margin-right:6px; }}
.li {{ font-size:40px; line-height:1.55; opacity:0; }} .li b {{ color:{GOLD2}; font-size:30px; margin-right:16px; letter-spacing:.05em; }}
.li i {{ font-size:46px; }}
.row {{ display:flex; align-items:center; justify-content:space-between; opacity:0; }} .src {{ font-size:38px; margin-top:8px; }}
#tickmark {{ width:76px; height:76px; border-radius:50%; background:{TEAL}; color:{CREAM}; display:grid; place-items:center; font-size:46px; font-weight:700; }}
#grid {{ position:absolute; left:80px; right:80px; top:560px; display:flex; flex-wrap:wrap; flex-direction:row-reverse; justify-content:center; gap:26px; }}
.tile {{ position:relative; width:280px; height:200px; border-radius:30px; background:rgba(241,236,224,.07); border:2px solid rgba(241,236,224,.12);
  display:grid; place-items:center; font-family:"Ar"; font-weight:700; font-size:62px; direction:rtl; opacity:0; }}
#hl {{ position:absolute; width:296px; height:216px; border-radius:36px; border:5px solid rgba(241,236,224,.9); opacity:0; pointer-events:none; }}
.card.small {{ left:290px; width:500px; top:480px; height:460px; opacity:0; flex-direction:column; }} .ar.mid {{ font-size:150px; line-height:1.3; color:{GOLD2}; }}
.bub {{ position:absolute; left:110px; right:110px; border-radius:34px; background:#d9e9e3; color:{INK}; padding:30px 40px; font-size:44px; font-weight:700; line-height:1.3; opacity:0;
  box-shadow:0 18px 40px -20px rgba(0,0,0,.7); }} .bub .ar.in {{ font-size:54px; }} .bub .red {{ color:{RED}; letter-spacing:.1em; }}
.ar.huge {{ position:absolute; left:0; right:0; top:500px; text-align:center; font-size:300px; line-height:1.2; color:{GOLD2}; letter-spacing:.12em; text-shadow:0 0 60px rgba(233,185,73,.35); }}
.fam {{ position:absolute; left:110px; right:110px; display:flex; align-items:center; justify-content:space-between; padding:18px 36px; border-radius:26px;
  background:rgba(241,236,224,.06); font-size:40px; opacity:0; }} .fam .ar {{ font-size:70px; line-height:1.4; color:{GOLD2}; }} .fam i {{ color:rgba(241,236,224,.75); }}
#s6 .head {{ top:330px; font-size:88px; }}
#ask6 {{ position:absolute; left:60px; right:60px; top:960px; text-align:center; font-family:"InstrumentSerif"; font-size:130px; line-height:1.0; letter-spacing:-.02em; opacity:0; }}
#arrow6 {{ position:absolute; left:0; right:0; top:1260px; text-align:center; font-size:110px; opacity:0; }}
#send6 {{ position:absolute; left:130px; right:130px; top:1450px; text-align:center; font-size:38px; font-weight:700; line-height:1.3; color:rgba(241,236,224,.8);
  border:2px solid rgba(241,236,224,.35); border-radius:50px; padding:24px 30px; opacity:0; }}
"""
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><title>ghurabaa-quiet</title>
<script src="assets/gsap.min.js"></script><style>{css}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{END}">
{body}
{chr(10).join(au)}
</div><script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;</script></body></html>
""")
    print("built", END, "s, scenes at", round(s3, 2), round(s4, 2), round(s5, 2), round(s6, 2), "sounds", len(au) - 1)

if __name__ == "__main__":
    build()
