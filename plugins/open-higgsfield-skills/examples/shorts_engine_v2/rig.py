"""Rig 2D articulado: cuerpo completo con cuello, cabeza, pelo, orejas, brazos (hombro-codo-mano), manos con 5 dedos de 2 falanges,
piernas (cadera-rodilla-tobillo-pie). Todo se calcula con cinematica directa para que cada pieza quede unida a la anterior."""
import math
from core import *

def _rotv(v,t):
    c,s=math.cos(t),math.sin(t); return (v[0]*c-v[1]*s,v[0]*s+v[1]*c)
def shade(c,k): return tuple(max(0,min(255,int(v*k))) for v in c[:3])

SKIN=(236,190,150)
BASE=dict(skin=SKIN,hair=(60,40,28),hairstyle="short",shirt=(70,110,170),shirt2=None,pants=(50,56,76),shoes=(30,28,32),
          sleeve="long",dress=False,skirt_col=None,hat=None,glasses=False,beard=False,brow=(40,28,20),eyes=(40,30,24),
          bulk=1.0,claws=False,horns=False,tail=None,hands_col=None,mask=None,coat=None,belt=None,bust=False,mouth_col=(150,70,70),
          neck_col=None,cap_col=None,face=True,ear=True,height=1.0)

# ---------------- poses ----------------
def P_idle(u,ph=0.0):
    b=math.sin(u*2.0+ph)
    return dict(al=(.10+.02*b,.16),ar=(.10-.02*b,.16),ll=(.05,.05),lr=(.05,.05),bob=b*1.2,tilt=.03*math.sin(u*1.3+ph),look=(math.sin(u*.9+ph)*.5,0),mouth=0)
def P_walk(u,speed=3.2,ph=0.0):
    w=math.sin(u*speed+ph); c=math.cos(u*speed+ph)
    return dict(al=(.10+.18*w,.2+.25*max(0,w)),ar=(.10-.18*w,.2+.25*max(0,-w)),ll=(.07+.10*c,.05+.85*max(0,-c)),lr=(.07-.10*c,.05+.85*max(0,c)),bob=abs(c)*3,tilt=.04*w,look=(0,0),mouth=0,lean=.03*w)
def P_talk(u,ph=0.0):
    b=math.sin(u*2.0+ph); g=math.sin(u*3.1+ph)
    return dict(al=(.12+.03*b,.2),ar=(.55+.25*g,2.0+.3*math.sin(u*4.2+ph)),ll=(.05,.05),lr=(.05,.05),bob=b*1.2,tilt=.05*math.sin(u*1.7+ph),look=(0,0),mouth=.5+.5*math.sin(u*9+ph),curlR=.2,spreadR=.9)
def P_wave(u,ph=0.0):
    w=math.sin(u*6+ph)
    return dict(al=(.10,.16),ar=(2.2+.1*w,2.6+.4*w),ll=(.05,.05),lr=(.05,.05),bob=0,tilt=.05*w,look=(0,0),mouth=.6,spreadR=1.0)
def P_point(u,ph=0.0,dirx=1.0):
    return dict(al=(.10,.16),ar=(1.45,1.5),ll=(.05,.05),lr=(.05,.05),bob=math.sin(u*2)*1,tilt=.02,look=(.6*dirx,0),mouth=.4,pointR=True)
def P_hold(u,ph=0.0,r=(1.1,2.4),l=None,grip=1.0):
    b=math.sin(u*2.0+ph)
    return dict(al=l or (.10,.16),ar=r,ll=(.05,.05),lr=(.05,.05),bob=b*1.1,tilt=.03*math.sin(u+ph),look=(0,0),mouth=0,curlR=grip,curlL=grip if l else .3)
def P_both(u,ph=0.0,l=(1.0,2.3),r=(1.0,2.3),grip=1.0):
    b=math.sin(u*2.0+ph)
    return dict(al=l,ar=r,ll=(.05,.05),lr=(.05,.05),bob=b*1.1,tilt=0,look=(0,0),mouth=0,curlL=grip,curlR=grip,hands_front=True)
