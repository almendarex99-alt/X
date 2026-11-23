import sys; sys.path.insert(0,"..")
from kit import *
from rooms import mk, render_room
from sets import *
CLAY=(150,98,70)
IMP=dict(skin=CLAY,hairstyle="bald",horns=True,claws=True,tail=CLAY,shirt=shade(CLAY,1.08),pants=shade(CLAY,.7),shoes=(60,36,26),bulk=1.55,sleeve="none",eyes=(255,210,60),ear=False,brow=(30,10,10),mouth_col=(60,10,10),height=1.05)
ARTIST=dict(skin=(226,184,150),hair=(54,36,26),hairstyle="short",beard=True,glasses=True,shirt=(190,190,196),coat=(120,84,60),sleeve="long",pants=(56,60,76))
PROG=dict(skin=(232,192,156),hair=(40,30,24),hairstyle="short",glasses=True,shirt=(70,80,120),pants=(60,60,76),sleeve="short")
PROG2=dict(skin=(214,170,130),hair=(150,100,50),hairstyle="long",shirt=(160,60,70),pants=(60,60,80),sleeve="short")
WORK=mk(H=3.0,hw=3.0,zend=4.6,zback=-3.2,wall="concrete",wcol=(120,108,96),floor="wood",fcol=(96,70,48),ceil="beams",ccol=(90,76,64),ambient=.16,amb_rgb=(1,.85,.7),fog=.012,fogcol=(10,6,4),fov=52,
          plights=dict(gap=100,off=1.0,xs=(.4,),y=2.4,rgb=(1,.8,.5),I=.9,k=.35))
OFFD=mk(H=2.8,hw=2.8,zend=4.4,zback=-2.6,wall="plaster",wcol=(180,176,168),floor="carpet",fcol=(80,84,96),ceil="tile",ccol=(200,198,190),ambient=.22,amb_rgb=(.9,.95,1),fog=.012,fov=52,
          plights=dict(gap=2.4,off=0,xs=(0,),y=2.65,rgb=(.9,.96,1),I=.45,k=.5))
def imp_deco(d,hx,hy,sc):
    for sg in(-1,1): d.E(hx+sg*8.5*sc,hy-3*sc,13*sc,11*sc,(255,210,60,60))
def imp(d,x,y,sc,u,pose=None,ph=0.0,**kw):
    st=dict(IMP); st.update(kw.pop("style",{}))
    return person(d,x,y,sc,u,pose or P_walk(u,2.6,ph),st,deco=imp_deco,**kw)
def vign_(img,k=.5): return Image.alpha_composite(img.convert("RGBA"),vignette_ov(img.size,k)).convert("RGB")
def sprite_img(pose,u,facing="front",size=(60,80)):
    tmp=Image.new("RGB",(900,1200),(30,30,40)); d=D(tmp); imp(d,150,385,1.2,u,pose=pose,facing=facing)
    return tmp.resize(size,Image.NEAREST if False else Image.BOX).resize(size,Image.NEAREST)
