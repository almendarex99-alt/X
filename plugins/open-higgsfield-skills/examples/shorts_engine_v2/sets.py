"""Mobiliario y decorado reutilizable (cajas y cuadrilateros con textura) para dar vida a los interiores."""
import math, numpy as np
from PIL import Image, ImageDraw, ImageFilter
from solids import *
from kit import mono, text_img
def tex_books(w=240,h=300,seed=1,shelves=5):
    rng=np.random.default_rng(seed); im=Image.new("RGB",(w,h),(54,36,24)); d=ImageDraw.Draw(im)
    sh=h/shelves
    for s in range(shelves):
        y0=s*sh+6; x=8
        while x<w-12:
            bw=int(10+rng.random()*14); bh=int(sh*(.55+rng.random()*.3)); col=tuple(int(c) for c in (rng.random(3)*150+60))
            d.rectangle([x,y0+sh-bh-8,x+bw,y0+sh-8],fill=col,outline=(30,20,16)); d.line([x+3,y0+sh-bh-4,x+3,y0+sh-12],fill=tuple(min(255,c+50) for c in col)); x+=bw+1
        d.rectangle([0,y0+sh-8,w,y0+sh-3],fill=(96,66,40))
    return im
def tex_window(w=200,h=260,night=True,curtains=(150,50,50),seed=2):
    im=Image.new("RGB",(w,h),(10,14,30) if night else (150,190,235)); d=ImageDraw.Draw(im); rng=np.random.default_rng(seed)
    if night:
        for k in range(30): x=rng.random()*w; y=rng.random()*h*.7; d.ellipse([x-1,y-1,x+1,y+1],fill=(220,230,255))
    d.rectangle([0,0,w-1,h-1],outline=(90,70,50),width=10); d.line([(w/2,0),(w/2,h)],fill=(90,70,50),width=6); d.line([(0,h*.55),(w,h*.55)],fill=(90,70,50),width=6)
    for sg in (0,1):
        x0=0 if sg==0 else w-46
        for k in range(8): d.rectangle([x0+k*6,0,x0+k*6+5,h],fill=tuple(int(c*(.8+.25*(k%2))) for c in curtains))
    return im
def tex_poster(w=160,h=220,seed=3,col=(200,60,50)):
    rng=np.random.default_rng(seed); im=Image.new("RGB",(w,h),col); d=ImageDraw.Draw(im)
    for k in range(5):
        x0=rng.random()*w*.5; y0=rng.random()*h*.5; d.ellipse([x0,y0,x0+30+rng.random()*w*.5,y0+30+rng.random()*h*.4],fill=tuple(int(c) for c in (rng.random(3)*200+40)))
    d.rectangle([4,4,w-5,h-5],outline=(250,250,240),width=4); return im
def tex_rug(w=300,h=200,base=(120,40,40)):
    im=Image.new("RGB",(w,h),base); d=ImageDraw.Draw(im)
    for k in range(7): d.rectangle([k*10,k*10,w-k*10,h-k*10],outline=tuple(int(c*(.6+.5*(k%2))) for c in base),width=6)
    for x in range(40,w-40,40):
        for y in range(40,h-40,40): d.polygon([(x,y-12),(x+12,y),(x,y+12),(x-12,y)],fill=(220,190,90))
    return im
def tex_wood(w=200,h=200,base=(150,110,70),seed=3):
    rng=np.random.default_rng(seed); im=Image.new("RGB",(w,h),base); d=ImageDraw.Draw(im)
    for k in range(40): y=rng.random()*h; d.line([(0,y),(w,y+rng.random()*6-3)],fill=tuple(int(c*(.7+rng.random()*.3)) for c in base),width=int(1+rng.random()*2))
    return im
