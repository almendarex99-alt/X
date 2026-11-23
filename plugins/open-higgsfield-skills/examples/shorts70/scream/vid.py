import sys; sys.path.insert(0,"..")
from kit import *
from rooms import mk, render_room
from terrain import render_terrain, mk as tmk
from sets import *
from scream.helpers import gmask, GHOST, SCOUT, CRAVEN, PROD, CLERK
HALLW=mk(H=2.6,hw=1.5,zend=9.0,zback=-3.0,wall="plaster",wcol=(150,140,126),wcol2=(70,56,44),floor="wood",fcol=(96,70,48),ceil="plaster",ccol=(170,164,150),ambient=.07,amb_rgb=(.7,.8,1),fog=.05,fogcol=(2,3,6),fov=56,open_p=.3,seg=5.0,D=2.4)
SETR=mk(H=2.7,hw=2.6,zend=4.6,zback=-3.0,wall="plaster",wcol=(190,176,150),floor="wood",fcol=(116,84,56),ceil="plaster",ccol=(210,204,190),ambient=.2,amb_rgb=(1,.9,.76),fog=.01,fov=52,plights=dict(gap=100,off=1,xs=(0,),y=2.4,rgb=(1,.86,.62),I=.5,k=.5))
SHOP=mk(H=2.7,hw=2.8,zend=4.6,zback=-3.0,wall="plaster",wcol=(210,196,170),floor="wood",fcol=(120,86,56),ceil="plaster",ccol=(200,190,170),ambient=.2,amb_rgb=(1,.9,.76),fog=.01,fov=52,plights=dict(gap=3,off=1,xs=(0,),y=2.55,rgb=(1,.86,.62),I=.35,k=.5))
DUSK=tmk(fov=54,ground="street",sky="dusk",fog=.014,fogcol=(120,86,96),hills=.04,hcol=(40,30,50),amb=(.8,.62,.6),ambient=.9)
OFFS_=mk(H=2.7,hw=2.4,zend=4.4,zback=-2.6,wall="plaster",wcol=(210,204,190),floor="wood",fcol=(100,76,56),ceil="plaster",ccol=(220,216,206),ambient=.26,fov=52,plights=dict(gap=100,off=1,xs=(0,),y=2.4,rgb=(1,.9,.7),I=.4,k=.5))
def vign_(img,k=.5): return Image.alpha_composite(img.convert("RGBA"),vignette_ov(img.size,k)).convert("RGB")
def gf(d,cam,st,x,z,u,pose=None,hm=1.85,tone=1.0):
    pl=place3(cam,st,x,z,hm)
    if not pl: return None
    lx,ly,sc,z2=pl; return person(d,lx,ly,sc,u,pose or dict(P_idle(u),al=(.25,.6),ar=(.25,.6),tilt=.1*math.sin(u*1.5)),fade(GHOST,min(1.0,tone*math.exp(-z2*.02)),(4,4,8)))
def sceneA(u,final=False):
    t=u+(0 if not final else 3); cam=walk_cam(t,speed=.3); cam["pitch"]=.07+cam["pitch"]*.3; cam["y"]=1.55; st=HALLW
    bg=render_room(cam,st,t,flick(t,.97),extra=[(0,1.8,cam["z"]+8.0,(.9,.9,1.0),1.4)]); big=fin(bg); d=D(big)
    gf(d,cam,st,0,cam["z"]+lerp(10,6,sm(t/8)),t,hm=1.9,tone=1.4)
    return grade(vign_(big,.6),sat=.8,seed=int(u*30),tint=(.96,.98,1.06))
def sceneB(u):
    st=SETR; cam=dict(x=lerp(-1.2,.4,sm(u/7)),y=1.45,z=lerp(-1.6,-.6,sm(u/7)),yaw=lerp(.2,0,sm(u/7)),pitch=.05)
    bg=render_room(cam,st,u,1.0,extra=[(-1.5,1.4,2.2,(1,.85,.6),.8),(1.4,1.4,2.2,(1,.9,.7),.5)]); back=new_ov()
    box(back,cam,st,-1.0,1.0,0,.45,1.6,2.5,(120,60,50)); box(back,cam,st,-1.0,1.0,.45,1.0,2.4,2.7,(130,64,54)); lamp(back,cam,st,-1.8,2.4,h=1.3); bookcase(back,cam,st,1.9,3.7,w=1.2,h=2.0,d=.3,seed=9)
    box(back,cam,st,-.5,.5,.4,1.0,3.5,4.1,(40,42,46)); box(back,cam,st,-.2,.2,.5,.85,3.1,3.5,(30,30,34)); box(back,cam,st,-.4,.4,0,.4,3.6,4.0,(70,70,74))
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,-1.4,3.0,CRAVEN,dict(P_idle(u),ar=(1.4,1.2),mouth=.5+.5*math.sin(u*7),curlR=.2),hm=1.78,u=u,fog=(30,22,16)); P3(d,cam,st,1.3,3.2,PROD,dict(P_hold(u,r=(1.3,2.0))),hm=1.78,u=u,fog=(30,22,16))
    clapper(d,430,830,1.1,open_=clamp(math.sin(u*2.2))); ptext(d,40,270,"1996",9,(255,255,255)); ptext(d,40,340,"WES CRAVEN",4.6,(255,214,120))
    return grade(vign_(big,.4),sat=.95,seed=int(u*30),tint=(1.03,.98,.94))
