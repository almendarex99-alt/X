import sys; sys.path.insert(0,"..")
from kit import *
from rooms import mk, render_room
from terrain import render_terrain, mk as tmk
from sets import *
def g(v): return (v,v,v)
NIGHT=tmk(fov=54,ground="grass",sky="night",fog=.016,fogcol=(26,28,40),hills=.03,hcol=(14,16,24),amb=(.30,.34,.5),ambient=1.0)
ZB=dict(skin=g(176),hair=g(40),hairstyle="short",shirt=g(90),pants=g(52),shoes=g(24),sleeve="long",brow=g(30),eyes=g(10),mouth_col=g(30))
ZW=dict(ZB,hairstyle="long",hair=g(36),shirt=g(120),dress=True,skirt_col=g(110))
ZC=dict(ZB,hairstyle="bald",shirt=g(70),pants=g(40))
MAN=dict(skin=g(204),hair=g(30),hairstyle="short",shirt=g(210),pants=g(60),shoes=g(20),sleeve="long",brow=g(30),eyes=g(20),mouth_col=g(70))
WOMAN=dict(skin=g(214),hair=g(50),hairstyle="long",shirt=g(236),dress=True,skirt_col=g(226),sleeve="long",brow=g(40),eyes=g(20),mouth_col=g(70),shoes=g(30))
DIRN=dict(MAN,glasses=True,beard=True,shirt=g(150),coat=g(60))
ROOM=mk(H=2.6,hw=2.4,zend=4.0,zback=-3.0,wall="wood",wcol=(120,110,100),floor="wood",fcol=(100,90,80),ceil="plaster",ccol=(190,186,180),ambient=.22,fog=.01,fov=52,plights=dict(gap=100,off=1,xs=(0,),y=2.3,rgb=(1,.96,.9),I=.3,k=.5))
def bw(img,seed=0,grain=9):
    a=np.asarray(img).astype(np.float32).mean(2); a=np.clip((a-18)*1.15,0,255); a+=np.random.default_rng(seed).normal(0,grain,a.shape)
    yy,xx=np.mgrid[0:a.shape[0],0:a.shape[1]]; r=((xx-a.shape[1]/2)/(a.shape[1]/2))**2+((yy-a.shape[0]/2)/(a.shape[0]/2))**2; a*=(1-.45*np.clip(r-.3,0,1))
    if seed%7==0: a[:, ::]*=.98
    out=np.stack([a,a,a],-1); return Image.fromarray(np.clip(out,0,255).astype(np.uint8))
def farm_scene(cam,u,zs=()):
    ex=[(0,2.5,14,(1,.95,.85),1.8)]; bg=render_terrain(cam,NIGHT,u,extra=ex); ov=new_ov()
    house(ov,cam,NIGHT,-6.5,14,w=9,d=7,h=4.4,wall=(150,146,140),seed=51,t=u,lit=.5); 
    for (x,z) in ((6,8),(-9,24),(9,22)): tree(ov,cam,NIGHT,x,z,h=3.4,col=(30,40,34),trunk=(40,34,30))
    box(ov,cam,NIGHT,-12,12,0,1.0,30,30.2,(60,54,50),shadow=False)
    return bg,ov
def sceneA(u,final=False):
    t=u+(0 if not final else 3); cam=dict(x=lerp(-1.5,0,sm(t/7)),y=1.5,z=lerp(-1,2,sm(t/7)),yaw=lerp(.15,0,sm(t/7)),pitch=.05)
    bg,ov=farm_scene(cam,t); big=fin(composite(bg,ov)); d=D(big)
    for k,(x,z,st) in enumerate(((1.5,9,ZB),(-.6,11,ZW),(2.8,12,ZC),(.4,7.2,ZB))): P3(d,cam,NIGHT,x-u*.05*(1+k*.1),z-t*.25,st,P_zombie(t,k*1.3),hm=1.75,u=t,fog=(26,28,40))
    return grade(bw(big,int(u*30)),sat=1,grain=0,seed=int(u*30))
