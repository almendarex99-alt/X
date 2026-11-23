import sys; sys.path.insert(0,"..")
from kit import *
from rooms import mk, render_room
from terrain import render_terrain, mk as tmk
from sets import *
from elm.helpers import FRED, TEEN, TEENF, BULLY, blades
def fred3(d,cam,st,x,z,u,pose=None,hm=1.85):
    pl=place3(cam,st,x,z,hm)
    if not pl: return None
    lx,ly,sc,z2=pl; k=math.exp(-z2*.015)
    o=person(d,lx,ly,sc,u,pose or dict(P_walk(u,2.2),ar=(.9,.9)),fade(FRED,min(1.0,k),(20,14,24)),deco=lambda dd,hx,hy,s: dd.E(hx,hy-1*s,17*s,15*s,(20,14,14,200)))
    blades(d,o["hand_r"],sc,u); return o
BED=mk(H=2.5,hw=2.2,zend=3.6,zback=-3.0,wall="plaster",wcol=(120,104,140),wcol2=(60,50,70),floor="wood",fcol=(86,64,48),ceil="plaster",ccol=(150,140,160),ambient=.08,amb_rgb=(.7,.7,1.0),fog=.03,fogcol=(6,4,12),fov=52)
BOIL=mk(H=3.4,hw=2.2,wall="metal",wcol=(96,84,80),floor="grate",fcol=(60,56,56),ceil="pipes",ccol=(60,54,50),ambient=.08,amb_rgb=(1,.6,.5),fog=.06,fogcol=(18,6,4),fov=56,strip=(255,120,60),hazard=False,
        plights=dict(gap=5,off=2,xs=(0,),y=3.0,rgb=(1.0,.45,.2),I=1.3,flk=.8,flp=.25,k=.4))
CLASS=mk(H=3.0,hw=3.2,zend=6.0,zback=-3.0,wall="plaster",wcol=(176,176,150),floor="wood",fcol=(130,100,70),ceil="tile",ccol=(200,198,190),ambient=.26,fog=.01,fov=52,plights=dict(gap=3,off=1,xs=(-1.2,1.2),y=2.8,rgb=(1,.97,.85),I=.4,k=.4))
SUBN=tmk(fov=54,ground="street",sky="night",fog=.018,fogcol=(22,26,44),hills=.03,hcol=(18,22,36),amb=(.28,.34,.52),ambient=1.0)
CRAV=dict(skin=(230,190,156),hair=(180,180,186),hairstyle="short",beard=True,glasses=True,shirt=(60,60,70),coat=(40,44,56),pants=(50,50,60),sleeve="long")
KIDN=dict(skin=(236,196,160),hair=(120,70,40),hairstyle="short",shirt=(200,200,210),pants=(70,70,100),sleeve="short")
def vign_(img,k=.6): return Image.alpha_composite(img.convert("RGBA"),vignette_ov(img.size,k)).convert("RGB")
def bedroom(cam,u):
    st=BED; bg=render_room(cam,st,u,1.0,extra=[(-1.4,1.4,2.8,(.5,.6,1.0),.9),(1.6,.9,2.8,(1.0,.7,.4),.4)]); back=new_ov()
    tquad(back,cam,st,(-1.3,2.0,3.59),(.1,2.0,3.59),(.1,.8,3.59),(-1.3,.8,3.59),tex_window(night=True,curtains=(90,50,90))); glow(back,cam,st,(-.6,1.4,3.5),(130,150,255),1.2,50,5)
    box(back,cam,st,.5,2.0,0,.5,1.2,3.4,(86,70,96)); box(back,cam,st,.5,2.0,.5,.62,1.2,3.4,(190,190,210)); box(back,cam,st,.5,2.0,.5,1.4,3.35,3.45,(70,52,40)); box(back,cam,st,.6,1.4,.62,.74,2.9,3.3,(236,236,244),shadow=False)
    return st,bg,back
def street_big(cam,u):
    ex=[(3.8 if k%2==0 else -3.8,3.0,z,(1.0,.66,.34),2.6) for k,z in enumerate((8,20,32))]; bg=render_terrain(cam,SUBN,u,extra=ex); ov=new_ov()
    for k,z in enumerate((12,26,40)): house(ov,cam,SUBN,-9.5,z,seed=k+61,t=u,lit=.5); house(ov,cam,SUBN,9.5,z+6,seed=k+71,t=u)
    for k,z in enumerate((8,20,32)):
        x=3.8 if k%2==0 else -3.8; box(ov,cam,SUBN,x-.06,x+.06,0,3.0,z-.06,z+.06,(30,30,34),shadow=False); glow(ov,cam,SUBN,(x,3.0,z),(255,190,110),1.0,90,6)
    return bg,ov
