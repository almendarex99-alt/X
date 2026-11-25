// #10 Por qué el analog horror da tanto miedo
const DUR=50,COVER_T=44.65;
function COVER(g){big(g,'NO',470,260,1);big(g,'*MIRES*',720,260,1)}
cue(0,'bed',{kind:'tape',end:DUR});cue(0,'bars',{end:4.4});
[[0.2,'hit2'],[0.9,'hit2'],[2.6,'hit2'],[3.3,'hit'],[4.45,'glitch'],[4.7,'hit'],[7.3,'hit2'],[10.95,'glitch'],[11.1,'hit2'],[12.6,'hit'],
 [16.95,'glitch'],[17.1,'hit'],[22.95,'glitch'],[23.1,'hit'],[28.95,'glitch'],[29.1,'hit'],[34.95,'glitch'],[35.1,'hit2'],[37.4,'hit2'],
 [40.45,'glitch'],[40.6,'hit2'],[41.6,'hit'],[44.3,'stinger'],[46.45,'glitch'],[46.6,'hit']].forEach(([t,ty])=>cue(t,ty));
cue(32.7,'eas',{end:34.8});cue(42.4,'riser',{end:44.1});cue(44.1,'silence',{end:44.3});cue(23.3,'staticb',{end:28.8});cue(36,'heart',{end:42,bpm0:70,bpm1:120});
window.extraGlitch=t=>(t<4.4?.15+.25*(hash(Math.floor(t*6))>.7):0)+(t>44.3&&t<44.9?.6:0);

const TVB=mk(640,480),tx=TVB.getContext('2d');
function bars(g,w,h,t){const cols=['#c0c0c0','#c0c000','#00c0c0','#00c000','#c000c0','#c00000','#0000c0'];
  cols.forEach((c,i)=>{g.fillStyle=c;g.fillRect(i*w/7,0,w/7+1,h*.67)});
  ['#0000c0','#131313','#c000c0','#131313','#00c0c0','#131313','#c0c0c0'].forEach((c,i)=>{g.fillStyle=c;g.fillRect(i*w/7,h*.67,w/7+1,h*.08)});
  ['#00214c','#ffffff','#32006a','#131313','#090909','#131313','#1d1d1d'].forEach((c,i)=>{g.fillStyle=c;g.fillRect(i*w/7,h*.75,w/7+1,h*.25)})}
function tvContent(mode,t,k){const g=tx,w=640,h=480;g.save();g.fillStyle='#000';g.fillRect(0,0,w,h);
  if(mode==='bars')bars(g,w,h,t);
  else if(mode==='static'){g.drawImage(GRAIN[Math.floor(t*30)%6],0,0,w,h)}
  else if(mode==='station'){g.fillStyle='#14204a';g.fillRect(0,0,w,h);g.fillStyle='#e9e2d2';g.font='130px Anton';g.textAlign='center';g.fillText('58',w/2,280);g.font='34px VT';g.fillText('EMISIÓN NOCTURNA',w/2,340);g.fillText('476 MHz',w/2,380)}
  else if(mode==='weather'){g.fillStyle='#1a4aa8';g.fillRect(0,0,w,h);g.fillStyle='#f6d24a';g.beginPath();g.arc(180,220,70,0,7);g.fill();g.fillStyle='#000';g.beginPath();g.arc(160,205,8,0,7);g.arc(200,205,8,0,7);g.fill();
    g.strokeStyle='#000';g.lineWidth=6;g.beginPath();g.arc(180,225,32,.2,Math.PI-.2);g.stroke();g.fillStyle='#fff';g.font='54px Anton';g.fillText('EL TIEMPO',300,180);g.font='40px VT';g.fillText('MAÑANA: DESPEJADO',300,240);g.fillText('MÍN 4° · MÁX 13°',300,290);
    if(k>2.5){g.fillStyle='#000';g.beginPath();g.arc(160,205,9,0,7);g.arc(200,205,9,0,7);g.fill();g.fillStyle='#f6d24a';g.fillRect(140,235,80,20);g.strokeStyle='#000';g.beginPath();g.arc(180,255,32,Math.PI+.3,-.3);g.stroke()}}
  else if(mode==='face'){g.drawImage(GRAIN[Math.floor(t*30)%6],0,0,w,h);g.globalAlpha=.18+.1*Math.sin(t*2);g.fillStyle='#000';g.beginPath();g.ellipse(320,230,90,120,0,0,7);g.fill();
    g.fillStyle='#fff';g.beginPath();g.ellipse(290,210,12,6,0,0,7);g.ellipse(350,210,12,6,0,0,7);g.fill();g.fillStyle='#000';g.fillRect(270,280,100,8);g.globalAlpha=1}
  else if(mode==='alert'||mode==='window'){g.fillStyle='#000';g.fillRect(0,0,w,h);g.fillStyle='#e9e2d2';g.font='46px VT';g.textAlign='center';
    const L=mode==='alert'?['AVISO A LA POBLACIÓN','','NO MIRE POR LA VENTANA.','APAGUE LAS LUCES.','PERMANEZCA EN SILENCIO.']:['','NO MIRE','POR LA VENTANA.'];
    L.forEach((l,i)=>{if(k>i*.35)g.fillText(l,w/2,120+i*62)});if(mode==='alert'){g.fillStyle='#e0162b';g.fillRect(0,0,w,40);g.fillRect(0,h-40,w,40)}}
  g.restore()}
