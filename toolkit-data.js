/* ── Connectors, sentence starters, and verb conjugation ────────────── */

const CONNECTORS=[
 {cat:"Adding",catAr:"الإِضافَة",items:[
  {ar:"وَ",en:"and",ex:"أَدْرُسُ الْعَرَبِيَّةَ وَالتَّارِيخَ.",exEn:"I study Arabic and history."},
  {ar:"أَيْضًا",en:"also, too",ex:"وَأَنا أَدْرُسُ الْعَرَبِيَّةَ أَيْضًا.",exEn:"I study Arabic too."},
  {ar:"كَذَلِكَ",en:"likewise",ex:"وَأُخْتِي كَذَلِكَ.",exEn:"And my sister likewise."},
  {ar:"بِالإِضافَةِ إِلى",en:"in addition to",ex:"بِالإِضافَةِ إِلى ذَلِكَ، الشَّقَّةُ قَرِيبَةٌ.",exEn:"In addition, the flat is nearby."}]},

 {cat:"Sequencing",catAr:"التَّرْتِيب",items:[
  {ar:"ثُمَّ",en:"then",ex:"أُصَلِّي، ثُمَّ أَتَناوَلُ الْفَطُورَ.",exEn:"I pray, then I have breakfast."},
  {ar:"بَعْدَ ذَلِكَ",en:"after that",ex:"بَعْدَ ذَلِكَ أَذْهَبُ إِلى الْعَمَلِ.",exEn:"After that I go to work."},
  {ar:"أَوَّلًا",en:"first",ex:"أَوَّلًا أَتَوَضَّأُ.",exEn:"First I do wudu."},
  {ar:"ثانِيًا",en:"secondly",ex:"ثانِيًا أَقْرَأُ الْقُرْآنَ.",exEn:"Secondly I read Qur'an."},
  {ar:"أَخِيرًا",en:"finally",ex:"وَأَخِيرًا أَنامُ.",exEn:"And finally I sleep."},
  {ar:"قَبْلَ أَنْ",en:"before (doing)",ex:"أَقْرَأُ قَبْلَ أَنْ أَنامَ.",exEn:"I read before I sleep."},
  {ar:"بَعْدَ أَنْ",en:"after (doing)",ex:"خَرَجْتُ بَعْدَ أَنْ أَكَلْتُ.",exEn:"I went out after I ate."},
  {ar:"عِنْدَما",en:"when",ex:"عِنْدَما يَكُونُ الْجَوُّ بارِدًا أَبْقى فِي الْبَيْتِ.",exEn:"When the weather is cold I stay home."}]},

 {cat:"Contrasting",catAr:"التَّضادّ",items:[
  {ar:"لَكِنَّ",en:"but (+ noun)",ex:"الْمَدِينَةُ كَبِيرَةٌ، لَكِنَّ فِيها ضَوْضاءَ.",exEn:"The city is big, but it's noisy."},
  {ar:"لَكِنْ",en:"but (+ verb)",ex:"أُحِبُّ الْقَهْوَةَ لَكِنْ لا أَشْرَبُها.",exEn:"I like coffee but I don't drink it."},
  {ar:"مَعَ ذَلِكَ",en:"nevertheless",ex:"الشَّقَّةُ غالِيَةٌ، وَمَعَ ذَلِكَ أُحِبُّها.",exEn:"The flat is expensive; even so I like it."},
  {ar:"بَلْ",en:"rather, but instead",ex:"لَسْتُ طالِبًا بَلْ مُدَرِّسٌ.",exEn:"I'm not a student but a teacher."}]},

 {cat:"Cause & result",catAr:"السَّبَب وَالنَّتِيجَة",items:[
  {ar:"لِأَنَّ",en:"because (+ noun)",ex:"آكُلُ قَلِيلًا لِأَنَّ وَزْنِي كَثِيرٌ.",exEn:"I eat little because my weight is high."},
  {ar:"لِأَنِّي",en:"because I",ex:"أَضَعُ الْمُنَبِّهَ لِأَنِّي كَسْلانُ.",exEn:"I set the alarm because I'm lazy."},
  {ar:"لِأَنَّها",en:"because she/it (f)",ex:"أُحِبُّ الْقِراءَةَ لِأَنَّها مُفِيدَةٌ.",exEn:"I like reading because it's useful."},
  {ar:"بِسَبَبِ",en:"because of (+ noun)",ex:"تَأَخَّرْتُ بِسَبَبِ الازْدِحامِ.",exEn:"I was late because of the traffic."},
  {ar:"لِذَلِكَ",en:"so, therefore",ex:"تُمْطِرُ، لِذَلِكَ أَخَذْتُ الْمِظَلَّةَ.",exEn:"It's raining, so I took the umbrella."},
  {ar:"لِهَذا",en:"for this reason",ex:"عَمَلِي بَعِيدٌ، لِهَذا أَسْتَيْقِظُ مُبَكِّرًا.",exEn:"My work is far, so I wake early."}]},

 {cat:"Condition",catAr:"الشَّرْط",items:[
  {ar:"إِذا",en:"if",ex:"إِذا كانَ عِنْدِي وَقْتٌ أَقْرَأُ.",exEn:"If I have time I read."},
  {ar:"إِنْ شاءَ اللهُ",en:"God willing",ex:"إِنْ شاءَ اللهُ أَزُورُكَ غَدًا.",exEn:"God willing I'll visit you tomorrow."},
  {ar:"لَوْ",en:"if (hypothetical)",ex:"لَوْ كُنْتُ غَنِيًّا لَسافَرْتُ.",exEn:"If I were rich I would travel."}]},

 {cat:"Examples",catAr:"التَّمْثِيل",items:[
  {ar:"مَثَلًا",en:"for example",ex:"أُحِبُّ الْفاكِهَةَ، مَثَلًا الْعِنَبَ.",exEn:"I like fruit, for example grapes."},
  {ar:"عَلى سَبِيلِ الْمِثالِ",en:"for instance",ex:"عَلى سَبِيلِ الْمِثالِ، هَذا الْكِتابُ مُفِيدٌ.",exEn:"For instance, this book is useful."},
  {ar:"مِثْلَ",en:"like, such as",ex:"أَهْوى الرِّياضَةَ مِثْلَ السِّباحَةِ.",exEn:"I like sport such as swimming."}]},

 {cat:"Opinion",catAr:"الرَّأْي",items:[
  {ar:"فِي رَأْيِي",en:"in my opinion",ex:"فِي رَأْيِي الْقَرْيَةُ أَهْدَأُ.",exEn:"In my opinion the village is quieter."},
  {ar:"أَظُنُّ أَنَّ",en:"I think that",ex:"أَظُنُّ أَنَّ الْجَوَّ سَيَكُونُ بارِدًا.",exEn:"I think the weather will be cold."},
  {ar:"أَعْتَقِدُ أَنَّ",en:"I believe that",ex:"أَعْتَقِدُ أَنَّ هَذا صَحِيحٌ.",exEn:"I believe that's correct."},
  {ar:"فِي الْحَقِيقَةِ",en:"actually, in fact",ex:"فِي الْحَقِيقَةِ لا أَعْرِفُ.",exEn:"Actually, I don't know."},
  {ar:"بِصَراحَةٍ",en:"frankly",ex:"بِصَراحَةٍ، الطَّعامُ لَذِيذٌ.",exEn:"Frankly, the food is delicious."}]},

 {cat:"Asking",catAr:"الاسْتِفْهام",items:[
  {ar:"هَلْ",en:"(yes/no question)",ex:"هَلْ أَنْتَ طالِبٌ؟",exEn:"Are you a student?"},
  {ar:"ما",en:"what (+ noun)",ex:"ما اسْمُكَ؟",exEn:"What's your name?"},
  {ar:"ماذا",en:"what (+ verb)",ex:"ماذا تَفْعَلُ؟",exEn:"What are you doing?"},
  {ar:"مَنْ",en:"who",ex:"مَنْ هَذا؟",exEn:"Who is this?"},
  {ar:"أَيْنَ",en:"where",ex:"أَيْنَ تَسْكُنُ؟",exEn:"Where do you live?"},
  {ar:"مِنْ أَيْنَ",en:"where from",ex:"مِنْ أَيْنَ أَنْتَ؟",exEn:"Where are you from?"},
  {ar:"إِلى أَيْنَ",en:"where to",ex:"إِلى أَيْنَ أَنْتَ ذاهِبٌ؟",exEn:"Where are you going?"},
  {ar:"مَتى",en:"when",ex:"مَتى تَسْتَيْقِظُ؟",exEn:"When do you wake up?"},
  {ar:"كَيْفَ",en:"how",ex:"كَيْفَ الْجَوُّ الْيَوْمَ؟",exEn:"How's the weather today?"},
  {ar:"لِماذا",en:"why",ex:"لِماذا تَدْرُسُ الْعَرَبِيَّةَ؟",exEn:"Why do you study Arabic?"},
  {ar:"كَمْ",en:"how many (+ sing. acc.)",ex:"كَمْ ساعَةً تَعْمَلُ؟",exEn:"How many hours do you work?"},
  {ar:"بِكَمْ",en:"how much (price)",ex:"بِكَمْ هَذا الْقَمِيصُ؟",exEn:"How much is this shirt?"},
  {ar:"أَيُّ",en:"which",ex:"أَيُّ فَصْلٍ تُحِبُّ؟",exEn:"Which season do you like?"},
  {ar:"ما رَأْيُكَ فِي",en:"what do you think of",ex:"ما رَأْيُكَ فِي الْمَدِينَةِ؟",exEn:"What do you think of the city?"}]},

 {cat:"How often",catAr:"التَّكْرار",items:[
  {ar:"دائِمًا",en:"always",ex:"أُصَلِّي الْفَجْرَ دائِمًا.",exEn:"I always pray Fajr."},
  {ar:"عادَةً",en:"usually",ex:"أَذْهَبُ مَشْيًا عادَةً.",exEn:"I usually walk."},
  {ar:"أَحْيانًا",en:"sometimes",ex:"أَحْيانًا أَذْهَبُ بِالْحافِلَةِ.",exEn:"Sometimes I go by bus."},
  {ar:"نادِرًا",en:"rarely",ex:"نادِرًا ما أَشْرَبُ الْقَهْوَةَ.",exEn:"I rarely drink coffee."},
  {ar:"أَبَدًا",en:"never (with negation)",ex:"لا أَتَكَلَّمُ الإِنْجِلِيزِيَّةَ أَبَدًا.",exEn:"I never speak English."},
  {ar:"كُلَّ يَوْمٍ",en:"every day",ex:"أَدْرُسُ كُلَّ يَوْمٍ.",exEn:"I study every day."}]}
];

