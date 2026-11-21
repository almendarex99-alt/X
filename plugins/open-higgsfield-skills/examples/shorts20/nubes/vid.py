import sys; sys.path.insert(0,"..")
from art import *
SKY=(92,148,252); BR=(200,76,12); BR2=(252,152,56); GR=(0,168,0); GR2=(0,88,0); WH=(252,252,252); CY=(60,188,252)
SH=["....##....##....","...####..####...","..############..",".##############.","################","################","################",".##############."]
def shape(d,x,y,cell,fill,outline,scale=1.0,shade=None):
    for ox,oy in((-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1),(-1,1),(1,-1)):
        pix(d,x+ox*cell*.5,y+oy*cell*.5,cell,SH,{"#":outline})
    pix(d,x,y,cell,SH,{"#":fill})
    if shade:
        for c in (3,4,5,7,8,9,10,11,12): d.R(x+c*cell,y+6*cell,x+(c+1)*cell,y+7*cell,shade+(255,),0)
def hill(d,x,y,w,h):
    d.P([(x,y),(x+w*.22,y-h*.7),(x+w*.38,y-h),(x+w*.62,y-h),(x+w*.78,y-h*.7),(x+w,y)],GR+(255,))
    d.P([(x+w*.08,y),(x+w*.26,y-h*.62),(x+w*.38,y-h*.85),(x+w*.3,y)],GR2+(255,)); 
    d.R(x+w*.40,y-h*.72,x+w*.44,y-h*.58,(0,0,0),0); d.R(x+w*.56,y-h*.72,x+w*.60,y-h*.58,(0,0,0),0)
def ground(d,y,off=0):
    d.R(0,y,540,960,BR+(255,),0)
    for r in range(int((960-y)/36)+1):
        for c in range(-1,16):
            x=c*36+((r%2)*18)-off%36; yy=y+r*36
            d.R(x,yy,x+36,yy+36,BR+(255,),0); d.R(x,yy,x+36,yy+3,BR2+(255,),0); d.R(x,yy,x+3,yy+36,BR2+(255,),0); d.R(x+33,yy,x+36,yy+36,(100,30,0),0); d.R(x,yy+33,x+36,yy+36,(100,30,0),0)
def qblock(d,x,y,u):
    d.R(x,y,x+54,y+54,(252,168,56),2); d.R(x+3,y+3,x+51,y+51,(200,120,20),2)
    ptext(d,x+14,y+10,"?",6.0,(252,252,252))
def hud(d,u):
    ptext(d,16,16,"SCORE",3.0,WH); ptext(d,16,36,"000000",3.0,WH); ptext(d,190,36,"X00",3.0,WH); ptext(d,260,16,"WORLD",3.0,WH); ptext(d,270,36,"1-1",3.0,WH); ptext(d,420,16,"TIME",3.0,WH); ptext(d,430,36,str(400-int(u*2)).zfill(3),3.0,WH)
def level(d,u,off=0.0,hl=0.0):
    d.R(0,0,540,960,SKY+(255,),0)
    for k,(x,y) in enumerate([(60,160),(300,110),(520,200),(780,140)]):
        xx=(x-off*.3)%900-120; shape(d,xx,y,9,WH,CY,shade=(200,220,252))
    gy=700
    for k,(x,w,h) in enumerate([(-40,220,130),(430,160,90),(700,220,130)]):
        xx=(x-off)%900-120; hill(d,xx,gy,w*1.4,h*1.5)
    for k,x in enumerate([200,560,860]):
        xx=(x-off)%900-120; shape(d,xx,gy-62,9,GR,GR2,shade=(0,120,0))
    qblock(d,(330-off)%900-100,500,u)
    ground(d,gy,off)
    if hl>0:
        for k,(x,y) in enumerate([(60,160),(300,110),(520,200),(780,140)]): xx=(x-off*.3)%900-120; d.R(xx-8,y-8,xx+152,y+80,None,6,(255,230,90,int(200*hl)),3)
        for k,x in enumerate([200,560,860]): xx=(x-off)%900-120; d.R(xx-8,gy-70,xx+152,gy+10,None,6,(255,230,90,int(200*hl)),3)
    hud(d,u)
def sceneA(u,final=False):
    im=new(SKY,SKY); d=D(im); level(d,u,off=u*60)
    return im
