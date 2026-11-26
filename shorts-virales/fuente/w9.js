// W9 · Cómo sobrevivir a Slender: las 8 páginas
window.BED='forest';window.GRADE='rgba(120,140,170,.06)';window.COVER_TEXT=['NO','*LO MIRES*'];
window.DATE=()=>'JUN. 2012';
window.GLITCH=(t,L,k)=>({static:.35+.3*Math.sin(t*9),behind:.5,closer:.15}[L.scene]||0);
function slender(g,x,fy,h,t,a=1){const s=h/100;g.save();g.globalAlpha=a;g.translate(x+(hash(Math.floor(t*12))-.5)*s*.6,fy);g.scale(s,s);g.fillStyle='#030303';
  g.fillRect(-4,-48,3.4,48);g.fillRect(1,-48,3.4,48);g.beginPath();g.moveTo(-8,-86);g.lineTo(8,-86);g.lineTo(6,-46);g.lineTo(-6,-46);g.closePath();g.fill();
  g.fillStyle='#e8e4da';g.beginPath();g.moveTo(-2.5,-86);g.lineTo(2.5,-86);g.lineTo(0,-74);g.closePath();g.fill();g.fillStyle='#7a0e0e';g.fillRect(-.8,-84,1.6,8);
  g.fillStyle='#030303';g.fillRect(-11,-84,3,44);g.fillRect(8,-84,3,44);
  g.fillStyle='#e8e4da';g.beginPath();g.ellipse(0,-94,5.4,7.2,0,0,7);g.fill();g.restore()}
function page(g,x,y,rot,s,t){g.save();g.translate(x,y);g.rotate(rot);g.scale(s,s);g.fillStyle='#eae6da';g.fillRect(-60,-80,120,160);g.strokeStyle='#111';g.lineWidth=3;
  for(let i=0;i<5;i++){g.beginPath();g.moveTo(-40+hash(i)*20,-50+i*20);g.lineTo(30-hash(i*3)*20,-40+i*22);g.stroke()}g.beginPath();g.moveTo(-30,50);g.lineTo(-10,20);g.lineTo(10,60);g.lineTo(30,25);g.stroke();
  g.font='22px Anton';g.fillStyle='#111';g.textAlign='center';g.fillText('NO MIRES',0,-62);g.restore()}
function woods(g,t,ks,o={}){forest(g,t,{drift:.6,flash:o.flash??1,figure:o.fig?{layer:o.layer??2,draw:o.fig}:null});
  if(o.torch!==undefined){g.fillStyle=`rgba(0,0,0,${.5*(1-o.torch)})`;g.fillRect(0,0,W,H)}
  g.save();g.font='54px VT';g.fillStyle='#e9e2d2';g.textAlign='right';g.fillText('PÁGINAS '+(o.pages??0)+'/8',W-70,1460);g.restore()}
const SC={
 forest:(g,t,ks)=>woods(g,t,ks,{fig:()=>slender(g,760,1300,260,t,clamp((ks-1.6)*2)*.9)}),
 page:(g,t,ks)=>{woods(g,t,ks,{pages:1});page(g,540,1060,-.05,2.2+Math.sin(t)*.03,t)},
 static:(g,t,ks)=>{woods(g,t,ks,{pages:3,fig:()=>slender(g,560,1500,900,t)});noise(g,.25+.2*Math.sin(t*7),t)},
 closer:(g,t,ks)=>{const k=Math.floor(ks/1.2)%4;woods(g,t,ks,{pages:4+k,fig:()=>slender(g,[300,780,420,640][k],1380+k*60,320+k*170,t)})},
 torch:(g,t,ks)=>{const b=clamp(1-ks/4);woods(g,t,ks,{pages:6,torch:b});g.save();g.strokeStyle='#e9e2d2';g.lineWidth=6;g.strokeRect(120,1400,220,90);g.fillRect(340,1425,16,40);g.fillStyle=b>.3?'#3fd06b':'#e0162b';g.fillRect(132,1412,196*b,66);g.restore()},
 behind:(g,t,ks)=>{woods(g,t,ks,{pages:7,flash:0,torch:.2,layer:2,fig:()=>slender(g,540,2300,2600,t)});noise(g,.45,t)},
 forestend:(g,t,ks)=>{woods(g,t,ks,{pages:7,fig:()=>slender(g,860,1330,300,t,.9)});page(g,540,1100,.06,1.6,t)}};
