import sys; sys.path.insert(0,"..")
from art import *
RED=(190,30,30); GRN=(30,120,50)
def stripes(d,x0,y0,x1,y1):
    d.R(x0,y0,x1,y1,RED,0); k=0
    for y in range(int(y0),int(y1),18):
        if k%2: d.R(x0,y,x1,min(y+9,y1),GRN,0)
        k+=1
def hat(d,x,y,sc):
    d.E(x,y,80*sc,16*sc,(120,90,60)); d.R(x-44*sc,y-70*sc,x+44*sc,y,(130,96,64),6*sc); d.R(x-44*sc,y-22*sc,x+44*sc,y-8*sc,(60,40,30),0)
def claw(d,x,y,sc,ang=0.0):
    pts=rotpts([(x-18*sc,y),(x+18*sc,y),(x+18*sc,y+50*sc),(x-18*sc,y+50*sc)],x,y,ang); d.P(pts,(130,90,60))
    for k in range(4): d.P(rotpts([(x-16*sc+k*10*sc,y+50*sc),(x-10*sc+k*10*sc,y+50*sc),(x-8*sc+k*10*sc,y+120*sc)],x,y,ang),(200,206,214))
def bed(d,x,y,sc):
    d.R(x-150*sc,y-30*sc,x+150*sc,y+60*sc,(110,90,110),10*sc); d.R(x-150*sc,y-110*sc,x-128*sc,y+70*sc,(70,50,40),4*sc); d.R(x+128*sc,y-80*sc,x+150*sc,y+70*sc,(70,50,40),4*sc)
    d.R(x-140*sc,y-26*sc,x+130*sc,y-4*sc,(200,200,214),6*sc); d.R(x-132*sc,y-60*sc,x-50*sc,y-26*sc,(230,230,240),8*sc)
def room(d,u):
    gradient(d,0,560,(18,14,30),(40,30,56)); d.R(0,560,540,960,(30,22,30),0)
    for k in range(7): d.L(0,590+k*50,540,590+k*50,(0,0,0,50),2)
    d.R(330,110,500,360,(16,20,40),6); d.R(330,110,500,360,None,6,(100,80,70),8); d.L(415,110,415,360,(100,80,70),6); d.E(415,200,18,18,(240,240,250,200))
def dream_fog(d,u): fogband(d,u,520,820,(150,120,170),50,10)
def sceneA(u,final=False):
    im=new((18,14,30),(40,30,56)); d=D(im); room(d,u); bed(d,200,740,1.3); dream_fog(d,u)
    d.E(130,700,40,28,(240,230,240,230)); d.E(300,670,28,16,(30,20,30,int(60+40*math.sin(u*2)))) if False else None
    b=sm(u/1.2) if not final else 1.0
    # sombra del sombrero y garra en la pared
    hat(d,420,470,1.2*b); claw(d,440,520,1.0*b,.2)
    stripes(d,60,150,160,230)
    return im
def sceneB(u):
    im=new((14,14,24),(34,34,52)); d=D(im); d.R(0,640,540,960,(24,26,28),0)
    d.R(180,260,360,640,(40,36,44),0); d.P([(160,260),(270,150),(380,260)],(30,28,34))
    d.R(230,420,310,640,(70,50,40),2); d.R(200,300,260,380,(255,210,130,int(200*flicker(u,3,5))),2)
    d.R(40,650,500,730,(0,160,90),6); ptext(d,60,670,"ELM STREET",8,(255,255,255))
    ptext(d,40,200,"1984",9,(255,255,255))
    return im
def sceneC(u):
    im=new((30,28,26),(62,58,52)); d=D(im); d.R(0,700,540,960,(90,66,46),0)
    d.R(90,150,450,700,(236,230,214),4); d.R(90,150,450,210,(60,56,50),4); ptext(d,110,170,"NOTICIA",8,(240,240,240))
    for k in range(3): d.R(110,250+k*50,250,290+k*50,(180,176,164),2)
    for k in range(9): d.R(270,250+k*24,430,258+k*24,(110,106,98),2)
    for k in range(5): d.R(110,420+k*24,250,428+k*24,(110,106,98),2)
    return im
def sceneD(u):
    im=new((10,12,24),(26,30,52)); d=D(im); d.R(0,740,540,960,(40,30,30),0)
    # reloj, tazas de cafe y ojo que se cierra
    d.E(150,300,90,90,(236,236,240)); d.E(150,300,90,90,None,(40,40,50),6)
    a=u*2.0; d.L(150,300,150+math.cos(a)*62,300+math.sin(a)*62,(30,30,36),5); d.L(150,300,150+math.cos(a*12)*76,300+math.sin(a*12)*76,(210,40,40),3)
    for k in range(3): d.R(310+k*60,640,350+k*60,700,(240,240,244),6); d.R(350+k*60,656,364+k*60,680,(240,240,244),4); d.E(330+k*60,626-(u*30+k*20)%40,8,12,(240,240,250,90))
    lid=.2+.8*(0.5+0.5*math.sin(u*1.2))
    d.E(270,520,120,60,(240,240,246)); d.E(270,520,32,32,(40,60,100)); d.E(270,520,14,14,(10,10,14)); d.R(130,430,410,430+(1-lid)*100+0,(34,28,36),0)
    d.E(270,430+(1-lid)*100,142,6,(90,70,70))
    ptext(d,40,225,"NO DORMIR",7,(255,255,255))
    return im
def sceneE(u):
    im=new((24,10,28),(60,24,60)); d=D(im)
    corridor(d,u,speed=.22,wall=(70,44,60),floor=(34,30,34),ceil=(40,30,44),door=(90,60,50),light=(255,140,90),n=9,doors=False,pulse=flicker(u,3,5))
    for k in range(6): d.L(0,520+k*70,540,520+k*70,(255,255,255,0),1)
    dream_fog(d,u)
    hat(d,270,430,.8)
    return im
def sceneF(u):
    im=new((30,26,22),(64,54,44)); d=D(im); d.R(0,640,540,960,(90,66,46),0)
    # pupitre de colegio con nombre
    d.R(60,420,480,500,(160,120,80),6); d.R(80,500,100,700,(80,70,66),2); d.R(440,500,460,700,(80,70,66),2)
    d.R(90,440,300,470,(255,255,255,40),4); ptext(d,110,444,"FRED",8,(60,40,30))
    silhouette(d,380,640,1.6,(30,26,30))
    ptext(d,40,225,"EL COLEGIO",5,(255,255,255))
    return im
def sceneG(u):
    im=new((14,10,24),(34,24,50)); d=D(im);
    d.R(40,200,250,420,(236,230,214),6); d.R(40,200,250,240,(60,56,50),6);
    for k in range(5): d.R(56,260+k*30,230-((k*29)%50),270+k*30,(110,106,98),2)
    d.R(290,200,500,420,(160,120,80),6); ptext(d,310,290,"FRED",7,(60,40,30))
    stripes(d,70,520,470,640); hat(d,270,500,1.4); claw(d,270,640,1.2,0.0)
    ptext(d,40,225,"DOS MIEDOS",6,(255,255,255))
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx in(0,7): return 1.0,270,480
    return 1.0+.1*sm(p),270,480
core.CAM=cam
if __name__=="__main__": core.main()
