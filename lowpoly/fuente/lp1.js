// LP1 · "Surtidor 2" — historia de terror original en estilo low-poly (PS1), con el VHS de siempre
window.BED='drone';window.SUBS=true;window.NOZOOM_ALL=true;window.GRADE='rgba(70,100,140,.07)';
window.COVER_TEXT=['SURTIDOR','*2*'];window.DATE=(L)=>['ext_car','cctv_car','man','man_close','cctv_empty','hall','cctv_me'].includes(L.scene)?'AM 3:12':'NOCHE 3';
const T0=s=>LINES.find(l=>l.scene===s).t;window.COVER_AT=T0('man_close')+1.4;
window.EXTRA_CUES=[[T0('ext_car')-.2,'roll',{end:T0('ext_car')+3.5}],[T0('man')+.2,'coin'],[T0('man')+.5,'coin'],[T0('hall')+1.2,'knock'],[T0('ext_end')+3,'ring',{end:T0('ext_end')+6}],
  [T0('cctv_car'),'staticb',{end:T0('cctv_car')+3}],[T0('cctv_empty'),'staticb',{end:T0('cctv_empty')+3}],[T0('cctv_me'),'staticb',{end:T0('cctv_me')+3}]];
// ---------- motor 3D de baja resolución ----------
const RW=360,RH=640;const R=new THREE.WebGLRenderer({antialias:false,preserveDrawingBuffer:true});R.setPixelRatio(1);R.setSize(RW,RH);
const S3=new THREE.Scene();S3.background=new THREE.Color(0x04050a);S3.fog=new THREE.Fog(0x070910,10,60);
const CAM=new THREE.PerspectiveCamera(64,RW/RH,.05,300);
S3.add(new THREE.HemisphereLight(0x3a4a6a,0x0a0a10,.55));const MOON=new THREE.DirectionalLight(0x8090c0,.35);MOON.position.set(-20,30,10);S3.add(MOON);
function ps1(m){m.onBeforeCompile=sh=>{sh.vertexShader=sh.vertexShader.replace('#include <project_vertex>','#include <project_vertex>\n  vec4 sp=gl_Position;sp.xyz/=sp.w;sp.xy=floor(sp.xy*vec2(150.0,266.0))/vec2(150.0,266.0);sp.xyz*=sp.w;gl_Position=sp;')};return m}
const M=(c,o={})=>ps1(new THREE.MeshLambertMaterial(Object.assign({color:c,flatShading:true},o)));
const B=(w,h,d,mat,x,y,z,parent=S3)=>{const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat);m.position.set(x,y,z);parent.add(m);return m};
function texCanvas(w,h,draw){const c=document.createElement('canvas');c.width=w;c.height=h;draw(c.getContext('2d'),w,h);const t=new THREE.CanvasTexture(c);t.magFilter=THREE.NearestFilter;t.minFilter=THREE.NearestFilter;return t}
// persona low-poly
function human(shirt,opts={}){const g=new THREE.Group();const skin=M(0xb59a84),pant=M(0x1b1d24);
  B(.22,.85,.24,pant,-.13,.43,0,g);B(.22,.85,.24,pant,.13,.43,0,g);const torso=B(.6,.75,.32,M(shirt),0,1.25,0,g);B(.16,.68,.18,M(shirt),-.4,1.22,0,g);B(.16,.68,.18,M(shirt),.4,1.22,0,g);
  const head=new THREE.Mesh(new THREE.IcosahedronGeometry(.22,0),skin);head.position.set(0,1.85,0);g.add(head);
  if(opts.cap){B(.46,.1,.46,M(0xa01818),0,2.02,0,g);B(.3,.04,.2,M(0xa01818),0,1.98,.28,g)}
  const face=new THREE.Mesh(new THREE.PlaneGeometry(.34,.34),new THREE.MeshBasicMaterial({map:opts.face||FACE,transparent:true}));face.position.set(0,1.85,.215);g.add(face);g.userData.face=face;
  if(opts.tag)B(.12,.06,.02,M(0xd8d2c4,{emissive:0x222222}),.16,1.45,.17,g);S3.add(g);return g}
