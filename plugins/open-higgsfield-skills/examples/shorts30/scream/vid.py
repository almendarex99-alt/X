import sys; sys.path.insert(0,"..")
from art import *
PALE=(232,230,222)
def gmask(d,x,y,sc,u=0.0,hood=True,glow=0.0):
    """mascara original de cara alargada y ojos y boca caidos, con capucha negra"""
    if hood:
        d.P([(x-90*sc,y+250*sc),(x-96*sc,y-60*sc),(x-60*sc,y-150*sc),(x,y-176*sc),(x+60*sc,y-150*sc),(x+96*sc,y-60*sc),(x+90*sc,y+250*sc)],(8,8,10))
    d.E(x,y,58*sc,126*sc,PALE+(255,)); d.E(x-18*sc,y-40*sc,20*sc,70*sc,(255,255,255,40))
    d.P([(x-30*sc,y+100*sc),(x+30*sc,y+100*sc),(x,y+150*sc)],PALE)
    for sg in(-1,1):
        d.P([(x+sg*14*sc,y-60*sc),(x+sg*44*sc,y-52*sc),(x+sg*38*sc,y-6*sc),(x+sg*28*sc,y+30*sc),(x+sg*22*sc,y-6*sc)],(8,8,10))
        if glow: d.E(x+sg*30*sc,y-34*sc,40*sc,56*sc,(255,255,255,int(26*glow)))
    d.P([(x-22*sc,y+50*sc),(x+22*sc,y+50*sc),(x+26*sc,y+86*sc),(x,y+128*sc),(x-26*sc,y+86*sc)],(8,8,10))
def house_out(d,u):
    gradient(d,0,520,(40,30,60),(220,140,110)); d.E(400,200,60,60,(255,210,150,200))
    d.R(0,520,540,960,(24,22,26),0)
    d.R(100,300,440,540,(70,56,60),0); d.P([(80,300),(270,190),(460,300)],(50,38,44));
    for (x,y) in((130,360),(330,360),(130,460),(330,460)): d.R(x,y,x+80,y+70,(255,200,120,int(200*flicker(u,x,4))) if (x+y)%3 else (30,24,30),2)
    d.R(230,440,310,540,(40,28,28),2)
def clipboard(d,x,y,sc):
    d.R(x,y,x+90*sc,y+120*sc,(120,86,56),6*sc); d.R(x+8*sc,y+16*sc,x+82*sc,y+112*sc,(240,236,222),2*sc); d.R(x+28*sc,y+4*sc,x+62*sc,y+20*sc,(160,160,170),3*sc)
    for k in range(5): d.R(x+14*sc,y+30*sc+k*16*sc,x+70*sc,y+34*sc+k*16*sc,(110,106,98),1)
def sceneA(u,final=False):
    im=new((6,6,10),(20,16,24)); d=D(im); b=sm(u/1.0) if not final else 1.0
    d.E(270,420,240,330,(255,255,255,14)); gmask(d,270,420,2.0*(.85+.15*b),u,glow=1)
    for k in range(10): a=k*.62+u*.2; d.E(270+math.cos(a)*230,420+math.sin(a)*300,2.5,2.5,(255,255,255,50))
    return im
def sceneB(u):
    im=new((8,8,14),(24,22,32)); d=D(im); d.R(0,700,540,960,(14,12,18),0)
    clapper(d,270,420,2.0,open_=clamp(math.sin(u*2.2)))
    ptext(d,40,200,"1996",9,(255,255,255)); ptext(d,40,690,"WES CRAVEN",4.6,(255,214,120))
    return im
def sceneC(u):
    im=new((40,30,60),(220,140,110)); d=D(im); house_out(d,u)
    # ventana con la mascara colgada
    d.R(330,360,410,430,(30,24,30),2); gmask(d,370,392,.3,hood=False)
    flashlight(d,120,820,350,400,spread=.18,L=560,a=60)
    silhouette(d,120,880,1.6,(10,8,12)); clipboard(d,160,760,.9)
    ptext(d,40,235,"LOCALIZACIONES",4,(255,255,255))
    return im
def sceneD(u):
    im=new((24,20,30),(52,44,60)); d=D(im); d.R(0,640,540,960,(70,52,40),0)
    for r,y in enumerate((280,520)):
        d.R(0,y,540,y+14,(110,80,56),0)
        for c in range(4):
            x=70+c*135; col=[(70,110,70),(120,60,60),(60,70,120),(230,196,60)][(r+c)%4]
            if (r,c)==(1,2): gmask(d,x,y-92,.42,hood=False)
            else: d.E(x,y-60,34,46,col+(255,)); d.E(x-12,y-72,6,6,(10,10,12)); d.E(x+12,y-72,6,6,(10,10,12))
    ptext(d,40,650,"DE TIENDA",7,(255,255,255))
    return im
def sceneE(u):
    im=new((8,8,12),(22,20,28)); d=D(im); b=sm(u/1.0)
    gmask(d,270,470,2.3,u,glow=b)
    d.L(60,300,200,380,(255,255,255,0),1)
    ptext(d,40,235,"CARA ALARGADA",4.4,(255,214,120))
    return im
def sceneF(u):
    im=new((24,20,30),(52,44,60)); d=D(im); d.R(0,700,540,960,(60,48,40),0)
    d.R(90,200,450,640,(240,236,222),6)
    for k in range(10): d.R(120,240+k*28,420-((k*37)%100),248+k*28,(110,106,98),2)
    d.R(90,200,450,240,(210,60,60),6); ptext(d,110,208,"ACUERDO",4.4,(255,255,255))
    t=sm((u-1.5)/1.0); d.L(130,590,300,590,(30,40,120,int(255*t)),5)
    # manos que se estrechan
    d.R(60,720,260,780,SK,18); d.R(280,720,480,780,SK2,18); d.E(270,750,34,28,SK)
    return im
def sceneG(u):
    im=new((6,6,10),(20,16,24)); d=D(im)
    for k in range(3):
        x=90+k*180; gmask(d,x,430,.7,hood=True)
    ptext(d,40,235,"ICONO",8,(255,255,255))
    film_strip(d,780,u,h=100)
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx in(0,7,5): return 1.0,270,480
    return 1.0+.1*sm(p),270,480
core.CAM=cam
if __name__=="__main__": core.main()
