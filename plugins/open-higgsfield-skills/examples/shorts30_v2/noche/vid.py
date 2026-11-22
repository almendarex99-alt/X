import sys; sys.path.insert(0,"..")
from art import *
from rig import *
def g(v): return (v,v,v)
ZB=dict(skin=g(176),hair=g(40),hairstyle="short",shirt=g(90),pants=g(52),shoes=g(24),sleeve="long",brow=g(30),eyes=g(10),mouth_col=g(30))
ZW=dict(ZB,hairstyle="long",hair=g(36),shirt=g(120),dress=True,skirt_col=g(110))
ZC=dict(ZB,hairstyle="bald",shirt=g(70),pants=g(40))
MAN=dict(skin=g(204),hair=g(30),hairstyle="short",shirt=g(210),pants=g(60),shoes=g(20),sleeve="long",brow=g(30),eyes=g(20),mouth_col=g(70))
WOMAN=dict(skin=g(214),hair=g(50),hairstyle="long",shirt=g(236),dress=True,skirt_col=g(226),sleeve="long",brow=g(40),eyes=g(20),mouth_col=g(70),shoes=g(30))
DIR=dict(MAN,glasses=True,beard=True,shirt=g(150),coat=g(60))
def farm(d,u,x=270,y=560,sc=1.0,lit=True):
    d.R(x-130*sc,y-120*sc,x+130*sc,y,g(38),0); d.P([(x-150*sc,y-120*sc),(x,y-220*sc),(x+150*sc,y-120*sc)],g(24)); d.R(x+70*sc,y-210*sc,x+96*sc,y-150*sc,g(30),0)
    for (dx,dy) in((-80,-90),(30,-90)): d.R(x+dx*sc,y+dy*sc,x+(dx+50)*sc,y+(dy+56)*sc,g(230) if lit and int(u*3+dx)%5 else g(12),2)
    d.R(x-20*sc,y-70*sc,x+20*sc,y,g(14),2)
def field(d,u,hz=560):
    d.R(0,hz,540,960,g(18),0)
    for k in range(40): x=rnd(k)*540; y=hz+10+rnd(k,1)*(960-hz); d.L(x,y,x+2,y-10,g(60),2)
def sky(d,u):
    gradient(d,0,560,g(6),g(46)); d.E(110,120,34,34,g(235)); d.E(110,120,70,70,g(235)+(30,))
    for k in range(30): d.E(rnd(k)*540,rnd(k,1)*300,1.5,1.5,g(220)+(170,))
def reel(d,x,y,sc,u):
    d.E(x,y,60*sc,60*sc,g(200)); d.E(x,y,52*sc,52*sc,g(40))
    for k in range(6): a=k*1.05+u*3; d.E(x+math.cos(a)*30*sc,y+math.sin(a)*30*sc,12*sc,12*sc,g(200))
    d.E(x,y,10*sc,10*sc,g(200))
def copyright(d,x,y,r,col=(255,255,255)):
    d.E(x,y,r,r,None,col,r*.12); ptext(d,x-r*.34,y-r*.5,"C",r*.2,col)
def sceneA(u,final=False):
    im=new(g(6),g(40)); d=D(im); sky(d,u); field(d,u); farm(d,u,150,600,.9)
    b=sm(u/1.0) if not final else 1.0
    for k,(x,y,sc,st) in enumerate(((430,740,1.0,ZB),(330,690,.8,ZW),(230,660,.7,ZC),(500,820,1.4,ZC))):
        person(d,x-u*7*(1+k*.1)%80,y+ (0),sc,u,P_zombie(u,k*1.3),st)
    return im
def sceneB(u):
    im=new(g(10),g(50)); d=D(im); d.R(0,760,540,960,g(14),0)
    d.L(170,760,130,960,g(60),8); d.L(170,760,210,960,g(60),8); d.L(170,760,170,960,g(60),8)
    d.R(120,600,230,700,g(30),10); d.E(250,650,28,28,g(20)); d.E(250,650,20,20,g(70)); d.R(228,646,248,654,g(30),2)
    person(d,100,930,1.4,u,P_hold(u,r=(1.3,2.3)),dict(DIR),props={"r":lambda dd,x,y,a,s: dd.R(x-4,y-6,x+4,y+20,g(60),2)})
    person(d,330,930,1.35,u,dict(P_hold(u,r=(1.2,1.6)),mouth=.4),MAN,props={"r":lambda dd,x,y,a,s: dd.R(x-44,y-24,x+44,y+30,g(30),3)})
    clapper(d,430,830,1.0,open_=clamp(math.sin(u*2.4)))
    ptext(d,40,200,"1968",9,g(240)); ptext(d,40,300,"PITTSBURGH",5,g(240))
    return im