function tvRoom(g,t,mode,k,o={}){
  g.fillStyle='#060607';g.fillRect(0,0,W,H);
  // ventana a la izquierda
  g.fillStyle='#0d1420';g.fillRect(40,520,300,520);g.strokeStyle='#1a1a1a';g.lineWidth=18;g.strokeRect(40,520,300,520);g.beginPath();g.moveTo(190,520);g.lineTo(190,1040);g.moveTo(40,780);g.lineTo(340,780);g.stroke();
  if(o.figure){g.fillStyle='#000';g.beginPath();g.ellipse(250,700,46,58,0,0,7);g.fill();g.fillRect(190,750,120,290);g.fillStyle='rgba(235,228,210,.9)';g.beginPath();g.ellipse(236,696,7,3,0,0,7);g.ellipse(266,696,7,3,0,0,7);g.fill()}
  // mueble y televisor
  g.fillStyle='#120d09';g.fillRect(260,1500,760,420);
  g.fillStyle='#1c1814';rr(g,290,980,700,540,40);g.fill();g.fillStyle='#0c0a08';rr(g,330,1020,620,460,30);g.fill();
  tvContent(mode,t,k);g.save();rr(g,350,1040,580,420,40);g.clip();g.drawImage(TVB,350,1040,580,420);
  g.globalCompositeOperation='multiply';g.drawImage(SCAN,0,0);g.globalCompositeOperation='source-over';
  const gl=g.createRadialGradient(640,1250,60,640,1250,420);gl.addColorStop(0,'rgba(255,255,255,.08)');gl.addColorStop(1,'rgba(0,0,0,.45)');g.fillStyle=gl;g.fillRect(350,1040,580,420);g.restore();
  // luz del televisor sobre la habitación
  const rg=g.createRadialGradient(640,1250,100,640,1250,1000);rg.addColorStop(0,`rgba(150,170,210,${.16*flick(t,.5)})`);rg.addColorStop(1,'rgba(150,170,210,0)');g.globalCompositeOperation='lighter';g.fillStyle=rg;g.fillRect(0,0,W,H);g.globalCompositeOperation='source-over';
  g.fillStyle='#2a2520';g.beginPath();g.arc(960,1300,14,0,7);g.arc(960,1360,14,0,7);g.fill();
}
function tapes(g,t,k){g.fillStyle='#08070a';g.fillRect(0,0,W,H);
  [['GEMINI HOME ENT.','2019'],['THE MANDELA CATALOGUE','2021'],['LOCAL 58','2015']].forEach(([n,y],i)=>{const a=clamp((k-i*.6)/.4);if(a<=0)return;g.save();g.globalAlpha=a;
    g.translate(W/2,1500-i*170);g.rotate((i-1)*.03);g.fillStyle='#151515';g.fillRect(-380,-70,760,140);g.fillStyle='#ece6d6';g.fillRect(-300,-46,600,92);
    g.fillStyle='#1a1a1a';g.font='700 32px Inter';g.textAlign='left';g.fillText(n,-280,12);g.textAlign='right';g.fillStyle='#e0162b';g.font='44px VT';g.fillText(y,285,14);g.restore()})}
