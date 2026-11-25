import sys; sys.path.insert(0,"..")
from kit import *
from rooms import mk, render_room
from terrain import render_terrain, mk as tmk
from sets import *
from art import door_swing
from common import ps1f
import nes
_FT={}
def ptext(d,x,y,txt,cell,col=(255,255,255),a=255):
    sz=int(cell*5.4*core.S); f=_FT.get(sz) or _FT.setdefault(sz,ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",sz))
    d.d.text((x*core.S,y*core.S),txt.upper(),font=f,fill=col+(a,),stroke_width=max(3,int(cell*.55*core.S/3*1.6)),stroke_fill=(0,0,0,min(255,a)))
# ---------- decorados ----------
GOTH=mk(H=4.2,hw=3.2,zend=8.0,zback=-3.0,wall="wood",wcol=(86,56,36),floor="wood",fcol=(76,52,36),ceil="beams",ccol=(56,40,30),ambient=.10,amb_rgb=(.8,.85,1),fog=.03,fogcol=(4,4,8),fov=54,
         plights=dict(gap=5,off=1,xs=(-2.8,2.8),y=2.4,rgb=(1,.7,.4),I=.8,k=.4))
BEDRM=mk(H=2.7,hw=2.4,zend=4.4,zback=-2.6,wall="plaster",wcol=(176,150,124),floor="carpet",fcol=(110,84,66),ceil="tile",ccol=(150,142,132),ambient=.11,amb_rgb=(.85,.88,1),fov=52,fog=.012,
          plights=dict(gap=2.4,off=0,xs=(0,),y=2.55,rgb=(1,.82,.6),I=.28,k=.5))
NIGHTT=tmk(fov=54,ground="grass",sky="night",fog=.018,fogcol=(14,18,32),hills=.05,hcol=(10,14,26),amb=(.26,.32,.5),ambient=1.0)
# ---------- reparto: cinco personajes distintos ----------
HERO=dict(skin=(230,190,156),hair=(60,44,32),hairstyle="short",shirt=(180,160,120),coat=(110,84,56),pants=(60,52,48),shoes=(40,30,26),sleeve="long",belt=(70,50,40),brow=(40,28,20))
HEROINE=dict(skin=(240,200,166),hair=(120,70,40),hairstyle="long",shirt=(60,80,120),dress=True,skirt_col=(70,92,134),sleeve="long",shoes=(40,30,30))
DEVA=dict(skin=(232,192,156),hair=(40,30,24),hairstyle="short",glasses=True,shirt=(70,100,150),pants=(60,60,76),sleeve="long",beard=True)
PONY=dict(skin=(236,196,160),hair=(50,36,30),hairstyle="ponytail",shirt=(70,130,90),pants=(60,60,80),shoes=(40,30,30),sleeve="long")
OLD=dict(skin=(226,184,150),hair=(150,150,150),hairstyle="short",shirt=(130,60,60),coat=(80,80,90),pants=(60,56,52),shoes=(36,30,28),sleeve="long")
CAST=[HERO,HEROINE,DEVA,PONY,OLD]
def torch(dd,x,y,a,s,K=1.0): dd.R(x-6*K,y-12*K,x+6*K,y+26*K,(60,60,70),4*K); dd.E(x,y+30*K,10*K,7*K,(255,240,180))
def tree(ov,cam,st,x,z,h=5,col=(16,40,26),trunk=(30,24,20)):
    box(ov,cam,st,x-.15,x+.15,0,h*.3,z-.15,z+.15,trunk,shadow=False)
    for k in range(3):
        y0=h*.2+k*h*.22; w=h*.32*(1-k*.22); poly3(ov,cam,st,[(x-w,y0,z),(x+w,y0,z),(x,y0+h*.42,z)],shd(col,1+k*.12))
def vign_(img,k=.5): return Image.alpha_composite(img.convert("RGBA"),vignette_ov(img.size,k)).convert("RGB")
def mansion(ov,cam,st,x,z,t):
    box(ov,cam,st,x-10,x+10,0,9,z,z+8,(40,34,44)); poly3(ov,cam,st,[(x-11,9,z-.6),(x+11,9,z-.6),(x,15,z+4)],(26,22,30))
    box(ov,cam,st,x-3,x+3,0,13,z-1,z+3,(36,30,40)); poly3(ov,cam,st,[(x-3.6,13,z-1.6),(x+3.6,13,z-1.6),(x,18,z+1)],(22,18,26))
    for r in range(2):
        for c in range(6):
            on=((r*3+c*2+int(t*.8))%5)>1; poly3(ov,cam,st,[(x-9+c*3.2,2+r*3.6,z-.02),(x-8+c*3.2,2+r*3.6,z-.02),(x-8+c*3.2,4.4+r*3.6,z-.02),(x-9+c*3.2,4.4+r*3.6,z-.02)],(255,190,100) if on else (16,18,30))
    poly3(ov,cam,st,[(x-1,0,z-1.02),(x+1,0,z-1.02),(x+1,3,z-1.02),(x-1,3,z-1.02)],(70,40,30))
def hall(cam,u,extra=()):
    st=GOTH; bg=render_room(cam,st,u,flick(u,.97),extra=list(extra)); back=new_ov()
    box(back,cam,st,2.2,3.0,0,2.2,5.5,6.2,(80,50,32)); tquad(back,cam,st,(-2.9,2.8,7.99),(-1.2,2.8,7.99),(-1.2,.3,7.99),(-2.9,.3,7.99),tex_window(night=True,curtains=(100,40,40)))
    for x in (-2.8,2.8): box(back,cam,st,x-.1,x+.1,0,.5,3,3.2,(60,50,44),shadow=False); glow(back,cam,st,(x,2.4,3.1),(255,170,90),1.2,70,5)
    return st,bg,back
TINT=(1.03,.98,.94)
# ---------- 0 y 7: mansion de noche ----------
def sceneA(u,final=False):
    t=u+(0 if not final else 3); cam=dict(x=lerp(-3,1,sm(t/9)),y=1.6,z=lerp(0,3,sm(t/9)),yaw=lerp(.2,-.03,sm(t/9)),pitch=.08)
    bg=render_terrain(cam,NIGHTT,t); ov=new_ov(); mansion(ov,cam,NIGHTT,0,24,t)
    for k,(x,z) in enumerate(((-6,12),(6,14),(-9,18),(9,20))): tree(ov,cam,NIGHTT,x,z,h=5,col=(16,40,26),trunk=(30,24,20))
    big=fin(composite(bg,ov)); d=D(big)
    if (t%4.0)<.12: d.R(0,0,540,960,(255,255,255,int(150*(1-(t%4.0)/.12))),0)
    P3(d,cam,NIGHTT,-1.0+u*.1,cam["z"]+5,HERO,P_walk(t,2.4),hm=1.75,u=t,facing="back",props={"r":torch},fog=(14,18,32))
    big=snow_particles(big,t,n=40,col=(170,180,200),sz=2,speed=30,alpha=60,scale=2.2); d=D(big)
    if not final:
        ptext(d,40,270,"REMAKE?",8,(255,255,255))
        if u>2.0: ptext(d,40,350,"SOLO EN JAPÓN",4,(255,214,120))
    else:
        ptext(d,40,270,"COMENTA",8,(255,255,255))
        if int(u*1.6)%2==0: ptext(d,40,350,"SUSCRÍBETE",5,(255,214,120))
    return grade(vign_(big,.5),sat=.9,seed=int(u*30),tint=(.95,.98,1.06))
# ---------- 1: Famicom + TV ----------
def nes_title(u):
    im=Image.new("RGB",(256,240),(8,6,14)); d=ImageDraw.Draw(im)
    d.ellipse([196,40,226,70],fill=(236,230,200)); d.polygon([(26,128),(128,84),(230,128)],fill=(34,26,50)); d.rectangle([40,128,216,206],fill=(24,18,36))
    d.rectangle([108,70,148,128],fill=(28,22,42)); d.polygon([(104,70),(128,46),(152,70)],fill=(38,30,56))
    for k,(wx,wy) in enumerate([(54,142),(84,142),(160,142),(190,142),(54,172),(190,172),(84,172),(160,172)]):
        on=((int(u*1.5)+k)%3)!=0; d.rectangle([wx,wy,wx+14,wy+18],fill=(252,200,90) if on else (20,16,30))
    d.rectangle([116,172,140,206],fill=(80,40,26)); d.rectangle([0,206,255,240],fill=(14,40,22))
    nes.text(d,68,8,"SWEET HOME",(232,48,48),3); nes.text(d,92,26,"CAPCOM 1989",(250,250,250),1)
    if int(u*2)%2==0: nes.text(d,80,222,"PUSH START",(250,250,250),1)
    return im
def sceneB(u):
    st=BEDRM; k=sm(u/7); cam=dict(x=lerp(-.9,.1,k),y=1.35,z=lerp(-.9,.9,k),yaw=lerp(.18,0,k),pitch=.05)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.4,2.9,(.6,.7,1),.9)]); back=new_ov()
    tquad(back,cam,st,(-1.95,2.3,4.38),(-1.15,2.3,4.38),(-1.15,.9,4.38),(-1.95,.9,4.38),tex_poster(col=(120,40,60))); tquad(back,cam,st,(.95,2.4,4.38),(1.95,2.4,4.38),(1.95,.8,4.38),(.95,.8,4.38),tex_window(night=True,curtains=(90,40,50))); glow(back,cam,st,(1.45,1.6,4.2),(120,140,255),1.0,30,5)
    box(back,cam,st,-1.4,1.4,0,.74,2.3,3.3,(120,84,58))
    box(back,cam,st,-.62,.62,.74,1.8,2.6,3.2,(52,46,44)); tquad(back,cam,st,(-.44,1.7,2.595),(.44,1.7,2.595),(.44,.88,2.595),(-.44,.88,2.595),crt(nes_title(u),1.05,int(u*30))); glow(back,cam,st,(0,1.3,2.4),(150,170,255),1.0,55,5)
    box(back,cam,st,.4,1.15,.74,.86,2.3,2.62,(238,236,226)); box(back,cam,st,.4,1.15,.86,.9,2.3,2.62,(200,40,40)); box(back,cam,st,.55,1.0,.9,.94,2.34,2.5,(86,52,34)); box(back,cam,st,.6,.9,.9,1.0,2.4,2.46,(60,60,64))
    box(back,cam,st,-1.0,-.5,.74,.78,2.35,2.55,(200,200,206)); box(back,cam,st,-.95,-.9,.78,.8,2.4,2.45,(40,40,44)); box(back,cam,st,-.8,-.75,.78,.8,2.4,2.45,(200,40,40))
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,-1.7,3.6,HERO,P_idle(u),hm=1.75,u=u,fog=(20,20,26),facing="back") if False else None
    ptext(d,40,270,"CAPCOM",8,(255,255,255)); ptext(d,40,350,"FAMICOM",5,(255,214,120))
    return grade(vign_(big,.35),sat=.95,seed=int(u*30),tint=(.98,1.0,1.05))
