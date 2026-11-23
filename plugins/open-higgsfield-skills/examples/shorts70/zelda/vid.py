import sys; sys.path.insert(0,"..")
from kit import *
from rooms import mk, render_room
from terrain import render_terrain, mk as tmk
from sets import *
GOLD=(255,214,70); GRN=(40,150,60)
LINK=dict(skin=(244,200,160),hair=(214,170,80),hairstyle="short",hat="greencap",shirt=(40,150,60),pants=(240,236,220),shoes=(130,84,50),belt=(130,80,40),sleeve="short",brow=(120,80,30),eyes=(60,90,160))
ZELDA=dict(skin=(244,206,170),hair=(232,190,84),hairstyle="long",hat="crown",dress=True,shirt=(240,150,200),skirt_col=(244,170,214),sleeve="long",shoes=(200,160,60),eyes=(60,90,160),brow=(150,110,40))
DESIGNER=dict(skin=(230,190,150),hair=(30,24,20),hairstyle="short",glasses=True,shirt=(210,210,216),sleeve="long",pants=(60,64,80))
FLAPPER=dict(skin=(244,206,176),hair=(50,34,28),hairstyle="bob",hat="headband",dress=True,shirt=(190,60,100),skirt_col=(200,80,116),sleeve="none",shoes=(60,40,40),brow=(40,26,20))
WRITER=dict(skin=(236,196,160),hair=(70,56,40),hairstyle="short",shirt=(40,50,70),coat=(30,34,50),pants=(40,44,60),sleeve="long",shoes=(30,28,32))
KID=dict(skin=(226,176,140),hair=(40,26,20),hairstyle="short",shirt=(200,70,60),pants=(60,70,110),sleeve="short")
FIELD=tmk(fov=54,ground="meadow",sky="day",fog=.012,fogcol=(206,224,246),hills=.06,hcol=(110,140,170),amb=(1.0,1.0,.96),ambient=1.0)
SUNSET=tmk(fov=54,ground="meadow",sky="sunset",fog=.012,fogcol=(240,190,140),hills=.06,hcol=(150,100,110),amb=(1.0,.82,.7),ambient=.9)
PARLOR=mk(H=3.0,hw=2.8,zend=4.4,zback=-3.0,wall="wood",wcol=(104,70,44),floor="wood",fcol=(86,60,40),ceil="plaster",ccol=(190,176,150),ambient=.20,amb_rgb=(1,.84,.66),fog=.01,fov=52,
            plights=dict(gap=100,off=1,xs=(0,),y=2.7,rgb=(1,.8,.5),I=.8,k=.35))
STUDIO=mk(H=2.8,hw=2.6,zend=4.4,zback=-2.6,wall="plaster",wcol=(210,204,188),floor="wood",fcol=(110,84,60),ceil="plaster",ccol=(220,216,206),ambient=.28,amb_rgb=(1,.96,.88),fog=.01,fov=52,
            plights=dict(gap=100,off=1,xs=(0,),y=2.4,rgb=(1,.92,.75),I=.5,k=.5))
def tri(d,x,y,s,col=GOLD,a=255): d.P([(x,y-s),(x-s*.9,y+s*.7),(x+s*.9,y+s*.7)],col+(a,))
def triforce(d,x,y,s,glow_=1.0):
    d.E(x,y,s*2.2,s*2.0,GOLD+(int(40*glow_),)); d.E(x,y,s*1.5,s*1.4,GOLD+(int(50*glow_),)); tri(d,x,y-s*.55,s*.5); tri(d,x-s*.5,y+s*.35,s*.5); tri(d,x+s*.5,y+s*.35,s*.5)
def sword_prop(dd,x,y,a,s,K=1.0): dd.R(x-3*K,y-82*K,x+3*K,y-8*K,(224,230,240),1); dd.R(x-13*K,y-10*K,x+13*K,y-4*K,(130,80,40),2); dd.R(x-3*K,y-4*K,x+3*K,y+16*K,(110,70,40),1)
def shield_prop(dd,x,y,a,s,K=1.0): dd.E(x-4*K,y,22*K,28*K,(30,70,170)); dd.E(x-4*K,y,16*K,22*K,(210,60,60)); dd.P([(x-4*K,y-14*K),(x-10*K,y+8*K),(x+2*K,y+8*K)],GOLD)
def vign_(img,k=.4): return Image.alpha_composite(img.convert("RGBA"),vignette_ov(img.size,k)).convert("RGB")
def field_scene(cam,st,u,ov=None):
    bg=render_terrain(cam,st,u); ov=ov or new_ov()
    for k,(x,z) in enumerate(((-6,10),(6,14),(-9,22),(8,26),(-4,34),(10,40))): tree(ov,cam,st,x,z,h=3+k%3*.6)
    return bg,ov
