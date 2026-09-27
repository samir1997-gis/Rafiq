# plain-grammar.py — rewrite the grammar notes and mistake explanations in drills-data.js
# for complete beginners: an English title (h), a translation of the example (tr),
# tools/plain-grammar.json holds the current wording (a few notes were simplified again after
# tools/typesafe-exp/grammar_clarity.py); this script records the first pass.
# and an explanation with no grammar terms (en). The Arabic (t, ar) is unchanged, so
# the recordings still match. Run: python3 tools/plain-grammar.py   (safe to re-run)
import json, os, re
ROOT = os.path.join(os.path.dirname(__file__), '..')
NOTES = {  # old en → (h, tr, new en)
 "No verb 'to be'. Both halves are marfūʿ — subject and predicate simply sit side by side.":
  ("No word for ‘am’, ‘is’ or ‘are’", "I am an engineer.", "Arabic just puts the two words side by side: ‘I engineer’. There’s no word for ‘is’ in the present, and both words keep their usual ending."),
 "The demonstrative agrees in gender with what follows.":
  ("‘This’ has a male and a female form", "This is a student (m) · This is a student (f).", "Use هَذا for a man or a masculine word, and هَذِهِ for a woman or a feminine word (most end in ة)."),
 "Add ـِيّ to a country to make a nationality; add ة for the feminine.":
  ("Turning a country into a nationality", "Pakistani (man) · Pakistani (woman)", "Add ـِيّ to the country to say where someone is from. For a woman, add ة as well: ـِيَّة."),
 "ما asks about things, مَنْ about people, هَلْ makes a yes/no question.":
  ("Question words", "What? · Who? · Is…? / Are…? · Where from?", "ما asks ‘what’, مَنْ asks ‘who’, and مِنْ أَيْنَ asks ‘where from’. Put هَلْ at the start of a sentence to make it a yes/no question."),
 "Two nouns joined: the first takes no ال and no tanwin; the second is genitive.":
  ("‘The X of Y’: two nouns side by side", "a picture of my family", "Say the thing first, then whose it is: ‘picture family-my’. The first word never takes ال or the extra -n; the second ends in -i (here hidden under ـِي, ‘my’)."),
 "Possession is a suffix on the noun, not a separate word.":
  ("‘My’, ‘your’, ‘his’ are endings", "my father · your father · his father", "Instead of a separate word, Arabic adds an ending: ـِي for ‘my’, ـكَ for ‘your’, ـهُ for ‘his’."),
 "The prefix carries the person: أ for 'I', يـ for 'he', تـ for 'she' or 'you'.":
  ("Who’s doing it? Look at the first letter", "I make wudu · he makes wudu", "In the present tense, the first letter shows who: أ for ‘I’, يـ for ‘he’, تـ for ‘she’ or ‘you’."),
 "The counted noun comes after, in the plural and genitive.":
  ("Counting from 3 to 10", "nine boys", "The number comes first, then the thing you’re counting, in the plural and ending in -in."),
 "'There is' sentences put the place first and the thing second, marfūʿ.":
  ("Saying ‘there is’", "There is a bed in the room.", "Start with the place, then the thing: ‘in the room, a bed’. There’s no separate word for ‘there is’."),
 "With a feminine noun the number drops its ة — reverse agreement.":
  ("Numbers 3 to 10 swap genders", "five rooms", "Odd but true: with a feminine word like غُرْفَة the number loses its ة (خَمْس), and with a masculine word it keeps it (خَمْسَة)."),
 "After كَمْ the noun is singular and manṣūb, never plural.":
  ("‘How many?’ takes one, not many", "How many rooms?", "After كَمْ, use the singular word ending in -an: ‘how many room?’. Never the plural."),
 "Ordinals follow the noun and match it in definiteness and case.":
  ("‘First’, ‘fifth’ come after the noun", "the fifth floor", "Arabic says ‘the floor the fifth’: the number word comes after the noun and copies it, so if the noun has ال, so does the number."),
 "The present tense covers habits: 'I wake up', 'I usually wake up'.":
  ("The present tense for habits", "I wake up early.", "The same verb means ‘I wake up’, ‘I’m waking up’ and ‘I usually wake up’. The situation tells you which."),
 "These adverbs are manṣūb — they always end in -an.":
  ("Words for ‘how’ or ‘when’ end in -an", "early · late", "Words that say how or when you do something usually end in -an (ـًا)."),
 "بِـ marks the means of transport, and takes the genitive.":
  ("‘By bus’: بِـ", "by bus", "Put بِـ on the front of the transport. The word after it ends in -i."),
 "لا negates the present tense; ما is for the past.":
  ("Saying ‘don’t’", "I don’t watch TV.", "Put لا before a present-tense verb. (For the past you’ll use ما later on.)"),
 "The object of a verb is manṣūb — fatḥa, or -an if indefinite.":
  ("The thing you eat, drink or want ends in -a", "I eat rice.", "The word that receives the action ends in -a, or -an if it has no ال: آكُلُ خُبْزًا, ‘I eat bread’."),
 "Accusative before عَلى, genitive after it.":
  ("‘I prefer X to Y’", "I prefer tea to coffee.", "أُفَضِّلُ + what you like more + عَلى + the other thing. The first ends in -a, the one after عَلى in -i."),
 "لِأَنَّ needs a noun after it, and that noun is manṣūb; the predicate stays marfūʿ.":
  ("‘Because’: لِأَنَّ", "because I weigh a lot", "لِأَنَّ is followed by a noun (or an ending like ـها), not straight by a verb. That noun ends in -a; the describing word after it keeps -u."),
 "The فَعْلان pattern is a diptote — no tanwin.":
  ("‘Hungry’ and ‘thirsty’: no extra -n", "I’m hungry.", "Words like جَوْعان (hungry) and عَطْشان (thirsty) never add the extra -n sound: جَوْعانُ, not جَوْعانٌ."),
 "'Going' is an adjective here, not a verb, and agrees with the speaker's gender.":
  ("‘I’m going’ uses a describing word", "going (said by a man) · going (said by a woman)", "أَنا ذاهِبٌ is literally ‘I (am) going’. It works like a describing word, so a woman adds ة: أَنا ذاهِبَةٌ."),
 "لِـ means 'for the purpose of', and takes the genitive.":
  ("‘For’ something: لِـ", "for the Dhuhr prayer", "لِـ on the front of a word means ‘for’. The word after it ends in -i."),
 "Place names like مَكَّة take a fatḥa where you'd expect a kasra, and never tanwin.":
  ("Some names never take -in", "to Makkah", "Place names like مَكَّة use -a where you’d expect -i, and never add the extra -n."),
 "Compound prepositions end in a genitive noun.":
  ("‘Next to’, ‘in front of’", "next to the house", "These place words go straight before the noun, and the noun ends in -i."),
 "After لِـ the verb takes a fatḥa — the subjunctive. This is the 'in order to' construction.":
  ("‘In order to’: لِـ + a verb", "I go (in order) to study.", "Put لِـ on a present-tense verb to say ‘in order to’. The verb then ends in -a: أَدْرُسَ, not أَدْرُسُ."),
 "Singular and manṣūb after كَمْ, however many you mean.":
  ("‘How many?’ again: one, ending in -an", "How many lessons?", "The same rule as before: after كَمْ, use the singular word ending in -an."),
 "'College of Education' — the second noun is genitive and carries the definiteness.":
  ("‘College of Education’", "the College of Education", "Two nouns side by side mean ‘X of Y’. Only the second one takes ال, and it ends in -i."),
 "Plural masculine verbs end in ـُونَ in the present.":
  ("‘They’ (men) study: ـُونَ", "they (men) study", "For ‘they’ meaning men or a mixed group, the present verb starts with يَـ and ends in ـُونَ."),
 "Doubling the middle letter turns 'do' into 'make someone do'.":
  ("Doubling a letter changes the meaning", "I study · I teach", "The shadda (ّ) doubles the middle letter and often means ‘make someone do it’: study → teach."),
 "Nouns ending in ى never change their ending, whatever the case.":
  ("Words ending in ى don’t change", "in the hospital", "Words ending in ى, like مُسْتَشْفى (hospital), keep the same ending whatever comes before them."),
 "Most job names form the feminine by adding ة.":
  ("Jobs for women: add ة", "nurse (man) · nurse (woman)", "Most job words become feminine by adding ة, just like nationalities."),
 "Same rule as always after كَمْ: singular, manṣūb.":
  ("How many hours?", "How many hours do you work?", "The same كَمْ rule: one hour, ending in -an: ساعَةً."),
 "Prices use بِكَمْ, not كَمْ on its own.":
  ("‘How much is it?’", "How much is this shirt?", "For prices, say بِكَمْ (‘for how much?’). كَمْ on its own asks ‘how many?’."),
 "The thing wanted is the object, so it and its adjective are manṣūb.":
  ("What you want ends in -a", "I want a white shirt.", "The thing you want takes the -a ending, and so does its colour: قَمِيصًا أَبْيَضَ."),
 "The أَفْعَل colour pattern never takes tanwin — fatḥa in the accusative.":
  ("Colours never add the extra -n", "white · blue", "Colours like أَبْيَض and أَزْرَق never end in -un or -an. Where other words take -an, they just take -a."),
 "After 11–99 the counted noun is singular and manṣūb.":
  ("From 11 to 99: one riyal", "fifty riyals", "After numbers from 11 to 99, the thing you’re counting is singular and ends in -an: ‘fifty riyal’."),
 "كانَ leaves the subject marfūʿ but makes the predicate manṣūb.":
  ("‘Was’: كانَ", "The weather was cold.", "Use كانَ for ‘was’. It makes the describing word end in -an: بارِدًا."),
 "لَيْسَ behaves exactly like كانَ — predicate manṣūb.":
  ("‘Isn’t’: لَيْسَ", "The weather isn’t hot.", "لَيْسَ means ‘is not’. Like كانَ, it makes the describing word end in -an."),
 "لِذَلِكَ introduces a result; لِأَنَّ introduces a cause. Don't swap them.":
  ("‘So’ and ‘because’", "It’s raining, so I took the umbrella.", "لِذَلِكَ means ‘so’ (what happened as a result). لِأَنَّ means ‘because’ (the reason). Don’t mix them up."),
 "An iḍāfa: 'the season of spring'.":
  ("‘The season of spring’", "spring (the season of spring)", "Arabic says ‘season (of) the spring’: two nouns side by side, the second with ال and ending in -i."),
 "لَكِنَّ with shadda takes a noun and makes it manṣūb; لَكِنْ without shadda doesn't.":
  ("Two ways to say ‘but’", "but there’s noise in it", "لَكِنَّ (with a shadda) is followed by a noun ending in -a. لَكِنْ (without one) can go before anything and changes nothing."),
 "To say 'there isn't', use لَيْسَ, not لا.":
  ("Saying ‘there isn’t’", "There isn’t any crowding in the village.", "Start with لَيْسَ, then the place, then the thing. Don’t use لا for this."),
 "The فَعْلاء pattern is a diptote — never any tanwin.":
  ("Colours for feminine words", "white · blue (for feminine words)", "For a feminine word the colour changes: أَبْيَض → بَيْضاء, أَزْرَق → زَرْقاء. These never add the extra -n either."),
 "Duals end in ـانِ when marfūʿ and ـَيْنِ otherwise.":
  ("Two of something: ـانِ or ـَيْنِ", "two hours", "Add ـانِ for ‘two’: ساعَتانِ. After words like فِي, or for the thing receiving an action, use ـَيْنِ: ساعَتَيْنِ."),
 "Both halves marfūʿ; no verb needed.":
  ("No word for ‘is’ (again)", "My hobby is reading.", "As in unit 1, just put the two parts side by side. Both keep their usual -u ending."),
 "Sound feminine plurals take a kasra in the accusative, never a fatḥa.":
  ("Plurals ending in ـات: -in, not -an", "I read magazines.", "Plurals ending in ـات never take -a. Where other words would end in -an, these end in -in: مَجَلَّاتٍ."),
 "When the reason refers back to something already mentioned, attach the pronoun to لِأَنَّ.":
  ("‘Because it…’: لِأَنَّها", "because it’s useful", "Join ‘it’, ‘he’ or ‘I’ straight onto لِأَنَّ: لِأَنَّها ‘because it (f)’, لِأَنَّهُ ‘because he / it’, لِأَنَّنِي ‘because I’."),
 "A defective verb — the final ى doesn't change in the present.":
  ("Verbs ending in ى", "I love collecting stamps.", "Some verbs end in ى, like أَهْوى (‘I love doing’). The ى stays the same."),
}
WHY = {  # mistake explanations: old → new
 "أُخْت is feminine, so the demonstrative must be هَذِهِ.": "أُخْت (sister) is feminine, so ‘this’ is هَذِهِ.",
 "The predicate of a nominal sentence is marfūʿ, not manṣūb.": "In a sentence with no verb, the describing word ends in -un, not -an.",
 "مِصْر is a diptote: fatḥa instead of kasra, and never any tanwin.": "مِصْر (Egypt) never adds the extra -n, and takes -a where you’d expect -i.",
 "The second half of an iḍāfa; the pronoun suffix makes it definite.": "It’s the second word of an ‘X of Y’ pair, and the ‘my / your’ ending already makes it ‘the’.",
 "Anything after فِي is genitive.": "The word after فِي (in) ends in -i.",
 "After 3–10: plural, genitive, indefinite.": "After 3 to 10: plural, no ال, ending in -in.",
 "A noun with a possessive suffix is already definite — no ال.": "A word with ‘my’, ‘your’ etc. on the end can’t take ال as well.",
 "Counted noun after 3–10 is genitive.": "After 3 to 10, the word you’re counting ends in -in.",
 "فِي always takes the genitive.": "The word after فِي (in) always ends in -i.",
 "كَمْ takes a singular accusative — the commonest slip at this level.": "After كَمْ: one (singular), ending in -an. The most common slip at this stage.",
 "After 3–10: plural and genitive.": "After 3 to 10: plural, ending in -in.",
 "The adjective copies the noun's case — genitive after فِي.": "The describing word copies the noun’s ending: -i after فِي.",
 "شَقَّة is feminine, and the predicate is marfūʿ.": "شَقَّة (flat) is feminine, so the describing word takes ة, and it ends in -un.",
 "أَيّ is genitive after فِي, and the noun after it is genitive too.": "After فِي, أَيّ ends in -i, and so does the word after it.",
 "After كَمْ: singular, accusative.": "After كَمْ: singular, ending in -an.",
 "After 3–10: plural, genitive.": "After 3 to 10: plural, ending in -in.",
 "The adjective must match the genitive noun.": "The describing word must copy the noun’s -i ending.",
 "Indefinite and marfūʿ — it needs the tanwin.": "With no ال, it needs the extra -n: -un.",
 "Adverbs of manner are manṣūb.": "Words for how you do something end in -an.",
 "Adverb — manṣūb.": "A ‘how / when’ word: it ends in -an.",
 "Direct object — manṣūb.": "It’s the thing receiving the action, so it ends in -a (or -an).",
 "فَعْلان is a diptote — ḍamma with no tanwin.": "Words like جَوْعان never add the extra -n: just -u.",
 "Genitive after إِلى.": "The word after إِلى (to) ends in -i.",
 "Object of a verb is manṣūb.": "The thing receiving the action ends in -a (or -an).",
 "لِأَنَّ makes its subject manṣūb, but the predicate stays marfūʿ.": "After لِأَنَّ the first word ends in -a, but the describing word keeps -u.",
 "Diptote — no tanwin.": "This word never adds the extra -n.",
 "Indefinite and genitive after فِي.": "After فِي, with no ال: it ends in -in.",
 "بِـ makes جانِب genitive; الْبَيْتِ is genitive as the second term.": "After بِـ, جانِب ends in -i, and so does الْبَيْتِ (‘next to the house’).",
 "Diptote: fatḥa, no tanwin, no ال.": "This name never takes ال or the extra -n, and uses -a where you’d expect -i.",
 "Diptote — fatḥa, no tanwin.": "This word uses -a where you’d expect -i, and never adds the extra -n.",
 "After بِـ the noun is genitive.": "The word after بِـ ends in -i.",
 "Object of the verb — manṣūb.": "The thing receiving the action ends in -a (or -an).",
 "لِـ of purpose puts the verb in the subjunctive — fatḥa.": "After لِـ meaning ‘in order to’, the verb ends in -a.",
 "كَمْ takes singular accusative.": "After كَمْ: singular, ending in -an.",
 "Second term of an iḍāfa — genitive.": "The second word of an ‘X of Y’ pair ends in -i.",
 "Subjunctive after لِـ.": "After لِـ (‘in order to’), the verb ends in -a.",
 "Singular accusative after كَمْ.": "After كَمْ: singular, ending in -an.",
 "كُلِّيَّة is genitive after فِي even though it heads the iḍāfa.": "After فِي, كُلِّيَّة ends in -i, even though it’s the first word of ‘college of…’.",
 "Object and its adjective both manṣūb.": "The thing wanted and its describing word both end in -a (or -an).",
 "Genitive after فِي.": "The word after فِي (in) ends in -i.",
 "Second term of the iḍāfa.": "The second word of an ‘X of Y’ pair ends in -i.",
 "Feminine subject, feminine predicate.": "A feminine person or thing needs a feminine describing word (with ة).",
 "Predicate of a nominal sentence is marfūʿ.": "In a sentence with no verb, the describing word ends in -u (-un).",
 "Accusative adjective, but a diptote — fatḥa with no tanwin.": "The colour ends in -a here, but never adds the extra -n.",
 "Singular accusative after 11–99.": "After 11 to 99: singular, ending in -an.",
 "Feminine of أَفْعَل colours is فَعْلاء, and here it's marfūʿ.": "For a feminine word the colour takes its ـاء form (like حَمْراء), ending in -u here.",
 "First term of an iḍāfa: no ال and no tanwin.": "The first word of an ‘X of Y’ pair has no ال and no extra -n.",
 "Colour diptote: fatḥa, no tanwin.": "Colours never add the extra -n; here it ends in -a.",
 "Diptote — the noun takes tanwin but the colour doesn't.": "The noun adds the extra -n, but the colour never does.",
 "كانَ makes its predicate manṣūb.": "After كانَ, the describing word ends in -an.",
 "فَوْقَ is a fixed accusative adverb, followed by a genitive.": "فَوْقَ (above) always ends in -a, and the word after it ends in -i.",
 "Predicate of كانَ is manṣūb.": "After كانَ, the describing word ends in -an.",
 "Object of the verb — manṣūb, even though it heads an iḍāfa.": "It receives the action, so it ends in -a, even as the first word of ‘X of Y’.",
 "Feminine colour, marfūʿ.": "The feminine form of the colour, ending in -u.",
 "Predicate after ما — marfūʿ.": "The describing word here keeps its -u ending.",
 "Here ازْدِحام is the delayed subject of لَيْسَ — marfūʿ.": "ازْدِحام is the thing there isn’t, so it keeps its -un ending.",
 "لا cannot negate a nominal sentence like this.": "لا can’t say ‘is not’ here: use لَيْسَ.",
 "Accusative dual.": "For ‘two’ here, use the ـَيْنِ ending.",
 "Predicate — marfūʿ.": "The describing word keeps its -u (-un) ending.",
 "Predicate of a nominal sentence — marfūʿ.": "In a sentence with no verb, the second part ends in -u.",
 "Sound feminine plural: kasra in the accusative. This one catches people for years.": "Plurals ending in ـات use -in where others use -an. This one catches people for years.",
 "Object of the verb and head of an iḍāfa: manṣūb, no ال, no tanwin.": "It receives the action, so it ends in -a, and as the first word of ‘X of Y’ it has no ال and no extra -n.",
 "Sound feminine plural takes kasra in the accusative.": "Plurals ending in ـات use -in, never -an.",
}
if __name__ == '__main__':
    p = os.path.join(ROOT, 'drills-data.js'); s = open(p, encoding='utf8').read()
    q = lambda t: json.dumps(t, ensure_ascii=False)
    n = w = 0
    for old, (h, tr, new) in NOTES.items():
        a = 'en:' + q(old)
        if a in s: s = s.replace(a, f'h:{q(h)},tr:{q(tr)},en:{q(new)}'); n += 1
        else:
            b = 'en:"' + old.replace('"', '\\"') + '"'
            if not (b in s or q(new) in s): print("already rewritten differently (see plain-grammar.json):", h)
            if b in s: s = s.replace(b, f'h:{q(h)},tr:{q(tr)},en:{q(new)}'); n += 1
    for old, new in WHY.items():
        for a in ('w:' + q(old), 'w:"' + old + '"'):
            if a in s: w += s.count(a); s = s.replace(a, 'w:' + q(new))
    open(p, 'w', encoding='utf8').write(s)
    json.dump({'notes': {k: {'h': v[0], 'tr': v[1], 'en': v[2]} for k, v in NOTES.items()}, 'why': WHY},
              open(os.path.join(ROOT, 'tools/plain-grammar.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print(f'notes rewritten: {n} of {len(NOTES)} · mistake explanations: {w}')
