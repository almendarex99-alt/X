import sys; sys.path.insert(0,"..")
from art import *
from common import ps1f
CLAY=(150,98,70)
def imp(d,x,y,sc,u,col=CLAY,eyes=(255,210,60),prints=True,lit=0.0):
    sh=tuple(int(c*.72) for c in col)
    shadow(d,x,y+4,70*sc,8*sc,90)
    for sg in(-1,1): d.R(x+sg*20*sc-14*sc,y-60*sc,x+sg*20*sc+14*sc,y,sh+(255,),6*sc)
    d.R(x-48*sc,y-168*sc,x+48*sc,y-52*sc,col+(255,),26*sc)
    for sg in(-1,1):
        d.R(x+sg*48*sc-12*sc,y-160*sc,x+sg*(48+16)*sc+12*sc,y-80*sc+math.sin(u*3+sg)*8*sc,col+(255,),10*sc)
        for q in range(3): d.P([(x+sg*(60+q*3)*sc,y-84*sc+q*10*sc),(x+sg*(76)*sc,y-70*sc+q*10*sc),(x+sg*(58)*sc,y-76*sc+q*10*sc)],(230,220,200))
    d.E(x,y-200*sc,38*sc,38*sc,col+(255,))
    for sg in(-1,1): d.P([(x+sg*24*sc,y-228*sc),(x+sg*50*sc,y-262*sc),(x+sg*36*sc,y-216*sc)],(220,210,190))
    d.E(x,y-196*sc,30*sc,24*sc,tuple(min(255,int(c*1.12)) for c in col))
    for sg in(-1,1): d.E(x+sg*14*sc,y-208*sc,8*sc,6*sc,eyes+(255,)); d.E(x+sg*14*sc,y-208*sc,16*sc,14*sc,eyes+(60,))
    d.R(x-18*sc,y-182*sc,x+18*sc,y-170*sc,(40,10,10),5*sc)
    for k in range(5): d.P([(x-16*sc+k*8*sc,y-182*sc),(x-12*sc+k*8*sc,y-182*sc),(x-14*sc+k*8*sc,y-174*sc)],(240,236,220))
    if prints:
        for q in range(7):
            ax=x-30*sc+(q%4)*20*sc; ay=y-130*sc+(q//4)*34*sc
            for r in (3,6,9): d.A(ax,ay,r*sc,r*sc*.8,200,360,(0,0,0,50),1.2*sc)
    if lit: d.R(x,y-170*sc,x+48*sc,y-52*sc,(0,0,0,int(90*lit)),26*sc)
def lump(d,x,y,sc):
    d.E(x,y,90*sc,40*sc,(120,78,54)); d.E(x-20*sc,y-12*sc,50*sc,18*sc,(160,108,78,160))
    for q in range(6): d.A(x-60*sc+q*24*sc,y,8*sc,6*sc,200,360,(0,0,0,50),1.5*sc)
def hand(d,x,y,sc,ang=0.0):
    pts=rotpts([(x-18*sc,y),(x+18*sc,y),(x+14*sc,y+80*sc),(x-14*sc,y+80*sc)],x,y,ang); d.P(pts,SK)
    for k in range(4): d.E(x-13*sc+k*9*sc,y-4*sc,5*sc,10*sc,SK)
def hell_bg(d,u):
    gradient(d,0,520,(24,4,6),(120,22,12)); d.R(0,520,540,960,(36,14,12),0)
    for k in range(10): x=rnd(k)*540; d.E(x,520+rnd(k,1)*20,60+rnd(k,2)*60,10,(255,100,30,40))
    for k in range(5): d.L(0,540+k*70,540,540+k*70,(255,90,30,40),2)
    for k in range(20): d.E((rnd(k,5)*540+u*20)%540,(rnd(k,6)*900-u*50)%900,2,2,(255,150,60,160))
def sceneA(u,final=False):
    im=new((24,4,6),(120,22,12)); d=D(im); hell_bg(d,u); b=sm(u/1.2) if not final else 1.0
    imp(d,270,760,1.9*(.85+.15*b),u,eyes=(255,210,60))
    return im
def sceneB(u):
    im=new((30,24,20),(60,50,44)); d=D(im)
    corridor(d,u,speed=.35,wall=(90,80,70),floor=(60,46,36),ceil=(40,40,44),door=(100,70,40),light=(255,224,160),n=9,doors=True)
    d.R(0,780,540,960,(110,96,86),0); d.R(0,780,540,788,(60,50,44),0)
    d.R(40,800,500,940,(80,70,64),6)
    d.E(270,870,36,40,(222,176,140)); d.E(256,862,4,4,(40,20,10)); d.E(284,862,4,4,(40,20,10)); d.R(262,882,278,886,(120,40,40),1)
    d.R(70,818,200,860,(20,10,10),4); ptext(d,82,826,"100",5,(240,60,40)); d.R(340,818,470,860,(20,10,10),4); ptext(d,352,826,"050",5,(240,200,60))
    d.R(240,690,300,780,(70,70,76),4); d.R(250,640,290,700,(110,110,118),4); d.R(264,620,276,650,(60,60,66),2)
    ptext(d,40,200,"1993",8,(255,255,255))
    return im
def sceneC(u):
    im=new((40,30,26),(70,56,48)); d=D(im); d.R(0,740,540,960,(90,60,40),0); d.R(0,740,540,748,(255,255,255,30),0)
    p=sm(u/5.5); lump(d,270,760,1.3)
    imp(d,270,730,.4+1.2*p,u,col=CLAY,prints=True)
    hand(d,150+20*math.sin(u*3),600,1.5,.5); hand(d,390-20*math.sin(u*3),600,1.5,-.5)
    ptext(d,40,190,"A MANO",8,(255,220,140))
    return im
def sceneD(u):
    im=new((20,18,22),(46,40,44)); d=D(im); d.R(0,700,540,960,(70,56,46),0)
    ang=u*1.4
    d.E(330,760,100,18,(110,96,86))
    imp(d,330+math.sin(ang)*10,740,.95,u,col=CLAY,eyes=(255,210,60) if math.cos(ang)>0 else (60,40,30))
    d.R(30,520,150,620,(34,34,40),10); d.E(150,570,34,34,(18,18,24)); d.E(150,570,22,22,(80,110,160)); d.E(142,562,6,6,(255,255,255,200))
    for sg in(-1,1): d.L(90,620,90+sg*40,760,(60,60,68),6)
    if math.sin(u*5)>.7: d.E(120,540,80,80,(255,255,230,90))
    for q in range(8):
        x=22+q*62; d.R(x,860,x+54,950,(236,236,236,230),3); imp(d,x+27+(q%2)*2,945,.2,u,col=CLAY,prints=False,eyes=(255,210,60) if q<4 else (60,40,30))
    ptext(d,40,190,"FOTOS",8,(255,220,140))
    return im
def sceneE(u):
    im=new((24,24,32),(50,50,64)); d=D(im)
    for r in range(3):
        for c in range(3):
            x=100+c*170; y=360+r*190; d.R(x-70,y-90,x+70,y+90,(0,0,0,70),6)
            imp(d,x,y+80,.55,u+r*.2+c*.1,col=CLAY,prints=False,eyes=(255,210,60) if (c+r)%3 else (60,40,30))
    ptext(d,40,190,"SPRITES",8,(255,255,255))
    return ps1f(im,block=9)
def sceneF(u):
    im=new((30,10,10),(100,30,18)); d=D(im); hell_bg(d,u)
    imp(d,270,820,2.2,u,col=CLAY,prints=True,lit=.8)
    d.E(270,830,160,12,(0,0,0,80))
    d.L(60,300,200,380,(255,240,200,120),4); d.E(60,300,10,10,(255,240,200))
    ptext(d,40,190,"VOLUMEN",8,(255,220,140))
    return im
def sceneG(u):
    im=new((34,26,24),(70,56,48)); d=D(im); b=sm(u/1.0)
    lump(d,110,720,.7); imp(d,270,730,.9,u,prints=False)
    d.R(380,560,500,700,(34,34,40),10); d.E(440,630,32,32,(80,110,160))
    for k in range(2): d.P([(180+k*20,640),(220+k*20,640),(220+k*20,626),(240+k*20,650),(220+k*20,674),(220+k*20,660),(180+k*20,660)],(255,220,140))
    imp(d,270,300,.8*b,u,col=CLAY)
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx in(0,7): return 1.0,270,480
    return 1.0+.1*sm(p),270,480
core.CAM=cam
if __name__=="__main__": core.main()