def sceneC(u):
    im=new(g(12),g(44)); d=D(im)
    o=person(d,270,1000,1.7,u,dict(al=(.95,1.85),ar=(.95,1.85),ll=(.05,.05),lr=(.05,.05),bob=math.sin(u*2),tilt=.05,look=(0,.8),mouth=.2,curlL=.9,curlR=.9,hands_front=True),MAN)
    cx=(o["hand_l"][0]+o["hand_r"][0])/2; cy=(o["hand_l"][1]+o["hand_r"][1])/2
    d.R(cx-70,cy-40,cx+70,cy+30,g(40),12); d.R(cx-66,cy-36,cx+66,cy-10,g(70),10)
    for k in range(3): d.E(cx-30+k*30,cy+90+(u*60+k*30)%80,14,6,g(230));
    ptext(d,40,235,"POCO DINERO",5.6,g(240))
    return im
def sceneD(u):
    im=new(g(10),g(40)); d=D(im)
    d.R(60,320,480,520,g(220),8); ptext(d,84,360,"OTRO TITULO",6,g(20))
    t=sm(u/1.6)
    d.L(60+420*t,330,60+420*t,510,(210,40,40),8) if False else None
    d.L(60,330,60+420*t,510,(210,40,40),8)
    d.R(60,560,480,760,g(240),8); ptext(d,84,600,"NUEVO TITULO",6,g(20))
    def marker(dd,x,y,a,s): dd.R(x-5,y-8,x+5,y+36,(210,40,40),3)
    person(d,380,1010,1.6,u,dict(al=(1.3,1.7),ar=(1.9,1.3+.5*math.sin(u*5)),ll=(.05,.05),lr=(.05,.05),bob=0,tilt=.05,look=(-.5,0),mouth=.2,curlR=1.0,hands_front=True),MAN,props={"r":marker})
    return im
def sceneE(u):
    im=new(g(10),g(44)); d=D(im)
    d.R(130,300,410,640,g(236),8)
    for k in range(7): d.R(160,330+k*40,380-((k*37)%80),340+k*40,g(120),2)
    r=sm((u-1.5)/1.0)
    copyright(d,270,700,48,g(30)); d.L(222,652,318,748,(210,40,40,int(255*r)),9); d.L(318,652,222,748,(210,40,40,int(255*r)),9)
    def paper(dd,x,y,a,s): pass
    person(d,100,1010,1.5,u,dict(al=(.7,1.9),ar=(1.1,1.6+.3*math.sin(u*4)),ll=(.05,.05),lr=(.05,.05),bob=math.sin(u*2),tilt=.05,look=(.7,.4),mouth=0,curlR=1.0,hands_front=True),WOMAN)
    person(d,450,1010,1.5,u,dict(al=(1.1,1.6),ar=(.7,1.9),ll=(.05,.05),lr=(.05,.05),bob=math.sin(u*2),tilt=-.05,look=(-.7,.4),mouth=0,curlL=1.0,hands_front=True),MAN)
    ptext(d,40,235,"SIN AVISO",6,g(240))
    return im
def sceneF(u):
    im=new(g(10),g(44)); d=D(im)
    for c in range(3): reel(d,100+c*170,390,.6,u+c*.3)
    d.R(40,500,500,740,g(60),10); d.R(70,525,470,715,g(8),6)
    for k,st in enumerate((MAN,WOMAN,DIR)):
        person(d,130+k*140,1000,1.35,u,dict(P_idle(u,k),al=(.1,.2),ar=(.1,.2),look=(0,-.4)),st)
    d.R(0,860,540,960,g(30),0)
    ptext(d,40,235,"PARA TODOS",6,g(240))
    return im
def sceneG(u):
    im=new(g(6),g(40)); d=D(im); sky(d,u); field(d,u); farm(d,u,140,620,.7)
    for k in range(6): person(d,((u*14+k*110)%640)-60,780+(k%3)*40,1.0+.15*(k%3),u,P_zombie(u,k*1.1),[ZB,ZW,ZC][k%3])
    film_strip(d,830,u,h=90)
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx in(0,7): return 1.0+.1*sm(p),270,520
    return 1.0+.1*sm(p),270+14*math.sin(u*.9),480
core.CAM=cam
if __name__=="__main__": core.main()