def lamp(back,cam,st,x,z,h=1.3,col=(255,196,120)):
    box(back,cam,st,x-.1,x+.1,0,.05,z-.1,z+.1,(60,44,34)); box(back,cam,st,x-.025,x+.025,.05,h-.3,z-.025,z+.025,(80,60,44))
    box(back,cam,st,x-.2,x+.2,h-.3,h,z-.2,z+.2,col,emis=.55,shadow=False); glow(back,cam,st,(x,h-.15,z),col,.9,70,6)
def plant(back,cam,st,x,z,h=1.1):
    box(back,cam,st,x-.16,x+.16,0,.32,z-.16,z+.16,(150,84,56))
    for k in range(7):
        a=k*.9; ox=math.cos(a)*.14; oz=math.sin(a)*.14; box(back,cam,st,x+ox-.1,x+ox+.1,.3+.1*k%.5,.3+.1*k%.5+.6+(k%3)*.1,z+oz-.03,z+oz+.03,(40+k*8,110+k*4,48),shadow=False)
def bookcase(back,cam,st,x,z,face="z0",w=1.2,h=2.0,d=.35,seed=1):
    box(back,cam,st,x-w/2,x+w/2,0,h,z,z+d,(86,58,36))
    tquad(back,cam,st,(x-w/2+.04,h-.05,z-.003),(x+w/2-.04,h-.05,z-.003),(x+w/2-.04,.05,z-.003),(x-w/2+.04,.05,z-.003),tex_books(seed=seed))
def sidewindow(back,cam,st,x,z0,z1,y0=.8,y1=2.1,night=True,curt=(150,50,50)):
    tquad(back,cam,st,(x,y1,z0),(x,y1,z1),(x,y0,z1),(x,y0,z0),tex_window(night=night,curtains=curt))
def tex_carts(w=300,h=220,seed=5):
    rng=np.random.default_rng(seed); im=Image.new("RGB",(w,h),(46,40,38)); d=ImageDraw.Draw(im)
    for r in range(4):
        y=r*55+8; d.rectangle([0,y+46,w,y+52],fill=(120,100,80))
        for c in range(7):
            x=8+c*42; col=[(200,40,40),(40,70,200),(40,160,70),(230,200,60)][(r+c)%4]; d.rectangle([x,y,x+34,y+44],fill=(160,160,156),outline=(90,90,90)); d.rectangle([x+4,y+5,x+30,y+26],fill=col); d.rectangle([x+8,y+32,x+26,y+40],fill=(60,60,60))
    return im
def bulldozer(ov,cam,st,x,z,face=1,col=(236,186,40),blade_lift=0.0):
    f=face
    box(ov,cam,st,x-1.4,x-.9,0,.9,z-1.7,z+1.7,(40,40,44)); box(ov,cam,st,x+.9,x+1.4,0,.9,z-1.7,z+1.7,(40,40,44))
    box(ov,cam,st,x-1.0,x+1.0,.55,1.4,z-1.4,z+1.5,col); box(ov,cam,st,x-.8,x+.8,1.4,2.6,z-1.3,z-.1,col)
    tquad(ov,cam,st,(x-.78,2.45,z-1.31),(x+.78,2.45,z-1.31),(x+.78,1.5,z-1.31),(x-.78,1.5,z-1.31),Image.new("RGB",(60,50),(80,110,140))) if f>0 else None
    box(ov,cam,st,x+.5,x+.62,1.4,2.9,z+.6,z+.72,(50,50,54),shadow=False)
    bz=z+1.9*f
    box(ov,cam,st,x-1.6,x+1.6,.15+blade_lift,1.2+blade_lift,bz-.1,bz+.1,(210,160,34)); 
    for sg in (-1,1): box(ov,cam,st,x+sg*1.2-.06,x+sg*1.2+.06,.5,.8,z+1.4,bz,(60,60,64),shadow=False)
