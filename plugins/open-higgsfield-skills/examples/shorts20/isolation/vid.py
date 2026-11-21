import sys; sys.path.insert(0,"..")
from art import *
GRN=(110,255,150); AMB=(255,170,60)
def alien_head(d,x,y,sc,u,glow=0.0):
    d.E(x,y,40*sc,90*sc,(6,8,10)); d.P([(x-30*sc,y-20*sc),(x+30*sc,y-20*sc),(x+10*sc,y-120*sc),(x-10*sc,y-120*sc)],(6,8,10))
    d.R(x-18*sc,y+60*sc,x+18*sc,y+140*sc,(6,8,10),10*sc)
    d.E(x-12*sc,y+68*sc,3*sc,3*sc,(255,255,255,int(255*glow)))
    d.E(x,y-30*sc,50*sc,20*sc,(255,255,255,18))
def tracker(d,x,y,sc,u,rate=1.0,blip=(0,0),bw=True):
    """detector de movimiento: cuerpo amarillento con pantalla verde y barrido radar"""
    d.R(x-90*sc,y-130*sc,x+90*sc,y+130*sc,(166,160,110),14*sc); d.R(x-90*sc,y-130*sc,x-76*sc,y+130*sc,(255,255,255,40),14*sc)
    d.R(x-70*sc,y-100*sc,x+70*sc,y+30*sc,(8,24,14),8*sc)
    cx,cy=x,y-35*sc
    for r in (20,40,60): d.E(cx,cy,r*sc,r*sc*.7,None,GRN+(120,),2*sc)
    a=(u*rate*2.2)%(2*math.pi); d.L(cx,cy,cx+math.cos(a)*62*sc,cy+math.sin(a)*43*sc,GRN+(230,),3*sc)
    for i in range(6): aa=a-i*.1; d.L(cx,cy,cx+math.cos(aa)*62*sc,cy+math.sin(aa)*43*sc,GRN+(int(80-i*12),),2*sc)
    if blip!=(0,0): d.E(cx+blip[0]*sc,cy+blip[1]*sc,5*sc,5*sc,GRN+(int(255*(1-((u*rate*2.2)%1.0)*.5)),))
    d.E(x-40*sc,y+70*sc,12*sc,12*sc,(220,60,40)); d.R(x+10*sc,y+54*sc,x+70*sc,y+90*sc,(60,60,50),4*sc)
def station(d,u,speed=.06,steam=True):
    corridor(d,u,speed=speed,wall=(74,92,98),floor=(44,52,56),ceil=(36,44,50),door=(150,110,60),light=(255,200,120),pulse=flicker(u,1,8),n=9,doors=True)
    if steam:
        for k in range(5):
            t=k*1.6+.8; s=depth(t); xx=planes(s)[0]+26*s
            for q in range(3): a=((u*.7+k*.31+q*.33)%1); d.E(xx,HY+30*s-a*120*s,(12+a*30)*s,(10+a*18)*s,(230,236,240,int(110*(1-a))))
def brain(d,x,y,sc,col,glow=0.0):
    for sg in(-1,1):
        d.E(x+sg*28*sc,y,36*sc,30*sc,col+(255,)); d.E(x+sg*20*sc,y-6*sc,20*sc,16*sc,col+(0,))
    d.L(x,y-30*sc,x,y+30*sc,(0,0,0,80),3*sc)
    for k in range(4): d.A(x+(k-1.5)*18*sc,y-4*sc,14*sc,10*sc,180,360,(255,255,255,70),2*sc)
    if glow>0: d.E(x,y,100*sc,80*sc,col+(int(50*glow),))
def sceneA(u,final=False):
    im=new((8,14,18),(30,44,52)); d=D(im)
    station(d,u)
    # rejilla de ventilacion con la silueta que se desplaza
    d.R(150,60,390,170,(20,24,28),6)
    for k in range(7): d.R(160+k*32,70,168+k*32,160,(60,70,78),2)
    ax=lerp(170,370,(u*.18)%1); d.E(ax,116,14,48,(4,4,6,190)); d.L(ax-20,150,ax-80,122,(4,4,6,160),6)
    tracker(d,430,780,.8,u,rate=1.0+u*.2,blip=(-20,-10))
    return im
def sceneB(u):
    im=new((20,24,28),(40,52,60)); d=D(im)
    d.R(0,640,540,960,(30,36,42)); d.R(0,640,540,646,(255,255,255,24))
    # monitor CRT verde con plano de estacion, estilo anos 70
    d.R(60,150,480,540,(40,46,50),14); d.R(76,166,464,524,(4,20,10),8)
    for k in range(6): d.L(100,200+k*50,440,200+k*50,GRN+(60,),2)
    for k in range(5): d.R(110+k*66,230+(k%2)*60,160+k*66,270+(k%2)*60,GRN+(30,),3); d.R(110+k*66,230+(k%2)*60,160+k*66,270+(k%2)*60,None,3,GRN+(150,),2)
    for k in range(int(358/6)): d.R(76,166+k*6,464,167+k*6,(0,0,0,60))
    keyboard(d,150,570,240,50); person_back(d,270,790,1.45,1,u)
    ptext(d,40,90,"CREATIVE  ASSEMBLY",3.6,GRN); ptext(d,40,126,"2014",4.0,GRN)
    return im
