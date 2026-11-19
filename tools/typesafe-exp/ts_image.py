"""TypeSafe with images (19 Nov 2026). Images and the Box question are a "danger zone" feature: every request that carries an
image or a Box question must send the header TypeSafe-Danger-Zone-Images: true. Box needs jev-1.14.0 (jev-latest points to it).
Docs: https://docs.typesafe.ai/images, https://docs.typesafe.ai/primitives/box. Images: PNG or JPEG, each side 280 to 1568 px
(out-of-range images are rejected, not resized, so fit() resizes first), billed as input tokens.

  from ts_image import ask_img
  ask_img({"slide": "slide-1"}, {"slide-1": "path/to.png"}, questions)   # a reference string in the state is swapped for the image
"""
import base64, io, json, os, time, uuid, urllib.request
from PIL import Image

KEY = os.environ.get("TYPESAFE_API_KEY") or os.environ["TYPE_SAFE_KEY"]
HEADERS = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json", "TypeSafe-Danger-Zone-Images": "true"}

def fit(path, lo=280, hi=1568):
    """PNG bytes inside the API's size limits, upright, alpha flattened."""
    im = Image.open(path); im = im.convert("RGB")
    w, h = im.size; s = min(1.0, hi / max(w, h)); s = max(s, lo / min(w, h))
    if s != 1.0: im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "PNG"); return b.getvalue()

def ask_img(state, images, questions, model="jev-latest"):
    """images: {reference used in state/instructions/criteria: file path}. References should be unique strings."""
    assets = {ref: {"type": "image", "format": "png", "data_base64": base64.b64encode(fit(p)).decode()} for ref, p in images.items()}
    body = json.dumps({"model": model, "state": state, "assets": assets, "questions": questions}).encode()
    for a in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request("https://api.typesafe.ai/v1/systemone", body, HEADERS), timeout=120) as f: return json.load(f)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504, 529) and a < 4: time.sleep(2 ** a); continue
            raise RuntimeError(f"{e.code}: {e.read().decode()[:400]}")

def ref(): return "img-" + uuid.uuid4().hex
