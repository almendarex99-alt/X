import sys; sys.path.insert(0,"..")
from kit import *
from rooms import mk, render_room
from sets import *
import nes
LIV=mk(H=2.45,hw=2.4,zend=2.9,zback=-3.2,wall="wood",wcol=(116,82,52),floor="carpet",fcol=(112,64,52),ceil="plaster",ccol=(196,188,170),ambient=.20,amb_rgb=(.95,.82,.68),fog=.006,fov=52)
OFF=mk(H=2.7,hw=2.4,zend=4.0,zback=-2.0,wall="plaster",wcol=(206,200,184),floor="tile",fcol=(136,136,130),ceil="tile",ccol=(214,212,202),ambient=.26,amb_rgb=(.92,.96,1),fog=.01,fov=52)
KID=dict(skin=(232,190,152),hair=(70,48,32),hairstyle="short",shirt=(206,64,56),shirt2=(240,230,210),pants=(60,70,110),sleeve="short")
KID2=dict(skin=(238,200,164),hair=(190,140,60),hairstyle="short",shirt=(60,130,90),pants=(60,60,80),sleeve="short")
KID3=dict(skin=(214,170,130),hair=(30,24,20),hairstyle="bun",shirt=(230,170,60),pants=(80,60,60),sleeve="short")
DEV=dict(skin=(232,192,156),hair=(40,30,24),hairstyle="short",glasses=True,shirt=(230,230,236),coat=(236,236,240),pants=(60,60,76),sleeve="long")
TVZ=2.40
def liv_extras(u,bright=1.0): return [(-1.8,1.15,1.6,(1.0,.72,.44),1.0),(0,1.0,TVZ-.3,(.45,.68,1.0),1.5*bright)]
def living(cam,u,from_front=False,mode=0.0):
    st=LIV; bg=render_room(cam,st,u,flick(u,.97),extra=liv_extras(u)); back=new_ov(); front=new_ov()
    sidewindow(back,cam,st,-2.39,.3,1.5,night=True); tquad(back,cam,st,(2.39,2.0,.4),(2.39,2.0,1.4),(2.39,1.0,1.4),(2.39,1.0,.4),tex_poster()) if False else None
    tquad(back,cam,st,(1.0,1.95,2.89),(1.8,1.95,2.89),(1.8,1.0,2.89),(1.0,1.0,2.89),tex_poster(col=(40,90,160)))
    tquad(back,cam,st,(-1.8,1.9,2.89),(-1.0,1.9,2.89),(-1.0,1.2,2.89),(-1.8,1.2,2.89),tex_poster(seed=7,col=(30,120,90)))
    tquad(back,cam,st,(-1.4,.006,-.8),(1.4,.006,-.8),(1.4,.006,1.9),(-1.4,.006,1.9),tex_rug())
    lamp(back,cam,st,-1.8,1.6); plant(back,cam,st,2.0,2.4); bookcase(back,cam,st,2.0,.6,w=.9,h=1.9,d=.1) if False else None
    box(back,cam,st,-.5,.5,0,.4,1.0,1.7,(110,76,50))
    for k in range(3): box(back,cam,st,-.4+k*.2,-.4+k*.2+.12,.4,.54,1.2,1.22,(120,120,126),shadow=False)
    tex=crt(nes.level(off=u*36,mode=mode,u=u),1.0,int(u*30))
    box(back,cam,st,-.9,.9,0,.5,TVZ-.05,TVZ+.5,(104,70,44)); box(back,cam,st,-.62,.62,.5,1.25,TVZ,TVZ+.48,(70,54,42))
    tquad(back,cam,st,(-.5,1.18,TVZ-.004),(.5,1.18,TVZ-.004),(.5,.58,TVZ-.004),(-.5,.58,TVZ-.004),tex)
    glow(back,cam,st,(0,.9,TVZ-.15),(120,170,255),1.1,60,6)
    return st,bg,back,front
