// #7 Mitos de terror de GTA San Andreas
const DUR=48,COVER_T=40.95;
function COVER(g){big(g,'NUNCA',520,250,1);big(g,'*ESTUVO*',760,250,1)}
// ---------- cues de sonido ----------
cue(0,'bed',{kind:'forest',end:DUR});
[[0.15,'hit2'],[0.9,'hit2'],[2.4,'hit'],[1.8,'flash'],[4.15,'glitch'],[4.4,'hit'],[9.45,'glitch'],[9.6,'hit2'],[13.6,'stampfx'],[14.0,'hit2'],
 [17.45,'glitch'],[17.6,'hit2'],[21.6,'stampfx'],[22.0,'hit2'],[24.45,'glitch'],[24.6,'hit2'],[28.6,'stampfx'],[29.0,'hit'],
 [34.45,'glitch'],[34.6,'hit2'],[37.6,'hit'],[40.8,'stinger'],[42.45,'glitch'],[42.6,'hit']].forEach(([t,ty])=>cue(t,ty));
cue(17.8,'chainsaw',{end:23.9});cue(25.0,'roll',{end:34.0});cue(38.4,'riser',{end:40.6});cue(40.6,'silence',{end:40.8});
cue(10.6,'shutter');cue(13.0,'heart',{end:17.3,bpm0:60,bpm1:95});

// ---------- bosque nocturno ----------
const TREES=[
 [...Array(13)].map((_,i)=>({x:i/13*1.6-.3+hash(i)*.05,h:.26+hash(i*1.7)*.14})),
 [...Array(8)].map((_,i)=>({x:i/8*1.6-.3+hash(i+9)*.08,h:.36+hash(i*2.3)*.14})),
 [{x:-.06,h:.95},{x:.06,h:.8},{x:.9,h:.9},{x:1.04,h:1},{x:1.5,h:.9}]];
