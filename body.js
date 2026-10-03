/* body.js — Practise → Everyday essentials → The body (#202): a drawing of a
   person to explore. Tap a region (the head, the arm…) to zoom in and see its
   parts; tap any part to hear it. ← Back and the breadcrumb zoom out again.
   Words: body-data.js (BODY_WORDS). This file is only the drawing, which shape
   is which part (svgZoneId), where each label's line points, and what each
   view frames. Uses audio.js (RQ) when present. Mounted by essentials.js.

   The drawing is one scene (a figure about 200 × 510 units, head at the top).
   A view is a box in that scene plus the labels down each side; zooming moves
   the scene with a CSS transform so the box fills the middle of the stage. */
(function(){
  const esc = t => String(t).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const W = 300, H = 400;                       // the stage's own units (its viewBox); it's always 3:4
  const reduce = () => matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- the drawing ---------- */
  // the hand, palm forward and thumb out, drawn round the wrist (0,0); placed by HAND
  const HAND = 'translate(164 260) rotate(-9)';
  const FINGERS = [[-5.6, 12], [-1.9, 16], [1.8, 17.5], [5.4, 15]];       // x, length (little → index)
  const handArt = `
    ${FINGERS.map(([x, l]) => `<rect class="skin ink" x="${x-1.8}" y="14" width="3.6" height="${l+2}" rx="1.8"/>`).join('')}
    <g transform="translate(7.6 5) rotate(-38)"><rect class="skin ink" x="-1.9" y="0" width="3.8" height="14" rx="1.9"/>
      <rect class="nailc fine" x="-1.2" y="9.6" width="2.4" height="3.2" rx="1.1"/></g>
    ${FINGERS.map(([x, l]) => `<rect class="nailc fine" x="${x-1.25}" y="${14+l-2.6}" width="2.5" height="3.2" rx="1.1"/>`).join('')}
    <path class="skin ink" d="M-7.6,0 L7.6,0 C9.4,6 9.8,12 8.4,17.6 C6,20.4 -6,20.4 -8.4,17.6 C-9.6,12 -9.4,6 -7.6,0 Z"/>
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

  const SVG = `
<g class="bx-fig">
  <g class="arms">${both(`<path class="skin ink" d="${ARM}"/>`)}
    ${both(`<g transform="${HAND}">${handArt}</g>`)}</g>
  <g class="legs">${both(`<path class="skin ink" d="${LEG}"/><path class="skin ink" d="${FOOT}"/>
    <path class="crease" d="M146,503.5 C146.5,500 149,498.5 151.5,499.5 M141.5,503.5 C142,500.5 144,499.5 146,500"/>
    <path class="crease" d="M127.5,473 q3.2,2.4 0,5.4"/><path class="crease" d="M113,381 q9,4 18,0"/>`)}</g>
  ${both('<path class="crease" d="M148.6,194.5 q3.4,2.6 7.4,1.4"/>')}
  <path class="skin ink" d="${TRUNK}"/>
  <g data-out="back">
    <ellipse class="navel" cx="100" cy="226" rx="1.5" ry="2.2"/></g>
  <g data-in="back"><path class="crease" d="M100,112 L100,232"/>
    <path class="crease" d="M80,128 C75,140 78,152 87,156 M120,128 C125,140 122,152 113,156"/></g>
  <path class="shorts ink" d="M69.5,236 C68,250 65.5,270 65,290 L60,348 L99,348 L100,306 L101,348 L140,348 L135,290 C134.5,270 132,250 130.5,236 Z"/>
  <path class="crease" d="M69,244 L131,244"/>
  <path class="skin ink" d="M90,84 L90,103 C95,106.5 105,106.5 110,103 L110,84 Z"/>
  ${both('<ellipse class="skin ink" cx="71" cy="55" rx="4.6" ry="8.5"/><path class="crease" d="M72.5,50 q-3,5 0,10"/>')}
  <ellipse class="skin ink" cx="100" cy="52" rx="29" ry="35"/>
  <g data-out="back">
    <path class="hair ink" d="${HAIR}"/>
    ${both(`<path class="brow" d="M85,42.6 Q89,40.6 93,42.2"/>
      <ellipse class="pupil" cx="89" cy="49.5" rx="2.6" ry="3.2"/><circle class="glint" cx="90" cy="48.3" r="0.9"/>
      <circle class="blush" cx="83.5" cy="62.5" r="4.6"/>`)}
    <path class="crease" d="M100.6,55.5 C99.8,58.6 98.4,60.4 98.8,61.6 C99.6,62.6 101.6,62.4 102.6,61.6"/>
    <path class="lips" d="${LIPS}"/><path class="mouthin" d="${OPEN}"/>
    <path class="teeth" d="${TEETH}"/><ellipse class="tongue" cx="100" cy="78" rx="4.4" ry="1.9"/>
  </g>
  <path data-in="back" class="hair ink" d="M70.6,52 C69.5,20 88,12 100,12.5 C116,12.5 131,22 129.4,52 C129.4,68 124,79 116,83 L84,83 C76,79 70.6,68 70.6,52 Z"/>
  <g data-in="inside" class="organs">
    <path class="org brainc ink" d="${BRAIN}"/>
    <path class="crease" d="M84,28.5 q4,-4 8,0 t8,0 t8,0 M81,37 q5,-4 9.5,0 t9.5,0 t9.5,0"/>
    <path class="crease" d="M100,100 L100,124 M100,124 L92,131 M100,124 L108,131"/>
    ${both(`<path class="org lung ink" d="${LUNG}"/><path class="org kidney ink" d="${KIDNEY}"/>`)}
    <path class="org liver ink" d="${LIVER}"/><path class="org stomach ink" d="${STOMACH}"/>
    <path class="org gut ink" d="${GUT}"/>
    <path class="crease" d="M89,224 c4,-4 8,4 12,0 s8,4 10,0 M89,236 c4,-4 8,4 12,0 s8,4 10,0 M89,248 c4,-4 8,4 12,0 s8,4 10,0"/>
    <path class="org heart ink" d="${HEART}"/>
  </g>
  <g data-in="torso" class="peek"><circle cx="104" cy="160" r="9"/><path d="M104,155.5 v9 M99.5,160 h9"/></g>
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
  <circle id="z-inside" class="zone" cx="104" cy="160" r="10"/>
  <path id="z-brain" class="zone" d="${BRAIN}"/>
  <g id="z-lungs" class="zone">${both(`<path d="${LUNG}"/>`)}</g>
  <path id="z-liver" class="zone" d="${LIVER}"/>
  <path id="z-stomach" class="zone" d="${STOMACH}"/>
  <g id="z-kidneys" class="zone">${both(`<path d="${KIDNEY}"/>`)}</g>
  <path id="z-intestines" class="zone" d="${GUT}"/>
  <path id="z-heart" class="zone" d="${HEART}"/>
</g>`;

  /* ---------- where each label points (scene units) ---------- */
  const AT = {
    head:[76,32], neck:[93,96], chest:[84,148], torso:[124,196], arm:[157,172], hand:handPt(1,14), belly:[90,212],
    back:[123,108], leg:[124,410], foot:[140,497],
    hair:[82,20], forehead:[92,35], eyebrow:[86,41.6], eye:[87.5,50], ear:[69.5,60], cheek:[82,64],
    nose:[101.5,60], mouth:[109.6,72], teeth:[103,73.2], tongue:[102,78.2], lip:[96,80.6], chin:[103,86],
    shoulder:[146,113], upperarm:[156,156], elbow:[149,198], forearm:[164,228], wrist:handPt(-6,0.5),
    palm:handPt(-2,10), fingers:handPt(-1.9,27), thumb:handPt(12.2,15), nail:handPt(5.4,30.6),
    thigh:[111,328], knee:[121,383], shin:[118,428], ankle:[127,474], heel:[112.5,497], toe:[150,499],
    waist:[67,232], navel:[100,226.5], inside:[104,160],
    brain:[90,27], lungs:[79,152], liver:[84,193], kidneys:[75,216], heart:[106,161], stomach:[121,195], intestines:[110,240]
  };
  /* The views: the box they frame, and the labels down the left (l) and right (r).
     A part with a view of its own zooms into it; flip turns the figure round;
     at moves a label's point (to the hand or leg on its own side); lit is lit on arrival. */
  const VIEWS = {
    body:  { box:[18,8,182,506],  l:['head','neck','torso','hand'], r:['back','arm','leg','foot'],
             at:{ torso:[80,190], hand:[200 - handPt(1,14)[0], handPt(1,14)[1]] } },      // the torso and hand on their side
    back:  { box:[18,8,182,506],  l:[], r:['back'], flip:true, lit:'back', at:{ back:[116,168] } },
    head:  { box:[65,10,135,92],  l:['hair','forehead','eyebrow','eye','ear','cheek','lip'], r:['nose','mouth','teeth','tongue','chin'] },
    arm:   { box:[126,102,180,302], l:['shoulder','elbow','wrist'], r:['upperarm','forearm','hand'] },
    hand:  { box:[148,252,188,300], l:['wrist','palm','fingers'], r:['thumb','nail'] },
    leg:   { box:[50,286,150,506], l:['thigh','knee','shin'], r:['ankle','foot'], at:{ thigh:[89,328], knee:[79,383], shin:[82,428] } },
    foot:  { box:[106,458,156,506], l:['heel'], r:['ankle','toe'] },
    torso: { box:[52,100,148,300], l:['chest','waist'], r:['inside','belly','navel'] },
    inside:{ box:[64,14,136,266], l:['brain','lungs','liver','kidneys'], r:['heart','stomach','intestines'] }
  };

  /* ---------- styles ---------- */
  const css = document.createElement('style');
  css.textContent = `
.bx-bar{display:flex;align-items:center;gap:10px;min-height:40px;margin:0 0 8px}
.bx-up{border:1px solid var(--rule);background:var(--card);color:var(--ink);border-radius:999px;min-height:40px;padding:0 14px;
  font:600 14px var(--la);cursor:pointer;touch-action:manipulation;transition:transform var(--press,120ms) var(--ease-out,ease-out)}
.bx-up:active{transform:scale(.95)}
.bx-up[hidden]{display:none}
.bx-crumbs{flex:1;min-width:0;font-size:14px;color:var(--ink-soft);line-height:1.4}
.bx-crumbs button{background:none;border:0;padding:6px 2px;font:inherit;color:var(--verdigris);cursor:pointer;text-decoration:underline;text-underline-offset:3px}
.bx-crumbs b{color:var(--ink);font-weight:600}
.bx-crumbs .sep{margin:0 3px;color:var(--ink-soft)}
.bx-stage{position:relative;width:100%;max-width:480px;aspect-ratio:3/4;margin:0 auto;background:var(--card);border:1px solid var(--rule);
  border-radius:14px;overflow:hidden;touch-action:manipulation;user-select:none;-webkit-user-select:none}
.bx-svg,.bx-lines{position:absolute;inset:0;width:100%;height:100%;display:block}
.bx-lines{pointer-events:none}
.bx-cam{transition:transform .7s cubic-bezier(.3,.7,.15,1)}
.bx-stage.still .bx-cam,.bx-stage.still .bx-fig{transition:none}
.bx-fig{transform-box:fill-box;transform-origin:center;transition:transform .22s ease-in}
/* the drawing keeps its own colours in dark mode too, like a printed picture: the light theme's ink, paper and accents */
.bx-svg{--di:#3B3431;--dp:#F1ECE0;--dr:#B4322A;--dv:#2E7263;--dg:#A8842C}      /* a warm brown ink: softer than the page's */
.bx-svg .ink{stroke:var(--di);stroke-width:1.5;stroke-linejoin:round;vector-effect:non-scaling-stroke}
.bx-svg .fine{stroke:var(--di);stroke-width:1;vector-effect:non-scaling-stroke}
.bx-svg .skin{fill:#F0D6B4}
.bx-svg .hair{fill:#4A3A31}
.bx-svg .shorts{fill:color-mix(in srgb,var(--dv) 32%,var(--dp))}
.bx-svg .crease,.bx-svg .brow{fill:none;stroke:var(--di);stroke-width:1;stroke-linecap:round;vector-effect:non-scaling-stroke}
.bx-svg .brow{stroke:#4A3A31;stroke-width:1.8}
.bx-svg .glint{fill:#fff}
.bx-svg .pupil,.bx-svg .navel{fill:var(--di)}
.bx-svg .blush{fill:#E8907A;opacity:.35}
.bx-svg .lips{fill:#D98B7E}
.bx-svg .mouthin{fill:#7A3A35}
.bx-svg .teeth{fill:#fff}
.bx-svg .tongue{fill:#E58C86}
.bx-svg .nailc{fill:#F8E6D4}
.bx-svg .org{stroke-width:1.2}
.bx-svg .brainc{fill:color-mix(in srgb,var(--dr) 22%,var(--dp))}
.bx-svg .lung{fill:color-mix(in srgb,var(--dr) 32%,var(--dp))}
.bx-svg .heart{fill:var(--dr)}
.bx-svg .liver{fill:color-mix(in srgb,var(--dr) 55%,var(--di))}
.bx-svg .stomach{fill:color-mix(in srgb,var(--dg) 55%,var(--dp))}
.bx-svg .gut{fill:color-mix(in srgb,var(--dg) 30%,var(--dp))}
.bx-svg .kidney{fill:color-mix(in srgb,var(--dr) 45%,var(--dg))}
.bx-svg .peek circle{fill:var(--dp);stroke:var(--dv);stroke-width:1.6;stroke-dasharray:3 2;vector-effect:non-scaling-stroke}
.bx-svg .peek path{stroke:var(--dv);stroke-width:1.6;vector-effect:non-scaling-stroke}
.bx-svg [data-in],.bx-svg [data-out]{transition:opacity .35s}
.bx-svg [data-in]{opacity:0}
.bx-stage.v-inside .shorts,.bx-stage.v-inside .crease:not(.organs .crease){opacity:.35}
.bx-stage.v-inside .skin{fill-opacity:.55}
.bx-svg .zone{fill:transparent;stroke:none;pointer-events:none}
.bx-svg .zone.live{pointer-events:all;cursor:pointer}
.bx-svg .zone.on,.bx-svg .zone.on *{fill:var(--verdigris);fill-opacity:.28;stroke:var(--verdigris);stroke-width:2;vector-effect:non-scaling-stroke}
.bx-lines line{stroke:var(--ink-soft);stroke-width:1;vector-effect:non-scaling-stroke}
.bx-lines line.dash{stroke-dasharray:3 3}
.bx-lines circle{fill:var(--ink-soft)}
.bx-lines .on line{stroke:var(--verdigris);stroke-width:2}
.bx-lines .on circle{fill:var(--verdigris)}
.bx-labs{position:absolute;inset:0;pointer-events:none}
.bx-lab{position:absolute;pointer-events:auto;display:flex;flex-direction:column;max-width:30%;padding:3px 6px;border-radius:9px;
  background:color-mix(in srgb,var(--card) 88%,transparent);border:1px solid transparent;cursor:pointer;font:inherit;color:var(--ink);
  touch-action:manipulation;transition:opacity .2s,transform var(--press,120ms) var(--ease-out,ease-out),border-color .2s,background .2s}
.bx-lab:active{transform:scale(.95)}
.bx-lab.l{align-items:flex-end;text-align:right}
.bx-lab.r{align-items:flex-start;text-align:left}
.bx-lab .a{font-family:var(--ar);font-size:18px;line-height:1.45;direction:rtl}
.bx-lab .e{font-family:var(--la);font-size:12.5px;line-height:1.25;color:var(--ink-soft)}
.bx-lab .e i{font-style:normal;color:var(--verdigris);font-weight:700}
.bx-lab.on{border-color:var(--verdigris);background:color-mix(in srgb,var(--verdigris) 12%,var(--card))}
.bx-lab.on .a{color:var(--verdigris)}
.bx-lab.speaking .a{color:var(--verdigris)}
.bx-labs.hide .bx-lab,.bx-lines.hide{opacity:0;pointer-events:none}
.bx-lines{transition:opacity .2s}
.bx-help{font-size:13.5px;color:var(--ink-soft);text-align:center;margin:10px 0 0;line-height:1.5}
@media (max-width:440px){.bx-lab .a{font-size:16.5px;line-height:1.4}.bx-lab .e{font-size:11.5px}.bx-lab{padding:2px 4px}}
@media (prefers-reduced-motion:reduce){.bx-cam,.bx-fig,.bx-lab,.bx-lines,.bx-svg [data-in],.bx-svg [data-out]{transition:none}}`;
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

  /* ---------- the explorer ---------- */
  function mount(el, opts){
    opts = opts || {};
    el.innerHTML = `<button class="es-back" type="button">‹ All essentials</button>
      <h2 style="margin:0 0 6px">🧍 The body <span style="font-family:var(--ar);font-weight:400;color:var(--ink-soft)">الجِسْم</span></h2>
      <p class="es-note">Tap a part to hear it. Tap a region, like the head or the hand, to zoom in on its parts.</p>
      <div class="bx-bar"><button class="bx-up" type="button" hidden>← Back</button><div class="bx-crumbs" aria-live="polite"></div></div>
      <div class="bx-stage still" role="group" aria-label="A drawing of a person, labelled in Arabic">
        <svg class="bx-svg" viewBox="0 0 ${W} ${H}" aria-hidden="true"><g class="bx-cam">${SVG}</g></svg>
        <svg class="bx-lines" viewBox="0 0 ${W} ${H}" aria-hidden="true"></svg>
        <div class="bx-labs"></div>
      </div>
      <p class="bx-help">These words are waiting for a teacher’s check.</p>`;
    el.querySelector('.es-back').onclick = () => { stop(); if(opts.back) opts.back(); };
    const stage = el.querySelector('.bx-stage'), cam = el.querySelector('.bx-cam'), fig = el.querySelector('.bx-fig'),
      lines = el.querySelector('.bx-lines'), labs = el.querySelector('.bx-labs'), up = el.querySelector('.bx-up'),
      crumbs = el.querySelector('.bx-crumbs');
    const stack = ['body'];
    let sel = null, busy = 0, flipped = false, timer = null;
    const view = () => VIEWS[stack[stack.length - 1]];
    const parts = v => v.l.concat(v.r);

    ready().then(() => { draw(false); scrollTo(0, 0); });

    function crumbsHTML(){
      const s = stack.map((id, i) => i === stack.length - 1 && !sel ? `<b>${esc(cap(short(word(id))))}</b>`
        : `<button type="button" data-i="${i}">${esc(cap(short(word(id))))}</button>`);
      if(sel) s.push(`<b>${esc(short(word(sel)))}</b>`);
      return s.join('<span class="sep" aria-hidden="true">›</span>');
    }
    function chrome(){
      crumbs.innerHTML = crumbsHTML();
      crumbs.querySelectorAll('[data-i]').forEach(b => b.onclick = () => {
        const i = +b.dataset.i;
        if(i === stack.length - 1){ pick(null); return; }
        stack.length = i + 1; sel = null; draw(true);
      });
      up.hidden = stack.length < 2;
    }
    up.onclick = () => { if(stack.length > 1){ stack.pop(); sel = null; draw(true); } };
    const onKey = e => { if(!stage.isConnected) return stop(); if(e.key === 'Escape' && stack.length > 1){ e.preventDefault(); up.click(); } };
    document.addEventListener('keydown', onKey);

    // the camera: the view's box, as big as fits between the label columns, in the middle
    // (each side's column is as wide as its widest label; the box is centred in what's left)
    function camera(v, colL, colR){
      const [x0, y0, x1, y1] = v.box, mid = W - colL - colR - 8;
      const s = Math.min((H - 16) / (y1 - y0), mid / (x1 - x0));
      return { s, cx: (x0 + x1) / 2, cy: (y0 + y1) / 2, ox: colL + 4 + mid / 2 };
    }
    const toStage = (c, p) => [c.ox + (p[0] - c.cx) * c.s, H / 2 + (p[1] - c.cy) * c.s];

    function draw(animate){
      const v = view(), id = stack[stack.length - 1];
      busy++; const mine = busy;
      clearTimeout(timer);
      if(!animate || reduce()) stage.classList.add('still'); else stage.classList.remove('still');
      stage.className = stage.className.replace(/\bv-\S+/g, '').trim() + ' v-' + id;
      chrome();
      // labels first (hidden) so their size sets the columns
      labs.innerHTML = parts(v).map(pid => {
        const w = word(pid), more = VIEWS[pid] && pid !== id;
        return `<button type="button" class="bx-lab ${v.l.includes(pid) ? 'l' : 'r'}" data-id="${pid}" aria-label="${esc(w.en)}: ${esc(w.ar)}${more ? ', zoom in' : ''}">
          <span class="a" lang="ar">${esc(w.ar)}</span><span class="e">${esc(w.en)}${more ? ' <i aria-hidden="true">' + (pid === 'back' ? '↻' : '+') + '</i>' : ''}</span></button>`;
      }).join('');
      labs.classList.add('hide'); lines.classList.add('hide');
      const k = W / stage.clientWidth;                         // stage units per pixel
      const els = [...labs.children], size = new Map(els.map(b => [b.dataset.id, [b.offsetWidth * k, b.offsetHeight * k]]));
      const col = side => Math.max(40, ...els.filter(b => b.classList.contains(side)).map(b => b.offsetWidth * k)) + 4;
      const colL = v.l.length ? col('l') : 40, colR = v.r.length ? col('r') : 40;
      const c = camera(v, colL, colR);
      cam.style.transform = `translate(${c.ox}px,${H/2}px) scale(${c.s}) translate(${-c.cx}px,${-c.cy}px)`;
      // what's drawn only in some views, and which shapes can be tapped here
      const flip = !!v.flip;
      stage.querySelectorAll('[data-in]').forEach(n => n.style.opacity = n.dataset.in.split(' ').includes(id) ? 1 : 0);
      stage.querySelectorAll('[data-out]').forEach(n => n.style.opacity = n.dataset.out.split(' ').includes(id) ? 0 : 1);
      stage.querySelectorAll('.zone').forEach(z => z.classList.remove('live', 'on'));
      parts(v).forEach(pid => { const z = stage.querySelector('#' + word(pid).svgZoneId); if(z) z.classList.add('live'); });
      if(flip !== flipped && animate && !reduce()){              // turn round: squash, swap, open
        fig.style.transform = 'scaleX(0)';
        setTimeout(() => { if(mine !== busy) return; flipped = flip; fig.style.transform = 'scaleX(1)'; }, 220);
      } else flipped = flip;
      // place the labels: each side in the order of what it points at, pushed apart so none overlap
      const place = (ids, left) => {
        const items = ids.map(pid => ({ pid, p: toStage(c, (v.at && v.at[pid]) || AT[pid]), h: size.get(pid)[1] })).sort((a, b) => a.p[1] - b.p[1]);
        // labels that would overlap join into a block, centred on what its labels point at
        const G = 3; let blocks = items.map(it => ({ its:[it], want:it.p[1], h:it.h }));
        const settle = b => { b.top = Math.min(Math.max(b.want - b.h / 2, 4), H - 4 - b.h); };
        blocks.forEach(settle);
        for(let i = 0; i < blocks.length - 1;){
          const a = blocks[i], b = blocks[i + 1];
          if(a.top + a.h + G > b.top){
            const n = a.its.length + b.its.length;
            const m = { its:a.its.concat(b.its), h:a.h + G + b.h, want:(a.want * a.its.length + b.want * b.its.length) / n };
            settle(m); blocks.splice(i, 2, m); i = Math.max(0, i - 1);
          } else i++;
        }
        blocks.forEach(b => { let y = b.top; b.its.forEach(it => { it.top = y; y += it.h + G; }); });
        items.forEach(it => {
          const b = labs.querySelector(`[data-id="${it.pid}"]`);
          b.style.top = (it.top / H * 100) + '%';
          if(left) b.style.right = ((W - colL) / W * 100) + '%'; else b.style.left = ((W - colR) / W * 100) + '%';
          it.x = left ? colL : W - colR; it.y = it.top + it.h / 2;
        });
        return items;
      };
      const placed = place(v.l, true).concat(place(v.r, false));
      lines.innerHTML = placed.map(it => `<g data-id="${it.pid}"><line class="${it.pid === 'back' && !flip ? 'dash' : ''}" x1="${it.x}" y1="${it.y}" x2="${it.p[0]}" y2="${it.p[1]}"/>
        <circle cx="${it.p[0]}" cy="${it.p[1]}" r="1.8"/></g>`).join('');
      els.forEach(b => b.onclick = () => tap(b.dataset.id, b));
      const show = () => { if(mine !== busy) return; labs.classList.remove('hide'); lines.classList.remove('hide'); stage.classList.remove('still');
        if(sel) mark(sel); else if(v.lit) mark(v.lit, true); };
      if(stage.classList.contains('still')) show(); else timer = setTimeout(show, 720);
    }

    stage.querySelector('.bx-zones').addEventListener('click', e => {
      const z = e.target.closest('.zone.live'); if(!z) return;
      const w = WORDS.find(x => x.svgZoneId === z.id && parts(view()).includes(x.id));
      if(w) tap(w.id, labs.querySelector(`[data-id="${w.id}"]`));
    });

    function mark(id, force){
      stage.querySelectorAll('.zone.on').forEach(z => z.classList.remove('on'));
      labs.querySelectorAll('.bx-lab.on').forEach(b => b.classList.remove('on'));
      lines.querySelectorAll('g.on').forEach(g => g.classList.remove('on'));
      if(!id) return;
      const w = word(id), z = stage.querySelector('#' + w.svgZoneId);
      if(z && (force || !VIEWS[id])) z.classList.add('on');      // a region about to open isn't left lit up
      const b = labs.querySelector(`[data-id="${id}"]`); if(b) b.classList.add('on');
      const g = lines.querySelector(`g[data-id="${id}"]`); if(g) g.classList.add('on');
    }
    function pick(id){ sel = id; mark(id); chrome(); }

    function tap(id, b){
      const w = word(id);
      if(window.RQ) RQ.speak(w.say, b || null);
      const cur = stack[stack.length - 1];
      if(VIEWS[id] && id !== cur){
        // light it up, then zoom in (the turn-round for the back is a view too)
        const z = stage.querySelector('#' + w.svgZoneId); if(z){ mark(null); z.classList.add('on'); }
        if(b) b.classList.add('on');
        busy++; const mine = busy;
        setTimeout(() => { if(mine !== busy) return; stack.push(id); sel = null; draw(true); }, reduce() ? 0 : 260);
        return;
      }
      pick(id);
    }

    function stop(){ busy++; clearTimeout(timer); removeEventListener('resize', onResize); document.removeEventListener('keydown', onKey); }
    let rz = null; const onResize = () => { clearTimeout(rz); rz = setTimeout(() => { if(stage.isConnected) draw(false); else stop(); }, 120); };
    addEventListener('resize', onResize);
  }

  window.RafiqBody = { mount, count, ready, VIEWS, AT };
})();
