import sys; sys.path.insert(0,"..")
from art import *
from common import zombie
def g(v): return (v,v,v)
def farm(d,u,x=270,y=560,sc=1.0,lit=True):
    d.R(x-130*sc,y-120*sc,x+130*sc,y,g(38),0); d.P([(x-150*sc,y-120*sc),(x,y-220*sc),(x+150*sc,y-120*sc)],g(24))
    d.R(x+70*sc,y-210*sc,x+96*sc,y-150*sc,g(30),0)
    for (dx,dy) in((-80,-90),(30,-90)): d.R(x+dx*sc,y+dy*sc,x+(dx+50)*sc,y+(dy+56)*sc,g(230) if lit and int(u*3+dx)%5 else g(12),2)
    d.R(x-20*sc,y-70*sc,x+20*sc,y,g(14),2)
def field(d,u,hz=560):
    d.R(0,hz,540,960,g(18),0)
    for k in range(40): x=rnd(k)*540; y=hz+10+rnd(k,1)*(960-hz); d.L(x,y,x+2,y-10,g(60),2)
def sky(d,u):
    gradient(d,0,560,g(6),g(46)); d.E(110,120,34,34,g(235)); d.E(110,120,70,70,g(235)+(30,))
    for k in range(30): d.E(rnd(k)*540,rnd(k,1)*300,1.5,1.5,g(220)+(170,))
def reel(d,x,y,sc,u):
    d.E(x,y,60*sc,60*sc,g(200)); d.E(x,y,52*sc,52*sc,g(40));
    for k in range(6): a=k*1.05+u*3; d.E(x+math.cos(a)*30*sc,y+math.sin(a)*30*sc,12*sc,12*sc,g(200))
    d.E(x,y,10*sc,10*sc,g(200))
def copyright(d,x,y,r,col=(255,255,255)):
    d.E(x,y,r,r,None,col,r*.12); ptext(d,x-r*.34,y-r*.5,"C",r*.2,col)
def sceneA(u,final=False):
    im=new(g(6),g(40)); d=D(im); sky(d,u); field(d,u); farm(d,u,150,600,.9)
    b=sm(u/1.0) if not final else 1.0
    zombie(d,380+math.sin(u)*10,780,2.0,u,col=g(4));
    for k in range(2): zombie(d,230+k*90,640,.9,u+k,col=g(8))
    return im
def sceneB(u):
    im=new(g(10),g(50)); d=D(im); d.R(0,700,540,960,g(14),0)
    clapper(d,270,420,2.0,open_=clamp(math.sin(u*2.2)))
    ptext(d,40,200,"1968",9,g(240)); ptext(d,40,820,"PITTSBURGH",5,g(240))
    return im
def sceneC(u):
    im=new(g(12),g(44)); d=D(im)
    # cartera vacia con pocas monedas
    d.R(80,360,460,640,g(190),24); d.R(80,360,460,420,g(150),24); d.R(380,470,470,530,g(120),12); d.E(420,500,8,8,g(220))
    for k in range(3): d.E(180+k*40,720+k*8,24,10,g(230)); d.E(180+k*40,716+k*8,24,10,g(190))
    ptext(d,40,200,"POCO DINERO",5.6,g(240))
    return im
def sceneD(u):
    im=new(g(10),g(40)); d=D(im)
    d.R(60,300,480,520,g(220),8); ptext(d,84,340,"OTRO TITULO",6,g(20)); d.L(60,310,480,510,(210,40,40),8)
    r=sm((u-1.2)/1.0); d.R(60,560,480,780,g(240),8); ptext(d,84,600,"NUEVO TITULO",6,g(20))
    copyright(d,420,740,34,g(20)); d.L(390,710,450,770,(210,40,40,int(255*r)),8); d.L(450,710,390,770,(210,40,40,int(255*r)),8)
    return im
def sceneE(u):
    im=new(g(10),g(44)); d=D(im)
    d.R(120,190,420,760,g(236),8);
    for k in range(10): d.R(150,230+k*44,390-((k*37)%80),240+k*44,g(120),2)
    r=sm((u-1.5)/1.0)
    copyright(d,270,860,56,g(240)); d.L(214,804,326,916,(210,40,40,int(255*r)),10); d.L(326,804,214,916,(210,40,40,int(255*r)),10)
    ptext(d,40,100,"SIN AVISO",6,g(240))
    return im
def sceneF(u):
    im=new(g(10),g(44)); d=D(im)
    for r in range(3):
        for c in range(3): reel(d,100+c*170,300+r*190,.8,u+c*.3+r)
    ptext(d,40,100,"PARA TODOS",6,g(240))
    d.R(40,820,500,900,g(0),6); ptext(d,60,844,"PUBLICO",5,g(240))
    return im
def sceneG(u):
    im=new(g(6),g(40)); d=D(im); sky(d,u); field(d,u)
    farm(d,u,140,620,.7)
    for k in range(5): zombie(d,230+k*60,700+(k%2)*40,1.2,u+k*.4,col=g(6))
    film_strip(d,820,u,h=90)
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx in(0,7,3,4): return 1.0,270,480
    return 1.0+.1*sm(p),270,480
core.CAM=cam
if __name__=="__main__": core.main()