function bigfoot(g,x,fy,h,a,t,walk=1){
  g.save();g.globalAlpha=a;const s=h/100,st=Math.sin(t*4)*walk;g.translate(x,fy);g.scale(s,s);
  const bl=g.createRadialGradient(0,-70,5,0,-70,75);bl.addColorStop(0,'rgba(170,190,200,.55)');bl.addColorStop(1,'rgba(170,190,200,0)');g.fillStyle=bl;g.fillRect(-80,-150,160,150);g.fillStyle='#0b0908';g.strokeStyle='#0b0908';g.lineCap='round';
  g.lineWidth=11;g.beginPath();g.moveTo(-4,-46);g.lineTo(-7-st*6,-2);g.moveTo(5,-46);g.lineTo(8+st*6,-2);g.stroke();            // piernas
  g.beginPath();g.ellipse(0,-64,19,26,.12,0,7);g.fill();                                                                   // torso encorvado
  g.beginPath();g.ellipse(6,-88,9,10,0,0,7);g.fill();g.beginPath();g.ellipse(3,-80,15,8,0,0,7);g.fill();                   // cabeza y hombros
  g.lineWidth=8;g.beginPath();g.moveTo(-12,-76);g.quadraticCurveTo(-22,-52,-16+st*5,-30);g.moveTo(14,-76);g.quadraticCurveTo(24,-55,20-st*5,-32);g.stroke(); // brazos largos
  g.fillStyle='rgba(255,190,120,.85)';g.beginPath();g.arc(10,-89,1.3,0,7);g.fill();                                       // brillo de un ojo
  g.restore();
}
function forest(g,t,o={}){
  const sky=g.createLinearGradient(0,0,0,H);sky.addColorStop(0,'#04070b');sky.addColorStop(.35,'#1a2730');sky.addColorStop(.6,'#3a4a52');sky.addColorStop(.85,'#1a2329');sky.addColorStop(1,'#07090b');g.fillStyle=sky;g.fillRect(0,0,W,H);
  g.fillStyle='rgba(220,230,235,.9)';for(let i=0;i<60;i++){const x=hash(i*9.1)*W,y=hash(i*4.3)*H*.45;g.fillRect(x,y,2,2)}
  const mx=800,my=330,mg=g.createRadialGradient(mx,my,40,mx,my,380);mg.addColorStop(0,'rgba(210,225,230,.35)');mg.addColorStop(1,'rgba(210,225,230,0)');g.fillStyle=mg;g.fillRect(0,0,W,H);
  g.fillStyle='#d8e2e4';g.beginPath();g.arc(mx,my,62,0,7);g.fill();
  const drift=(o.drift??1)*t;
  TREES.forEach((layer,l)=>{const col=['#24333b','#111c22','#030506'][l],y0=[1250,1420,1700][l],sp=[8,18,40][l],sc=1;
    if(o.figure&&o.figure.layer===l)o.figure.draw();
    g.fillStyle=col;
    layer.forEach(tr=>{let x=((tr.x*W-drift*sp)%(W*1.6)+W*1.6)%(W*1.6)-W*.3;const h=tr.h*H*sc,bw=h*.2;
      g.fillRect(x-bw*.06,y0-h*.25,bw*.12,h*.25+H);
      for(let k=0;k<6;k++){const ty=y0-h+k*h*.13,tw=bw*(.35+k*.13);g.beginPath();g.moveTo(x,ty-h*.06);g.lineTo(x+tw,ty+h*.16);g.lineTo(x-tw,ty+h*.16);g.closePath();g.fill()}});
    if(l<2){g.globalAlpha=.22;g.drawImage(FOG,-((t*12*(l+1))%540),y0-900,W*1.6,900);g.globalAlpha=1}});
  g.fillStyle='#020303';g.fillRect(0,1640,W,H);
  if(o.prints){for(let i=0;i<7;i++){const z=i/7,x=W/2+Math.sin(i*1.3)*60*(1-z)+(i%2?30:-30)*(1-z*.7),y=1820-i*60;g.fillStyle=`rgba(80,70,55,${.8-z*.6})`;
    g.beginPath();g.ellipse(x,y,26*(1-z*.6),12*(1-z*.6),0,0,7);g.fill()}}
  if(o.flash){const fx=W/2+Math.sin(t*1.1)*330,fy=1050+Math.sin(t*.7)*120,lg=g.createRadialGradient(fx,fy,10,fx,fy,420);
    lg.addColorStop(0,'rgba(255,240,200,.32)');lg.addColorStop(1,'rgba(255,240,200,0)');g.globalCompositeOperation='lighter';g.fillStyle=lg;g.fillRect(0,0,W,H);g.globalCompositeOperation='source-over'}
}
// ---------- polaroid borrosa ----------
const PH=mk(270,300),phx=PH.getContext('2d');
function polaroid(g,x,y,rot,age,label){
  if(age<0)return;const k=clamp(age/.35);g.save();g.translate(x,y+(1-ease(k))*300);g.rotate(rot);g.globalAlpha=k;
  phx.setTransform(.25,0,0,.25,0,0);forest(phx,12,{drift:0,figure:{layer:2,draw:()=>bigfoot(phx,560,1420,820,1,0,0)}});phx.setTransform(1,0,0,1,0,0);
  phx.globalCompositeOperation='screen';phx.fillStyle='rgba(60,62,52,.35)';phx.fillRect(0,0,270,300);const fg=phx.createRadialGradient(135,160,10,135,160,170);fg.addColorStop(0,'rgba(255,250,220,.35)');fg.addColorStop(1,'rgba(255,250,220,0)');phx.fillStyle=fg;phx.fillRect(0,0,270,300);phx.globalCompositeOperation='source-over';
  g.fillStyle='#ece6d8';g.shadowColor='rgba(0,0,0,.6)';g.shadowBlur=30;g.fillRect(-300,-330,600,720);g.shadowBlur=0;
  g.imageSmoothingEnabled=true;g.drawImage(PH,0,0,270,300,-260,-290,520,560);
  g.fillStyle='#2a2a2a';g.font='italic 700 44px Inter';g.textAlign='center';g.fillText(label,0,345);g.restore();
}
// ---------- granero ----------
function barn(g,t,k){
  const sky=g.createLinearGradient(0,0,0,H);sky.addColorStop(0,'#05070c');sky.addColorStop(1,'#151612');g.fillStyle=sky;g.fillRect(0,0,W,H);
  g.fillStyle='#0d0d0a';g.fillRect(0,1450,W,H);
  g.fillStyle='#2a1310';g.beginPath();g.moveTo(140,1460);g.lineTo(140,900);g.lineTo(540,640);g.lineTo(940,900);g.lineTo(940,1460);g.closePath();g.fill();
  g.strokeStyle='#160806';g.lineWidth=6;for(let x=170;x<940;x+=46){g.beginPath();g.moveTo(x,Math.max(900-(x<540?(x-140)*.65:(940-x)*.65),640));g.lineTo(x,1460);g.stroke()}
  const fl=flick(t,.8);const dl=g.createLinearGradient(0,1040,0,1460);dl.addColorStop(0,`rgba(255,170,80,${.55*fl})`);dl.addColorStop(1,`rgba(255,120,40,${.8*fl})`);
  g.fillStyle=dl;g.fillRect(410,1040,260,420);
  const pg=g.createRadialGradient(540,1460,10,540,1460,520);pg.addColorStop(0,`rgba(255,150,60,${.35*fl})`);pg.addColorStop(1,'rgba(255,150,60,0)');g.fillStyle=pg;g.fillRect(0,1100,W,820);
  // silueta con motosierra en la puerta
  const sh=(hash(Math.floor(t*30))-.5)*3;g.save();g.translate(540+sh,1460);g.fillStyle='#050302';g.strokeStyle='#050302';g.lineCap='round';
  g.lineWidth=26;g.beginPath();g.moveTo(-18,-150);g.lineTo(-30,0);g.moveTo(18,-150);g.lineTo(30,0);g.stroke();
  g.beginPath();g.moveTo(-50,-300);g.lineTo(50,-300);g.lineTo(40,-140);g.lineTo(-40,-140);g.closePath();g.fill();
  g.beginPath();g.ellipse(0,-335,30,36,0,0,7);g.fill();
  g.lineWidth=20;g.beginPath();g.moveTo(-45,-285);g.lineTo(-30,-200);g.lineTo(40,-215);g.moveTo(45,-285);g.lineTo(60,-225);g.stroke();
  g.fillRect(30,-245,70,46);g.fillRect(95,-232,150,20);  // motosierra
  g.restore();
}
// ---------- colina y coche fantasma ----------
function hillRoad(g,t,k){
  const sky=g.createLinearGradient(0,0,0,H);sky.addColorStop(0,'#04060c');sky.addColorStop(1,'#141a20');g.fillStyle=sky;g.fillRect(0,0,W,H);
  g.fillStyle='#d8e2e4';g.beginPath();g.arc(830,380,55,0,7);g.fill();
  const ang=.42,x0=-100,y0=760,len=1500;const pt=s=>[x0+Math.cos(ang)*s,y0+Math.sin(ang)*s];
  g.fillStyle='#0a0c0b';g.beginPath();g.moveTo(...pt(-200));g.lineTo(...pt(len+200));g.lineTo(W+400,H);g.lineTo(-300,H);g.closePath();g.fill();
  g.strokeStyle='#2c2f2a';g.lineWidth=18;g.beginPath();g.moveTo(...pt(-200));g.lineTo(...pt(len+200));g.stroke();
  g.strokeStyle='rgba(220,200,120,.5)';g.lineWidth=4;g.setLineDash([40,40]);g.lineDashOffset=0;g.beginPath();g.moveTo(...pt(-200).map((v,i)=>v+(i?14:0)));g.lineTo(...pt(len+200).map((v,i)=>v+(i?14:0)));g.stroke();g.setLineDash([]);
  // postes
  for(let s=0;s<len;s+=330){const [px,py]=pt(s);g.strokeStyle='#121410';g.lineWidth=8;g.beginPath();g.moveTo(px,py-6);g.lineTo(px,py-260);g.stroke()}
  // coche
  const s=lerp(-150,len-250,k),[cx,cy]=pt(s);const lg=g.createRadialGradient(cx,cy-80,10,cx,cy-80,380);lg.addColorStop(0,'rgba(190,205,215,.28)');lg.addColorStop(1,'rgba(190,205,215,0)');g.fillStyle=lg;g.fillRect(cx-400,cy-460,800,800);g.save();g.translate(cx,cy-8);g.rotate(ang);g.scale(1.55,1.55);
  g.fillStyle='#5a625c';rr(g,-150,-80,300,62,16);g.fill();g.beginPath();g.moveTo(-90,-80);g.lineTo(-55,-130);g.lineTo(60,-130);g.lineTo(100,-80);g.closePath();g.fill();
  g.fillStyle='rgba(150,170,175,.55)';g.beginPath();g.moveTo(-78,-84);g.lineTo(-50,-122);g.lineTo(0,-122);g.lineTo(0,-84);g.closePath();g.fill();g.beginPath();g.moveTo(8,-84);g.lineTo(8,-122);g.lineTo(55,-122);g.lineTo(88,-84);g.closePath();g.fill();
  g.fillStyle='rgba(30,35,36,.8)';g.fillRect(-40,-104,16,22);   // asiento vacío
  const wr=t*6;[-95,95].forEach(wx=>{g.fillStyle='#070707';g.beginPath();g.arc(wx,-14,30,0,7);g.fill();g.strokeStyle='#555';g.lineWidth=4;g.beginPath();g.moveTo(wx+Math.cos(wr)*18,-14+Math.sin(wr)*18);g.lineTo(wx-Math.cos(wr)*18,-14-Math.sin(wr)*18);g.stroke()});
  g.fillStyle='#ffe9a8';g.fillRect(140,-70,12,14);g.restore();
}
function scene(g,t,forLoop){
  let date='OCT. 2004';
  if(t<4.2){const fig=t>1.8&&t<2.25;forest(g,t,{flash:1,figure:{layer:1,draw:()=>fig&&bigfoot(g,700,1330,430,.95,t)}});
    if(!forLoop){big(g,'MILLONES LO BUSCAMOS',560,104,t-.15);big(g,'EN *SAN ANDREAS*.',700,112,t-.9);big(g,'NUNCA ESTUVO AHÍ.',920,138,t-2.4)}}
  else if(t<9.5){const k=t-4.2;forest(g,t,{drift:2});g.fillStyle='rgba(0,0,0,.55)';g.fillRect(0,0,W,H);
    big(g,'OCTUBRE 2004',640,150,k-.2);g.save();g.font='62px VT';g.textAlign='center';g.fillStyle='#e0162b';g.globalAlpha=clamp((k-.7)*3);g.fillText('GRAND THEFT AUTO: SAN ANDREAS',W/2,760);g.restore();
    small(g,'Un mapa enorme, bosques, montañas… y rumores.',960,k-1.4,{size:44,weight:700})}
  else if(t<17.5){const k=t-9.5;forest(g,t,{drift:.6});g.fillStyle='rgba(0,0,0,.35)';g.fillRect(0,0,W,H);
    big(g,'MITO 1: *BIGFOOT*',500,128,k-.1);polaroid(g,W/2-10,1060,-.06,k-1.0,'¿¿real??');
    if(k>4.1){stamp(g,'FALSO',W/2,1120,k-4.1)}
    if(k>4.5){big(g,'ROCKSTAR LO NEGÓ EN *2005*.',1520,84,k-4.5,{dx:-20,maxW:840})}}
  else if(t<24.5){const k=t-17.5;barn(g,t,k);
    big(g,'MITO 2: EL HOMBRE',470,110,k-.1);big(g,'DE LA *MOTOSIERRA*',600,110,k-.4);small(g,'Un asesino escondido en el campo, como en la película.',760,k-1.4,{size:40});
    if(k>4.1){stamp(g,'FALSO',W/2,1000,k-4.1)}if(k>4.5)big(g,'SOLO ERAN FOTOS *TRUCADAS*.',1660,80,k-4.5,{dx:-20,maxW:820})}
  else if(t<34.5){const k=t-24.5;hillRoad(g,t,ease(clamp((k-.5)/9)));
    big(g,'MITO 3: COCHES',470,116,k-.1);big(g,'*SIN CONDUCTOR*',600,116,k-.4);
    if(k>4.1)stamp(g,'REAL',W/2,1240,k-4.1,'#f2d24a',.12);if(k>4.5)big(g,'ESTE ERA *REAL*.',1440,110,k-4.5,{dx:-20});
    small(g,'Aparecían en cuestas empinadas y rodaban solos: un fallo, no un fantasma.',1600,k-6,{size:36,dx:-20,maxW:800})}
  else if(t<42.5){const k=t-34.5;date='2013';
    const close=t>=40.8;forest(g,t,{prints:!close,figure:{layer:close?2:1,draw:()=>close?bigfoot(g,560,1980,1500,1,t,.2):bigfoot(g,300+k*18,1400,330,clamp((k-2.5)*.6)*.95,t)}});
    if(!close){big(g,'AÑOS DESPUÉS…',520,110,k-.1);big(g,'ROCKSTAR SE RIÓ DEL MITO.',660,96,k-1.1);big(g,'EN *GTA V* SÍ PUEDES',840,112,k-3.1);big(g,'ENCONTRARLO.',970,130,k-3.4)}
    else{if(t-40.8<.1){g.fillStyle=`rgba(255,255,255,${.6*(1-(t-40.8)/.1)})`;g.fillRect(0,0,W,H)}}}
  else{const k=t-42.5;forest(g,t,{flash:1});g.fillStyle='rgba(0,0,0,.4)';g.fillRect(0,0,W,H);
    big(g,'¿TÚ TAMBIÉN',600,140,k-.1);big(g,'LO *BUSCASTE*?',760,140,k-.4);small(g,'Comenta BIGFOOT si pasaste noches en ese bosque.',1000,k-1.5,{size:42,weight:700})}
  return date;
}
