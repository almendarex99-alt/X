import sys; sys.path.insert(0,"..")
from kit import *
from rooms import mk, render_room
from sets import *
CORR=mk(H=2.7,hw=1.6,wall="panel",wcol=(206,196,172),wcol2=(92,72,56),floor="rubber",fcol=(54,52,50),ceil="strip",ccol=(150,146,136),ambient=.12,amb_rgb=(1,.88,.7),fog=.04,fogcol=(10,6,4),fov=56,strip=(255,214,160),open_p=.4,seg=6.0,D=3.0,
        plights=dict(gap=4,off=1,xs=(0,),y=2.55,rgb=(1.0,.82,.55),I=1.0,flk=.8,flp=.2,k=.45))
LAB=mk(H=2.8,hw=2.6,zend=5.0,zback=-3.0,wall="panel",wcol=(206,196,172),wcol2=(92,72,56),floor="rubber",fcol=(60,58,56),ceil="strip",ccol=(150,146,136),ambient=.18,amb_rgb=(1,.9,.75),fog=.02,fogcol=(10,6,4),fov=54,strip=(255,220,170),
        plights=dict(gap=3,off=1,xs=(0,),y=2.6,rgb=(1.0,.85,.6),I=.9,k=.45))
VENT=mk(H=1.1,hw=.7,wall="metal",wcol=(70,74,78),floor="grate",fcol=(50,54,58),ceil="pipes",ccol=(48,52,56),ambient=.08,amb_rgb=(1,.5,.4),fog=.09,fogcol=(8,2,2),fov=60,strip=(255,60,40),
        plights=dict(gap=3,off=2,xs=(0,),y=1.0,rgb=(1.0,.25,.2),I=1.2,flk=.7,flp=.3,k=.8))
AMA=dict(skin=(232,192,156),hair=(80,50,34),hairstyle="ponytail",shirt=(60,110,170),pants=(50,90,150),shoes=(40,40,46),sleeve="long",belt=(200,200,206),brow=(50,32,22))
DEV=dict(skin=(232,192,156),hair=(40,30,24),hairstyle="short",glasses=True,shirt=(120,130,150),pants=(60,60,76),sleeve="long",beard=True)
def alien_head(d,hx,hy,sc):
    d.E(hx,hy-14*sc,20*sc,46*sc,(22,24,30,255)); d.E(hx-6*sc,hy-24*sc,6*sc,22*sc,(120,130,150,110)); d.E(hx,hy+10*sc,15*sc,17*sc,(30,32,38,255))
    d.R(hx-7*sc,hy+14*sc,hx+7*sc,hy+24*sc,(150,150,156,255),2*sc)
    for k in range(5): d.R(hx-6*sc+k*3*sc,hy+17*sc,hx-5*sc+k*3*sc,hy+23*sc,(236,236,240,255),0)
ALN=dict(skin=(26,28,34),hair=(26,28,34),hairstyle="bald",shirt=(30,32,38),pants=(26,28,34),shoes=(20,20,24),sleeve="none",claws=True,tail=(30,32,38),bulk=.8,height=1.3,face=False,ear=False,mask=alien_head,hands_col=(34,36,42),neck_col=(30,32,38))
def tracker(t,lvl=1.0,blip=(0,0)):
    def f(dd,x,y,a,s,K=1.0):
        dd.R(x-16*K,y-12*K,x+16*K,y+44*K,(150,142,100,255),3*K); dd.R(x-12*K,y-8*K,x+12*K,y+12*K,(8,24,14,255),2*K)
        ang=(t*2.4*lvl)%(2*math.pi); dd.L(x,y+2*K,x+math.cos(ang)*10*K,y+2*K+math.sin(ang)*10*K,(110,255,150,255),1.2*K); dd.E(x,y+2*K,10*K,10*K,None,(110,255,150,140),1)
        if blip!=(0,0): dd.E(x+blip[0]*K,y+2*K+blip[1]*K,1.6*K,1.6*K,(200,255,220,255))
        dd.E(x,y+2*K,24*K,24*K,(110,255,150,22))
    return f
