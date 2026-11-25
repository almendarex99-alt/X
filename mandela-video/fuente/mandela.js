// The Mandela Catalogue: la historia explicada — video horizontal 1920x1080
const DUR=TL.dur,LINES=TL.lines;
const COVER_T=LINES.find(l=>l.scene==='camface').t+1.2;
function COVER(g){g.fillStyle='rgba(0,0,0,.25)';g.fillRect(0,0,W,H);
  g.save();g.font='250px Anton';g.textAlign='left';g.lineJoin='round';g.strokeStyle='#000';g.lineWidth=34;g.strokeText('NO',90,430);g.strokeText('ABRAS',90,700);
  g.fillStyle='#f2ece0';g.fillText('NO',90,430);g.fillStyle='#e0162b';g.fillText('ABRAS',90,700);g.restore()}
// ---------- señales de sonido desde la línea de tiempo ----------
cue(0,'bed',{kind:'tape',end:DUR});
const firstOf=s=>LINES.find(l=>l.scene===s);
LINES.forEach((l,i)=>{const prev=LINES[i-1];const ns=!prev||prev.scene!==l.scene;
  if(l.scene.startsWith('chapter')){cue(l.t-.15,'glitch');cue(l.t,'hit')}
  else if(ns){cue(l.t-.15,'glitch');cue(l.t,'hit2')}});
cue(firstOf('broadcast').t,'eas',{end:firstOf('broadcast').t+2.2});
cue(firstOf('phone').t-.1,'ring',{end:firstOf('phone').t+2.4});
const sc=firstOf('scream');cue(sc.t-1.6,'riser',{end:sc.t-.2});cue(sc.t-.2,'silence',{end:sc.t});cue(sc.t,'stinger');
const cf=firstOf('camface');cue(cf.t-1.4,'riser',{end:cf.t-.15});cue(cf.t-.15,'silence',{end:cf.t});cue(cf.t,'stinger');
const rm=firstOf('room');cue(rm.t+1,'heart',{end:firstOf('camface').t-1.5,bpm0:60,bpm1:130});cue(rm.t+5,'knock');cue(rm.t+11,'knock');
cue(firstOf('skin').t,'stinger');cue(firstOf('apple').t,'fogpad',{end:LINES.filter(l=>l.scene==='apple').slice(-1)[0].end});
cue(firstOf('bad').t,'glitch');cue(firstOf('distort').t,'glitch');
LINES.filter(l=>l.scene==='alert').forEach(l=>cue(l.t,'eas',{end:l.t+1.6}));
window.extraGlitch=t=>{const L=lineAt(t);if(!L)return 0;const k=t-L.t;
  if(L.scene==='distort')return .25+.35*(hash(Math.floor(t*5))>.6);if(L.scene==='bad')return .3;if(L.scene==='camface'&&k<.5)return .6;if(L.scene==='scream'&&k<.4)return .5;return 0};
function lineAt(t){let r=null;for(const l of LINES){if(t>=l.t-0.0)r=l;else break}return r}

// ---------- utilidades ----------
function kb(g,k,d,fn,z=.06,cx=W/2,cy=H/2){g.save();const s=1+z*clamp(k/Math.max(d,1));g.translate(cx,cy);g.scale(s,s);g.translate(-cx,-cy);fn();g.restore()}
function lower(g,txt,age){if(!txt||age<0)return;const a=clamp(age/.3);g.save();g.globalAlpha=a;g.font='44px VT';const w=g.measureText(txt).width;
  g.fillStyle='rgba(0,0,0,.75)';g.fillRect(80,H-190,w+70,74);g.fillStyle='#e0162b';g.fillRect(80,H-190,10,74);g.fillStyle='#f2ece0';g.fillText(txt,112,H-140);g.restore()}
function quote(g,txt,age,y=H*.78){if(age<0)return;big(g,txt,y,96,age,{maxW:1500})}
function person(g,x,fy,h,o={}){const s=h/100;g.save();g.translate(x,fy);g.scale(s,s);const c=o.c||'#050505';g.fillStyle=c;g.strokeStyle=c;g.lineCap='round';
  if(o.dress){g.beginPath();g.moveTo(-10,-70);g.lineTo(10,-70);g.lineTo(17,-18);g.lineTo(-17,-18);g.closePath();g.fill();g.lineWidth=5;g.beginPath();g.moveTo(-6,-20);g.lineTo(-7,0);g.moveTo(6,-20);g.lineTo(7,0);g.stroke()}
  else{g.lineWidth=7;g.beginPath();g.moveTo(-5,-46);g.lineTo(-7,0);g.moveTo(5,-46);g.lineTo(7,0);g.stroke();g.beginPath();g.moveTo(-13,-80);g.lineTo(13,-80);g.lineTo(11,-44);g.lineTo(-11,-44);g.closePath();g.fill()}
  g.lineWidth=5;g.beginPath();g.moveTo(-12,-76);g.lineTo(o.armUp?-24:-15,o.armUp?-96:-46);g.moveTo(12,-76);g.lineTo(15,-46);g.stroke();
  g.beginPath();g.ellipse(0,-90,8.5,10,0,0,7);g.fill();
  if(o.hair){g.beginPath();g.moveTo(-9,-96);g.quadraticCurveTo(0,-106,9,-96);g.lineTo(11,-66);g.lineTo(-11,-66);g.closePath();g.fill()}
  if(o.suit){g.fillStyle='#d8d2c4';g.beginPath();g.moveTo(-5,-80);g.lineTo(5,-80);g.lineTo(0,-64);g.closePath();g.fill();g.fillStyle='#000';g.fillRect(-4,-79,8,3)}
  if(o.eyes){g.fillStyle=o.eyes;g.shadowColor=o.eyes;g.shadowBlur=6;g.fillRect(-4.5,-92,3,1.6);g.fillRect(1.5,-92,3,1.6)}
  g.restore()}
