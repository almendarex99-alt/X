"""Motor 3D por trazado de rayos (numpy) para espacios liminales: pasillos, salas y tuneles con texturas procedurales
(papel pintado, moqueta humeda, techo de placas con fluorescentes), iluminacion con caida, parpadeo, niebla y sombras de entidades."""
import math, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
RW,RH=720,1280
_ys,_xs=np.mgrid[0:RH,0:RW]; _SX=((_xs-RW/2)/(RW/2)).astype(np.float32); _SY=(-(_ys-RH/2)/(RW/2)).astype(np.float32)
def _noise(seed,n=512,octaves=5):
    rng=np.random.default_rng(seed); acc=np.zeros((n,n),np.float32); amp=1.0; tot=0.0
    for o in range(octaves):
        s=2**(o+2); g=rng.random((s,s)).astype(np.float32)
        im=Image.fromarray((g*255).astype(np.uint8)).resize((n,n),Image.BICUBIC); acc+=np.asarray(im,np.float32)/255*amp; tot+=amp; amp*=.55
    return acc/tot
N1=_noise(1); N2=_noise(2,octaves=6); N3=_noise(3,octaves=4)
FINE=np.random.default_rng(7).random((512,512)).astype(np.float32)
def S(tex,u,v): return tex[(v*512).astype(np.int64)&511,(u*512).astype(np.int64)&511]
def _hash(a,b=0):
    h=(a.astype(np.int64)*73856093) ^ (np.int64(b)*19349663) ^ (a.astype(np.int64)*83492791)
    return ((h&0xFFFF)/65535.0).astype(np.float32)

YELLOW=dict(name="yellow",H=2.75,hw=1.7,seg=6.0,open_p=.55,open_a=.25,open_b=.62,D=5.0,fov=64,
  wall=(200,180,100),wall2=(188,168,90),floor=(132,112,64),ceil=(228,224,198),panel=(255,252,226),base=(92,70,40),
  light_gap=3.6,fog=.026,fogcol=(60,52,22),ambient=.30,gain=1.0,damp=True,stripe=.16,panel_cols=(0,),wallpaper=True)
OFFICE=dict(YELLOW,name="office",gain=.8,H=2.7,hw=3.2,open_p=.0,wall=(232,232,236),wall2=(222,224,230),floor=(96,102,116),ceil=(236,238,242),panel=(235,245,255),base=(150,150,156),fog=.02,fogcol=(70,76,90),ambient=.30,damp=False,stripe=0.0,wallpaper=False)
WIDE=dict(YELLOW,name="wide",hw=7.0,open_p=0.0,fov=70,panel_cols=(-2,0,2),fog=.03,gain=.62,ambient=.22)
CONCRETE=dict(YELLOW,name="concrete",H=2.3,hw=3.2,open_p=.4,wall=(150,150,146),wall2=(138,138,134),floor=(96,96,92),ceil=(130,130,126),panel=(255,190,110),base=(70,70,68),fog=.04,fogcol=(30,26,20),ambient=.22,damp=True,stripe=0.0,wallpaper=False,gain=1.4)
TUNNEL=dict(YELLOW,name="tunnel",H=2.3,hw=1.0,open_p=.0,wall=(92,98,104),wall2=(80,86,92),floor=(70,72,70),ceil=(82,86,90),panel=(255,90,70),base=(50,54,58),fog=.07,fogcol=(14,10,10),ambient=.14,damp=True,stripe=0.0,wallpaper=False,gain=1.3)

