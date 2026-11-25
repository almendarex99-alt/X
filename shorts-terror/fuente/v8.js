// #8 Polybius: el arcade que nadie ha encontrado
const DUR=48,COVER_T=45.9;
function COVER(g){big(g,'NO INSERTES',470,190,1);big(g,'*MONEDA*',680,230,1)}
cue(0,'bed',{kind:'arcade',end:DUR});
[[0.15,'hit2'],[0.7,'hit2'],[2.3,'hit'],[4.15,'glitch'],[4.4,'hit'],[7.6,'hit2'],[9.95,'glitch'],[10.2,'hit2'],[11.4,'hit'],
 [15.95,'glitch'],[16.1,'hit2'],[17.4,'hit2'],[19.2,'hit'],[23.95,'glitch'],[24.1,'hit2'],[25.2,'hit2'],[27.3,'stampfx'],[28.4,'hit2'],
 [32.95,'glitch'],[33.1,'hit2'],[35.0,'hit'],[40.95,'glitch'],[41.1,'hit'],[45.5,'stinger'],[45.5,'glitch']].forEach(([t,ty])=>cue(t,ty));
cue(41.6,'coin');cue(43.2,'riser',{end:45.3});cue(45.3,'silence',{end:45.5});cue(19,'heart',{end:23.8,bpm0:65,bpm1:110});
window.extraGlitch=t=>(t>45.5&&t<46.2)?.5:0;

