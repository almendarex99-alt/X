"""Terreno abierto (numpy): suelo con textura procedural (arena, hierba, asfalto con acera, tierra, nieve), cielo con degradado,
sol/luna, estrellas, montanas lejanas, niebla y luces puntuales."""
import math, numpy as np
from PIL import Image, ImageFilter
from liminal import S,N1,N2,N3,FINE,_hash,RW,RH,_SX,_SY
SKY=dict(
 sunset=dict(hor=(255,170,96),zen=(52,70,130),sun=(.62,.10,.77),sunc=(255,236,190),stars=0),
 dusk=dict(hor=(180,110,110),zen=(18,24,60),sun=(.7,.06,.7),sunc=(255,200,160),stars=.3),
 night=dict(hor=(36,46,84),zen=(6,9,26),sun=(.3,.6,.7),sunc=(235,240,255),stars=1),
 day=dict(hor=(206,224,246),zen=(70,130,212),sun=(.3,.7,.65),sunc=(255,250,225),stars=0),
 overcast=dict(hor=(176,182,190),zen=(130,138,150),sun=(.0,.9,.1),sunc=(0,0,0),stars=0))
def mk(**kw):
    d=dict(fov=66,ground="sand",sky="sunset",fog=.012,fogcol=(220,170,130),amb=(1,1,1),ambient=1.0,hills=.05,hcol=(120,80,70),ncol=1.0)
    d.update(kw); return d
def _ground(kind,x,z,t_):
    fn=(S(FINE,x*30,z*30)-.5)*np.exp(-t_/10.0)
    if kind=="sand":
        base=np.array((214,170,112),np.float32); col=base[None,:]*(1+(S(N2,x*.35,z*.35)-.5)*.3)[:,None]*(1+(S(N3,x*2.0,z*.5)-.5)*.1)[:,None]*(1+fn*.2)[:,None]
        sc=(S(FINE,x*40+4,z*40)>.99)*np.exp(-t_/18); col+=(sc*40)[:,None]
    elif kind=="grass":
        base=np.array((44,70,40),np.float32); col=base[None,:]*(1+(S(N2,x*.5,z*.5)-.5)*.4)[:,None]*(1+fn*.5)[:,None]
    elif kind=="dirt":
        base=np.array((98,72,50),np.float32); col=base[None,:]*(1+(S(N2,x*.8,z*.8)-.5)*.4)[:,None]*(1+fn*.4)[:,None]
    elif kind=="snow":
        base=np.array((226,232,246),np.float32); col=base[None,:]*(1+(S(N2,x*.5,z*.5)-.5)*.14)[:,None]
    elif kind=="asphalt":
        base=np.array((58,58,62),np.float32); col=base[None,:]*(1+(S(N2,x*.9,z*.9)-.5)*.3)[:,None]*(1+fn*.35)[:,None]
        for cx_ in (-6,6): pass
    elif kind=="street":
        ax=np.abs(x); road=ax<3.4; walk=(ax>=3.4)&(ax<4.6)
        asp=np.array((54,54,58),np.float32)[None,:]*(1+(S(N2,x*.9,z*.9)-.5)*.3)[:,None]*(1+fn*.35)[:,None]
        dash=(np.abs(x)<.08)&(((z/3.0)%1.0)<.5); asp=np.where(dash[:,None],np.array((220,190,60),np.float32)[None,:],asp)
        cw=np.array((150,150,146),np.float32)[None,:]*(1+(S(N2,x*.6,z*.6)-.5)*.15)[:,None]*(1+fn*.2)[:,None]; sm_=((z/1.5)%1.0<.02); cw=np.where(sm_[:,None],cw*.7,cw)
        gr=np.array((46,72,40),np.float32)[None,:]*(1+(S(N2,x*.5,z*.5)-.5)*.4)[:,None]*(1+fn*.5)[:,None]
        col=np.where(road[:,None],asp,np.where(walk[:,None],cw,gr))
    else: col=np.repeat(np.array((120,120,120),np.float32)[None,:],x.shape[0],0)
    return col
