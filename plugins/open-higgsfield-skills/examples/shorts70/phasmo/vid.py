import sys; sys.path.insert(0,"..")
from kit import *
from rooms import mk, render_room
from terrain import render_terrain, mk as tmk
from sets import *
from phasmo.helpers import ghost, GHOST, emf, mic, waves, GRN
HALL=mk(H=2.9,hw=1.9,zend=9.0,zback=-3.0,wall="plaster",wcol=(88,104,100),wcol2=(40,34,30),floor="wood",fcol=(70,52,38),ceil="beams",ccol=(70,64,58),ambient=.11,amb_rgb=(.6,.75,1.0),fog=.04,fogcol=(2,4,6),fov=56,open_p=.3,seg=6.0,D=2.5)
ROOMH=mk(H=2.8,hw=2.6,zend=5.0,zback=-3.0,wall="plaster",wcol=(96,110,104),wcol2=(40,34,30),floor="wood",fcol=(74,56,40),ceil="beams",ccol=(70,64,58),ambient=.11,amb_rgb=(.6,.75,1.0),fog=.03,fogcol=(2,4,6),fov=54)
NIGHT=tmk(fov=54,ground="grass",sky="night",fog=.02,fogcol=(16,22,40),hills=.04,hcol=(12,16,30),amb=(.26,.32,.52),ambient=1.0)
HUNT=dict(skin=(226,184,150),hair=(60,44,32),hairstyle="short",shirt=(70,86,110),pants=(44,48,60),shoes=(30,26,24),sleeve="long")
HUNT2=dict(HUNT,hair=(180,110,50),hairstyle="ponytail",shirt=(120,70,70),skin=(236,196,160))
HUNT3=dict(HUNT,hair=(30,26,24),hairstyle="bun",shirt=(60,110,90),skin=(210,160,120),hat="headphones")
def torch(dd,x,y,a,s,K=1.0): dd.R(x-6*K,y-14*K,x+6*K,y+26*K,(60,60,70),4*K); dd.E(x,y+30*K,10*K,7*K,(255,240,180))
def vign_(img,k=.6): return Image.alpha_composite(img.convert("RGBA"),vignette_ov(img.size,k)).convert("RGB")
def ghost3(d,cam,st,x,z,u,hm=1.8,reach=0.0,tone=1.0):
    pl=place3(cam,st,x,z,hm)
    if pl: ghost(d,pl[0],pl[1],pl[2],u,reach=reach)
def window_tex(w=200,h=260):
    im=Image.new("RGB",(w,h),(18,26,50)); d=ImageDraw.Draw(im); d.rectangle([0,0,w-1,h-1],outline=(70,56,44),width=10); d.line([(w/2,0),(w/2,h)],fill=(70,56,44),width=6); d.line([(0,h*.55),(w,h*.55)],fill=(70,56,44),width=6)
    d.ellipse([140,30,170,60],fill=(220,230,255)); return im
def hallway(cam,u,extra=()):
    bg=render_room(cam,HALL,u,flick(u,.96),extra=[(.3,1.2,cam["z"]+.8,(1,.95,.8),1.1)]+list(extra)); return bg
def sceneA(u,final=False):
    t=u+(0 if not final else 3); cam=walk_cam(t,speed=.5); cam["pitch"]=.06+cam["pitch"]*.4; cam["y"]=1.6
    dz=cam["z"]+2.4; bg=hallway(cam,t,[(.4,1.2,dz,(1,.95,.8),1.4)]); big=fin(bg); d=D(big)
    ghost3(d,cam,HALL,0,dz+8,t,hm=1.9,reach=.3+.2*math.sin(t))
    o=P3(d,cam,HALL,cam["x"],dz,HUNT,dict(P_walk(t,2.0),ar=(1.2,1.6),curlR=.9),hm=1.7,u=t,facing="back",props={"r":torch},fog=(2,4,6))
    big=snow_particles(big,t,n=30,col=(200,210,230),sz=2,speed=-8,alpha=50,scale=2.2)
    return grade(vign_(big,.5),sat=.85,seed=int(u*30),tint=(.95,1.0,1.06))
