"""camel-check.py: check the word list's spelling and vowel marks, and the salah roots,
against CAMeL Tools (NYU Abu Dhabi's Arabic morphological analyser). Build-time only.

  pip install --no-deps camel-tools muddler && pip install six cachetools pyrsistent \
      emoji editdistance requests tqdm docopt-ng tabulate
  camel_data -i light
  python3 tools/camel-check.py          # writes tools/camel-report.md

It flags things for a person to look at; it doesn't decide. The analyser knows Modern
Standard Arabic, so greetings, dialect words and Quranic spellings can be flagged
even when they're right.
"""
import json, re, subprocess, collections
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer
from camel_tools.utils.dediac import dediac_ar

SHADDA, SUKUN = "ّ", "ْ"
MARKS = set("ًٌٍَُِّْٰ")
LETTER = re.compile(r"[ء-يٱ]")

def js(file, name):
    code = f"{open(file, encoding='utf8').read()}\nprocess.stdout.write(JSON.stringify({name}))"
    return json.loads(subprocess.run(["node"], input=code, capture_output=True, text=True, check=True).stdout)   # stdin: drills-data.js is too long for -e

DAGGER, FATHA = "\u0670", "\u064e"

def letters(word):
    """[(letter, marks)], normalised so spelling conventions don't count as differences:
    sukun dropped (we often leave it out), dagger alif read as fatha, and no shadda on
    the sun letter after al- (the analyser doesn't write it)."""
    out = []
    for ch in word:
        if ch in MARKS:
            if out and ch != SUKUN:
                out[-1][1].add(FATHA if ch == DAGGER else ch)
        elif LETTER.match(ch):
            out.append((ch, set()))
    for i in range(2, len(out)):
        if out[i-2][0] == "ا" and out[i-1][0] == "ل" and not out[i-1][1] and (i == 2 or out[i-3][0] in "وفب"):
            out[i][1].discard(SHADDA)
    for i in range(len(out) - 1):                          # fatha before alif is implied
        if out[i+1][0] == "ا":
            out[i][1].discard(FATHA)
    return out

def fits(ours, theirs):
    """Same letters, and every mark we wrote matches theirs. A letter we left bare
    matches anything (so does leaving the vowel off a shadda); the last letter's marks (case endings) are not compared."""
    a, b = letters(ours), letters(theirs)
    if [x for x, _ in a] != [x for x, _ in b]:
        return None                                   # different spelling
    end = len(a) - 2 if a[-1][0] == "ا" else len(a) - 1     # tanween sits either side of a final alif
    return all(ma <= mb and SHADDA not in mb - ma for i, ((_, ma), (_, mb)) in enumerate(zip(a, b)) if i < end)

def tokens(phrase):
    for t in re.split(r"[\s/،,.؟?!()«»:;…\-]+", phrase):
        if t and "ـ" not in t and LETTER.search(t):
            yield t

analyzer = Analyzer(MorphologyDB.builtin_db(), backoff="NONE")
cache = {}
def analyses(token):
    bare = dediac_ar(token)
    if bare not in cache:
        cache[bare] = analyzer.analyze(bare)
    return cache[bare]

def check_vocab():
    unknown, spelling, vowels = [], [], []
    for w in js("vocab-data.js", "VOCAB"):
        for t in tokens(w["ar"]):
            an = analyses(t)
            if not an:
                unknown.append((w, t)); continue
            res = [fits(t, a["diac"]) for a in an]
            if all(r is None for r in res):
                spelling.append((w, t, sorted({a["diac"] for a in an})[:3]))
            elif not any(res):
                vowels.append((w, t, sorted({a["diac"] for a in an if fits(t, a["diac"]) is not None})[:4]))
    return unknown, spelling, vowels

WEAK = "وياأإآءئؤى"
def same_root(ours, theirs):
    """The analyser writes weak radicals (waw, ya, hamza) as #."""
    return len(ours) == len(theirs) and all(t == o or (t == "#" and o in WEAK) for o, t in zip(ours, theirs))

def check_roots():
    salah, out, seen = js("salah-data.js", "SALAH"), [], set()
    for part in salah["parts"]:
        for line in part.get("lines", []):
            for w in line.get("words", []):
                root = w.get("root")
                if not root or (w["ar"], root) in seen:
                    continue
                seen.add((w["ar"], root))
                an = [a for a in analyses(w["ar"]) if fits(w["ar"], a["diac"])] or analyses(w["ar"])
                found = {a.get("root", "").replace(".", "") for a in an}
                found.discard("")
                if found and not any(same_root(root, f) for f in found):
                    out.append((part["title"], w, sorted(found)))
    return out

def fits_full(ours, theirs):
    """Like fits, but the last letter's marks count too: the ending itself is checked."""
    a, b = letters(ours), letters(theirs)
    return [x for x, _ in a] == [x for x, _ in b] and all(ma <= mb and SHADDA not in mb - ma for (_, ma), (_, mb) in zip(a, b))

