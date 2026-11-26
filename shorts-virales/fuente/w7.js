// W7 · Cómo sobrevivir a Un lugar en silencio
window.BED='forest';window.GRADE='rgba(120,160,120,.06)';window.COVER_TEXT=['NI UN','*RUIDO*'];
window.DATE=(L)=>L.scene==='island'?'PARTE II':'DÍA 89';
function creature(g,x,fy,h,t,open=0){const s=h/100;g.save();g.translate(x,fy);g.scale(s,s);g.fillStyle='#08090a';g.strokeStyle='#08090a';g.lineCap='round';
  g.lineWidth=4;[[-8,-50,-24,-24,-30,0],[8,-50,26,-22,32,0]].forEach(a=>{g.beginPath();g.moveTo(a[0],a[1]);g.lineTo(a[2],a[3]);g.lineTo(a[4],a[5]);g.stroke()});
  g.beginPath();g.moveTo(-14,-52);g.quadraticCurveTo(0,-78,14,-52);g.lineTo(8,-40);g.lineTo(-8,-40);g.closePath();g.fill();
  g.lineWidth=3.2;[[-12,-62,-40,-40,-46,-6],[12,-62,40,-42,48,-8]].forEach(a=>{g.beginPath();g.moveTo(a[0],a[1]);g.lineTo(a[2],a[3]);g.lineTo(a[4],a[5]);g.stroke()});
  g.save();g.translate(0,-80);g.beginPath();g.ellipse(0,0,10,13,0,0,7);g.fill();
  if(open>0){g.fillStyle='#3a1a14';g.beginPath();g.moveTo(-3,-10);g.lineTo(-16*open,-4);g.lineTo(-10,10);g.lineTo(0,4);g.lineTo(10,10);g.lineTo(16*open,-4);g.lineTo(3,-10);g.closePath();g.fill();
    g.strokeStyle='rgba(230,220,200,.7)';g.lineWidth=.8;for(let i=-3;i<=3;i++){g.beginPath();g.moveTo(i*3,0);g.lineTo(i*3.4,5);g.stroke()}}
  g.restore();g.restore()}
function farm(g,t,ks,o={}){const s=g.createLinearGradient(0,0,0,H);s.addColorStop(0,'#04060a');s.addColorStop(.6,'#151c1a');s.addColorStop(1,'#050605');g.fillStyle=s;g.fillRect(0,0,W,H);
  g.fillStyle='#d8e2e4';g.beginPath();g.arc(800,400,46,0,7);g.fill();g.fillStyle='#0a0c0b';g.fillRect(0,1300,W,620);
  // campo de maíz
  for(let i=0;i<70;i++){const x=hash(i*3.1)*W,y=1300+hash(i*1.7)*120;g.strokeStyle='#0f1410';g.lineWidth=5;g.beginPath();g.moveTo(x,y+40);g.lineTo(x+Math.sin(t+i)*8,y-160);g.stroke()}
  // casa y silo
  g.fillStyle='#0d0f10';g.beginPath();g.moveTo(240,1300);g.lineTo(240,1000);g.lineTo(420,880);g.lineTo(600,1000);g.lineTo(600,1300);g.fill();g.fillRect(760,860,150,440);g.beginPath();g.ellipse(835,860,75,40,0,Math.PI,0);g.fill();
  g.fillStyle=`rgba(255,200,120,${.5*flick(t,.3)})`;g.fillRect(290,1060,70,80);
  // tira de bombillas rojas (alarma)
  for(let i=0;i<9;i++){const x=120+i*110,y=1180+Math.sin(i)*10,on=o.alarm?Math.floor(t*3)%2===0:true;g.fillStyle=on?(o.alarm?'#ff2020':'rgba(255,190,120,.9)'):'#331010';g.beginPath();g.arc(x,y,9,0,7);g.fill();
    if(on){const rg=g.createRadialGradient(x,y,2,x,y,70);rg.addColorStop(0,o.alarm?'rgba(255,30,30,.4)':'rgba(255,190,120,.25)');rg.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=rg;g.fillRect(x-70,y-70,140,140)}}
  g.globalAlpha=.25;g.drawImage(FOG,-(t*8)%540,900,W*1.6,700);g.globalAlpha=1;if(o.fig)o.fig()}