def sceneB(u):
    cam=dict(x=lerp(-3,.4,sm(u/7)),y=1.5,z=lerp(-1,.4,sm(u/7)),yaw=lerp(.25,0,sm(u/7)),pitch=.05)
    ex=[(0,3.0,12,(.5,.6,1.0),1.0)]; bg=render_terrain(cam,NIGHT,u,extra=ex); ov=new_ov()
    house(ov,cam,NIGHT,0,16,w=14,d=8,h=6.0,wall=(120,116,110),seed=41,t=u,lit=.4); 
    house_front=ov
    # casa de frente (puerta al eje z): usamos caja y ventanas
    box(ov,cam,NIGHT,-3.4,3.4,0,5.4,17,21,(108,104,98)); poly3(ov,cam,NIGHT,[(-3.7,5.4,16.8),(3.7,5.4,16.8),(0,8.2,16.8)],(70,56,52))
    for k,x in enumerate((-2.2,2.2)): poly3(ov,cam,NIGHT,[(x-.6,1.2,16.98),(x+.6,1.2,16.98),(x+.6,2.5,16.98),(x-.6,2.5,16.98)],(255,196,110) if k else (20,26,44))
    poly3(ov,cam,NIGHT,[(-.5,0,16.98),(.5,0,16.98),(.5,2.2,16.98),(-.5,2.2,16.98)],(60,40,32)); poly3(ov,cam,NIGHT,[(-1.0,3.2,16.98),(1.0,3.2,16.98),(1.0,4.6,16.98),(-1.0,4.6,16.98)],(20,26,44))
    box(ov,cam,NIGHT,2.5,5.5,0,2.2,9,12,(220,222,226)); box(ov,cam,NIGHT,2.8,5.2,2.2,2.6,9.4,11.6,(190,192,198))
    big=fin(composite(bg,ov)); d=D(big)
    for k,(x,stl) in enumerate(((-1.4,HUNT),(0,HUNT2),(1.4,HUNT3))):
        o=P3(d,cam,NIGHT,x,6+k*.6+u*.4,stl,dict(P_walk(u,2.6,k),ar=(1.2,2.0)),hm=1.72,u=u,props={"r":torch},fog=(16,22,40))
    ptext(d,40,270,"2020",9,(255,255,255))
    return grade(vign_(big,.5),sat=.9,seed=int(u*30),tint=(.95,.99,1.05))
def sceneC(u):
    st=ROOMH; cam=dict(x=lerp(-.6,.2,sm(u/8)),y=1.3,z=lerp(-1.0,.4,sm(u/8)),yaw=lerp(.12,0,sm(u/8)),pitch=.06)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.1,2.4,(1,.9,.7),1.2)]); back=new_ov()
    box(back,cam,st,-1.4,1.4,0,.8,2.5,3.4,(96,70,48)); tquad(back,cam,st,(-1.0,2.2,4.99),(0,2.2,4.99),(0,1.0,4.99),(-1.0,1.0,4.99),window_tex()); glow(back,cam,st,(-.5,1.6,4.9),(160,190,255),1.2,50,5)
    # equipo: EMF, termometro, camara
    box(back,cam,st,-.9,-.7,.8,.98,2.7,3.0,(40,44,50)); 
    for k in range(5): box(back,cam,st,-.88,-.72,.82+k*.03,.84+k*.03,2.69,2.7,[(60,230,90),(60,230,90),(240,220,60),(240,220,60),(240,60,50)][k],emis=.5,shadow=False)
    box(back,cam,st,-.2,-.1,.8,1.1,2.7,2.78,(224,224,230)); box(back,cam,st,.3,.7,.8,.98,2.6,2.9,(34,34,40)); glow(back,cam,st,(.5,.9,2.6),(80,110,160),.4,60,3)
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,0,3.7,HUNT,dict(P_both(u,l=(.9,2.0),r=(.9,2.0),grip=.8),look=(0,.5),mouth=.2),hm=1.75,u=u,fog=(2,4,6))
    for k,t_ in enumerate(("EMF","TEMP","CAMARA")): ptext(d,60+k*160,830,t_,3.6,(255,255,255))
    return grade(vign_(big,.5),sat=.85,seed=int(u*30),tint=(.96,1.0,1.05))
def asr_tex(u,w=300,h=200):
    im=Image.new("RGB",(w,h),(8,14,12)); d=ImageDraw.Draw(im); G=(110,255,150); d.text((10,8),"RECONOCIMIENTO DE VOZ",font=mono(14,True),fill=G)
    for k in range(24): hh=6+abs(math.sin(k*.7+u*8))*50; d.rectangle([10+k*11,100-hh,10+k*11+6,100+hh],fill=G)
    txt="¿ESTAS AQUI?"; n=int(clamp(u/3.0)*len(txt)); d.text((10,160),"> "+txt[:n],font=mono(20,True),fill=(255,255,255)); return im
