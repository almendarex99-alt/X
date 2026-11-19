import math, json, sys, wave, random
import numpy as np
from PIL import Image, ImageDraw
from multiprocessing import Pool
W,H=540,960; S=3; OUT=1080,1920; FPS=30
TL=json.load(open("timeline.json")); SC=TL["scenes"]; TOTAL=TL["total"]
def new(c1,c2):
    a=np.zeros((H*S//4,1,3),np.float32)
    t=np.linspace(0,1,a.shape[0])[:,None]
    a[:,0,:]=np.array(c1)[None,:]*(1-t)+np.array(c2)[None,:]*t
    im=Image.fromarray(a.astype(np.uint8)).resize((W*S,H*S),Image.BILINEAR)
    return im
class D:
    def __init__(s,im): s.im=im; s.d=ImageDraw.Draw(im,"RGBA")
    def R(s,x0,y0,x1,y1,c,r=0,o=None,ow=0):
        s.d.rounded_rectangle([x0*S,y0*S,x1*S,y1*S],radius=r*S,fill=c,outline=o,width=int(ow*S))
    def E(s,cx,cy,rx,ry,c,o=None,ow=0): s.d.ellipse([(cx-rx)*S,(cy-ry)*S,(cx+rx)*S,(cy+ry)*S],fill=c,outline=o,width=int(ow*S))
    def P(s,pts,c): s.d.polygon([(x*S,y*S) for x,y in pts],fill=c)
    def L(s,x0,y0,x1,y1,c,w=2): s.d.line([x0*S,y0*S,x1*S,y1*S],fill=c,width=int(w*S))
    def A(s,cx,cy,rx,ry,a0,a1,c,w=2): s.d.arc([(cx-rx)*S,(cy-ry)*S,(cx+rx)*S,(cy+ry)*S],a0,a1,fill=c,width=int(w*S))
def rnd(i,k=0): return ((i*9301+49297+k*233)%233280)/233280.0
def sm(t): t=max(0,min(1,t)); return t*t*(3-2*t)
# ---------- escenas ----------
def errico(d,cx,cy,sc,a=255):
    d.E(cx,cy,48*sc,48*sc,(230,40,50,a)); d.E(cx,cy,48*sc,48*sc,None,(255,255,255,a),3*sc)
    d.R(cx-6*sc,cy-28*sc,cx+6*sc,cy+6*sc,(255,255,255,a),3); d.E(cx,cy+22*sc,6.5*sc,6.5*sc,(255,255,255,a))
def sceneA(u,final=False):
    im=new((8,10,28),(26,12,44)); d=D(im)
    for k in range(40): d.E(30+rnd(k)*480,20+rnd(k,1)*160,1.4,1.4,(255,255,255,150))
    d.R(0,690,540,960,(18,14,30)); d.R(40,720,500,770,(30,26,48),6)
    d.R(60,190,480,650,(36,36,52),26); d.R(80,212,460,616,(6,22,14),12)
    for k in range(16):
        y=230+k*24-(u*36)%24
        if y<222 or y>600: continue
        n=int(rnd(k+int(u*1.5)%7*3)*10)
        x=96+(n%4)*14
        for j in range(3+n%4):
            w=22+int(rnd(k*7+j)*56); c=(60,220,120,230) if (k+j)%3 else (120,255,200,230)
            d.R(x,y,x+w,y+10,c,3); x+=w+8
    # linea con error
    blink=(int(u*3)%2==0)
    if blink: d.R(86,396,454,424,(255,40,60,110),6)
    d.R(96,402,300,418,(255,90,100,240),4)
    errico(d,270,130,1.0+0.1*math.sin(u*8)) if (blink or u<.6) else errico(d,270,130,.9,130)
    d.R(240,650,300,690,(26,24,40)); d.R(190,688,350,700,(26,24,40),4)
    return im
def person(d,cx,cy,sc,hair,shirt,phase=0,laugh=False,back=False):
    dy=math.sin(phase*14)*3*sc if laugh else 0
    d.R(cx-34*sc,cy+30*sc+dy,cx+34*sc,cy+120*sc,shirt,18*sc)
    d.E(cx,cy+dy,28*sc,31*sc,(244,200,160))
    d.E(cx,cy-12*sc+dy,29*sc,22*sc,hair)
    if not back:
        if laugh:
            d.A(cx-11*sc,cy-2*sc+dy,6*sc,5*sc,200,340,(40,30,30),2*sc); d.A(cx+11*sc,cy-2*sc+dy,6*sc,5*sc,200,340,(40,30,30),2*sc)
            d.d.pieslice([(cx-13*sc)*S,(cy+6*sc+dy)*S,(cx+13*sc)*S,(cy+26*sc+dy)*S],0,180,fill=(120,30,40,255))
        else:
            d.E(cx-10*sc,cy,3*sc,3*sc,(40,30,30)); d.E(cx+10*sc,cy,3*sc,3*sc,(40,30,30)); d.A(cx,cy+8*sc,9*sc,6*sc,20,160,(40,30,30),2*sc)
def monitor(d,x,y,w,h,mini=None,u=0):
    d.R(x,y,x+w,y+h,(50,48,64),8); d.R(x+6,y+6,x+w-6,y+h-8,(8,26,18),4)
    d.R(x+w/2-12,y+h,x+w/2+12,y+h+14,(40,38,54)); d.R(x+w/2-30,y+h+12,x+w/2+30,y+h+20,(40,38,54),3)
    if mini=="code":
        for k in range(int((h-20)/12)):
            ww=20+rnd(k+int(u*2))*(w-60); d.R(x+14,y+12+k*12,x+14+ww,y+19+k*12,(70,230,130,220),2)
    elif mini=="chase":
        d.R(x+6,y+6,x+w-6,y+h-8,(46,50,60),4)
        for k in range(4): d.R(x+w/2-2,((u*50+k*26)%(h-16))+y+6,x+w/2+2,((u*50+k*26)%(h-16))+y+16,(240,240,240,200))
        d.R(x+w/2+6,y+h-34,x+w/2+18,y+h-14,(235,60,60)); d.R(x+w/2-18,y+h-52+math.sin(u*9)*3,x+w/2-6,y+h-32,(240,240,255))
def sceneB(u):
    im=new((70,44,86),(30,26,56)); d=D(im)
    zoom=1+0.05*u/8
    d.R(40,80,180,220,(30,22,50),6); d.R(48,88,172,212,(255,170,90,120),4)  # ventana
    for k,c in enumerate([(235,90,120),(90,170,235),(250,200,80)]): d.R(220+k*90,90,290+k*90,170,c+(200,),4)
    d.R(0,620,540,960,(34,26,50))
    d.R(30,560,510,610,(78,56,90),8)
    monitor(d,80,380,170,130,"code",u); monitor(d,290,380,170,130,"code",u+.7)
    person(d,150,690,1.35,(60,40,30),(70,120,200),back=True); person(d,390,700,1.35,(200,140,60),(220,90,110),back=True)
    d.R(70,780,230,800,(120,80,60),5); d.R(310,790,470,810,(120,80,60),5)
    d.E(260,840,16,12,(250,250,250)); d.R(250,860,272,886,(250,250,250),4)
    return im
def car(d,cx,cy,w,h,body,roof,light=None,ph=0,shake=0):
    cx+=shake
    d.R(cx-w/2-3,cy-h/2+8,cx-w/2+3,cy-h/2+30,(15,15,18),2); d.R(cx+w/2-3,cy-h/2+8,cx+w/2+3,cy-h/2+30,(15,15,18),2)
    d.R(cx-w/2-3,cy+h/2-30,cx-w/2+3,cy+h/2-8,(15,15,18),2); d.R(cx+w/2-3,cy+h/2-30,cx+w/2+3,cy+h/2-8,(15,15,18),2)
    d.R(cx-w/2,cy-h/2,cx+w/2,cy+h/2,body,14)
    d.R(cx-w/2+6,cy-h/2+18,cx+w/2-6,cy-h/2+36,(40,60,90,230),5)
    d.R(cx-w/2+8,cy-h/2+40,cx+w/2-8,cy+h/2-32,roof,6)
    d.R(cx-w/2+6,cy+h/2-30,cx+w/2-6,cy+h/2-14,(40,60,90,230),5)
    if light:
        a=int(ph*8)%2
        d.R(cx-w/2+8,cy-6,cx-2,cy+6,(255,40,50) if a else (40,40,90),3); d.R(cx+2,cy-6,cx+w/2-8,cy+6,(60,120,255) if not a else (40,40,90),3)
        g=(255,40,50,70) if a else (60,120,255,70)
        d.E(cx,cy,w*1.1,w*1.1,g)
def road(d,u,speed=300):
    d.R(0,0,540,960,(26,34,52)); 
    for k in range(10):
        y=((k*130+u*speed*.6)%1300)-170; d.R(10+(k%2)*8,y,90,y+90,(50,64,96)); d.R(450,y+40,520-(k%2)*8,y+130,(50,64,96))
    d.R(120,0,420,960,(52,54,64)); d.R(116,0,121,960,(220,200,80)); d.R(419,0,424,960,(220,200,80))
    for k in range(14): y=((k*80+u*speed)%1120)-80; d.R(268,y,274,y+44,(230,230,230))
def sceneC(u):
    im=new((10,12,24),(10,12,24)); d=D(im); road(d,u)
    bump=max(0,math.sin(u*5.2)) ** 6
    py=620+ (bump*10)
    cy=py+120-bump*110 + math.sin(u*2)*8
    sh=math.sin(u*40)*6*bump
    car(d,270+math.sin(u*2.1)*40,py,92,170,(238,238,244),(30,30,44),True,u,sh)
    car(d,270+math.sin(u*2.1)*40+ math.sin(u*3)*10,cy+80,92,170,(24,24,30),(240,240,240),True,u+.5,0)
    if bump>.4:
        for k in range(6): a=k*math.pi/3+u*3; d.L(270+math.sin(u*2.1)*40+math.cos(a)*38,py+170+math.sin(a)*18,270+math.sin(u*2.1)*40+math.cos(a)*70,py+170+math.sin(a)*38,(255,230,120,220),4)
    return im
def sceneD(u):
    im=new((92,52,100),(36,26,62)); d=D(im)
    monitor(d,150,150,240,190,"chase",u)
    for k in range(6): d.E(60+k*84,70+math.sin(u*3+k)*8,10,10,(255,220,120,90))
    d.R(0,640,540,960,(34,26,50)); d.R(60,620,480,660,(78,56,90),8)
    person(d,170,500,1.6,(60,40,30),(70,120,200),u,True); person(d,370,505,1.6,(200,140,60),(220,90,110),u+.4,True)
    return im
def sceneE(u):
    im=new((10,12,24),(10,12,24)); d=D(im); road(d,u,360)
    p=sm((u-1.6)/1.6); 
    xr=270+60*math.sin(u*2); 
    cop_y=360+(620-360)*p; red_y=620+(360-620)*p
    # coches
    car(d,xr-30*(1-p),red_y,92,170,(215,36,52),(120,20,32),False)
    car(d,xr+30*(p),cop_y,92,170,(238,238,244),(30,30,44),True,u)
    cx,cy=270,200
    d.E(cx,cy,64,64,(255,255,255,40)); d.A(cx,cy,48,48,40,320,(255,240,120,255),8)
    d.P([(cx+40,cy-50),(cx+74,cy-34),(cx+34,cy-24)],(255,240,120,255))
    return im
def sceneF(u):
    im=new((24,10,56),(255,88,160)); d=D(im)
    for k in range(60): d.E(rnd(k)*540,rnd(k,1)*380,1.2,1.2,(255,255,255,170))
    d.E(270,470,90,90,(255,200,120,230))
    # skyline
    for k in range(16):
        x=((k*58-u*10)%700)-80; h=160+rnd(k)*230; w=46+rnd(k,2)*30
        d.R(x,560-h,x+w,640,(20,14,44)); 
        for r in range(int(h/22)):
            for c in range(int(w/14)):
                if rnd(k*31+r*7+c)>.45: d.R(x+6+c*14,560-h+10+r*22,x+14+c*14,560-h+20+r*22,(255,220,130,200) if rnd(r+c+k,3)>.3 else (120,220,255,200))
        if k%5==0: d.R(x+6,560-h-18,x+w-6,560-h-8,(60,255,230,230),3)
    d.R(0,640,540,960,(18,14,34))
    for k in range(12):
        t=((k/12)+u*.5)%1; y=640+t*t*320; wd=20+t*180
        d.R(270-wd,y,270+wd,y+3+t*10,(60,50,90,255)); 
    d.P([(270,640),(40,960),(500,960)],(40,36,62,230))
    for k in range(8): t=((k/8)+u*.8)%1; d.L(270+(-1 if k%2 else 1)*t*20,640+t*t*320,270+(-1 if k%2 else 1)*t*190,640+t*t*320+t*60,(255,240,200,200),2+t*5)
    car(d,270,820,100,140,(215,36,52),(120,20,32),False)
    return im
def sceneG(u):
    im=new((8,10,28),(30,16,50)); d=D(im)
    for k in range(18):
        a=k*math.pi/9+u*.4; d.P([(270,430),(270+math.cos(a-.08)*700,430+math.sin(a-.08)*700),(270+math.cos(a+.08)*700,430+math.sin(a+.08)*700)],(255,255,255,12))
    p=sm((u-1.0)/.6)
    if p<1: errico(d,270,430,2.6*(1-p),int(255*(1-p)))
    if p>0:
        s=2.7*(.2+.8*p)*(1+.1*math.sin((u-1)*10)*max(0,1-(u-1)*1.5))
        d.E(270,430,100*s/1.8,100*s/1.8,(40,200,100,255)); d.E(270,430,100*s/1.8,100*s/1.8,None,(255,255,255,255),6)
        d.L(270-44*s/1.8,430+4*s/1.8,270-10*s/1.8,430+36*s/1.8,(255,255,255),14*s/1.8); d.L(270-10*s/1.8,430+36*s/1.8,270+50*s/1.8,430-30*s/1.8,(255,255,255),14*s/1.8)
        for k in range(24):
            a=k*.26; r=(u-1)*160*rnd(k,5)+20; d.E(270+math.cos(a)*r*1.6,430+math.sin(a)*r*1.6+ (u-1)*30,5,5,[(255,220,80),(80,220,255),(255,100,150)][k%3]+(220,))
    return im
SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def glitch(im,amount,seed):
    a=np.array(im); rng=np.random.default_rng(seed); h=a.shape[0]
    for _ in range(int(14*amount)):
        y=int(rng.integers(0,h-60)); hh=int(rng.integers(20,160)); a[y:y+hh]=np.roll(a[y:y+hh],int(rng.integers(-180,180)),axis=1)
    a[:,:,0]=np.roll(a[:,:,0],int(14*amount),axis=1); a[:,:,2]=np.roll(a[:,:,2],-int(14*amount),axis=1)
    return Image.fromarray(a)
def frame(i):
    t=i/FPS
    idx=0
    for k,s in enumerate(SC):
        if t>=s["start"]: idx=k
    s=SC[idx]; u=t-s["start"]
    im=SCN[idx](u)
    g=0
    if idx==0 and u<.5: g=1-u/.5
    if idx==7 and t>TOTAL-1.0: g=(t-(TOTAL-1.0))/1.0
    # transicion corta: destello de entrada
    f=im.resize(OUT,Image.LANCZOS)
    if g>0: f=glitch(f,g,i)
    if idx>0 and u<.12:
        a=np.array(f).astype(np.float32); a=a*(u/.12)+0*(1-u/.12); f=Image.fromarray(a.astype(np.uint8))
    f.save(f"fr/f{i:05d}.png",compress_level=1)
    return i
if __name__=="__main__":
    n=int(TOTAL*FPS)
    a=[int(x) for x in sys.argv[1:3]] if len(sys.argv)>2 else [0,n]
    import os; os.makedirs("fr",exist_ok=True)
    with Pool(4) as p:
        for _ in p.imap_unordered(frame,range(a[0],min(a[1],n)),chunksize=4): pass
