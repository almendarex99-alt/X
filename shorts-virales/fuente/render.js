function render(t,cover){
  window.COVERMODE=!!cover;const date=scene(bx,t,!!cover);window.COVERMODE=false;
  ctx.drawImage(BUF,0,0);
  if(t>DUR-.9&&!window.NOLOOP){scene(bx2,0,true);ctx.globalAlpha=clamp((t-(DUR-.9))/.9);ctx.drawImage(BUF2,0,0);ctx.globalAlpha=1}
  glitch(ctx,BUF,glitchAmt(t),t);
  if(cover)COVER(ctx);
  ctx.globalCompositeOperation='overlay';ctx.globalAlpha=.2;ctx.imageSmoothingEnabled=false;ctx.drawImage(GRAIN[Math.floor(t*30)%6],0,0,W,H);ctx.imageSmoothingEnabled=true;
  ctx.globalCompositeOperation='source-over';ctx.globalAlpha=1;ctx.drawImage(SCAN,0,0);ctx.drawImage(VIG,0,0);
  if(!cover)osd(ctx,t,t>DUR-.9?scene0date:date);
}
let scene0date='';
window.render=render;window.CUES=CUES;
window.ready=Promise.all(['100px Anton','64px VT','700 40px Inter','500 40px Inter'].map(f=>document.fonts.load(f))).then(()=>document.fonts.ready).then(()=>{scene0date=scene(bx2,0,true);window.DUR=DUR;window.COVER_T=COVER_T});
