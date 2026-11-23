"""Personajes y utileria del folclore de Krampus (estilos del rig, mascaras, cuernos, cascabeles, ramas, mitra y baculo)."""
import math, random
from core import *
from rig import *
KT=[0.0]            # tiempo para animar lengua y cadenas
def _horn(d,hx,hy,sc,sg,col=(214,204,180),L=1.0,curl=1.0):
    pts=[]
    for i in range(13):
        t=i/12; x=11+34*math.sin(t*math.pi*.78)*curl; y=16+64*(t**.85)*L; pts.append((hx+sg*x*sc,hy-y*sc))
    left=[];right=[]
    for i,(x,y) in enumerate(pts):
        j=min(i+1,len(pts)-1); k=max(i-1,0); tx,ty=pts[j][0]-pts[k][0],pts[j][1]-pts[k][1]; n=math.hypot(tx,ty)+1e-6; nx,ny=-ty/n,tx/n
        w=(7.5*(1-i/12)+1.2)*sc; left.append((x+nx*w,y+ny*w)); right.append((x-nx*w,y-ny*w))
    d.P(left+right[::-1],col+(255,))
    for i in range(1,12,2): d.L(left[i][0],left[i][1],right[i][0],right[i][1],(130,118,96,200),1.2*sc)
def krampus_face(d,hx,hy,sc):
    t=KT[0]
    d.E(hx,hy+2*sc,21*sc,24*sc,(86,70,62,255))
    d.P([(hx-20*sc,hy-10*sc),(hx,hy-6*sc),(hx+20*sc,hy-10*sc),(hx+16*sc,hy-16*sc),(hx,hy-12*sc),(hx-16*sc,hy-16*sc)],(40,30,26))
    for sg in(-1,1):
        d.E(hx+sg*9*sc,hy-3*sc,6.2*sc,4.2*sc,(255,206,56,255)); d.E(hx+sg*9*sc,hy-3*sc,13*sc,11*sc,(255,190,40,45)); d.E(hx+sg*9*sc,hy-3*sc,1.1*sc,3.8*sc,(10,8,6,255))
        d.L(hx+sg*3*sc,hy-9*sc,hx+sg*16*sc,hy-13*sc,(30,22,18,255),2.2*sc)
    d.P([(hx-3*sc,hy),(hx+3*sc,hy),(hx+5*sc,hy+9*sc),(hx-5*sc,hy+9*sc)],(66,52,46)); d.E(hx-2.4*sc,hy+9*sc,1.4*sc,1.1*sc,(16,12,10)); d.E(hx+2.4*sc,hy+9*sc,1.4*sc,1.1*sc,(16,12,10))
    d.P([(hx-14*sc,hy+12*sc),(hx+14*sc,hy+12*sc),(hx+11*sc,hy+24*sc),(hx,hy+27*sc),(hx-11*sc,hy+24*sc)],(52,14,16,255))
    for k in range(7): d.P([(hx-12*sc+k*4*sc,hy+12.4*sc),(hx-9*sc+k*4*sc,hy+12.4*sc),(hx-10.5*sc+k*4*sc,hy+18*sc)],(240,236,220))
    for k in range(5): d.P([(hx-8*sc+k*4*sc,hy+25*sc),(hx-5*sc+k*4*sc,hy+25*sc),(hx-6.5*sc+k*4*sc,hy+19.5*sc)],(240,236,220))
    ln=(18+6*math.sin(t*5))*sc; w=math.sin(t*4)*2*sc
    d.P([(hx-5*sc,hy+21*sc),(hx+5*sc,hy+21*sc),(hx+4*sc+w,hy+21*sc+ln),(hx+w,hy+24*sc+ln),(hx-4*sc+w,hy+21*sc+ln)],(190,30,44,255)); d.L(hx+w*.5,hy+22*sc,hx+w,hy+20*sc+ln,(130,16,26,255),1.2*sc)
    d.P([(hx-16*sc,hy+16*sc),(hx+16*sc,hy+16*sc),(hx+9*sc,hy+40*sc),(hx,hy+46*sc),(hx-9*sc,hy+40*sc)],(40,30,26,235))
def kdeco(d,hx,hy,sc):
    for sg in(-1,1):
        _horn(d,hx,hy,sc,sg)
        d.P([(hx+sg*19*sc,hy-4*sc),(hx+sg*36*sc,hy-16*sc),(hx+sg*20*sc,hy+7*sc)],(96,78,68,255)); d.P([(hx+sg*21*sc,hy-3*sc),(hx+sg*31*sc,hy-11*sc),(hx+sg*21*sc,hy+3*sc)],(150,100,96,255))
    rnd_=random.Random(5)
    for i in range(70):
        x=hx+(rnd_.random()-.5)*74*sc; y=hy+(38+rnd_.random()*92)*sc; l=(7+rnd_.random()*8)*sc; a=1.57+(rnd_.random()-.5)*.8
        d.L(x,y,x+math.cos(a)*l*.35,y+math.sin(a)*l,(26,18,14,210),1.7*sc)
