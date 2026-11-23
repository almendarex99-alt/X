"""Calle alpina nevada de noche (motor de rayos numpy): casas con entramado de madera, ventanas con luz, tejados con nieve,
farolillos con pozas de luz calida, cielo estrellado con luna, nieve en el suelo y nieve cayendo. Reutiliza helpers de liminal."""
import math, numpy as np
from PIL import Image, ImageDraw, ImageFilter
from liminal import S,N1,N2,N3,FINE,_hash,RW,RH,_SX,_SY,project,walk_cam,font
STREET=dict(name="street",H=7.5,hw=3.4,seg=7.0,open_p=.35,open_a=.30,open_b=.62,D=6.0,fov=64,gap=7.0,fog=.020,fogcol=(18,26,48),
            ambient=.30,amb_rgb=(.42,.56,1.0),lamp_rgb=(1.0,.64,.32),gain=1.0)
def render_street(cam,st,t=0.0,flick=1.0):
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
        side=np.where(dx>0,1,-1)
        zh=cz+tw*dz; yh=cy+tw*dy
        seg=st["seg"]; k=np.floor(zh/seg); zl=(zh/seg)-k
        h=_hash(k,0)*.5+_hash(k,1)*.5*(side>0)+_hash(k,2)*.5*(side<0)
        opn=(h<st["open_p"])&(zl>st["open_a"])&(zl<st["open_b"])&(yh<4.2)&(yh>0)&(tw<INF)
        D=st["D"]; tw2=np.where(dx>1e-6,(hw+D-cx)/dx,np.where(dx<-1e-6,(-hw-D-cx)/dx,INF)); tw2=np.where(tw2>0,tw2,INF)
        tw=np.where(opn,tw2,tw)
        tf=np.where(dy<-1e-6,(0-cy)/dy,INF); tc=np.where(dy>1e-6,(H-cy)/dy,INF)
    tf=np.where(tf>0,tf,INF); tc=np.where(tc>0,tc,INF)
    t_=np.minimum(np.minimum(tf,tc),tw)
    isf=(tf<=tc)&(tf<=tw); isc=(~isf)&(tc<=tw); isw=~(isf|isc)
    xh=cx+t_*dx; yh=cy+t_*dy; zh=cz+t_*dz
    out=np.zeros((RH,RW,3),np.float32)
    # ---- farolillos ----
    gap=st["gap"]; kc=np.floor(zh/gap+.5); Ls=np.zeros((RH,RW),np.float32)
    for dk in (-2,-1,0,1,2):
        kk=kc+dk; zk=kk*gap; xk=(hw-.45)*np.where(np.mod(kk,2)==0,1.0,-1.0); yk=3.0
        fl=1.0-.45*((_hash(kk,9)<.12)&(np.floor(t*8)%3<1.5))*flick
        d2=(xh-xk)**2+(yk-yh)**2+(zh-zk)**2; Ls+=(fl*1.7/(1+.28*d2)).astype(np.float32)
    amb=np.array(st["amb_rgb"],np.float32); lamp=np.array(st["lamp_rgb"],np.float32)
    def L3(m): return (st["ambient"]*amb[None,:]+Ls[m][:,None]*lamp[None,:])*st["gain"]
    # ---- suelo: nieve con surcos ----
    m=isf
    if m.any():
        xs,zs=xh[m],zh[m]; base=np.array((196,208,236),np.float32)
        bump=S(N2,xs*.5,zs*.5)-.5; col=base[None,:]*(1+bump[:,None]*.26)
        rut=np.exp(-((xs-.95)**2)/.03)+np.exp(-((xs+.95)**2)/.03)+.6*np.exp(-((xs-.15)**2)/.4)
        col*=(1-.17*np.clip(rut,0,1)*(.6+.4*S(N3,zs*1.5,xs*.5)))[:,None]
        edge=np.clip((np.abs(xs)-(hw-1.1))/1.1,0,1); col*=(1+.08*edge)[:,None]
        col*=(1+(S(FINE,xs*40,zs*40)-.5)*.10*np.exp(-t_[m]/6.0))[:,None]
        sp_=(S(FINE,xs*70+3,zs*70)>.987)*np.exp(-t_[m]/16.0)
        Lm=L3(m); out[m]=col*Lm+sp_[:,None]*np.array([255,240,215],np.float32)[None,:]*np.clip(Lm.mean(1,keepdims=True)*1.2,0,1)
    # ---- cielo nocturno ----
    m=isc
    if m.any():
        ddx,ddy,ddz=dx[m],dy[m],dz[m]; n=np.sqrt(ddx**2+ddy**2+ddz**2)+1e-6; e=np.clip(ddy/n,0,1)
        hor=np.array((30,40,74),np.float32); zen=np.array((6,9,24),np.float32)
        col=hor[None,:]*(1-np.clip(e*1.6,0,1))[:,None]+zen[None,:]*np.clip(e*1.6,0,1)[:,None]
        ux,uz=ddx/(ddy+1e-3),ddz/(ddy+1e-3); star=(S(FINE,ux*70+1.1,uz*70)>.9965)*(.5+.5*np.sin(t*3+ux*40))
        col+=star[:,None]*np.array([220,230,255],np.float32)[None,:]*(.5+.5*np.clip(e*2,0,1))[:,None]
        mx,my,mz=.30,.62,.72; mn=math.sqrt(mx*mx+my*my+mz*mz); dot=(ddx*mx+ddy*my+ddz*mz)/n/mn
        col+=(np.exp((dot-1)*260)*60+(dot>.99965)*220)[:,None]*np.array([.92,.95,1.0],np.float32)[None,:]
        out[m]=col
    # ---- paredes: casas alpinas con entramado ----
    m=isw
    if m.any():
        xw,yw,zw=xh[m],yh[m],zh[m]; u=zw; bay=2.8; ub=u/bay; ib=np.floor(ub); fu=ub-ib
        sd=np.where(xw>0,1,-1)
        plaster=np.array((208,194,162),np.float32); stone=np.array((132,126,118),np.float32); beam=np.array((70,46,30),np.float32)
        col=np.repeat(plaster[None,:],xw.shape[0],0)*(1+(S(N2,u*.6,yw*.6)-.5)*.28)[:,None]
        col=np.where((yw<.75)[:,None],stone[None,:]*(1+(S(N3,u*2,yw*2)-.5)*.3)[:,None],col)
        post=(fu<.045)|(fu>.955); beam_h=((yw>2.82)&(yw<3.02))|((yw>5.26)&(yw<5.46))|((yw>.75)&(yw<.85))
        col=np.where((post|beam_h)[:,None],beam[None,:]*(1+(S(N3,u*6,yw*1.2)-.5)*.4)[:,None],col)
        # contraventanas
        for lo,hi in((.215,.30),(.70,.785)):
            sh=(fu>lo)&(fu<hi)&(((yw>1.3)&(yw<2.35))|((yw>3.55)&(yw<4.6)))
            col=np.where(sh[:,None],np.array((74,102,64),np.float32)[None,:]*(.85+.3*((fu*60)%1.0>.5))[:,None],col)
        # ventanas
        emis=np.zeros_like(col)
        for lo_y,hi_y,fl in((1.3,2.35,0),(3.55,4.6,1)):
            win=(fu>.30)&(fu<.70)&(yw>lo_y)&(yw<hi_y)
            lit=_hash(ib*7+fl*3+sd*11,4)<.58
            wy=(yw-lo_y)/(hi_y-lo_y); wx=(fu-.30)/.40
            frame=(wx<.07)|(wx>.93)|(wy<.07)|(wy>.93)|(np.abs(wx-.5)<.03)|(np.abs(wy-.5)<.025)
            glow=np.array((255,196,112),np.float32)[None,:]*(.80+.2*np.sin(u*3+t*2.0+ib))[:,None]
            ecol=np.where((win&lit&~frame)[:,None],glow*(.7+.5*wy[:,None]),0.0)
            emis+=ecol
            dark=np.array((20,28,44),np.float32)[None,:]*(1+.5*wy)[:,None]
            col=np.where((win&~lit&~frame)[:,None],dark,col)
            col=np.where((win&frame)[:,None],beam[None,:]*.9,col)
            col=np.where((win&lit&~frame)[:,None],0.0,col)
            led=(fu>.27)&(fu<.73)&(yw>lo_y-.1)&(yw<lo_y-.01)
            col=np.where(led[:,None],np.array((232,238,250),np.float32)[None,:],col)
        # tejado con nieve
        roof=yw>5.6
        tile=np.array((66,46,44),np.float32)[None,:]*(.8+.2*((yw*9)%1.0>.5))[:,None]
        col=np.where(roof[:,None],tile,col); col=np.where((yw>6.85)[:,None],np.array((236,242,252),np.float32)[None,:],col)
        col=np.where(((yw>5.2)&(yw<5.6))[:,None],col*.78,col)
        col*=(1+(S(FINE,u*20,yw*20)-.5)*.1*np.exp(-t_[m]/6.0))[:,None]
        Lm=L3(m)*(.8+.2*np.minimum(np.abs(xw)/hw,1.0))[:,None]
        out[m]=col*Lm+emis
    # ---- niebla ----
    fg=np.exp(-np.minimum(t_,200)*st["fog"])[:,:,None]; fc=np.array(st["fogcol"],np.float32)[None,None,:]
    out=out*fg+fc*(1-fg)
    out=np.clip(out,0,255)
    return Image.fromarray(out.astype(np.uint8)).filter(ImageFilter.GaussianBlur(.7))
