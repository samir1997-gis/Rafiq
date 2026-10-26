#!/usr/bin/env python3
"""The chalkboard ad (owner, 26 Oct 2026, #295): how Rafiq makes studying Arabic easy and how soon you improve, chalk written and
drawn on a blackboard as Callum explains (the standard: his voice, the hook word shouted and slammed on with a crash and a shake,
words arriving one at a time, numbers counting with a click on every step, Rafiq's Arabic level with Callum, the comment ask heard
in full, the fountain bed, -16 LUFS). Six boards, each wiped with a duster before the next:
  1 "TEN minutes a day": TEN on frame 0, circled · 2 "you've heard Arabic takes years… grammar first": YEARS? over a grammar table,
  crossed out · 3 "your first week: the 20 words you say most in salah… more than half of every four-rakʿah prayer": 20 counting, a pie
  filling past half · 4 "every word comes with audio and a picture… back just before you'd forget": the سُبْحانَ card (the app's
  recording), a memory curve topped up by reviews · 5 "then you keep going": the list, 785 and 36 counting · 6 "10 minutes a day, free
  for 7 days, no card", rafiq-arabic.com, the comment ask.
Claims are the site's and the app's own (index.html; the 20 words = over half of a four-rakʿah prayer before the surah: salah-data.js).

  python3 brag-quiz/reels/chalkboard/build.py   then  cd brag-quiz/reels/chalkboard/out/v && npx hyperframes render -o ../chalkboard-raw.mp4
"""
import json, os, re, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
V6 = os.path.join(ROOT, "brag-output-v6/composition/assets"); VO = os.path.join(ROOT, "brag-quiz/voice/chalkboard")
CHALK, GOLD, PINK, BOARD = "#f2efe6", "#f3d27a", "#ef8f86", "#1f3a30"
dur = lambda f: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
words = lambda n: json.load(open(os.path.join(VO, n + ".words.json")))
WORD = os.path.join(ROOT, "audio", "1l7mydd.mp3")                      # the app's own سُبْحانَ (salah, ruku)
GAP = {"k2": 0.05, "k3": 0.45, "k4": 0.45, "k5": 0.4, "k6": 0.4, "k7": 0.45}
L = {"k1": 0.35}
for n in GAP: p = f"k{int(n[1]) - 1}"; L[n] = round(L[p] + dur(os.path.join(VO, p + ".mp3")) + GAP[n], 2)
SUB = round(L["k5"] + dur(os.path.join(VO, "k5.mp3")) + 0.25, 2)        # سُبْحانَ, the app's recording, right after Callum's line
L2 = dict(L)
for n in ("k5", "k6", "k7"):                                            # Rafiq's word gets its own moment: the later lines wait for it
    if n != "k5": L2[n] = round(L[n] + 1.3, 2)
L = L2
def at(n, key, last=False, end=False):
    hits = [(s, e) for w, s, e in words(n) if key in re.sub(r"[^a-z0-9']", "", w.lower())]
    s, e = hits[-1] if last else hits[0]
    return round(L[n] + (e if end else s), 2)
END = round(L["k7"] + dur(os.path.join(VO, "k7.mp3")) + 0.9, 2)

