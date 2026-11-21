import sys; sys.path.insert(0,"..")
from art import *
from common import tv
CY=(80,230,255)
def isaac(d,x,y,sc,u,hp=1.0,flash=0.0):
    """protagonista de espaldas con traje espacial; barra de salud luminosa en la columna"""
    shadow(d,x,y+4,70*sc,8*sc,90)
    d.R(x-30*sc,y-90*sc,x-8*sc,y-6*sc,(70,76,84),8*sc); d.R(x+8*sc,y-90*sc,x+30*sc,y-6*sc,(70,76,84),8*sc)
    d.R(x-40*sc,y-210*sc,x+40*sc,y-86*sc,(92,98,108),16*sc); d.R(x-40*sc,y-210*sc,x+40*sc,y-200*sc,(255,255,255,40),16*sc)
    for sg in(-1,1): d.R(x+sg*52*sc-12*sc,y-206*sc,x+sg*52*sc+12*sc,y-120*sc,(78,84,94),8*sc); d.E(x+sg*50*sc,y-208*sc,22*sc,18*sc,(104,110,122))
    d.E(x,y-246*sc,28*sc,30*sc,(86,92,102)); d.E(x,y-246*sc,20*sc,22*sc,(30,34,40)); d.E(x-6*sc,y-252*sc,7*sc,5*sc,(255,255,255,70))
    d.R(x-10*sc,y-218*sc,x+10*sc,y-206*sc,(60,64,72),3*sc)
    # columna de luz = salud
    n=10
    for k in range(n):
        on=k<int(math.ceil(hp*n)); col=CY if hp>.35 else (240,70,50)
        yy=y-196*sc+k*10.4*sc
        d.R(x-6*sc,yy,x+6*sc,yy+8*sc,col+(255,) if on else (30,40,46,255),2*sc)
        if on: d.E(x,yy+4*sc,16*sc,10*sc,col+(40,))
    d.R(x-18*sc,y-110*sc,x+18*sc,y-92*sc,(50,54,62),4*sc); d.E(x,y-100*sc,5*sc,5*sc,CY if hp>.35 else (240,70,50))
def holo_panel(d,x,y,w,h,u,items=6):
    d.R(x,y,x+w,y+h,CY+(26,),10); d.R(x,y,x+w,y+h,None,10,CY+(190,),3)
    for r in range(3):
        for c in range(2):
            k=r*2+c
            if k<items and h>150:
                d.R(x+14+c*(w/2-8),y+54+r*(h-70)/3,x+w/2-8+c*(w/2-8),y+54+r*(h-70)/3+(h-80)/3,CY+(40,),6); d.R(x+14+c*(w/2-8),y+54+r*(h-70)/3,x+w/2-8+c*(w/2-8),y+54+r*(h-70)/3+(h-80)/3,None,6,CY+(150,),2)
                ptext(d,x+24+c*(w/2-8),y+62+r*(h-70)/3,["MED","AMMO","KEY","NODE","SUIT","GUN"][k],2.8,CY)
    for k in range(int(h/10)): d.R(x,y+k*10,x+w,y+k*10+1,CY+(18,),0)
def sceneA(u,final=False):
    im=new((8,10,16),(26,30,44)); d=D(im)
    corridor(d,u,speed=.1,wall=(54,60,70),floor=(30,32,36),ceil=(24,26,32),door=(70,76,86),light=(255,90,70),pulse=flicker(u,2,6),n=9,doors=True)
    isaac(d,270,HY+400,1.6,u,hp=.9)
    d.R(0,0,540,960,(255,40,30,int(10+10*math.sin(u*4))),0)
    return im
def sceneB(u):
    im=new((24,26,36),(52,56,70)); d=D(im)
    d.R(0,640,540,960,(36,38,48)); d.R(0,640,540,646,(255,255,255,24))
    # estudio: pizarra con boceto del traje y monitores
    d.R(30,90,300,420,(240,240,236),6)
    isaac(d,165,400,.8,u,hp=.8)
    d.R(330,90,510,260,(20,24,32),8); d.R(336,96,504,254,(60,70,90),4); corridor_mini(d,336,96,168,158)
    d.R(40,440,500,520,(70,74,86),6)
    for k,(x,w) in enumerate([(70,160),(300,160)]): d.R(x,540,x+w,690,(40,44,56),6); d.R(x+6,546,x+w-6,684,(10,14,20),4)
    ptext(d,40,730,"VISCERAL  2008",3.6,(255,255,255))
    return im