def sceneC(u):
    im=new((8,14,18),(24,34,44)); d=D(im)
    # dos cerebros: director (grande, con ojo) y alien (pequeno, con onda de sonido)
    a=sm(u/1.2)
    brain(d,150,330,1.5*a,(220,170,60),glow=1)
    d.E(150,170,40*a,22*a,(255,255,255,int(240*a))); d.E(150,170,12*a,12*a,(20,20,24,int(240*a)))
    brain(d,390,500,1.0*a,(80,200,170),glow=1)
    for k in range(3): t=(u*.7+k*.33)%1; d.A(470,500,30+t*60,30+t*60,-50,50,(110,255,200,int(180*(1-t))),3)
    ptext(d,40,520,"DIRECTOR",3.6,(255,255,255)); ptext(d,300,640,"ALIEN",3.6,(255,255,255))
    d.L(190,380,350,480,(255,255,255,110),3)
    return im
def sceneD(u):
    im=new((6,12,14),(16,30,34)); d=D(im)
    # plano superior de la estacion; el director sabe donde esta el jugador
    for r in range(8): d.L(0,60+r*100,540,60+r*100,GRN+(24,),2)
    for c in range(6): d.L(30+c*90,0,30+c*90,960,GRN+(24,),2)
    rooms=[(40,120,160,120),(240,120,260,120),(40,300,120,200),(180,300,160,200),(360,300,140,200),(40,540,200,140),(280,540,220,140)]
    for (x,y,w,h) in rooms: d.R(x,y,x+w,y+h,GRN+(26,),4); d.R(x,y,x+w,y+h,None,4,GRN+(140,),2)
    px,py=300,420; d.E(px,py,10,10,(255,90,70)); 
    for k in range(3): t=(u*.8+k*.33)%1; d.E(px,py,20+t*100,20+t*100,None,(255,90,70,int(200*(1-t))),3)
    ax,ay=lerp(100,260,sm(u/5.0)),lerp(620,470,sm(u/5.0)); d.E(ax,ay,8,8,(255,230,90)); d.E(ax,ay,26,26,None,(255,230,90,180),3)
    ptext(d,40,860,"SABE DONDE ESTAS",3.6,GRN)
    return im
def sceneE(u):
    im=new((6,10,12),(20,30,34)); d=D(im)
    station(d,u,speed=0.0,steam=False)
    ax=lerp(120,300,sm(u/5.0)); alien_head(d,ax,HY+40,1.2,u,glow=.6)
    # cono de vision y ondas de sonido de pasos
    d.P([(ax,HY+110),(ax+300,HY+10),(ax+300,HY+230)],GRN+(26,))
    for k in range(3): t=(u*.8+k*.33)%1; d.E(420,HY+330,20+t*170,12+t*80,None,(255,255,255,int(200*(1-t))),3)
    silhouette(d,420,HY+380,1.1,(8,10,14))
    ptext(d,40,880,"SOLO OIDO Y VISTA",3.4,(255,255,255))
    return im
def sceneF(u):
    im=new((6,10,12),(20,30,34)); d=D(im)
    station(d,u,speed=.02,steam=True)
    # taquilla donde se esconde el jugador, rendijas y detector cada vez mas rapido
    d.R(60,200,280,900,(70,86,92),10); 
    for k in range(10): d.R(90,260+k*20,250,272+k*20,(8,10,12),2)
    d.E(170,420,10,10,(255,255,255,int(160*abs(math.sin(u*2)))))
    near=clamp(u/6.0); ax=lerp(540,330,near); alien_head(d,ax,HY+80,lerp(.8,1.6,near),u,glow=near)
    tracker(d,420,800,.8,u,rate=1.0+near*3,blip=(int(-30*(1-near)),int(-20*(1-near))))
    return im
def sceneG(u):
    im=new((6,10,14),(16,28,36)); d=D(im); stars(d,u,50,960)
    b=sm(u/.8)
    brain(d,160,520,1.8*b,(220,170,60),glow=1); brain(d,380,520,1.8*b,(80,200,170),glow=1)
    alien_head(d,270,360,1.0,u,glow=b)
    for k in range(24): a=k*.26+u*.3; d.E(270+math.cos(a)*230,520+math.sin(a)*300,3,3,GRN+(150,))
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur)); return 1.0+.2*sm(p),270,500
core.CAM=cam
if __name__=="__main__": core.main()