function tunnel(g,cx,cy,r,t,hue=0){
  g.save();g.translate(cx,cy);g.lineWidth=3;g.globalCompositeOperation='lighter';
  const n=7,rot=t*.7;for(let i=0;i<9;i++){const z=((i/9+t*.18)%1),rr2=r*Math.pow(z,1.6);g.strokeStyle=`hsla(${(180+hue+i*22)%360},100%,60%,${.25+z*.75})`;
    g.beginPath();for(let k=0;k<=n;k++){const a=rot*(1-z)+k/n*6.283;const x=Math.cos(a)*rr2,y=Math.sin(a)*rr2*.8;k?g.lineTo(x,y):g.moveTo(x,y)}g.stroke()}
  g.strokeStyle='rgba(255,60,200,.6)';for(let k=0;k<n;k++){const a=rot+k/n*6.283;g.beginPath();g.moveTo(0,0);g.lineTo(Math.cos(a)*r,Math.sin(a)*r*.8);g.stroke()}
  g.restore();
}
function cabinet(g,x,y,s,t,o={}){
  g.save();g.translate(x,y);g.scale(s,s);
  const scr=o.screen??1;
  // cuerpo
  g.fillStyle=o.wire?'rgba(0,0,0,0)':'#0b0a10';g.strokeStyle=o.wire?'rgba(120,255,240,.7)':'#22202c';g.lineWidth=o.wire?4:6;
  g.beginPath();g.moveTo(-270,-640);g.lineTo(270,-640);g.lineTo(270,-470);g.lineTo(300,-470);g.lineTo(240,-90);g.lineTo(300,-40);g.lineTo(300,640);g.lineTo(-300,640);g.lineTo(-300,-40);g.lineTo(-240,-90);g.lineTo(-300,-470);g.lineTo(-270,-470);g.closePath();g.fill();g.stroke();
  if(!o.wire){
    // marquesina
    const mg=g.createLinearGradient(0,-630,0,-480);mg.addColorStop(0,'#2a1240');mg.addColorStop(1,'#120820');g.fillStyle=mg;g.fillRect(-255,-625,510,140);
    g.save();g.font='92px Anton';g.textAlign='center';g.fillStyle='#f3f0ff';g.shadowColor='#b040ff';g.shadowBlur=30*flick(t,.3);g.fillText('POLYBIUS',0,-520);g.restore();
    // pantalla
    g.fillStyle='#020205';rr(g,-215,-430,430,330,30);g.fill();
    if(scr>0){g.save();rr(g,-215,-430,430,330,30);g.clip();g.globalAlpha=scr;
      if(o.text){g.fillStyle='#020205';g.fillRect(-215,-430,430,330);g.font='58px VT';g.textAlign='center';g.fillStyle='#7dffef';g.shadowColor='#7dffef';g.shadowBlur=18;
        o.text.split('\n').forEach((l,i,a)=>g.fillText(l,0,-265-(a.length-1)*30+i*60))}
      else tunnel(g,0,-265,240,t,o.hue||0);
      g.restore();const sg=g.createRadialGradient(0,-265,20,0,-265,520);sg.addColorStop(0,`rgba(120,220,255,${.22*scr})`);sg.addColorStop(1,'rgba(120,220,255,0)');g.fillStyle=sg;g.fillRect(-600,-800,1200,1100)}
    // panel de control
    g.fillStyle='#17151f';g.beginPath();g.moveTo(-240,-90);g.lineTo(240,-90);g.lineTo(300,-40);g.lineTo(-300,-40);g.closePath();g.fill();
    g.fillStyle='#e0162b';g.beginPath();g.arc(-120,-62,16,0,7);g.fill();g.fillStyle='#111';g.fillRect(-124,-110,8,46);
    ['#f2d24a','#2ec5ff','#e0162b'].forEach((c,i)=>{g.fillStyle=c;g.beginPath();g.ellipse(60+i*55,-62,18,10,0,0,7);g.fill()});
    // ranura de monedas
    g.fillStyle='#1d1b24';g.fillRect(-70,120,140,180);g.fillStyle=`rgba(255,60,40,${.6+.4*Math.sin(t*3)})`;g.fillRect(-40,160,24,60);g.fillRect(16,160,24,60);
    g.font='26px VT';g.textAlign='center';g.fillStyle='rgba(255,120,90,.9)';g.fillText('25¢',0,270);
  }
  g.restore();
}
function room(g,t,o={}){
  g.fillStyle='#07050c';g.fillRect(0,0,W,H);
  // máquinas de fondo
  [[-60,.55,40],[180,.5,300],[900,.5,120],[1140,.55,220]].forEach(([x,s,h])=>{g.save();g.globalAlpha=.55;cabinet(g,x,1080,s,t+h,{hue:h});g.restore()});
  g.fillStyle='rgba(7,5,12,.55)';g.fillRect(0,0,W,H);
  // suelo con moqueta
  const fl=g.createLinearGradient(0,1500,0,H);fl.addColorStop(0,'#120c1c');fl.addColorStop(1,'#050308');g.fillStyle=fl;g.fillRect(0,1500,W,H);
  g.fillStyle='rgba(120,60,200,.12)';for(let i=0;i<40;i++){const x=hash(i*3.3)*W,y=1520+hash(i*7.7)*400;g.beginPath();g.arc(x,y,6+hash(i)*10,0,7);g.fill()}
  if(o.police){const a=Math.sin(t*2.2);g.globalCompositeOperation='lighter';g.fillStyle=`rgba(255,30,40,${.16*Math.max(a,0)})`;g.fillRect(0,0,W,H);g.fillStyle=`rgba(40,80,255,${.16*Math.max(-a,0)})`;g.fillRect(0,0,W,H);g.globalCompositeOperation='source-over'}
}
function mib(g,x,fy,h){const s=h/100;g.save();g.translate(x,fy);g.scale(s,s);const gl=g.createRadialGradient(0,-60,5,0,-60,70);gl.addColorStop(0,'rgba(120,200,255,.35)');gl.addColorStop(1,'rgba(120,200,255,0)');g.fillStyle=gl;g.fillRect(-80,-140,160,150);g.fillStyle='#010101';
  g.fillRect(-9,-48,7,48);g.fillRect(2,-48,7,48);g.beginPath();g.moveTo(-13,-84);g.lineTo(13,-84);g.lineTo(11,-46);g.lineTo(-11,-46);g.closePath();g.fill();
  g.beginPath();g.ellipse(0,-92,7,8,0,0,7);g.fill();g.fillRect(-12,-99,24,2.6);g.fillRect(-7,-108,14,9);
  g.fillStyle='rgba(240,240,240,.7)';g.fillRect(10,-70,9,12);g.restore()}

