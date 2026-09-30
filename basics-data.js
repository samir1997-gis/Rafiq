/* The basics (#165): a short section between the reading starter and unit 1. It teaches the
   building blocks simply, then tests them simply: single words and two- or three-word sentences.
   Order and length chosen with TypeSafe (tools/typesafe-exp/basics_section.py).

   Each lesson: {key, title, words (word-list ids it uses, which count as met when it's done),
   teach: [{h, pairs: [[arabic, english], ...], en}], drills: [[question, arabic shown or '',
   options (the right one first; shown shuffled), why]]}. Missed drills come back at the end of
   the lesson. The Arabic is listed for the teacher in tools/teach/REVIEW.md. */
const BASICS = [
  {key:'the', title:'‘The’ and ‘a’', words:[90, 150, 62, 627, 520],
   teach:[
    {h:'ال means ‘the’', pairs:[['بَيْتٌ','a house'],['الْبَيْتُ','the house']],
     en:'Put ال on the front of a word for ‘the’. There’s no word for ‘a’: the -un ending (ٌ) does that job. A word has one or the other, never both.'},
    {h:'Sun letters: the ل goes quiet', pairs:[['الْكِتابُ','al-kitāb: the book'],['الشَّمْسُ','ash-shams: the sun']],
     en:'Before half the letters (like ك, ب, م, ق) you say al-. Before the other half, the sun letters (like ش, س, ت, د, ر, ن), the ل is silent and the next letter doubles.'}],
   drills:[
    ['How do you say ‘the book’?', '', ['الْكِتابُ','كِتابٌ','الْكِتابٌ'], 'ال for ‘the’, and then no -un.'],
    ['How do you say ‘a mosque’?', '', ['مَسْجِدٌ','الْمَسْجِدُ','الْمَسْجِدٌ'], 'No ال, and the -un ending.'],
    ['What does it mean?', 'الْبابُ', ['the door','a door','doors'], 'ال: ‘the’.'],
    ['What does it mean?', 'بَيْتٌ', ['a house','the house','my house'], 'The -un ending: ‘a’.'],
    ['How is it said?', 'الشَّمْسُ', ['ash-shams','al-shams'], 'ش is a sun letter: the ل goes quiet.'],
    ['How is it said?', 'الْبابُ', ['al-bāb','ab-bāb'], 'ب is a moon letter: you say the ل.'],
    ['How is it said?', 'الطّالِبُ', ['aṭ-ṭālib','al-ṭālib'], 'ط is a sun letter: the ل goes quiet.'],
    ['How is it said?', 'الْمَسْجِدُ', ['al-masjid','am-masjid'], 'م is a moon letter: you say the ل.']]},

  {key:'gender', title:'Masculine and feminine', words:[30, 26, 27, 58, 28, 298, 29, 50, 33, 468, 75, 149],
   teach:[
    {h:'Look for ة', pairs:[['مُدَرِّسٌ','a teacher (a man)'],['مُدَرِّسَةٌ','a teacher (a woman)'],['صَدِيقٌ','a friend (a man)'],['صَدِيقَةٌ','a friend (a woman)']],
     en:'Every Arabic noun, a person or a thing, is masculine or feminine. Most feminine nouns end in ة, and adding ة to a man’s word often makes the woman’s: مُدَرِّس → مُدَرِّسَة. Things too: بَيْتٌ (a house) is masculine, غُرْفَةٌ (a room) is feminine.'},
    {h:'A few are feminine without ة', pairs:[['أُمٌّ','a mother'],['أُخْتٌ','a sister'],['بِنْتٌ','a girl']],
     en:'These mean a woman, so they’re feminine even without ة.'}],
   drills:[
    ['Masculine or feminine?', 'مُدَرِّسَةٌ', ['feminine','masculine'], 'It ends in ة.'],
    ['Masculine or feminine?', 'صَدِيقٌ', ['masculine','feminine'], 'No ة, and it means a man.'],
    ['Masculine or feminine?', 'أُمٌّ', ['feminine','masculine'], 'No ة, but a mother is a woman.'],
    ['Masculine or feminine?', 'غُرْفَةٌ', ['feminine','masculine'], 'It ends in ة.'],
    ['Make it feminine', 'طالِبٌ', ['طالِبَةٌ','طالِبٌ','طُلّابٌ'], 'Add ة: طالِبَة.'],
    ['Make it feminine', 'طَبِيبٌ', ['طَبِيبَةٌ','طَبِيبٌ','طالِبَةٌ'], 'Add ة: طَبِيبَة.'],
    ['Which one is a woman?', '', ['صَدِيقَةٌ','صَدِيقٌ','مُدَرِّسٌ'], 'صَدِيقَة ends in ة.'],
    ['Which one is feminine?', '', ['أُخْتٌ','كِتابٌ','بَيْتٌ'], 'A sister is a woman: feminine, even without ة.']]},

  {key:'people', title:'I, you, he, she', words:[15, 16, 17, 18, 19, 30, 28, 29, 298],
   teach:[
    {h:'I, you, he, she', pairs:[['أَنا','I'],['أَنْتَ','you (to a man)'],['أَنْتِ','you (to a woman)'],['هُوَ','he'],['هِيَ','she']],
     en:'‘You’ has two forms: أَنْتَ to a man, أَنْتِ to a woman.'},
    {h:'No word for ‘is’', pairs:[['أَنا مُدَرِّسٌ','I’m a teacher'],['هِيَ طالِبَةٌ','She’s a student'],['أَنا مُدَرِّسٌ وَهِيَ طالِبَةٌ','I’m a teacher and she’s a student']],
     en:'In the present, Arabic just puts the two words side by side: ‘I teacher’. وَ means ‘and’, written joined to the next word.'}],
   drills:[
    ['Which fits?', '___ طالِبَةٌ', ['هِيَ','هُوَ'], 'طالِبَة is a woman: هِيَ.'],
    ['Which fits?', '___ مُدَرِّسٌ', ['هُوَ','هِيَ'], 'مُدَرِّس is a man: هُوَ.'],
    ['How do you say ‘I’m a teacher’ (a man)?', '', ['أَنا مُدَرِّسٌ','أَنْتَ مُدَرِّسٌ','هُوَ مُدَرِّسٌ'], 'أَنا is ‘I’.'],
    ['How do you say ‘you’re a doctor’ to a woman?', '', ['أَنْتِ طَبِيبَةٌ','أَنْتَ طَبِيبٌ','هِيَ طَبِيبَةٌ'], 'To a woman: أَنْتِ, and طَبِيبَة with ة.'],
    ['What does it mean?', 'هُوَ طَبِيبٌ', ['He’s a doctor','She’s a doctor','I’m a doctor'], 'هُوَ is ‘he’.'],
    ['What does it mean?', 'أَنْتَ طالِبٌ', ['You’re a student (to a man)','You’re a student (to a woman)','I’m a student'], 'أَنْتَ: ‘you’ to a man.'],
    ['Which fits?', 'أَنا مُدَرِّسٌ وَهِيَ ___', ['طالِبَةٌ','طالِبٌ'], 'After هِيَ, the feminine: طالِبَة.'],
    ['Which fits?', 'هِيَ ___', ['طَبِيبَةٌ','طَبِيبٌ'], 'After هِيَ, the feminine: طَبِيبَة.']]},

  {key:'this', title:'This one, and describing words', words:[20, 21, 90, 75, 62, 149, 161, 639, 468, 454],
   teach:[
    {h:'هَذا and هَذِهِ', pairs:[['هَذا بَيْتٌ','This is a house'],['هَذِهِ غُرْفَةٌ','This is a room']],
     en:'‘This’ is هَذا for a masculine word and هَذِهِ for a feminine one.'},
    {h:'Describing words come after, and match', pairs:[['بَيْتٌ كَبِيرٌ','a big house'],['غُرْفَةٌ كَبِيرَةٌ','a big room']],
     en:'A describing word comes after the noun and matches it: with ة if the noun is feminine.'},
    {h:'Plurals of things take هَذِهِ', pairs:[['هَذِهِ كُتُبٌ','These are books'],['هَذِهِ غُرَفٌ','These are rooms']],
     en:'A plural of things (not people) is treated as feminine: هَذِهِ, not هَذا.'}],
   drills:[
    ['Which fits?', '___ مَسْجِدٌ', ['هَذا','هَذِهِ'], 'مَسْجِد is masculine: هَذا.'],
    ['Which fits?', '___ مَدْرَسَةٌ', ['هَذِهِ','هَذا'], 'مَدْرَسَة ends in ة: هَذِهِ.'],
    ['Which fits?', '___ أُمِّي', ['هَذِهِ','هَذا'], 'A mother is feminine, even without ة.'],
    ['How do you say ‘a big room’?', '', ['غُرْفَةٌ كَبِيرَةٌ','غُرْفَةٌ كَبِيرٌ','كَبِيرَةٌ غُرْفَةٌ'], 'The describing word comes after, with ة for a feminine noun.'],
    ['How do you say ‘a big house’?', '', ['بَيْتٌ كَبِيرٌ','بَيْتٌ كَبِيرَةٌ','كَبِيرٌ بَيْتٌ'], 'بَيْت is masculine: no ة.'],
    ['Which fits?', 'هَذا وَلَدٌ وَهَذِهِ ___', ['بِنْتٌ','وَلَدٌ'], 'هَذِهِ goes with a feminine word: بِنْت.'],
    ['How do you say ‘these are books’?', '', ['هَذِهِ كُتُبٌ','هَذا كُتُبٌ'], 'A plural of things takes هَذِهِ.'],
    ['What does it mean?', 'هَذِهِ مَدْرَسَةٌ كَبِيرَةٌ', ['This is a big school','This is a big house','This is a school'], 'مَدْرَسَة is a school, and كَبِيرَة is big.']]},

  {key:'many', title:'One and many', words:[58, 299, 639, 51, 150, 454, 75, 92],
   teach:[
    {h:'Many plurals change inside the word', pairs:[['طالِبٌ · طُلّابٌ','a student · students'],['وَلَدٌ · أَوْلادٌ','a boy · boys'],['كِتابٌ · كُتُبٌ','a book · books'],['غُرْفَةٌ · غُرَفٌ','a room · rooms']],
     en:'Some plurals add an ending, but many change the inside of the word. There’s no simple rule, so learn each word with its plural.'},
    {h:'We, you (a group), they', pairs:[['نَحْنُ طُلّابٌ','We’re students'],['أَنْتُمْ طُلّابٌ','You’re students (to a group)'],['هُمْ أَوْلادٌ','They’re boys']],
     en:'For more than one person: نَحْنُ we, أَنْتُمْ you, هُمْ they (for men or a mixed group; a group of only women has its own forms, which come later). Still no word for ‘are’.'}],
   drills:[
    ['What’s the plural?', 'كِتابٌ', ['كُتُبٌ','كِتابٌ','كُتُبِي'], 'كِتاب changes inside: كُتُب.'],
    ['What’s the plural?', 'وَلَدٌ', ['أَوْلادٌ','وَلَدٌ','بِنْتٌ'], 'وَلَد changes inside: أَوْلاد.'],
    ['What’s the plural?', 'طالِبٌ', ['طُلّابٌ','طالِبَةٌ','طالِبٌ'], 'طالِب changes inside: طُلّاب.'],
    ['One, or more than one?', 'غُرَفٌ', ['more than one','one'], 'غُرَف is the plural of غُرْفَة.'],
    ['One, or more than one?', 'كِتابٌ', ['one','more than one'], 'كِتاب is one book; books are كُتُب.'],
    ['How do you say ‘we’re students’?', '', ['نَحْنُ طُلّابٌ','هُمْ طُلّابٌ','أَنا طالِبٌ'], 'نَحْنُ is ‘we’.'],
    ['How do you say ‘they’re boys’?', '', ['هُمْ أَوْلادٌ','نَحْنُ أَوْلادٌ','هُوَ وَلَدٌ'], 'هُمْ is ‘they’.'],
    ['Which fits?', 'أَنْتُمْ ___', ['طُلّابٌ','طالِبٌ'], 'أَنْتُمْ is more than one person: the plural.']]},

  {key:'my', title:'My, your, his, her', words:[50, 32, 75, 150, 90, 26, 27, 149],
   teach:[
    {h:'Endings for ‘my’, ‘your’, ‘his’, ‘her’', pairs:[['أُمِّي','my mother'],['أُمُّكَ','your mother (to a man)'],['أُمُّكِ','your mother (to a woman)'],['أُمُّهُ','his mother'],['أُمُّها','her mother']],
     en:'There’s no separate word: add an ending. ـِي my, ـكَ / ـكِ your, ـهُ his, ـها her.'},
    {h:'ة becomes ت', pairs:[['مَدْرَسَةٌ','a school'],['مَدْرَسَتِي','my school']],
     en:'When an ending is added, ة is written and said as ت: غُرْفَة → غُرْفَتِي, my room.'}],
   drills:[
    ['How do you say ‘my brother’?', '', ['أَخِي','أَخٌ','الْأَخُ'], 'Add ـِي for ‘my’.'],
    ['How do you say ‘my room’?', '', ['غُرْفَتِي','غُرْفَةِي','غُرْفَتُكَ'], 'ة becomes ت, then ـِي.'],
    ['How do you say ‘your book’ to a woman?', '', ['كِتابُكِ','كِتابُكَ','كِتابِي'], 'To a woman: ـكِ.'],
    ['How do you say ‘her house’?', '', ['بَيْتُها','بَيْتُهُ','بَيْتِي'], '‘Her’ is ـها.'],
    ['What does it mean?', 'صَدِيقُهُ', ['his friend','her friend','my friend'], 'ـهُ is ‘his’.'],
    ['How do you say ‘my friend’ (a woman)?', '', ['صَدِيقَتِي','صَدِيقِي','صَدِيقَةِي'], 'صَدِيقَة: ة becomes ت, then ـِي.'],
    ['What does it mean?', 'مَدْرَسَتُها', ['her school','his school','my school'], 'ـها is ‘her’; ة became ت.'],
    ['Which fits?', 'هَذا ___', ['بَيْتِي','الْبَيْتِي'], 'A word with ‘my’ doesn’t take ال too.']]},
];