# ---------- 2: cinco personajes entran a la mansion ----------
def sceneC(u):
    cam=dict(x=lerp(-1.2,0,sm(u/7)),y=1.55,z=lerp(-2.8,-1.4,sm(u/7)),yaw=lerp(.12,0,sm(u/7)),pitch=.06)
    st,bg,back=hall(cam,u,[(0,1.2,1.5,(1,.8,.5),1.0)]); big=fin(composite(bg,back)); d=D(big)
    for k,(x,z) in enumerate(((-1.6,3.5),(-.8,3.0),(0,3.4),(.8,3.0),(1.6,3.5))):
        P3(d,cam,st,x,z,CAST[k],dict(P_walk(u,2.6,k*.9),ar=(1.3,2.0)) if k==0 else P_walk(u,2.6,k*.9),hm=1.75,u=u,fog=(6,4,6),props={"r":torch} if k==0 else None)
    ptext(d,40,270,"5 PERSONAJES",6,(255,255,255)); ptext(d,40,350,"UNA MANSIÓN",5,(255,214,120))
    return grade(vign_(big,.5),sat=.9,seed=int(u*30),tint=TINT)
# ---------- 3: un objeto cada uno ----------
def sceneD(u):
    k=sm(u/6); cam=dict(x=lerp(-1.0,.5,k),y=1.55,z=-1.2,yaw=lerp(.2,-.05,k),pitch=.16)
    st,bg,back=hall(cam,u,[(0,1.2,1.5,(1,.8,.5),1.0)])
    box(back,cam,st,-1.5,1.5,.7,.8,1.2,2.2,(96,64,42))
    for x in (-1.4,1.4):
        for zz in (1.3,2.0): box(back,cam,st,x-.06,x+.06,0,.7,zz,zz+.1,(70,48,34))
    for i,(x,c) in enumerate([(-1.1,(212,212,220)),(-.55,(240,240,240)),(0,(46,46,58)),(.55,(236,196,64)),(1.1,(120,170,110))]):
        if u>.5+i*.75:
            box(back,cam,st,x-.14,x+.14,.8,.98,1.55,1.85,c,emis=.25); glow(back,cam,st,(x,1.05,1.7),c,.55,55,5)
            if i==1: box(back,cam,st,x-.02,x+.02,.98,.995,1.6,1.8,(220,30,30),shadow=False); box(back,cam,st,x-.09,x+.09,.98,.995,1.68,1.72,(220,30,30),shadow=False)
            if i==2: box(back,cam,st,x-.05,x+.05,.84,.92,1.5,1.56,(10,10,12),shadow=False)
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,-.5,3.2,HERO,dict(P_talk(u),al=(1.2,1.6)),hm=1.75,u=u,fog=(6,4,6)); P3(d,cam,st,.6,3.4,HEROINE,P_idle(u,1.0),hm=1.68,u=u,fog=(6,4,6))
    ptext(d,40,270,"5 OBJETOS",7,(255,255,255))
    if u>4.0: ptext(d,40,350,"COMBÍNALOS",5,(255,214,120))
    return grade(vign_(big,.5),sat=.9,seed=int(u*30),tint=TINT)