function scene(g,t,forLoop){
  let date='1981';
  if(t<4.2){room(g,t);cabinet(g,W/2,1320,1,t);
    if(!forLoop){big(g,'UN ARCADE QUE',440,120,t-.15);big(g,'*BORRABA LA MEMORIA*.',575,108,t-.7);big(g,'NADIE HA ENCONTRADO UNO.',1720,86,t-2.3,{dx:-20,maxW:820})}}
  else if(t<10){const k=t-4.2;room(g,t);cabinet(g,W/2,1320+k*6,1-k*.02,t);g.fillStyle='rgba(0,0,0,.45)';g.fillRect(0,0,W,H);
    big(g,'PORTLAND, 1981.',470,140,k-.2);small(g,'Dicen que apareció de la nada en los arcades de Oregón.',640,k-.9,{size:40});big(g,'SE LLAMABA *POLYBIUS*.',1720,96,k-3.4,{dx:-20,maxW:840})}
  else if(t<16){const k=t-10;room(g,t);cabinet(g,W/2,1320,1,t,{hue:120});g.fillStyle='rgba(0,0,0,.55)';g.fillRect(0,0,W,H);
    big(g,'EL FABRICANTE:',470,110,k-.2);big(g,'*SINNESLÖSCHEN*',620,128,k-1.4);small(g,'En alemán: «borrar los sentidos».',800,k-2.6,{size:46,weight:700})}
  else if(t<24){const k=t-16;room(g,t);cabinet(g,W/2,1320,1,t,{hue:200});
    if(k>3.2){mib(g,180,1700,520);mib(g,900,1700,540)}g.fillStyle='rgba(0,0,0,.3)';g.fillRect(0,0,W,H);
    big(g,'PESADILLAS. AMNESIA.',440,108,k-.1);big(g,'JUGADORES QUE *NO VOLVÍAN*.',580,96,k-1.4);
    big(g,'Y HOMBRES DE NEGRO',1500,96,k-3.2,{dx:-20});big(g,'RECOGIENDO DATOS DE NOCHE.',1620,76,k-4.2,{dx:-20,maxW:820})}
  else if(t<33){const k=t-24;room(g,t);const fade=clamp((k-1)/1.5);
    g.save();g.globalAlpha=1-fade;cabinet(g,W/2,1320,1,t);g.restore();g.save();g.globalAlpha=fade;cabinet(g,W/2,1320,1,t,{wire:1});g.restore();
    big(g,'PERO…',440,130,k-.1);big(g,'NI UNA FOTO. NI UNA PLACA.',580,92,k-1.2);if(k>3.3)stamp(g,'NADA',W/2,1000,k-3.3);
    small(g,'Primera mención: una web de arcades, hacia el año 2000.',1480,k-4.4,{size:38,dx:-20,maxW:820});small(g,'En papel: hasta 2003.',1640,k-6.6,{size:42,weight:700,dx:-20})}
  else if(t<41){const k=t-33;room(g,t,{police:1});cabinet(g,W/2,1320,1,t);g.fillStyle='rgba(0,0,0,.4)';g.fillRect(0,0,W,H);
    big(g,'LO QUE *SÍ* PASÓ:',440,128,k-.1);small(g,'1981: dos jugadores enferman en un arcade de Portland el mismo día.',620,k-1.6,{size:42,weight:700});
    big(g,'LA LEYENDA HIZO EL RESTO.',1660,84,k-4.6,{dx:-20,maxW:820})}
  else{const k=t-41;room(g,t);const scare=t>=45.5;const z=1+clamp((k-.5)/4)*.35;
    cabinet(g,W/2,1320+ (z-1)*300,z,t,{text:scare?'TE ESTÁBAMOS\nESPERANDO':(Math.floor(t*1.2)%2?'INSERT COIN':' ')});
    if(!scare){big(g,'¿JUGARÍAS',440,140,k-.1);big(g,'*UNA PARTIDA*?',590,130,k-.4);small(g,'Comenta INSERT COIN si te atreves.',1720,k-1.4,{size:42,weight:700,dx:-20})}
    else{date='HOY';big(g,'¿JUGARÍAS',440,140,k-.1);big(g,'*UNA PARTIDA*?',590,130,k-.4)}}
  return date;
}
