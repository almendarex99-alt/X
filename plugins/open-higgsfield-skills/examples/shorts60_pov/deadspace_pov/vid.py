import sys; sys.path.insert(0,"..")
from kit import *
from rooms import mk, render_room
from creatures import claw_arm
from sets import *
SHIP=mk(H=3.0,hw=1.5,wall="metal",wcol=(98,106,116),floor="grate",fcol=(72,76,82),ceil="pipes",ccol=(60,64,70),ambient=.16,amb_rgb=(.7,.85,1.0),hazard=True,fog=.035,fogcol=(6,8,12),fov=56,strip=(120,190,255),
        plights=dict(gap=5,off=1.5,xs=(0,),y=2.8,rgb=(.8,.92,1.0),I=1.2,flk=.9,flp=.25,k=.4))
ROOM=mk(H=3.4,hw=3.2,zend=6.0,zback=-3.0,wall="metal",wcol=(92,98,108),floor="grate",fcol=(66,70,76),ceil="pipes",ccol=(56,60,66),ambient=.16,amb_rgb=(.7,.85,1.0),hazard=True,fog=.03,fogcol=(6,8,12),fov=54,strip=(110,180,255),
        plights=dict(gap=4,off=2,xs=(-1.5,1.5),y=3.2,rgb=(.8,.92,1.0),I=.9,flk=.9,flp=.2,k=.4))
def helmet(d,hx,hy,sc):
    d.E(hx,hy,25*sc,28*sc,(190,194,200,255)); d.E(hx,hy-2*sc,19*sc,22*sc,(28,32,38,255)); d.E(hx-6*sc,hy-8*sc,8*sc,10*sc,(120,170,230,160)); d.R(hx-9*sc,hy+16*sc,hx+9*sc,hy+28*sc,(150,154,160,255),3*sc)
SUIT=dict(skin=(150,154,160),hair=(150,154,160),hairstyle="bald",shirt=(140,146,154),pants=(120,126,134),shoes=(60,64,70),sleeve="long",bulk=1.35,height=1.05,face=False,ear=False,mask=helmet,hands_col=(86,90,96),belt=(200,150,50),neck_col=(120,126,134))
def spine_deco(level,t):
    def f(d,hx,hy,sc):
        for k in range(9):
            on=k<int(level*9)+1; col=(70,190,255) if on else (24,40,60)
            y=hy+32*sc+k*8.6*sc
            d.R(hx-3.2*sc,y,hx+3.2*sc,y+6*sc,col+(255,),2*sc)
            if on: d.E(hx,y+3*sc,12*sc,7*sc,(70,190,255,40))
        d.L(hx,hy+30*sc,hx,hy+110*sc,(200,150,50,160),1.2*sc)
    return f
