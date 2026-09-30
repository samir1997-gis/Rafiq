/* The basics (#165, #168): a short section between the reading starter and unit 1. It has a goal:
   by the end you can say BASICS_GOAL. Each lesson teaches one building block and adds a piece of that
   sentence, shown at the end as "your sentence so far". Chosen with TypeSafe
   (tools/typesafe-exp/basics_goal.py: simpler, less overload and better recall than without a goal).

   Each lesson: {key, title, words (word-list ids it uses, which count as met when it's done),
   teach: [{h, pairs: [[arabic, english], ...], en}], drills: [[question, arabic shown or '',
   options (the right one first; shown shuffled), why]], sofar: {m, f, en, adds}} — the sentence
   so far as a man and as a woman says it, its meaning, and the part this lesson added. Missed drills
   come back at the end of the lesson. The names are examples: the learner says their own.
   The Arabic is listed for the teacher in tools/teach/REVIEW.md. */
const BASICS_GOAL = {m:'السَّلامُ عَلَيْكُمْ، اسْمِي سَمِير، وَأَنا طالِبُ اللُّغَةِ الْعَرَبِيَّةِ.',
                     f:'السَّلامُ عَلَيْكُمْ، اسْمِي مَرْيَم، وَأَنا طالِبَةُ اللُّغَةِ الْعَرَبِيَّةِ.',
                     en:'Peace be upon you. My name is …, and I’m a student of the Arabic language.'};
