import sys,io; sys.path.insert(0,"..")
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import core
from core import clamp, sm
from alpine import *
from kramp import *
from rig import *
from art import ptext
OUTSZ=(1620,2880)
def fin(img): return img.resize(OUTSZ,Image.BICUBIC)
def flick(u): return 1.0 if (math.sin(u*37)*math.sin(u*11.3+1.7))<.93 else .6
def grade(img,sat=.95,grain=3.5,seed=0,tint=(0.98,1.0,1.04)):
    a=np.asarray(img).astype(np.float32); g=a.mean(2,keepdims=True); a=g+(a-g)*sat
    a=a*np.array(tint,np.float32)[None,None,:]
    a=a+np.random.default_rng(seed).normal(0,grain,a.shape[:2])[:,:,None]
    return Image.fromarray(np.clip(a,0,255).astype(np.uint8))
def serif(sz,bold=True): return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif%s.ttf"%("-Bold" if bold else ""),sz)
def street_big(cam,t,st=STREET,fl=1.0,snow=260):
    im=render_street(cam,st,t,fl); im=lamp_glow(im,cam,st,t)
    if snow: im=snowfall(im,t,n=snow)
    return fin(im)
def P(d,cam,st,xw,zw,style,pose,hm=1.8,u=0.0,**kw):
    pl=place(cam,st,xw,zw,hm)
    if not pl: return None
    lx,ly,sc,z2=pl; k=math.exp(-z2*.020)
    return person(d,lx,ly,sc,u,pose,fade_style(style,k),**kw)
def kr_pose(u,ph=0.0,rod=False):
    po=dict(P_walk(u,2.1,ph)); po.update(al=(.28+.12*math.sin(u*2.1+ph),.5),ar=(.34-.12*math.sin(u*2.1+ph),.6),curlL=.9,curlR=.9,mouth=1.0,spreadL=1.0,spreadR=1.0)
    if rod: po.update(ar=(2.1+.15*math.sin(u*5),2.5))
    return po
# ---------------- escena 0 / 7: Krampus avanza por la calle ----------------
def sceneA(u,final=False):
    KT[0]=u; t=u+(0 if not final else 4); st=dict(STREET,fov=52)
    cam=walk_cam(t,speed=.6); cam["pitch"]=.10+cam["pitch"]
    big=street_big(cam,t,st,flick(u)); d=D(big)
    zd=(11.5-min(u,6.5)*.85) if not final else (6.2-min(u,5)*.4)
    P(d,cam,st,.45+.25*math.sin(u*.8),cam["z"]+zd,KR,kr_pose(u),hm=2.0,u=u,props={"l":chain_prop,"r":rods_prop},deco=kdeco,back_deco=basket_back)
    big=snowfall(big,t*1.3,n=70,scale=2.4,seed=9)
    return grade(big,seed=int(u*30))