def sceneB(u):
    cam=dict(x=lerp(-2.4,.6,sm(u/7)),y=1.5,z=lerp(0,.8,sm(u/7)),yaw=lerp(.2,0,sm(u/7)),pitch=.05)
    bg,ov=farm_scene(cam,u)
    box(ov,cam,NIGHT,-.5,.5,.5,1.1,5.2,5.8,(40,42,46)); box(ov,cam,NIGHT,-.2,.2,.6,.95,4.8,5.2,(30,30,34)); box(ov,cam,NIGHT,-.4,.4,0,.5,5.3,5.7,(70,70,74))
    for (x,z) in ((-3,6),(3,7)): box(ov,cam,NIGHT,x-.5,x+.5,2.0,3.0,z,z+.4,(224,228,236),emis=.6,shadow=False); box(ov,cam,NIGHT,x-.04,x+.04,0,2.0,z+.15,z+.25,(40,40,44),shadow=False); glow(ov,cam,NIGHT,(x,2.5,z-.2),(255,250,230),2.0,100,7)
    big=fin(composite(bg,ov)); d=D(big)
    P3(d,cam,NIGHT,-1.2,5.5,DIRN,dict(P_point(u,dirx=1),ar=(1.45,1.6),mouth=.5),hm=1.78,u=u,fog=(26,28,40)); P3(d,cam,NIGHT,1.3,5.4,MAN,dict(P_hold(u,r=(1.3,2.0))),hm=1.75,u=u,fog=(26,28,40))
    clapper(d,430,830,1.0,open_=clamp(math.sin(u*2.4))); ptext(d,40,270,"1968",9,g(240)); ptext(d,40,340,"PITTSBURGH",5,g(240))
    return grade(bw(big,int(u*30)),sat=1,grain=0,seed=int(u*30))
def sceneC(u):
    st=ROOM; cam=dict(x=lerp(-.6,.3,sm(u/9)),y=1.4,z=lerp(-1,.2,sm(u/9)),yaw=lerp(.15,0,sm(u/9)),pitch=.04)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.2,2.0,(1,.95,.9),.8)]); back=new_ov(); box(back,cam,st,-1.2,1.2,0,.76,2.4,3.2,(120,100,80))
    big=fin(composite(bg,back)); d=D(big)
    o=P3(d,cam,st,0,2.0,MAN,dict(al=(.95,1.85),ar=(.95,1.85),ll=(.05,.05),lr=(.05,.05),bob=math.sin(u*2),tilt=.05,look=(0,.8),mouth=.2,curlL=.9,curlR=.9,hands_front=True),hm=1.78,u=u,fog=(20,20,20))
    if o:
        cx=(o["hand_l"][0]+o["hand_r"][0])/2; cy=(o["hand_l"][1]+o["hand_r"][1])/2; d.R(cx-70,cy-30,cx+70,cy+34,g(40),12); d.R(cx-66,cy-26,cx+66,cy-4,g(70),10)
        for k in range(3): d.E(cx-30+k*30,cy+90+(u*60+k*30)%90,14,6,g(230))
    ptext(d,40,270,"POCO DINERO",5.6,g(240))
    return grade(bw(big,int(u*30)),sat=1,grain=0,seed=int(u*30))
def title_tex(txt,w=320,h=140,cross=0.0,col=g(236)):
    im=Image.new("RGB",(w,h),col); d=ImageDraw.Draw(im); d.rectangle([6,6,w-7,h-7],outline=g(40),width=4); d.text((w/2,h/2),txt,font=font(30,True),fill=g(30),anchor="mm")
    if cross>0: d.line([(10,10),(10+int((w-20)*cross),10+int((h-20)*cross))],fill=g(30),width=8)
    return im
def sceneD(u):
    st=ROOM; cam=dict(x=lerp(-.6,.3,sm(u/9)),y=1.4,z=lerp(-1,.3,sm(u/9)),yaw=.1,pitch=.04)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.4,2.4,(1,.95,.9),.8)]); back=new_ov()
    tquad(back,cam,st,(-1.9,2.3,3.99),(-.4,2.3,3.99),(-.4,1.4,3.99),(-1.9,1.4,3.99),title_tex("OTRO TITULO",cross=sm(u/2.0))); tquad(back,cam,st,(.0,2.3,3.99),(1.5,2.3,3.99),(1.5,1.4,3.99),(.0,1.4,3.99),title_tex("NUEVO TITULO"))
    big=fin(composite(bg,back)); d=D(big)
    def marker(dd,x,y,a,s,K=1.0): dd.R(x-5*K,y-8*K,x+5*K,y+36*K,g(30),3*K)
    P3(d,cam,st,.0,2.8,MAN,dict(al=(1.3,1.7),ar=(1.9,1.3+.5*math.sin(u*5)),ll=(.05,.05),lr=(.05,.05),bob=0,tilt=.05,look=(-.5,0),mouth=.2,curlR=1.0,hands_front=True),hm=1.78,u=u,props={"r":marker},fog=(20,20,20))
    return grade(bw(big,int(u*30)),sat=1,grain=0,seed=int(u*30))