def sceneA(u,final=False):
    t=u+(0 if not final else 3); cam=dict(x=lerp(-1.2,0,sm(t/7)),y=1.5,z=lerp(-1,3,sm(t/7)),yaw=lerp(.1,0,sm(t/7)),pitch=.05)
    bg,ov=field_scene(cam,FIELD,t); big=fin(composite(bg,ov)); d=D(big)
    P3(d,cam,FIELD,-.8,cam["z"]+5.0,LINK,P_walk(t,2.2),hm=1.7,u=t,props={"r":sword_prop,"l":shield_prop},fog=(206,224,246)); P3(d,cam,FIELD,.9,cam["z"]+5.6,ZELDA,P_idle(t,1),hm=1.7,u=t,fog=(206,224,246))
    triforce(d,270,300+8*math.sin(t*2),64,.7+.3*math.sin(t*3)); ptext(d,236,520,"?",12,(255,255,255))
    return grade(vign_(big,.3),sat=1.05,seed=int(u*30),tint=(1.02,1.0,.96))
def sceneB(u):
    st=dict(PARLOR,fov=50,ambient=.14); cam=dict(x=-.05+.05*math.sin(u*.6),y=.32,z=lerp(.0,.2,sm(u/6)),yaw=0,pitch=.2)
    bg=render_room(cam,st,u,1.0,extra=[(0,.5,1.8,(1,.8,.5),.9)]); back=new_ov(); front=new_ov(); cz=.82
    box(back,cam,st,-.13,.13,0,.07,cz,cz+.2,(176,172,166)); box(back,cam,st,-.13,.13,.07,.095,cz,cz+.2,(150,146,140)); poly3(back,cam,st,[(-.1,.074,cz-.002),(.1,.074,cz-.002),(.1,.088,cz-.002),(-.1,.088,cz-.002)],(40,38,40))
    p=sm((u-.5)/3.0); cy=lerp(.42,.1,p)
    box(front,cam,st,-.065,.065,cy,cy+.09,cz-.045,cz-.025,(224,186,50),shadow=False)
    tquad(front,cam,st,(-.05,cy+.08,cz-.0451),(.05,cy+.08,cz-.0451),(.05,cy+.03,cz-.0451),(-.05,cy+.03,cz-.0451),Image.new("RGB",(80,50),(30,40,30)))
    big=fin(composite(bg,back)); d=D(big)
    hand3(d,cam,st,(0,cy+.11,cz-.03),hand_m=.11,a=3.14,s=1,curl=.7,spread=.4,arm_from=(300,1.2),arm_w=.035)
    big=composite(big,front.resize(OUTSZ,Image.BICUBIC)); ptext(D(big),40,270,"1986",9,(255,255,255))
    return grade(vign_(big,.4),sat=1.0,seed=int(u*30),tint=(1.03,.98,.93))
def sketch_tex(u,w=320,h=420):
    im=Image.new("RGB",(w,h),(244,240,226)); d=ImageDraw.Draw(im)
    d.polygon([(160,240),(100,400),(220,400)],fill=(240,150,200),outline=(60,40,40)); d.ellipse([130,150,190,220],fill=(244,206,170),outline=(60,40,40)); d.polygon([(130,160),(140,125),(160,150),(180,125),(190,160)],fill=GOLD,outline=(60,40,40))
    for i,n in enumerate(("NOMBRE 1","NOMBRE 2","NOMBRE 3")):
        d.text((14,14+i*26),n,font=mono(14),fill=(60,60,60))
        if i<2: d.line([(14,22+i*26),(110,22+i*26)],fill=(210,50,50),width=3)
    d.text((130,100),"?",font=font(50,True),fill=(210,50,50)); return im
def sceneC(u):
    st=STUDIO; cam=dict(x=lerp(-.8,.2,sm(u/8)),y=1.4,z=lerp(-.6,.6,sm(u/8)),yaw=lerp(.2,0,sm(u/8)),pitch=.05)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.2,2.2,(1,.92,.75),.8)]); back=new_ov()
    box(back,cam,st,-1.2,1.2,0,.74,2.2,3.0,(140,104,70)); tquad(back,cam,st,(-.5,.78,2.4),(.5,.78,2.4),(.5,1.5,2.9),(-.5,1.5,2.9),sketch_tex(u))
    sidewindow(back,cam,st,-2.59,.5,2.0,night=False,curt=(190,190,180)); bookcase(back,cam,st,1.9,3.9,w=1.4,h=2.1,d=.3,seed=3)
    big=fin(composite(bg,back)); d=D(big)
    def pencil(dd,x,y,a,s,K=1.0): dd.L(x,y-10*K,x+10*K,y+36*K,(240,200,60),6*K); dd.P([(x+10*K,y+36*K),(x+7*K,y+46*K),(x+13*K,y+46*K)],(40,30,20))
    P3(d,cam,st,.0,3.3,DESIGNER,dict(al=(.5,.3),ar=(1.15+.08*math.sin(u*5),1.55+.2*math.sin(u*5)),ll=(.05,.05),lr=(.05,.05),bob=math.sin(u*2),tilt=.08,look=(0,.6),mouth=0,curlR=.8,hands_front=True),hm=1.75,u=u,props={"r":pencil},fog=(30,24,18))
    ptext(D(big),40,270,"NOMBRE",8,(255,255,255))
    return grade(vign_(big,.3),sat=1.0,seed=int(u*30),tint=(1.03,.99,.94))