def check_teach():
    """The Arabic added to teach units 1-3 (#156): the grammar cards of units 1-3 with the right
    form in each crossed-out note, and the greeting phrases taken apart word by word (teach.js).
    Here the endings are checked too, since that's what the new cards teach."""
    extra = js("drills-data.js", "EXTRA")
    parts = json.loads(subprocess.run(["node", "-e", "global.window={};eval(require('fs').readFileSync('teach.js','utf8'));"
        "const P=['السَّلامُ عَلَيْكُم','وَعَلَيْكُمُ السَّلام','كَيْفَ حالُكَ','كَيْفَ حالُكِ','الحَمْدُ لِلَّهِ','أَهْلاً وَسَهْلاً','مَعَ السَّلامَةِ','ما اسْمُكَ؟','ما اسْمُكِ؟',"
        "'ما جِنْسِيَّتُكَ؟','ما جِنْسِيَّتُكِ؟','مِنْ أَيْنَ؟','ما شاءَ اللهُ','إِلى أَيْنَ'];"
        "process.stdout.write(JSON.stringify(P.flatMap(p=>window.RafiqTeach.parts(p).map(x=>x[0]))))"], capture_output=True, text=True, check=True).stdout)
    texts = [(f"unit {int(n)}: {g['h']}", g["ar"]) for n in ("01", "02", "03") for g in extra[n]["grammar"]]
    texts += [(f"unit {int(n)}: {g['h']} (the right form)", " ".join(re.findall(r"[\u0600-\u06FF][\u0600-\u06FF\s]*", g["bad"][1])))
              for n in ("01", "02", "03") for g in extra[n]["grammar"] if g.get("bad")]
    texts += [("unit 1: a greeting word by word", w) for w in parts]
    unknown, spelling, vowels, endings, seen = [], [], [], [], set()
    for where, text in texts:
        for t in tokens(text):
            if t in seen: continue
            seen.add(t); an = analyses(t)
            if not an: unknown.append((where, t)); continue
            if all(fits(t, a["diac"]) is None for a in an): spelling.append((where, t, sorted({a["diac"] for a in an})[:3]))
            elif not any(fits(t, a["diac"]) for a in an): vowels.append((where, t, sorted({a["diac"] for a in an if fits(t, a["diac"]) is not None})[:4]))
            elif not any(fits_full(t, a["diac"]) for a in an): endings.append((where, t, sorted({a["diac"] for a in an if fits(t, a["diac"])})[:4]))
    return unknown, spelling, vowels, endings, len(seen)

def main():
    unknown, spelling, vowels = check_vocab()
    roots = check_roots()
    t_unknown, t_spelling, t_vowels, t_endings, t_n = check_teach()
    row = lambda w, t: f"| {w['id']} | {w['ar']} | {w['en']} | {t} |"
    md = ["# CAMeL Tools check", "",
          "Generated by `tools/camel-check.py`. These are things for the teacher to glance at (#98), "
          "not errors: the analyser only knows Modern Standard Arabic, so greetings, dialect and "
          "Quranic spellings can show up even when they're right.", "",
          f"- Vowel marks that match no reading the analyser knows: **{len(vowels)}**",
          f"- Spelling the analyser only knows differently (often hamza or alif): **{len(spelling)}**",
          f"- Words it doesn't know at all: **{len(unknown)}**",
          f"- Salah words whose root differs from the analyser's: **{len(roots)}**", "",
          "## Vowel marks to check", "", "| id | entry | meaning | word | analyser's readings |", "|---|---|---|---|---|"]
    md += [row(w, t)[:-1] + f"| {' · '.join(c)} |" for w, t, c in vowels]
    md += ["", "## Spelling to check", "", "| id | entry | meaning | word | analyser's spellings |", "|---|---|---|---|---|"]
    md += [row(w, t)[:-1] + f"| {' · '.join(c)} |" for w, t, c in spelling]
    md += ["", "## Words the analyser doesn't know", "", "| id | entry | meaning | word |", "|---|---|---|---|"]
    md += [row(w, t) for w, t in unknown]
    md += ["", "## Salah roots to check", "", "| part | word | meaning | our root | analyser's roots |", "|---|---|---|---|---|"]
    md += [f"| {p} | {w['ar']} | {w['en']} | {w['root']} | {' · '.join(f)} |" for p, w, f in roots]
    md += ["", "## Teach first (units 1-3, #156)", "",
           f"{t_n} words checked from the grammar cards of units 1-3 and the greetings taken apart word by word, endings included.", "",
           "| where | word | problem | analyser's readings |", "|---|---|---|---|"]
    md += [f"| {w} | {t} | not known | |" for w, t in t_unknown]
    md += [f"| {w} | {t} | spelling | {' · '.join(c)} |" for w, t, c in t_spelling]
    md += [f"| {w} | {t} | vowel marks | {' · '.join(c)} |" for w, t, c in t_vowels]
    md += [f"| {w} | {t} | ending | {' · '.join(c)} |" for w, t, c in t_endings]
    open("tools/camel-report.md", "w", encoding="utf8").write("\n".join(md) + "\n")
    print(f"teach first: {t_n} words, unknown {len(t_unknown)}, spelling {len(t_spelling)}, vowels {len(t_vowels)}, endings {len(t_endings)}")
    print(f"vowels {len(vowels)}, spelling {len(spelling)}, unknown {len(unknown)}, roots {len(roots)}"
          " -> tools/camel-report.md")

if __name__ == "__main__":
    main()
