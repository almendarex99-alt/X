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

PAL={"C":(255,140,40),"S":(244,200,160),"M":(100,60,30),"B":(60,100,220),"T":(245,245,245),"Y":(255,220,80),"H":(120,70,40)}
SPR=["...CCCCC....","..CCCCCCCCC.","..MMMSSMS...",".MSMSSSMSSS.",".MSMMSSSMSSS",".MMSSSSMMMM.","...SSSSSSS..","..TTBTTT....",".TTTBTTBTTT.","TTTTBBBBTTTT","SSTBYBBYBTSS","SSSBBBBBBSSS","..BBB..BBB..",".HHH....HHH."]
def sprite(d,x,y,cell,sil=False,reveal=None,alpha=255,flip=False,tool=None):
    n=0
    for r,row in enumerate(SPR):
        for c,ch in enumerate(row):
            if ch=='.': continue
            n+=1
            if reveal is not None and n>reveal: continue
            cc=c if not flip else len(row)-1-c
            col=(20,22,40) if sil else PAL[ch]
            d.R(x+cc*cell,y+r*cell,x+cc*cell+cell+.4,y+r*cell+cell+.4,col+(alpha,),0)
def pxq(d,x,y,cell,col=(255,255,255)):
    rows=["..###..","##...##","....##.","...##..","...#...",".......","...#..."]
    for r,row in enumerate(rows):
        for c,ch in enumerate(row):
            if ch=='#': d.R(x+c*cell,y+r*cell,x+c*cell+cell,y+r*cell+cell,col,1)
def sceneA(u,final=False):
    im=new((10,8,34),(40,12,60)); d=D(im)
    for k in range(50): d.E(rnd(k)*540,rnd(k,1)*420,1.4,1.4,(255,255,255,120+int(90*math.sin(u*2+k))))
    d.E(270,520,230,60,(255,60,200,40))
    shadow(d,270,880,170,16,90)
    bevel(d,100,170,440,880,(96,40,150),16); d.R(100,170,126,880,(255,255,255,18)); d.R(414,170,440,880,(0,0,0,50))
    bevel(d,120,150,420,236,(30,16,60),10); d.R(132,168,408,218,(255,60,190),6); 
    for k in range(10): d.E(146+k*28,193,5,5,(255,255,255,int(150+100*math.sin(u*6+k))))
    bevel(d,134,252,406,520,(18,16,30),12); d.R(146,264,394,508,(8,12,28),6)
    for k in range(20): d.R(146,264+k*12,394,265+k*12,(0,0,0,40))
    # silueta + signo de interrogacion
    sprite(d,236,322,9,sil=True)
    if int(u*3)%2==0 or final: pxq(d,260,276,6,(255,230,90))
    d.P([(150,266),(260,266),(190,508),(150,508)],(255,255,255,10))
    bevel(d,120,550,420,640,(60,24,100),10)
    d.E(190,596,18,18,(30,30,40)); d.E(190,596,10,10,(230,50,60)); d.L(190,596,190,570,(220,220,230),6); d.E(190,568,8,8,(240,50,60))
    for k,c in enumerate([(255,70,80),(80,200,255),(255,220,80)]): d.E(280+k*46,590+(k%2)*8,14,14,(30,20,40)); d.E(280+k*46,588+(k%2)*8,11,11,c)
    d.R(246,676,294,700,(10,10,20),3); d.R(262,682,278,694,(255,220,80,180),2)
    d.R(130,730,410,860,(78,34,124),6); d.R(130,730,410,736,(255,255,255,20))
    return im
def girders(d,u):
    d.R(0,0,540,960,(8,8,20))
    levels=[(790,0.02),(640,-0.02),(490,0.02),(340,-0.02),(200,0.0)]
    for y,sl in levels:
        d.P([(20,y),(520,y+sl*500),(520,y+sl*500+22),(20,y+22)],(220,70,60))
        d.P([(20,y),(520,y+sl*500),(520,y+sl*500+6),(20,y+6)],(255,140,120))
        for k in range(24): xx=24+k*21; d.L(xx,y+22+sl*(xx-20),xx+12,y+6+sl*(xx-20),(120,30,40),2)
        for k in range(12): xx=30+k*42; d.E(xx,y+11+sl*(xx-20),2.2,2.2,(255,220,200))
    for x,y0,y1 in [(150,790,640),(380,640,490),(130,490,340),(400,340,200),(270,200,200)]:
        d.L(x,y0,x,y1,(80,220,255),3); d.L(x+22,y0,x+22,y1,(80,220,255),3)
        for yy in range(int(y1),int(y0),14): d.L(x,yy,x+22,yy,(80,220,255),2.5)
def ape(d,x,y,u):
    c=(150,92,50); b=(98,58,30)
    d.E(x,y,52,46,b); d.E(x,y+8,38,32,c)
    pound=math.sin(u*10)*8
    d.E(x-54,y+20+pound,16,24,b); d.E(x+54,y+20-pound,16,24,b)
    d.E(x,y-38,30,26,b); d.E(x,y-32,22,17,(230,190,150))
    for sg in(-1,1): d.E(x+sg*9,y-38,5,5,(255,255,255)); d.E(x+sg*9,y-38,2.4,2.4,(20,20,30)); d.E(x+sg*37,y-36,7,8,b)
    d.A(x,y-24,11,6,20,160,(70,30,20),2.5)