// cara con distorsión 0..1
function face(g,cx,cy,r,t,d=0,o={}){g.save();g.translate(cx+(d>.3?(hash(Math.floor(t*20))-.5)*r*.06*d:0),cy);g.scale(1,1+d*.35);
  const sk=g.createRadialGradient(-r*.2,-r*.3,r*.1,0,0,r*1.2);sk.addColorStop(0,o.skin||'#e3dccf');sk.addColorStop(1,'#8f877b');g.fillStyle=sk;g.beginPath();g.ellipse(0,0,r*.78,r,0,0,7);g.fill();
  g.save();g.beginPath();g.ellipse(0,0,r*.8,r*1.02,0,0,7);g.clip();g.fillStyle='#17130f';g.beginPath();g.ellipse(0,-r*.62,r*.95,r*.6,0,0,7);g.fill();
  g.beginPath();g.moveTo(-r*.8,-r*.35);g.quadraticCurveTo(-r*.3,-r*.2,r*.1,-r*.45);g.quadraticCurveTo(r*.5,-r*.3,r*.8,-r*.4);g.lineTo(r*.8,-r);g.lineTo(-r*.8,-r);g.closePath();g.fill();
  const cs=g.createRadialGradient(0,r*.2,r*.3,0,0,r*1.05);cs.addColorStop(0,'rgba(0,0,0,0)');cs.addColorStop(1,'rgba(20,14,10,.55)');g.fillStyle=cs;g.fillRect(-r,-r*1.1,r*2,r*2.2);g.restore();
  [-1,1].forEach(sd=>{const so=g.createRadialGradient(sd*r*.3,-r*.1,2,sd*r*.3,-r*.1,r*.26);so.addColorStop(0,'rgba(40,28,22,.55)');so.addColorStop(1,'rgba(40,28,22,0)');g.fillStyle=so;g.fillRect(sd*r*.3-r*.3,-r*.4,r*.6,r*.6)});
  const ey=-r*.12+d*r*.18,ew=r*.15*(1+d*.9),eh=r*.08*(1+d*1.8);
  [-1,1].forEach(sd=>{g.fillStyle=d>.5?'#f4f0e6':'#efe9dd';g.beginPath();g.ellipse(sd*r*.3,ey+sd*d*r*.06,ew,eh,0,0,7);g.fill();g.fillStyle='#000';g.beginPath();g.arc(sd*r*.3,ey+sd*d*r*.06,Math.max(r*.02,r*.06*(1-d*.8)),0,7);g.fill()});
  g.fillStyle='rgba(60,45,40,.35)';g.beginPath();g.moveTo(0,-r*.02);g.lineTo(-r*.07,r*.25);g.lineTo(r*.05,r*.27);g.closePath();g.fill();
  const mw=r*(.28+d*.5),my=r*.5+d*r*.1;g.fillStyle=d>.2?'#100606':'rgba(90,40,40,.8)';g.beginPath();g.moveTo(-mw,my);g.quadraticCurveTo(0,my+r*(.08+d*.45),mw,my);g.quadraticCurveTo(0,my+r*.03,-mw,my);g.fill();
  if(d>.35){g.strokeStyle='rgba(230,225,210,.8)';g.lineWidth=r*.012;for(let i=-6;i<=6;i++){const x=i/6*mw*.9;g.beginPath();g.moveTo(x,my+r*.02);g.lineTo(x,my+r*(.05+d*.25)*(1-Math.abs(i)/7));g.stroke()}}
  g.restore()}
function crtIn(g,x,y,w,h,draw){g.save();g.fillStyle='#16130f';rr(g,x-36,y-36,w+72,h+110,30);g.fill();g.fillStyle='#050505';rr(g,x,y,w,h,22);g.fill();
  g.save();rr(g,x,y,w,h,22);g.clip();g.translate(x,y);draw(g,w,h);g.restore();
  g.save();rr(g,x,y,w,h,22);g.clip();g.fillStyle='rgba(0,0,0,.25)';for(let yy=y;yy<y+h;yy+=4)g.fillRect(x,yy,w,2);const v=g.createRadialGradient(x+w/2,y+h/2,w*.2,x+w/2,y+h/2,w*.7);v.addColorStop(0,'rgba(0,0,0,0)');v.addColorStop(1,'rgba(0,0,0,.6)');g.fillStyle=v;g.fillRect(x,y,w,h);g.restore();
  g.fillStyle='#e0162b';g.beginPath();g.arc(x+30,y+h+40,7,0,7);g.fill();g.restore()}
function broadcastScreen(g,w,h,t,k,head,lines,ticker){const b=g.createLinearGradient(0,0,0,h);b.addColorStop(0,'#0a1433');b.addColorStop(1,'#03060f');g.fillStyle=b;g.fillRect(0,0,w,h);
  const s=w/1920;g.fillStyle='#b5121f';g.fillRect(0,0,w,110*s);g.font=`${58*s}px VT`;g.fillStyle='#fff';g.textAlign='center';g.fillText(head,w/2,74*s);
  g.font=`${112*s}px VT`;lines.forEach((l,i)=>{const n=Math.floor((k-i*.5)*22);if(n>0){g.fillStyle=i===lines.length-1?'#ff4a55':'#e9e2d2';g.fillText(l.slice(0,n),w/2,h*.38+i*130*s)}});
  if(ticker){g.fillStyle='#000';g.fillRect(0,h-90*s,w,90*s);g.font=`${48*s}px VT`;g.fillStyle='#f2d24a';g.textAlign='left';const tx=ticker+'   ·   '+ticker;const tw=g.measureText(tx).width/2;g.fillText(tx,-((t*140*s)%tw),h-30*s)}
  g.textAlign='left'}