const BASICS = [
  {key:'the', title:'‘The’ and ‘a’', words:[90, 150, 62, 627, 520, 1],
   teach:[
    {h:'ال means ‘the’', pairs:[['بَيْتٌ','a house'],['الْبَيْتُ','the house']],
     en:'Put ال on the front of a word for ‘the’. There’s no word for ‘a’: the -un ending (ٌ) does that job. A word has one or the other, never both.'},
    {h:'Sun letters: the ل goes quiet', pairs:[['الْكِتابُ','al-kitāb: the book'],['الشَّمْسُ','ash-shams: the sun'],['السَّلامُ','as-salām: (the) peace']],
     en:'Before half the letters (like ك, ب, م, ق) you say al-. Before the other half, the sun letters (like ش, س, ت, د, ر, ن), the ل is silent and the next letter doubles. That’s why the greeting is as-salām.'}],
   drills:[
    ['How do you say ‘the book’?', '', ['الْكِتابُ','كِتابٌ','الْكِتابٌ'], 'ال for ‘the’, and then no -un.'],
    ['How do you say ‘a mosque’?', '', ['مَسْجِدٌ','الْمَسْجِدُ','الْمَسْجِدٌ'], 'No ال, and the -un ending.'],
    ['What does it mean?', 'الْبابُ', ['the door','a door','doors'], 'ال: ‘the’.'],
    ['What does it mean?', 'بَيْتٌ', ['a house','the house','my house'], 'The -un ending: ‘a’.'],
    ['How is it said?', 'السَّلامُ', ['as-salām','al-salām'], 'س is a sun letter: the ل goes quiet.'],
    ['How is it said?', 'الشَّمْسُ', ['ash-shams','al-shams'], 'ش is a sun letter: the ل goes quiet.'],
    ['How is it said?', 'الْبابُ', ['al-bāb','ab-bāb'], 'ب is a moon letter: you say the ل.'],
    ['How is it said?', 'الْمَسْجِدُ', ['al-masjid','am-masjid'], 'م is a moon letter: you say the ل.']],
   sofar:{m:'السَّلامُ عَلَيْكُمْ', f:'السَّلامُ عَلَيْكُمْ', en:'Peace be upon you. (السَّلامُ: the peace; عَلَيْكُمْ: upon you)', adds:'السَّلامُ عَلَيْكُمْ'}},

  {key:'my', title:'My, your, his, her', words:[784, 50, 32, 75, 150, 90, 26, 27, 149],
   teach:[
    {h:'Endings for ‘my’, ‘your’, ‘his’, ‘her’', pairs:[['اسْمٌ','a name'],['اسْمِي','my name'],['اسْمُكَ','your name (to a man)'],['اسْمُكِ','your name (to a woman)'],['اسْمُهُ','his name'],['اسْمُها','her name']],
     en:'There’s no separate word: add an ending. ـِي my, ـكَ / ـكِ your, ـهُ his, ـها her.'},
    {h:'ة becomes ت', pairs:[['مَدْرَسَةٌ','a school'],['مَدْرَسَتِي','my school']],
     en:'When an ending is added, ة is written and said as ت: غُرْفَة → غُرْفَتِي, my room.'}],
   drills:[
    ['How do you say ‘my name’?', '', ['اسْمِي','اسْمُكَ','الاِسْمُ'], 'Add ـِي for ‘my’.'],
    ['How do you say ‘my brother’?', '', ['أَخِي','أَخٌ','الْأَخُ'], 'Add ـِي for ‘my’.'],
    ['How do you say ‘my room’?', '', ['غُرْفَتِي','غُرْفَةِي','غُرْفَتُكَ'], 'ة becomes ت, then ـِي.'],
    ['How do you say ‘your book’ to a woman?', '', ['كِتابُكِ','كِتابُكَ','كِتابِي'], 'To a woman: ـكِ.'],
    ['How do you say ‘her house’?', '', ['بَيْتُها','بَيْتُهُ','بَيْتِي'], '‘Her’ is ـها.'],
    ['What does it mean?', 'اسْمُهُ', ['his name','her name','my name'], 'ـهُ is ‘his’.'],
    ['How do you say ‘my mother’?', '', ['أُمِّي','أُمٌّ','الْأُمُّ'], 'Add ـِي for ‘my’.'],
    ['What does it mean?', 'مَدْرَسَتُها', ['her school','his school','my school'], 'ـها is ‘her’; ة became ت.']],
   sofar:{m:'السَّلامُ عَلَيْكُمْ، اسْمِي سَمِير', f:'السَّلامُ عَلَيْكُمْ، اسْمِي مَرْيَم', en:'Peace be upon you. My name is …', adds:'اسْمِي'}},

  {key:'people', title:'I, you, he, she', words:[15, 16, 17, 18, 19, 30, 28, 29, 298, 58],
   teach:[
    {h:'I, you, he, she', pairs:[['أَنا','I'],['أَنْتَ','you (to a man)'],['أَنْتِ','you (to a woman)'],['هُوَ','he'],['هِيَ','she']],
     en:'‘You’ has two forms: أَنْتَ to a man, أَنْتِ to a woman.'},
    {h:'No word for ‘is’', pairs:[['أَنا طالِبٌ','I’m a student'],['هُوَ مُدَرِّسٌ','He’s a teacher'],['أَنا طالِبٌ وَهُوَ مُدَرِّسٌ','I’m a student and he’s a teacher']],
     en:'In the present, Arabic just puts the two words side by side: ‘I student’. وَ means ‘and’, written joined to the next word.'}],
   drills:[
    ['What does it mean?', 'هِيَ', ['she','he','I'], 'هِيَ is ‘she’.'],
    ['How do you say ‘you’ to a woman?', '', ['أَنْتِ','أَنْتَ','أَنا'], 'To a woman: أَنْتِ.'],
    ['How do you say ‘I’m a student’ (a man)?', '', ['أَنا طالِبٌ','أَنْتَ طالِبٌ','هُوَ طالِبٌ'], 'أَنا is ‘I’.'],
    ['How do you say ‘he’s a student’?', '', ['هُوَ طالِبٌ','أَنا طالِبٌ','أَنْتَ طالِبٌ'], 'هُوَ is ‘he’.'],
    ['What does it mean?', 'هُوَ طَبِيبٌ', ['He’s a doctor','She’s a doctor','I’m a doctor'], 'هُوَ is ‘he’.'],
    ['What does it mean?', 'أَنْتَ طالِبٌ', ['You’re a student (to a man)','You’re a student (to a woman)','I’m a student'], 'أَنْتَ: ‘you’ to a man.'],
    ['Which fits?', 'أَنا طالِبٌ وَهُوَ ___', ['مُدَرِّسٌ','أَنا'], '‘and he’s a teacher’: وَهُوَ مُدَرِّسٌ.'],
    ['What does it mean?', 'وَأَنا طالِبٌ', ['and I’m a student','I’m not a student','and he’s a student'], 'وَ is ‘and’, أَنا is ‘I’.']],
   sofar:{m:'السَّلامُ عَلَيْكُمْ، اسْمِي سَمِير، وَأَنا طالِبٌ', f:'السَّلامُ عَلَيْكُمْ، اسْمِي مَرْيَم، وَأَنا طالِبَةٌ', en:'Peace be upon you. My name is …, and I’m a student. (Why a woman says طالِبَةٌ: next lesson.)', adds:'وَأَنا'}},

  {key:'gender', title:'Masculine and feminine', words:[30, 26, 27, 58, 28, 298, 29, 50, 33, 468, 75, 149, 20, 21, 62],
   teach:[
    {h:'Look for ة', pairs:[['طالِبٌ','a student (a man)'],['طالِبَةٌ','a student (a woman)'],['صَدِيقٌ','a friend (a man)'],['صَدِيقَةٌ','a friend (a woman)']],
     en:'Every Arabic noun, a person or a thing, is masculine or feminine. Most feminine nouns end in ة, and adding ة to a man’s word often makes the woman’s: طالِب → طالِبَة. Things too: بَيْتٌ (a house) is masculine, غُرْفَةٌ (a room) is feminine.'},
    {h:'A few are feminine without ة', pairs:[['أُمٌّ','a mother'],['أُخْتٌ','a sister'],['بِنْتٌ','a girl']],
     en:'These mean a woman, so they’re feminine even without ة.'},
    {h:'‘This’: هَذا and هَذِهِ', pairs:[['هَذا بَيْتٌ','This is a house'],['هَذِهِ غُرْفَةٌ','This is a room']],
     en:'‘This’ is هَذا for a masculine word and هَذِهِ for a feminine one.'}],
   drills:[
    ['Masculine or feminine?', 'طالِبَةٌ', ['feminine','masculine'], 'It ends in ة.'],
    ['Masculine or feminine?', 'صَدِيقٌ', ['masculine','feminine'], 'No ة, and it means a man.'],
    ['Masculine or feminine?', 'أُمٌّ', ['feminine','masculine'], 'No ة, but a mother is a woman.'],
    ['Make it feminine', 'طَبِيبٌ', ['طَبِيبَةٌ','طَبِيبٌ','طالِبَةٌ'], 'Add ة: طَبِيبَة.'],
    ['Make it feminine', 'مُدَرِّسٌ', ['مُدَرِّسَةٌ','مُدَرِّسٌ','مَدْرَسَةٌ'], 'Add ة: مُدَرِّسَة.'],
    ['Which fits?', '___ مَسْجِدٌ', ['هَذا','هَذِهِ'], 'مَسْجِد is masculine: هَذا.'],
    ['Which fits?', '___ مَدْرَسَةٌ', ['هَذِهِ','هَذا'], 'مَدْرَسَة ends in ة: هَذِهِ.'],
    ['A woman says ‘I’m a student’:', '', ['أَنا طالِبَةٌ','أَنا طالِبٌ','هِيَ طالِبٌ'], 'A woman: طالِبَة, with ة.']],
   sofar:{m:'السَّلامُ عَلَيْكُمْ، اسْمِي سَمِير، وَأَنا طالِبٌ', f:'السَّلامُ عَلَيْكُمْ، اسْمِي مَرْيَم، وَأَنا طالِبَةٌ', en:'Peace be upon you. My name is …, and I’m a student. (A man says طالِبٌ, a woman طالِبَةٌ.)', adds:'طالِب'}},

  {key:'of', title:'‘Of’, and describing words', words:[785, 58, 28, 150, 90, 627, 75, 161, 449],
   teach:[
    {h:'‘Of’: two nouns side by side', pairs:[['بابُ الْبَيْتِ','the door of the house'],['كِتابُ الطّالِبِ','the student’s book (the book of the student)'],['طالِبُ اللُّغَةِ','a student of the language']],
     en:'There’s no separate word for ‘of’: put the two nouns side by side. The first loses ال and the -un ending; the second ends in -i.'},
    {h:'Describing words come after, and match', pairs:[['بَيْتٌ كَبِيرٌ','a big house'],['غُرْفَةٌ كَبِيرَةٌ','a big room'],['اللُّغَةُ الْعَرَبِيَّةُ','the Arabic language']],
     en:'A describing word comes after the noun and matches it: ة if the noun is feminine, and ال if the noun has ال. لُغَة (language) is feminine, so it’s الْعَرَبِيَّة.'}],
   drills:[
    ['How do you say ‘a student of the language’?', '', ['طالِبُ اللُّغَةِ','طالِبٌ اللُّغَةُ','الطّالِبُ اللُّغَةِ'], 'Side by side: the first word loses ال and -un.'],
    ['How do you say ‘the student’s book’?', '', ['كِتابُ الطّالِبِ','الْكِتابُ الطّالِبِ','كِتابٌ الطّالِبُ'], 'كِتابُ, then الطّالِبِ ending in -i.'],
    ['What does it mean?', 'بابُ الْبَيْتِ', ['the door of the house','a big door','the house'], 'Two nouns side by side: ‘of’.'],
    ['How do you say ‘the Arabic language’?', '', ['اللُّغَةُ الْعَرَبِيَّةُ','اللُّغَةُ عَرَبِيٌّ','لُغَةٌ الْعَرَبِيَّةُ'], 'The describing word matches: ال and ة.'],
    ['How do you say ‘a big room’?', '', ['غُرْفَةٌ كَبِيرَةٌ','غُرْفَةٌ كَبِيرٌ','كَبِيرَةٌ غُرْفَةٌ'], 'After the noun, with ة for a feminine noun.'],
    ['How do you say ‘a big house’?', '', ['بَيْتٌ كَبِيرٌ','بَيْتٌ كَبِيرَةٌ','كَبِيرٌ بَيْتٌ'], 'بَيْت is masculine: no ة.'],
    ['Which fits?', 'طالِبُ اللُّغَةِ ___', ['الْعَرَبِيَّةِ','عَرَبِيَّةٌ'], 'It matches اللُّغَةِ: ال, ة and -i.'],
    ['A woman says ‘I’m a student of the Arabic language’:', '', ['أَنا طالِبَةُ اللُّغَةِ الْعَرَبِيَّةِ','أَنا طالِبُ اللُّغَةِ الْعَرَبِيَّةِ','أَنا طالِبَةٌ اللُّغَةُ الْعَرَبِيَّةُ'], 'طالِبَة for a woman; side by side, no -un.']],
   sofar:{m:BASICS_GOAL.m, f:BASICS_GOAL.f, en:BASICS_GOAL.en, adds:'اللُّغَةِ الْعَرَبِيَّةِ'}},

  {key:'many', title:'One and many', words:[58, 299, 639, 51, 150, 454, 75, 92],
   teach:[
    {h:'Many plurals change inside the word', pairs:[['طالِبٌ · طُلّابٌ','a student · students'],['وَلَدٌ · أَوْلادٌ','a boy · boys'],['كِتابٌ · كُتُبٌ','a book · books'],['غُرْفَةٌ · غُرَفٌ','a room · rooms']],
     en:'Some plurals add an ending, but many change the inside of the word. There’s no simple rule, so learn each word with its plural. A plural of things takes هَذِهِ: هَذِهِ كُتُبٌ, these are books.'},
    {h:'We, you (a group), they', pairs:[['نَحْنُ طُلّابٌ','We’re students'],['أَنْتُمْ طُلّابٌ','You’re students (to a group)'],['هُمْ أَوْلادٌ','They’re boys']],
     en:'For more than one person: نَحْنُ we, أَنْتُمْ you, هُمْ they (for men or a mixed group; a group of only women has its own forms, which come later). Still no word for ‘are’.'}],
   drills:[
    ['What’s the plural?', 'كِتابٌ', ['كُتُبٌ','كِتابٌ','كُتُبِي'], 'كِتاب changes inside: كُتُب.'],
    ['What’s the plural?', 'وَلَدٌ', ['أَوْلادٌ','وَلَدٌ','بِنْتٌ'], 'وَلَد changes inside: أَوْلاد.'],
    ['What’s the plural?', 'طالِبٌ', ['طُلّابٌ','طالِبَةٌ','طالِبٌ'], 'طالِب changes inside: طُلّاب.'],
    ['One, or more than one?', 'غُرَفٌ', ['more than one','one'], 'غُرَف is the plural of غُرْفَة.'],
    ['How do you say ‘these are books’?', '', ['هَذِهِ كُتُبٌ','هَذا كُتُبٌ'], 'A plural of things takes هَذِهِ.'],
    ['How do you say ‘we’re students’?', '', ['نَحْنُ طُلّابٌ','هُمْ طُلّابٌ','أَنا طالِبٌ'], 'نَحْنُ is ‘we’.'],
    ['How do you say ‘they’re boys’?', '', ['هُمْ أَوْلادٌ','نَحْنُ أَوْلادٌ','هُوَ وَلَدٌ'], 'هُمْ is ‘they’.'],
    ['Which fits?', 'نَحْنُ ___ اللُّغَةِ الْعَرَبِيَّةِ', ['طُلّابُ','طالِبُ'], 'نَحْنُ is more than one: the plural, طُلّاب.']],
   sofar:{m:'نَحْنُ طُلّابُ اللُّغَةِ الْعَرَبِيَّةِ', f:'نَحْنُ طُلّابُ اللُّغَةِ الْعَرَبِيَّةِ', en:'A bonus: we’re students of the Arabic language.', adds:'نَحْنُ طُلّابُ', bonus:true}},
];