def render_terrain(cam,st,t=0.0,extra=()):
    f=1.0/math.tan(math.radians(st["fov"])/2); cx,cy,cz=cam["x"],cam["y"],cam["z"]; yaw=cam.get("yaw",0.0); pit=cam.get("pitch",0.0); roll=cam.get("roll",0.0)
    sx,sy=_SX,_SY
    if roll: sx,sy=sx*math.cos(roll)-sy*math.sin(roll),sx*math.sin(roll)+sy*math.cos(roll)
    dx0,dy0,dz0=sx,sy,np.full_like(sx,f)
    cp,sp=math.cos(pit),math.sin(pit); dy1=dy0*cp-dz0*sp; dz1=dy0*sp+dz0*cp
    cyw,syw=math.cos(yaw),math.sin(yaw); dx=dx0*cyw+dz1*syw; dz=-dx0*syw+dz1*cyw; dy=dy1
    sk=SKY[st["sky"]]; n=np.sqrt(dx*dx+dy*dy+dz*dz)+1e-6; e=dy/n
    with np.errstate(divide="ignore",invalid="ignore"): tf=np.where(dy<-1e-5,(0-cy)/dy,1e6)
    isg=tf<1e5; out=np.zeros((RH,RW,3),np.float32)
    hor=np.array(sk["hor"],np.float32); zen=np.array(sk["zen"],np.float32)
    s=np.clip(e*1.7,0,1)[:,:,None]; sky=hor[None,None,:]*(1-s)+zen[None,None,:]*s
    if sk["stars"]:
        ux,uz=dx/(dy+1e-3),dz/(dy+1e-3); star=(S(FINE,ux*70+1.1,uz*70)>.9966)*(.5+.5*np.sin(t*3+ux*40))*sk["stars"]*(e>0.02)
        sky=sky+star[:,:,None]*np.array([220,230,255],np.float32)[None,None,:]*.9
    mx,my,mz=sk["sun"]; mn=math.sqrt(mx*mx+my*my+mz*mz); dot=(dx*mx+dy*my+dz*mz)/n/mn
    sc=np.array(sk["sunc"],np.float32)[None,None,:]; sky=sky+(np.exp((dot-1)*40)*60+np.exp((dot-1)*900)*140+(dot>.9992)*255)[:,:,None]*sc/255*1.0
    # montanas lejanas
    az=np.arctan2(dx,dz); hh=st["hills"]*(.5+S(N1,(az*1.3)%1.0*0+az*.35,np.zeros_like(az)+.3)+.6*S(N2,az*.9,np.zeros_like(az)+.1))
    hc=np.array(st["hcol"],np.float32)[None,None,:]; mt=(e<hh)&(e>0)
    sky=np.where(mt[:,:,None],hc*(.7+.4*(e/ (hh+1e-3)))[:,:,None]*.0+hc*(1-.4*(e/(hh+1e-4)))[:,:,None],sky)
    out=sky
    if isg.any():
        xh=cx+tf*dx; zh=cz+tf*dz; m=isg; col=_ground(st["ground"],xh[m],zh[m],tf[m])
        amb=np.array(st["amb"],np.float32)[None,:]*st["ambient"]; Ls=np.zeros((int(m.sum()),3),np.float32)
        for (x,y,z,rgb,I) in extra:
            d2=(xh[m]-x)**2+(y-0)**2+(zh[m]-z)**2; Ls+=(I/(1+.3*d2))[:,None]*np.array(rgb,np.float32)[None,:]
        out[m]=col*(amb+Ls)
    # niebla dependiente de la distancia (suelo) y del horizonte
    dist=np.where(isg,tf*n,0.0); fg=np.exp(-np.minimum(dist,600)*st["fog"])[:,:,None]; fc=np.array(st["fogcol"],np.float32)[None,None,:]
    out=out*fg+fc*(1-fg)
    haze=np.where(isg,0.0,np.exp(-np.clip(e,0,1)*7)*.45)[:,:,None]; out=out*(1-haze)+fc*haze
    out=np.clip(out,0,255)
    return Image.fromarray(out.astype(np.uint8)).filter(ImageFilter.GaussianBlur(.6))
