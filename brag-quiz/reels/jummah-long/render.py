"""Captions and hadith cards over the owner's own edit of the Jumuʿah quiz (owner, 23 Oct 2026: "edit the jummah long video with
captions and add graphics where they fit of the related hadeeths and references"; Drive: Rafiq videos / Jummah long.mp4). The video
already has the l2-jumuah ladder on top and the owner cut out below, so nothing is cut: the captions sit on his chest (the reel
template's kinetic style), and each hadith slides in over the quiz area once its answer is out, while he explains it.
  python3 render.py WORK       (WORK has raw.mp4 and words.json: [(word, start, end)] from faster-whisper) → WORK/jummah-long-edit.mp4"""
import json, os, re, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"; FPS = 30
W = os.path.abspath(sys.argv[1])
FIX = {"rusul": "ghusl", "jumma": "Jumu'ah", "jumwa": "Jumu'ah", "uter": "'itr", "libas": "libas", "muljumma": "al-Jumu'ah", "yawmul": "Yawm al-"}
JOIN = {27.34: "jama'ah", 32.38: "jama'ah", 83.64: "ansit", 23.64: "Yawm"}   # two Whisper pieces said as one word; "your" was "yawm"
DROP = {0.0, 28.06, 32.66, 84.02}                          # 0.0: a stray "up" Whisper hears in the meme intro
EM = {4.16, 4.7, 7.22, 11.04, 17.12, 17.48, 18.26, 22.56, 33.64, 37.52, 40.98, 43.3, 50.34, 55.42, 59.64, 63.76, 76.34, 76.7, 80.28,
      88.76, 89.54, 95.08, 100.38}
CARDS = [  # when he says it (a, b), a kicker, the Arabic, the English, the reference
    dict(a=18.6, b=25.3, k="THE PROPHET ﷺ SAID", ar="إِذا جاءَ أَحَدُكُمُ الجُمُعَةَ فَلْيَغْتَسِلْ",
         en="“When one of you comes to Jumu'ah, let him do ghusl.”", ref="AL-BUKHARI 877 · MUSLIM 844"),
    dict(a=35.4, b=41.9, k="ONE ROOT · TO GATHER", root="ج م ع", ar="جَماعَة · جُمُعَة",
         en="the congregation, and the day of gathering", ref=""),
    dict(a=51.6, b=57.4, k="PERFUME ON FRIDAY", ar="وَأَنْ يَمَسَّ طِيبًا إِنْ وَجَدَ",
         en="“…and to put on perfume, if he finds it.”", ref="AL-BUKHARI 880"),
    dict(a=57.5, b=61.5, k="THE PROPHET ﷺ SAID", ar="حُبِّبَ إِلَيَّ مِنَ الدُّنْيا النِّساءُ وَالطِّيبُ",
         en="“Of this world, women and perfume were made beloved to me.”", ref="AN-NASA'I 3939"),
    dict(a=72.9, b=78.7, k="YOUR BEST CLOTHES", ar="مَنِ اغْتَسَلَ يَوْمَ الجُمُعَةِ وَلَبِسَ مِنْ أَحْسَنِ ثِيابِهِ",
         en="“Whoever does ghusl on Friday and wears his best clothes…”", ref="ABU DAWUD 343"),
    dict(a=89.9, b=100.9, k="THE PROPHET ﷺ SAID", ar="إِذا قُلْتَ لِصاحِبِكَ يَوْمَ الجُمُعَةِ أَنْصِتْ وَالإِمامُ يَخْطُبُ فَقَدْ لَغَوْتَ",
         en="“If you tell your companion ‘Be quiet!’ on Friday while the imam is giving the khutbah, you have spoken idly.”",
         ref="AL-BUKHARI 934 · MUSLIM 851"),
]
end = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{W}/raw.mp4"]))

if len(sys.argv) > 2 and sys.argv[2] == "frames":           # one browser: every K-th frame from k
    from playwright.sync_api import sync_playwright
    C = json.load(open(f"{W}/overlay.json")); k, K = int(sys.argv[3]), int(sys.argv[4])
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME); p = b.new_page(viewport={"width": 1080, "height": 1920})
        p.goto("file://" + f"{W}/overlay.html"); p.evaluate(f"C = {json.dumps(C)}; build()"); p.evaluate("document.fonts.ready.then(() => true)"); p.wait_for_timeout(500)
        for i in range(k, round(end * FPS), K):
            f = f"{W}/ov/{i:05d}.png"
            if os.path.exists(f): continue
            p.evaluate(f"update({i / FPS})"); p.screenshot(path=f, omit_background=True)
        b.close()
    sys.exit()

