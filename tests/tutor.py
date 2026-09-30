"""AI tutor check (#127), with a stand-in for the `tutor` function (the real one needs the
Claude API key) and a signed-in stand-in for Supabase:
  - the Tutor tab is in the bottom bar and opens the chat
  - a question sends the learner's unit, words and grammar notes; the answer streams in
    with its Arabic in its own font, and can be reported; the chat survives a reload
  - a question about the prayer also sends the salah lines
  - the daily limit gives a clear message and hands the question back
  - "Why?" appears only after a wrong answer, explains it from what's on screen, and
    goes once the next question is on screen

  python3 .claude/skills/webapp-testing/scripts/with_server.py \
    --server "python3 -m http.server 8765 >/dev/null 2>&1" --port 8765 -- python3 tests/tutor.py
"""
import json, os, sys
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8765/"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
# a signed-in learner with nothing saved yet: every query answers empty
FAKE_SUPABASE = """
window.supabase = { createClient: () => {
  const q = () => { const o = new Proxy(function(){}, { get: (t, k) => k === 'then'
      ? (res => res({ data: null, error: null, count: 0 })) : () => o }); return o; };
  const session = { access_token: 'test-token', expires_at: Date.now() / 1000 + 3600, user: { id: 'u1', email: 't@example.com' } };
  return { from: q, rpc: q, auth: {
    getSession: async () => ({ data: { session } }), getUser: async () => ({ data: { user: session.user } }),
    onAuthStateChange: () => ({ data: { subscription: { unsubscribe() {} } } }), signOut: async () => ({}) } };
} };
"""
ANSWER = "Use **هَذِهِ** for a feminine word.\n\n- هَذا بَيْتٌ = this is a house\n- هَذِهِ غُرْفَةٌ = this is a room"
WHY = "The right answer is **and the mercy**: وَرَحْمَةُ starts with وَ, *and*."

