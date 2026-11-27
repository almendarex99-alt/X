// componentes de la tanda w
function tendrils(g,x,y,len,t,seed,grow,col='rgba(200,190,150,.85)',w=4){g.save();g.strokeStyle=col;g.lineCap='round';
  for(let i=0;i<9;i++){const a=-Math.PI/2+(hash(seed+i)-.5)*2.6,l=len*(.5+hash(seed*3+i)*.6)*grow;g.lineWidth=w*(1-i/14);g.beginPath();g.moveTo(x,y);
    const cx=x+Math.cos(a+.6)*l*.5+Math.sin(t*.8+i)*8,cy=y+Math.sin(a+.6)*l*.5,ex=x+Math.cos(a)*l,ey=y+Math.sin(a)*l;g.quadraticCurveTo(cx,cy,ex,ey);g.stroke();
    if(grow>.5){g.lineWidth=w*.4;g.beginPath();g.moveTo(ex,ey);g.lineTo(ex+Math.cos(a-.7)*l*.3,ey+Math.sin(a-.7)*l*.3);g.stroke()}}g.restore()}
function embers(g,t,n=40,col='255,140,60'){for(let i=0;i<n;i++){const x=(hash(i*3.3)*W+Math.sin(t+i)*30),y=H-((t*(40+hash(i)*80)+hash(i*7)*H)%H);g.fillStyle=`rgba(${col},${.3+.5*hash(i*5)})`;g.fillRect(x,y,3,3)}}
function skyline(g,t,y0,col,seed,hmax,win){let x=-40;let i=0;while(x<W+40){const w=60+hash(seed+i)*120,h=120+hash(seed*2+i)*hmax;g.fillStyle=col;g.fillRect(x,y0-h,w,h+600);
  if(win){for(let yy=y0-h+20;yy<y0-20;yy+=36)for(let xx=x+10;xx<x+w-14;xx+=24)if(hash(xx*.3+yy*.7+seed)>.82){g.fillStyle=`rgba(255,${150+hash(xx)*60},80,${.5+.4*flick(t+xx,.3)})`;g.fillRect(xx,yy,10,14)}}x+=w+6;i++}}
function mangrove(g,x,y,s,col){g.save();g.translate(x,y);g.scale(s,s);g.strokeStyle=col;g.fillStyle=col;g.lineWidth=10;
  for(let i=-3;i<=3;i++){g.beginPath();g.moveTo(i*12,-120);g.quadraticCurveTo(i*40,-40,i*55,10);g.stroke()}g.fillRect(-14,-420,28,300);
  for(let i=0;i<6;i++){g.beginPath();g.ellipse(-60+i*24,-430-hash(i)*60,90,50,0,0,7);g.fill()}g.restore()}
function statue(g,x,fy,h,t,o={}){const s=h/100;g.save();g.translate(x,fy);g.scale(s,s);
  const c=g.createLinearGradient(-20,-100,20,0);c.addColorStop(0,'#9a9486');c.addColorStop(1,'#5e5a50');g.fillStyle=c;
  g.beginPath();g.moveTo(-12,0);g.lineTo(-14,-55);g.quadraticCurveTo(-18,-70,-10,-78);g.lineTo(10,-78);g.quadraticCurveTo(18,-70,14,-55);g.lineTo(12,0);g.closePath();g.fill();
  g.beginPath();g.ellipse(0,-90,13,15,0,0,7);g.fill();g.strokeStyle='#6a665c';g.lineWidth=5;g.lineCap='round';g.beginPath();g.moveTo(-14,-70);g.lineTo(-22,-38);g.moveTo(14,-70);g.lineTo(22,-38);g.stroke();
  g.strokeStyle='#5a3a2a';g.lineWidth=1.4;[[-6,-60,-4,-50],[8,-40,12,-30],[-10,-20,-14,-8]].forEach(a=>{g.beginPath();g.moveTo(a[0],a[1]);g.lineTo(a[2],a[3]);g.stroke()});
  g.strokeStyle='#3a3a3a';g.lineWidth=1.8;g.beginPath();g.moveTo(-8,-2);g.lineTo(-10,6);g.moveTo(6,-4);g.lineTo(9,5);g.stroke();
  g.fillStyle='rgba(40,140,60,.9)';g.fillRect(-9,-96,6,4);g.fillRect(3,-96,6,4);g.fillStyle='rgba(170,30,30,.9)';g.beginPath();g.moveTo(-7,-84);g.quadraticCurveTo(0,-80,7,-84);g.lineTo(5,-82);g.quadraticCurveTo(0,-79,-5,-82);g.fill();
  g.fillStyle='rgba(0,0,0,.25)';g.fillRect(0,-100,14,100);g.restore()}