def sceneA(u,final=False):
    t=u+(0 if not final else 3); cam=walk_cam(t,speed=.5); cam["pitch"]=.08+cam["pitch"]*.4; cam["y"]=1.6
    dz=cam["z"]+2.4; ex=[(cam["x"]+.35,1.2,dz-.2,(.4,1.0,.55),.35)]
    bg=render_room(cam,CORR,t,flick(t),extra=ex); big=fin(bg); d=D(big)
    P3(d,cam,CORR,0.0,dz+9+1.5*math.sin(t*.4),ALN,dict(P_walk(t,2.0),ar=(.4,.7),al=(.4,.7)),hm=2.2,u=t,fog=(10,6,4),tone=.6)
    P3(d,cam,CORR,cam["x"],dz,AMA,dict(P_walk(t,2.2),ar=(1.1,1.6),curlR=.9),hm=1.7,u=t,facing="back",props={"r":tracker(t,1.0+.4*math.sin(t),(-6,-5))},fog=(10,6,4))
    for k in range(5): a=((t*.4+k*.2)%1); d.E(80+k*100,300+a*20,(10+a*40),(8+a*20),(230,230,236,int(70*(1-a))))
    return grade(vign(big,.5),sat=.9,seed=int(u*30),tint=(1.02,.98,.94))
def vign(img,k=.6): return Image.alpha_composite(img.convert("RGBA"),vignette_ov(img.size,k)).convert("RGB")
def ai_tex(w=300,h=220,t=0.0):
    im=Image.new("RGB",(w,h),(8,24,14)); d=ImageDraw.Draw(im); G=(110,255,150)
    d.rectangle([4,4,w-5,h-5],outline=G,width=2)
    d.rectangle([30,30,130,80],outline=G,width=2); d.text((80,55),"DIRECTOR",font=mono(14,True),fill=G,anchor="mm")
    d.rectangle([170,140,270,190],outline=G,width=2); d.text((220,165),"ALIEN",font=mono(14,True),fill=G,anchor="mm")
    p=(t*.8)%1; d.line([(130,60),(220,140)],fill=G,width=2); d.ellipse([130+90*p-4,60+80*p-4,130+90*p+4,60+80*p+4],fill=G)
    for k in range(int(h/4)): d.line([(0,k*4),(w,k*4)],fill=(0,0,0),width=1)
    return im
def map_tex(w=300,h=240,t=0.0):
    im=Image.new("RGB",(w,h),(6,18,12)); d=ImageDraw.Draw(im); G=(110,255,150)
    for (x,y,ww,hh) in((20,20,90,50),(130,20,150,50),(20,90,70,80),(110,90,80,80),(210,90,70,80),(20,190,120,40),(160,190,120,40)): d.rectangle([x,y,x+ww,y+hh],outline=G,width=2)
    px,py=190,130; r=10+(t*30)%40; d.ellipse([px-3,py-3,px+3,py+3],fill=(255,90,70)); d.ellipse([px-r,py-r,px+r,py+r],outline=(255,90,70))
    ax=int(60+80*sm((t*.2)%1)); d.ellipse([ax-4,200-4,ax+4,200+4],fill=(255,230,90)); d.ellipse([ax-10,196-6,ax+10,206],outline=(255,230,90))
    for k in range(int(h/4)): d.line([(0,k*4),(w,k*4)],fill=(0,0,0),width=1)
    return im
def sceneB(u):
    st=LAB; cam=dict(x=lerp(-1.0,.0,sm(u/6)),y=1.45,z=lerp(-.3,.8,sm(u/6)),yaw=lerp(.15,.05,sm(u/6)),pitch=.05)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.4,3.0,(.5,1.0,.6),.9)]); back=new_ov()
    box(back,cam,st,-1.6,-.2,0,.74,3.0,3.8,(120,110,96)); box(back,cam,st,-1.3,-.5,.74,1.25,3.2,3.7,(190,180,150))
    tquad(back,cam,st,(-1.25,1.22,3.195),(-.55,1.22,3.195),(-.55,.8,3.195),(-1.25,.8,3.195),crt(ai_tex(t=u),1.0,int(u*30)))
    glow(back,cam,st,(-.9,1.0,3.1),(110,255,150),.9,50,5)
    tquad(back,cam,st,(.4,2.2,4.99),(2.2,2.2,4.99),(2.2,.9,4.99),(.4,.9,4.99),crt(map_tex(t=u),1.0,int(u*30)))
    box(back,cam,st,1.4,2.4,0,.74,3.6,4.4,(110,100,86))
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,.9,3.2,DEV,dict(P_talk(u),al=(1.3,2.1),ar=(.2,.3)),hm=1.75,u=u,fog=(10,6,4))
    return grade(vign(big,.4),sat=.9,seed=int(u*30),tint=(1.0,.98,.96))
