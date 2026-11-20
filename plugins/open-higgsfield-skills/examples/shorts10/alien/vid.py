import sys; sys.path.insert(0,"..")
from art import *
SKIN=[(236,200,170),(176,128,96),(214,168,130),(120,84,62),(240,214,190)]
SUIT=[(214,176,60),(70,120,190),(200,80,80),(90,160,120),(230,230,236),(180,120,200),(120,140,170)]
def bust(d,x,y,sc,k,react=0.0,u=0,look=0):
    dx=math.sin(u*40)*react*3; 
    x+=dx; y+=react*30*sc
    d.R(x-28*sc,y-10*sc,x+28*sc,y+70*sc,SUIT[k%7]+(255,),12*sc)
    d.E(x,y-30*sc,19*sc,22*sc,SKIN[k%5]+(255,)); d.E(x,y-40*sc,20*sc,12*sc,[(40,30,24),(200,170,90),(20,20,24),(120,70,40),(180,180,190)][k%5]+(255,))
    ey=y-32*sc
    for sg in(-1,1):
        d.E(x+sg*7*sc,ey,(4+react*3)*sc,(4+react*4)*sc,(255,255,255)); d.E(x+sg*7*sc+look*sc,ey,(1.8+react)*sc,(1.8+react)*sc,(20,20,24))
        d.L(x+sg*11*sc,ey-8*sc-react*5*sc,x+sg*3*sc,ey-9*sc-react*7*sc,(50,34,26),1.8*sc)
    d.E(x,y-18*sc,(4+react*5)*sc,(2+react*7)*sc,(120,30,36)) if react>0 else d.L(x-5*sc,y-18*sc,x+5*sc,y-18*sc,(120,50,50),1.8*sc)
def metal_room(d,u,col=(70,82,92),light=(210,240,255)):
    corridor(d,u,speed=0.0,wall=col,floor=(36,42,48),ceil=(30,36,42),door=(50,60,70),light=light,pulse=flicker(u,1,5),n=9,doors=False)
    xl,xr,yt,yb=planes(depth(2))
    for k in range(3):
        d.L(planes(depth(0))[0]+4,HY-120+k*34,xl,HY-120+k*34*.6,(190,200,210,160),5)
        d.L(planes(depth(0))[1]-4,HY-120+k*34,xr,HY-120+k*34*.6,(190,200,210,160),5)
def table_scene(d,u,react=0.0,mist=0.0,glow=(120,240,170)):
    gradient(d,0,700,(10,20,22),(26,44,46))
    for k in range(6): d.R(30+k*88,80,60+k*88,96,glow+(200,),3); d.E(45+k*88,100,40,16,glow+(30,))
    d.R(0,620,540,960,(30,34,38),0); 
    for i in range(7): 
        bust(d,56+i*72,520+(i%2)*14,.95,i,react=react if i in(2,3,4) else react*.5,u=u+i)
    bevel(d,10,640,530,720,(190,196,204),10); d.R(10,720,530,960,(150,156,166),0)
    for i in range(7): d.E(52+i*72,676,22,7,(236,240,244)); d.E(52+i*72,672,12,4,(150,100,70)) if i!=3 else None
def face(d,x,y,sc,u,blood=0.0,react=1.0):
    d.R(x-70*sc,y+30*sc,x+70*sc,y+150*sc,SUIT[1]+(255,),24*sc)
    d.E(x,y-30*sc,62*sc,76*sc,SKIN[0]+(255,)); d.E(x,y-84*sc,64*sc,40*sc,(60,36,24))
    for sg in(-1,1):
        d.E(x+sg*24*sc,y-28*sc,16*sc,(18+react*4)*sc,(255,255,255)); d.E(x+sg*24*sc,y-28*sc,6*sc,6*sc,(20,24,36))
        d.L(x+sg*38*sc,y-62*sc-react*6*sc,x+sg*10*sc,y-66*sc-react*10*sc,(60,40,30),4*sc)
    d.E(x,y+30*sc,14*sc,(12+react*8)*sc,(120,30,36)); d.E(x,y+10*sc,6*sc,5*sc,(190,140,110))
    for k in range(int(40*blood)):
        a=rnd(k,3)*6.28; r=rnd(k,4)*66*sc; d.E(x+math.cos(a)*r,y-20*sc+math.sin(a)*r*1.15,(2+rnd(k,5)*5)*sc,(2+rnd(k,6)*7)*sc,(176,22,34,220))
def sceneA(u,final=False):
    im=new((10,20,22),(26,44,46)); d=D(im); table_scene(d,u)
    d.E(270,420,160,260,(120,240,170,16))
    return im
def sceneB(u):
    im=new((10,16,22),(30,40,52)); d=D(im)
    metal_room(d,u)
    for k in range(4): d.R(0,120+k*50,540,126+k*50,(0,0,0,0),0)
    film_camera(d,170,850,.9,u); clapper(d,380,880,.8,open_=(math.sin(u*3)>.4)*1.0)
    d.L(430,780,430,620,(120,130,140),6); d.R(396,620,466,646,(80,88,100),6)
    silhouette(d,300,850,1.2,(14,18,24))
    return im
