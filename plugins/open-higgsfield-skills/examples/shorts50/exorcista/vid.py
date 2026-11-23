import sys,random; sys.path.insert(0,"..")
from kit import *
from rooms import mk, render_room
from terrain import render_terrain, mk as tmk
from sets import *
BEDR=mk(H=2.6,hw=2.2,zend=3.6,zback=-3.2,wall="plaster",wcol=(150,160,168),wcol2=(96,100,106),floor="wood",fcol=(104,76,52),ceil="plaster",ccol=(176,182,190),ambient=.12,amb_rgb=(.7,.82,1.0),fog=.02,fogcol=(10,14,22),fov=52)
SUBN=tmk(fov=54,ground="street",sky="night",fog=.018,fogcol=(22,26,44),hills=.03,hcol=(18,22,36),amb=(.26,.32,.5),ambient=1.0)
ACT=dict(skin=(236,196,160),hair=(120,80,50),hairstyle="long",shirt=(236,230,224),dress=True,skirt_col=(232,226,220),sleeve="long",shoes=(150,120,110),brow=(100,60,40))
ACTM=dict(skin=(226,184,150),hair=(60,44,32),hairstyle="short",shirt=(90,100,120),coat=(60,64,76),pants=(50,50,64),sleeve="long")
CREWC=dict(skin=(214,170,130),hair=(40,30,24),hairstyle="short",shirt=(70,90,110),coat=(90,70,50),pants=(60,60,74),sleeve="long",hat="cap",cap_col=(60,60,80))
FRIED=dict(skin=(230,190,156),hair=(50,40,34),hairstyle="short",glasses=True,shirt=(180,170,150),coat=(70,56,44),pants=(70,66,60),sleeve="long")
def breath(d,hx,hy,sc,u,n=7,dirx=1.0,a=130,size=1.0):
    for q in range(n):
        t=((u*.5+q/n)%1); d.E(hx+dirx*(14+t*90)*sc*size,hy+18*sc-t*40*sc*size+math.sin(t*7+q)*5*sc,(8+t*40)*sc*size,(6+t*28)*sc*size,(240,248,255,int(a*(1-t))))
def frost_tex(w=200,h=260,seed=4):
    rng=np.random.default_rng(seed); im=Image.new("RGB",(w,h),(8,12,26)); d=ImageDraw.Draw(im)
    for k in range(90):
        x=rng.random()*w; y=rng.random()*h; r=8+rng.random()*30
        for q in range(6): a=q*1.047; d.line([(x,y),(x+math.cos(a)*r,y+math.sin(a)*r)],fill=(210,230,255),width=1)
    for k in range(40): d.ellipse([rng.random()*w,rng.random()*h,0,0],fill=None) if False else None
    d.rectangle([0,0,w-1,h-1],outline=(90,80,70),width=10); d.line([(w/2,0),(w/2,h)],fill=(90,80,70),width=6); d.line([(0,h*.55),(w,h*.55)],fill=(90,80,70),width=6)
    return im
def bedroom(cam,u,warm=False):
    st=BEDR; bg=render_room(cam,st,u,1.0,extra=[(-1.5,1.4,2.4,(.55,.75,1.0),.9),(1.4,.9,2.8,(1.0,.7,.4),.5)]); back=new_ov(); front=new_ov()
    tquad(back,cam,st,(-1.2,2.0,3.59),(.2,2.0,3.59),(.2,.8,3.59),(-1.2,.8,3.59),frost_tex()); glow(back,cam,st,(-.5,1.4,3.5),(150,190,255),1.3,60,6)
    box(back,cam,st,.6,2.1,0,.5,1.4,3.5,(96,76,60)); box(back,cam,st,.6,2.1,.5,.62,1.4,3.5,(210,210,220)); box(back,cam,st,.6,2.1,.5,1.3,3.45,3.55,(80,60,44)); box(back,cam,st,.7,1.5,.62,.72,3.0,3.4,(240,240,244),shadow=False)
    box(back,cam,st,-2.1,-1.5,0,.7,1.0,1.8,(96,70,50)); lamp(back,cam,st,-1.8,1.4,h=1.15,col=(255,210,150))
    return st,bg,back,front
def sceneA(u,final=False):
    t=u+(0 if not final else 3); cam=dict(x=lerp(-1.0,-.2,sm(t/6)),y=1.5,z=lerp(-2.0,-1.0,sm(t/6)),yaw=lerp(.2,.05,sm(t/6)),pitch=.05)
    st,bg,back,front=bedroom(cam,t); big=fin(composite(bg,back)); d=D(big)
    o=P3(d,cam,st,-.1,1.4,ACT,dict(P_scared(t),al=(.8,2.2),ar=(.8,2.2),mouth=.8,look=(.4,0)),hm=1.62,u=t,fog=(10,14,22))
    if o: hx,hy=o["head"]; sc=place3(cam,st,-.1,1.4,1.62)[2]; breath(d,hx,hy,sc,t,dirx=1.0,a=150,size=1.2)
    big=snow_particles(big,t,n=50,col=(220,235,255),sz=2,speed=20,alpha=100,scale=2.2)
    return grade(vign_(big,.5),sat=.85,seed=int(u*30),tint=(.94,.98,1.08))