def render(cam,st,t=0.0,flick=1.0):
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
        opn=(h<st["open_p"])&(zl>st["open_a"])&(zl<st["open_b"])&(yh<2.15)&(yh>0)&(tw<INF)
        D=st["D"]; tw2=np.where(dx>1e-6,(hw+D-cx)/dx,np.where(dx<-1e-6,(-hw-D-cx)/dx,INF)); tw2=np.where(tw2>0,tw2,INF)
        tw=np.where(opn,tw2,tw)
        tf=np.where(dy<-1e-6,(0-cy)/dy,INF); tc=np.where(dy>1e-6,(H-cy)/dy,INF)
    tf=np.where(tf>0,tf,INF); tc=np.where(tc>0,tc,INF)
    t_=np.minimum(np.minimum(tf,tc),tw)
    isf=(tf<=tc)&(tf<=tw); isc=(~isf)&(tc<=tw); isw=~(isf|isc)
    xh=cx+t_*dx; yh=cy+t_*dy; zh=cz+t_*dz
    out=np.zeros((RH,RW,3),np.float32)
    # ---- iluminacion: fluorescentes a lo largo del pasillo ----
    gap=st["light_gap"]; kc=np.floor((zh-.6)/gap+.5); I=np.full((RH,RW),st["ambient"],np.float32)
    for dk in (-1,0,1):
        kk=kc+dk; zk=kk*gap+.6
        fl=1.0-.9*((_hash(kk,5)<.10)&(np.floor(t*9)%3<1.5))*flick
        for cxl in st["panel_cols"]:
            d2=(xh-cxl*1.2)**2+(H-yh)**2+(zh-zk)**2; I+=(fl*1.5/(1+.55*d2)).astype(np.float32)
    I*=st["gain"]*flick**.3
    # ---- suelo: moqueta ----
    m=isf
    if m.any():
        xs,zs=xh[m],zh[m]; base=np.array(st["floor"],np.float32)
        mott=S(N2,xs*.9,zs*.9)-.5; col=base[None,:]*(1+mott[:,None]*.38)
        fn=(S(FINE,xs*22,zs*22)-.5)*np.exp(-t_[m]/5.0); col*=(1+fn[:,None]*.34)
        if st["damp"]:
            patch=np.clip((S(N1,xs*.22+.3,zs*.22)-.55)*7,0,1); col*=(1-.32*patch[:,None])
            col[:,2]*=(1-.1*patch)
        tile=((xs/.5)%1.0<.015)|((zs/.5)%1.0<.015); col*=np.where(tile,.9,1.0)[:,None]
        Ic=I[m]; spec=np.exp(-((xs)**2*.25+((zs-.6+gap/2)%gap-gap/2)**2*.5))*.16*np.exp(-t_[m]/20)
        out[m]=col*Ic[:,None]+spec[:,None]*255*np.array([1,.97,.8],np.float32)[None,:]*np.clip(Ic[:,None],0,1)
    # ---- techo: placas y fluorescentes ----
    m=isc
    if m.any():
        xs,zs=xh[m],zh[m]; tu=(xs+.3)/.6; tv=zs/.6; iu=np.floor(tu).astype(np.int64); iv=np.floor(tv).astype(np.int64)
        fu=tu-iu; fv=tv-iv; line=(fu<.035)|(fu>.965)|(fv<.035)|(fv>.965)
        base=np.array(st["ceil"],np.float32); col=np.repeat(base[None,:],xs.shape[0],0)
        fn=(S(FINE,xs*30,zs*30)-.5)*np.exp(-t_[m]/5.0)
        col*=(.93+(S(N3,xs*1.7,zs*1.7)-.5)*.12+fn*.2)[:,None]; col*=np.where(line,.72,1.0)[:,None]
        pan=np.zeros(xs.shape,bool)
        for cc in st["panel_cols"]: pan|=((iu==int(cc*2))&((iv%6)<2))
        grille=((fu*8)%1.0<.12)&pan
        Ic=I[m]; kkp=np.floor(zs/gap)
        fl=1.0-.9*((_hash(kkp,5)<.10)&(np.floor(t*9)%3<1.5))*flick
        pc=np.array(st["panel"],np.float32)
        col=np.where(pan[:,None],pc[None,:]*(1.2*fl)[:,None]*np.where(grille,.9,1.0)[:,None],col*np.clip(Ic*.8,0,1.2)[:,None])
        out[m]=col
    # ---- paredes: papel pintado ----
    m=isw
    if m.any():
        xw,yw,zw=xh[m],yh[m],zh[m]; u=np.where(np.abs(xw)>hw+.1,zw,zw); u=zw
        base=np.array(st["wall"],np.float32); b2=np.array(st["wall2"],np.float32)
        if st["wallpaper"]:
            ph=(u/st["stripe"])%2.0; stripe=np.where(ph<1.0,0.0,1.0)
            col=base[None,:]*(1-stripe[:,None]*.07)+b2[None,:]*(stripe[:,None]*.07)
            damask=.5+.5*np.cos(2*np.pi*u/(st["stripe"]*2)); col*=(1-.025*damask)[:,None]
        else: col=np.repeat(base[None,:],xw.shape[0],0)*(1+(S(N2,zw*.7,yw*.7)-.5)*.2)[:,None]
        fn=(S(FINE,u*20,yw*20)-.5)*np.exp(-t_[m]/5.0); col*=(1+fn[:,None]*.3)
        if st["damp"]:
            stn=np.clip((S(N1,u*.4+2,yw*.9)-.56)*6,0,1)*np.clip(1.4-yw,0,1); col*=(1-.3*stn[:,None]); col[:,2]*=(1-.15*stn)
            col*=(1-.12*np.clip(1-yw/.35,0,1))[:,None]
        bb=np.array(st["base"],np.float32); col=np.where((yw<.11)[:,None],bb[None,:]*(.9+.2*S(N3,u*3,yw*3))[:,None],col)
        col=np.where(((yw>.11)&(yw<.125))[:,None],col*.7,col)
        col=np.where((yw>H-.085)[:,None],np.array(st["ceil"],np.float32)[None,:]*.96,col)
        col=np.where(((yw>H-.1)&(yw<H-.085))[:,None],col*.75,col)
        Ic=I[m]*(.82+.18*np.minimum(np.abs(xw),1)); out[m]=col*Ic[:,None]
    # ---- niebla / profundidad ----
    fg=np.exp(-np.minimum(t_,200)*st["fog"])[:,:,None]; fc=np.array(st["fogcol"],np.float32)[None,None,:]
    out=out*fg+fc*(1-fg)*np.clip(I[:,:,None]*.6,0,1)
    out=np.clip(out,0,255)
    # pequeno desenfoque de lente + corrección tonal
    img=Image.fromarray(out.astype(np.uint8)).filter(ImageFilter.GaussianBlur(.6))
    return img