def sceneC(u):
    im=new((10,20,22),(26,44,46)); d=D(im); table_scene(d,u,react=0.0)
    # guion con la indicacion y gotita roja (algo de sangre)
    for k in range(3):
        a=sm((u-.6-k*.8)/.4)
        if a>0:
            x=60+k*160; y=120+k*20; d.R(x,y,x+120,y+150,(244,240,226,int(255*a)),4)
            for q in range(7): d.L(x+10,y+20+q*16,x+110-(q%3)*14,y+20+q*16,(0,0,0,int(100*a)),2.5)
            if k==2: d.E(x+60,y+120,10,14,(190,30,40,int(255*a)))
    return im
def sceneD(u):
    im=new((16,22,28),(40,52,60)); d=D(im)
    # corte transversal de la mesa: deposito, tuberia y valvula ocultos
    bevel(d,40,300,500,340,(206,212,220),6); d.R(60,340,480,520,(0,0,0,40),0)
    for x in(80,440): d.R(x,340,x+22,760,(96,104,116),3)
    # deposito rojo + manometro
    d.R(150,500,360,700,(120,126,138),30); d.R(158,560,352,696,(180,30,40),26)
    d.E(255,520,0,0,(0,0,0,0)); 
    d.R(240,420,270,500,(150,156,166),3); d.R(240,332,270,420,(150,156,166),3)
    d.E(420,470,48,48,(244,244,240)); d.E(420,470,48,48,None,(40,40,46),5)
    p=clamp(u/4.0); a=-2.4+p*2.8; d.L(420,470,420+math.cos(a)*34,470+math.sin(a)*34,(210,40,50),5)
    for k in range(9): aa=-2.4+k*.35; d.L(420+math.cos(aa)*40,470+math.sin(aa)*40,420+math.cos(aa)*46,470+math.sin(aa)*46,(0,0,0),2)
    # tecnico agachado
    silhouette(d,110,760,.9,(10,12,16))
    # tubo hacia la mesa y burbujas de presion
    for k in range(6):
        t=(u*1.2+k*.17)%1; d.E(255,500-t*160,6,6,(240,60,70,int(255*(1-t))))
    d.R(0,0,0,0,(0,0,0,0),0)
    # ojos de la mesa: actores sentados encima, ignorantes (signos de interrogacion)
    for i in range(4): bust(d,100+i*100,250,.7,i,u=u)
    return im
def sceneE(u):
    im=new((10,20,22),(26,44,46)); d=D(im)
    boom=u-1.4
    react=clamp(boom/.25) if boom>0 else 0.0
    table_scene(d,u,react=react)
    if boom>0:
        for k in range(46):
            a=-math.pi/2+(rnd(k)-.5)*2.4; v=240+rnd(k,2)*420; t=boom
            x=270+math.cos(a)*v*t; y=640+math.sin(a)*v*t+520*t*t
            s=3+rnd(k,3)*7; d.E(x,y,s,s*1.4,(190,26,36,int(255*clamp(1-t/1.8))))
        d.R(0,0,540,960,(255,255,255,int(255*clamp(1-boom/.18))),0) if boom<.18 else None
    return im
def sceneF(u):
    im=new((20,28,34),(40,52,60)); d=D(im)
    for k in range(14): d.R(0,k*70,540,k*70+2,(255,255,255,8),0)
    face(d,270,430,2.0,u,blood=sm((u-.5)/.5),react=1.0+.1*math.sin(u*12))
    clapper(d,120,880,.7,open_=(math.sin(u*3)>.4)*1.0)
    film_strip(d,820,u,90)
    return im
def sceneG(u):
    im=new((10,16,20),(24,40,44)); d=D(im)
    for k in range(5):
        x=20+k*100; y=300+math.sin(u*2+k)*6
        d.R(x,y-10,x+92,y+330,(8,8,10),6)
        for q in range(4): d.R(x+4,y+q*84,x+88,y+q*84+76,(230,236,244,20),4)
        face(d,x+46,y+150,.62,u+k,blood=0.0,react=.9+.2*math.sin(u*3+k))
    film_strip(d,110,u,90); film_strip(d,720,u*1.3,90)
    for k in range(20): a=k*.31+u*.3; d.E(270+math.cos(a)*250,430+math.sin(a)*300,3,3,(120,240,170,150))
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx==0: return 1.0+.4*sm(p),270,540
    if idx==1: return 1.0+.2*sm(p),270,560
    if idx==2: return 1.0+.25*sm(p),270,520
    if idx==3: return 1.0+.1*sm(p),270,520
    if idx==4:
        sh=max(0,1-(u-1.4)/.9) if u>=1.4 else 0
        return 1.0+.15*sm(p)+.06*sh,270+math.sin(u*70)*10*sh,540+math.cos(u*55)*10*sh
    if idx==5: return 1.0+.2*sm(p),270,470
    if idx==6: return 1.2-.2*sm(p),270,480
    return 1.4-.4*sm(p),270,540
core.CAM=cam
if __name__=="__main__": core.main()
