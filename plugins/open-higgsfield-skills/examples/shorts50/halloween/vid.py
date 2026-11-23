import sys; sys.path.insert(0,"..")
from kit import *
from rooms import mk, render_room
from terrain import render_terrain, mk as tmk
from sets import *
SUB=tmk(fov=54,ground="street",sky="night",fog=.016,fogcol=(26,26,44),hills=.03,hcol=(20,20,36),amb=(.30,.34,.52),ambient=1.0)
SHOP=mk(H=2.7,hw=2.8,zend=4.6,zback=-3.0,wall="plaster",wcol=(210,196,170),floor="wood",fcol=(120,86,56),ceil="plaster",ccol=(200,190,170),ambient=.24,amb_rgb=(1,.9,.76),fog=.01,fov=52,
         plights=dict(gap=3,off=1,xs=(0,),y=2.55,rgb=(1,.86,.62),I=.6,k=.5))
def whitemask(d,hx,hy,sc,paint=1.0):
    d.E(hx,hy+2*sc,22*sc,26*sc,(236,236,232,255)); d.E(hx-7*sc,hy-8*sc,9*sc,12*sc,(255,255,255,40))
    for sg in(-1,1): d.E(hx+sg*8.6*sc,hy-3*sc,5.2*sc,5.6*sc,(8,8,10,255))
    d.P([(hx-2*sc,hy),(hx+2*sc,hy),(hx+4*sc,hy+9*sc),(hx-4*sc,hy+9*sc)],(214,214,210,255)); d.R(hx-8*sc,hy+16*sc,hx+8*sc,hy+17.5*sc,(190,190,188,255),0)
def hair_deco(d,hx,hy,sc):
    rnd_=random.Random(3)
    for i in range(36):
        a=3.14+rnd_.random()*3.14; r=(20+rnd_.random()*10)*sc; d.L(hx+math.cos(a)*18*sc,hy-4*sc+math.sin(a)*22*sc,hx+math.cos(a)*r*1.2,hy-4*sc+math.sin(a)*r*1.4,(60,40,24,255),2.2*sc)
import random
BAD=dict(skin=(236,236,232),hair=(60,40,24),hairstyle="short",shirt=(48,56,84),pants=(48,56,84),shoes=(24,24,28),sleeve="long",face=False,ear=False,mask=whitemask,belt=(40,36,30),bulk=1.12,height=1.08,hands_col=(214,196,176),neck_col=(48,56,84),brow=(60,40,24))
CREW=dict(skin=(226,184,150),hair=(40,30,24),hairstyle="short",shirt=(80,100,90),pants=(60,64,80),sleeve="long",coat=(70,80,70))
DIR=dict(skin=(230,190,156),hair=(70,56,40),hairstyle="short",beard=True,hat="cap",cap_col=(40,50,60),shirt=(150,70,60),coat=(40,44,56),pants=(60,60,70),sleeve="long")
CLERK=dict(skin=(238,200,164),hair=(190,150,80),hairstyle="long",shirt=(200,70,100),pants=(60,60,70),sleeve="short")
BUYER=dict(skin=(214,170,130),hair=(30,24,20),hairstyle="short",beard=True,shirt=(70,110,90),coat=(60,70,60),pants=(60,60,80),sleeve="long")
PROD=dict(skin=(226,184,150),hair=(200,200,200),hairstyle="short",shirt=(240,240,244),coat=(30,30,50),pants=(30,30,50),sleeve="long")
def street_scene(cam,t,st=SUB,figure=None,lamp_z=(8,22,36)):
    ex=[(3.8 if k%2==0 else -3.8,3.0,z,(1.0,.66,.34),3.0) for k,z in enumerate(lamp_z)]+[(-7,.5,z+3,(1.0,.5,.1),1.0) for z in (14,30)]
    bg=render_terrain(cam,st,t,extra=ex); ov=new_ov()
    for k,z in enumerate((14,28,42,56)):
        house(ov,cam,st,-9.5,z,seed=k+1,t=t); house(ov,cam,st,9.5,z+7,seed=k+9,t=t,wall=(170,160,140))
    for k,z in enumerate(lamp_z):
        x=3.8 if k%2==0 else -3.8; box(ov,cam,st,x-.06,x+.06,0,3.0,z-.06,z+.06,(30,30,34),shadow=False); glow(ov,cam,st,(x,3.0,z),(255,190,110),1.0,90,6)
    for (x,z) in ((-6.5,13),(-7.2,27),(6.8,20),(7.4,34)): 
        box(ov,cam,st,x-.22,x+.22,0,.42,z-.22,z+.22,(240,120,30),emis=.4,shadow=False); glow(ov,cam,st,(x,.25,z),(255,140,40),.5,100,4)
    for (x,z) in ((-11,10),(11,24),(-11,38)): 
        box(ov,cam,st,x-.2,x+.2,0,5,z-.2,z+.2,(30,24,20),shadow=False)
        for q in range(4): poly3(ov,cam,st,[(x,5,z),(x+(q-1.5)*1.6,6.4+q%2,z),(x+(q-1.5)*1.7,6.5+q%2,z+.1)],(30,24,20))
    return bg,ov
