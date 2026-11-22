import sys,io; sys.path.insert(0,"..")
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import core
from core import clamp, sm
from liminal import *
OUTSZ=(1620,2880)
def fin(img): return img.resize(OUTSZ,Image.BICUBIC)
def cam_at(t,speed=1.1,sway=1.0,z0=0.0,yaw0=0.0,pitch=.14,y0=1.62):
    c=walk_cam(t,speed,z0=z0,yaw0=yaw0,sway=sway,y0=y0); c["pitch"]=pitch+c["pitch"]; return c
def flick(u): return 1.0 if (math.sin(u*37)*math.sin(u*11.3+1.7))<.93 else .55
def tear(img,amount,seed):
    a=np.array(img); rng=np.random.default_rng(seed); h=a.shape[0]
    for _ in range(int(16*amount)):
        y=int(rng.integers(0,h-80)); hh=int(rng.integers(12,140)); a[y:y+hh]=np.roll(a[y:y+hh],int(rng.integers(-160,160)),axis=1)
    a[:,:,0]=np.roll(a[:,:,0],int(10*amount),axis=1); a[:,:,2]=np.roll(a[:,:,2],-int(10*amount),axis=1)
    return Image.fromarray(a)
def grade(img,warm=1.0,sat=.92,grain=4.0,seed=0):
    a=np.asarray(img).astype(np.float32); g=a.mean(2,keepdims=True); a=g+(a-g)*sat
    a[:,:,0]*=1+.03*warm; a[:,:,2]*=1-.05*warm
    a=a+np.random.default_rng(seed).normal(0,grain,a.shape[:2])[:,:,None]
    return Image.fromarray(np.clip(a,0,255).astype(np.uint8))
# ---------------- escena 0 / 7: caminando por el pasillo ----------------
def sceneA(u,final=False):
    t=u+(0 if not final else 5)
    cam=cam_at(t,speed=1.15,sway=1.0)
    im=render(cam,YELLOW,t,flick(u))
    if not final and u>1.2:
        d=22-min(u-1.2,6)*.9; im=entity(im,cam,YELLOW,.15,cam["z"]+d,h=2.35,t=u,walk=u*1.2,arms=1.0,a=int(235*clamp((u-1.2)/1.0)))
    return fin(grade(im,seed=int(u*30)))
# ---------------- escena 1: la foto en el foro (movil) ----------------
_PHOTO=None
def photo():
    global _PHOTO
    if _PHOTO is None:
        st=dict(WIDE,hw=9.0,fov=76,gain=.7)
        c=dict(x=-2.0,y=1.55,z=0.0,yaw=.45,pitch=.16)
        im=render(c,st,0.0).crop((0,360,RW,360+int(RW*.75))).resize((400,300),Image.BILINEAR)
        a=np.asarray(im).astype(np.float32); yy,xx=np.mgrid[0:300,0:400]; fl=1+.25*np.exp(-(((xx-200)/260)**2+((yy-150)/200)**2)); a*=fl[:,:,None]
        im=Image.fromarray(np.clip(a,0,255).astype(np.uint8)); b=io.BytesIO(); im.save(b,"JPEG",quality=22); b.seek(0); _PHOTO=Image.open(b).convert("RGB")
    return _PHOTO