def build():
    out = os.path.join(HERE, "out", "v"); a = os.path.join(out, "assets")
    if os.path.exists(out): shutil.rmtree(out)
    os.makedirs(a)
    for f in ("karla-latin-500-normal.woff2", "karla-latin-700-normal.woff2", "ibm-plex-sans-arabic-arabic-700-normal.woff2"): shutil.copy(os.path.join(V6, "fonts", f), a)
    for f in ("fredoka-latin-600-normal.woff2", "fredoka-latin-700-normal.woff2", "instrument-serif-latin-400-normal.woff2"): shutil.copy(os.path.join(ROOT, "brag-quiz/fonts", f), a)
    shutil.copy(os.path.join(V6, "lib/gsap.min.js"), a)
    for f in ("chalk.wav", "duster.wav", "thump.wav", "tick.wav", "shimmer.wav"): shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/soft", f), a)
    for f in ("click.wav", "swoosh.wav"): shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/ref", f), a)
    shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/crash.wav"), a)
    lv = lambda f: float(re.findall(r"I:\s+(-?[\d.]+) LUFS", subprocess.run(["ffmpeg", "-i", f, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr)[-1])
    for n in L: shutil.copy(os.path.join(VO, n + ".mp3"), a)
    target = lv(os.path.join(VO, "k4.mp3"))                              # Rafiq's word level with Callum (the standard)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", WORD, "-af", f"volume={target - lv(WORD):.1f}dB,alimiter=limit=0.95", os.path.join(a, "subhana.mp3")], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", os.path.join(V6, "sfx-gen/fountain.mp3"), "-af",
                    f"volume=6dB,atrim=0:{END},afade=t=in:d=0.6,afade=t=out:st={END - 0.3}:d=0.3", "-c:a", "libmp3lame", "-q:a", "3", os.path.join(a, "bed.mp3")], check=True)
    au = []
    def snd(name, t0, vol, d=None, track=None):
        d = d or dur(os.path.join(a, name))
        au.append(f'<audio id="s{len(au)}" src="assets/{name}" data-start="{max(0, t0):.3f}" data-duration="{d:.3f}" data-volume="{vol:.3f}" data-track-index="{track or 3 + len(au)}"></audio>')
    for n, t0 in L.items(): snd(f"{n}.mp3", t0, 1.0, track=1)
    snd("subhana.mp3", SUB, 1.0, track=2); snd("bed.mp3", 0, 0.1, END, track=3)
    js = []; T = js.append

    def chalk(sel, t, d=0.45, vol=0.35):                               # written on left to right, with the chalk's sound
        T(f'tl.fromTo("{sel}", {{clipPath:"inset(0% 100% 0% 0%)", opacity:1}}, {{clipPath:"inset(0% 0% 0% 0%)", opacity:1, duration:{d}, ease:"power1.inOut"}}, {t:.2f});')
        snd("chalk.wav", t, vol, min(d + 0.1, 0.7))
    def draw(sel, t, d=0.6, vol=0.3):                                   # a chalk line drawn along its path
        T(f'tl.fromTo("{sel}", {{strokeDashoffset:1, opacity:1}}, {{strokeDashoffset:0, opacity:1, duration:{d}, ease:"power1.inOut"}}, {t:.2f});')
        snd("chalk.wav", t, vol, min(d + 0.1, 0.7))
    def wipe(board, t):                                                 # the duster sweeps the board clean
        T(f'tl.fromTo("#duster", {{x:-700, opacity:1}}, {{x:1300, opacity:1, duration:0.55, ease:"power1.inOut"}}, {t:.2f});')
        T(f'tl.to("{board}", {{opacity:0, filter:"blur(6px)", duration:0.4}}, {t + 0.12:.2f});'); snd("duster.wav", t, 0.5)
    def count(sel, to, t, d, suffix=""):                                # a number counting up, a click on every step
        T(f'(() => {{ const o = {{v:0}}, el = document.querySelector("{sel}"); tl.to(o, {{v:{to}, duration:{d}, ease:"power2.out", onUpdate:() => el.textContent = Math.round(o.v) + "{suffix}"}}, {t:.2f}); }})();')
        steps = min(to, 12)
        for k in range(steps): snd("click.wav", t + d * (1 - (1 - (k + 1) / steps) ** 2) * 0.95, 0.18)

    # 1 · TEN on frame 0; it slams on the shout (crash, shake, chalk dust), gets circled; "minutes a day" … "your salah"
    sh = L["k1"] + 0.12
    T(f'tl.fromTo("#ten", {{scale:1}}, {{scale:1.18, duration:0.08, yoyo:true, repeat:1, ease:"power2.out"}}, {sh:.2f});')
    T(f'tl.fromTo("#board", {{x:-18}}, {{x:0, duration:0.45, ease:"elastic.out(1,0.3)"}}, {sh:.2f});')
    T(f'tl.fromTo(".dust", {{opacity:0.9, scale:0.3}}, {{opacity:0, scale:1.6, duration:0.9, ease:"power2.out", immediateRender:false}}, {sh:.2f});')
    snd("crash.wav", sh - 0.02, 0.55); snd("thump.wav", sh, 0.6)
    draw("#ring", sh + 0.4, 0.5)
    for i, k in enumerate(("minutes", "day")): chalk(f"#m{i}", at("k2", k) - 0.05, 0.35)
    chalk("#arr1", at("k2", "takes"), 0.3); chalk("#m2", at("k2", "understanding") - 0.05, 0.5); chalk("#m3", at("k2", "salah") - 0.1, 0.4)
    wipe("#b1", L["k3"] - 0.45)
    # 2 · "years… because most courses start with grammar": a grammar table, YEARS?, struck through
    T(f'tl.set("#b2", {{opacity:1}}, {L["k3"] - 0.05:.2f});')
    chalk("#y0", at("k3", "arabic") - 0.05, 0.4); chalk("#y1", at("k3", "years") - 0.05, 0.4)
    chalk("#gt", at("k3", "grammar") - 0.4, 0.8, 0.3)
    draw("#x1", at("k3", "grammar", end=True) + 0.1, 0.25); draw("#x2", at("k3", "grammar", end=True) + 0.35, 0.25); snd("thump.wav", at("k3", "grammar", end=True) + 0.4, 0.35)
    wipe("#b2", L["k4"] - 0.45)
    # 3 · "the words you already say… your first week: the 20 words… more than half of every four-rakʿah prayer"
    T(f'tl.set("#b3", {{opacity:1}}, {L["k4"] - 0.05:.2f});')
    chalk("#w0", at("k4", "already") - 0.2, 0.6)
    chalk("#wk", at("k4", "week") - 0.1, 0.45)
    T(f'tl.set("#n20", {{opacity:1}}, {at("k4", "20") - 0.05:.2f});'); count("#n20", 20, at("k4", "20") - 0.05, 0.9)
    chalk("#w1", at("k4", "words", last=True) + 0.2, 0.5)
    draw("#pieo", at("k4", "half") - 0.6, 0.5)
    T(f'tl.fromTo("#pief", {{strokeDashoffset:100}}, {{strokeDashoffset:44, duration:1.0, ease:"power2.out"}}, {at("k4", "half") - 0.1:.2f});'); snd("shimmer.wav", at("k4", "half"), 0.25, 1.2)
    chalk("#w2", at("k4", "half") + 0.2, 0.5); chalk("#w3", at("k4", "surah") - 0.3, 0.45)
    wipe("#b3", L["k5"] - 0.4)
    # 4 · "every word comes with audio and a picture" (the card; Rafiq says سُبْحانَ) "…back just before you'd forget it" (the curve)
    T(f'tl.set("#b4", {{opacity:1}}, {L["k5"] - 0.05:.2f});')
    draw("#card", L["k5"] + 0.1, 0.5); chalk("#car", at("k5", "audio") - 0.2, 0.45); draw("#wave", at("k5", "audio"), 0.45)
    draw("#sun", at("k5", "picture") - 0.1, 0.5); chalk("#cen", SUB + 0.2, 0.45)
    T(f'tl.fromTo("#car", {{color:"{CHALK}"}}, {{color:"{GOLD}", duration:0.2, yoyo:true, repeat:1}}, {SUB:.2f});')
    draw("#axis", at("k5", "comes", last=True) - 0.3, 0.4); draw("#curve", at("k5", "back") - 0.2, 1.4)
    for i, w in enumerate(("before", "forget")): chalk(f"#rv{i}", at("k5", w) - 0.05, 0.3, 0.2)
    wipe("#b4", L["k6"] - 0.4)
    # 5 · "then you keep going": the list ticked off, 785 and 36 counting
    T(f'tl.set("#b5", {{opacity:1}}, {L["k6"] - 0.05:.2f});')
    chalk("#l0", at("k6", "every") - 0.1, 0.55); draw("#t0", at("k6", "salah", end=True), 0.2)
    chalk("#l1", at("k6", "surahs") - 0.5, 0.5); draw("#t1", at("k6", "surahs", end=True), 0.2)
    T(f'tl.set("#l2", {{opacity:1, clipPath:"inset(0% 0% 0% 0%)"}}, {at("k6", "785") - 0.05:.2f});'); count("#c785", 785, at("k6", "785") - 0.05, 1.6)
    draw("#t2", at("k6", "words", last=True, end=True), 0.2)
    T(f'tl.set("#l3", {{opacity:1, clipPath:"inset(0% 0% 0% 0%)"}}, {at("k6", "36") - 0.05:.2f});'); count("#c36", 36, at("k6", "36") - 0.05, 0.9)
    draw("#t3", at("k6", "conversations", end=True), 0.2)
    wipe("#b5", L["k7"] - 0.4)
    # 6 · "Ten minutes a day. Free for seven days, no card." the site; "Which part of your salah…? Tell me in the comments!"
    T(f'tl.set("#b6", {{opacity:1}}, {L["k7"] - 0.05:.2f});')
    chalk("#e0", L["k7"], 0.5); chalk("#e1", at("k7", "free") - 0.05, 0.6); draw("#box", at("k7", "card", end=True), 0.5)
    chalk("#e2", at("k7", "card", end=True) + 0.15, 0.6); chalk("#e3", at("k7", "which") - 0.05, 0.9); chalk("#e4", at("k7", "comments") - 0.3, 0.5)
    draw("#arr2", at("k7", "comments"), 0.4)

    dust = "".join(f'<i class="dust" style="left:{x}px;top:{y}px"></i>' for x, y in ((300, 520), (760, 470), (520, 760), (230, 820), (840, 760)))
    css = f"""
@font-face {{ font-family:"FR"; src:url("assets/fredoka-latin-600-normal.woff2"); font-weight:600; }}
@font-face {{ font-family:"FR"; src:url("assets/fredoka-latin-700-normal.woff2"); font-weight:700; }}
@font-face {{ font-family:"KA"; src:url("assets/karla-latin-700-normal.woff2"); font-weight:700; }}
@font-face {{ font-family:"AR"; src:url("assets/ibm-plex-sans-arabic-arabic-700-normal.woff2"); }}
* {{ margin:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:#4a2e1a; }}
#board {{ position:absolute; left:34px; top:34px; right:34px; bottom:150px; border-radius:10px; overflow:hidden;
  background:radial-gradient(ellipse at 30% 25%, #2b4a3e 0%, {BOARD} 55%, #16291f 100%); box-shadow:inset 0 0 120px rgba(0,0,0,.55), 0 0 0 14px #6b4426, 0 0 0 18px #3a2414; }}
#smudge {{ position:absolute; inset:0; opacity:.35; background:radial-gradient(ellipse 380px 160px at 30% 70%, rgba(255,255,255,.06), transparent 70%),
  radial-gradient(ellipse 300px 120px at 75% 35%, rgba(255,255,255,.05), transparent 70%), radial-gradient(ellipse 500px 200px at 60% 88%, rgba(255,255,255,.05), transparent 70%); }}
#tray {{ position:absolute; left:0; right:0; bottom:70px; height:44px; background:linear-gradient(#7a4e2c,#4d3019); box-shadow:0 8px 20px rgba(0,0,0,.5); }}
#tray i {{ position:absolute; bottom:30px; height:14px; border-radius:7px; }}
.b {{ position:absolute; inset:0; opacity:0; }} #b1 {{ opacity:1; }}
.c {{ position:absolute; left:0; right:0; text-align:center; font-family:FR; font-weight:600; color:{CHALK}; filter:url(#chalkf); opacity:0; line-height:1.1; }}
.ar {{ font-family:AR; direction:rtl; }}
svg.full {{ position:absolute; left:0; top:0; width:1012px; height:1736px; overflow:visible; filter:url(#chalkf); }}
svg path, svg line, svg circle, svg polyline, svg rect {{ fill:none; stroke:{CHALK}; stroke-width:9; stroke-linecap:round; stroke-linejoin:round; }}
.dr {{ stroke-dasharray:1; stroke-dashoffset:1; }}
.dust {{ position:absolute; width:180px; height:180px; border-radius:50%; background:radial-gradient(circle, rgba(242,239,230,.55), rgba(242,239,230,0) 65%); opacity:0; }}
#duster {{ position:absolute; top:-200px; left:0; width:340px; height:2200px; background:linear-gradient(90deg, rgba(31,58,48,0), rgba(60,90,76,.9) 30%, rgba(60,90,76,.9) 70%, rgba(31,58,48,0)); opacity:0; transform:rotate(8deg); }}
"""
    body = f"""
<svg width="0" height="0" style="position:absolute"><filter id="chalkf" x="-5%" y="-5%" width="110%" height="110%">
  <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="4" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="5" xChannelSelector="R" yChannelSelector="G" result="d"/>
  <feTurbulence type="fractalNoise" baseFrequency="1.6" numOctaves="1" seed="9" result="g"/>
  <feColorMatrix in="g" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.1 1.45" result="m"/>
  <feComposite in="d" in2="m" operator="in"/></filter></svg>
<div id="board"><div id="smudge"></div>{dust}
 <div class="b" id="b1">
  <div class="c" id="ten" style="top:250px;font-size:420px;font-weight:700;opacity:1;clip-path:none;color:{GOLD}">TEN</div>
  <svg class="full" viewBox="0 0 1012 1736"><path id="ring" class="dr" pathLength="1" d="M190 330 C 150 160, 870 140, 860 380 C 850 640, 160 650, 170 420 C 175 330, 260 270, 330 255" style="stroke:{PINK}"/></svg>
  <div class="c" id="m0" style="top:800px;font-size:110px">minutes</div><div class="c" id="m1" style="top:930px;font-size:110px">a day</div>
  <div class="c" id="arr1" style="top:1090px;font-size:110px">↓</div>
  <div class="c" id="m2" style="top:1250px;font-size:84px">to start understanding</div><div class="c" id="m3" style="top:1360px;font-size:110px;color:{GOLD}">your salah</div>
 </div>
 <div class="b" id="b2">
  <div class="c" id="y0" style="top:160px;font-size:130px">Arabic =</div><div class="c" id="y1" style="top:320px;font-size:230px;color:{PINK}">YEARS?</div>
  <div class="c" id="gt" style="top:700px;font-size:70px;line-height:1.5">
   <div style="display:grid;grid-template-columns:repeat(3,250px);justify-content:center;gap:0;border:6px solid {CHALK};margin:0 80px">
   <span style="border:3px solid {CHALK};padding:8px">past</span><span style="border:3px solid {CHALK};padding:8px">present</span><span style="border:3px solid {CHALK};padding:8px">form I</span>
   <span class="ar" style="border:3px solid {CHALK};padding:8px">فَعَلَ</span><span class="ar" style="border:3px solid {CHALK};padding:8px">يَفْعَلُ</span><span class="ar" style="border:3px solid {CHALK};padding:8px">فَعِلَ</span>
   <span class="ar" style="border:3px solid {CHALK};padding:8px">فَعُلَ</span><span class="ar" style="border:3px solid {CHALK};padding:8px">يَفْعِلُ</span><span class="ar" style="border:3px solid {CHALK};padding:8px">فاعِل</span></div>
   <div style="margin-top:30px;font-size:60px">…before a single word of your salah</div></div>
  <svg class="full" viewBox="0 0 1012 1736"><path id="x1" class="dr" pathLength="1" d="M120 660 L 900 1200" style="stroke:{PINK};stroke-width:16"/><path id="x2" class="dr" pathLength="1" d="M900 660 L 120 1200" style="stroke:{PINK};stroke-width:16"/></svg>
 </div>
 <div class="b" id="b3">
  <div class="c" id="w0" style="top:120px;font-size:72px">start with the words<br>you already say</div>
  <div class="c" id="wk" style="top:390px;font-size:130px;color:{GOLD}">WEEK 1</div>
  <div class="c" id="n20" style="top:560px;font-size:300px;font-weight:700;clip-path:none">0</div>
  <div class="c" id="w1" style="top:890px;font-size:84px">words you say most</div>
  <svg class="full" viewBox="0 0 1012 1736"><circle id="pieo" class="dr" pathLength="1" cx="506" cy="1250" r="190"/>
   <circle id="pief" cx="506" cy="1250" r="95" pathLength="100" transform="rotate(-90 506 1250)" style="stroke:{GOLD};stroke-width:190;stroke-dasharray:100;stroke-dashoffset:100;stroke-linecap:butt;opacity:.85"/></svg>
  <div class="c" id="w2" style="top:1470px;font-size:84px;color:{GOLD}">over half of every prayer</div>
  <div class="c" id="w3" style="top:1580px;font-size:52px">(four rakʿahs, before the surah)</div>
 </div>
 <div class="b" id="b4">
  <svg class="full" viewBox="0 0 1012 1736"><rect id="card" class="dr" pathLength="1" x="170" y="140" width="672" height="560" rx="40"/>
   <path id="wave" class="dr" pathLength="1" d="M230 610 l20 -30 l20 60 l20 -90 l20 120 l20 -60 l20 30" style="stroke:{GOLD}"/>
   <path id="sun" class="dr" pathLength="1" d="M760 230 m-46 0 a46 46 0 1 0 92 0 a46 46 0 1 0 -92 0 M760 150 v-26 M760 336 v-26 M680 230 h-26 M866 230 h-26 M704 174 l-18 -18 M834 304 l-18 -18 M816 174 l18 -18 M686 304 l18 -18" style="stroke:{GOLD};stroke-width:7"/>
   <path id="axis" class="dr" pathLength="1" d="M120 860 L 120 1500 L 920 1500"/>
   <path id="curve" class="dr" pathLength="1" d="M120 900 C 220 1200, 260 1300, 320 1340 L 330 920 C 420 1150, 470 1220, 540 1250 L 550 900 C 650 1060, 740 1110, 900 1130" style="stroke:{GOLD}"/></svg>
  <div class="c ar" id="car" style="top:240px;font-size:170px;line-height:1.5">سُبْحانَ</div>
  <div class="c" id="cen" style="top:500px;left:300px;font-size:76px">Glory be</div>
  <div class="c" id="rv0" style="top:1540px;font-size:62px">review</div><div class="c" id="rv1" style="top:1620px;font-size:58px;color:{GOLD}">just before you'd forget</div>
 </div>
 <div class="b" id="b5">
  <div class="c" id="l0" style="top:200px;left:180px;text-align:left;font-size:76px">every word of your salah</div><div class="c" id="l1" style="top:420px;left:180px;text-align:left;font-size:76px">10 short surahs</div>
  <div class="c" id="l2" style="top:640px;left:180px;text-align:left;font-size:78px;clip-path:none"><b id="c785" style="color:{GOLD};font-size:150px">0</b> words</div>
  <div class="c" id="l3" style="top:960px;left:180px;text-align:left;font-size:78px;clip-path:none"><b id="c36" style="color:{GOLD};font-size:150px">0</b> conversations</div>
  <svg class="full" viewBox="0 0 1012 1736">{''.join(f'<polyline id="t{i}" class="dr" pathLength="1" points="60,{y} 90,{y + 30} 140,{y - 40}" style="stroke:{GOLD};stroke-width:12"/>' for i, y in enumerate((250, 470, 760, 1080)))}</svg>
 </div>
 <div class="b" id="b6">
  <div class="c" id="e0" style="top:150px;font-size:110px;color:{GOLD}">10 min a day</div>
  <div class="c" id="e1" style="top:330px;font-size:84px">7 days free · no card</div>
  <svg class="full" viewBox="0 0 1012 1736"><rect id="box" class="dr" pathLength="1" x="110" y="560" width="792" height="190" rx="30" style="stroke:{GOLD}"/>
   <path id="arr2" class="dr" pathLength="1" d="M506 1330 L 506 1500 M 450 1440 L 506 1505 L 562 1440" style="stroke:{PINK}"/></svg>
  <div class="c" id="e2" style="top:600px;font-size:96px">rafiq-arabic.com</div>
  <div class="c" id="e3" style="top:930px;font-size:76px">Which part of your salah<br>do you want to understand first?</div>
  <div class="c" id="e4" style="top:1190px;font-size:84px;color:{PINK}">Tell me in the comments</div>
 </div>
 <div id="duster"></div>
</div>
<div id="tray"><i style="left:180px;width:90px;background:{CHALK}"></i><i style="left:300px;width:60px;background:{GOLD}"></i><i style="left:700px;width:200px;background:#2d2d2d;height:40px;bottom:30px;border-radius:8px"></i></div>"""
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><title>chalkboard</title>
<script src="assets/gsap.min.js"></script><style>{css}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{END}">
{body}
{chr(10).join(au)}
</div><script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;</script></body></html>
""")
    print("built", END, "s,", len(au), "sounds;", L, "subhana", SUB)

if __name__ == "__main__":
    build()