def P_zombie(u,ph=0.0,speed=2.2):
    w=math.sin(u*speed+ph); c=math.cos(u*speed+ph)
    return dict(al=(.75+.08*w,2.3),ar=(.75-.08*w,2.3),ll=(.05+.2*c,.05+.3*max(0,-c)),lr=(.05-.2*c,.05+.3*max(0,c)),bob=abs(c)*2,tilt=.12+.04*w,look=(0,0),mouth=.8,lean=.1,curlL=.5,curlR=.5,spreadL=1.0,spreadR=1.0,hands_front=True)
def P_cheer(u,ph=0.0):
    w=math.sin(u*5+ph)
    return dict(al=(2.5+.15*w,2.8),ar=(2.5-.15*w,2.8),ll=(.12,.12),lr=(.12,.12),bob=abs(w)*3,tilt=0,look=(0,0),mouth=1.0,spreadL=1.0,spreadR=1.0)
def P_scared(u,ph=0.0):
    t=math.sin(u*14+ph)*.02
    return dict(al=(.7,2.3),ar=(.7,2.3),ll=(.12,.1),lr=(.12,.1),bob=math.sin(u*11)*1.2,tilt=.04+t,look=(.4,0),mouth=1.0,curlL=.3,curlR=.3,spreadL=1.0,spreadR=1.0,hands_front=True)

# ---------------- manos ----------------
def hand(d,wx,wy,a,s,sc,skin,curl=.3,spread=.6,claws=False,prop=None,sleeve_col=None,point=False,rot=0.0):
    """muneca en (wx,wy); a = angulo del antebrazo respecto a la vertical (0 abajo); s=-1 izq, +1 der"""
    v=(s*math.sin(a),math.cos(a)); n=(-v[1],v[0]); pl=9*sc
    cx,cy=wx+v[0]*pl*.9,wy+v[1]*pl*.9
    d.E(wx,wy,5.2*sc,5.2*sc,skin+(255,))
    if prop: prop(d,cx,cy,a,s)
    pw=6.2*sc
    d.P([(wx+n[0]*pw*.9,wy+n[1]*pw*.9),(wx-n[0]*pw*.9,wy-n[1]*pw*.9),(cx-n[0]*pw+v[0]*pl*.4,cy-n[1]*pw+v[1]*pl*.4),(cx+n[0]*pw+v[0]*pl*.4,cy+n[1]*pw+v[1]*pl*.4)],skin+(255,))
    d.E(cx+v[0]*2*sc,cy+v[1]*2*sc,pw*1.05,pl*.55,skin+(255,))
    fl=[(10.5,8.5),(12.5,10),(11.5,9),(8.5,7)]
    cols=skin
    for i in range(4):
        off=(i-1.5)
        base=(cx+n[0]*off*pw*.62+v[0]*pl*.5,cy+n[1]*off*pw*.62+v[1]*pl*.5)
        ang=(off*.22*spread)*s*-1
        c1=curl*1.0; c2=curl*1.4
        if point and i>0: c1,c2=1.4,1.8
        if point and i==0: c1,c2=0,0
        d1=_rotv(v,ang+ (c1*.9)*s*-1*-1)  # primera falange
        L1,L2=fl[i][0]*sc*(1-.3*c1),fl[i][1]*sc*(1-.3*c1)
        p1=(base[0]+d1[0]*L1,base[1]+d1[1]*L1)
        d2=_rotv(v,ang+(c1*.9+c2*1.1)*s*-1*-1)
        p2=(p1[0]+d2[0]*L2,p1[1]+d2[1]*L2)
        for (a0,b0) in ((base,p1),(p1,p2)): d.L(a0[0],a0[1],b0[0],b0[1],skin+(255,),3.6*sc); d.E(b0[0],b0[1],1.8*sc,1.8*sc,skin+(255,))
        d.L(base[0]+(p1[0]-base[0])*.5,base[1]+(p1[1]-base[1])*.5,base[0]+(p1[0]-base[0])*.5,base[1]+(p1[1]-base[1])*.5,shade(skin,.8)+(255,),1)
        d.E(p1[0],p1[1],.7*sc,.7*sc,shade(skin,.8)+(200,))
        if claws:
            tip=(p2[0]+d2[0]*7*sc,p2[1]+d2[1]*7*sc); d.P([(p2[0]+n[0]*1.8*sc,p2[1]+n[1]*1.8*sc),(p2[0]-n[0]*1.8*sc,p2[1]-n[1]*1.8*sc),tip],(236,230,214))
    # pulgar
    tb=(cx-n[0]*pw*1.0*(-1)+v[0]*pl*.1,cy-n[1]*pw*1.0*(-1)+v[1]*pl*.1)
    ta=_rotv(v,s*.75*(1-curl*.4)*-1*-1*-1)
    t1=(tb[0]+ta[0]*7*sc,tb[1]+ta[1]*7*sc); ta2=_rotv(v,s*(.55+curl*.8)*-1*-1*-1); t2=(t1[0]+ta2[0]*6*sc,t1[1]+ta2[1]*6*sc)
    # el pulgar siempre sale del lado interior (hacia el cuerpo)
    inner=-s
    tb=(cx+n[0]*pw*.9*inner*(1 if n[0]*inner>=0 else 1),cy+n[1]*pw*.9*inner)
    tb=(cx+(-s)*pw*.95*abs(n[0])*1.0+0,cy+n[1]*pw*.2)
    ta=_rotv(v,(-s)*-(.7-.3*curl)); t1=(tb[0]+ta[0]*7*sc,tb[1]+ta[1]*7*sc)
    ta2=_rotv(v,(-s)*-(.4-.7*curl)); t2=(t1[0]+ta2[0]*6*sc,t1[1]+ta2[1]*6*sc)
    d.L(tb[0],tb[1],t1[0],t1[1],skin+(255,),4*sc); d.L(t1[0],t1[1],t2[0],t2[1],skin+(255,),3.4*sc); d.E(t2[0],t2[1],1.8*sc,1.8*sc,skin+(255,))
    return (cx,cy)