def basket_back(d,hx,hy,sc):
    x0,y0,x1,y1=hx-34*sc,hy+26*sc,hx+34*sc,hy+112*sc
    d.R(x0,y0,x1,y1,(126,88,50,255),8*sc)
    for k in range(9): d.L(x0,y0+k*10*sc,x1,y0+k*10*sc,(88,58,32,255),1.4*sc)
    for k in range(7): d.L(x0+k*11*sc,y0,x0+k*11*sc,y1,(150,108,64,255),1.4*sc)
    d.R(x0,y0,x1,y0+6*sc,(96,66,38,255),3*sc)
def rods_prop(dd,x,y,a,s,K=1.0):
    for i in range(11):
        ang=(i-5)*.075; ex=x+math.sin(ang)*108*K; ey=y-math.cos(ang)*108*K-6*K
        dd.L(x,y,ex,ey,(206,182,142,255),1.7*K)
        for q in range(3): bx=x+math.sin(ang)*(60+q*16)*K; by=y-math.cos(ang)*(60+q*16)*K; dd.L(bx,by,bx+math.sin(ang+.6)*14*K,by-math.cos(ang+.6)*14*K,(190,166,128,255),1.1*K)
    dd.R(x-6*K,y-6*K,x+6*K,y+8*K,(150,40,40,255),2*K)
def chain_prop(dd,x,y,a,s,K=1.0):
    t=KT[0]; px,py=x,y+6*K
    for i in range(10):
        nx=x+math.sin(t*2.6+i*.45)*(i*1.7)*K; ny=y+(6+i*10.5)*K
        dd.E((px+nx)/2,(py+ny)/2,3.6*K,(5.8 if i%2==0 else 3.2)*K,None,(150,152,160,255),max(1.0,1.6*K)); px,py=nx,ny
    dd.E(px,py+9*K,9*K,9*K,(236,190,60,255)); dd.E(px-2.5*K,py+6*K,3*K,3*K,(255,240,170,200)); dd.R(px-1.4*K,py+12*K,px+1.4*K,py+17*K,(60,40,10,255),1)
def torch_prop(dd,x,y,a,s,K=1.0):
    t=KT[0]; dd.R(x-3.5*K,y-70*K,x+3.5*K,y+14*K,(96,64,36,255),2*K); fl=math.sin(t*14+x)*3*K
    dd.E(x,y-84*K,15*K,22*K,(255,120,30,60)); dd.E(x,y-84*K,26*K,38*K,(255,150,40,26)); dd.E(x,y-84*K,46*K,60*K,(255,140,40,14))
    dd.P([(x-10*K,y-72*K),(x-6*K+fl,y-100*K),(x+fl,y-116*K),(x+6*K+fl,y-98*K),(x+10*K,y-72*K)],(255,140,30,255)); dd.P([(x-5*K,y-72*K),(x+fl*.5,y-100*K),(x+5*K,y-72*K)],(255,224,110,255))
def mitre_deco(d,hx,hy,sc):
    d.P([(hx-22*sc,hy-18*sc),(hx-10*sc,hy-62*sc),(hx+10*sc,hy-62*sc),(hx+22*sc,hy-18*sc)],(200,30,44,255))
    d.P([(hx-22*sc,hy-18*sc),(hx-10*sc,hy-62*sc),(hx,hy-50*sc)],(222,50,60,255)); d.R(hx-23*sc,hy-24*sc,hx+23*sc,hy-16*sc,(240,200,70,255),2*sc)
    d.R(hx-2*sc,hy-52*sc,hx+2*sc,hy-34*sc,(240,200,70,255),1); d.R(hx-8*sc,hy-44*sc,hx+8*sc,hy-40*sc,(240,200,70,255),1)
    d.L(hx-4*sc,hy-18*sc,hx-8*sc,hy+12*sc,(240,200,70,255),2*sc); d.L(hx+4*sc,hy-18*sc,hx+8*sc,hy+12*sc,(240,200,70,255),2*sc)
def crozier_prop(dd,x,y,a,s,K=1.0):
    dd.L(x,y+90*K,x,y-130*K,(224,182,60,255),5*K); dd.A(x+14*K,y-132*K,16*K,16*K,90,330,(224,182,60,255),5*K); dd.E(x+28*K,y-124*K,5*K,5*K,(224,182,60,255))
    dd.L(x,y-50*K,x,y-44*K,(180,30,40,255),9*K)
