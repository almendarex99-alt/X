import sys; sys.path.insert(0,"..")
from art import *
from common import tv
def photo(d,x,y,w,h,u,k=0):
    d.R(x-6,y-6,x+w+6,y+h+6,(236,232,220),3)
    for kk in range(12): d.R(x,y+kk*h/12,x+w,y+(kk+1)*h/12+1,mixc((150,136,112),(88,76,60),kk/11.0),0)
    for i in range(7):
        tx=x+10+i*w/6.5; d.P([(tx-8,y+h),(tx+8,y+h),(tx+5,y),(tx-5,y)],(40,34,28,140))
    for i,(fx) in enumerate([x+w*.22,x+w*.42,x+w*.62]):
        silhouette(d,fx,y+h-6,.22,(40,34,28),arms=False)
    tallman(d,x+w*.84,y+h-8,.24,u,(20,18,18))
    d.R(x,y,x+w,y+h,(255,240,200,18),0)
def paper(d,x,y,sc,u,glow=1.0):
    d.E(x,y,34*sc,34*sc,(255,255,255,int(34*glow)))
    d.R(x-14*sc,y-18*sc,x+14*sc,y+18*sc,(244,242,230),1.5*sc); 
    for k in range(4): d.L(x-9*sc,y-10*sc+k*7*sc,x+9*sc,y-10*sc+k*7*sc,(40,40,40,150),1.4*sc)
def sceneA(u,final=False):
    im=new((12,18,30),(30,38,56)); d=D(im)
    forest(d,u,sky=(24,36,66),sky2=(84,106,142),ground=(16,24,20),fog=(170,190,210),dense=15)
    tallman(d,300+math.sin(u*.5)*4,640,.7+.05*u,u,(8,8,12))
    fogband(d,u,520,760,(160,176,192),34)
    flashlight(d,160,880,320,560,.3,560,70)
    return im
def sceneB(u):
    im=new((20,22,30),(34,36,48)); d=D(im)
    d.R(20,40,520,920,(30,32,44),16); d.R(20,40,520,96,(48,50,68),16)
    for k in range(3): d.E(50+k*26,68,7,7,[(255,90,90),(255,200,70),(90,220,110)][k])
    d.R(150,52,490,84,(20,22,32),10)
    # lista de mensajes del foro con dos fotos
    for k in range(4): d.R(40,120+k*40,500,150+k*40,(40,44,60,200 if k else 255),6)
    photo(d,56,300,200,150,u); photo(d,288,300,200,150,u+1)
    for k in range(5): d.R(56,480+k*30,300+k*30,500+k*30,(60,64,84),5)
    # cursor
    cx,cy=380+math.sin(u*1.2)*50,520+math.cos(u*.9)*30
    d.P([(cx,cy),(cx+16,cy+22),(cx+6,cy+22),(cx,cy+34)],(250,250,250))
    for k in range(3): d.R(56,700+k*60,480,730+k*60,(40,44,60,200),6)
    return im
