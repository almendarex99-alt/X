import sys; sys.path.insert(0,"..")
from creatures import *
from kit import *
from rooms import mk, render_room
from terrain import render_terrain, mk as tmk
from sets import *
JUN=tmk(fov=54,ground="meadow",sky="dusk",fog=.02,fogcol=(60,80,70),hills=.06,hcol=(24,50,40),amb=(.55,.7,.6),ambient=.8)
SAV=tmk(fov=54,ground="meadow",sky="day",fog=.01,fogcol=(206,224,246),hills=.05,hcol=(110,140,120),amb=(1,1,.96),ambient=1.0)
STUDIO=mk(H=3.0,hw=3.0,zend=5.0,zback=-3.0,wall="wood",wcol=(70,56,46),floor="carpet",fcol=(50,46,56),ceil="plaster",ccol=(60,56,60),ambient=.14,amb_rgb=(1,.9,.8),fov=52,fog=.015,fogcol=(6,6,8),
              plights=dict(gap=100,off=1,xs=(0,),y=2.6,rgb=(1,.82,.6),I=.6,k=.4))
ENG=dict(skin=(230,188,150),hair=(90,70,50),hairstyle="short",beard=True,glasses=True,shirt=(120,150,170),pants=(60,64,80),hat="headphones",sleeve="short")
DIRX=dict(skin=(234,194,160),hair=(70,56,44),hairstyle="short",beard=True,glasses=True,shirt=(200,70,60),coat=(80,100,70),hat="cap",cap_col=(40,50,90),pants=(70,80,100),sleeve="long")
GOLDM=dict(skin=(250,200,50),hair=(250,200,50),hairstyle="bald",shirt=(250,200,50),pants=(250,200,50),shoes=(220,170,40),face=False,ear=False,sleeve="none",hands_col=(250,200,50),neck_col=(240,190,50))
def vign_(img,k=.4): return Image.alpha_composite(img.convert("RGBA"),vignette_ov(img.size,k)).convert("RGB")
def creature(big,cam,st,fn,x,z,u,hm=3.6,**kw):
    """dibuja una criatura de creatures.py en el sitio 3D indicado (escala ajustada a la altura hm)"""
    pl=place3(cam,st,x,z,hm)
    if not pl: return
    lx,ly,sc,z2=pl; d=D(big); k=math.exp(-z2*.012); fn(d,lx,ly,sc*.62,u,**kw)
def sceneA(u,final=False):
    t=u+(0 if not final else 3); cam=dict(x=lerp(-1.5,0,sm(t/7)),y=1.5,z=lerp(0,2.5,sm(t/7)),yaw=lerp(.12,0,sm(t/7)),pitch=.05)
    bg=render_terrain(cam,JUN,t); ov=new_ov()
    for k,(x,z) in enumerate(((-6,10),(6,12),(-9,20),(9,22),(-4,30),(5,34))): tree(ov,cam,JUN,x,z,h=4+k%3,col=(24,70,40),trunk=(40,34,28))
    box(ov,cam,JUN,-3,-2.6,0,5,14,14.4,(60,54,50),shadow=False); box(ov,cam,JUN,2.6,3,0,5,14,14.4,(60,54,50),shadow=False); box(ov,cam,JUN,-3,3,4.6,5,14,14.4,(70,60,54),shadow=False)
    big=fin(composite(bg,ov)); b=sm(clamp(t/1.0))
    creature(big,cam,JUN,trex,-.2,lerp(13,8,sm(t/8)),t,hm=7.5,jaw=b,facing=1)
    d=D(big)
    for k in range(5):
        a=((t*.6+k/5)%1); d.A(380,360,40+a*200,30+a*160,-50,50,(255,210,120,int(180*(1-a))),5)
    big=snow_particles(big,t,n=40,col=(200,220,200),sz=2,speed=-10,alpha=60,scale=2.2)
    return grade(vign_(big,.5),sat=.95,seed=int(u*30),tint=(.96,1.0,.96))
def amber_tex(u,w=260,h=340):
    im=Image.new("RGBA",(w,h),(0,0,0,0)); d=ImageDraw.Draw(im); d.ellipse([6,6,w-6,h-6],fill=(236,150,30,255)); d.ellipse([20,18,w-30,h*.55],fill=(250,190,70,255)); d.ellipse([40,30,100,110],fill=(255,240,200,120))
    cx,cy=w/2,h/2+20; d.ellipse([cx-12,cy-6,cx+12,cy+8],fill=(40,24,10)); d.line([(cx,cy),(cx-30,cy-26)],fill=(60,40,20),width=2); d.line([(cx,cy),(cx+30,cy-26)],fill=(60,40,20),width=2); d.line([(cx,cy),(cx-20,cy+24)],fill=(60,40,20),width=2); d.line([(cx,cy),(cx+20,cy+24)],fill=(60,40,20),width=2); d.line([(cx,cy+6),(cx+60,cy+40)],fill=(60,40,20),width=3)
    return im
