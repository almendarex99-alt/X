import math, random, sys
from PIL import Image, ImageDraw
W,H,S,FPS,N=1280,720,2,24,120
out=sys.argv[1]
random.seed(3)
drops=[(random.uniform(-1,1),random.uniform(.6,1.3),random.uniform(-1,1)) for _ in range(26)]
def E(d,cx,cy,rx,ry,fill,outline=None):
    d.ellipse([(cx-rx)*S,(cy-ry)*S,(cx+rx)*S,(cy+ry)*S],fill=fill,outline=outline,width=3*S if outline else 0)
for f in range(N):
    t=f/FPS
    im=Image.new("RGB",(W*S,H*S),(150,215,255)); d=ImageDraw.Draw(im)
    # sky gradient
    for y in range(0,H*S,4):
        k=y/(H*S); d.rectangle([0,y,W*S,y+4],fill=(int(130+60*k),int(205+30*k),255))
    # sun
    sx,sy=1100,110; 
    for i in range(12):
        a=i*math.pi/6+t*.5; d.line([sx*S,sy*S,(sx+90*math.cos(a))*S,(sy+90*math.sin(a))*S],fill=(255,225,90),width=8*S)
    E(d,sx,sy,55,55,(255,214,60)); E(d,sx-18,sy-8,6,8,(90,60,20)); E(d,sx+18,sy-8,6,8,(90,60,20))
    d.arc([(sx-22)*S,(sy)*S,(sx+22)*S,(sy+30)*S],20,160,fill=(90,60,20),width=4*S)
    # clouds
    for cx0,cy,sp in((200,120,20),(640,80,12),(900,200,16)):
        cx=(cx0+sp*t)%1500-100
        for dx,dy,r in((0,0,45),(-40,10,32),(40,10,34),(15,-18,32)): E(d,cx+dx,cy+dy,r*1.2,r,(255,255,255))
    # hills + ground
    E(d,250,560,520,200,(125,205,110)); E(d,1050,580,560,230,(105,195,100))
    d.rectangle([0,540*S,W*S,H*S],fill=(120,205,95))
    # flowers
    for i,fx in enumerate((90,210,420,860,1010,1180)):
        fy=600+(i%3)*30; sw=math.sin(t*3+i)*4
        d.line([fx*S,fy*S,(fx+sw)*S,(fy-40)*S],fill=(60,150,60),width=5*S)
        col=[(255,120,170),(255,255,255),(255,170,60)][i%3]
        for k in range(6):
            a=k*math.pi/3; E(d,fx+sw+14*math.cos(a),fy-40+14*math.sin(a),10,10,col)
        E(d,fx+sw,fy-40,8,8,(255,220,60))
    # puddle
    px,py=640,590
    E(d,px,py,330,70,(70,150,225)); E(d,px,py-6,300,56,(110,185,250))
    # bounce
    cyc=(t*1.6)%1; hop=abs(math.sin(cyc*math.pi)); 
    bob=hop*150; air=hop>.08
    dy=-bob; squash=1-.16*(1-hop)**6 if hop<.2 else 1
    # ripples
    for k in range(3):
        ph=((t*1.6)-.0+k*.33)%1; r=ph; 
        E(d,px,py,60+r*260,10+r*50,None,(235,250,255)) if False else d.ellipse([(px-60-r*260)*S,(py-10-r*50)*S,(px+60+r*260)*S,(py+10+r*50)*S],outline=(235,250,255),width=int(4*S*(1-r)+1))
    # drops on landing
    land=(t*1.6)%1
    if land<.55:
        for i,(vx,vy,_) in enumerate(drops):
            tt=land/1.6*1.0
            x=px+vx*(150+60*vy)*land*1.8; y=py-vy*420*land+900*land*land
            if y<py+20: E(d,x,y,7,9,(190,230,255),(255,255,255))
    # shadow
    E(d,px,py+10,110-bob*.25,22-bob*.06,(50,110,190))
    # duck
    cx,cy=px,py-20+dy
    sw=squash
    # body
    E(d,cx,cy-55,95/sw*1.0,80*sw,(255,214,40))
    # wing
    ang=math.sin(t*14)*.3
    E(d,cx-70,cy-50+math.sin(t*14)*12,32,45,(255,190,30))
    E(d,cx+70,cy-50-math.sin(t*14)*12,32,45,(255,190,30))
    # feet
    for sgn in(-1,1): E(d,cx+sgn*45,cy+20,32,12,(255,140,30))
    # head
    hx,hy=cx,cy-165
    E(d,hx,hy,78,70,(255,226,60))
    # cheeks
    E(d,hx-48,hy+22,16,10,(255,150,130)); E(d,hx+48,hy+22,16,10,(255,150,130))
    # eyes
    blink=(t%2.0)<.12
    for sgn in(-1,1):
        if blink: d.line([(hx+sgn*30-14)*S,(hy-8)*S,(hx+sgn*30+14)*S,(hy-8)*S],fill=(30,20,20),width=5*S)
        else:
            E(d,hx+sgn*30,hy-8,17,21,(25,20,30)); E(d,hx+sgn*30+5,hy-15,7,8,(255,255,255)); E(d,hx+sgn*30-4,hy-2,3,3,(255,255,255))
    # beak (open smile)
    E(d,hx,hy+28,34,14,(255,140,30)); E(d,hx,hy+36,24,9,(200,70,60))
    # rain hat
    E(d,hx,hy-52,70,20,(225,40,50)); 
    d.pieslice([(hx-55)*S,(hy-98)*S,(hx+55)*S,(hy-8)*S],180,360,fill=(240,55,65))
    E(d,hx,hy-96,9,9,(255,255,255))
    im=im.resize((W,H),Image.LANCZOS); im.save(f"{out}/f{f:04d}.png")
