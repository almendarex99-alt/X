// W4 · Misterios de terror que se resolvieron AÑOS después
window.BED='tape';window.GRADE='rgba(255,210,120,.06)';window.COVER_TEXT=['RESUELTO','*AÑOS DESPUÉS*'];
window.DATE=(L)=>({backrooms:'MAY. 2019',found:'MAY. 2024',pt:'AGO. 2014',lisa:'SEP. 2019',polybius:'1981'}[L.scene]||'HOY');
const YEL={wall:[190,172,96],floor:[120,104,58],ceil:[200,194,168],base:[170,152,84]};
function board(g,t,ks){g.fillStyle='#14100c';g.fillRect(0,0,W,H);g.fillStyle='#3a2c1e';g.fillRect(60,400,960,1200);g.strokeStyle='#221a12';g.lineWidth=16;g.strokeRect(60,400,960,1200);
  const pins=[[260,620],[780,700],[300,1150],[760,1240],[540,920]];g.strokeStyle='rgba(200,30,30,.8)';g.lineWidth=4;g.beginPath();pins.forEach((p,i)=>i?g.lineTo(...p):g.moveTo(...p));g.stroke();
  pins.forEach(([x,y],i)=>{g.save();g.translate(x,y);g.rotate((hash(i)-.5)*.2);g.fillStyle='#e8e1cf';g.fillRect(-110,-80,220,160);g.fillStyle='#2a2622';g.fillRect(-96,-66,192,110);g.fillStyle='#1c1c1c';g.font='22px VT';g.fillText(['BACKROOMS','P.T.','POLYBIUS','???','2019'][i],-90,70);g.restore();g.fillStyle='#c01818';g.beginPath();g.arc(x,y-80,10,0,7);g.fill()});
  const lg=g.createRadialGradient(540,900,40,540,900,700);lg.addColorStop(0,'rgba(255,230,170,.2)');lg.addColorStop(1,'rgba(0,0,0,.4)');g.fillStyle=lg;g.fillRect(0,0,W,H)}
const PH4=mk(540,720),ph4=PH4.getContext('2d');
function backrooms(g,t,ks){g.fillStyle='#0a0906';g.fillRect(0,0,W,H);ph4.setTransform(.5,0,0,.375,0,0);hall(ph4,{t,cam:{x:.2,y:0,z:.4},pal:YEL,panels:1,flick:1,lampZ:-10,amb:.62});ph4.setTransform(1,0,0,1,0,0);
  g.save();g.translate(540,1150);g.rotate(-.05);g.fillStyle='#ece6d8';g.shadowColor='rgba(0,0,0,.7)';g.shadowBlur=30;g.fillRect(-330,-430,660,860);g.shadowBlur=0;g.drawImage(PH4,0,0,540,720,-300,-400,600,700);g.fillStyle='#333';g.font='italic 700 40px Inter';g.textAlign='center';g.fillText('¿dónde es?',0,380);g.restore()}
function found(g,t,ks){g.fillStyle='#07090c';g.fillRect(0,0,W,H);g.strokeStyle='rgba(120,160,200,.2)';g.lineWidth=2;for(let i=0;i<30;i++){g.beginPath();g.moveTo(0,i*70);g.lineTo(W,i*70+Math.sin(i)*40);g.stroke()}
  g.fillStyle='rgba(60,90,120,.35)';g.beginPath();g.moveTo(300,600);g.lineTo(800,560);g.lineTo(860,1300);g.lineTo(260,1340);g.closePath();g.fill();g.strokeStyle='#7dffef';g.lineWidth=3;g.stroke();
  const pz=clamp(ks/2);const px=560,py=lerp(400,960,ease(pz));g.fillStyle='#e0162b';g.beginPath();g.arc(px,py,26,0,7);g.fill();g.beginPath();g.moveTo(px-20,py+10);g.lineTo(px,py+60);g.lineTo(px+20,py+10);g.fill();
  if(ks>1.6){for(let i=0;i<3;i++){const r=((t*120+i*80)%240);g.strokeStyle=`rgba(224,22,43,${1-r/240})`;g.lineWidth=4;g.beginPath();g.arc(px,py+60,r,0,7);g.stroke()}
    g.save();g.globalAlpha=clamp((ks-1.6)*2);g.fillStyle='#120f0a';g.fillRect(180,1360,720,300);g.fillStyle='#f2d24a';g.fillRect(180,1360,720,60);g.fillStyle='#120f0a';g.font='48px Anton';g.textAlign='center';g.fillText('HOBBY',540,1408);
    g.fillStyle='rgba(255,230,150,.7)';g.fillRect(240,1460,160,140);g.fillRect(680,1460,160,140);g.fillStyle='#0a0806';g.fillRect(460,1460,160,200);g.restore()}}
function pt(g,t,ks){hall(g,{t,cam:{x:0,y:Math.sin(t*1.7)*.02,z:ks*.12},flick:flick(t),lisa:ks>2.2&&ks<2.5?{x:.05,z:8.8,a:.95}:null})}
function lisaS(g,t,ks){hall(g,{t,cam:{x:0,y:0,z:0},flick:flick(t,1)*.55,red:.35,lampZ:3.2,lisa:{x:.06,z:.86,a:1}})}
function poly(g,t,ks){room(g,t);const f=clamp((ks-2)/1.5);g.save();g.globalAlpha=1-f;cabinet(g,W/2,1320,1,t);g.restore();g.save();g.globalAlpha=f;cabinet(g,W/2,1320,1,t,{wire:1});g.restore();if(ks>3.5)stamp(g,'LEYENDA',W/2,1100,ks-3.5,'#e0162b',-.15,110)}
const SC={hook:board,backrooms,found,pt,lisa:lisaS,polybius:poly,hookend:board};