def sprites_tex(u,w=320,h=300):
    im=Image.new("RGB",(w,h),(24,28,60)); d=ImageDraw.Draw(im); d.rectangle([0,0,w,16],fill=(60,70,150)); d.text((6,2),"SPRITES",font=mono(11,True),fill=(250,250,250))
    for k in range(9):
        x=10+(k%3)*104; y=24+(k//3)*90; d.rectangle([x,y,x+98,y+84],outline=(70,80,130))
        sp=sprite_img(P_walk(u,3.0,k*1.1),u,"front" if k%3!=2 else "back",(60,80)); im.paste(sp,(x+19,y+2))
    return im
def doom_tex(u,w=160,h=100):
    im=Image.new("RGB",(w,h),(40,30,24)); d=ImageDraw.Draw(im)
    d.polygon([(0,0),(w,0),(w*.62,h*.32),(w*.38,h*.32)],fill=(70,70,76)); d.polygon([(0,0),(w*.38,h*.32),(w*.38,h*.64),(0,h*.8)],fill=(112,84,52)); d.polygon([(w,0),(w*.62,h*.32),(w*.62,h*.64),(w,h*.8)],fill=(96,72,44)); d.polygon([(0,h*.8),(w*.38,h*.64),(w*.62,h*.64),(w,h*.8),(w,h),(0,h)],fill=(70,52,40))
    d.rectangle([w*.38,h*.32,w*.62,h*.64],fill=(20,14,12)); d.rectangle([w*.46,h*.44,w*.54,h*.64],fill=(150,60,40))
    d.rectangle([w*.44,h*.72,w*.56,h],fill=(90,90,96)); d.rectangle([0,h*.86,w,h],fill=(60,50,44)); d.text((6,h*.88),"100%",font=mono(9,True),fill=(240,60,40)); d.text((w-34,h*.88),"050",font=mono(9,True),fill=(240,200,60))
    return im
def workshop(cam,u,extra=()):
    st=WORK; bg=render_room(cam,st,u,flick(u,.98),extra=[(1.4,1.2,3.3,(1.0,.3,.15),.5)]+list(extra)); back=new_ov(); front=new_ov()
    box(back,cam,st,-1.4,1.4,0,.82,2.4,3.4,(120,88,58)); box(back,cam,st,-2.9,-1.9,0,2.2,3.5,4.0,(86,60,40)); box(back,cam,st,1.9,2.9,0,2.2,3.5,4.0,(86,60,40))
    for sx in (-2.9,1.9):
        for lv in range(4): box(back,cam,st,sx,sx+1.0,.5*lv+.5,.5*lv+.54,3.45,4.0,(60,44,30),shadow=False)
    tquad(back,cam,st,(-.4,2.4,4.59),(1.0,2.4,4.59),(1.0,1.2,4.59),(-.4,1.2,4.59),tex_poster(seed=5,col=(150,30,24)))
    glow(back,cam,st,(.3,1.8,4.5),(255,60,30),1.3,45,5)
    return st,bg,back,front
def shelf_imps(d,cam,st,u):
    for sx in (-2.9,1.9):
        for lv in range(3):
            for k in range(3): P3(d,cam,st,sx+.25+k*.28,3.7,dict(IMP,shirt=(140,92,66)),P_idle(u,k+lv),hm=.38,u=u,y0=.5*lv+.54,fog=(20,14,10))
def sceneA(u,final=False):
    t=u+(0 if not final else 3); cam=dict(x=lerp(-.8,0,sm(t/6)),y=1.45,z=lerp(-2.2,-.6,sm(t/6)),yaw=lerp(.12,0,sm(t/6)),pitch=.06)
    st,bg,back,front=workshop(cam,t); big=fin(composite(bg,back)); d=D(big); shelf_imps(d,cam,st,t)
    P3(d,cam,st,0,3.1,ARTIST,dict(P_hold(t,r=(.5,.5),l=(.5,.5),grip=.6),mouth=.2,look=(0,.8),tilt=.05*math.sin(t*1.3)),hm=1.78,u=t,fog=(20,14,10))
    P3(d,cam,st,0,2.9,dict(IMP,shirt=(140,92,66),pants=(110,74,54)),dict(P_idle(t),mouth=.8),hm=.75,u=t,y0=.82,fog=(20,14,10))
    return grade(vign_(big,.5),sat=.95,seed=int(u*30),tint=(1.04,.97,.92))
def sceneB(u):
    st=OFFD; cam=dict(x=lerp(-1.0,.3,sm(u/9)),y=1.35,z=lerp(-.8,.6,sm(u/9)),yaw=lerp(.2,.0,sm(u/9)),pitch=.04)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.4,3.0,(.5,.7,1.0),.7)]); back=new_ov()
    for k,x in enumerate((-1.4,0.6)):
        box(back,cam,st,x-.7,x+.7,0,.74,2.4,3.2,(120,100,80)); box(back,cam,st,x-.38,x+.38,.74,1.26,2.55,3.05,(206,200,184))
        tquad(back,cam,st,(x-.3,1.21,2.545),(x+.3,1.21,2.545),(x+.3,.84,2.545),(x-.3,.84,2.545),crt(doom_tex(u+k),1.0,int(u*30)))
        glow(back,cam,st,(x,1.0,2.45),(255,120,90),.7,40,4)
    tquad(back,cam,st,(1.8,2.4,4.39),(2.7,2.4,4.39),(2.7,1.4,4.39),(1.8,1.4,4.39),tex_poster(seed=8,col=(30,60,110)))
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,-.8,3.6,PROG,dict(P_talk(u),al=(1.3,2.0),ar=(.2,.3)),hm=1.75,u=u,fog=(20,24,30)); P3(d,cam,st,1.4,3.5,PROG2,dict(P_point(u,dirx=-1),ar=(1.4,1.6)),hm=1.7,u=u,fog=(20,24,30))
    ptext(d,40,270,"1993",9,(255,255,255))
    return grade(vign_(big,.3),sat=.95,seed=int(u*30),tint=(.98,1.0,1.04))
