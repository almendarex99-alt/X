// #9 Eternal Darkness: el juego que te mentía (y Nintendo lo patentó)
const DUR=50,COVER_T=3.4;
function COVER(g){big(g,'PARTIDA',560,230,1);big(g,'*BORRADA*',800,230,1)}
cue(0,'bed',{kind:'drone',end:DUR});
[[0.2,'hit2'],[0.7,'hit'],[2.6,'glitch'],[2.8,'hit'],[4.45,'glitch'],[4.7,'hit'],[10.45,'glitch'],[10.6,'hit2'],[12.2,'hit'],
 [15.95,'glitch'],[16.1,'hit2'],[19.45,'glitch'],[19.6,'hit2'],[22.95,'glitch'],[23.1,'hit2'],[26.45,'glitch'],[26.6,'hit2'],
 [29.95,'glitch'],[30.1,'hit2'],[38.0,'stampfx'],[38.4,'hit'],[42.5,'glitch'],[42.5,'stinger'],[44.6,'hit2'],[46.45,'glitch'],[46.6,'hit']].forEach(([t,ty])=>cue(t,ty));
cue(0.3,'deleting',{end:2.6});cue(26.7,'deleting',{end:29.6});cue(16.3,'volume',{end:19.2});cue(19.7,'unplug');cue(23.1,'crawl',{end:26.4});cue(11,'heart',{end:15.8,bpm0:60,bpm1:120});
window.extraGlitch=t=>(t>42.5&&t<43.1)?.8:0;

const uiBg=g=>{const b=g.createLinearGradient(0,0,0,H);b.addColorStop(0,'#0b1430');b.addColorStop(1,'#04060f');g.fillStyle=b;g.fillRect(0,0,W,H)};
function saveScreen(g,t,k,done){
  uiBg(g);g.save();g.translate(0,150);g.font='700 46px Inter';g.fillStyle='#cfd8ff';g.textAlign='left';g.fillText('DATOS GUARDADOS',110,720);
  g.fillStyle='rgba(160,180,255,.25)';g.fillRect(110,745,860,3);
  ['PARTIDA 1   ·   Capítulo 7   ·   12:44','PARTIDA 2   ·   Capítulo 3   ·   04:10','PARTIDA 3   ·   Capítulo 11  ·   21:37'].forEach((s,i)=>{
    const gone=done||(k>(i+1)*.3);g.fillStyle=gone?'rgba(30,40,70,.5)':'rgba(40,60,120,.55)';g.fillRect(110,790+i*120,860,96);
    g.font='500 36px Inter';g.fillStyle=gone?'rgba(150,160,190,.35)':'#e8ecff';g.fillText(gone?'— VACÍO —':s,150,850+i*120)});
  g.fillStyle='rgba(10,14,30,.95)';g.fillRect(160,1180,760,260);g.strokeStyle='#8aa0ff';g.lineWidth=3;g.strokeRect(160,1180,760,260);
  g.font='700 40px Inter';g.fillStyle='#fff';g.textAlign='center';g.fillText(done?'TODOS LOS DATOS BORRADOS':'BORRANDO…',540,1260);
  g.fillStyle='#1b2550';g.fillRect(220,1320,640,40);g.fillStyle=done?'#e0162b':'#6f8cff';g.fillRect(220,1320,640*(done?1:clamp(k)),40);
  g.font='500 34px Inter';g.fillStyle='#cfd8ff';g.fillText(done?'100%':Math.floor(clamp(k)*100)+'%',540,1410);g.restore();
}
function sanityBar(g,v,t){g.save();const x=140,y=1250,w=800,h=56;g.fillStyle='rgba(0,0,0,.6)';g.fillRect(x-10,y-70,w+20,h+90);
  g.font='60px VT';g.fillStyle='#bfe6c4';g.fillText('CORDURA',x,y-14);
  g.fillStyle='#132018';g.fillRect(x,y,w,h);const c=v>.5?'#3fd06b':v>.25?'#e2c442':'#e0162b';g.fillStyle=c;g.shadowColor=c;g.shadowBlur=20;g.fillRect(x,y,w*v,h);g.restore()}
