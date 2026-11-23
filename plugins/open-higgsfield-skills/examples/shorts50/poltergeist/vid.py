import sys; sys.path.insert(0,"..")
from kit import *
from rooms import mk, render_room
from terrain import render_terrain, mk as tmk
from sets import *
NIGHT=tmk(fov=54,ground="grass",sky="night",fog=.02,fogcol=(18,24,40),hills=.04,hcol=(14,18,30),amb=(.28,.34,.55),ambient=1.0)
WARE=mk(H=4.0,hw=3.6,zend=7.0,zback=-3.0,wall="concrete",wcol=(130,128,122),floor="concrete",fcol=(100,98,94),ceil="plaster",ccol=(70,68,66),ambient=.14,amb_rgb=(.9,.95,1),fov=54,fog=.02,fogcol=(10,10,12),
         plights=dict(gap=4,off=1,xs=(0,),y=3.7,rgb=(1,.96,.85),I=.6,k=.2))
ACTR=dict(skin=(238,200,166),hair=(180,130,70),hairstyle="long",shirt=(232,228,236),dress=True,skirt_col=(226,222,232),sleeve="long",shoes=(150,120,110),brow=(120,80,40))
CREWP=dict(skin=(214,170,130),hair=(40,30,24),hairstyle="short",shirt=(70,90,110),coat=(80,70,56),pants=(60,60,74),sleeve="long",hat="cap",cap_col=(60,60,80))
DIRP=dict(skin=(230,190,156),hair=(60,50,40),hairstyle="short",beard=True,shirt=(190,80,70),coat=(50,56,70),pants=(70,66,60),sleeve="long",glasses=True)
CLK=dict(skin=(226,184,150),hair=(210,210,210),hairstyle="short",shirt=(240,240,244),coat=(236,236,240),pants=(60,60,76),sleeve="long")
def vign_(img,k=.6): return Image.alpha_composite(img.convert("RGBA"),vignette_ov(img.size,k)).convert("RGB")
def yard(cam,u,lights=True):
    ex=[(0,6,16,(1,.95,.85),2.5),(-6,3,8,(1,.9,.8),1.2)]
    bg=render_terrain(cam,NIGHT,u,extra=ex); ov=new_ov()
    house(ov,cam,NIGHT,-12,26,w=12,d=8,h=5.6,wall=(176,166,150),seed=31,t=u,lit=.6)
    # piscina: foso rectangular con borde y barro
    xs=(-3.0,3.0); zs=(5.0,11.0)
    poly3(ov,cam,NIGHT,[(xs[0]-.5,.02,zs[0]-.5),(xs[1]+.5,.02,zs[0]-.5),(xs[1]+.5,.02,zs[1]+.5),(xs[0]-.5,.02,zs[1]+.5)],(150,150,146))
    poly3(ov,cam,NIGHT,[(xs[0],.03,zs[0]),(xs[1],.03,zs[1]-7),(xs[1],.03,zs[1]),(xs[0],.03,zs[1])],(62,44,30)) if False else poly3(ov,cam,NIGHT,[(xs[0],.03,zs[0]),(xs[1],.03,zs[0]),(xs[1],.03,zs[1]),(xs[0],.03,zs[1])],(62,44,30))
    for k in range(10): poly3(ov,cam,NIGHT,[(xs[0]+k*.6,.04,zs[0]+(k%3)*2),(xs[0]+k*.6+.9,.04,zs[0]+(k%3)*2),(xs[0]+k*.6+.9,.04,zs[0]+(k%3)*2+1.2),(xs[0]+k*.6,.04,zs[0]+(k%3)*2+1.2)],(78,56,38))
    return bg,ov
def sk_layer(big,cam,st,x,z,mud=True,u=0.0,hm=1.8,wave=0.0,sway=1.0):
    pl=place3(cam,st,x,z,hm); 
    if not pl: return big
    lx,ly,sc,z2=pl; lay=Image.new("RGBA",big.size,(0,0,0,0)); dd=D(lay); skeleton(dd,lx,ly+ 40*sc,sc,u,wave=wave,sway=sway)
    arr=np.asarray(lay).copy(); cut=int(ly*3)   # recorta por debajo del barro
    arr[cut:,:,3]=0; lay=Image.fromarray(arr)
    return Image.alpha_composite(big.convert("RGBA"),lay).convert("RGB")
