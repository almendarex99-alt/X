// W1 · The Last of Us: el desayuno que acabó con el mundo
window.BED='drone';window.GRADE='rgba(255,140,60,.10)';window.COVER_TEXT=['EL HONGO','*EN TU PAN*'];
window.DATE=(L)=>({tv:'1968',factory:'SEP. 2003',flour:'SEP. 2003',globe:'26 SEP. 2003'}[L.scene]||'2003');
// raíces de hongo que crecen
function tendrils(g,x,y,len,t,seed,grow,col='rgba(200,190,150,.85)',w=4){g.save();g.strokeStyle=col;g.lineCap='round';
  for(let i=0;i<9;i++){const a=-Math.PI/2+(hash(seed+i)-.5)*2.6,l=len*(.5+hash(seed*3+i)*.6)*grow;g.lineWidth=w*(1-i/14);g.beginPath();g.moveTo(x,y);
    const cx=x+Math.cos(a+.6)*l*.5+Math.sin(t*.8+i)*8,cy=y+Math.sin(a+.6)*l*.5,ex=x+Math.cos(a)*l,ey=y+Math.sin(a)*l;g.quadraticCurveTo(cx,cy,ex,ey);g.stroke();
    if(grow>.5){g.lineWidth=w*.4;g.beginPath();g.moveTo(ex,ey);g.lineTo(ex+Math.cos(a-.7)*l*.3,ey+Math.sin(a-.7)*l*.3);g.stroke()}}g.restore()}
function embers(g,t,n=40,col='255,140,60'){for(let i=0;i<n;i++){const x=(hash(i*3.3)*W+Math.sin(t+i)*30),y=H-((t*(40+hash(i)*80)+hash(i*7)*H)%H);g.fillStyle=`rgba(${col},${.3+.5*hash(i*5)})`;g.fillRect(x,y,3,3)}}
function skyline(g,t,y0,col,seed,hmax,win){let x=-40;let i=0;while(x<W+40){const w=60+hash(seed+i)*120,h=120+hash(seed*2+i)*hmax;g.fillStyle=col;g.fillRect(x,y0-h,w,h+600);
  if(win){for(let yy=y0-h+20;yy<y0-20;yy+=36)for(let xx=x+10;xx<x+w-14;xx+=24)if(hash(xx*.3+yy*.7+seed)>.82){g.fillStyle=`rgba(255,${150+hash(xx)*60},80,${.5+.4*flick(t+xx,.3)})`;g.fillRect(xx,yy,10,14)}}x+=w+6;i++}}
function city(g,t,ks){const s=g.createLinearGradient(0,0,0,H);s.addColorStop(0,'#120806');s.addColorStop(.45,'#4a1a0c');s.addColorStop(.7,'#8a3a14');s.addColorStop(1,'#0a0504');g.fillStyle=s;g.fillRect(0,0,W,H);
  g.globalAlpha=.5;g.drawImage(FOG,-(t*15)%540,600,W*1.6,900);g.globalAlpha=1;
  skyline(g,t,1350,'#2a120b',11,520,false);skyline(g,t,1500,'#100605',29,640,true);
  const fg=g.createRadialGradient(540,1500,40,540,1500,700);fg.addColorStop(0,'rgba(255,120,40,.5)');fg.addColorStop(1,'rgba(255,120,40,0)');g.globalCompositeOperation='lighter';g.fillStyle=fg;g.fillRect(0,800,W,1120);g.globalCompositeOperation='source-over';
  // haz de helicóptero
  const hx=300+Math.sin(t*.5)*300;g.fillStyle='rgba(255,250,230,.08)';g.beginPath();g.moveTo(hx,380);g.lineTo(hx-160,1500);g.lineTo(hx+160,1500);g.fill();g.fillStyle='#050302';g.fillRect(hx-30,370,60,16);
  g.fillStyle='#050302';g.fillRect(0,1600,W,320);embers(g,t,60)}
