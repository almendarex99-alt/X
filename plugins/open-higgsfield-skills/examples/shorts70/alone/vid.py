import sys; sys.path.insert(0,"..")
from kit import *
from rooms import mk, render_room
from terrain import render_terrain, mk as tmk
from sets import *
GOTH=mk(H=4.2,hw=3.2,zend=8.0,zback=-3.0,wall="wood",wcol=(86,56,36),floor="wood",fcol=(76,52,36),ceil="beams",ccol=(56,40,30),ambient=.10,amb_rgb=(.8,.85,1),fog=.03,fogcol=(4,4,8),fov=54,
         plights=dict(gap=5,off=1,xs=(-2.8,2.8),y=2.4,rgb=(1,.7,.4),I=.8,k=.4))
OFFD=mk(H=2.7,hw=2.4,zend=4.4,zback=-2.6,wall="plaster",wcol=(190,186,176),floor="carpet",fcol=(84,86,98),ceil="tile",ccol=(206,204,196),ambient=.24,amb_rgb=(.92,.96,1),fov=52,fog=.012,plights=dict(gap=2.4,off=0,xs=(0,),y=2.55,rgb=(.9,.96,1),I=.4,k=.5))
NIGHTT=tmk(fov=54,ground="grass",sky="night",fog=.018,fogcol=(14,18,32),hills=.05,hcol=(10,14,26),amb=(.26,.32,.5),ambient=1.0)
HERO=dict(skin=(230,190,156),hair=(60,44,32),hairstyle="short",shirt=(180,160,120),coat=(110,84,56),pants=(60,52,48),shoes=(40,30,26),sleeve="long",belt=(70,50,40),brow=(40,28,20))
HEROINE=dict(skin=(240,200,166),hair=(120,70,40),hairstyle="long",shirt=(60,80,120),dress=True,skirt_col=(70,92,134),sleeve="long",shoes=(40,30,30))
DEVA=dict(skin=(232,192,156),hair=(40,30,24),hairstyle="short",glasses=True,shirt=(70,100,150),pants=(60,60,76),sleeve="long",beard=True)
def mon_deco(d,hx,hy,sc):
    for sg in(-1,1): d.E(hx+sg*8.5*sc,hy-3*sc,11*sc,9*sc,(255,60,40,60))
MONST=dict(skin=(80,110,66),hair=(60,80,50),hairstyle="bald",shirt=(70,100,60),pants=(56,80,50),shoes=(40,50,36),claws=True,eyes=(255,60,40),sleeve="none",bulk=1.2,ear=False,brow=(20,30,20),mouth_col=(60,10,10),tail=(80,110,66))
def torch(dd,x,y,a,s,K=1.0): dd.R(x-6*K,y-12*K,x+6*K,y+26*K,(60,60,70),4*K); dd.E(x,y+30*K,10*K,7*K,(255,240,180))
def vign_(img,k=.5): return Image.alpha_composite(img.convert("RGBA"),vignette_ov(img.size,k)).convert("RGB")
def mansion(ov,cam,st,x,z,t):
    box(ov,cam,st,x-10,x+10,0,9,z,z+8,(40,34,44)); poly3(ov,cam,st,[(x-11,9,z-.6),(x+11,9,z-.6),(x,15,z+4)],(26,22,30))
    box(ov,cam,st,x-3,x+3,0,13,z-1,z+3,(36,30,40)); poly3(ov,cam,st,[(x-3.6,13,z-1.6),(x+3.6,13,z-1.6),(x,18,z+1)],(22,18,26))
    for r in range(2):
        for c in range(6):
            on=((r*3+c*2)%5)>1; poly3(ov,cam,st,[(x-9+c*3.2,2+r*3.6,z-.02),(x-8+c*3.2,2+r*3.6,z-.02),(x-8+c*3.2,4.4+r*3.6,z-.02),(x-9+c*3.2,4.4+r*3.6,z-.02)],(255,190,100) if on else (16,18,30))
    poly3(ov,cam,st,[(x-1,0,z-1.02),(x+1,0,z-1.02),(x+1,3,z-1.02),(x-1,3,z-1.02)],(70,40,30))
