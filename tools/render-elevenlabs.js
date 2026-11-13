#!/usr/bin/env node
const fs=require('fs'), path=require('path'), root=path.join(__dirname,'..');
const KEY=process.env.ELEVENLABS_API_KEY;
/* A flag with no value used to swallow the next flag — e.g. a blank --limit
   would eat --model. Treat "next thing starts with --" as no value given. */
const arg=(f,d)=>{
  const i=process.argv.indexOf(f);
  if(i<0) return d;
  const v=process.argv[i+1];
  return (v===undefined || v.startsWith('--')) ? d : v;
};
const has=f=>process.argv.includes(f);

const VOICE=arg('--voice'), MODEL=arg('--model','eleven_multilingual_v2');
const ONLY=(arg('--only','')||'').split(',').filter(Boolean);
// --ids <file>: only these clips (one id per line), in the file's order
const IDS=arg('--ids') ? fs.readFileSync(path.join(root,arg('--ids')),'utf8').split('\n').map(l=>l.trim()).filter(l=>l && !l.startsWith('#')) : null;
const rawLimit=arg('--limit','0');
const LIMIT=Number.isFinite(parseInt(rawLimit,10))?parseInt(rawLimit,10):0;   // blank or junk = no limit
const DRY=has('--dry'), STRIP=has('--strip'), FORCE=has('--force'), PAUSAL=has('--pausal');   // --force re-records clips that already exist (e.g. a new voice)
const outDir=path.join(root,'audio');

const stripTashkeel=s=>s.replace(/[\u064B-\u0652\u0670\u0640]/g,'');
/* --pausal (owner, 13 Nov 2026: "don't overemphasise the ending of the word"): Arabic said on its own, or at a stop, drops its case
   ending (waqf). Only what's sent to the voice changes: the clip's id still comes from the fully vowelled text the page shows.
   At the end of a clip and before ، . ؟ ! : ؛ the last word loses its final short vowel or -un/-in; -an becomes a long ā; ة
   becomes a soft h. Endings that carry meaning stay: -ka/-ki, -ta/-ti (your, you, to a man or a woman), and words ending in
   و / ي with a vowel (هُوَ، هِيَ، عَلَيَّ). */
const SHADDA='ّ';
function pausalWord(w){
  const m=w.match(/^(.*?)([^ء-ْٰ]*)$/s), c=m[1], tail=m[2];          // keep trailing punctuation as it is
  if(!c) return w;
  if(/ً[اى]$/.test(c)) return c.replace(/ً([اى])$/,'َ$1')+tail;   // -an written with alif (or ى): a long ā
  const mm=c.match(/^(.*[^ً-ْ])([ً-ْ]*)$/s); if(!mm) return w;
  const stem=mm[1], marks=mm[2], end=stem.slice(-1), sh=marks.includes(SHADDA)?SHADDA:'', v=marks.replace(/[ّْ]/g,'');
  if(end==='ة') return stem.slice(0,-1)+'هْ'+tail;                  // ة → a soft h
  if(!v) return w;                                                                // already still (sukun, or no mark)
  if('كت'.includes(end) && (/^[َِ]$/.test(v) || (end==='ت' && v==='ُ')) && !/ال/.test(stem)) return w;   // and -tu: I   // -ka/-ki, -ta/-ti: to a man or a woman (كِتابُكَ / كِتابُكِ، كَتَبْتَ / كَتَبْتِ)
  if('وي'.includes(end) && v==='َ') return w;                      // هُوَ، هِيَ، عَلَيَّ
  if(v==='ً') return stem+sh+'َا'+tail;                            // -an with no alif written (ماءً): a long ā
  return stem+sh+tail;                                                            // -u/-a/-i and -un/-in: gone (a shadda stays)
}
const pausal=s=>s.split(/(\s+)/).map((t,i,a)=>{
  if(/^\s+$/.test(t)) return t;
  const next=a.slice(i+1).find(x=>!/^\s+$/.test(x));
  const stop=!next || /[،.؟!:؛?,]$/.test(t) || /^[،.؟!:؛?,]/.test(next||'');
  return stop ? pausalWord(t) : t;
}).join('');

