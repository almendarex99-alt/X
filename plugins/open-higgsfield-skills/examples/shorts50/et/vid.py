import sys; sys.path.insert(0,"..")
from kit import *
from rooms import mk, render_room
from terrain import render_terrain, mk as tmk
from sets import *
import nes
WORKER=dict(skin=(214,170,130),hair=(60,40,30),hairstyle="short",hat="cap",cap_col=(220,120,30),shirt=(220,130,40),pants=(60,70,110),shoes=(60,44,30),sleeve="short")
WORKER2=dict(WORKER,skin=(190,140,100),shirt=(180,200,220),cap_col=(40,40,60))
DEVR=dict(skin=(232,192,156),hair=(70,50,34),hairstyle="short",beard=True,glasses=True,shirt=(70,120,160),pants=(70,70,86),sleeve="long")
BOSS=dict(skin=(226,184,150),hair=(210,210,210),hairstyle="short",shirt=(240,240,244),coat=(60,60,80),pants=(50,50,60),sleeve="long")
CROWD=[dict(skin=(226,184,150),hair=(60,44,32),hairstyle="short",shirt=(80,110,150),pants=(60,60,80),sleeve="short",hat="cap",cap_col=(160,60,50)),
       dict(skin=(214,170,130),hair=(30,24,20),hairstyle="long",shirt=(200,90,110),pants=(60,60,90),sleeve="short"),
       dict(skin=(236,196,160),hair=(190,150,80),hairstyle="short",shirt=(90,150,100),pants=(80,70,60),sleeve="short"),
       dict(skin=(190,140,100),hair=(20,16,14),hairstyle="bun",shirt=(230,200,80),pants=(60,60,70),sleeve="short")]
LIV=mk(H=2.45,hw=2.4,zend=2.9,zback=-3.2,wall="wood",wcol=(116,82,52),floor="carpet",fcol=(104,70,50),ceil="plaster",ccol=(196,188,170),ambient=.20,amb_rgb=(.95,.82,.68),fog=.006,fov=52)
WH=mk(H=6.0,hw=6.0,zend=12,zback=-4.0,wall="concrete",wcol=(150,146,138),floor="concrete",fcol=(110,108,104),ceil="plaster",ccol=(70,68,66),ambient=.12,amb_rgb=(.9,.95,1),fov=58,fog=.012,fogcol=(14,14,16),
      plights=dict(gap=4.0,off=0,xs=(-2.5,2.5),y=5.5,rgb=(1,.96,.85),I=.55,k=.12))
def atari_tex(u):
    im=Image.new("RGB",(160,192),(120,80,40)); d=ImageDraw.Draw(im); d.rectangle([0,0,159,24],fill=(40,60,20)); text_=nes.text; text_(d,8,8,"E.T.",(220,200,80),2)
    for k,(x,y) in enumerate(((30,70),(96,60),(60,120),(120,140),(24,150))): d.ellipse([x-14,y-8,x+14,y+8],fill=(20,14,8),outline=(90,60,30))
    px=int(60+30*math.sin(u*1.5)); py=int(96+16*math.sin(u*2.1)); d.rectangle([px,py,px+8,py+16],fill=(170,120,60)); d.rectangle([px+1,py+2,px+7,py+6],fill=(210,170,110))
    d.rectangle([0,176,159,191],fill=(60,40,16)); return im
def tv_scene(cam,u,tex):
    st=LIV; bg=render_room(cam,st,u,flick(u,.97),extra=[(-1.8,1.15,1.6,(1,.72,.44),1.0),(0,1.0,2.1,(.45,.68,1.0),1.5)]); back=new_ov(); front=new_ov()
    sidewindow(back,cam,st,-2.39,.3,1.5,night=True); lamp(back,cam,st,-1.8,1.6); plant(back,cam,st,2.0,2.4)
    tquad(back,cam,st,(-1.4,.006,-.8),(1.4,.006,-.8),(1.4,.006,1.9),(-1.4,.006,1.9),tex_rug(base=(90,50,30)))
    tquad(back,cam,st,(1.0,1.95,2.89),(1.8,1.95,2.89),(1.8,1.0,2.89),(1.0,1.0,2.89),tex_poster(col=(40,90,160)))
    box(back,cam,st,-.9,.9,0,.5,2.35,2.9,(104,70,44)); box(back,cam,st,-.62,.62,.5,1.25,2.4,2.88,(70,54,42))
    tquad(back,cam,st,(-.5,1.18,2.395),(.5,1.18,2.395),(.5,.58,2.395),(-.5,.58,2.395),crt(tex,1.0,int(u*30)))
    glow(back,cam,st,(0,.9,2.25),(120,170,255),1.1,60,6)
    box(back,cam,st,-.55,-.1,.5,.58,2.4,2.8,(86,60,40),shadow=False); box(back,cam,st,-.52,-.12,.58,.68,2.5,2.75,(120,86,60),shadow=False)
    return st,bg,back,front
