import sys; sys.path.insert(0,"..")
from art import *
def mansion(d,u,x=270,y=620,sc=1.0,lit=True):
    d.R(x-150*sc,y-200*sc,x+150*sc,y,(34,28,38),0); d.P([(x-170*sc,y-200*sc),(x-70*sc,y-300*sc),(x+70*sc,y-300*sc),(x+170*sc,y-200*sc)],(24,20,28))
    d.P([(x-40*sc,y-300*sc),(x,y-380*sc),(x+40*sc,y-300*sc)],(24,20,28)); d.R(x+90*sc,y-340*sc,x+112*sc,y-280*sc,(24,20,28),0)
    for k in range(3):
        for r in range(2): d.R(x-120*sc+k*90*sc,y-170*sc+r*86*sc,x-76*sc+k*90*sc,y-120*sc+r*86*sc,(255,200,110,int(220*flicker(u,k*3+r,4))) if lit and (k+r)%2 else (14,12,18),2*sc)
    d.R(x-20*sc,y-76*sc,x+20*sc,y,(70,44,36),2*sc)
def lightning(d,u,t0=1.0):
    p=(u-t0)%4.0
    if p<.12: d.R(0,0,540,960,(255,255,255,int(180*(1-p/.12))),0)
def poly_hero(d,x,y,sc,ang=0.0,col=(210,170,90)):
    """personaje de pocos poligonos, sombreado plano"""
    c=math.cos(ang);
    def P(pts,cc): d.P([(x+px*sc*(c*.4+.6) if False else x+px*sc,y+py*sc) for px,py in pts],cc)
    P([(-16,-60),(16,-60),(22,0),(-22,0)],(60,50,50)); P([(-14,-120),(14,-120),(18,-60),(-18,-60)],tuple(int(v*.7) for v in col)); P([(0,-120),(14,-120),(18,-60),(0,-60)],col)
    P([(-14,-150),(14,-150),(12,-120),(-12,-120)],(230,190,160)); P([(0,-150),(14,-150),(12,-120),(0,-120)],(210,170,140))
    P([(-18,-168),(0,-182),(18,-168),(14,-150),(-14,-150)],(60,40,30))
    P([(-30,-116),(-18,-120),(-16,-70),(-26,-70)],tuple(int(v*.6) for v in col)); P([(18,-120),(30,-116),(26,-70),(16,-70)],col)
    P([(-18,0),(-4,0),(-6,40),(-22,40)],(40,34,34)); P([(4,0),(18,0),(22,40),(6,40)],(50,42,42))
def poly_monster(d,x,y,sc,u):
    d.P([(x-40*sc,y),(x,y-140*sc),(x+40*sc,y)],(70,100,60)); d.P([(x,y-140*sc),(x+40*sc,y),(x+10*sc,y-20*sc)],(50,80,44))
    d.P([(x-26*sc,y-120*sc),(x+26*sc,y-120*sc),(x,y-176*sc)],(90,120,80)); d.E(x-8*sc,y-134*sc,4*sc,4*sc,(255,60,40)); d.E(x+8*sc,y-134*sc,4*sc,4*sc,(255,60,40))
    d.P([(x-40*sc,y-80*sc),(x-70*sc,y-40*sc),(x-34*sc,y-60*sc)],(70,100,60)); d.P([(x+40*sc,y-80*sc),(x+70*sc,y-40*sc),(x+34*sc,y-60*sc)],(70,100,60))
def hall(d,u):
    d.R(0,0,540,960,(60,46,44),0)
    for k in range(10): d.R(k*60,0,k*60+4,640,(0,0,0,40),0)
    d.R(0,640,540,960,(100,70,50),0)
    for k in range(8): d.L(0,660+k*40,540,660+k*40,(0,0,0,50),2)
    d.R(330,130,490,420,(14,12,20),6); d.R(330,130,490,420,None,6,(110,80,60),8)
    d.R(40,250,200,640,(90,56,40),6); d.R(60,270,180,440,(70,42,30),4); d.R(60,460,180,620,(70,42,30),4)
    d.R(240,420,330,640,(120,80,50),6)
    d.E(300,180,12,12,(255,220,150,200)); d.L(300,100,300,168,(40,30,30),3)
    d.R(0,0,540,960,(0,0,0,70),0)