def sceneC(u):
    cam=dict(x=0,y=1.15,z=lerp(1.0,1.7,sm(u/8)),yaw=0,pitch=.1); st=dict(WORK,fov=46)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.3,2.0,(1,.8,.5),1.0)]); back=new_ov(); box(back,cam,st,-1.4,1.4,0,.82,2.4,3.4,(120,88,58))
    big=fin(composite(bg,back)); d=D(big); p=sm(u/5.5)
    P3(d,cam,st,0,2.8,dict(IMP,shirt=(140,92,66),pants=(110,74,54)),dict(P_idle(u),mouth=.5),hm=.45+.7*p,u=u,y0=.82,fog=(20,14,10))
    for sg in (-1,1): hand3(d,cam,st,(sg*.28,.9+.1*math.sin(u*3+sg),2.7),hand_m=.2,a=2.6*(1 if sg>0 else 1),s=sg,curl=.8,spread=.5,arm_from=(270+sg*300,1.2),arm_w=.08,sleeve=(190,190,196))
    ptext(d,40,270,"A MANO",8,(255,220,140))
    return grade(vign_(big,.5),sat=.95,seed=int(u*30),tint=(1.04,.97,.92))
def sceneD(u):
    st=dict(WORK,fov=50); cam=dict(x=lerp(-1.2,.2,sm(u/8)),y=1.4,z=lerp(-1.2,-.4,sm(u/8)),yaw=lerp(.2,0,sm(u/8)),pitch=.05)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.5,2.4,(1,.97,.9),1.0)]); back=new_ov()
    box(back,cam,st,-1.4,1.4,0,.82,2.4,3.4,(120,88,58)); box(back,cam,st,.5,.9,.82,1.0,2.8,3.2,(70,70,76))
    for sx in (-1.2,): pass
    tquad(back,cam,st,(-2.8,2.5,4.59),(-1.2,2.5,4.59),(-1.2,1.3,4.59),(-2.8,1.3,4.59),sprites_tex(u*.3,w=320,h=300))
    box(back,cam,st,-.2,.2,0,1.4,1.0,1.04,(40,40,44),shadow=False); box(back,cam,st,-.28,.28,1.2,1.5,1.0,1.4,(30,30,34)); 
    big=fin(composite(bg,back)); d=D(big)
    ang=u*1.4; P3(d,cam,st,.7,3.0,dict(IMP,shirt=(140,92,66),pants=(110,74,54)),dict(P_idle(u),mouth=.4),hm=.7,u=u,y0=1.0,fog=(20,14,10))
    P3(d,cam,st,-.1,2.0,dict(ARTIST,coat=None,shirt=(70,90,130)),dict(P_both(u,l=(1.6,2.3),r=(1.6,2.3),grip=.9),look=(.6,0)),hm=1.75,u=u,fog=(20,14,10))
    if math.sin(u*5)>.8: glow(big if False else back,cam,st,(.7,1.5,3.0),(255,255,230),2.5,120,7)
    big=composite(big,back) if False else big
    ptext(d,40,270,"FOTOS",8,(255,220,140))
    return grade(vign_(big,.4),sat=.95,seed=int(u*30),tint=(1.03,.98,.94))
