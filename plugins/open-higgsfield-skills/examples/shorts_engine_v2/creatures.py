"""Criaturas articuladas (cuadrupedos, T. rex, raptor, brazo robotico). Cada pata y la cola son cadenas de segmentos unidos."""
import math
from core import *
def shade(c,k): return tuple(max(0,min(255,int(v*k))) for v in c[:3])
def seg(d,p,q,w,col):
    d.L(p[0],p[1],q[0],q[1],col+(255,),w); d.E(p[0],p[1],w/2,w/2,col+(255,)); d.E(q[0],q[1],w/2,w/2,col+(255,))
def leg(d,hx,hy,l1,l2,t1,t2,w,col,foot=1,toe=1.0,fs=1.0):
    """pata de dos segmentos: t1,t2 angulos respecto a la vertical (0=abajo); foot=+1 pie hacia la derecha"""
    k=(hx+math.sin(t1)*l1,hy+math.cos(t1)*l1); a=(k[0]+math.sin(t2)*l2,k[1]+math.cos(t2)*l2)
    seg(d,(hx,hy),k,w,col); seg(d,k,a,w*.82,shade(col,.93))
    d.E(a[0]+foot*w*.35,a[1]+w*.12,w*.85*fs,w*.42,shade(col,.8)+(255,))
    return a
def trex(d,x,y,sc,u,jaw=0.6,col=(78,104,64),walk=True,facing=1,roar=0.0):
    f=facing; S=sc; ph=u*2.6 if walk else 0.0
    dk=shade(col,.62); lt=shade(col,1.18)
    def X(px): return x+f*px*S
    body=(X(0),y-170*S)
    # cola (cadena de segmentos que se afina y ondula)
    tp=(X(-52),y-176*S); pts=[tp]; ang=math.pi+.25
    for k in range(9):
        ang+= math.sin(u*2.2-k*.55)*.06; L=(34-k*2.2)*S
        pts.append((pts[-1][0]+f*math.cos(ang)*L*-1*-1*1 if False else pts[-1][0]+f*math.cos(ang)*L,pts[-1][1]+math.sin(ang)*L*-1))
    for i in range(len(pts)-1): seg(d,pts[i],pts[i+1],(46-i*4.4)*S,col)
    # patas traseras (muslo grueso + espinilla + pie con 3 dedos)
    for k,off in enumerate((0,math.pi)):
        sw=math.sin(ph+off)*.4 if walk else .1
        hip=(X(-8+k*6),y-150*S); knee=(hip[0]+f*math.sin(.5+sw)*58*S,hip[1]+math.cos(.5+sw)*58*S)
        ank=(knee[0]+f*math.sin(-.35+sw*.5-max(0,-math.cos(ph+off))*.5)*62*S,knee[1]+math.cos(-.35+sw*.5)*62*S)
        seg(d,hip,knee,40*S,shade(col,.9+.1*k)); seg(d,knee,ank,26*S,shade(col,.82+.1*k))
        for t in range(3):
            tip=(ank[0]+f*(10+t*9)*S,ank[1]+(10-t*1)*S); d.P([(ank[0],ank[1]-4*S),(tip[0],tip[1]),(ank[0],ank[1]+6*S)],shade(col,.75)+(255,)); d.E(tip[0],tip[1],3*S,3*S,(240,236,220))
    # tronco
    d.E(X(0),y-176*S,74*S,52*S,col+(255,)); d.E(X(8),y-158*S,52*S,28*S,lt+(255,));
    for k in range(7): d.A(X(-40+k*14),y-190*S,10*S,8*S,200,340,dk+(120,),2*S)
    # cuello y cabeza con mandibula articulada
    nk=(X(54),y-208*S); hd=(X(98),y-238*S+math.sin(u*2)*3*S)
    d.P([(X(30),y-190*S),(nk[0],nk[1]-20*S),(hd[0],hd[1]-14*S),(hd[0],hd[1]+24*S),(X(56),y-168*S)],col+(255,))
    d.E(hd[0],hd[1],44*S,32*S,col+(255,))
    d.P([(hd[0]+12*S*f,hd[1]-14*S),(hd[0]+96*S*f,hd[1]-6*S),(hd[0]+92*S*f,hd[1]+14*S),(hd[0]+10*S*f,hd[1]+22*S)],shade(col,1.02)+(255,))
    jw=jaw*34*S
    d.P([(hd[0]+8*S*f,hd[1]+14*S),(hd[0]+92*S*f,hd[1]+8*S+jw*.9),(hd[0]+84*S*f,hd[1]+24*S+jw),(hd[0]+4*S*f,hd[1]+34*S+jw*.3)],dk+(255,))
    if jaw>.15: d.P([(hd[0]+12*S*f,hd[1]+16*S),(hd[0]+90*S*f,hd[1]+12*S),(hd[0]+86*S*f,hd[1]+8*S+jw*.9),(hd[0]+10*S*f,hd[1]+26*S+jw*.2)],(170,50,60,255))
    for k in range(8):
        tx=hd[0]+(18+k*10)*S*f; d.P([(tx,hd[1]+14*S),(tx+4*S*f,hd[1]+14*S),(tx+2*S*f,hd[1]+14*S+11*S)],(244,240,224));
        if jaw>.15: d.P([(tx+3*S*f,hd[1]+12*S+jw*.8),(tx+7*S*f,hd[1]+12*S+jw*.8),(tx+5*S*f,hd[1]+jw*.8-2*S+4*S)],(244,240,224))
    d.E(hd[0]+14*S*f,hd[1]-12*S,7*S,6*S,(255,210,60)); d.E(hd[0]+16*S*f,hd[1]-12*S,2.4*S,5*S,(10,10,10))
    d.E(hd[0]+84*S*f,hd[1]-2*S,3*S,2*S,(20,30,20)); d.L(hd[0]+6*S*f,hd[1]-22*S,hd[0]+26*S*f,hd[1]-18*S,dk+(255,),3*S)
    # bracitos con 2 garras
    sh=(X(46),y-170*S); el=(sh[0]+f*14*S,sh[1]+22*S+math.sin(u*4)*3*S); wr=(el[0]+f*18*S,el[1]+10*S)
    seg(d,sh,el,11*S,col); seg(d,el,wr,9*S,col)
    for t in range(2): d.P([(wr[0],wr[1]-3*S+t*5*S),(wr[0]+f*14*S,wr[1]+3*S+t*6*S),(wr[0],wr[1]+2*S+t*5*S)],(236,230,214))
    return hd
