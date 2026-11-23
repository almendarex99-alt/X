import sys; sys.path.insert(0,"..")
from kit import *
from rooms import mk, render_room
from terrain import render_terrain, mk as tmk
from sets import *
BEDR=mk(H=2.5,hw=2.2,zend=3.4,zback=-2.6,wall="plaster",wcol=(176,170,160),wcol2=(110,100,90),floor="carpet",fcol=(110,100,90),ceil="plaster",ccol=(190,186,180),ambient=.10,amb_rgb=(.8,.9,1),fog=.02,fogcol=(6,8,8),fov=60)
LIV=mk(H=2.5,hw=2.4,zend=3.6,zback=-3.0,wall="plaster",wcol=(200,190,170),floor="wood",fcol=(130,96,64),ceil="plaster",ccol=(210,206,198),ambient=.28,amb_rgb=(1,.92,.8),fog=.01,fov=52,
         plights=dict(gap=100,off=1.0,xs=(0,),y=2.2,rgb=(1,.8,.55),I=.5,k=.5))
OFFC=mk(H=2.8,hw=2.6,zend=4.6,zback=-2.6,wall="plaster",wcol=(210,204,190),floor="wood",fcol=(100,76,56),ceil="plaster",ccol=(220,216,206),ambient=.30,amb_rgb=(1,.96,.9),fog=.01,fov=52,
         plights=dict(gap=100,off=1.0,xs=(0,),y=2.4,rgb=(1,.9,.7),I=.5,k=.5))
PELI=dict(skin=(226,184,150),hair=(40,30,24),hairstyle="short",beard=True,shirt=(80,110,150),pants=(60,60,80),sleeve="long")
WOM=dict(skin=(238,200,164),hair=(150,100,50),hairstyle="long",shirt=(200,90,110),pants=(60,60,90),sleeve="short")
EXEC=dict(skin=(226,184,150),hair=(200,200,200),hairstyle="short",shirt=(236,236,240),coat=(40,44,60),pants=(40,44,60),sleeve="long",glasses=True)
EXEC2=dict(skin=(214,170,130),hair=(30,24,20),hairstyle="short",shirt=(240,240,244),coat=(70,60,56),pants=(60,60,70),sleeve="long")
def vign_(img,k=.6): return Image.alpha_composite(img.convert("RGBA"),vignette_ov(img.size,k)).convert("RGB")
def nv(img,t,seed=0):
    a=np.asarray(img).astype(np.float32); g=a.mean(2); g=np.clip(g*1.6,0,255); rng=np.random.default_rng(seed)
    g=g+rng.normal(0,14,g.shape); g[::4]*=.9
    out=np.stack([g*.45,g*1.0,g*.5],-1); return Image.fromarray(np.clip(out,0,255).astype(np.uint8))
def cashbox(ov,cam,st,x,z,w,h,col=(110,170,110)):
    box(ov,cam,st,x-w/2,x+w/2,0,h,z-w/3,z+w/3,col,edge=(40,70,40))
    for k in range(int(h/.1)): poly3(ov,cam,st,[(x-w/2,k*.1+.05,z-w/3-.002),(x+w/2,k*.1+.05,z-w/3-.002),(x+w/2,k*.1+.07,z-w/3-.002),(x-w/2,k*.1+.07,z-w/3-.002)],(70,120,70))