def project(cam,p):
    cx,cy,cz=cam["x"],cam["y"],cam["z"]; yaw=cam.get("yaw",0.0); pit=cam.get("pitch",0.0)
    dx,dy,dz=p[0]-cx,p[1]-cy,p[2]-cz
    cyw,syw=math.cos(-yaw),math.sin(-yaw); x1=dx*cyw+dz*syw; z1=-dx*syw+dz*cyw; y1=dy
    cp,sp=math.cos(-pit),math.sin(-pit); y2=y1*cp-z1*sp; z2=y1*sp+z1*cp
    return x1,y2,z2
def entity(img,cam,st,xw,zw,h=2.3,col=(8,7,4),a=235,lean=0.0,t=0.0,walk=0.0,arms=1.0):
    """silueta alta y delgada (extremidades largas) proyectada en 3D sobre el pasillo"""
    f=1.0/math.tan(math.radians(st["fov"])/2); k=f*RW/2
    def P(x,y,z):
        x1,y2,z2=project(cam,(x,y,z))
        if z2<.3: return None
        return (RW/2+x1/z2*k, RH/2-y2/z2*k)
    ov=Image.new("RGBA",img.size,(0,0,0,0)); d=ImageDraw.Draw(ov); c=col+(a,)
    s=h/2.3
    def seg(p,q,w):
        pa=P(*p); pb=P(*q)
        if pa and pb:
            z2=project(cam,(xw,1,zw))[2]; wpx=max(1.0,w*k/z2); d.line([pa,pb],fill=c,width=int(wpx)); d.ellipse([pa[0]-wpx/2,pa[1]-wpx/2,pa[0]+wpx/2,pa[1]+wpx/2],fill=c); d.ellipse([pb[0]-wpx/2,pb[1]-wpx/2,pb[0]+wpx/2,pb[1]+wpx/2],fill=c)
    sw=math.sin(walk); sway=lean+.03*math.sin(t*1.3)
    hip=(xw+sway*.2,1.05*s,zw); sh=(xw+sway,1.82*s,zw); hd=(xw+sway*1.3,2.02*s,zw)
    seg(hip,sh,.30*s); seg(sh,hd,.08*s)
    pa=P(*hd);
    if pa:
        z2=project(cam,(xw,1,zw))[2]; r=.11*s*k/z2; d.ellipse([pa[0]-r*.85,pa[1]-r*1.15,pa[0]+r*.85,pa[1]+r*1.15],fill=c)
    for sg in(-1,1):
        el=(xw+sway+sg*.24*s,1.28*s+.05*sg*sw*.5,zw+.05*arms); wr=(xw+sway+sg*.26*s,.74*s,zw+.08*sg*sw*arms)
        seg((xw+sway+sg*.18*s,1.78*s,zw),el,.06*s); seg(el,wr,.05*s)
        seg(wr,(wr[0],wr[1]-.2*s,wr[2]),.035*s)
        lk=(xw+sg*.1*s,.55*s,zw+.15*sg*sw); an=(xw+sg*.12*s+.02,0.06*s,zw+.25*sg*sw)
        seg((xw+sg*.09*s,1.05*s,zw),lk,.11*s); seg(lk,an,.08*s)
    ov=ov.filter(ImageFilter.GaussianBlur(1.1))
    img.paste(Image.alpha_composite(img.convert("RGBA"),ov).convert("RGB"))
    return img