const FACE=texCanvas(32,32,(x,w,h)=>{x.fillStyle='rgba(0,0,0,.55)';x.fillRect(8,9,6,7);x.fillRect(18,9,6,7);x.fillStyle='#000';x.fillRect(10,12,3,3);x.fillRect(19,12,3,3);x.fillRect(12,23,8,1)});
const GRIN=texCanvas(32,32,(x,w,h)=>{x.fillStyle='#000';x.beginPath();x.ellipse(11,12,4,5,0,0,7);x.ellipse(21,12,4,5,0,0,7);x.fill();x.fillStyle='#eee';x.fillRect(11,12,1,1);x.fillRect(21,12,1,1);x.fillStyle='#3a0606';x.beginPath();x.moveTo(1,17);x.quadraticCurveTo(16,36,31,17);x.quadraticCurveTo(16,23,1,17);x.fill();x.fillStyle='#e8e0cc';for(let i=3;i<30;i+=2)x.fillRect(i,19+Math.abs(16-i)*.15,1,3)});
// ---------- EXTERIOR: gasolinera ----------
const ground=new THREE.Mesh(new THREE.PlaneGeometry(400,400),M(0x101114));ground.rotation.x=-Math.PI/2;S3.add(ground);
const road=new THREE.Mesh(new THREE.PlaneGeometry(400,7),M(0x17181c));road.rotation.x=-Math.PI/2;road.position.set(0,.01,9);S3.add(road);
for(let x=-190;x<190;x+=6)B(2.6,.02,.18,M(0x8a7a40),x,.02,9);
B(11,.45,7.5,M(0x2a2c33),0,4.4,0);B(11.2,.5,.2,M(0xb8b4a8,{emissive:0x3a3a3a}),0,4.4,3.8);[[-5,-3],[5,-3],[-5,3],[5,3]].forEach(([x,z])=>B(.35,4.2,.35,M(0x3a3c44),x,2.1,z));
const panels=[-3,0,3].map(x=>B(1.6,.06,4,M(0xfff4d6,{emissive:0xfff0c8}),x,4.15,0));
const L1=new THREE.PointLight(0xfff0d0,2.6,26);L1.position.set(0,3.6,0);S3.add(L1);
[[-2.4,0],[2.4,0]].forEach(([x,z],i)=>{B(.9,1.7,.6,M(0x8a1c1c),x,.85,z);B(.6,.4,.05,M(0x0a2a20,{emissive:0x1a6a4a}),x,1.35,z+.33);
  const t=texCanvas(32,32,(c)=>{c.fillStyle='#e9e2d2';c.fillRect(0,0,32,32);c.fillStyle='#111';c.font='bold 26px sans-serif';c.textAlign='center';c.fillText(String(i+1),16,26)});
  const p=new THREE.Mesh(new THREE.PlaneGeometry(.4,.4),new THREE.MeshBasicMaterial({map:t}));p.position.set(x,1.85,z+.31);S3.add(p)});
// tienda
B(10,3.4,6,M(0x3a3d36),0,1.7,-9);B(10.4,.5,6.4,M(0x2a2c30),0,3.6,-9);
const winM=M(0xf2e6b0,{emissive:0x9a8a50});B(3.2,1.6,.05,winM,-2.8,1.5,-5.98);B(2.2,1.6,.05,winM,2.6,1.5,-5.98);B(1.2,2.2,.05,M(0x1a2a30,{emissive:0x263540}),.2,1.1,-5.98);
const sign=texCanvas(64,32,(c)=>{c.fillStyle='#120c0a';c.fillRect(0,0,64,32);c.fillStyle='#ff3b3b';c.font='bold 20px sans-serif';c.textAlign='center';c.fillText('24H',32,23)});
const sg=new THREE.Mesh(new THREE.PlaneGeometry(2.4,1.2),new THREE.MeshBasicMaterial({map:sign}));sg.position.set(0,4.4,-5.75);S3.add(sg);
const L2=new THREE.PointLight(0xffe0a0,1.4,12);L2.position.set(0,2.5,-4.5);S3.add(L2);
// árboles
for(let i=0;i<120;i++){const a=hash(i*3.1)*6.28,r=20+hash(i*7.7)*60;const x=Math.cos(a)*r,z=Math.sin(a)*r-10;if(Math.abs(z-9)<6)continue;const h=4+hash(i)*5;
  const c=new THREE.Mesh(new THREE.ConeGeometry(1.4+hash(i*2)*1.2,h,5),M(0x0c1a12));c.position.set(x,h/2+1,z);S3.add(c);B(.3,1.2,.3,M(0x1a120c),x,.6,z)}