function sTV(g,t,ks){g.fillStyle='#070605';g.fillRect(0,0,W,H);
  crtIn(g,160,820,760,580,(c,w,h)=>{c.fillStyle='#2a2a2a';c.fillRect(0,0,w,h);c.fillStyle='#4a4a4a';c.fillRect(0,h*.62,w,h);
    c.fillStyle='#111';[[w*.3,'#111'],[w*.68,'#151515']].forEach(([x])=>{c.beginPath();c.ellipse(x,h*.35,26,30,0,0,7);c.fill();c.fillRect(x-40,h*.42,80,h*.3);c.fillRect(x-60,h*.6,120,18)});
    c.strokeStyle='#888';c.lineWidth=3;c.beginPath();c.moveTo(w*.5,h*.62);c.lineTo(w*.5,h*.35);c.stroke();c.fillStyle='#aaa';c.fillRect(w*.5-10,h*.32,20,18);
    c.font='42px VT';c.fillStyle='#ddd';c.fillText('1968',24,48);c.globalAlpha=.3;c.drawImage(GRAIN[Math.floor(t*30)%6],0,0,w,h);c.globalAlpha=1});
  const rg=g.createRadialGradient(540,1110,80,540,1110,900);rg.addColorStop(0,'rgba(190,200,210,.14)');rg.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=rg;g.fillRect(0,0,W,H)}
function factory(g,t,ks){g.fillStyle='#0d0b08';g.fillRect(0,0,W,H);
  for(let i=0;i<5;i++){const x=80+i*230;g.fillStyle='#1b1712';g.fillRect(x,300,120,1300);g.fillStyle='#14110d';g.fillRect(x-20,280,160,40)}
  // haces de luz con polvo
  for(let i=0;i<3;i++){const x=200+i*330;const lg=g.createLinearGradient(x,0,x+220,1500);lg.addColorStop(0,'rgba(255,240,200,.18)');lg.addColorStop(1,'rgba(255,240,200,0)');g.fillStyle=lg;g.beginPath();g.moveTo(x,0);g.lineTo(x+80,0);g.lineTo(x+380,1500);g.lineTo(x+200,1500);g.fill()}
  for(let i=0;i<90;i++){const x=(hash(i*2.1)*W+Math.sin(t*.4+i)*40)%W,y=(hash(i*5.3)*H+t*12*(1+hash(i)))%H;g.fillStyle=`rgba(255,245,220,${.25+.4*hash(i)})`;g.fillRect(x,y,3,3)}
  // sacos de harina
  for(let r=0;r<4;r++)for(let c=0;c<4;c++){const x=120+c*220+(r%2)*60,y=1560-r*120;g.fillStyle='#d9cfb8';rr(g,x,y,200,110,26);g.fill();g.fillStyle='#8a1b1b';g.font='26px Anton';g.fillText('TEPUNG',x+40,y+50);g.fillStyle='#4a4030';g.font='20px VT';g.fillText('TERIGU · 25 KG',x+40,y+80)}
  tendrils(g,560,1440,420,t,7,clamp(ks/4),'rgba(220,205,160,.9)',6)}
function flour(g,t,ks){const s=g.createRadialGradient(540,1100,50,540,1100,1100);s.addColorStop(0,'#3a2e22');s.addColorStop(1,'#070504');g.fillStyle=s;g.fillRect(0,0,W,H);
  for(let i=0;i<140;i++){const a=hash(i)*6.28,r=(ks*90+hash(i*3)*600)%900;g.fillStyle=`rgba(245,238,220,${.5*(1-r/900)})`;g.beginPath();g.arc(540+Math.cos(a)*r,1150+Math.sin(a)*r*.6,2+hash(i*7)*4,0,7);g.fill()}
  const items=[['bread',280,1000],['cereal',800,980],['pancake',540,1320]];items.forEach(([n,x,y],i)=>{const by=y+Math.sin(t*1.3+i)*24,rot=Math.sin(t*.7+i)*.12;g.save();g.translate(x,by);g.rotate(rot);
    if(n==='bread'){g.fillStyle='#b8823f';g.beginPath();g.ellipse(0,0,150,80,0,Math.PI,0);g.fill();g.fillRect(-150,0,300,70);g.strokeStyle='#7a4f20';g.lineWidth=6;for(let k=-1;k<=1;k++){g.beginPath();g.moveTo(k*60-20,-50);g.lineTo(k*60+20,-10);g.stroke()}}
    if(n==='cereal'){g.fillStyle='#c4352a';g.fillRect(-90,-150,180,300);g.fillStyle='#f2d24a';g.font='44px Anton';g.textAlign='center';g.fillText('CEREAL',0,-60);g.fillStyle='#f0e6cc';g.beginPath();g.arc(0,40,55,0,7);g.fill()}
    if(n==='pancake'){for(let k=0;k<5;k++){g.fillStyle=k%2?'#c98a45':'#d89b55';g.beginPath();g.ellipse(0,-k*26,170,40,0,0,7);g.fill()}g.fillStyle='#e8c04a';g.fillRect(-30,-140,60,26)}
    g.restore();tendrils(g,x,by+60,160,t,i*9+3,clamp((ks-1)/3),'rgba(210,200,160,.75)',3)})}