NEC=dict(skin=(150,140,120),hair=(120,110,96),hairstyle="bald",shirt=(130,120,100),pants=(110,100,86),shoes=(70,60,50),sleeve="none",claws=True,bulk=.9,height=1.15,face=False,ear=False,mask=lambda d,hx,hy,sc:(d.E(hx,hy,22*sc,30*sc,(160,150,128,255)),d.E(hx-6*sc,hy-4*sc,3*sc,4*sc,(255,200,60,255)),d.E(hx+6*sc,hy-4*sc,3*sc,4*sc,(255,200,60,255))),hands_col=(120,110,92),neck_col=(120,110,92))
def holo_tex(u,items=4,w=300,h=360):
    im=Image.new("RGBA",(w,h),(40,170,255,40)); d=ImageDraw.Draw(im); d.rectangle([0,0,w-1,h-1],outline=(120,210,255,230),width=3); d.rectangle([0,0,w,34],fill=(60,180,255,120)); d.text((12,6),"INVENTARIO",font=mono(18,True),fill=(220,245,255,255))
    names=["BOTIQUIN","MUNICION","NODO","TRAJE","LLAVE","ARMA"]
    for k in range(items):
        x=14+(k%2)*140; y=50+(k//2)*100; d.rectangle([x,y,x+130,y+88],outline=(120,210,255,200),fill=(60,180,255,60),width=2); d.text((x+8,y+60),names[k],font=mono(13),fill=(220,245,255,255)); d.ellipse([x+40,y+10,x+90,y+50],outline=(180,230,255,220),width=3)
    for k in range(int(h/6)): d.line([(0,k*6),(w,k*6)],fill=(0,0,0,40))
    return im
def plasma(dd,x,y,a,s,K=1.0):
    dd.R(x-5*K,y-6*K,x+5*K,y+34*K,(70,74,80,255),3*K); dd.R(x-3*K,y-34*K,x+3*K,y-6*K,(110,114,120,255),2*K); dd.R(x-12*K,y-34*K,x+12*K,y-26*K,(70,74,80,255),2*K); dd.E(x,y-30*K,5*K,5*K,(255,150,40,255))
def scene_ship(cam,u,st=SHIP,fl=1.0): return render_room(cam,st,u,fl)
def sceneA(u,final=False):
    t=u+(0 if not final else 3); cam=walk_cam(t,speed=.8); cam["pitch"]=.09+cam["pitch"]*.5; cam["y"]=1.62
    bg=render_room(cam,SHIP,t,flick(t)); big=fin(bg); d=D(big)
    o=P3(d,cam,SHIP,cam["x"]+.0,cam["z"]+2.6,SUIT,dict(P_walk(t,2.6),ar=(1.0,1.9),curlR=.9),hm=1.85,u=t,facing="back",deco=spine_deco(.8-.15*math.sin(t),t),props={"r":plasma},fog=(6,8,12),tone=1.0)
    for k in range(6): 
        a=((t*.5+k*.17)%1); d.E(110+k*60,300+a*30,(8+a*40),(6+a*24),(220,230,240,int(90*(1-a))))
    return grade(big,sat=.9,seed=int(u*30),tint=(.95,1.0,1.08))
def ship_exterior(u):
    st=dict(SHIP); im=Image.new("RGB",(RW,RH),(4,6,12)); rng=np.random.default_rng(3); d=ImageDraw.Draw(im)
    for k in range(260): x=rng.random()*RW; y=rng.random()*RH; r=rng.random()*1.8; d.ellipse([x-r,y-r,x+r,y+r],fill=(180+int(rng.random()*70),)*3)
    d.ellipse([-300,820,560,1700],fill=(34,58,96)); d.ellipse([-280,840,540,1680],fill=(60,96,150)); d.ellipse([-200,900,380,1500],fill=(90,126,180))
    return im
def sceneB(u):
    cam=dict(x=0,y=0,z=0,yaw=0,pitch=0); st=dict(SHIP,fov=56); bg=ship_exterior(u); ov=new_ov()
    cam=dict(x=lerp(-9,-5,sm(u/8)),y=1.5,z=-30,yaw=lerp(.15,.05,sm(u/8)),pitch=.05)
    box(ov,cam,st,-6,6,-1.2,1.2,0,34,(120,126,134),lt=(1,1,1.05)); box(ov,cam,st,-3,3,1.2,3.4,6,22,(104,110,120)); box(ov,cam,st,-9,-6,-.7,.7,4,12,(96,102,110)); box(ov,cam,st,6,9,-.7,.7,14,26,(96,102,110))
    for k in range(10): poly3(ov,cam,st,[(-6.01,.6,2+k*3),(-6.01,.6,3+k*3),(-6.01,.1,3+k*3),(-6.01,.1,2+k*3)],(255,200,110))
    glow(ov,cam,st,(0,0,34),(120,180,255),3,90,6)
    big=fin(composite(bg,ov)); d=D(big)
    return grade(big,sat=.95,seed=int(u*30),tint=(.95,1.0,1.06))
def sceneC(u):
    cam=walk_cam(u+7,speed=.0); cam["pitch"]=.09; st=SHIP; bg=render_room(cam,st,u,flick(u)); big=fin(bg); d=D(big)
    o=P3(d,cam,st,.0,3.2,SUIT,dict(P_idle(u),ar=(.3,.5)),hm=1.85,u=u,facing="back",deco=spine_deco(.8,u),fog=(6,8,12))
    # interfaz tradicional tachada
    d.R(30,230,330,300,(20,20,28,200),8); ptext(d,44,246,"VIDA 100",4,(255,80,80)); d.L(30,230,330,300,(255,60,60,255),6); d.L(30,300,330,230,(255,60,60,255),6)
    d.R(30,330,200,380,(20,20,28,200),8); ptext(d,44,344,"MENU",4,(255,80,80)); d.L(30,330,200,380,(255,60,60,255),6); d.L(30,380,200,330,(255,60,60,255),6)
    return grade(big,sat=.9,seed=int(u*30),tint=(.95,1.0,1.08))
def sceneD(u):
    cam=dict(x=lerp(.5,-.3,sm(u/9)),y=1.55,z=lerp(-.2,.9,sm(u/9)),yaw=lerp(-.1,.1,sm(u/9)),pitch=.1); st=dict(SHIP,fov=46)
    bg=render_room(cam,st,u,flick(u)); big=fin(bg); d=D(big)
    lvl=.9-.08*u
    o=P3(d,cam,st,cam["x"]+.0,cam["z"]+1.9,SUIT,dict(P_idle(u),ar=(.3,.5)),hm=1.85,u=u,facing="back",deco=spine_deco(lvl,u),fog=(6,8,12))
    return grade(big,sat=.9,seed=int(u*30),tint=(.95,1.0,1.08))
def sceneE(u):
    cam=dict(x=-.2,y=1.5,z=lerp(-1.0,-.4,sm(u/8)),yaw=.1*math.sin(u*.4),pitch=.08); st=ROOM
    bg=render_room(cam,st,u,flick(u),extra=[(0,1.4,1.4,(.4,.7,1.0),1.1)]); back=new_ov()
    ph=sm(clamp((u-1.0)/1.0)); w=1.6; hh=1.9*ph
    tquad(back,cam,st,(-.1-.2,1.9+.3,1.6),(1.4,1.9+.3,1.6),(1.4,1.9+.3-hh,1.6),(-.2,1.9+.3-hh,1.6),holo_tex(u)) if ph>.05 else None
    glow(back,cam,st,(.6,1.5,1.6),(80,190,255),1.2,60,5)
    big=fin(composite(bg,back)); d=D(big)
    def holo_ammo(dd,x,y,a,s,K=1.0): 
        plasma(dd,x,y,a,s,K); dd.R(x-34*K,y-76*K,x+34*K,y-48*K,(20,60,90,180),5*K); ptext(dd,x-28*K,y-70*K,"%02d"%(30-int(u*1.4)%30),4.0*K,(120,220,255))
    P3(d,cam,st,-.8,3.0,SUIT,dict(P_hold(u,r=(1.15,1.5)),curlR=1.0),hm=1.85,u=u,props={"r":holo_ammo},fog=(6,8,12))
    return grade(big,sat=.9,seed=int(u*30),tint=(.95,1.0,1.08))
def sceneF(u):
    cam=dict(x=.0,y=1.5,z=lerp(-1.2,-.2,sm(u/8)),yaw=.0,pitch=.08); st=ROOM
    bg=render_room(cam,st,u,flick(u),extra=[(0,1.4,1.6,(.4,.7,1.0),1.1)]); back=new_ov()
    tquad(back,cam,st,(-.6,2.1,2.0),(.8,2.1,2.0),(.8,.6,2.0),(-.6,.6,2.0),holo_tex(u,items=4))
    big=fin(composite(bg,back)); d=D(big)
    # monstruo que sale del conducto mientras busca en el inventario
    mz=lerp(10.0,4.6,sm((u-1.5)/4.0)); P3(d,cam,st,2.0,mz,NEC,dict(P_zombie(u,0,2.6),mouth=1.0),hm=2.1,u=u,fog=(6,8,12))
    P3(d,cam,st,-.8,2.9,SUIT,dict(P_hold(u,r=(1.15,1.5)),curlR=1.0),hm=1.85,u=u,facing="back",deco=spine_deco(.8-.1*max(0,u-4),u),fog=(6,8,12))
    return grade(big,sat=.9,seed=int(u*30),tint=(.95,1.0,1.08))
def sceneG(u):
    cam=walk_cam(u+12,speed=.7); cam["pitch"]=.1+cam["pitch"]*.5; cam["y"]=1.62
    bg=render_room(cam,SHIP,u,flick(u)); big=fin(bg); d=D(big)
    P3(d,cam,SHIP,cam["x"],cam["z"]+3.0+u*.25,SUIT,dict(P_walk(u,2.6),ar=(1.0,1.9),curlR=.9),hm=1.85,u=u,facing="back",deco=spine_deco(.9,u),props={"r":plasma},fog=(6,8,12))
    return grade(big,sat=.9,seed=int(u*30),tint=(.95,1.0,1.08))

def sceneF(u):
    cam=dict(x=.1*math.sin(u*.5),y=3.0,z=lerp(-1.6,-.9,sm(u/8)),yaw=.02*math.sin(u*.7),pitch=.30); st=ROOM
    bg=render_room(cam,st,u,flick(u),extra=[(0,1.4,1.6,(.4,.7,1.0),1.1)]); back=new_ov()
    tquad(back,cam,st,(-.6,2.1,2.0),(.8,2.1,2.0),(.8,.6,2.0),(-.6,.6,2.0),holo_tex(u,items=4))
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,-.8,2.9,SUIT,dict(P_hold(u,r=(1.15,1.5)),curlR=1.0),hm=1.85,u=u,facing="back",deco=spine_deco(.8-.1*max(0,u-4),u),fog=(6,8,12))
    ov=Image.new("RGBA",big.size,(0,0,0,0)); od=ImageDraw.Draw(ov); od.rectangle([0,0,1620,2880],fill=(4,6,8,255))
    for k in range(12): y0=int(160+k*210); od.rectangle([100,y0,1520,y0+130],fill=(0,0,0,0))
    ov=ov.filter(ImageFilter.GaussianBlur(1.2)); big=Image.alpha_composite(big.convert("RGBA"),ov).convert("RGB"); d=D(big)
    monster_arms(d,u,tone=(176,164,140),still=True,size=1.5,reach=.15+.5*clamp((u-3.0)/4.0),claw=True)
    big=tint(big,(.9,1.1,.95),.8); big=pov_vignette(big,.8,(0,10,10))
    return grade(big,sat=.85,seed=int(u*30),tint=(.95,1.0,1.05))
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur): return 1.0,270,480
core.CAM=cam
if __name__=="__main__": core.main()
