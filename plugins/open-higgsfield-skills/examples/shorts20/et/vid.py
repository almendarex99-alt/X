import sys; sys.path.insert(0,"..")
from art import *
from common import tv
SAND=(210,170,110); DUSK=(244,150,80)
def desert(d,u,t=0.0,night=False):
    if night: gradient(d,0,520,(10,12,30),(60,40,70)); stars(d,u,40,400); d.E(420,140,34,34,(240,240,250,230))
    else: gradient(d,0,520,(250,170,90),(255,226,170)) if t<.5 else gradient(d,0,520,(130,190,240),(220,236,248))
    if not night: d.E(110,420,50,50,(255,240,190,230))
    d.P([(0,520),(90,420),(200,500),(300,400),(420,490),(540,430),(540,540),(0,540)],(150,110,90) if not night else (30,24,40))
    d.R(0,520,540,960,(SAND if not night else (70,56,50)),0)
    for k in range(40): d.E(rnd(k)*540,540+rnd(k,1)*420,3+rnd(k,2)*7,1.5+rnd(k,3)*3,(190,150,100,150) if not night else (50,40,36,150))
def cartridge(d,x,y,sc,col=(70,70,74),lab=(230,200,90)):
    d.R(x,y,x+44*sc,y+54*sc,col,4*sc); d.R(x+6*sc,y+6*sc,x+38*sc,y+34*sc,lab,2*sc); d.R(x+8*sc,y+44*sc,x+36*sc,y+52*sc,(30,30,34),1)
def box(d,x,y,w,h,col=(168,130,80)):
    d.R(x,y,x+w,y+h,col,3); d.R(x,y+h*.38,x+w,y+h*.46,(120,90,50),0); d.R(x+w*.4,y,x+w*.6,y+h*.18,(236,226,200),1)
def bulldozer(d,x,y,sc,u):
    shadow(d,x,y+4,100*sc,8*sc,80)
    d.R(x-70*sc,y-60*sc,x+54*sc,y-16*sc,(240,190,40),6*sc); d.R(x-20*sc,y-110*sc,x+40*sc,y-60*sc,(240,190,40),6*sc); d.R(x-10*sc,y-102*sc,x+32*sc,y-66*sc,(120,170,200),3*sc)
    d.R(x-82*sc,y-16*sc,x+66*sc,y+4*sc,(40,40,44),8*sc)
    for k in range(6): d.E(x-70*sc+k*26*sc,y-6*sc,9*sc,9*sc,(90,90,96))
    d.R(x+60*sc,y-70*sc,x+74*sc,y-20*sc,(180,180,190),2*sc); d.R(x+68*sc,y-76*sc,x+88*sc,y,(240,190,40),3*sc)
    d.R(x-52*sc,y-130*sc,x-42*sc,y-100*sc,(50,50,56),1)
    for k in range(4): a=((u*.8+k*.25)%1); d.E(x-47*sc,y-134*sc-a*46*sc,(6+a*12)*sc,(5+a*8)*sc,(90,90,96,int(170*(1-a))))
def sceneA(u,final=False):
    im=new((244,150,80),(255,214,150)); d=D(im); desert(d,u,t=0.0)
    d.P([(60,700),(480,700),(430,850),(110,850)],(80,60,44))
    for r in range(4):
        for c in range(9): cartridge(d,110+c*34+(r%2)*14,720+r*30,.62,(60+r*8,60+r*8,66+r*8))
    bulldozer(d,170+((u*18)%60),680,1.0,u)
    return im
def sceneB(u):
    im=new((26,20,16),(64,48,38)); d=D(im)
    d.R(0,640,540,960,(60,44,34)); d.R(0,640,540,646,(255,255,255,24))
    def inner(d_,x,y,w,h):
        d_.R(x,y,x+w,y+h,(30,90,60)); d_.R(x,y+h*.6,x+w,y+h,(120,90,60))
        for k in range(3): d_.R(x+30+k*90,y+h*.7,x+80+k*90,y+h*.78,(10,10,10),2)
        pix(d_,x+w*.5-12,y+h*.34,6,["..##..",".####.","######","######",".#..#."],{"#":(90,60,40)})
    tv(d,70,180,400,330,inner,u)
    # Atari 2600: caja negra con panel de madera y palancas
    shadow(d,270,780,170,12,80); bevel(d,80,700,460,800,(34,30,28),8); d.R(80,700,460,730,(140,90,50),4)
    for k in range(6): d.R(120+k*50,744,142+k*50,770,(70,70,76),3); d.R(126+k*50,748,136+k*50,762,(210,210,216),2)
    # palanca con boton rojo
    d.E(380,880,34,16,(30,30,34)); d.R(372,830,388,880,(40,40,44),4); d.E(380,826,12,12,(220,40,40))
    ptext(d,40,90,"1982",6.0,(255,255,255))
    return im