def sceneA(u,final=False):
    t=u+(0 if not final else 3); st=dict(OFFC,fov=54)
    cam=dict(x=lerp(-1.2,.2,sm(t/7)),y=1.3,z=lerp(-2.0,-.6,sm(t/7)),yaw=lerp(.2,-.02,sm(t/7)),pitch=.05)
    bg=render_room(cam,st,t,1.0,extra=[(0,1.4,2.4,(1,.9,.7),.8)]); back=new_ov()
    box(back,cam,st,-.9,.9,0,.8,1.5,2.5,(110,84,60)); cashbox(back,cam,st,-.4,1.6,.4,.12)
    h=lerp(.3,3.6,sm(t/5)); cashbox(back,cam,st,1.2,3.0,1.6,h*1.0)
    tag=Image.new("RGB",(260,110),(250,250,240)); td=ImageDraw.Draw(tag); td.text((130,30),"15.000 $",font=font(34,True),fill=(30,110,40),anchor="mm"); tquad(back,cam,st,(-.9,1.5,1.49),(.1,1.5,1.49),(.1,1.1,1.49),(-.9,1.1,1.49),tag)
    tg2=Image.new("RGB",(300,110),(250,250,240)); t2=ImageDraw.Draw(tg2); t2.text((150,30),"190.000.000 $",font=font(30,True),fill=(30,110,40),anchor="mm"); tquad(back,cam,st,(.5,3.8,2.49),(2.0,3.8,2.49),(2.0,3.2,2.49),(.5,3.2,2.49),tg2)
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,-1.6,2.6,EXEC2,dict(P_point(t,dirx=1),ar=(1.4,1.6),mouth=.5),hm=1.78,u=t,fog=(30,28,24))
    return grade(vign_(big,.4),sat=.95,seed=int(u*30),tint=(1.02,1.0,.96))
def sceneB(u):
    st=LIV; cam=dict(x=lerp(-1.2,.4,sm(u/8)),y=1.5,z=lerp(-2.0,-1.0,sm(u/8)),yaw=lerp(.18,-.05,sm(u/8)),pitch=.05)
    bg=render_room(cam,st,u,1.0,extra=[(-1.5,1.4,2.2,(1,.8,.55),.8)]); back=new_ov()
    sidewindow(back,cam,st,-2.39,.5,1.8,night=True); box(back,cam,st,-.9,.9,0,.45,1.4,2.3,(120,60,50)); box(back,cam,st,-.9,.9,.45,1.0,2.2,2.5,(130,64,54)); box(back,cam,st,1.8,2.3,0,.7,2.0,3.0,(110,84,60)); lamp(back,cam,st,-1.8,2.4,h=1.3)
    bookcase(back,cam,st,2.0,3.5,w=1.2,h=2.0,d=.3,seed=7)
    big=fin(composite(bg,back)); d=D(big)
    def cam_prop(dd,x,y,a,s,K=1.0): dd.R(x-26*K,y-14*K,x+26*K,y+22*K,(30,30,36,255),5*K); dd.E(x-28*K,y+4*K,12*K,12*K,(20,24,32,255)); dd.E(x-28*K,y+4*K,7*K,7*K,(60,100,160,255)); dd.E(x+16*K,y-18*K,4*K,4*K,(240,40,40,255))
    P3(d,cam,st,.1,1.8,PELI,dict(P_hold(u,r=(1.5,1.8),l=(1.3,1.7),grip=.9),mouth=.5,look=(0,0)),hm=1.78,u=u,props={"r":cam_prop},fog=(40,30,20))
    ptext(d,300,260,"2007",9,(255,255,255))
    return grade(vign_(big,.4),sat=.95,seed=int(u*30),tint=(1.03,1.0,.94))