function volumeOSD(g,k){g.save();const n=Math.max(0,Math.round(20*(1-k)));g.font='72px VT';g.fillStyle='#4dff7a';g.shadowColor='#4dff7a';g.shadowBlur=12;
  g.fillText(n?'VOLUMEN':'SILENCIO',120,1260);for(let i=0;i<20;i++){g.globalAlpha=i<n?1:.15;g.fillRect(120+i*42,1290,30,70)}g.restore()}
function padMsg(g,t){g.save();g.fillStyle='rgba(0,0,0,.85)';g.fillRect(90,1140,900,260);g.strokeStyle='#e9e2d2';g.lineWidth=3;g.strokeRect(90,1140,900,260);
  g.font='700 46px Inter';g.fillStyle='#fff';g.textAlign='center';g.fillText('MANDO DESCONECTADO',540,1235);g.font='500 34px Inter';g.fillStyle='#c9c3b8';g.fillText('Vuelve a conectar el mando al puerto 1',540,1300);
  g.fillText(Math.floor(t*2)%2?'Pulsa START para continuar':'',540,1360);g.restore()}
const BUGS=[...Array(26)].map((_,i)=>({x:hash(i*3.7)*W,y:hash(i*5.1)*H,a:hash(i*9.3)*6.28,v:60+hash(i)*120,s:.7+hash(i*2.2)*.9}));
function bugs(g,t,k){g.save();BUGS.forEach((b,i)=>{const n=Math.floor(BUGS.length*clamp(k*1.6));if(i>=n)return;const a=b.a+Math.sin(t*2+i)*.6,x=(b.x+Math.cos(a)*b.v*t)%W,y=(b.y+Math.sin(a)*b.v*t+H)%H;
  g.save();g.translate((x+W)%W,y);g.rotate(a+Math.PI/2);g.scale(b.s*3.2,b.s*3.2);g.fillStyle='#0a0705';g.beginPath();g.ellipse(0,0,6,10,0,0,7);g.fill();g.beginPath();g.arc(0,-11,4,0,7);g.fill();
  g.strokeStyle='#0a0705';g.lineWidth=1.6;for(let l=-1;l<=1;l++){const w=Math.sin(t*25+l+i)*2;g.beginPath();g.moveTo(-5,l*5);g.lineTo(-12,l*6+w);g.moveTo(5,l*5);g.lineTo(12,l*6-w);g.stroke()}g.restore()});g.restore()}
function patentDoc(g,t,k){g.save();const a=clamp(k/.4);g.globalAlpha=a;g.translate(W/2,1150+(1-ease(a))*200);g.rotate(-.03);
  g.fillStyle='#ece6d6';g.shadowColor='rgba(0,0,0,.6)';g.shadowBlur=30;g.fillRect(-400,-480,800,960);g.shadowBlur=0;
  g.fillStyle='#1c1c1c';g.font='700 34px Inter';g.textAlign='left';g.fillText('United States Patent',-350,-400);g.textAlign='right';g.fillText('US 6,935,954 B2',350,-400);
  g.fillRect(-350,-380,700,3);g.textAlign='left';g.font='700 44px Inter';g.fillText('Sanity system for video game',-350,-310);
  g.font='500 28px Inter';g.fillText('Assignee: Nintendo of America Inc.',-350,-250);g.fillText('Filed: Dec. 14, 2000',-350,-210);g.fillText('Granted: Aug. 30, 2005',-350,-170);
  g.fillStyle='rgba(30,30,30,.55)';for(let i=0;i<12;i++)g.fillRect(-350,-110+i*36,i%4==3?420:700,12);
  g.strokeStyle='#1c1c1c';g.lineWidth=3;g.strokeRect(-350,330,300,110);g.beginPath();g.moveTo(-50,385);g.lineTo(60,385);g.stroke();g.strokeRect(60,330,290,110);
  g.restore()}