def sceneB(u):
    im=new((24,20,40),(60,50,70)); d=D(im)
    d.R(0,660,540,960,(44,38,50)); d.R(0,660,540,666,(255,255,255,24))
    def inner(d_,x,y,w,h): 
        d_.R(x,y,x+w,y+h,SKY); d_.R(x,y+h*.78,x+w,y+h,BR); shape(d_,x+30,y+30,3,WH,CY); shape(d_,x+w*.5,y+h*.78-24,3,GR,GR2)
    from common import tv
    tv(d,80,200,380,330,inner,u)
    # NES: caja gris con franja negra y ranura del cartucho
    shadow(d,270,780,150,12,80); bevel(d,130,700,410,780,(176,176,172),6); d.R(130,722,410,744,(40,40,44),0); d.R(240,704,300,714,(20,20,22),2); d.E(380,760,6,6,(220,40,40))
    # cartucho
    d.R(180,820,360,900,(130,130,136),6); d.R(196,830,344,880,(214,70,50),4); d.R(206,840,334,872,(252,252,252),2); ptext(d,216,846,"1985",5.0,(40,40,44))
    d.R(60,100,200,200,(244,240,230),6); d.R(60,100,200,128,(200,50,60),6)
    return im
def sceneC(u):
    im=new((12,16,30),(26,30,56)); d=D(im)
    # chip de memoria + cuadricula de gráficos que se llena
    d.R(150,90,390,250,(24,24,30),8)
    for k in range(10): d.R(138,104+k*14,150,112+k*14,(190,190,200),1); d.R(390,104+k*14,402,112+k*14,(190,190,200),1)
    ptext(d,176,120,"40 KB",6.0,(255,255,255)); d.R(166,200,374,212,(60,60,70),3)
    fill=clamp(u/5.0); d.R(166,200,166+208*fill,212,mixc((80,200,120),(230,60,50),fill),3)
    for r in range(14):
        for c in range(14):
            k=r*14+c; on=k<int(fill*196)
            d.R(60+c*28,320+r*28,60+c*28+26,320+r*28+26,(120,200,255) if on else (28,34,60),2)
    ptext(d,60,730,"CADA GRAFICO CUESTA",3.4,(255,255,255))
    return im
def sceneD(u):
    im=new((24,20,40),(60,50,70)); d=D(im)
    # una sola forma en tonos de gris, y los cuatro colores posibles de la paleta
    shape(d,120,260,18,(200,200,206),(80,80,90),shade=(150,150,160))
    ptext(d,150,170,"UN SOLO DIBUJO",3.6,(255,255,255))
    for k,c in enumerate([WH,CY,GR,GR2]):
        d.E(110+k*100,620,36,36,c+(255,)); d.E(110+k*100,620,36,36,None,(255,255,255,200),4)
    pk=int(u*.8)%4; d.R(70+pk*100,570,150+pk*100,670,None,10,(255,230,90),4)
    return im
def sceneE(u):
    im=new(SKY,SKY); d=D(im)
    d.R(0,0,540,960,SKY+(255,),0); ground(d,700)
    ph=(u%4.8)/4.8
    to_cloud=ph<.5; q=sm((ph%.5)/.5*1.4)
    # la forma se mueve del centro al cielo (blanco) o al suelo (verde) segun el color
    x=180; 
    cx=lerp(180,200,q); 
    if to_cloud:
        y=lerp(420,170,q); fill=mixc((200,200,206),WH,q); out=mixc((80,80,90),CY,q)
    else:
        y=lerp(420,636,q); fill=mixc((200,200,206),GR,q); out=mixc((80,80,90),GR2,q)
    shape(d,cx,y,13,fill,out)
    # bote de pintura
    bx=420; by=300+math.sin(u*3)*4; col=WH if to_cloud else GR
    d.R(bx,by,bx+70,by+60,(120,120,130),6); d.R(bx+4,by-6,bx+66,by+4,col,3)
    for k in range(8): t=(u*1.5+k*.13)%1; d.E(bx-20-t*140,by+20+t*90,5,7,col+(int(230*(1-t)),))
    ptext(d,40,40,"BLANCO" if to_cloud else "VERDE",5.0,(255,255,255))
    return im
def sceneF(u):
    im=new(SKY,SKY); d=D(im); level(d,u,off=u*30,hl=.6+.4*math.sin(u*5))
    d.A(270,430,200,120,200,340,(255,230,90,230),6)
    ptext(d,150,160,"2 EN 1",8.0,(255,255,255))
    return im
def sceneG(u):
    im=new((24,20,60),(70,40,110)); d=D(im); stars(d,u,60,960)
    for k in range(16):
        a=k*math.pi/8+u*.4; d.P([(270,430),(270+math.cos(a-.07)*800,430+math.sin(a-.07)*800),(270+math.cos(a+.07)*800,430+math.sin(a+.07)*800)],(255,240,160,16))
    b=sm(u/.8)
    shape(d,200-60*b+60,300,16*b+1,WH,CY,shade=(200,220,252)); shape(d,200-60*b+60,560,16*b+1,GR,GR2,shade=(0,120,0))
    d.L(270,420,270,540,(255,255,255,200),5)
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx in (0,5,7): return 1.0,270,480
    return (1.0+.18*sm(p),270,480) if idx!=6 else (1.3-.3*sm(p),270,480)
core.CAM=cam
if __name__=="__main__": core.main()