def sceneC(u):
    st=BEDR; cam=dict(x=-1.9,y=2.2,z=-2.4,yaw=.62,pitch=.30+.01*math.sin(u))
    bg=render_room(cam,st,u,1.0,extra=[(0,.9,.5,(.8,.9,1.0),.4)]); back=new_ov(); front=new_ov()
    box(back,cam,st,-1.0,1.0,0,.5,.0,2.2,(180,176,170)); box(back,cam,st,-1.0,1.0,.5,.56,.0,2.2,(206,200,196)); box(back,cam,st,-1.0,1.0,.5,1.2,2.1,2.3,(110,80,60))
    box(back,cam,st,-.9,-.2,.56,.66,1.6,2.1,(240,240,244),shadow=False); box(back,cam,st,.2,.9,.56,.66,1.6,2.1,(240,240,244),shadow=False)
    # puerta entreabierta que se mueve
    ang=sm((u-1.5)/3.0)*.9; box(back,cam,st,1.5,1.55+ang*.9,0,2.0,2.5,3.2,(120,96,76)) if False else poly3(back,cam,st,[(2.19,0,2.0),(2.19-ang*.8,0,2.0+ang*.6+.3),(2.19-ang*.8,2.0,2.0+ang*.6+.3),(2.19,2.0,2.0)],(120,96,76))
    poly3(back,cam,st,[(2.19,0,2.0),(2.19,0,2.9),(2.19,2.0,2.9),(2.19,2.0,2.0)],(6,6,8))
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,-.55,1.2,WOM,dict(P_idle(u),tilt=.03),hm=1.3,u=u,y0=.5,bust=True,fog=(6,8,8))
    big=composite(big,front.resize(OUTSZ,Image.BICUBIC))
    big=nv(big,u,int(u*30)); od=D(big); 
    for (x,y,s_,sy_) in ((30,30,1,1),(510,30,-1,1),(30,930,1,-1),(510,930,-1,-1)): od.L(x,y,x+s_*30,y,(180,255,190,230),2.5); od.L(x,y,x,y+sy_*30,(180,255,190,230),2.5)
    if int(u*1.2)%2==0: od.E(46,52,8,8,(255,60,60,255))
    ptext(od,66,42,"REC",3.2,(230,255,230)); ptext(od,300,42,"OCT 3  03:%02d:%02d"%(int(u*7)%60,int(u*60)%60),3.2,(230,255,230))
    return grade(vign_(big,.6),sat=1.0,grain=6,seed=int(u*30))
def script_tex(u,w=340,h=440):
    im=Image.new("RGB",(w,h),(246,244,236)); d=ImageDraw.Draw(im)
    for k in range(14): d.rectangle([30,50+k*26,w-30-((k*43)%110),58+k*26],fill=(60,60,60) if k%3 else (90,90,90))
    d.text((w/2,24),"GUION  -  FINAL",font=mono(20,True),fill=(30,30,30),anchor="mm")
    t=sm((u-1.0)/1.4); d.line([(40,330),(40+int(260*t),330)],fill=(200,30,30),width=6)
    if t>.9: d.text((w/2,400),"CAMBIAR?",font=mono(34,True),fill=(200,30,30),anchor="mm")
    return im
def sceneD(u):
    st=OFFC; cam=dict(x=lerp(-1.0,.4,sm(u/8)),y=1.4,z=lerp(.4,1.4,sm(u/8)),yaw=lerp(.2,.0,sm(u/8)),pitch=.05)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.6,2.8,(1,.9,.7),.8)]); back=new_ov()
    box(back,cam,st,-1.6,1.6,0,.76,2.4,3.6,(110,76,50)); 
    tquad(back,cam,st,(-.5,.77,2.5),(.5,.77,2.5),(.5,.77,3.3),(-.5,.77,3.3),script_tex(u))
    sidewindow(back,cam,st,-2.59,.5,2.0,night=False,curt=(190,190,180))
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,-1.0,3.9,EXEC,dict(P_talk(u),mouth=.5),hm=1.78,u=u,fog=(30,28,24)); P3(d,cam,st,.9,3.9,EXEC2,dict(P_point(u,dirx=-1),ar=(1.4,1.6),mouth=.4),hm=1.78,u=u,fog=(30,28,24))
    hand3(d,cam,st,(.15,.78,2.9),hand_m=.16,a=2.4,s=1,curl=.8,spread=.3,arm_from=(480,1.2),arm_w=.06,sleeve=(40,44,60),prop=lambda dd,x,y,a,s,K=1.0: dd.L(x,y-6*K,x+4*K,y+26*K,(200,30,30,255),3*K))
    return grade(vign_(big,.4),sat=.95,seed=int(u*30),tint=(1.03,1.0,.95))
