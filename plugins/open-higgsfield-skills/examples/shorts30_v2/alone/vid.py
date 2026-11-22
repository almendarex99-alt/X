import sys; sys.path.insert(0,"..")
from art import *
from rig import *
HERO=dict(skin=(230,190,156),hair=(60,44,32),hairstyle="short",shirt=(180,160,120),coat=(110,84,56),pants=(60,52,48),shoes=(40,30,26),sleeve="long",belt=(70,50,40),brow=(40,28,20))
HEROINE=dict(skin=(240,200,166),hair=(120,70,40),hairstyle="long",shirt=(60,80,120),dress=True,skirt_col=(70,92,134),sleeve="long",shoes=(40,30,30))
MONST=dict(skin=(80,110,66),hair=(60,80,50),hairstyle="bald",shirt=(70,100,60),pants=(56,80,50),shoes=(40,50,36),claws=True,eyes=(255,60,40),sleeve="none",bulk=1.2,ear=False,brow=(20,30,20),mouth_col=(60,10,10),tail=(80,110,66))
def mon_deco(d,hx,hy,sc):
    for sg in(-1,1): d.E(hx+sg*8.5*sc,hy-3*sc,11*sc,9*sc,(255,60,40,60))
def monster(d,x,y,sc,u,ph=0.0): return person(d,x,y,sc,u,dict(P_zombie(u,ph,1.8),mouth=1.0),MONST,deco=mon_deco)
def mansion(d,u,x=270,y=620,sc=1.0,lit=True):
    d.R(x-150*sc,y-200*sc,x+150*sc,y,(34,28,38),0); d.P([(x-170*sc,y-200*sc),(x-70*sc,y-300*sc),(x+70*sc,y-300*sc),(x+170*sc,y-200*sc)],(24,20,28))
    d.P([(x-40*sc,y-300*sc),(x,y-380*sc),(x+40*sc,y-300*sc)],(24,20,28)); d.R(x+90*sc,y-340*sc,x+112*sc,y-280*sc,(24,20,28),0)
    for k in range(3):
        for r in range(2): d.R(x-120*sc+k*90*sc,y-170*sc+r*86*sc,x-76*sc+k*90*sc,y-120*sc+r*86*sc,(255,200,110,int(220*flicker(u,k*3+r,4))) if lit and (k+r)%2 else (14,12,18),2*sc)
    d.R(x-20*sc,y-76*sc,x+20*sc,y,(70,44,36),2*sc)
def lightning(d,u,t0=1.0):
    p=(u-t0)%4.0
    if p<.12: d.R(0,0,540,960,(255,255,255,int(180*(1-p/.12))),0)
def hall(d,u):
    d.R(0,0,540,960,(60,46,44),0)
    for k in range(10): d.R(k*60,0,k*60+4,700,(0,0,0,40),0)
    d.R(0,700,540,960,(100,70,50),0)
    for k in range(8): d.L(0,720+k*34,540,720+k*34,(0,0,0,50),2)
    d.R(340,130,500,430,(14,12,20),6); d.R(340,130,500,430,None,6,(110,80,60),8)
    d.R(30,250,190,700,(90,56,40),6); d.R(50,270,170,450,(70,42,30),4); d.R(50,470,170,680,(70,42,30),4)
    d.E(300,190,12,12,(255,220,150,200)); d.L(300,110,300,178,(40,30,30),3)
    d.R(0,0,540,960,(0,0,0,70),0)
def camera_icon(d,x,y,sc):
    d.R(x-30*sc,y-18*sc,x+22*sc,y+18*sc,(30,30,36),6*sc); d.P([(x+22*sc,y-8*sc),(x+44*sc,y-18*sc),(x+44*sc,y+18*sc),(x+22*sc,y+8*sc)],(50,50,58)); d.E(x-8*sc,y,8*sc,8*sc,(90,120,170)); d.E(x+10*sc,y-24*sc,8*sc,8*sc,(240,60,60))
def torch(dd,x,y,a,s): dd.R(x-6,y-12,x+6,y+26,(60,60,70),4); dd.E(x,y+30,10,7,(255,240,180))
def sceneA(u,final=False):
    im=new((6,8,18),(26,28,44)); d=D(im); stars(d,u,30,300); d.E(400,120,32,32,(230,230,245,200))
    d.R(0,720,540,960,(10,14,12),0); mansion(d,u,270,720,1.45)
    fogband(d,u,700,900,(150,160,175),50,8); lightning(d,u,1.0)
    person(d,130+u*14,950,1.2,u,P_walk(u,2.6),HERO,facing="back")
    return im
