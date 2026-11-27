// X4 · Cómo sobrevivir a la mansión de Resident Evil
window.CINE=1;window.BED='drone';window.GRADE='rgba(200,140,80,.07)';window.COVER_TEXT=['QUEMA EL','*CUERPO*'];
window.DATE=()=>'JUL. 1998';
function zombie(g,x,fy,h,t,o={}){const s=h/100,sw=Math.sin(t*1.6+x)*.08;g.save();g.translate(x,fy);g.scale(s,s);g.rotate(sw*.3);g.fillStyle=o.col||'#0b0908';g.strokeStyle=o.col||'#0b0908';g.lineCap='round';
  g.lineWidth=7;g.beginPath();g.moveTo(-5,-46);g.lineTo(-9,0);g.moveTo(5,-46);g.lineTo(8,0);g.stroke();g.beginPath();g.moveTo(-13,-80);g.lineTo(13,-80);g.lineTo(11,-44);g.lineTo(-11,-44);g.closePath();g.fill();
  g.lineWidth=5;g.beginPath();g.moveTo(-12,-76);g.lineTo(-20,-74+Math.sin(t*2)*3);g.lineTo(-30,-70);g.moveTo(12,-76);g.lineTo(22,-72);g.lineTo(32,-68+Math.sin(t*2+1)*3);g.stroke();
  g.save();g.translate(3,-90);g.rotate(.35);g.beginPath();g.ellipse(0,0,8.5,10,0,0,7);g.fill();if(o.eyes){g.fillStyle=o.eyes;g.fillRect(-5,-2,3,2);g.fillRect(2,-2,3,2)}g.restore();g.restore()}
function hallM(g,t,ks,o={}){const s=g.createLinearGradient(0,0,0,H);s.addColorStop(0,'#0e0805');s.addColorStop(1,'#050302');g.fillStyle=s;g.fillRect(0,0,W,H);
  // escalinata
  g.fillStyle='#2a1810';g.beginPath();g.moveTo(260,1500);g.lineTo(420,980);g.lineTo(660,980);g.lineTo(820,1500);g.fill();g.fillStyle='#5a1414';g.beginPath();g.moveTo(420,1500);g.lineTo(490,980);g.lineTo(590,980);g.lineTo(660,1500);g.fill();
  for(let i=0;i<14;i++){const y=lerp(1500,980,i/14);g.fillStyle='rgba(0,0,0,.25)';g.fillRect(lerp(260,420,i/14),y,lerp(560,240,i/14),4)}
  g.fillStyle='#1c120c';g.fillRect(140,760,800,220);g.fillStyle='#0b0705';[200,380,700,880].forEach(x=>g.fillRect(x-30,760,60,760));
  g.fillStyle='#2a1c10';g.fillRect(0,1500,W,420);for(let i=0;i<8;i++){g.fillStyle=i%2?'#1e140c':'#241810';g.fillRect(i*140,1500,140,420)}
  // lámpara de araña
  const cy=520;g.strokeStyle='#2a2018';g.lineWidth=4;g.beginPath();g.moveTo(540,250);g.lineTo(540,cy);g.stroke();for(let i=0;i<7;i++){const x=540+(i-3)*60,y=cy+Math.abs(i-3)*-8;g.fillStyle=`rgba(255,210,140,${.8*flick(t+i,.4)})`;g.beginPath();g.arc(x,y,8,0,7);g.fill()}
  const lg=g.createRadialGradient(540,cy,20,540,cy+300,800);lg.addColorStop(0,`rgba(255,200,130,${.3*flick(t,.5)})`);lg.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=lg;g.fillRect(0,0,W,H);
  if(o.fig)o.fig()}
function typewriter(g,t,ks){g.fillStyle='#0a0605';g.fillRect(0,0,W,H);const lg=g.createRadialGradient(540,1000,40,540,1000,700);lg.addColorStop(0,'rgba(255,220,160,.35)');lg.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=lg;g.fillRect(0,0,W,H);
  g.fillStyle='#2a1c12';g.fillRect(0,1250,W,700);g.fillStyle='#1a1a1c';rr(g,200,1050,680,260,30);g.fill();g.fillStyle='#2a2a2e';for(let r=0;r<3;r++)for(let k=0;k<10;k++){g.beginPath();g.arc(260+k*62+r*14,1170+r*48,20,0,7);g.fill()}
  g.fillStyle='#e8e0cc';g.fillRect(320,760,440,320);g.fillStyle='#1a1a1a';g.font='32px VT';const s='¿GUARDAR PARTIDA?';g.fillText(s.slice(0,Math.floor(ks*10)),350,840);if(ks>2){g.fillText('> SÍ    NO',350,900)}
  g.save();g.translate(860,1350);g.rotate(.2);g.fillStyle='#2a2a2e';g.fillRect(-70,-30,140,60);g.fillStyle='#c33';g.fillRect(-60,-8,120,16);g.fillStyle='#ddd';g.font='22px VT';g.fillText('INK RIBBON',-58,-14);g.restore()}
function ammo(g,t,ks){hallM(g,t,ks,{fig:()=>{zombie(g,380,1520,520,t);zombie(g,700,1500,480,t+1);zombie(g,540,1460,360,t+2)}});g.save();g.font='70px VT';g.fillStyle='#e9e2d2';g.textAlign='right';g.fillText('BALAS: '+Math.max(0,15-Math.floor(ks*3)),W-80,1600);g.restore()}
function crimson(g,t,ks){hallM(g,t,ks,{fig:()=>{if(ks<1.5){g.save();g.translate(540,1600);g.rotate(-Math.PI/2);zombie(g,0,0,420,t);g.restore()}else{zombie(g,540,1620,lerp(500,900,clamp((ks-1.5)/2)),t*2.5,{col:'#3a0a06',eyes:'#ff3b2b'})}
  if(ks>3.4){for(let i=0;i<30;i++){const x=540+(hash(i)-.5)*400,y=1600-((t*300+i*40)%500);g.fillStyle=`rgba(255,${120+hash(i)*100},40,${.6})`;g.beginPath();g.ellipse(x,y,20,40,0,0,7);g.fill()}}}})}
function diary(g,t,ks){g.fillStyle='#0b0705';g.fillRect(0,0,W,H);g.save();g.translate(540,1100);g.rotate(-.04);g.fillStyle='#d8cdb2';g.fillRect(-400,-500,800,1000);g.fillStyle='rgba(120,90,50,.25)';for(let i=0;i<20;i++)g.fillRect(-380,-460+i*48,760,2);
  g.fillStyle='#2a1a10';g.font='italic 700 40px Inter';const lines=['3 de mayo: hoy nos han','encargado vigilar a...','','...me pica todo el cuerpo','','','picor.','sabroso.'];
  lines.forEach((l,i)=>{const a=clamp(ks*2-i*.4);if(a<=0)return;g.globalAlpha=a;g.save();if(i>=6){g.font=`italic 700 ${44+i*6}px Inter`;g.fillStyle='#5a1010';g.rotate((hash(i)-.5)*.2)}g.fillText(l,-340,-400+i*90);g.restore()});g.globalAlpha=1;
  g.fillStyle='rgba(90,10,10,.6)';g.beginPath();g.ellipse(200,300,60,30,.4,0,7);g.fill();g.restore()}
const SC={mansion:(g,t,ks)=>hallM(g,t,ks,{fig:()=>{if(ks>2.5)zombie(g,540,990,140,t)}}),typewriter,ammo,crimson,diary,mansionend:(g,t,ks)=>hallM(g,t,ks,{fig:()=>{person(g,380,1700,520,{});person(g,700,1700,540,{})}})};