const CONNECT_EX=[
 {q:"أُصَلِّي، ___ أَتَناوَلُ الْفَطُورَ.",o:["ثُمَّ","لَكِنَّ","لِأَنَّ","مَثَلًا"],a:0,w:"One action follows another in time — ثُمَّ."},
 {q:"تُمْطِرُ فِي الْخارِجِ، ___ أَخَذْتُ الْمِظَلَّةَ.",o:["لِأَنَّ","لِذَلِكَ","لَكِنْ","أَيْضًا"],a:1,w:"The umbrella is the result, not the cause. لِذَلِكَ introduces a result."},
 {q:"أَخَذْتُ الْمِظَلَّةَ ___ الْجَوَّ مُمْطِرٌ.",o:["لِذَلِكَ","لِأَنَّ","ثُمَّ","بَلْ"],a:1,w:"Here the weather is the cause, so لِأَنَّ."},
 {q:"الْمَدِينَةُ كَبِيرَةٌ، ___ فِيها ضَوْضاءَ.",o:["لَكِنْ","لَكِنَّ","لِأَنَّ","كَذَلِكَ"],a:1,w:"A noun follows, so it’s لَكِنَّ with the shadda, and the noun ends in -a."},
 {q:"أُحِبُّ الْقَهْوَةَ ___ لا أَشْرَبُها فِي اللَّيْلِ.",o:["لَكِنْ","لَكِنَّ","لِذَلِكَ","ثُمَّ"],a:0,w:"A verb follows, so the light لَكِنْ."},
 {q:"أُحِبُّ الْقِراءَةَ ___ مُفِيدَةٌ.",o:["لِأَنَّ","لِأَنِّي","لِأَنَّها","لِذَلِكَ"],a:2,w:"The reason refers back to reading — feminine, so لِأَنَّها."},
 {q:"أَضَعُ الْمُنَبِّهَ ___ كَسْلانُ فِي الصَّباحِ.",o:["لِأَنَّ","لِأَنِّي","لِأَنَّها","بِسَبَبِ"],a:1,w:"The reason is about me, so the pronoun attaches: لِأَنِّي."},
 {q:"___ أَتَوَضَّأُ، ثُمَّ أُصَلِّي.",o:["أَخِيرًا","أَوَّلًا","أَيْضًا","مَثَلًا"],a:1,w:"It's the first step in a sequence."},
 {q:"أَقْرَأُ كِتابًا ___ أَنامَ.",o:["بَعْدَ ذَلِكَ","قَبْلَ أَنْ","لِأَنَّ","عِنْدَما"],a:1,w:"After قَبْلَ أَنْ (‘before’), the verb ends in -a: أَنامَ."},
 {q:"___ يَكُونُ الْجَوُّ بارِدًا أَبْقى فِي الْبَيْتِ.",o:["عِنْدَما","لِذَلِكَ","بَلْ","أَيْضًا"],a:0,w:"عِنْدَما = when, introducing the circumstance."},
 {q:"أُحِبُّ الْفاكِهَةَ، ___ الْعِنَبَ وَالتَّمْرَ.",o:["لِذَلِكَ","مَثَلًا","لَكِنْ","ثُمَّ"],a:1,w:"You're giving an example."},
 {q:"___ الْقَرْيَةُ أَهْدَأُ مِنَ الْمَدِينَةِ.",o:["فِي رَأْيِي","لِذَلِكَ","أَيْضًا","ثُمَّ"],a:0,w:"You're marking it as your opinion."},
 {q:"___ ساعَةً تَقْرَأُ فِي الْيَوْمِ؟",o:["ما","كَمْ","بِكَمْ","أَيُّ"],a:1,w:"Counting hours: كَمْ, then one hour, ending in -an."},
 {q:"___ هَذا الْقَمِيصُ؟",o:["كَمْ","بِكَمْ","ما","كَيْفَ"],a:1,w:"Prices always take بِكَمْ."},
 {q:"___ تَفْعَلُ فِي الْعُطْلَةِ؟",o:["ما","ماذا","مَنْ","أَيْنَ"],a:1,w:"ماذا comes before a verb; ما before a noun."},
 {q:"___ اسْمُكَ؟",o:["ما","ماذا","مَنْ","كَيْفَ"],a:0,w:"ما before a noun."},
 {q:"___ الْجَوُّ الْيَوْمَ؟",o:["ما","كَيْفَ","مَتى","أَيْنَ"],a:1,w:"Weather is asked with كَيْفَ, not ما."},
 {q:"___ أَنْتَ ذاهِبٌ؟",o:["مِنْ أَيْنَ","إِلى أَيْنَ","أَيْنَ","كَيْفَ"],a:1,w:"Destination — إِلى أَيْنَ."},
 {q:"___ فَصْلٍ تُحِبُّ؟",o:["ما","أَيُّ","كَمْ","مَنْ"],a:1,w:"Choosing among options — أَيُّ."},
 {q:"أَذْهَبُ مَشْيًا ___ ، وَأَحْيانًا بِالْحافِلَةِ.",o:["دائِمًا","عادَةً","أَبَدًا","نادِرًا"],a:1,w:"'Usually' pairs naturally with the 'sometimes' that follows."},
 {q:"لا أَتَكَلَّمُ الإِنْجِلِيزِيَّةَ فِي الدَّرْسِ ___ .",o:["دائِمًا","أَبَدًا","عادَةً","أَحْيانًا"],a:1,w:"أَبَدًا means 'never' only alongside a negative."},
 {q:"لَسْتُ طالِبًا ___ مُدَرِّسٌ.",o:["لَكِنْ","بَلْ","وَ","ثُمَّ"],a:1,w:"بَلْ corrects the first statement: not X but rather Y."},
 {q:"تَأَخَّرْتُ ___ الازْدِحامِ.",o:["لِأَنَّ","بِسَبَبِ","لِذَلِكَ","عِنْدَما"],a:1,w:"بِسَبَبِ takes a noun directly; لِأَنَّ needs a whole clause."},
 {q:"الشَّقَّةُ غالِيَةٌ، ___ أُحِبُّها.",o:["لِذَلِكَ","مَعَ ذَلِكَ","لِأَنَّ","مَثَلًا"],a:1,w:"You're conceding the point and going the other way."}
];

