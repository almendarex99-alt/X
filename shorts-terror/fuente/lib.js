const W=1080,H=1920,F=560,VPY=880;
const C=document.getElementById('c'),ctx=C.getContext('2d');
const mk=(w,h)=>{const c=document.createElement('canvas');c.width=w;c.height=h;return c};
const BUF=mk(W,H),bx=BUF.getContext('2d');      // escena principal
const BUF2=mk(W,H),bx2=BUF2.getContext('2d');
const SMALL=mk(135,240),sx=SMALL.getContext('2d');   // segunda vista (giro / loop)
// ---------- utilidades ----------
const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
const lerp=(a,b,k)=>a+(b-a)*k;
const ease=k=>k<.5?4*k*k*k:1-Math.pow(-2*k+2,3)/2;
function hash(n){n=Math.sin(n*127.1+311.7)*43758.5453;return n-Math.floor(n)}
function flick(t,depth=1){const a=hash(Math.floor(t*22));const b=hash(Math.floor(t*7)+3);
  let v=1-.06*Math.sin(t*120);if(a>.93)v*=.25;if(b>.96)v*=.5;return lerp(1,v,depth)}
// ---------- capas precalculadas ----------
const GRAIN=[...Array(6)].map((_,i)=>{const c=mk(360,640),g=c.getContext('2d'),d=g.createImageData(360,640);
  for(let k=0;k<d.data.length;k+=4){const v=Math.random()*255;d.data[k]=d.data[k+1]=d.data[k+2]=v;d.data[k+3]=255}g.putImageData(d,0,0);return c});
const VIG=(()=>{const c=mk(W,H),g=c.getContext('2d'),r=g.createRadialGradient(W/2,H*.46,H*.18,W/2,H*.5,H*.72);
  r.addColorStop(0,'rgba(0,0,0,0)');r.addColorStop(1,'rgba(0,0,0,.92)');g.fillStyle=r;g.fillRect(0,0,W,H);return c})();
const SCAN=(()=>{const c=mk(W,H),g=c.getContext('2d');g.fillStyle='rgba(0,0,0,.16)';for(let y=0;y<H;y+=4)g.fillRect(0,y,W,2);return c})();
const FOG=(()=>{const c=mk(540,960),g=c.getContext('2d');for(let i=0;i<70;i++){const x=Math.random()*540,y=Math.random()*960,r=60+Math.random()*160,
  gr=g.createRadialGradient(x,y,0,x,y,r);gr.addColorStop(0,'rgba(220,220,214,.22)');gr.addColorStop(1,'rgba(220,220,214,0)');g.fillStyle=gr;g.fillRect(0,0,540,960)}return c})();

