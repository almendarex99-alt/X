// W2 · Lo más aterrador que ya encontraron en GTA VI
window.BED='forest';window.GRADE='rgba(40,200,190,.08)';window.COVER_TEXT=['YA LO','*ENCONTRARON*'];
window.DATE=()=>'NOV. 2026';window.SMALLS={5:'Según algunos jugadores · aún sin confirmar del todo'};
function mangrove(g,x,y,s,col){g.save();g.translate(x,y);g.scale(s,s);g.strokeStyle=col;g.fillStyle=col;g.lineWidth=10;
  for(let i=-3;i<=3;i++){g.beginPath();g.moveTo(i*12,-120);g.quadraticCurveTo(i*40,-40,i*55,10);g.stroke()}g.fillRect(-14,-420,28,300);
  for(let i=0;i<6;i++){g.beginPath();g.ellipse(-60+i*24,-430-hash(i)*60,90,50,0,0,7);g.fill()}g.restore()}
function swamp(g,t,ks,o={}){const s=g.createLinearGradient(0,0,0,H);s.addColorStop(0,'#05030c');s.addColorStop(.42,'#2a0d33');s.addColorStop(.55,'#0f4a52');s.addColorStop(.62,'#071216');s.addColorStop(1,'#020406');g.fillStyle=s;g.fillRect(0,0,W,H);
  // ciudad de neón lejana
  let x=0,i=0;while(x<W){const w=30+hash(i)*60,h=40+hash(i*3)*180;g.fillStyle='#120818';g.fillRect(x,1060-h,w,h);if(hash(i*7)>.5){g.fillStyle=hash(i)>.5?'rgba(255,60,170,.8)':'rgba(40,230,220,.8)';g.fillRect(x+6,1060-h+10,w-12,4)}x+=w+4;i++}
  const ng=g.createLinearGradient(0,900,0,1100);ng.addColorStop(0,'rgba(255,60,170,0)');ng.addColorStop(1,'rgba(255,60,170,.25)');g.fillStyle=ng;g.fillRect(0,900,W,200);
  // agua con reflejos
  g.fillStyle='#03080a';g.fillRect(0,1120,W,800);for(let k=0;k<40;k++){const y=1130+k*18,a=.12*(1-k/40);g.fillStyle=`rgba(255,80,180,${a})`;g.fillRect(W*.2+Math.sin(t*1.5+k)*40,y,W*.6*(1-k/50),3)}
  g.globalAlpha=.35;g.drawImage(FOG,-(t*10)%540,800,W*1.6,700);g.globalAlpha=1;
  mangrove(g,120,1180,1.1,'#020203');mangrove(g,980,1200,1.3,'#010102');mangrove(g,700,1120,.6,'#06040a');
  if(o.fig)o.fig();
  for(let k=0;k<26;k++){const fx=(hash(k*3.1)*W+Math.sin(t*.7+k)*30),fy=900+hash(k*1.7)*700+Math.sin(t+k)*20;g.fillStyle=`rgba(200,255,120,${.4+.5*Math.sin(t*3+k)})`;g.fillRect(fx,fy,4,4)}}
function skunk(g,t,ks){swamp(g,t,ks,{fig:()=>{bigfoot(g,560,1360,lerp(500,720,clamp(ks/6)),1,t,.4);
  for(let k=0;k<30;k++){const a=hash(k)*6.28,r=(t*60+hash(k*3)*300)%300;g.fillStyle=`rgba(150,200,60,${.25*(1-r/300)})`;g.beginPath();g.arc(560+Math.cos(a)*r,1050+Math.sin(a)*r*.6,24,0,7);g.fill()}}})}
function callback(g,t,ks){g.save();g.beginPath();g.rect(0,0,W/2,H);g.clip();forest(g,t,{drift:.3});g.restore();g.save();g.beginPath();g.rect(W/2,0,W/2,H);g.clip();swamp(g,t,ks,{fig:()=>bigfoot(g,820,1330,520,1,t,.3)});g.restore();
  g.fillStyle='#000';g.fillRect(W/2-4,0,8,H);g.font='70px VT';g.fillStyle='#e9e2d2';g.fillText('2004',70,1500);g.textAlign='right';g.fillText('2026',W-70,1500);g.textAlign='left';
  if(ks>1.2)stamp(g,'FALSO',270,1260,ks-1.2,'#e0162b',-.15,90);if(ks>2)stamp(g,'REAL',810,1260,ks-2,'#f2d24a',.12,90)}
