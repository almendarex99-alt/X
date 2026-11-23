"""Motor 3D general de interiores (numpy): pasillos y salas cerradas con muchos materiales (yeso, metal, piedra, madera, hormigon, panel retro),
suelos (rejilla, losas, tarima, goma, moqueta), techos (yeso, vigas, tuberias, bovedas, tiras de luz), luces puntuales de color con parpadeo
y luces dinamicas (linterna, antorchas, pantallas). Complementa a liminal.py."""
import math, numpy as np
from PIL import Image, ImageFilter
from liminal import S,N1,N2,N3,FINE,_hash,RW,RH,_SX,_SY,project,walk_cam,font
BASE=dict(H=2.8,hw=2.0,seg=6.0,open_p=0.0,open_a=.3,open_b=.6,D=4.0,fov=66,zend=None,zback=None,
  wall="plaster",floor="wood",ceil="plaster",wcol=(206,198,184),wcol2=(150,130,100),fcol=(120,86,54),ccol=(222,220,212),
  ambient=.30,amb_rgb=(1,1,1),gain=1.0,fog=.02,fogcol=(10,10,12),plights=None,strip=(150,190,255),hazard=False,sheen=.0)
def mk(**kw): d=dict(BASE); d.update(kw); return d
def _wall(kind,u,v,st,dist):
    base=np.array(st["wcol"],np.float32); b2=np.array(st["wcol2"],np.float32); n=u.shape[0]; emis=None
    fn=(S(FINE,u*22,v*22)-.5)*np.exp(-dist/5.0)
    if kind=="plaster":
        col=base[None,:]*(1+(S(N2,u*.6,v*.6)-.5)*.16)[:,None]*(1+fn*.12)[:,None]
        col=np.where((v<.12)[:,None],b2[None,:]*(.9+.2*S(N3,u*3,v*3))[:,None],col); col=np.where(((v>.12)&(v<.135))[:,None],col*.72,col)
        stn=np.clip((S(N1,u*.3+2,v*.7)-.6)*5,0,1)*np.clip(1.2-v,0,1); col*=(1-.22*stn)[:,None]
    elif kind=="metal":
        fu=(u/1.2)%1.0; fv=(v/1.0)%1.0; pid=np.floor(u/1.2)*7+np.floor(v/1.0)*3; h=_hash(pid,3)
        col=base[None,:]*(.82+.3*h)[:,None]*(1+(S(N2,u*1.5,v*1.5)-.5)*.2)[:,None]*(1+fn*.1)[:,None]
        seam=(fu<.018)|(fu>.982)|(fv<.018)|(fv>.982); col=np.where(seam[:,None],col*.45,col)
        riv=(((fu-.06)**2+(fv-.06)**2)<.0006)|(((fu-.94)**2+(fv-.06)**2)<.0006)|(((fu-.06)**2+(fv-.94)**2)<.0006)|(((fu-.94)**2+(fv-.94)**2)<.0006); col=np.where(riv[:,None],col*1.35,col)
        vent=(h>.86)&(fv>.25)&(fv<.75)&(fu>.2)&(fu<.8)&(((fv*14)%1.0)<.5); col=np.where(vent[:,None],col*.35,col)
        if st["hazard"]: hz=(v<.22); stp=((u+v)*5)%1.0<.5; col=np.where(hz[:,None],np.where(stp[:,None],np.array((226,186,40),np.float32)[None,:],np.array((30,30,32),np.float32)[None,:])*(.9+fn[:,None]*.1),col)
        es=((v>2.12)&(v<2.2)); ok=_hash(np.floor(u/1.2),8)<.9; emis=np.where((es&ok)[:,None],np.array(st["strip"],np.float32)[None,:]*.9,0.0)
        col=np.where((es&ok)[:,None],0.0,col)
    elif kind=="stone":
        row=np.floor(v/.32); off=.5*(row%2); cu=u/.64+off; fu=cu-np.floor(cu); fv=v/.32-row; bid=np.floor(cu)*13+row*7
        h=_hash(bid,4); col=base[None,:]*(.7+.5*h)[:,None]*(1+(S(N2,u*2,v*2)-.5)*.28)[:,None]*(1+fn*.2)[:,None]
        mort=(fu<.035)|(fu>.965)|(fv<.07)|(fv>.93); col=np.where(mort[:,None],b2[None,:]*.55,col)
        damp=np.clip(1.3-v,0,1)*np.clip((S(N1,u*.5,v*.5)-.4)*3,0,1); col=col*(1-.3*damp)[:,None]; col[:,1]*=(1+.15*damp)
    elif kind=="panel":
        col=base[None,:]*(1+(S(N2,u*.8,v*.8)-.5)*.1)[:,None]*(1+fn*.08)[:,None]
        dado=v<.9; col=np.where(dado[:,None],b2[None,:]*(1-.1*(((u*6)%1.0)<.07))[:,None],col)
        col=np.where(((v>.9)&(v<1.0))[:,None],np.array((226,128,40),np.float32)[None,:],col); col=np.where(((v>1.0)&(v<1.05))[:,None],np.array((60,44,36),np.float32)[None,:],col)
        pg=((u/.9)%1.0<.02)|((u/.9)%1.0>.98); col=np.where(pg[:,None]&(v>1.05)[:,None],col*.8,col)
    elif kind=="wood":
        fu=(u/.12)%1.0; pid=np.floor(u/.12); h=_hash(pid,5)
        col=base[None,:]*(.8+.4*h)[:,None]*(1+(S(N2,u*.4,v*10)-.5)*.35)[:,None]; col=np.where(((fu<.04))[:,None],col*.5,col)
    elif kind=="concrete":
        col=base[None,:]*(1+(S(N2,u*.7,v*.7)-.5)*.3)[:,None]*(1+fn*.2)[:,None]
        fm=((u/1.2)%1.0<.012)|((v/1.2)%1.0<.012); col=np.where(fm[:,None],col*.7,col)
        stn=np.clip((S(N1,u*.3+1,v*.5)-.55)*5,0,1)*np.clip(1.5-v,0,1); col*=(1-.25*stn)[:,None]
    else: col=np.repeat(base[None,:],n,0)
    return col,emis