def main():
    asked, mode = [], {"limit": False}
    def tutor(route):
        if route.request.method == "OPTIONS":
            return route.fulfill(status=200, body="ok")
        body = json.loads(route.request.post_data or "{}")
        asked.append(body)
        if mode["limit"]:
            return route.fulfill(status=429, content_type="application/json", body='{"error":"limit","limit":20}')
        route.fulfill(status=200, content_type="text/plain; charset=utf-8", body=WHY if body.get("mode") == "why" else ANSWER)

    proxy = os.environ.get("HTTPS_PROXY")
    ok = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None,
                              args=["--proxy-server=" + proxy, "--proxy-bypass-list=localhost,127.0.0.1"] if proxy else [])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, ignore_https_errors=bool(proxy))
        ctx.route("**/@supabase/**", lambda r: r.fulfill(status=200, content_type="application/javascript", body=FAKE_SUPABASE))
        ctx.route("**/functions/v1/tutor", tutor)
        ctx.route("**/functions/v1/quran", lambda r: r.fulfill(status=503, content_type="application/json", body='{"error":"stub"}'))
        ctx.route("https://fonts.googleapis.com/**", lambda r: r.abort())
        page = ctx.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))

        # the tab
        page.goto(BASE + "progress.html", wait_until="domcontentloaded")
        page.wait_for_timeout(1200)
        tabs = page.eval_on_selector_all(".tabbar a", "as => as.map(a => a.textContent.trim())")
        ok.append(("Tutor tab in the bottom bar %s" % tabs, any(t.endswith("Tutor") for t in tabs)))
        page.click(".tabbar a[href='tutor.html']")
        page.wait_for_url("**/tutor.html")
        page.wait_for_selector(".starts button")
        ok.append(("Tutor tab marked as the current one", page.eval_on_selector(".tabbar a.on", "a => a.textContent").endswith("Tutor")))

        # a question, from a learner past the reading starter (unit 1)
        page.evaluate("RafiqPath.skipReading(); RafiqPath.steps(RafiqPath.units()[1]).forEach(s => RafiqPath.complete('0b', s.key))")   # and the basics (#165)
        page.click(".starts button >> nth=0")
        page.wait_for_selector(".msg.tu .rep")
        c = asked[-1]
        ok.append(("chat question sent", c["mode"] == "chat" and c["messages"][-1]["role"] == "user" and "هَذِهِ" in c["messages"][-1]["content"]))
        ok.append(("sends the unit, its words and grammar notes",
                   "Current unit:" in c["context"] and "Words in this unit:" in c["context"] and "How it works" in c["context"]))
        ok.append(("no salah lines for a grammar question", "Your salah" not in c["context"]))
        ans = page.inner_html(".msg.tu .tu-ans")
        ok.append(("answer shown: bold, list, Arabic in its own font", "<b>" in ans and "<li>" in ans and '<bdi lang="ar"' in ans))
        page.click(".msg.tu .rep")
        page.wait_for_selector(".rp-sheet.on")
        ok.append(("Report this answer opens the report form with the answer", "Tutor's answer" in page.inner_text(".rp-sheet") or "Asked the tutor" in page.inner_text(".rp-sheet")))
        page.click(".rp-sheet .rp-x")
        page.wait_for_timeout(400)

        # the chat survives a reload
        page.reload(wait_until="domcontentloaded")
        page.wait_for_selector(".msg.tu")
        ok.append(("chat kept after reload", page.locator(".msg").count() == 2))

        # a question about the prayer brings the salah lines
        page.fill("#q", "What does ruku mean in salah?")
        page.press("#q", "Enter")
        page.wait_for_function("document.querySelectorAll('.msg.tu .rep').length === 2")
        c = asked[-1]
        ok.append(("follow-up sends the chat so far", [m["role"] for m in c["messages"]] == ["user", "assistant", "user"]))
        ok.append(("salah question sends the salah lines", "Your salah" in c["context"] and "اللَّهُ أَكْبَرُ" in c["context"] and "\n = \n" not in c["context"]))
        ok.append(("an Arabic phrase from the prayer counts too", page.evaluate("RafiqTutor.learner('What does سَمِعَ اللَّهُ لِمَنْ حَمِدَهُ mean?').then(t => t.includes('Your salah'))")))

        # the daily limit
        mode["limit"] = True
        page.fill("#q", "One more?")
        page.click("#send")
        page.wait_for_selector(".msg.err")
        ok.append(("limit: clear message", "20 questions today" in page.inner_text(".msg.err")))
        ok.append(("limit: question handed back", page.input_value("#q") == "One more?"))
        mode["limit"] = False

        # New chat
        page.click("#new")
        ok.append(("New chat clears it", page.locator(".starts button").count() == 4))

        # "Why?" after a wrong answer, in the salah quiz
        page.goto(BASE + "learn.html?salah=quiz", wait_until="domcontentloaded")
        page.wait_for_selector(".opt")
        ok.append(("no Why? before answering", page.locator(".tu-why").count() == 0))
        wrong = False
        for _ in range(10):
            page.locator(".opt").last.click()
            page.wait_for_timeout(500)
            if page.locator(".opt.wrong").count():
                wrong = True
                break
            ok_right = page.locator(".tu-why").count() == 0
            if not ok_right:
                ok.append(("no Why? after a right answer", False))
            page.click("button.go")
            page.wait_for_timeout(400)
        ok.append(("got a wrong answer to try", wrong))
        ok.append(("Why? appears after a wrong answer", page.locator(".lhead .tu-why").count() == 1))
        page.click(".tu-why")
        page.wait_for_selector(".rp-sheet.on #tuOk:visible")
        c = asked[-1]
        ok.append(("Why? sends what's on screen", c["mode"] == "why" and "PICK THE MEANING" in c["context"].upper()))
        ok.append(("Why? shows the explanation", "and the mercy" in page.inner_text(".rp-sheet")))
        page.click("#tuOk")
        page.wait_for_timeout(400)
        page.click("button.go")
        page.wait_for_timeout(500)
        ok.append(("Why? gone on the next question", page.locator(".tu-why").count() == 0))
        ok.append(("no page errors", not errors))
        for e in errors:
            print("    " + e[:300])
        b.close()
    for name, good in ok:
        print(("ok   " if good else "FAIL ") + name)
    sys.exit(0 if all(g for _, g in ok) else 1)

if __name__ == "__main__":
    main()
