// W5 · Cómo sobrevivir en las Backrooms (Nivel 0)
window.BED='tape';window.GRADE='rgba(255,230,120,.08)';window.COVER_TEXT=['NIVEL 0','*NO CORRAS*'];
window.DATE=(L)=>L.scene==='origin'?'MAY. 2019':'NIVEL 0';
const YL={wall:[196,176,98],floor:[124,108,60],ceil:[206,200,172],base:[176,158,88]};
function bHall(g,t,ks,o={}){hall(g,Object.assign({t,cam:{x:Math.sin(t*.3)*.15,y:Math.sin(t*1.6)*.015,z:ks*.25},pal:YL,panels:1,flick:1,lampZ:-10,amb:.62},o));
  if(o.flick!==undefined&&o.flick<1){g.fillStyle=`rgba(0,0,0,${.5*(1-o.flick)})`;g.fillRect(0,0,W,H)}
  // zumbido visual: líneas finas que tiemblan
  g.fillStyle='rgba(255,250,200,.04)';for(let i=0;i<6;i++)g.fillRect(0,hash(i+Math.floor(t*20))*H,W,2)}
function maze(g,t,ks){g.fillStyle='#2a2410';g.fillRect(0,0,W,H);const z=1+ks*.35;g.save();g.translate(W/2,H*.55);g.scale(z,z);g.rotate(t*.03);
  for(let x=-14;x<=14;x++)for(let y=-14;y<=14;y++){const h=hash(x*31+y*17);g.fillStyle='#c4b062';if(h>.55)g.fillRect(x*80-40,y*80-40,80,10);if(h<.35)g.fillRect(x*80-40,y*80-40,10,80)}
  g.restore();const v=g.createRadialGradient(W/2,H*.55,100,W/2,H*.55,900);v.addColorStop(0,'rgba(0,0,0,0)');v.addColorStop(1,'rgba(20,16,6,.85)');g.fillStyle=v;g.fillRect(0,0,W,H);
  g.fillStyle='#e0162b';g.beginPath();g.arc(W/2,H*.55,10,0,7);g.fill()}
function entity(g,t,ks){bHall(g,t,ks,{panels:2,flick:flick(t,.6)});const z=lerp(7.6,4.2,clamp(ks/4)),zz=z-ks*.25;if(zz>.3){const P=[W/2+F*(.1)/zz,VPY+F*1.25/zz],h=F*2.6/zz;
  g.save();g.globalAlpha=.92;g.fillStyle='#0a0904';g.fillRect(P[0]-h*.04,P[1]-h,h*.08,h);g.beginPath();g.ellipse(P[0],P[1]-h,h*.06,h*.08,0,0,7);g.fill();g.lineWidth=h*.02;g.strokeStyle='#0a0904';
  g.beginPath();g.moveTo(P[0],P[1]-h*.85);g.lineTo(P[0]-h*.18,P[1]-h*.35);g.moveTo(P[0],P[1]-h*.85);g.lineTo(P[0]+h*.2,P[1]-h*.4);g.stroke();g.restore()}}
function door(g,t,ks){bHall(g,t,ks);const z=3.2,zz=z-ks*.25;const a=[W/2+F*(-.99)/zz,VPY+F*(-.6)/zz],b=[W/2+F*(-.99)/(zz+.6),VPY+F*1.25/(zz+.6)];
  g.fillStyle='#2a2310';g.beginPath();g.moveTo(a[0],a[1]);g.lineTo(b[0],VPY+F*(-.6)/(zz+.6));g.lineTo(b[0],b[1]);g.lineTo(a[0],VPY+F*1.25/zz);g.closePath();g.fill();
  const lg=g.createRadialGradient(a[0],VPY,10,a[0],VPY,320);lg.addColorStop(0,`rgba(255,255,255,${.25+.1*Math.sin(t*3)})`);lg.addColorStop(1,'rgba(255,255,255,0)');g.globalCompositeOperation='lighter';g.fillStyle=lg;g.fillRect(0,0,W,H);g.globalCompositeOperation='source-over'}
function origin(g,t,ks){g.fillStyle='#d9d4c4';g.fillRect(0,0,W,H);g.fillStyle='#f0e0d6';g.fillRect(70,420,940,1120);g.strokeStyle='#b7a89a';g.lineWidth=4;g.strokeRect(70,420,940,1120);
  g.fillStyle='#117743';g.font='700 34px Inter';g.fillText('Anónimo',110,490);g.fillStyle='#555';g.font='30px VT';g.fillText('/x/ · paranormal · 2019',330,490);
  g.save();g.beginPath();g.rect(110,530,520,400);g.clip();g.setTransform(.48,0,0,.208,110,530);hall(g,{t,cam:{x:.2,y:0,z:.4},pal:YL,panels:1,amb:.62});g.restore();
  g.fillStyle='#222';g.font='500 26px Inter';['Si no tienes','cuidado y te sales','de la realidad en','el lugar equivocado,','acabarás en las','Backrooms.'].forEach((l,i)=>g.fillText(l,650,570+i*40));
  g.fillStyle='#1c1c1c';rr(g,220,1180,640,250,30);g.fill();g.fillStyle='#e0162b';g.beginPath();g.arc(300,1260,18,0,7);g.fill();g.fillStyle='#e9e2d2';g.font='64px VT';g.fillText('KANE PIXELS',350,1280);g.font='40px VT';g.fillText('serie en YouTube · 2022',350,1350)}
const SC={hall:(g,t,ks)=>bHall(g,t,ks),maze,entity,flicker:(g,t,ks)=>bHall(g,t,ks,{panels:2,flick:flick(t,1)}),door,origin,hallend:(g,t,ks)=>bHall(g,t,ks,{panels:2})};