def _floor(kind,x,z,st,dist):
    base=np.array(st["fcol"],np.float32); n=x.shape[0]; fn=(S(FINE,x*30,z*30)-.5)*np.exp(-dist/5.0)
    if kind=="wood":
        fu=(x/.14)%1.0; pid=np.floor(x/.14); cut=((z+_hash(pid,6)*1.8)/1.8)%1.0; seg=np.floor((z+_hash(pid,6)*1.8)/1.8)
        h=_hash(pid*5+seg,7); col=base[None,:]*(.78+.45*h)[:,None]*(1+(S(N2,x*.8,z*.15)-.5)*.3)[:,None]*(1+fn*.1)[:,None]
        col=np.where(((fu<.03)|(cut<.006))[:,None],col*.45,col)
    elif kind=="grate":
        fu=(x/.25)%1.0; fv=(z/.25)%1.0; bar=(fu<.14)|(fv<.14); h=_hash(np.floor(x/.25)*3+np.floor(z/.25),2)
        col=np.where(bar[:,None],base[None,:]*(.8+.3*h)[:,None]*(1+fn*.15)[:,None],np.array((6,8,10),np.float32)[None,:])
    elif kind=="flag":
        cu=x/.8; cv=z/.8; iu=np.floor(cu); iv=np.floor(cv); h=_hash(iu*17+iv*5,3); fu=cu-iu; fv=cv-iv
        col=base[None,:]*(.65+.6*h)[:,None]*(1+(S(N2,x*1.8,z*1.8)-.5)*.3)[:,None]*(1+fn*.2)[:,None]
        col=np.where(((fu<.04)|(fv<.04))[:,None],np.array(st["wcol2"],np.float32)[None,:]*.5,col)
    elif kind=="rubber":
        col=base[None,:]*(1+(S(N2,x*1.2,z*1.2)-.5)*.25)[:,None]*(1+fn*.25)[:,None]; sm_=((x/.6)%1.0<.012)|((z/.6)%1.0<.012); col=np.where(sm_[:,None],col*.7,col)
    elif kind=="tile":
        ck=(np.floor(x/.5)+np.floor(z/.5))%2; col=base[None,:]*(.82+.22*ck)[:,None]*(1+fn*.12)[:,None]
        gl=((x/.5)%1.0<.02)|((z/.5)%1.0<.02); col=np.where(gl[:,None],col*.6,col)
    elif kind=="concrete":
        col=base[None,:]*(1+(S(N2,x*.7,z*.7)-.5)*.3)[:,None]*(1+fn*.2)[:,None]
    elif kind=="sand":
        col=base[None,:]*(1+(S(N2,x*.4,z*.4)-.5)*.3)[:,None]*(1+fn*.2)[:,None]
    elif kind=="carpet":
        col=base[None,:]*(1+(S(N2,x*.9,z*.9)-.5)*.25)[:,None]*(1+fn*.3)[:,None]
    else: col=np.repeat(base[None,:],n,0)
    return col