def walk_cam(t,speed=1.1,x0=0.0,z0=0.0,y0=1.62,yaw0=0.0,sway=1.0):
    step=t*speed*1.9
    return dict(x=x0+math.sin(step*.5)*.05*sway,y=y0+abs(math.sin(step))*.035*sway,z=z0+t*speed,yaw=yaw0+math.sin(t*.7)*.02*sway+math.sin(t*2.1)*.004,pitch=-.01+math.sin(step)*.006*sway,roll=math.sin(step*.5)*.006*sway)
def font(sz,bold=False):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf"%("-Bold" if bold else ""),sz)
def camcorder_overlay(img,t,rec=True,date="OCT 14 1998",extra=True):
    d=ImageDraw.Draw(img); W,Hh=img.size
    f=font(34,True)
    if rec and int(t*1.4)%2==0: d.ellipse([46,60,78,92],fill=(235,30,30))
    d.text((92,56),"REC",font=f,fill=(240,240,240)); d.text((46,Hh-120),date,font=font(30),fill=(240,240,240))
    s=int(t)%60; d.text((W-250,Hh-120),"00:%02d:%02d"%((int(t)//60)%60,s),font=font(30),fill=(240,240,240))
    d.rectangle([W-120,60,W-50,90],outline=(240,240,240),width=3); d.rectangle([W-122,70,W-116,80],fill=(240,240,240)); d.rectangle([W-114,64,W-84,86],fill=(240,240,240))
    d.text((W/2-30,Hh-160),"SP",font=font(26),fill=(240,240,240))
    # esquinas del visor
    for (x,y,sx_,sy_) in((30,30,1,1),(W-30,30,-1,1),(30,Hh-30,1,-1),(W-30,Hh-30,-1,-1)):
        d.line([(x,y),(x+sx_*50,y)],fill=(240,240,240),width=3); d.line([(x,y),(x,y+sy_*50)],fill=(240,240,240),width=3)
    return img
def vhs(img,t,amount=1.0):
    a=np.asarray(img).astype(np.float32); h,w,_=a.shape; rng=np.random.default_rng(int(t*30)+5)
    # canal cromatico desplazado y sangrado de color horizontal
    a[:,:,0]=np.roll(a[:,:,0],int(3*amount),axis=1); a[:,:,2]=np.roll(a[:,:,2],-int(3*amount),axis=1)
    a=a*.9+np.roll(a,2,axis=1)*.1
    # lineas de barrido
    a[::3]*=0.9; a=a+rng.normal(0,7*amount,a.shape[:2])[:,:,None]
    # banda de seguimiento (tracking) que sube
    y=int((h-(t*220)%h)); band=slice(max(0,y-26),min(h,y+26)); a[band]=np.roll(a[band],int(18*amount*math.sin(t*20)),axis=1)*.85+rng.normal(0,28,a[band].shape[:2])[:,:,None]
    return Image.fromarray(np.clip(a,0,255).astype(np.uint8))
