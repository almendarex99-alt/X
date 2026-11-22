import sys; sys.path.insert(0,"..")
from art import *
from rig import *
GRN=(110,255,150)
HUNT=dict(skin=(226,184,150),hair=(60,44,32),hairstyle="short",shirt=(70,86,110),shirt2=None,pants=(44,48,60),shoes=(30,26,24),sleeve="long",coat=None,hat=None)
HUNT2=dict(HUNT,hair=(180,110,50),hairstyle="ponytail",shirt=(120,70,70),skin=(236,196,160))
HUNT3=dict(HUNT,hair=(30,26,24),hairstyle="bun",shirt=(60,110,90),skin=(210,160,120),hat="headphones")
GHOST=dict(skin=(214,226,246),hair=(196,212,240),hairstyle="long",shirt=(222,232,252),skirt_col=(210,224,250),dress=True,sleeve="long",eyes=(10,12,20),brow=(150,170,200),mouth_col=(20,24,40),shoes=(214,226,246))
def ghost_deco(d,hx,hy,sc):
    for sg in(-1,1): d.E(hx+sg*8.5*sc,hy-3*sc,6*sc,9*sc,(6,8,16,255))
    d.E(hx,hy+12*sc,4.4*sc,8*sc,(6,8,16,255))
def ghost(d,x,y,sc,u,pose=None,a=255,reach=0.0):
    fy=y-26*sc+math.sin(u*2)*8*sc
    d.E(x,y+4*sc,60*sc,8*sc,(0,0,0,50))
    d.E(x,fy-120*sc,96*sc,150*sc,(210,226,255,34)); d.E(x,fy-120*sc,66*sc,110*sc,(210,226,255,40))
    po=pose or dict(P_idle(u),mouth=.8,al=(.9+.3*reach,1.6),ar=(.9+.3*reach,1.6),curlL=.2,curlR=.2,spreadL=1.0,spreadR=1.0,hands_front=True)
    person(d,x,fy,sc,u,po,GHOST,deco=ghost_deco)
    for k in range(4): d.E(x-30*sc+k*20*sc,fy-6*sc+math.sin(u*3+k)*5*sc,10*sc,18*sc,(214,226,246,230))
def house_room(d,u):
    gradient(d,0,560,(6,8,16),(16,20,34)); d.R(0,560,540,960,(30,24,26),0)
    for k in range(7): d.L(0,590+k*50,540,590+k*50,(0,0,0,60),2)
    d.R(0,540,540,560,(10,8,10),0)
    d.R(40,150,200,410,(10,12,22),6); d.R(40,150,200,410,None,6,(70,60,50),8); d.L(120,150,120,410,(70,60,50),6); d.E(120,230,50,70,(200,220,255,int(20+10*math.sin(u))))
    d.R(330,360,490,640,(24,18,20),6); d.R(330,360,490,640,None,6,(70,60,50),6)
def torch(dd,x,y,a,s): dd.R(x-6,y-14,x+6,y+26,(60,60,70),4); dd.E(x,y+30,10,7,(255,240,180))
def beam(d,x,y,tx,ty): flashlight(d,x,y,tx,ty,spread=.3,L=620,a=70)
def emf(d,x,y,sc,lvl):
    d.R(x-36*sc,y-90*sc,x+36*sc,y+90*sc,(40,44,50),10*sc)
    for k in range(5): d.R(x-20*sc,y+60*sc-k*28*sc,x+20*sc,y+78*sc-k*28*sc,((60,230,90) if k<2 else (240,220,60) if k<4 else (240,60,50)) if k<lvl else (30,32,36),3*sc)
def mic(d,x,y,sc):
    d.R(x-20*sc,y-60*sc,x+20*sc,y+20*sc,(70,74,82),20*sc)
    for k in range(5): d.L(x-18*sc,y-50*sc+k*14*sc,x+18*sc,y-50*sc+k*14*sc,(30,32,36),2*sc)
    d.A(x,y+10*sc,34*sc,34*sc,0,180,(130,134,142),4*sc); d.L(x,y+44*sc,x,y+90*sc,(130,134,142),5*sc)
def waves(d,x,y,u,col=GRN,n=4,r0=40):
    for k in range(n): t=((u*.6+k/n)%1); d.A(x,y,r0+t*190,r0*.9+t*170,-60,60,col+(int(200*(1-t)),),4); d.A(x,y,r0+t*190,r0*.9+t*170,120,240,col+(int(200*(1-t)),),4)
def sceneA(u,final=False):
    im=new((6,8,16),(16,20,34)); d=D(im); house_room(d,u)
    b=sm(u/1.0) if not final else 1.0
    ghost(d,380,800,1.5,u,a=int(150*b+60))
    o=person(d,140,900,1.4,u,dict(P_walk(u,2.0),ar=(1.2,2.0)),HUNT,props={"r":torch})
    beam(d,o["hand_r"][0],o["hand_r"][1],380,640)
    return im