def _ceil(kind,x,z,st,dist):
    base=np.array(st["ccol"],np.float32); n=x.shape[0]; emis=None; fn=(S(FINE,x*26,z*26)-.5)*np.exp(-dist/5.0)
    col=base[None,:]*(1+(S(N2,x*.7,z*.7)-.5)*.14)[:,None]*(1+fn*.1)[:,None]
    if kind=="beams":
        bm=((z/1.5)%1.0<.12); col=np.where(bm[:,None],np.array((70,48,32),np.float32)[None,:]*(.8+.3*S(N3,z*4,x*.5))[:,None],col)
    elif kind=="pipes":
        bm=((z/1.2)%1.0<.08); col=np.where(bm[:,None],col*.6,col)
        for px in (-.55,.0,.6):
            d=np.abs(x-px); pp=np.clip(1-d/.16,0,1); col=np.where((d<.16)[:,None],col*(.4+.9*pp)[:,None]*np.array((1,.98,.95),np.float32)[None,:],col)
    elif kind=="strip":
        stp=(np.abs(x)<.14)&(((z/1.8)%1.0)<.62)
        emis=np.where(stp[:,None],np.array(st["strip"],np.float32)[None,:],0.0); col=np.where(stp[:,None],0.0,col*.7)
    elif kind=="vault":
        col*=.7
    elif kind=="tile":
        tu=(x+.3)/.6; tv=z/.6; fu=tu-np.floor(tu); fv=tv-np.floor(tv); line=(fu<.035)|(fu>.965)|(fv<.035)|(fv>.965); col=np.where(line[:,None],col*.75,col)
    return col,emis
def _lights(xh,yh,zh,st,t,flick,extra):
    Ls=np.zeros((RH,RW,3),np.float32); P=st["plights"]
    if P:
        gap=P["gap"]; off=P.get("off",0.0); kc=np.floor((zh-off)/gap+.5); rgb=np.array(P["rgb"],np.float32)[None,None,:]
        for dk in (-2,-1,0,1,2):
            kk=kc+dk; zk=kk*gap+off
            fl=1.0-P.get("flk",0.0)*((_hash(kk,9)<P.get("flp",.1))&(np.floor(t*9)%3<1.5))*flick
            for xo in P["xs"]:
                xk=xo*np.where(np.mod(kk,2)==0,1.0,-1.0) if P.get("alt") else xo
                d2=(xh-xk)**2+(P["y"]-yh)**2+(zh-zk)**2; Ls+=((fl*P["I"]/(1+P.get("k",.35)*d2))[:,:,None]*rgb).astype(np.float32)
    for (x,y,z,rgb,I) in extra:
        d2=(xh-x)**2+(y-yh)**2+(zh-z)**2; Ls+=((I/(1+.35*d2))[:,:,None]*np.array(rgb,np.float32)[None,None,:]).astype(np.float32)
    return Ls
