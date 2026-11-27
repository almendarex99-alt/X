// X6 · Lo más aterrador escondido en GTA V
window.CINE=1;window.BED='forest';window.GRADE='rgba(120,150,255,.07)';window.COVER_TEXT=['MONTE','*GORDO*'];
window.DATE=(L)=>({ghost:'PM 11:00',jock:'PM 11:30',ufo:'AM 3:00',bigfoot:'100%'}[L.scene]||'2013');
function cliff(g,t,ks,o={}){const s=g.createLinearGradient(0,0,0,H);s.addColorStop(0,'#03050c');s.addColorStop(.5,'#0d1a2a');s.addColorStop(1,'#020306');g.fillStyle=s;g.fillRect(0,0,W,H);
  for(let i=0;i<120;i++){g.fillStyle=`rgba(220,230,255,${.3+.6*hash(i)})`;g.fillRect(hash(i*3.3)*W,hash(i*7.7)*800,2,2)}
  g.fillStyle='#d8e2e4';g.beginPath();g.arc(820,330,40,0,7);g.fill();
  // mar y luces de ciudad
  g.fillStyle='#050a12';g.fillRect(0,1100,W,300);for(let i=0;i<60;i++){g.fillStyle=`rgba(255,${180+hash(i)*60},120,.7)`;g.fillRect(hash(i*5.1)*W,1140+hash(i*2.3)*60,3,3)}
  g.fillStyle='#070809';g.beginPath();g.moveTo(0,1250);g.lineTo(380,1180);g.lineTo(520,1220);g.lineTo(700,1400);g.lineTo(W,1500);g.lineTo(W,H);g.lineTo(0,H);g.fill();
  g.fillStyle='#0b0c0d';g.beginPath();g.moveTo(330,1190);g.lineTo(470,1170);g.lineTo(520,1230);g.lineTo(380,1250);g.fill();
  if(o.ghost){const a=.55+.35*Math.sin(t*2);g.save();g.globalAlpha=a;const gg=g.createRadialGradient(430,1060,10,430,1060,220);gg.addColorStop(0,'rgba(200,230,255,.7)');gg.addColorStop(1,'rgba(200,230,255,0)');g.fillStyle=gg;g.fillRect(200,820,460,460);
    g.fillStyle='rgba(225,240,255,.85)';g.beginPath();g.ellipse(430,1000,18,22,0,0,7);g.fill();g.beginPath();g.moveTo(410,1020);g.quadraticCurveTo(400,1100,380,1170+Math.sin(t*3)*6);g.lineTo(480,1170+Math.sin(t*3+1)*6);g.quadraticCurveTo(460,1100,450,1020);g.fill();g.restore()}
  if(o.blood){g.save();g.translate(420,1215);g.rotate(-.06);g.font='italic 64px Anton';g.fillStyle='rgba(150,8,8,.95)';g.fillText('JOCK',-60,0);g.fillStyle='rgba(150,8,8,.7)';[[-40,6],[0,10],[30,8]].forEach(([x,l])=>g.fillRect(x,4,4,l*3));g.restore()}}
function chiliad(g,t,ks){g.fillStyle='#020306';g.fillRect(0,0,W,H);const fl=hash(Math.floor(t*3))>.85;if(fl){g.fillStyle='rgba(200,220,255,.35)';g.fillRect(0,0,W,H);g.strokeStyle='rgba(240,245,255,.9)';g.lineWidth=5;g.beginPath();let x=700,y=0;g.moveTo(x,y);while(y<900){x+=(hash(y+t)-.5)*120;y+=80;g.lineTo(x,y)}g.stroke()}
  g.fillStyle='#08090b';g.beginPath();g.moveTo(0,1500);g.lineTo(540,1000);g.lineTo(W,1500);g.lineTo(W,H);g.lineTo(0,H);g.fill();g.fillStyle='#14161a';g.fillRect(500,980,80,30);
  const ux=540+Math.sin(t*.4)*30,uy=700;g.save();g.globalAlpha=.7+.3*Math.sin(t*4);g.fillStyle='rgba(140,255,220,.15)';g.beginPath();g.moveTo(ux-80,uy+40);g.lineTo(ux+80,uy+40);g.lineTo(ux+200,1000);g.lineTo(ux-200,1000);g.fill();
  g.fillStyle='#2a3a3a';g.beginPath();g.ellipse(ux,uy,240,50,0,0,7);g.fill();g.fillStyle='#4a6a6a';g.beginPath();g.ellipse(ux,uy-30,110,50,0,Math.PI,0);g.fill();
  for(let k=0;k<10;k++){g.fillStyle=Math.floor(t*5+k)%2?'#7dffef':'#ffffff';g.beginPath();g.arc(ux-200+k*44,uy+8,7,0,7);g.fill()}g.font='28px Anton';g.fillStyle='#d8e0e0';g.fillText('FIB',ux-20,uy+4);g.restore();
  for(let i=0;i<150;i++){const x=(hash(i*3.3)*W+t*80)%W,y=(hash(i*7.7)*H+t*1500)%H;g.strokeStyle='rgba(200,210,230,.3)';g.lineWidth=2;g.beginPath();g.moveTo(x,y);g.lineTo(x-10,y+40);g.stroke()}}
function hookG(g,t,ks){cliff(g,t,ks,{});g.fillStyle='rgba(0,0,0,.3)';g.fillRect(0,0,W,H);g.save();g.font='60px VT';g.fillStyle='#e9e2d2';g.textAlign='center';g.fillText('COMPLETADO: 100%',540,1000);g.fillStyle='#3fd06b';g.fillRect(240,1040,600*clamp(ks/2),26);g.strokeStyle='#e9e2d2';g.lineWidth=3;g.strokeRect(240,1040,600,26);g.restore()}
const SC={hook:hookG,ghost:(g,t,ks)=>cliff(g,t,ks,{ghost:1}),jock:(g,t,ks)=>{cliff(g,t,ks,{ghost:ks<2,blood:1})},ufo:chiliad,
 bigfoot:(g,t,ks)=>forest(g,t,{flash:1,figure:{layer:2,draw:()=>bigfoot(g,lerp(300,620,clamp(ks/5)),1500,lerp(600,900,clamp(ks/5)),1,t,.6)}}),hookend:(g,t,ks)=>cliff(g,t,ks,{ghost:1})};