def sceneA(u,final=False):
    t=u+(0 if not final else 3); cam=dict(x=lerp(-1.0,-.2,sm(t/6)),y=1.5,z=lerp(-2.0,-1.0,sm(t/6)),yaw=lerp(.2,.05,sm(t/6)),pitch=.05)
    st,bg,back=bedroom(cam,t); big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,1.3,2.4,TEEN,dict(P_scared(t),al=(.7,1.9),ar=(.7,1.9)),hm=1.3,u=t,y0=.42,bust=True,fog=(6,4,12))
    box(back,cam,st,0,0,0,0,0,0,(0,0,0)) if False else None
    fred3(d,cam,st,-.6,3.4,t,dict(P_idle(t),ar=(.9,1.0)),hm=1.9)
    for k in range(10): fogband(d,t,520,820,(150,120,170),40,10) if False else None
    return grade(vign_(big,.6),sat=.85,seed=int(u*30),tint=(.96,.96,1.08))
def sceneB(u):
    cam=dict(x=lerp(-1.5,.5,sm(u/7)),y=1.5,z=lerp(0,1.0,sm(u/7)),yaw=lerp(.12,0,sm(u/7)),pitch=.05)
    bg,ov=street_big(cam,u)
    box(ov,cam,SUBN,2.0,2.1,0,3.0,10,10.1,(60,60,66),shadow=False); tquad(ov,cam,SUBN,(.6,3.0,9.95),(3.6,3.0,9.95),(3.6,2.3,9.95),(.6,2.3,9.95),Image.new("RGB",(300,70),(0,150,80)))
    big=fin(composite(bg,ov)); d=D(big)
    P3(d,cam,SUBN,-1.2,6.0,TEEN,P_walk(u,2.6),hm=1.7,u=u,fog=(22,26,44)); P3(d,cam,SUBN,1.2,6.4,TEENF,P_walk(u,2.6,1.5),hm=1.7,u=u,fog=(22,26,44))
    ptext(d,40,270,"1984",9,(255,255,255))
    pl=place3(cam,SUBN,2.1,10,1.0,2.45)
    if pl: ptext(d,pl[0]-70,pl[1]-8,"ELM STREET",3.0,(255,255,255))
    return grade(vign_(big,.5),sat=.9,seed=int(u*30),tint=(.96,.98,1.06))
def news_tex(w=320,h=420):
    im=Image.new("RGB",(w,h),(236,230,214)); d=ImageDraw.Draw(im); d.rectangle([0,0,w,56],fill=(60,56,50)); d.text((w/2,28),"NOTICIA",font=serif(30),fill=(240,240,240),anchor="mm")
    for k in range(3): d.rectangle([16,76+k*50,150,116+k*50],fill=(176,172,160))
    for k in range(9): d.rectangle([166,76+k*22,w-14,84+k*22],fill=(110,106,98))
    for k in range(5): d.rectangle([16,240+k*22,150,248+k*22],fill=(110,106,98))
    return im
def sceneC(u):
    st=mk(H=2.7,hw=2.4,zend=4.4,zback=-2.6,wall="plaster",wcol=(90,80,70),floor="wood",fcol=(90,68,48),ceil="plaster",ccol=(140,130,120),ambient=.12,amb_rgb=(1,.85,.7),fov=52,fog=.015,fogcol=(8,6,6))
    cam=dict(x=lerp(-.6,.3,sm(u/9)),y=1.4,z=lerp(-.8,.2,sm(u/9)),yaw=.08,pitch=.05)
    bg=render_room(cam,st,u,1.0,extra=[(.8,1.3,2.5,(1,.8,.5),1.2)]); back=new_ov()
    box(back,cam,st,-1.4,1.4,0,.76,2.4,3.4,(110,76,50)); tquad(back,cam,st,(-.5,.77,2.55),(.5,.77,2.55),(.5,.9,3.25),(-.5,.9,3.25),news_tex()); lamp(back,cam,st,1.1,2.6,h=1.5,col=(255,210,150))
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,.0,3.7,CRAV,dict(P_hold(u,r=(1.4,2.0),l=(1.4,2.0),grip=.7),look=(0,.7),mouth=.3),hm=1.78,u=u,fog=(14,10,8))
    ptext(d,40,270,"NOTICIA",8,(255,255,255))
    return grade(vign_(big,.5),sat=.95,seed=int(u*30),tint=(1.03,.98,.93))