def sceneA(u,final=False):
    t=u+(0 if not final else 3); cam=dict(x=.3*math.sin(t*.4),y=1.55,z=lerp(0,3.0,sm(t/9)),yaw=.0,pitch=.05)
    bg,ov=street_scene(cam,t); big=fin(composite(bg,ov)); d=D(big)
    dist=lerp(13,6.5,sm(t/8)); P3(d,cam,SUB,.8,cam["z"]+dist,BAD,dict(P_idle(t),tilt=.12*math.sin(t*.7),ar=(.12,.2),al=(.12,.2)),hm=1.9,u=t,deco=hair_deco,fog=(26,26,44),tone=.9)
    big=snow_particles(big,t,n=60,col=(224,130,40),sz=3,speed=40,alpha=190,scale=2.4)
    return grade(vign_(big,.5),sat=.95,seed=int(u*30),tint=(.98,.98,1.04))
def vign_(img,k=.6): return Image.alpha_composite(img.convert("RGBA"),vignette_ov(img.size,k)).convert("RGB")
def sceneB(u):
    cam=dict(x=lerp(-2.5,.5,sm(u/6)),y=1.45,z=lerp(0,.8,sm(u/6)),yaw=lerp(.2,.0,sm(u/6)),pitch=.04)
    bg,ov=street_scene(cam,u+4)
    # camara de cine sobre carril, focos grandes y claqueta
    for k in range(5): box(ov,cam,SUB,-.1,.1,0,.05,5+k*1.0,5+k*1.0+.8,(60,60,64),shadow=False)
    box(ov,cam,SUB,-.5,.5,.5,1.1,5.3,5.9,(40,42,46)); box(ov,cam,SUB,-.2,.2,.6,.95,4.9,5.3,(30,30,34)); box(ov,cam,SUB,-.35,.35,0,.5,5.4,5.8,(70,70,74))
    for (x,z) in ((-3.5,7),(3.5,9)):
        box(ov,cam,SUB,x-.5,x+.5,2.0,3.0,z,z+.4,(220,224,230),emis=.6,shadow=False); box(ov,cam,SUB,x-.04,x+.04,0,2.0,z+.15,z+.25,(40,40,44),shadow=False); glow(ov,cam,SUB,(x,2.5,z-.2),(255,250,230),2.0,100,7)
    big=fin(composite(bg,ov)); d=D(big)
    P3(d,cam,SUB,-1.2,6.4,DIR,dict(P_point(u,dirx=1),ar=(1.45,1.6),mouth=.5),hm=1.78,u=u,fog=(26,26,44)); P3(d,cam,SUB,1.3,5.8,CREW,dict(P_hold(u,r=(1.4,1.8)),mouth=.2),hm=1.75,u=u,fog=(26,26,44))
    P3(d,cam,SUB,2.5,6.9,CREW,dict(P_walk(u,2.0)),hm=1.75,u=u,fog=(26,26,44))
    ptext(d,40,270,"1978",9,(255,255,255))
    return grade(vign_(big,.4),sat=.95,seed=int(u*30),tint=(.98,.98,1.04))
def tex_masks(w=300,h=220,seed=2):
    rng=np.random.default_rng(seed); im=Image.new("RGB",(w,h),(60,44,36)); d=ImageDraw.Draw(im)
    for r in range(3):
        d.rectangle([0,r*72+62,w,r*72+68],fill=(110,84,56))
        for c in range(5):
            x=34+c*58; y=r*72+34; col=[(70,160,80),(200,60,60),(230,220,200),(110,80,160),(230,160,50)][(r+c)%5]
            d.ellipse([x-20,y-24,x+20,y+26],fill=col); d.ellipse([x-12,y-10,x-4,y],fill=(10,10,10)); d.ellipse([x+4,y-10,x+12,y],fill=(10,10,10)); d.arc([x-10,y+6,x+10,y+18],10,170,fill=(10,10,10),width=2)
    return im