def sceneC(u):
    st=CORR; cam=dict(x=0,y=1.6,z=0,yaw=lerp(.3,.05,sm(u/6)),pitch=.06)
    bg=render_room(cam,st,u,flick(u)); back=new_ov()
    tquad(back,cam,st,(-1.59,2.0,2.5),(-1.59,2.0,4.5),(-1.59,.9,4.5),(-1.59,.9,2.5),crt(ai_tex(t=u),1.0,int(u*30)))
    glow(back,cam,st,(-1.5,1.4,3.5),(110,255,150),1.0,50,5)
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,-.4,2.0,AMA,dict(P_idle(u),look=(-.8,0),ar=(1.2,1.7),curlR=.9),hm=1.7,u=u,facing="back",props={"r":tracker(u)},fog=(10,6,4))
    return grade(vign(big,.5),sat=.9,seed=int(u*30),tint=(1.02,.98,.94))
def sceneD(u):
    st=LAB; cam=dict(x=lerp(-.7,.3,sm(u/7)),y=1.5,z=lerp(.2,1.3,sm(u/7)),yaw=lerp(.15,.0,sm(u/7)),pitch=.05)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.4,4.2,(.5,1.0,.6),1.2)]); back=new_ov()
    tquad(back,cam,st,(-1.4,2.3,4.99),(1.4,2.3,4.99),(1.4,.7,4.99),(-1.4,.7,4.99),crt(map_tex(t=u),1.0,int(u*30)))
    glow(back,cam,st,(0,1.5,4.9),(110,255,150),1.6,60,6)
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,-.5,3.3,AMA,dict(P_point(u,dirx=1),ar=(1.45,1.6)),hm=1.7,u=u,facing="back",fog=(10,6,4))
    return grade(vign(big,.4),sat=.9,seed=int(u*30),tint=(1.0,.98,.96))
def sceneE(u):
    st=VENT; cam=dict(x=0,y=.6,z=lerp(-1.0,2.0,sm(u/7)),yaw=0,pitch=.03)
    bg=render_room(cam,st,u,flick(u)); big=fin(bg); d=D(big)
    P3(d,cam,st,.0,lerp(8,3.6,sm((u-.8)/5)),ALN,dict(P_zombie(u,0,1.6),mouth=1.0),hm=1.4,u=u,fog=(8,2,2))
    for k in range(4): 
        a=((u*.5+k*.25)%1); d.A(270,500,40+a*200,30+a*160,-60,60,(255,255,255,int(150*(1-a))),4); d.A(270,500,40+a*200,30+a*160,120,240,(255,255,255,int(150*(1-a))),4)
    return grade(vign(big,.7),sat=.8,seed=int(u*30),tint=(1.04,.95,.92))
def sceneF(u):
    st=CORR; cam=dict(x=.0,y=1.55,z=0.0,yaw=0,pitch=.05)
    bg=render_room(cam,st,u,flick(u)); big=fin(bg); d=D(big)
    az=lerp(14,2.2,sm(u/7)); P3(d,cam,st,.3,az,ALN,dict(P_walk(u,2.0),ar=(.4,.7)),hm=2.3,u=u,fog=(10,6,4),tone=.9)
    # taquilla vista desde dentro: rendijas horizontales
    ov=Image.new("RGBA",big.size,(0,0,0,0)); od=ImageDraw.Draw(ov); od.rectangle([0,0,1620,2880],fill=(6,8,10,255))
    for k in range(9): y0=int(520+k*150+math.sin(u*1.3)*4); od.rectangle([160,y0,1460,y0+54],fill=(0,0,0,0))
    ov=ov.filter(ImageFilter.GaussianBlur(1.5)); big=Image.alpha_composite(big.convert("RGBA"),ov).convert("RGB")
    d=D(big); ptext(d,20,830,"",3,(255,255,255))
    return grade(vign(big,.8),sat=.85,seed=int(u*30),tint=(1.04,.96,.92))
