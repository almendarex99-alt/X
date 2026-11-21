import sys; sys.path.insert(0,"..")
from art import *
from PIL import Image
import numpy as np
BR=(92,48,24)
def gray(v): return (v,v,v)
def syrup_bottle(d,x,y,sc,u,tilt=0.0):
    pts=[(x-20*sc,y),(x+20*sc,y),(x+20*sc,y-70*sc),(x+8*sc,y-96*sc),(x+8*sc,y-112*sc),(x-8*sc,y-112*sc),(x-8*sc,y-96*sc),(x-20*sc,y-70*sc)]
    d.P(rotpts(pts,x,y,tilt),(70,36,18)); d.R(x-6*sc,y-120*sc,x+6*sc,y-112*sc,(240,240,240),2*sc) if tilt==0 else None
    d.P(rotpts([(x-20*sc,y-60*sc),(x+20*sc,y-60*sc),(x+20*sc,y-24*sc),(x-20*sc,y-24*sc)],x,y,tilt),(236,226,200))
def drain_spiral(d,cx,cy,R,u,brown=True,a=255):
    d.E(cx,cy,R,R*.5,gray(210)+(a,)); d.E(cx,cy,R*.92,R*.46,gray(160)+(a,))
    for k in range(5):
        ang=u*3+k*1.26; r=R*.8*(1-k*.14); col=(BR+(a,)) if brown else (gray(46)+(a,))
        d.E(cx+math.cos(ang)*r*.5,cy+math.sin(ang)*r*.25,R*.32,R*.18,col)
    d.E(cx,cy,R*.25,R*.12,(20,20,22,a))
    for k in range(6): d.L(cx-R*.2+k*R*.08,cy-R*.1,cx-R*.2+k*R*.08,cy+R*.1,(80,80,86,a),2)