def sofa(back,front,cam,st,x=0,z=-.2,from_front=False):
    box(back,cam,st,x-1.25,x+1.25,0,.42,z-.1,z+.9,(118,50,44));
    (back if from_front else front).__class__
    tgt=back if from_front else front
    box(tgt,cam,st,x-1.25,x+1.25,.42,.98,z-.2,z+.1,(128,56,48)); box(tgt,cam,st,x-1.32,x-1.12,.42,.74,z-.1,z+.9,(112,46,40)); box(tgt,cam,st,x+1.12,x+1.32,.42,.74,z-.1,z+.9,(112,46,40))
def finish(bg,back,front,persons=None,seed=0,sat=.95,tint=(1.0,.97,.93),extra=None):
    big=fin(composite(bg,back)); d=D(big)
    if persons: persons(d)
    if front is not None: big=composite(big,front.resize(OUTSZ,Image.BICUBIC))
    if extra: big=extra(big)
    return grade(big,sat=sat,seed=seed,tint=tint)
def sceneA(u,final=False):
    t=u+(0 if not final else 3); p=sm(clamp(t/6.0))
    cam=dict(x=lerp(-.5,-.15,p),y=lerp(1.45,1.12,p),z=lerp(-2.3,-1.25,p),yaw=.02*math.sin(t*.5),pitch=lerp(.06,.02,p))
    st,bg,back,front=living(cam,t); sofa(back,front,cam,st)
    def pp(d):
        P3(d,cam,st,-.45,.25,KID,dict(P_idle(t),tilt=.05*math.sin(t*.9),look=(0,.3)),hm=1.2,u=t,y0=-.08,bust=True,facing="back",fog=(40,30,26))
        P3(d,cam,st,.5,.25,KID2,dict(P_idle(t,1.3),tilt=-.04),hm=1.1,u=t,y0=-.08,bust=True,facing="back",fog=(40,30,26))
    return finish(bg,back,front,pp,seed=int(u*30))
def sceneB(u):
    st=dict(LIV,fov=50,ambient=.14); cam=dict(x=-.05+.05*math.sin(u*.6),y=.30,z=lerp(.05,.25,sm(u/6)),yaw=0.0,pitch=.2)
    bg=render_room(cam,st,u,1.0,extra=[(0,.5,1.8,(.45,.68,1.0),1.0),(-1.0,.8,.2,(1,.72,.44),.9)]); back=new_ov(); front=new_ov(); cz=.82
    box(back,cam,st,-.13,.13,0,.07,cz,cz+.2,(176,172,166)); box(back,cam,st,-.13,.13,.07,.095,cz,cz+.2,(150,146,140))
    poly3(back,cam,st,[(-.1,.074,cz-.002),(.1,.074,cz-.002),(.1,.088,cz-.002),(-.1,.088,cz-.002)],(40,38,40)); poly3(back,cam,st,[(-.1,.03,cz-.002),(.05,.03,cz-.002),(.05,.045,cz-.002),(-.1,.045,cz-.002)],(150,30,36))
    glow(back,cam,st,(.1,.04,cz-.03),(255,60,40),.05,120,3)
    p=sm((u-.5)/3.0); cy=lerp(.42,.1,p)
    box(front,cam,st,-.065,.065,cy,cy+.09,cz-.045,cz-.025,(122,122,128),shadow=False)
    tquad(front,cam,st,(-.05,cy+.08,cz-.0451),(.05,cy+.08,cz-.0451),(.05,cy+.03,cz-.0451),(-.05,cy+.03,cz-.0451),Image.new("RGB",(80,50),(220,190,70)))
    box(back,cam,st,.25,.37,0,.025,.3,.42,(190,186,180));
    big=fin(composite(bg,back)); d=D(big)
    hand3(d,cam,st,(0,cy+.11,cz-.03),hand_m=.11,a=3.14,s=1,curl=.7,spread=.4,arm_from=(300,1.2),arm_w=.035)
    big=composite(big,front.resize(OUTSZ,Image.BICUBIC)); return grade(big,seed=int(u*30),tint=(1.0,.97,.93))
