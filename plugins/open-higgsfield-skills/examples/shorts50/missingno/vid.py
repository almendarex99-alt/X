import sys; sys.path.insert(0,"..")
from kit import *
from rooms import mk, render_room
from terrain import render_terrain, mk as tmk
from sets import *
import nes
BED=mk(H=2.5,hw=2.2,zend=3.0,zback=-3.0,wall="plaster",wcol=(150,170,200),wcol2=(110,120,140),floor="carpet",fcol=(96,86,110),ceil="plaster",ccol=(190,190,200),ambient=.05,amb_rgb=(.6,.7,1.0),fog=.01,fov=52)
STORE=mk(H=2.7,hw=2.6,zend=4.0,zback=-3.0,wall="plaster",wcol=(236,230,220),floor="tile",fcol=(176,172,160),ceil="tile",ccol=(224,222,214),ambient=.20,amb_rgb=(1,.98,.94),fog=.008,fov=54,
        plights=dict(gap=2.0,off=0,xs=(-1.0,1.0),y=2.55,rgb=(1,.97,.9),I=.28,k=.5))
KID=dict(skin=(234,196,160),hair=(40,30,24),hairstyle="short",shirt=(220,200,60),pants=(60,70,110),sleeve="short")
KIDB=dict(skin=(226,180,140),hair=(20,16,14),hairstyle="short",shirt=(60,120,200),pants=(80,80,90),sleeve="short",hat="cap",cap_col=(200,50,50))
KIDC=dict(skin=(240,204,170),hair=(150,90,40),hairstyle="ponytail",shirt=(200,70,110),pants=(70,70,100),sleeve="short")
CLERK=dict(skin=(232,196,160),hair=(30,24,20),hairstyle="short",shirt=(40,100,170),coat=(40,100,170),pants=(50,50,60),sleeve="long",glasses=False)
GBG=(160,160,150)
def gb_prop(d,cx,cy,sc,tex=None,glow_=True,back=False):
    w=34*sc; h=56*sc
    d.R(cx-w/2,cy-h/2,cx+w/2,cy+h/2,GBG+(255,),5*sc); d.R(cx-w/2,cy-h/2,cx+w/2,cy-h/2+4*sc,(255,255,255,70),4*sc)
    if not back:
        d.R(cx-w*.42,cy-h*.44,cx+w*.42,cy-h*.02,(70,70,84,255),3*sc)
        if tex is not None: d.im.paste(tex.resize((int(w*.78*3),int(h*.38*3)),Image.NEAREST),(int((cx-w*.39)*3),int((cy-h*.42)*3)))
        d.E(cx-w*.28,cy+h*.2,5*sc,5*sc,(70,50,100,255)); d.R(cx-w*.4,cy+h*.1,cx-w*.16,cy+h*.14,(60,60,70,255),1); d.R(cx-w*.3,cy,cx-w*.26,cy+h*.28,(60,60,70,255),1)
        d.E(cx+w*.28,cy+h*.18,3.6*sc,3.6*sc,(160,30,70,255)); d.E(cx+w*.14,cy+h*.26,3.6*sc,3.6*sc,(160,30,70,255))
    else:
        for k in range(6): d.L(cx-w*.3,cy-h*.2+k*4*sc,cx+w*.3,cy-h*.2+k*4*sc,(130,130,122,255),1)
def bedroom(cam,u,glow_rgb=(.35,.8,.35),gi=.6):
    st=BED; bg=render_room(cam,st,u,1.0,extra=[(0,1.1,.1,glow_rgb,.9*gi),(-1.6,.7,2.2,(1,.7,.4),.5)]); back=new_ov(); front=new_ov()
    sidewindow(back,cam,st,-2.19,.8,2.0,night=True,curt=(60,80,150)); tquad(back,cam,st,(.6,2.0,2.99),(1.6,2.0,2.99),(1.6,1.0,2.99),(.6,1.0,2.99),tex_poster(seed=9,col=(30,90,150)))
    tquad(back,cam,st,(-1.2,1.9,2.99),(-.4,1.9,2.99),(-.4,1.1,2.99),(-1.2,1.1,2.99),tex_poster(seed=11,col=(180,60,40)))
    box(back,cam,st,-1.0,1.0,0,.45,1.4,3.0,(70,90,140)); box(back,cam,st,-1.0,1.0,.45,.52,1.4,3.0,(110,120,170)); box(back,cam,st,-1.0,1.0,.45,1.0,2.9,3.0,(96,70,50))
    box(back,cam,st,1.3,2.1,0,.75,1.9,2.9,(130,96,64)); lamp(back,cam,st,1.7,2.4,h=1.2,col=(255,200,140))
    return st,bg,back,front