// ---------- escenas ----------
function sBroadcast(g,t,k){broadcastScreen(g,W,H,t,k,'AVISO DE EMERGENCIA · CONDADO DE MANDELA',['SI ALGUIEN CON TU CARA','LLAMA A TU PUERTA','NO ABRAS.'],'PERMANEZCA EN CASA · NO RESPONDA A VOCES CONOCIDAS · MANTENGA LAS LUCES ENCENDIDAS')}
function sTitle(g,t,k){g.fillStyle='#030303';g.fillRect(0,0,W,H);noise(g,.12,t);
  big(g,'THE MANDELA CATALOGUE',H*.48,150,k-.1,{split:hash(Math.floor(t*9))>.85?12:0});
  g.save();g.font='64px VT';g.textAlign='center';g.fillStyle='#e0162b';g.globalAlpha=clamp((k-.8)*2);g.fillText('LA HISTORIA EXPLICADA',W/2,H*.6);g.font='38px VT';g.fillStyle='#9a958c';g.fillText('SERIE DE ALEX KISTER · 2021',W/2,H*.67);g.restore()}
function sCreator(g,t,k){g.fillStyle='#080605';g.fillRect(0,0,W,H);
  const lg=g.createRadialGradient(1300,300,30,1300,300,900);lg.addColorStop(0,'rgba(255,200,120,.22)');lg.addColorStop(1,'rgba(255,200,120,0)');g.fillStyle=lg;g.fillRect(0,0,W,H);
  g.fillStyle='#2a1c12';g.fillRect(0,760,W,320);g.fillStyle='#1d140d';g.fillRect(0,760,W,14);
  crtIn(g,180,320,560,400,(c,w,h)=>{c.drawImage(GRAIN[Math.floor(t*30)%6],0,0,w,h);c.fillStyle='rgba(0,0,0,.4)';c.fillRect(0,0,w,h);c.font='48px VT';c.fillStyle='#e9e2d2';c.textAlign='center';c.fillText('VOL. 1',w/2,h/2+16)});
  // cámara de vídeo
  g.fillStyle='#121212';rr(g,860,560,360,200,24);g.fill();g.fillStyle='#050505';g.beginPath();g.arc(1240,660,90,0,7);g.fill();g.strokeStyle='#333';g.lineWidth=10;g.stroke();
  g.fillStyle='#1c2b3a';g.beginPath();g.arc(1240,660,50,0,7);g.fill();g.fillStyle=`rgba(255,30,30,${.5+.5*Math.sin(t*4)})`;g.beginPath();g.arc(900,590,9,0,7);g.fill();
  // cintas
  ['VOL. 1','VOL. 2','VOL. 3','VOL. 4'].forEach((n,i)=>{g.save();g.translate(1480,740-i*70);g.rotate((i%2?-1:1)*.02);g.fillStyle='#111';g.fillRect(0,0,360,62);g.fillStyle='#e8e1cf';g.fillRect(40,12,280,38);g.fillStyle='#1a1a1a';g.font='700 26px Inter';g.fillText('MANDELA · '+n,56,40);g.restore()})}
function sMap(g,t,k){g.fillStyle='#050807';g.fillRect(0,0,W,H);g.strokeStyle='rgba(80,140,110,.18)';g.lineWidth=2;
  for(let i=0;i<22;i++){g.beginPath();for(let x=0;x<=W;x+=40){const y=i*55+Math.sin(x*.004+i)*30+Math.sin(x*.011+i*2)*12;x?g.lineTo(x,y):g.moveTo(x,y)}g.stroke()}
  g.strokeStyle='rgba(200,200,190,.25)';g.lineWidth=3;[[0,300,W,520],[400,0,700,H],[1300,0,1100,H]].forEach(a=>{g.beginPath();g.moveTo(a[0],a[1]);g.lineTo(a[2],a[3]);g.stroke()});
  const pts=[[720,260],[1180,230],[1260,520],[1120,820],[760,790],[640,520]];g.beginPath();pts.forEach((p,i)=>i?g.lineTo(...p):g.moveTo(...p));g.closePath();
  g.fillStyle=`rgba(224,22,43,${.08+.05*Math.sin(t*2)})`;g.fill();g.strokeStyle='#e0162b';g.lineWidth=5;g.setLineDash([18,10]);g.stroke();g.setLineDash([]);
  g.font='86px Anton';g.textAlign='center';g.fillStyle='#e9e2d2';g.fillText('MANDELA',950,560);g.textAlign='left';
  for(let i=0;i<9;i++){const x=760+hash(i*3.1)*420,y=320+hash(i*7.7)*420,on=hash(i+Math.floor(t*1.5))>.5;g.fillStyle=on?'#f2d24a':'rgba(242,210,74,.25)';g.fillRect(x,y,10,10)}}
function sTV(g,t,k,L){g.fillStyle='#060607';g.fillRect(0,0,W,H);
  g.fillStyle='#0d1420';g.fillRect(120,180,300,480);g.strokeStyle='#1a1a1a';g.lineWidth=16;g.strokeRect(120,180,300,480);g.beginPath();g.moveTo(270,180);g.lineTo(270,660);g.stroke();
  g.fillStyle='#120d09';g.fillRect(560,820,800,260);
  crtIn(g,620,240,680,500,(c,w,h)=>{broadcastScreen(c,w,h,t,k+3,'INSTRUCCIONES PARA RESIDENTES',['1. NO ABRA LA PUERTA','2. NO MIRE POR LA VENTANA','3. NO SE PREGUNTE QUIÉN ES'],null)});
  const rg=g.createRadialGradient(960,490,100,960,490,1000);rg.addColorStop(0,`rgba(150,170,210,${.14*flick(t,.5)})`);rg.addColorStop(1,'rgba(150,170,210,0)');g.globalCompositeOperation='lighter';g.fillStyle=rg;g.fillRect(0,0,W,H);g.globalCompositeOperation='source-over';
  if(L.i>40){person(g,300,640,330,{eyes:'rgba(240,235,220,.9)'})}}