def sceneB(u):
    im=new((8,12,30),(20,30,60)); d=D(im)
    d.R(70,360,160,620,(0,40,150),0); d.R(160,360,250,620,(240,240,244),0); d.R(250,360,340,620,(220,30,50),0)
    ptext(d,40,200,"1992",9,(255,255,255)); ptext(d,40,700,"INFOGRAMES",5,(255,255,255)); ptext(d,40,770,"FRANCIA",5,(255,214,120))
    person(d,420,980,1.5,u,dict(P_idle(u),ar=(1.4,1.2),mouth=.4),dict(HERO,coat=None,shirt=(60,60,90),hat="cap",cap_col=(60,60,90)))
    return im
def sceneC(u):
    im=new((20,16,22),(60,46,44)); d=D(im); hall(d,u)
    person(d,180,960,1.6,u,dict(P_walk(u,2.6),ar=(1.3,2.0)),HERO,props={"r":torch})
    person(d,400,960,1.5,u,P_walk(u,2.6,1.4),HEROINE)
    ptext(d,40,235,"MANSION",7,(255,255,255))
    return im
def sceneD(u):
    im=new((20,16,22),(60,46,44)); d=D(im); hall(d,u)
    person(d,180,960,1.6,u,dict(P_walk(u,3.2),ar=(1.2,2.0)),HERO,props={"r":torch})
    monster(d,400,960,1.5,u)
    d.R(20,240,260,300,(0,0,0,150),8); ptext(d,34,256,"POLIGONOS",3.8,(255,214,120))
    d.R(280,240,520,300,(0,0,0,150),8); ptext(d,294,256,"FONDO DIBUJADO",2.8,(255,255,255))
    return im
def sceneE(u):
    im=new((20,16,22),(60,46,44)); d=D(im)
    p=int(u*.5)%2
    if p==0: hall(d,u)
    else:
        d.R(0,0,540,960,(40,30,40),0); corridor(d,u,speed=0.0,wall=(80,56,48),floor=(60,40,34),ceil=(30,24,30),door=(100,70,50),light=(255,200,120),n=8)
    person(d,270+(30 if p else 0),960,1.6,u,dict(P_walk(u,2.8),ar=(1.2,2.0)),HERO,props={"r":torch})
    camera_icon(d,70,90,1.6); d.R(0,0,540,960,None,0,(255,255,255,60),6)
    ptext(d,40,235,"CAMARA FIJA",5,(255,255,255))
    return im
def sceneF(u):
    im=new((10,12,24),(28,30,56)); d=D(im); b=sm(u/1.0)
    d.R(150,260,390,560,(236,196,60),12); ptext(d,230,340,"1",14,(120,80,10))
    for k in range(24): a=k*.5+u; d.E(270+math.cos(a)*(200+k*3),440+math.sin(a)*(200+k*3),2.5,2.5,(255,230,140,int(220*abs(math.sin(u*2+k)))))
    person(d,270,980,1.6,u,dict(P_cheer(u),ar=(2.4,2.8),al=(.9,1.2)),HERO)
    ptext(d,40,235,"PIONERO",8,(255,255,255))
    return im
def sceneG(u):
    im=new((8,10,18),(22,24,38)); d=D(im)
    d.R(40,240,200,400,(50,50,60),8); ptext(d,70,300,"1992",3.6,(255,214,120))
    for k in range(3): d.R(230+k*90,420+k*60,310+k*90,500+k*60,(120,40,40),6); ptext(d,246+k*90,446+k*60,"RE",5,(255,255,255))
    d.L(200,330,240,430,(255,255,255,140),4)
    mansion(d,u,270,860,.7)
    person(d,100,960,1.3,u,dict(P_point(u),ar=(1.6,1.6)),HERO)
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx in(0,7): return 1.0+.12*sm(p),270,560
    return 1.0+.1*sm(p),270+14*math.sin(u*.9),480
core.CAM=cam
if __name__=="__main__": core.main()
