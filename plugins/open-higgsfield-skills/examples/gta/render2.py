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

# ---------- escenas (v2 con mas detalle) ----------
SK=(244,200,160); SK2=(222,170,132)
def shadow(d,cx,cy,rx,ry,a=70):
    for k in range(5): d.E(cx,cy,rx*(1+.1*k),ry*(1+.1*k),(0,0,0,a//3))
def bevel(d,x0,y0,x1,y1,c,r=6):
    d.R(x0,y0,x1,y1,c,r); d.R(x0+2,y0+2,x1-2,(y0+y1)/2,(255,255,255,36),r); d.R(x0+2,(y0+y1)/2,x1-2,y1-2,(0,0,0,40),r)
def errico(d,cx,cy,sc,a=255):
    d.E(cx,cy,48*sc,48*sc,(150,20,30,a)); d.E(cx,cy,44*sc,44*sc,(230,40,50,a)); d.E(cx-8*sc,cy-14*sc,28*sc,18*sc,(255,255,255,int(a*.18)))
    d.E(cx,cy,48*sc,48*sc,None,(255,255,255,a),3*sc)
    d.R(cx-6*sc,cy-28*sc,cx+6*sc,cy+6*sc,(255,255,255,a),3); d.E(cx,cy+22*sc,6.5*sc,6.5*sc,(255,255,255,a))
def keyboard(d,x,y,w,h):
    d.R(x,y,x+w,y+h,(40,38,58),5); d.R(x,y,x+w,y+3,(255,255,255,30),3)
    for r in range(3):
        for c in range(int(w/11)-1): d.R(x+5+c*11,y+4+r*(h-8)/3,x+13+c*11,y+4+r*(h-8)/3+5,(88,86,112),1.5)
def mug(d,x,y,u,col=(245,245,250)):
    shadow(d,x+2,y+24,16,4,60); bevel(d,x-14,y,x+14,y+24,col,5); d.A(x+16,y+11,9,8,-80,80,col,4)
    d.R(x-12,y+2,x+12,y+7,(90,50,30)); 
    for k in range(3): d.A(x-6+k*6,y-8-(u*14+k*4)%12,3,5,0,180,(255,255,255,int(150-((u*14+k*4)%12)*10)),1.5)
def monitor(d,x,y,w,h,mini=None,u=0,glare=True):
    shadow(d,x+w/2,y+h+24,w*.5,8,60)
    d.R(x+w/2-10,y+h,x+w/2+10,y+h+18,(34,32,48)); bevel(d,x+w/2-34,y+h+16,x+w/2+34,y+h+24,(52,50,70),4)
    bevel(d,x,y,x+w,y+h,(58,56,76),9); d.R(x+7,y+7,x+w-7,y+h-11,(6,22,16),5)
    d.E(x+w-14,y+h-5,2.2,2.2,(80,255,140))
    if mini=="code":
        for k in range(int((h-26)/12)):
            ww=18+rnd(k+int(u*2))*(w-70); xx=x+14+(k%3)*8
            d.R(xx,y+13+k*12,xx+ww,y+20+k*12,(70,230,130,225),2); d.R(xx+ww+4,y+13+k*12,xx+ww+4+rnd(k,9)*20,y+20+k*12,(255,200,90,200),2)
    elif mini=="chase":
        d.R(x+7,y+7,x+w-7,y+h-11,(46,50,60),5)
        for k in range(4): yy=((u*50+k*26)%(h-24))+y+8; d.R(x+w/2-2,yy,x+w/2+2,yy+10,(240,240,240,200))
        d.R(x+w/2+8,y+h-44,x+w/2+22,y+h-20,(235,60,60),3); d.R(x+w/2-22,y+h-62+math.sin(u*9)*3,x+w/2-8,y+h-38,(240,240,255),3)
    if glare: d.P([(x+10,y+8),(x+w*.55,y+8),(x+w*.25,y+h-12),(x+10,y+h-12)],(255,255,255,16))
def hair_front(d,cx,cy,sc,col,style):
    d.E(cx,cy-12*sc,31*sc,24*sc,col); d.E(cx,cy-18*sc,27*sc,16*sc,(255,255,255,26))
    if style==0:
        for k in range(5): d.P([(cx-26*sc+k*13*sc,cy-8*sc),(cx-18*sc+k*13*sc,cy-8*sc),(cx-22*sc+k*13*sc,cy+(2 if k%2 else 7)*sc)],col)
        d.E(cx-29*sc,cy,5*sc,12*sc,col); d.E(cx+29*sc,cy,5*sc,12*sc,col)
    else:
        d.E(cx,cy-38*sc,13*sc,11*sc,col); d.E(cx,cy-38*sc,13*sc,11*sc,None,(255,255,255,40),1.5*sc); d.R(cx-12*sc,cy-30*sc,cx+12*sc,cy-26*sc,(255,90,120),2*sc)
        d.E(cx-30*sc,cy+4*sc,6*sc,16*sc,col); d.E(cx+30*sc,cy+4*sc,6*sc,16*sc,col)
        d.P([(cx-26*sc,cy-6*sc),(cx+6*sc,cy-24*sc),(cx+27*sc,cy-6*sc),(cx+27*sc,cy+2*sc),(cx+2*sc,cy-12*sc),(cx-26*sc,cy+4*sc)],col)
def face(d,cx,cy,sc,laugh,glasses,beard,ph=0):
    d.E(cx-29*sc,cy+3*sc,5.5*sc,8.5*sc,SK2); d.E(cx+29*sc,cy+3*sc,5.5*sc,8.5*sc,SK2)
    d.E(cx,cy,28*sc,31*sc,SK); d.E(cx+8*sc,cy+10*sc,22*sc,20*sc,(255,255,255,0)); d.E(cx-12*sc,cy+14*sc,12*sc,12*sc,(0,0,0,12))
    d.E(cx-15*sc,cy+9*sc,6.5*sc,4*sc,(255,110,110,85)); d.E(cx+15*sc,cy+9*sc,6.5*sc,4*sc,(255,110,110,85))
    d.E(cx,cy+6*sc,3.2*sc,3.6*sc,SK2); 
    if beard:
        d.d.pieslice([(cx-27*sc)*S,(cy-2*sc)*S,(cx+27*sc)*S,(cy+34*sc)*S],20,160,fill=(60,42,32,170))
    if laugh:
        for sg in(-1,1):
            d.A(cx+sg*11*sc,cy-3*sc,6.5*sc,5.5*sc,200,340,(40,30,30),2.2*sc)
            d.L(cx+sg*17*sc,cy-12*sc,cx+sg*6*sc,cy-(13+sg*1)*sc,(70,45,30),2*sc)
        d.d.pieslice([(cx-14*sc)*S,(cy+8*sc)*S,(cx+14*sc)*S,(cy+28*sc)*S],0,180,fill=(120,28,38,255))
        d.d.pieslice([(cx-13*sc)*S,(cy+8*sc)*S,(cx+13*sc)*S,(cy+15*sc)*S],0,180,fill=(250,250,250,255))
        d.E(cx,cy+22*sc,7*sc,3.5*sc,(235,110,120))
    else:
        for sg in(-1,1):
            d.E(cx+sg*10.5*sc,cy-2*sc,6*sc,4.6*sc,(255,255,255)); d.E(cx+sg*10.5*sc,cy-2*sc,2.9*sc,2.9*sc,(40,30,30)); d.E(cx+sg*9.5*sc,cy-3.2*sc,1*sc,1*sc,(255,255,255))
            d.L(cx+sg*16*sc,cy-9*sc,cx+sg*6*sc,cy-9.5*sc,(70,45,30),2*sc)
        d.A(cx,cy+11*sc,9*sc,6*sc,20,160,(110,40,40),2*sc)
    if glasses:
        for sg in(-1,1): d.E(cx+sg*10.5*sc,cy-2*sc,8.5*sc,7*sc,None,(30,30,40),1.8*sc); d.E(cx+sg*10.5*sc-2*sc,cy-4*sc,4*sc,2*sc,(255,255,255,70))
        d.L(cx-2*sc,cy-3*sc,cx+2*sc,cy-3*sc,(30,30,40),1.8*sc)
def person_front(d,cx,cy,sc,which,u,laugh=True):
    ph=u*14; dy=math.sin(ph)*3*sc if laugh else 0
    shirt=(70,120,210) if which==0 else (222,84,110); hair=(58,40,30) if which==0 else (190,120,50)
    shadow(d,cx,cy+138*sc,50*sc,8*sc,60)
    d.R(cx-9*sc,cy+24*sc+dy,cx+9*sc,cy+46*sc+dy,SK2)
    bevel(d,cx-42*sc,cy+38*sc+dy,cx+42*sc,cy+138*sc,shirt,22*sc)
    if which==0:
        d.E(cx,cy+42*sc+dy,24*sc,10*sc,(shirt[0]-20,shirt[1]-20,shirt[2]-20)); d.L(cx-8*sc,cy+52*sc+dy,cx-9*sc,cy+82*sc+dy,(240,240,240),2*sc); d.L(cx+8*sc,cy+52*sc+dy,cx+9*sc,cy+82*sc+dy,(240,240,240),2*sc)
        d.R(cx-22*sc,cy+98*sc+dy,cx+22*sc,cy+118*sc+dy,(0,0,0,30),6*sc)
    else:
        d.P([(cx-12*sc,cy+38*sc+dy),(cx+12*sc,cy+38*sc+dy),(cx,cy+58*sc+dy)],SK); d.E(cx-34*sc,cy+10*sc+dy,2*sc,3*sc,(255,215,90))
    for sg in(-1,1):
        ax=cx+sg*46*sc; bevel(d,ax-10*sc,cy+52*sc+dy,ax+10*sc,cy+120*sc+dy,shirt,9*sc); d.E(ax,cy+126*sc+dy,10*sc,9*sc,SK)
    hair_front(d,cx,cy+dy,sc,hair,which)
    face(d,cx,cy+dy,sc,laugh,which==0,False,ph)
def person_back(d,cx,cy,sc,which,u):
    shirt=(70,120,210) if which==0 else (222,84,110); hair=(58,40,30) if which==0 else (190,120,50)
    chair=(44,32,60)
    shadow(d,cx,cy+148*sc,56*sc,8*sc,60)
    bevel(d,cx-48*sc,cy-20*sc,cx+48*sc,cy+120*sc,chair,18*sc); bevel(d,cx-20*sc,cy-34*sc,cx+20*sc,cy-8*sc,chair,8*sc)
    bevel(d,cx-40*sc,cy+34*sc,cx+40*sc,cy+138*sc,shirt,22*sc)
    d.L(cx,cy+40*sc,cx,cy+120*sc,(0,0,0,50),2*sc)
    if which==0: d.E(cx,cy+42*sc,26*sc,12*sc,(shirt[0]-25,shirt[1]-25,shirt[2]-25))
    d.R(cx-9*sc,cy+22*sc,cx+9*sc,cy+42*sc,SK2)
    d.E(cx-28*sc,cy+2*sc,5*sc,8*sc,SK2); d.E(cx+28*sc,cy+2*sc,5*sc,8*sc,SK2)
    d.E(cx,cy,29*sc,32*sc,hair); d.E(cx-6*sc,cy-12*sc,16*sc,9*sc,(255,255,255,30))
    for k in range(6): d.A(cx,cy,(8+k*4)*sc,(9+k*4)*sc,200+k*8,340-k*8,(0,0,0,45),1.2*sc)
    if which==1: d.E(cx,cy-36*sc,13*sc,11*sc,hair); d.R(cx-12*sc,cy-30*sc,cx+12*sc,cy-26*sc,(255,90,120),2*sc)
    for sg in(-1,1):
        ax=cx+sg*50*sc; bevel(d,ax-9*sc,cy+52*sc,ax+9*sc,cy+104*sc,shirt,8*sc)
def sceneA(u,final=False):
    im=new((8,10,28),(26,12,44)); d=D(im)
    for k in range(40): d.E(30+rnd(k)*480,20+rnd(k,1)*130,1.4,1.4,(255,255,255,150))
    d.E(90,90,32,32,(250,240,210,230)); d.E(80,80,7,7,(0,0,0,25)); d.E(100,100,5,5,(0,0,0,25))
    d.R(0,690,540,960,(18,14,30)); d.R(0,690,540,696,(255,255,255,18))
    shadow(d,270,700,230,12,70)
    bevel(d,60,190,480,650,(40,40,58),26); d.R(80,212,460,616,(6,22,14),12)
    for k in range(16):
        y=230+k*24-(u*36)%24
        if y<222 or y>600: continue
        n=int(rnd(k+int(u*1.5)%7*3)*10); x=96+(n%4)*14
        for j in range(3+n%4):
            w=22+int(rnd(k*7+j)*56); c=(60,220,120,230) if (k+j)%3 else (120,255,200,230)
            d.R(x,y,x+w,y+10,c,3); x+=w+8
    blink=(int(u*3)%2==0)
    if blink: d.R(86,396,454,424,(255,40,60,110),6)
    d.R(96,402,300,418,(255,90,100,240),4)
    errico(d,452,150,.78+.08*math.sin(u*8)) if (blink or u<.6) else errico(d,452,150,.7,130)
    d.P([(90,222),(300,222),(190,610),(90,610)],(255,255,255,14))
    d.E(270,634,3,3,(80,255,140))
    # post-its en el borde
    for k,(x,y,c) in enumerate([(66,236,(255,230,90)),(70,296,(255,150,180)),(448,330,(120,230,255))]):
        d.R(x,y,x+26,y+26,c+(255,),2); d.L(x+4,y+8,x+22,y+8,(0,0,0,60),1.5); d.L(x+4,y+14,x+18,y+14,(0,0,0,60),1.5)
    d.R(240,650,300,690,(30,28,46)); d.R(190,688,350,700,(30,28,46),4)
    keyboard(d,150,716,240,60); mug(d,450,730,u); 
    d.R(60,735,110,775,(250,250,245),2); d.L(66,745,104,745,(0,0,0,50),1.5); d.L(66,753,96,753,(0,0,0,50),1.5)
    return im
def sceneB(u):
    im=new((72,46,88),(32,26,58)); d=D(im)
    # ventana con ciudad
    bevel(d,36,70,196,236,(30,22,50),8); d.R(44,78,188,228,(255,160,100),4); d.R(44,150,188,228,(120,60,120),4)
    for k in range(7): d.R(48+k*20,150-(k*37%40),64+k*20,228,(60,30,80))
    d.L(116,78,116,228,(30,22,50),4); d.L(44,153,188,153,(30,22,50),4)
    # estante
    d.R(230,100,500,108,(110,70,50)); 
    for k,c in enumerate([(220,80,90),(90,150,230),(250,200,80),(120,200,140),(200,120,220),(240,140,80)]): d.R(236+k*14,70-(k%3)*6,246+k*14,100,c,2)
    d.R(330,70,352,100,(250,210,80),3); d.E(341,64,9,8,(250,210,80)); d.R(334,100,348,108,(160,120,50))
    d.R(380,70,400,100,(230,230,240),3); d.R(390,84,394,92,(60,60,200))
    # poster
    d.R(430,120,500,230,(250,250,240),3); d.R(436,126,494,180,(80,160,240),2); d.L(440,194,490,194,(0,0,0,60),2); d.L(440,204,478,204,(0,0,0,60),2)
    # planta
    d.R(470,610,520,660,(200,120,90),6); 
    for k in range(5): a=-1.2+k*.6; d.E(495+math.sin(a)*24,596-math.cos(a)*26,9,22,(60,170,90),None,0)
    d.R(0,630,540,960,(34,26,50)); d.R(0,630,540,636,(255,255,255,16))
    bevel(d,26,556,514,620,(88,62,100),10)
    monitor(d,70,372,180,138,"code",u); monitor(d,290,372,180,138,"code",u+.7)
    keyboard(d,94,572,130,34); keyboard(d,314,572,130,34); d.E(252,596,8,5,(70,68,96)); d.E(470,596,8,5,(70,68,96))
    mug(d,262,540,u); d.R(40,540,66,566,(255,230,90),2); d.R(48,520,74,546,(120,230,255),2)
    person_back(d,150,690,1.3,0,u); person_back(d,392,700,1.3,1,u)
    return im
def car2(d,cx,cy,w,h,kind,ph=0,shake=0,lights=True,glowlight=True):
    cx+=shake
    shadow(d,cx+8,cy+12,w*.58,h*.52,80)
    pol=kind in("cop","cop2")
    body={"cop":(238,238,244),"cop2":(26,26,34),"red":(214,36,52)}[kind]
    roof={"cop":(40,44,60),"cop2":(240,240,244),"red":(150,24,38)}[kind]
    for sx in(-1,1):
        for yy in(-h*.28,h*.3):
            d.R(cx+sx*(w/2)-4,cy+yy-17,cx+sx*(w/2)+4,cy+yy+17,(14,14,18),3); d.R(cx+sx*(w/2)-1.5,cy+yy-9,cx+sx*(w/2)+1.5,cy+yy+9,(150,150,165),1)
    bevel(d,cx-w/2,cy-h/2,cx+w/2,cy+h/2,body,15)
    if pol:
        dp=(24,24,32) if kind=="cop" else (240,240,244)
        d.R(cx-w/2+3,cy-h/2+3,cx+w/2-3,cy-h/2+h*.27,dp,12); d.R(cx-w/2+3,cy+h/2-h*.2,cx+w/2-3,cy+h/2-3,dp,12)
    else:
        d.R(cx-3,cy-h/2+6,cx+3,cy+h/2-6,(255,255,255,70)); 
    d.R(cx-w/2+10,cy-h/2+h*.1,cx-w/2+22,cy-h/2+h*.14,(255,255,255,40),2)
    for yy in(-.02,.18): 
        d.L(cx-w/2+3,cy+h*yy,cx-w/2+3,cy+h*(yy+.12),(0,0,0,70),1.5); d.L(cx+w/2-3,cy+h*yy,cx+w/2-3,cy+h*(yy+.12),(0,0,0,70),1.5)
    d.E(cx-w/2-3,cy-h*.18,5,3.5,roof); d.E(cx+w/2+3,cy-h*.18,5,3.5,roof)
    d.R(cx-w/2+7,cy-h/2+h*.27,cx+w/2-7,cy-h/2+h*.4,(40,66,96,235),6); d.P([(cx-w/2+12,cy-h/2+h*.28),(cx-w/2+28,cy-h/2+h*.28),(cx-w/2+14,cy-h/2+h*.39)],(255,255,255,70))
    bevel(d,cx-w/2+8,cy-h/2+h*.41,cx+w/2-8,cy+h/2-h*.3,roof,8)
    d.R(cx-w/2+7,cy+h/2-h*.3,cx+w/2-7,cy+h/2-h*.19,(40,66,96,235),5)
    for sx in(-1,1):
        d.E(cx+sx*(w/2-13),cy-h/2+6,7,4.5,(255,245,200)); d.E(cx+sx*(w/2-13),cy-h/2+6,12,9,(255,240,160,60))
        d.R(cx+sx*(w/2-16)-5,cy+h/2-8,cx+sx*(w/2-16)+5,cy+h/2-3,(255,40,50),1.5)
    d.R(cx-12,cy+h/2-5,cx+12,cy+h/2+1,(250,250,250),1.5); d.R(cx-10,cy-h/2+2,cx+10,cy-h/2+5,(20,20,28),1.5)
    if pol:
        a=int(ph*8)%2
        d.R(cx-w/2+10,cy-6,cx+w/2-10,cy+8,(20,20,28),3)
        d.R(cx-w/2+12,cy-4,cx-2,cy+6,(255,50,60) if a else (90,30,40),2); d.R(cx+2,cy-4,cx+w/2-12,cy+6,(70,130,255) if not a else (30,40,90),2)
        d.R(cx-3,cy-3,cx+3,cy+5,(250,250,250),1)
        if glowlight:
            g=(255,40,50,70) if a else (60,120,255,70)
            d.E(cx+(-1 if a else 1)*w*.22,cy,w*.95,w*.95,g)
def car_rear(d,cx,cy,w,h,col=(214,36,52),roof=(150,24,38),u=0):
    shadow(d,cx,cy+h/2+6,w*.64,10,90)
    for sx in(-1,1): d.R(cx+sx*(w/2)-8,cy+h/2-24,cx+sx*(w/2)+8,cy+h/2+2,(14,14,18),4)
    bevel(d,cx-w/2,cy-h*.08,cx+w/2,cy+h/2-10,col,14)
    bevel(d,cx-w*.38,cy-h*.5,cx+w*.38,cy-h*.02,roof,16)
    d.R(cx-w*.32,cy-h*.44,cx+w*.32,cy-h*.1,(38,62,96,240),10); d.P([(cx-w*.28,cy-h*.42),(cx-w*.12,cy-h*.42),(cx-w*.26,cy-h*.12)],(255,255,255,60))
    d.R(cx-w/2-3,cy-h*.1,cx+w/2+3,cy-h*.04,roof,3)
    for sx in(-1,1):
        d.R(cx+sx*(w*.4)-14,cy+h*.1,cx+sx*(w*.4)+14,cy+h*.2,(255,40,50),4); d.E(cx+sx*(w*.4),cy+h*.15,28,16,(255,40,50,60+int(25*math.sin(u*6))))
        d.R(cx+sx*(w*.18)-8,cy+h/2-14,cx+sx*(w*.18)+8,cy+h/2-7,(80,80,90),3)
    d.R(cx-16,cy+h*.2,cx+16,cy+h*.3,(250,250,250),2); d.L(cx-12,cy+h*.25,cx+12,cy+h*.25,(60,60,60),1.5)
def road(d,u,speed=300):
    d.R(0,0,540,960,(34,42,60))
    for k in range(9):
        y=((k*150+u*speed*.6)%1350)-190
        d.R(14,y,112,y+110,(58,72,100)); d.R(14,y,112,y+6,(255,255,255,22))
        d.R(428,y+55,526,y+165,(58,72,100)); 
        d.E(60,y+135,18,18,(40,120,70)); d.E(60,y+135,12,12,(60,160,90)); d.E(480,y+20,20,20,(40,120,70)); d.E(480,y+20,13,13,(60,160,90))
    d.R(112,0,122,960,(150,150,160)); d.R(418,0,428,960,(150,150,160))
    d.R(122,0,418,960,(56,58,70))
    d.R(122,0,418,960,(255,255,255,6))
    for k in range(12): y=((k*100+u*speed*.6)%1200)-110; d.E(160+(k%3)*70,y,5,5,(0,0,0,40)) if k%2==0 else None
    for k in range(14): y=((k*80+u*speed)%1120)-80; d.R(267,y,273,y+44,(235,235,235))
    for k in range(6):
        y=((k*220+u*speed*.8)%1320)-150
        if k==2:
            for j in range(9): d.R(130+j*32,y,152+j*32,y+34,(240,240,240,200))
    for k in range(5):
        y=((k*260+u*speed*.6)%1300)-120; d.E(112,y,46,46,(255,230,150,26)); d.E(112,y,5,5,(255,240,180))
def sceneC(u):
    im=new((10,12,24),(10,12,24)); d=D(im); road(d,u)
    bump=max(0,math.sin(u*5.2))**6
    px=270+math.sin(u*2.1)*40; py=610+bump*8; sh=math.sin(u*40)*6*bump
    car2(d,px,py,94,172,"cop",u,sh)
    cy=py+148-bump*120+math.sin(u*2)*6
    car2(d,px+math.sin(u*3)*10,cy+60,94,172,"cop2",u+.5,0)
    if bump>.35:
        for k in range(7): a=k*math.pi/3.5+u*3; d.L(px+math.cos(a)*36,py+150+math.sin(a)*16,px+math.cos(a)*76,py+150+math.sin(a)*40,(255,230,120,230),4)
        d.E(px,py+150,24,12,(255,255,255,200))
    for sg in(-1,1):
        for k in range(4): d.L(px+sg*60,py-30+k*50,px+sg*60,py+10+k*50,(255,255,255,50),3)
    return im
def sceneD(u):
    im=new((94,54,102),(38,26,64)); d=D(im)
    for k in range(7): d.E(50+k*74,60+math.sin(u*3+k)*8,9,9,(255,220,120,120)); d.E(50+k*74,60+math.sin(u*3+k)*8,16,16,(255,220,120,40))
    d.R(0,640,540,960,(34,26,50)); d.R(0,640,540,646,(255,255,255,16))
    monitor(d,140,140,260,200,"chase",u)
    d.R(220,372,320,384,(60,50,80),3)
    bevel(d,50,596,490,656,(88,62,100),10)
    person_front(d,168,470,1.55,0,u,True); person_front(d,372,476,1.55,1,u+.4,True)
    d.E(270,420,20,16,(255,255,255,0))
    for k in range(3):  # ja ja
        a=(u*2+k*.33)%1; d.A(80+k*30,250-a*50,12,10,0,360,(255,255,255,int(160*(1-a))),2)
    mug(d,270,568,u,(255,210,90))
    return im
def sceneE(u):
    im=new((10,12,24),(10,12,24)); d=D(im); road(d,u,360)
    p=sm((u-1.6)/1.6)
    xr=270+60*math.sin(u*2)
    cop_y=360+(620-360)*p; red_y=620+(360-620)*p
    car2(d,xr-30*(1-p),red_y,94,172,"red",u)
    car2(d,xr+30*p,cop_y,94,172,"cop",u,0,True,True)
    cx,cy=270,170
    d.E(cx,cy,72,72,(0,0,0,90)); d.E(cx,cy,66,66,(255,255,255,28)); d.A(cx,cy,48,48,40,320,(255,240,120,255),9); d.A(cx,cy,48,48,40,320,(255,200,60,255),4)
    d.P([(cx+40,cy-52),(cx+78,cy-34),(cx+34,cy-22)],(255,240,120,255))
    return im
def sceneF(u):
    im=new((24,10,56),(255,88,160)); d=D(im)
    for k in range(70): d.E(rnd(k)*540,rnd(k,1)*380,1.3,1.3,(255,255,255,130+int(70*math.sin(u*3+k))))
    d.E(400,250,52,52,(255,236,200,235)); d.E(386,238,9,9,(210,190,170,150)); d.E(414,262,7,7,(210,190,170,150)); d.E(400,246,50,50,None,(255,255,255,60),3)
    d.E(270,500,110,110,(255,190,120,90))
    for k in range(18):
        x=((k*58-u*10)%720)-90; h=150+rnd(k)*240; w=46+rnd(k,2)*32; col=(18+int(rnd(k,4)*14),12,40+int(rnd(k,5)*20))
        bevel(d,x,560-h,x+w,640,col,2); d.R(x,560-h,x+4,640,(255,255,255,26))
        if k%4==1: d.L(x+w/2,560-h,x+w/2,560-h-34,(120,120,140),2); d.E(x+w/2,560-h-36,3,3,(255,60,60,120+int(120*math.sin(u*5+k))))
        for r in range(int(h/22)):
            for c in range(int(w/14)):
                if rnd(k*31+r*7+c)>.45: d.R(x+6+c*14,560-h+10+r*22,x+14+c*14,560-h+20+r*22,(255,220,130,210) if rnd(r+c+k,3)>.3 else (120,220,255,210),1)
        if k%5==0: d.R(x+6,560-h-20,x+w-6,560-h-6,(60,255,230,235),3); d.R(x+6,560-h-20,x+w-6,560-h-6,None,3,(255,255,255,130),1.5)
        if k%6==2: d.R(x+4,560-h+14,x+w-4,560-h+44,(255,70,150,230),3); d.L(x+10,560-h+29,x+w-10,560-h+29,(255,255,255,200),3)
    d.R(0,640,540,960,(18,14,34))
    for k in range(12):
        t=((k/12)+u*.5)%1; y=640+t*t*320; wd=20+t*180
        d.R(270-wd,y,270+wd,y+3+t*10,(60,50,90,255))
    d.P([(270,640),(40,960),(500,960)],(44,40,68,230))
    for k in range(8): t=((k/8)+u*.8)%1; sg=(-1 if k%2 else 1); d.L(270+sg*t*20,640+t*t*320,270+sg*t*190,640+t*t*320+t*60,(255,240,200,200),2+t*5)
    d.E(270,930,120,20,(255,50,60,40))
    car_rear(d,270,790,112,168,u=u)
    return im
def sceneG(u):
    im=new((8,10,28),(30,16,50)); d=D(im)
    for k in range(18):
        a=k*math.pi/9+u*.4; d.P([(270,430),(270+math.cos(a-.08)*700,430+math.sin(a-.08)*700),(270+math.cos(a+.08)*700,430+math.sin(a+.08)*700)],(255,255,255,12))
    p=sm((u-1.0)/.6)
    if p<1: errico(d,270,430,2.6*(1-p),int(255*(1-p)))
    if p>0:
        s=1.5*(.2+.8*p)*(1+.1*math.sin((u-1)*10)*max(0,1-(u-1)*1.5)); r=100*s
        shadow(d,270,430+r*.95,r*.9,r*.15,90)
        d.E(270,430,r,r,(20,120,70)); d.E(270,430,r*.93,r*.93,(40,200,100)); d.E(270-r*.2,430-r*.35,r*.6,r*.35,(255,255,255,50)); d.E(270,430,r,r,None,(255,255,255),6*s)
        d.L(270-44*s,430+4*s,270-10*s,430+36*s,(0,0,0,70),16*s); d.L(270-10*s,430+36*s,270+50*s,430-30*s,(0,0,0,70),16*s)
        d.L(270-44*s,430+2*s,270-10*s,430+34*s,(255,255,255),14*s); d.L(270-10*s,430+34*s,270+50*s,430-32*s,(255,255,255),14*s)
        for k in range(26):
            a=k*.25; rr=(u-1)*170*rnd(k,5)+30; d.E(270+math.cos(a)*rr*1.6,430+math.sin(a)*rr*1.6+(u-1)*34,5,5,[(255,220,80),(80,220,255),(255,100,150)][k%3]+(230,))
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
