// X7 · Creepypastas de videojuegos que eran FALSAS
window.CINE=1;window.BED='tape';window.GRADE='rgba(160,120,255,.07)';window.COVER_TEXT=['ERA','*MENTIRA*'];
window.DATE=(L)=>({lavender:'1996',lavfalse:'2010',ben:'SEP. 2010',hero:'2011'}[L.scene]||'HOY');
const GB=['#0f380f','#306230','#8bac0f','#9bbc0f'];
function cart(g,x,y,s,label,col,t){g.save();g.translate(x,y);g.scale(s,s);g.fillStyle='#2a2a30';rr(g,-150,-180,300,330,20);g.fill();g.fillStyle='#1a1a20';for(let i=0;i<5;i++)g.fillRect(-130,-170+i*12,260,6);
  g.fillStyle=col;rr(g,-120,-110,240,170,10);g.fill();g.fillStyle='#fff';g.font='34px Anton';g.textAlign='center';g.fillText(label,0,-10);g.font='20px VT';g.fillText('PARA SIEMPRE',0,30);
  g.fillStyle='#c8a030';for(let i=0;i<10;i++)g.fillRect(-110+i*22,120,12,30);g.restore()}
function table(g,t,ks){g.fillStyle='#0a0808';g.fillRect(0,0,W,H);const lg=g.createRadialGradient(540,1150,40,540,1150,800);lg.addColorStop(0,'rgba(255,200,150,.3)');lg.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=lg;g.fillRect(0,0,W,H);
  g.fillStyle='#22160e';g.fillRect(0,1300,W,620);cart(g,280,1220,.8,'???','#6a1a1a',t);cart(g,540,1180,.9,'ZELDA?','#1a4a2a',t);cart(g,800,1220,.8,'BLOQUES','#2a3a6a',t);
  for(let i=0;i<30;i++){const x=hash(i)*W,y=(hash(i*5)*H+t*20)%H;g.fillStyle='rgba(255,230,200,.15)';g.fillRect(x,y,3,3)}}
function lavender(g,t,ks){g.fillStyle=GB[0];g.fillRect(0,0,W,H);const p=24;g.save();g.translate(540,1100);
  for(let y=-14;y<14;y++)for(let x=-18;x<18;x++){const v=hash(x*31+y*17);g.fillStyle=v>.85?GB[1]:GB[2];g.fillRect(x*p,y*p,p,p)}
  g.fillStyle=GB[0];g.fillRect(-90,-330,180,420);for(let k=0;k<6;k++){g.fillStyle=GB[3];g.fillRect(-60,-300+k*60,30,30);g.fillRect(30,-300+k*60,30,30)}g.fillStyle=GB[0];g.beginPath();g.moveTo(-110,-330);g.lineTo(0,-420);g.lineTo(110,-330);g.fill();
  for(let i=0;i<6;i++){const nx=-300+i*120+Math.sin(t*2+i)*20,ny=-200-((t*60+i*70)%300);g.fillStyle=GB[0];g.font='48px VT';g.fillText('♪',nx,ny)}g.restore();
  g.fillStyle='rgba(15,56,15,.35)';for(let y=0;y<H;y+=6)g.fillRect(0,y,W,2)}
function benS(g,t,ks){g.fillStyle='#030806';g.fillRect(0,0,W,H);const z=1+ks*.05;g.save();g.translate(540,1150);g.scale(z,z);g.fillStyle='rgba(30,200,120,.12)';for(let i=0;i<6;i++){g.beginPath();g.arc(0,0,100+i*90,0,7);g.fill()}
  g.fillStyle='#eae2c8';g.beginPath();g.ellipse(0,-60,80,95,0,0,7);g.fill();g.fillStyle='#000';g.beginPath();g.ellipse(-30,-70,16,22,0,0,7);g.ellipse(30,-70,16,22,0,0,7);g.fill();
  g.fillStyle='#ff2020';g.shadowColor='#f00';g.shadowBlur=18;g.beginPath();g.arc(-30,-64,6,0,7);g.arc(30,-64,6,0,7);g.fill();g.shadowBlur=0;g.strokeStyle='#000';g.lineWidth=4;g.beginPath();g.moveTo(-40,-10);g.quadraticCurveTo(0,10,40,-10);g.stroke();
  g.fillStyle='#1a5a2a';g.beginPath();g.moveTo(-90,-110);g.lineTo(0,-260);g.lineTo(90,-110);g.fill();g.restore();noise(g,.12,t)}
function heroS(g,t,ks){g.fillStyle='#4a6a8a';g.fillRect(0,0,W,H);const s=g.createLinearGradient(0,0,0,H);s.addColorStop(0,'#1a2a40');s.addColorStop(.55,'#6a8aa8');s.addColorStop(.56,'#2a4a1a');s.addColorStop(1,'#14200c');g.fillStyle=s;g.fillRect(0,0,W,H);
  const bl=40;for(let x=0;x<W;x+=bl){const h=Math.floor(hash(x)*4);for(let k=0;k<h;k++){g.fillStyle=k===h-1?'#4a7a2a':'#5a3a1a';g.fillRect(x,1056-k*bl,bl-2,bl-2)}}
  for(let i=0;i<5;i++){const x=80+i*220;g.fillStyle='#3a2a14';g.fillRect(x+60,820,40,240);g.fillStyle='#1a4a14';g.fillRect(x,660,160,180)}
  const hx=lerp(760,640,clamp(ks/4));g.fillStyle='#2a6aa8';g.fillRect(hx-40,880,80,100);g.fillStyle='#3a2a6a';g.fillRect(hx-40,980,80,90);g.fillStyle='#b88a6a';g.fillRect(hx-36,800,72,80);g.fillStyle='#3a2414';g.fillRect(hx-36,800,72,20);
  g.fillStyle='#ffffff';g.shadowColor='#fff';g.shadowBlur=20;g.fillRect(hx-26,830,18,10);g.fillRect(hx+8,830,18,10);g.shadowBlur=0;g.fillStyle='rgba(0,0,0,.35)';g.fillRect(0,0,W,H)}
const SC={hook:table,lavender,lavfalse:(g,t,ks)=>{lavender(g,t,ks);stamp(g,'FALSO',540,1150,ks-.2,'#e0162b',-.15,150)},ben:benS,hero:(g,t,ks)=>{heroS(g,t,ks);if(ks>3)stamp(g,'ELIMINADO',540,1350,ks-3,'#e0162b',.1,100)},hookend:table};