def render_room(cam,st,t=0.0,flick=1.0,extra=()):
    H=st["H"]; hw=st["hw"]; f=1.0/math.tan(math.radians(st["fov"])/2)
    cx,cy,cz=cam["x"],cam["y"],cam["z"]; yaw=cam.get("yaw",0.0); pit=cam.get("pitch",0.0); roll=cam.get("roll",0.0)
    sx,sy=_SX,_SY
    if roll: sx,sy=sx*math.cos(roll)-sy*math.sin(roll),sx*math.sin(roll)+sy*math.cos(roll)
    dx0,dy0,dz0=sx,sy,np.full_like(sx,f)
    cp,sp=math.cos(pit),math.sin(pit); dy1=dy0*cp-dz0*sp; dz1=dy0*sp+dz0*cp
    cyw,syw=math.cos(yaw),math.sin(yaw); dx=dx0*cyw+dz1*syw; dz=-dx0*syw+dz1*cyw; dy=dy1
    INF=np.float32(1e6)
    with np.errstate(divide="ignore",invalid="ignore"):
        tw=np.where(dx>1e-6,(hw-cx)/dx,np.where(dx<-1e-6,(-hw-cx)/dx,INF)); tw=np.where(tw>0,tw,INF)
        if st["open_p"]>0:
            side=np.where(dx>0,1,-1); zh=cz+tw*dz; yh=cy+tw*dy; seg=st["seg"]; k=np.floor(zh/seg); zl=(zh/seg)-k
            h=_hash(k,0)*.5+_hash(k,1)*.5*(side>0)+_hash(k,2)*.5*(side<0)
            opn=(h<st["open_p"])&(zl>st["open_a"])&(zl<st["open_b"])&(yh<2.15)&(yh>0)&(tw<INF)
            D=st["D"]; tw2=np.where(dx>1e-6,(hw+D-cx)/dx,np.where(dx<-1e-6,(-hw-D-cx)/dx,INF)); tw2=np.where(tw2>0,tw2,INF); tw=np.where(opn,tw2,tw)
        tz=np.full_like(sx,INF)
        if st["zend"] is not None: tzf=np.where(dz>1e-6,(st["zend"]-cz)/dz,INF); tz=np.minimum(tz,np.where(tzf>0,tzf,INF))
        if st["zback"] is not None: tzb=np.where(dz<-1e-6,(st["zback"]-cz)/dz,INF); tz=np.minimum(tz,np.where(tzb>0,tzb,INF))
        tf=np.where(dy<-1e-6,(0-cy)/dy,INF); tc=np.where(dy>1e-6,(H-cy)/dy,INF)
    tf=np.where(tf>0,tf,INF); tc=np.where(tc>0,tc,INF)
    t_=np.minimum(np.minimum(np.minimum(tf,tc),tw),tz)
    isf=(tf<=t_); isc=(~isf)&(tc<=t_); isend=(~isf)&(~isc)&(tz<=t_); isw=~(isf|isc|isend)
    xh=cx+t_*dx; yh=cy+t_*dy; zh=cz+t_*dz
    out=np.zeros((RH,RW,3),np.float32); Ls=_lights(xh,yh,zh,st,t,flick,extra)
    amb=np.array(st["amb_rgb"],np.float32)
    def L3(m): return (st["ambient"]*amb[None,:]+Ls[m])*st["gain"]
    m=isf
    if m.any():
        xs,zs=xh[m],zh[m]; col=_floor(st["floor"],xs,zs,st,t_[m]); Lm=L3(m); out[m]=col*Lm
        if st["sheen"]>0:
            spec=(Lm.mean(1,keepdims=True)**2)*st["sheen"]*np.exp(-t_[m]/12)[:,None]; out[m]+=spec*255*.3
    m=isc
    if m.any():
        xs,zs=xh[m],zh[m]; col,em=_ceil(st["ceil"],xs,zs,st,t_[m]); out[m]=col*L3(m)*.9+(em if em is not None else 0)
    for mm,uu,tgt in ((isw,zh,None),(isend,xh,None)):
        if mm.any():
            u=uu[mm]; v=yh[mm]; col,em=_wall(st["wall"],u,v,st,t_[mm]); out[mm]=col*L3(mm)+(em if em is not None else 0)
    fg=np.exp(-np.minimum(t_,200)*st["fog"])[:,:,None]; fc=np.array(st["fogcol"],np.float32)[None,None,:]
    out=out*fg+fc*(1-fg)
    out=np.clip(out,0,255)
    return Image.fromarray(out.astype(np.uint8)).filter(ImageFilter.GaussianBlur(.6))