def vign_(img,k=.6): return Image.alpha_composite(img.convert("RGBA"),vignette_ov(img.size,k)).convert("RGB")
def sceneB(u):
    cam=dict(x=lerp(-2.0,.6,sm(u/7)),y=1.5,z=lerp(0,1.0,sm(u/7)),yaw=lerp(.2,0,sm(u/7)),pitch=.05)
    ex=[(3.8,3.0,z,(1.0,.66,.34),2.6) for z in (8,24)]+[(-3.8,3.0,16,(1.0,.66,.34),2.6)]
    bg=render_terrain(cam,SUBN,u,extra=ex); ov=new_ov()
    house(ov,cam,SUBN,-9.5,13,w=9,d=7,h=5.2,wall=(150,140,130),seed=21,t=u,lit=.5); house(ov,cam,SUBN,9.5,18,seed=22,t=u); house(ov,cam,SUBN,-9.5,30,seed=23,t=u)
    for k,z in enumerate((8,16,24)):
        x=3.8 if k%2==0 else -3.8; box(ov,cam,SUBN,x-.06,x+.06,0,3.0,z-.06,z+.06,(30,30,34),shadow=False); glow(ov,cam,SUBN,(x,3.0,z),(255,190,110),1.0,90,6)
    box(ov,cam,SUBN,-.8,.8,.4,1.1,5.5,6.1,(40,42,46)); box(ov,cam,SUBN,-.2,.2,.5,.9,5.1,5.5,(30,30,34)); box(ov,cam,SUBN,-.4,.4,0,.4,5.6,6.0,(70,70,74))
    box(ov,cam,SUBN,-3.0,-2.0,2.0,3.0,7.0,7.4,(224,228,236),emis=.6,shadow=False); glow(ov,cam,SUBN,(-2.5,2.5,6.8),(255,250,235),2.0,100,7)
    big=fin(composite(bg,ov)); d=D(big)
    P3(d,cam,SUBN,-1.6,6.0,FRIED,dict(P_point(u,dirx=1),ar=(1.45,1.6),mouth=.5),hm=1.78,u=u,fog=(22,26,44)); P3(d,cam,SUBN,1.4,5.2,CREWC,dict(P_hold(u,r=(1.4,1.8))),hm=1.75,u=u,fog=(22,26,44))
    big=snow_particles(big,u,n=60,col=(230,240,255),sz=2.4,speed=30,alpha=130,scale=2.4)
    ptext(D(big),40,270,"1973",9,(255,255,255))
    return grade(vign_(big,.4),sat=.9,seed=int(u*30),tint=(.96,.98,1.06))
def sceneC(u):
    cam=dict(x=lerp(.6,-.3,sm(u/9)),y=1.5,z=lerp(-2.4,-1.6,sm(u/9)),yaw=lerp(-.15,.1,sm(u/9)),pitch=.05)
    st,bg,back,front=bedroom(cam,u)
    for (x,col) in ((-1.0,(200,206,214)),(.6,(190,196,206))):
        box(back,cam,st,x-.5,x+.5,0,1.3,3.0,3.55,col); 
        for k in range(5): poly3(back,cam,st,[(x-.4,.25+k*.2,2.99),(x+.4,.25+k*.2,2.99),(x+.4,.3+k*.2,2.99),(x-.4,.3+k*.2,2.99)],(60,66,74))
        for q in range(6): glow(back,cam,st,(x+(q-2.5)*.1,.1,2.7),(200,230,255),.5,80,4)
    big=fin(composite(bg,back)); d=D(big)
    for k,(x,stl) in enumerate(((-.9,CREWC),(.5,ACTM),(1.6,ACT))):
        o=P3(d,cam,st,x,1.8,stl,dict(P_scared(u,k),al=(.4,1.0),ar=(.4,1.0)),hm=1.7,u=u,fog=(10,14,22))
        if o: sc=place3(cam,st,x,1.8,1.7)[2]; breath(d,o["head"][0],o["head"][1],sc,u+k,dirx=1.0,a=130)
    tt=int(lerp(16,-4,sm(u/9))); d.R(150,230,390,330,(8,10,14,200),12); ptext(d,170,254,("-" if tt<0 else "")+str(abs(tt))+" C",9,(130,210,255))
    return grade(vign_(big,.5),sat=.85,seed=int(u*30),tint=(.94,.98,1.08))
