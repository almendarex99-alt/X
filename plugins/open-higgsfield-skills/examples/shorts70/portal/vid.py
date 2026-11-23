import sys; sys.path.insert(0,"..")
from kit import *
from rooms import mk, render_room
from sets import *
from portal.helpers import glados, cake, cube, note, mic
BLU=(60,170,255); ORG=(255,150,40)
CH=mk(H=4.2,hw=3.0,zend=8.0,zback=-3.0,wall="concrete",wcol=(226,228,232),wcol2=(200,204,208),floor="tile",fcol=(214,218,222),ceil="plaster",ccol=(206,210,216),ambient=.30,amb_rgb=(.95,.98,1),fog=.01,fogcol=(120,124,130),fov=54,
      plights=dict(gap=3.5,off=1,xs=(0,),y=3.9,rgb=(.9,.95,1),I=.5,k=.2))
DARK=mk(H=4.2,hw=3.0,zend=8.0,zback=-3.0,wall="metal",wcol=(60,64,70),floor="rubber",fcol=(40,42,46),ceil="pipes",ccol=(40,42,46),ambient=.10,amb_rgb=(.9,.95,1),fog=.03,fogcol=(4,4,6),fov=54,strip=(255,190,60),
        plights=dict(gap=100,off=3,xs=(0,),y=3.0,rgb=(1,.8,.4),I=1.0,k=.3))
SUBJ=dict(skin=(226,176,140),hair=(70,44,30),hairstyle="ponytail",shirt=(236,236,236),sleeve="none",pants=(240,120,30),shoes=(60,60,68),brow=(50,30,20),belt=(200,200,206))
ACTRESS=dict(skin=(236,196,160),hair=(120,70,40),hairstyle="long",shirt=(90,60,130),hat="headphones",sleeve="long",pants=(50,50,70))
SINGER=dict(skin=(226,186,150),hair=(80,60,40),hairstyle="short",glasses=True,shirt=(60,110,90),sleeve="long",pants=(60,60,70))
def portal_tex(col,w=240,h=420):
    im=Image.new("RGBA",(w,h),(0,0,0,0)); d=ImageDraw.Draw(im)
    for k in range(10): d.ellipse([k*3,k*4,w-k*3,h-k*4],outline=col+(int(255-k*22),),width=4)
    d.ellipse([30,42,w-30,h-42],fill=(10,14,24,255)); 
    for q in range(30): a=q*.21; d.ellipse([w/2+math.cos(a)*(w/2-34)-3,h/2+math.sin(a)*(h/2-46)-3,w/2+math.cos(a)*(w/2-34)+3,h/2+math.sin(a)*(h/2-46)+3],fill=(255,255,255,200))
    return im
def portals(back,cam,st,z=7.99,xb=-1.4,xo=1.4,u=0.0):
    tquad(back,cam,st,(xb-.55,2.6,z),(xb+.55,2.6,z),(xb+.55,.2,z),(xb-.55,.2,z),portal_tex(BLU)); tquad(back,cam,st,(xo-.55,2.6,z),(xo+.55,2.6,z),(xo+.55,.2,z),(xo-.55,.2,z),portal_tex(ORG))
    glow(back,cam,st,(xb,1.4,z-.1),BLU,1.2,60,5); glow(back,cam,st,(xo,1.4,z-.1),ORG,1.2,60,5)
def vign_(img,k=.5): return Image.alpha_composite(img.convert("RGBA"),vignette_ov(img.size,k)).convert("RGB")
def sceneA(u,final=False):
    t=u+(0 if not final else 3); st=DARK; cam=dict(x=lerp(-.5,.3,sm(t/6)),y=1.5,z=lerp(-2.0,-.8,sm(t/6)),yaw=.0,pitch=.06)
    bg=render_room(cam,st,t,1.0,extra=[(0,1.6,2.5,(1,.8,.3),.8)]); big=fin(bg); d=D(big)
    pl=place3(cam,st,0,5.0,1.0,2.4)
    if pl: glados(d,pl[0],pl[1]-0,pl[2]*4.0,t,glow=.7+.3*math.sin(t*3))
    for k in range(5): tt=(t*.45+k*.2)%1; note(d,80+k*90+math.sin(t+k)*10,860-tt*420,1.3,(255,200,60,int(220*(1-tt))))
    return grade(vign_(big,.5),sat=.9,seed=int(u*30),tint=(1.02,.98,.95))
