#!/usr/bin/env node
/* Builds audio-manifest.json — every line of Arabic anywhere in the app that
   wants a pre-rendered clip.
   Run:  node tools/build-manifest.js                                          */
const fs=require('fs'), path=require('path'), root=path.join(__dirname,'..');

// Must match aid() in the browser — same text in, same filename out.
function aid(s){let h=5381;for(let i=0;i<s.length;i++)h=((h*33)^s.charCodeAt(i))>>>0;return h.toString(36);}

function load(file, names){
  const p=path.join(root,file);
  if(!fs.existsSync(p)){ console.error('missing '+file); process.exit(1); }
  let src=fs.readFileSync(p,'utf8');
  names.forEach(n=>{ src=src.replace(new RegExp('const\\s+'+n+'\\s*=','g'),'globalThis.'+n+'='); });
  eval(src);
}

// unit content and the toolkit each live in their own file now
load('drills-data.js',  ['DATA','EXTRA']);
load('vocab-data.js',   ['VOCAB']);
load('toolkit-data.js', ['CONNECTORS','CONNECT_EX','VERBS','PRONOUNS','VERB_SENT']);
load('scenes-data.js',  ['SCENES']);
Object.keys(EXTRA).forEach(k=>{
  const u=DATA.find(x=>x.n===k);
  if(u) Object.assign(u,EXTRA[k]);
});

const glue=(a,s)=>a+(s.startsWith('،')?'':' ')+s, J=a=>a.reduce(glue);
const seen=new Map();
const add=(bucket,unit,text)=>{
  if(!text) return; text=String(text).trim(); if(!text) return;
  const id=aid(text);
  if(!seen.has(id)) seen.set(id,{id,text,bucket,unit,chars:text.length});
};

DATA.forEach(u=>{
  /* Every conversation, not just the first. u.dialogue holds whichever one the
     page last selected, so read convos when it exists. */
  const convos = (u.convos && u.convos.length) ? u.convos : [{lines:u.dialogue||[]}];
  convos.forEach(c=>(c.lines||[]).forEach(line=>add('dialogue',u.n,line[1])));

  (u.ladders||[]).forEach(l=>l.steps.forEach((_,i)=>add('ladder',u.n,J(l.steps.slice(0,i+1)))));
  (u.transforms||[]).forEach(t=>{add('transform',u.n,t.src);add('transform',u.n,t.ans);});
  (u.cloze||[]).forEach(c=>add('cloze',u.n,c.q.replace('___',c.o[c.a])));
  (u.fix||[]).forEach(f=>add('fix',u.n,f.good));
  (u.builds||[]).forEach(b=>add('build',u.n,J(b.parts)));
  (u.prompts||[]).forEach(p=>{add('prompt',u.n,p[0]);add('model',u.n,p[2]);});
  (u.grammar||[]).forEach(g=>{
    add('grammar',u.n,g.ar);
    // paired examples show one per row, each with its own play (pairsOf in learn.html / drills.html)
    const a=g.ar.split(' · '), e=(g.tr||'').split(' · ');
    if(g.tr && a.length>1 && a.length===e.length) a.forEach(x=>add('grammar',u.n,x.replace(/[.،]\s*$/,'').trim()));
  });
});

VOCAB.forEach(v=>add('vocab',v.unit,v.ar));

/* Word tiles ("Say this in Arabic" in sessions, "Build it" on Sentences): each
   tile is spoken when tapped. Recorded without punctuation; audio.js falls back
   to that bare form. The pieces match sayParts() and decoys() in session.html. */