def pcb_tex(u):
    im=Image.new("RGB",(640,480),(24,110,70)); d=ImageDraw.Draw(im)
    for k in range(70):
        x=20+(k*47)%600; y=30+(k*83)%420; d.line([(x,y),(x+80,y),(x+80,y+30+k%40)],fill=(92,184,120),width=3)
    for (x,y,w,h,lab) in((60,70,230,320,"PRG-ROM 32 KB"),(380,110,190,260,"CHR-ROM 8 KB")):
        d.rectangle([x,y,x+w,y+h],fill=(26,26,30)); d.rectangle([x+8,y+8,x+w-8,y+h-8],outline=(60,60,66),width=2)
        for q in range(14): d.rectangle([x-14,y+16+q*(h-40)/14,x,y+22+q*(h-40)/14],fill=(200,190,150)); d.rectangle([x+w,y+16+q*(h-40)/14,x+w+14,y+22+q*(h-40)/14],fill=(200,190,150))
        d.text((x+w/2,y+h/2),lab,font=mono(22,True),fill=(210,210,200),anchor="mm")
    for k in range(18): d.rectangle([20+k*16,446,28+k*16,476],fill=(214,180,70))
    return im
def sceneC(u):
    st=mk(floor="wood",fcol=(88,60,40),H=3.0,hw=3.0,zend=6,zback=-3,ambient=.16,amb_rgb=(1,.9,.8),fov=52,fog=.01,fogcol=(10,8,6))
    cam=dict(x=-.02+.015*math.sin(u*.5),y=.30,z=.10+.01*u,yaw=.0,pitch=1.15); bg=render_room(cam,st,u,1.0,extra=[(.0,.8,.5,(1,.8,.55),1.6)])
    back=new_ov(); P=.06
    tquad(back,cam,st,(-.065,.01,.34),(.065,.01,.34),(.065,.01,.25),(-.065,.01,.25),pcb_tex(u))
    big=fin(composite(bg,back)); d=D(big)
    ptext(d,40,230,"40 KB",9,(255,230,150),int(255*clamp(u/.8)))
    d.R(40,320,40+int(440*clamp(u/3.0)),350,(255,200,70,255),6); d.R(40,320,480,350,None,6,(255,255,255,200),2)
    return grade(big,seed=int(u*30),tint=(1.02,.97,.92))
def editor_tex(u):
    im=Image.new("RGB",(320,240),(24,28,60)); d=ImageDraw.Draw(im); d.rectangle([0,0,320,16],fill=(60,70,150)); d.text((6,2),"SPRITE EDITOR",font=mono(11,True),fill=(250,250,250))
    for r,row in enumerate(nes.SH):
        for c,ch in enumerate(row):
            x=40+c*14; y=40+r*14; d.rectangle([x,y,x+12,y+12],fill=(252,252,252) if ch=="#" else (40,46,90),outline=(70,80,130))
    for k,col in enumerate((nes.WHT,nes.CYN,nes.GRN,nes.GRN2)): d.rectangle([270,40+k*30,300,64+k*30],fill=col,outline=(250,250,250) if k==int(u*1.2)%4 else (60,60,60),width=2)
    d.text((40,170),"16 x 8 pixeles",font=mono(14),fill=(200,220,255)); return im
def office(cam,u):
    st=OFF; bg=render_room(cam,st,u,1.0,extra=[(0,1.3,2.0,(.55,.75,1.0),.8)]); back=new_ov(); front=new_ov()
    tquad(back,cam,st,(-2.39,2.0,.5),(-2.39,2.0,2.4),(-2.39,1.0,2.4),(-2.39,1.0,.5),tex_window(night=False,curtains=(200,200,190)))
    bookcase(back,cam,st,1.5,3.6,w=1.4,h=2.1,d=.3,seed=4)
    box(back,cam,st,-1.0,1.0,0,.74,2.3,3.1,(150,110,70)); box(back,cam,st,-.38,.38,.74,1.28,2.5,3.0,(206,200,184))
    tquad(back,cam,st,(-.3,1.23,2.495),(.3,1.23,2.495),(.3,.83,2.495),(-.3,.83,2.495),crt(editor_tex(u),1.0,int(u*30)))
    glow(back,cam,st,(0,1.0,2.4),(140,170,255),.9,50,5); box(back,cam,st,.5,.8,.74,.78,2.4,2.8,(226,220,204)); plant(back,cam,st,-1.6,3.4)
    return st,bg,back,front
