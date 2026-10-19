# Renders ads.html to ad-news.png, ad-time.png, ad-ba.png (1080x1350). Run from the repo: python3 brag-social/ads/render.py
import os
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__))
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium"); p = b.new_page(viewport={"width": 1080, "height": 1350})
    p.goto("file://" + os.path.join(D, "ads.html")); p.evaluate("document.fonts.ready"); p.wait_for_timeout(400)
    for ad in ("ad-news", "ad-time", "ad-ba"):
        p.evaluate(f"show('{ad}')"); p.wait_for_timeout(150); p.screenshot(path=os.path.join(D, ad + ".png"))
    b.close()
