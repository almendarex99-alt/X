// X3 · Cómo sobrevivir a Alien (1979)
window.CINE=1;window.BED='drone';window.GRADE='rgba(80,200,170,.07)';window.COVER_TEXT=['NADIE TE','*OYE*'];
window.DATE=()=>'2122';
const MET={wall:[90,100,96],floor:[60,66,64],ceil:[80,88,86],base:[50,56,54]};
function stars(g,t){g.fillStyle='#010204';g.fillRect(0,0,W,H);for(let i=0;i<220;i++){const x=(hash(i*3.1)*W-t*4*(1+hash(i)))%W,y=hash(i*7.3)*H;g.fillStyle=`rgba(220,230,255,${.3+.6*hash(i*5)})`;g.fillRect((x+W)%W,y,2,2)}}
function nostromo(g,x,y,s,t){g.save();g.translate(x,y);g.scale(s,s);g.fillStyle='#14171a';g.fillRect(-260,-60,520,120);g.fillRect(-180,-130,300,80);g.fillRect(140,-40,180,80);
  g.fillStyle='#0c0e10';for(let i=0;i<8;i++)g.fillRect(-250+i*62,-20,40,60);g.fillStyle='rgba(255,220,160,.8)';for(let i=0;i<14;i++)if(hash(i)>.4)g.fillRect(-240+i*34,-50,8,6);
  const eg=g.createRadialGradient(-280,0,4,-280,0,120);eg.addColorStop(0,'rgba(120,200,255,.9)');eg.addColorStop(1,'rgba(120,200,255,0)');g.fillStyle=eg;g.fillRect(-420,-120,200,240);g.restore()}
function corridor(g,t,ks,o={}){hall(g,{t,cam:{x:Math.sin(t*.4)*.1,y:Math.sin(t*1.5)*.02,z:ks*.18},pal:MET,lampZ:4.6,red:o.red??.45,flick:flick(t,.8),dark:o.dark||.2});
  for(let i=0;i<40;i++){const x=hash(i*3)*W,y=(hash(i*7)*H-t*60*(1+hash(i)))%H;g.fillStyle='rgba(220,230,230,.08)';g.beginPath();g.arc(x,(y+H)%H,20+hash(i)*30,0,7);g.fill()}
  if(Math.floor(t*1.2)%2){g.fillStyle='rgba(255,30,30,.10)';g.fillRect(0,0,W,H)}}
function egg(g,x,y,s,t,open){g.save();g.translate(x,y);g.scale(s,s);const eg=g.createRadialGradient(-10,-30,6,0,0,90);eg.addColorStop(0,'#6a6a52');eg.addColorStop(1,'#1c1c14');g.fillStyle=eg;
  g.beginPath();g.moveTo(-50,40);g.quadraticCurveTo(-70,-60,0,-80);g.quadraticCurveTo(70,-60,50,40);g.closePath();g.fill();
  if(open){g.fillStyle='#0a0a06';g.beginPath();for(let i=0;i<4;i++){const a=-Math.PI/2+(i-1.5)*.5;g.moveTo(0,-60);g.lineTo(Math.cos(a)*40,-60+Math.sin(a)*30)}g.fill();g.strokeStyle='#8a8a60';g.lineWidth=4;g.beginPath();g.moveTo(-30,-70);g.lineTo(0,-50);g.lineTo(30,-70);g.stroke()}
  g.restore()}
function eggs(g,t,ks){g.fillStyle='#030503';g.fillRect(0,0,W,H);const bl=g.createLinearGradient(0,900,0,H);bl.addColorStop(0,'rgba(80,180,255,0)');bl.addColorStop(.5,'rgba(80,180,255,.25)');bl.addColorStop(1,'rgba(80,180,255,.05)');g.fillStyle=bl;g.fillRect(0,900,W,1020);
  for(let i=0;i<9;i++){const x=120+(i%3)*400+(i>2?100:0)*(i%2),y=1300+Math.floor(i/3)*170;egg(g,x%W,y,lerp(.8,1.3,Math.floor(i/3)/2),t,i===4&&ks>1.4)}
  for(let i=0;i<50;i++){const x=hash(i*4.4)*W,y=900+hash(i*2.2)*900;g.fillStyle='rgba(140,210,255,.08)';g.beginPath();g.arc(x+Math.sin(t+i)*20,y,40,0,7);g.fill()}}
