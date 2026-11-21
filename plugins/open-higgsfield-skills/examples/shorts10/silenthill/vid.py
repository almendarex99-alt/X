import sys; sys.path.insert(0,"..")
from art import *
from common import *
from PIL import Image, ImageOps
import numpy as np

def harry(d,x,y,sc,u,walk=0.0):
    """protagonista de espaldas: chaqueta marron, vaqueros, botas y linterna"""
    sw=math.sin(walk)*4*sc
    shadow(d,x,y+4,40*sc,6*sc,80)
    d.R(x-14*sc,y-66*sc,x-2*sc,y-6*sc+sw,(40,52,80),5*sc); d.R(x+2*sc,y-66*sc,x+14*sc,y-6*sc-sw,(40,52,80),5*sc)
    d.R(x-15*sc,y-8*sc+sw,x-1*sc,y,(26,22,20),3*sc); d.R(x+1*sc,y-8*sc-sw,x+15*sc,y,(26,22,20),3*sc)
    d.R(x-22*sc,y-132*sc,x+22*sc,y-62*sc,(96,66,44),10*sc); d.R(x-22*sc,y-132*sc,x+22*sc,y-124*sc,(255,255,255,30),10*sc)
    d.R(x-32*sc,y-130*sc,x-22*sc,y-78*sc,(96,66,44),5*sc); d.R(x+22*sc,y-130*sc,x+32*sc,y-90*sc,(96,66,44),5*sc)
    d.E(x,y-146*sc,15*sc,17*sc,(190,140,110)); d.E(x,y-152*sc,16*sc,11*sc,(60,40,28))
    d.R(x+28*sc,y-104*sc,x+44*sc,y-90*sc,(30,30,34),3*sc)
def rust(d,u):
    d.R(0,0,540,960,(122,54,30),0)
    for r in range(-2,40):
        for c in range(-2,22):
            x=c*30+(15 if r%2 else 0); y=r*30
            d.E(x,y,13,13,(40,16,10)); d.E(x,y,8,8,(150,70,36))
    for k in range(60): d.E(rnd(k)*540,rnd(k,1)*960,10+rnd(k,2)*30,6+rnd(k,3)*14,(170,40,24,120))
    d.R(0,0,540,960,(255,60,30,int(30+30*math.sin(u*30))),0)
def brick_building(d,x,y,w,h,k,fog):
    col=mixc((94,62,52),(150,150,156),fog); d.R(x,y,x+w,y+h,col+(255,),2)
    for r in range(int(h/14)): d.L(x,y+r*14,x+w,y+r*14,(0,0,0,40),1.5)
    for r in range(int(h/70)):
        for c in range(int(w/50)):
            if rnd(k*7+r*3+c)>.35: d.R(x+10+c*50,y+14+r*70,x+34+c*50,y+54+r*70,(16,16,22),2)
    d.R(x-4,y-6,x+w+4,y+4,mixc((60,44,40),(130,130,138),fog),1)
def parked_car(d,x,y,sc,fog):
    col=mixc((70,70,86),(150,150,158),fog)
    d.R(x-70*sc,y-34*sc,x+70*sc,y,col+(255,),8*sc); d.R(x-44*sc,y-62*sc,x+36*sc,y-30*sc,col+(255,),10*sc); d.R(x-38*sc,y-58*sc,x+30*sc,y-34*sc,(30,36,46),6*sc)
    for sx in(-46,46): d.E(x+sx*sc,y,13*sc,13*sc,(14,14,18)); d.E(x+sx*sc,y,6*sc,6*sc,(120,120,126))
