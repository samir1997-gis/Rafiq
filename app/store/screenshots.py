"""The store screenshots (#352): the app's real screens, with a learner partway through the course, each under a short
headline in our colours. App Store 6.9" (1320×2868) and Google Play phone (1080×1920).

  node app/build-web.js            (if app/www is missing)
  python3 .claude/skills/webapp-testing/scripts/with_server.py --server "python3 -m http.server 8766 -d app/www >/dev/null 2>&1" \
    --port 8766 -- python3 app/store/screenshots.py
Writes app/store/screenshots/{appstore,play}-N.png. The account and the network are stood in for (tests/startup_speed.py's
stand-in Supabase); the Ask Rafiq answer is a real kind of answer, written here."""
import base64, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tests"))
from startup_speed import FAKE, MIRROR
# the stand-in server answers "offline", so the sample progress stays on the device (as on a phone with no signal)
FAKE = FAKE.replace("error: null, count: 0", "error: { message: 'offline' }, count: 0")
from playwright.sync_api import sync_playwright

APP = "http://localhost:8766/"
OUT = os.path.join(HERE, "screenshots"); os.makedirs(OUT, exist_ok=True)
RAW = os.path.join(OUT, "raw"); os.makedirs(RAW, exist_ok=True)
W, H = 440, 956                       # an iPhone 6.9" screen in points; ×3 = 1320×2868
# inside the app: native, no install card, plugins that do nothing
CAP = ("window.Capacitor={isNativePlatform:()=>true,getPlatform:()=>'ios',registerPlugin:()=>new Proxy({},{get:()=>async()=>({})}),"
       "Plugins:new Proxy({},{get:()=>new Proxy({},{get:()=>async()=>({})})})};")
CHAT = [{"role": "user", "content": "What's the difference between هَذا and هَذِهِ?"},
        {"role": "assistant", "content": "**هَذا** (hādhā) means *this* for a masculine word, and **هَذِهِ** (hādhihi) for a feminine one:\n- This is a book: هَذا كِتابٌ\n- This is a car: هَذِهِ سَيّارَةٌ\nA quick tip: a word ending in ة is usually feminine, so it takes هَذِهِ."}]
SEED = ("localStorage.setItem('rafiq_progress_mirror',%s);localStorage.setItem('rafiq_onboarded','u1');localStorage.setItem('rafiq_salah_on','1');"
        "localStorage.setItem('bay_name','Aisha');localStorage.setItem('rafiq_ai_ok','1');localStorage.setItem('rafiq_tutor_chat',%s);"
        % (json.dumps(json.dumps(MIRROR)), json.dumps(json.dumps(CHAT))))
# a learner two units in: the reading starter, the basics and units 1–2 done, unit 3 under way, a 12-day streak
PROGRESS = """() => { const U = RafiqPath.units();
  U.slice(0, 4).forEach(u => RafiqPath.steps(u).forEach(s => RafiqPath.complete(u.n, s.key)));
  RafiqPath.steps(U[4]).slice(0, 9).forEach(s => RafiqPath.complete(U[4].n, s.key));
  for(let d = 1; d <= 12; d++){ const k = 's:' + new Date(Date.now() - d * 864e5).toISOString().slice(0, 10); Progress.touch(k); Progress.touch(k); }
  Progress.flush && Progress.flush(); }"""

SHOTS = [   # (page, what to do there, headline, the words in green)
    ("dashboard.html", None, "5 minutes a day.\nJust press Continue.", "Just press Continue."),
    ("salah.html", None, "Understand every\nword of your salah", "your salah"),
    ("onboarding.html", "first", "Say your first\nsentence today", "first sentence"),
    ("tutor.html", None, "Stuck? Ask Rafiq,\nyour AI tutor", "Ask Rafiq,"),
    ("practise.html", None, "Practise your way:\nscenes, verbs, spelling", "your way:"),
    ("lesson", None, "Every word with audio,\nfully vowelled", "with audio,"),
]