const VERBS=[
 {ar:"ذَهَبَ",pres:"يَذْهَبُ",en:"to go",pat:"sound I",
  past:["ذَهَبْتُ","ذَهَبْتَ","ذَهَبْتِ","ذَهَبَ","ذَهَبَتْ","ذَهَبْنا"],
  pr:["أَذْهَبُ","تَذْهَبُ","تَذْهَبِينَ","يَذْهَبُ","تَذْهَبُ","نَذْهَبُ"]},
 {ar:"دَرَسَ",pres:"يَدْرُسُ",en:"to study",pat:"sound I",
  past:["دَرَسْتُ","دَرَسْتَ","دَرَسْتِ","دَرَسَ","دَرَسَتْ","دَرَسْنا"],
  pr:["أَدْرُسُ","تَدْرُسُ","تَدْرُسِينَ","يَدْرُسُ","تَدْرُسُ","نَدْرُسُ"]},
 {ar:"كَتَبَ",pres:"يَكْتُبُ",en:"to write",pat:"sound I",
  past:["كَتَبْتُ","كَتَبْتَ","كَتَبْتِ","كَتَبَ","كَتَبَتْ","كَتَبْنا"],
  pr:["أَكْتُبُ","تَكْتُبُ","تَكْتُبِينَ","يَكْتُبُ","تَكْتُبُ","نَكْتُبُ"]},
 {ar:"شَرِبَ",pres:"يَشْرَبُ",en:"to drink",pat:"sound I",
  past:["شَرِبْتُ","شَرِبْتَ","شَرِبْتِ","شَرِبَ","شَرِبَتْ","شَرِبْنا"],
  pr:["أَشْرَبُ","تَشْرَبُ","تَشْرَبِينَ","يَشْرَبُ","تَشْرَبُ","نَشْرَبُ"]},
 {ar:"سَكَنَ",pres:"يَسْكُنُ",en:"to live, reside",pat:"sound I",
  past:["سَكَنْتُ","سَكَنْتَ","سَكَنْتِ","سَكَنَ","سَكَنَتْ","سَكَنَّا"],
  pr:["أَسْكُنُ","تَسْكُنُ","تَسْكُنِينَ","يَسْكُنُ","تَسْكُنُ","نَسْكُنُ"]},
 {ar:"عَمِلَ",pres:"يَعْمَلُ",en:"to work",pat:"sound I",
  past:["عَمِلْتُ","عَمِلْتَ","عَمِلْتِ","عَمِلَ","عَمِلَتْ","عَمِلْنا"],
  pr:["أَعْمَلُ","تَعْمَلُ","تَعْمَلِينَ","يَعْمَلُ","تَعْمَلُ","نَعْمَلُ"]},
 {ar:"فَتَحَ",pres:"يَفْتَحُ",en:"to open",pat:"sound I",
  past:["فَتَحْتُ","فَتَحْتَ","فَتَحْتِ","فَتَحَ","فَتَحَتْ","فَتَحْنا"],
  pr:["أَفْتَحُ","تَفْتَحُ","تَفْتَحِينَ","يَفْتَحُ","تَفْتَحُ","نَفْتَحُ"]},
 {ar:"سَمِعَ",pres:"يَسْمَعُ",en:"to hear",pat:"sound I",
  past:["سَمِعْتُ","سَمِعْتَ","سَمِعْتِ","سَمِعَ","سَمِعَتْ","سَمِعْنا"],
  pr:["أَسْمَعُ","تَسْمَعُ","تَسْمَعِينَ","يَسْمَعُ","تَسْمَعُ","نَسْمَعُ"]},
 {ar:"أَكَلَ",pres:"يَأْكُلُ",en:"to eat",pat:"hamzated",
  past:["أَكَلْتُ","أَكَلْتَ","أَكَلْتِ","أَكَلَ","أَكَلَتْ","أَكَلْنا"],
  pr:["آكُلُ","تَأْكُلُ","تَأْكُلِينَ","يَأْكُلُ","تَأْكُلُ","نَأْكُلُ"]},
 {ar:"قَرَأَ",pres:"يَقْرَأُ",en:"to read",pat:"hamzated",
  past:["قَرَأْتُ","قَرَأْتَ","قَرَأْتِ","قَرَأَ","قَرَأَتْ","قَرَأْنا"],
  pr:["أَقْرَأُ","تَقْرَأُ","تَقْرَئِينَ","يَقْرَأُ","تَقْرَأُ","نَقْرَأُ"]},
 {ar:"قالَ",pres:"يَقُولُ",en:"to say",pat:"hollow",
  past:["قُلْتُ","قُلْتَ","قُلْتِ","قالَ","قالَتْ","قُلْنا"],
  pr:["أَقُولُ","تَقُولُ","تَقُولِينَ","يَقُولُ","تَقُولُ","نَقُولُ"]},
 {ar:"كانَ",pres:"يَكُونُ",en:"to be",pat:"hollow",
  past:["كُنْتُ","كُنْتَ","كُنْتِ","كانَ","كانَتْ","كُنَّا"],
  pr:["أَكُونُ","تَكُونُ","تَكُونِينَ","يَكُونُ","تَكُونُ","نَكُونُ"]},
 {ar:"زارَ",pres:"يَزُورُ",en:"to visit",pat:"hollow",
  past:["زُرْتُ","زُرْتَ","زُرْتِ","زارَ","زارَتْ","زُرْنا"],
  pr:["أَزُورُ","تَزُورُ","تَزُورِينَ","يَزُورُ","تَزُورُ","نَزُورُ"]},
 {ar:"نامَ",pres:"يَنامُ",en:"to sleep",pat:"hollow",
  past:["نِمْتُ","نِمْتَ","نِمْتِ","نامَ","نامَتْ","نِمْنا"],
  pr:["أَنامُ","تَنامُ","تَنامِينَ","يَنامُ","تَنامُ","نَنامُ"]},
 {ar:"رَأى",pres:"يَرى",en:"to see",pat:"defective",
  past:["رَأَيْتُ","رَأَيْتَ","رَأَيْتِ","رَأى","رَأَتْ","رَأَيْنا"],
  pr:["أَرى","تَرى","تَرَيْنَ","يَرى","تَرى","نَرى"]},
 {ar:"اشْتَرى",pres:"يَشْتَرِي",en:"to buy",pat:"form VIII",
  past:["اشْتَرَيْتُ","اشْتَرَيْتَ","اشْتَرَيْتِ","اشْتَرى","اشْتَرَتْ","اشْتَرَيْنا"],
  pr:["أَشْتَرِي","تَشْتَرِي","تَشْتَرِينَ","يَشْتَرِي","تَشْتَرِي","نَشْتَرِي"]},
 {ar:"صَلَّى",pres:"يُصَلِّي",en:"to pray",pat:"form II",
  past:["صَلَّيْتُ","صَلَّيْتَ","صَلَّيْتِ","صَلَّى","صَلَّتْ","صَلَّيْنا"],
  pr:["أُصَلِّي","تُصَلِّي","تُصَلِّينَ","يُصَلِّي","تُصَلِّي","نُصَلِّي"]},
 {ar:"دَرَّسَ",pres:"يُدَرِّسُ",en:"to teach",pat:"form II",
  past:["دَرَّسْتُ","دَرَّسْتَ","دَرَّسْتِ","دَرَّسَ","دَرَّسَتْ","دَرَّسْنا"],
  pr:["أُدَرِّسُ","تُدَرِّسُ","تُدَرِّسِينَ","يُدَرِّسُ","تُدَرِّسُ","نُدَرِّسُ"]},
 {ar:"سافَرَ",pres:"يُسافِرُ",en:"to travel",pat:"form III",
  past:["سافَرْتُ","سافَرْتَ","سافَرْتِ","سافَرَ","سافَرَتْ","سافَرْنا"],
  pr:["أُسافِرُ","تُسافِرُ","تُسافِرِينَ","يُسافِرُ","تُسافِرُ","نُسافِرُ"]},
 {ar:"تَكَلَّمَ",pres:"يَتَكَلَّمُ",en:"to speak",pat:"form V",
  past:["تَكَلَّمْتُ","تَكَلَّمْتَ","تَكَلَّمْتِ","تَكَلَّمَ","تَكَلَّمَتْ","تَكَلَّمْنا"],
  pr:["أَتَكَلَّمُ","تَتَكَلَّمُ","تَتَكَلَّمِينَ","يَتَكَلَّمُ","تَتَكَلَّمُ","نَتَكَلَّمُ"]},
 {ar:"اسْتَيْقَظَ",pres:"يَسْتَيْقِظُ",en:"to wake up",pat:"form X",
  past:["اسْتَيْقَظْتُ","اسْتَيْقَظْتَ","اسْتَيْقَظْتِ","اسْتَيْقَظَ","اسْتَيْقَظَتْ","اسْتَيْقَظْنا"],
  pr:["أَسْتَيْقِظُ","تَسْتَيْقِظُ","تَسْتَيْقِظِينَ","يَسْتَيْقِظُ","تَسْتَيْقِظُ","نَسْتَيْقِظُ"]}
];