function sand(g,t,ks){farm(g,t,ks);const pg=g.createLinearGradient(0,1300,0,H);pg.addColorStop(0,'#3a3426');pg.addColorStop(1,'#6a5e44');g.fillStyle=pg;g.beginPath();g.moveTo(480,1300);g.lineTo(600,1300);g.lineTo(820,H);g.lineTo(260,H);g.fill();
  for(let i=0;i<8;i++){const z=i/8,x=lerp(540,560,z)+(i%2?30:-30)*(1-z*.7),y=lerp(1860,1330,z),s=lerp(1,.25,z);if(i/8>1-clamp(ks/4))continue;g.fillStyle='rgba(40,34,24,.8)';g.beginPath();g.ellipse(x,y,22*s,40*s,0,0,7);g.fill()}}
function waterfall(g,t,ks){const s=g.createLinearGradient(0,0,0,H);s.addColorStop(0,'#0a1214');s.addColorStop(1,'#030506');g.fillStyle=s;g.fillRect(0,0,W,H);
  g.fillStyle='#0e1513';g.fillRect(0,300,280,1200);g.fillRect(800,300,280,1200);
  for(let i=0;i<60;i++){const x=300+hash(i)*480,y=(t*900+hash(i*3)*1400)%1400+300;g.fillStyle=`rgba(200,225,235,${.25+.35*hash(i*7)})`;g.fillRect(x,y,4+hash(i)*6,80)}
  const mg=g.createRadialGradient(540,1500,40,540,1500,600);mg.addColorStop(0,'rgba(220,235,240,.45)');mg.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=mg;g.fillRect(0,1000,W,900);
  g.fillStyle='#050707';g.fillRect(0,1560,W,400);person(g,380,1700,420,{});person(g,640,1700,300,{})}
function pitch(g,t,ks){farm(g,t,ks,{fig:()=>{const rec=clamp((ks-.6)*1.5);g.save();g.translate(Math.sin(t*40)*rec*10,0);creature(g,600,1360,lerp(620,560,rec),t,1);g.restore()}});
  for(let i=0;i<8;i++){const r=((t*600+i*90)%720);g.strokeStyle=`rgba(125,255,239,${.7*(1-r/720)})`;g.lineWidth=4;g.beginPath();for(let a=0;a<=6.3;a+=.1){const rr2=r+Math.sin(a*40+t*30)*6;const x=300+Math.cos(a)*rr2,y=1200+Math.sin(a)*rr2;a?g.lineTo(x,y):g.moveTo(x,y)}g.stroke()}}
function island(g,t,ks){const s=g.createLinearGradient(0,0,0,H);s.addColorStop(0,'#0a0f1a');s.addColorStop(.5,'#3a2a3a');s.addColorStop(.56,'#e0a070');s.addColorStop(.6,'#1a2430');s.addColorStop(1,'#04070a');g.fillStyle=s;g.fillRect(0,0,W,H);
  g.fillStyle='#070a0d';g.beginPath();g.ellipse(760,1100,260,40,0,Math.PI,0);g.fill();for(let i=0;i<6;i++){g.fillRect(620+i*50,980-hash(i)*60,10,120)}
  for(let k=0;k<30;k++){g.fillStyle=`rgba(255,200,150,${.15*(1-k/30)})`;g.fillRect(200+Math.sin(t+k)*30,1120+k*22,700-k*10,3)}
  const bx=lerp(160,520,clamp(ks/6));g.fillStyle='#050608';g.beginPath();g.moveTo(bx-110,1300);g.lineTo(bx+110,1300);g.lineTo(bx+80,1340);g.lineTo(bx-80,1340);g.fill();person(g,bx,1300,190,{});
  g.save();g.globalAlpha=.85;creature(g,120,1180,240,t)}
const SC={farm:(g,t,ks)=>farm(g,t,ks),creature:(g,t,ks)=>farm(g,t,ks,{alarm:1,fig:()=>creature(g,540,1500,lerp(700,1000,clamp(ks/4)),t,clamp((ks-1.2)*2))}),sand,waterfall,pitch,island,farmend:(g,t,ks)=>farm(g,t,ks,{fig:()=>creature(g,880,1310,260,t)})};