function sFaces(g,t,k,L,variant){g.fillStyle='#0a0908';g.fillRect(0,0,W,H);
  if(!variant){const n=5;for(let i=0;i<n;i++){const x=W/2+(i-2)*340,y=H*.47;g.fillStyle='#d9d2c3';g.fillRect(x-140,y-190,280,380);g.fillStyle='#2a2622';g.fillRect(x-124,y-174,248,300);
      const odd=i===3,d=odd?clamp((k-1.2)/3)*.55:0;face(g,x,y-30,110,t,d);g.fillStyle='#1a1a1a';g.font='22px VT';g.textAlign='center';g.fillText(odd?'¿VECINO?':'VECINO',x,y+160);g.textAlign='left'}}
  else{face(g,W/2,H*.5,330,t,clamp(k/5)*.9);
    const W2=['te conozco','abre la puerta','es culpa tuya','nadie te cree','soy yo'];W2.forEach((w,i)=>{const a=clamp((k-.6-i*.7)*1.2)*clamp(2-(k-.6-i*.7)*.4);if(a<=0)return;g.save();g.globalAlpha=a*.85;
      g.font='italic 700 46px Inter';g.fillStyle='#e9e2d2';const x=[260,1500,330,1460,900][i],y=[260,300,820,800,140][i]-(k-i*.7)*12;g.fillText('«'+w+'»',x,y);g.restore()})}}
function car(g,w,h,t,alt){const b=g.createLinearGradient(0,0,0,h);b.addColorStop(0,'#08101c');b.addColorStop(1,'#020407');g.fillStyle=b;g.fillRect(0,0,w,h);
  g.strokeStyle='rgba(160,190,220,.25)';g.lineWidth=2;for(let i=0;i<50;i++){const x=(hash(i*3.3)*w+t*30)%w,y=(hash(i*7.1)*h*.6+t*220*(.5+hash(i)))%(h*.6);g.beginPath();g.moveTo(x,y);g.lineTo(x-4,y+22);g.stroke()}
  g.fillStyle='#030303';g.fillRect(0,h*.62,w,h);g.strokeStyle='#111';g.lineWidth=26;g.beginPath();g.arc(w*.62,h*.95,170,Math.PI*1.1,Math.PI*1.9);g.stroke();
  g.fillStyle='rgba(80,160,255,.25)';g.fillRect(w*.3,h*.64,w*.5,14);
  person(g,w*.4,h*1.25,h*1.05,{suit:true,eyes:alt?'rgba(255,255,255,.95)':null});
  g.fillStyle='#111';g.fillRect(w*.4-60*(h/700),h*.37,26,64)}
function bedroomPanel(g,w,h,t){const b=g.createRadialGradient(w*.7,h*.3,20,w*.7,h*.3,w);b.addColorStop(0,'#3a2a18');b.addColorStop(1,'#0b0806');g.fillStyle=b;g.fillRect(0,0,w,h);
  g.fillStyle='#120d09';g.fillRect(0,h*.68,w,h);g.fillStyle='#24180f';g.fillRect(w*.08,h*.6,w*.5,30);
  g.fillStyle='#0d0d0d';rr(g,w*.12,h*.48,150,86,12);g.fill();g.fillStyle=`rgba(255,30,30,${.5+.5*Math.sin(t*4)})`;g.beginPath();g.arc(w*.12+20,h*.48+18,6,0,7);g.fill();
  person(g,w*.7,h*1.2,h*1.0,{});g.fillStyle='#111';g.fillRect(w*.7+30*(h/700)-20,h*.35,24,62)}
function sPhone(g,t,k,L,alt){const hw=W/2-6;
  g.save();g.beginPath();g.rect(0,0,hw,H);g.clip();car(g,hw,H,t,alt);g.restore();
  g.save();g.translate(W/2+6,0);g.beginPath();g.rect(0,0,hw,H);g.clip();bedroomPanel(g,hw,H,t);g.restore();
  g.fillStyle='#000';g.fillRect(W/2-6,0,12,H);
  g.strokeStyle=alt?'#e0162b':'#7dffef';g.lineWidth=4;g.beginPath();for(let x=-240;x<=240;x+=6){const y=Math.sin(x*.08+t*14)*Math.sin(t*3+x*.01)*40*(hash(Math.floor(t*8))>.3?1:.2);x>-240?g.lineTo(W/2+x,H*.5+y):g.moveTo(W/2+x,H*.5+y)}g.stroke();
  g.font='46px VT';g.fillStyle=alt?'#ff4a55':'#e9e2d2';g.fillText(alt?'¿CESAR TORRES?':'CESAR TORRES',60,H-70);g.textAlign='right';g.fillStyle='#e9e2d2';g.fillText('MARK HEATHCLIFF',W-60,H-70);g.textAlign='left';
  if(alt){g.fillStyle='rgba(224,22,43,.12)';g.fillRect(0,0,hw,H)}}
