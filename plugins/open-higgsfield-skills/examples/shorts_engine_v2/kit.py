"""Utilidades comunes de escena (composicion 3D + personajes del rig + efectos)."""
import math, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import core
from core import clamp, sm
from liminal import project,RW,RH,walk_cam,font,vhs,camcorder_overlay
from rig import *
from art import ptext,film_strip,clapper,stars,gradient,film_camera
from solids import *
OUTSZ=(1620,2880)
def fin(img): return img.resize(OUTSZ,Image.BICUBIC)
def lerp(a,b,t): return a+(b-a)*t
def flick(u,r=.93): return 1.0 if (math.sin(u*37)*math.sin(u*11.3+1.7))<r else .55
def grade(img,sat=.95,grain=3.5,seed=0,tint=(1,1,1),vig=0.0):
    a=np.asarray(img).astype(np.float32); g=a.mean(2,keepdims=True); a=g+(a-g)*sat
    a=a*np.array(tint,np.float32)[None,None,:]+np.random.default_rng(seed).normal(0,grain,a.shape[:2])[:,:,None]
    return Image.fromarray(np.clip(a,0,255).astype(np.uint8))
def serif(sz,bold=True): return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif%s.ttf"%("-Bold" if bold else ""),sz)
def mono(sz,bold=False): return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono%s.ttf"%("-Bold" if bold else ""),sz)
def place3(cam,st,xw,zw,hm=1.75,y0=0.0):
    p=project(cam,(xw,y0,zw)); x1,y2,z2=p
    if z2<.3: return None
    k=(1.0/math.tan(math.radians(st["fov"])/2))*RW/2; px=RW/2+x1/z2*k; py=RH/2-y2/z2*k; ph=hm*k/z2
    return px/RW*540,py/RH*960,(ph/RH*960)/232.0,z2
def mix_(c,fc,k): return tuple(int(c[i]*k+fc[i]*(1-k)) for i in range(3))
def fade(style,k,fog=(20,20,24)):
    out={}
    for key,v in style.items():
        out[key]=tuple(int(c*k+fog[i]*(1-k)*.8) for i,c in enumerate(v)) if (isinstance(v,tuple) and len(v)==3 and all(isinstance(c,(int,float)) for c in v)) else v
    return out
def P3(d,cam,st,xw,zw,style,pose,hm=1.75,u=0.0,y0=0.0,tone=1.0,fog=(20,20,24),**kw):
    pl=place3(cam,st,xw,zw,hm,y0)
    if not pl: return None
    lx,ly,sc,z2=pl; k=tone*math.exp(-z2*.015); bust=kw.pop('bust',False); stl=fade(style,min(1.0,k),fog)
    if bust: stl['bust']=True
    return person(d,lx,ly,sc,u,pose,stl,**kw)
def hand3(d,cam,st,p3,hand_m=.19,a=3.0,s=1,skin=(236,190,150),curl=.4,spread=.6,prop=None,point=False,sleeve=(70,90,120),arm_from=(0,1.3),arm_w=.075):
    """mano grande en un punto 3D (muneca), con antebrazo desde el borde inferior"""
    q=project(cam,p3); x1,y2,z2=q
    if z2<.2: return
    k=(1.0/math.tan(math.radians(st["fov"])/2))*RW/2; px=(RW/2+x1/z2*k)/RW*540; py=(RH/2-y2/z2*k)/RH*960; pxh=hand_m*k/z2*960/RH; sc=pxh/22.0
    ax=(arm_from[0] if arm_from[0] else px+60*sc/2)*1; ay=960*arm_from[1]
    w=arm_w*k/z2*960/RH
    d.L(ax,ay,px,py,sleeve+(255,),w); d.L(px-(px-ax)*.0,py-(py-ay)*.0,px,py,sleeve+(255,),w)
    d.L(px+(ax-px)*.16,py+(ay-py)*.16,px,py,skin+(255,),w*.78)
    hand(d,px,py,a,s,sc,skin,curl=curl,spread=spread,prop=prop,point=point)
def crt(tex,glow=1.0,seed=0):
    """pantalla CRT: reescala con pixeles gruesos, lineas de barrido, mascara de fosforo y viñeteo"""
    w,h=tex.size; im=tex.resize((w*3,h*3),Image.NEAREST).filter(ImageFilter.GaussianBlur(.8)); a=np.asarray(im).astype(np.float32)
    a[1::3]*=.78; a[2::3]*=.88
    yy,xx=np.mgrid[0:a.shape[0],0:a.shape[1]]; r=((xx-a.shape[1]/2)/(a.shape[1]/2))**2+((yy-a.shape[0]/2)/(a.shape[0]/2))**2; a*=(1-.28*np.clip(r-.25,0,1))[:,:,None]
    a=a*glow+np.random.default_rng(seed).normal(0,3,a.shape[:2])[:,:,None]
    return Image.fromarray(np.clip(a,0,255).astype(np.uint8))
def screen_glow(ov,cam,st,p,rgb,r=1.6,a=70):
    glow(ov,cam,st,p,rgb,r,a,layers=7)
def text_img(w,h,bg,lines,fg=(255,255,255),sz=26,f=None,pad=14,bold=True):
    im=Image.new("RGB",(w,h),bg); d=ImageDraw.Draw(im); y=pad
    for ln in lines:
        d.text((pad,y),ln,font=(f or font)(sz,bold) if f is None else f(sz),fill=fg); y+=int(sz*1.4)
    return im
def snow_particles(img,t,n=80,col=(255,255,255),sz=2.0,speed=60,seed=1,alpha=160,scale=1.0):
    rng=np.random.default_rng(seed); W,Hh=img.size; ov=Image.new("RGBA",img.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    for i in range(n):
        r=(sz*(.6+rng.random()))*scale; x=(rng.random()*W+math.sin(t*1.3+i)*14)%W; y=(rng.random()*Hh+t*speed*(.5+rng.random())*scale)%Hh
        d.ellipse([x-r,y-r,x+r,y+r],fill=col+(alpha,))
    return Image.alpha_composite(img.convert("RGBA"),ov.filter(ImageFilter.GaussianBlur(.6))).convert("RGB")
def vignette_ov(size,strength=.5):
    w,h=size; yy,xx=np.mgrid[0:h,0:w]; r=((xx-w/2)/(w/2))**2+((yy-h/2)/(h/2))**2
    a=(np.clip(r-.35,0,1)*255*strength).astype(np.uint8); ov=np.zeros((h,w,4),np.uint8); ov[...,3]=a; return Image.fromarray(ov)
