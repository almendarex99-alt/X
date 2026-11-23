"""Objetos 3D sobre las imagenes de fondo: cajas con caras sombreadas, poligonos, cuadrilateros con textura en perspectiva
(pantallas, carteles, papeles), y casas. Todo se proyecta con la misma camara del fondo para que encaje en perspectiva."""
import math, numpy as np
from PIL import Image, ImageDraw, ImageFilter
from liminal import project,RW,RH
def _k(st): return (1.0/math.tan(math.radians(st["fov"])/2))*RW/2
def pj(cam,st,p):
    x1,y2,z2=project(cam,p)
    if z2<.08: return None
    k=_k(st); return (RW/2+x1/z2*k, RH/2-y2/z2*k, z2)
def shd(c,k): return tuple(max(0,min(255,int(v*k))) for v in c[:3])
def new_ov(): return Image.new("RGBA",(RW,RH),(0,0,0,0))
def poly3(ov,cam,st,pts,col,alpha=255,outline=None):
    P=[pj(cam,st,p) for p in pts]
    if any(q is None for q in P): return
    d=ImageDraw.Draw(ov); d.polygon([(q[0],q[1]) for q in P],fill=tuple(col[:3])+(alpha,),outline=outline)
def box(ov,cam,st,x0,x1,y0,y1,z0,z1,col,lt=(1,1,1),emis=0.0,edge=None,light_dir=(-.35,.8,-.5),shadow=True,tops=None):
    """caja alineada a ejes; dibuja solo las caras visibles, de atras a delante, con sombreado simple"""
    c3=(x0+x1)/2,(y0+y1)/2,(z0+z1)/2
    faces=[((0,-1,0),[(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)]),((0,1,0),[(x0,y1,z0),(x1,y1,z0),(x1,y1,z1),(x0,y1,z1)]),
           ((-1,0,0),[(x0,y0,z0),(x0,y1,z0),(x0,y1,z1),(x0,y0,z1)]),((1,0,0),[(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)]),
           ((0,0,-1),[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0)]),((0,0,1),[(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)])]
    L=np.array(light_dir,float); L/=np.linalg.norm(L); d=ImageDraw.Draw(ov)
    if shadow and y0<=.05:
        sh=[pj(cam,st,p) for p in ((x0-.12,.0,z0-.1),(x1+.18,.0,z0-.1),(x1+.18,.0,z1+.12),(x0-.12,.0,z1+.12))]
        if all(sh):
            s=Image.new("RGBA",ov.size,(0,0,0,0)); ImageDraw.Draw(s).polygon([(q[0],q[1]) for q in sh],fill=(0,0,0,90)); s=s.filter(ImageFilter.GaussianBlur(5)); ov.alpha_composite(s)
            d=ImageDraw.Draw(ov)
    vis=[]
    for n,pts in faces:
        fc=np.mean(np.array(pts),0); to=np.array((cam["x"],cam["y"],cam["z"]))-fc
        if np.dot(n,to)>0:
            pp=[pj(cam,st,p) for p in pts]
            if any(q is None for q in pp): continue
            dist=np.linalg.norm(to); vis.append((dist,n,pp))
    vis.sort(key=lambda r:-r[0])
    for dist,n,pp in vis:
        sh=.42+.58*max(0.0,float(np.dot(n,L))); cc=tuple(int(max(0,min(255,col[i]*lt[i]*sh+emis*255))) for i in range(3))
        if tops is not None and n==(0,1,0): cc=tuple(tops)
        d.polygon([(q[0],q[1]) for q in pp],fill=cc+(255,),outline=(edge or shd(cc,.7))+(255,))