def sceneB(u):
    img=Image.new("RGB",(RW,RH),(8,8,10)); d=ImageDraw.Draw(img)
    # resplandor de la pantalla sobre la mesa
    for k in range(6): d.ellipse([-200-k*30,500-k*30,RW+200+k*30,1500+k*30],fill=(14+k*3,14+k*3,18+k*3))
    sw,sh=560,1060; sx0,sy0=80,110; zoom=1.0+.18*sm((u-3.0)/3.0)
    page=Image.new("RGB",(sw,sh+500),(236,236,232)); p=ImageDraw.Draw(page)
    p.rectangle([0,0,sw,70],fill=(36,40,52)); p.text((22,18),"foro anonimo  /paranormal/",font=font(26,True),fill=(230,230,240))
    p.rectangle([0,70,sw,100],fill=(214,218,228)); p.text((22,74),"Hilo: lugares liminales",font=font(20),fill=(60,60,80))
    p.text((22,118),"Anonimo   14/05/2019   Nº 1",font=font(20,True),fill=(20,110,40))
    p.text((22,150),"Si te sales de la realidad por el",font=font(24),fill=(30,30,40)); p.text((22,182),"sitio equivocado, acabas aqui.",font=font(24),fill=(30,30,40))
    page.paste(photo().resize((516,387)),(22,226)); p.rectangle([22,226,538,613],outline=(120,120,130),width=2)
    p.text((22,626),"imagen.jpg (74 KB, 1024x768)",font=font(17),fill=(90,90,100))
    for k in range(8):
        y=670+k*92; p.rectangle([0,y,sw,y+82],fill=(224,228,238) if k%2==0 else (232,235,242)); p.text((22,y+8),"Anonimo   Nº %d"%(2+k),font=font(17,True),fill=(20,110,40))
        p.rectangle([22,y+36,22+int(260+80*math.sin(k*2.3)),y+46],fill=(120,124,136)); p.rectangle([22,y+56,22+int(180+60*math.cos(k*1.7)),y+66],fill=(150,154,164))
    scroll=int(110*sm(u/5.5))
    view=page.crop((0,scroll,sw,scroll+sh))
    if zoom>1.001:
        cw,chh=int(sw/zoom),int(sh/zoom); cx0=int(sw*.5-cw*.5); cy0=int(max(0,240-scroll)*0+120*(zoom-1)/.18*.4)
        view=view.crop((cx0,cy0,cx0+cw,cy0+chh)).resize((sw,sh),Image.BICUBIC)
    # marco del telefono
    d.rounded_rectangle([sx0-26,sy0-30,sx0+sw+26,sy0+sh+40],radius=46,fill=(24,24,28));
    img.paste(view,(sx0,sy0)); d=ImageDraw.Draw(img)
    d.rounded_rectangle([sx0+sw//2-60,sy0-14,sx0+sw//2+60,sy0-2],radius=6,fill=(10,10,12))
    # reflejo del cristal y brillo
    ov=Image.new("RGBA",img.size,(0,0,0,0)); od=ImageDraw.Draw(ov); od.polygon([(sx0,sy0),(sx0+sw*.55,sy0),(sx0+sw*.2,sy0+sh)],fill=(255,255,255,16)); img=Image.alpha_composite(img.convert("RGBA"),ov).convert("RGB")
    return fin(grade(img,warm=.6,seed=int(u*30)))
# ---------------- escena 2: noclip ----------------
def sceneC(u):
    seed=int(u*30)
    if u<3.0:
        t=u; cam=walk_cam(t,speed=.9); cam["pitch"]=.14+.4*sm((u-1.6)/1.4); cam["y"]=1.62-1.35*sm((u-1.8)/1.2)*1.0
        im=render(cam,OFFICE,t,1.0)
    elif u<3.5:
        p=(u-3.0)/.5; cam=dict(x=0,y=.05,z=2.5,yaw=.0,pitch=.5)
        im=render(cam,OFFICE,u,1.0); im=tear(im,3.0,seed); a=np.asarray(im).astype(np.float32)*(1-p*.9); im=Image.fromarray(a.astype(np.uint8))
    else:
        t=u-3.5; fall=sm(clamp(t/1.2)); cam=dict(x=0.0,y=2.55-.93*fall+(.04*math.sin(t*14)*math.exp(-t*3) if t>1.2 else 0),z=0.0,yaw=.35*sm(clamp((t-1.8)/2.5)),pitch=.6-.46*fall)
        im=render(cam,YELLOW,t,flick(u))
        if t<.35: im=tear(im,2.0*(1-t/.35),seed)
        if t<.5:
            a=np.asarray(im).astype(np.float32); a=a*(.2+.8*clamp(t/.5)); im=Image.fromarray(a.astype(np.uint8))
    return fin(grade(im,seed=seed))
# ---------------- escena 3: laberinto infinito ----------------
def sceneD(u):
    t=u; cam=cam_at(t+3,speed=1.0,sway=1.1); cam["yaw"]=.9*math.sin(t*.55)*(1 if int(t*.55/math.pi)%2==0 else 1)
    im=render(cam,YELLOW,t,flick(u))
    if 2.5<u<8: im=entity(im,cam,YELLOW,-2.4,cam["z"]+11,h=2.3,t=u,walk=u*1.0,a=int(200*clamp((u-2.5)/1.0)*clamp((8-u)/1.0)),lean=.1)
    return fin(grade(im,seed=int(u*30)))
# ---------------- escena 4: archivo de niveles y entidades ----------------
_TH={}
def thumbs():
    if not _TH:
        c=dict(x=0,y=1.6,z=0,yaw=0,pitch=.08)
        def mk(st,cam,ent=False):
            im=render(cam,st,0.0)
            if ent: im=entity(im,cam,st,.2,13.0,h=2.35,t=1.0,walk=.5)
            return im.crop((0,380,RW,380+int(RW*.56))).resize((600,336),Image.BILINEAR)
        _TH["0"]=mk(YELLOW,dict(c)); _TH["1"]=mk(CONCRETE,dict(c,z=2.0)); _TH["2"]=mk(TUNNEL,dict(c,z=3.0)); _TH["e"]=mk(YELLOW,dict(c,z=8.0),True)
    return _TH
def sceneE(u):
    th=thumbs(); PH=2300; page=Image.new("RGB",(RW,PH),(24,26,30)); p=ImageDraw.Draw(page)
    p.rectangle([0,0,RW,110],fill=(12,14,18)); p.text((40,30),"ARCHIVO: LOS BACKROOMS",font=font(38,True),fill=(232,214,110))
    y=140
    for key,name,desc in(("0","NIVEL 0  -  Las salas","Oficinas vacias, moqueta humeda y luz fluorescente."),("1","NIVEL 1  -  Garaje","Hormigon, pilares y farolas apagadas."),("2","NIVEL 2  -  Tuneles","Tuberias, calor y oscuridad."),("e","ENTIDADES","Figuras altas que se ven al fondo.")):
        p.text((40,y),name,font=font(32,True),fill=(240,240,240)); y+=52
        page.paste(th[key].resize((640,358)),(40,y)); p.rectangle([40,y,680,y+358],outline=(90,92,100),width=2); y+=374
        p.text((40,y),desc,font=font(24),fill=(190,192,200)); y+=58
    p.text((40,y),"REGLAS",font=font(32,True),fill=(240,240,240)); y+=56
    for k in range(5):
        p.rectangle([40,y,70,y+30],outline=(232,214,110),width=3); p.rectangle([90,y+8,90+int(380+90*math.sin(k*1.9)),y+22],fill=(120,124,136)); y+=54
    scroll=int(1500*sm(u/7.0)); view=page.crop((0,scroll,RW,scroll+RH))
    # parpadeo suave del monitor
    a=np.asarray(view).astype(np.float32); yy=np.arange(RH)[:,None,None]; a*=(.96+.04*np.sin(yy*1.2+u*30)); view=Image.fromarray(np.clip(a,0,255).astype(np.uint8))
    return fin(grade(view,warm=.3,grain=3,seed=int(u*30)))
# ---------------- escena 5: grabacion de camara (metraje encontrado) ----------------
def sceneF(u):
    t=u+11; cam=cam_at(t,speed=.9,sway=2.3,pitch=.1)
    zoom=1.0+.25*sm(u/6.5)
    st=dict(YELLOW,fov=64/zoom)
    im=render(cam,st,u,flick(u*1.3))
    vis=(math.sin(u*5.3)*math.sin(u*2.1)>-.55)
    if u>.8 and vis: im=entity(im,cam,st,.05+.2*math.sin(u),cam["z"]+16-u*.9,h=2.4,t=u,walk=u*1.5,a=235)
    im=vhs(im,u,1.0); im=camcorder_overlay(im,u+31)
    return fin(grade(im,warm=.5,sat=.8,grain=6,seed=int(u*30)))
# ---------------- escena 6: sala enorme ----------------
def sceneG(u):
    t=u+20; cam=dict(x=0.0,y=1.62+.02*math.sin(t*3.8),z=u*.8,yaw=.35*math.sin(u*.35),pitch=.13)
    st=dict(WIDE,hw=9.0,panel_cols=(-3,-1,0,1,3),fov=72,gain=.5)
    im=render(cam,st,u,flick(u*.7))
    for k,(xe,ze,ph) in enumerate(((-3.5,15,0),(3.0,21,1.5),(.5,27,3))): im=entity(im,cam,st,xe,cam["z"]+ze-u*.2,h=2.3,t=u+ph,walk=0,a=int(190-k*30))
    return fin(grade(im,seed=int(u*30)))
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur): return 1.0,270,480
core.CAM=cam
if __name__=="__main__": core.main()
