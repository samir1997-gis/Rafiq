/* tiles.js — build a sentence from word tiles. Tap a tile to put it on the
   answer line (right to left) and hear it; tap a placed tile to send it back
   to its old place. Used for "Say this in Arabic" in the early lessons (see
   RafiqPath.answerStyle) and for "Build it" on the Sentences page.

     RafiqTiles.create({parts, extra, en, say, onCorrect, okText, checkLabel})
       → {el, reveal}
     parts      the sentence's pieces, in order
     extra      pieces that don't belong (may be empty)
     en         the English, for the word-order check
     say(t,el)  speak a piece or the sentence
     onCorrect({firstTry, text})  once, when the answer is right
     strict     only the exact order counts (the words of the prayer, the Quran)
     reveal()   put the right answer on the line (for "Show the answer")

   A different order gets a second opinion from RafiqJudge.build(): Arabic
   often allows more than one. */
(function(){
  const glue=(a,s)=>a+(s.startsWith('،')?'':' ')+s;
  const joinAr=a=>a.length?a.reduce(glue):'';
  const shuffle=a=>{const b=a.slice();for(let i=b.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[b[i],b[j]]=[b[j],b[i]]}return b};
  const still=()=>window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const sound=ok=>{ if(window.RafiqSound) RafiqSound.answer(ok); };

  /* Every tile glides from where it was to where it lands (and back the same
     way), starting from its on-screen position so a tap mid-glide redirects it. */
  function flip(tiles, change){
    const before=tiles.map(t=>t.getBoundingClientRect());
    tiles.forEach(t=>t.getAnimations().forEach(a=>a.cancel()));
    change();
    if(still()) return;
    tiles.forEach((t,i)=>{
      const a=before[i], b=t.getBoundingClientRect(), dx=a.left-b.left, dy=a.top-b.top;
      if(Math.abs(dx)<1 && Math.abs(dy)<1) return;
      t.animate([{transform:`translate(${dx}px,${dy}px)`},{transform:'none'}],
                {duration:280, easing:'cubic-bezier(.16,1,.3,1)'});
    });
  }

  function create({parts, extra=[], en='', say, onCorrect, okText, checkLabel='Check', strict=false}){
    let order=shuffle(parts.map(t=>({t, real:true})).concat(extra.map(t=>({t, real:false}))));
    if(!extra.length && parts.length>1 && order.every((p,i)=>p.t===parts[i])) order=order.slice(1).concat(order[0]);
    const el=document.createElement('div'); el.className='tl';
    el.innerHTML=`<div class="tl-line empty" aria-label="Your answer"></div><div class="tl-pool"></div>
      <div class="tl-bar"><button type="button" class="btn tl-check">${checkLabel}</button>
      <button type="button" class="btn ghost tl-clear">Clear</button></div><div class="tl-verdict" aria-live="polite"></div>`;
    const line=el.querySelector('.tl-line'), pool=el.querySelector('.tl-pool'), verdict=el.querySelector('.tl-verdict');
    let tries=0, done=false, seq=0;
    const note=(t,cls)=>{ verdict.textContent=t||''; verdict.className='tl-verdict'+(cls?' '+cls:''); };
    const refresh=()=>{ line.classList.toggle('empty',!line.children.length); line.classList.remove('wrong'); note(''); seq++; };
    const tiles=order.map(pc=>{
      const b=document.createElement('button'); b.type='button'; b.className='tl-tile'; b.textContent=pc.t; b._pc=pc;
      b.onclick=()=>{
        if(done) return;
        flip(tiles,()=>{
          if(b.parentNode===pool) line.appendChild(b);
          else pool.insertBefore(b, tiles.slice(tiles.indexOf(b)+1).find(x=>x.parentNode===pool)||null);   // back to its own spot
        });
        refresh();
        if(say && b.parentNode===line) say(pc.t,b);
      };
      pool.appendChild(b); return b;
    });

    const placed=()=>[...line.children].map(b=>b._pc);
    function right(text, other){
      done=true; line.classList.add('right'); line.classList.remove('wrong'); sound(true);
      note(other ? 'That order works too ✓ Another way to say it: '+other : (okText||'Correct ✓'), 'ok');
      el.querySelectorAll('.tl-bar .btn').forEach(b=>b.disabled=true);
      if(say) say(text,line);
      if(onCorrect) onCorrect({firstTry:tries===1, text});
    }
    function notYet(msg){
      line.classList.add('wrong'); sound(false);
      note(msg||'Not yet. Look for the word that has to come first.','no');
    }
    el.querySelector('.tl-check').onclick=()=>{
      if(done) return;
      const p=placed();
      if(!p.some(x=>!x.real) && p.length<parts.length){ note('Place every piece first.','no'); return; }
      tries++;
      if(p.some(x=>!x.real)) return notYet('Not yet. One of these pieces doesn\'t belong in this sentence.');
      const model=joinAr(parts), mine=joinAr(p.map(x=>x.t));
      if(mine===model) return right(model);
      if(strict || !(window.RafiqJudge && RafiqJudge.on)) return notYet();
      const mySeq=++seq; note('Checking…');
      RafiqJudge.build(en, model, mine).then(ok=>{
        if(mySeq!==seq || done) return;                 // tiles moved while we waited
        if(ok) right(mine, model); else notYet();
      });
    };
    el.querySelector('.tl-clear').onclick=()=>{
      if(done) return;
      flip(tiles,()=>tiles.forEach(b=>pool.appendChild(b)));
      refresh();
    };
    function reveal(){
      if(done) return;
      done=true;
      flip(tiles,()=>{
        const left=tiles.slice();
        parts.forEach(t=>{ const i=left.findIndex(b=>b._pc.real && b._pc.t===t); if(i>=0) line.appendChild(left.splice(i,1)[0]); });
        left.forEach(b=>pool.appendChild(b));
      });
      line.classList.remove('empty','wrong'); line.classList.add('right'); note('');
      el.querySelectorAll('.tl-bar .btn').forEach(b=>b.disabled=true);
    }
    return {el, reveal};
  }

  // one stylesheet so every page that loads this file gets the tiles
  const css=document.createElement('style');
  css.textContent=`
.tl-line{direction:rtl;min-height:62px;border-bottom:2px solid var(--rule);padding:8px 2px;display:flex;flex-wrap:wrap;gap:6px;
  align-items:center;margin:8px 0 14px;transition:border-color var(--settle,220ms) var(--ease-out,ease-out)}
.tl-line.empty::after{content:"اضْغَطِ الْقِطَعَ بِالتَّرْتِيبِ";font-family:var(--ar);font-size:16px;line-height:1.8;color:var(--ink-soft);opacity:.55}
.tl-line.right{border-bottom-color:var(--verdigris)}
.tl-line.wrong{border-bottom-color:var(--rubric)}
.tl-pool{direction:rtl;display:flex;flex-wrap:wrap;gap:8px;min-height:48px;margin-bottom:14px}
.tl-tile{font-family:var(--ar);font-size:20px;line-height:1.7;direction:rtl;min-height:44px;padding:2px 14px;border-radius:10px;
  border:1px solid var(--rule);background:var(--card);color:var(--ink);cursor:pointer;touch-action:manipulation;
  user-select:none;-webkit-user-select:none;box-shadow:0 1px 0 var(--rule);
  transition:transform var(--press,120ms) var(--ease-out,ease-out),background .15s,color .15s,border-color .15s}
.tl-tile:active{transform:scale(.94)}
.tl-line .tl-tile{background:var(--paper-deep,var(--paper))}
.tl-line.right .tl-tile{background:var(--verdigris);border-color:var(--verdigris);color:#fff}
.tl-bar{display:flex;gap:8px}
.tl-bar .btn{flex:1}
.tl-bar .btn:disabled{opacity:.45;cursor:default}
.tl-verdict{font-size:14.5px;margin-top:10px;line-height:1.5}
.tl-verdict.ok{color:var(--verdigris)}
.tl-verdict.no{color:var(--rubric)}
@media (hover:hover) and (pointer:fine){.tl-tile:hover{border-color:var(--verdigris)}}`;
  document.head.appendChild(css);

  window.RafiqTiles={create, joinAr};
})();