def sceneG(u):
    st=dict(VENT,fov=46); cam=dict(x=0,y=.6,z=0,yaw=0,pitch=.0)
    bg=render_room(cam,st,u,flick(u)); big=fin(bg); d=D(big)
    P3(d,cam,st,.0,1.8,ALN,dict(P_idle(u),mouth=1.0,tilt=.12*math.sin(u*.8)),hm=1.1,u=u,fog=(8,2,2))
    for k,(x,col) in enumerate(((120,(220,170,60)),(420,(80,200,170)))): d.E(x,240,60,50,col+(255,)); d.E(x+(15 if k else -15),240,50,44,col+(255,)); d.E(x,240,110,92,col+(40,))
    return grade(vign(big,.7),sat=.85,seed=int(u*30),tint=(1.03,.95,.92))

def run_cam(t,speed=2.3,y=1.25,bob=.07):
    step=t*speed*1.8
    return dict(x=math.sin(step*.5)*.07,y=y+abs(math.sin(step))*bob,z=t*speed,yaw=math.sin(t*1.2)*.03+math.sin(step)*.012,pitch=.05+math.sin(step)*.015,roll=math.sin(step*.5)*.012)
def alien_fx(big,u,d=None,hb=1.0):
    big=tint(big,(1.15,.78,.62),.7)
    pulse=.5+.5*math.sin(u*7.5)
    big=pov_vignette(big,.75+.15*pulse,(40,0,0))
    a=np.asarray(big).astype(np.float32); a[::5]*=.93; return Image.fromarray(np.clip(a,0,255).astype(np.uint8))
def chase_pov(u,t0,dist0,dist1,final=False,st=CORR,hide=None):
    t=u+t0; cam=run_cam(t); dz=cam["z"]+lerp(dist0,dist1,clamp(u/7.0)); ex=[(0.0,1.2,dz,(.4,1.0,.55),.5)]
    bg=render_room(cam,st,t,flick(t),extra=ex); big=fin(bg); d=D(big)
    o=P3(d,cam,st,0.0+.3*math.sin(t*1.1),dz,AMA,dict(P_walk(t,7.0),al=(.7,1.2),ar=(1.2,1.6),curlR=.9,tilt=.05*math.sin(t*3)),hm=1.7,u=t,facing="back",props={"r":tracker(t,2.5,(-6,-5))},fog=(10,6,4))
    if o:
        pl=place3(cam,st,0.0,dz,1.7); sound_rings(d,cam,st,0.0,dz,t); outline_glow(d,o,pl[2])
    monster_arms(d,t,tone=(26,28,34),run=7.0,size=1.6)
    return alien_fx(big,t,d)
def sceneA(u,final=False):
    big=chase_pov(u,0 if not final else 3,7.0,4.0 if not final else 3.4,final)
    return grade(big,sat=.9,seed=int(u*30),tint=(1.02,.97,.94))