# ---------------- persona ----------------
def person(d,x,y,sc=1.0,u=0.0,pose=None,style=None,facing="front",rot=0.0,props=None,deco=None,back_deco=None,alpha=255):
    """(x,y)=suelo bajo los pies. Devuelve dict con puntos de articulaciones (manos, cabeza...)."""
    st=dict(BASE); st.update(style or {}); po=pose or P_idle(u)
    skin=st["skin"]; hc=st["hair"]; H=st["height"]
    leg=48*sc*H; hipy=y-leg*2-6*sc*H
    bob=po.get("bob",0)*sc; lean=po.get("lean",0)+rot
    bk=st["bulk"]; hw=13*sc*bk; sw=24*sc*bk*(1+.015*math.sin(u*2))
    tors=70*sc*H
    cx,cy=x,hipy-bob      # centro de cadera
    def T(px,py):
        if lean==0: return (px,py)
        dx,dy=px-cx,py-(hipy); r=_rotv((dx,dy),lean); return (cx+r[0],hipy+r[1])
    sh_c=T(cx,cy-tors); sy=sh_c[1]; sx=sh_c[0]
    tilt=po.get("tilt",0)+lean
    neck=T(cx,cy-tors-3*sc);
    head_c=(neck[0]+math.sin(tilt)*26*sc,neck[1]-math.cos(tilt)*(24*sc+12*sc))
    out={}
    # ---- detras ----
    if back_deco: back_deco(d,head_c[0],head_c[1],sc)
    hs=st["hairstyle"]; hx,hy=head_c
    if hs in("long","bob","ponytail","braid","bun"):
        sway=math.sin(u*2.2)*3*sc
        if hs=="long":
            d.P([(hx-23*sc,hy-6*sc),(hx+23*sc,hy-6*sc),(sx+34*sc+sway,sy+40*sc),(sx+10*sc+sway,sy+64*sc),(sx-10*sc+sway,sy+64*sc),(sx-34*sc+sway,sy+40*sc)],hc+(255,))
            d.E(hx,hy-6*sc,24*sc,28*sc,hc+(255,))
        elif hs=="bob":
            d.E(hx,hy-2*sc,26*sc,30*sc,hc+(255,)); d.R(hx-26*sc,hy-4*sc,hx+26*sc,hy+24*sc,hc+(255,),8*sc)
        elif hs=="ponytail":
            d.E(hx,hy-4*sc,23*sc,27*sc,hc+(255,))
            px=hx+(14*sc)*(1 if facing=="back" else -1)*0+0
            d.P([(hx-6*sc,hy-24*sc),(hx+6*sc,hy-24*sc),(hx+16*sc+sway*2,hy+34*sc),(hx+4*sc+sway*2,hy+60*sc),(hx-10*sc+sway*2,hy+34*sc)],hc+(255,))
        elif hs=="braid":
            d.E(hx,hy-4*sc,23*sc,27*sc,hc+(255,))
            for k in range(7): d.E(hx+(k%2*6-3)*sc+sway*(k/6),hy+18*sc+k*11*sc,7*sc,6*sc,shade(hc,1.1 if k%2 else .85)+(255,))
        elif hs=="bun":
            d.E(hx,hy-4*sc,23*sc,27*sc,hc+(255,)); d.E(hx,hy-34*sc,12*sc,11*sc,hc+(255,))
    # tail de criatura
    if st["tail"]:
        tw=math.sin(u*2.5)*10*sc
        d.P([(cx-6*sc,cy-6*sc),(cx+6*sc,cy-6*sc),(cx+34*sc+tw,cy+26*sc),(cx+60*sc+tw*2,cy+14*sc),(cx+40*sc+tw,cy+40*sc),(cx+4*sc,cy+10*sc)],st["tail"]+(255,))
    # ---- piernas ----
    pants=st["pants"]; shoes=st["shoes"]
    if not st["bust"]:
        if st["dress"]:
            sk=st["skirt_col"] or st["shirt"]
            d.P([T(cx-hw*1.4,cy-4*sc),T(cx+hw*1.4,cy-4*sc),T(cx+hw*3.6+math.sin(u*2)*2*sc,y-26*sc),T(cx-hw*3.6+math.sin(u*2)*2*sc,y-26*sc)],sk+(255,))
            d.P([T(cx-hw*1.4,cy-4*sc),T(cx,cy-4*sc),T(cx+hw*.4,y-26*sc),T(cx-hw*3.6,y-26*sc)],shade(sk,.88)+(255,))
            for sgn,key in((-1,"ll"),(1,"lr")):
                tt,ss=po.get(key,(.05,.05)); ax=cx+sgn*hw*.9+sgn*math.sin(tt)*(leg*.9)
                d.L(ax,y-leg*1.1,ax,y-9*sc,skin+(255,),7*sc); d.E(ax,y-6*sc,8*sc,4.5*sc,shoes+(255,))
        else:
            for sgn,key in((-1,"ll"),(1,"lr")):
                tt,ss=po.get(key,(.05,.05))
                hp=T(cx+sgn*hw*.9,cy); kn=(hp[0]+sgn*math.sin(tt)*leg,hp[1]+math.cos(tt)*leg)
                ang2=tt-ss*1.0*(1)  # la espinilla vuelve hacia la vertical
                an=(kn[0]+sgn*math.sin(ang2)*leg,kn[1]+math.cos(ang2)*leg)
                d.L(hp[0],hp[1],kn[0],kn[1],pants+(255,),12*sc*bk); d.E(kn[0],kn[1],6*sc*bk,6*sc*bk,pants+(255,)); d.E(hp[0],hp[1],7*sc*bk,7*sc*bk,pants+(255,))
                d.L(kn[0],kn[1],an[0],an[1],shade(pants,.92)+(255,),10*sc*bk); d.E(an[0],an[1],5*sc*bk,5*sc*bk,shade(pants,.92)+(255,))
                d.E(an[0]+sgn*4*sc,an[1]+3*sc,9.5*sc,4.8*sc,shoes+(255,)); d.E(an[0]+sgn*6*sc,an[1]+1.5*sc,6*sc,3*sc,shade(shoes,1.5)+(120,))
    # ---- torso ----
    shirt=st["shirt"]; tw_top=sw; tw_bot=hw*1.15
    top=T(cx,cy-tors)
    pts=[T(cx-tw_top,cy-tors+4*sc),T(cx-tw_top*.95,cy-tors+10*sc),T(cx-tw_bot*1.25,cy-8*sc),T(cx-tw_bot*1.1,cy+4*sc),T(cx+tw_bot*1.1,cy+4*sc),T(cx+tw_bot*1.25,cy-8*sc),T(cx+tw_top*.95,cy-tors+10*sc),T(cx+tw_top,cy-tors+4*sc),T(cx+tw_top*.6,cy-tors-4*sc),T(cx-tw_top*.6,cy-tors-4*sc)]
    d.P(pts,shirt+(255,))
    d.E(*T(cx-tw_top*.9,cy-tors+8*sc),9*sc,9*sc,shirt+(255,)); d.E(*T(cx+tw_top*.9,cy-tors+8*sc),9*sc,9*sc,shirt+(255,))
    if st["shirt2"]:
        n=7
        for k in range(n):
            if k%2:
                y0=cy-tors+6*sc+k*(tors-10*sc)/n; y1=y0+(tors-10*sc)/n
                f0=(y0-(cy-tors))/tors; f1=(y1-(cy-tors))/tors
                w0=tw_top*(1-f0)+tw_bot*1.2*f0; w1=tw_top*(1-f1)+tw_bot*1.2*f1
                d.P([T(cx-w0,y0),T(cx+w0,y0),T(cx+w1,y1),T(cx-w1,y1)],st["shirt2"]+(255,))
    if st["coat"]:
        cc=st["coat"]; d.P([T(cx-tw_top,cy-tors+6*sc),T(cx-4*sc,cy-tors+4*sc),T(cx-8*sc,cy+30*sc),T(cx-tw_bot*1.8,cy+30*sc)],cc+(255,)); d.P([T(cx+tw_top,cy-tors+6*sc),T(cx+4*sc,cy-tors+4*sc),T(cx+8*sc,cy+30*sc),T(cx+tw_bot*1.8,cy+30*sc)],shade(cc,.9)+(255,))
    if st["belt"]: d.P([T(cx-tw_bot*1.2,cy-8*sc),T(cx+tw_bot*1.2,cy-8*sc),T(cx+tw_bot*1.15,cy+1*sc),T(cx-tw_bot*1.15,cy+1*sc)],st["belt"]+(255,))
    # ---- cuello ----
    d.R(neck[0]-6.5*sc,neck[1]-14*sc,neck[0]+6.5*sc,neck[1]+8*sc,(st["neck_col"] or shade(skin,.92))+(255,),3*sc)
    d.P([(neck[0]-10*sc,neck[1]+6*sc),(neck[0]+10*sc,neck[1]+6*sc),(neck[0],neck[1]+18*sc)],shade(skin,.86)+(255,)) if not st["coat"] and not st["dress"] else None
    # ---- brazos ----
    def arm(sgn,key,ck,sk,hold):
        a1,a2=po.get(key,(.1,.16)); shp=T(cx+sgn*(sw*.95),cy-tors+8*sc)
        u1=(sgn*math.sin(a1),math.cos(a1)); el=(shp[0]+u1[0]*40*sc*H,shp[1]+u1[1]*40*sc*H)
        u2=(sgn*math.sin(a2),math.cos(a2)); wr=(el[0]+u2[0]*36*sc*H,el[1]+u2[1]*36*sc*H)
        sleeve=shirt if st["sleeve"]!="none" else skin
        d.L(shp[0],shp[1],el[0],el[1],sleeve+(255,),12*sc*bk); d.E(el[0],el[1],6*sc*bk,6*sc*bk,sleeve+(255,)); d.E(shp[0],shp[1],7*sc*bk,7*sc*bk,sleeve+(255,))
        if st["sleeve"]=="short":
            d.L(shp[0],shp[1],shp[0]+(el[0]-shp[0])*.55,shp[1]+(el[1]-shp[1])*.55,shirt+(255,),12.5*sc); d.L(shp[0]+(el[0]-shp[0])*.5,shp[1]+(el[1]-shp[1])*.5,el[0],el[1],skin+(255,),10*sc)
        d.L(el[0],el[1],wr[0],wr[1],shade(sleeve,.96)+(255,) if st["sleeve"]!="short" else skin+(255,),10.5*sc*bk)
        if st["sleeve"]!="short": d.E(wr[0],wr[1],5.5*sc,5.5*sc,shade(sleeve,.9)+(255,))
        hp=hand(d,wr[0],wr[1],a2,sgn,sc,st["hands_col"] or skin,curl=po.get(ck,.25),spread=po.get(sk,.6),claws=st["claws"],prop=(props or {}).get("l" if sgn<0 else "r"),point=po.get("pointR",False) and sgn>0)
        out["hand_l" if sgn<0 else "hand_r"]=hp; out["wrist_l" if sgn<0 else "wrist_r"]=wr; out["elbow_l" if sgn<0 else "elbow_r"]=el
    hands_front=po.get("hands_front",False)
    if not hands_front:
        arm(-1,"al","curlL","spreadL",None); arm(1,"ar","curlR","spreadR",None)
    # ---- cabeza ----
    rx,ry=21*sc*H,24*sc*H
    if facing=="back":
        d.E(hx,hy,rx,ry,hc+(255,))
    else:
        d.E(hx,hy,rx,ry,skin+(255,)); d.E(hx-6*sc,hy-8*sc,10*sc,8*sc,(255,255,255,34))
        if st["ear"]:
            for sg in(-1,1): d.E(hx+sg*(rx-.5*sc),hy+2*sc,4.2*sc,6*sc,shade(skin,.96)+(255,)); d.E(hx+sg*(rx-.5*sc),hy+2*sc,2*sc,3.4*sc,shade(skin,.8)+(255,))
        # cara
        lk=po.get("look",(0,0)); mo=po.get("mouth",0); blink=(math.sin(u*1.7+x)>.985)
        if st["face"]:
            for sg in(-1,1):
                ex=hx+sg*8.5*sc; ey=hy-3*sc
                if blink: d.L(ex-4*sc,ey,ex+4*sc,ey,(30,20,20),1.6*sc)
                else:
                    d.E(ex,ey,5.2*sc,4.4*sc,(250,250,250)); d.E(ex+lk[0]*1.8*sc,ey+lk[1]*1.5*sc,2.7*sc,2.7*sc,st["eyes"]+(255,)); d.E(ex+lk[0]*1.8*sc,ey+lk[1]*1.5*sc,1.3*sc,1.3*sc,(8,8,10)); d.E(ex+lk[0]*1.8*sc-.9*sc,ey-1*sc,.8*sc,.8*sc,(255,255,255))
                d.L(ex-5*sc,ey-7*sc-(mo>.8)*1.5*sc,ex+5*sc,ey-7.6*sc+(mo>.8)*(-1.2*sc),st["brow"]+(255,),1.8*sc)
                if st["glasses"]: d.E(ex,ey,7.4*sc,6.6*sc,None,(30,30,36),1.4*sc)
            if st["glasses"]: d.L(hx-1.1*sc,hy-3*sc,hx+1.1*sc,hy-3*sc,(30,30,36),1.2*sc)
            d.L(hx,hy-1*sc,hx-1.5*sc,hy+6*sc,shade(skin,.8)+(255,),1.6*sc); d.L(hx-1.5*sc,hy+6*sc,hx+1.5*sc,hy+6*sc,shade(skin,.8)+(255,),1.4*sc)
            my=hy+13*sc
            if mo>.25: d.E(hx,my,(4+3*mo)*sc,(1.6+4*mo)*sc,(60,20,26)); d.E(hx,my-.4*sc,(3+2*mo)*sc,1.1*sc,(250,250,250,200)) if mo>.5 else None
            else: d.A(hx,my-2*sc,6*sc,3.4*sc,20,160,st["mouth_col"]+(255,),1.6*sc)
            if st["beard"]: d.P([(hx-rx*.9,hy+4*sc),(hx+rx*.9,hy+4*sc),(hx+rx*.6,hy+ry*1.1),(hx,hy+ry*1.3),(hx-rx*.6,hy+ry*1.1)],shade(hc,.9)+(230,))
        if st["mask"]: st["mask"](d,hx,hy,sc)
    # ---- pelo delante ----
    if hs!="bald" and facing!="back":
        if hs in("short","bun","ponytail","braid","bob","long"):
            d.P([(hx-rx*1.02,hy+2*sc),(hx-rx*1.0,hy-8*sc),(hx-rx*.6,hy-ry*1.1),(hx,hy-ry*1.2),(hx+rx*.6,hy-ry*1.1),(hx+rx*1.0,hy-8*sc),(hx+rx*1.02,hy+2*sc),(hx+rx*.82,hy-8*sc),(hx+rx*.4,hy-14*sc),(hx-rx*.1,hy-12*sc),(hx-rx*.6,hy-10*sc),(hx-rx*.82,hy-6*sc)],hc+(255,))
            d.E(hx-6*sc,hy-ry*1.0,8*sc,3*sc,(255,255,255,26))
        if hs=="long" or hs=="bob":
            for sg in(-1,1): d.R(hx+sg*rx-4*sc,hy-6*sc,hx+sg*rx+4*sc,hy+20*sc+(8*sc if hs=="long" else 0),hc+(255,),4*sc)
    if facing=="back" and hs=="short": d.E(hx,hy-4*sc,rx*1.02,ry*1.0,hc+(255,))
    if st["horns"]:
        for sg in(-1,1): d.P([(hx+sg*10*sc,hy-ry*1.0),(hx+sg*26*sc,hy-ry*1.9),(hx+sg*18*sc,hy-ry*.9)],(236,228,206))
    hat=st["hat"]
    if hat=="fedora": d.E(hx,hy-14*sc,38*sc,9*sc,(124,92,60,255)); d.R(hx-22*sc,hy-44*sc,hx+22*sc,hy-14*sc,(130,96,64),7*sc); d.R(hx-22*sc,hy-22*sc,hx+22*sc,hy-16*sc,(70,40,34),0); d.E(hx,hy-12*sc,38*sc,9*sc,None,(0,0,0,50),1)
    elif hat=="cap": d.P([(hx-rx*1.05,hy-6*sc),(hx-rx*.6,hy-ry*1.5),(hx+rx*.6,hy-ry*1.5),(hx+rx*1.05,hy-6*sc)],st["cap_col"] or (40,150,60)+()); d.R(hx-rx*1.0,hy-14*sc,hx+rx*1.0,hy-8*sc,shade(st["cap_col"] or (40,150,60),.8)+(255,),2*sc)
    elif hat=="greencap": d.P([(hx-rx*1.08,hy-4*sc),(hx-rx*.8,hy-ry*1.3),(hx,hy-ry*2.2),(hx+rx*.8,hy-ry*1.2),(hx+rx*1.4,hy+12*sc),(hx+rx*1.0,hy-4*sc)],(40,150,60)); d.R(hx-rx*1.08,hy-14*sc,hx+rx*1.08,hy-6*sc,(255,214,120),2*sc)
    elif hat=="crown": d.P([(hx-16*sc,hy-ry*1.1),(hx-12*sc,hy-ry*1.9),(hx-5*sc,hy-ry*1.3),(hx,hy-ry*2.0),(hx+5*sc,hy-ry*1.3),(hx+12*sc,hy-ry*1.9),(hx+16*sc,hy-ry*1.1)],(255,214,70))
    elif hat=="headphones": d.A(hx,hy-6*sc,rx*1.1,ry*1.2,180,360,(40,40,46),3*sc); [d.E(hx+sg*rx*1.05,hy+1*sc,6*sc,9*sc,(40,40,46)) for sg in(-1,1)]
    elif hat=="hood": d.E(hx,hy-6*sc,rx*1.3,ry*1.3,None,st["shirt"]+(255,),7*sc)
    elif hat=="headband": d.R(hx-rx*1.0,hy-12*sc,hx+rx*1.0,hy-8*sc,(255,214,70),1*sc)
    if deco: deco(d,hx,hy,sc)
    if hands_front:
        arm(-1,"al","curlL","spreadL",None); arm(1,"ar","curlR","spreadR",None)
    out.update(head=head_c,neck=neck,shoulder=(sx,sy),hip=(cx,cy),feet=(x,y))
    return out