def sceneB(u):
    st=CH; cam=dict(x=lerp(-1.0,.4,sm(u/8)),y=1.5,z=lerp(-2.0,-.8,sm(u/8)),yaw=lerp(.12,-.04,sm(u/8)),pitch=.05)
    bg=render_room(cam,st,u,1.0); back=new_ov(); portals(back,cam,st,u=u)
    box(back,cam,st,-.8,.8,0,.3,2.6,3.6,(150,152,158)); 
    big=fin(composite(bg,back)); d=D(big)
    t=clamp(u/4.0); P3(d,cam,st,lerp(-1.0,-1.4,sm(t)),lerp(3.5,7.0,sm(t)) if u<4 else lerp(7.0,3.5,sm((u-4)/4)),SUBJ,P_walk(u,3.2),hm=1.7,u=u,fog=(140,144,150),facing="back" if u<4 else "front") if False else P3(d,cam,st,(-1.0 if u<4 else 1.4),lerp(3.5,7.0,sm(u/4.0)) if u<4 else lerp(7.0,3.8,sm((u-4)/4.0)),SUBJ,P_walk(u,3.2),hm=1.7,u=u,fog=(140,144,150),facing="back" if u<4 else "front")
    d.R(150,860,420,940,(255,150,30),10); d.R(150,860,420,892,(40,40,48),10); ptext(d,166,866,"THE ORANGE BOX",3.0,(255,255,255)); ptext(d,166,904,"2007",5,(30,20,10))
    return grade(big,sat=.95,seed=int(u*30),tint=(.99,1.0,1.02))
def graf_tex(w=420,h=220):
    im=Image.new("RGB",(w,h),(34,36,40)); d=ImageDraw.Draw(im)
    for k in range(80): d.line([(rng_(k,0)*w,rng_(k,1)*h),(rng_(k,0)*w+10,rng_(k,1)*h+3)],fill=(60,62,66))
    d.text((w/2,70),"LA TARTA ES",font=font(46,True),fill=(255,70,60),anchor="mm"); d.text((w/2,140),"MENTIRA",font=font(56,True),fill=(255,70,60),anchor="mm"); return im
def rng_(k,j): return ((k*9301+49297+j*233)%233280)/233280.0
def sceneC(u):
    st=dict(DARK,fov=52); cam=dict(x=lerp(-.8,.4,sm(u/8)),y=1.5,z=lerp(-1.5,-.4,sm(u/8)),yaw=lerp(.1,-.05,sm(u/8)),pitch=.05)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.6,3.0,(1,.8,.4),1.0)]); back=new_ov()
    tquad(back,cam,st,(-1.6,3.0,7.99),(1.6,3.0,7.99),(1.6,1.3,7.99),(-1.6,1.3,7.99),graf_tex())
    box(back,cam,st,-1.4,-.2,0,.8,6.4,7.4,(110,112,118))
    big=fin(composite(bg,back)); d=D(big)
    pl=place3(cam,st,-.8,6.9,1.0,.8)
    if pl: cake(d,pl[0],pl[1],pl[2]*1.8,u)
    P3(d,cam,st,.9,5.5,SUBJ,dict(P_point(u,dirx=-1),ar=(1.45,1.6)),hm=1.7,u=u,fog=(10,10,12))
    return grade(vign_(big,.4),sat=.95,seed=int(u*30),tint=(1.02,.98,.96))
def sceneD(u):
    st=mk(H=2.8,hw=2.2,zend=5.0,zback=-2.5,wall="plaster",wcol=(60,62,70),floor="carpet",fcol=(40,40,46),ceil="tile",ccol=(70,72,80),ambient=.14,fov=52,fog=.02,fogcol=(6,6,8))
    cam=dict(x=lerp(-.8,.2,sm(u/8)),y=1.45,z=lerp(-1.2,0,sm(u/8)),yaw=lerp(.15,0,sm(u/8)),pitch=.04)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.8,2.5,(1,.85,.6),.9)]); back=new_ov()
    tquad(back,cam,st,(-1.8,2.3,4.99),(1.8,2.3,4.99),(1.8,.9,4.99),(-1.8,.9,4.99),Image.new("RGB",(300,100),(14,14,18)))
    box(back,cam,st,-1.4,1.4,0,.8,4.0,4.9,(40,42,48))
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,.0,2.6,ACTRESS,dict(P_talk(u),ar=(.5,.4),mouth=.5+.5*math.sin(u*9)),hm=1.7,u=u,fog=(10,10,14))
    pl=place3(cam,st,.7,2.6,1.0,.0)
    if pl: mic(d,pl[0],pl[1]-140*pl[2]*1.2,pl[2]*1.6)
    pl=place3(cam,st,0,5.0,1.0,2.5)
    if pl: glados(d,pl[0],pl[1],pl[2]*2.0,u)
    ptext(d,40,270,"ELLEN MCLAIN",4.2,(255,255,255))
    return grade(vign_(big,.5),sat=.9,seed=int(u*30),tint=(1.0,.98,1.02))
def credits_tex(u,w=300,h=420):
    im=Image.new("RGB",(w,h),(4,6,10)); d=ImageDraw.Draw(im); G=(120,230,150)
    d.text((w/2,60),"STILL ALIVE",font=font(34,True),fill=G,anchor="mm")
    for k in range(14):
        y=(h-((u*40+k*30)%h)); d.text((w/2,y),"- - - - - - - -" if k%3 else "J. COULTON",font=mono(16),fill=G,anchor="mm")
    return im