def sceneB(u):
    st=dict(STUDIO,fov=48); cam=dict(x=lerp(-.4,.3,sm(u/7)),y=1.35,z=lerp(-.6,.2,sm(u/7)),yaw=0,pitch=.03)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.6,2.6,(1,.8,.5),1.2)]); back=new_ov(); box(back,cam,st,-1.0,1.0,0,.9,2.4,3.4,(70,56,46)); box(back,cam,st,-.1,.1,.9,1.2,2.8,3.0,(60,60,66))
    tquad(back,cam,st,(-.45,2.0,2.6),(.45,2.0,2.6),(.45,1.0,2.6),(-.45,1.0,2.6),amber_tex(u)); glow(back,cam,st,(0,1.5,2.5),(255,170,50),1.6,70,6)
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,1.6,3.0,DIRX,dict(P_point(u,dirx=-1),ar=(1.4,1.6),mouth=.5),hm=1.78,u=u,fog=(20,14,10)); ptext(d,40,270,"1993",9,(255,255,255))
    return grade(vign_(big,.5),sat=1.0,seed=int(u*30),tint=(1.05,.98,.92))
def faders_tex(u,w=360,h=140):
    im=Image.new("RGB",(w,h),(40,42,50)); d=ImageDraw.Draw(im)
    for k in range(12):
        x=20+k*28; d.rectangle([x-3,16,x+3,h-16],fill=(14,14,18)); fy=24+(math.sin(u*1.6+k*1.4)*.5+.5)*(h-70); d.rectangle([x-11,fy,x+11,fy+18],fill=(200,200,210)); d.ellipse([x-4,6,x+4,14],fill=(80,230,120) if k%2 else (240,200,60))
    return im
def sceneC(u):
    st=STUDIO; cam=dict(x=lerp(-.6,.3,sm(u/8)),y=1.45,z=lerp(-1.4,-.4,sm(u/8)),yaw=lerp(.1,-.04,sm(u/8)),pitch=.06)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.6,2.8,(1,.82,.6),1.0)]); back=new_ov()
    box(back,cam,st,-1.6,1.6,0,.9,2.4,3.4,(60,56,62)); tquad(back,cam,st,(-1.4,.92,2.45),(1.4,.92,2.45),(1.4,.92,3.1),(-1.4,.92,3.1),faders_tex(u))
    box(back,cam,st,-.3,.3,1.3,1.8,3.5,3.55,(30,30,34),shadow=False)
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,0,3.7,ENG,dict(al=(.5+.2*math.sin(u*1.6),.3),ar=(.5-.2*math.sin(u*1.6),.3),ll=(.05,.05),lr=(.05,.05),bob=math.sin(u*2),tilt=.07*math.sin(u*1.3),look=(0,.8),mouth=0,curlL=.5,curlR=.5,hands_front=True),hm=1.8,u=u,fog=(20,14,10))
    ptext(d,60,300,"?",8,(255,255,255)); ptext(d,440,300,"?",8,(255,255,255))
    return grade(vign_(big,.5),sat=1.0,seed=int(u*30),tint=(1.04,.98,.94))
def sceneD(u):
    cam=dict(x=lerp(-1,1,sm(u/7)),y=1.5,z=0,yaw=lerp(.15,-.15,sm(u/7)),pitch=.04)
    bg=render_terrain(cam,SAV,u); ov=new_ov()
    for k,(x,z) in enumerate(((-7,14),(7,18),(-9,26),(9,30))): tree(ov,cam,SAV,x,z,h=3.4,col=(60,130,60))
    big=fin(composite(bg,ov))
    creature(big,cam,SAV,elephant,-2.4,7.0,u,hm=3.6); creature(big,cam,SAV,tiger,2.4,6.5,u,hm=2.6,facing=-1); creature(big,cam,SAV,croc,0,4.2,u,hm=2.0)
    d=D(big); ptext(d,236,500,"+",12,(255,255,255),200); ptext(d,236,700,"+",12,(255,255,255),200)
    return grade(vign_(big,.3),sat=1.05,seed=int(u*30),tint=(1.02,1.0,.97))