# ---------------- escena 1: mapa de los Alpes ----------------
_PARCH=None
def parchment():
    global _PARCH
    if _PARCH is None:
        n=np.random.default_rng(4); W,Hh=RW,RH
        yy,xx=np.mgrid[0:Hh,0:W]; base=np.array((224,202,152),np.float32)
        a=np.zeros((Hh,W,3),np.float32)+base
        nz=np.asarray(Image.fromarray((n.random((24,18))*255).astype(np.uint8)).resize((W,Hh),Image.BICUBIC),np.float32)/255
        a*=(.88+nz[:,:,None]*.22)
        e=np.minimum(np.minimum(xx,W-xx),np.minimum(yy,Hh-yy)); a*=np.clip(.55+e/110.0,0,1)[:,:,None]
        a=a+n.normal(0,3,(Hh,W))[:,:,None]
        im=Image.fromarray(np.clip(a,0,255).astype(np.uint8))
        d=ImageDraw.Draw(im,"RGBA")
        regs={"BAVIERA":[(.10,.06),(.92,.06),(.92,.30),(.62,.34),(.36,.33),(.10,.30)],
              "AUSTRIA":[(.20,.36),(.38,.34),(.62,.35),(.92,.33),(.92,.50),(.70,.55),(.50,.52),(.30,.53),(.20,.48)],
              "ESLOVENIA":[(.60,.58),(.90,.56),(.92,.72),(.70,.76),(.58,.68)],
              "ITALIA":[(.10,.56),(.50,.55),(.56,.70),(.40,.84),(.10,.80)],
              "SUIZA":[(.03,.34),(.17,.34),(.17,.52),(.10,.60),(.03,.55)]}
        X0,Y0,WW,HH=40,150,640,980
        cols={"BAVIERA":(196,170,120),"AUSTRIA":(206,150,108),"ESLOVENIA":(190,176,124),"ITALIA":(200,184,130),"SUIZA":(204,176,140)}
        for nm,pts in regs.items():
            P_=[(X0+x*WW,Y0+y*HH) for x,y in pts]; d.polygon(P_,fill=cols[nm]+(255,)); d.line(P_+[P_[0]],fill=(90,60,36,255),width=4)
        for k in range(46):
            mx=X0+(.18+n.random()*.7)*WW; my=Y0+(.36+n.random()*.40)*HH; s=10+n.random()*16
            d.polygon([(mx,my-s),(mx-s*.8,my+s*.5),(mx+s*.8,my+s*.5)],fill=(120,96,70,200)); d.polygon([(mx,my-s),(mx+s*.2,my-s*.1),(mx-s*.25,my-s*.1)],fill=(246,246,240,230))
        f=font(30,True)
        for nm,(x,y) in {"BAVIERA":(.50,.18),"AUSTRIA":(.56,.45),"ESLOVENIA":(.74,.66),"ITALIA":(.32,.69),"SUIZA":(.09,.43)}.items():
            d.text((X0+x*WW,Y0+y*HH),nm,font=f if nm!="SUIZA" else font(18,True),fill=(70,40,22,255),anchor="mm")
        d.rectangle([60,60,660,130],fill=(150,52,40,255)); d.text((360,95),"LOS ALPES",font=serif(42),fill=(244,226,176,255),anchor="mm")
        cx,cy=590,1180
        for q in range(4):
            a=q*math.pi/2; d.polygon([(cx+math.cos(a)*50,cy+math.sin(a)*50),(cx+math.cos(a+.3)*12,cy+math.sin(a+.3)*12),(cx+math.cos(a-.3)*12,cy+math.sin(a-.3)*12)],fill=(80,50,30,255))
        d.text((cx,cy-66),"N",font=font(26,True),fill=(70,40,22,255),anchor="mm")
        _PARCH=im
    return _PARCH