def gift_prop(dd,x,y,a,s,K=1.0):
    dd.R(x-16*K,y-6*K,x+16*K,y+26*K,(60,120,190,255),3*K); dd.R(x-3*K,y-6*K,x+3*K,y+26*K,(240,210,80,255),0); dd.R(x-16*K,y+8*K,x+16*K,y+13*K,(240,210,80,255),0)
    dd.P([(x,y-6*K),(x-10*K,y-16*K),(x-2*K,y-8*K)],(240,210,80,255)); dd.P([(x,y-6*K),(x+10*K,y-16*K),(x+2*K,y-8*K)],(240,210,80,255))
def woodmask(d,hx,hy,sc,col=(150,100,58)):
    d.E(hx,hy+2*sc,22*sc,27*sc,col+(255,))
    for k in range(7): d.A(hx,hy+2*sc,(6+k*3.2)*sc,(10+k*3.4)*sc,200,340,(104,66,36,150),1.2*sc)
    d.P([(hx-20*sc,hy-8*sc),(hx,hy-3*sc),(hx+20*sc,hy-8*sc),(hx+15*sc,hy-16*sc),(hx,hy-11*sc),(hx-15*sc,hy-16*sc)],(60,36,20,255))
    for sg in(-1,1): d.E(hx+sg*9*sc,hy-3*sc,5*sc,3.6*sc,(14,8,6,255)); d.E(hx+sg*9*sc,hy-3*sc,1.8*sc,1.8*sc,(255,180,60,255))
    d.P([(hx-3*sc,hy),(hx+3*sc,hy),(hx+6*sc,hy+10*sc),(hx-6*sc,hy+10*sc)],shade(col,.8)+(255,))
    d.P([(hx-14*sc,hy+13*sc),(hx+14*sc,hy+13*sc),(hx+11*sc,hy+25*sc),(hx-11*sc,hy+25*sc)],(80,18,16,255))
    for sg in(-1,1): d.P([(hx+sg*10*sc,hy+13*sc),(hx+sg*14*sc,hy+13*sc),(hx+sg*13*sc,hy+3*sc)],(236,228,200));
    for k in range(5): d.R(hx-9*sc+k*4*sc,hy+13*sc,hx-7*sc+k*4*sc,hy+17*sc,(236,228,200,255),0)
    d.P([(hx-5*sc,hy+22*sc),(hx+5*sc,hy+22*sc),(hx+3*sc,hy+36*sc+math.sin(KT[0]*4)*2*sc),(hx-3*sc,hy+36*sc)],(196,36,40,255))
def rdeco(col):
    def f(d,hx,hy,sc):
        for sg in(-1,1): _horn(d,hx,hy,sc,sg,col=col,L=.8,curl=.9)
        rnd_=random.Random(int(hx)%97)
        for i in range(60):
            x=hx+(rnd_.random()-.5)*72*sc; y=hy+(38+rnd_.random()*90)*sc; l=(7+rnd_.random()*8)*sc
            d.L(x,y,x+(rnd_.random()-.5)*3*sc,y+l,(40,28,20,210),1.8*sc)
    return f
KR=dict(skin=(86,70,62),hair=(34,28,24),hairstyle="short",shirt=(52,40,34),pants=(58,44,36),shoes=(22,16,14),sleeve="long",claws=True,tail=(52,40,34),bulk=1.3,height=1.1,face=False,ear=False,hands_col=(72,58,50),belt=(140,140,150),neck_col=(60,48,42),mask=krampus_face)
NIC=dict(skin=(236,196,160),hair=(240,240,244),hairstyle="short",beard=True,shirt=(190,28,44),dress=True,skirt_col=(176,24,40),sleeve="long",shoes=(60,40,30),brow=(210,210,214),glasses=False)
KIDA=dict(skin=(236,196,160),hair=(150,100,50),hairstyle="short",shirt=(70,110,170),pants=(60,62,90),shoes=(60,40,30),sleeve="long",hat="cap",cap_col=(200,60,60))
KIDB=dict(skin=(240,204,170),hair=(120,70,40),hairstyle="braid",shirt=(160,60,90),dress=True,skirt_col=(120,50,80),sleeve="long",shoes=(50,34,30),hat="hood")
def runner(col,fur,horn):
    return dict(skin=(150,100,58),hair=fur,hairstyle="short",shirt=fur,pants=shade(fur,.8),shoes=(24,18,14),sleeve="long",claws=False,tail=fur,bulk=1.25,height=1.08,face=False,ear=False,mask=lambda d,hx,hy,sc: woodmask(d,hx,hy,sc,col),hands_col=(60,44,34),belt=(150,150,158))
