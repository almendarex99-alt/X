import sys; sys.path.insert(0,"..")
from art import *
BONE=(232,226,208)
def skull(d,x,y,sc,tilt=0.0):
    d.E(x,y,22*sc,24*sc,BONE+(255,)); d.R(x-12*sc,y+14*sc,x+12*sc,y+32*sc,BONE+(255,),4*sc)
    for sg in(-1,1): d.E(x+sg*9*sc,y-2*sc,6.5*sc,7.5*sc,(20,16,18))
    d.P([(x-3*sc,y+8*sc),(x+3*sc,y+8*sc),(x,y+2*sc)],(20,16,18))
    for k in range(4): d.L(x-9*sc+k*6*sc,y+22*sc,x-9*sc+k*6*sc,y+32*sc,(30,24,24),1.4*sc)
def skeleton(d,x,y,sc,u,wave=0.0):
    d.L(x,y-60*sc,x,y+40*sc,BONE+(255,),6*sc)
    for k in range(5): d.R(x-26*sc+k*2*sc,y-48*sc+k*14*sc,x+26*sc-k*2*sc,y-42*sc+k*14*sc,BONE+(255,),3*sc)
    d.R(x-18*sc,y+36*sc,x+18*sc,y+56*sc,BONE+(255,),6*sc)
    for sg in(-1,1): d.L(x+sg*10*sc,y+56*sc,x+sg*14*sc,y+130*sc,BONE+(255,),6*sc); d.L(x+sg*26*sc,y-52*sc,x+sg*(40+16*wave*sg)*sc,y+16*sc,BONE+(255,),5*sc)
    skull(d,x,y-86*sc,sc)
def mud(d,u,y0=420):
    gradient(d,y0,960,(54,40,28),(30,22,16))
    for k in range(40): x=rnd(k)*560; y=y0+10+rnd(k,1)*(960-y0); d.E(x,y,16+rnd(k,2)*26,6+rnd(k,2)*8,(18,12,8,70))
def pool(d,u):
    gradient(d,0,400,(8,10,24),(30,30,56)); d.E(400,120,32,32,(240,240,250,220))
    d.R(0,400,540,960,(60,54,64),0)
    d.P([(60,540),(480,540),(540,780),(0,780)],(40,120,150)); d.P([(60,540),(480,540),(450,570),(90,570)],(120,180,200))
    for k in range(8): y=560+k*28; d.L(80-k*8,y,460+k*8,y,(255,255,255,40),2)
def sceneA(u,final=False):
    im=new((6,8,18),(20,22,40)); d=D(im); stars(d,u,40,360)
    mud(d,u,520)
    b=sm(u/1.2)
    for k,(x,y,s) in enumerate([(120,640,1.0),(280,700,1.35),(430,660,1.1)]):
        wob=math.sin(u*3+k)*8*(1-b)
        skeleton(d,x,y+(1-b)*180+wob,s,u,wave=math.sin(u*3+k))
    d.R(0,0,540,0,(0,0,0),0)
    return im
def sceneB(u):
    im=new((8,10,22),(24,26,48)); d=D(im); pool(d,u)
    ptext(d,40,200,"1982",8,(255,255,255)); ptext(d,40,265,"HOOPER  SPIELBERG",3.4,(255,220,120))
    clapper(d,380,360,1.3,open_=clamp(math.sin(u*2.2)))
    return im
def sceneC(u):
    im=new((10,8,20),(30,24,44)); d=D(im); pool(d,u)
    # cadaveres que emergen del barro (esqueletos): fondo de piscina con barro
    d.P([(60,540),(480,540),(540,960),(0,960)],(40,28,20,230))
    for k,(x,y) in enumerate([(130,700),(300,760),(420,690)]):
        r=sm((u-.6-k*.7)/1.4); skeleton(d,x,y+(1-r)*160,.9,u,wave=math.sin(u*3+k))
    return im
def sceneD(u):
    im=new((10,12,22),(30,34,50)); d=D(im)
    # caja de proveedor medico vs plastico: dos precios
    d.R(30,190,250,450,(150,110,70),8); d.R(30,190,250,230,(120,84,50),8)
    ptext(d,60,300,"MEDICO",5,(30,24,16)); skull(d,140,380,1.0)
    d.R(290,190,510,450,(90,150,200),8); d.R(290,190,510,230,(60,110,160),8)
    ptext(d,310,300,"PLASTICO",4.4,(10,24,40)); skull(d,400,380,1.0)
    for x,lab,hgt,col in((140,"REAL",50,(120,200,140)),(400,"FALSO",190,(240,110,90))):
        d.R(x-50,780-hgt,x+50,780,col+(255,),6); ptext(d,x-48,800,lab,4.4,(255,255,255))
    ptext(d,40,190,"SE CUENTA",5,(255,220,120))
    return im
def sceneE(u):
    im=new((8,10,20),(24,28,44)); d=D(im); mud(d,u,640); pool(d,u)
    # silueta de actriz rodeada de huesos
    silhouette(d,270,760,1.4,(220,150,130)); d.E(270,760,40,8,(0,0,0,70))
    for k in range(10): a=k*.62+u*.1; skull(d,270+math.cos(a)*210,760+math.sin(a)*54*(1+(k%2)),.45)
    skeleton(d,90,740,.55,u); skeleton(d,450,740,.55,u,wave=-1)
    return im
def sceneF(u):
    im=new((6,6,12),(16,14,24)); d=D(im)
    # escalofrio: zigzag que recorre la espalda
    for q in range(5):
        pts=[(270+math.sin(k*1.4+u*6+q)*24*(1-abs(k-8)/10),200+k*60) for k in range(0,14)]
        for i in range(len(pts)-1): d.L(pts[i][0]+(q-2)*50,pts[i][1],pts[i+1][0]+(q-2)*50,pts[i+1][1],(160,220,255,int(180-q*20)),4)
    skull(d,270,720,2.4); 
    ptext(d,40,190,"ESCALOFRIO EXTRA",4,(255,255,255))
    return im
def sceneG(u):
    im=new((6,6,12),(16,14,24)); d=D(im)
    # tele con estatica, icono de la saga: pantalla azul con ruido y manos en la pantalla
    d.R(90,240,450,640,(60,52,56),20); d.R(110,260,430,620,(10,14,22),12)
    noise_static(d,110,260,320,360,u,a=170,cell=10)
    for k in range(7): d.R(110,260+((u*140+k*60)%360),430,264+((u*140+k*60)%360),(255,255,255,60),0)
    d.R(220,640,320,700,(40,34,38),4); d.E(270,830,20,8,(0,0,0,60))
    ptext(d,40,190,"UN CLASICO",6,(255,255,255))
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx in(1,3,5,6): return 1.0,270,480
    return 1.0+.15*sm(p),270,500
core.CAM=cam
if __name__=="__main__": core.main()