// coche
const car=new THREE.Group();B(2,.75,4.2,M(0x3a0e12),0,.65,0,car);B(1.75,.65,2,M(0x2a0a0e),0,1.35,-.2,car);B(1.7,.5,.05,M(0x06080a,{emissive:0x05070a}),0,1.35,.81,car);
[[-1,1.3],[1,1.3],[-1,-1.3],[1,-1.3]].forEach(([x,z])=>{const w=new THREE.Mesh(new THREE.CylinderGeometry(.36,.36,.28,7),M(0x050505));w.rotation.z=Math.PI/2;w.position.set(x,.36,z);car.add(w)});
const driver=new THREE.Group();B(.5,.55,.3,M(0x0a0a0c),0,1.25,-.1,driver);const dh=new THREE.Mesh(new THREE.IcosahedronGeometry(.18,0),M(0x0a0a0c));dh.position.set(0,1.65,-.1);driver.add(dh);car.add(driver);
const carDoor=B(.06,.6,1.1,M(0x3a0e12),1.0,1.0,-.2,car);S3.add(car);
// ---------- INTERIOR (x=100) ----------
const IX=100;const roomBox=new THREE.Mesh(new THREE.BoxGeometry(10,3.2,8),M(0x6d7a6a,{side:THREE.BackSide}));roomBox.position.set(IX,1.6,0);S3.add(roomBox);
const tiles=texCanvas(16,16,(c)=>{for(let y=0;y<16;y++)for(let x=0;x<16;x++){c.fillStyle=(x>>2^y>>2)&1?'#cfcabd':'#9a958a';c.fillRect(x,y,1,1)}});tiles.wrapS=tiles.wrapT=THREE.RepeatWrapping;tiles.repeat.set(5,4);
const fl=new THREE.Mesh(new THREE.PlaneGeometry(10,8),ps1(new THREE.MeshLambertMaterial({map:tiles})));fl.rotation.x=-Math.PI/2;fl.position.set(IX,.01,0);S3.add(fl);
B(4.4,1.1,1,M(0x4a3a2a),IX,.55,1.2);B(.6,.35,.5,M(0x1c1c20),IX-.55,1.27,1.1);B(.3,.5,.3,M(0xc8a030),IX+.5,1.35,1.2);const mon=B(.7,.5,.4,M(0x1c1c20),IX+1.3,1.36,1.0);B(.6,.4,.02,M(0x203a2a,{emissive:0x2a6a3a}),IX+1.3,1.36,1.21);
for(let r=0;r<3;r++)for(let s=0;s<2;s++){B(2.6,.08,.5,M(0x3a3a3a),IX-3+s*6,.6+r*.7,-3.6);for(let k=0;k<8;k++)B(.22,.32,.3,M([0xc33,0x3a6,0xdc3,0x36c][(r+k+s)%4]),IX-4.1+s*6+k*.3,.82+r*.7,-3.6)}
const tubes=[-2.5,0,2.5].map(z=>B(2.2,.06,.2,M(0xffffff,{emissive:0xf4f8ff}),IX,3.15,z));
const IL=new THREE.PointLight(0xe8f0ff,1.8,14);IL.position.set(IX,2.9,0);S3.add(IL);
B(1.6,2.4,.1,M(0x0a1420,{emissive:0x0a1420}),IX,1.2,3.95);
const rulesT=texCanvas(128,160,(c,w,h)=>{c.fillStyle='#ece6d6';c.fillRect(0,0,w,h);c.fillStyle='#111';c.font='bold 16px sans-serif';c.fillText('REGLAS',36,22);c.font='11px sans-serif';
  ['1. Si un coche para con','las luces apagadas,','NO SALGAS.','','2. Si alguien pide la','llave del baño después','de las 3:00, dile que','ESTÁ ROTA.','','3. No contestes si te','llaman por tu nombre.'].forEach((l,i)=>c.fillText(l,8,44+i*11))});