async function listVoices(){
  const r=await fetch('https://api.elevenlabs.io/v1/voices',{headers:{'xi-api-key':KEY}});
  if(!r.ok){console.error('API error',r.status,await r.text());process.exit(1);}
  const {voices}=await r.json();
  voices.forEach(v=>console.log('  '+v.voice_id+'  '+v.name));
}

async function main(){
  if(has('--list-voices')){ if(!KEY){console.error('Set ELEVENLABS_API_KEY first.');process.exit(1);} return listVoices(); }

  let items=JSON.parse(fs.readFileSync(path.join(root,'audio-manifest.json'),'utf8'));
  // --only also sets the order: buckets listed first are rendered first
  if(ONLY.length) items=items.filter(i=>ONLY.includes(i.bucket)).sort((a,b)=>ONLY.indexOf(a.bucket)-ONLY.indexOf(b.bucket));
  if(IDS){ const at=new Map(IDS.map((id,i)=>[id,i])); items=items.filter(i=>at.has(i.id)).sort((a,b)=>at.get(a.id)-at.get(b.id)); }
  fs.mkdirSync(outDir,{recursive:true});
  const todo=FORCE?items:items.filter(i=>!fs.existsSync(path.join(outDir,i.id+'.mp3')));
  const done=items.length-todo.length;
  const batch=LIMIT?todo.slice(0,LIMIT):todo;
  const chars=batch.reduce((a,b)=>a+b.chars,0);

  console.log(items.length+' clips selected · '+done+' already rendered · '+batch.length+' to do · '+chars+' characters');
  if(DRY){console.log('(dry run — nothing sent)');return;}
  if(!KEY){console.error('Set ELEVENLABS_API_KEY first.');process.exit(1);}
  if(!VOICE){console.error('Pass --voice <id>.');process.exit(1);}
  if(!batch.length){console.log('Nothing to do.');return writeIndex();}

  let ok=0,fail=0;
  for(const [n,it] of batch.entries()){
    let text=PAUSAL?pausal(it.text):it.text; if(STRIP) text=stripTashkeel(text);
    try{
      const r=await fetch('https://api.elevenlabs.io/v1/text-to-speech/'+VOICE,{
        method:'POST',
        headers:{'xi-api-key':KEY,'Content-Type':'application/json','Accept':'audio/mpeg'},
        body:JSON.stringify({text,model_id:MODEL,
          voice_settings:{stability:0.5,similarity_boost:0.75,style:0,use_speaker_boost:true}})
      });
      if(!r.ok){
        const msg=await r.text();
        if(r.status===429 || /quota_exceeded/.test(msg)){console.error('\nRate limited or out of credits. Progress saved — rerun later.');break;}
        console.error('  x '+it.id+' '+r.status+' '+msg.slice(0,120));fail++;continue;
      }
      fs.writeFileSync(path.join(outDir,it.id+'.mp3'),Buffer.from(await r.arrayBuffer()));
      ok++;
      console.log('  '+(n+1)+'/'+batch.length+'  '+it.bucket+'  '+it.text.slice(0,28));
      await new Promise(r=>setTimeout(r,250));
    }catch(e){console.error('  x '+it.id+' '+e.message);fail++;}
  }
  console.log('\nrendered '+ok+', failed '+fail);
  writeIndex();
}

function writeIndex(){
  const ids=fs.readdirSync(outDir).filter(f=>f.endsWith('.mp3')).map(f=>f.replace('.mp3',''));
  fs.writeFileSync(path.join(outDir,'index.json'),JSON.stringify(ids));
  console.log('audio/index.json now lists '+ids.length+' clips');
}
if(require.main===module) main();
module.exports={pausal};