ws = []                                                    # the words, spelled right, the gold ones marked
for w, s, e in json.load(open(f"{W}/words.json")):
    if round(s, 2) in DROP: continue
    core = re.sub(r"[^\w'-]", "", w).lower().strip("-"); tail = re.sub(r"^[\w' -]+", "", w)
    w = JOIN.get(round(s, 2), FIX[core] + tail if core in FIX else w)
    ws.append((w, s, e))
for i in range(len(ws) - 1, 0, -1):                       # "45" "%" → "45%"; "Yawm al-" "Jumu'ah" → one word
    w, s, e = ws[i]
    if w.startswith("%") or ws[i - 1][0] == "Yawm al-": ws[i - 1] = (ws[i - 1][0] + w, ws[i - 1][1], e); del ws[i]
caps, cur = [], []                                         # lines of up to 4 words, broken at punctuation and pauses (as the template's plan)
for i, (w, s, e) in enumerate(ws):
    cur.append((w, s, e)); nxt = ws[i + 1][1] if i + 1 < len(ws) else end
    if len(cur) >= 4 or w[-1] in ",.?" or (len(cur) >= 2 and nxt - e > .35) or i + 1 == len(ws):
        caps.append([cur[0][1], nxt if nxt - cur[-1][2] < .6 else cur[-1][2] + .3,
                     [[v[0].rstrip(",") if j == len(cur) - 1 else v[0], v[1], round(v[1], 2) in EM] for j, v in enumerate(cur)]]); cur = []
for f in ("anton-latin-400-normal.woff2", "instrument-serif-latin-400-normal.woff2", "ibm-plex-sans-arabic-arabic-700-normal.woff2"):
    os.makedirs(f"{W}/fonts", exist_ok=True); shutil.copy(os.path.join(REPO, "brag-quiz", "fonts", f), f"{W}/fonts/{f}")
shutil.copy(os.path.join(HERE, "overlay.html"), f"{W}/overlay.html")
json.dump(dict(caps=caps, cards=CARDS), open(f"{W}/overlay.json", "w"), ensure_ascii=False)
os.makedirs(f"{W}/ov", exist_ok=True); K = os.cpu_count() or 1
for p in [subprocess.Popen([sys.executable, __file__, W, "frames", str(k), str(K)]) for k in range(K)]: assert p.wait() == 0
# over his video; a soft swoosh as each card comes in
sw = os.path.join(REPO, "brag-quiz", "sfx", "ref", "swoosh.wav")
args = ["ffmpeg", "-v", "error", "-y", "-i", f"{W}/raw.mp4", "-framerate", str(FPS), "-i", f"{W}/ov/%05d.png"]
fc = ["[0:v]scale=1080:1920:flags=lanczos,fps=30,format=yuv420p[b]", "[b][1:v]overlay=0:0:format=auto,format=yuv420p[v]"]
for i, c in enumerate(CARDS):
    args += ["-i", sw]; ms = int(c["a"] * 1000)
    fc.append(f"[{i + 2}:a]aresample=48000,aformat=channel_layouts=stereo,volume=0.35,adelay={ms}|{ms}[s{i}]")
fc.append("[0:a]aresample=48000,aformat=channel_layouts=stereo[v0];[v0]" + "".join(f"[s{i}]" for i in range(len(CARDS))) +
          f"amix=inputs={len(CARDS) + 1}:normalize=0:duration=first[a]")
subprocess.run(args + ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "19", "-preset", "medium",
                       "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", f"{W}/jummah-long-edit.mp4"], check=True)
m = subprocess.run(["ffmpeg", "-i", f"{W}/jummah-long-edit.mp4", "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
gain = -14.5 - float(re.findall(r"I:\s+(-?[\d.]+) LUFS", m)[-1])  # to the reels' level; the high cut and 4x-oversampled limiter keep AAC's peaks under 0
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{W}/jummah-long-edit.mp4", "-c:v", "copy", "-af",
                f"volume={gain:.2f}dB,lowpass=f=15000:poles=2,aresample=192000,alimiter=limit=0.75:attack=1:release=60:level=false,aresample=48000",
                "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", f"{W}/jummah-long-final.mp4"], check=True)
print(" | ".join(" ".join(x[0].upper() if x[2] else x[0] for x in c[2]) for c in caps))