const rules=new THREE.Mesh(new THREE.PlaneGeometry(.55,.7),ps1(new THREE.MeshLambertMaterial({map:rulesT})));rules.position.set(IX-4.97,1.6,.4);rules.rotation.y=Math.PI/2;S3.add(rules);
const man=human(0x2a4a8a,{cap:true,tag:true});man.position.set(IX,0,2.15);man.rotation.y=Math.PI;
const me=human(0x2a4a8a,{cap:true,tag:true});me.position.set(IX,0,-.4);
// ---------- PASILLO (x=200) ----------
const HX=200;const hallBox=new THREE.Mesh(new THREE.BoxGeometry(2.2,3,14),M(0x5a6455,{side:THREE.BackSide}));hallBox.position.set(HX,1.5,0);S3.add(hallBox);
const door=B(1,2.1,.08,M(0x3a3026),HX+.3,1.05,-6.9);door.rotation.y=.5;B(1.2,2.2,.05,M(0x000000),HX,1.1,-6.97);
const bt=texCanvas(64,32,(c)=>{c.fillStyle='#ddd';c.fillRect(0,0,64,32);c.fillStyle='#111';c.font='bold 18px sans-serif';c.textAlign='center';c.fillText('BAÑO',32,22)});const bs=new THREE.Mesh(new THREE.PlaneGeometry(.6,.3),new THREE.MeshBasicMaterial({map:bt}));bs.position.set(HX,2.5,-6.9);S3.add(bs);
const HL=new THREE.PointLight(0xe0f0d0,1.2,9);HL.position.set(HX,2.7,-2);S3.add(HL);B(.8,.05,.2,M(0xffffff,{emissive:0xe0f0d0}),HX,2.97,-2);
// ---------- render por escena ----------
function look(px,py,pz,tx,ty,tz,shake=.012,t=0){CAM.position.set(px+Math.sin(t*1.3)*shake,py+Math.sin(t*2.1)*shake,pz);CAM.lookAt(tx,ty,tz)}
function setCar(x,z,ry,drv=true,open=false){car.position.set(x,0,z);car.rotation.y=ry;driver.visible=drv;carDoor.rotation.y=open?.9:0;carDoor.position.x=open?1.4:1.0}
const DITH=(()=>{const c=document.createElement('canvas');c.width=4;c.height=4;const x=c.getContext('2d');const b=[0,8,2,10,12,4,14,6,3,11,1,9,15,7,13,5];b.forEach((v,i)=>{x.fillStyle=`rgba(0,0,0,${v/16*.5})`;x.fillRect(i%4,Math.floor(i/4),1,1)});return c})();
function draw3D(g,setup,t,cctv){const fk=flick(t,.5);L1.intensity=2.6*fk;IL.intensity=1.8*flick(t+3,.7);HL.intensity=1.2*flick(t+7,1);setup();
  tubes.forEach((m,i)=>m.material.emissive.setScalar(IL.intensity>1.2?.95:.3));R.render(S3,CAM);
  g.save();g.imageSmoothingEnabled=false;g.drawImage(R.domElement,0,0,W,H);g.globalAlpha=.35;for(let y=0;y<H;y+=12)for(let x=0;x<W;x+=12)0;g.restore();
  g.save();g.globalAlpha=.08;const p=g.createPattern(DITH,'repeat');g.setTransform(3,0,0,3,0,0);g.fillStyle=p;g.fillRect(0,0,W,H);g.restore();
  if(cctv){g.save();g.globalCompositeOperation='color';g.fillStyle='rgba(80,140,90,1)';g.globalAlpha=.55;g.fillRect(0,0,W,H);g.restore();noise(g,.18,t);
    g.save();g.font='54px VT';g.fillStyle='#e9e2d2';g.fillText(cctv,60,420);g.textAlign='right';g.fillText('03:'+String(12+Math.floor(t/60)).padStart(2,'0')+':'+String(Math.floor(t)%60).padStart(2,'0'),W-60,420);g.restore()}}
