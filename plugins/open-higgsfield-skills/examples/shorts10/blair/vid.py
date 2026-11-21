import sys; sys.path.insert(0,"..")
from art import *
from PIL import Image, ImageOps
import numpy as np
FOR=dict(sky=(18,28,44),sky2=(70,90,118),ground=(14,20,16),fog=(150,170,186))

def bw16(im,u):
    """pelicula de 16 mm en blanco y negro: grano, arañazos verticales y parpadeo"""
    g=np.array(ImageOps.grayscale(im)).astype(np.float32); rng=np.random.default_rng(int(u*24))
    g=g*(0.94+0.1*rng.random())+rng.normal(0,18,g.shape)
    for _ in range(3):
        x=int(rng.integers(0,g.shape[1])); g[:,x:x+int(rng.integers(1,4))]+=rng.integers(20,60)*(1 if rng.random()<.5 else -1)
    h,w=g.shape; yy,xx=np.mgrid[0:h,0:w]; r=np.sqrt(((xx-w/2)/(w/2))**2+((yy-h/2)/(h/2))**2); g*=1-.35*np.clip(r-.4,0,1)
    g=np.clip(g,0,255).astype(np.uint8); return Image.fromarray(g).convert("RGB")
def hi8(im,u):
    """video Hi8: poca resolucion, color sucio, ruido y desplazamiento de crominancia"""
    w,h=im.size; sm_=im.resize((w//5,h//5),Image.BOX).resize((w,h),Image.BILINEAR)
    a=np.array(sm_).astype(np.float32); rng=np.random.default_rng(int(u*30)+5)
    a[...,0]=np.roll(a[...,0],6,axis=1); a[...,2]=np.roll(a[...,2],-6,axis=1)
    a+=rng.normal(0,12,a.shape[:2])[...,None]; a=a*np.array([1.0,1.04,.92]); 
    return Image.fromarray(np.clip(a,0,255).astype(np.uint8))
def stickman(d,x,y,sc):
    d.L(x,y-130*sc,x,y-80*sc,(60,44,30),2*sc)
    d.L(x-24*sc,y-80*sc,x+24*sc,y-30*sc,(90,66,42),4*sc); d.L(x+24*sc,y-80*sc,x-24*sc,y-30*sc,(90,66,42),4*sc)
    d.L(x-30*sc,y-62*sc,x+30*sc,y-62*sc,(90,66,42),4*sc); d.L(x,y-80*sc,x,y-18*sc,(90,66,42),4*sc)
    d.E(x,y-86*sc,8*sc,8*sc,(90,66,42))
def cairn(d,x,y,sc):
    for k,(w,h) in enumerate([(34,16),(26,13),(18,11),(11,9)]): d.E(x,y-sum([16,13,11,9][:k])*sc,w*sc,h*sc,(80+k*8,78+k*8,72+k*6))
def bare_trees(d,u,n=9):
    for i in range(n):
        x=(i*(560.0/n)+rnd(i,9)*50)%560-10; w=18+rnd(i,2)*16
        d.P([(x-w,960),(x+w,960),(x+w*.45,40),(x-w*.45,40)],(10,12,10,255))
        for b in range(4):
            by=200+b*150+rnd(i,b)*60; d.L(x,by,x+(60+b*20)*(1 if (i+b)%2 else -1),by-50,(10,12,10),5)
def viewfinder(d,u,rec=True):
    for (x,y,sx,sy) in((24,24,1,1),(516,24,-1,1),(24,936,1,-1),(516,936,-1,-1)):
        d.L(x,y,x+34*sx,y,(255,255,255,220),4); d.L(x,y,x,y+34*sy,(255,255,255,220),4)
    if rec and int(u*1.6)%2==0: d.E(56,60,9,9,(240,40,40)); 
    d.R(80,50,150,70,(0,0,0,0),0)
    t=int(u)+ 43*60+17
    for i,ch in enumerate(f"{(t//60)%60:02d}{t%60:02d}"): seg7(d,380+i*26+(12 if i>1 else 0),46,20,34,int(ch),(255,255,255),(0,0,0))
    d.R(450,900,500,926,(255,255,255),3); d.R(500,908,506,918,(255,255,255),1); d.R(454,904,484,922,(120,255,150),2)
    for k in range(int(960/6)): d.R(0,k*6,540,k*6+1,(0,0,0,30))
def trio(d,u,x0,y,sc):
    for k in range(3):
        x=x0+k*70; bob=abs(math.sin(u*5+k))*4*sc
        silhouette(d,x,y-bob,sc,(8,8,12)); d.R(x-18*sc,y-128*sc-bob,x+18*sc,y-76*sc-bob,(30,34,28),6*sc)
def sceneA(u,final=False):
    im=new((14,22,34),(50,66,90)); d=D(im)
    forest(d,u,dense=15,**FOR)
    bare_trees(d,u,8); stickman(d,380,520,1.5); stickman(d,120,560,1.1); cairn(d,300,820,1.4)
    fogband(d,u,520,800,(150,170,186),34)
    flashlight(d,170,900,350,520,.3,620,70)
    viewfinder(d,u)
    return hi8(im,u)
def sceneB(u):
    im=new((14,22,34),(50,66,90)); d=D(im)
    forest(d,u,dense=15,**FOR); bare_trees(d,u,7)
    d.P([(250,960),(330,960),(290,600),(262,600)],(40,34,28,230))
    x=((u*40)%700)-80
    trio(d,u,x*.5+90,780,1.2)
    for k in range(3):   # camara en mano del primero
        pass
    xc=x*.5+90+34; d.R(xc,660,xc+34,684,(20,20,24),3); d.E(xc+36,672,8,8,(60,70,90))
    fogband(d,u,560,820,(150,170,186),30)
    viewfinder(d,u,False)
    return bw16(im,u)
def sceneC(u):
    im=new((8,12,18),(24,36,46)); d=D(im)
    forest(d,u,sky=(10,16,28),sky2=(44,56,80),ground=(10,14,12),fog=(120,140,160),dense=12,moon=False)
    # campamento: tienda y fogata; tarjetas con instrucciones diarias
    d.P([(80,820),(230,820),(155,700)],(64,96,64)); d.P([(120,820),(190,820),(155,740)],(10,12,14))
    d.E(360,820,30,8,(0,0,0,80)); 
    for k in range(6): a=(u*3+k)%1; d.P([(360-14+k*5,820),(360+14-k*5,820),(360+math.sin(u*9+k)*6,780-a*40)],(255,150+k*14,40,230))
    d.E(360,810,80,50,(255,170,70,40))
    # tarjeta/nota del director sujeta a un arbol y mapa
    d.R(380,520,500,640,(244,240,226),3); 
    for q in range(5): d.L(392,540+q*18,486-(q%2)*20,540+q*18,(0,0,0,110),2.5)
    d.E(440,530,6,6,(220,60,60))
    d.R(40,520,180,620,(214,196,150),4); d.L(60,540,160,600,(60,100,60),3); d.L(60,600,160,540,(60,100,60,0),0); d.E(110,570,5,5,(220,60,60))
    # burbujas de dialogo improvisado
    for k,(x,y) in enumerate([(70,260),(300,320)]):
        a=sm((u-.8-k*1.4)/.4); 
        if a>0:
            d.R(x,y,x+150,y+60,(255,255,255,int(240*a)),14); d.P([(x+30,y+58),(x+54,y+58),(x+30,y+82)],(255,255,255,int(240*a)))
            for q in range(3): d.E(x+34+q*34,y+30,7,7,(60,60,70,int(255*a)))
    viewfinder(d,u)
    return hi8(im,u)
def poster(d,x,y,w,h,k,u):
    d.R(x,y,x+w,y+h,(244,240,226),2); d.R(x,y,x+w,y+h*.12,(200,40,50),2); ptext(d,x+10,y+4,'MISSING',w/60.0*1.0,(255,255,255))
    d.R(x+w*.18,y+h*.22,x+w*.82,y+h*.7,(120,116,108),3); silhouette(d,x+w*.5,y+h*.7,w/260.0*1.1,(30,30,34),arms=False)
    for q in range(3): d.L(x+w*.14,y+h*.78+q*h*.06,x+w*.86-(q%2)*w*.2,y+h*.78+q*h*.06,(0,0,0,110),2)
def sceneD(u):
    im=new((24,26,34),(44,46,60)); d=D(im)
    d.R(0,0,540,960,(36,34,36)); 
    for r in range(18):
        for c in range(8): d.R(c*70,r*54,c*70+66,r*54+50,(48,46,50),2)
    # carteles de desaparecidos
    for k,(x,y) in enumerate([(30,120),(190,150),(350,110),(60,420),(230,440)]):
        a=sm((u-.3-k*.6)/.4); 
        if a>0: poster(d,x,y+(1-a)*30,130,190,k,u)
    # ventana de navegador con la web
    d.R(280,420,510,760,(34,36,52),12); d.R(280,420,510,460,(60,64,90),12)
    for k in range(3): d.E(302+k*22,440,6,6,[(255,90,90),(255,200,70),(90,220,110)][k])
    d.R(300,480,490,610,(18,22,18),6); forest(d,u,**FOR) if False else None
    for k in range(5): d.L(310,630+k*22,310+150+((k*37)%100),630+k*22,(255,255,255,70),3)
    cx,cy=420+math.sin(u*1.1)*40,540+math.cos(u*.8)*30; d.P([(cx,cy),(cx+16,cy+22),(cx+6,cy+22),(cx,cy+34)],(250,250,250))
    return im
def sceneE(u):
    im=new((20,18,34),(46,38,64)); d=D(im)
    d.R(0,640,540,960,(36,30,40)); d.R(0,640,540,646,(255,255,255,24))
    def inner(d_,x,y,w,h):
        d_.R(x,y,x+w,y+h,(8,12,12)); 
        for k in range(6): xx=x+10+k*w/6; d_.P([(xx-6,y+h),(xx+6,y+h),(xx+3,y),(xx-3,y)],(20,30,24))
        flashlight(d_,x+w*.3,y+h-6,x+w*.55,y+h*.3,.3,h*.9,90); noise_static(d_,x,y,w,h,u,40,6)
    box=crt(d,130,380,280,250,(2,8,10),(190,182,158)); inner(d,*box); crt_fx(d,box)
    person_back(d,270,780,1.5,0,u)
    # pensamiento: ¿real? (signos de interrogacion y exclamacion)
    for k,(x,y,ch) in enumerate([(90,190,"?"),(250,130,"!"),(410,200,"?")]):
        a=sm((u-.5-k*.8)/.4)
        if a>0:
            d.E(x,y,42*a,42*a,(255,255,255,int(240*a)))
            if ch=="?": d.A(x,y-6,12,12,200,500,(40,40,50,int(255*a)),6); d.E(x,y+20,4,4,(40,40,50,int(255*a)))
            else: d.R(x-5,y-22,x+5,y+8,(40,40,50,int(255*a)),3); d.E(x,y+20,4,4,(40,40,50,int(255*a)))
    return im
def sceneF(u):
    im=new((10,14,22),(28,36,52)); d=D(im)
    for r in range(30): d.L(0,r*32,540,r*32,(255,255,255,7),1)
    for c in range(18): d.L(c*32,0,c*32,960,(255,255,255,7),1)
    p=sm(u/4.5)
    # barra pequena: presupuesto (unos 60 mil) frente a barra enorme: recaudacion (mas de 240 millones)
    d.R(90,820-8,200,820,(255,214,90),4)
    d.R(320,820-740*p,430,820,(80,200,130),6)
    for k in range(int(10*p)): d.E(375,800-k*70*p,34,10,(255,214,90,180))
    d.R(60,820,470,826,(255,255,255,90),0)
    ptext(d,70,150,'60K',9.0,(255,214,90)); ptext(d,280,150,str(int(240*p))+'M',9.0,(80,200,130))
    d.R(90,230,210,244,(0,0,0,0),0)
    return im
def sceneG(u):
    im=new((10,14,22),(28,36,52)); d=D(im)
    for r in range(3):
        for c in range(3):
            x=24+c*170; y=120+r*270; d.R(x,y,x+154,y+240,(18,22,28),8)
            d.R(x+6,y+6,x+148,y+234,(6,10,10),6); flashlight(d,x+30+(c*20)%80,y+230,x+90,y+80,.3,170,90) 
            for q in range(3): xx=x+14+q*46; d.P([(xx-4,y+234),(xx+4,y+234),(xx+2,y+12),(xx-2,y+12)],(14,20,18))
            if int(u*1.6+r+c)%2==0: d.E(x+20,y+26,5,5,(240,40,40))
            if (r+c)%2==0: d.R(x+6,y+6,x+148,y+234,(120,120,120,70),6)
            for k in range(8): d.R(x+6,y+6+k*28+(u*20)%28,x+148,y+7+k*28+(u*20)%28,(255,255,255,18),0)
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def shake(t,a=6): return math.sin(t*9.3)*a*.6+math.sin(t*23.1)*a*.4, math.cos(t*8.1)*a*.6+math.cos(t*19.7)*a*.4
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur)); sx,sy=shake(u+idx*3,5 if idx in(0,1,2,7) else 1.5)
    if idx==0: return 1.1+.3*sm(p),270+sx,520+sy
    if idx==1: return 1.1+.15*sm(p),270+sx,520+sy
    if idx==2: return 1.05+.1*sm(p),270+sx,500+sy
    if idx==3: return 1.0+.15*sm(p),270+sx,480+sy
    if idx==4: return 1.0+.3*sm(p),270+sx,540+sy
    if idx==5: return 1.0+.05*sm(p),270+sx,480+sy
    if idx==6: return 1.1-.1*sm(p),270+sx,480+sy
    return 1.4-.3*sm(p),270+sx,520+sy
core.CAM=cam
if __name__=="__main__": core.main()
