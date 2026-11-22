import sys; sys.path.insert(0,"..")
from art import *
from rig import *
PALE=(232,230,222)
def gmask(d,hx,hy,sc):
    """mascara original de cara alargada con ojos y boca caidos, ajustada a la cabeza"""
    d.E(hx,hy+4*sc,22*sc,34*sc,PALE+(255,)); d.P([(hx-14*sc,hy+28*sc),(hx+14*sc,hy+28*sc),(hx,hy+44*sc)],PALE)
    for sg in(-1,1): d.P([(hx+sg*5*sc,hy-14*sc),(hx+sg*17*sc,hy-10*sc),(hx+sg*14*sc,hy+4*sc),(hx+sg*10*sc,hy+12*sc),(hx+sg*8*sc,hy+2*sc)],(8,8,10))
    d.P([(hx-8*sc,hy+12*sc),(hx+8*sc,hy+12*sc),(hx+10*sc,hy+24*sc),(hx,hy+36*sc),(hx-10*sc,hy+24*sc)],(8,8,10))
GHOST=dict(skin=PALE,hair=(8,8,10),hairstyle="bald",shirt=(10,10,14),pants=(10,10,14),shoes=(10,10,14),coat=(8,8,10),hat="hood",sleeve="long",face=False,mask=gmask,hands_col=(190,190,196),neck_col=(8,8,10),ear=False)
SCOUT=dict(skin=(226,184,150),hair=(60,44,32),hairstyle="short",shirt=(80,110,130),pants=(70,64,56),shoes=(50,44,40),sleeve="long",coat=(90,100,80))
CRAVEN=dict(skin=(230,190,156),hair=(180,180,186),hairstyle="short",beard=True,glasses=True,shirt=(60,60,70),coat=(40,44,56),pants=(50,50,60),sleeve="long")
PROD=dict(skin=(214,170,130),hair=(30,24,20),hairstyle="short",shirt=(200,200,210),coat=(60,60,80),pants=(50,50,64),sleeve="long")
CLERK=dict(skin=(240,200,160),hair=(150,100,50),hairstyle="bob",shirt=(200,60,60),pants=(50,56,76),sleeve="short")
def ghost(d,x,y,sc,u,pose=None,ph=0.0):
    return person(d,x,y,sc,u,pose or dict(P_walk(u,2.0,ph),al=(.35,.6),ar=(.35,.6)),GHOST)
def house_out(d,u):
    gradient(d,0,520,(40,30,60),(220,140,110)); d.E(400,200,60,60,(255,210,150,200))
    d.R(0,520,540,960,(24,22,26),0)
    d.R(100,300,440,540,(70,56,60),0); d.P([(80,300),(270,190),(460,300)],(50,38,44))
    for (x,y) in((130,360),(330,360),(130,460),(330,460)): d.R(x,y,x+80,y+70,(255,200,120,int(200*flicker(u,x,4))) if (x+y)%3 else (30,24,30),2)
    d.R(230,440,310,540,(40,28,28),2)
def sceneA(u,final=False):
    im=new((6,6,10),(20,16,24)); d=D(im); b=sm(u/1.0) if not final else 1.0
    d.E(270,420,240,330,(255,255,255,12))
    ghost(d,270,980,1.5+.3*b,u,dict(P_idle(u),al=(.25,.6),ar=(.25,.6),tilt=.1*math.sin(u*1.5)))
    for k in range(10): a=k*.62+u*.2; d.E(270+math.cos(a)*230,420+math.sin(a)*300,2.5,2.5,(255,255,255,50))
    return im
def sceneB(u):
    im=new((8,8,14),(24,22,32)); d=D(im); d.R(0,760,540,960,(14,12,18),0)
    clapper(d,380,820,1.3,open_=clamp(math.sin(u*2.2)))
    person(d,150,950,1.5,u,dict(P_idle(u),ar=(1.4,1.2),mouth=.5+.5*math.sin(u*7),curlR=.2),CRAVEN)
    ptext(d,40,200,"1996",9,(255,255,255)); ptext(d,40,300,"WES CRAVEN",4.6,(255,214,120))
    return im