function sHouse(g,t,k){const b=g.createLinearGradient(0,0,0,H);b.addColorStop(0,'#04060c');b.addColorStop(1,'#11151a');g.fillStyle=b;g.fillRect(0,0,W,H);
  g.fillStyle='#d8e2e4';g.beginPath();g.arc(1600,180,48,0,7);g.fill();g.fillStyle='#050608';g.fillRect(0,860,W,220);
  const mg=g.createRadialGradient(1600,180,40,1600,180,1300);mg.addColorStop(0,'rgba(180,200,215,.22)');mg.addColorStop(1,'rgba(180,200,215,0)');g.fillStyle=mg;g.fillRect(0,0,W,H);
  g.fillStyle='#1a1d24';g.beginPath();g.moveTo(560,860);g.lineTo(560,480);g.lineTo(960,250);g.lineTo(1360,480);g.lineTo(1360,860);g.closePath();g.fill();g.strokeStyle='rgba(190,205,215,.35)';g.lineWidth=4;g.stroke();
  const win=(x,y,on)=>{g.fillStyle=on?`rgba(255,200,120,${.75*flick(t,.6)})`:'#07080a';g.fillRect(x,y,110,130);g.strokeStyle='#050505';g.lineWidth=6;g.strokeRect(x,y,110,130);g.beginPath();g.moveTo(x+55,y);g.lineTo(x+55,y+130);g.stroke()};
  win(640,540,false);win(1170,540,k>2);win(640,700,false);win(1170,700,false);
  g.fillStyle='#050505';g.fillRect(900,680,120,180);g.fillStyle=`rgba(255,220,150,${.5*flick(t,.8)})`;g.beginPath();g.arc(1050,670,12,0,7);g.fill();
  g.fillStyle='#020303';g.beginPath();g.moveTo(170,860);g.lineTo(250,300);g.lineTo(330,860);g.fill();g.beginPath();g.ellipse(250,420,170,230,0,0,7);g.fill();
  person(g,lerp(1700,1000,clamp(k/4)),860,170,{})}
const CAMB=[0,1,2,3].map(()=>mk(480,270));
function camFeed(i,t,o={}){const c=CAMB[i],x=c.getContext('2d');x.setTransform(.25,0,0,.25,0,0);
  const P=[{cam:{x:0,y:0,z:.2},lampZ:4},{cam:{x:.3,y:-.1,z:1.5},lampZ:3.2,red:.1},{cam:{x:0,y:0,z:1.1},lampZ:5.5,dark:.15},{cam:{x:-.3,y:-.2,z:.6},lampZ:4.4}][i];
  hall(x,Object.assign({t,flick:flick(t+i,.6)},P,o));x.setTransform(1,0,0,1,0,0);
  x.fillStyle='rgba(120,140,130,.18)';x.globalCompositeOperation='color';x.fillRect(0,0,480,270);x.globalCompositeOperation='source-over';return c}
function camLabels(g,x,y,w,h,i,t){const n=['CAM 1 · ENTRADA','CAM 2 · COCINA','CAM 3 · PASILLO DE ATRÁS','CAM 4 · SALÓN'][i];const s=w/960,ty=y+(w>1000?H-70:50*s);
  g.font=`${40*s}px VT`;g.fillStyle='#e9e2d2';g.fillText(n,x+24*s,ty);g.textAlign='right';g.fillText('08:14:'+String(Math.floor(t)%60).padStart(2,'0'),x+w-24*s,ty);g.textAlign='left';
  g.fillStyle=Math.floor(t*2)%2?'#e0162b':'transparent';g.beginPath();g.arc(x+w-40*s,y+h-40*s,10*s,0,7);g.fill()}
function sCams(g,t,k,L){g.fillStyle='#000';g.fillRect(0,0,W,H);for(let i=0;i<4;i++){const x=(i%2)*960,y=Math.floor(i/2)*540;g.drawImage(camFeed(i,t),x+4,y+4,952,532);camLabels(g,x+4,y+4,952,532,i,t)}
  g.strokeStyle='#e0162b';g.lineWidth=6;if(Math.floor(t*2)%2)g.strokeRect(4,544,952,532)}
function sCamHall(g,t,k,L,scream){const c=camFeed(2,t,{lisa:null});g.drawImage(c,0,0,W,H);
  // figuras: la madre delante y "Cesar" al fondo
  const sh=scream?(hash(Math.floor(t*30))-.5)*14:0;person(g,760+sh,1020,620,{dress:true,hair:true,armUp:scream});person(g,1130,760,230,{suit:true,eyes:scream&&k>.3?'rgba(255,255,255,.95)':null});
  camLabels(g,0,0,W,H,2,t)}
function sDistort(g,t,k,L){g.fillStyle='#050403';g.fillRect(0,0,W,H);const first=L.i===firstOf('distort').i;const d=first?clamp(k/2.2):.85+.15*Math.sin(t*3);
  face(g,W/2,H*.52,360,t,d);if(first&&k<2.4){g.fillStyle=`rgba(224,22,43,${.12*Math.max(0,Math.sin(t*6))})`;g.fillRect(0,0,W,H)}
  g.save();g.font='40px VT';g.fillStyle='#e9e2d2';g.fillText('CAM 3 · 08:14:'+String(Math.floor(t)%60).padStart(2,'0')+' · ZOOM x8',60,H-60);g.restore()}
function sStreet(g,t,k){const b=g.createLinearGradient(0,0,0,H);b.addColorStop(0,'#03050a');b.addColorStop(1,'#0c0f12');g.fillStyle=b;g.fillRect(0,0,W,H);
  g.fillStyle='#0a0b0c';g.beginPath();g.moveTo(0,H);g.lineTo(880,520);g.lineTo(1040,520);g.lineTo(W,H);g.fill();
  g.strokeStyle='rgba(220,200,120,.4)';g.lineWidth=6;g.setLineDash([60,60]);g.lineDashOffset=-t*40;g.beginPath();g.moveTo(960,H);g.lineTo(960,520);g.stroke();g.setLineDash([]);
  for(let i=0;i<5;i++){const z=i/5,x=lerp(260,850,z),y=lerp(H,540,z),hh=lerp(560,60,z);g.strokeStyle='#050505';g.lineWidth=lerp(14,3,z);g.beginPath();g.moveTo(x,y);g.lineTo(x,y-hh);g.stroke();
    const lg=g.createRadialGradient(x,y-hh,4,x,y-hh*.2,hh*.9);lg.addColorStop(0,`rgba(255,210,140,${.4*flick(t+i,.4)})`);lg.addColorStop(1,'rgba(255,210,140,0)');g.globalCompositeOperation='lighter';g.fillStyle=lg;g.fillRect(x-hh,y-hh,hh*2,hh*1.4);g.globalCompositeOperation='source-over'}
  person(g,980,700,120,{});const fz=clamp(k/6);person(g,lerp(1500,1240,fz),H+lerp(140,60,fz),lerp(900,1100,fz),{eyes:fz>.6?'rgba(255,255,255,.8)':null})}
