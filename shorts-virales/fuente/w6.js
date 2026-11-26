// W6 · Cómo sobrevivir a SCP-173 (contenido de la Fundación SCP, CC BY-SA 3.0)
window.BED='drone';window.GRADE='rgba(150,180,170,.07)';window.COVER_TEXT=['NO','*PARPADEES*'];
window.DATE=()=>'CONT. 173';window.SMALLS={7:'SCP-173 · SCP Wiki · CC BY-SA 3.0'};
window.NOZOOM=['blink'];
function cellRoom(g,t,ks){const s=g.createLinearGradient(0,0,0,H);s.addColorStop(0,'#0c0e0d');s.addColorStop(1,'#050606');g.fillStyle=s;g.fillRect(0,0,W,H);
  // paredes de hormigón en perspectiva
  g.fillStyle='#1c201e';g.beginPath();g.moveTo(0,0);g.lineTo(260,520);g.lineTo(260,1360);g.lineTo(0,1920);g.fill();g.beginPath();g.moveTo(W,0);g.lineTo(820,520);g.lineTo(820,1360);g.lineTo(W,1920);g.fill();
  g.fillStyle='#262b28';g.fillRect(260,520,560,840);g.fillStyle='#131614';g.beginPath();g.moveTo(0,1920);g.lineTo(260,1360);g.lineTo(820,1360);g.lineTo(W,1920);g.fill();
  g.strokeStyle='rgba(0,0,0,.35)';g.lineWidth=3;for(let i=0;i<8;i++){g.beginPath();g.moveTo(260,520+i*105);g.lineTo(820,520+i*105);g.stroke()}
  // manchas rojizas
  g.fillStyle='rgba(90,30,20,.55)';for(let i=0;i<7;i++){g.beginPath();g.ellipse(300+hash(i)*480,1340+hash(i*3)*80,40+hash(i*5)*70,12,0,0,7);g.fill()}
  // foco cenital
  const lg=g.createRadialGradient(540,700,20,540,1100,700);lg.addColorStop(0,`rgba(230,240,230,${.35*flick(t,.4)})`);lg.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=lg;g.fillRect(0,0,W,H);
  g.fillStyle='#e0162b';g.beginPath();g.arc(780,560,8,0,7);g.fill()}
function statue(g,x,fy,h,t,o={}){const s=h/100;g.save();g.translate(x,fy);g.scale(s,s);
  const c=g.createLinearGradient(-20,-100,20,0);c.addColorStop(0,'#9a9486');c.addColorStop(1,'#5e5a50');g.fillStyle=c;
  g.beginPath();g.moveTo(-12,0);g.lineTo(-14,-55);g.quadraticCurveTo(-18,-70,-10,-78);g.lineTo(10,-78);g.quadraticCurveTo(18,-70,14,-55);g.lineTo(12,0);g.closePath();g.fill();
  g.beginPath();g.ellipse(0,-90,13,15,0,0,7);g.fill();g.strokeStyle='#6a665c';g.lineWidth=5;g.lineCap='round';g.beginPath();g.moveTo(-14,-70);g.lineTo(-22,-38);g.moveTo(14,-70);g.lineTo(22,-38);g.stroke();
  g.strokeStyle='#5a3a2a';g.lineWidth=1.4;[[-6,-60,-4,-50],[8,-40,12,-30],[-10,-20,-14,-8]].forEach(a=>{g.beginPath();g.moveTo(a[0],a[1]);g.lineTo(a[2],a[3]);g.stroke()});
  g.strokeStyle='#3a3a3a';g.lineWidth=1.8;g.beginPath();g.moveTo(-8,-2);g.lineTo(-10,6);g.moveTo(6,-4);g.lineTo(9,5);g.stroke();
  g.fillStyle='rgba(40,140,60,.9)';g.fillRect(-9,-96,6,4);g.fillRect(3,-96,6,4);g.fillStyle='rgba(170,30,30,.9)';g.beginPath();g.moveTo(-7,-84);g.quadraticCurveTo(0,-80,7,-84);g.lineTo(5,-82);g.quadraticCurveTo(0,-79,-5,-82);g.fill();
  g.fillStyle='rgba(0,0,0,.25)';g.fillRect(0,-100,14,100);g.restore()}
function sCell(g,t,ks,L){cellRoom(g,t,ks);statue(g,540,1360,lerp(480,620,clamp(ks/6)),t)}
function sNeck(g,t,ks){cellRoom(g,t,ks);statue(g,540,2300,2400,t);g.fillStyle=`rgba(150,0,0,${.15+.1*Math.sin(t*5)})`;g.fillRect(0,0,W,H)}
function sTeam(g,t,ks){cellRoom(g,t,ks);statue(g,540,1300,420,t);
  [[200,1800],[540,1880],[880,1800]].forEach(([x,y],i)=>{person(g,x,y,700,{});const ex=x+(540-x)*.1,ey=y-640;g.save();g.globalCompositeOperation='lighter';const fl=g.createLinearGradient(ex,ey,540,1100);fl.addColorStop(0,'rgba(255,250,220,.22)');fl.addColorStop(1,'rgba(255,250,220,0)');g.fillStyle=fl;g.beginPath();g.moveTo(ex-10,ey);g.lineTo(540-120,1000);g.lineTo(540+120,1000);g.lineTo(ex+10,ey);g.fill();g.restore()})}
function sBlink(g,t,ks){cellRoom(g,t,ks);const closed=ks<.55;if(ks<.35)statue(g,540,1360,560,t);else statue(g,540,2100,1800,t);
  const lid=ks<.3?ease(ks/.3):ks<.55?1:1-ease((ks-.55)/.25);g.fillStyle='#000';g.fillRect(0,0,W,H/2*lid);g.fillRect(0,H-H/2*lid,W,H/2*lid)}
const SC={cell:sCell,statue:sCell,neck:sNeck,team:sTeam,blink:sBlink,cellend:sCell};