function creature(g,x,fy,h,t,open=0){const s=h/100;g.save();g.translate(x,fy);g.scale(s,s);g.fillStyle='#08090a';g.strokeStyle='#08090a';g.lineCap='round';
  g.lineWidth=4;[[-8,-50,-24,-24,-30,0],[8,-50,26,-22,32,0]].forEach(a=>{g.beginPath();g.moveTo(a[0],a[1]);g.lineTo(a[2],a[3]);g.lineTo(a[4],a[5]);g.stroke()});
  g.beginPath();g.moveTo(-14,-52);g.quadraticCurveTo(0,-78,14,-52);g.lineTo(8,-40);g.lineTo(-8,-40);g.closePath();g.fill();
  g.lineWidth=3.2;[[-12,-62,-40,-40,-46,-6],[12,-62,40,-42,48,-8]].forEach(a=>{g.beginPath();g.moveTo(a[0],a[1]);g.lineTo(a[2],a[3]);g.lineTo(a[4],a[5]);g.stroke()});
  g.save();g.translate(0,-80);g.beginPath();g.ellipse(0,0,10,13,0,0,7);g.fill();
  if(open>0){g.fillStyle='#3a1a14';g.beginPath();g.moveTo(-3,-10);g.lineTo(-16*open,-4);g.lineTo(-10,10);g.lineTo(0,4);g.lineTo(10,10);g.lineTo(16*open,-4);g.lineTo(3,-10);g.closePath();g.fill();
    g.strokeStyle='rgba(230,220,200,.7)';g.lineWidth=.8;for(let i=-3;i<=3;i++){g.beginPath();g.moveTo(i*3,0);g.lineTo(i*3.4,5);g.stroke()}}
  g.restore();g.restore()}
function swamp(g,t,ks,o={}){const s=g.createLinearGradient(0,0,0,H);s.addColorStop(0,'#05030c');s.addColorStop(.42,'#2a0d33');s.addColorStop(.55,'#0f4a52');s.addColorStop(.62,'#071216');s.addColorStop(1,'#020406');g.fillStyle=s;g.fillRect(0,0,W,H);
  // ciudad de neón lejana
  let x=0,i=0;while(x<W){const w=30+hash(i)*60,h=40+hash(i*3)*180;g.fillStyle='#120818';g.fillRect(x,1060-h,w,h);if(hash(i*7)>.5){g.fillStyle=hash(i)>.5?'rgba(255,60,170,.8)':'rgba(40,230,220,.8)';g.fillRect(x+6,1060-h+10,w-12,4)}x+=w+4;i++}
  const ng=g.createLinearGradient(0,900,0,1100);ng.addColorStop(0,'rgba(255,60,170,0)');ng.addColorStop(1,'rgba(255,60,170,.25)');g.fillStyle=ng;g.fillRect(0,900,W,200);
  // agua con reflejos
  g.fillStyle='#03080a';g.fillRect(0,1120,W,800);for(let k=0;k<40;k++){const y=1130+k*18,a=.12*(1-k/40);g.fillStyle=`rgba(255,80,180,${a})`;g.fillRect(W*.2+Math.sin(t*1.5+k)*40,y,W*.6*(1-k/50),3)}
  g.globalAlpha=.35;g.drawImage(FOG,-(t*10)%540,800,W*1.6,700);g.globalAlpha=1;
  mangrove(g,120,1180,1.1,'#020203');mangrove(g,980,1200,1.3,'#010102');mangrove(g,700,1120,.6,'#06040a');
  if(o.fig)o.fig();
  for(let k=0;k<26;k++){const fx=(hash(k*3.1)*W+Math.sin(t*.7+k)*30),fy=900+hash(k*1.7)*700+Math.sin(t+k)*20;g.fillStyle=`rgba(200,255,120,${.4+.5*Math.sin(t*3+k)})`;g.fillRect(fx,fy,4,4)}}
