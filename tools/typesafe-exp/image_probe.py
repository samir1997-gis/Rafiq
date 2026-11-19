# First image test (19 Nov 2026): one of our own carousel slides (no people), three question types and a Box.
import sys, json; sys.path.insert(0, "tools/typesafe-exp"); from ts_image import ask_img, ref
r = ref(); path = sys.argv[1] if len(sys.argv) > 1 else "brag-quiz/stills/jamil/jamil-2.png"
Q = {"marks_on_letters": {"type": "noul", "instructions": "In `slide`, do the Arabic vowel marks sit directly on or under the letters they belong to?",
                          "criteria": {"true": "each small mark is just above or below its letter, as in a printed Qur'an",
                                       "false": "marks float well above the word, or sit over the wrong letters"}},
     "readable": {"type": "score", "instructions": "How easy is the English text in `slide` to read on a phone screen?",
                  "criteria": ["Hard to read: small or low contrast", "Readable with effort", "Easy to read", "Very easy: large and high contrast"]},
     "off_brand": {"type": "noul", "instructions": "Does `slide` use pastel colour blobs or hand-drawn doodles?"},
     "arabic_box": {"type": "box", "instructions": "the large Arabic phrase in `slide`"}}
out = ask_img({"slide": r}, {r: path}, Q)
print(json.dumps(out.get("answers"), ensure_ascii=False, indent=1)); print("model:", out.get("model"), "usage:", out.get("usage"))