def sceneE(u):
    st=mk(H=2.8,hw=2.4,zend=5.0,zback=-2.5,wall="wood",wcol=(110,80,52),floor="wood",fcol=(90,64,44),ceil="plaster",ccol=(170,160,146),ambient=.2,amb_rgb=(1,.85,.7),fov=52,fog=.01,
          plights=dict(gap=100,off=1,xs=(0,),y=2.3,rgb=(1,.8,.5),I=.7,k=.4))
    cam=dict(x=lerp(-.6,.4,sm(u/7)),y=1.4,z=lerp(-1.4,-.4,sm(u/7)),yaw=lerp(.1,-.05,sm(u/7)),pitch=.04)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.4,4.0,(.4,1.0,.6),.9)]); back=new_ov()
    tquad(back,cam,st,(-1.2,2.4,4.99),(1.2,2.4,4.99),(1.2,.8,4.99),(-1.2,.8,4.99),crt(credits_tex(u),1.0,int(u*30))); glow(back,cam,st,(0,1.6,4.9),(120,230,150),1.4,50,5)
    big=fin(composite(bg,back)); d=D(big)
    def hl(dd,x,y,a,s,K=1.0): dd.R(x-8*K,y-6*K,x+8*K,y+14*K,(150,100,60,255),3*K)
    o=P3(d,cam,st,0,3.0,SINGER,dict(al=(1.15,2.5),ar=(.5+.2*math.sin(u*8),.6),ll=(.05,.05),lr=(.05,.05),bob=math.sin(u*2),tilt=.05,look=(0,0),mouth=.5+.5*math.sin(u*8),curlL=.7,curlR=.4,hands_front=True),hm=1.75,u=u,props={"l":hl},fog=(20,14,10))
    if o: d.E(o["hip"][0]+10,o["hip"][1]-20,40,46,(190,120,60)); d.E(o["hip"][0]+10,o["hip"][1]-20,12,12,(30,20,14))
    for k in range(4): tt=(u*.5+k*.25)%1; note(d,60+k*130,860-tt*400,1.4,(255,200,60,int(220*(1-tt))))
    ptext(d,40,270,"JONATHAN COULTON",3.2,(255,255,255))
    return grade(vign_(big,.4),sat=.95,seed=int(u*30),tint=(1.0,.98,1.0))
def lyrics_tex(u,w=360,h=480):
    im=Image.new("RGB",(w,h),(4,10,8)); d=ImageDraw.Draw(im); G=(110,230,150)
    for r in range(18):
        y=(h-((u*50+r*30)%(h+30))); wd=100+((r*61)%220); d.rectangle([20,y,20+wd,y+8],fill=G)
    return im
def sceneF(u):
    st=dict(CH,wcol=(40,44,50),wcol2=(30,34,38),ambient=.2); cam=dict(x=lerp(-.8,.5,sm(u/8)),y=1.5,z=lerp(-1.5,-.5,sm(u/8)),yaw=lerp(.1,-.05,sm(u/8)),pitch=.05)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.6,4.5,(.4,1.0,.6),.9)]); back=new_ov()
    tquad(back,cam,st,(-1.8,3.2,7.99),(1.8,3.2,7.99),(1.8,.6,7.99),(-1.8,.6,7.99),crt(lyrics_tex(u),1.0,int(u*30))); glow(back,cam,st,(0,1.8,7.9),(110,230,150),1.6,50,5)
    big=fin(composite(bg,back)); d=D(big)
    o=P3(d,cam,st,-.4,4.6,SUBJ,dict(P_both(u,l=(1.0,2.2),r=(1.0,2.2),grip=1.0),look=(0,0)),hm=1.7,u=u,fog=(10,10,12))
    if o:
        cx=(o["hand_l"][0]+o["hand_r"][0])/2; cy=(o["hand_l"][1]+o["hand_r"][1])/2; cube(d,cx,cy+22,1.0)
    ptext(d,40,270,"HUMOR NEGRO",5,(255,255,255))
    return grade(vign_(big,.4),sat=.95,seed=int(u*30),tint=(1.0,.98,1.0))
def sceneG(u):
    st=CH; cam=dict(x=lerp(-.6,.6,sm(u/6)),y=1.5,z=lerp(-1.4,-.6,sm(u/6)),yaw=lerp(.1,-.1,sm(u/6)),pitch=.05)
    bg=render_room(cam,st,u,1.0); back=new_ov(); portals(back,cam,st,u=u,xb=-1.8,xo=1.8)
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,0,4.0,SUBJ,P_cheer(u),hm=1.7,u=u,fog=(140,144,150))
    pl=place3(cam,st,1.0,4.6,1.0,0)
    if pl: cake(d,pl[0],pl[1],pl[2]*1.0,u,candle=False)
    return grade(big,sat=.95,seed=int(u*30),tint=(.99,1.0,1.02))
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur): return 1.0,270,480
core.CAM=cam
if __name__=="__main__": core.main()