function dexter(g,t,ks){const s=g.createLinearGradient(0,0,0,H);s.addColorStop(0,'#06030e');s.addColorStop(1,'#1a0a22');g.fillStyle=s;g.fillRect(0,0,W,H);
  let x=0,i=0;while(x<W){const w=50+hash(i+40)*90,h=200+hash(i*5)*520;g.fillStyle='#0c0612';g.fillRect(x,1250-h,w,h);for(let yy=1250-h+20;yy<1240;yy+=30)for(let xx=x+8;xx<x+w-10;xx+=20)if(hash(xx+yy)>.85){g.fillStyle='rgba(255,80,190,.6)';g.fillRect(xx,yy,8,10)}x+=w+6;i++}
  g.fillStyle='#120c10';g.fillRect(0,1250,W,700);g.strokeStyle='rgba(210,220,230,.35)';g.lineWidth=3;for(let k=0;k<6;k++){g.beginPath();g.moveTo(80+k*170,1250);g.quadraticCurveTo(120+k*170+Math.sin(t*2+k)*30,1500,90+k*170,1900);g.stroke()}
  g.fillStyle='#2a1f1a';g.fillRect(260,1420,560,40);g.fillRect(290,1460,20,200);g.fillRect(770,1460,20,200);
  g.fillStyle='#8a8a8a';g.beginPath();g.arc(380,1395,45,0,7);g.fill();g.fillStyle='#2a1f1a';g.beginPath();g.arc(380,1395,18,0,7);g.fill();
  g.strokeStyle='#a08050';g.lineWidth=10;for(let k=0;k<4;k++){g.beginPath();g.ellipse(560,1400-k*6,70-k*8,22,0,0,7);g.stroke()}
  g.save();g.translate(700,1395);g.rotate(-.2);g.fillStyle='rgba(220,230,240,.9)';g.fillRect(-60,-8,90,16);g.fillStyle='#c33';g.fillRect(-20,-6,40,12);g.strokeStyle='#ddd';g.lineWidth=3;g.beginPath();g.moveTo(30,0);g.lineTo(70,0);g.stroke();g.restore();
  const lg=g.createRadialGradient(540,1380,20,540,1380,420);lg.addColorStop(0,'rgba(255,250,230,.25)');lg.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=lg;g.fillRect(0,900,W,800)}
function ufo(g,t,ks){const s=g.createLinearGradient(0,0,0,H);s.addColorStop(0,'#02030a');s.addColorStop(1,'#0a0c12');g.fillStyle=s;g.fillRect(0,0,W,H);
  for(let i=0;i<80;i++){g.fillStyle='rgba(230,235,255,.8)';g.fillRect(hash(i*3.3)*W,hash(i*7.1)*900,2,2)}
  g.fillStyle='#050608';g.beginPath();g.moveTo(0,1500);g.lineTo(380,1150);g.lineTo(700,1150);g.lineTo(W,1500);g.lineTo(W,H);g.lineTo(0,H);g.fill();
  const ux=540+Math.sin(t*.6)*80,uy=640+Math.sin(t*1.3)*20;const bg=g.createLinearGradient(0,uy,0,1500);bg.addColorStop(0,'rgba(170,255,230,.45)');bg.addColorStop(1,'rgba(170,255,230,.05)');g.fillStyle=bg;g.beginPath();g.moveTo(ux-60,uy+30);g.lineTo(ux+60,uy+30);g.lineTo(ux+260,1500);g.lineTo(ux-260,1500);g.fill();
  g.fillStyle='#1c2028';g.beginPath();g.ellipse(ux,uy,230,46,0,0,7);g.fill();g.fillStyle='#3a4250';g.beginPath();g.ellipse(ux,uy-30,100,50,0,Math.PI,0);g.fill();
  for(let k=0;k<8;k++){g.fillStyle=Math.floor(t*6+k)%2?'#7dffef':'#e0162b';g.beginPath();g.arc(ux-180+k*52,uy+6,8,0,7);g.fill()}
  [[300,1420],[760,1440]].forEach(([x,y],i)=>{g.fillStyle='#0a0a0a';rr(g,x-110,y-60,220,70,16);g.fill();g.fillStyle=`rgba(255,${120+i*40},40,${.5+.5*Math.sin(t*9+i)})`;g.fillRect(x-80,y-40,160,10)});
  g.fillStyle='#14161a';g.fillRect(820,1180,200,200);g.fillStyle='#f2d24a';g.beginPath();g.moveTo(920,1210);g.lineTo(980,1310);g.lineTo(860,1310);g.closePath();g.fill();g.fillStyle='#14161a';g.font='70px Anton';g.textAlign='center';g.fillText('!',920,1300);g.textAlign='left'}
const SC={swamp:(g,t,ks)=>swamp(g,t,ks,{fig:()=>{if(ks>2.6)bigfoot(g,820,1180,240,clamp((ks-2.6)*.8)*.9,t)}}),skunk,callback,dexter,ufo,
  swampend:(g,t,ks)=>swamp(g,t,ks,{fig:()=>bigfoot(g,300,1210,300,.8,t,.2)})};
