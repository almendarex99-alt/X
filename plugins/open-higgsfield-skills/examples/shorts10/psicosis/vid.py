import sys; sys.path.insert(0,"..")
from art import *
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
def sceneA(u,final=False):
    im=new((176,176,176),(120,120,124)); d=D(im); shower(d,u)
    # chorro de chocolate cayendo: unico color de la escena
    syrup_bottle(d,430,420,1.5,u,tilt=-.9)
    for k in range(30):
        t=(u*1.3+k*.05)%1; x=380-t*80+math.sin(k)*3; y=360+t*500
        d.E(x,y,5,9,BR+(255,))
    d.R(60,860,480,900,(60,60,64),10); drain_spiral(d,270,870,110,u)
    return im
def sceneB(u):
    im=new((70,70,74),(18,18,20)); d=D(im)
    for k in range(16):
        a=-1.2+k*.16; d.P([(270,80),(270+math.cos(a-.05)*800,80+math.sin(a-.05)*800+0),(270+math.cos(a+.05)*800,80+math.sin(a+.05)*800)],(255,255,255,10))
    d.E(400,160,48,48,gray(236)+(230,)); d.E(400,160,100,100,gray(236)+(30,))
    # casa y motel sobre la colina (silueta de cine clasico)
    d.P([(0,520),(160,460),(300,500),(440,440),(540,470),(540,640),(0,640)],gray(12)+(255,))
    d.R(120,360,230,480,gray(10)+(255,),2); d.P([(110,360),(175,310),(240,360)],gray(10)); d.R(150,330,166,364,gray(10),1); d.R(138,392,154,418,gray(236),1); d.R(190,392,206,418,gray(70),1)
    d.R(0,640,540,960,gray(26)+(255,),0)
    film_camera(d,150,820,.9,u)
    # silla de director y silueta
    d.L(380,820,380,740,gray(150),6); d.R(350,740,420,752,gray(170),3); d.L(352,752,420,820,gray(150),5); d.L(418,752,352,820,gray(150),5)
    silhouette(d,380,742,.8,gray(190)) if False else None
    clapper(d,300,880,.8,open_=(math.sin(u*3)>.4)*1.0)
    return im
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
def violin(d,x,y,sc,ang,u,k=0):
    pts_body=[(x-28*sc,y),(x+28*sc,y)]
    d.E(x,y,28*sc,36*sc,(120,70,36)); d.E(x,y-30*sc,22*sc,28*sc,(120,70,36)); d.R(x-6*sc,y-110*sc,x+6*sc,y-70*sc,(40,24,16),2*sc)
    d.R(x-3*sc,y-130*sc,x+3*sc,y-60*sc,(20,14,10),1)
    for q in(-1,1): d.A(x+q*10*sc,y-4*sc,5*sc,16*sc,70,110,(20,10,6),2*sc)
    # arco que corta las cuerdas con movimiento rapido
    bx=x+math.sin(u*14+k)*34*sc; d.L(bx-40*sc,y-26*sc,bx+40*sc,y-14*sc,(236,230,214),3*sc)
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
    d.E(270,520,120,120,(60,180,110,int(255*ck))); d.L(222,520,258,556,(255,255,255,int(255*ck)),16); d.L(258,556,328,470,(255,255,255,int(255*ck)),16)
    violin(d,270,860,1.5,0,u,1)
    for k in range(3): d.A(270,720,70+k*40+((u*60)%40),70+k*40+((u*60)%40),200,340,gray(255)+(int(180*(1-k*.3)),),3)
    return im
def sceneG(u):
    im=new((190,190,190),(110,110,114)); d=D(im); shower(d,u)
    # cortina translucida con la sombra de una figura (sin violencia explicita)
    d.R(40,60,500,900,(236,236,236,150),10)
    for k in range(8): d.A(40+k*60,60,20,16,180,360,gray(150),3)
    silhouette(d,270,880,2.5,gray(30),arms=True); d.R(0,0,540,960,(255,255,255,0),0)
    # rafagas del violin
    for k in range(12):
        a=k*.52+u*.2; d.L(270,520,270+math.cos(a)*400,520+math.sin(a)*500,(0,0,0,int(70*abs(math.sin(u*14+k)))),5)
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
