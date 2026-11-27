// X8 · ¿Qué pasaría si cayeras a la Fosa de las Marianas?
window.CINE=1;window.BED='drone';window.GRADE='rgba(40,120,200,.08)';window.COVER_TEXT=['11 KM','*DE ABISMO*'];
const DEPTH={surface:0,d200:200,d1000:1000,fish:8336,bottom:10935,sub:10935,subend:10935};
window.DATE=(L)=>'PROF. '+(DEPTH[L.scene]||0).toLocaleString('es-ES')+' M';
function sea(g,t,depth,ks){const k=clamp(Math.log10(1+depth)/4.05);const c1=[lerp(40,0,k),lerp(140,4,k),lerp(200,10,k)],c2=[lerp(10,0,k),lerp(60,2,k),lerp(110,6,k)];
  const s=g.createLinearGradient(0,0,0,H);s.addColorStop(0,`rgb(${c1.map(Math.round)})`);s.addColorStop(1,`rgb(${c2.map(Math.round)})`);g.fillStyle=s;g.fillRect(0,0,W,H);
  if(depth<300){for(let i=0;i<6;i++){const x=200+i*140+Math.sin(t*.5+i)*40;g.fillStyle=`rgba(200,240,255,${.08*(1-depth/300)})`;g.beginPath();g.moveTo(x,0);g.lineTo(x+60,0);g.lineTo(x+260,H);g.lineTo(x+120,H);g.fill()}}
  for(let i=0;i<120;i++){const x=(hash(i*3.1)*W+Math.sin(t*.3+i)*20)%W,y=(hash(i*7.3)*H+t*25*(1+hash(i)))%H;g.fillStyle=`rgba(220,235,240,${.12+.25*hash(i*5)})`;g.fillRect(x,y,3,3)}
  // medidor
  g.save();g.fillStyle='rgba(0,0,0,.5)';rr(g,W-150,420,90,960,20);g.fill();const yy=420+960*k;g.fillStyle='#7dffef';g.fillRect(W-140,yy-4,70,8);g.font='30px VT';g.fillStyle='#e9e2d2';g.textAlign='right';g.fillText(depth.toLocaleString('es-ES')+' m',W-170,yy+10);g.restore()}
function glowFish(g,t){for(let i=0;i<9;i++){const x=(hash(i*4.4)*W+Math.sin(t*.4+i)*80),y=700+hash(i*2.2)*900+Math.sin(t*.7+i)*40;const gl=g.createRadialGradient(x,y,1,x,y,40);gl.addColorStop(0,`rgba(${i%2?'120,255,240':'255,120,220'},.9)`);gl.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=gl;g.fillRect(x-40,y-40,80,80)}
  const ax=380+Math.sin(t*.5)*60,ay=1200;g.fillStyle='#050608';g.beginPath();g.ellipse(ax,ay,140,70,0,0,7);g.fill();g.beginPath();g.moveTo(ax+130,ay);g.lineTo(ax+200,ay-50);g.lineTo(ax+200,ay+50);g.fill();
  g.strokeStyle='#0a0c10';g.lineWidth=5;g.beginPath();g.moveTo(ax-60,ay-60);g.quadraticCurveTo(ax-120,ay-200,ax-200,ay-130);g.stroke();const lg=g.createRadialGradient(ax-200,ay-130,2,ax-200,ay-130,60);lg.addColorStop(0,'rgba(200,255,250,1)');lg.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=lg;g.fillRect(ax-260,ay-190,120,120);
  g.fillStyle='#e8e0cc';for(let i=0;i<8;i++){g.beginPath();g.moveTo(ax-120+i*12,ay+10);g.lineTo(ax-114+i*12,ay+34);g.lineTo(ax-108+i*12,ay+10);g.fill()}}
function snailfish(g,x,y,s,t){g.save();g.translate(x+Math.sin(t*.8)*30,y);g.scale(s,s);g.globalAlpha=.85;const fg=g.createLinearGradient(-150,0,150,0);fg.addColorStop(0,'rgba(255,200,210,.85)');fg.addColorStop(1,'rgba(255,170,190,.25)');g.fillStyle=fg;
  g.beginPath();g.moveTo(-150,0);g.quadraticCurveTo(-120,-60,0,-40);g.quadraticCurveTo(120,-20,170,Math.sin(t*4)*10);g.quadraticCurveTo(120,30,0,40);g.quadraticCurveTo(-120,60,-150,0);g.fill();
  g.fillStyle='#200810';g.beginPath();g.arc(-110,-10,8,0,7);g.fill();g.restore()}
function sub(g,t,ks,big){const x=540,y=lerp(900,1100,clamp(ks/6));g.save();g.translate(x,y);g.scale(big?1.3:1,big?1.3:1);
  const lb=g.createLinearGradient(0,0,0,700);lb.addColorStop(0,'rgba(240,250,255,.4)');lb.addColorStop(1,'rgba(240,250,255,0)');g.fillStyle=lb;g.beginPath();g.moveTo(-60,40);g.lineTo(60,40);g.lineTo(300,700);g.lineTo(-300,700);g.fill();
  g.fillStyle='#d8c26a';g.beginPath();g.ellipse(0,0,120,150,0,0,7);g.fill();g.fillStyle='#1a2a3a';g.beginPath();g.arc(0,-20,48,0,7);g.fill();g.fillStyle='rgba(150,220,255,.5)';g.beginPath();g.arc(-14,-34,14,0,7);g.fill();
  g.fillStyle='#8a7a3a';g.fillRect(-130,80,260,30);g.restore()}
const SC={surface:(g,t,ks)=>{sea(g,t,lerp(0,120,clamp(ks/4)),ks);person(g,540,lerp(900,1300,clamp(ks/4)),300,{})},
 d200:(g,t,ks)=>{sea(g,t,lerp(150,600,clamp(ks/4)),ks);person(g,540,1300,220,{})},
 d1000:(g,t,ks)=>{sea(g,t,lerp(1000,3000,clamp(ks/4)),ks);glowFish(g,t)},
 fish:(g,t,ks)=>{sea(g,t,8336,ks);snailfish(g,540,1150,2.4,t)},
 bottom:(g,t,ks)=>{sea(g,t,10935,ks);g.fillStyle='#020304';g.beginPath();g.moveTo(0,1500);for(let x=0;x<=W;x+=60)g.lineTo(x,1500+Math.sin(x*.02)*40+hash(x)*30);g.lineTo(W,H);g.lineTo(0,H);g.fill();
   g.save();g.translate(540,1100);g.strokeStyle='#e9e2d2';g.lineWidth=8;g.beginPath();g.arc(0,0,170,Math.PI*.8,Math.PI*2.2);g.stroke();const a=Math.PI*.8+Math.PI*1.4*clamp(ks/2.5)+Math.sin(t*20)*.02;g.strokeStyle='#e0162b';g.lineWidth=10;g.beginPath();g.moveTo(0,0);g.lineTo(Math.cos(a)*150,Math.sin(a)*150);g.stroke();g.font='40px VT';g.fillStyle='#e9e2d2';g.textAlign='center';g.fillText('PRESIÓN',0,90);g.restore()},
 sub:(g,t,ks)=>{sea(g,t,10935,ks);sub(g,t,ks)},subend:(g,t,ks)=>{sea(g,t,10935,ks);sub(g,t,ks,1)}};