function sRoom(g,t,k,L){const day=1+Math.floor(clamp((t-firstOf('room').t)/2.2,0,9));g.fillStyle='#0b0907';g.fillRect(0,0,W,H);
  kb(g,k,L.end-L.t,()=>{g.fillStyle='#16110c';g.fillRect(0,0,W,H);g.fillStyle='#0e0a07';g.fillRect(0,800,W,280);
    g.fillStyle='#1d1610';g.fillRect(120,640,700,220);g.fillStyle='#2a2119';g.fillRect(120,600,700,60);g.fillStyle='#3a3026';rr(g,150,560,200,80,30);g.fill();
    g.fillStyle='#090706';g.fillRect(1240,220,380,620);g.strokeStyle='#1d1610';g.lineWidth=14;g.strokeRect(1240,220,380,620);g.fillStyle='#c9a66a';g.beginPath();g.arc(1580,560,12,0,7);g.fill();
    const lg=g.createLinearGradient(0,830,0,846);g.fillStyle=`rgba(255,210,140,${.7*flick(t,.5)})`;g.fillRect(1250,834,360,8);
    const ft=Math.sin(t*.7);if(ft>.2){g.fillStyle='#000';g.fillRect(1330+ft*60,834,60,8);g.fillRect(1440+ft*60,834,60,8)}});
  g.save();g.font='54px VT';g.fillStyle='#e0162b';g.fillText('● REC',60,170);g.fillStyle='#e9e2d2';g.textAlign='right';g.fillText('DÍA '+day,W-60,H-70);g.restore();
  g.strokeStyle='rgba(233,226,210,.7)';g.lineWidth=4;[[40,40],[W-40,40],[40,H-40],[W-40,H-40]].forEach(([x,y])=>{g.beginPath();g.moveTo(x,y+(y<H/2?60:-60));g.lineTo(x,y);g.lineTo(x+(x<W/2?60:-60),y);g.stroke()})}
function sBad(g,t,k){g.fillStyle='#000';g.fillRect(0,0,W,H);noise(g,.08,t);g.save();g.font='170px VT';g.textAlign='center';g.fillStyle='#e0162b';g.shadowColor='#e0162b';g.shadowBlur=30;
  const s='BAD DECISION, MARK!';g.fillText(s.slice(0,Math.floor(k*14)),W/2,H*.5);g.restore();small(g,'«Mala decisión, Mark.»',H*.72,k-1.4,{size:44,weight:700})}
function sCamFace(g,t,k){const s=1+.04*Math.sin(t*1.6)+k*.02;g.save();g.translate(W/2+(hash(Math.floor(t*12))-.5)*10,H/2+(hash(Math.floor(t*12)+5)-.5)*10);g.rotate(-.04);g.scale(s,s);
  g.fillStyle='#0a0807';g.fillRect(-W,-H,W*2,H*2);face(g,0,60,520,t,.95,{skin:'#cfc6b6'});g.restore();
  g.save();g.font='54px VT';g.fillStyle='#e0162b';g.fillText('● REC',60,170);g.restore()}
function sVictim(g,t,k){g.fillStyle='#0b0907';g.fillRect(0,0,W,H);g.save();g.translate(W/2,H/2+30);g.rotate(-.025);
  g.fillStyle='#c9b48a';g.fillRect(-640,-380,1280,760);g.fillStyle='#b9a37a';g.fillRect(-640,-420,420,60);
  [['VÍCTIMA 1','MARK HEATHCLIFF','17 AÑOS'],['VÍCTIMA 2','CESAR TORRES','REEMPLAZADO']].forEach((v,i)=>{const x=-580+i*640;g.fillStyle='#2a2622';g.fillRect(x,-300,220,280);
    g.save();g.beginPath();g.rect(x,-300,220,280);g.clip();person(g,x+110,0,300,{suit:i===1});g.restore();
    g.strokeStyle='#8c1b1b';g.lineWidth=10;if(k>1.5+i*.8){g.beginPath();g.moveTo(x,-300);g.lineTo(x+220,-20);g.moveTo(x+220,-300);g.lineTo(x,-20);g.stroke()}
    g.fillStyle='#1c1c1c';g.font='44px VT';g.fillText(v[0],x+250,-250);g.font='700 34px Inter';g.fillText(v[1],x+250,-190);g.font='40px VT';g.fillText(v[2],x+250,-140)});
  g.fillStyle='rgba(30,30,30,.5)';for(let i=0;i<6;i++)g.fillRect(-560,80+i*42,i%3==2?700:1120,14);g.restore();stamp(g,'ARCHIVO',W*.72,H*.78,k-.6,'#8c1b1b',-.12,110)}