def sceneD(u):
    st=mk(H=2.6,hw=2.2,zend=4.0,zback=-2.6,wall="plaster",wcol=(150,140,120),floor="tile",fcol=(150,140,130),ceil="plaster",ccol=(190,184,170),ambient=.2,fov=52,fog=.012,plights=dict(gap=100,off=1,xs=(0,),y=2.3,rgb=(1,.92,.75),I=.4,k=.5))
    cam=dict(x=lerp(-.6,.3,sm(u/8)),y=1.4,z=lerp(-.8,.2,sm(u/8)),yaw=.08,pitch=.05)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.2,2.4,(1,.92,.75),.6)]); back=new_ov()
    box(back,cam,st,-1.2,1.2,0,.74,2.4,3.2,(120,90,64))
    for k in range(3): box(back,cam,st,.1+k*.28,.3+k*.28,.74,.86,2.5,2.7,(240,240,244)); glow(back,cam,st,(.2+k*.28,.95,2.6),(240,240,250),.16,60,3)
    ck=Image.new("RGB",(160,160),(236,236,240)); cd=ImageDraw.Draw(ck); cd.ellipse([4,4,156,156],outline=(40,40,50),width=8); a=u*2.0; cd.line([(80,80),(80+math.cos(a)*50,80+math.sin(a)*50)],fill=(30,30,36),width=7); cd.line([(80,80),(80+math.cos(a*12)*66,80+math.sin(a*12)*66)],fill=(210,40,40),width=3)
    tquad(back,cam,st,(-1.6,2.2,3.99),(-.7,2.2,3.99),(-.7,1.3,3.99),(-1.6,1.3,3.99),ck)
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,-.1,3.0,TEEN,dict(P_idle(u),al=(.25,.5),ar=(.9,1.9),tilt=.2*math.sin(u*1.2)+.05,look=(0,.5),mouth=.2*(math.sin(u*1.2)>0),bob=math.sin(u*1.2)*3),hm=1.72,u=u,fog=(20,18,16))
    ptext(d,40,270,"NO DORMIR",7,(255,255,255))
    return grade(vign_(big,.4),sat=.95,seed=int(u*30),tint=(1.02,.99,.95))
def sceneE(u):
    cam=walk_cam(u,speed=.0); cam["pitch"]=.08; cam["x"]=0; cam["z"]=0; cam["y"]=1.6; st=BOIL
    bg=render_room(cam,st,u,flick(u)); big=fin(bg); d=D(big)
    z=lerp(11.0,5.0,sm(u/6)); fred3(d,cam,st,0,z,u,dict(P_walk(u,2.2),ar=(.9,1.0)),hm=1.9)
    P3(d,cam,st,.2,3.0,TEEN,dict(P_walk(u,6.0),al=(.8,1.3),ar=(.8,1.3),mouth=1.0),hm=1.7,u=u,facing="back",fog=(18,6,4))
    for k in range(7): a_=((u*.5+k*.14)%1); d.E(100+k*60,300+a_*40,(10+a_*50),(8+a_*30),(230,230,236,int(80*(1-a_))))
    return grade(vign_(big,.6),sat=.9,seed=int(u*30),tint=(1.04,.96,.94))
def sceneF(u):
    st=CLASS; cam=dict(x=lerp(-.8,.6,sm(u/8)),y=1.3,z=lerp(-1.2,-.2,sm(u/8)),yaw=lerp(.15,0,sm(u/8)),pitch=.05)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.8,2.5,(1,.97,.85),.5)]); back=new_ov()
    tquad(back,cam,st,(-2.2,2.4,5.99),(2.2,2.4,5.99),(2.2,.9,5.99),(-2.2,.9,5.99),Image.new("RGB",(300,100),(30,60,44)))
    for k,x in enumerate((-1.2,0,1.2)): box(back,cam,st,x-.4,x+.4,.55,.62,2.6,3.2,(170,130,90)); box(back,cam,st,x-.3,x-.25,0,.55,2.7,2.75,(70,70,76),shadow=False); box(back,cam,st,x+.25,x+.3,0,.55,2.7,2.75,(70,70,76),shadow=False)
    nm=Image.new("RGB",(120,40),(200,160,110)); nd=ImageDraw.Draw(nm); nd.text((60,20),"FRED",font=font(26,True),fill=(60,40,30),anchor="mm"); tquad(back,cam,st,(-.3,.62,2.58),(.3,.62,2.58),(.3,.62,2.9),(-.3,.62,2.9),nm)
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,-.6,3.8,KIDN,dict(P_scared(u),al=(.5,1.2),ar=(.5,1.2)),hm=1.4,u=u,fog=(40,36,30)); P3(d,cam,st,.9,3.6,BULLY,dict(P_talk(u),al=(.9,.9),ar=(.9,.9),mouth=.8),hm=1.5,u=u,fog=(40,36,30))
    ptext(d,40,270,"EL COLEGIO",5,(255,255,255))
    return grade(vign_(big,.3),sat=.95,seed=int(u*30),tint=(1.02,.99,.95))
def sceneG(u):
    cam=walk_cam(u,speed=.0); cam["pitch"]=.08; cam["x"]=0; cam["z"]=0; cam["y"]=1.6; st=BOIL
    bg=render_room(cam,st,u,flick(u)); big=fin(bg); d=D(big)
    fred3(d,cam,st,0,lerp(6,3.6,sm(u/6)),u,dict(P_idle(u),ar=(.9,1.0),al=(.3,.4)),hm=1.9)
    d.R(40,780,260,860,(236,230,214,230),6); ptext(d,52,800,"NOTICIA",4,(60,56,50)); d.R(290,780,500,860,(200,160,110,230),6); ptext(d,310,800,"FRED",5,(60,40,30)); ptext(d,40,270,"DOS MIEDOS",6,(255,255,255))
    return grade(vign_(big,.6),sat=.9,seed=int(u*30),tint=(1.04,.96,.94))
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur): return 1.0,270,480
core.CAM=cam
if __name__=="__main__": core.main()
