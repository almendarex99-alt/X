// X1 · Cómo sobrevivir al Creeper (Jeepers Creepers)
window.CINE=1;window.BED='forest';window.GRADE='rgba(255,170,90,.08)';window.COVER_TEXT=['NO TE','*ASOMES*'];
window.DATE=()=>'PRIMAVERA';
function dust(g,t,n=60,col='255,230,190'){for(let i=0;i<n;i++){const x=(hash(i*2.7)*W+Math.sin(t*.3+i)*30)%W,y=(hash(i*5.9)*H+t*8*(1+hash(i)))%H;g.fillStyle=`rgba(${col},${.15+.35*hash(i*3)})`;g.fillRect(x,y,3,3)}}
function plains(g,t,o={}){const s=g.createLinearGradient(0,0,0,H);s.addColorStop(0,'#1a0c08');s.addColorStop(.45,'#6a2e14');s.addColorStop(.58,'#c06a2a');s.addColorStop(.62,'#2a160c');s.addColorStop(1,'#070403');g.fillStyle=s;g.fillRect(0,0,W,H);
  const sun=g.createRadialGradient(540,1130,10,540,1130,420);sun.addColorStop(0,'rgba(255,190,110,.85)');sun.addColorStop(.25,'rgba(255,130,60,.35)');sun.addColorStop(1,'rgba(255,100,40,0)');g.fillStyle=sun;g.fillRect(0,600,W,900);
  g.fillStyle='#0a0504';g.fillRect(0,1180,W,740);
  for(let i=0;i<40;i++){const x=hash(i*4.1)*W;g.strokeStyle='rgba(10,5,4,1)';g.lineWidth=3;g.beginPath();g.moveTo(x,1190);g.lineTo(x+Math.sin(t+i)*6,1150-hash(i)*40);g.stroke()}
  if(o.road){g.fillStyle='#120b08';g.beginPath();g.moveTo(500,1180);g.lineTo(580,1180);g.lineTo(980,H);g.lineTo(100,H);g.fill();g.fillStyle='#c9a440';for(let k=0;k<10;k++){const z=((k/10)+t*.25)%1,y=lerp(1190,H,z*z),w=lerp(2,14,z*z),h=lerp(6,90,z*z);g.fillRect(540-w/2,y,w,h)}}
  dust(g,t,40)}
function truck(g,x,y,s,t){g.save();g.translate(x,y);g.scale(s,s);g.fillStyle='#0b0907';rr(g,-170,-150,340,170,18);g.fill();g.fillRect(-120,-230,240,90);
  g.fillStyle='rgba(255,200,120,.06)';g.fillRect(-110,-220,220,70);g.fillStyle='#050403';g.beginPath();g.arc(-120,20,48,0,7);g.arc(120,20,48,0,7);g.fill();
  g.fillStyle='rgba(255,230,180,.9)';g.shadowColor='rgba(255,220,150,1)';g.shadowBlur=40;g.beginPath();g.arc(-130,-60,18,0,7);g.arc(130,-60,18,0,7);g.fill();g.shadowBlur=0;
  g.fillStyle='#cfc7b0';g.fillRect(-70,-20,140,40);g.fillStyle='#1a1a1a';g.font='30px Anton';g.textAlign='center';g.fillText('BEATNGU',0,12);g.textAlign='left';g.restore()}
function mirror(g,t,ks){plains(g,t,{road:1});g.save();g.translate(540,1060);g.rotate(-.03);g.fillStyle='#050403';rr(g,-380,-180,760,360,170);g.fill();
  g.save();rr(g,-360,-160,720,320,150);g.clip();const mg=g.createLinearGradient(0,-160,0,160);mg.addColorStop(0,'#3a1a0c');mg.addColorStop(1,'#0a0605');g.fillStyle=mg;g.fillRect(-360,-160,720,320);
  truck(g,0,120,lerp(.6,1.4,clamp(ks/4)),t);g.restore();g.strokeStyle='#2a2420';g.lineWidth=10;rr(g,-360,-160,720,320,150);g.stroke();g.restore()}
function church(g,t,ks){plains(g,t);g.fillStyle='#0c0605';g.beginPath();g.moveTo(330,1190);g.lineTo(330,880);g.lineTo(470,760);g.lineTo(610,880);g.lineTo(610,1190);g.fill();g.fillRect(450,600,40,170);g.fillRect(430,640,80,16);
  g.fillStyle=`rgba(255,170,80,${.3+.2*Math.sin(t*2)})`;g.fillRect(445,950,50,80);
  g.fillStyle='#1a120c';g.save();g.translate(760,1240);g.rotate(-.4);g.fillRect(-60,-40,260,80);g.fillStyle='#000';g.beginPath();g.ellipse(-60,0,30,40,0,0,7);g.fill();g.restore();
  if(ks>2){g.save();g.globalAlpha=clamp((ks-2)*.6);winged(g,470,760,300,t,.3);g.restore()}}
function winged(g,x,y,h,t,open=1){const s=h/100;g.save();g.translate(x,y);g.scale(s,s);g.fillStyle='#050302';
  const wo=open*(1+.05*Math.sin(t*3));[-1,1].forEach(sd=>{g.save();g.scale(sd,1);g.beginPath();g.moveTo(5,-60);g.quadraticCurveTo(70*wo,-110,110*wo,-60);g.lineTo(90*wo,-40);g.lineTo(80*wo,-55);g.lineTo(60*wo,-30);g.lineTo(50*wo,-45);g.lineTo(30*wo,-20);g.lineTo(8,-30);g.fill();g.restore()});
  g.fillRect(-8,-62,16,58);g.beginPath();g.ellipse(0,-70,9,11,0,0,7);g.fill();g.fillRect(-14,-80,28,4);g.fillRect(-9,-90,18,10);
  g.fillStyle='rgba(255,220,120,.9)';g.fillRect(-5,-71,3,2);g.fillRect(2,-71,3,2);g.restore()}
function calendar(g,t,ks){g.fillStyle='#0c0907';g.fillRect(0,0,W,H);const lg=g.createRadialGradient(540,1000,60,540,1000,800);lg.addColorStop(0,'rgba(255,200,140,.3)');lg.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=lg;g.fillRect(0,0,W,H);
  g.fillStyle='#e8e0cc';g.fillRect(140,760,800,760);g.fillStyle='#8a1b1b';g.fillRect(140,760,800,100);g.fillStyle='#fff';g.font='60px Anton';g.textAlign='center';g.fillText('PRIMAVERA',540,832);
  const n=Math.min(23,Math.floor(ks*5));for(let d=0;d<28;d++){const x=170+(d%7)*108,y=900+Math.floor(d/7)*140;g.fillStyle='#1c1c1c';g.font='44px Anton';g.fillText(String(d+1),x+50,y+60);
    if(d<n){g.strokeStyle='#b01414';g.lineWidth=8;g.beginPath();g.moveTo(x+14,y+14);g.lineTo(x+86,y+90);g.moveTo(x+86,y+14);g.lineTo(x+14,y+90);g.stroke()}}g.textAlign='left'}
function wings(g,t,ks){plains(g,t);const z=lerp(.7,2.2,ease(clamp(ks/4)));winged(g,540,1400+z*120,500*z,t,1);dust(g,t,50,'255,200,150')}
const SC={road:mirror,truck:(g,t,ks)=>{plains(g,t,{road:1});truck(g,540,1520,lerp(1.4,1.9,clamp(ks/5)),t)},spring:(g,t,ks)=>{plains(g,t);winged(g,540,1180,260,t,clamp(ks/2))},church,calendar,wings,roadend:mirror};
