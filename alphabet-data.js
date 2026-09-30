/* The reading starter (unit 0): the 28 letters in groups that share a shape,
   then the vowel marks, the reading rules, then a listening test. Each letter: [letter, name, how
   it sounds, example word, example meaning, examples]. Letters marked * never
   join to the letter after them.
   examples: three words with the letter at the start, in the middle and at the
   end, as [word, transliteration, meaning]; [brackets] mark the letter's sound
   in the transliteration. Most come from vocab-data.js; a teacher should check
   the rest. */
const ALPHABET_GROUPS = [
  {title:'Letters 1: the "boat" shapes', letters:[
    ['ا','أَلِف','A long "aa", or a seat for a glottal stop (the catch in "uh-oh") *','أَسَد','lion',
      [['أَسَد','[a]sad','lion'],['كِتاب','kit[ā]b','book'],['هَذا','hādh[ā]','this']]],
    ['ب','باء','"b" as in "bed" — one dot below','بَيْت','house',
      [['بَيْت','[b]ayt','house'],['طالِبَة','ṭāli[b]a','student (f)'],['كِتاب','kitā[b]','book']]],
    ['ت','تاء','"t" as in "tea" — two dots above','تَمْر','dates',
      [['تَمْر','[t]amr','dates'],['مَتَى','ma[t]ā','when?'],['بَيْت','bay[t]','house']]],
    ['ث','ثاء','"th" as in "think" — three dots above','ثَلاثَة','three',
      [['ثَلاثَة','[th]alātha','three'],['اثْنانِ','i[th]nān','two'],['حَدِيث','ḥadī[th]','a conversation; a hadith']]]]},
  {title:'Letters 2: the "hook" shapes', letters:[
    ['ج','جِيم','"j" as in "jam" — dot inside','جَمَل','camel',
      [['جَمَل','[j]amal','camel'],['مَسْجِد','mas[j]id','mosque'],['ثَلْج','thal[j]','snow']]],
    ['ح','حاء','A breathy "h" from deep in the throat — no dot','حَلِيب','milk',
      [['حَلِيب','[ḥ]alīb','milk'],['واحِد','wā[ḥ]id','one'],['صَباح','ṣabā[ḥ]','morning']]],
    ['خ','خاء','"kh" as in Scottish "loch" — dot above','خُبْز','bread',
      [['خُبْز','[kh]ubz','bread'],['أُخْت','u[kh]t','sister'],['أَخ','a[kh]','brother']]]]},
  {title:'Letters 3: small letters that don\'t join', letters:[
    ['د','دال','"d" as in "door" *','دَرْس','lesson',
      [['دَرْس','[d]ars','lesson'],['مَدْرَسَة','ma[d]rasa','school'],['واحِد','wāḥi[d]','one']]],
    ['ذ','ذال','"th" as in "this" *','ذَهَب','gold',
      [['ذَهَب','[dh]ahab','gold'],['هَذا','hā[dh]ā','this'],['تِلْمِيذ','tilmī[dh]','pupil']]],
    ['ر','راء','A rolled "r" *','رَجُل','man',
      [['رَجُل','[r]ajul','man'],['أَرْبَعَة','a[r]baʿa','four'],['شَهْر','shah[r]','month']]],
    ['ز','زاي','"z" as in "zoo" *','زَيْت','oil',
      [['زَيْت','[z]ayt','oil'],['وَزْن','wa[z]n','weight'],['خُبْز','khub[z]','bread']]]]},
  {title:'Letters 4: the "teeth" shapes', letters:[
    ['س','سِين','"s" as in "sun"','سَمَك','fish',
      [['سَمَك','[s]amak','fish'],['خَمْسَة','kham[s]a','five'],['دَرْس','dar[s]','lesson']]],
    ['ش','شِين','"sh" as in "ship" — three dots','شَمْس','sun',
      [['شَمْس','[sh]ams','sun'],['عَشاء','ʿa[sh]āʾ','dinner'],['عَطَش','ʿaṭa[sh]','thirst']]],
    ['ص','صاد','A heavy "s", said with the tongue low','صَدِيق','friend',
      [['صَدِيق','[ṣ]adīq','friend'],['عَصِير','ʿa[ṣ]īr','juice'],['قَمِيص','qamī[ṣ]','shirt']]],
    ['ض','ضاد','A heavy "d" — the letter Arabic is famous for','ضَيْف','guest',
      [['ضَيْف','[ḍ]ayf','guest'],['أَيْضاً','ay[ḍ]an','also'],['بَيْض','bay[ḍ]','eggs']]]]},
  {title:'Letters 5: tall letters and the throat', letters:[
    ['ط','طاء','A heavy "t"','طالِب','student',
      [['طالِب','[ṭ]ālib','student'],['فُطُور','fu[ṭ]ūr','breakfast'],['قِطّ','qi[ṭṭ]','cat']]],
    ['ظ','ظاء','A heavy "th" as in "this"','ظُهْر','noon',
      [['ظُهْر','[ẓ]uhr','noon'],['عَظْمَة','ʿa[ẓ]ma','bone'],['حافِظ','ḥāfi[ẓ]','someone who knows the Qurʾan by heart']]],
    ['ع','عَيْن','ʿayn: a squeeze deep in the throat — no English sound like it','عَيْن','eye',
      [['عَيْن','[ʿ]ayn','eye'],['نَعَمْ','na[ʿ]am','yes'],['أُسْبُوع','usbū[ʿ]','week']]],
    ['غ','غَيْن','"gh", like a French "r"','غُرْفَة','room',
      [['غُرْفَة','[gh]urfa','room'],['صَغِير','ṣa[gh]īr','small'],['فارِغ','fāri[gh]','empty']]]]},
  {title:'Letters 6: loops and hooks', letters:[
    ['ف','فاء','"f" as in "fish" — one dot above','فِيل','elephant',
      [['فِيل','[f]īl','elephant'],['عَفْواً','ʿa[f]wan','you\'re welcome'],['صَيْف','ṣay[f]','summer']]],
    ['ق','قاف','"q": a "k" from far back in the throat — two dots','قَلَم','pen',
      [['قَلَم','[q]alam','pen'],['وَقْت','wa[q]t','time'],['سُوق','sū[q]','market']]],
    ['ك','كاف','"k" as in "kite"','كِتاب','book',
      [['كِتاب','[k]itāb','book'],['شُكْراً','shu[k]ran','thank you'],['سَمَك','sama[k]','fish']]],
    ['ل','لام','"l" as in "lamp"','لَيْل','night',
      [['لَيْل','[l]ayl','night'],['طالِبَة','ṭā[l]iba','student (f)'],['مال','mā[l]','money']]]]},
  {title:'Letters 7: the last five', letters:[
    ['م','مِيم','"m" as in "moon"','ماء','water',
      [['ماء','[m]āʾ','water'],['خَمْسَة','kha[m]sa','five'],['أُمّ','u[mm]','mother']]],
    ['ن','نُون','"n" as in "noon" — one dot above','نُور','light',
      [['نُور','[n]ūr','light'],['أَنا','a[n]ā','I'],['مَنْ','ma[n]','who?']]],
    ['ه','هاء','"h" as in "hat"','هِلال','crescent moon',
      [['هِلال','[h]ilāl','crescent moon'],['شَهْر','sha[h]r','month'],['وَجْه','waj[h]','face']]],
    ['و','واو','"w", or a long "oo" *','وَلَد','boy',
      [['وَلَد','[w]alad','boy'],['يَوْم','ya[w]m','day'],['هُوَ','hu[w]a','he']]],
    ['ي','ياء','"y", or a long "ee" — two dots below','يَد','hand',
      [['يَد','[y]ad','hand'],['بَيْت','ba[y]t','house'],['فِي','f[ī]','in']]]]},
];
/* Vowel marks, shown on ب. [written, sound, what it is, example]. The mark (or,
   for a long vowel, the letter) after ب is what's shown in red. */