def sceneD(u):
    st=dict(ROOMH,fov=48); cam=dict(x=0,y=1.4,z=-.4,yaw=0,pitch=.04)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.2,2.6,(.4,1.0,.6),.9)]); back=new_ov()
    tquad(back,cam,st,(.3,2.2,4.99),(1.9,2.2,4.99),(1.9,1.0,4.99),(.3,1.0,4.99),crt(asr_tex(u),1.0,int(u*30))); glow(back,cam,st,(1.1,1.6,4.9),(110,255,150),1.0,50,5)
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,-.6,2.6,HUNT3,dict(P_talk(u),ar=(.9,1.3),mouth=.5+.5*math.sin(u*9)),hm=1.7,u=u,fog=(2,4,6))
    pl=place3(cam,st,.5,2.4,1.0,0)
    if pl: mic(d,pl[0],pl[1]-170*pl[2]*1.1,pl[2]*1.5); waves(d,pl[0],pl[1]-170*pl[2]*1.1,u,n=4,r0=60)
    ptext(d,40,270,"VOZ",12,(255,255,255))
    return grade(vign_(big,.5),sat=.85,seed=int(u*30),tint=(.96,1.0,1.04))
def sceneE(u):
    st=ROOMH; cam=dict(x=lerp(-.5,.3,sm(u/8)),y=1.5,z=lerp(-1.2,-.4,sm(u/8)),yaw=lerp(.1,-.05,sm(u/8)),pitch=.05)
    bg=render_room(cam,st,u,flick(u,.97),extra=[(-1,1.4,1.5,(1,.95,.8),.8)]); back=new_ov(); tquad(back,cam,st,(.6,2.2,4.99),(1.6,2.2,4.99),(1.6,1.0,4.99),(.6,1.0,4.99),window_tex())
    big=fin(composite(bg,back)); d=D(big)
    ghost3(d,cam,st,.9,3.6,u,hm=1.9,reach=.2)
    P3(d,cam,st,-.9,2.4,HUNT2,dict(P_talk(u),ar=(1.2,1.5)),hm=1.72,u=u,facing="back",props={"r":torch},fog=(2,4,6))
    t1=sm((u-.6)/.8); d.R(40,300,290,380,(255,255,255,int(230*t1)),10); ptext(d,54,320,"ESTAS AQUI?",3.4,(20,20,30))
    t2=sm((u-2.8)/.8); d.R(260,420,500,500,(180,200,255,int(230*t2)),10); ptext(d,276,442,"...",8,(10,10,20))
    return grade(vign_(big,.5),sat=.85,seed=int(u*30),tint=(.95,1.0,1.06))
def sceneF(u):
    t=u; cam=walk_cam(t,speed=2.2,sway=1.8); cam["pitch"]=.06; cam["y"]=1.6; dz=cam["z"]+lerp(5.0,3.5,clamp(u/6)); bg=hallway(cam,t,[(.3,1.2,dz,(1,.95,.8),1.4)]); big=fin(bg); d=D(big)
    P3(d,cam,HALL,cam["x"],dz,HUNT,dict(P_walk(t,6.5),al=(.8,1.4),ar=(1.2,1.6),mouth=1.0,tilt=.05*math.sin(t*3)),hm=1.7,u=t,facing="back",props={"r":torch},fog=(2,4,6))
    ghost3(d,cam,HALL,cam["x"]*0,cam["z"]+lerp(2.0,1.6,sm(u/6))+0,t,hm=2.0,reach=1.0)
    d.R(40,225,500,255,(255,255,255,40),8); d.R(40,225,40+460*(1-.7*clamp(u/6)),255,GRN+(230,),8); ptext(d,40,265,"CORDURA",3.4,(255,255,255))
    return grade(vign_(big,.6),sat=.8,seed=int(u*30),tint=(.95,1.0,1.06))
def sceneG(u):
    st=ROOMH; cam=dict(x=lerp(-.4,.4,sm(u/6)),y=1.5,z=lerp(-1.2,-.5,sm(u/6)),yaw=0,pitch=.05)
    bg=render_room(cam,st,u,1.0,extra=[(-1,1.4,1.5,(1,.95,.8),.7)]); back=new_ov(); box(back,cam,st,-.8,.8,0,2.0,4.8,4.95,(70,50,38)); poly3(back,cam,st,[(-.8,2.0,4.79),(.8,2.0,4.79),(.8,0,4.79),(-.8,0,4.79)],(30,22,18))
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,-.9,2.4,HUNT,dict(P_idle(u),ar=(1.9,2.8),mouth=.5+.5*math.sin(u*8),look=(.5,0)),hm=1.72,u=u,fog=(2,4,6))
    pl=place3(cam,st,-.9,2.4,1.7); 
    if pl: waves(d,pl[0]-20,pl[1]-170*pl[2],u,n=4,r0=60)
    ghost3(d,cam,st,.9,4.4,u,hm=1.8,reach=.3)
    return grade(vign_(big,.5),sat=.85,seed=int(u*30),tint=(.95,1.0,1.06))
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur): return 1.0,270,480
core.CAM=cam
if __name__=="__main__": core.main()
