// X10 · 5 reglas si alguien te habla en un servidor vacío (historia original)
window.CINE=1;window.BED='tape';window.GRADE='rgba(120,90,255,.07)';window.COVER_TEXT=['1/32','*JUGADORES*'];
window.DATE=()=>'AM 3:33';
function desk(g,t,ks,o={}){g.fillStyle='#05040a';g.fillRect(0,0,W,H);
  const mg=g.createRadialGradient(540,960,80,540,960,1100);mg.addColorStop(0,o.red?'rgba(255,60,80,.28)':'rgba(120,140,255,.28)');mg.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=mg;g.fillRect(0,0,W,H);
  g.fillStyle='#0e0d14';g.fillRect(0,1380,W,540);g.fillStyle='#14121c';rr(g,90,640,900,620,24);g.fill();
  g.save();rr(g,120,670,840,560,14);g.clip();(o.screen||lobby)(g,t,ks,o);g.fillStyle='rgba(0,0,0,.18)';for(let y=670;y<1230;y+=5)g.fillRect(120,y,840,2);g.restore();
  g.fillStyle='#14121c';g.fillRect(500,1260,80,120);g.fillRect(380,1370,320,20);
  // cascos con luz RGB
  g.save();g.translate(860,1460);g.strokeStyle=o.red?'#e0162b':'#6a5aff';g.lineWidth=18;g.shadowColor=o.red?'#f33':'#86f';g.shadowBlur=20;g.beginPath();g.arc(0,0,90,Math.PI,0);g.stroke();g.shadowBlur=0;g.fillStyle='#14121c';rr(g,-110,-20,50,90,20);g.fill();rr(g,60,-20,50,90,20);g.fill();g.restore();
  g.fillStyle='#1a1822';rr(g,180,1420,420,90,14);g.fill();if(o.fig){g.fillStyle='#000';g.beginPath();g.ellipse(160,520,60,74,0,0,7);g.fill();g.fillRect(90,580,140,800);g.fillStyle='rgba(240,240,230,.9)';g.fillRect(138,512,14,5);g.fillRect(170,512,14,5)}}
function lobby(g,t,ks,o){g.fillStyle='#0a0c18';g.fillRect(120,670,840,560);g.font='40px VT';g.fillStyle='#cfd8ff';g.fillText('SERVIDOR #4471 · MAPA: BOSQUE',150,720);
  const players=o.players||['TÚ'];g.fillText('JUGADORES: '+(o.count||'1/32'),150,780);players.forEach((p,i)=>{g.fillStyle=p==='TÚ'?'rgba(60,80,160,.6)':'rgba(160,20,30,.5)';g.fillRect(150,810+i*70,780,56);g.fillStyle='#e8ecff';g.fillText(p,180,850+i*70)});
  if(o.voice){const on=Math.floor(t*4)%2;g.fillStyle=on?'#3fd06b':'#1a4a2a';g.beginPath();g.arc(900,720,16,0,7);g.fill();g.fillStyle='#e9e2d2';g.font='30px VT';g.fillText('HABLANDO: ???',640,1200)}}
function gameView(g,t,ks,o){const s=g.createLinearGradient(0,670,0,1230);s.addColorStop(0,'#0a1018');s.addColorStop(1,'#04060a');g.fillStyle=s;g.fillRect(120,670,840,560);
  for(let i=0;i<14;i++){const x=120+hash(i*3)*840,h=200+hash(i*7)*300;g.fillStyle='#03050a';g.beginPath();g.moveTo(x,1230-h);g.lineTo(x+50,1230);g.lineTo(x-50,1230);g.fill()}
  const fz=clamp(ks/3);person(g,540,1230,lerp(120,420,fz),{eyes:'rgba(240,240,230,.9)'});g.font='30px VT';g.fillStyle='#e9e2d2';g.fillText('TÚ (?)',lerp(560,620,fz),lerp(1100,800,fz))}
function saveV(g,t,ks,o){g.fillStyle='#0a1030';g.fillRect(120,670,840,560);g.font='38px VT';g.fillStyle='#cfd8ff';g.fillText('CARGAR PARTIDA',150,730);
  [['PARTIDA 1','12 h'],['PARTIDA 2','31 h'],['PARTIDA 2','31 h + 6 h ???']].forEach(([a,b],i)=>{g.fillStyle=i===2?'rgba(224,22,43,.4)':'rgba(60,80,160,.5)';g.fillRect(150,770+i*120,780,96);g.fillStyle=i===2?'#ff8890':'#e8ecff';g.fillText(a+' · '+b,180,830+i*120)})}
const SC={lobby:(g,t,ks)=>desk(g,t,ks,{voice:ks>1.4}),r1:(g,t,ks)=>desk(g,t,ks,{voice:true}),r2:(g,t,ks)=>desk(g,t,ks,{voice:true,count:ks>2?'2/32':'1/32',players:ks>2?['TÚ','TÚ']:['TÚ']}),
 r3:(g,t,ks)=>desk(g,t,ks,{screen:gameView}),r4:(g,t,ks)=>desk(g,t,ks,{red:true,voice:true,fig:ks>1.2}),r5:(g,t,ks)=>desk(g,t,ks,{screen:saveV}),lobbyend:(g,t,ks)=>desk(g,t,ks,{voice:true,fig:true,red:true})};
