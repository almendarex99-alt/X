import sys; sys.path.insert(0,"..")
from kit import *
from rooms import mk, render_room
from terrain import render_terrain, mk as tmk
from sets import *
STONE=mk(H=3.2,hw=1.4,wall="stone",wcol=(116,108,98),wcol2=(56,52,46),floor="flag",fcol=(88,82,76),ceil="vault",ccol=(70,66,60),ambient=.05,amb_rgb=(.8,.85,1.0),fog=.06,fogcol=(2,2,3),fov=56,open_p=.35,seg=7.0,D=3.0)
HALL=mk(H=4.2,hw=3.0,zend=7.0,zback=-3.0,wall="stone",wcol=(112,104,94),wcol2=(54,50,44),floor="flag",fcol=(84,78,72),ceil="beams",ccol=(60,56,50),ambient=.05,amb_rgb=(.8,.85,1.0),fog=.045,fogcol=(2,2,3),fov=56)
DAN=dict(skin=(226,184,150),hair=(60,44,32),hairstyle="short",shirt=(110,84,60),coat=(60,56,60),pants=(56,52,50),shoes=(36,28,24),sleeve="long",belt=(70,50,34),brow=(40,28,20))
MON=dict(skin=(110,100,90),hair=(60,50,44),hairstyle="bald",shirt=(70,60,56),coat=(60,52,48),pants=(60,54,50),shoes=(30,26,24),sleeve="long",claws=True,bulk=.95,height=1.2,face=False,ear=False,hands_col=(100,90,80),mask=lambda d,hx,hy,sc:(d.E(hx,hy,22*sc,30*sc,(130,120,106,255)),d.E(hx-6*sc,hy-5*sc,3*sc,4*sc,(255,210,90,255)),d.E(hx+6*sc,hy-5*sc,3*sc,4*sc,(255,210,90,255)),d.A(hx,hy+14*sc,10*sc,5*sc,10,170,(30,10,10,255),2*sc)))
def lantern(dd,x,y,a,s,K=1.0,t=0.0):
    fl=1+.12*math.sin(t*13)
    dd.L(x,y,x,y+10*K,(60,50,40,255),2*K); dd.R(x-9*K,y+10*K,x+9*K,y+38*K,(90,70,40,255),3*K); dd.R(x-6*K,y+13*K,x+6*K,y+35*K,(255,214,120,255),2*K)
    dd.E(x,y+24*K,14*K*fl,24*K*fl,(255,190,80,70)); dd.E(x,y+24*K,34*K*fl,50*K*fl,(255,170,60,30)); dd.P([(x-4*K,y+32*K),(x,y+18*K*fl),(x+4*K,y+32*K)],(255,240,170,255))
def lan_prop(t):
    def f(dd,x,y,a,s,K=1.0): lantern(dd,x,y,a,s,K,t)
    return f
def lan_light(x,y,z,t,I=3.2): return (x,y,z,(1.0,.72,.38),I*(1+.1*math.sin(t*13)))
def warp(img,amount,t,drift=0.0):
    a=np.asarray(img); H,W,_=a.shape; yy=np.arange(H); sh=(amount*np.sin(yy*.012+t*3.0)*40+amount*np.sin(yy*.05+t*7)*10).astype(int)
    idx=(np.arange(W)[None,:]-sh[:,None])%W; out=a[yy[:,None],idx]
    if amount>0.3: out[:,:,0]=np.roll(out[:,:,0],int(14*amount),axis=1); out[:,:,2]=np.roll(out[:,:,2],-int(14*amount),axis=1)
    return Image.fromarray(out)
def vign(img,k=.6):
    ov=vignette_ov(img.size,k); return Image.alpha_composite(img.convert("RGBA"),ov).convert("RGB")
