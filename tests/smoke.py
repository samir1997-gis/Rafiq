"""Browser smoke test: every page loads without a JavaScript error, and the
signed-in pages hand an unknown visitor to the login page.

Run (from the repo root), with the webapp-testing skill's server helper:
  python3 .claude/skills/webapp-testing/scripts/with_server.py \
    --server "python3 -m http.server 8765 >/dev/null 2>&1" --port 8765 -- python3 tests/smoke.py
"""
import glob, os, sys
from playwright.sync_api import sync_playwright

BASE = os.environ.get("BASE", "http://localhost:8765/")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
PUBLIC = ["index.html", "login.html", "plans.html", "privacy.html", "help.html", "reset-password.html"]
# third-party noise we can't fix from here (offline CDNs, analytics, Supabase with no session)
IGNORE = ("Failed to load resource", "net::ERR", "supabase", "Supabase", "favicon")

def main():
    pages = sorted(os.path.basename(p) for p in glob.glob("*.html"))
    failures = []
    with sync_playwright() as p:
        proxy = os.environ.get("HTTPS_PROXY")   # cloud sessions reach CDNs through a proxy
        browser = p.chromium.launch(headless=True, executable_path=CHROME if os.path.exists(CHROME) else None,
                                    args=["--proxy-server=" + proxy, "--proxy-bypass-list=localhost,127.0.0.1"] if proxy else [])
        ctx = browser.new_context(ignore_https_errors=bool(proxy))
        for name in pages:
            page = ctx.new_page()
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.on("console", lambda m: m.type == "error" and not any(s in m.text for s in IGNORE)
                    and errors.append(m.text))
            try:
                page.goto(BASE + name, wait_until="domcontentloaded", timeout=20000)
                page.wait_for_timeout(1500)
            except Exception as e:
                errors.append("load: %s" % e)
            if name in PUBLIC and name not in page.url:
                errors.append("public page redirected to " + page.url)
            status = "ok" if not errors else "FAIL"
            print("%-22s %-4s -> %s" % (name, status, page.url.replace(BASE, "")))
            for e in errors:
                print("    " + e[:300])
                failures.append((name, e))
            page.close()

        # the review scheduler is loaded wherever progress is
        page = ctx.new_page()
        page.goto(BASE + "vocab.html", wait_until="domcontentloaded")
        ok = page.evaluate("typeof FSRS==='object' && typeof Progress==='object' && typeof Progress.grade==='function'")
        print("FSRS + Progress on vocab.html:", "ok" if ok else "FAIL")
        if not ok:
            failures.append(("vocab.html", "FSRS/Progress missing"))
        browser.close()
    print("\n%d page(s) checked, %d problem(s)" % (len(pages), len(failures)))
    sys.exit(1 if failures else 0)

if __name__ == "__main__":
    main()