const carIn=()=>{const k=clamp((lineAt(T0('ext_car')+.01).t,0));};
const SC={
 ext_far:(g,t,ks)=>draw3D(g,()=>{setCar(60,9,Math.PI/2);man.visible=false;me.visible=false;look(lerp(-34,-20,ks/8),1.7,lerp(9,10,ks/8),0,1.6,-4,.02,t)},t),
 counter:(g,t,ks)=>draw3D(g,()=>{man.visible=false;me.visible=false;look(IX,1.65,-1.2+ks*.05,IX,1.3,4,.012,t)},t),
 rules:(g,t,ks)=>draw3D(g,()=>{look(IX-4.1+ks*.03,1.6,.4,IX-4.97,1.6,.4,.006,t)},t),
 ext_car:(g,t,ks)=>draw3D(g,()=>{const k=ease(clamp(ks/3.2));const x=lerp(30,4.4,k),z=k<.75?9:lerp(9,.4,(k-.75)/.25);setCar(x,z,k<.75?-Math.PI/2:-Math.PI/2+(k-.75)*4*Math.PI/2*.0+(-Math.PI/2*0));look(-.5,1.7,-5.6,3.5,1,1.5,.008,t)},t),
 cctv_car:(g,t,ks)=>draw3D(g,()=>{setCar(4.4,.4,-Math.PI/2);look(-6,5,7,3.5,.8,0,0,t)},t,'CAM 2 · SURTIDORES'),
 man:(g,t,ks)=>draw3D(g,()=>{man.visible=true;man.userData.face.material.map=FACE;look(IX,1.65,-1.0,IX,1.55,2.15,.012,t)},t),
 man_close:(g,t,ks)=>draw3D(g,()=>{man.visible=true;man.userData.face.material.map=ks>.4?GRIN:FACE;man.userData.face.material.needsUpdate=true;IL.intensity=.6;const z=lerp(1.15,1.6,clamp(ks/2.5));look(IX,1.84,z,IX,1.84,2.15,.004+(ks>.4?.012:0),t)},t),
 cctv_empty:(g,t,ks)=>draw3D(g,()=>{setCar(4.4,.4,-Math.PI/2,false,true);look(-6,5,7,3.5,.8,0,0,t)},t,'CAM 2 · SURTIDORES'),
 hall:(g,t,ks)=>draw3D(g,()=>{look(HX,1.6,lerp(5.5,0,clamp(ks/6)),HX+.2,1.3,-7,.02,t)},t),
 cctv_me:(g,t,ks)=>draw3D(g,()=>{man.visible=false;me.visible=true;me.rotation.y=ks>2.2?Math.PI*.15:0;look(IX+3,2.7,2.6,IX,1.3,-.4,0,t)},t,'CAM 1 · CAJA'),
 ext_end:(g,t,ks)=>draw3D(g,()=>{me.visible=false;const k=ease(clamp((ks-1)/5));setCar(lerp(4.4,-60,k),k>.05?9:.4,Math.PI/2,true);look(lerp(-8,-14,clamp(ks/10)),lerp(3,6,clamp(ks/10)),lerp(16,24,clamp(ks/10)),0,1,-2,.01,t)},t)};