def sceneA(u,final=False):
    t=u+(0 if not final else 3); p=sm(clamp(t/6))
    cam=dict(x=lerp(.25,0.0,p),y=lerp(1.45,1.2,p),z=lerp(-.7,.35,p),yaw=.02*math.sin(t*.5),pitch=lerp(.16,.05,p))
    st,bg,back,front=bedroom(cam,t,gi=.55+.1*math.sin(t*4)); big=fin(composite(bg,back)); d=D(big)
    o=P3(d,cam,st,0,1.35,KID,dict(P_both(t,l=(.55,1.9),r=(.55,1.9)),mouth=.0,look=(0,.2)),hm=1.2,u=t,y0=.3,bust=True,tone=1.0,fog=(14,20,40))
    if o:
        cx=(o["hand_l"][0]+o["hand_r"][0])/2; cy=(o["hand_l"][1]+o["hand_r"][1])/2; sc=place3(cam,st,0,1.35,1.2,.3)[2]
        gb_prop(d,cx,cy-8*sc,sc*1.15,back=True)
        hx,hy=o["head"]; 
        for k in range(5): d.E(hx,hy+6*sc,(46+k*18)*sc,(54+k*18)*sc,(110,230,110,int(22/(1+k*.4))))
    big=composite(big,front.resize(OUTSZ,Image.BICUBIC)); return grade(big,sat=.95,seed=int(u*30),tint=(.95,1.02,1.0))
def sceneB(u):
    cam=dict(x=lerp(-.8,.3,sm(u/9)),y=1.4,z=lerp(-1.0,.1,sm(u/9)),yaw=lerp(.25,.0,sm(u/9)),pitch=.05); st=STORE
    bg=render_room(cam,st,u,1.0,extra=[(0,1.2,3.0,(1,.9,.8),.5)]); back=new_ov(); front=new_ov()
    tquad(back,cam,st,(-2.5,2.4,3.99),(-.4,2.4,3.99),(-.4,.4,3.99),(-2.5,.4,3.99),tex_carts(seed=3)); tquad(back,cam,st,(.4,2.4,3.99),(2.5,2.4,3.99),(2.5,.4,3.99),(.4,.4,3.99),tex_carts(seed=8))
    box(back,cam,st,-2.5,2.5,0,.4,3.7,4.0,(90,66,46))
    box(back,cam,st,-1.0,1.0,0,1.0,1.6,2.4,(150,110,70)); box(back,cam,st,-.3,.3,1.0,1.3,1.8,2.2,(60,60,70))
    # bandera de Japon y farolillos
    fl=Image.new("RGB",(150,100),(246,246,246)); ImageDraw.Draw(fl).ellipse([45,20,105,80],fill=(200,30,50)); tquad(back,cam,st,(1.4,2.5,3.98),(2.2,2.5,3.98),(2.2,2.0,3.98),(1.4,2.0,3.98),fl)
    for x in (-1.8,-.6,.6,1.8): box(back,cam,st,x-.14,x+.14,2.0,2.3,1.2,1.5,(210,40,40),emis=.5,shadow=False); glow(back,cam,st,(x,2.15,1.35),(255,80,60),.5,60,4)
    def pp(d):
        P3(d,cam,st,-1.7,2.6,KIDB,dict(P_idle(u),al=(1.0,2.0),curlL=.6),hm=1.4,u=u)
        P3(d,cam,st,.5,3.1,CLERK,dict(P_talk(u),al=(.9,1.6)),hm=1.75,u=u)
        P3(d,cam,st,1.6,2.7,KIDC,dict(P_point(u,dirx=-1),ar=(1.4,1.5)),hm=1.4,u=u)
    big=fin(composite(bg,back)); d=D(big); pp(d); big=composite(big,front.resize(OUTSZ,Image.BICUBIC)); return grade(big,seed=int(u*30),tint=(1.0,.98,.95))
