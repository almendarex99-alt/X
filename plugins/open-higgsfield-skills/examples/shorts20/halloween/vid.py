import sys; sys.path.insert(0,"..")
from art import *
ORG=(255,140,30)
def mask(d,x,y,sc,paint=1.0,eyes=1.0,hair=1.0,glow=0.0):
    """mascara de cara inexpresiva: de tono carne (paint=0) a blanco (paint=1)"""
    skin=mixc((222,176,140),(236,236,232),paint)
    # pelo detras
    if hair>0:
        d.E(x,y-10*sc,88*sc*hair,112*sc*hair,(34,22,14,255))
        for k in range(14):
            a=math.pi*1.05+k/13*math.pi*.9; d.E(x+math.cos(a)*84*sc*hair,y-20*sc+math.sin(a)*100*sc*hair,14*sc,16*sc,(34,22,14,255))
        d.E(x,y-70*sc,70*sc,40*sc*hair,(42,28,18))
    d.E(x,y,70*sc,92*sc,skin+(255,)); d.E(x-24*sc,y-30*sc,30*sc,50*sc,(255,255,255,26))
    d.R(x-12*sc,y+40*sc,x+12*sc,y+78*sc,skin+(255,),6*sc)  # barbilla
    # nariz
    d.P([(x-3*sc,y-6*sc),(x+3*sc,y-6*sc),(x+10*sc,y+24*sc),(x-10*sc,y+24*sc)],mixc(skin,(120,100,90),.25)+(255,))
    # ojos
    ew=(11+9*eyes)*sc; eh=(8+10*eyes)*sc
    for sg in(-1,1):
        d.E(x+sg*30*sc,y-20*sc,ew,eh,(6,6,8)); 
        if glow>0: d.E(x+sg*30*sc,y-20*sc,ew*1.6,eh*1.6,(255,255,255,int(40*glow)))
    # cejas arqueadas solo en la mascara original (paint bajo)
    if paint<.6:
        for sg in(-1,1): d.L(x+sg*14*sc,y-44*sc,x+sg*48*sc,y-58*sc,(40,28,22,int(255*(1-paint))),4*sc)
        d.A(x,y+40*sc,22*sc,8*sc,10,170,(110,60,50,int(255*(1-paint))),3*sc)
    else: d.R(x-16*sc,y+46*sc,x+16*sc,y+49*sc,(60,60,60,160),1)
def pumpkin(d,x,y,sc,u):
    d.E(x,y,40*sc,32*sc,ORG+(255,)); d.E(x-18*sc,y,22*sc,30*sc,(230,110,20)); d.E(x+18*sc,y,22*sc,30*sc,(230,110,20)); d.R(x-5*sc,y-40*sc,x+5*sc,y-30*sc,(60,90,30),2*sc)
    g=int(255*(.6+.4*math.sin(u*9+x)))
    for sg in(-1,1): d.P([(x+sg*20*sc,y-6*sc),(x+sg*8*sc,y-6*sc),(x+sg*14*sc,y-18*sc)],(255,220,80,g))
    d.A(x,y+8*sc,18*sc,10*sc,10,170,(255,220,80,g),4*sc)
def street(d,u):
    gradient(d,0,520,(10,8,24),(40,24,50)); d.E(400,150,40,40,(255,240,200,220)); d.E(400,150,80,80,(255,240,200,40))
    for k in range(3):
        x=60+k*170; h=220+k*30; d.R(x,520-h,x+130,520,(20,16,28),0)
        for r in range(4):
            for c in range(3): d.R(x+14+c*38,520-h+20+r*46,x+40+c*38,520-h+50+r*46,(255,200,100,int(180*flicker(u,k+r+c,3))) if (r+c+k)%2 else (30,26,40),2)
    d.R(0,520,540,960,(18,14,22),0)
    for k in range(6): d.R(0,520+k*60,540,522+k*60,(255,255,255,10),0)
    for k in range(3): pumpkin(d,90+k*180,640+k*30,1.0+.1*k,u)
def sceneA(u,final=False):
    im=new((6,6,10),(20,14,26)); d=D(im)
    for k in range(12): a=k*.52+u*.2; d.E(270+math.cos(a)*220,330+math.sin(a)*260,3,3,(255,255,255,50))
    d.E(270,420,240,300,(255,255,255,14))
    b=sm(u/1.0) if not final else 1.0
    mask(d,270,420,2.3*(.8+.2*b),paint=1.0,eyes=1.0,hair=1.0,glow=1)
    if u>1.0:
        # sombra de pregunta: aparecen interrogantes que flotan
        for k in range(4): t=(u*.35+k*.25)%1; ptext(d,70+k*110,760-t*160,"?",6,(255,255,255),int(200*(1-t)))
    return im