def dump_truck(ov,cam,st,x,z,face=1,col=(200,60,40),tilt=0.0):
    box(ov,cam,st,x-1.0,x+1.0,.5,2.4,z-2.6*face,z-1.2*face,col)
    box(ov,cam,st,x-1.1,x+1.1,.7,1.3,z-1.1*face,z+2.6*face,(90,90,96)); box(ov,cam,st,x-1.2,x+1.2,1.2+tilt,2.2+tilt,z-1.0*face,z+2.8*face,(150,150,156))
    for zz in (-1.9,-.2,1.6,2.3):
        for sg in (-1,1): box(ov,cam,st,x+sg*1.1-.15,x+sg*1.1+.15,0,.9,z+zz*face-.4,z+zz*face+.4,(24,24,26),shadow=False)
def carts_heap(ov,cam,st,x,z,n=140,r=2.4,h=1.2,seed=1):
    rng=np.random.default_rng(seed); items=[]
    for k in range(n):
        a=rng.random()*6.28; rr=r*math.sqrt(rng.random()); hh=h*(1-rr/r)**1.2*rng.random()+.03
        items.append((x+math.cos(a)*rr,hh,z+math.sin(a)*rr*.8,rng.random(),rng.random()))
    items.sort(key=lambda it:-((it[0]-cam["x"])**2+(it[2]-cam["z"])**2))
    for (cx,cy,cz,r1,r2) in items:
        c=int(130+r1*70); box(ov,cam,st,cx-.07,cx+.07,cy,cy+.18,cz-.015,cz+.015,(c,c,c-6),edge=(70,70,70),shadow=False)
        if r2>.5: poly3(ov,cam,st,[(cx-.05,cy+.12,cz-.0155),(cx+.05,cy+.12,cz-.0155),(cx+.05,cy+.05,cz-.0155),(cx-.05,cy+.05,cz-.0155)],(220,190,60) if r1>.5 else (200,60,50))
def excavator(ov,cam,st,x,z,face=1,col=(236,186,40),ang=0.0):
    box(ov,cam,st,x-1.4,x+1.4,0,.7,z-1.6,z+1.6,(40,40,44)); box(ov,cam,st,x-1.1,x+1.1,.7,1.7,z-1.2,z+1.0,col); box(ov,cam,st,x-.7,x+.7,1.7,2.8,z-1.1,z-.1,col)
    tquad(ov,cam,st,(x-.68,2.7,z-1.11),(x+.68,2.7,z-1.11),(x+.68,1.8,z-1.11),(x-.68,1.8,z-1.11),Image.new("RGB",(60,50),(80,110,140)))
    bx=x; 
    poly3(ov,cam,st,[(bx-.15,1.4,z+1.0),(bx+.15,1.4,z+1.0),(bx+.15,3.4+.4*math.sin(ang),z+3.6*face),(bx-.15,3.4+.4*math.sin(ang),z+3.6*face)],col)
    poly3(ov,cam,st,[(bx-.12,3.4+.4*math.sin(ang),z+3.6*face),(bx+.12,3.4+.4*math.sin(ang),z+3.6*face),(bx+.12,1.0+.5*math.cos(ang),z+5.4*face),(bx-.12,1.0+.5*math.cos(ang),z+5.4*face)],shd(col,.85))
    box(ov,cam,st,bx-.5,bx+.5,.6+.5*math.cos(ang),1.3+.5*math.cos(ang),z+5.2*face,z+5.9*face,(150,120,40),shadow=False)