// ---------- pasillo 3D ----------
function shade(base,k,red){return `rgb(${Math.round(clamp(lerp(base[0],150,red)*k,0,255))},${Math.round(clamp(lerp(base[1],18,red)*k,0,255))},${Math.round(clamp(lerp(base[2],16,red)*k,0,255))})`}
function hall(g,o){
  const cam=o.cam||{x:0,y:0,z:0},yaw=o.yaw||0,red=o.red||0,lampZ=o.lampZ??5.2,fl=o.flick??1,dark=o.dark||0;
  const P=(x,y,z)=>{const zz=Math.max(z-cam.z,.12);return [W/2+yaw+F*(x-cam.x)/zz,VPY+F*(y-cam.y)/zz]};
  const poly=(pts,fill)=>{g.beginPath();pts.forEach((p,i)=>{const q=P(...p);i?g.lineTo(q[0],q[1]):g.moveTo(q[0],q[1])});g.closePath();g.fillStyle=fill;g.fill()};
  const L=(z,y)=>{const d=(z-lampZ)**2+(y+0.95)**2*.6;return (.07+1.5*fl/(1+d*.55))*Math.exp(-Math.max(z-cam.z,0)*.1)*(1-dark)};
  g.fillStyle='#000';g.fillRect(0,0,W,H);
  const ZB=9.2;
  // pared del fondo
  poly([[-1,-1.25,ZB],[1,-1.25,ZB],[1,1.25,ZB],[-1,1.25,ZB]],shade([125,118,92],L(ZB,0)*.9,red));
  // puerta del fondo
  poly([[-.42,-.8,ZB-.01],[.42,-.8,ZB-.01],[.42,1.25,ZB-.01],[-.42,1.25,ZB-.01]],shade([40,30,24],L(ZB,0),red));
  poly([[-.36,-.72,ZB-.02],[.30,-.72,ZB-.02],[.30,1.25,ZB-.02],[-.36,1.25,ZB-.02]],'#0a0706');
  if(o.doorGlow){poly([[.30,-.72,ZB-.02],[.36,-.72,ZB-.02],[.36,1.25,ZB-.02],[.30,1.25,ZB-.02]],`rgba(200,40,30,${o.doorGlow})`)}
  // segmentos de lejos a cerca
  const near=cam.z+.13;
  for(let z=ZB;z>near;z-=.3){const z2=Math.max(z-.3,near),zm=(z+z2)/2;
    poly([[-1,1.25,z],[1,1.25,z],[1,1.25,z2],[-1,1.25,z2]],shade([96,70,46],L(zm,1.25),red));     // suelo
    poly([[-1,-1.25,z],[1,-1.25,z],[1,-1.25,z2],[-1,-1.25,z2]],shade([118,112,90],L(zm,-1.25)*1.1,red)); // techo
    poly([[-1,-1.25,z],[-1,1.25,z],[-1,1.25,z2],[-1,-1.25,z2]],shade([132,124,96],L(zm,0)*.95,red));  // izq
    poly([[1,-1.25,z],[1,1.25,z],[1,1.25,z2],[1,-1.25,z2]],shade([126,118,92],L(zm,0)*.85,red));      // der
    // zócalo de madera inferior
    poly([[-1,.3,z],[-1,1.25,z],[-1,1.25,z2],[-1,.3,z2]],shade([70,50,34],L(zm,.8),red));
    poly([[1,.3,z],[1,1.25,z],[1,1.25,z2],[1,.3,z2]],shade([66,46,32],L(zm,.8),red));
  }
  // tablas del suelo
  g.lineWidth=2;
  for(let k=-4;k<=4;k++){const x=k*.22;const a=P(x,1.25,near),b=P(x,1.25,ZB);g.strokeStyle=`rgba(0,0,0,${.35})`;g.beginPath();g.moveTo(a[0],a[1]);g.lineTo(b[0],b[1]);g.stroke()}
  // molduras
  [[-1,.3],[1,.3],[-1,-1.25],[1,-1.25]].forEach(([x,y])=>{const a=P(x,y,near),b=P(x,y,ZB);g.strokeStyle='rgba(20,14,10,.6)';g.lineWidth=4;g.beginPath();g.moveTo(a[0],a[1]);g.lineTo(b[0],b[1]);g.stroke()});
  // cuadros pared izquierda
  [[2.2,2.9],[6.1,6.6]].forEach(([a,b],i)=>{if(b<near)return;const zm=(a+b)/2;
    poly([[-.995,-.62,a],[-.995,-.62,b],[-.995,.08,b],[-.995,.08,a]],shade([70,54,36],L(zm,-.3),red));
    poly([[-.99,-.55,a+.06],[-.99,-.55,b-.06],[-.99,.01,b-.06],[-.99,.01,a+.06]],shade(i?[60,48,52]:[42,46,40],L(zm,-.3)*.8,red))});
  // puerta lateral derecha (baño)
  if(4.3>near){poly([[.995,-.8,3.5],[.995,-.8,4.3],[.995,1.25,4.3],[.995,1.25,3.5]],shade([82,62,44],L(3.9,0),red));
    poly([[.99,-.72,3.56],[.99,-.72,4.24],[.99,1.25,4.24],[.99,1.25,3.56]],shade([60,44,32],L(3.9,0),red));
    const k=P(.985,.25,4.16);g.fillStyle=shade([180,160,110],L(3.9,0),red);g.beginPath();g.arc(k[0],k[1],Math.max(2,F*.025/Math.max(4.16-cam.z,.2)),0,7);g.fill()}
  // mesa con radio a la izquierda
  if(4.9>near){poly([[-.995,.45,4.4],[-.62,.45,4.4],[-.62,.45,4.9],[-.995,.45,4.9]],shade([60,40,26],L(4.6,.4),red));
    poly([[-.62,.45,4.4],[-.62,1.25,4.4],[-.62,1.25,4.45],[-.62,.45,4.45]],shade([40,28,18],L(4.6,.8),red));
    poly([[-.95,.2,4.5],[-.7,.2,4.5],[-.7,.45,4.5],[-.95,.45,4.5]],shade([52,36,24],L(4.6,.3),red));
    const d=P(-.77,.31,4.5);g.fillStyle=`rgba(255,60,40,${.5*fl})`;g.beginPath();g.arc(d[0],d[1],Math.max(1.5,F*.012/Math.max(4.5-cam.z,.2)),0,7);g.fill()}
  // lámpara colgante
  if(lampZ>near){const top=P(0,-1.25,lampZ),b=P(0,-.92,lampZ),zz=Math.max(lampZ-cam.z,.2);
    g.strokeStyle='#111';g.lineWidth=Math.max(1,F*.01/zz);g.beginPath();g.moveTo(top[0],top[1]);g.lineTo(b[0],b[1]);g.stroke();
    const r=F*1.7/zz,gr=g.createRadialGradient(b[0],b[1],0,b[0],b[1],r);gr.addColorStop(0,`rgba(255,226,150,${.38*fl*(1-dark)})`);gr.addColorStop(1,'rgba(255,226,150,0)');
    g.globalCompositeOperation='lighter';g.fillStyle=gr;g.fillRect(b[0]-r,b[1]-r,2*r,2*r);g.globalCompositeOperation='source-over';
    g.fillStyle=`rgba(255,240,200,${clamp(fl*(1-dark)+.05)})`;g.beginPath();g.arc(b[0],b[1],F*.06/zz,0,7);g.fill()}
  // Lisa en el pasillo
  if(o.lisa){const l=o.lisa;const zz=l.z-cam.z;if(zz>.15){const f=P(l.x,1.25,l.z);lisa(g,f[0],f[1],F*2.0/zz,l.a??1,o.t||0)}}
}
// ---------- Lisa (silueta original) ----------
function lisa(g,x,fy,h,a,t){
  g.save();g.globalAlpha=a;const s=h/100,j=(hash(Math.floor(t*14))-.5)*.6,twitch=hash(Math.floor(t*3))>.82?(hash(Math.floor(t*40))-.5)*.25:0;
  g.translate(x+j*s,fy);g.scale(s,s);
  // halo de luz detrás (la lámpara a su espalda)
  const hg=g.createRadialGradient(1,-84,2,1,-84,40);hg.addColorStop(0,'rgba(255,220,160,.20)');hg.addColorStop(1,'rgba(255,220,160,0)');g.fillStyle=hg;g.fillRect(-45,-130,90,90);
  g.shadowColor='rgba(0,0,0,.9)';g.shadowBlur=3;
  // piernas flacas
  g.strokeStyle='#8f8a7e';g.lineCap='round';g.lineWidth=2.2;
  g.beginPath();g.moveTo(-3,-32);g.quadraticCurveTo(-4.5,-16,-4,-1);g.moveTo(3.2,-32);g.quadraticCurveTo(4,-16,5,0);g.stroke();
  // vestido casi negro con bajo rasgado
  g.fillStyle='#120d0b';g.beginPath();g.moveTo(-8,-75);g.quadraticCurveTo(-13,-55,-13.5,-30);
  const hem=[-13.5,-11,-9,-6.5,-4,-1,2,5,8,11,13.5];hem.forEach((hx,i)=>g.lineTo(hx,-30+(i%2?4+hash(i)*3:0)));
  g.quadraticCurveTo(13.5,-55,8,-75);g.closePath();g.fill();
  g.fillStyle='rgba(70,8,8,.55)';g.beginPath();g.moveTo(-6,-52);g.quadraticCurveTo(-2,-40,-5,-31);g.lineTo(-9,-31);g.quadraticCurveTo(-8,-44,-6,-52);g.fill();
  // brazos largos hasta las rodillas
  g.strokeStyle='#7f796d';g.lineWidth=1.5;g.beginPath();g.moveTo(-8,-73);g.quadraticCurveTo(-14,-55,-12.5,-24);g.moveTo(8,-73);g.quadraticCurveTo(14.5,-56,13,-25);g.stroke();
  g.lineWidth=.8;g.beginPath();for(const [sx,d] of [[-12.5,-1],[13,1]]){for(let f=0;f<4;f++){g.moveTo(sx,-24.5);g.lineTo(sx+d*(f-1.5)*.7,-19.5+f*.3)}}g.stroke();
  // cuello y cabeza inclinada
  g.translate(1.5,-83);g.rotate(.26+twitch);
  g.strokeStyle='#8f8a7e';g.lineWidth=2.4;g.beginPath();g.moveTo(0,6);g.lineTo(-.5,10);g.stroke();
  g.fillStyle='#b9b2a2';g.beginPath();g.ellipse(0,0,5.8,7.6,0,0,7);g.fill();
  // pelo: mechones largos que tapan la cara
  g.shadowBlur=0;g.strokeStyle='#050404';g.lineCap='round';
  for(let i=-9;i<=9;i++){if(i===3||i===4)continue;const sx=i*.66,len=12+hash(i*3.1)*22,sway=Math.sin(t*1.3+i)*.6;g.lineWidth=.55+hash(i)*.55;
    g.beginPath();g.moveTo(sx*.55,-7.4+Math.abs(i)*.1);g.quadraticCurveTo(sx*1.05,3,sx*.95+sway,len);g.stroke()}
  g.fillStyle='#050404';g.beginPath();g.ellipse(0,-3.2,6.4,5,0,Math.PI,0);g.fill();
  // un ojo entre los mechones
  g.fillStyle='rgba(230,224,205,.95)';g.beginPath();g.ellipse(2.4,1.2,1.35,.7,.1,0,7);g.fill();g.fillStyle='#000';g.beginPath();g.arc(2.7,1.2,.5,0,7);g.fill();
  g.restore();
  // las piernas se pierden en la oscuridad
  const dg=g.createLinearGradient(0,fy-h*.42,0,fy);dg.addColorStop(0,'rgba(0,0,0,0)');dg.addColorStop(1,'rgba(0,0,0,.85)');g.fillStyle=dg;g.fillRect(0,fy-h*.42,W,h*.42+400);
}
// ---------- texto ----------
function segs(str){const out=[];str.split(/(\*[^*]+\*)/).forEach(p=>{if(!p)return;if(p[0]==='*')out.push([p.slice(1,-1),1]);else out.push([p,0])});return out}
function ttFix(y,o){if(!window.TIKTOK)return [y,o];o=Object.assign({},o);if(y>1300)y=1300+(y-1300)*.3;if(y>850){o.dx=(o.dx||0)-40;o.maxW=Math.min(o.maxW||880,780)}return [y,o]}
function big(g,str,y,size,age,o={}){
  if(age<0||window.COVERMODE)return;[y,o]=ttFix(y,o);const sc=1+.32*Math.exp(-age*16),al=clamp(age/.05);const S=segs(str);
  g.save();g.font=`${size}px Anton`;g.textBaseline='alphabetic';g.lineJoin='round';
  const tw=S.reduce((a,s)=>a+g.measureText(s[0]).width,0);const fit=Math.min(1,(o.maxW||880)/tw);
  g.translate(W/2+(o.dx||0),y);g.scale(sc*fit,sc*fit);g.globalAlpha=al*(o.alpha??1);
  const split=Math.max(0,16*Math.exp(-age*9))+(o.split||0);
  const draw=(dx,dy,mode,col)=>{let x=-tw/2;S.forEach(s=>{
     if(mode==='stroke'){g.strokeText(s[0],x+dx,dy)}else{g.fillStyle=col||(s[1]?'#e0162b':'#f2ece0');g.fillText(s[0],x+dx,dy)}
     x+=g.measureText(s[0]).width})};
  g.strokeStyle='rgba(0,0,0,.92)';g.lineWidth=size*.16;draw(0,0,'stroke');
  if(split>.5){g.globalCompositeOperation='lighter';draw(-split,0,'fill','rgba(255,0,40,.55)');draw(split,0,'fill','rgba(0,200,255,.45)');g.globalCompositeOperation='source-over'}
  draw(0,0,'fill');g.restore();
}
function small(g,str,y,age,o={}){
  if(age<0||window.COVERMODE)return;[y,o]=ttFix(y,o);const size=o.size||44,maxW=o.maxW||860,lh=size*1.32;
  g.save();g.font=`${o.weight||500} ${size}px Inter`;
  const lines=[];let cur='';str.split(' ').forEach(w=>{const tr=cur?cur+' '+w:w;if(g.measureText(tr).width>maxW&&cur){lines.push(cur);cur=w}else cur=tr});lines.push(cur);
  const n=Math.floor(age*46);if(n<=0){g.restore();return}
  const bw=Math.max(...lines.map(l=>g.measureText(l).width)),pad=22,top=y-size-14;
  g.fillStyle='rgba(0,0,0,.66)';g.fillRect(W/2+(o.dx||0)-bw/2-pad,top,bw+pad*2,lh*(lines.length-1)+size+34);
  g.fillStyle=o.color||'#e9e2d2';let left=n;
  lines.forEach((l,i)=>{const sh=l.slice(0,Math.max(0,left));left-=l.length+1;if(!sh)return;const x=W/2+(o.dx||0)-bw/2,yy=y+i*lh;g.fillText(sh,x,yy);
    if(left<0&&sh.length<l.length&&Math.floor(age*6)%2===0){g.fillRect(x+g.measureText(sh).width+4,yy-size+6,4,size-2)}});
  g.restore();
}
function osd(g,t,date){
  g.save();g.font='64px VT';g.fillStyle='rgba(240,240,232,.9)';g.shadowColor='rgba(0,0,0,.8)';g.shadowBlur=6;
  g.fillText(Math.floor(t*2)%2?'▶ PLAY':'▶',70,270);
  g.textAlign='right';g.fillText(date,W-70,270);
  const s=Math.floor(t)+33*60+3*3600;const hh=3,mm=33+Math.floor(t/60),ss=Math.floor(t)%60;
  g.fillText(`AM ${hh}:${String(mm).padStart(2,'0')}:${String(ss).padStart(2,'0')}`,W-70,334);
  g.restore();
}
function glitch(g,src,amt,t){ // bandas de tracking VHS
  if(amt<=0)return;const n=Math.floor(3+amt*10);
  for(let i=0;i<n;i++){const y=Math.floor(hash(i*13+Math.floor(t*30))*H),h=Math.floor(8+hash(i+t)*90*amt),dx=(hash(i*7+Math.floor(t*30))-.5)*240*amt;
    g.drawImage(src,0,y,W,h,dx,y,W,h)}
  g.fillStyle=`rgba(255,255,255,${.05*amt})`;g.fillRect(0,Math.floor(hash(Math.floor(t*30))*H),W,6);
}