# ---------- 4: muerte permanente ----------
def sceneE(u):
    cam=dict(x=0,y=1.5,z=lerp(-2.8,-1.8,sm(u/7)),yaw=0,pitch=.06)
    st,bg,back=hall(cam,u,[(0,1.2,1.5,(1,.8,.5),1.0)]); big=fin(composite(bg,back)); d=D(big)
    deaths={1:1.5,3:3.2}
    for k,x in enumerate((-1.6,-.8,0,.8,1.6)):
        td=deaths.get(k); a=255 if td is None else int(255*clamp(1-(u-td)/.8))
        if a>0: P3(d,cam,st,x,3.2,CAST[k],P_scared(u,k) if (td is not None and u>td-.6) else P_idle(u,k),hm=1.75,u=u,fog=(6,4,6),alpha=a)
        if td is not None and u>td+.3:
            pl=place3(cam,st,x,3.2,1.75)
            if pl:
                lx,ly,sc,_=pl; al=int(255*clamp((u-td-.3)/.6)); d.R(lx-3*sc,ly-62*sc,lx+3*sc,ly-6*sc,(235,235,235,al),1); d.R(lx-15*sc,ly-48*sc,lx+15*sc,ly-42*sc,(235,235,235,al),1)
    ptext(d,40,270,"PARA SIEMPRE",6,(255,255,255))
    if u>4.2: ptext(d,40,350,"OTRO FINAL",5,(255,214,120))
    return grade(vign_(big,.55),sat=.85,seed=int(u*30),tint=TINT)