def raptor(d,x,y,sc,u,col=(92,100,64),facing=1,jaw=0.2):
    f=facing; S=sc; ph=u*5
    def X(px): return x+f*px*S
    pts=[(X(-24),y-92*S)]; ang=math.pi+.1
    for k in range(7): ang+=math.sin(u*3-k*.6)*.07; L=(22-k*2)*S; pts.append((pts[-1][0]+f*math.cos(ang)*L,pts[-1][1]-math.sin(ang)*L*-1*-1*0+math.sin(ang)*L*-1*-1))
    for i in range(len(pts)-1): seg(d,pts[i],pts[i+1],(22-i*2.6)*S,col)
    for k,off in enumerate((0,math.pi)):
        sw=math.sin(ph+off)*.5; hip=(X(-4+k*5),y-78*S); kn=(hip[0]+f*math.sin(.7+sw)*34*S,hip[1]+math.cos(.7+sw)*34*S); an=(kn[0]+f*math.sin(-.6+sw*.4)*36*S,kn[1]+math.cos(-.6+sw*.4)*36*S)
        seg(d,hip,kn,18*S,shade(col,.9)); seg(d,kn,an,11*S,shade(col,.8))
        for t in range(3): tp=(an[0]+f*(7+t*6)*S,an[1]+6*S); d.P([(an[0],an[1]-2*S),tp,(an[0],an[1]+4*S)],shade(col,.7)+(255,))
        d.P([(an[0]+f*4*S,an[1]-8*S),(an[0]+f*16*S,an[1]-14*S),(an[0]+f*6*S,an[1]-2*S)],(240,236,220))
    d.E(X(0),y-98*S,40*S,26*S,col+(255,)); d.E(X(4),y-88*S,28*S,14*S,shade(col,1.2)+(255,))
    hd=(X(52),y-132*S); d.P([(X(26),y-108*S),(X(44),y-128*S),(hd[0],hd[1]-6*S),(hd[0],hd[1]+10*S),(X(36),y-92*S)],col+(255,)); d.E(hd[0],hd[1],18*S,13*S,col+(255,))
    d.P([(hd[0]+4*S*f,hd[1]-6*S),(hd[0]+36*S*f,hd[1]-2*S),(hd[0]+34*S*f,hd[1]+6*S),(hd[0]+2*S*f,hd[1]+10*S)],col+(255,))
    jw=jaw*18*S; d.P([(hd[0]+2*S*f,hd[1]+6*S),(hd[0]+34*S*f,hd[1]+5*S+jw),(hd[0]+30*S*f,hd[1]+12*S+jw),(hd[0],hd[1]+14*S)],shade(col,.6)+(255,))
    d.E(hd[0]+6*S*f,hd[1]-5*S,3.2*S,3*S,(255,210,60)); d.E(hd[0]+7*S*f,hd[1]-5*S,1.2*S,2.6*S,(10,10,10))
    for k in range(5): d.P([(hd[0]+(10+k*5)*S*f,hd[1]+6*S),(hd[0]+(12+k*5)*S*f,hd[1]+6*S),(hd[0]+(11+k*5)*S*f,hd[1]+10*S)],(244,240,224))
    # brazos con 3 dedos con garra
    sh=(X(26),y-104*S); el=(sh[0]+f*10*S,sh[1]+14*S); wr=(el[0]+f*12*S,el[1]+6*S+math.sin(u*5)*3*S)
    seg(d,sh,el,6*S,col); seg(d,el,wr,5*S,col)
    for t in range(3): d.P([(wr[0],wr[1]-3*S+t*3*S),(wr[0]+f*10*S,wr[1]+t*4*S),(wr[0],wr[1]+t*3*S)],(236,230,214))
