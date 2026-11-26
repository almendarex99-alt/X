// W10 · 5 reglas si tu consola se enciende sola a las 3:33 (historia original)
window.BED='tape';window.GRADE='rgba(90,120,255,.07)';window.COVER_TEXT=['3:33','*NO LA TOQUES*'];
window.DATE=()=>'AM 3:33';
function bedroom(g,t,ks,o={}){g.fillStyle='#04050a';g.fillRect(0,0,W,H);
  const tvOn=o.tv!==false;const glow=tvOn?(o.glow||'rgba(120,150,255,.35)'):'rgba(0,0,0,0)';
  g.fillStyle='#0c0d14';g.fillRect(0,1500,W,420);g.fillStyle='#14121a';g.fillRect(140,1240,800,260);
  crtIn(g,250,800,580,430,(c,w,h)=>{if(!tvOn){c.fillStyle='#030304';c.fillRect(0,0,w,h);if(o.reflect){c.fillStyle='rgba(120,130,150,.18)';c.fillRect(0,0,w,h);c.fillStyle='#020203';c.beginPath();c.ellipse(w*.7,h*.45,40,50,0,0,7);c.fill();c.fillRect(w*.7-55,h*.55,110,h)}return}(o.screen||((c,w,h)=>{c.fillStyle='#08102a';c.fillRect(0,0,w,h)}))(c,w,h)});
  // consola
  g.fillStyle='#111118';rr(g,380,1330,320,90,14);g.fill();g.fillStyle=o.led===false?'#222':`rgba(80,160,255,${.6+.4*Math.sin(t*3)})`;g.shadowColor='#5af';g.shadowBlur=20;g.beginPath();g.arc(660,1375,10,0,7);g.fill();g.shadowBlur=0;
  if(tvOn){const rg=g.createRadialGradient(540,1015,60,540,1015,1000);rg.addColorStop(0,glow);rg.addColorStop(1,'rgba(0,0,0,0)');g.globalCompositeOperation='lighter';g.fillStyle=rg;g.fillRect(0,0,W,H);g.globalCompositeOperation='source-over'}
  // puerta al fondo
  g.fillStyle='#07080c';g.fillRect(860,560,180,700);if(o.door){g.fillStyle='#000';g.fillRect(880,580,140,680);person(g,950,1260,560,{eyes:'rgba(240,240,230,.9)'})}
  if(o.extra)o.extra()}
const screenClock=(c,w,h,t)=>{c.fillStyle='#04081a';c.fillRect(0,0,w,h);c.font='150px VT';c.textAlign='center';c.fillStyle='#e9e2d2';c.shadowColor='#7af';c.shadowBlur=20;c.fillText('3:33',w/2,h/2+50)};
const screenSave=(c,w,h,t)=>{c.fillStyle='#0a1030';c.fillRect(0,0,w,h);c.font='34px VT';c.fillStyle='#cfd8ff';c.fillText('CARGAR PARTIDA',30,50);
  ['PARTIDA 1 · TUYA · 12:04','PARTIDA 2 · TUYA · 03:17','PARTIDA ? · ??? · 99:99'].forEach((s,i)=>{c.fillStyle=i===2?'rgba(224,22,43,.35)':'rgba(60,80,160,.5)';c.fillRect(30,80+i*100,w-60,80);c.fillStyle=i===2?'#ff6670':'#e8ecff';c.fillText(s,50,130+i*100)})};
const screenName=(c,w,h,t)=>{c.fillStyle='#000';c.fillRect(0,0,w,h);c.font='40px VT';c.fillStyle='#e9e2d2';c.textAlign='center';c.fillText('JUGADOR:',w/2,h*.38);c.font='90px VT';c.fillStyle='#ff4a55';c.fillText('TÚ',w/2,h*.62)};
const screenStart=(c,w,h,t)=>{c.fillStyle='#000';c.fillRect(0,0,w,h);if(Math.floor(t*1.5)%2){c.font='70px VT';c.textAlign='center';c.fillStyle='#e9e2d2';c.fillText('PULSA START',w/2,h/2+24)}};
function padS(g,t,ks){bedroom(g,t,ks,{screen:(c,w,h)=>screenClock(c,w,h,t),extra:()=>{const sh=Math.sin(t*70)*6;g.save();g.translate(540+sh,1680);g.fillStyle='#1d1d24';rr(g,-170,-55,340,120,55);g.fill();
  g.fillStyle='#2a2a34';g.beginPath();g.arc(-90,0,26,0,7);g.arc(90,0,26,0,7);g.fill();g.fillStyle='#5af';g.beginPath();g.arc(0,-28,6,0,7);g.fill();g.restore();
  for(let i=0;i<3;i++){const r=((t*200+i*60)%180);g.strokeStyle=`rgba(120,170,255,${1-r/180})`;g.lineWidth=3;g.beginPath();g.ellipse(540,1680,170+r,55+r*.4,0,0,7);g.stroke()}}})}
const SC={
 console:(g,t,ks)=>bedroom(g,t,ks,{tv:ks>.8,led:ks>.4,screen:(c,w,h)=>screenClock(c,w,h,t)}),
 pad:padS,
 save:(g,t,ks)=>bedroom(g,t,ks,{screen:(c,w,h)=>screenSave(c,w,h,t)}),
 name:(g,t,ks)=>bedroom(g,t,ks,{tv:ks<2.6,screen:(c,w,h)=>screenName(c,w,h,t),glow:'rgba(255,60,70,.3)'}),
 reflect:(g,t,ks)=>bedroom(g,t,ks,{tv:false,reflect:ks>1.2}),
 voice:(g,t,ks)=>bedroom(g,t,ks,{screen:(c,w,h)=>screenStart(c,w,h,t),door:ks>1.4}),
 consoleend:(g,t,ks)=>bedroom(g,t,ks,{screen:(c,w,h)=>screenClock(c,w,h,t),door:true})};