function globe(g,t,ks){g.fillStyle='#030406';g.fillRect(0,0,W,H);const cx=540,cy=1100,r=380;const gg=g.createRadialGradient(cx-120,cy-120,40,cx,cy,r);gg.addColorStop(0,'#1d3a4a');gg.addColorStop(1,'#050b10');g.fillStyle=gg;g.beginPath();g.arc(cx,cy,r,0,7);g.fill();
  g.strokeStyle='rgba(120,170,190,.25)';g.lineWidth=2;for(let i=0;i<8;i++){const a=(i/8*Math.PI+t*.2)%Math.PI;g.beginPath();g.ellipse(cx,cy,Math.abs(Math.cos(a))*r,r,0,0,7);g.stroke()}for(let j=-3;j<=3;j++){g.beginPath();g.ellipse(cx,cy+j*r/4,Math.sqrt(1-(j/4)**2)*r,10,0,0,7);g.stroke()}
  const n=Math.floor(clamp(ks/2.5)*70);for(let i=0;i<n;i++){const a=hash(i*3.7)*6.28+t*.2,b=(hash(i*5.1)-.5)*2.4,x=cx+Math.cos(a)*Math.cos(b)*r*.95,y=cy+Math.sin(b)*r*.9;if(Math.sin(a)<0)continue;
    g.fillStyle='rgba(255,40,30,.9)';g.beginPath();g.arc(x,y,6+4*Math.sin(t*4+i),0,7);g.fill();const rg=g.createRadialGradient(x,y,0,x,y,40);rg.addColorStop(0,'rgba(255,40,30,.35)');rg.addColorStop(1,'rgba(255,40,30,0)');g.fillStyle=rg;g.fillRect(x-40,y-40,80,80)}}
function infected(g,x,fy,h,stage,t){const s=h/100;g.save();g.translate(x+Math.sin(t*3+x)*2,fy);g.scale(s,s);g.fillStyle='#050404';g.strokeStyle='#050404';g.lineCap='round';
  g.lineWidth=7;g.beginPath();g.moveTo(-5,-46);g.lineTo(-9,0);g.moveTo(5,-46);g.lineTo(8,0);g.stroke();g.beginPath();g.moveTo(-13,-80+stage*3);g.lineTo(13,-80);g.lineTo(11,-44);g.lineTo(-11,-44);g.closePath();g.fill();
  g.lineWidth=5;g.beginPath();g.moveTo(-12,-76);g.lineTo(-18-stage*3,-48);g.moveTo(12,-76);g.lineTo(18+stage*2,-46);g.stroke();
  g.save();g.translate(stage*2,-90+stage*2);g.rotate(stage*.12);g.beginPath();g.ellipse(0,0,8.5+stage*2,10+stage*1.5,0,0,7);g.fill();
  if(stage>=1){g.fillStyle='#2a2418';for(let p=0;p<stage*3;p++){const a=-Math.PI/2+(p-stage*1.5)*.5;g.beginPath();g.ellipse(Math.cos(a)*9,Math.sin(a)*9-2,5+stage,3+stage*.6,a,0,7);g.fill()}}
  if(stage>=3){g.fillStyle='#3a3020';g.beginPath();g.ellipse(-6,10,12,9,0,0,7);g.ellipse(8,16,10,8,0,0,7);g.fill()}g.restore();g.restore()}