def barrel(d,x,y,r):
    d.E(x,y,r,r,(160,100,50)); d.E(x,y,r*.7,r*.7,None,(90,50,20),2); d.L(x-r,y,x+r,y,(90,50,20),2)
def sceneB(u):
    im=new((8,8,20),(8,8,20)); d=D(im); girders(d,u)
    ape(d,130,150,u)
    for k in range(3):
        t=((u*.22+k/3)%1); seg=int(t*4); f=t*4-seg
        pts=[(60,180),(500,280),(60,432),(480,590),(60,742)]
        # barril rodando por plataformas en zigzag
        xa,ya=pts[seg]; xb,yb=pts[seg+1] if seg<4 else pts[4]
        d.E(0,0,0,0,None)
        barrel(d,xa+(xb-xa)*f,ya+(yb-ya)*f-14,13)
    # heroe subiendo/saltando
    hy=790-sm((u%6)/6)*150 - abs(math.sin(u*6))*6
    sprite(d,150,hy-100,6.5)
    for k in range(70): d.R(0,k*14,540,k*14+1,(0,0,0,60))
    d.R(0,0,540,960,(0,0,0,0)); d.E(270,480,420,520,(0,0,0,0))
    return im
def sceneC(u):
    im=new((14,10,38),(30,14,56)); d=D(im)
    G=32; ox=54; oy=250; n=14
    d.R(ox-12,oy-12,ox+12*G*1.0+12-12+12*0+12,oy+12,(0,0,0,0))
    for r in range(15):
        for c in range(12): 
            d.R(ox+c*G,oy+r*G,ox+c*G+G-2,oy+r*G+G-2,(26,24,60),2)
    total=sum(ch!='.' for row in SPR for ch in row)
    reveal=int(min(1,u/3.2)*total)
    sprite(d,ox,oy,G,reveal=reveal)
    # resaltar gorra y bigote
    for r in range(15):
        pass
    if u>3.4:
        a=int(160+90*math.sin(u*7))
        d.R(ox+2*G-6,oy-6,ox+11*G+6,oy+2*G+6,None,10,(255,160,60,a),4)
        d.R(ox+1*G-6,oy+2*G-6,ox+11*G+6,oy+6*G+6,None,10,(255,255,255,a),3)
    # preview pequeno
    d.R(380,60,500,200,(20,18,50),8); d.R(380,60,500,66,(255,255,255,20),8)
    sprite(d,408,84,5)
    d.R(20,780,520,940,(20,18,50,200),10)
    for k in range(6): d.R(40+k*78,806,98+k*78,864,(40+k*14,50,120),4)
    return im
def landlord(d,cx,cy,sc,u):
    shadow(d,cx,cy+138*sc,52*sc,8*sc,60)
    bevel(d,cx-44*sc,cy+38*sc,cx+44*sc,cy+138*sc,(124,84,52),22*sc)
    d.P([(cx-10*sc,cy+38*sc),(cx+10*sc,cy+38*sc),(cx,cy+70*sc)],(245,245,245)); d.R(cx-4*sc,cy+48*sc,cx+4*sc,cy+100*sc,(200,40,50),2*sc)
    d.R(cx-9*sc,cy+24*sc,cx+9*sc,cy+46*sc,SK2)
    knock=math.sin(u*9)*10*sc if (u%2.4)<1.4 else 0
    bevel(d,cx-58*sc,cy+52*sc,cx-38*sc,cy+120*sc,(124,84,52),9*sc); d.E(cx-48*sc,cy+126*sc,10*sc,9*sc,SK)
    ax=cx+46*sc; bevel(d,ax-10*sc,cy+40*sc+knock,ax+10*sc,cy+104*sc+knock,(124,84,52),9*sc); d.E(ax,cy+108*sc+knock,10*sc,9*sc,SK)
    d.R(cx-70*sc,cy+120*sc,cx-30*sc,cy+160*sc,(250,250,240),3); d.L(cx-62*sc,cy+132*sc,cx-38*sc,cy+132*sc,(200,40,40),2); d.L(cx-62*sc,cy+142*sc,cx-44*sc,cy+142*sc,(0,0,0,70),2)
    hair_front(d,cx,cy,sc,(190,190,200),0)
    face(d,cx,cy,sc,False,False,False)
    d.P([(cx-18*sc,cy+13*sc),(cx,cy+8*sc),(cx+18*sc,cy+13*sc),(cx+12*sc,cy+19*sc),(cx,cy+14*sc),(cx-12*sc,cy+19*sc)],(70,60,60))
    d.L(cx-18*sc,cy-10*sc,cx-5*sc,cy-6*sc,(60,50,50),3*sc); d.L(cx+18*sc,cy-10*sc,cx+5*sc,cy-6*sc,(60,50,50),3*sc)