def tquad(ov,cam,st,p0,p1,p2,p3,tex,alpha=1.0):
    """textura en perspectiva: p0=arriba-izq, p1=arriba-der, p2=abajo-der, p3=abajo-izq (puntos 3D)"""
    P=[pj(cam,st,p) for p in (p0,p1,p2,p3)]
    if any(q is None for q in P): return
    dst=[(q[0],q[1]) for q in P]; w,h=tex.size; src=[(0,0),(w,0),(w,h),(0,h)]
    A=[];B=[]
    for (X,Y),(u,v) in zip(dst,src): A.append([X,Y,1,0,0,0,-u*X,-u*Y]); A.append([0,0,0,X,Y,1,-v*X,-v*Y]); B+= [u,v]
    try: co=np.linalg.solve(np.array(A,float),np.array(B,float))
    except np.linalg.LinAlgError: return
    t=tex.convert("RGBA");
    if alpha<1: a=t.split()[3].point(lambda v:int(v*alpha)); t.putalpha(a)
    warped=t.transform((RW,RH),Image.PERSPECTIVE,tuple(co),Image.BICUBIC)
    mask=Image.new("L",(RW,RH),0); ImageDraw.Draw(mask).polygon(dst,fill=255)
    ov.alpha_composite(Image.composite(warped,Image.new("RGBA",(RW,RH),(0,0,0,0)),mask))
def glow(ov,cam,st,p,rgb,r_m=.5,a=60,layers=6):
    q=pj(cam,st,p)
    if not q: return
    k=_k(st); r=r_m*k/q[2]; g=Image.new("RGBA",ov.size,(0,0,0,0)); d=ImageDraw.Draw(g)
    for i in range(layers): rr=r*(1+i*.7); d.ellipse([q[0]-rr,q[1]-rr,q[0]+rr,q[1]+rr],fill=tuple(rgb)+(int(a/(1+i*.3)/3),))
    ov.alpha_composite(g.filter(ImageFilter.GaussianBlur(3)))
def composite(img,ov): return Image.alpha_composite(img.convert("RGBA"),ov).convert("RGB")
def house(ov,cam,st,x,z,w=7.0,d=6.0,h=3.2,wall=(190,176,150),roof=(70,50,50),lit=0.6,rot=0,t=0.0,porch=True,seed=1):
    """casa suburbana con tejado a dos aguas, puerta, ventanas iluminadas y luz de porche; el frente mira al eje x (hacia la calle)"""
    s=-1 if x>0 else 1; xf=x-s*d/2; xb=x+s*d/2; z0,z1=z-w/2,z+w/2
    box(ov,cam,st,min(xf,xb),max(xf,xb),0,h,z0,z1,wall,shadow=True)
    rh=h+1.9; ridge=z
    # tejado: dos faldones
    for (za,zb) in ((z0-.4,ridge),(z1+.4,ridge)):
        poly3(ov,cam,st,[(min(xf,xb)-.35,h,za),(max(xf,xb)+.35,h,za),(max(xf,xb)+.35,rh,zb),(min(xf,xb)-.35,rh,zb)],shd(roof,.9 if za<z else .7))
    # frontones
    for xx in (xf,xb): poly3(ov,cam,st,[(xx,h,z0),(xx,h,z1),(xx,rh,z)],shd(wall,.85))
    rnd=np.random.default_rng(seed)
    for j in range(2):
        zc=z0+w*(.28+.44*j); on=rnd.random()<lit
        col=(255,198,108) if on else (24,30,44)
        poly3(ov,cam,st,[(xf-s*.02,1.0,zc-.6),(xf-s*.02,1.0,zc+.6),(xf-s*.02,2.2,zc+.6),(xf-s*.02,2.2,zc-.6)],shd(col,.55+.45*(.8+.2*math.sin(t*3+j))) if on else col)
        poly3(ov,cam,st,[(xf-s*.03,1.6,zc-.6),(xf-s*.03,1.6,zc+.6),(xf-s*.03,1.63,zc+.6),(xf-s*.03,1.63,zc-.6)],(60,44,32)); poly3(ov,cam,st,[(xf-s*.03,1.0,zc-.03),(xf-s*.03,2.2,zc-.03),(xf-s*.03,2.2,zc+.03),(xf-s*.03,1.0,zc+.03)],(60,44,32))
    poly3(ov,cam,st,[(xf-s*.02,0,z-.45),(xf-s*.02,0,z+.45),(xf-s*.02,2.1,z+.45),(xf-s*.02,2.1,z-.45)],(70,44,34))
    if porch: glow(ov,cam,st,(xf-s*.3,2.3,z+.9),(255,196,110),.5,70)
