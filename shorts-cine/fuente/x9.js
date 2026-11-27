// X9 · Cómo sobrevivir en Phasmophobia
window.CINE=1;window.BED='drone';window.GRADE='rgba(90,140,255,.07)';window.COVER_TEXT=['NO DIGAS','*SU NOMBRE*'];
window.DATE=()=>'CONTRATO';
function houseHall(g,t,ks,o={}){hall(g,{t,cam:{x:Math.sin(t*.4)*.12,y:Math.sin(t*1.6)*.02,z:ks*.12},flick:flick(t,o.hunt?1:.5)*(o.hunt?.5:1),red:o.hunt?.5:0,dark:.35,lisa:o.ghost?{x:.1,z:o.gz||6,a:.85}:null});
  // linterna
  const fx=540+Math.sin(t*.9)*200,fy=1000+Math.sin(t*.6)*120;const fl=g.createRadialGradient(fx,fy,20,fx,fy,520);fl.addColorStop(0,'rgba(255,250,230,.25)');fl.addColorStop(1,'rgba(0,0,0,0)');g.globalCompositeOperation='lighter';g.fillStyle=fl;g.fillRect(0,0,W,H);g.globalCompositeOperation='source-over';
  g.fillStyle=`rgba(0,0,0,${o.hunt?.25:.15})`;g.fillRect(0,0,W,H)}
function emf(g,t,ks,lvl){g.save();g.translate(760,1350);g.rotate(-.12);g.fillStyle='#1a1c22';rr(g,-130,-220,260,440,30);g.fill();for(let i=0;i<5;i++){g.fillStyle=i<lvl?['#3fd06b','#3fd06b','#e2c442','#ff8a2a','#e0162b'][i]:'#2a2a2e';g.beginPath();g.arc(-80+i*40,-150,14,0,7);g.fill()}
  g.font='34px VT';g.fillStyle='#e9e2d2';g.textAlign='center';g.fillText('EMF',0,-90);g.restore()}
function micS(g,t,ks){houseHall(g,t,ks);g.save();g.translate(540,1350);g.fillStyle='rgba(0,0,0,.6)';rr(g,-360,-120,720,240,30);g.fill();g.strokeStyle='#7dffef';g.lineWidth=5;g.beginPath();
  for(let x=-320;x<=320;x+=6){const y=Math.sin(x*.07+t*16)*Math.sin(t*4+x*.01)*70*(hash(Math.floor(t*6))>.3?1:.15);x>-320?g.lineTo(x,y):g.moveTo(x,y)}g.stroke();g.fillStyle='#e0162b';g.beginPath();g.arc(-320,-90,12,0,7);g.fill();g.font='34px VT';g.fillStyle='#e9e2d2';g.fillText('MIC',-296,-80);g.restore()}
function sanityS(g,t,ks){houseHall(g,t,ks,{ghost:ks>2.5,gz:5});const v=clamp(1-ks/4);g.save();g.fillStyle='rgba(0,0,0,.55)';rr(g,140,1260,800,140,20);g.fill();g.font='54px VT';g.fillStyle='#e9e2d2';g.fillText('CORDURA: '+Math.round(v*100)+'%',180,1350);
  g.fillStyle=v>.5?'#3fd06b':v>.25?'#e2c442':'#e0162b';g.fillRect(620,1310,300*v,40);g.restore()}
function crucifixS(g,t,ks){houseHall(g,t,ks,{hunt:ks>2.2});g.save();g.translate(540,1450);const glow=g.createRadialGradient(0,0,10,0,0,240);glow.addColorStop(0,`rgba(255,230,160,${.3+.2*Math.sin(t*3)})`);glow.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=glow;g.fillRect(-240,-240,480,480);
  g.fillStyle='#c8a050';g.fillRect(-14,-150,28,240);g.fillRect(-80,-90,160,28);g.restore();g.save();g.font='44px VT';g.fillStyle='#e9e2d2';g.textAlign='center';g.fillText('USOS: '+(ks>3.4?1:2)+'/2',540,1680);g.restore()}
const SC={house:(g,t,ks)=>houseHall(g,t,ks,{ghost:ks>1.8,gz:7}),mic:micS,name:(g,t,ks)=>{houseHall(g,t,ks,{hunt:ks>.6,ghost:true,gz:lerp(7,2.4,clamp(ks/3))});emf(g,t,ks,ks>.6?5:2)},sanity:sanityS,crucifix:crucifixS,houseend:(g,t,ks)=>houseHall(g,t,ks,{ghost:true,gz:4})};
