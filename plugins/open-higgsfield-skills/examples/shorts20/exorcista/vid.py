import sys; sys.path.insert(0,"..")
from art import *
ICE=(170,210,240)
def snow(d,u,n=60,a=170):
    for k in range(n):
        x=(rnd(k)*560+math.sin(u*1.3+k)*14)%540; y=(rnd(k,1)*980+u*(40+rnd(k,2)*60))%980-10
        d.E(x,y,2+rnd(k,3)*2.5,2+rnd(k,3)*2.5,(235,245,255,a))
def breath(d,x,y,u,dirx=1,n=7,a=110):
    for q in range(n):
        t=((u*.5+q/n)%1); d.E(x+dirx*t*170,y-t*60+math.sin(t*6+q)*8,(14+t*50),(10+t*36),(235,245,255,int(a*(1-t))))
def room(d,u,frost=0.5):
    gradient(d,0,560,(20,30,46),(36,52,72)); d.R(0,560,540,960,(36,30,34),0)
    for k in range(7): d.L(0,590+k*50,540,590+k*50,(0,0,0,50),2)
    d.R(0,540,540,560,(24,20,24),0)
    # ventana con escarcha
    d.R(330,110,500,380,(24,34,52),6); d.R(330,110,500,380,None,6,(110,90,70),8); d.L(415,110,415,380,(110,90,70),6); d.L(330,245,500,245,(110,90,70),6)
    for k in range(16): a=k*.4; d.L(415+math.cos(a)*12,245+math.sin(a)*12,415+math.cos(a)*(30+k*5)*frost,245+math.sin(a)*(30+k*5)*frost,(230,245,255,130),2)
    d.E(415,245,80*frost,80*frost,(230,245,255,int(50*frost)))
def bed(d,x,y,sc):
    d.R(x-130*sc,y-30*sc,x+130*sc,y+50*sc,(120,100,100),10*sc); d.R(x-130*sc,y-96*sc,x-110*sc,y+60*sc,(70,50,40),4*sc); d.R(x+110*sc,y-76*sc,x+130*sc,y+60*sc,(70,50,40),4*sc)
    d.R(x-120*sc,y-30*sc,x+110*sc,y-10*sc,(200,200,210),6*sc); d.R(x-110*sc,y-56*sc,x-40*sc,y-28*sc,(224,224,232),8*sc)
def sceneA(u,final=False):
    im=new((8,14,28),(24,44,70)); d=D(im); room(d,u,0.4+0.5*sm(u/3))
    snow(d,u,50,120)
    silhouette(d,160,820,1.5,(10,12,18)); breath(d,205,615,u,1,8,150)
    # termometro
    d.R(40,110,76,420,(230,230,236),14); d.R(50,120,66,400,(30,40,56),8); d.E(58,420,24,24,(220,60,60)); 
    lvl=lerp(270,60,sm(u/3.0)); d.R(52,120+lvl,64,400,(80,150,255),4)
    ptext(d,40,450,"FRIO",5,(190,220,255))
    return im
def sceneB(u):
    im=new((6,6,12),(16,14,24)); d=D(im)
    # casa oscura con una sola ventana iluminada (escenario del rodaje)
    d.R(90,300,450,720,(18,16,24),0); d.P([(70,300),(270,180),(470,300)],(14,12,20))
    d.R(220,420,320,500,(255,210,120,int(210*flicker(u,2,5))),2); d.R(220,420,320,500,None,2,(10,10,14),5); d.L(270,420,270,500,(10,10,14),4)
    d.R(130,700,410,740,(10,8,12),0)
    clapper(d,150,820,1.2,open_=clamp(math.sin(u*2.2)))
    d.E(400,120,34,34,(235,235,240,230))
    ptext(d,40,200,"1973",8,(255,255,255)); ptext(d,40,265,"FRIEDKIN",3.6,(255,220,120))
    return im