def sceneE(u):
    cam=dict(x=lerp(1,-1,sm(u/7)),y=1.5,z=0,yaw=lerp(-.15,.15,sm(u/7)),pitch=.04)
    bg=render_terrain(cam,SAV,u); ov=new_ov()
    for k,(x,z) in enumerate(((-7,14),(7,18),(-9,26))): tree(ov,cam,SAV,x,z,h=3.4,col=(60,130,60))
    big=fin(composite(bg,ov))
    creature(big,cam,SAV,raptor,-2.2,6.0,u,hm=3.4,facing=1); creature(big,cam,SAV,horse,2.4,7.0,u,hm=3.6,facing=-1); creature(big,cam,SAV,tortoise,0,4.0,u,hm=1.8)
    ptext(D(big),40,270,"SE CUENTA",5,(255,214,120))
    return grade(vign_(big,.3),sat=1.05,seed=int(u*30),tint=(1.02,1.0,.97))
def wave_tex(u,w=360,h=240):
    im=Image.new("RGB",(w,h),(8,12,10)); d=ImageDraw.Draw(im)
    for k in range(40): hh=8+abs(math.sin(k*.6+u*6))*100*(1-abs(k-20)/24); d.rectangle([10+k*8.5,h/2-hh,10+k*8.5+5,h/2+hh],fill=(255,210,120))
    return im
def sceneF(u):
    st=STUDIO; cam=dict(x=lerp(-.7,.4,sm(u/6)),y=1.4,z=lerp(-1.2,-.4,sm(u/6)),yaw=.08,pitch=.05)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.4,4.0,(1,.8,.5),1.4)]); back=new_ov()
    tquad(back,cam,st,(-1.8,2.6,4.99),(1.0,2.6,4.99),(1.0,1.0,4.99),(-1.8,1.0,4.99),crt(wave_tex(u),1.0,int(u*30))); glow(back,cam,st,(-.4,1.8,4.9),(255,210,120),1.6,60,5)
    box(back,cam,st,-1.6,1.6,0,.9,3.0,3.8,(60,56,62)); tquad(back,cam,st,(-1.4,.92,3.05),(1.4,.92,3.05),(1.4,.92,3.7),(-1.4,.92,3.7),faders_tex(u))
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,1.2,4.2,ENG,dict(P_idle(u),al=(1.0,2.6),mouth=.3,look=(-.5,0)),hm=1.8,u=u,fog=(20,14,10))
    return grade(vign_(big,.5),sat=1.0,seed=int(u*30),tint=(1.04,.98,.94))
def sceneG(u):
    st=mk(H=5.0,hw=4.0,zend=8.0,zback=-3.0,wall="plaster",wcol=(60,30,40),floor="wood",fcol=(60,40,30),ceil="plaster",ccol=(30,20,24),ambient=.12,amb_rgb=(1,.85,.7),fov=52,fog=.02,fogcol=(10,6,8))
    cam=dict(x=lerp(-.6,.5,sm(u/6)),y=1.5,z=lerp(-1.4,-.6,sm(u/6)),yaw=0,pitch=.06)
    bg=render_room(cam,st,u,1.0,extra=[(0,3.6,3.0,(1,.9,.6),2.4)]); back=new_ov()
    box(back,cam,st,-1.6,1.6,0,.3,2.0,5.0,(110,40,50)); glow(back,cam,st,(0,3.0,3.0),(255,230,160),2.4,90,7)
    big=fin(composite(bg,back)); d=D(big)
    def oscar(dd,x,y,a,s,K=1.0): person(dd,x,y+80*K,.52*K,u,dict(al=(.05,.1),ar=(.05,.1),ll=(.05,.05),lr=(.05,.05),bob=0,tilt=0,look=(0,0),mouth=0),GOLDM)
    P3(d,cam,st,0,3.4,ENG,dict(P_hold(u,r=(2.2,2.9),grip=.9),mouth=.6),hm=1.8,u=u,props={"r":oscar},fog=(10,6,8),tone=1.2)
    for k in range(30): a=k*.5+u; d.E(270+math.cos(a)*(150+k*3),470+math.sin(a)*(160+k*3),2.5,2.5,(255,230,140,int(220*abs(math.sin(u*2+k)))))
    ptext(d,40,270,"OSCAR",9,(255,214,70))
    return grade(vign_(big,.5),sat=1.0,seed=int(u*30),tint=(1.05,.98,.92))
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur): return 1.0,270,480
core.CAM=cam
if __name__=="__main__": core.main()