def sceneA(u,final=False):
    t=u+(0 if not final else 3); cam=dict(x=lerp(-1.5,.6,sm(t/7)),y=1.4,z=lerp(0,3.0,sm(t/7)),yaw=lerp(.12,-.04,sm(t/7)),pitch=.05)
    bg,ov=yard(cam,t); big=fin(composite(bg,ov))
    rise=sm(clamp(t/3.0)); 
    for k,(x,z,w) in enumerate(((-1.4,7.8,.3),(0.4,9.2,.9),(1.8,6.9,.5))): big=sk_layer(big,cam,NIGHT,x,z+(1-rise)*.0,u=t+k,hm=2.2*rise+.01,wave=w*math.sin(t*1.5+k),sway=1.0)
    big=snow_particles(big,t,n=40,col=(200,200,210),sz=2,speed=15,alpha=60,scale=2.2)
    return grade(vign_(big,.5),sat=.9,seed=int(u*30),tint=(.96,.98,1.06))
def sceneB(u):
    cam=dict(x=lerp(-2.4,.8,sm(u/7)),y=1.5,z=lerp(0,1.2,sm(u/7)),yaw=lerp(.2,.0,sm(u/7)),pitch=.05)
    bg,ov=yard(cam,u); box(ov,cam,NIGHT,-.8,.8,.4,1.1,5.0,5.6,(40,42,46)); box(ov,cam,NIGHT,-.2,.2,.5,.9,4.6,5.0,(30,30,34)); box(ov,cam,NIGHT,-.4,.4,0,.4,5.1,5.5,(70,70,74))
    for (x,z) in ((-4,6),(4,8)): box(ov,cam,NIGHT,x-.5,x+.5,2.0,3.0,z,z+.4,(224,228,236),emis=.6,shadow=False); box(ov,cam,NIGHT,x-.04,x+.04,0,2.0,z+.15,z+.25,(40,40,44),shadow=False); glow(ov,cam,NIGHT,(x,2.5,z-.2),(255,250,230),2.0,100,7)
    big=fin(composite(bg,ov)); d=D(big)
    P3(d,cam,NIGHT,-1.4,5.8,DIRP,dict(P_point(u,dirx=1),ar=(1.45,1.6),mouth=.5),hm=1.8,u=u,fog=(18,24,40)); P3(d,cam,NIGHT,1.5,5.0,CREWP,dict(P_hold(u,r=(1.4,1.8))),hm=1.75,u=u,fog=(18,24,40)); P3(d,cam,NIGHT,3.0,6.5,dict(CREWP,hat=None,hair=(120,80,50)),dict(P_walk(u,2.0)),hm=1.7,u=u,fog=(18,24,40))
    ptext(D(big),40,270,"1982",9,(255,255,255))
    return grade(vign_(big,.4),sat=.9,seed=int(u*30),tint=(.96,.98,1.06))
def sceneC(u):
    cam=dict(x=lerp(-3.0,2.0,sm(u/9)),y=1.5,z=lerp(2.0,3.5,sm(u/9)),yaw=lerp(.5,.0,sm(u/9)),pitch=.14)
    bg,ov=yard(cam,u); big=fin(composite(bg,ov))
    for k,(x,z) in enumerate(((-2.0,6.5),(-.4,7.5),(1.2,6.2),(2.2,8.6),(-1.2,9.2),(.6,10.0))): big=sk_layer(big,cam,NIGHT,x,z,u=u+k,hm=1.0+.2*(k%2),wave=.4*math.sin(u+k),sway=.6)
    d=D(big)
    for k,(x,z,stl) in enumerate(((-4.4,12,CREWP),(4.3,12.5,DIRP))): P3(d,cam,NIGHT,x,z,stl,dict(P_point(u,k),ar=(1.2,1.5)),hm=1.78,u=u,fog=(18,24,40))
    return grade(vign_(big,.5),sat=.9,seed=int(u*30),tint=(.96,.98,1.06))
def tag_tex(txt,price,col):
    im=Image.new("RGB",(260,150),col); d=ImageDraw.Draw(im); d.rectangle([4,4,255,145],outline=(30,30,30),width=4); d.text((130,44),txt,font=font(34,True),fill=(20,20,20),anchor="mm"); d.text((130,100),price,font=font(44,True),fill=(20,20,20),anchor="mm"); return im
def sceneD(u):
    st=WARE; cam=dict(x=lerp(-1.2,.8,sm(u/7)),y=1.5,z=lerp(-2.0,-1.0,sm(u/7)),yaw=lerp(.1,-.05,sm(u/7)),pitch=.05)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.8,3.0,(1,.95,.85),.7)]); back=new_ov()
    box(back,cam,st,-2.8,-.4,0,.9,3.0,5.0,(150,110,70)); box(back,cam,st,-2.8,-.4,.9,1.0,3.0,5.0,(120,84,50))
    tquad(back,cam,st,(-2.0,2.4,2.98),(-1.0,2.4,2.98),(-1.0,1.8,2.98),(-2.0,1.8,2.98),tag_tex("REAL","BARATO",(150,210,150)))
    box(back,cam,st,.6,3.0,0,.7,3.0,4.6,(90,150,200)); tquad(back,cam,st,(1.2,2.4,2.98),(2.4,2.4,2.98),(2.4,1.8,2.98),(1.2,1.8,2.98),tag_tex("PLASTICO","CARO",(240,170,150)))
    big=fin(composite(bg,back)); d=D(big)
    # esqueleto dentro de la caja (de lado) con su etiqueta de proveedor
    for k,(x,y) in enumerate(((-1.6,.95),(1.8,.75))): pass
    P3(d,cam,st,.0,3.4,CLK,dict(P_hold(u,r=(1.3,1.8)),mouth=.3),hm=1.75,u=u,fog=(10,10,12))
    ptext(d,40,270,"SE CUENTA",5,(255,220,120))
    return grade(vign_(big,.4),sat=.9,seed=int(u*30),tint=(1.0,.99,.96))