def sceneC(u):
    cam=dict(x=lerp(-2,.6,sm(u/7)),y=1.5,z=lerp(0,1.2,sm(u/7)),yaw=lerp(.2,0,sm(u/7)),pitch=.05)
    ex=[(3.8,3.0,z,(1.0,.66,.34),2.0) for z in (10,24)]; bg=render_terrain(cam,DUSK,u,extra=ex); ov=new_ov()
    for k,z in enumerate((14,28)): house(ov,cam,DUSK,-9.5,z,seed=k+81,t=u,lit=.5)
    house(ov,cam,DUSK,9.5,16,seed=85,t=u); box(ov,cam,DUSK,-9.0,-8.9,2.3,2.9,13.4,13.9,(30,24,30),shadow=False)
    mk_=Image.new("RGBA",(60,90),(0,0,0,0)); md=ImageDraw.Draw(mk_); md.ellipse([8,4,52,86],fill=(236,234,226,255)); md.polygon([(18,26),(26,24),(24,46),(20,56)],fill=(8,8,10,255)); md.polygon([(42,26),(34,24),(36,46),(40,56)],fill=(8,8,10,255)); md.ellipse([24,58,38,80],fill=(8,8,10,255))
    tquad(ov,cam,DUSK,(-8.93,2.7,13.2),(-8.93,2.7,13.8),(-8.93,2.0,13.8),(-8.93,2.0,13.2),mk_)
    big=fin(composite(bg,ov)); d=D(big)
    def torch(dd,x,y,a,s,K=1.0): dd.R(x-6*K,y-12*K,x+6*K,y+26*K,(60,60,70),4*K); dd.E(x,y+30*K,10*K,7*K,(255,240,180))
    P3(d,cam,DUSK,-1.0,7.5,SCOUT,dict(P_walk(u,2.0),ar=(1.3,2.0)),hm=1.75,u=u,props={"r":torch},fog=(120,86,96)); P3(d,cam,DUSK,1.2,8.2,PROD,dict(P_point(u,dirx=-1),ar=(1.45,1.5)),hm=1.78,u=u,fog=(120,86,96))
    ptext(d,40,270,"LOCALIZACIONES",4,(255,255,255))
    return grade(vign_(big,.4),sat=.95,seed=int(u*30),tint=(1.04,.98,.95))
def tex_masks2(w=300,h=220):
    im=Image.new("RGB",(w,h),(60,44,36)); d=ImageDraw.Draw(im)
    for r in range(3):
        d.rectangle([0,r*72+62,w,r*72+68],fill=(110,84,56))
        for c in range(5):
            x=34+c*58; y=r*72+34
            if (r,c)==(1,2):
                d.ellipse([x-18,y-26,x+18,y+30],fill=(236,234,226)); d.polygon([(x-10,y-8),(x-4,y-10),(x-6,y+8),(x-9,y+14)],fill=(8,8,10)); d.polygon([(x+10,y-8),(x+4,y-10),(x+6,y+8),(x+9,y+14)],fill=(8,8,10)); d.ellipse([x-5,y+14,x+5,y+28],fill=(8,8,10))
            else:
                col=[(70,160,80),(200,60,60),(110,80,160),(230,160,50)][(r+c)%4]; d.ellipse([x-20,y-24,x+20,y+26],fill=col); d.ellipse([x-12,y-10,x-4,y],fill=(10,10,10)); d.ellipse([x+4,y-10,x+12,y],fill=(10,10,10))
    return im
