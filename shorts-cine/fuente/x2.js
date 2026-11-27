// X2 · Cómo sobrevivir a Pennywise (It)
window.CINE=1;window.BED='drone';window.GRADE='rgba(120,160,220,.07)';window.COVER_TEXT=['EL GLOBO','*ROJO*'];
window.DATE=()=>'DERRY';
function rain(g,t,n=120,a=.35){g.strokeStyle=`rgba(200,215,230,${a})`;g.lineWidth=2;for(let i=0;i<n;i++){const x=(hash(i*3.3)*W+t*60)%W,y=(hash(i*7.7)*H+t*1400*(.7+hash(i)*.5))%H;g.beginPath();g.moveTo(x,y);g.lineTo(x-8,y+40);g.stroke()}}
function balloon(g,x,y,s,t){g.save();g.translate(x+Math.sin(t*1.2)*14*s,y+Math.sin(t*.9)*20*s);g.scale(s,s);g.strokeStyle='rgba(230,230,230,.6)';g.lineWidth=2;g.beginPath();g.moveTo(0,70);g.quadraticCurveTo(14,140,-6,220);g.stroke();
  const bg=g.createRadialGradient(-22,-30,6,0,0,80);bg.addColorStop(0,'#ff6a6a');bg.addColorStop(1,'#8a0a0a');g.fillStyle=bg;g.beginPath();g.ellipse(0,0,62,76,0,0,7);g.fill();g.beginPath();g.moveTo(-6,74);g.lineTo(6,74);g.lineTo(0,84);g.fill();
  g.fillStyle='rgba(255,255,255,.35)';g.beginPath();g.ellipse(-22,-30,12,20,-.4,0,7);g.fill();g.restore()}
function street(g,t,ks,o={}){const s=g.createLinearGradient(0,0,0,H);s.addColorStop(0,'#05080c');s.addColorStop(1,'#10161c');g.fillStyle=s;g.fillRect(0,0,W,H);
  [[60,500,260],[760,420,300]].forEach(([x,y,w])=>{g.fillStyle='#0b0e12';g.fillRect(x,y,w,900);for(let yy=y+40;yy<y+700;yy+=90)for(let xx=x+30;xx<x+w-40;xx+=80)if(hash(xx+yy)>.6){g.fillStyle='rgba(255,210,140,.5)';g.fillRect(xx,yy,40,50)}});
  const lp=g.createRadialGradient(330,700,10,330,900,520);lp.addColorStop(0,'rgba(255,220,160,.35)');lp.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=lp;g.fillRect(0,0,W,H);g.fillStyle='#050608';g.fillRect(320,680,14,700);
  g.fillStyle='#0c0f12';g.fillRect(0,1380,W,540);g.fillStyle='#1a1e22';g.fillRect(0,1380,W,40);
  for(let k=0;k<30;k++){g.fillStyle=`rgba(255,220,160,${.06*(1-k/30)})`;g.fillRect(300+Math.sin(t*2+k)*20,1430+k*14,90-k*2,3)}
  // alcantarilla
  g.fillStyle='#030303';rr(g,560,1395,420,70,10);g.fill();g.fillStyle='#1a1e22';for(let i=0;i<7;i++)g.fillRect(580+i*58,1400,20,60);
  if(o.eyes){g.fillStyle='rgba(255,215,60,.95)';g.shadowColor='#ffd23c';g.shadowBlur=24;g.beginPath();g.ellipse(745,1432,10,6,0,0,7);g.ellipse(800,1432,10,6,0,0,7);g.fill();g.shadowBlur=0}
  if(o.boat){const bx=lerp(200,690,clamp(ks/4)),by=1490;g.fillStyle='#e8e0cc';g.beginPath();g.moveTo(bx-60,by);g.lineTo(bx+60,by);g.lineTo(bx+40,by+24);g.lineTo(bx-40,by+24);g.fill();g.beginPath();g.moveTo(bx,by);g.lineTo(bx,by-70);g.lineTo(bx+40,by);g.fill()}
  if(o.balloon)balloon(g,o.bx||540,o.by||900,o.bs||1.6,t);rain(g,t)}