const VOWEL_MARKS = [
  ['بَ','ba','Fatha — a small stroke above: a short "a"',['بَيْت','b[a]yt','house']],
  ['بِ','bi','Kasra — a small stroke below: a short "i"',['بِنْت','b[i]nt','girl']],
  ['بُ','bu','Damma — a small curl above: a short "u"',['خُبْز','kh[u]bz','bread']],
  ['بْ','b','Sukun — a small circle: no vowel after the letter',['مَنْ','ma[n]','who?']],
  ['بّ','bb','Shadda — a small "w": the letter is doubled',['أُمّ','u[mm]','mother']],
  ['با','baa','Alif after fatha — a long "aa"',['باب','b[ā]b','door']],
  ['بي','bii','Ya after kasra — a long "ee"',['فِيل','f[ī]l','elephant']],
  ['بو','buu','Waw after damma — a long "oo"',['نُور','n[ū]r','light']],
  ['بٌ','bun','Tanwin — a doubled mark: adds "n" at the end of a word',['كِتابٌ','kitāb[un]','a book']],
];
/* Reading rules (#163), after the vowel marks: five things the marks alone don't tell you, one per
   screen, each followed by a pick. [title, what to know, examples [word, transliteration, meaning],
   check [question, options, right one, why, the Arabic to hear]]. */