def sceneB(u):
    KT[0]=u
    img=Image.new("RGB",(RW,RH),(40,26,16)); a=np.asarray(img).astype(np.float32); nn=np.random.default_rng(2).random((1,RW)); a*=(.8+np.asarray(Image.fromarray((np.random.default_rng(3).random((40,6))*255).astype(np.uint8)).resize((RW,RH),Image.BICUBIC),np.float32)[:,:,None]/255*.6); img=Image.fromarray(np.clip(a,0,255).astype(np.uint8))
    img.paste(parchment(),(0,0)); big=fin(img); d=D(big)
    pts=[(200,250),(190,360),(160,470)]  # AUSTRIA? aprox en logico (540x960)
    spots=[(.50*640+40,.18*980+150),(.56*640+40,.45*980+150),(.74*640+40,.66*980+150)]
    L=[(x*540/RW,y*960/RH) for x,y in spots]
    ph=u/1.8; idx=min(2,int(ph)); fr=ph-int(ph)
    for i,(lx,ly) in enumerate(L):
        if i<=idx and u>.2:
            pu=1+.15*math.sin(u*6+i); sc=.5*pu
            for k in range(3): d.E(lx,ly,26+k*8+4*math.sin(u*4),26+k*8+4*math.sin(u*4),None,(180,40,30,130-k*35),2)
            for sg in(-1,1):
                from kramp import _horn
                _horn(d,lx,ly-6*sc,sc*.55,sg,col=(236,228,200))
            krampus_face(d,lx,ly,sc*.55)
    # mano que senala cada region
    tx,ty=L[idx]; ox,oy=lerp_pt((300,900),(tx+10,ty+40),sm(fr*1.4)) if False else (tx+16,ty+44)
    sx0=380+90*math.sin(u*.4); 
    d.L(sx0,1000,ox,oy+36,(196,150,120,255),28); d.L(sx0,1000,ox,oy+36,(60,60,70,255),30) if False else None
    d.L(sx0+8,1010,ox+4,oy+40,(70,90,120,255),34); d.L(ox+4+(sx0+8-ox-4)*.18,oy+40+(1010-oy-40)*.18,ox+4,oy+40,(236,190,150,255),26)
    hand(d,ox,oy+30,3.0+.02*math.sin(u*3),1,1.5,(236,190,150),curl=.4,spread=.5,point=True)
    # luz de vela
    ov=Image.new("RGBA",big.size,(0,0,0,0)); od=ImageDraw.Draw(ov); fl=.9+.1*math.sin(u*9)
    for k in range(10): r=1700-k*150; od.ellipse([420-r,2500-r,420+r,2500+r],fill=(255,170,70,int(6*fl)))
    od.rectangle([0,0,1620,2880],fill=(0,0,0,40))
    big=Image.alpha_composite(big.convert("RGBA"),ov).convert("RGB")
    return grade(big,sat=1.0,grain=3,seed=int(u*30),tint=(1.03,1.0,.94))
def lerp_pt(a,b,t): return (a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t)
# ---------------- escena 2: 5 de diciembre ----------------
def sceneC(u):
    KT[0]=u; st=dict(STREET,fov=48); cam=dict(x=0.1,y=1.45,z=0.0+u*.06,yaw=.04*math.sin(u*.5),pitch=.06)
    big=street_big(cam,u+7,st,flick(u)); 
    pl=Image.new("RGBA",big.size,(0,0,0,0)); pd=ImageDraw.Draw(pl)
    pd.rounded_rectangle([200,690,1420,880],radius=18,fill=(112,72,40,255)); pd.rounded_rectangle([200,690,1420,880],radius=18,outline=(60,38,22,255),width=8)
    for k in range(7): pd.line([(210,712+k*24),(1410,706+k*24)],fill=(88,56,32,140),width=3)
    pd.text((810,785),"5 DIC · KRAMPUSNACHT",font=serif(70),fill=(246,226,170,255),anchor="mm")
    for (x,y) in((226,716),(1394,716),(226,854),(1394,854)): pd.ellipse([x-9,y-9,x+9,y+9],fill=(40,40,44,255))
    big=Image.alpha_composite(big.convert("RGBA"),pl).convert("RGB"); d=D(big)
    P(d,cam,st,.9,5.4,KR,kr_pose(u,1.0,rod=True),hm=2.0,u=u,props={"l":chain_prop,"r":rods_prop},deco=kdeco,back_deco=basket_back)
    pose_n=dict(P_idle(u),al=(1.1,2.0),ar=(.12,.2),curlL=.4,mouth=.5)
    P(d,cam,st,-.75,3.1,NIC,pose_n,hm=1.8,u=u,props={"l":gift_prop,"r":crozier_prop},deco=mitre_deco)
    P(d,cam,st,.0,2.7,KIDA,dict(P_cheer(u),al=(1.9,2.4),ar=(1.7,2.4)),hm=1.25,u=u)
    P(d,cam,st,.95,3.0,KIDB,dict(P_scared(u),mouth=1.0),hm=1.2,u=u)
    big=snowfall(big,u*1.3,n=70,scale=2.4,seed=9)
    return grade(big,seed=int(u*30))