def sceneA(u,final=False):
    t=u+(0 if not final else 3.5)
    st=tmk(fov=54,ground="sand",sky="sunset",fog=.012,fogcol=(236,176,120),hills=.05,hcol=(150,96,80),amb=(1.0,.82,.66),ambient=.85)
    cam=dict(x=lerp(-3.5,-1.0,sm(t/7)),y=1.5,z=lerp(-1.0,2.0,sm(t/7)),yaw=lerp(.2,.05,sm(t/7)),pitch=.04)
    bg=render_terrain(cam,st,t); ov=new_ov()
    box(ov,cam,st,-30,30,-4,0,22,23,(120,80,60),shadow=False)
    carts_heap(ov,cam,st,2.5,16,n=150,r=3.0,h=1.4,seed=2)
    dump_truck(ov,cam,st,-5,17,face=-1,tilt=.35); bulldozer(ov,cam,st,1.5+math.sin(t*.4)*.5,10,face=1,blade_lift=.0)
    big=fin(composite(bg,ov)); d=D(big)
    P3(d,cam,st,-2.0,8.5,WORKER,P_walk(t,2.4),hm=1.75,u=t,fog=(236,176,120)); P3(d,cam,st,4.5,11,WORKER2,dict(P_point(t,dirx=-1)),hm=1.75,u=t,fog=(236,176,120))
    big=snow_particles(big,t,n=60,col=(236,196,150),sz=3,speed=-20,alpha=70,scale=2.2)
    return grade(big,sat=1.05,seed=int(u*30),tint=(1.04,.98,.9))
def sceneB(u):
    cam=dict(x=lerp(.6,0,sm(u/6)),y=.9,z=lerp(-.9,.5,sm(u/6)),yaw=lerp(-.1,0,sm(u/6)),pitch=.03)
    st,bg,back,front=tv_scene(cam,u,atari_tex(u))
    box(back,cam,st,-.28,.28,0,.1,1.1,1.5,(70,50,36)); box(back,cam,st,-.28,.28,.1,.14,1.1,1.5,(30,30,34)); 
    for k in range(6): box(back,cam,st,-.24+k*.08,-.2+k*.08,.12,.15,1.12,1.18,(90,90,96),shadow=False)
    box(back,cam,st,.6,.8,0,.05,.9,1.1,(30,30,34)); box(back,cam,st,.68,.72,.05,.22,.98,1.02,(20,20,24)); 
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,-.1,.7,dict(skin=(236,200,164),hair=(110,70,40),hairstyle="short",shirt=(200,80,60),pants=(60,70,110),sleeve="short"),dict(P_both(u,l=(.7,1.9),r=(.7,1.9)),look=(0,0)),hm=1.15,u=u,y0=-.05,bust=True,facing="back",fog=(40,30,26))
    return grade(big,seed=int(u*30),tint=(1.0,.97,.93))
def cal_tex(u,days):
    im=Image.new("RGB",(320,380),(244,240,226)); d=ImageDraw.Draw(im); d.rectangle([0,0,320,50],fill=(190,40,40)); d.text((160,26),"DICIEMBRE",font=font(26,True),fill=(250,250,250),anchor="mm")
    for r in range(5):
        for c in range(7):
            n=r*7+c+1; x=14+c*43; y=64+r*58; d.rectangle([x,y,x+38,y+50],outline=(150,150,150)); d.text((x+4,y+3),str(n if n<=31 else ""),font=mono(13),fill=(60,60,60))
            if n<=days: d.line([x+4,y+6,x+34,y+46],fill=(210,30,30),width=3); d.line([x+34,y+6,x+4,y+46],fill=(210,30,30),width=3)
    return im