def sceneE(u):
    st=dict(CORR,fov=60); cam=dict(x=0,y=2.4,z=0,yaw=0,pitch=.42+.01*math.sin(u*2))
    dz=lerp(5.0,9.0,sm(u/7)); bg=render_room(cam,st,u,flick(u),extra=[(0,1.2,dz,(.4,1.0,.55),.6)]); big=fin(bg); d=D(big)
    o=P3(d,cam,st,0.0,dz,AMA,dict(P_walk(u,2.2),ar=(1.1,1.6),curlR=.9),hm=1.7,u=u,facing="back",props={"r":tracker(u,1.0,(-6,-5))},fog=(10,6,4))
    sound_rings(d,cam,st,0.0,dz,u,n=4,maxr=2.4)
    if o: outline_glow(d,o,place3(cam,st,0.0,dz,1.7)[2],a=26)
    # rejilla del conducto de ventilacion
    ov=Image.new("RGBA",big.size,(0,0,0,0)); od=ImageDraw.Draw(ov); od.rectangle([0,0,1620,2880],fill=(4,4,6,255))
    for k in range(11): y0=int(300+k*190); od.rectangle([120,y0,1500,y0+120],fill=(0,0,0,0))
    ov=ov.filter(ImageFilter.GaussianBlur(1.2)); big=Image.alpha_composite(big.convert("RGBA"),ov).convert("RGB"); d=D(big)
    monster_arms(d,u,tone=(26,28,34),still=True,size=1.4,reach=.25)
    big=alien_fx(big,u,d); return grade(big,sat=.85,seed=int(u*30),tint=(1.03,.96,.93))
def sceneF(u):
    t=u+5; cam=run_cam(t,speed=2.3); zl=4.0*2.3+9.0+3.0; dz=cam["z"]+lerp(8.0,3.5,clamp(u/4.0)); ax=lerp(0.0,1.25,sm((u-2.0)/2.0))
    st=CORR; bg=render_room(cam,st,t,flick(t),extra=[(0.0,1.2,dz,(.4,1.0,.55),.5)]); back=new_ov()
    big=fin(composite(bg,back)); d=D(big)
    if u<4.2:
        o=P3(d,cam,st,ax,dz,AMA,dict(P_walk(t,7.0),al=(.7,1.2),ar=(1.2,1.6),curlR=.9),hm=1.7,u=t,facing="back",props={"r":tracker(t,2.5,(-6,-5))},fog=(10,6,4))
        pl=place3(cam,st,ax,dz,1.7)
        if pl: sound_rings(d,cam,st,ax,dz,t); outline_glow(d,o,pl[2])
    else:
        sound_rings(d,cam,st,1.25,dz,t,n=3,maxr=1.0)
    ov=new_ov(); box(ov,cam,st,1.0,1.55,0,2.0,dz-.45,dz+.45,(70,78,84),lt=(1,.9,.8)); 
    for k in range(7): poly3(ov,cam,st,[(.998,1.2+k*.1,dz-.3),(.998,1.2+k*.1,dz+.3),(.998,1.23+k*.1,dz+.3),(.998,1.23+k*.1,dz-.3)],(6,6,8))
    big=composite(big,ov.resize(OUTSZ,Image.BICUBIC)) if False else big
    d=D(big); still=u>4.4
    monster_arms(d,t,tone=(26,28,34),run=7.0,size=1.6,still=still,reach=.1 if still else 0)
    return grade(alien_fx(big,t,d),sat=.85,seed=int(u*30),tint=(1.02,.96,.93))
def sceneG(u):
    t=u+9; st=dict(CORR,zend=7.0); cam=run_cam(t*.3,speed=1.4,y=1.25)
    bg=render_room(cam,st,t,flick(t),extra=[(0.0,1.2,5.0,(.4,1.0,.55),.5)]); big=fin(bg); d=D(big)
    o=P3(d,cam,st,.1,cam["z"]+lerp(5,3.0,clamp(u/5)),AMA,dict(P_scared(t),al=(1.2,2.2),ar=(1.2,2.2),mouth=1.0),hm=1.7,u=t,fog=(10,6,4))
    if o: outline_glow(d,o,place3(cam,st,.1,cam["z"]+lerp(5,3.0,clamp(u/5)),1.7)[2])
    monster_arms(d,t,tone=(26,28,34),still=False,run=2.0,size=1.6,reach=clamp(u/5.0)*.9)
    big=alien_fx(big,t,d)
    f=clamp((u-4.9)/.7); a=np.asarray(big).astype(np.float32)*(1-f); return grade(Image.fromarray(a.astype(np.uint8)),sat=.85,seed=int(u*30),tint=(1.02,.96,.93))
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur): return 1.0,270,480
core.CAM=cam
if __name__=="__main__": core.main()
