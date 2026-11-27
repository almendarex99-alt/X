const BLM=mk(W/6,H/6),blm=BLM.getContext('2d');
function cine(t){ // brillo suave en las luces, aberración en los bordes y fuga de luz
  blm.drawImage(C,0,0,W/6,H/6);ctx.save();ctx.globalCompositeOperation='screen';ctx.globalAlpha=.22;ctx.imageSmoothingEnabled=true;ctx.drawImage(BLM,0,0,W,H);ctx.restore();
  ctx.save();ctx.globalCompositeOperation='lighter';ctx.globalAlpha=.05;ctx.drawImage(C,-5,0);ctx.drawImage(C,5,0);ctx.restore();
  const lx=W*(.15+.7*(Math.sin(t*.11)+1)/2),lg=ctx.createRadialGradient(lx,H*.18,10,lx,H*.18,W*.9);lg.addColorStop(0,'rgba(255,140,70,.10)');lg.addColorStop(1,'rgba(255,140,70,0)');
  ctx.save();ctx.globalCompositeOperation='lighter';ctx.fillStyle=lg;ctx.fillRect(0,0,W,H);ctx.restore()}
function render(t,cover){
  window.COVERMODE=!!cover;const date=scene(bx,t,!!cover);window.COVERMODE=false;
  ctx.drawImage(BUF,0,0);
  if(t>DUR-.9&&!window.NOLOOP){scene(bx2,0,true);ctx.globalAlpha=clamp((t-(DUR-.9))/.9);ctx.drawImage(BUF2,0,0);ctx.globalAlpha=1}
  if(window.CINE)cine(t);
  glitch(ctx,BUF,glitchAmt(t),t);
  if(cover)COVER(ctx);
  ctx.globalCompositeOperation='overlay';ctx.globalAlpha=.2;ctx.imageSmoothingEnabled=false;ctx.drawImage(GRAIN[Math.floor(t*30)%6],0,0,W,H);ctx.imageSmoothingEnabled=true;
  ctx.globalCompositeOperation='source-over';ctx.globalAlpha=1;ctx.drawImage(SCAN,0,0);ctx.drawImage(VIG,0,0);
  if(!cover)osd(ctx,t,t>DUR-.9?scene0date:date);
}
let scene0date='';
window.render=render;window.CUES=CUES;
window.ready=Promise.all(['100px Anton','64px VT','700 40px Inter','500 40px Inter'].map(f=>document.fonts.load(f))).then(()=>document.fonts.ready).then(()=>{scene0date=scene(bx2,0,true);window.DUR=DUR;window.COVER_T=COVER_T});
