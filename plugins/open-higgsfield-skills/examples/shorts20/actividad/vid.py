import sys; sys.path.insert(0,"..")
from art import *
def cam_overlay(d,u,t0=0,date="1 OCT"):
    d.R(0,0,540,960,None,0,(255,255,255,40),6); 
    if int(u*1.2)%2==0: d.E(46,50,9,9,(240,40,40))
    ptext(d,66,40,"REC",3.4,(240,240,240)); 
    s=int(t0+u*60)%60; m=(int(t0+u*60)//60)%60
    ptext(d,330,40,"%02d:%02d"%(m,s),3.4,(240,240,240))
def night_room(d,u,door=0.0):
    gradient(d,0,560,(10,12,18),(20,22,30)); d.R(0,560,540,960,(26,22,22),0)
    for k in range(6): d.L(0,590+k*55,540,590+k*55,(0,0,0,50),2)
    d.R(0,540,540,560,(10,10,14),0)
    # cama y puerta entreabierta en la oscuridad
    d.R(60,640,400,760,(70,64,72),10); d.R(60,610,120,780,(40,32,28),4); d.R(80,646,380,672,(110,106,118),6)
    d.R(410,300,520,640,(6,6,10),4)
    d.P([(410,300),(410+30+door*60,310),(410+30+door*60,640),(410,640)],(26,20,18))
def sceneA(u,final=False):
    im=new((8,8,12),(18,18,24)); d=D(im); night_room(d,u,0.0)
    b=sm(u/1.2)
    # cifras: 15.000 -> 190.000.000 
    d.R(40,150,500,330,(0,0,0,150),10); ptext(d,60,170,"15 MIL",9,(120,230,150)); ptext(d,60,250,"190 MILL",9,(255,200,90),)
    cam_overlay(d,u,0,"")
    return im
def sceneB(u):
    im=new((10,10,16),(24,24,32)); d=D(im); night_room(d,u,.3)
    # casa unifamiliar con camara domestica
    d.R(30,160,300,430,(80,70,76),6); d.P([(10,170),(165,70),(320,170)],(60,44,48)); d.R(120,300,190,430,(30,24,28),3); d.R(60,210,100,260,(255,220,130),2)
    d.R(330,740,500,860,(40,40,50),12); d.E(415,800,38,38,(20,22,30)); d.E(415,800,26,26,(70,100,160)); d.E(404,790,8,8,(255,255,255,200))
    ptext(d,300,190,"2007",8,(255,255,255)); ptext(d,40,330,"OREN PELI",3.6,(255,220,120))
    cam_overlay(d,u,10)
    return im
def sceneC(u):
    im=new((6,8,12),(14,14,22)); d=D(im); night_room(d,u,.2+.25*sm((u-3)/2))
    # camara fija: marco de trípode abajo y tiempo avanzando rapido
    d.L(270,880,200,960,(60,60,72),8); d.L(270,880,340,960,(60,60,72),8); d.L(270,880,270,960,(60,60,72),8)
    d.R(250,830,290,880,(30,30,40),6)
    ptext(d,40,190,"CAMARA FIJA",5,(255,255,255))
    for k in range(10): d.R(0,((u*120)+k*100)%960,540,((u*120)+k*100)%960+2,(255,255,255,18),0)
    cam_overlay(d,u,30+u*3)
    return im
def sceneD(u):
    im=new((10,10,16),(26,26,36)); d=D(im)
    # guion con una pagina y una sugerencia; sin retratos reales
    d.R(130,160,410,620,(236,232,220),8); 
    for k in range(10): d.R(160,200+k*36,380-((k*37)%60),210+k*36,(110,106,98),2)
    d.R(130,160,410,200,(210,60,60),8); ptext(d,150,170,"FINAL",5,(255,255,255))
    t=sm((u-1.5)/1.0)
    d.L(160,520,380,520,(210,60,60,int(255*t)),6); d.L(160,520,380,430,(210,60,60,int(255*t)),0)
    d.R(300,640,500,860,(255,230,120,int(255*t)),8); ptext(d,318,670,"SUGIERE",4,(40,30,10)); ptext(d,318,720,"CAMBIAR",4,(40,30,10))
    return im
def sceneE(u):
    im=new((8,8,14),(20,20,28)); d=D(im)
    # dos finales: el original tachado y el nuevo; claqueta; cine
    d.R(40,160,250,420,(60,60,72,230),10); ptext(d,58,200,"ORIGINAL",3.6,(200,200,210)); d.L(40,160,250,420,(210,60,60),6); d.L(250,160,40,420,(210,60,60),6)
    d.R(290,160,500,420,(255,230,120),10); ptext(d,304,200,"NUEVO",3.6,(40,30,10)); 
    ptext(d,40,540,"2009",11,(255,255,255)); 
    clapper(d,270,780,1.5,open_=clamp(math.sin(u*2.0)))
    return im
def sceneF(u):
    im=new((6,6,10),(16,16,24)); d=D(im)
    b=sm(u/3.0); base=780
    d.R(100,base-8,200,base,(120,230,150),4)
    d.R(310,base-520*b,420,base,(255,200,90),6)
    ptext(d,70,base+30,"15 MIL",3.4,(255,255,255)); ptext(d,300,base+30,"190 MILL",3.4,(255,255,255))
    for k in range(12): d.E(365+math.sin(k+u*3)*50,base-520*b-14-((u*70+k*36)%120),3.6,3.6,(255,230,130,200))
    ptext(d,40,190,"TAQUILLA",6,(255,255,255))
    return im
def sceneG(u):
    im=new((6,8,12),(14,16,24)); d=D(im)
    # camara de mano con ojo/lente que reaparece; "metraje encontrado"
    d.R(150,300,390,560,(30,32,40),20); d.R(390,360,470,500,(24,26,34),10); d.E(270,430,76,76,(14,16,22)); d.E(270,430,56,56,(60,90,140)); d.E(270,430,32,32,(6,8,12)); d.E(252,412,10,10,(255,255,255,220))
    d.E(420,330,8,8,(240,40,40,int(255*(math.sin(u*5)>0))))
    ptext(d,40,190,"METRAJE",6,(255,255,255)); ptext(d,40,250,"ENCONTRADO",6,(255,220,120))
    cam_overlay(d,u,55)
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    return 1.0,270,480
core.CAM=cam
if __name__=="__main__": core.main()
