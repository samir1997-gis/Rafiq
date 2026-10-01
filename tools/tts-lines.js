#!/usr/bin/env node
/* Speaks a list of lines with ElevenLabs: [{file, voice, text, stability?, style?, speed?}, ...] → <out-dir>/<file>.mp3
   Usage: ELEVENLABS_API_KEY=… node tools/tts-lines.js <lines.json> <out-dir> [--force]
   Write Arabic names in Arabic script inside English lines (e.g. "Meet رَفِيق") so they're said the Arabic way. */
const fs=require('fs'), path=require('path');
const KEY=process.env.ELEVENLABS_API_KEY, [,,list,out]=process.argv, FORCE=process.argv.includes('--force');
const items=JSON.parse(fs.readFileSync(list,'utf8')); fs.mkdirSync(out,{recursive:true});
(async()=>{
  let ok=0,fail=0;
  for(const it of items){
    const file=path.join(out,it.file+'.mp3');
    if(!FORCE&&fs.existsSync(file)){console.log('  = '+it.file);continue;}
    const r=await fetch('https://api.elevenlabs.io/v1/text-to-speech/'+it.voice,{method:'POST',
      headers:{'xi-api-key':KEY,'Content-Type':'application/json','Accept':'audio/mpeg'},
      body:JSON.stringify({text:it.text,model_id:it.model||'eleven_multilingual_v2',
        voice_settings:{stability:it.stability??0.5,similarity_boost:0.75,style:it.style??0.15,use_speaker_boost:true,...(it.speed?{speed:it.speed}:{})}})});
    if(!r.ok){ const m=await r.text(); if(r.status===429||/quota_exceeded/.test(m)){console.error('Out of credits — stopping.');break;}
      console.error('  x '+it.file+' '+r.status+' '+m.slice(0,160)); fail++; continue; }
    fs.writeFileSync(file,Buffer.from(await r.arrayBuffer())); ok++; console.log('  ✓ '+it.file+'  '+it.text);
  }
  console.log('\nspoken '+ok+', failed '+fail);
})();
