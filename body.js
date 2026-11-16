/* body.js — Practise → Everyday essentials → The body (#202, redesigned #392): a figure to
   explore, full screen. Each part has a dot: tap it to hear the word and see it on the card at the
   bottom, one word at a time. A dot with + can be looked at closer (the head, the hand…); ‹ zooms
   out again. "Find it" turns the view into a game: the word is said, tap where it is.
   Words: body-data.js (BODY_WORDS). This file is only the drawing, which shape is which part
   (svgZoneId), where each dot sits, and what each view frames. Uses audio.js (RQ) when present.
   Mounted by essentials.js.

   The drawing is one scene (a figure about 200 × 510 units, head at the top). A view is a box in
   that scene; zooming moves the scene with a CSS transform so the box fills the stage. */
(function(){
  const esc = t => String(t).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const CARD = 132;                              // the card's height in px: the figure is framed above it
  const reduce = () => matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- the drawing ---------- */
  // the hand, palm forward and thumb out, drawn round the wrist (0,0); placed by HAND
  const HAND = 'translate(164 260) rotate(-9)';
  const FINGERS = [[-5.6, 12], [-1.9, 16], [1.8, 17.5], [5.4, 15]];       // x, length (little → index)
  const handArt = `
    ${FINGERS.map(([x, l]) => `<rect class="skin" x="${x-1.8}" y="14" width="3.6" height="${l+2}" rx="1.8"/>`).join('')}
    <g transform="translate(7.6 5) rotate(-38)"><rect class="skin" x="-1.9" y="0" width="3.8" height="14" rx="1.9"/>
      <rect class="nailc" x="-1.2" y="9.6" width="2.4" height="3.2" rx="1.1"/></g>
    ${FINGERS.map(([x, l]) => `<rect class="nailc" x="${x-1.25}" y="${14+l-2.6}" width="2.5" height="3.2" rx="1.1"/>`).join('')}
    <path class="skin" d="M-7.6,0 L7.6,0 C9.4,6 9.8,12 8.4,17.6 C6,20.4 -6,20.4 -8.4,17.6 C-9.6,12 -9.4,6 -7.6,0 Z"/>
    <path class="crease" d="M-5.5,10 Q0,13 6,8.6"/>`;
  const handZones = `
    <path id="z-palm" class="zone" d="M-7.6,0 L7.6,0 C9.4,6 9.8,12 8.4,17.6 C6,20.4 -6,20.4 -8.4,17.6 C-9.6,12 -9.4,6 -7.6,0 Z"/>
    <path id="z-fingers" class="zone" d="M-7.8,19 L7.6,19 L7.6,30 L3.8,35.5 L-3.8,35.5 L-7.8,28 Z"/>
    <g id="z-thumb" class="zone"><rect transform="translate(7.6 5) rotate(-38)" x="-2.6" y="2" width="5.2" height="13" rx="2.6"/></g>
    <g id="z-nail" class="zone">${FINGERS.map(([x, l]) => `<rect x="${x-1.8}" y="${14+l-3.2}" width="3.6" height="4.4" rx="1.4"/>`).join('')}
      <rect transform="translate(7.6 5) rotate(-38)" x="-1.8" y="9" width="3.6" height="4.4" rx="1.4"/></g>`;
  const handPt = (x, y) => { const a = -9 * Math.PI / 180;
    return [164 + x * Math.cos(a) - y * Math.sin(a), 260 + x * Math.sin(a) + y * Math.cos(a)]; };

  const ARM = 'M128,106 C142,107 151,113 153,126 L160,196 L170,258 L158,261.5 L148,198 L140,146 L132,130 Z';
  const LEG = 'M100,292 L104,330 C106,356 109,370 110,382 C112,410 114,440 116,471 L128,471 C133,440 132,410 134,382 C137,352 138,322 134,286 L100,286 Z';
  const FOOT = 'M116,466 C115.5,480 112,489 111.5,496 C111.5,501 115,503.5 121,503.5 L146,503.5 C151,503.5 153.5,501 152.5,497.5 C151.5,494 146,492 140,490 C134,488 129.5,482 128,466 Z';
  const TRUNK = 'M90,102 C78,104 60,106 55,118 C56,130 59,140 61,150 C63,190 67,215 70,236 C67,255 65,272 66,290 L134,290 C135,272 133,255 130,236 C133,215 137,190 139,150 C141,140 144,130 145,118 C140,106 122,104 110,102 Z';
  const UPPER = 'M90,102 C78,104 60,106 55,118 C56,130 59,140 61,150 C63,190 67,215 69.5,238 L130.5,238 C133,215 137,190 139,150 C141,140 144,130 145,118 C140,106 122,104 110,102 Z';   // the trunk down to the waistband
  const HAIR = 'M70.5,55 C66,25 85,10 101,10.5 C119,11 136,24 129.5,55 C128.5,46 126,39 121,34 C114,38 101,38.5 92,33.5 C86,38.5 78,42 74.5,48 C72.8,50.5 71.5,52.5 70.5,55 Z';
  const LIPS = 'M90,70.6 C95,71.6 105,71.6 110,70.6 C109.5,77.5 105,81.2 100,81.2 C95,81.2 90.5,77.5 90,70.6 Z';     // a small, soft open smile
  const OPEN = 'M91.6,71.7 C96,72.4 104,72.4 108.4,71.7 C107.8,76.8 104.4,79.7 100,79.7 C95.6,79.7 92.2,76.8 91.6,71.7 Z';
  const TEETH = 'M92.2,72 C96,72.6 104,72.6 107.8,72 L107.3,74 C104,74.6 96,74.6 92.7,74 Z';
  const mirror = s => `<g transform="translate(200 0) scale(-1 1)">${s}</g>`;
  const both = s => s + mirror(s);

  // organs (stage 3): drawn over the trunk, shown only when looking inside
  const LUNG = 'M86,124 C75,127 70,150 71,172 C72,183 81,185 89,180 C93,168 93,140 91,127 C90,123.5 88,122.5 86,124 Z';
  const HEART = 'M104,171 C95,164 93,156 97.5,151.5 C100.5,148.5 104,150.5 104,153.5 C104.5,150.5 108.5,148.5 111.5,151.5 C115,155.5 113,164 104,171 Z';
  const LIVER = 'M70,187 C78,180 98,182 106,188 C102,198 88,204 75,202 C70.5,198 69,192 70,187 Z';
  const STOMACH = 'M107.5,185 C116,180 127,185 127,196 C127,207 118,213 108,209 C103.5,207 105,200.5 110.5,198.5 C114,197 112.5,190 107.5,185 Z';
  const GUT = 'M84,214 C84,210 116,210 116,214 L118,256 C118,263 82,263 82,256 Z';
  const BRAIN = 'M78,36 C76.5,24 89,18.5 100,19 C112,18.5 124,24 122,36 C121.5,42.5 112,45 100,44.5 C88,45 78.5,42.5 78,36 Z';
  const KIDNEY = 'M77,206 C72,206 70.5,212 71,217 C71.5,223 75,226 79,224.5 C81.5,223.5 80,220 81.5,216 C83,212 82,206 77,206 Z';

  /* The figure (owner, 16 Nov 2026: "more modern", #392): flat shapes with no ink outline, clothed (a long-sleeved top and
     trousers) and faceless like the word pictures. The face is drawn only where its parts are the lesson (the head and the
     mouth); the organs only when looking inside. */
  const SVG = `
<g class="bx-fig">
  <g class="legs">${both(`<path class="trs" d="${LEG}"/><path class="skin" d="${FOOT}"/>`)}</g>
  <g class="arms">${both(`<path class="slv" d="${ARM}"/>`)}
    ${both(`<g transform="${HAND}">${handArt}</g>`)}</g>
  <path class="top" d="${TRUNK}"/>
  <path class="hem" d="M66,284 L134,284"/>
  <g data-in="back"><path class="fold" d="M100,112 L100,270"/></g>
  <path class="skin" d="M90,84 L90,103 C95,106.5 105,106.5 110,103 L110,84 Z"/>
  ${both('<ellipse class="skin" cx="71" cy="55" rx="4.6" ry="8.5"/>')}
  <ellipse class="skin head" cx="100" cy="52" rx="29" ry="35"/>
  <path data-out="back" class="hair" d="${HAIR}"/>
  <g data-in="head mouth" class="face">
    ${both(`<path class="brow" d="M85,42.6 Q89,40.6 93,42.2"/>
      <ellipse class="pupil" cx="89" cy="49.5" rx="2.4" ry="3"/>
      <circle class="blush" cx="83.5" cy="62.5" r="4.6"/>`)}
    <path class="nose" d="M100.6,55.5 C99.8,58.6 98.4,60.4 98.8,61.6 C99.6,62.6 101.6,62.4 102.6,61.6"/>
    <path class="lips" d="${LIPS}"/><path class="mouthin" d="${OPEN}"/>
    <path class="teeth" d="${TEETH}"/><ellipse class="tongue" cx="100" cy="78" rx="4.4" ry="1.9"/>
  </g>
  <path data-in="back" class="hair" d="M70.6,52 C69.5,20 88,12 100,12.5 C116,12.5 131,22 129.4,52 C129.4,68 124,79 116,83 L84,83 C76,79 70.6,68 70.6,52 Z"/>
  <g data-in="inside" class="organs">
    <path class="org brainc" d="${BRAIN}"/>
    <path class="fold" d="M84,28.5 q4,-4 8,0 t8,0 t8,0 M81,37 q5,-4 9.5,0 t9.5,0 t9.5,0"/>
    <path class="fold" d="M100,100 L100,124 M100,124 L92,131 M100,124 L108,131"/>
    ${both(`<path class="org lung" d="${LUNG}"/><path class="org kidney" d="${KIDNEY}"/>`)}
    <path class="org liver" d="${LIVER}"/><path class="org stomach" d="${STOMACH}"/>
    <path class="org gut" d="${GUT}"/>
    <path class="fold" d="M89,224 c4,-4 8,4 12,0 s8,4 10,0 M89,236 c4,-4 8,4 12,0 s8,4 10,0 M89,248 c4,-4 8,4 12,0 s8,4 10,0"/>
    <path class="org heart" d="${HEART}"/>
  </g>
</g>
<g class="bx-zones">
  <rect id="z-body" class="zone" x="0" y="0" width="0" height="0"/>
  <path id="z-back" class="zone" d="${UPPER}"/>
  <path id="z-torso" class="zone" d="${UPPER}"/>
  <path id="z-chest" class="zone" d="M57,113 C70,105 130,105 143,113 L139.4,182 L60.6,182 Z"/>
  <path id="z-belly" class="zone" d="M60.6,182 L139.4,182 L131,240 L69,240 Z"/>
  <g id="z-arm" class="zone">${both(`<path d="${ARM}"/>`)}</g>
  <g id="z-hand" class="zone">${both(`<rect transform="${HAND}" x="-10" y="-1" width="27" height="37" rx="8"/>`)}</g>
  <g id="z-leg" class="zone">${both(`<path d="${LEG}"/>`)}</g>
  <g id="z-foot" class="zone">${both(`<path d="${FOOT}"/>`)}</g>
  <ellipse id="z-head" class="zone" cx="100" cy="52" rx="34" ry="37"/>
  <rect id="z-neck" class="zone" x="88" y="86" width="24" height="18" rx="4"/>
  <path id="z-hair" class="zone" d="${HAIR}"/>
  <ellipse id="z-forehead" class="zone" cx="100" cy="35.5" rx="16" ry="4.2"/>
  <g id="z-ear" class="zone">${both('<ellipse cx="71" cy="55" rx="6" ry="10"/>')}</g>
  <g id="z-cheek" class="zone">${both('<circle cx="83" cy="63" r="6.5"/>')}</g>
  <g id="z-eyebrow" class="zone">${both('<ellipse cx="89" cy="41.6" rx="6.4" ry="2.6"/>')}</g>
  <g id="z-eye" class="zone">${both('<ellipse cx="89" cy="49" rx="6" ry="4.4"/>')}</g>
  <ellipse id="z-nose" class="zone" cx="100" cy="57.5" rx="5.5" ry="8"/>
  <ellipse id="z-mouth" class="zone" cx="100" cy="75.8" rx="13" ry="8"/>
  <path id="z-lip" class="zone" fill-rule="evenodd" d="${LIPS} ${OPEN}"/>
  <path id="z-teeth" class="zone" d="M91.6,71.6 C96,72.2 104,72.2 108.4,71.6 L107.8,74.8 C104,75.4 96,75.4 92.2,74.8 Z"/>
  <ellipse id="z-tongue" class="zone" cx="100" cy="78" rx="5" ry="2.3"/>
  <ellipse id="z-chin" class="zone" cx="100" cy="85" rx="9" ry="3.6"/>
  <ellipse id="z-shoulder" class="zone" cx="145" cy="116" rx="10" ry="9"/>
  <path id="z-upperarm" class="zone" d="M141,128 L153.4,128 L159.3,188 L147,189.5 Z"/>
  <ellipse id="z-elbow" class="zone" cx="154" cy="197" rx="8.5" ry="7.5"/>
  <path id="z-forearm" class="zone" d="M148.4,205.5 L161,204 L168.6,250 L156.6,252.5 Z"/>
  <ellipse id="z-wrist" class="zone" transform="${HAND}" cx="0" cy="0" rx="8.4" ry="4"/>
  <g transform="${HAND}">${handZones}</g>
  <g id="z-thigh" class="zone">${both('<path d="M102.5,300 L136.5,292 L135.5,368 L108.5,370 Z"/>')}</g>
  <g id="z-knee" class="zone">${both('<ellipse cx="122" cy="381" rx="13" ry="9"/>')}</g>
  <g id="z-shin" class="zone">${both('<path d="M110,391 L134,391 L129,463 L115.6,463 Z"/>')}</g>
  <ellipse id="z-ankle" class="zone" cx="122" cy="472" rx="9" ry="6"/>
  <ellipse id="z-heel" class="zone" cx="115" cy="497" rx="6" ry="6.5"/>
  <ellipse id="z-toe" class="zone" cx="147" cy="499" rx="6.5" ry="5"/>
  <g id="z-waist" class="zone">${both('<ellipse cx="70" cy="230" rx="6" ry="14"/>')}</g>
  <circle id="z-navel" class="zone" cx="100" cy="226" r="4.5"/>
  <circle id="z-inside" class="zone" cx="116" cy="150" r="9"/>
  <path id="z-brain" class="zone" d="${BRAIN}"/>
  <g id="z-lungs" class="zone">${both(`<path d="${LUNG}"/>`)}</g>
  <path id="z-liver" class="zone" d="${LIVER}"/>
  <path id="z-stomach" class="zone" d="${STOMACH}"/>
  <g id="z-kidneys" class="zone">${both(`<path d="${KIDNEY}"/>`)}</g>
  <path id="z-intestines" class="zone" d="${GUT}"/>
  <path id="z-heart" class="zone" d="${HEART}"/>
</g>`;

  /* ---------- where each part's dot sits (scene units) ---------- */
  const AT = {
    head:[100,40], neck:[100,95], torso:[100,170], arm:[151,160], hand:[200 - handPt(1,16)[0], handPt(1,16)[1]], back:[100,168],
    leg:[78,395], foot:[140,497],
    hair:[100,18], forehead:[100,34], eyebrow:[117,43.5], eye:[89,55], ear:[71,56], cheek:[117,63], nose:[100,58.5], mouth:[100,75], chin:[100,85.5],
    lip:[93,79.6], teeth:[104.5,73.2], tongue:[100,78],
    shoulder:[146,114], upperarm:[150,158], elbow:[154,197], forearm:[160,228], wrist:handPt(0,0.5),
    palm:handPt(0,10), fingers:handPt(-1.9,24), thumb:handPt(12.4,13), nail:handPt(5.4,31),
    thigh:[118,328], knee:[122,381], shin:[122,428], ankle:[122,471], heel:[114,497], toe:[148,499],
    chest:[84,140], belly:[86,203], waist:[68,232], navel:[100,226], inside:[116,150],
    brain:[100,30], lungs:[79,152], liver:[85,193], kidneys:[75,216], heart:[105,160], stomach:[120,197], intestines:[100,240]
  };
  /* The views: the box each frames and the parts dotted in it. A part with a view of its own can be looked at closer;
     flip turns the figure round (reached by the Turn round button, not a dot); at moves a part's dot in this view. */
  const VIEWS = {
    body:  { box:[18,8,182,506],   parts:['head','neck','torso','arm','hand','leg','foot'] },
    back:  { box:[18,8,182,506],   parts:['back'], flip:true },
    head:  { box:[62,6,138,96],    parts:['hair','forehead','eyebrow','eye','ear','cheek','nose','mouth','chin'] },
    mouth: { box:[84,64,116,88],   parts:['lip','teeth','tongue'] },
    arm:   { box:[126,100,182,302], parts:['shoulder','upperarm','elbow','forearm','wrist','hand'], at:{ hand:handPt(1,18) } },
    hand:  { box:[146,250,190,302], parts:['wrist','palm','fingers','thumb','nail'] },
    leg:   { box:[50,284,150,508], parts:['thigh','knee','shin','ankle','foot'] },
    foot:  { box:[104,456,158,508], parts:['ankle','heel','toe'] },
    torso: { box:[50,98,150,296],  parts:['chest','inside','belly','navel','waist'] },
    inside:{ box:[62,12,138,268],  parts:['brain','lungs','heart','liver','stomach','kidneys','intestines'] }
  };

  /* ---------- styles ---------- */
  const css = document.createElement('style');
  css.textContent = `
.bx-full{position:fixed;inset:0;z-index:1000;background:var(--paper,#F1ECE0);display:flex;justify-content:center}
.bx-in{position:relative;width:100%;max-width:560px;height:100%;display:flex;flex-direction:column;
  padding:max(10px,env(safe-area-inset-top)) 12px max(12px,env(safe-area-inset-bottom))}
.bx-bar{display:flex;align-items:center;gap:8px;min-height:48px;flex:none}
.bx-up,.bx-x{flex:none;width:44px;height:44px;border-radius:50%;border:1px solid var(--rule);background:var(--card);color:var(--ink);
  font:600 20px/1 var(--la);cursor:pointer;touch-action:manipulation;transition:transform var(--press,120ms) var(--ease-out,ease-out)}
.bx-up:active,.bx-x:active{transform:scale(.92)}
.bx-up[hidden]{visibility:hidden;display:block}
.bx-crumbs{flex:1;min-width:0;text-align:center;font:600 16px/1.3 var(--la);color:var(--ink);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bx-crumbs small{display:block;font-weight:400;font-size:12.5px;color:var(--ink-soft)}
.bx-stage{position:relative;flex:1;min-height:0;border-radius:22px;overflow:hidden;touch-action:manipulation;user-select:none;-webkit-user-select:none;
  background:radial-gradient(120% 80% at 50% 30%,color-mix(in srgb,var(--verdigris) 9%,var(--card)),var(--card))}
.bx-svg{position:absolute;inset:0;width:100%;height:100%;display:block}
.bx-cam{transform-origin:0 0;transition:transform .65s cubic-bezier(.3,.7,.15,1)}
.bx-stage.still .bx-cam,.bx-stage.still .bx-fig{transition:none}
.bx-fig{transform-box:fill-box;transform-origin:center;transition:transform .22s ease-in}
/* the drawing keeps its own colours in dark mode too, like the word pictures */
.bx-svg{--sk:#E9C6A0;--tp:#2E7263;--tr:#27343B;--hr:#3A2A1C;--dp:#F6F1E6;--dr:#B4322A;--dg:#A8842C}
.bx-svg .skin{fill:var(--sk)}
.bx-svg .top{fill:var(--tp)}
.bx-svg .slv{fill:color-mix(in srgb,var(--tp) 86%,#000)}
.bx-svg .trs{fill:var(--tr)}
.bx-svg .hair{fill:var(--hr)}
.bx-svg .hem,.bx-svg .fold{fill:none;stroke:#00000026;stroke-width:1.2;stroke-linecap:round;vector-effect:non-scaling-stroke}
.bx-svg .arms .skin{stroke:#0000001f;stroke-width:1;vector-effect:non-scaling-stroke}
.bx-svg .nailc{fill:#F8E6D4}
.bx-svg .crease{fill:none;stroke:#0000002e;stroke-width:1.2;stroke-linecap:round;vector-effect:non-scaling-stroke}
.bx-svg .brow{fill:none;stroke:var(--hr);stroke-width:2.2;stroke-linecap:round;vector-effect:non-scaling-stroke}
.bx-svg .nose{fill:none;stroke:#0000003d;stroke-width:1.6;stroke-linecap:round;vector-effect:non-scaling-stroke}
.bx-svg .pupil{fill:#2A2320}
.bx-svg .blush{fill:#E8907A;opacity:.4}
.bx-svg .lips{fill:#D98B7E}
.bx-svg .mouthin{fill:#7A3A35}
.bx-svg .teeth{fill:#fff}
.bx-svg .tongue{fill:#E58C86}
.bx-svg .org{stroke:var(--dp);stroke-width:1.5;vector-effect:non-scaling-stroke}
.bx-svg .brainc{fill:#E2A6A0}
.bx-svg .lung{fill:#E08E86}
.bx-svg .heart{fill:var(--dr)}
.bx-svg .liver{fill:#8C3B34}
.bx-svg .stomach{fill:#D2A85A}
.bx-svg .gut{fill:#E6C88F}
.bx-svg .kidney{fill:#A8553F}
.bx-svg [data-in],.bx-svg [data-out],.bx-svg .top,.bx-svg .slv,.bx-svg .head{transition:opacity .35s}
.bx-svg [data-in]{opacity:0}
.bx-stage.v-inside .top,.bx-stage.v-inside .slv{opacity:.22}
.bx-stage.v-inside .head{opacity:.55}
.bx-stage.v-inside .hair{opacity:.12!important}
.bx-svg .zone{fill:transparent;stroke:none;pointer-events:none}
.bx-svg .zone.live{pointer-events:all;cursor:pointer}
.bx-svg .zone.on,.bx-svg .zone.on *{fill:#fff;fill-opacity:.3;stroke:#fff;stroke-width:2.5;vector-effect:non-scaling-stroke}
.bx-dots{position:absolute;inset:0;pointer-events:none;transition:opacity .2s}
.bx-dots.hide{opacity:0}
.bx-dots.hide .bx-dot{pointer-events:none}
.bx-dot{position:absolute;width:40px;height:40px;margin:-20px 0 0 -20px;border:0;padding:0;background:none;border-radius:50%;cursor:pointer;
  pointer-events:auto;touch-action:manipulation;-webkit-tap-highlight-color:transparent}
.bx-dot i{position:absolute;inset:11px;border-radius:50%;background:#fff;box-shadow:0 0 0 2px var(--verdigris),0 2px 6px #0003;
  transition:transform .28s cubic-bezier(.3,1.5,.5,1),background .2s,box-shadow .2s}
.bx-dot::before{content:"";position:absolute;inset:11px;border-radius:50%;border:2px solid #fff;opacity:0;animation:bx-pulse 2.4s ease-out infinite}
.bx-dot:nth-child(3n)::before{animation-delay:.5s}.bx-dot:nth-child(3n+1)::before{animation-delay:1.1s}
.bx-dot.seen i{background:var(--verdigris);box-shadow:0 0 0 2px #fff,0 2px 6px #0003}
.bx-dot.seen::before,.bx-dot.on::before,.bx-stage.game .bx-dot::before{animation:none}
.bx-dot.more i::after{content:"+";position:absolute;inset:0;display:grid;place-items:center;font:700 14px/1 var(--la);color:var(--verdigris)}
.bx-dot.more.seen i::after{color:#fff}
.bx-stage.game .bx-dot.more i::after{content:""}
.bx-stage.game .bx-dot i{background:#fff;box-shadow:0 0 0 2px var(--ink),0 2px 6px #0003}
.bx-dot:active i{transform:scale(.85)}
.bx-dot.on i{transform:scale(1.5);background:var(--gold,#A8842C);box-shadow:0 0 0 3px #fff,0 3px 10px #0004}
.bx-dot.on.more i::after{color:#fff}
.bx-dot.right i{transform:scale(1.4);background:var(--verdigris)!important;box-shadow:0 0 0 3px #fff,0 3px 10px #0004!important}
.bx-dot.done{pointer-events:none}
.bx-dot.done i{background:var(--verdigris)!important;opacity:.55;transform:scale(.8)}
.bx-dot.wrong i{background:var(--cinnabar,#B4322A)!important;animation:bx-shake .32s ease-out}
.bx-dot.hint::before{animation:bx-pulse .9s ease-out infinite;border-color:var(--gold,#A8842C);border-width:3px}
@keyframes bx-pulse{0%{transform:scale(1);opacity:.9}70%,100%{transform:scale(2.4);opacity:0}}
@keyframes bx-shake{0%,100%{translate:0}25%{translate:-5px}75%{translate:5px}}
.bx-turn{position:absolute;top:12px;right:12px;min-height:40px;padding:0 14px;border-radius:999px;border:1px solid var(--rule);
  background:color-mix(in srgb,var(--card) 82%,transparent);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);
  color:var(--ink);font:600 14px var(--la);cursor:pointer;touch-action:manipulation;transition:transform var(--press,120ms) var(--ease-out,ease-out)}
.bx-turn:active{transform:scale(.95)}
.bx-turn[hidden]{display:none}
.bx-card{position:absolute;left:10px;right:10px;bottom:10px;height:${CARD}px;border-radius:20px;padding:14px 16px;
  background:color-mix(in srgb,var(--card) 86%,transparent);backdrop-filter:blur(18px) saturate(1.4);-webkit-backdrop-filter:blur(18px) saturate(1.4);
  border:1px solid var(--rule);box-shadow:0 8px 28px #0000001f;display:flex;align-items:center;gap:12px}
.bx-card.in{animation:bx-in .34s cubic-bezier(.3,1.35,.5,1)}
@keyframes bx-in{from{transform:translateY(22px);opacity:0}to{transform:none;opacity:1}}
.bx-w{flex:1;min-width:0}
.bx-w .a{font-family:var(--ar);font-size:34px;line-height:1.5;direction:rtl;text-align:left;color:var(--ink)}
.bx-w .e{font:600 16px/1.3 var(--la);color:var(--ink)}
.bx-w .t{font:400 13.5px/1.3 var(--la);color:var(--ink-soft)}
.bx-w .idle{font:400 15px/1.45 var(--la);color:var(--ink-soft)}
.bx-w .idle b{display:block;color:var(--ink);font-size:16px}
.bx-w .ask{font:600 13px/1.2 var(--la);color:var(--ink-soft);text-transform:uppercase;letter-spacing:.06em}
.bx-acts{display:flex;flex-direction:column;gap:8px;align-items:stretch;flex:none}
.bx-btn{min-height:44px;padding:0 16px;border-radius:999px;border:0;background:var(--verdigris);color:#fff;font:600 15px var(--la);cursor:pointer;
  touch-action:manipulation;white-space:nowrap;transition:transform var(--press,120ms) var(--ease-out,ease-out)}
.bx-btn.ghost{background:none;border:1px solid var(--rule);color:var(--ink)}
.bx-btn:active{transform:scale(.95)}
.bx-say{width:48px;height:48px;padding:0;font-size:20px}
.bx-say.speaking{background:var(--gold,#A8842C)}
.bx-prog{height:4px;border-radius:2px;background:var(--rule);margin-top:8px;overflow:hidden}
.bx-prog span{display:block;height:100%;background:var(--verdigris);border-radius:2px;transition:width .3s ease-out}
@media (max-width:380px){.bx-w .a{font-size:29px}.bx-btn{padding:0 12px;font-size:14px}}
@media (prefers-reduced-motion:reduce){.bx-cam,.bx-fig,.bx-dot i,.bx-svg [data-in],.bx-svg [data-out]{transition:none}
  .bx-dot::before,.bx-card.in,.bx-dot.wrong i{animation:none}}`;
  document.head.appendChild(css);

  /* ---------- the words ---------- */
  let WORDS = null;
  const word = id => WORDS.find(w => w.id === id);
  // the Arabic of words also in the word list comes from vocab-data.js: load it if this page hasn't
  function ready(){
    if(WORDS) return Promise.resolve();
    const go = () => { WORDS = BODY_RESOLVE(typeof VOCAB !== 'undefined' ? VOCAB : []); };
    if(typeof VOCAB !== 'undefined'){ go(); return Promise.resolve(); }
    return new Promise(res => {
      const s = document.createElement('script'); s.src = 'vocab-data.js';
      s.onload = s.onerror = () => { go(); res(); };
      document.head.appendChild(s);
    });
  }
  // the count on the menu card: each different word once (السّاق is both the leg and the shin)
  const count = () => new Set(BODY_WORDS.filter(w => w.level > 0).map(w => w.ar || 'v' + w.vocab)).size;
  const cap = s => s.charAt(0).toUpperCase() + s.slice(1);
  const short = w => w.en.replace(/^the /, '');
  const shuffle = a => { a = a.slice(); for(let i = a.length - 1; i > 0; i--){ const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };

  /* ---------- the explorer ---------- */
  function mount(el, opts){
    opts = opts || {};
    el.innerHTML = `<div class="bx-full"><div class="bx-in">
      <div class="bx-bar"><button class="bx-up" type="button" aria-label="Back" hidden>‹</button>
        <div class="bx-crumbs" aria-live="polite"></div>
        <button class="bx-x es-back" type="button" aria-label="Close, back to all essentials">✕</button></div>
      <div class="bx-stage still" role="group" aria-label="A drawing of a person: tap a dot to hear that part in Arabic">
        <svg class="bx-svg" aria-hidden="true"><g class="bx-cam">${SVG}</g></svg>
        <div class="bx-dots"></div>
        <button class="bx-turn" type="button" hidden>↻ Turn round</button>
        <div class="bx-card" aria-live="polite"></div>
      </div></div></div>`;
    const scrollWas = document.documentElement.style.overflow;
    document.documentElement.style.overflow = 'hidden';
    const stage = el.querySelector('.bx-stage'), cam = el.querySelector('.bx-cam'), fig = el.querySelector('.bx-fig'),
      dots = el.querySelector('.bx-dots'), up = el.querySelector('.bx-up'), crumbs = el.querySelector('.bx-crumbs'),
      card = el.querySelector('.bx-card'), turn = el.querySelector('.bx-turn');
    el.querySelector('.bx-x').onclick = () => { stop(); el.innerHTML = ''; if(opts.back) opts.back(); };
    const stack = ['body'], seen = new Set();
    let sel = null, busy = 0, flipped = false, timer = null, game = null;
    const cur = () => stack[stack.length - 1], view = () => VIEWS[cur()];
    const say = (w, b) => { if(window.RQ) RQ.speak(w.say, b || null); };

    ready().then(() => draw(false));

    function chrome(){
      const v = view(), n = v.parts.filter(p => seen.has(p)).length;
      crumbs.innerHTML = esc(cap(short(word(cur()))))
        + `<small>${game ? 'Find it' : n + ' of ' + v.parts.length + ' heard'}</small>`;
      up.hidden = stack.length < 2;
      turn.hidden = cur() !== 'body' || !!game;
    }
    const out = () => { if(game){ game = null; stage.classList.remove('game'); sel = null; draw(false); return; }
      if(stack.length > 1){ stack.pop(); sel = null; draw(true); } };
    up.onclick = out;
    turn.onclick = () => { say(word('back'), turn); stack.push('back'); sel = null; draw(true); };
    const onKey = e => { if(!stage.isConnected) return stop(); if(e.key === 'Escape' && (stack.length > 1 || game)){ e.preventDefault(); out(); } };
    document.addEventListener('keydown', onKey);

    // the camera: the view's box as big as fits above the card, in the middle
    function camera(v){
      const W = stage.clientWidth, H = stage.clientHeight, pad = 30, y0s = 18, room = H - y0s - CARD - 34;
      const [x0, y0, x1, y1] = v.box, s = Math.min((W - 2 * pad) / (x1 - x0), room / (y1 - y0));
      return { s, cx: (x0 + x1) / 2, cy: (y0 + y1) / 2, ox: W / 2, oy: y0s + room / 2 };
    }
    const toStage = (c, p) => [c.ox + (p[0] - c.cx) * c.s, c.oy + (p[1] - c.cy) * c.s];

    function draw(animate){
      const v = view(), id = cur();
      busy++; const mine = busy;
      clearTimeout(timer);
      if(!animate || reduce()) stage.classList.add('still'); else stage.classList.remove('still');
      stage.className = stage.className.replace(/\bv-\S+/g, '').trim() + ' v-' + id;
      chrome();
      const c = camera(v);
      cam.style.transform = `translate(${c.ox}px,${c.oy}px) scale(${c.s}) translate(${-c.cx}px,${-c.cy}px)`;
      // what's drawn only in some views, and which shapes can be tapped here
      const flip = !!v.flip;
      stage.querySelectorAll('[data-in]').forEach(n => n.style.opacity = n.dataset.in.split(' ').includes(id) ? 1 : 0);
      stage.querySelectorAll('[data-out]').forEach(n => n.style.opacity = n.dataset.out.split(' ').includes(id) ? 0 : 1);
      stage.querySelectorAll('.zone').forEach(z => z.classList.remove('live', 'on'));
      v.parts.forEach(pid => { const z = stage.querySelector('#' + word(pid).svgZoneId); if(z) z.classList.add('live'); });
      if(flip !== flipped && animate && !reduce()){              // turn round: squash, swap, open
        fig.style.transform = 'scaleX(0)';
        setTimeout(() => { if(mine !== busy) return; flipped = flip; fig.style.transform = 'scaleX(1)'; }, 220);
      } else flipped = flip;
      dots.innerHTML = v.parts.map(pid => {
        const w = word(pid), p = toStage(c, (v.at && v.at[pid]) || AT[pid]), more = VIEWS[pid] && pid !== id;
        return `<button type="button" class="bx-dot${more ? ' more' : ''}${seen.has(pid) ? ' seen' : ''}" data-id="${pid}"
          style="left:${p[0].toFixed(1)}px;top:${p[1].toFixed(1)}px" aria-label="${esc(w.en)}${more ? ', can be looked at closer' : ''}"><i></i></button>`;
      }).join('');
      dots.classList.add('hide');
      dots.querySelectorAll('.bx-dot').forEach(b => b.onclick = () => tap(b.dataset.id));
      const show = () => { if(mine !== busy) return; dots.classList.remove('hide'); stage.classList.remove('still'); if(sel) mark(sel); };
      if(game) ask(); else showCard();
      if(stage.classList.contains('still')) show(); else timer = setTimeout(show, 680);
    }

    stage.querySelector('.bx-zones').addEventListener('click', e => {
      const z = e.target.closest('.zone.live'); if(!z) return;
      const w = WORDS.find(x => x.svgZoneId === z.id && view().parts.includes(x.id));
      if(w) tap(w.id);
    });

    const dot = id => dots.querySelector(`[data-id="${id}"]`);
    function mark(id){
      stage.querySelectorAll('.zone.on').forEach(z => z.classList.remove('on'));
      dots.querySelectorAll('.bx-dot.on').forEach(b => b.classList.remove('on'));
      if(!id) return;
      const z = stage.querySelector('#' + word(id).svgZoneId); if(z) z.classList.add('on');
      const b = dot(id); if(b) b.classList.add('on', 'seen');
    }

    // the card at the bottom: one word at a time
    function showCard(){
      const v = view();
      card.classList.remove('in'); void card.offsetWidth; card.classList.add('in');
      if(!sel){
        const n = v.parts.length;
        card.innerHTML = `<div class="bx-w"><div class="idle"><b>Tap a dot to hear it</b>${cur() === 'back' ? 'This is the back.' : 'A dot with + opens up.'}
          <span style="display:block;font-size:12px;margin-top:4px">Words awaiting a teacher’s check.</span></div></div>`
          + (n >= 3 ? `<div class="bx-acts"><button class="bx-btn bx-play" type="button">▶ Find it</button></div>` : '');
        const pl = card.querySelector('.bx-play'); if(pl) pl.onclick = start;
        return;
      }
      const w = word(sel), more = VIEWS[sel] && sel !== cur();
      card.innerHTML = `<div class="bx-w"><div class="a" lang="ar">${esc(w.ar)}</div><div class="e">${esc(w.en)}</div><div class="t">${esc(w.tr)}</div></div>
        <div class="bx-acts"><button class="bx-btn bx-say" type="button" aria-label="Hear it again">🔊</button>
        ${more ? `<button class="bx-btn ghost bx-more" type="button">Look closer</button>` : ''}</div>`;
      card.querySelector('.bx-say').onclick = e => say(w, e.currentTarget);
      const m = card.querySelector('.bx-more'); if(m) m.onclick = () => { stack.push(sel); sel = null; draw(true); };
    }

    function tap(id){
      if(game) return answer(id);
      const w = word(id);
      seen.add(id); sel = id; mark(id); chrome(); showCard();
      say(w, card.querySelector('.bx-say'));
    }

    /* Find it: the word is said and shown, tap where it is. A miss comes back later; after two misses its dot is shown. */
    function start(){
      game = { queue: shuffle(view().parts), total: view().parts.length, missed: new Set(), miss: 0, done: 0 };
      sel = null; mark(null); stage.classList.add('game'); chrome();
      dots.querySelectorAll('.bx-dot').forEach(b => b.classList.remove('seen', 'done', 'right'));
      ask();
    }
    function ask(){
      const w = word(game.queue[0]);
      game.miss = 0;
      card.classList.remove('in'); void card.offsetWidth; card.classList.add('in');
      card.innerHTML = `<div class="bx-w"><div class="ask">Tap this part</div><div class="a" lang="ar">${esc(w.ar)}</div>
        <div class="bx-prog"><span style="width:${game.done / game.total * 100}%"></span></div></div>
        <div class="bx-acts"><button class="bx-btn bx-say" type="button" aria-label="Hear it again">🔊</button></div>`;
      card.querySelector('.bx-say').onclick = e => say(w, e.currentTarget);
      say(w, card.querySelector('.bx-say'));
    }
    function answer(id){
      const want = game.queue[0], b = dot(id);
      if(!b || b.classList.contains('done')) return;
      if(id === want){
        game.done++; game.queue.shift();
        dots.querySelectorAll('.hint').forEach(x => x.classList.remove('hint'));
        b.classList.add('right'); seen.add(id);
        const mine = busy;
        setTimeout(() => { if(mine !== busy || !game) return; b.classList.remove('right'); b.classList.add('done');
          if(game.queue.length) ask(); else finish(); }, reduce() ? 250 : 650);
        return;
      }
      game.miss++; game.missed.add(want);
      b.classList.remove('wrong'); void b.offsetWidth; b.classList.add('wrong');
      setTimeout(() => b.classList.remove('wrong'), 400);
      if(game.miss === 1 && game.queue.length > 1){ game.queue.push(game.queue.shift()); const mine = busy;   // it comes back later
        setTimeout(() => { if(mine === busy && game) ask(); }, 500); }
      else { const h = dot(want); if(h) h.classList.add('hint'); }
    }
    function finish(){
      const g = game; g.first = g.total - g.missed.size;
      card.classList.remove('in'); void card.offsetWidth; card.classList.add('in');
      card.innerHTML = `<div class="bx-w"><div class="e">${g.first === g.total ? 'All ' + g.total + ' first time 🎉' : 'Found all ' + g.total}</div>
        <div class="t">${g.first === g.total ? 'Try another part of the body.' : g.first + ' of ' + g.total + ' first time. Play again to beat it.'}</div></div>
        <div class="bx-acts"><button class="bx-btn bx-again" type="button">Play again</button><button class="bx-btn ghost bx-done" type="button">Explore</button></div>`;
      card.querySelector('.bx-again').onclick = start;
      card.querySelector('.bx-done').onclick = out;
    }

    function stop(){ busy++; clearTimeout(timer); removeEventListener('resize', onResize); document.removeEventListener('keydown', onKey);
      document.documentElement.style.overflow = scrollWas; }
    let rz = null; const onResize = () => { clearTimeout(rz); rz = setTimeout(() => { if(stage.isConnected) draw(false); else stop(); }, 120); };
    addEventListener('resize', onResize);
  }

  window.RafiqBody = { mount, count, ready, VIEWS, AT };
})();
