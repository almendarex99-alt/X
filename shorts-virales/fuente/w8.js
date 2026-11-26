// W8 · Cómo sobrevivir tu primera noche en Five Nights at Freddy's
window.BED='drone';window.GRADE='rgba(80,120,200,.07)';window.COVER_TEXT=['12 A 6','*NO DUERMAS*'];
window.DATE=(L,t)=>{const h=Math.min(6,Math.floor((t/DUR)*6));return (h===0?'12':h)+' AM'};
// animatrónicos genéricos (siluetas propias)
function animatronic(g,x,fy,h,kind,t,eyes=true){const s=h/100;g.save();g.translate(x,fy);g.scale(s,s);g.fillStyle='#0b0a0a';
  g.fillRect(-16,-58,32,48);g.fillRect(-12,-12,9,12);g.fillRect(3,-12,9,12);g.fillRect(-24,-56,8,34);g.fillRect(16,-56,8,34);
  g.beginPath();g.ellipse(0,-74,17,16,0,0,7);g.fill();g.beginPath();g.ellipse(0,-66,11,7,0,0,7);g.fill();
  if(kind==='bear'){g.beginPath();g.arc(-12,-88,6,0,7);g.arc(12,-88,6,0,7);g.fill();g.fillRect(-9,-100,18,6);g.fillRect(-6,-110,12,10)}
  if(kind==='bunny'){g.fillRect(-12,-118,7,30);g.fillRect(5,-118,7,30)}
  if(kind==='chicken'){g.beginPath();g.moveTo(-4,-92);g.lineTo(0,-100);g.lineTo(4,-92);g.fill();g.fillStyle='#2a2620';g.fillRect(-14,-50,28,16)}
  if(kind==='fox'){g.beginPath();g.moveTo(-15,-84);g.lineTo(-10,-100);g.lineTo(-4,-86);g.moveTo(15,-84);g.lineTo(10,-100);g.lineTo(4,-86);g.fill();g.beginPath();g.moveTo(-8,-66);g.lineTo(0,-56);g.lineTo(8,-66);g.fill()}
  if(eyes){g.fillStyle='rgba(255,255,255,.95)';g.shadowColor='#fff';g.shadowBlur=8;g.beginPath();g.arc(-6,-76,2.6,0,7);g.arc(6,-76,2.6,0,7);g.fill();g.shadowBlur=0}
  g.restore()}
function office(g,t,ks,o={}){const s=g.createLinearGradient(0,0,0,H);s.addColorStop(0,'#0b0d14');s.addColorStop(1,'#050508');g.fillStyle=s;g.fillRect(0,0,W,H);
  // puertas laterales
  [[0,'L'],[1,'R']].forEach(([i])=>{const x=i?860:40;g.fillStyle=o.lit&&o.lit[i]?'#3a3a48':'#020203';g.fillRect(x,700,180,760);g.strokeStyle='#22242c';g.lineWidth=14;g.strokeRect(x,700,180,760);
    if(o.lit&&o.lit[i]&&o.who&&o.who[i])animatronic(g,x+90,1460,620,o.who[i],t);
    g.fillStyle='#2b2d36';g.fillRect(i?780:240,960,60,180);g.fillStyle=o.lit&&o.lit[i]?'#ffffff':'#666';g.beginPath();g.arc(i?810:270,1000,16,0,7);g.fill();g.fillStyle='#c22';g.beginPath();g.arc(i?810:270,1090,16,0,7);g.fill()});
  // escritorio, monitores y ventilador
  g.fillStyle='#1a1712';g.fillRect(100,1440,880,480);g.fillStyle='#0e0e10';g.fillRect(360,1220,360,220);g.fillStyle=`rgba(120,170,140,${.35*flick(t,.4)})`;g.fillRect(380,1240,320,180);
  g.save();g.translate(800,1350);g.fillStyle='#22242c';g.fillRect(-6,0,12,90);g.rotate(t*25);for(let i=0;i<3;i++){g.rotate(2.09);g.fillStyle='#3a3c46';g.beginPath();g.ellipse(0,-34,12,34,0,0,7);g.fill()}g.restore();
  g.fillStyle='rgba(30,30,40,.9)';g.font='26px VT';g.fillText('¡CELEBRA!',430,900);
  const lamp=g.createRadialGradient(540,700,30,540,900,900);lamp.addColorStop(0,`rgba(255,235,190,${.2*flick(t,.6)})`);lamp.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=lamp;g.fillRect(0,0,W,H);if(o.extra)o.extra()}