# ---------------- escena 3: rasgos de Krampus ----------------
def sceneD(u):
    KT[0]=u; st=dict(STREET,fov=44); cam=dict(x=.1*math.sin(u*.4),y=1.5,z=0.0,yaw=.03*math.sin(u*.5),pitch=.05)
    big=street_big(cam,u+3,st,flick(u*.8)); d=D(big)
    po=kr_pose(u,0); po.update(al=(.9,1.3),ar=(.55,.9))
    o=P(d,cam,st,0.0,3.3,KR,po,hm=2.0,u=u,props={"l":chain_prop,"r":rods_prop},deco=kdeco,back_deco=basket_back)
    big=snowfall(big,u*1.3,n=60,scale=2.4,seed=9); d=D(big)
    if o:
        hd=o["head"]; hl=o["hand_l"]; hr=o["hand_r"]
        items=[(.8,"CUERNOS",(hd[0]+30,hd[1]-60),(60,200)),(1.8,"LENGUA LARGA",(hd[0]+6,hd[1]+34),(300,300)),(2.8,"CADENAS",(hl[0]-4,hl[1]+50),(40,640)),(3.8,"RAMAS DE ABEDUL",(hr[0],hr[1]-60),(280,150))]
        for (t0,txt,tgt,pos) in items:
            a=clamp((u-t0)/.5)
            if a<=0: continue
            lx,ly=pos; w=len(txt)*4*3.2+24
            d.R(lx-6,ly-8,lx+w,ly+30,(10,10,16,int(180*a)),8); ptext(d,lx+6,ly,txt,3.2,(255,230,150),int(255*a))
            d.L(lx+w/2,ly+30 if ly<tgt[1] else ly-8,tgt[0],tgt[1],(255,230,150,int(220*a)),1.6); d.E(tgt[0],tgt[1],4,4,(255,230,150,int(255*a)))
    return grade(big,seed=int(u*30))
# ---------------- escena 4: Krampuslauf ----------------
def sceneE(u):
    KT[0]=u; st=dict(STREET,fov=54); cam=dict(x=0.0,y=1.5,z=0.0,yaw=.0,pitch=.08)
    big=street_big(cam,u+11,st,flick(u)); d=D(big)
    runs=[(-.9,(150,100,58),(70,46,32),"rods"),(.95,(120,86,60),(40,34,32),"torch"),(0.05,(170,120,66),(92,70,50),"chain"),(-1.7,(140,96,56),(56,40,30),"torch"),(1.75,(160,108,62),(84,56,38),"rods")]
    items=[]
    for i,(x,mc,fur,kind) in enumerate(runs):
        z=21-clamp((u-i*.25)/4.3)*17.8-(i%2)*1.2
        items.append((z,x,i,mc,fur,kind))
    for j,(x,z0,stl) in enumerate(((-2.7,6,KIDA),(2.7,7,KIDB),(-2.8,11,KIDB),(2.8,12,KIDA))): items.append((z0,x,100+j,None,None,stl))
    items.sort(key=lambda r:-r[0])
    for (z,x,i,mc,fur,kind) in items:
        if i>=100:
            P(d,cam,st,x,z,kind,dict(P_scared(u+i)),hm=1.25,u=u+i); continue
        stl=runner(mc,fur,(214,204,180)); po=dict(P_walk(u*1.15,3.4,i*1.3)); po.update(curlL=.9,curlR=.9,mouth=1.0)
        if kind=="rods": props={"l":chain_prop,"r":rods_prop}
        elif kind=="torch": props={"l":None,"r":torch_prop}; po.update(ar=(1.3+.2*math.sin(u*4+i),2.5))
        else: props={"l":chain_prop,"r":None}; po.update(ar=(2.1+.2*math.sin(u*6),2.6))
        props={k:v for k,v in props.items() if v}
        P(d,cam,st,x,z,stl,po,hm=1.9,u=u,props=props,deco=rdeco((214,204,180)))
    big=snowfall(big,u*1.3,n=70,scale=2.4,seed=9)
    ov=Image.new("RGBA",big.size,(0,0,0,0)); od=ImageDraw.Draw(ov)
    for k in range(8): r=1300-k*130; od.ellipse([810-r,1900-r,810+r,1900+r],fill=(255,120,40,int(6*(.8+.2*math.sin(u*11)))))
    big=Image.alpha_composite(big.convert("RGBA"),ov).convert("RGB")
    return grade(big,seed=int(u*30))