def sceneE(u):
    cam=dict(x=lerp(-1.4,1.0,sm(u/7)),y=1.3,z=lerp(3.0,4.5,sm(u/7)),yaw=lerp(.3,-.1,sm(u/7)),pitch=.14)
    bg,ov=yard(cam,u); big=fin(composite(bg,ov))
    for k,(x,z) in enumerate(((-2.4,6.8),(2.4,7.2),(-.8,9.6),(1.6,9.0))): big=sk_layer(big,cam,NIGHT,x,z,u=u+k,hm=1.0,wave=.3,sway=.5)
    d=D(big)
    P3(d,cam,NIGHT,.0,6.0,ACTR,dict(P_scared(u),al=(.8,2.2),ar=(.8,2.2),mouth=1.0),hm=1.62,u=u,fog=(18,24,40))
    return grade(vign_(big,.5),sat=.9,seed=int(u*30),tint=(.96,.98,1.06))
def sceneF(u):
    cam=dict(x=0,y=1.4,z=-.5,yaw=0,pitch=.03); st=dict(NIGHT,fov=40)
    bg,ov=yard(cam,u); big=fin(bg); d=D(big)
    ov2=Image.new("RGBA",big.size,(0,0,0,0)); od=ImageDraw.Draw(ov2); od.rectangle([0,0,1620,2880],fill=(0,0,0,150)); big=Image.alpha_composite(big.convert("RGBA"),ov2).convert("RGB"); d=D(big)
    P3(d,cam,st,0,.9,ACTR,dict(P_scared(u),al=(.8,2.2),ar=(.8,2.2),mouth=.9,look=(.3,0)),hm=1.4,u=u,fog=(18,24,40))
    for k in range(5): xx=60+k*100; d.L(xx,300,xx+math.sin(u*6+k)*18,420+((u*100+k*30)%80),(160,220,255,int(120-k*10)),3)
    return grade(vign_(big,.6),sat=.85,seed=int(u*30),tint=(.96,.98,1.08))
def static_tex(u,w=200,h=150):
    rng=np.random.default_rng(int(u*30)); a=(rng.random((h,w))*255).astype(np.uint8); im=Image.fromarray(a).convert("RGB")
    d=ImageDraw.Draw(im); 
    for k in range(3): y=int((u*80+k*50)%h); d.rectangle([0,y,w,y+4],fill=(255,255,255))
    return im
def sceneG(u):
    st=mk(H=2.5,hw=2.4,zend=3.4,zback=-3.0,wall="plaster",wcol=(90,86,80),floor="carpet",fcol=(70,56,50),ceil="plaster",ccol=(100,96,90),ambient=.04,amb_rgb=(.7,.8,1),fog=.03,fogcol=(4,4,6),fov=50)
    cam=dict(x=lerp(-.4,.4,sm(u/6)),y=1.15,z=lerp(-1.6,-.6,sm(u/6)),yaw=.0,pitch=.03)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.0,2.6,(.8,.9,1.0),1.8*(.7+.3*math.sin(u*40)))]); back=new_ov()
    box(back,cam,st,-.8,.8,0,.5,2.8,3.3,(60,50,44)); box(back,cam,st,-.62,.62,.5,1.25,2.85,3.3,(70,60,50))
    tquad(back,cam,st,(-.5,1.18,2.845),(.5,1.18,2.845),(.5,.58,2.845),(-.5,.58,2.845),crt(static_tex(u),1.2,int(u*30)))
    glow(back,cam,st,(0,.9,2.7),(200,220,255),1.4,80,6)
    big=fin(composite(bg,back)); d=D(big)
    for k,(x,stl) in enumerate(((-.7,dict(CREWP,hat=None)),(.6,dict(ACTR)))): P3(d,cam,st,x,.6,stl,dict(P_idle(u,k),look=(0,0)),hm=1.15,u=u,y0=-.1,bust=True,facing="back",fog=(4,4,6))
    return grade(vign_(big,.6),sat=.9,seed=int(u*30),tint=(.98,.99,1.06))
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur): return 1.0,270,480
core.CAM=cam
if __name__=="__main__": core.main()
