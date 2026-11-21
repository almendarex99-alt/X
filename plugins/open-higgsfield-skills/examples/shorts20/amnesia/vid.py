import sys; sys.path.insert(0,"..")
from art import *
from PIL import Image
import numpy as np
def warp(im,amp,t):
    a=np.array(im); h=a.shape[0]; out=np.empty_like(a)
    for y in range(0,h,6):
        sh=int(math.sin(y/60.0+t*3)*amp*3)
        out[y:y+6]=np.roll(a[y:y+6],sh,axis=1)
    out[...,0]=np.roll(out[...,0],int(amp*.9),axis=1); out[...,2]=np.roll(out[...,2],-int(amp*.9),axis=1)
    return Image.fromarray(out)
def stone(d,x0,y0,x1,y1,seed=0,col=(78,70,64)):
    d.R(x0,y0,x1,y1,col+(255,),0)
    for r in range(int((y1-y0)/46)+1):
        for c in range(int((x1-x0)/80)+2):
            x=x0+c*80-(40 if r%2 else 0); y=y0+r*46; v=int(rnd(r*13+c,seed)*26)
            d.R(x+2,y+2,x+78,y+44,(col[0]+v-12,col[1]+v-12,col[2]+v-12,255),2)
def lantern_light(d,cx,cy,r,u,k=1.0):
    fl=.9+.1*math.sin(u*9)+.05*math.sin(u*23)
    for i in range(7): d.E(cx,cy,r*(1-i*.12)*fl,r*(1-i*.12)*fl,(255,190,90,int(20*k)))
def dungeon(d,u,light=1.0):
    corridor(d,u,speed=.08,wall=(72,64,58),floor=(40,36,32),ceil=(30,28,26),door=(60,44,34),light=(255,190,90),pulse=flicker(u,2,7)*light,n=9,doors=True,lights=False)
    for k in range(14):
        t=k*.7+.5; s=depth(t); xl=planes(s)[0]; xr=planes(s)[1]
        for xx in (xl+16*s,xr-16*s): d.L(xx,HY-120*s,xx+(8*s if xx<270 else -8*s),HY-60*s,(30,26,24),3)
def hand_lantern(d,u,x=420,y=760,flame=True):
    d.R(x-16,y-60,x+16,y+20,(60,60,66),4); d.R(x-22,y-70,x+22,y-60,(40,40,44),2); d.R(x-22,y+18,x+22,y+30,(40,40,44),2)
    d.R(x-14,y-56,x+14,y+14,(255,200,100,200),3)
    if flame: d.E(x,y-24,8,18+3*math.sin(u*14),(255,230,150))
    d.R(x+8,y+30,x+60,y+120,(196,150,120),14); d.R(x-6,y-90,x+6,y-70,(60,60,66),1)
def sceneA(u,final=False):
    im=new((8,6,8),(30,24,22)); d=D(im)
    dungeon(d,u)
    lantern_light(d,420,740,420,u,.9)
    hand_lantern(d,u)
    return im
def sceneB(u):
    im=new((20,28,44),(48,64,90)); d=D(im)
    d.R(0,640,540,960,(30,34,46)); d.R(0,640,540,646,(255,255,255,24))
    # ventana con nieve y mesa con monitores y boceto de castillo
    bevel(d,30,70,230,300,(60,60,70),8); d.R(40,80,220,290,(20,28,56))
    for k in range(40): d.E((rnd(k)*180+u*10*(k%3+1))%180+40,(rnd(k,1)*210+u*30)%210+80,2.2,2.2,(255,255,255,200))
    d.R(270,90,510,300,(240,236,226),4); stone(d,282,102,498,170,2,(120,110,100)); d.P([(300,172),(400,130),(480,172)],(90,84,80))
    d.R(40,440,500,500,(112,76,52),6)
    for k,(x,w) in enumerate([(70,170),(290,170)]): d.R(x,330,x+w,430,(40,44,56),6); d.R(x+6,336,x+w-6,424,(10,14,20),4)
    from common import tv
    d.R(200,520,340,640,(0,0,0,0),0)
    person_back(d,270,760,1.45,0,u)
    ptext(d,40,880,"FRICTIONAL  2010",3.4,(255,255,255))
    return im