def sceneC(u):
    im=new((10,16,30),(30,46,70)); d=D(im); room(d,u,.9); bed(d,200,740,1.3)
    # unidades de frio que soplan hielo
    for sg,x in((-1,70),(1,470)):
        d.R(x-50,150,x+50,260,(150,160,176),8); 
        for k in range(5): d.R(x-40,164+k*18,x+40,170+k*18,(40,48,60),2)
        for q in range(6): t=((u*.7+q/6)%1); d.E(x-sg*20*t*-1+sg*t*60,260+t*120,14+t*30,10+t*20,ICE+(int(110*(1-t)),))
    # contador de temperatura bajando
    tmp=int(lerp(18,-4,sm(u/5.0))); 
    d.R(180,60,360,140,(8,10,14),8); 
    ptext(d,196,84,("-" if tmp<0 else "")+str(abs(tmp))+" C",7,(120,220,255))
    snow(d,u,40,100)
    return im
def sceneD(u):
    im=new((6,10,20),(14,24,40)); d=D(im)
    # perfil del rostro exhalando vapor, primer plano
    d.E(170,520,120,160,(222,196,170)); d.P([(260,500),(300,520),(262,540)],(222,196,170)); d.E(205,470,8,5,(30,20,20)); d.A(228,572,22,8,200,340,(130,70,60),4)
    d.E(60,460,130,180,(24,20,28))
    b=sm(u/1.0)
    for k in range(9): 
        t=((u*.45+k/9)%1); d.E(270+t*260,568-t*90+math.sin(t*8+k)*10,(24+t*80)*b,(18+t*50)*b,(240,248,255,int(160*(1-t))))
    snow(d,u,30,80)
    ptext(d,40,730,"NO ES UN EFECTO",4.2,(255,255,255)); 
    return im
def sceneE(u):
    im=new((10,8,14),(26,22,32)); d=D(im)
    d.R(0,700,540,960,(30,24,26),0); d.R(0,120,540,136,(60,60,70),0)
    # arnes de seguridad atado a la cintura, con cable lateral a una polea; la figura se desplaza hacia atras (sin gore)
    d.R(40,690,500,740,(80,60,120,200),8)   # colchoneta
    k=math.sin(u*4)*(1 if int(u*2)%2 else .3); sx=230-abs(k)*90
    d.E(470,150,16,16,(120,120,130)); d.R(440,120,500,136,(60,60,70),3)
    d.L(470,150,sx+20,610,(200,200,210),3)
    silhouette(d,sx,700,1.5,(90,96,120)); d.R(sx-24,596,sx+24,624,(210,170,60),4)
    d.E(sx,704,70,10,(0,0,0,60))
    for q in range(3): d.A(sx-90,600,24+q*16,24+q*16,150,210,(255,255,255,120-q*30),3)
    ptext(d,40,190,"SE CUENTA",5,(255,220,120)); 
    return im
def sceneF(u):
    im=new((6,6,12),(14,12,22)); d=D(im)
    # forma de onda de un grito (barras), con el rollo de pelicula
    for k in range(30):
        h=20+abs(math.sin(k*.6+u*8))*180*(1-abs(k-15)/18)*sm(u/1.0)
        d.R(30+k*16,480-h,30+k*16+10,480+h,(255,230,160,255),2)
    film_strip(d,780,u,h=100)
    ptext(d,40,190,"SE QUEDO",6,(255,255,255)); ptext(d,40,250,"EN LA PELICULA",4,(255,220,120))
    return im
def sceneG(u):
    im=new((6,10,20),(16,30,48)); d=D(im); snow(d,u,70,170)
    b=sm(u/1.2); d.E(270,470,150*b,90*b,(235,240,250)); d.E(270,470,52*b,52*b,(30,60,110)); d.E(270,470,20*b,20*b,(6,6,10)); d.E(262,462,6*b,6*b,(255,255,255))
    for k in range(5): d.L(0,470,540,470,(255,255,255,0),1)
    breath(d,270,640,u,1,7,120)
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx in(0,2,7): return 1.0,270,480
    return 1.0+.15*sm(p),270,480
core.CAM=cam
if __name__=="__main__": core.main()