def sceneD(u):
    st=dict(BEDR,fov=40); cam=dict(x=0,y=1.4,z=-1.0,yaw=0,pitch=.0)
    st_,bg,back,front=bedroom(cam,u); bg=render_room(cam,st,u,1.0,extra=[(-1.5,1.4,2.4,(.55,.75,1.0),.9)]); big=fin(bg); d=D(big)
    o=P3(d,cam,st,0,.7,ACT,dict(P_idle(u),mouth=.7,tilt=.06*math.sin(u*1.4)),hm=1.4,u=u,fog=(10,14,22))
    if o: sc=place3(cam,st,0,.7,1.4)[2]; breath(d,o["head"][0]+8*sc,o["head"][1],sc,u,n=9,dirx=1.0,a=170,size=1.7)
    return grade(vign_(big,.5),sat=.85,seed=int(u*30),tint=(.94,.98,1.08))
def sceneE(u):
    cam=dict(x=lerp(-1.0,.4,sm(u/7)),y=1.5,z=-1.8,yaw=lerp(.15,-.05,sm(u/7)),pitch=.05)
    st,bg,back,front=bedroom(cam,u)
    box(back,cam,st,-.8,.8,0,.35,1.6,2.6,(90,64,48)); box(back,cam,st,-.2,.2,2.2,3.0,2.0,2.05,(70,70,76),shadow=False) if False else None
    big=fin(composite(bg,back)); d=D(big)
    # arnes de seguridad: poste y cable atado a la cintura; el cable sube a una polea
    o=P3(d,cam,st,.0,2.0,ACT,dict(P_scared(u),al=(.5,1.3),ar=(.5,1.3),mouth=.3,lean=-.12*abs(math.sin(u*2))),hm=1.62,u=u,fog=(10,14,22))
    if o:
        hx,hy=o["hip"]; d.L(hx,hy,hx+70,hy-560,(210,210,220,255),3); d.E(hx+70,hy-560,12,12,(160,160,170,255)); d.R(hx-30,hy-10,hx+30,hy+8,(210,170,60,255),3)
    P3(d,cam,st,1.6,2.4,CREWC,dict(P_hold(u,r=(1.6,2.0),l=(1.6,2.0),grip=1.0),mouth=.3),hm=1.78,u=u,fog=(10,14,22))
    ptext(d,40,270,"SE CUENTA",5,(255,220,120))
    return grade(vign_(big,.5),sat=.85,seed=int(u*30),tint=(.94,.98,1.08))
def sceneF(u):
    cam=dict(x=0,y=1.4,z=-1.2,yaw=0,pitch=.04); st=BEDR
    bg=render_room(cam,st,u,1.0,extra=[(0,1.5,1.6,(1.0,.8,.5),.6)]); big=fin(bg); d=D(big)
    for k in range(34):
        h=14+abs(math.sin(k*.6+u*8))*210*(1-abs(k-17)/20)*sm(u/1.0); d.R(60+k*13,560-h,60+k*13+8,560+h,(255,230,150,235),2)
    def boom(dd,x,y,a,s,K=1.0): dd.L(x,y,x+120*K,y-300*K,(40,40,44,255),4*K); dd.R(x+100*K,y-330*K,x+150*K,y-296*K,(60,60,66,255),6*K)
    P3(d,cam,st,1.2,2.0,dict(CREWC,hat="headphones"),dict(P_hold(u,r=(2.0,2.9),l=(1.9,2.6),grip=1.0)),hm=1.78,u=u,props={"r":boom},fog=(10,14,22))
    film_strip(d,830,u,h=100)
    ptext(d,40,235,"",3,(255,255,255))
    return grade(vign_(big,.5),sat=.9,seed=int(u*30),tint=(1.0,.98,1.0))
def sceneG(u):
    cam=dict(x=lerp(.8,-.2,sm(u/6)),y=1.5,z=lerp(-1.8,-.9,sm(u/6)),yaw=lerp(-.2,.0,sm(u/6)),pitch=.05)
    st,bg,back,front=bedroom(cam,u); big=fin(composite(bg,back)); d=D(big)
    o=P3(d,cam,st,-.2,1.9,ACT,dict(P_idle(u),mouth=.6,look=(.3,0)),hm=1.62,u=u,fog=(10,14,22))
    if o: sc=place3(cam,st,-.2,1.9,1.62)[2]; breath(d,o["head"][0],o["head"][1],sc,u,dirx=1.0,a=150,size=1.2)
    big=snow_particles(big,u,n=60,col=(220,235,255),sz=2,speed=20,alpha=100,scale=2.2)
    return grade(vign_(big,.6),sat=.85,seed=int(u*30),tint=(.94,.98,1.08))
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur): return 1.0,270,480
core.CAM=cam
if __name__=="__main__": core.main()