def sceneC(u):
    im=new((8,6,8),(30,24,22)); d=D(im)
    # armario con rendijas: alguien escondido mirando por las lamas
    stone(d,0,0,540,960,5,(54,48,44))
    d.R(110,120,430,860,(70,46,30),6); d.R(110,120,430,860,None,6,(30,18,10),6)
    for k in range(14): d.R(130,160+k*46,410,184+k*46,(10,8,8),2)
    for k in range(14): d.R(130,184+k*46,410,200+k*46,(130,92,60),2)
    for k in range(2): d.E(220+k*100,420,8,8,(255,255,255,int(200*abs(math.sin(u*2+k)))))
    # silueta de monstruo pasando por fuera, con luz tenue
    mx=lerp(-80,620,(u*.14)%1); d.E(mx,520,40,80,(4,4,6,200)); d.R(mx-24,540,mx+24,900,(4,4,6,200),14)
    # armas: casillero vacio tachado
    d.R(26,26,160,100,(0,0,0,170),8); ptext(d,34,40,"ARMAS: 0",2.8,(255,255,255)); d.L(30,30,156,96,(230,60,60),5)
    return im
def sceneD(u):
    im=new((6,6,10),(18,16,26)); d=D(im)
    dungeon(d,u,light=.4)
    s=clamp(1.0-u/6.0*.9)
    # indicador de cordura: cerebro + barra
    cx,cy=270,200
    for sg in(-1,1): d.E(cx+sg*30,cy,38,32,(240,170,180,int(60+190*s))); d.E(cx+sg*30,cy,38,32,None,(255,220,230,200),3)
    d.L(cx,cy-30,cx,cy+30,(255,220,230,200),3)
    d.R(120,270,420,300,(10,10,16),8); d.R(124,274,124+292*s,296,mixc((230,60,70),(110,220,160),s),6)
    ptext(d,160,330,"CORDURA",3.6,(255,255,255))
    # oscuridad que aumenta
    d.R(0,0,540,960,(0,0,0,int(160*(1-s))),0)
    return warp(im,(1-s)*14,u)
def sceneE(u):
    im=new((8,6,8),(30,24,22)); d=D(im)
    dungeon(d,u,light=.6)
    for k,x in enumerate([120,430,300]): 
        a=clamp(math.sin(u*1.2+k*2)*.8+.2)
        silhouette(d,x,HY+120,.5,(4,4,6)); d.E(x,HY-60,20,28,(150,160,180,int(80*a)))
    for k in range(10): d.L(rnd(k)*540,rnd(k,1)*960,rnd(k)*540+30,rnd(k,1)*960+4,(255,255,255,int(80*abs(math.sin(u*5+k)))),2)
    lantern_light(d,420,740,300,u,.5); hand_lantern(d,u)
    return warp(im,6+10*clamp(u/5.0),u*2)
def sceneF(u):
    im=new((8,6,8),(30,24,22)); d=D(im)
    stone(d,0,0,540,960,7,(46,40,36))
    # esquina oscura con alguien agazapado y un monstruo grande que se acerca por el pasillo
    d.R(0,520,540,960,(14,12,12),0)
    t=clamp(u/6.0); sx=lerp(540,330,t); sc=lerp(.8,1.6,t)
    d.E(sx,620-130*sc,34*sc,44*sc,(4,4,6)); d.R(sx-46*sc,620-110*sc,sx+46*sc,640,(4,4,6),24*sc)
    for k in range(2): d.R(sx-26*sc+k*38*sc,620-176*sc,sx-14*sc+k*38*sc,620-164*sc,(255,200,100,230),3)
    d.R(sx-90*sc,620-86*sc,sx-46*sc,640,(4,4,6),10*sc); d.R(sx+46*sc,620-86*sc,sx+92*sc,640,(4,4,6),10*sc)
    silhouette(d,110,900,1.0,(6,6,8)); d.E(110,900-148,16,18,(196,150,120,60))
    # circulos de respiracion/pulso
    for k in range(3): a=(u*.8+k*.33)%1; d.E(110,760,16+a*70,16+a*70,None,(255,255,255,int(120*(1-a))),3)
    return im
def sceneG(u):
    im=new((2,2,4),(10,8,12)); d=D(im)
    b=sm(u/.8)
    lantern_light(d,270,520,300*b,u,1.2); 
    d.R(262,540,278,620,(230,226,214),3); d.E(270,520,8,22+4*math.sin(u*14),(255,224,150))
    for k in range(24): a=k*.26+u*.3; d.E(270+math.cos(a)*220,520+math.sin(a)*280,3,3,(255,220,150,150))
    ptext(d,100,200,"ESCONDERSE",6.0,(255,224,150),int(255*b))
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur)); return 1.0+.2*sm(p),270,520
core.CAM=cam
if __name__=="__main__": core.main()