function stages(g,t,ks){g.fillStyle='#0b0907';g.fillRect(0,0,W,H);const lg=g.createRadialGradient(540,1000,60,540,1000,800);lg.addColorStop(0,'rgba(170,150,110,.25)');lg.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=lg;g.fillRect(0,0,W,H);
  g.fillStyle='#050403';g.fillRect(0,1480,W,440);['CORREDOR','ACECHADOR','CHASQUEADOR','HINCHADO'].forEach((n,i)=>{const a=clamp((ks-i*.5)*2);if(a<=0)return;g.globalAlpha=a;infected(g,170+i*250,1480,i===3?520:440,i,t);
    g.font='30px VT';g.textAlign='center';g.fillStyle='#d9cfb8';g.fillText(n,170+i*250,1540);g.textAlign='left';g.globalAlpha=1})}
function clicker(g,t,ks){g.fillStyle='#040404';g.fillRect(0,0,W,H);const fx=540+Math.sin(t*.8)*160,fy=1100;const fl=g.createRadialGradient(fx,fy,20,fx,fy,520);fl.addColorStop(0,'rgba(220,230,240,.32)');fl.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=fl;g.fillRect(0,0,W,H);
  for(let i=0;i<4;i++){const r=((t*260+i*190)%760);g.strokeStyle=`rgba(230,220,190,${.45*(1-r/760)})`;g.lineWidth=5;g.beginPath();g.arc(540,1000,r,0,7);g.stroke()}
  infected(g,540,1900,1250,2,t)}
function crops(g,t,ks){const s=g.createLinearGradient(0,0,0,H);s.addColorStop(0,'#05070a');s.addColorStop(.5,'#14180f');s.addColorStop(1,'#050604');g.fillStyle=s;g.fillRect(0,0,W,H);g.fillStyle='#d8e2e4';g.beginPath();g.arc(820,380,50,0,7);g.fill();
  for(let r=0;r<12;r++){const z=r/12,y=lerp(1880,1000,z),sc=lerp(1,.2,z);for(let c=-8;c<=8;c++){const x=540+c*120*sc+Math.sin(t+r+c)*4*sc;g.strokeStyle=`rgba(${40+z*20},${60+z*20},30,1)`;g.lineWidth=6*sc;g.beginPath();g.moveTo(x,y);g.lineTo(x+Math.sin(t*1.2+c)*10*sc,y-120*sc);g.stroke()}}
  tendrils(g,540,1700,600,t,21,clamp(ks/3),'rgba(200,190,140,.7)',5);for(let i=0;i<60;i++){const x=hash(i*4.4)*W,y=(hash(i*2.2)*1500+t*-30*(1+hash(i)))%1500+300;g.fillStyle='rgba(220,210,170,.5)';g.fillRect(x,(y+1500)%1500+300,3,3)}}
function breakfast(g,t,ks){const s=g.createLinearGradient(0,0,0,H);s.addColorStop(0,'#2a1d12');s.addColorStop(1,'#0a0705');g.fillStyle=s;g.fillRect(0,0,W,H);
  const wg=g.createLinearGradient(700,0,200,1200);wg.addColorStop(0,'rgba(255,220,160,.35)');wg.addColorStop(1,'rgba(255,220,160,0)');g.fillStyle=wg;g.beginPath();g.moveTo(700,0);g.lineTo(1080,0);g.lineTo(600,1300);g.lineTo(100,1300);g.fill();
  g.fillStyle='#3a2716';g.fillRect(0,1250,W,700);g.fillStyle='#e8e1d0';g.beginPath();g.ellipse(540,1360,300,80,0,0,7);g.fill();for(let k=0;k<4;k++){g.fillStyle=k%2?'#c98a45':'#d89b55';g.beginPath();g.ellipse(540,1340-k*24,200,46,0,0,7);g.fill()}
  g.fillStyle='#d9cfb8';rr(g,820,1080,180,240,20);g.fill();g.fillStyle='#8a1b1b';g.font='30px Anton';g.fillText('HARINA',850,1180);tendrils(g,910,1090,300,t,33,clamp(ks/3),'rgba(230,220,180,.85)',5)}
const SC={city,tv:sTV,factory,flour,globe,stages,clicker,crops,breakfast};