def sceneA(u,final=False):
    t=u+(0 if not final else 3); cam=dict(x=lerp(-3,1,sm(t/7)),y=1.6,z=lerp(0,3,sm(t/7)),yaw=lerp(.2,-.03,sm(t/7)),pitch=.08)
    bg=render_terrain(cam,NIGHTT,t); ov=new_ov(); mansion(ov,cam,NIGHTT,0,24,t)
    for k,(x,z) in enumerate(((-6,12),(6,14),(-9,18),(9,20))): tree(ov,cam,NIGHTT,x,z,h=5,col=(16,40,26),trunk=(30,24,20))
    big=fin(composite(bg,ov)); d=D(big)
    if (t%4.0)<.12: d.R(0,0,540,960,(255,255,255,int(150*(1-(t%4.0)/.12))),0)
    P3(d,cam,NIGHTT,-1.0+u*.1,cam["z"]+5,HERO,P_walk(t,2.4),hm=1.75,u=t,facing="back",props={"r":torch},fog=(14,18,32))
    big=snow_particles(big,t,n=40,col=(170,180,200),sz=2,speed=30,alpha=60,scale=2.2)
    return grade(vign_(big,.5),sat=.9,seed=int(u*30),tint=(.95,.98,1.06))
def pc_tex(u,w=320,h=200):
    im=Image.new("RGB",(w,h),(20,24,40)); d=ImageDraw.Draw(im); d.polygon([(0,0),(w,0),(w*.7,h*.3),(w*.3,h*.3)],fill=(70,50,40)); d.rectangle([0,h*.3,w,h],fill=(90,60,44)); d.polygon([(w*.3,h*.3),(w*.7,h*.3),(w,h),(0,h)],fill=(60,40,30))
    x=int(w*.5+math.sin(u*2)*30); d.polygon([(x-14,h-20),(x+14,h-20),(x+10,h*.5),(x-10,h*.5)],fill=(180,160,120)); d.ellipse([x-8,h*.38,x+8,h*.52],fill=(230,190,156)); d.text((8,6),"ALONE",font=mono(12,True),fill=(250,250,250)); return im
def sceneB(u):
    st=OFFD; cam=dict(x=lerp(-1,.3,sm(u/9)),y=1.4,z=lerp(-.6,.5,sm(u/9)),yaw=lerp(.2,0,sm(u/9)),pitch=.05)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.4,3.0,(.5,.7,1),.8)]); back=new_ov()
    box(back,cam,st,-1.2,1.2,0,.74,2.4,3.2,(130,100,76)); box(back,cam,st,-.4,.4,.74,1.28,2.55,3.05,(206,200,184)); tquad(back,cam,st,(-.32,1.23,2.545),(.32,1.23,2.545),(.32,.83,2.545),(-.32,.83,2.545),crt(pc_tex(u),1.0,int(u*30))); glow(back,cam,st,(0,1.0,2.4),(140,170,255),.9,50,5)
    fl=Image.new("RGB",(150,100)); fd=ImageDraw.Draw(fl); fd.rectangle([0,0,50,100],fill=(0,40,150)); fd.rectangle([50,0,100,100],fill=(240,240,244)); fd.rectangle([100,0,150,100],fill=(220,30,50))
    tquad(back,cam,st,(1.2,2.4,4.39),(2.2,2.4,4.39),(2.2,1.7,4.39),(1.2,1.7,4.39),fl)
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,1.2,3.4,DEVA,dict(P_talk(u),al=(1.3,2.0),ar=(.2,.3)),hm=1.78,u=u,fog=(20,24,30)); ptext(d,40,270,"1992",9,(255,255,255)); ptext(d,40,340,"FRANCIA",5,(255,214,120))
    return grade(vign_(big,.3),sat=.95,seed=int(u*30),tint=(.98,1.0,1.04))
def hall(cam,u,extra=()):
    st=GOTH; bg=render_room(cam,st,u,flick(u,.97),extra=list(extra)); back=new_ov()
    box(back,cam,st,2.2,3.0,0,2.2,5.5,6.2,(80,50,32)); tquad(back,cam,st,(-2.9,2.8,7.99),(-1.2,2.8,7.99),(-1.2,.3,7.99),(-2.9,.3,7.99),tex_window(night=True,curtains=(100,40,40)))
    for x in (-2.8,2.8): box(back,cam,st,x-.1,x+.1,0,.5,3,3.2,(60,50,44),shadow=False); glow(back,cam,st,(x,2.4,3.1),(255,170,90),1.2,70,5)
    return st,bg,back