# ---------- 5: la puerta (1989 -> 1996) ----------
def sceneF(u):
    first=u<3.4; q=(u if first else u-3.4)
    im=new((12,9,16),(36,26,24)) if first else new((6,12,12),(18,32,28)); d=D(im)
    d.R(0,640,540,960,(44,30,26) if first else (26,36,32)); d.R(0,636,540,646,(0,0,0,110))
    for k in range(-1,3): d.R(k*210+14,190,k*210+176,610,(255,255,255,12),4)
    op=sm(q/2.0)
    door_swing(d,270,640,220,360,op,col=(116,74,46) if first else (62,92,70),light=(255,222,150) if first else (176,236,196))
    if op>.4: d.P([(160,640),(380,640),(470,960),(70,960)],(255,222,150,int(70*op)) if first else (176,236,196,int(70*op)))
    walk=sm(clamp((q-1.2)/1.6)); a=int(255*(1-clamp((q-2.2)/.6))) if q>2.2 else 255
    if q>.6 and a>0: person(d,270,lerp(790,650,walk),lerp(.95,.55,walk),u,P_walk(u,3.0),HERO,facing="back",alpha=a)
    img=ps1f(im,block=14 if first else 6); d2=D(img)
    ptext(d2,40,270,"1989" if first else "1996",9,(255,255,255)); ptext(d2,40,360,"SWEET HOME" if first else "RESIDENT EVIL",4,(255,214,120))
    return grade(vign_(img,.4),sat=.95,seed=int(u*30),tint=(1,1,1))