def kirk_mask(d,cx,cy,sc,paint=0.0,eyes=0.0,hair=0.0):
    skin=tuple(int(a+(b-a)*paint) for a,b in zip((222,176,140),(238,238,234)))
    if hair>0:
        d.E(cx,cy-6*sc,66*sc*(.6+.4*hair),82*sc*(.6+.4*hair),(54,36,22,255))
        for i in range(30): a=3.14+i/29*3.14; d.L(cx+math.cos(a)*50*sc,cy-8*sc+math.sin(a)*62*sc,cx+math.cos(a)*(70+(i%3)*8)*sc*hair,cy-8*sc+math.sin(a)*(86+(i%4)*7)*sc*hair,(54,36,22,255),3*sc)
    d.E(cx,cy,56*sc,72*sc,skin+(255,)); d.E(cx-18*sc,cy-24*sc,22*sc,38*sc,(255,255,255,30))
    for sg in(-1,1): d.E(cx+sg*22*sc,cy-14*sc,(8+9*eyes)*sc,(7+11*eyes)*sc,(8,8,10,255))
    d.P([(cx-3*sc,cy),(cx+3*sc,cy),(cx+9*sc,cy+22*sc),(cx-9*sc,cy+22*sc)],tuple(int(c*.9) for c in skin)+(255,))
    if paint<.6:
        for sg in(-1,1): d.L(cx+sg*8*sc,cy-34*sc,cx+sg*38*sc,cy-46*sc,(40,28,22,int(255*(1-paint))),3*sc)
        d.A(cx,cy+30*sc,18*sc,7*sc,10,170,(120,60,50,int(255*(1-paint))),2.5*sc)
def sceneC(u):
    cam=dict(x=lerp(-.8,.6,sm(u/8)),y=1.4,z=lerp(-1.0,.0,sm(u/8)),yaw=lerp(.15,-.05,sm(u/8)),pitch=.04); st=SHOP
    bg=render_room(cam,st,u,1.0,extra=[(0,1.6,2.0,(1,.86,.6),.5)]); back=new_ov()
    for k,x in enumerate((-2.6,-.9,.8,2.5)): pass
    tquad(back,cam,st,(-2.7,2.3,4.59),(-.3,2.3,4.59),(-.3,.5,4.59),(-2.7,.5,4.59),tex_masks(seed=2)); tquad(back,cam,st,(.3,2.3,4.59),(2.7,2.3,4.59),(2.7,.5,4.59),(.3,.5,4.59),tex_masks(seed=6))
    box(back,cam,st,-1.4,1.4,0,1.0,2.6,3.4,(140,100,64)); box(back,cam,st,.5,.9,1.0,1.18,2.8,3.1,(60,60,66)) 
    big=fin(composite(bg,back)); d=D(big)
    def maskp(dd,x,y,a,s,K=1.0): kirk_mask(dd,x,y+10*K,.34*K,0,0,0)
    P3(d,cam,st,.7,3.9,CLERK,dict(P_talk(u),mouth=.4),hm=1.7,u=u,fog=(40,30,20))
    P3(d,cam,st,-.5,2.3,BUYER,dict(P_hold(u,r=(1.4,2.0),grip=.8),mouth=.3),hm=1.78,u=u,props={"r":maskp},fog=(40,30,20),facing="back")
    d.R(180,720,360,780,(250,240,210,255),8); ptext(d,196,738,"OFERTA",4.4,(160,30,30))
    return grade(vign_(big,.4),sat=.95,seed=int(u*30),tint=(1.02,.98,.94))
def sceneD(u):
    st=dict(SHOP,fov=46); cam=dict(x=0,y=1.3,z=0,yaw=0,pitch=.1)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.2,1.0,(1,.86,.6),1.2)]); big=fin(bg); d=D(big)
    p=sm((u-.6)/1.8); e=sm((u-2.4)/1.6); h=sm((u-4.4)/1.6)
    d.R(120,1050,420,1120,(130,96,60,255),0)
    kirk_mask(d,270,420,1.9,paint=p,eyes=e,hair=h)
    hand(d,100,720,3.0,-1,3.0,(236,190,150),curl=.5,spread=.5); hand(d,440,720,3.0,1,3.0,(236,190,150),curl=.5,spread=.5)
    for i,s in enumerate(("PINTAR","OJOS","PELO")):
        on=[p,e,h][i]; x=40+i*160; d.R(x,860,x+140,920,(250,130,30,int(60+195*on)),8); ptext(d,x+12,878,s,5,(255,255,255)); d.R(x,930,x+140,942,(255,255,255,40),4); d.R(x,930,x+140*on,942,(250,130,30,255),4)
    return grade(vign_(big,.5),sat=.95,seed=int(u*30),tint=(1.02,.98,.94))