# ---------------- escena 5: postales ----------------
def card(variant):
    cw,ch=450,630; paper=[(238,224,186),(214,226,196),(206,214,230)][variant%3]
    im=Image.new("RGB",(cw,ch),paper); a=np.asarray(im).astype(np.float32); rng=np.random.default_rng(variant+1)
    nz=np.asarray(Image.fromarray((rng.random((18,13))*255).astype(np.uint8)).resize((cw,ch),Image.BICUBIC),np.float32)/255; a*=(.9+nz[:,:,None]*.14)
    im=Image.fromarray(np.clip(a,0,255).astype(np.uint8)); d=ImageDraw.Draw(im)
    d.rectangle([14,14,cw-14,ch-14],outline=(170,130,50),width=5); d.rectangle([26,26,cw-26,ch-26],outline=(170,130,50),width=2)
    for (x,y) in((26,26),(cw-26,26),(26,ch-26),(cw-26,ch-26)): d.ellipse([x-12,y-12,x+12,y+12],fill=(170,130,50))
    d.text((cw/2,92),"Gruss vom",font=serif(44),fill=(150,30,36),anchor="mm"); d.text((cw/2,146),"KRAMPUS!",font=serif(60),fill=(150,30,36),anchor="mm")
    # fondo nevado y figura
    d.rectangle([40,190,cw-40,ch-48],fill=[(70,86,120),(80,96,110),(60,70,100)][variant%3])
    for k in range(60): x=40+rng.random()*(cw-80); y=190+rng.random()*(ch-238); d.ellipse([x-2,y-2,x+2,y+2],fill=(240,246,255))
    d.rectangle([40,ch-130,cw-40,ch-48],fill=(226,232,244))
    D_=D(im); KT[0]=variant*1.7
    from kramp import _horn
    po=dict(P_idle(variant*1.1),al=(.5,.9),ar=(2.0,2.4) if variant!=1 else (.3,.5),curlL=.9,curlR=.9,mouth=1.0)
    person(D_,75,205,.57,variant*.9,po,KR,props={"l":chain_prop,"r":rods_prop},deco=kdeco,back_deco=basket_back)
    d.rectangle([cw-110,34,cw-42,100],outline=(150,30,36),width=3); d.text((cw-76,67),"1 Pf",font=serif(20),fill=(150,30,36),anchor="mm")
    return im