function rr(g,x,y,w,h,r){g.beginPath();g.moveTo(x+r,y);g.arcTo(x+w,y,x+w,y+h,r);g.arcTo(x+w,y+h,x,y+h,r);g.arcTo(x,y+h,x,y,r);g.arcTo(x,y,x+w,y,r);g.closePath()}
const CUES=[];const cue=(t,type,x={})=>CUES.push(Object.assign({t,type},x));
function glitchAmt(t){let a=0;CUES.forEach(c=>{if(c.type==='glitch'){const d=t-c.t;if(d>=0&&d<.28)a=Math.max(a,1-d/.28)}});if(window.extraGlitch)a=Math.max(a,extraGlitch(t));return a}
function stamp(g,txt,x,y,age,col='#e0162b',rot=-.18,size=150){if(age<0)return;const sc=1+1.4*Math.exp(-age*14);g.save();g.translate(x,y);g.rotate(rot);g.scale(sc,sc);g.globalAlpha=clamp(age/.06)*.92;
  g.font=`${size}px Anton`;const w=g.measureText(txt).width;g.strokeStyle=col;g.lineWidth=12;g.strokeRect(-w/2-30,-size*.95,w+60,size*1.2);g.fillStyle=col;g.textAlign='center';g.fillText(txt,0,size*.05);g.restore()}
function noise(g,a,t){g.save();g.globalAlpha=a;g.imageSmoothingEnabled=false;g.drawImage(GRAIN[Math.floor(t*30)%6],0,0,W,H);g.restore()}