def corridor_mini(d,x,y,w,h):
    d.P([(x,y),(x+w,y),(x+w*.7,y+h*.4),(x+w*.3,y+h*.4)],(60,66,76)); d.P([(x,y+h),(x+w,y+h),(x+w*.7,y+h*.6),(x+w*.3,y+h*.6)],(30,32,38)); d.R(x+w*.3,y+h*.4,x+w*.7,y+h*.6,(6,6,10),0)
def sceneC(u):
    im=new((8,10,16),(26,30,44)); d=D(im)
    # misma escena a dos paneles: con HUD tradicional (tachado) y sin HUD
    for xo in (0,270):
        d.R(xo+6,60,xo+264,860,(16,20,28),8)
        d.P([(xo+30,160),(xo+240,160),(xo+180,420),(xo+90,420)],(40,46,56)); d.R(xo+90,420,xo+180,520,(10,10,14),0)
        isaac(d,xo+135,780,.9,u,hp=.9) if xo else isaac(d,xo+135,780,.9,u,hp=.9)
    # HUD clasico a la izquierda
    d.R(18,72,150,96,(60,200,90),3); d.R(18,72,100,96,(60,200,90),3); ptext(d,18,102,"HEALTH",2.6,(255,255,255)); ptext(d,170,760,"AMMO 30",3.0,(255,255,255)); d.R(180,80,254,150,(40,60,40),3)
    d.L(20,70,260,860,(230,60,60,230),10); d.L(260,70,20,860,(230,60,60,230),10)
    ptext(d,40,880,"CON MENUS",3.2,(255,255,255)); ptext(d,300,880,"SIN MENUS",3.2,CY)
    return im
def sceneD(u):
    im=new((6,8,14),(20,26,40)); d=D(im)
    hp=clamp(1.0-u/6.0*.8)
    isaac(d,270,900,2.6,u,hp=hp)
    d.E(270,420,160,260,CY+(10,)) if hp>.35 else d.E(270,420,160,260,(240,70,50,14))
    for k in range(18): a=k*.35+u*.5; d.E(270+math.cos(a)*230,430+math.sin(a)*300,2.5,2.5,CY+(120,))
    return im
def sceneE(u):
    im=new((6,10,18),(20,30,44)); d=D(im)
    isaac(d,150,900,1.8,u,hp=.9)
    # arma con holograma de municion y panel de inventario que se abre en el aire
    d.R(260,660,500,700,(80,88,98),8); d.R(280,700,330,780,(70,76,86),6); d.R(470,650,520,690,(60,66,76),4)
    ptext(d,300,580,"AMMO",3.4,CY); ptext(d,300,616,str(30-int(u*1.4)%30).zfill(2),6.0,CY)
    d.L(360,640,360,624,CY+(180,),3)
    p=sm((u-1.6)/.7); holo_panel(d,230,160,280,360*p+10,u) if p>.05 else None
    return im
def sceneF(u):
    im=new((8,6,10),(36,16,18)); d=D(im)
    corridor(d,u,speed=.05,wall=(60,52,56),floor=(28,24,26),ceil=(30,24,28),door=(70,60,64),light=(255,70,50),pulse=flicker(u,3,9),n=9,doors=True)
    isaac(d,200,HY+420,1.7,u,hp=.7)
    holo_panel(d,250,200,250,300,u)
    # amenaza que se acerca por detras (silueta)
    t=clamp(u/5.0); sx=lerp(440,330,t); sy=HY+120+t*40
    d.E(sx,sy-120*(.5+t),22*(.5+t),26*(.5+t),(4,4,6)); d.R(sx-30*(.5+t),sy-100*(.5+t),sx+30*(.5+t),sy,(4,4,6),10)
    for k in range(2): d.E(sx-8+k*16,sy-124*(.5+t),3,3,(255,60,50))
    ptext(d,40,880,"NO HAY PAUSA",4.0,(255,255,255))
    return im
def sceneG(u):
    im=new((2,4,8),(8,14,24)); d=D(im); stars(d,u,40,960)
    b=sm(u/.8)
    for k in range(10):
        yy=300+k*40; d.R(250,yy,290,yy+30,CY+(int(255*b),),6); d.E(270,yy+15,60*b,24*b,CY+(30,))
    ptext(d,120,200,"SIN HUD",9.0,CY,int(255*b))
    for k in range(26): a=k*.24+u*.3; d.E(270+math.cos(a)*250,520+math.sin(a)*330,3,3,CY+(150,))
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx in(2,): return 1.0,270,480
    return 1.0+.25*sm(p),270,520
core.CAM=cam
if __name__=="__main__": core.main()