def lamp_pos(cam,st):
    gap=st["gap"]; hw=st["hw"]; kc=math.floor(cam["z"]/gap)
    res=[]
    for kk in range(kc-1,kc+6):
        res.append(((hw-.45)*(1 if kk%2==0 else -1),3.0,kk*gap))
    return res
def lamp_glow(img,cam,st,t=0.0):
    f=1.0/math.tan(math.radians(st["fov"])/2); k=f*RW/2
    ov=Image.new("RGBA",img.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    for (x,y,z) in lamp_pos(cam,st):
        x1,y2,z2=project(cam,(x,y,z))
        if z2<.6: continue
        px=RW/2+x1/z2*k; py=RH/2-y2/z2*k; r=.28*k/z2; fl=.85+.15*math.sin(t*7+z)
        for q in range(7): rr=r*(5.0-q*.7); d.ellipse([px-rr,py-rr,px+rr,py+rr],fill=(255,170,80,int(14*fl)))
        d.rectangle([px-r*.45,py-r*.8,px+r*.45,py+r*.55],fill=(40,30,24,255)); d.rectangle([px-r*.3,py-r*.6,px+r*.3,py+r*.4],fill=(255,214,140,255)); d.polygon([(px-r*.5,py-r*.8),(px,py-r*1.3),(px+r*.5,py-r*.8)],fill=(30,24,20,255))
    ov=ov.filter(ImageFilter.GaussianBlur(2.0))
    return Image.alpha_composite(img.convert("RGBA"),ov).convert("RGB")
def snowfall(img,t,n=330,wind=1.0,seed=3,scale=1.0):
    rng=np.random.default_rng(seed); W,Hh=img.size
    xs=rng.random(n); ys=rng.random(n); sz=rng.random(n)**2.0
    ov=Image.new("RGBA",img.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    for i in range(n):
        r=(1.0+sz[i]*5.0)*scale; sp=(40+sz[i]*160)*scale
        x=(xs[i]*W+t*wind*(20+sz[i]*30)+math.sin(t*1.7+i)*12)%W; y=(ys[i]*Hh+t*sp)%Hh
        d.ellipse([x-r,y-r,x+r,y+r],fill=(240,246,255,int(120+110*sz[i])))
    ov=ov.filter(ImageFilter.GaussianBlur(.7))
    return Image.alpha_composite(img.convert("RGBA"),ov).convert("RGB")
def place(cam,st,xw,zw,hm=1.9):
    """proyecta un punto del suelo a coordenadas logicas 540x960 y escala de personaje (alto de persona = 232*sc)"""
    x1,y2,z2=project(cam,(xw,0.0,zw))
    if z2<.6: return None
    f=1.0/math.tan(math.radians(st["fov"])/2); k=f*RW/2
    px=RW/2+x1/z2*k; py=RH/2-y2/z2*k; ph=hm*k/z2
    return px/RW*540, py/RH*960, (ph/RH*960)/232.0, z2
def fade_style(style,k,fog=(22,30,52)):
    """mezcla los colores del estilo con la niebla segun la distancia (k=1 cerca, 0 lejos)"""
    out={}
    for key,v in style.items():
        if isinstance(v,tuple) and len(v)==3 and all(isinstance(c,(int,float)) for c in v): out[key]=tuple(int(c*k+fog[i]*(1-k)*.8) for i,c in enumerate(v))
        else: out[key]=v
    return out
