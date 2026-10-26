#!/usr/bin/env python3
"""Word timings for the English lines of a lines file, without faster-whisper (its model comes from huggingface.co, which some
sessions can't reach): pocketsphinx's own English model (pip install pocketsphinx) is forced-aligned to each line's text, and the
result is written as the <mp3>.words.json cache that words_at() in build_formula.py reads. Lines already cached are skipped.
Checked against Whisper on g4-v3a.mp3: the same words, starts within ~0.4 s (pocketsphinx is the later of the two).

  python3 brag-quiz/align_words.py brag-quiz/voice/rahma-lines.json brag-quiz/voice/rahma"""
import json, os, re, subprocess, sys
from pocketsphinx import Decoder

EXTRA = {"fatiha": "F AA T IH HH AH", "raheem": "R AH HH IY M", "rakah": "R AA K AH", "deen": "D IY N", "allah": "AA L AH",
         "mashallah": "M AA SH AA L AH", "barik": "B AA R IH K", "allahumma": "AA L AH HH UH M AH",
         "salah": "S AH L AA", "dua": "D UW AA", "adhan": "AH DH AA N", "musalla": "M UH S AH L AA",
         "jabr": "JH AE B ER", "aljabr": "AE L JH AE B ER", "khwarizmi": "K W AA R IH Z M IY", "alkhwarizmi": "AE L K W AA R IH Z M IY",
         "alkhwarizmi's": "AE L K W AA R IH Z M IY Z", "bonesetter": "B OW N S EH T ER", "algebrista": "AE L JH AH B R IY S T AH",
         "sujood": "S UW JH UW D", "qahwa": "K AA HH W AH", "kahve": "K AA V EY", "koffie": "K AO F IY", "sufis": "S UW F IY Z",
         "makkah": "M AE K AH", "masjid": "M AA S JH IH D", "820": "EY T T W EH N T IY", "1582": "F IH F T IY N EY T IY T UW",
         "1400s": "F AO R T IY N HH AH N D R AH D Z", "fourteenhundreds": "F AO R T IY N HH AH N D R AH D Z"}

def pcm(path):
    return subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True, check=True).stdout

def align(mp3, text):
    """[(word as written, start s)] for every word of text; a word the model can't place gets a start between its neighbours."""
    shown = re.sub(r"\[[^\]]*\]", " ", text).split()
    keys = [re.sub(r"[^a-z0-9']", "", w.lower()) for w in shown]                 # years are in EXTRA as spoken ("820": eight twenty)
    d = Decoder(samprate=16000, bestpath=False)
    for k, ph in EXTRA.items():
        if not d.lookup_word(k): d.add_word(k, ph, False)
    known = [k for k in keys if k and d.lookup_word(k)]
    d.set_align_text(" ".join(known)); d.start_utt(); d.process_raw(pcm(mp3), full_utt=True); d.end_utt()
    got = iter([s.start_frame / 100 for s in d.seg() if s.word not in ("<s>", "</s>", "<sil>", "[NOISE]")])
    starts = [next(got) if k and d.lookup_word(k) else None for k in keys]
    for i, s in enumerate(starts):                        # fill gaps: halfway between the neighbours that were placed
        if s is None:
            a = next((starts[j] for j in range(i - 1, -1, -1) if starts[j] is not None), 0.0)
            b = next((starts[j] for j in range(i + 1, len(starts)) if starts[j] is not None), a + 0.6)
            starts[i] = round((a + b) / 2, 2)
    return [(w, round(s, 2)) for w, s in zip(shown, starts)]

if __name__ == "__main__":
    lines, out = sys.argv[1], sys.argv[2]
    for it in json.load(open(lines)):
        mp3 = os.path.join(out, it["file"] + ".mp3"); cache = mp3[:-4] + ".words.json"
        if "text" not in it or not re.search("[A-Za-z]", re.sub(r"\[[^\]]*\]", "", it["text"])) or not os.path.exists(mp3) or os.path.exists(cache): continue
        W = align(mp3, it["text"]); json.dump(W, open(cache, "w"), ensure_ascii=False)
        print(it["file"], " ".join(f"{w}@{s}" for w, s in W))
