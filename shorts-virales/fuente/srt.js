// Motor común de los 10 shorts: la línea de tiempo sale de la voz (TL), cada video aporta sus escenarios (SC)
const DUR=TL.dur,LINES=TL.lines;
function lineAt(t){let r=LINES[0];for(const l of LINES){if(t>=l.t)r=l;else break}return r}
function firstScene(s){return LINES.find(l=>l.scene===s)}
function setupCues(){
  COVER_T=window.COVER_AT??((LINES.find(l=>l.fx==='stinger')||LINES[1]).t+.35);
  cue(0,'bed',{kind:window.BED||'drone',end:DUR});
  LINES.forEach((l,i)=>{const prev=LINES[i-1];
    if(!prev||prev.scene!==l.scene){if(i)cue(l.t-.15,'glitch');cue(l.t,i?'hit2':'hit')}
    if(l.fx==='hit')cue(l.t+.05,'hit');
    if(l.fx==='stinger'){cue(l.t-1.2,'riser',{end:l.t-.15});cue(l.t-.15,'silence',{end:l.t});cue(l.t,'stinger')}});
  (window.EXTRA_CUES||[]).forEach(c=>cue(c[0],c[1],c[2]||{}));
}
let COVER_T=0;
function COVER(g){const [a,b]=window.COVER_TEXT;g.fillStyle='rgba(0,0,0,.3)';g.fillRect(0,0,W,H);big(g,a,560,a.length>8?190:240,1);big(g,b,800,b.length>9?190:240,1)}
window.extraGlitch=t=>{const L=lineAt(t),k=t-L.t;let a=0;if(L.fx==='stinger'&&k<.45)a=.55;if(window.GLITCH)a=Math.max(a,window.GLITCH(t,L,k));return a};
function scene(g,t,forLoop){
  const L=lineAt(t),k=t-L.t;let i0=L.i;while(i0>0&&LINES[i0-1].scene===L.scene)i0--;const ks=t-LINES[i0].t,span=LINES[L.i].end-LINES[i0].t;
  const fn=SC[L.scene]||SC[L.scene.replace(/end$/,'')];
  g.save();kb(g,ks,span,()=>fn(g,t,ks,L,k,span),window.NOZOOM&&window.NOZOOM.includes(L.scene)?0:.07);g.restore();
  if(window.GRADE){g.save();g.globalCompositeOperation='soft-light';g.fillStyle=window.GRADE;g.fillRect(0,0,W,H);g.restore()}
  // franjas de cine arriba y abajo con degradado
  const tg=g.createLinearGradient(0,0,0,360);tg.addColorStop(0,'rgba(0,0,0,.75)');tg.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=tg;g.fillRect(0,0,W,360);
  const bg=g.createLinearGradient(0,H-520,0,H);bg.addColorStop(0,'rgba(0,0,0,0)');bg.addColorStop(1,'rgba(0,0,0,.8)');g.fillStyle=bg;g.fillRect(0,H-520,W,520);
  if(!forLoop){if(L.cap1)big(g,L.cap1,560,L.cap1.length>16?96:120,k-.08);if(L.cap2)big(g,L.cap2,705,L.cap2.length>16?92:124,k-.35)}
  if(window.SMALLS&&window.SMALLS[L.i])small(g,window.SMALLS[L.i],1210,k-.9,{size:38});
  return window.DATE?window.DATE(L,t):'';
}