def sceneC(u):
    cam=dict(x=lerp(-1.4,0,sm(u/8)),y=1.55,z=lerp(-2.4,-1.2,sm(u/8)),yaw=lerp(.15,0,sm(u/8)),pitch=.06)
    st,bg,back=hall(cam,u,[(0,1.2,1.5,(1,.8,.5),1.0)]); big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,-.4,2.6,HERO,dict(P_walk(u,2.6),ar=(1.3,2.0)),hm=1.78,u=u,props={"r":torch},fog=(6,4,6)); P3(d,cam,st,1.2,3.2,HEROINE,P_walk(u,2.6,1.4),hm=1.68,u=u,fog=(6,4,6))
    ptext(d,40,270,"MANSION",7,(255,255,255))
    return grade(vign_(big,.5),sat=.9,seed=int(u*30),tint=(1.03,.98,.94))
def sceneD(u):
    cam=dict(x=lerp(-1.4,0,sm(u/8)),y=1.55,z=lerp(-2.4,-1.4,sm(u/8)),yaw=lerp(.15,0,sm(u/8)),pitch=.06)
    st,bg,back=hall(cam,u,[(0,1.2,1.5,(1,.8,.5),1.0)]); big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,-.4,2.6,HERO,dict(P_walk(u,3.2),ar=(1.2,2.0)),hm=1.78,u=u,props={"r":torch},fog=(6,4,6)); P3(d,cam,st,1.4,3.4,MONST,P_zombie(u,0,1.8),hm=2.0,u=u,fog=(6,4,6),deco=mon_deco)
    d.R(20,240,260,300,(0,0,0,150),8); ptext(d,34,256,"POLIGONOS",3.8,(255,214,120)); d.R(280,240,520,300,(0,0,0,150),8); ptext(d,294,256,"FONDO DIBUJADO",2.8,(255,255,255))
    return grade(vign_(big,.5),sat=.9,seed=int(u*30),tint=(1.03,.98,.94))
def sceneE(u):
    p=int(u*.5)%2; cam=dict(x=-1.8,y=2.2,z=-2.4,yaw=.5,pitch=.22) if p==0 else dict(x=1.8,y=1.4,z=1.0,yaw=-.5,pitch=.04)
    st,bg,back=hall(cam,u,[(0,1.2,1.5,(1,.8,.5),1.0)]); big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,-.4+(.6 if p else 0),2.6,HERO,dict(P_walk(u,2.4),ar=(1.3,2.0)),hm=1.78,u=u,props={"r":torch},fog=(6,4,6))
    d.R(0,0,540,960,None,0,(255,255,255,60),6); ptext(d,40,270,"CAMARA FIJA",5,(255,255,255))
    if int(u*1.2)%2==0: d.E(60,330,8,8,(240,50,50))
    return grade(vign_(big,.5),sat=.9,seed=int(u*30),tint=(1.03,.98,.94))
def sceneF(u):
    cam=dict(x=lerp(-1,.4,sm(u/7)),y=1.55,z=-1.8,yaw=lerp(.15,-.03,sm(u/7)),pitch=.06)
    st,bg,back=hall(cam,u,[(0,1.2,1.5,(1,.8,.5),1.0)]); box(back,cam,st,-1.0,1.0,0,.8,1.6,2.4,(120,90,50)); glow(back,cam,st,(0,1.4,2.0),(255,214,90),1.2,80,6)
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,0,3.0,HERO,dict(P_cheer(u),ar=(2.4,2.8),al=(.9,1.2)),hm=1.78,u=u,fog=(6,4,6)); ptext(d,230,330,"1",14,(255,214,70)); ptext(d,40,270,"PIONERO",8,(255,255,255))
    return grade(vign_(big,.5),sat=.9,seed=int(u*30),tint=(1.04,.98,.92))
def sceneG(u):
    cam=dict(x=lerp(-1,.6,sm(u/6)),y=1.5,z=lerp(-1.6,-.8,sm(u/6)),yaw=lerp(.15,-.05,sm(u/6)),pitch=.06)
    st,bg,back=hall(cam,u,[(0,1.2,1.5,(1,.8,.5),1.0)]); big=fin(composite(bg,back)); d=D(big)
    d.R(40,320,200,400,(50,50,60),8); ptext(d,70,350,"1992",3.6,(255,214,120))
    for k in range(3): d.R(230+k*90,420+k*60,310+k*90,500+k*60,(120,40,40),6); ptext(d,246+k*90,446+k*60,"RE",5,(255,255,255))
    d.L(200,360,240,430,(255,255,255,140),4)
    P3(d,cam,st,-.5,3.0,HERO,dict(P_point(u),ar=(1.6,1.6)),hm=1.78,u=u,fog=(6,4,6))
    return grade(vign_(big,.5),sat=.9,seed=int(u*30),tint=(1.03,.98,.94))
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur): return 1.0,270,480
core.CAM=cam
if __name__=="__main__": core.main()
