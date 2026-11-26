// componentes reutilizados de los videos anteriores
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
function kb(g,k,d,fn,z=.06,cx=W/2,cy=H/2){g.save();const s=1+z*clamp(k/Math.max(d,1));g.translate(cx,cy);g.scale(s,s);g.translate(-cx,-cy);fn();g.restore()}
function person(g,x,fy,h,o={}){const s=h/100;g.save();g.translate(x,fy);g.scale(s,s);const c=o.c||'#050505';g.fillStyle=c;g.strokeStyle=c;g.lineCap='round';
  if(o.dress){g.beginPath();g.moveTo(-10,-70);g.lineTo(10,-70);g.lineTo(17,-18);g.lineTo(-17,-18);g.closePath();g.fill();g.lineWidth=5;g.beginPath();g.moveTo(-6,-20);g.lineTo(-7,0);g.moveTo(6,-20);g.lineTo(7,0);g.stroke()}
  else{g.lineWidth=7;g.beginPath();g.moveTo(-5,-46);g.lineTo(-7,0);g.moveTo(5,-46);g.lineTo(7,0);g.stroke();g.beginPath();g.moveTo(-13,-80);g.lineTo(13,-80);g.lineTo(11,-44);g.lineTo(-11,-44);g.closePath();g.fill()}
  g.lineWidth=5;g.beginPath();g.moveTo(-12,-76);g.lineTo(o.armUp?-24:-15,o.armUp?-96:-46);g.moveTo(12,-76);g.lineTo(15,-46);g.stroke();
  g.beginPath();g.ellipse(0,-90,8.5,10,0,0,7);g.fill();
  if(o.hair){g.beginPath();g.moveTo(-9,-96);g.quadraticCurveTo(0,-106,9,-96);g.lineTo(11,-66);g.lineTo(-11,-66);g.closePath();g.fill()}
  if(o.suit){g.fillStyle='#d8d2c4';g.beginPath();g.moveTo(-5,-80);g.lineTo(5,-80);g.lineTo(0,-64);g.closePath();g.fill();g.fillStyle='#000';g.fillRect(-4,-79,8,3)}
  if(o.eyes){g.fillStyle=o.eyes;g.shadowColor=o.eyes;g.shadowBlur=6;g.fillRect(-4.5,-92,3,1.6);g.fillRect(1.5,-92,3,1.6)}
  g.restore()}
// cara con distorsión 0..1
function face(g,cx,cy,r,t,d=0,o={}){g.save();g.translate(cx+(d>.3?(hash(Math.floor(t*20))-.5)*r*.06*d:0),cy);g.scale(1,1+d*.35);
  const sk=g.createRadialGradient(-r*.2,-r*.3,r*.1,0,0,r*1.2);sk.addColorStop(0,o.skin||'#e3dccf');sk.addColorStop(1,'#8f877b');g.fillStyle=sk;g.beginPath();g.ellipse(0,0,r*.78,r,0,0,7);g.fill();
  g.save();g.beginPath();g.ellipse(0,0,r*.8,r*1.02,0,0,7);g.clip();g.fillStyle='#17130f';g.beginPath();g.ellipse(0,-r*.62,r*.95,r*.6,0,0,7);g.fill();
  g.beginPath();g.moveTo(-r*.8,-r*.35);g.quadraticCurveTo(-r*.3,-r*.2,r*.1,-r*.45);g.quadraticCurveTo(r*.5,-r*.3,r*.8,-r*.4);g.lineTo(r*.8,-r);g.lineTo(-r*.8,-r);g.closePath();g.fill();
  const cs=g.createRadialGradient(0,r*.2,r*.3,0,0,r*1.05);cs.addColorStop(0,'rgba(0,0,0,0)');cs.addColorStop(1,'rgba(20,14,10,.55)');g.fillStyle=cs;g.fillRect(-r,-r*1.1,r*2,r*2.2);g.restore();
  [-1,1].forEach(sd=>{const so=g.createRadialGradient(sd*r*.3,-r*.1,2,sd*r*.3,-r*.1,r*.26);so.addColorStop(0,'rgba(40,28,22,.55)');so.addColorStop(1,'rgba(40,28,22,0)');g.fillStyle=so;g.fillRect(sd*r*.3-r*.3,-r*.4,r*.6,r*.6)});
  const ey=-r*.12+d*r*.18,ew=r*.15*(1+d*.9),eh=r*.08*(1+d*1.8);
  [-1,1].forEach(sd=>{g.fillStyle=d>.5?'#f4f0e6':'#efe9dd';g.beginPath();g.ellipse(sd*r*.3,ey+sd*d*r*.06,ew,eh,0,0,7);g.fill();g.fillStyle='#000';g.beginPath();g.arc(sd*r*.3,ey+sd*d*r*.06,Math.max(r*.02,r*.06*(1-d*.8)),0,7);g.fill()});
  g.fillStyle='rgba(60,45,40,.35)';g.beginPath();g.moveTo(0,-r*.02);g.lineTo(-r*.07,r*.25);g.lineTo(r*.05,r*.27);g.closePath();g.fill();
  const mw=r*(.28+d*.5),my=r*.5+d*r*.1;g.fillStyle=d>.2?'#100606':'rgba(90,40,40,.8)';g.beginPath();g.moveTo(-mw,my);g.quadraticCurveTo(0,my+r*(.08+d*.45),mw,my);g.quadraticCurveTo(0,my+r*.03,-mw,my);g.fill();
  if(d>.35){g.strokeStyle='rgba(230,225,210,.8)';g.lineWidth=r*.012;for(let i=-6;i<=6;i++){const x=i/6*mw*.9;g.beginPath();g.moveTo(x,my+r*.02);g.lineTo(x,my+r*(.05+d*.25)*(1-Math.abs(i)/7));g.stroke()}}
  g.restore()}