function sAlert(g,t,k){broadcastScreen(g,W,H,t,k,'ALERTA · INTRUSO',['NIÑOS DESAPARECIDOS','EN CUATRO CONDADOS','NO DEJE SOLOS A SUS HIJOS'],'SI VE ALGO EN LA HABITACIÓN DE SUS HIJOS NO LO MIRE · LLAME A LAS AUTORIDADES')}
function sMissing(g,t,k){g.fillStyle='#1a1712';g.fillRect(0,0,W,H);const off=-k*30;
  for(let r=0;r<4;r++)for(let c=0;c<9;c++){const x=c*240+off+(r%2)*120-60,y=r*270+30,rot=(hash(r*9+c)-.5)*.12+Math.sin(t*2+r+c)*.012;g.save();g.translate(x+100,y+120);g.rotate(rot);
    g.fillStyle='#e8e1cf';g.fillRect(-95,-115,190,240);g.fillStyle='#b5121f';g.fillRect(-95,-115,190,36);g.fillStyle='#fff';g.font='26px Anton';g.textAlign='center';g.fillText('DESAPARECIDO',0,-88);
    g.fillStyle='#3a3530';g.fillRect(-60,-70,120,120);g.save();g.beginPath();g.rect(-60,-70,120,120);g.clip();person(g,0,90,150,{});g.restore();g.fillStyle='rgba(30,30,30,.6)';g.fillRect(-70,64,140,10);g.fillRect(-70,84,100,10);g.restore()}
  big(g,'MILES DE NIÑOS · 4 CONDADOS',H*.9,80,k-1,{maxW:1300})}
function sIntruder(g,t,k,L){g.fillStyle='#05070c';g.fillRect(0,0,W,H);const nl=g.createRadialGradient(380,820,10,380,820,380);nl.addColorStop(0,'rgba(120,150,255,.3)');nl.addColorStop(1,'rgba(120,150,255,0)');g.fillStyle=nl;g.fillRect(0,0,W,H);
  g.fillStyle='#0d1018';g.fillRect(0,860,W,220);g.fillStyle='#161a24';g.fillRect(140,700,620,170);g.fillStyle='#1f2533';rr(g,170,660,220,70,30);g.fill();g.fillStyle='#1a1f2c';g.beginPath();g.ellipse(520,700,200,60,0,Math.PI,0);g.fill();
  g.fillStyle='#f2d24a';g.beginPath();g.arc(380,820,10,0,7);g.fill();
  const dx=1300,dy=180;const dl=g.createLinearGradient(dx,0,dx+340,0);dl.addColorStop(0,'#2a2a30');dl.addColorStop(1,'#14141a');g.fillStyle=dl;g.fillRect(dx,dy,340,700);g.strokeStyle='#0f121a';g.lineWidth=18;g.strokeRect(dx,dy,340,700);
  const tilt=Math.sin(t*.6)*.08+clamp(k/5)*.12;g.save();g.translate(dx+170,dy+700);g.rotate(tilt*.2);g.fillStyle='#000';g.fillRect(-40,-650,80,650);g.beginPath();g.ellipse(0,-680,46,60,tilt,0,7);g.fill();
  g.fillStyle='rgba(230,225,210,.85)';g.fillRect(-20,-690,10,4);g.fillRect(10,-690,10,4);g.restore();
  g.strokeStyle='#000';g.lineWidth=7;g.lineCap='round';for(let f=0;f<4;f++){g.beginPath();g.moveTo(dx-6,dy+300+f*22);g.quadraticCurveTo(dx-50,dy+305+f*22,dx-70-f*6,dy+330+f*26);g.stroke()}}
function sBasement(g,t,k,L){g.fillStyle='#030303';g.fillRect(0,0,W,H);const bx=W*.5+Math.sin(t*.9)*420,by=H*.55+Math.sin(t*.6)*90;
  g.fillStyle='#0b0a09';for(let i=0;i<8;i++)g.fillRect(i*80,i*60,90,26);
  const fl=g.createRadialGradient(bx,by,10,bx,by,320);fl.addColorStop(0,'rgba(255,240,200,.45)');fl.addColorStop(1,'rgba(255,240,200,0)');g.globalCompositeOperation='lighter';g.fillStyle=fl;g.fillRect(0,0,W,H);g.globalCompositeOperation='source-over';
  g.fillStyle='#0d0c0b';g.fillRect(0,880,W,200);person(g,820,960,420,{});person(g,1100,960,400,{});
  const Wd=L.i===firstOf('basement').i?[]:['¿QUÉ HAS HECHO?','¿QUÉ HAS HECHO?','HICE LO CORRECTO','¿QUÉ HAS HECHO?','HICE LO CORRECTO'];
  Wd.forEach((w,i)=>{const a=clamp((k-i*.8)*1.5)*clamp(2.5-(k-i*.8)*.5);if(a<=0)return;g.save();g.globalAlpha=a;g.font=(i%2?'700 ':'italic 700 ')+'52px Inter';g.fillStyle=w.startsWith('HICE')?'#7dffef':'#e9e2d2';
    g.fillText(w,[140,1300,200,1250,700][i],[220,180,620,560,140][i]-(k-i*.8)*10);g.restore()})}
function sSkin(g,t,k){g.fillStyle='#070505';g.fillRect(0,0,W,H);const off=6+clamp(k/3)*18;
  for(let i=3;i>=0;i--){g.save();g.globalAlpha=i?.25:1;person(g,W/2+(i?Math.sin(t*3+i)*off:0),H+80,900,{c:i?'#7a1c1c':'#0a0807',eyes:i?null:'rgba(255,255,255,.9)'});g.restore()}
  g.strokeStyle='rgba(180,40,40,.6)';g.lineWidth=3;for(let i=0;i<6;i++){g.beginPath();g.moveTo(W/2-60+i*24,H*.35);g.quadraticCurveTo(W/2-80+i*30,H*.5,W/2-40+i*20,H*.7);g.stroke()}}