def street(d,u,fog=0.0,popin=0.0,speed=0.0,lamps=True,sky=(70,74,84),n=9):
    gradient(d,0,HY+30,sky,mixc(sky,(150,154,160),.7))
    # carretera en perspectiva
    xl,xr,yt,yb=planes(depth(0)); xl2,xr2,yt2,yb2=planes(depth(n))
    d.P([(60,960),(480,960),(300,HY+20),(240,HY+20)],(48,48,54)); d.P([(0,960),(60,960),(240,HY+20),(0,HY+20)],(74,70,66)); d.P([(480,960),(540,960),(540,HY+20),(300,HY+20)],(74,70,66))
    off=(u*speed)%1.0
    for k in range(14):
        t=k-off+.2; s=1.7/(1+.62*t*1.2)
        y=HY+20+(960-HY-20)*clamp(s/1.7)**1.0; 
        d.R(270-3*s*3,y,270+3*s*3,y+10*s*3,(220,210,120,int(200*clamp(1-t/14))),0)
    # edificios a ambos lados, cada uno aparece segun distancia (pop-in)
    for side in(-1,1):
        for k in range(8):
            t=k*1.15+.8-off*1.15; 
            if t<.2: continue
            s=1.7/(1+.62*t); x=270+side*(150+210*s*.55); w=130*s; h=(260+rnd(k,side+2)*160)*s
            ytop=HY+20-h+ (30*s); base=HY+20+120*s
            vis=1.0
            if popin>0:
                vis=1.0 if (k*3+(0 if side<0 else 1))%5<3 else (1 if int(u*14+k)%2==0 else 0)  # parpadean al aparecer
            if vis:
                col=mixc((38,36,44),(110,112,120),clamp(t/9.0))
                d.R(x-w/2,ytop,x+w/2,base,col+(255,),2)
                for r in range(int(h/(34*max(.3,s)))):
                    for c in range(2): d.R(x-w/2+8+c*w*.46,ytop+8+r*34*max(.3,s),x-w/2+8+c*w*.46+w*.3,ytop+22+r*34*max(.3,s),(255,214,120,60) if rnd(k*9+r*3+c)>.7 else (14,14,20),1)
    d.R(0,HY+20,60,HY+190,(60,56,52),0) if False else None
    parked_car(d,120,HY+210,1.5,fog*.8); parked_car(d,430,HY+200,1.3,fog*.8)
    if lamps:
        for k in range(5):
            t=k*1.7+.6-((u*speed)%1.0)*1.7
            if t<.1: continue
            s=1.7/(1+.62*t); 
            for side in(-1,1):
                x=270+side*(120+130*s*.5); d.R(x-2*s*3,HY-130*s*1.1,x+2*s*3,HY+40+60*s,(10,10,14)); d.E(x,HY-134*s*1.1,10*s*3,10*s*3,(255,226,150)); d.E(x,HY-134*s*1.1,44*s*3,44*s*3,(255,226,150,46))
    # niebla: bandas y degradado (aumenta con la distancia)
    if fog>0:
        for k in range(14):
            y=HY-80+k*30; d.R(0,y,540,y+30,(166,170,176,int(fog*(18+k*4))),0)
        fogband(d,u,HY-150,HY+160,(190,194,200),int(fog*60),n=12)
        d.E(270,HY,360,150,(190,194,200,int(fog*130)))
def sceneA(u,final=False):
    im=new((70,72,80),(150,150,156)); d=D(im)
    street(d,u,fog=.85,speed=.15)
    harry(d,270+math.sin(u*.4)*6,HY+330,1.4,u,walk=u*5)
    flashlight(d,330,HY+220,300,HY-100,.26,420,70)
    fogband(d,u,700,900,(190,190,196),30)
    return ps1f(im,6)
def sceneB(u):
    im=new((26,22,40),(60,50,70)); d=D(im)
    d.R(0,640,540,960,(54,40,40)); d.R(0,640,540,646,(255,255,255,24))
    def inner(d_,x,y,w,h):
        gradient(d_,y,y+h,(120,124,132),(70,72,80))
        d_.R(x+w*.3,y+h*.42,x+w*.46,y+h*.86,(30,30,38)); d_.R(x+w*.56,y+h*.5,x+w*.78,y+h*.86,(36,34,44))
        d_.E(x+w/2,y+h*.5,w*.7,h*.3,(190,194,200,120)); silhouette(d_,x+w/2,y+h*.96,.34,(8,8,12))
    tv(d,90,330,360,330,inner,u); ps1(d,270,760,1.0,u)
    d.R(40,120,200,290,(244,240,230),6); d.R(40,120,200,150,(200,50,60),6)
    for r in range(3):
        for c in range(4): d.R(52+c*34,164+r*38,76+c*34,190+r*38,(210,210,220) if (r*4+c)!=int(u*1.2)%12 else (255,210,80),2)
    return im