def quad(d,x,y,sc,u,col,belly=None,kind="elephant",facing=1,walk=True,spd=2.4):
    f=facing; S=sc; ph=u*spd if walk else 0
    def X(px): return x+f*px*S
    ll={"elephant":62,"tiger":46,"horse":84,"tortoise":22,"croc":18}[kind]
    bh={"elephant":96,"tiger":50,"horse":58,"tortoise":50,"croc":26}[kind]
    bw={"elephant":86,"tiger":84,"horse":78,"tortoise":72,"croc":120}[kind]
    wd={"elephant":22,"tiger":13,"horse":10,"tortoise":14,"croc":12}[kind]
    by=y-ll*S-bh*S*.45
    shadow_=d.E(X(0),y+2*S,bw*S*1.1,7*S,(0,0,0,60))
    # patas traseras y delanteras (2 segmentos); las del lado lejano mas oscuras
    for k,(px,off,dim) in enumerate(((-bw*.62,math.pi,.8),(bw*.62-6,0,.8),(-bw*.62+14,0,1.0),(bw*.62-20,math.pi,1.0))):
        sw=math.sin(ph+off)*(.38 if kind!="croc" else .5);
        leg(d,X(px),by+bh*S*.25,ll*S*.52,ll*S*.52,f*(sw),f*(sw*.4-max(0,math.cos(ph+off))*.3*(1 if kind!="elephant" else .4)),wd*S,shade(col,dim),foot=f)
    # cola
    tw=math.sin(u*2.6)*10*S; seg(d,(X(-bw*.85),by-6*S),(X(-bw*1.05),by+18*S+tw),(7 if kind!="croc" else 14)*S,col)
    if kind=="croc": seg(d,(X(-bw*1.05),by+0*S),(X(-bw*1.35),by+14*S+tw),8*S,col); seg(d,(X(-bw*1.35),by+14*S+tw),(X(-bw*1.7),by+10*S+tw*1.6),4*S,col)
    # cuerpo
    d.E(X(0),by,bw*S,bh*S*.5,col+(255,));
    if belly: d.E(X(0),by+bh*S*.22,bw*S*.9,bh*S*.26,belly+(255,))
    d.E(X(-bw*.2),by-bh*S*.28,bw*S*.5,bh*S*.12,(255,255,255,26))
    return dict(by=by,bw=bw,bh=bh,X=X,S=S,f=f)