function sApple(g,t,k,L){g.fillStyle='#020203';g.fillRect(0,0,W,H);const cg=g.createRadialGradient(W/2,H*.42,20,W/2,H*.42,700);cg.addColorStop(0,'rgba(255,245,220,.35)');cg.addColorStop(1,'rgba(255,245,220,0)');g.fillStyle=cg;g.fillRect(0,0,W,H);
  for(let p=0;p<3;p++)[-1,1].forEach(sd=>{g.save();g.translate(W/2,H*.42);g.scale(sd,1);g.rotate(-.5+p*.45+Math.sin(t*.8+p)*.05);g.fillStyle=`rgba(${200-p*50},${195-p*50},${180-p*50},${.55-p*.12})`;
    g.beginPath();g.moveTo(40,0);g.quadraticCurveTo(320,-160,560-p*60,-40);g.quadraticCurveTo(340,40,40,0);g.fill();
    for(let e=0;e<4;e++){const ex=150+e*95,ey=-50+e*6,open=Math.max(0,Math.sin(t*1.3+e+p*2+(sd>0?1:0)));g.fillStyle='#000';g.beginPath();g.ellipse(ex,ey,16,7*open+1,0,0,7);g.fill();if(open>.4){g.fillStyle='#f4efe3';g.beginPath();g.arc(ex,ey,3,0,7);g.fill()}}g.restore()});
  const ay=H*.62+Math.sin(t*1.6)*22,ar=Math.sin(t*.9)*.25;g.save();g.translate(W/2,ay);g.rotate(ar);const ag=g.createRadialGradient(0,0,10,0,0,160);ag.addColorStop(0,'rgba(255,40,40,.45)');ag.addColorStop(1,'rgba(255,40,40,0)');g.fillStyle=ag;g.fillRect(-160,-160,320,320);
  const ap=g.createRadialGradient(-22,-20,6,0,0,80);ap.addColorStop(0,'#ff6b6b');ap.addColorStop(1,'#7a0710');g.fillStyle=ap;g.beginPath();g.moveTo(0,-48);g.bezierCurveTo(60,-78,96,-12,64,40);g.bezierCurveTo(44,78,10,70,0,60);g.bezierCurveTo(-10,70,-44,78,-64,40);g.bezierCurveTo(-96,-12,-60,-78,0,-48);g.fill();
  g.strokeStyle='#3a2a14';g.lineWidth=7;g.beginPath();g.moveTo(0,-48);g.lineTo(6,-82);g.stroke();g.fillStyle='#2f6b2a';g.beginPath();g.ellipse(26,-76,22,9,-.4,0,7);g.fill();g.restore();
  const hr=clamp((t-firstOf('apple').t)/8);g.fillStyle='#0a0807';g.beginPath();g.moveTo(W/2-60,H+20);g.lineTo(W/2-30,lerp(H+20,ay+150,hr));g.lineTo(W/2+30,lerp(H+20,ay+150,hr));g.lineTo(W/2+60,H+20);g.fill()}
function sEnd(g,t,k){broadcastScreen(g,W,H,t,k,'FIN DE LA EMISIÓN',['¿QUIERES LA PARTE 2?','COMENTA «MANDELA»','Y NO ABRAS LA PUERTA.'],'BASADO EN THE MANDELA CATALOGUE DE ALEX KISTER · MIRA LA SERIE ORIGINAL EN SU CANAL')}
function sChapter(g,t,k,L){const [,a,b]=L.scene.split(':');g.fillStyle='#020202';g.fillRect(0,0,W,H);noise(g,.1,t);g.fillStyle='#e0162b';g.fillRect(W/2-300,H*.5+40,600*clamp(k/.6),6);
  big(g,a,H*.46,150,k-.1);if(b){g.save();g.font='70px VT';g.textAlign='center';g.fillStyle='#e9e2d2';g.globalAlpha=clamp((k-.5)*2);g.fillText(b,W/2,H*.62);g.restore()}}
function sWarn(g,t){g.fillStyle='#000';g.fillRect(0,0,W,H);g.save();g.textAlign='center';g.font='700 44px Inter';g.fillStyle='#e9e2d2';g.fillText('AVISO',W/2,H*.4);
  g.font='500 34px Inter';g.fillStyle='#b9b3a8';g.fillText('Este video habla de muerte, desapariciones y suicidio en una serie de ficción.',W/2,H*.5);g.fillText('Si estás pasando por un mal momento, busca ayuda: no estás solo.',W/2,H*.56);g.restore()}

const SC={broadcast:sBroadcast,title:sTitle,creator:sCreator,map:sMap,tv:sTV,faces:(g,t,k,L)=>sFaces(g,t,k,L,0),faces2:(g,t,k,L)=>sFaces(g,t,k,L,1),
  phone:(g,t,k,L)=>sPhone(g,t,k,L,0),phonealt:(g,t,k,L)=>sPhone(g,t,k,L,1),house:sHouse,cams:sCams,camhall:(g,t,k,L)=>sCamHall(g,t,k,L,0),scream:(g,t,k,L)=>sCamHall(g,t,k,L,1),
  distort:sDistort,street:sStreet,room:sRoom,bad:sBad,camface:sCamFace,victim:sVictim,alert:sAlert,missing:sMissing,intruder:sIntruder,basement:sBasement,skin:sSkin,apple:sApple,end:sEnd};
function scene(g,t,forLoop){
  if(t<LINES[0].t){sWarn(g,t);return 'MANDELA'}
  const L=lineAt(t),k=t-L.t,key=L.scene.startsWith('chapter')?'chapter':L.scene;
  // edad de escena: desde la primera línea consecutiva con la misma escena
  let i0=L.i;while(i0>0&&LINES[i0-1].scene===L.scene)i0--;const ks=t-LINES[i0].t;
  const fn=key==='chapter'?sChapter:SC[key];kb(g,ks,LINES[L.i].end-LINES[i0].t,()=>fn(g,t,key==='chapter'?k:ks,L),key==='camface'||key==='distort'?0:.05);
  const qs={scream:'«¿QUIÉN ERES?»',skin:'«TU PIEL NO ES TUYA»'}[key];if(qs)quote(g,qs,k-.2);else if(L.label)lower(g,L.label,k-.4);
  return key==='basement'||key==='skin'?'2009':key==='apple'?'VOL. 4':'MANDELA CO.'
}
window.NOLOOP=true;