def sceneC(u):
    st=dict(mk(H=2.7,hw=2.4,zend=4.0,zback=-2.0,wall="plaster",wcol=(206,200,184),floor="tile",fcol=(136,136,130),ceil="tile",ccol=(214,212,202),ambient=.26,amb_rgb=(.92,.96,1),fog=.01,fov=52))
    cam=dict(x=lerp(-.7,.1,sm(u/6)),y=1.4,z=lerp(.2,1.1,sm(u/6)),yaw=.1,pitch=.04)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.3,2.0,(.55,.75,1.0),.8)]); back=new_ov()
    tquad(back,cam,st,(.6,2.3,3.99),(2.2,2.3,3.99),(2.2,.8,3.99),(.6,.8,3.99),cal_tex(u,int(u*5.5)))
    box(back,cam,st,-2.0,-.2,0,.74,2.5,3.2,(150,110,70)); box(back,cam,st,-1.5,-.7,.74,1.2,2.7,3.1,(206,200,184)); 
    tquad(back,cam,st,(-1.46,1.16,2.695),(-.74,1.16,2.695),(-.74,.8,2.695),(-1.46,.8,2.695),crt(nes.level(off=u*20,u=u) if False else atari_tex(u),1.0,int(u*30)))
    glow(back,cam,st,(-1.1,1.0,2.6),(140,170,255),.8,50,4)
    # arbolito de Navidad
    box(back,cam,st,-2.3,-2.0,0,.25,3.4,3.7,(90,60,40)); 
    for k in range(4): poly3(back,cam,st,[(-2.15-.55+k*.1,.25+k*.35,3.55),(-2.15+.55-k*.1,.25+k*.35,3.55),(-2.15,.25+k*.35+.55,3.55)],(30,110,50))
    for (x,y) in((-2.2,.5),(-2.0,.9),(-2.1,1.2)): glow(back,cam,st,(x,y,3.5),(255,60,60) if int(u*3)%2 else (255,220,80),.12,120,3)
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,.2,3.5,DEVR,dict(P_point(u,dirx=1),ar=(1.5,1.7)),hm=1.75,u=u)
    return grade(big,seed=int(u*30),tint=(.98,1.0,1.04))
def sceneD(u):
    st=WH; cam=dict(x=lerp(-1.6,.6,sm(u/8)),y=1.5,z=lerp(-3.0,-1.0,sm(u/8)),yaw=.0,pitch=.04)
    bg=render_room(cam,st,u,1.0); back=new_ov(); front=new_ov()
    for r in range(3):
        for c in range(5):
            bx=-4.2+c*1.7+(r%2)*.4; bz=3.0+r*2.6
            for lvl in range(4): box(back,cam,st,bx,bx+1.4,lvl*.9,lvl*.9+.85,bz,bz+.9,[(170,140,100),(190,160,120),(150,120,84)][(c+lvl)%3],edge=(90,70,50),shadow=(lvl==0))
    tquad(back,cam,st,(2.0,3.4,2.99),(5.0,3.4,2.99),(5.0,1.6,2.99),(2.0,1.6,2.99),Image.new("RGB",(80,50),(24,24,28)))
    ch=Image.new("RGB",(300,180),(250,250,250)); cd=ImageDraw.Draw(ch); cd.text((10,6),"VENTAS",font=font(22,True),fill=(30,30,30)); cd.line([(20,40),(100,50),(180,120),(280,160)],fill=(210,30,30),width=6)
    tquad(back,cam,st,(-5.2,3.6,5.5),(-2.4,3.6,5.5),(-2.4,1.8,5.5),(-5.2,1.8,5.5),ch)
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,-.4,2.0,BOSS,dict(P_hold(u,r=(1.2,1.6)),mouth=.3),hm=1.75,u=u,fog=(14,14,16))
    P3(d,cam,st,1.6,2.4,WORKER2,dict(P_walk(u,2.4)),hm=1.75,u=u,fog=(14,14,16))
    return grade(big,seed=int(u*30),tint=(1.0,.99,.96))
def sceneE(u):
    st=tmk(fov=54,ground="dirt",sky="night",fog=.014,fogcol=(26,28,50),hills=.04,hcol=(24,28,54),amb=(.3,.36,.6),ambient=1.0)
    cam=dict(x=lerp(-3,2.5,sm(u/9)),y=1.6,z=lerp(-1.0,1.0,sm(u/9)),yaw=lerp(.15,-.05,sm(u/9)),pitch=.04)
    ex=[(x,10,z,(1,.9,.7),3.0) for (x,z) in ((-6,10),(6,14),(0,22))]
    bg=render_terrain(cam,st,u,extra=ex); ov=new_ov()
    for (x,z) in ((-6,10),(6,14),(0,22)):
        box(ov,cam,st,x-.1,x+.1,0,10,z-.1,z+.1,(50,50,54),shadow=False); glow(ov,cam,st,(x,10,z),(255,240,200),1.6,90,6)
    box(ov,cam,st,-20,20,0,2.5,26,26.2,(60,60,66),shadow=False)
    carts_heap(ov,cam,st,0,15,n=140,r=3.2,h=1.3,seed=5); dump_truck(ov,cam,st,-4,16,face=-1,tilt=.4); bulldozer(ov,cam,st,3.4,12,face=-1,col=(220,170,40))
    big=fin(composite(bg,ov)); d=D(big)
    P3(d,cam,st,.5,8,WORKER,dict(P_walk(u,2.4)),hm=1.75,u=u,fog=(26,28,50)); P3(d,cam,st,-2.2,9.5,BOSS,dict(P_point(u,dirx=1),ar=(1.4,1.6)),hm=1.75,u=u,fog=(26,28,50))
    big=snow_particles(big,u,n=40,col=(200,200,210),sz=2,speed=-10,alpha=60,scale=2.2)
    return grade(big,sat=.95,seed=int(u*30),tint=(.96,.98,1.06))