def sceneD(u):
    st=SHOP; cam=dict(x=lerp(-.8,.6,sm(u/8)),y=1.4,z=lerp(-1.0,0,sm(u/8)),yaw=lerp(.15,-.05,sm(u/8)),pitch=.04)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.6,2.0,(1,.86,.6),.5)]); back=new_ov()
    tquad(back,cam,st,(-2.7,2.3,4.59),(-.3,2.3,4.59),(-.3,.5,4.59),(-2.7,.5,4.59),tex_masks2()); tquad(back,cam,st,(.3,2.3,4.59),(2.7,2.3,4.59),(2.7,.5,4.59),(.3,.5,4.59),tex_masks2())
    box(back,cam,st,-1.4,1.4,0,1.0,2.6,3.4,(140,100,64))
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,.7,3.9,CLERK,dict(P_talk(u),mouth=.4),hm=1.7,u=u,fog=(40,30,20)); P3(d,cam,st,-.5,2.3,SCOUT,dict(P_hold(u,r=(1.4,2.0),grip=.7),mouth=.3),hm=1.78,u=u,facing="back",fog=(40,30,20))
    ptext(d,40,270,"DE TIENDA",7,(255,255,255))
    return grade(vign_(big,.4),sat=.95,seed=int(u*30),tint=(1.02,.98,.94))
def sceneE(u):
    st=dict(HALLW,hw=2.4,zend=7.0); cam=dict(x=0,y=1.5,z=lerp(-1,.4,sm(u/7)),yaw=0,pitch=.04)
    bg=render_room(cam,st,u,flick(u,.97),extra=[(0,1.8,3.0,(.9,.9,1.0),1.6)]); big=fin(bg); d=D(big)
    gf(d,cam,st,0,3.4,u,hm=1.9,tone=1.5); ptext(d,40,270,"CARA ALARGADA",4.4,(255,214,120))
    return grade(vign_(big,.6),sat=.8,seed=int(u*30),tint=(.96,.98,1.06))
def sceneF(u):
    st=OFFS_; cam=dict(x=lerp(-.7,.3,sm(u/6)),y=1.4,z=lerp(-1.0,0,sm(u/6)),yaw=.06,pitch=.05)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.4,2.2,(1,.9,.7),.6)]); back=new_ov(); box(back,cam,st,-1.4,1.4,0,.76,2.3,3.3,(110,80,54))
    doc=Image.new("RGB",(300,380),(240,236,222)); dd=ImageDraw.Draw(doc); dd.rectangle([0,0,300,40],fill=(210,60,60)); dd.text((150,20),"ACUERDO",font=font(24,True),fill=(255,255,255),anchor="mm")
    for k in range(10): dd.rectangle([20,60+k*28,280-((k*37)%100),68+k*28],fill=(110,106,98))
    tquad(back,cam,st,(-.5,.77,2.4),(.5,.77,2.4),(.5,.77,2.95),(-.5,.77,2.95),doc)
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,-1.0,3.8,CRAVEN,dict(al=(.5,1.2),ar=(1.3+.08*math.sin(u*6),1.5+.1*math.sin(u*6)),ll=(.05,.05),lr=(.05,.05),bob=0,tilt=.04,look=(.6,0),mouth=.3,curlR=.6,hands_front=True),hm=1.78,u=u,fog=(30,24,18))
    P3(d,cam,st,1.0,3.8,PROD,dict(al=(1.3+.08*math.sin(u*6),1.5+.1*math.sin(u*6)),ar=(.5,1.2),ll=(.05,.05),lr=(.05,.05),bob=0,tilt=-.04,look=(-.6,0),mouth=.3,curlL=.6,hands_front=True),hm=1.78,u=u,fog=(30,24,18))
    ptext(d,40,270,"ACUERDO",5,(255,255,255)) if False else None
    return grade(vign_(big,.4),sat=.95,seed=int(u*30),tint=(1.03,.98,.94))
def sceneG(u):
    cam=dict(x=0,y=1.6,z=lerp(-1,.6,sm(u/6)),yaw=0,pitch=.05)
    ex=[(0,3.0,z,(1.0,.66,.34),3.0) for z in (8,14)]; NI=tmk(fov=54,ground="street",sky="night",fog=.02,fogcol=(18,22,40),hills=.03,hcol=(14,18,30),amb=(.26,.32,.5),ambient=1.0)
    bg=render_terrain(cam,NI,u,extra=ex); big=fin(bg); d=D(big)
    for k,x in enumerate((-1.6,0,1.6)): gf(d,cam,NI,x,5.5+k*.5,u+k,pose=dict(P_walk(u,2.0,k*1.2),al=(.3,.5),ar=(.3,.5)),hm=1.85,tone=1.4)
    film_strip(d,840,u,h=90); ptext(d,40,270,"ICONO",8,(255,255,255))
    return grade(vign_(big,.5),sat=.9,seed=int(u*30),tint=(.96,.98,1.06))
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur): return 1.0,270,480
core.CAM=cam
if __name__=="__main__": core.main()