def camera_icon(d,x,y,sc):
    d.R(x-30*sc,y-18*sc,x+22*sc,y+18*sc,(30,30,36),6*sc); d.P([(x+22*sc,y-8*sc),(x+44*sc,y-18*sc),(x+44*sc,y+18*sc),(x+22*sc,y+8*sc)],(50,50,58)); d.E(x-8*sc,y,8*sc,8*sc,(90,120,170)); d.E(x+10*sc,y-24*sc,8*sc,8*sc,(240,60,60))
def sceneA(u,final=False):
    im=new((6,8,18),(26,28,44)); d=D(im); stars(d,u,30,300); d.E(400,120,32,32,(230,230,245,200))
    d.R(0,640,540,960,(10,14,12),0)
    mansion(d,u,270,640,1.5)
    fogband(d,u,620,820,(150,160,175),50,8); lightning(d,u,1.0)
    return im
def sceneB(u):
    im=new((8,12,30),(20,30,60)); d=D(im)
    d.R(70,360,160,620,(0,40,150),0); d.R(160,360,250,620,(240,240,244),0); d.R(250,360,340,620,(220,30,50),0)
    ptext(d,40,200,"1992",9,(255,255,255)); ptext(d,40,640,"INFOGRAMES",5,(255,255,255)); ptext(d,40,710,"FRANCIA",5,(255,214,120))
    return im
def sceneC(u):
    im=new((20,16,22),(60,46,44)); d=D(im); hall(d,u)
    poly_hero(d,270,780,1.9,0.0)
    d.R(300,720,420,760,(90,60,40),4); ptext(d,40,235,"MANSION",7,(255,255,255))
    return im
def sceneD(u):
    im=new((20,16,22),(60,46,44)); d=D(im); hall(d,u)
    d.R(0,0,540,960,(255,255,255,0),0)
    poly_hero(d,180,800,1.7,u); poly_monster(d,400,800,1.5,u)
    # etiquetas de poligonos y fondo dibujado
    d.R(20,240,260,300,(0,0,0,150),8); ptext(d,34,256,"POLIGONOS",3.8,(255,214,120))
    d.R(280,240,520,300,(0,0,0,150),8); ptext(d,294,256,"FONDO DIBUJADO",2.8,(255,255,255))
    for k in range(10):
        a=k*.62+u; d.L(180,640,180+math.cos(a)*40,640+math.sin(a)*40,(255,255,255,70),1.5)
    return im
def sceneE(u):
    im=new((20,16,22),(60,46,44)); d=D(im)
    p=int(u*.5)%2
    if p==0: hall(d,u)
    else:
        d.R(0,0,540,960,(40,30,40),0); corridor(d,u,speed=0.0,wall=(80,56,48),floor=(60,40,34),ceil=(30,24,30),door=(100,70,50),light=(255,200,120),n=8)
    poly_hero(d,270 if p==0 else 300,800,1.7,0.5)
    camera_icon(d,70,90,1.6)
    d.R(0,0,540,960,None,0,(255,255,255,60),6)
    ptext(d,40,235,"CAMARA FIJA",5,(255,255,255))
    return im
def sceneF(u):
    im=new((10,12,24),(28,30,56)); d=D(im); b=sm(u/1.0)
    d.R(150,260,390,600,(236,196,60),12); ptext(d,262,360,"1",30*b,(120,80,10)) if False else None
    ptext(d,230,340,"1",14,(120,80,10))
    d.E(270,640,80,40,(236,196,60)); d.R(240,640,300,740,(236,196,60),6)
    poly_hero(d,270,900,1.3,0.0)
    for k in range(24): a=k*.5+u; d.E(270+math.cos(a)*(200+k*3),440+math.sin(a)*(200+k*3),2.5,2.5,(255,230,140,int(220*abs(math.sin(u*2+k)))))
    ptext(d,40,235,"PIONERO",8,(255,255,255))
    return im
def sceneG(u):
    im=new((8,10,18),(22,24,38)); d=D(im)
    d.R(60,240,200,400,(50,50,60),8); ptext(d,92,300,"1992",3.6,(255,214,120))
    for k in range(3):
        d.R(230+k*90,420+k*60,310+k*90,500+k*60,(120,40,40),6); ptext(d,246+k*90,446+k*60,"RE",5,(255,255,255))
    d.L(200,330,240,430,(255,255,255,140),4); d.P([(240,430),(226,416),(244,414)],(255,255,255,200))
    mansion(d,u,270,860,.8)
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx in(0,7,4,6): return 1.0,270,480
    return 1.0+.08*sm(p),270,480
core.CAM=cam
if __name__=="__main__": core.main()