function crtIn(g,x,y,w,h,draw){g.save();g.fillStyle='#16130f';rr(g,x-36,y-36,w+72,h+110,30);g.fill();g.fillStyle='#050505';rr(g,x,y,w,h,22);g.fill();
  g.save();rr(g,x,y,w,h,22);g.clip();g.translate(x,y);draw(g,w,h);g.restore();
  g.save();rr(g,x,y,w,h,22);g.clip();g.fillStyle='rgba(0,0,0,.25)';for(let yy=y;yy<y+h;yy+=4)g.fillRect(x,yy,w,2);const v=g.createRadialGradient(x+w/2,y+h/2,w*.2,x+w/2,y+h/2,w*.7);v.addColorStop(0,'rgba(0,0,0,0)');v.addColorStop(1,'rgba(0,0,0,.6)');g.fillStyle=v;g.fillRect(x,y,w,h);g.restore();
  g.fillStyle='#e0162b';g.beginPath();g.arc(x+30,y+h+40,7,0,7);g.fill();g.restore()}
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
function padMsg(g,t){g.save();g.fillStyle='rgba(0,0,0,.85)';g.fillRect(90,1140,900,260);g.strokeStyle='#e9e2d2';g.lineWidth=3;g.strokeRect(90,1140,900,260);
  g.font='700 46px Inter';g.fillStyle='#fff';g.textAlign='center';g.fillText('MANDO DESCONECTADO',540,1235);g.font='500 34px Inter';g.fillStyle='#c9c3b8';g.fillText('Vuelve a conectar el mando al puerto 1',540,1300);
  g.fillText(Math.floor(t*2)%2?'Pulsa START para continuar':'',540,1360);g.restore()}
const BUGS=[...Array(26)].map((_,i)=>({x:hash(i*3.7)*W,y:hash(i*5.1)*H,a:hash(i*9.3)*6.28,v:60+hash(i)*120,s:.7+hash(i*2.2)*.9}));
function bugs(g,t,k){g.save();BUGS.forEach((b,i)=>{const n=Math.floor(BUGS.length*clamp(k*1.6));if(i>=n)return;const a=b.a+Math.sin(t*2+i)*.6,x=(b.x+Math.cos(a)*b.v*t)%W,y=(b.y+Math.sin(a)*b.v*t+H)%H;
  g.save();g.translate((x+W)%W,y);g.rotate(a+Math.PI/2);g.scale(b.s*3.2,b.s*3.2);g.fillStyle='#0a0705';g.beginPath();g.ellipse(0,0,6,10,0,0,7);g.fill();g.beginPath();g.arc(0,-11,4,0,7);g.fill();
  g.strokeStyle='#0a0705';g.lineWidth=1.6;for(let l=-1;l<=1;l++){const w=Math.sin(t*25+l+i)*2;g.beginPath();g.moveTo(-5,l*5);g.lineTo(-12,l*6+w);g.moveTo(5,l*5);g.lineTo(12,l*6-w);g.stroke()}g.restore()});g.restore()}
