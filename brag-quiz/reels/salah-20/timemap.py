"""Times in the owner's take → times after the silence cut (chunks.json from `reel.py <W> cut`), so the edit keeps its own
timings when the pauses go. A time inside a removed pause lands on the cut."""
import json, os
FPS = 30
def loader(W):
    ch = json.load(open(os.path.join(W, "chunks.json")))
    def m(t):
        acc = 0.0
        for a, b in ch:
            d = round((b - a) * FPS) / FPS          # what `base` keeps of each piece, frame-exact
            if t < a: return round(acc, 3)
            if t <= a + d: return round(acc + t - a, 3)
            acc += d
        return round(acc, 3)
    return m