function scene(g,t,forLoop){
  let date='JUN. 2002';
  if(t<4.5){date='HOY';const done=t>=2.6;saveScreen(g,t,t/2.5,done);
    if(!forLoop){big(g,'ESTE JUEGO',500,140,t-.2);big(g,'TE *MINTIÓ*.',670,170,t-.7);if(done)big(g,'Y NINTENDO LO *PATENTÓ*.',1740,90,t-2.8,{dx:-20,maxW:840})}}
  else if(t<10.5){const k=t-4.5;hall(g,{t,cam:{x:0,y:0,z:.5+k*.1},red:.2,dark:.25,flick:flick(t)});g.fillStyle='rgba(0,0,0,.45)';g.fillRect(0,0,W,H);
    big(g,'2002 · GAMECUBE',560,128,k-.2);g.save();g.font='96px VT';g.textAlign='center';g.fillStyle='#e0162b';g.globalAlpha=clamp((k-.8)*3);g.fillText('ETERNAL DARKNESS',W/2,690);g.restore();
    small(g,'Un juego de terror con una barra de cordura.',900,k-1.8,{size:44,weight:700})}
  else if(t<16){const k=t-10.5;hall(g,{t,cam:{x:0,y:0,z:1.2},red:.2+k*.06,dark:.3,flick:flick(t)});sanityBar(g,clamp(1-k/5),t);
    big(g,'CUANTO MÁS BAJA…',480,120,k-.1);big(g,'MÁS TE MENTÍA',630,120,k-1.6);big(g,'*A TI*.',800,190,k-2.6)}
  else if(t<30){const k=t-16,i=Math.floor(k/3.5),kk=k-i*3.5;hall(g,{t,cam:{x:0,y:0,z:1.6},red:.35,dark:.35,flick:flick(t)});
    if(i===0){volumeOSD(g,clamp(kk/2.6));big(g,'FINGÍA BAJAR',480,120,kk-.1);big(g,'EL *VOLUMEN* DE TU TELE.',620,100,kk-.5)}
    if(i===1){padMsg(g,t);big(g,'TE DECÍA QUE EL MANDO',480,100,kk-.1);big(g,'SE HABÍA *DESCONECTADO*.',610,100,kk-.5)}
    if(i===2){bugs(g,t,kk/2);big(g,'LLENABA LA PANTALLA',480,110,kk-.1);big(g,'DE *INSECTOS*.',620,130,kk-.5)}
    if(i>=3){saveScreen(g,t,kk/2.8,kk>2.9);big(g,'Y FINGÍA BORRAR',500,110,kk-.1);big(g,'TU *PARTIDA*.',650,130,kk-.5)}}
  else if(t<42.5){const k=t-30;date='AGO. 2005';hall(g,{t,cam:{x:0,y:0,z:1},dark:.55,flick:flick(t,.5)});g.fillStyle='rgba(0,0,0,.45)';g.fillRect(0,0,W,H);
    big(g,'NINTENDO LO *PATENTÓ*:',440,112,k-.1);patentDoc(g,t,k-.6);
    if(k>=8){date='HOY';stamp(g,'EXPIRADA',W/2,1200,k-8);big(g,'HOY ESA PATENTE YA *EXPIRÓ*.',1760,80,k-8.4,{dx:-20,maxW:820})}}
  else if(t<46.5){const k=t-42.5;date='HOY';g.fillStyle='#000';g.fillRect(0,0,W,H);noise(g,.5*clamp(1-k/1.2),t);
    if(k<1.8){g.save();g.font='700 50px Inter';g.textAlign='center';g.fillStyle='#e9e2d2';g.fillText('ERROR DE REPRODUCCIÓN',W/2,900);g.font='500 34px Inter';g.fillStyle='#9a958c';g.fillText('Este video está dañado (código 0x0F)',W/2,970);g.restore()}
    else{big(g,'TRANQUILO.',800,150,k-1.9);big(g,'ERA UNA *BROMA*…',960,120,k-2.2);small(g,'…como las del juego.',1120,k-2.9,{size:46,weight:700})}}
  else{const k=t-46.5;hall(g,{t,cam:{x:0,y:0,z:.3},red:.15,dark:.3,flick:flick(t)});g.fillStyle='rgba(0,0,0,.45)';g.fillRect(0,0,W,H);
    big(g,'¿TE HABRÍA',560,150,k-.1);big(g,'*ENGAÑADO*?',730,150,k-.4);small(g,'Comenta CORDURA si lo jugaste.',960,k-1.2,{size:44,weight:700})}
  return date;
}