def sceneC(u):
    im=new((10,12,24),(24,18,44)); d=D(im); stars(d,u,40,300)
    cx,cy=270,430
    # foto central y red de creaciones que se propagan
    n=int(clamp(u/5.0)*18)+2
    for k in range(n):
        a=k*2.4+u*.1; r=70+ (k%6)*38+ (k//6)*22; x=cx+math.cos(a)*r*1.05; y=cy+math.sin(a)*r*1.35
        t=sm((u-k*.22)/.5)
        d.L(cx,cy,x,y,(255,255,255,int(50*t)),2)
        col=[(240,200,90),(90,170,240),(240,110,150),(110,220,150)][k%4]
        d.R(x-18*t,y-14*t,x+18*t,y+14*t,col+(int(255*t),),4)
        if k%4==0: d.P([(x-5*t,y-7*t),(x-5*t,y+7*t),(x+8*t,y)],(255,255,255,int(255*t)))
        elif k%4==1: d.L(x-9*t,y-5*t,x+9*t,y-5*t,(40,40,50),2); d.L(x-9*t,y+1*t,x+6*t,y+1*t,(40,40,50),2)
        elif k%4==2: d.A(x,y,8*t,8*t,200,520,(40,40,50),2)
    photo(d,cx-70,cy-50,140,100,u)
    return im
def sceneD(u):
    im=new((22,20,34),(48,40,58)); d=D(im)
    d.R(0,690,540,960,(40,30,40)); bevel(d,16,640,524,700,(116,78,56),6)
    def scr(d_,x0,y0,x1,y1):
        d_.R(x0,y0,x1,y1,(6,10,14)); 
        for k in range(5):
            x=x0+10+k*(x1-x0)/5; d_.P([(x-6,y1),(x+6,y1),(x+3,y0+10),(x-3,y0+10)],(18,26,22))
        flashlight(d_,(x0+x1)/2,y1-6,(x0+x1)/2+20,y0+30,.3,(y1-y0)*.9,90); tallman(d_,x0+(x1-x0)*.72,y1-30,.16,u,(8,8,12))
        paper(d_,x0+40,y0+50,.5,u)
    box=crt(d,150,400,240,214,(2,8,10),(190,182,158)); scr(d,*box); crt_fx(d,box)
    keyboard(d,190,664,160,30); person_back(d,270,742,1.45,1,u)
    d.R(40,120,200,290,(244,240,230),6); d.R(40,120,200,150,(200,50,60),6)
    for r in range(3):
        for c in range(4): d.R(52+c*34,164+r*38,76+c*34,190+r*38,(210,210,220) if (r*4+c)!=int(u*1.2)%12 else (255,210,80),2)
    return im
def sceneE(u):
    im=new((12,18,30),(30,38,56)); d=D(im)
    forest(d,u,sky=(24,36,66),sky2=(84,106,142),ground=(16,24,20),fog=(170,190,210),dense=16)
    got=min(8,int(u/.8))
    spots=[(80,640),(190,600),(300,660),(410,620),(120,700),(250,730),(380,720),(470,670)]
    for k,(x,y) in enumerate(spots):
        if k>=got: paper(d,x,y-60,1.2,u)
    near=clamp(u/7.0)
    tallman(d,380-near*80,600+near*60,lerp(.6,1.1,near),u,(8,8,12))
    fogband(d,u,500,800,(150,170,190),30)
    flashlight(d,270,940,270+math.sin(u*.8)*160,560,.34,640,90)
    for k in range(8): d.R(24+k*26,24,44+k*26,52,(244,242,230) if k<got else (255,255,255,40),3)
    return im
def sceneF(u):
    im=new((8,10,16),(20,24,34)); d=D(im)
    forest(d,u,sky=(18,26,48),sky2=(60,80,112),ground=(12,18,16),fog=(150,170,190),dense=14,moon=False)
    s=lerp(.9,2.6,sm(u/5.0)); tallman(d,270+math.sin(u*30)*(s-1)*3,760+s*40,s,u,(6,6,10))
    fogband(d,u,500,800,(150,170,190),28)
    flashlight(d,270,940,270,520,.3,640,80)
    st=sm(u/5.0); noise_static(d,0,0,540,960,u,int(30+220*st*st),8)
    d.R(0,0,540,960,(255,255,255,int(20*abs(math.sin(u*20))*st)),0)
    return im
def sceneG(u):
    im=new((14,10,26),(34,22,54)); d=D(im); stars(d,u,70,500)
    for k in range(5): d.E(270,560,90+k*50+((u*40)%50),90+k*50+((u*40)%50),None,(255,255,255,int(80*(1-(k+((u*40)%50)/50)/5))),3)
    tallman(d,270,760,1.9+.05*math.sin(u*2),u,(6,6,10))
    for k in range(22): a=k*.29+u*.3; d.E(270+math.cos(a)*260,430+math.sin(a)*330,3,3,(255,255,255,140))
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx==0: return 1.0+.35*sm(p),300,560
    if idx==1: return 1.0+.12*sm(p),270,500
    if idx==2: return 1.0+.1*sm(p),270,470
    if idx==3: return 1.0+.5*sm(p),270,520
    if idx==4: return 1.0+.2*sm(p),270,560
    if idx==5: return 1.0+.1*sm(p),270,500
    if idx==6: return 1.3-.3*sm(p),270,520
    return 1.4-.4*sm(p),300,560
core.CAM=cam
if __name__=="__main__": core.main()
