// W3 · 3 mitos de videojuegos de terror que resultaron REALES
window.BED='tape';window.GRADE='rgba(120,160,255,.06)';window.COVER_TEXT=['ERAN','*REALES*'];
window.DATE=(L)=>({ghostcar:'OCT. 2004',mantis:'1998',bigfoot:'NOV. 2026'}[L.scene]||'HOY');
function files(g,t,ks,real){g.fillStyle='#08080a';g.fillRect(0,0,W,H);const lg=g.createRadialGradient(540,1150,40,540,1150,800);lg.addColorStop(0,'rgba(255,220,160,.22)');lg.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=lg;g.fillRect(0,0,W,H);
  g.fillStyle='#2a1f16';g.fillRect(0,1350,W,600);
  ['SAN ANDREAS · 2004','METAL GEAR SOLID · 1998','GTA VI · 2026'].forEach((n,i)=>{g.save();g.translate(250+i*290,1220+Math.sin(t+i)*6);g.rotate((i-1)*.08);g.fillStyle='#c9b48a';g.fillRect(-120,-160,240,300);g.fillStyle='#b9a37a';g.fillRect(-120,-190,100,34);
    g.fillStyle='#1c1c1c';g.font='24px VT';g.textAlign='center';g.fillText('EXPEDIENTE',0,-110);g.font='700 22px Inter';g.fillText(n,0,-70);g.fillStyle='rgba(30,30,30,.5)';for(let k=0;k<5;k++)g.fillRect(-90,-30+k*30,180,10);
    g.restore();if(real&&ks>.8+i*.4)stamp(g,'REAL',250+i*290,1230,ks-.8-i*.4,'#f2d24a',(i-1)*.1,62)})}
function mantis(g,t,ks,L){g.fillStyle='#060608';g.fillRect(0,0,W,H);const second=L.i>3;
  const rg=g.createRadialGradient(540,1000,40,540,1000,700);rg.addColorStop(0,'rgba(120,180,255,.22)');rg.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=rg;g.fillRect(0,0,W,H);
  for(let i=0;i<7;i++){const a=i/7*6.28+t*.4,r=360;g.save();g.translate(540+Math.cos(a)*r,1050+Math.sin(a)*r*.5+Math.sin(t*2+i)*20);g.rotate(Math.sin(t+i)*.4);g.fillStyle='#2a2622';g.fillRect(-40,-30,80,60);g.fillStyle='#1a1612';g.fillRect(-34,-24,68,48);g.restore()}
  const by=1350+Math.sin(t*1.4)*30;person(g,540,by,560,{});g.save();g.translate(540,by-560*.9);g.fillStyle='#1d1d22';g.beginPath();g.ellipse(0,0,46,52,0,0,7);g.fill();
  g.fillStyle='rgba(255,60,40,.9)';g.shadowColor='#f33';g.shadowBlur=20;g.beginPath();g.arc(-18,-6,10,0,7);g.arc(18,-6,10,0,7);g.fill();g.shadowBlur=0;g.strokeStyle='#111';g.lineWidth=8;g.beginPath();g.moveTo(0,30);g.quadraticCurveTo(40,80,10,140);g.stroke();g.restore();
  if(second){g.save();g.translate(540,1620);const sh=Math.sin(t*60)*6;g.translate(sh,0);g.fillStyle='#2b2b30';rr(g,-200,-60,400,140,60);g.fill();g.fillStyle='#e0162b';g.beginPath();g.arc(120,0,14,0,7);g.fill();g.restore();
    g.save();g.translate(800,1520);g.rotate(.1);g.fillStyle='#d9d2c3';g.fillRect(-90,-120,180,240);g.fillStyle='#222';g.font='20px VT';['CASTLEVANIA','SUIKODEN','POLICENAUTS','AZURE DREAMS'].forEach((n,i)=>g.fillText(n,-80,-80+i*44));g.restore()}}
function ghostcar(g,t,ks,L){hillRoad(g,t,ease(clamp(ks/7)));if(L.i===2)stamp(g,'FALLO',W/2,1250,L.t?(t-L.t)-.6:0,'#f2d24a',.12,110)}
function bigS(g,t,ks){forest(g,t,{flash:1,figure:{layer:2,draw:()=>bigfoot(g,560,1980,1300,1,t,.2)}});if(ks>1.4)stamp(g,'REAL',W/2,1150,ks-1.4,'#f2d24a',-.1,120)}
const SC={hook:(g,t,ks)=>files(g,t,ks,true),ghostcar,mantis,bigfoot:bigS,hookend:(g,t,ks)=>files(g,t,ks,true)};