function scene(g,t,forLoop){
  let date='OCT. 2015';
  if(t<4.5){bars(g,W,H,t);g.fillStyle='rgba(0,0,0,.35)';g.fillRect(0,0,W,H);
    if(!forLoop){big(g,'UNA CINTA *NO PUEDE*',590,112,t-.2);big(g,'HACERTE DAÑO.',730,128,t-.9);big(g,'¿ENTONCES POR QUÉ',1300,100,t-2.6,{dx:-20});big(g,'NO PUEDES *DEJAR DE VERLA*?',1430,86,t-3.3,{dx:-20,maxW:840})}}
  else if(t<11){const k=t-4.5;tvRoom(g,t,k<1.5?'static':'station',k);
    big(g,'26 OCT. 2015.',510,140,k-.2);small(g,'Kris Straub sube «Local 58» a YouTube.',670,k-1,{size:42,weight:700});big(g,'UN CANAL DE TV *FALSO*.',830,100,k-2.8)}
  else if(t<17){const k=t-11;tvRoom(g,t,'station',k);g.fillStyle='rgba(0,0,0,.45)';g.fillRect(0,0,W,H);
    big(g,'SU LEMA LE DIO NOMBRE',510,100,k-.1);big(g,'AL GÉNERO:',640,110,k-.6);
    g.save();g.font='92px VT';g.textAlign='center';g.fillStyle='#7dffef';g.shadowColor='#7dffef';g.shadowBlur=24*flick(t,.4);g.globalAlpha=clamp((k-1.6)*3);g.fillText('ANALOG HORROR',W/2,850);g.fillText('AT 476 MHz',W/2,940);g.restore()}
  else if(t<23){const k=t-17;tvRoom(g,t,'weather',k);big(g,'1. FORMATOS',510,120,k-.1);big(g,'EN LOS QUE *CONFÍAS*.',650,110,k-.5);small(g,'Noticias, el tiempo, anuncios, tutoriales.',830,k-1.4,{size:42})}
  else if(t<29){const k=t-23;tvRoom(g,t,'face',k);big(g,'2. LA MALA CALIDAD',510,112,k-.1);big(g,'*ESCONDE* COSAS.',650,118,k-.5);small(g,'Tu cerebro rellena lo que falta.',830,k-1.8,{size:44,weight:700})}
  else if(t<35){const k=t-29;tvRoom(g,t,'alert',k);big(g,'3. TE HABLA',510,130,k-.1);big(g,'*A TI*.',670,170,k-.5);small(g,'Con calma. Con instrucciones.',870,k-1.6,{size:44,weight:700})}
  else if(t<40.5){const k=t-35;date='2019 · 2021';tapes(g,t,k);big(g,'DESPUÉS LLEGARON',510,112,k-.1);big(g,'*MILES* DE CINTAS.',650,112,k-2.6)}
  else if(t<46.5){const k=t-40.5;date='HOY';const fig=t>=44.3;tvRoom(g,t,'window',k-1.2,{figure:fig});
    if(!fig){big(g,'Y ESTE VIDEO…',510,130,k-.1);big(g,'TAMBIÉN ES UNA *CINTA*.',660,110,k-1.1)}
    else if(t-44.3<.1){g.fillStyle=`rgba(255,255,255,${.5*(1-(t-44.3)/.1)})`;g.fillRect(0,0,W,H)}}
  else{const k=t-46.5;date='HOY';tvRoom(g,t,'static',k,{figure:true});g.fillStyle='rgba(0,0,0,.45)';g.fillRect(0,0,W,H);
    big(g,'¿CUÁL TE DIO',530,140,k-.1);big(g,'*MÁS MIEDO*?',690,150,k-.4);small(g,'Comenta LOCAL 58, GEMINI o MANDELA.',890,k-1.1,{size:42,weight:700})}
  return date;
}