def sceneB(u):
    im=new((4,6,14),(12,16,30)); d=D(im); stars(d,u,40,380); d.E(420,120,30,30,(235,235,245,220))
    d.R(110,380,430,700,(16,14,20),0); d.P([(90,380),(270,260),(450,380)],(12,10,16))
    for (x,y) in ((150,450),(330,450),(150,580),(330,580)): d.R(x,y,x+60,y+70,(255,210,120,int(180*flicker(u,x,4))) if (x+y)%3 else (20,20,28),2)
    d.R(230,600,310,700,(30,22,22),2); d.R(0,700,540,960,(14,18,16),0)
    for k,(x,st) in enumerate(((120,HUNT),(250,HUNT2),(390,HUNT3))):
        o=person(d,x+u*8,950,1.1,u,dict(P_walk(u,2.6,k),ar=(1.2,2.0)),st,props={"r":torch}); beam(d,o["hand_r"][0],o["hand_r"][1],270,640)
    ptext(d,40,200,"2020",9,(255,255,255))
    return im
def sceneC(u):
    im=new((10,12,20),(22,24,36)); d=D(im); d.R(0,780,540,960,(50,38,30),0); d.R(0,780,540,790,(255,255,255,20),0)
    d.R(330,620,500,780,(34,34,40),10); d.E(415,700,40,40,(16,16,22)); d.E(415,700,26,26,(80,110,160)); d.E(405,690,7,7,(255,255,255,200))
    def emfp(dd,x,y,a,s): dd.R(x-16,y-40,x+16,y+40,(40,44,50),5); [dd.R(x-9,y+26-k*14,x+9,y+34-k*14,((60,230,90) if k<2 else (240,220,60) if k<4 else (240,60,50)) if k<int(1+u*1.2)%6 else (30,32,36),2) for k in range(5)]
    def thp(dd,x,y,a,s): dd.R(x-6,y-44,x+6,y+30,(224,224,230),6); dd.E(x,y+32,9,9,(220,60,60)); dd.R(x-3,y-32+10,x+3,y+24,(80,150,255),2)
    person(d,200,1010,1.7,u,dict(al=(.9,2.1),ar=(.9,2.1),ll=(.05,.05),lr=(.05,.05),bob=math.sin(u*2),tilt=.04,look=(.5,.4),mouth=.2,curlL=.9,curlR=.9,hands_front=True),HUNT,props={"l":emfp,"r":thp})
    for k,t in enumerate(["EMF","TEMP","CAMARA"]): ptext(d,60+k*160,830,t,3.6,(255,255,255))
    return im
def sceneD(u):
    im=new((6,8,16),(14,18,30)); d=D(im)
    waves(d,380,520,u,n=5,r0=90); mic(d,380,520,2.0)
    person(d,150,960,1.9,u,dict(P_talk(u),ar=(.9,1.3),mouth=.5+.5*math.sin(u*9)),HUNT3)
    for k in range(22):
        h=10+abs(math.sin(k*.8+u*7))*60*sm(u/1.0); d.R(40+k*22,880-h,40+k*22+12,880+h*0,GRN+(180,),2)
    ptext(d,40,190,"VOZ",12,(255,255,255))
    return im
def sceneE(u):
    im=new((6,8,16),(16,20,34)); d=D(im); house_room(d,u)
    ghost(d,380,820,1.6,u,reach=.2)
    person(d,130,930,1.55,u,dict(P_talk(u),ar=(1.2,1.5)),HUNT2)
    t=sm((u-.6)/.8); d.R(40,300,290,380,(255,255,255,int(230*t)),10); ptext(d,54,320,"ESTAS AQUI?",3.4,(20,20,30))
    t2=sm((u-2.8)/.8); d.R(260,420,500,500,(180,200,255,int(230*t2)),10); ptext(d,276,442,"...",8,(10,10,20))
    return im
def sceneF(u):
    im=new((6,8,16),(14,18,30)); d=D(im); house_room(d,u)
    near=clamp(u/6.0)
    ghost(d,lerp(520,330,near),840,lerp(1.2,2.0,near),u,reach=1.0)
    person(d,120+near*60,930,1.4,u,dict(P_walk(u,6.0),al=(.8,1.5),ar=(.8,1.5),mouth=1.0,tilt=-.08),HUNT)
    d.R(40,225,500,255,(255,255,255,40),8); d.R(40,225,40+460*(1-.7*near),255,GRN+(230,),8); ptext(d,40,265,"CORDURA",3.4,(255,255,255))
    return im
def sceneG(u):
    im=new((6,8,16),(14,18,30)); d=D(im); house_room(d,u)
    waves(d,150,700,u,n=4,r0=60)
    person(d,130,960,1.7,u,dict(P_idle(u),ar=(1.9,2.8),mouth=.5+.5*math.sin(u*8),look=(.5,0)),HUNT)
    ghost(d,390,840,1.5,u,reach=.4)
    d.A(390,560,60,70,-40,40,(230,240,255,160),4); d.A(390,560,90,100,-40,40,(230,240,255,100),4)
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx in(0,7): return 1.0+.12*sm(p),270,520
    return 1.0+.1*sm(p),270+14*math.sin(u*.9),490
core.CAM=cam
if __name__=="__main__": core.main()