_CARDS={}
def sceneF(u):
    KT[0]=u
    img=Image.new("RGB",(RW,RH),(46,30,18)); a=np.asarray(img).astype(np.float32)
    g=np.asarray(Image.fromarray((np.random.default_rng(3).random((50,5))*255).astype(np.uint8)).resize((RW,RH),Image.BICUBIC),np.float32)/255
    a*=(.7+g[:,:,None]*.7); img=Image.fromarray(np.clip(a,0,255).astype(np.uint8))
    img=img.convert("RGBA")
    for i,(ang,cx,cy,t0) in enumerate(((-14,230,560,.2),(5,420,640,1.0),(18,330,760,1.8))):
        if i not in _CARDS: _CARDS[i]=card(i)
        p=sm((u-t0)/.9); 
        if p<=0: continue
        c=_CARDS[i].convert("RGBA").resize((380,532),Image.LANCZOS)
        sh=Image.new("RGBA",(c.width+60,c.height+60),(0,0,0,0)); ImageDraw.Draw(sh).rectangle([30,40,c.width+30,c.height+40],fill=(0,0,0,130)); sh=sh.filter(ImageFilter.GaussianBlur(14))
        rot=c.rotate(ang+(1-p)*30,expand=True,resample=Image.BICUBIC); rs=sh.rotate(ang+(1-p)*30,expand=True,resample=Image.BICUBIC)
        x=int(cx+(1-p)*(500 if i%2 else -500)-rot.width/2); y=int(cy+math.sin(u*1.2+i)*3-rot.height/2)
        img.alpha_composite(rs,(x-30+30,y+10)) if x>-2000 else None; img.alpha_composite(rot,(x,y))
    img=img.convert("RGB"); big=fin(img); d=D(big)
    ox=300+40*math.sin(u*.5); oy=840
    d.L(480,1060,ox+8,oy+36,(70,90,120,255),38); hand(d,ox,oy+30,3.0+.04*math.sin(u*2),1,1.6,(236,190,150),curl=.5,spread=.6)
    ov=Image.new("RGBA",big.size,(0,0,0,0)); od=ImageDraw.Draw(ov); fl=.9+.1*math.sin(u*9)
    for k in range(10): r=1900-k*170; od.ellipse([200-r,2700-r,200+r,2700+r],fill=(255,170,70,int(6*fl)))
    big=Image.alpha_composite(big.convert("RGBA"),ov).convert("RGB")
    big=snowfall(big,u*1.1,n=36,scale=2.4,seed=11)
    return grade(big,sat=1.0,grain=3,seed=int(u*30),tint=(1.03,1.0,.94))
# ---------------- escena 6: cine ----------------
def hook_frame(t):
    KT[0]=t; cam=walk_cam(t,speed=.7); cam["pitch"]=.10+cam["pitch"]
    st=dict(STREET,fov=50)
    big=street_big(cam,t,st,1.0,snow=200); d=D(big)
    P(d,cam,st,.1,cam["z"]+6.0,KR,kr_pose(t),hm=2.0,u=t,props={"l":chain_prop,"r":rods_prop},deco=kdeco,back_deco=basket_back)
    return big
def sceneG(u):
    img=Image.new("RGB",(RW,RH),(6,6,10)); big=fin(img)
    scr=hook_frame(u*.8+3.0).crop((100,980,1520,1830)).resize((1380,826),Image.BICUBIC)
    sx,sy=120,260
    ov=Image.new("RGBA",big.size,(0,0,0,0)); od=ImageDraw.Draw(ov)
    for k in range(8): r=1800-k*180; od.ellipse([810-r,1500-r,810+r,1500+r],fill=(110,140,220,int(5)))
    od.polygon([(760,2900),(860,2900),(sx+1380,sy+826),(sx,sy+826)],fill=(200,215,255,22))
    big=Image.alpha_composite(big.convert("RGBA"),ov).convert("RGB")
    big.paste(scr,(sx,sy)); d=D(big)
    d.R(sx/3-6,sy/3-6,(sx+1380)/3+6,(sy+826)/3+6,None,4,(52,40,36,255),5)
    for k in range(8): d.R(20+k*68,760,80+k*68,820,(46,12,16,255),10)
    ppl=[(110,"short",(60,40,30),(70,50,90)),(270,"long",(120,70,40),(60,90,70)),(430,"bun",(40,30,28),(110,50,60))]
    for (x,hs,hc,shc) in ppl:
        stl=dict(skin=(150,120,100),hair=shade(hc,.8),hairstyle=hs,shirt=shade(shc,.6),pants=(20,20,30),sleeve="long")
        person(d,x,1090,1.55,u+x,dict(P_idle(u+x*.01),look=(0,-.6)),stl,facing="back")
    d.R(0,600,540,960,(0,0,0,40),0)
    big=grade(big,sat=.92,grain=5,seed=int(u*30),tint=(.96,.99,1.08))
    return big
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur): return 1.0,270,480
core.CAM=cam
if __name__=="__main__": core.main()
