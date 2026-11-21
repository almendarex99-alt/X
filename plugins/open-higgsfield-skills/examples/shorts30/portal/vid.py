import sys; sys.path.insert(0,"..")
from art import *
BLU=(60,170,255); ORG=(255,150,40)
def chamber(d,u,tint=(224,228,232)):
    d.R(0,0,540,960,tint,0)
    for r in range(12):
        for c in range(7): d.R(c*80+2,r*80+2,c*80+78,r*80+78,(236,240,244),2); d.R(c*80+2,r*80+2,c*80+78,r*80+6,(255,255,255,90),2)
    d.R(0,0,540,960,(0,0,0,26),0)
def ring(d,x,y,rx,ry,col,u=0.0):
    for k in range(4): d.E(x,y,rx*(1.2-k*.1),ry*(1.12-k*.08),col+(60+k*30,))
    d.E(x,y,rx,ry,col+(255,)); d.E(x,y,rx*.78,ry*.8,(10,14,24))
    for q in range(10): a=q*.63+u*2; d.E(x+math.cos(a)*rx*.9,y+math.sin(a)*ry*.9,3,3,(255,255,255,170))
def glados(d,x,y,sc,u,glow=1.0):
    for sg in(-2,-1,0,1,2): d.L(x+sg*12*sc,0,x+sg*20*sc,y-50*sc,(40,40,46),4*sc)
    d.E(x,y,52*sc,46*sc,(232,232,238)); d.E(x-14*sc,y-14*sc,28*sc,18*sc,(255,255,255,120)); d.E(x,y+24*sc,44*sc,14*sc,(190,190,198))
    d.R(x-22*sc,y+28*sc,x+22*sc,y+54*sc,(210,210,218),6*sc)
    d.E(x,y+2*sc,20*sc,20*sc,(20,20,24)); d.E(x,y+2*sc,13*sc,13*sc,(255,200,60,int(255*glow))); d.E(x,y+2*sc,30*sc,30*sc,(255,200,60,int(60*glow)))
    d.E(x,y+2*sc,4*sc,4*sc,(255,255,255,int(255*glow)))
def cake(d,x,y,sc,u,candle=True):
    shadow(d,x,y+4,90*sc,9*sc,80)
    d.R(x-70*sc,y-60*sc,x+70*sc,y,(120,70,50),6*sc); d.R(x-70*sc,y-90*sc,x+70*sc,y-58*sc,(250,244,236),8*sc)
    for k in range(7): d.E(x-60*sc+k*20*sc,y-58*sc,8*sc,10*sc,(250,244,236))
    d.R(x-70*sc,y-62*sc,x+70*sc,y-56*sc,(180,40,50),0)
    d.R(x-4*sc,y-120*sc,x+4*sc,y-90*sc,(230,230,240),1)
    if candle: d.E(x,y-130*sc,6*sc,10*sc+math.sin(u*9)*2*sc,(255,180,50)); d.E(x,y-130*sc,12*sc,16*sc,(255,200,80,50))
def cube(d,x,y,sc):
    d.R(x-34*sc,y-68*sc,x+34*sc,y,(150,150,158),6*sc); d.R(x-34*sc,y-68*sc,x+34*sc,y-58*sc,(210,210,218),6*sc)
    d.R(x-24*sc,y-58*sc,x+24*sc,y-10*sc,(110,110,118),4*sc);
    d.E(x-8*sc,y-42*sc,9*sc,9*sc,(255,120,170)); d.E(x+8*sc,y-42*sc,9*sc,9*sc,(255,120,170)); d.P([(x-17*sc,y-38*sc),(x+17*sc,y-38*sc),(x,y-20*sc)],(255,120,170))
def note(d,x,y,sc,col):
    d.E(x,y,9*sc,7*sc,col); d.R(x+7*sc,y-40*sc,x+10*sc,y,col,0); d.P([(x+10*sc,y-40*sc),(x+24*sc,y-28*sc),(x+10*sc,y-30*sc)],col)