const PUNCT=/[؟?!.،,:]/g, bare=s=>s.replace(/[؟?!.،,:؛]/g,' ').replace(/\s+/g,' ').trim();
const tile=(unit,t)=>{ const b=bare(t); if(/[\u0621-\u064A]/.test(b)) add('tile',unit,b); };
DATA.forEach(u=>{
  const convos=(u.convos&&u.convos.length)?u.convos:[{lines:u.dialogue||[]}];
  const lines=[]; convos.forEach(c=>(c.lines||[]).forEach(l=>lines.push(l[1]))); (u.dialogue||[]).forEach(l=>lines.push(l[1]));
  lines.forEach(ar=>{
    const w=[]; ar.split(/\s+/).filter(Boolean).forEach(t=>{ if(!t.replace(PUNCT,'')&&w.length) w[w.length-1]+=t; else w.push(t); });
    const size=Math.ceil(w.length/7); for(let i=0;i<w.length;i+=size) tile(u.n,w.slice(i,i+size).join(' '));
    ar.split(/\s+/).forEach(t=>tile(u.n,t));                    // decoy pieces are single words from these lines
  });
  (u.builds||[]).forEach(b=>b.parts.forEach(p=>{ tile(u.n,p); p.split(/\s+/).forEach(t=>tile(u.n,t)); }));
  // "Find the mistake" and rewrite exercises as tiles in units 1–3 (tileDrill in session.html):
  // every word of the answer, plus the words that change (the decoys)
  (u.fix||[]).forEach(f=>{ f.good.split(/\s+/).forEach(t=>tile(u.n,t)); f.bad.split(/\s+/).forEach(t=>tile(u.n,t)); });
  (u.transforms||[]).forEach(x=>{ x.ans.split(/\s+/).forEach(t=>tile(u.n,t)); x.src.split(/\s+/).forEach(t=>tile(u.n,t)); });
});

/* Reading starter: each letter's name, its example words, the vowel-mark
   examples and the listening-test words (said without being shown). */
eval(fs.readFileSync(path.join(root,'alphabet-data.js'),'utf8')
      .replace(/const (ALPHABET_GROUPS|VOWEL_MARKS|LISTEN_TEST)/g,'globalThis.$1'));
ALPHABET_GROUPS.forEach(g=>g.letters.forEach(l=>{
  add('alphabet','00',l[1]); add('alphabet','00',l[3]);
  (l[5]||[]).forEach(e=>add('alphabet','00',e[0]));
}));
VOWEL_MARKS.forEach(v=>{ if(v[3]) add('alphabet','00',v[3][0]); });
LISTEN_TEST.forEach(t=>add('alphabet','00',t[0]));

/* Everyday essentials (Practise): numbers, days, months, colours (both forms), time. */
eval(fs.readFileSync(path.join(root,'essentials-data.js'),'utf8').replace(/const ESSENTIALS/,'globalThis.ESSENTIALS'));
ESSENTIALS.forEach(s=>s.items.forEach(it=>{ add('essentials',s.id,it[0]); if(s.id==='colours') add('essentials',s.id,it[2]); }));

SCENES.forEach(sc=>sc.lines.forEach(l=>add('scene',sc.id,l[1])));

/* "Your salah" (salah.js): the prayer phrases and their words, in the app's voice.
   Never the Quran (Al-Fatiha, the surahs): that only ever plays a licensed human
   recitation. Render the 'salah' bucket once the teacher has signed off (#38). */
load('salah-data.js', ['SALAH']);
SALAH.parts.filter(p=>p.group==='prayer' && !/^fatiha/.test(p.id)).forEach(p=>p.lines.forEach(l=>{
  add('salah',p.id,l.ar); l.words.forEach(w=>add('salah',p.id,w.ar));
}));

CONNECTORS.forEach(cat=>cat.items.forEach(it=>{
  add('connector','-',it.ar);
  add('connector-ex','-',it.ex);
}));
CONNECT_EX.forEach(t=>add('connector-ex','-',t.q.replace('___',t.o[t.a])));

VERBS.forEach(v=>{
  v.past.forEach(f=>add('verb','-',f));
  v.pr.forEach(f=>{ add('verb','-',f); add('verb','-','سَ'+f); });
});
VERB_SENT.forEach(it=>{
  const v=VERBS[it.v]; if(!v) return;
  const form = it.t==='past' ? v.past[it.p] : it.t==='pr' ? v.pr[it.p] : 'سَ'+v.pr[it.p];
  add('verb-sent','-',it.s.replace('___',form));
});

const items=[...seen.values()];
fs.writeFileSync(path.join(root,'audio-manifest.json'),JSON.stringify(items,null,1));

const by={}; items.forEach(i=>{by[i.bucket]=by[i.bucket]||{n:0,c:0};by[i.bucket].n++;by[i.bucket].c+=i.chars;});
console.log('bucket'.padEnd(14),'clips'.padStart(6),'chars'.padStart(8));
Object.entries(by).forEach(([k,v])=>console.log(k.padEnd(14),String(v.n).padStart(6),String(v.c).padStart(8)));
console.log(''.padEnd(30,'-'));
console.log('total'.padEnd(14),String(items.length).padStart(6),
            String(items.reduce((a,b)=>a+b.chars,0)).padStart(8));
console.log('\nwrote audio-manifest.json');