/* Contextual verb items: the sentence carries a time marker that forces the tense.
   v = index into VERBS, p = index into PRONOUNS, t = past | pr | fut          */
const VERB_SENT=[
 {v:0,p:3,t:'past',s:"أَمْسِ ___ إِلى السُّوقِ.",en:"Yesterday he went to the market.",cue:"أَمْسِ"},
 {v:0,p:0,t:'pr',  s:"___ إِلى الْعَمَلِ كُلَّ يَوْمٍ.",en:"I go to work every day.",cue:"كُلَّ يَوْمٍ"},
 {v:0,p:5,t:'fut', s:"غَدًا ___ إِلى الْمَسْجِدِ.",en:"Tomorrow we will go to the mosque.",cue:"غَدًا"},
 {v:1,p:0,t:'past',s:"___ اللُّغَةَ الْعَرَبِيَّةَ فِي الْعُطْلَةِ الْماضِيَةِ.",en:"I studied Arabic last holiday.",cue:"الْماضِيَةِ"},
 {v:1,p:4,t:'pr',  s:"___ فِي كُلِّيَّةِ الطِّبِّ الآنَ.",en:"She studies at the College of Medicine now.",cue:"الآنَ"},
 {v:2,p:1,t:'past',s:"هَلْ ___ الدَّرْسَ أَمْسِ؟",en:"Did you write the lesson yesterday?",cue:"أَمْسِ"},
 {v:3,p:0,t:'pr',  s:"___ الشَّايَ كُلَّ صَباحٍ.",en:"I drink tea every morning.",cue:"كُلَّ صَباحٍ"},
 {v:4,p:5,t:'past',s:"___ فِي بَيْتٍ قَدِيمٍ قَبْلَ سَنَةٍ.",en:"We lived in an old house a year ago.",cue:"قَبْلَ سَنَةٍ"},
 {v:5,p:3,t:'pr',  s:"___ فِي شَرِكَةٍ كَبِيرَةٍ.",en:"He works at a big company.",cue:"—"},
 {v:6,p:4,t:'past',s:"___ الْبابَ لِأَنَّ الْجَوَّ حارٌّ.",en:"She opened the door because it's hot.",cue:"—"},
 {v:7,p:0,t:'past',s:"___ أَذانَ الْفَجْرِ، ثُمَّ تَوَضَّأْتُ.",en:"I heard the Fajr adhan, then did wudu.",cue:"ثُمَّ تَوَضَّأْتُ"},
 {v:8,p:0,t:'pr',  s:"___ الْفَطُورَ فِي السَّاعَةِ السَّابِعَةِ.",en:"I eat breakfast at seven.",cue:"—"},
 {v:9,p:3,t:'fut', s:"بَعْدَ الصَّلاةِ ___ الْقُرْآنَ.",en:"After the prayer he will read Qur'an.",cue:"بَعْدَ الصَّلاةِ"},
 {v:10,p:4,t:'past',s:"ماذا ___ لَكَ أَمْسِ؟",en:"What did she say to you yesterday?",cue:"أَمْسِ"},
 {v:11,p:3,t:'past',s:"___ الْجَوُّ بارِدًا أَمْسِ.",en:"The weather was cold yesterday.",cue:"أَمْسِ"},
 {v:12,p:5,t:'past',s:"___ جَدَّنا فِي الْعُطْلَةِ.",en:"We visited our grandfather in the holiday.",cue:"—"},
 {v:13,p:0,t:'past',s:"___ مُتَأَخِّرًا لَيْلَةَ أَمْسِ.",en:"I slept late last night.",cue:"لَيْلَةَ أَمْسِ"},
 {v:14,p:1,t:'past',s:"هَلْ ___ صَدِيقِي فِي الْمَعْرِضِ؟",en:"Did you see my friend at the exhibition?",cue:"—"},
 {v:15,p:0,t:'past',s:"___ قَمِيصًا أَبْيَضَ مِنَ السُّوقِ.",en:"I bought a white shirt from the market.",cue:"—"},
 {v:16,p:5,t:'past',s:"___ الْمَغْرِبَ فِي الْمَسْجِدِ.",en:"We prayed Maghrib at the mosque.",cue:"—"},
 {v:17,p:4,t:'pr',  s:"___ الأَطْفالَ فِي الْمَرْحَلَةِ الابْتِدائِيَّةِ.",en:"She teaches children at primary level.",cue:"—"},
 {v:18,p:0,t:'fut', s:"إِنْ شاءَ اللهُ ___ إِلى مَكَّةَ فِي رَمَضانَ.",en:"God willing I will travel to Mecca in Ramadan.",cue:"إِنْ شاءَ اللهُ"},
 {v:19,p:5,t:'pr',  s:"___ بِالْعَرَبِيَّةِ فِي الدَّرْسِ.",en:"We speak Arabic in the lesson.",cue:"—"},
 {v:20,p:0,t:'pr',  s:"___ مُبَكِّرًا كُلَّ يَوْمٍ.",en:"I wake up early every day.",cue:"كُلَّ يَوْمٍ"}
];

const PRONOUNS=[
 {ar:"أَنا",en:"I"},{ar:"أَنْتَ",en:"you (m)"},{ar:"أَنْتِ",en:"you (f)"},
 {ar:"هُوَ",en:"he"},{ar:"هِيَ",en:"she"},{ar:"نَحْنُ",en:"we"}
];