def sceneC(u):
    im=new((214,196,160),(190,170,130)); d=D(im)
    # mapa de papel con calles, manzanas y marcas rojas
    for r in range(8): d.L(0,100+r*100,540,100+r*100,(120,100,70,170),3)
    for c in range(6): d.L(40+c*90,0,40+c*90,960,(120,100,70,170),3)
    for k in range(34):
        x=50+(k%6)*90; y=110+(k//6)*100; d.R(x,y,x+70,y+80,(176,150,112,230),2)
    d.R(0,0,540,70,(120,100,70,60),0)
    cx,cy=270,430
    R=60+sm(math.sin(u*.9)*.5+.5)*210
    for k in range(40):
        a=rnd(k)*6.28; r=60+rnd(k,1)*290; x=cx+math.cos(a)*r; y=cy+math.sin(a)*r*.8
        if r<R: d.R(x-14,y-14,x+14,y+14,(70,110,180,230),3)
        else: d.R(x-14,y-14,x+14,y+14,None,3,(90,70,50,150),1.5)
    d.E(cx,cy,R,R*.8,None,(200,40,40,220),4)
    d.L(cx-12,cy-12,cx+12,cy+12,(200,40,40),5); d.L(cx+12,cy-12,cx-12,cy+12,(200,40,40),5)
    load=clamp((R-60)/210.0)
    d.R(40,780,500,820,(40,30,24),8); d.R(44,784,44+452*load,816,mixc((80,200,140),(230,60,50),load),6)
    for i,ch in enumerate(str(int(60-load*38)).zfill(2)): seg7(d,60+i*34,860,28,56,int(ch),(40,30,24),(200,184,150))
    ptext(d,150,872,"FPS",4.0,(40,30,24))
    return im
def sceneD(u):
    im=new((60,64,74),(120,124,130)); d=D(im)
    f=sm((u-1.8)/3.0)
    street(d,u,fog=f,popin=(1.0 if f<.45 else 0.0),speed=.12)
    harry(d,270,HY+330,1.4,u,walk=u*4)
    return ps1f(im,6)
def sceneE(u):
    im=new((60,64,72),(130,132,138)); d=D(im)
    street(d,u,fog=1.0,speed=.0)
    for k,(x,sc) in enumerate([(120,.5),(420,.45),(270,.34)]):
        a=clamp((math.sin(u*.9+k*2)+.2)*.6)
        zombie(d,x,HY+30,sc*1.2,u+k,(40,40,44)); d.E(x,HY-60*sc,60*sc,90*sc,(190,190,196,int(150*(1-a))))
    harry(d,270,HY+430,2.0,u,walk=0)
    flashlight(d,330,HY+250,270+math.sin(u*.8)*120,HY-60,.3,520,80)
    return ps1f(im,6)
def sceneF(u):
    im=new((30,24,30),(66,52,60)); d=D(im)
    near=clamp(sm(u/5.0))
    # monstruo que se acerca detras
    zombie(d,82,760,lerp(.6,1.9,near),u,(10,8,10)); zombie(d,458,780,lerp(.5,1.6,near),u+1,(10,8,10))
    d.E(270,430,300,380,(190,194,200,int(40+60*near)))
    # radio de bolsillo
    cx,cy=270,560
    shadow(d,cx,cy+270,150,16,80)
    d.R(cx-110,cy-210,cx+110,cy+270,(34,34,40),34); d.R(cx-110,cy-210,cx-96,cy+270,(255,255,255,40),34)
    d.L(cx+70,cy-210,cx+120,cy-410,(150,150,160),6); d.E(cx+120,cy-410,6,6,(220,220,230))
    d.R(cx-84,cy-180,cx+84,cy-60,(150,152,160),12)
    for r in range(5): 
        for c in range(14): d.E(cx-72+c*11,cy-168+r*21,3.4,3.4,(40,40,46))
    # dial con aguja y estatica creciente
    d.R(cx-84,cy-30,cx+84,cy+20,(14,14,18),8)
    for k in range(10): d.L(cx-72+k*16,cy-24,cx-72+k*16,cy-14,(255,255,255,120),2)
    d.L(cx-60+near*120,cy-30,cx-60+near*120,cy+20,(255,80,80),3)
    d.E(cx+70,cy+60,9,9,(255,60,60) if int(u*(2+near*10))%2==0 else (80,20,20))
    d.R(cx-84,cy+90,cx+84,cy+240,(54,54,62),14)
    for k in range(7): d.L(cx-70,cy+110+k*17,cx+70,cy+110+k*17,(60,56,50,150),3)
    # ondas de estatica que salen de la radio
    for k in range(18):
        a=(u*.9+k/18.0)%1; amp=near*60
        d.A(cx,cy-100,60+a*260,60+a*260,200,340,(255,255,255,int(150*(1-a)*(.3+near))),3)
    noise_static(d,cx-84,cy-180,168,120,u,int(60+190*near),5)
    return im
def sceneG(u):
    im=new((70,72,80),(150,150,156)); d=D(im)
    street(d,u,fog=.9,speed=.1); fogband(d,u,300,800,(190,194,200),34,14)
    for k in range(26):
        a=k*.24+u*.3; r=300+rnd(k,3)*50; d.E(270+math.cos(a)*r,430+math.sin(a)*r*.7,3,3,(240,244,250,150))
    d.E(270,380,200*sm(u/.8),60*sm(u/.8),(255,226,150,40))
    ow=(1.2<u<1.8) or (2.6<u<3.0)
    if ow: rust(d,u)
    harry(d,270,HY+330,1.4,u)
    return ps1f(im,6)
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx==0: return 1.0+.4*sm(p),270,500
    if idx==1: return 1.05+.2*sm(p),270,520
    if idx==2: return 1.0,270,480
    if idx==3: return 1.0+.2*sm(p),270,470
    if idx==4: return 1.0+.5*sm(p),270,520
    if idx==5: return 1.0+.2*sm(p),270,500
    if idx==6: return 1.3-.3*sm(p),270,470
    return 1.4-.4*sm(p),270,500
core.CAM=cam
if __name__=="__main__": core.main()