def sceneD(u):
    st=PARLOR; cam=dict(x=lerp(-.8,.4,sm(u/8)),y=1.5,z=lerp(-1.4,-.4,sm(u/8)),yaw=lerp(.15,-.05,sm(u/8)),pitch=.05)
    bg=render_room(cam,st,u,1.0,extra=[(-1.8,1.2,2.4,(1,.8,.5),.9)]); back=new_ov()
    bookcase(back,cam,st,-1.8,4.0,w=1.5,h=2.4,d=.35,seed=5); lamp(back,cam,st,1.8,3.4,h=1.3)
    ctex=Image.new("RGB",(200,260),(70,50,100)); cd=ImageDraw.Draw(ctex); cd.rectangle([14,14,186,246],outline=(240,210,120),width=4); cd.text((100,110),"F. SCOTT",font=serif(26),fill=(240,210,120),anchor="mm"); cd.text((100,150),"FITZGERALD",font=serif(22),fill=(240,210,120),anchor="mm")
    tquad(back,cam,st,(.2,2.2,4.39),(1.2,2.2,4.39),(1.2,.9,4.39),(.2,.9,4.39),ctex)
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,-.6,3.0,WRITER,P_idle(u),hm=1.78,u=u,fog=(30,22,16)); P3(d,cam,st,.6,2.8,FLAPPER,dict(P_wave(u,1),mouth=.4),hm=1.68,u=u,fog=(30,22,16))
    ptext(D(big),40,840,"ZELDA FITZGERALD",3.2,(255,255,255))
    return grade(vign_(big,.4),sat=1.0,seed=int(u*30),tint=(1.03,.98,.93))
def sceneE(u):
    cam=dict(x=0,y=1.6,z=lerp(-1,1.2,sm(u/6)),yaw=0,pitch=.04)
    bg,ov=field_scene(cam,SUNSET,u); big=fin(composite(bg,ov)); d=D(big)
    for i,ch in enumerate("ZELDA"): ptext(d,50+i*92,300+math.sin(u*3+i)*8,ch,18,GOLD)
    for k in range(26): a=k*.5+u; d.E(270+math.cos(a)*(190+k*3),420+math.sin(a)*(160+k*4),3,3,(255,240,150,int(200*abs(math.sin(u*2+k)))))
    P3(d,cam,SUNSET,0,cam["z"]+4.0,ZELDA,P_wave(u),hm=1.7,u=u,fog=(240,190,140))
    ptext(d,60,150,"",3,(255,255,255))
    return grade(vign_(big,.3),sat=1.05,seed=int(u*30),tint=(1.05,.98,.92))
def sceneF(u):
    cam=dict(x=lerp(-.6,.6,sm(u/6)),y=1.5,z=lerp(0,1.5,sm(u/6)),yaw=lerp(.1,-.1,sm(u/6)),pitch=.05)
    bg,ov=field_scene(cam,FIELD,u); big=fin(composite(bg,ov)); d=D(big); sw=math.sin(u*3)
    P3(d,cam,FIELD,-.9,cam["z"]+3.6,LINK,dict(P_hold(u),ar=(1.2+.6*sw,2.3+.8*sw),curlR=1.0),hm=1.7,u=u,props={"r":sword_prop,"l":shield_prop},fog=(206,224,246))
    P3(d,cam,FIELD,1.0,cam["z"]+3.4,ZELDA,P_wave(u),hm=1.7,u=u,fog=(206,224,246))
    d.R(40,320,260,370,(0,0,0,150),8); ptext(d,54,333,"ESTE ES LINK",3.4,(255,255,255)); d.R(290,320,510,370,(0,0,0,150),8); ptext(d,302,333,"ELLA ES ZELDA",3.0,(255,214,70))
    return grade(vign_(big,.3),sat=1.05,seed=int(u*30),tint=(1.02,1.0,.96))
def sceneG(u):
    cam=dict(x=0,y=1.5,z=lerp(0,1.2,sm(u/6)),yaw=0,pitch=.05)
    bg,ov=field_scene(cam,FIELD,u); big=fin(composite(bg,ov)); d=D(big)
    triforce(d,270,260,52,1.0)
    P3(d,cam,FIELD,0,cam["z"]+3.4,LINK,P_walk(u,3.0),hm=1.7,u=u,props={"r":sword_prop,"l":shield_prop},fog=(206,224,246))
    for k,(x,z,st) in enumerate(((-2.2,4.4,KID),(-1.1,5.0,DESIGNER),(1.2,5.0,WRITER),(2.3,4.4,FLAPPER))):
        P3(d,cam,FIELD,x,cam["z"]+z,st,dict(P_point(u+k,dirx=1 if x<0 else -1),ar=(1.45,1.5)) if x<0 else dict(P_point(u+k,dirx=-1),ar=(.12,.2),al=(1.45,1.5)),hm=1.7,u=u,fog=(206,224,246))
    return grade(vign_(big,.3),sat=1.05,seed=int(u*30),tint=(1.02,1.0,.96))
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur): return 1.0,270,480
core.CAM=cam
if __name__=="__main__": core.main()