def sceneC(u):
    im=new((40,30,60),(220,140,110)); d=D(im); house_out(d,u)
    d.R(330,360,410,430,(30,24,30),2); gmask(d,370,392,.9)
    def torch(dd,x,y,a,s): dd.R(x-6,y-12,x+6,y+26,(60,60,70),4); dd.E(x,y+30,10,7,(255,240,180))
    def clip(dd,x,y,a,s): dd.R(x-18,y-22,x+18,y+26,(120,86,56),4); dd.R(x-14,y-16,x+14,y+20,(240,236,222),2)
    o=person(d,120,950,1.5,u,dict(P_walk(u,2.0),ar=(1.3,2.0),al=(1.0,2.2),curlL=.9),SCOUT,props={"r":torch,"l":clip})
    flashlight(d,o["hand_r"][0],o["hand_r"][1],370,400,spread=.14,L=560,a=60)
    person(d,330,950,1.3,u,dict(P_walk(u,2.0,2),ar=(1.45,1.5)),PROD)
    ptext(d,40,235,"LOCALIZACIONES",4,(255,255,255))
    return im
def sceneD(u):
    im=new((24,20,30),(52,44,60)); d=D(im); d.R(0,740,540,960,(70,52,40),0)
    for r,y in enumerate((300,540)):
        d.R(0,y,540,y+14,(110,80,56),0)
        for c in range(4):
            x=70+c*135; col=[(70,110,70),(120,60,60),(60,70,120),(230,196,60)][(r+c)%4]
            if (r,c)==(1,2): gmask(d,x,y-70,1.0)
            else: d.E(x,y-60,34,46,col+(255,)); d.E(x-12,y-72,6,6,(10,10,12)); d.E(x+12,y-72,6,6,(10,10,12))
    def maskp(dd,x,y,a,s): gmask(dd,x,y-20,.9)
    person(d,120,960,1.4,u,dict(P_hold(u,r=(1.3,2.2),grip=.7),mouth=.3),CLERK)
    person(d,410,960,1.4,u,dict(P_hold(u,r=(1.3,1.5),grip=.2),ar=(1.4,1.4),mouth=.5,look=(-.5,0)),SCOUT)
    ptext(d,40,235,"DE TIENDA",7,(255,255,255))
    return im
def sceneE(u):
    im=new((8,8,12),(22,20,28)); d=D(im); b=sm(u/1.0)
    ghost(d,270,1000,1.9,u,dict(P_idle(u),al=(.4,.9),ar=(.4,.9),tilt=.08*math.sin(u*1.2)))
    ptext(d,40,235,"CARA ALARGADA",4.4,(255,214,120))
    return im
def sceneF(u):
    im=new((24,20,30),(52,44,60)); d=D(im); d.R(0,840,540,960,(60,48,40),0)
    d.R(120,190,420,520,(240,236,222),6)
    for k in range(7): d.R(144,236+k*28,396-((k*37)%100),244+k*28,(110,106,98),2)
    d.R(120,190,420,230,(210,60,60),6); ptext(d,136,198,"ACUERDO",4.4,(255,255,255))
    t=sm((u-1.5)/1.0); d.L(150,490,280,490,(30,40,120,int(255*t)),5)
    sh=sm(u/1.0)
    person(d,90,1000,1.6,u,dict(al=(.5,1.2),ar=(1.3+.08*math.sin(u*6),1.5+.1*math.sin(u*6)),ll=(.05,.05),lr=(.05,.05),bob=0,tilt=.04,look=(.6,0),mouth=.3,curlR=.6,hands_front=True),CRAVEN)
    person(d,450,1000,1.6,u,dict(al=(1.3+.08*math.sin(u*6),1.5+.1*math.sin(u*6)),ar=(.5,1.2),ll=(.05,.05),lr=(.05,.05),bob=0,tilt=-.04,look=(-.6,0),mouth=.3,curlL=.6,hands_front=True),PROD)
    return im
def sceneG(u):
    im=new((6,6,10),(20,16,24)); d=D(im)
    for k,x in enumerate((90,270,450)): ghost(d,x,900+(k%2)*30,1.15,u,dict(P_walk(u,2.0,k*1.2),al=(.3,.5),ar=(.3,.5)),) if False else ghost(d,x,900+(k%2)*30,1.15,u,ph=k*1.2)
    ptext(d,40,235,"ICONO",8,(255,255,255))
    film_strip(d,840,u,h=90)
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx in(0,7): return 1.0+.1*sm(p),270,520
    return 1.0+.1*sm(p),270+14*math.sin(u*.9),480
core.CAM=cam
if __name__=="__main__": core.main()