def doc_tex(u,w=300,h=400):
    im=Image.new("RGB",(w,h),g(240)); d=ImageDraw.Draw(im)
    for k in range(12): d.rectangle([20,50+k*26,w-20-((k*37)%90),58+k*26],fill=g(120))
    d.text((w/2,22),"AVISO DE DERECHOS",font=mono(16,True),fill=g(30),anchor="mm"); d.ellipse([w/2-34,h-100,w/2+34,h-34],outline=g(30),width=5); d.text((w/2,h-67),"C",font=font(40,True),fill=g(30),anchor="mm")
    r=sm((u-1.5)/1.0); d.line([(w/2-40,h-106),(w/2+40,h-28)],fill=g(20),width=int(10*r)+1) if r>0 else None; d.line([(w/2+40,h-106),(w/2-40,h-28)],fill=g(20),width=int(10*r)+1) if r>0 else None
    return im
def sceneE(u):
    st=ROOM; cam=dict(x=lerp(-.5,.3,sm(u/8)),y=1.4,z=lerp(-1,.2,sm(u/8)),yaw=.08,pitch=.04)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.4,2.4,(1,.95,.9),.8)]); back=new_ov(); box(back,cam,st,-1.4,1.4,0,.76,2.4,3.4,(110,92,74)); tquad(back,cam,st,(-.45,.77,2.6),(.45,.77,2.6),(.45,.77,3.3),(-.45,.77,3.3),doc_tex(u))
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,-1.0,3.8,WOMAN,dict(P_point(u,dirx=1),ar=(1.4,1.6)),hm=1.68,u=u,fog=(20,20,20)); P3(d,cam,st,1.0,3.8,MAN,dict(P_talk(u),al=(1.3,1.7)),hm=1.78,u=u,fog=(20,20,20))
    ptext(d,40,270,"SIN AVISO",6,g(240))
    return grade(bw(big,int(u*30)),sat=1,grain=0,seed=int(u*30))
def sceneF(u):
    st=ROOM; cam=dict(x=lerp(-.5,.4,sm(u/8)),y=1.2,z=lerp(-.6,.5,sm(u/8)),yaw=.0,pitch=.03)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.0,2.6,(.8,.9,1.0),1.8)]); back=new_ov()
    box(back,cam,st,-1.0,1.0,0,.5,2.5,3.2,(80,60,44)); box(back,cam,st,-.62,.62,.5,1.2,2.55,3.1,(70,60,50)); tquad(back,cam,st,(-.5,1.12,2.545),(.5,1.12,2.545),(.5,.58,2.545),(-.5,.58,2.545),crt(Image.fromarray((np.random.default_rng(int(u*20)).random((90,120))*200).astype(np.uint8)).convert("RGB"),1.0,int(u*30)))
    glow(back,cam,st,(0,.9,2.5),(220,230,255),1.5,70,6)
    box(back,cam,st,-2.2,-1.5,0,.8,2.6,3.4,(90,70,50))
    big=fin(composite(bg,back)); d=D(big)
    for k,(x,stl) in enumerate(((-.8,MAN),(0,WOMAN),(.8,DIRN))): P3(d,cam,st,x,.5,stl,dict(P_idle(u,k),look=(0,0)),hm=1.15,u=u,y0=-.08,bust=True,facing="back",fog=(20,20,20))
    for k in range(3): d.E(80+k*70,300,30,30,g(200)); d.E(80+k*70,300,22,22,g(40)); [d.E(80+k*70+math.cos(u*3+q*1.05)*13,300+math.sin(u*3+q*1.05)*13,6,6,g(200)) for q in range(6)]
    ptext(d,40,270,"PARA TODOS",6,g(240))
    return grade(bw(big,int(u*30)),sat=1,grain=0,seed=int(u*30))
def sceneG(u):
    cam=dict(x=lerp(-1,1,sm(u/6)),y=1.5,z=lerp(-1,1,sm(u/6)),yaw=lerp(.1,-.1,sm(u/6)),pitch=.05)
    bg,ov=farm_scene(cam,u); big=fin(composite(bg,ov)); d=D(big)
    for k in range(6): P3(d,cam,NIGHT,-3.5+k*1.4,7+(k%3)*1.2-u*.2,[ZB,ZW,ZC][k%3],P_zombie(u,k*1.1),hm=1.75,u=u,fog=(26,28,40))
    film_strip(d,830,u,h=90)
    return grade(bw(big,int(u*30)),sat=1,grain=0,seed=int(u*30))
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur): return 1.0,270,480
core.CAM=cam
if __name__=="__main__": core.main()