function acid(g,t,ks){corridor(g,t,ks,{red:.2});const k=clamp(ks/4);g.fillStyle='#0a1206';g.beginPath();g.ellipse(540,1500,120+k*160,40+k*50,0,0,7);g.fill();const ag=g.createRadialGradient(540,1500,10,540,1500,300);ag.addColorStop(0,'rgba(170,255,60,.5)');ag.addColorStop(1,'rgba(170,255,60,0)');g.fillStyle=ag;g.fillRect(200,1250,680,500);
  for(let i=0;i<20;i++){const y=1500-((t*120+i*40)%400);g.fillStyle='rgba(200,255,160,.12)';g.beginPath();g.arc(540+Math.sin(i+t)*60,y,24,0,7);g.fill()}
  for(let i=0;i<3;i++){const y=(t*500+i*300)%900+400;g.fillStyle='rgba(170,255,60,.9)';g.beginPath();g.ellipse(540+(i-1)*40,y,6,14,0,0,7);g.fill()}}
function tracker(g,t,ks){corridor(g,t,ks,{red:.3,dark:.4});g.save();g.translate(540,1150);g.fillStyle='#14161a';rr(g,-300,-260,600,560,40);g.fill();g.fillStyle='#03120c';g.beginPath();g.arc(0,40,220,Math.PI,0);g.lineTo(220,40);g.closePath();g.fill();
  g.strokeStyle='rgba(80,255,170,.35)';g.lineWidth=3;for(let r=60;r<=220;r+=55){g.beginPath();g.arc(0,40,r,Math.PI,0);g.stroke()}
  const sw=(t*1.3)%1;g.strokeStyle='rgba(80,255,170,.9)';g.beginPath();g.arc(0,40,220*sw,Math.PI,0);g.stroke();
  const d=lerp(200,30,clamp(ks/3.5));g.fillStyle='#ffffff';g.shadowColor='#5fffb0';g.shadowBlur=20;g.beginPath();g.arc(-20,40-d,12,0,7);g.fill();g.shadowBlur=0;
  g.font='44px VT';g.fillStyle='#5fffb0';g.textAlign='center';g.fillText(Math.max(0,Math.round(d/10))+' M',0,240);g.restore()}
function escape(g,t,ks){stars(g,t);const k=ease(clamp(ks/5));nostromo(g,560,1000,1.1,t);const fx=lerp(1,0,k);if(ks>2.5){const f=clamp((ks-2.5)*1.4);const fl=g.createRadialGradient(540,900,10,540,900,900*f);fl.addColorStop(0,`rgba(255,240,210,${1-f*.6})`);fl.addColorStop(1,'rgba(255,140,60,0)');g.fillStyle=fl;g.fillRect(0,0,W,H)}
  g.save();g.translate(lerp(540,780,k),lerp(1250,1500,k));g.fillStyle='#1c2024';rr(g,-90,-30,180,60,24);g.fill();g.fillStyle='rgba(120,200,255,.9)';g.beginPath();g.arc(-100,0,14,0,7);g.fill();g.restore()}
const SC={space:(g,t,ks)=>{stars(g,t);nostromo(g,lerp(500,620,ks/8),1050,1.2,t)},ship:(g,t,ks)=>corridor(g,t,ks),eggs,acid,tracker,escape,spaceend:(g,t,ks)=>{stars(g,t);nostromo(g,560,1050,.7,t)}};