/* The learner's own name in the goal sentence (#169): the first name given at sign-up, written in
   Arabic when it's a common name with a standard spelling (English spellings on the left). Anything
   else is shown as typed. Each Arabic name has a recorded clip; checked with TypeSafe
   (tools/typesafe-exp/names_check.py) and listed for the teacher in tools/teach/REVIEW.md. */
const BASICS_NAMES = (() => {
  const L = {
    // men
    'مُحَمَّد':'muhammad mohammed mohammad mohamed muhammed mohamad mohd', 'أَحْمَد':'ahmed ahmad', 'مَحْمُود':'mahmood mahmoud mahmud',
    'عَلِيّ':'ali', 'عُمَر':'omar umar', 'عُثْمان':'usman uthman osman othman', 'حَسَن':'hassan hasan', 'حُسَيْن':'hussain hussein husain husein hossain',
    'إِبْراهِيم':'ibrahim ebrahim', 'يُوسُف':'yusuf yousuf yousef yusef youssef', 'آدَم':'adam', 'إِدْرِيس':'idris idrees', 'عِمْران':'imran',
    'عِرْفان':'irfan', 'فَيْصَل':'faisal faysal', 'زَيْد':'zaid zayd', 'خالِد':'khalid khaled', 'طارِق':'tariq tarik tareq', 'سَمِير':'samir sameer',
    'أَمِير':'amir ameer', 'كَرِيم':'karim kareem', 'عَبْدُ اللهِ':'abdullah abdallah', 'عَبْدُ الرَّحْمَن':'abdulrahman abdurrahman abdelrahman',
    'بِلال':'bilal', 'حَمْزَة':'hamza hamzah', 'إِسْماعِيل':'ismail ismael', 'إِلْياس':'ilyas elias', 'يُونُس':'yunus younus younis',
    'مُوسَى':'musa moosa', 'عِيسَى':'isa eesa issa', 'داوُد':'dawud dawood daud', 'سُلَيْمان':'sulaiman sulayman suleman suleiman',
    'زَكَرِيّا':'zakariya zakaria zakariyya', 'يَحْيَى':'yahya', 'نُوح':'nuh nooh', 'هارُون':'harun haroon', 'إِسْحاق':'ishaq', 'يَعْقُوب':'yaqub yakub yaqoob',
    'أَيُّوب':'ayub ayoub ayyub', 'سَلْمان':'salman', 'رَيّان':'rayyan rayan', 'زُبَيْر':'zubair zubayr', 'سَعِيد':'saeed sayeed', 'رَشِيد':'rashid rasheed',
    'مالِك':'malik', 'ياسِر':'yasir yasser yaser', 'ناصِر':'nasir nasser naser', 'جَمال':'jamal', 'كَمال':'kamal', 'شَرِيف':'sharif shareef',
    'عادِل':'adil adel', 'عارِف':'arif', 'نَبِيل':'nabil nabeel', 'وَسِيم':'wasim waseem', 'عَزِيز':'aziz', 'رَحِيم':'rahim raheem',
    'أُسامَة':'usama osama usamah', 'مُصْطَفَى':'mustafa mostafa', 'أَنَس':'anas', 'مُعاذ':'muadh muaz moaz', 'سُفْيان':'sufyan sufian',
    'حامِد':'hamid hamed', 'عَمّار':'ammar', 'عَدْنان':'adnan', 'هِشام':'hisham', 'آصِف':'asif', 'نُعْمان':'numan nouman',
    // women
    'مَرْيَم':'maryam mariam mariyam maryum', 'عائِشَة':'aisha ayesha aishah ayisha aysha', 'فاطِمَة':'fatima fatimah fatema',
    'خَدِيجَة':'khadija khadijah', 'زَيْنَب':'zainab zaynab', 'سارَة':'sara sarah', 'آمِنَة':'amina aminah ameena', 'حَفْصَة':'hafsa hafsah',
    'سُمَيَّة':'sumayya sumayyah sumaya sumaiya', 'صَفِيَّة':'safiya safiyyah safia safiyah', 'أَسْماء':'asma asmaa', 'نُور':'noor nur nour',
    'هُدَى':'huda hoda', 'ياسْمِين':'yasmin yasmeen', 'لَيْلَى':'layla laila leila lailah', 'رُقَيَّة':'ruqayya ruqayyah ruqaiya',
    'زَهْراء':'zahra zahraa', 'سَلْمَى':'salma', 'إِيمان':'iman eman imaan', 'نادِيَة':'nadia nadiya', 'رانِيَة':'rania raniya', 'هاجَر':'hajar',
    'حَلِيمَة':'halima halimah', 'جَمِيلَة':'jamila jameela', 'رَحْمَة':'rahma rahmah', 'هِبَة':'hiba heba', 'دُعاء':'dua duaa', 'شَيْماء':'shaima shaimaa',
    'عالِيَة':'aliya aaliyah aliyah aaliya', 'أَمِيرَة':'amira ameera', 'نُسَيْبَة':'nusaybah nusaiba', 'رَيْحانَة':'rehana raihana rayhana',
    'مَلِيكَة':'malika', 'آسِيَة':'asiya asiyah aasiya', 'بُشْرَى':'bushra', 'سُعاد':'suad', 'تَسْنِيم':'tasnim tasneem', 'أَنِيسَة':'anisa anisah',
    'نَبِيلَة':'nabila nabeela', 'سَمِيرَة':'samira sameera', 'كَرِيمَة':'karima kareema',
  };
  const m = {};
  Object.entries(L).forEach(([ar, en]) => en.split(' ').forEach(k => m[k] = ar));
  return m;
})();
