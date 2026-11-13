# The new lesson wording from #358 (units 1-2) and #361 (reading starter, basics), checked with TypeSafe (#366; the earlier session couldn't).
# Each line in its place on the screen; a learner on a phone judges whether they know what to do, and how it feels.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
import sys
APP = ("Rafiq, an app for Muslims learning Arabic from zero, on a phone. A short lesson screen shows one instruction or message. ")
L = {  # key: (where it appears, the text)
 "guess_word":   ("Above a new Arabic word whose meaning is hidden until tapped.", "What do you think it means?"),
 "tap_see":      ("A button over the hidden meaning.", "Tap to see"),
 "guess_lesson": ("Under a question asked before a grammar lesson has taught it.", "Not sure? Guess: the lesson comes next."),
 "guess_rule":   ("Under a question asked before a reading rule has been taught.", "Not sure? Guess: the rule comes next."),
 "guess_title":  ("Heading of the guess screen before a grammar lesson.", "Possessive endings · before you start, have a guess"),
 "say_aloud":    ("Under a new word with its recording.", "Say it aloud once, then carry on"),
 "hear_pic":     ("Heading: a word is played and four pictures are shown.", "Hear it, tap the picture"),
 "hear_letter":  ("Heading: a letter's name is played and four letters are shown.", "Hear it, tap the letter"),
 "see_sound":    ("Heading: a letter is shown with four sounds to choose from.", "See it, pick its sound"),
 "match_tap":    ("Instruction in a game matching five Arabic words to their meanings.", "Tap a word, then its meaning"),
 "build":        ("Heading: build the Arabic phrase from word tiles.", "Build it in Arabic"),
 "notall":       ("After 'Build it in Arabic'.", "Not every tile belongs."),
 "say_ar":       ("Heading: an English meaning is shown and the learner picks the Arabic.", "How do you say it in Arabic?"),
 "one_more":     ("Heading when a word the learner got wrong comes back at the end.", "One more try"),
 "trace":        ("Over a pad where the learner traces an Arabic letter with a finger.", "Trace the letter with your finger"),
 "trace_wrong":  ("When the tracing strays from the letter's shape.", "Keep to the letter: clear it and try again"),
 "trace_ok":     ("When the tracing is complete.", "✓ Written. Try it on paper too."),
 "other_letter": ("Heading: a vowel mark just learned on ب is now shown on another letter.", "Now on another letter"),
 "bonus":        ("A button on the lesson's done screen, optional.", "⚡ Bonus: beat the clock"),
 "beat_best":    ("After the timed game, first time.", "That’s your score to beat."),
 "missed_back":  ("On the review's done screen.", "The ones you missed come back tomorrow."),
 "sci_words":    ("On the done screen of a 'meet 5 new words' lesson.", "🧠 You recalled each word 4 times, in 4 different ways. Recalling a word, not rereading it, is what makes it stick."),
 "sci_letters":  ("On the done screen of a letters lesson.", "🧠 You recalled each letter twice, by ear and by eye. Writing them on paper too helps them stick."),
 "say_name":     ("Done screen of the greetings lesson.", "You can say it, with your own name."),
 "all_there":    ("Done screen when every word was right.", "All still there."),
 "show_ans":     ("A button when the learner is stuck on a tile question.", "Show the answer"),
}
Q = {"clear": {"type": "score", "instructions": "`app` Where: `where` Text: `t`. Viewer: a 35-year-old beginner on a phone. Do they know exactly what to do or what it means?", "criteria": ["No", "Partly", "Mostly", "Fully"]},
     "tone":  {"type": "score", "instructions": "`app` Where: `where` Text: `t`. Viewer: a 35-year-old beginner on a phone. Does it feel warm and encouraging, not patronising, cold or odd?", "criteria": ["No", "Partly", "Mostly", "Fully"]}}
R2 = {
 "notall_a": (L["notall"][0], "Some tiles are extra: leave them out."), "notall_b": (L["notall"][0], "Watch out: there's an extra tile or two."),
 "all_a": (L["all_there"][0], "You remembered every one 🎉"), "all_b": (L["all_there"][0], "Every word remembered. Well done!"),
 "other_a": (L["other_letter"][0], "Same mark, new letter: how does it sound?"), "other_b": (L["other_letter"][0], "Now read the mark on a new letter"),
 "beat_a": (L["beat_best"][0], "Nice! Next time, try to beat it."), "beat_b": (L["beat_best"][0], "Your first score: beat it next time!"),
 "guessr_a": (L["guess_rule"][0], "Not sure? Just guess. Getting it wrong is fine: the rule comes next."), "guessr_b": (L["guess_rule"][0], "Have a guess, even a wild one: we'll explain it next."),
 "guessl_a": (L["guess_lesson"][0], "Not sure? Just guess. Getting it wrong is fine: the lesson comes next."), "guessl_b": (L["guess_lesson"][0], "Have a guess, even a wild one: we'll explain it next."),
 "bonus_a": (L["bonus"][0], "⚡ Bonus game: how many in 40 seconds?"), "bonus_b": (L["bonus"][0], "⚡ Bonus: beat the clock (40 sec)"),
 "build_a": (L["build"][0], "Tap the tiles to build it in Arabic"), "build_b": (L["build"][0], "Build the Arabic: tap the tiles in order"),
 "trace_a": (L["trace_wrong"][0], "Almost! Stay on the letter's lines: clear it and try again."), "trace_b": (L["trace_wrong"][0], "Off the lines a little. Tap Clear and have another go."),
}
W3 = "Under an English meaning, above word tiles the learner taps in order to build the Arabic; some tiles are decoys."
R3 = {"tiles_0": (W3, "Build it in Arabic. Not every tile belongs."), "tiles_a": (W3, "Build the Arabic: tap the tiles in order. Some tiles are extra."),
      "tiles_b": (W3, "Tap the tiles in order to build it in Arabic. Leave out the extra ones."),
      "tiles_c": (W3, "Build the Arabic: tap the tiles in order (one or two don't fit)."),
      "all_0": (L["all_there"][0], "All still there."), "other_0": (L["other_letter"][0], "Now on another letter")}
L.update(R2); L.update(R3)
keys = list(R3) if sys.argv[1:] == ["r3"] else list(R2) if sys.argv[1:] == ["r2"] else (sys.argv[1:] or [k for k in L if k not in R2 and k not in R3])
jobs = [(k, n) for k in keys for n in range(3)]
with ThreadPoolExecutor(24) as ex: r = list(ex.map(lambda j: (j[0], ask({"app": APP, "where": L[j[0]][0], "t": L[j[0]][1]}, Q)["answers"]), jobs))
rows = []
for k in keys:
    s = {q: round(sum(a[q]["score"] for kk, a in r if kk == k) / 3, 2) for q in Q}; rows.append((sum(s.values()), k, s))
for tot, k, s in sorted(rows): print(f"{k:13} {s} {tot:.2f}  {L[k][1]}")

# round 2 (13 Nov): rewrites for the lines under 3.0; run with  python3 lessons_copy.py r2
if keys == ["r2"]: pass