def sceneD(u):
    im=new((250,150,100),(90,50,110)); d=D(im)
    d.E(400,260,70,70,(255,230,150,230)); d.E(400,260,110,110,(255,230,150,40))
    d.R(0,720,540,960,(70,60,76)); d.R(0,720,540,726,(255,255,255,20))
    bevel(d,40,260,500,720,(150,88,70),6)
    for r in range(18):
        for c in range(14): 
            if (r+c)%2==0: d.R(42+c*32,262+r*25,42+c*32+30,262+r*25+23,(120,66,52,160),1)
    bevel(d,70,300,470,356,(60,50,80),4)
    for k in range(5): d.R(96+k*70,314,128+k*70,342,(255,230,120,160),2)
    bevel(d,320,430,460,720,(80,54,40),6); d.R(332,442,448,708,(60,40,32),4); d.E(338,590,6,6,(240,200,80))
    for sg in(0,1):
        d.R(100+sg*120,470,170+sg*120,570,(40,50,90),4); d.R(104+sg*120,474,166+sg*120,566,(255,230,140,200),3)
    shadow(d,200,860,150,14,70)
    landlord(d,180,520,1.5,u)
    # papel/recibo con $
    return im
def sceneE(u):
    im=new((94,54,102),(38,26,64)); d=D(im)
    d.R(0,640,540,960,(34,26,50)); d.R(0,640,540,646,(255,255,255,16))
    monitor(d,150,130,240,190,None,u)
    sprite(d,230,160+abs(math.sin(u*6))*-10,9)
    for k in range(7): d.E(50+k*74,60+math.sin(u*3+k)*8,9,9,(255,220,120,120))
    bevel(d,50,596,490,656,(88,62,100),10)
    person_front(d,168,470,1.55,0,u,True); person_front(d,372,476,1.55,1,u+.4,True)
    b=min(1,u/.5)
    d.R(300,350+0,500,420,(255,255,255,int(240*b)),18); d.P([(340,420),(370,420),(350,452)],(255,255,255,int(240*b)))
    if b>=1: sprite(d,364,362,4)
    for k in range(3):
        a=(u*2+k*.33)%1; d.A(80+k*30,250-a*50,12,10,0,360,(255,255,255,int(160*(1-a))),2)
    return im
def sceneF(u):
    im=new((24,18,60),(60,30,90)); d=D(im)
    for k in range(40): d.E(rnd(k)*540,rnd(k,1)*300,1.4,1.4,(255,255,255,140))
    d.R(0,640,540,960,(30,24,52)); d.R(0,640,540,646,(255,255,255,20))
    p=sm((u-2.0)/1.2)
    d.R(40,200,500,260,(20,18,50,200),10)
    # banco de trabajo / tuberia
    sw=math.sin(u*8)*18
    # carpintero (izq)
    x0=140+ -120*p
    shadow(d,x0+60,760,70,10,70)
    sprite(d,x0,560,9)
    d.R(x0+110,580-abs(sw),x0+118,650-abs(sw),(150,100,50),2); d.R(x0+98,570-abs(sw),x0+132,590-abs(sw),(190,190,200),3)
    d.R(x0+60,740,x0+190,760,(150,100,50),3)
    # fontanero (der)
    x1=640-300*p
    sprite(d,x1,560,9,flip=True)
    d.R(x1-40,690,x1+10,720,(120,130,150),4); d.R(x1-60,700,x1-30,712,(150,160,180),3); d.R(x1-20,640,x1-6,700,(150,160,180),3)
    d.E(x1-70,660+math.sin(u*5)*2,6,9,(120,200,255,200)); 
    cx=270;cy=360
    a_=int(255*sm((u-1.2)/.5)); d.A(cx,cy,60,60,30,330,(255,240,120,a_),10); d.P([(cx+52,cy-60),(cx+92,cy-40),(cx+44,cy-26)],(255,240,120,a_))
    return im
def sceneG(u):
    im=new((70,10,30),(20,6,30)); d=D(im)
    for k in range(16):
        a=k*math.pi/8+u*.5; d.P([(270,300),(270+math.cos(a-.09)*800,300+math.sin(a-.09)*800),(270+math.cos(a+.09)*800,300+math.sin(a+.09)*800)],(255,230,150,16))
    d.R(0,780,540,960,(110,24,36)); d.R(0,780,540,788,(255,255,255,30))
    for k in range(9): d.R(k*60,800,k*60+8,960,(0,0,0,40))
    s=.3+.7*sm(u/.8)
    landlord(d,150,420,1.25*s+.01,u*0)
    sprite(d,300,430,12*s+.1)
    for k in range(30):
        a=k*.21+u*.3; r=140+rnd(k,3)*180; x=270+math.cos(a)*r; y=360+math.sin(a)*r*.7
        d.P([(x,y-9),(x+3,y-3),(x+9,y),(x+3,y+3),(x,y+9),(x-3,y+3),(x-9,y),(x-3,y-3)],(255,230,120,200))
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