def sceneE(u):
    st=OFFD; cam=dict(x=lerp(-.3,.2,sm(u/8)),y=1.2,z=lerp(.8,1.6,sm(u/8)),yaw=0,pitch=.0)
    bg=render_room(cam,dict(st,fov=44),u,1.0,extra=[(0,1.2,2.6,(.5,.7,1.0),1.4)]); back=new_ov()
    box(back,cam,st,-1.4,1.4,0,.74,2.4,3.4,(120,100,80)); box(back,cam,st,-.85,.85,.74,1.6,2.6,3.2,(206,200,184))
    tquad(back,cam,st,(-.78,1.54,2.595),(.78,1.54,2.595),(.78,.82,2.595),(-.78,.82,2.595),crt(ps1f(sprites_tex(u*.5,w=320,h=300),block=2) if False else sprites_tex(u*.5,w=320,h=300),1.0,int(u*30)))
    glow(back,cam,st,(0,1.2,2.5),(140,170,255),1.4,60,6)
    big=fin(composite(bg,back)); d=D(big)
    ptext(d,40,270,"SPRITES",8,(255,255,255))
    return grade(vign_(big,.4),sat=.95,seed=int(u*30),tint=(.98,1.0,1.04))
def sceneF(u):
    cam=dict(x=lerp(-1.0,1.0,sm(u/7)),y=1.5,z=lerp(1.0,1.4,sm(u/7)),yaw=lerp(.2,-.2,sm(u/7)),pitch=.04); st=dict(WORK,fov=46)
    bg=render_room(cam,st,u,flick(u,.98),extra=[(0,1.8,3.0,(1,.3,.2),.9)]); back=new_ov(); box(back,cam,st,-1.4,1.4,0,.82,2.6,3.6,(100,70,46))
    big=fin(composite(bg,back)); d=D(big)
    imp(d,270,860,1.9,u,pose=dict(P_cheer(u),mouth=1.0)) if False else P3(d,cam,st,0,3.1,IMP,dict(P_cheer(u),mouth=1.0,al=(2.2,2.7),ar=(2.2,2.7)),hm=1.9,u=u,y0=.82,fog=(20,10,10),deco=imp_deco)
    ptext(d,40,270,"VOLUMEN",8,(255,220,140))
    return grade(vign_(big,.5),sat=.95,seed=int(u*30),tint=(1.06,.96,.9))
def sceneG(u):
    cam=dict(x=lerp(-.6,.6,sm(u/6)),y=1.45,z=-1.0,yaw=lerp(.15,-.1,sm(u/6)),pitch=.05)
    st,bg,back,front=workshop(cam,u); big=fin(composite(bg,back)); d=D(big); shelf_imps(d,cam,st,u)
    o=P3(d,cam,st,-.6,2.6,ARTIST,dict(P_hold(u,r=(1.4,2.2),grip=.5),mouth=.5),hm=1.78,u=u,fog=(20,14,10))
    if o: hx,hy=o["hand_r"]; sc=place3(cam,st,-.6,2.6,1.78)[2]; imp(d,hx,hy-4*sc,.24*sc*2.0,u,pose=P_wave(u))
    P3(d,cam,st,.9,2.8,IMP,P_walk(u,2.6),hm=1.7,u=u,fog=(20,14,10),deco=imp_deco)
    return grade(vign_(big,.5),sat=.95,seed=int(u*30),tint=(1.04,.97,.92))
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur): return 1.0,270,480
core.CAM=cam
if __name__=="__main__": core.main()