def elephant(d,x,y,sc,u,facing=1,walk=True,col=(150,154,164)):
    b=quad(d,x,y,sc,u,col,kind="elephant",facing=facing,walk=walk,spd=2.0); X=b["X"]; S=sc; f=facing; by=b["by"]
    hd=(X(96),by-24*S); d.P([(X(60),by-40*S),(X(96),by-60*S),(X(120),by-20*S),(X(104),by+24*S),(X(64),by+30*S)],col+(255,)); d.E(hd[0],hd[1],34*S,38*S,col+(255,))
    d.E(X(76),by-20*S,30*S,40*S,shade(col,.84)+(255,)); d.E(X(76),by-20*S,22*S,32*S,(190,150,150,120))   # oreja
    p=(X(116),by-6*S)
    for k in range(7):
        q=(p[0]+f*math.sin(.2+k*.34+math.sin(u*2)*.1)*12*S,p[1]+math.cos(.2+k*.2)*14*S); seg(d,p,q,(18-k*1.6)*S,col); p=q
    d.E(X(108),by-30*S,4*S,4*S,(20,20,24)); d.P([(X(112),by+4*S),(X(138),by+34*S),(X(120),by+8*S)],(240,236,220))
def tiger(d,x,y,sc,u,facing=1,walk=True,col=(236,140,40)):
    b=quad(d,x,y,sc,u,col,belly=(250,236,210),kind="tiger",facing=facing,walk=walk,spd=3.0); X=b["X"]; S=sc; f=facing; by=b["by"]
    for k in range(9): d.P([(X(-60+k*14),by-34*S),(X(-52+k*14),by-34*S),(X(-56+k*14),by+4*S+(k%3)*4*S)],(30,20,10,255))
    hd=(X(92),by-26*S); d.E(hd[0],hd[1],27*S,24*S,col+(255,)); d.E(hd[0]+f*14*S,hd[1]+8*S,15*S,11*S,(250,236,210))
    for sg in(-1,1): d.E(hd[0]-f*10*S,hd[1]-22*S+(sg>0)*3*S,8*S,9*S,col+(255,)); d.E(hd[0]-f*10*S,hd[1]-22*S+(sg>0)*3*S,4*S,5*S,(60,30,20))
    d.E(hd[0]+f*28*S,hd[1]+4*S,4*S,3*S,(40,20,20)); d.E(hd[0]+f*10*S,hd[1]-6*S,3.6*S,3*S,(250,230,90)); d.E(hd[0]+f*11*S,hd[1]-6*S,1.2*S,2.6*S,(10,10,10))
    for k in range(3): d.L(hd[0]-8*S*f,hd[1]-18*S+k*5*S,hd[0]+4*S*f,hd[1]-12*S+k*5*S,(30,20,10),2.2*S)
    d.A(hd[0]+f*18*S,hd[1]+14*S,10*S,5*S,10,170,(60,20,20),2*S)
def croc(d,x,y,sc,u,facing=1,jaw=0.3,col=(70,120,60)):
    b=quad(d,x,y,sc,u,col,belly=(190,200,120),kind="croc",facing=facing,spd=1.8); X=b["X"]; S=sc; f=facing; by=b["by"]
    for k in range(10): d.P([(X(-80+k*12),by-14*S),(X(-74+k*12),by-22*S),(X(-68+k*12),by-14*S)],shade(col,.7)+(255,))
    hd=(X(122),by-2*S); d.E(hd[0],hd[1],24*S,17*S,col+(255,)); jw=jaw*22*S
    d.P([(hd[0]+8*S*f,hd[1]-10*S),(hd[0]+86*S*f,hd[1]-4*S),(hd[0]+84*S*f,hd[1]+4*S),(hd[0]+4*S*f,hd[1]+8*S)],col+(255,))
    d.P([(hd[0]+4*S*f,hd[1]+6*S),(hd[0]+84*S*f,hd[1]+4*S+jw),(hd[0]+80*S*f,hd[1]+14*S+jw),(hd[0]+2*S*f,hd[1]+16*S)],shade(col,.8)+(255,))
    for k in range(9): d.P([(hd[0]+(14+k*8)*S*f,hd[1]+4*S),(hd[0]+(17+k*8)*S*f,hd[1]+4*S),(hd[0]+(15.5+k*8)*S*f,hd[1]+10*S)],(244,240,224))
    d.E(hd[0]+4*S*f,hd[1]-12*S,7*S,6*S,col+(255,)); d.E(hd[0]+5*S*f,hd[1]-12*S,3.2*S,3*S,(255,210,60)); d.E(hd[0]+6*S*f,hd[1]-12*S,1*S,2.6*S,(10,10,10))