def frame(page, png, size, headline, green):
    """the screen under its headline, on a page the store's size"""
    fw, fh = size; cap = int(fh * 0.20); sh = fh - cap - int(fh * 0.04); sw = int(sh * W / H)
    if sw > fw * 0.86: sw = int(fw * 0.86); sh = int(sw * H / W)
    lines = "".join(f"<div>{l.replace(green, f'<em>{green}</em>') if green in l else l}</div>" for l in headline.split("\n"))
    page.set_viewport_size({"width": fw, "height": fh})
    page.set_content(f"""<html><head><link href="https://fonts.googleapis.com/css2?family=Nunito:wght@800;900&display=swap" rel="stylesheet">
      <style>body{{margin:0;width:{fw}px;height:{fh}px;background:linear-gradient(180deg,#F1ECE0,#E6DFCF);font-family:Nunito,sans-serif;overflow:hidden}}
      .h{{height:{cap}px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;color:#17262B;
         font-weight:900;font-size:{int(fw * 0.072)}px;line-height:1.12;letter-spacing:-.01em}} .h em{{font-style:normal;color:#2E7263}}
      .s{{width:{sw}px;height:{sh}px;margin:0 auto;border-radius:{int(sw * 0.09)}px;overflow:hidden;
         box-shadow:0 {int(fh*.012)}px {int(fh*.03)}px rgba(23,38,43,.28);border:{max(2, int(fw*.004))}px solid #17262B}}
      .s img{{width:100%;height:100%;object-fit:cover;object-position:top}}</style></head>
      <body><div class="h">{lines}</div><div class="s"><img src="data:image/png;base64,{base64.b64encode(open(png, "rb").read()).decode()}"></div></body></html>""")
    page.wait_for_timeout(700)

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    c = b.new_context(viewport={"width": W, "height": H}, device_scale_factor=3, color_scheme="light")
    for pat in ("**/vendor/supabase.js", "**/@supabase/**"): c.route(pat, lambda r: r.fulfill(status=200, content_type="application/javascript", body=FAKE))
    c.add_init_script("if(!sessionStorage.getItem('seeded')){sessionStorage.setItem('seeded',1);" + SEED + "}" + CAP)
    p = c.new_page(); errs = []; p.on("pageerror", lambda e: errs.append(str(e)))
    p.goto(APP + "dashboard.html"); p.wait_for_timeout(1500); p.evaluate(PROGRESS); p.wait_for_timeout(500)
    raws = []
    for i, (pg, how, headline, green) in enumerate(SHOTS, 1):
        if how == "first":
            p.evaluate("localStorage.removeItem('rafiq_first_lesson')")
            p.goto(APP + pg); p.wait_for_timeout(1500)
            for _ in range(4):                                  # on to "Introduce yourself", half built
                if p.locator(".fl-opts").count(): p.locator(".fl-opts .opt", has_text="Peace be upon you").click(); p.wait_for_timeout(300)
                p.click("#flNext"); p.wait_for_timeout(500)
            p.locator(".fl-tile", has_text="as-salāmu").click(); p.wait_for_timeout(250)
            p.locator(".fl-tile", has_text="ismī").click(); p.wait_for_timeout(700)
        elif pg == "lesson":                                    # the next lesson, from Home's Continue
            p.goto(APP + "dashboard.html"); p.wait_for_timeout(1800)
            p.goto(APP + p.get_attribute("#home .today-card a.cont", "href")); p.wait_for_timeout(2500)
        else:
            p.goto(APP + pg); p.wait_for_timeout(2200)
            p.evaluate("document.querySelectorAll('.pwa-card,#pwaInstall,#remPrompt').forEach(e=>e.remove())")
        f = os.path.join(RAW, f"{i}.png"); p.screenshot(path=f); raws.append((f, headline, green))
    fp = b.new_page()
    for i, (f, headline, green) in enumerate(raws, 1):
        for name, size in (("appstore", (1320, 2868)), ("play", (1080, 1920))):
            frame(fp, f, size, headline, green); fp.screenshot(path=os.path.join(OUT, f"{name}-{i}.png"))
    print(len(raws), "screens;", "errors:", errs[:3])
    b.close()