def bands(im,y0,y1,seed,amp=180,n=9):
    """barras horizontales desplazadas (tarjeta de titulo estilo Saul Bass)"""
    a=np.array(im); S_=3; h=(y1-y0)*S_; y0s=y0*S_
    step=max(1,h//n)
    for k in range(n):
        off=int(math.sin(seed*1.2+k*1.9)*amp*S_*(1-0.5*(k%2)))
        a[y0s+k*step:y0s+(k+1)*step]=np.roll(a[y0s+k*step:y0s+(k+1)*step],off,axis=1)
    return Image.fromarray(a)
def big_head(d,u):
    d.E(270,80,110,28,(124,124,130)); d.E(270,72,110,22,(196,198,204))
    for r in range(5):
        for c in range(9): d.E(270-88+c*22+(r%2)*10,66+r*7,2.2,2.2,(60,60,66))
    d.R(258,0,282,56,(120,120,126),0)
    for k in range(40):
        x=170+rnd(k)*200; t=(u*1.5+rnd(k,2))%1; d.L(x,92+t*860,x-2,108+t*860,(255,255,255,170),2)
def violin(d,x,y,sc,ang,u,k=0):
    pts=lambda arr:[(x+px*sc,y+py*sc) for px,py in arr]
    d.E(x,y+22*sc,32*sc,24*sc,(120,66,30)); d.E(x,y-6*sc,24*sc,20*sc,(120,66,30)); d.R(x-18*sc,y-4*sc,x+18*sc,y+14*sc,(120,66,30),8*sc)
    d.E(x,y+22*sc,28*sc,20*sc,(150,84,38,160)); d.E(x,y-6*sc,20*sc,16*sc,(150,84,38,160))
    for sg in(-1,1): d.A(x+sg*10*sc,y+8*sc,5*sc,14*sc,70,110,(20,10,6),2*sc)
    d.R(x-5*sc,y-84*sc,x+5*sc,y-20*sc,(30,18,10),2*sc); d.E(x,y-92*sc,9*sc,9*sc,(30,18,10))
    for q in range(4): d.L(x-3*sc+q*2*sc,y-80*sc,x-3*sc+q*2*sc,y+36*sc,(230,226,210,200),1.1*sc)
    d.R(x-12*sc,y+40*sc,x+12*sc,y+46*sc,(20,12,8),2*sc)
    bx=x+math.sin(u*14+k)*36*sc; d.L(bx-52*sc,y+2*sc,bx+52*sc,y+12*sc,(236,230,214),3*sc); d.L(bx-52*sc,y+2*sc,bx+52*sc,y+12*sc,(30,20,12),1*sc)
def sceneA(u,final=False):
    im=new((176,176,176),(120,120,124)); d=D(im); shower(d,u); big_head(d,u)
    # chorro de chocolate cayendo: unico color de la escena
    syrup_bottle(d,430,420,1.5,u,tilt=-.9)
    for k in range(30):
        t=(u*1.3+k*.05)%1; x=380-t*80+math.sin(k)*3; y=360+t*500
        d.E(x,y,5,9,BR+(255,))
    d.R(60,860,480,900,(60,60,64),10); drain_spiral(d,270,870,110,u)
    return im
def sceneB(u):
    im=new((70,70,74),(18,18,20)); d=D(im)
    d.E(400,150,48,48,gray(236)+(230,)); d.E(400,150,100,100,gray(236)+(30,))
    d.P([(0,520),(160,470),(300,500),(440,450),(540,480),(540,640),(0,640)],gray(12)+(255,))
    # casa victoriana: torre, tejado en mansarda, porche y ventanas encendidas
    d.R(120,360,250,480,gray(10)+(255,),2); d.P([(108,360),(185,300),(262,360)],gray(10)); d.R(150,260,196,312,gray(10)+(255,),2); d.P([(144,262),(173,224),(202,262)],gray(10))
    d.R(100,476,270,492,gray(10),2)
    for (wx,wy,lit) in[(138,392,1),(190,392,0),(160,282,1),(214,424,1)]: d.R(wx,wy,wx+16,wy+26,gray(236) if lit else gray(60),2)
    # motel en L con letrero de neon
    d.R(300,520,520,566,gray(30)+(255,),2); d.R(300,512,520,522,gray(18),0)
    for k in range(5): d.R(316+k*40,530,336+k*40,566,gray(120),2)
    d.R(460,430,468,520,gray(40),1); d.R(412,420,520,462,gray(22),4)
    ptext(d,420,426,"MOTEL",3.4,(255,255,255)); ptext(d,420,448,"VACANCY",2.2,(255,255,255,200)[:3])
    d.R(0,640,540,960,gray(26)+(255,),0)
    film_camera(d,150,840,.9,u); clapper(d,330,890,.8,open_=(math.sin(u*3)>.4)*1.0)
    # tarjeta de titulo con barras horizontales
    d.R(0,0,540,196,gray(0)+(235,),0)
    ptext(d,86,40,"PSYCHO",11.0,(255,255,255))
    return bands(im,36,168,u,60,8)
def sceneC(u):
    im=new((176,176,176),(120,120,124)); d=D(im)
    for r in range(12):
        for c in range(14): d.R(c*40,r*40,c*40+38,r*40+38,gray(206),2)
    # izquierda: lo que ve el ojo (marron); derecha: lo que ve la camara en blanco y negro (gris oscuro)
    d.R(0,0,270,960,(0,0,0,0),0)
    drain_spiral(d,135,520,120,u,True); d.E(135,300,70,60,(0,0,0,0))
    drain_spiral(d,405,520,120,u,False)
    d.R(268,0,272,960,gray(20)+(255,),0)
    syrup_bottle(d,270,330,1.4,u,tilt=0.0)
    for k in range(18):
        t=(u*1.2+k*.06)%1; d.E(270,356+t*150,5,9,BR+(255,))
    # indicadores ojo / camara
    d.E(135,150,40,24,(255,255,255)); d.E(135,150,14,14,(60,40,20)); 
    d.R(350,126,460,176,gray(30)+(255,),8); d.E(405,150,16,16,gray(220)); d.E(405,150,7,7,(10,10,12))
    return im
def sceneD(u):
    im=new((24,24,26),(52,52,56)); d=D(im)
    # cuadricula de planos (cortes) que se encienden rapido
    n=int(clamp(u/5.0)*45)
    for r in range(9):
        for c in range(5):
            k=r*5+c; x=24+c*100; y=110+r*72
            on=k<n; hot=(k==n-1)
            d.R(x,y,x+92,y+62,gray(236) if hot else (gray(120) if on else gray(40)),4)
            if on:
                silhouette(d,x+30+(k%3)*14,y+60,.22,gray(30),arms=False); d.L(x+60,y+10,x+80,y+50,gray(40),3)
    # reloj/crono de menos de un minuto
    d.E(270,820,70,70,gray(240)); d.E(270,820,70,70,None,gray(20),5)
    a=(u/5.0)*math.pi*2*.8-math.pi/2; d.L(270,820,270+math.cos(a)*54,820+math.sin(a)*54,(210,40,50),4)
    d.A(270,820,60,60,-90,-90+360*.8,(210,40,50,255),5)
    number(d,330,788,min(78,int(u/5.0*78)),2,26,50,(255,255,255))
    return im
def sceneE(u):
    im=new((16,16,20),(40,40,50)); d=D(im)
    # silencio (linea plana) frente a violines estridentes (onda dentada)
    d.R(30,130,510,260,(10,10,14),10); d.L(40,195,500,195,gray(120),3)
    d.R(30,300,510,430,(10,10,14),10)
    pts=[]
    for x in range(40,500,5):
        t=(x/460.0)*4+u*3; v=(1 if int(t*2)%2 else -1)*(26+30*abs(math.sin(t*5)))
        pts.append((x,365+v*(sm(u/2.0)))) 
    for i in range(len(pts)-1): d.L(pts[i][0],pts[i][1],pts[i+1][0],pts[i+1][1],(255,255,255),3)
    d.L(40,128,40,128,(0,0,0,0),0)
    for k in range(5): violin(d,70+k*100,700+(k%2)*20,1.2,0,u,k)
    # pentagrama con notas que golpean
    for k in range(5): d.L(40,470+k*12,500,470+k*12,gray(200),1.5)
    for k in range(10):
        x=60+k*44; y=470+((k*7)%5)*12
        d.E(x,y,7,5,gray(250)); d.L(x+6,y,x+6,y-30,gray(250),2)
        d.P([(x+6,y-30),(x+18,y-22),(x+6,y-20)],gray(250))
    return im
def sceneF(u):
    im=new((10,10,14),(30,30,36)); d=D(im)
    for k in range(18):
        a=-1.57+(k-9)*.05; d.P([(270,60),(270+math.cos(a-.03)*900,60+math.sin(a-.03)*900+400),(270+math.cos(a+.03)*900,60+math.sin(a+.03)*900+400)],(255,255,255,12))
    d.R(130,90,410,150,gray(30),6); d.E(270,120,26,26,gray(190)); d.E(270,120,26,26,None,gray(240),4)
    ck=sm((u-1.2)/.5)
    d.E(270,470,120,120,gray(236)+(int(255*ck),)); d.L(222,470,258,506,gray(30)+(int(255*ck),),16); d.L(258,506,328,420,gray(30)+(int(255*ck),),16)
    violin(d,270,800,1.6,0,u,1)
    for k in range(3): d.A(270,690,70+k*40+((u*60)%40),70+k*40+((u*60)%40),200,340,gray(255)+(int(180*(1-k*.3)),),3)
    return im
def sceneG(u):
    im=new((190,190,190),(110,110,114)); d=D(im); shower(d,u); big_head(d,u)
    d.R(40,60,500,900,(236,236,236,150),10)
    for k in range(8): d.A(40+k*60,60,20,16,180,360,gray(150),3)
    silhouette(d,270,880,2.5,gray(30),arms=True)
    for k in range(12):
        a=k*.52+u*.2; d.L(270,520,270+math.cos(a)*400,520+math.sin(a)*500,(0,0,0,int(70*abs(math.sin(u*14+k)))),5)
    # la camara cae al desague y se convierte en un ojo (transicion clasica)
    e=sm((u-3.0)/1.4)
    if e>0:
        d.R(0,0,540,960,gray(0)+(int(255*e),),0)
        R=140+60*e
        d.E(270,480,R*1.4,R*.7,gray(236)+(int(255*e),)); d.E(270,480,R*.62,R*.62,gray(120)+(int(255*e),)); d.E(270,480,R*.26,R*.26,gray(0)+(int(255*e),))
        for k in range(12): a=k*.52; d.L(270+math.cos(a)*R*.28,480+math.sin(a)*R*.28,270+math.cos(a)*R*.6,480+math.sin(a)*R*.6,gray(60)+(int(255*e),),2)
        d.E(250,462,16,10,gray(255)+(int(220*e),))
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx==0: return 1.0+.35*sm(p),300,520
    if idx==1: return 1.0+.2*sm(p),270,560
    if idx==2: return 1.0+.15*sm(p),270,500
    if idx==3: return 1.0+.12*sm(p),270,480
    if idx==4: return 1.0+.2*sm(p),270,520
    if idx==5: return 1.0+.1*sm(p),270,500
    if idx==6: return 1.3-.3*sm(p),270,520
    return 1.4-.4*sm(p),300,520
core.CAM=cam
if __name__=="__main__": core.main()
