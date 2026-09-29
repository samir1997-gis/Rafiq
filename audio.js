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

  let CLIPS=null, curAudio=null, clipsReady=Promise.resolve();
  try{
    if(typeof fetch==='function'){
      clipsReady=fetch('audio/index.json?t='+Math.floor(Date.now()/60000)).then(r=>r.ok?r.json():[])
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

  /* One audio player for every clip. iPhone only lets a player start by itself
     (the next line, after the last one ends) once a tap has started that same
     player, so a fresh Audio() per clip needed a tap every time. The first tap
     anywhere unlocks this one; after that lines follow each other on their own. */
  let player=null;
  const SILENT='data:audio/wav;base64,UklGRrQBAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YZABAACAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA';
  function getPlayer(){ if(!player){ player=new Audio(); player.preload='auto'; } return player; }
  function unlock(){
    const a=getPlayer();
    if(a.src) return;                            // already used by a real clip (inside this tap)
    a.src=SILENT; a.play().catch(()=>{});
  }
  ['touchend','click','keydown'].forEach(ev=>document.addEventListener(ev,unlock,{capture:true,passive:true}));

  function stop(){
    if(curAudio){curAudio.onended=curAudio.onerror=null; curAudio.pause(); curAudio=null}
    if(window.speechSynthesis) speechSynthesis.cancel();
    document.querySelectorAll('.speaking').forEach(e=>e.classList.remove('speaking'));
  }
  /* after(): called once the line has finished playing (or couldn't play) */
  let seq=0;
  /* opts (optional): src plays that file instead of the text's clip (a licensed
     recitation), at normal speed; onStart(audio) runs once it is playing, so a page
     can follow audio.currentTime (the word-by-word highlight). */
  function speak(text,el,after,opts){
    opts=opts||{};
    const my=++seq;
    // the list of recordings is still loading (the first word on a page): wait for it,
    // rather than falling back to the device voice
    if(CLIPS===null){ if(el)el.classList.add('speaking'); clipsReady.then(()=>{ if(my===seq) speak(text,el,after,opts); }); return; }
    stop();
    if(el)el.classList.add('speaking');
    let ended=false;
    const done=()=>{if(el)el.classList.remove('speaking'); if(!ended){ended=true; if(after)after();}};
    const id=opts.src?null:clipId(text);
    if(id||opts.src){
      const a=getPlayer();
      a.onended=a.onerror=null; a.pause();
      a.src=opts.src||('audio/'+id+'.mp3');
      const r=opts.src?1:Math.max(0.6,Math.min(1.3,rate()+0.15));
      a.defaultPlaybackRate=r; a.playbackRate=r;          // a new src resets the rate to the default
      curAudio=a;
      const mine=()=>my===seq;                            // this line is still the one playing
      a.onended=()=>{ if(!mine()) return; curAudio=null; done(); };
      a.onerror=()=>{ if(!mine()) return; curAudio=null; if(opts.src) done(); else tts(text,done); };
      a.play().then(()=>{ if(mine() && opts.onStart) opts.onStart(a); }).catch(err=>{
        if(!mine()) return;                               // replaced by a newer line: not a failure
        curAudio=null;
        // the browser won't play sound before the first tap on the page (strict on iPhone):
        // keep this line and play it on that tap, with a cue so it doesn't seem silent
        if(err && err.name==='NotAllowedError'){ if(el)el.classList.remove('speaking'); waitForTap({text,el,after,opts}); return; }
        if(opts.src) done(); else tts(text,done);   // never a device voice for a recitation
      });
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

  /* A line refused before the first tap: shown as a "Tap anywhere to hear" cue,
     played on the first tap. If that tap starts other audio (Next, a word),
     that simply takes over. */
  let blocked=null, cue=null;
  function waitForTap(line){
    blocked=line;
    if(cue||!document.body) return;
    cue=document.createElement('button'); cue.type='button'; cue.className='rq-tap';
    cue.textContent='🔊 Tap anywhere to hear';
    cue.style.cssText='position:fixed;left:50%;bottom:calc(104px + env(safe-area-inset-bottom));transform:translateX(-50%);z-index:350;white-space:nowrap;'+
      'border:0;border-radius:999px;padding:9px 16px;background:var(--verdigris,#2E7263);color:var(--paper,#F1ECE0);'+
      'font:600 14px var(--la,system-ui);box-shadow:0 6px 20px -8px rgba(0,0,0,.45);cursor:pointer';
    document.body.appendChild(cue);
    // just above the lesson's buttons, however many there are
    const foot=document.querySelector('.foot'), top=foot && foot.getBoundingClientRect().top;
    if(top>0 && top<innerHeight) cue.style.bottom=Math.round(innerHeight-top+12)+'px';
  }
  function playBlocked(){
    if(cue){ cue.remove(); cue=null; }
    if(!blocked) return;
    const b=blocked; blocked=null;
    if(b.el && !b.el.isConnected) return;       // that screen has gone
    speak(b.text,b.el,b.after,b.opts);          // inside the tap, so the browser allows it
  }
  ['click','touchend','keydown'].forEach(ev=>document.addEventListener(ev,playBlocked,{capture:true,passive:true}));
  let unlocked=false;
  ['pointerdown','touchstart','keydown'].forEach(ev=>document.addEventListener(ev,()=>{
    if(unlocked)return; unlocked=true;
    try{const u=new SpeechSynthesisUtterance(' ');u.volume=0;speechSynthesis.speak(u)}catch(e){}
    setTimeout(sync,350);
  },{once:true,passive:true}));

  window.RQ={speak,stop,mount,sync,available,aid,clipId,rate,list,chosen};
})();