function camsF(g,t,ks){g.fillStyle='#0a0c0a';g.fillRect(0,0,W,H);g.fillStyle='#111611';rr(g,60,420,960,1100,40);g.fill();
  const cell=(x,y,w,h,label,draw)=>{g.save();g.beginPath();g.rect(x,y,w,h);g.clip();g.fillStyle='#14180f';g.fillRect(x,y,w,h);draw(x,y,w,h);g.globalAlpha=.35;g.drawImage(GRAIN[Math.floor(t*30)%6],x,y,w,h);g.globalAlpha=1;g.restore();g.font='30px VT';g.fillStyle='#e9e2d2';g.fillText(label,x+14,y+36)};
  cell(90,450,900,520,'CAM 1A · ESCENARIO',(x,y,w,h)=>{g.fillStyle='#2a1f16';g.fillRect(x,y+h*.7,w,h*.3);g.fillStyle='rgba(255,230,180,.15)';g.fillRect(x,y,w,h);['bunny','bear','chicken'].forEach((k,i)=>animatronic(g,x+w*(.25+i*.25),y+h*.88,h*.7,k,t,i!==1||Math.sin(t*2)>0))});
  cell(90,1000,440,480,'CAM 1C · CUEVA PIRATA',(x,y,w,h)=>{g.fillStyle='#3a0f2a';g.fillRect(x,y,w,h);g.fillStyle='#5a1840';for(let i=0;i<6;i++)g.fillRect(x+i*76,y+60,60,h);g.fillStyle='#f2d24a';for(let i=0;i<8;i++){g.beginPath();g.arc(x+30+i*55,y+120+(i%2)*60,6,0,7);g.fill()}});
  cell(550,1000,440,480,'CAM 2A · PASILLO',(x,y,w,h)=>{g.fillStyle='#0c0e0c';g.fillRect(x,y,w,h);g.strokeStyle='#1d221c';g.lineWidth=6;g.strokeRect(x+120,y+80,200,h-80)});
  g.fillStyle=Math.floor(t*2)%2?'#e0162b':'transparent';g.beginPath();g.arc(960,480,12,0,7);g.fill()}
function powerF(g,t,ks){office(g,t,ks);const p=Math.max(0,99-Math.floor(ks*9));g.fillStyle='rgba(0,0,0,.6)';g.fillRect(80,1500,920,280);g.font='70px VT';g.fillStyle='#e9e2d2';g.fillText('ENERGÍA: '+p+'%',120,1590);
  g.font='50px VT';g.fillText('USO:',120,1690);const u=1+Math.floor((Math.sin(t*1.3)+1)*1.6);for(let i=0;i<4;i++){g.fillStyle=i<u?(i<2?'#3fd06b':i<3?'#e2c442':'#e0162b'):'rgba(255,255,255,.12)';g.fillRect(260+i*60,1645,44,60)}}
function coveF(g,t,ks){g.fillStyle='#120612';g.fillRect(0,0,W,H);const open=clamp((ks-1)/2.5);
  g.fillStyle='#3a0f2a';g.fillRect(0,400,W,1300);for(let i=0;i<10;i++){const x=i*108,sw=(i<5?-1:1)*open*260*(Math.abs(i-4.5)<2?1:.3);g.fillStyle=i%2?'#5a1840':'#4a1236';g.fillRect(x+sw,400,108,1300)}
  g.fillStyle='#f2d24a';for(let i=0;i<14;i++){g.beginPath();g.arc(60+i*75,520+(i%3)*140,8,0,7);g.fill()}
  if(open>.2){const run=clamp((ks-3.2)/1);animatronic(g,540+run*900,1700+run*100,lerp(900,1400,run),'fox',t)}
  g.font='40px VT';g.fillStyle='#e9e2d2';g.fillText('CAM 1C · CUEVA PIRATA',80,470)}
function darkF(g,t,ks){g.fillStyle='#000';g.fillRect(0,0,W,H);office(g,t,ks,{});g.fillStyle=`rgba(0,0,0,${clamp(.6+ks*.3,0,.93)})`;g.fillRect(0,0,W,H);
  const on=Math.floor(t*4)%2===0||ks>2.2;if(on){g.fillStyle='rgba(255,255,255,.95)';g.shadowColor='#fff';g.shadowBlur=20;g.beginPath();g.arc(170,1040,9,0,7);g.arc(210,1040,9,0,7);g.fill();g.shadowBlur=0}}
function endF(g,t,ks){office(g,t,ks);g.fillStyle='rgba(0,0,0,.55)';g.fillRect(0,0,W,H);g.save();g.font='260px Anton';g.textAlign='center';g.fillStyle='#f2ece0';g.shadowColor='#fff';g.shadowBlur=30*Math.abs(Math.sin(t*2));g.fillText('6 AM',W/2,1260);g.restore()}
const SC={office:(g,t,ks)=>office(g,t,ks,{lit:[0,0]}),cams:camsF,power:powerF,doorlight:(g,t,ks)=>office(g,t,ks,{lit:[ks%2<1,ks%2>=1],who:['bunny','chicken']}),cove:coveF,dark:darkF,officeend:endF};