def tortoise(d,x,y,sc,u,facing=1,col=(110,120,70)):
    b=quad(d,x,y,sc,u,col,kind="tortoise",facing=facing,spd=1.2); X=b["X"]; S=sc; f=facing; by=b["by"]
    d.E(X(0),by-10*S,66*S,42*S,shade(col,1.1)+(255,));
    for k in range(5): d.A(X(-40+k*20),by-14*S,16*S,14*S,180,360,shade(col,.7)+(255,),2.4*S)
    hd=(X(78+math.sin(u*2)*3),by-8*S); seg(d,(X(60),by),hd,15*S,shade(col,1.2)); d.E(hd[0],hd[1],12*S,10*S,shade(col,1.2)+(255,)); d.E(hd[0]+f*6*S,hd[1]-2*S,2.4*S,2.4*S,(10,10,10))
def horse(d,x,y,sc,u,facing=1,walk=True,col=(130,86,56)):
    b=quad(d,x,y,sc,u,col,kind="horse",facing=facing,walk=walk,spd=3.0); X=b["X"]; S=sc; f=facing; by=b["by"]
    nk=(X(70),by-24*S); hd=(X(108),by-84*S); seg(d,(X(60),by-10*S),hd,34*S,col); d.E(hd[0],hd[1],24*S,18*S,col+(255,)); d.P([(hd[0]+4*S*f,hd[1]-6*S),(hd[0]+40*S*f,hd[1]+8*S),(hd[0]+34*S*f,hd[1]+22*S),(hd[0]-4*S*f,hd[1]+12*S)],col+(255,))
    d.P([(hd[0]-8*S*f,hd[1]-14*S),(hd[0]-4*S*f,hd[1]-34*S),(hd[0]+4*S*f,hd[1]-14*S)],col+(255,)); d.E(hd[0]+8*S*f,hd[1]-4*S,3.2*S,3*S,(10,10,10))
    for k in range(9): d.P([(X(66+k*1.5),by-20*S-k*7*S),(X(54+k*1.5),by-12*S-k*7*S),(X(68+k*1.5),by-6*S-k*7*S)],(40,26,20,255))
def claw_arm(d,x0,y0,a1,a2,sc,col=(120,126,136),l1=110,l2=100,fing=3,open_=0.6,w=10):
    """brazo robotico: dos segmentos + pinza de dedos"""
    p1=(x0+math.sin(a1)*l1*sc,y0+math.cos(a1)*l1*sc); p2=(p1[0]+math.sin(a2)*l2*sc,p1[1]+math.cos(a2)*l2*sc)
    seg(d,(x0,y0),p1,w*sc,col); seg(d,p1,p2,w*.8*sc,shade(col,.9)); d.E(p1[0],p1[1],w*.9*sc,w*.9*sc,shade(col,1.15)+(255,)); d.E(p2[0],p2[1],w*.8*sc,w*.8*sc,shade(col,.8)+(255,))
    for k in range(fing):
        t=(k-(fing-1)/2)*open_; q=(p2[0]+math.sin(a2+t)*26*sc,p2[1]+math.cos(a2+t)*26*sc); seg(d,p2,q,5*sc,shade(col,1.2)); q2=(q[0]+math.sin(a2+t*1.8)*14*sc,q[1]+math.cos(a2+t*1.8)*14*sc); seg(d,q,q2,4*sc,shade(col,1.3))
    return p2