def sceneA(u,final=False):
    t=u+(0 if not final else 3); cam=walk_cam(t,speed=.6); cam["pitch"]=.08+cam["pitch"]*.5; cam["y"]=1.6
    dz=cam["z"]+2.6; ex=[lan_light(cam["x"]+.32,1.1,dz-.15,t)]
    bg=render_room(cam,STONE,t,1.0,extra=ex); big=fin(bg); d=D(big)
    P3(d,cam,STONE,cam["x"],dz,DAN,dict(P_walk(t,2.2),ar=(.9,1.3),curlR=.9),hm=1.78,u=t,facing="back",props={"r":lan_prop(t)},tone=1.0,fog=(2,2,3))
    P3(d,cam,STONE,.1,dz+9+2*math.sin(t*.5),MON,dict(P_walk(t,1.8)),hm=2.1,u=t,fog=(2,2,3),tone=.7) if t>1.5 else None
    return grade(vign(big,.5),sat=.85,seed=int(u*30),tint=(1.0,.98,.95))
def castle(ov,cam,st,x,z,t):
    box(ov,cam,st,x-14,x+14,0,16,z,z+12,(86,80,84)); 
    for (tx,h) in ((-14,24),(14,24),(-7,20),(7,20)):
        box(ov,cam,st,x+tx-3,x+tx+3,0,h,z-2,z+6,(82,76,80)); poly3(ov,cam,st,[(x+tx-3.6,h,z-2.6),(x+tx+3.6,h,z-2.6),(x+tx,h+8,z+2)],(40,38,44))
    for r in range(3):
        for c in range(9):
            on=((r*5+c*3)%7)>2; poly3(ov,cam,st,[(x-12+c*3,3+r*4.5,z-.02),(x-10.8+c*3,3+r*4.5,z-.02),(x-10.8+c*3,5.2+r*4.5,z-.02),(x-12+c*3,5.2+r*4.5,z-.02)],(255,190,100) if on else (20,24,38))
def sceneB(u):
    st=tmk(fov=54,ground="grass",sky="night",fog=.012,fogcol=(18,24,44),hills=.05,hcol=(16,22,40),amb=(.24,.3,.5),ambient=1.0)
    cam=dict(x=lerp(-12,6,sm(u/9)),y=2.2,z=lerp(-8,-6,sm(u/9)),yaw=lerp(.35,-.05,sm(u/9)),pitch=.08)
    bg=render_terrain(cam,st,u); ov=new_ov(); castle(ov,cam,st,0,40,u)
    big=fin(composite(bg,ov)); d=D(big); big=snow_particles(big,u,n=40,col=(170,180,200),sz=2,speed=30,alpha=60,scale=2.2)
    return grade(vign(big,.4),sat=.9,seed=int(u*30),tint=(.95,.98,1.06))
def sceneC(u):
    cam=walk_cam(u+4,speed=.0); cam["pitch"]=.08; cam["x"]=0; cam["z"]=0
    dz=lerp(5.0,3.4,sm(u/5)); ex=[lan_light(.3,1.1,dz-.15,u),lan_light(-.1,1.5,dz-3.5,u,1.0)]
    bg=render_room(cam,STONE,u,1.0,extra=ex); big=fin(bg); d=D(big)
    P3(d,cam,STONE,.0,dz,DAN,dict(P_walk(u,6.0),al=(.9,1.3),ar=(.9,1.3),mouth=1.0,tilt=-.06),hm=1.78,u=u,facing="back",props={"r":lan_prop(u)},fog=(2,2,3))
    P3(d,cam,STONE,.0,dz+4.5-clamp(u/6)*1.2,MON,dict(P_walk(u,3.0)),hm=2.1,u=u,fog=(2,2,3),tone=.85)
    return grade(vign(big,.5),sat=.85,seed=int(u*30),tint=(1.0,.98,.95))
def sanity(img,level):
    ov=Image.new("RGBA",img.size,(0,0,0,0)); d=ImageDraw.Draw(ov); d.rounded_rectangle([60,2380,560,2440],radius=24,fill=(0,0,0,170))
    d.rounded_rectangle([70,2390,70+int(480*level),2430],radius=18,fill=(220,60,60,230)); d.text((70,2330),"CORDURA",font=font(46,True),fill=(255,255,255,235))
    return Image.alpha_composite(img.convert("RGBA"),ov).convert("RGB")