def sceneD(u):
    cam=dict(x=lerp(-.6,-.1,sm(u/6)),y=1.3,z=lerp(.3,1.0,sm(u/6)),yaw=lerp(.12,.05,sm(u/6)),pitch=.05)
    st,bg,back,front=office(cam,u)
    def pp(d): P3(d,cam,st,.95,2.6,DEV,dict(P_talk(u),al=(1.3,2.1),ar=(.2,.3)),hm=1.75,u=u)
    return finish(bg,back,front,pp,seed=int(u*30),tint=(.98,1.0,1.04))
def sceneE(u):
    cam=dict(x=0,y=.95,z=lerp(.4,1.1,sm(u/7)),yaw=0.0,pitch=.02); st=dict(LIV,fov=44)
    seq=int(u*.6)%3; st_,bg,back,front=living(cam,u,mode=(0,1,2)[seq]);
    big=fin(composite(bg,back)); d=D(big); lab=("COLOR: BLANCO","COLOR: VERDE","COLOR: BLANCO")[seq]
    d.R(130,700,410,760,(0,0,0,170),12); ptext(d,150,718,lab,4.2,(255,255,255))
    return grade(big,seed=int(u*30),tint=(1.0,.97,.93))
def sceneF(u):
    cam=dict(x=lerp(-.8,-.3,sm(u/5)),y=1.4,z=lerp(.6,1.5,sm(u/5)),yaw=.12,pitch=.05)
    st,bg,back,front=office(cam,u)
    wb=Image.new("RGB",(440,220),(246,246,242)); dd=ImageDraw.Draw(wb)
    for k,(col,x) in enumerate(((nes.WHT,40),(nes.GRN,250))):
        dd.rectangle([x-8,40,x+148,130],fill=(92,148,252))
        for oy,row in enumerate(nes.SH):
            for ox,c in enumerate(row):
                if c=="#": dd.rectangle([x+ox*8,50+oy*8,x+ox*8+7,50+oy*8+7],fill=col)
    dd.text((200,60),"=",font=font(54,True),fill=(30,30,30)); dd.text((40,148),"NUBE",font=font(26,True),fill=(30,30,30)); dd.text((250,148),"ARBUSTO",font=font(26,True),fill=(30,30,30))
    tquad(back,cam,st,(-2.0,2.2,3.99),(0.0,2.2,3.99),(0.0,1.0,3.99),(-2.0,1.0,3.99),wb)
    def pp(d): P3(d,cam,st,-.1,3.2,DEV,dict(P_point(u,dirx=-1),ar=(1.4,1.6)),hm=1.75,u=u)
    return finish(bg,back,front,pp,seed=int(u*30),tint=(.98,1.0,1.04))
def sceneG(u):
    cam=dict(x=lerp(-.5,.5,sm(u/7)),y=1.2,z=1.75,yaw=3.14159+.12*math.sin(u*.4),pitch=.05)
    st=LIV; bg=render_room(cam,st,u,flick(u,.97),extra=liv_extras(u,.5)+[(0,1.0,1.3,(.45,.68,1.0),1.3)]); back=new_ov(); front=new_ov()
    tquad(back,cam,st,(-1.4,.006,-.8),(1.4,.006,-.8),(1.4,.006,1.9),(-1.4,.006,1.9),tex_rug()); lamp(back,cam,st,-1.8,.5)
    sofa(back,front,cam,st,from_front=True)
    def pp(d):
        for k,(x,stl) in enumerate(((-.8,KID),(0.0,KID2),(.8,KID3))):
            po=dict(P_cheer(u,k),al=(.5,1.4),ar=(2.4,2.8)) if k==1 else dict(P_idle(u,k),mouth=.6,look=(0,.2))
            P3(d,cam,st,x,.25,stl,po,hm=1.15,u=u,y0=-.08,bust=True,fog=(40,30,26),tone=1.0)
    return finish(bg,back,front,pp,seed=int(u*30),tint=(.96,.97,1.04))
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur): return 1.0,270,480
core.CAM=cam
if __name__=="__main__": core.main()