function clown(g,x,fy,h,t,o={}){const s=h/100;g.save();g.translate(x,fy);g.scale(s,s);
  g.fillStyle='#08080a';g.beginPath();g.moveTo(-20,0);g.lineTo(-26,-58);g.lineTo(26,-58);g.lineTo(20,0);g.fill();
  g.fillStyle='#8a8478';for(let i=0;i<9;i++){const a=Math.PI+i/8*Math.PI;g.beginPath();g.ellipse(Math.cos(a)*20,-60+Math.sin(a)*-3,7,4,a,0,7);g.fill()}
  const fg=g.createLinearGradient(0,-100,0,-62);fg.addColorStop(0,'#bdb6a8');fg.addColorStop(1,'#6a645a');g.fillStyle=fg;g.beginPath();g.moveTo(-14,-92);g.quadraticCurveTo(-18,-70,-6,-63);g.lineTo(6,-63);g.quadraticCurveTo(18,-70,14,-92);g.quadraticCurveTo(0,-104,-14,-92);g.fill();
  g.fillStyle='#4a0f0a';[-1,1].forEach(sd=>{g.beginPath();g.moveTo(sd*12,-96);g.lineTo(sd*26,-100);g.lineTo(sd*20,-88);g.lineTo(sd*28,-84);g.lineTo(sd*14,-86);g.fill()});
  g.fillStyle='rgba(0,0,0,.55)';g.beginPath();g.ellipse(-6,-84,5,4,0,0,7);g.ellipse(6,-84,5,4,0,0,7);g.fill();
  g.fillStyle='rgba(255,205,50,.95)';g.shadowColor='#ffcc33';g.shadowBlur=10;g.beginPath();g.ellipse(-6,-84,2.4,1.6,-.2,0,7);g.ellipse(6,-84,2.4,1.6,.2,0,7);g.fill();g.shadowBlur=0;
  g.strokeStyle='#7a0e0e';g.lineWidth=1.4;g.beginPath();g.moveTo(-3,-92);g.lineTo(-5,-75);g.moveTo(3,-92);g.lineTo(5,-75);g.stroke();
  g.fillStyle='#1a0505';g.beginPath();g.moveTo(-9,-71);g.quadraticCurveTo(0,o.grin?-62:-67,9,-71);g.quadraticCurveTo(0,-69,-9,-71);g.fill();
  if(o.grin){g.fillStyle='#d8d0b8';for(let i=-7;i<=7;i+=2){g.beginPath();g.moveTo(i,-70);g.lineTo(i+1,-66);g.lineTo(i+2,-70);g.fill()}}
  g.restore()}
const SC={drain:(g,t,ks)=>street(g,t,ks,{eyes:ks>1.4,boat:1}),
 derry:(g,t,ks)=>{street(g,t,ks,{});g.fillStyle='rgba(0,0,0,.35)';g.fillRect(0,0,W,H);g.save();g.font='54px VT';g.fillStyle='#e9e2d2';g.textAlign='center';['1958','1985','2012?'].forEach((y,i)=>{const a=clamp((ks-.5-i*.8)*2);g.globalAlpha=a;g.fillText(y,540,1000+i*90)});g.restore()},
 fear:(g,t,ks)=>{street(g,t,ks,{});g.fillStyle='rgba(0,0,0,.5)';g.fillRect(0,0,W,H);clown(g,540,1900,lerp(1100,1500,clamp(ks/4)),t,{grin:ks>1})},
 group:(g,t,ks)=>{street(g,t,ks,{});for(let i=0;i<7;i++)person(g,170+i*125,1600,lerp(330,380,hash(i)),{});},
 small:(g,t,ks)=>{street(g,t,ks,{});const z=lerp(1.4,.35,ease(clamp(ks/4)));clown(g,540,1420,500*z,t,{})},
 balloon:(g,t,ks)=>street(g,t,ks,{balloon:1,bx:540,by:lerp(1300,900,clamp(ks/4)),bs:1.8,eyes:ks>2}),
 drainend:(g,t,ks)=>street(g,t,ks,{eyes:true,balloon:1,bx:880,by:1100,bs:1})};