BONE=(234,228,210)
def _bs(d,p,q,w,col=BONE): d.L(p[0],p[1],q[0],q[1],col+(255,),w); d.E(p[0],p[1],w/2*1.15,w/2*1.15,col+(255,)); d.E(q[0],q[1],w/2*1.15,w/2*1.15,col+(255,))
def skeleton(d,x,y,sc,u,wave=0.0,sway=0.0,lean=0.0):
    """esqueleto articulado (sin aspecto truculento): craneo, columna, costillas, pelvis, brazos con dedos y piernas con rodillas"""
    dk=(170,160,138); s=sway*math.sin(u*2)*4*sc
    hip=(x+s,y-98*sc); sh=(x+s+lean*20*sc,hip[1]-66*sc)
    for k in range(7): t=k/6; px=hip[0]+(sh[0]-hip[0])*t; py=hip[1]+(sh[1]-hip[1])*t; d.E(px,py,5*sc,3.4*sc,BONE+(255,)); d.E(px,py+1.5*sc,3.4*sc,2*sc,dk+(255,))
    for k in range(5):
        t=.35+k*.13; px=hip[0]+(sh[0]-hip[0])*t; py=hip[1]+(sh[1]-hip[1])*t; wd=(26-k*3)*sc
        for sg in(-1,1): d.A(px+sg*wd*.3,py,wd*.9,9*sc,0 if sg>0 else 180,180 if sg>0 else 360,BONE+(255,),2.4*sc) if False else d.L(px,py,px+sg*wd,py+5*sc,BONE+(255,),2.4*sc)
    d.L(sh[0]-26*sc,sh[1]+4*sc,sh[0]+26*sc,sh[1]+4*sc,BONE+(255,),4*sc)
    d.P([(hip[0]-20*sc,hip[1]-6*sc),(hip[0]+20*sc,hip[1]-6*sc),(hip[0]+14*sc,hip[1]+14*sc),(hip[0]-14*sc,hip[1]+14*sc)],BONE+(255,)); d.E(hip[0],hip[1]+4*sc,6*sc,6*sc,(30,24,20,255))
    hd=(sh[0]+lean*6*sc,sh[1]-30*sc); d.E(hd[0],hd[1],16*sc,18*sc,BONE+(255,)); d.R(hd[0]-9*sc,hd[1]+10*sc,hd[0]+9*sc,hd[1]+22*sc,BONE+(255,),3*sc)
    for sg in(-1,1): d.E(hd[0]+sg*6*sc,hd[1]-1*sc,4.6*sc,5.4*sc,(24,20,18,255))
    d.P([(hd[0]-2*sc,hd[1]+5*sc),(hd[0]+2*sc,hd[1]+5*sc),(hd[0],hd[1]+1*sc)],(24,20,18,255))
    for k in range(5): d.L(hd[0]-8*sc+k*4*sc,hd[1]+13*sc,hd[0]-8*sc+k*4*sc,hd[1]+20*sc,(40,30,26,255),1.2*sc)
    for sg in(-1,1):
        a1=.25+sg*0+.6*wave*(1 if sg>0 else .5); a2=.5+wave*1.4
        e=(sh[0]+sg*(28+math.sin(a1)*34)*sc,sh[1]+4*sc+math.cos(a1)*34*sc-wave*30*sc); w=(e[0]+sg*math.sin(a2)*32*sc,e[1]+math.cos(a2)*32*sc-wave*34*sc)
        _bs(d,(sh[0]+sg*26*sc,sh[1]+4*sc),e,5*sc); _bs(d,e,w,4.4*sc)
        for k in range(4): d.L(w[0],w[1],w[0]+sg*(3+k*2.4)*sc,w[1]+(14+(k%2)*3)*sc,BONE+(255,),1.8*sc)
        d.L(w[0],w[1],w[0]-sg*8*sc,w[1]+8*sc,BONE+(255,),1.8*sc)
    for sg in(-1,1):
        h_=(hip[0]+sg*10*sc,hip[1]+12*sc); k_=(h_[0]+sg*(6+math.sin(u*2+sg)*4)*sc,h_[1]+46*sc); a_=(k_[0]+sg*2*sc,k_[1]+46*sc)
        _bs(d,h_,k_,6.4*sc); _bs(d,k_,a_,5.2*sc); d.E(a_[0]+sg*6*sc,a_[1]+3*sc,10*sc,4.4*sc,BONE+(255,))