def sceneC(u):
    im=new((40,30,60),(70,50,90)); d=D(im)
    # calendario de cinco semanas que se tacha
    d.R(40,120,500,520,(244,240,230),10); d.R(40,120,500,176,(200,50,60),10)
    n=int(clamp(u/5.0)*5)
    for r in range(5):
        for c in range(7):
            d.R(56+c*62,196+r*62,108+c*62,246+r*62,(220,220,228),3)
            if r<n or (r==n and c<int((u/5.0*5-n)*7)): d.L(60+c*62,200+r*62,104+c*62,242+r*62,(220,60,60),4); d.L(104+c*62,200+r*62,60+c*62,242+r*62,(220,60,60),4)
    ptext(d,60,560,"5 SEMANAS",6.0,(255,255,255))
    # arbol de Navidad al final
    d.P([(270,640),(180,780),(360,780)],(40,140,70)); d.P([(270,700),(160,850),(380,850)],(30,120,60)); d.R(256,850,284,880,(110,70,40),2); d.E(270,632,10,10,(255,220,80))
    for k in range(8): d.E(220+(k*37)%100,730+(k*23)%110,4,4,[(240,70,70),(255,220,80),(90,160,250)][k%3]+(255,))
    return im
def sceneD(u):
    im=new((24,26,34),(52,56,68)); d=D(im)
    # almacen con cajas apiladas y una grafica que cae
    for r in range(3): d.R(20,160+r*100,520,172+r*100,(120,120,130),0)
    for r in range(3):
        for c in range(7): box(d,28+c*70,60+r*100,62,58)
    for k in range(30):
        x=(rnd(k)*500+10); y=730+rnd(k,1)*140; box(d,x,y,60,50)
    d.R(40,430,500,640,(20,24,36),8)
    pts=[(60,470),(150,500),(220,520),(300,560),(380,590),(470,610)]
    for i in range(len(pts)-1):
        t=clamp(u/4.0*5-i)
        if t>0: d.L(pts[i][0],pts[i][1],pts[i][0]+(pts[i+1][0]-pts[i][0])*t,pts[i][1]+(pts[i+1][1]-pts[i][1])*t,(240,70,70),6)
    d.P([(450,590),(480,610),(440,620)],(240,70,70))
    return im
def sceneE(u):
    im=new((10,12,30),(60,40,70)); d=D(im); desert(d,u,night=True)
    d.P([(60,700),(480,700),(430,860),(110,860)],(30,24,26))
    for k in range(int(clamp(u/5.0)*28)): cartridge(d,120+(k%10)*34,712+(k//10)*34,.6,(60,60,66))
    # camion volcando y excavadora tapando con tierra
    d.R(300,520,470,590,(200,70,50),6); d.R(300,590,470,610,(40,40,44),3); d.R(440,540,500,590,(160,50,40),4); d.E(340,616,16,16,(20,20,24)); d.E(440,616,16,16,(20,20,24))
    bulldozer(d,150,640,.9,u)
    d.E(270,640,260,60,(255,240,190,24)); d.P([(120,640),(180,640),(400,760),(100,760)],(255,240,190,20))
    ptext(d,60,60,"1983",6.0,(255,255,255))
    return im
def sceneF(u):
    im=new((130,190,240),(220,236,248)); d=D(im); desert(d,u,t=1.0)
    d.P([(60,700),(480,700),(430,860),(110,860)],(120,90,60)); 
    # excavadora con brazo y trabajadores con casco
    d.R(260,560,430,620,(240,190,40),6); d.R(290,500,360,560,(240,190,40),6); d.L(400,570,470,640,(80,80,90),10); d.L(470,640,440,700,(80,80,90),10); d.R(410,690,480,716,(80,80,90),4)
    for k,x in enumerate([120,180]):
        silhouette(d,x,780,.9,(40,50,80)); d.E(x,780-148*.9,16*.9,10*.9,(240,200,40))
    # un cartucho polvoriento en la mano
    cartridge(d,226,760,1.5,(70,70,74),(230,200,90)); d.R(0,0,540,960,(255,255,255,0),0)
    ptext(d,60,60,"2014",6.0,(30,30,40))
    # equipo de grabacion
    film_camera(d,60,900,.5,u)
    return im
def sceneG(u):
    im=new((250,170,90),(255,226,170)); d=D(im)
    for k in range(18):
        a=k*math.pi/9+u*.2; d.P([(270,560),(270+math.cos(a-.07)*900,560+math.sin(a-.07)*900),(270+math.cos(a+.07)*900,560+math.sin(a+.07)*900)],(255,240,190,22))
    d.R(0,640,540,960,SAND+(255,),0); d.E(270,660,200,40,(190,150,100,160))
    b=sm(u/.8); cartridge(d,194,560-20*b,2.2,(70,70,74),(230,200,90))
    for k in range(20): a=k*.31+u*.4; d.E(270+math.cos(a)*230,560+math.sin(a)*170,3,3,(255,240,190,200))
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur)); return 1.0+.25*sm(p),270,560
core.CAM=cam
if __name__=="__main__": core.main()