def sceneE(u):
    cam=dict(x=0,y=1.5,z=0,yaw=0,pitch=.04); ex=[(.0,1.7,2.0,(1,.95,.9),1.4)]
    bg=render_terrain(cam,dict(SUB,fog=.03),u,extra=[]); big=fin(bg); d=D(big)
    ov=Image.new("RGBA",big.size,(0,0,0,0)); od=ImageDraw.Draw(ov); od.rectangle([0,0,1620,2880],fill=(0,0,0,200)); big=Image.alpha_composite(big.convert("RGBA"),ov).convert("RGB"); d=D(big)
    z=1.3+.25*sm(u/6.0)
    for k in range(5): d.E(270,420,230-k*30,300-k*36,(255,255,255,int(7+k*3)))
    kirk_mask(d,270,420,1.0*z,paint=1,eyes=1,hair=1)
    return grade(vign_(big,.8),sat=.9,seed=int(u*30),tint=(1.0,.99,1.04))
def sceneF(u):
    st=SHOP; cam=dict(x=lerp(-.6,.4,sm(u/6)),y=1.4,z=lerp(-.6,.2,sm(u/6)),yaw=.1,pitch=.05)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.6,2.0,(1,.86,.6),.5)]); back=new_ov()
    box(back,cam,st,-1.4,1.4,0,1.0,2.6,3.4,(140,100,64))
    big=fin(composite(bg,back)); d=D(big)
    kirk_mask(d,170,470,1.0,1,1,1)
    def bills(dd,x,y,a,s,K=1.0):
        for k in range(3): dd.R(x-40*K,y-12*K+k*6*K,x+40*K,y+16*K+k*6*K,(120+k*20,176,120,255),2*K); dd.R(x-34*K,y-6*K+k*6*K,x+34*K,y+10*K+k*6*K,(90,140,90,255),2*K)
    P3(d,cam,st,.8,2.3,BUYER,dict(P_hold(u,r=(1.3,1.9)),mouth=.3),hm=1.78,u=u,props={"r":bills},fog=(40,30,20))
    return grade(vign_(big,.4),sat=.95,seed=int(u*30),tint=(1.02,.98,.94))
def sceneG(u):
    st=dict(SHOP,wall="plaster",wcol=(120,100,86),fov=52); cam=dict(x=lerp(-.6,.3,sm(u/6)),y=1.4,z=lerp(-.4,.4,sm(u/6)),yaw=.1,pitch=.04)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.6,2.0,(1,.86,.6),.7)]); back=new_ov()
    ch=Image.new("RGB",(320,230),(24,24,30)); cd=ImageDraw.Draw(ch); cd.text((160,18),"COSTE  vs  TAQUILLA",font=font(20,True),fill=(255,255,255),anchor="mm")
    b=sm(u/3.0); cd.rectangle([60,200-int(14*b),120,200],fill=(120,200,140)); cd.rectangle([190,200-int(160*b),250,200],fill=(250,160,50)); cd.text((90,214),"COSTE",font=font(14),fill=(255,255,255),anchor="mm"); cd.text((220,214),"TAQUILLA",font=font(14),fill=(255,255,255),anchor="mm")
    tquad(back,cam,st,(-1.2,2.4,4.59),(1.2,2.4,4.59),(1.2,.8,4.59),(-1.2,.8,4.59),ch); glow(back,cam,st,(0,1.6,4.5),(255,200,100),1.4,50,5)
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,1.8,3.8,PROD,dict(P_point(u,dirx=-1),ar=(1.4,1.6),mouth=.4),hm=1.75,u=u,fog=(30,24,18))
    return grade(vign_(big,.4),sat=.95,seed=int(u*30),tint=(1.02,.98,.94))
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur): return 1.0,270,480
core.CAM=cam
if __name__=="__main__": core.main()