def gb_macro(u,texfn,seed=0,title=None):
    cam=dict(x=0,y=1.2,z=-.5+.1*sm(u/6),yaw=0,pitch=.05); st=dict(BED,fov=48)
    st_,bg,back,front=bedroom(cam,u,gi=1.0); bg=render_room(cam,st,u,1.0,extra=[(0,1.2,0.4,(.35,.8,.35),.8),(-1.0,1.0,1.5,(1,.7,.4),.6)])
    tex=crt(texfn(u),1.0,int(u*30)) if False else texfn(u)
    big=fin(composite(bg,back)); d=D(big)
    cx,cy=270,430; w=250; h=int(w*1.6); sc=w/34
    gb_prop(d,cx,cy,sc,tex=None,back=False); big.paste(tex.resize((int(w*.78*3),int(h*.5*3*.7)),Image.NEAREST),(int((cx-w*.39)*3),int((cy-h*.42)*3))) if False else None
    # pantalla grande
    sw,sh=int(w*.78),int(w*.78*144/160); sx0,sy0=cx-sw/2,cy-h*.42
    d2=D(big); scr=tex.resize((int(sw*3),int(sh*3)),Image.NEAREST); big.paste(scr,(int(sx0*3),int(sy0*3)))
    big=big; d=D(big)
    # manos con los pulgares sobre los botones
    o1=hand(d,cx-w*.5,cy+h*.26,3.0,-1,2.2,(236,190,150),curl=.8,spread=.4); o2=hand(d,cx+w*.5,cy+h*.26,3.0,1,2.2,(236,190,150),curl=.8,spread=.4)
    return big
def sceneC(u): return grade(gb_macro(u,nes.gb_overworld),seed=int(u*30),tint=(.95,1.03,1.0))
def sceneD(u): return grade(gb_macro(u,nes.gb_dex if u<3 else nes.gb_glitch),seed=int(u*30),tint=(.95,1.03,1.0))
def sceneE(u): return grade(gb_macro(u,nes.gb_items),seed=int(u*30),tint=(.95,1.03,1.0))
def sceneF(u):
    st=tmk(fov=54,ground="asphalt",sky="day",fog=.01,fogcol=(206,224,246),hills=.02,hcol=(110,140,120),amb=(1,1,1),ambient=1.0)
    cam=dict(x=-.6*math.sin(u*.5),y=1.3,z=-.5*math.cos(u*.5),yaw=.25*math.sin(u*.5),pitch=.04)
    bg=render_terrain(cam,st,u); ov=new_ov()
    box(ov,cam,st,-14,14,0,6,16,22,(200,180,150)); 
    for k in range(7): tquad(ov,cam,st,(-12+k*3.6,4.8,15.99),(-10.5+k*3.6,4.8,15.99),(-10.5+k*3.6,3.0,15.99),(-12+k*3.6,3.0,15.99),Image.new("RGB",(60,60),(120,170,210)))
    for k in range(7): tquad(ov,cam,st,(-12+k*3.6,2.4,15.99),(-10.5+k*3.6,2.4,15.99),(-10.5+k*3.6,.8,15.99),(-12+k*3.6,.8,15.99),Image.new("RGB",(60,60),(120,170,210)))
    box(ov,cam,st,-14,14,0,1.0,10.0,10.12,(90,100,96),shadow=False)
    big=fin(composite(bg,ov)); d=D(big)
    spots=[(-1.4,4.2,KIDB),(1.4,4.2,KIDC),(-.5,5.6,KID),(.5,3.4,dict(KID,shirt=(60,160,90))),(2.2,5.0,dict(KIDB,shirt=(190,80,60)))]
    spots.sort(key=lambda r:-r[1])
    for k,(x,z,stl) in enumerate(spots):
        po=dict(P_point(u,k),ar=(1.0,2.2)) if k%2==0 else dict(P_talk(u,k),al=(.9,2.0))
        P3(d,cam,st,x,z,stl,po,hm=1.4,u=u,fog=(150,170,190))
    return grade(big,sat=1.0,seed=int(u*30),tint=(1.0,1.0,1.0))
def sceneG(u):
    cam=dict(x=-.5*math.sin(u*.5),y=1.3,z=-.9+.4*math.sin(u*.3),yaw=.12*math.sin(u*.5),pitch=.1)
    st,bg,back,front=bedroom(cam,u,glow_rgb=(.45,.9,.45),gi=.8)
    big=fin(composite(bg,back)); d=D(big)
    o=P3(d,cam,st,0,1.35,KID,dict(P_both(u,l=(.55,1.9),r=(.55,1.9)),mouth=.0,look=(0,.2)),hm=1.2,u=u,y0=.3,bust=True,fog=(14,20,40))
    big=composite(big,front.resize(OUTSZ,Image.BICUBIC))
    if int(u*3)%3==0:
        a=np.array(big); rng=np.random.default_rng(int(u*30))
        for _ in range(10):
            y=int(rng.integers(0,2700)); hh=int(rng.integers(20,100)); a[y:y+hh]=np.roll(a[y:y+hh],int(rng.integers(-120,120)),axis=1)
        big=Image.fromarray(a)
    return grade(big,seed=int(u*30),tint=(.95,1.03,1.0))
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur): return 1.0,270,480
core.CAM=cam
if __name__=="__main__": core.main()