def sceneB(u):
    im=new((8,6,16),(20,14,30)); d=D(im); street(d,u)
    clapper(d,150,380,1.5,open_=clamp(math.sin(u*2.5)))
    film_camera(d,380,820,1.0,u)
    ptext(d,40,200,"1978",8,(255,255,255)); ptext(d,40,265,"CARPENTER",3.6,ORG)
    return im
def sceneC(u):
    im=new((14,12,22),(30,26,44)); d=D(im)
    # estanteria de tienda de disfraces con mascaras alineadas
    d.R(0,640,540,960,(36,28,36),0)
    for r,y in enumerate((260,520,780)):
        d.R(0,y,540,y+16,(70,52,40),0); d.R(0,y+16,540,y+22,(0,0,0,70),0)
        for c in range(4):
            x=70+c*135; col=[(70,110,70),(120,60,60),(60,70,120),(230,196,60)][(r+c)%4]
            d.E(x,y-60,34,46,col+(255,)); d.E(x-12,y-72,6,6,(10,10,12)); d.E(x+12,y-72,6,6,(10,10,12))
    # la mascara protagonista: tono carne con cejas arqueadas, destacada con foco
    d.P([(270-80,0),(270+80,0),(270+260,520),(270-260,520)],(255,240,200,30))
    mask(d,270,420,1.45,paint=0.0,eyes=0.0,hair=0.0)
    d.R(210,620,330,660,(250,240,210),4); ptext(d,224,630,"CAPITAN",3,(30,30,30))
    d.R(330,330,400,370,(255,255,255),3); ptext(d,338,340,"$",5,(30,30,30))
    return im
def sceneD(u):
    im=new((10,8,18),(26,20,38)); d=D(im)
    p=sm((u-.6)/1.8); e=sm((u-2.4)/1.6); h=sm((u-4.4)/1.6)
    mask(d,270,360,1.2,paint=p,eyes=e,hair=h)
    steps=["PINTAR","OJOS","PELO"]; 
    for i,s in enumerate(steps):
        on=[p,e,h][i]; x=40+i*160
        d.R(x,700,x+140,760,ORG+(int(60+195*on),),8); ptext(d,x+12,718,s,5,(255,255,255) if on>.5 else (200,200,210))
        d.R(x,780,x+140,792,(255,255,255,40),4); d.R(x,780,x+140*on,792,ORG+(255,),4)
    return im
def sceneE(u):
    im=new((2,2,4),(12,10,18)); d=D(im)
    b=sm(u/1.2); z=lerp(1.4,2.5,sm(u/6.0))
    d.E(270,480,260*b,330*b,(255,255,255,18))
    mask(d,270,480,z,paint=1.0,eyes=1.0,hair=1.0,glow=b)
    # luz que recorre el rostro
    sx=lerp(120,420,(u*.3)%1); d.E(sx,480,50,300,(255,255,255,18))
    ptext(d,60,860,"NO MUESTRA NADA",4,(255,255,255))
    return im
def sceneF(u):
    im=new((8,6,14),(20,14,30)); d=D(im)
    # una moneda/etiqueta de precio pequena vs. cartel de pelicula
    t=sm(u/1.5)
    d.R(70,200,470,400,(255,255,255,20),10); d.R(70,200,470,400,None,10,(255,255,255,120),3)
    d.E(130,300,30,30,(236,196,70)); ptext(d,122,282,"$",7,(120,80,10))
    ptext(d,190,260,"BARATA",6,(255,255,255)); ptext(d,190,320,"POCOS $",6,(255,255,255))
    mask(d,270,640,1.1*t,paint=1.0,eyes=1.0,hair=1.0)
    film_strip(d,820,u,h=90)
    return im
def sceneG(u):
    im=new((8,6,16),(24,18,34)); d=D(im)
    ptext(d,40,90,"COSTE  VS  RECAUDACION",3.2,(255,255,255))
    base=800; 
    b=sm(u/2.0); b2=sm((u-2.0)/2.5)
    d.R(100,base-34*b,240,base,(120,200,140),6)   # coste, muy bajo
    d.R(300,base-560*b2,440,base,ORG+(255,),6)    # recaudacion, muy alta
    ptext(d,106,base+20,"COSTE",3.4,(255,255,255)); ptext(d,306,base+20,"TAQUILLA",3.4,(255,255,255))
    d.L(60,base,480,base,(255,255,255,120),3)
    for k in range(10):
        if b2>.5: d.E(370+math.sin(k+u*3)*60,base-560*b2-20-((u*80+k*40)%120),4,4,(255,230,120,200))
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx in(1,3,5,6): return 1.0,270,480
    return 1.0+.18*sm(p),270,480
core.CAM=cam
if __name__=="__main__": core.main()