# ---------- 6: Capcom 1996, PlayStation ----------
def ps1_tex(u):
    im=Image.new("RGB",(330,240),(8,8,14)); d=ImageDraw.Draw(im)
    for k in range(40): d.point((int(rnd(k)*330),int(rnd(k,1)*100)),fill=(220,220,255))
    d.ellipse([250,24,284,58],fill=(230,226,200)); d.polygon([(20,150),(165,96),(310,150)],fill=(30,24,44)); d.rectangle([40,150,290,214],fill=(22,18,32)); d.rectangle([140,84,190,150],fill=(26,20,38)); d.polygon([(134,84),(165,56),(196,84)],fill=(36,28,54))
    for k,(wx,wy) in enumerate([(62,162),(100,162),(222,162),(260,162),(62,190),(260,190)]):
        on=((int(u*1.4)+k)%3)!=0; d.rectangle([wx,wy,wx+16,wy+18],fill=(250,196,90) if on else (18,14,26))
    d.rectangle([152,176,178,214],fill=(76,40,26)); d.rectangle([0,214,330,240],fill=(12,32,20))
    d.text((38,8),"RESIDENT EVIL",font=mono(26,True),fill=(200,24,24))
    if int(u*2)%2==0: d.text((100,222),"PRESS START",font=mono(12,True),fill=(240,240,240))
    return ps1f(im,3)
def sceneG(u):
    st=BEDRM; k=sm(u/8); cam=dict(x=lerp(-.7,.2,k),y=1.4,z=lerp(-.8,.7,k),yaw=lerp(.15,0,k),pitch=.05)
    bg=render_room(cam,st,u,1.0,extra=[(0,1.4,2.9,(.6,.7,1),.9)]); back=new_ov()
    tquad(back,cam,st,(-1.95,2.3,4.38),(-1.15,2.3,4.38),(-1.15,.9,4.38),(-1.95,.9,4.38),tex_poster(col=(120,40,60))); tquad(back,cam,st,(.95,2.4,4.38),(1.95,2.4,4.38),(1.95,.8,4.38),(.95,.8,4.38),tex_window(night=True,curtains=(90,40,50))); glow(back,cam,st,(1.45,1.6,4.2),(120,140,255),1.0,30,5)
    box(back,cam,st,-1.4,1.4,0,.74,2.3,3.3,(120,84,58))
    box(back,cam,st,-.62,.62,.74,1.8,2.6,3.2,(52,46,44)); tquad(back,cam,st,(-.5,1.72,2.595),(.5,1.72,2.595),(.5,.86,2.595),(-.5,.86,2.595),crt(ps1_tex(u),1.05,int(u*30))); glow(back,cam,st,(0,1.3,2.4),(170,190,255),1.0,55,5)
    box(back,cam,st,.35,1.1,.74,.84,2.2,2.6,(176,176,182)); box(back,cam,st,.4,1.0,.84,.88,2.25,2.55,(206,206,212)); box(back,cam,st,.5,.8,.88,.92,2.3,2.5,(150,150,158))
    big=fin(composite(bg,back)); d=D(big)
    P3(d,cam,st,-1.45,3.9,DEVA,P_talk(u),hm=1.75,u=u,fog=(20,20,26))
    ptext(d,40,270,"EL CREADOR",8,(255,255,255)); ptext(d,40,350,"CAPCOM 1996",5,(255,214,120))
    return grade(vign_(big,.35),sat=.95,seed=int(u*30),tint=(.98,1.0,1.05))
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur): return 1.0+.07*sm(clamp(u/max(.01,dur))),270,480
core.CAM=cam
if __name__=="__main__": core.main()