def sceneA(u,final=False):
    im=new((8,8,12),(22,22,30)); d=D(im)
    b=sm(u/1.0) if not final else 1.0
    glados(d,270,420,2.6,u,glow=.7+.3*math.sin(u*3))
    for k in range(5): t=(u*.45+k*.2)%1; note(d,80+k*90+math.sin(u+k)*10,820-t*420,1.3,(255,200,60,int(220*(1-t))))
    return im
def sceneB(u):
    im=new((200,206,212),(226,230,236)); d=D(im); chamber(d,u)
    ring(d,130,540,74,150,BLU,u); ring(d,410,420,74,150,ORG,u)
    d.L(130,530,410,430,(255,255,255,90),6)
    d.R(150,740,390,900,(255,150,30),10); d.R(150,740,390,790,(40,40,48),10); ptext(d,170,752,"THE ORANGE BOX",3.2,(255,255,255)); ptext(d,170,830,"2007",9,(30,20,10))
    return im
def sceneC(u):
    im=new((190,194,200),(214,218,224)); d=D(im); chamber(d,u,tint=(204,206,212))
    # pared oscura con mensaje y tarta
    d.R(50,200,490,420,(40,40,46),8);
    for k in range(60): d.L(60+rnd(k)*420,210+rnd(k,1)*200,70+rnd(k)*420,214+rnd(k,1)*200,(255,255,255,18),1)
    ptext(d,66,250,"LA TARTA ES",7,(255,60,60)); ptext(d,66,320,"MENTIRA",7,(255,60,60))
    cake(d,270,780,1.4,u)
    return im
def sceneD(u):
    im=new((8,8,12),(26,26,34)); d=D(im)
    glados(d,270,360,2.2,u,glow=1.0)
    # microfono y nombre de la actriz
    d.R(250,640,290,760,(60,60,68),8); d.E(270,620,34,40,(120,120,128));
    for k in range(6): d.L(246,590+k*12,294,590+k*12,(30,30,34),2)
    d.L(270,760,270,860,(60,60,68),8); d.R(170,860,370,872,(60,60,68),4)
    ptext(d,40,190,"ELLEN MCLAIN",4.2,(255,255,255))
    return im
def sceneE(u):
    im=new((4,6,10),(10,16,26)); d=D(im)
    ptext(d,60,300,"STILL ALIVE",8,(120,230,150));
    for k in range(4): t=(u*.5+k*.25)%1; note(d,60+k*130,800-t*500,1.6,(255,200,60,int(220*(1-t))))
    for k in range(22):
        h=20+abs(math.sin(k*.7+u*6))*100; d.R(30+k*22,620-h,30+k*22+14,620+h,(120,230,150,170),2)
    ptext(d,60,860,"JONATHAN COULTON",3.2,(255,255,255))
    return im
def sceneF(u):
    im=new((4,8,10),(10,22,26)); d=D(im)
    for r in range(18):
        y=((u*70)+r*52)%900+30; w=160+rnd(r)*260; d.R(40,y,40+w,y+14,(120,230,150,int(200*(1-abs(y-450)/500))),2)
    d.R(0,0,540,120,(4,8,10),0); d.R(0,830,540,960,(4,8,10),0)
    d.E(270,780,10,10,(255,200,60)); ptext(d,40,190,"HUMOR NEGRO",5,(255,255,255))
    cube(d,420,720,1.2)
    return im
def sceneG(u):
    im=new((200,206,212),(226,230,236)); d=D(im); chamber(d,u)
    ring(d,150,420,70,140,BLU,u); ring(d,390,640,70,140,ORG,u)
    cube(d,150,830,1.3); cake(d,390,880,.7,u,candle=False)
    silhouette(d,270,880,1.4,(40,40,50))
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx in(0,7): return 1.0+.15*sm(p),270,440
    return 1.0+.08*sm(p),270,480
core.CAM=cam
if __name__=="__main__": core.main()
