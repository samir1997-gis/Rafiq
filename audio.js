/* Shared audio: voice ranking, pre-rendered clip playback, persisted preferences,
   and the settings panel. Loaded by Words, Verbs and Connectors; Sentences has the
   same logic inline because it also shows progress in the panel. */
(function(){
  const VKEY='bay_voice_uri', RKEY='bay_voice_rate', WKEY='bay_voicewarn_dismissed';

  function aid(s){let h=5381;for(let i=0;i<s.length;i++)h=((h*33)^s.charCodeAt(i))>>>0;return h.toString(36);}
  /* The recorded clip for a line: the exact text, or failing that the same words
     without punctuation (word tiles keep the sentence's commas and full stops).
     tools/build-manifest.js records the tiles in that bare form. */
  const bare=s=>String(s).replace(/[؟?!.،,:؛]/g,' ').replace(/\s+/g,' ').trim();
  function clipId(text){
    if(!CLIPS) return null;
    const a=aid(text); if(CLIPS.has(a)) return a;
    const b=aid(bare(text)); return CLIPS.has(b) ? b : null;
  }

  let CLIPS=null, curAudio=null;
  try{
    if(typeof fetch==='function'){
      fetch('audio/index.json?t='+Math.floor(Date.now()/60000)).then(r=>r.ok?r.json():[])
        .then(a=>{CLIPS=new Set(a);sync()}).catch(()=>{CLIPS=new Set()});
    } else CLIPS=new Set();
  }catch(e){ CLIPS=new Set(); }

  const sig=v=>((v.voiceURI||'')+' '+(v.name||'')).toLowerCase();
  function quality(v){
    const t=sig(v);
    if(/premium|neural|natural/.test(t))return 'premium';
    if(/enhanced/.test(t))return 'enhanced';
    if(/siri/.test(t))return 'siri';
    if(/compact/.test(t))return 'basic';
    return 'standard';
  }
  const RANK={premium:4,enhanced:3,siri:2,standard:1,basic:0};
  function score(v){
    let s=RANK[quality(v)]*100; const l=(v.lang||'').toLowerCase();
    if(/^ar-sa/.test(l))s+=10; else if(/^ar-(eg|ae|jo|kw|qa|bh)/.test(l))s+=6; else if(/^ar-001/.test(l))s+=4;
    if(v.localService===false)s+=3;
    return s;
  }
  function list(){
    const raw=(window.speechSynthesis? speechSynthesis.getVoices()||[] : []).filter(v=>/^ar/i.test(v.lang));
    const seen=new Map();                      // iOS repeats the same voice several times
    raw.forEach(v=>{const k=(v.voiceURI||v.name)+'|'+v.lang; if(!seen.has(k))seen.set(k,v)});
    return [...seen.values()].sort((a,b)=>score(b)-score(a));
  }
  function stored(){ try{return localStorage.getItem(VKEY)}catch(e){return null} }
  function chosen(){
    const l=list(); if(!l.length) return null;
    const want=stored();
    return (want && l.find(v=>(v.voiceURI||v.name)===want)) || l[0];
  }
  function rate(){
    let r=parseFloat((()=>{try{return localStorage.getItem(RKEY)}catch(e){return null}})());
    return (r>=0.5&&r<=1.1)?r:0.8;
  }
  function setRate(r){ try{localStorage.setItem(RKEY,r)}catch(e){} }
  function setVoice(uri){ try{localStorage.setItem(VKEY,uri)}catch(e){} }

  function stop(){
    if(curAudio){curAudio.pause();curAudio=null}
    if(window.speechSynthesis) speechSynthesis.cancel();
    document.querySelectorAll('.speaking').forEach(e=>e.classList.remove('speaking'));
  }
  /* after(): called once the line has finished playing (or couldn't play) */
  function speak(text,el,after){
    stop();
    if(el)el.classList.add('speaking');
    let ended=false;
    const done=()=>{if(el)el.classList.remove('speaking'); if(!ended){ended=true; if(after)after();}};
    const id=clipId(text);
    if(id){
      const a=new Audio('audio/'+id+'.mp3');
      a.playbackRate=Math.max(0.6,Math.min(1.3,rate()+0.15));
      curAudio=a; a.onended=()=>{curAudio=null;done()};
      a.onerror=()=>{curAudio=null;tts(text,done)};
      a.play().catch(()=>{curAudio=null;tts(text,done)});
      return;
    }
    tts(text,done);
  }
  function tts(text,done){
    const v=chosen(); if(!v){if(done)done();return}
    const u=new SpeechSynthesisUtterance(text);
    u.lang=v.lang||'ar-SA'; u.rate=rate(); u.pitch=1; u.voice=v;
    u.onend=done; u.onerror=done;
    speechSynthesis.speak(u);
  }
  const available=()=> (CLIPS&&CLIPS.size>0) || list().length>0;

  /* No picker any more — the best available voice is chosen automatically,
     and pre-rendered clips are used ahead of it wherever they exist. */
  function mount(){}
  function sync(){}

  if(window.speechSynthesis) speechSynthesis.onvoiceschanged=sync;
  let unlocked=false;
  ['pointerdown','touchstart','keydown'].forEach(ev=>document.addEventListener(ev,()=>{
    if(unlocked)return; unlocked=true;
    try{const u=new SpeechSynthesisUtterance(' ');u.volume=0;speechSynthesis.speak(u)}catch(e){}
    setTimeout(sync,350);
  },{once:true,passive:true}));

  window.RQ={speak,stop,mount,sync,available,aid,rate,list,chosen};
})();