def sceneD(u):
    cam=dict(x=0,y=1.6,z=0,yaw=0,pitch=.08); ex=[lan_light(.3,1.1,3.3,u,2.2)]
    bg=render_room(cam,STONE,u,1.0,extra=ex); big=fin(bg); d=D(big)
    P3(d,cam,STONE,.0,3.4,DAN,dict(P_idle(u),ar=(.9,1.3),tilt=.05*math.sin(u*2)),hm=1.78,u=u,facing="back",props={"r":lan_prop(u)},fog=(2,2,3))
    P3(d,cam,STONE,.0,11+math.sin(u),MON,dict(P_idle(u)),hm=2.1,u=u,fog=(2,2,3),tone=.5)
    big=vign(big,.8); big=sanity(big,max(.15,1-u/9.0))
    return grade(big,sat=.7,seed=int(u*30),tint=(.98,.98,1.0))
def sceneE(u):
    cam=dict(x=0,y=1.6,z=0,yaw=.05*math.sin(u),pitch=.08); ex=[lan_light(.3,1.1,3.3,u,1.8)]
    bg=render_room(cam,STONE,u,1.0,extra=ex); big=fin(bg); d=D(big)
    P3(d,cam,STONE,.0,3.4,DAN,dict(P_scared(u),ar=(.8,1.9),al=(.8,1.9)),hm=1.78,u=u,facing="back",fog=(2,2,3))
    for k,(x,z,a) in enumerate(((-1.0,7,.6),(1.0,9,.5),(.0,14,.4))): P3(d,cam,STONE,x,z+math.sin(u*2+k),MON,dict(P_idle(u,k)),hm=2.1,u=u,fog=(2,2,3),tone=a)
    amt=clamp(u/3.0)*1.2+.3; big=warp(big,amt,u); big=vign(big,.8); big=sanity(big,.2)
    return grade(big,sat=.6,seed=int(u*30),tint=(1.0,.94,.94))
def sceneF(u):
    cam=dict(x=0,y=1.1,z=lerp(0,.8,sm(u/6)),yaw=0,pitch=.05); ex=[lan_light(.0,.6,3.0,u,1.2*max(.3,1-u/8))]
    bg=render_room(cam,STONE,u,1.0,extra=ex); big=fin(bg); d=D(big)
    P3(d,cam,STONE,.0,3.2,DAN,dict(P_scared(u),ar=(.8,2.5),al=(.8,2.5)),hm=1.4,u=u,y0=0,fog=(2,2,3),bust=False)
    m=clamp((u-1.0)/5); P3(d,cam,STONE,.0,lerp(14,6,m),MON,dict(P_walk(u,2.0)),hm=2.1,u=u,fog=(2,2,3),tone=.8)
    return grade(vign(big,.8),sat=.75,seed=int(u*30),tint=(1.0,.96,.92))
def sceneG(u):
    st=dict(STONE,fov=44); cam=dict(x=0,y=1.3,z=0,yaw=.15*math.sin(u*.4),pitch=.0); fl=1+.12*math.sin(u*13)
    ex=[(.2,1.3,.6,(1.0,.72,.38),3.0*fl)]
    bg=render_room(cam,st,u,1.0,extra=ex); big=fin(bg); d=D(big)
    hand3(d,cam,st,(.2,1.05,.6),hand_m=.2,a=3.14,s=1,curl=.9,spread=.4,arm_from=(360,1.2),arm_w=.08,sleeve=(60,56,60),prop=lan_prop(u)) 
    return grade(vign(big,.6),sat=.85,seed=int(u*30),tint=(1.02,.98,.94))
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur): return 1.0,270,480
core.CAM=cam
if __name__=="__main__": core.main()