const READING_RULES = [
  ['The ending ة', 'ة at the end of a word sounds like a soft "a". When an ending or another word follows, it becomes a "t" sound, and before an ending it’s written ت.',
    [['مَدْرَسَة','madras[a]','school'],['مَدْرَسَتِي','madras[at]ī','my school']],
    ['How is مَدْرَسَتِي said?', ['madrasatī','madrasa-ī','madrasahī'], 0, 'Before an ending, ة is said and written as t.', 'مَدْرَسَتِي']],
  ['ال is said "al-"', 'ال on the front of a word means "the" (more on that in unit 1). Before half the letters, like ق, ب and ف (the "moon letters"), you say it as it looks: al-.',
    [['القُرْآن','[al]-qurʾān','the Qur’an'],['الفَجْر','[al]-fajr','dawn']],
    ['How is الفَجْر said?', ['al-fajr','af-fajr','fajr'], 0, '', 'الفَجْر']],
  ['Sun letters: the ل goes quiet', 'Before 14 letters the ل of ال isn’t said. The next letter doubles instead, which is why it carries ّ: as-salām, not al-salām. They’re called sun letters because الشَّمْس (the sun) starts with one. The 14: ت ث د ذ ر ز س ش ص ض ط ظ ل ن.',
    [['الشَّمْس','[ash-sh]ams','the sun'],['السَّلامُ عَلَيْكُم','[as-s]alāmu ʿalaykum','peace be upon you']],
    ['How is الشَّمْس said?', ['ash-shams','al-shams','a-shams'], 0, 'ش is a sun letter: the ل goes quiet and the ش doubles.', 'الشَّمْس']],
  ['In a sentence, ال drops its "a"', 'In a flowing sentence, the a of ال isn’t said: you go straight from the word before to the l. فِي الْبَيْتِ is said "fil-bayti" (the ī of فِي shortens), not "fī al-bayti". The same happens in بِسْمِ اللهِ: bismillāh.',
    [['فِي الْبَيْتِ','f[il]-bayti','in the house'],['بِسْمِ اللهِ','bism[ill]āh','in the name of Allah']],
    ['How is فِي الْبَيْتِ said?', ['fil-bayti','fī al-bayti','fī-bayti'], 0, 'After the vowel of فِي, the a of ال drops out.', 'فِي الْبَيْتِ']],
  ['Stopping: leave off the last vowel', 'At the end of a sentence, or whenever you pause, the last short vowel isn’t said, nor the -n of -un: هَذا بَيْتٌ is "hādhā bayt". Inside a sentence you say them. This app shows every ending, so you always know what they are.',
    [['بَيْتٌ','bayt (at a stop), bayt[un] (inside a sentence)','a house'],['السَّلامُ عَلَيْكُم','as-salām[u] ʿalaykum','peace be upon you']],
    ['You end a sentence on بَيْتٌ. How do you say it?', ['bayt','baytun','bayta'], 0, 'At a stop, the last vowel and the -n aren’t said.', 'بَيْتٌ']],
];
/* The listening test at the end of the unit: a word is played, the learner picks
   its first letter from letters that sound alike. [word, first letter, options,
   meaning]. Every word here has a recorded clip. */
const LISTEN_TEST = [
  ['سَمَك','س','سصث','fish'],   ['صَباح','ص','سصث','morning'], ['ثَلاثَة','ث','سصث','three'],
  ['تَمْر','ت','تط','dates'],    ['طَعام','ط','تط','food'],
  ['دَجاج','د','دضذ','chicken'], ['ضُيُوف','ض','دضذ','guests'], ['ذِراع','ذ','ذزظ','arm'],
  ['زَيْتون','ز','ذزظ','olives'], ['ظُهْرًا','ظ','ذزظ','at noon'],
  ['حَلِيب','ح','حهخ','milk'],   ['هَذا','ه','حهخ','this'],    ['خُبْز','خ','حهخ','bread'],
  ['كِتاب','ك','كقغ','book'],    ['قَهْوَة','ق','كقغ','coffee'],
  ['عَشَرَة','ع','عاه','ten'],    ['أَنا','ا','عاه','I'],
  ['غُرْفَة','غ','غخر','room'],
];