def sceneE(u):
    st=dict(BEDR,ambient=.30,fov=54); cam=dict(x=lerp(-1.0,.6,sm(u/6)),y=1.5,z=-1.9,yaw=lerp(.2,-.1,sm(u/6)),pitch=.05)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.8,.8,(1,.95,.9),1.0)]); back=new_ov()
    box(back,cam,st,-1.0,1.0,0,.5,.6,2.6,(180,176,170)); box(back,cam,st,-1.0,1.0,.5,.56,.6,2.6,(206,200,196))
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,-.2,3.0,WOM,dict(P_scared(u),mouth=1.0),hm=1.65,u=u,fog=(40,36,30)); P3(d,cam,st,1.5,2.0,dict(PELI,hat=None),dict(P_hold(u,r=(1.5,1.7),grip=.9)),hm=1.78,u=u,fog=(40,36,30))
    clapper(d,420,760,1.3,open_=clamp(math.sin(u*2.2))); ptext(d,320,270,"2009",9,(255,255,255))
    return grade(vign_(big,.4),sat=.95,seed=int(u*30),tint=(1.02,1.0,.96))
def sceneF(u):
    st=dict(OFFC,wcol=(60,56,60),ambient=.18); cam=dict(x=lerp(-.8,.4,sm(u/6)),y=1.4,z=lerp(0,1.0,sm(u/6)),yaw=lerp(.1,-.05,sm(u/6)),pitch=.05)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.6,3.5,(1,.9,.7),.8)]); back=new_ov()
    ch=Image.new("RGB",(360,240),(20,22,28)); cd=ImageDraw.Draw(ch); cd.text((180,18),"TAQUILLA MUNDIAL",font=font(22,True),fill=(255,255,255),anchor="mm")
    b=sm(u/3.0); cd.rectangle([60,210-int(10*b),120,210],fill=(120,200,140)); cd.rectangle([220,210-int(170*b),290,210],fill=(250,170,50)); cd.text((90,224),"COSTE",font=font(14),fill=(255,255,255),anchor="mm"); cd.text((255,224),"190 M$",font=font(16,True),fill=(255,255,255),anchor="mm")
    tquad(back,cam,st,(-1.6,2.6,4.59),(1.0,2.6,4.59),(1.0,.9,4.59),(-1.6,.9,4.59),ch); glow(back,cam,st,(-.3,1.7,4.5),(255,200,100),1.5,50,5)
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,1.6,3.8,EXEC2,dict(P_point(u,dirx=-1),ar=(1.4,1.6),mouth=.5),hm=1.78,u=u,fog=(30,24,20))
    for k in range(40): d.E((k*61+u*30)%540,(u*160+k*83)%960,3,3,(255,230,120,int(200*abs(math.sin(u*3+k)))))
    return grade(vign_(big,.4),sat=1.0,seed=int(u*30),tint=(1.03,1.0,.95))
def sceneG(u):
    st=dict(mk(H=2.5,hw=1.1,wall="plaster",wcol=(160,156,148),floor="wood",fcol=(90,70,50),ceil="plaster",ccol=(170,166,160),ambient=.14,amb_rgb=(1,.95,.9),fog=.05,fogcol=(6,6,6),fov=64,
        open_p=.35,seg=5.0,D=2.5,plights=dict(gap=100,off=6,xs=(0,),y=2.3,rgb=(.9,.9,1),I=.6,k=.5)))
    cam=walk_cam(u+3,speed=.5,sway=2.4); cam["pitch"]=.1+cam["pitch"]; cam["y"]=1.5
    bg=render_room(cam,st,u,flick(u)); big=fin(bg); d=D(big)
    if u>1.5: P3(d,cam,st,.1,cam["z"]+9-(u-1.5)*.6,dict(skin=(210,200,190),hair=(20,20,20),hairstyle="long",shirt=(200,196,190),dress=True,skirt_col=(196,192,186),sleeve="long"),dict(P_idle(u),tilt=.1),hm=1.7,u=u,fog=(6,6,6),tone=.8)
    big=vhs(big,u,1.0); big=camcorder_overlay(big,u+17,date="OCT 11 2006")
    return grade(big,sat=.8,grain=6,seed=int(u*30),tint=(1.0,1.0,.95))
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur): return 1.0,270,480
core.CAM=cam
if __name__=="__main__": core.main()