def sceneF(u):
    st=tmk(fov=54,ground="sand",sky="day",fog=.01,fogcol=(236,226,206),hills=.05,hcol=(176,136,104),amb=(1,.98,.94),ambient=1.0)
    cam=dict(x=lerp(-3.5,-.5,sm(u/7)),y=1.55,z=lerp(-1.0,1.2,sm(u/7)),yaw=lerp(.16,.0,sm(u/7)),pitch=.04)
    bg=render_terrain(cam,st,u); ov=new_ov()
    box(ov,cam,st,-6,6,-3,0,14,20,(150,110,78),shadow=False); carts_heap(ov,cam,st,0,16,n=100,r=2.6,h=.5,seed=9)
    excavator(ov,cam,st,-2.5,10,face=1,ang=u*.9)
    big=fin(composite(bg,ov)); d=D(big)
    for k,(x,z,stl) in enumerate(((1.0,6.8,CROWD[0]),(2.4,7.4,CROWD[1]),(3.6,6.5,CROWD[2]),(-.4,7.2,CROWD[3]),(4.8,7.8,CROWD[0]))):
        P3(d,cam,st,x,z,stl,dict(P_cheer(u,k)) if k==1 else dict(P_point(u,k),ar=(1.3,1.5)) if k%2==0 else dict(P_talk(u,k)),hm=1.7,u=u,fog=(236,226,206))
    P3(d,cam,st,-.9,6.4,dict(WORKER2,shirt=(210,210,214)),dict(P_hold(u,r=(2.0,2.8)),mouth=.5),hm=1.75,u=u,fog=(236,226,206))
    big=snow_particles(big,u,n=50,col=(236,206,160),sz=3,speed=-20,alpha=60,scale=2.2)
    return grade(big,sat=1.04,seed=int(u*30),tint=(1.03,1.0,.94))
def cart_tex():
    im=Image.new("RGB",(160,200),(150,150,146)); d=ImageDraw.Draw(im); d.rectangle([14,18,146,120],fill=(214,190,70),outline=(90,80,30),width=3); d.text((80,50),"E.T.",font=font(40,True),fill=(40,30,10),anchor="mm")
    d.polygon([(40,150),(120,150),(110,190),(50,190)],fill=(90,90,90)); return im
def sceneG(u):
    st=tmk(fov=46,ground="sand",sky="sunset",fog=.02,fogcol=(236,176,120),hills=.04,hcol=(150,96,80),amb=(1.0,.82,.66),ambient=.9)
    cam=dict(x=.6*math.sin(u*.4),y=1.2,z=-.3,yaw=-.2*math.sin(u*.4),pitch=.0)
    bg=render_terrain(cam,st,u); ov=new_ov()
    cx=.0; tquad(ov,cam,st,(cx-.18,1.2+.12*math.sin(u*.7),1.0),(cx+.18,1.2+.12*math.sin(u*.7),1.0),(cx+.18,.78+.12*math.sin(u*.7),1.0),(cx-.18,.78+.12*math.sin(u*.7),1.0),cart_tex())
    big=fin(composite(bg,ov)); d=D(big)
    hand3(d,cam,st,(cx,.7+.12*math.sin(u*.7),.98),hand_m=.2,a=3.14,s=1,curl=.8,spread=.4,arm_from=(300,1.2),arm_w=.07,sleeve=(190,120,50))
    big=snow_particles(big,u,n=90,col=(236,196,150),sz=3,speed=-25,alpha=110,scale=2.2)
    return grade(big,sat=1.05,seed=int(u*30),tint=(1.04,.98,.9))
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur): return 1.0,270,480
core.CAM=cam
if __name__=="__main__": core.main()
