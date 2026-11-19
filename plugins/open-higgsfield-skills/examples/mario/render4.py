import math, json, sys, wave, random
import numpy as np
from PIL import Image, ImageDraw
from multiprocessing import Pool
W,H=540,960; S=3; OUT=1080,1920; FPS=30
TL=json.load(open("timeline.json")); SC=TL["scenes"]; TOTAL=TL["total"]
def new(c1,c2):
    a=np.zeros((H*S//4,1,3),np.float32)
    t=np.linspace(0,1,a.shape[0])[:,None]
    a[:,0,:]=np.array(c1)[None,:]*(1-t)+np.array(c2)[None,:]*t
    im=Image.fromarray(a.astype(np.uint8)).resize((W*S,H*S),Image.BILINEAR)
    return im
class D:
    def __init__(s,im): s.im=im; s.d=ImageDraw.Draw(im,"RGBA")
    def R(s,x0,y0,x1,y1,c,r=0,o=None,ow=0):
        s.d.rounded_rectangle([x0*S,y0*S,x1*S,y1*S],radius=r*S,fill=c,outline=o,width=int(ow*S))
    def E(s,cx,cy,rx,ry,c,o=None,ow=0): s.d.ellipse([(cx-rx)*S,(cy-ry)*S,(cx+rx)*S,(cy+ry)*S],fill=c,outline=o,width=int(ow*S))
    def P(s,pts,c): s.d.polygon([(x*S,y*S) for x,y in pts],fill=c)
    def L(s,x0,y0,x1,y1,c,w=2): s.d.line([x0*S,y0*S,x1*S,y1*S],fill=c,width=int(w*S))
    def A(s,cx,cy,rx,ry,a0,a1,c,w=2): s.d.arc([(cx-rx)*S,(cy-ry)*S,(cx+rx)*S,(cy+ry)*S],a0,a1,fill=c,width=int(w*S))
def rnd(i,k=0): return ((i*9301+49297+k*233)%233280)/233280.0
def sm(t): t=max(0,min(1,t)); return t*t*(3-2*t)

# ---------- escenas (v2 con mas detalle) ----------
SK=(244,200,160); SK2=(222,170,132)
def shadow(d,cx,cy,rx,ry,a=70):
    for k in range(5): d.E(cx,cy,rx*(1+.1*k),ry*(1+.1*k),(0,0,0,a//3))
def bevel(d,x0,y0,x1,y1,c,r=6):
    d.R(x0,y0,x1,y1,c,r); d.R(x0+2,y0+2,x1-2,(y0+y1)/2,(255,255,255,36),r); d.R(x0+2,(y0+y1)/2,x1-2,y1-2,(0,0,0,40),r)
def errico(d,cx,cy,sc,a=255):
    d.E(cx,cy,48*sc,48*sc,(150,20,30,a)); d.E(cx,cy,44*sc,44*sc,(230,40,50,a)); d.E(cx-8*sc,cy-14*sc,28*sc,18*sc,(255,255,255,int(a*.18)))
    d.E(cx,cy,48*sc,48*sc,None,(255,255,255,a),3*sc)
    d.R(cx-6*sc,cy-28*sc,cx+6*sc,cy+6*sc,(255,255,255,a),3); d.E(cx,cy+22*sc,6.5*sc,6.5*sc,(255,255,255,a))
def keyboard(d,x,y,w,h):
    d.R(x,y,x+w,y+h,(40,38,58),5); d.R(x,y,x+w,y+3,(255,255,255,30),3)
    for r in range(3):
        for c in range(int(w/11)-1): d.R(x+5+c*11,y+4+r*(h-8)/3,x+13+c*11,y+4+r*(h-8)/3+5,(88,86,112),1.5)
def mug(d,x,y,u,col=(245,245,250)):
    shadow(d,x+2,y+24,16,4,60); bevel(d,x-14,y,x+14,y+24,col,5); d.A(x+16,y+11,9,8,-80,80,col,4)
    d.R(x-12,y+2,x+12,y+7,(90,50,30)); 
    for k in range(3): d.A(x-6+k*6,y-8-(u*14+k*4)%12,3,5,0,180,(255,255,255,int(150-((u*14+k*4)%12)*10)),1.5)
def monitor(d,x,y,w,h,mini=None,u=0,glare=True):
    shadow(d,x+w/2,y+h+24,w*.5,8,60)
    d.R(x+w/2-10,y+h,x+w/2+10,y+h+18,(34,32,48)); bevel(d,x+w/2-34,y+h+16,x+w/2+34,y+h+24,(52,50,70),4)
    bevel(d,x,y,x+w,y+h,(58,56,76),9); d.R(x+7,y+7,x+w-7,y+h-11,(6,22,16),5)
    d.E(x+w-14,y+h-5,2.2,2.2,(80,255,140))
    if mini=="code":
        for k in range(int((h-26)/12)):
            ww=18+rnd(k+int(u*2))*(w-70); xx=x+14+(k%3)*8
            d.R(xx,y+13+k*12,xx+ww,y+20+k*12,(70,230,130,225),2); d.R(xx+ww+4,y+13+k*12,xx+ww+4+rnd(k,9)*20,y+20+k*12,(255,200,90,200),2)
    elif mini=="chase":
        d.R(x+7,y+7,x+w-7,y+h-11,(46,50,60),5)
        for k in range(4): yy=((u*50+k*26)%(h-24))+y+8; d.R(x+w/2-2,yy,x+w/2+2,yy+10,(240,240,240,200))
        d.R(x+w/2+8,y+h-44,x+w/2+22,y+h-20,(235,60,60),3); d.R(x+w/2-22,y+h-62+math.sin(u*9)*3,x+w/2-8,y+h-38,(240,240,255),3)
    if glare: d.P([(x+10,y+8),(x+w*.55,y+8),(x+w*.25,y+h-12),(x+10,y+h-12)],(255,255,255,16))
def hair_front(d,cx,cy,sc,col,style):
    d.E(cx,cy-12*sc,31*sc,24*sc,col); d.E(cx,cy-18*sc,27*sc,16*sc,(255,255,255,26))
    if style==0:
        for k in range(5): d.P([(cx-26*sc+k*13*sc,cy-8*sc),(cx-18*sc+k*13*sc,cy-8*sc),(cx-22*sc+k*13*sc,cy+(2 if k%2 else 7)*sc)],col)
        d.E(cx-29*sc,cy,5*sc,12*sc,col); d.E(cx+29*sc,cy,5*sc,12*sc,col)
    else:
        d.E(cx,cy-38*sc,13*sc,11*sc,col); d.E(cx,cy-38*sc,13*sc,11*sc,None,(255,255,255,40),1.5*sc); d.R(cx-12*sc,cy-30*sc,cx+12*sc,cy-26*sc,(255,90,120),2*sc)
        d.E(cx-30*sc,cy+4*sc,6*sc,16*sc,col); d.E(cx+30*sc,cy+4*sc,6*sc,16*sc,col)
        d.P([(cx-26*sc,cy-6*sc),(cx+6*sc,cy-24*sc),(cx+27*sc,cy-6*sc),(cx+27*sc,cy+2*sc),(cx+2*sc,cy-12*sc),(cx-26*sc,cy+4*sc)],col)
def face(d,cx,cy,sc,laugh,glasses,beard,ph=0):
    d.E(cx-29*sc,cy+3*sc,5.5*sc,8.5*sc,SK2); d.E(cx+29*sc,cy+3*sc,5.5*sc,8.5*sc,SK2)
    d.E(cx,cy,28*sc,31*sc,SK); d.E(cx+8*sc,cy+10*sc,22*sc,20*sc,(255,255,255,0)); d.E(cx-12*sc,cy+14*sc,12*sc,12*sc,(0,0,0,12))
    d.E(cx-15*sc,cy+9*sc,6.5*sc,4*sc,(255,110,110,85)); d.E(cx+15*sc,cy+9*sc,6.5*sc,4*sc,(255,110,110,85))
    d.E(cx,cy+6*sc,3.2*sc,3.6*sc,SK2); 
    if beard:
        d.d.pieslice([(cx-27*sc)*S,(cy-2*sc)*S,(cx+27*sc)*S,(cy+34*sc)*S],20,160,fill=(60,42,32,170))
    if laugh:
        for sg in(-1,1):
            d.A(cx+sg*11*sc,cy-3*sc,6.5*sc,5.5*sc,200,340,(40,30,30),2.2*sc)
            d.L(cx+sg*17*sc,cy-12*sc,cx+sg*6*sc,cy-(13+sg*1)*sc,(70,45,30),2*sc)
        d.d.pieslice([(cx-14*sc)*S,(cy+8*sc)*S,(cx+14*sc)*S,(cy+28*sc)*S],0,180,fill=(120,28,38,255))
        d.d.pieslice([(cx-13*sc)*S,(cy+8*sc)*S,(cx+13*sc)*S,(cy+15*sc)*S],0,180,fill=(250,250,250,255))
        d.E(cx,cy+22*sc,7*sc,3.5*sc,(235,110,120))
    else:
        for sg in(-1,1):
            d.E(cx+sg*10.5*sc,cy-2*sc,6*sc,4.6*sc,(255,255,255)); d.E(cx+sg*10.5*sc,cy-2*sc,2.9*sc,2.9*sc,(40,30,30)); d.E(cx+sg*9.5*sc,cy-3.2*sc,1*sc,1*sc,(255,255,255))
            d.L(cx+sg*16*sc,cy-9*sc,cx+sg*6*sc,cy-9.5*sc,(70,45,30),2*sc)
        d.A(cx,cy+11*sc,9*sc,6*sc,20,160,(110,40,40),2*sc)
    if glasses:
        for sg in(-1,1): d.E(cx+sg*10.5*sc,cy-2*sc,8.5*sc,7*sc,None,(30,30,40),1.8*sc); d.E(cx+sg*10.5*sc-2*sc,cy-4*sc,4*sc,2*sc,(255,255,255,70))
        d.L(cx-2*sc,cy-3*sc,cx+2*sc,cy-3*sc,(30,30,40),1.8*sc)
def person_front(d,cx,cy,sc,which,u,laugh=True):
    ph=u*14; dy=math.sin(ph)*3*sc if laugh else 0
    shirt=(70,120,210) if which==0 else (222,84,110); hair=(58,40,30) if which==0 else (190,120,50)
    shadow(d,cx,cy+138*sc,50*sc,8*sc,60)
    d.R(cx-9*sc,cy+24*sc+dy,cx+9*sc,cy+46*sc+dy,SK2)
    bevel(d,cx-42*sc,cy+38*sc+dy,cx+42*sc,cy+138*sc,shirt,22*sc)
    if which==0:
        d.E(cx,cy+42*sc+dy,24*sc,10*sc,(shirt[0]-20,shirt[1]-20,shirt[2]-20)); d.L(cx-8*sc,cy+52*sc+dy,cx-9*sc,cy+82*sc+dy,(240,240,240),2*sc); d.L(cx+8*sc,cy+52*sc+dy,cx+9*sc,cy+82*sc+dy,(240,240,240),2*sc)
        d.R(cx-22*sc,cy+98*sc+dy,cx+22*sc,cy+118*sc+dy,(0,0,0,30),6*sc)
    else:
        d.P([(cx-12*sc,cy+38*sc+dy),(cx+12*sc,cy+38*sc+dy),(cx,cy+58*sc+dy)],SK); d.E(cx-34*sc,cy+10*sc+dy,2*sc,3*sc,(255,215,90))
    for sg in(-1,1):
        ax=cx+sg*46*sc; bevel(d,ax-10*sc,cy+52*sc+dy,ax+10*sc,cy+120*sc+dy,shirt,9*sc); d.E(ax,cy+126*sc+dy,10*sc,9*sc,SK)
    hair_front(d,cx,cy+dy,sc,hair,which)
    face(d,cx,cy+dy,sc,laugh,which==0,False,ph)
def person_back(d,cx,cy,sc,which,u):
    shirt=(70,120,210) if which==0 else (222,84,110); hair=(58,40,30) if which==0 else (190,120,50)
    chair=(44,32,60)
    shadow(d,cx,cy+148*sc,56*sc,8*sc,60)
    bevel(d,cx-48*sc,cy-20*sc,cx+48*sc,cy+120*sc,chair,18*sc); bevel(d,cx-20*sc,cy-34*sc,cx+20*sc,cy-8*sc,chair,8*sc)
    bevel(d,cx-40*sc,cy+34*sc,cx+40*sc,cy+138*sc,shirt,22*sc)
    d.L(cx,cy+40*sc,cx,cy+120*sc,(0,0,0,50),2*sc)
    if which==0: d.E(cx,cy+42*sc,26*sc,12*sc,(shirt[0]-25,shirt[1]-25,shirt[2]-25))
    d.R(cx-9*sc,cy+22*sc,cx+9*sc,cy+42*sc,SK2)
    d.E(cx-28*sc,cy+2*sc,5*sc,8*sc,SK2); d.E(cx+28*sc,cy+2*sc,5*sc,8*sc,SK2)
    d.E(cx,cy,29*sc,32*sc,hair); d.E(cx-6*sc,cy-12*sc,16*sc,9*sc,(255,255,255,30))
    for k in range(6): d.A(cx,cy,(8+k*4)*sc,(9+k*4)*sc,200+k*8,340-k*8,(0,0,0,45),1.2*sc)
    if which==1: d.E(cx,cy-36*sc,13*sc,11*sc,hair); d.R(cx-12*sc,cy-30*sc,cx+12*sc,cy-26*sc,(255,90,120),2*sc)
    for sg in(-1,1):
        ax=cx+sg*50*sc; bevel(d,ax-9*sc,cy+52*sc,ax+9*sc,cy+104*sc,shirt,8*sc)


PAL={"C":(255,140,40),"S":(244,200,160),"M":(100,60,30),"B":(60,100,220),"T":(245,245,245),"Y":(255,220,80),"H":(120,70,40)}
SPR=["...CCCCC....","..CCCCCCCCC.","..MMMSSMS...",".MSMSSSMSSS.",".MSMMSSSMSSS",".MMSSSSMMMM.","...SSSSSSS..","..TTBTTT....",".TTTBTTBTTT.","TTTTBBBBTTTT","SSTBYBBYBTSS","SSSBBBBBBSSS","..BBB..BBB..",".HHH....HHH."]
NCELLS=sum(ch!='.' for row in SPR for ch in row)
def clamp(x,a=0,b=1): return max(a,min(b,x))
def sprite(d,x,y,cell,sil=False,reveal=None,alpha=255,flip=False,legs=0,rf=None):
    n=0
    for r,row in enumerate(SPR):
        for c,ch in enumerate(row):
            if ch=='.': continue
            n+=1
            if reveal is not None and n>reveal: continue
            cc=c if not flip else len(row)-1-c
            col=(20,22,40) if sil else PAL[ch]
            sc=1.0; dx=0
            if r>=12 and legs: 
                dx=(1 if (c<6)==(legs>0) else -1)*abs(legs)*cell*.35
            if rf is not None:
                age=(rf-n)/7.0
                if 0<=age<1: sc=1+.5*math.sin(math.pi*age)
            o=(cell*sc-cell)/2
            d.R(x+cc*cell+dx-o,y+r*cell-o,x+cc*cell+dx+cell*sc-o+.4,y+r*cell+cell*sc-o+.4,col+(alpha,),0)
def pxq(d,x,y,cell,col=(255,255,255)):
    rows=["..###..","##...##","....##.","...##..","...#...",".......","...#..."]
    for r,row in enumerate(rows):
        for c,ch in enumerate(row):
            if ch=='#': d.R(x+c*cell,y+r*cell,x+c*cell+cell,y+r*cell+cell,col,1)
def rotpts(pts,px,py,a):
    ca,sa=math.cos(a),math.sin(a); return [(px+(x-px)*ca-(y-py)*sa,py+(x-px)*sa+(y-py)*ca) for x,y in pts]
# ---------- A: sala arcade ----------
def sceneA(u,final=False):
    im=new((10,8,34),(40,12,60)); d=D(im)
    for k in range(50): d.E(rnd(k)*540,rnd(k,1)*420,1.4,1.4,(255,255,255,120+int(90*math.sin(u*2+k))))
    # maquina vecina apagada al fondo
    bevel(d,-30,300,90,900,(30,18,56),10); d.R(-14,340,74,420,(10,10,20),6); bevel(d,450,300,570,900,(30,18,56),10); d.R(466,340,554,420,(10,10,20),6)
    # suelo con baldosas y reflejo
    d.R(0,860,540,960,(30,18,56))
    for k in range(10): d.L(0,860+k*14,540,860+k*14,(255,255,255,12),1.5)
    for k in range(9): d.L(k*68-20,860,k*68-90,960,(255,255,255,10),1.5)
    d.E(270,520,230,60,(255,60,200,40+int(15*math.sin(u*3))))
    shadow(d,270,884,170,16,90)
    bevel(d,100,170,440,880,(96,40,150),16); d.R(100,170,126,880,(255,255,255,18)); d.R(414,170,440,880,(0,0,0,50))
    for k in range(8): d.P([(100,700-k*80),(126,720-k*80),(126,740-k*80),(100,720-k*80)],(255,80,200,40))
    pulse=int(180+70*math.sin(u*5))
    bevel(d,120,150,420,236,(30,16,60),10); d.R(132,168,408,218,(255,60,190),6); d.R(132,168,408,218,None,6,(255,200,240,pulse),3)
    for k in range(10): d.E(146+k*28,193,5,5,(255,255,255,int(150+100*math.sin(u*6+k))))
    bevel(d,134,252,406,520,(18,16,30),12); d.R(146,264,394,508,(8,12,28),6)
    for k in range(20): d.R(146,264+k*12,394,265+k*12,(0,0,0,40))
    d.R(146,264,394,508,(60,100,255,int(14+8*math.sin(u*4))),6)
    wob=int(math.sin(u*4)*2)
    sprite(d,236,322+wob,9,sil=True)
    if int(u*3)%2==0 or final: pxq(d,260,276,6,(255,230,90))
    d.P([(150,266),(260,266),(190,508),(150,508)],(255,255,255,10))
    bevel(d,120,550,420,640,(60,24,100),10)
    jx=math.sin(u*2.3)*7
    d.E(190,596,18,18,(30,30,40)); d.L(190,596,190+jx,570,(220,220,230),6); d.E(190+jx,568,8,8,(240,50,60))
    for k,c in enumerate([(255,70,80),(80,200,255),(255,220,80)]):
        dn=3 if int(u*4+k)%5==0 else 0
        d.E(280+k*46,590+(k%2)*8,14,14,(30,20,40)); d.E(280+k*46,588+(k%2)*8+dn,11,11,c)
    d.R(246,676,294,700,(10,10,20),3); d.R(262,682,278,694,(255,220,80,int(120+100*(int(u*2)%2))),2)
    for k in range(5): d.R(150+k*44,736,180+k*44,744,(0,0,0,70),2)
    d.R(130,730,410,860,(78,34,124),6); d.R(130,730,410,736,(255,255,255,20))
    # polvo flotando
    for k in range(18):
        x=(rnd(k,2)*540+u*8*(k%3+1))%540; y=(rnd(k,3)*960-u*14*(k%2+1))%960; d.E(x,y,1.6,1.6,(255,255,255,70))
    return im
# ---------- B: arcade 1981 con fisica ----------
LVL=[(200,.02),(340,-.02),(490,.02),(640,-.02),(790,.02)]
def surf(i,x): y,s=LVL[i]; return y+s*(x-20)
def sim_barrel(ts,v=360.0,dt=1/60.0):
    tr=[]; i=0; x=215.0; y=surf(0,x)-13; ang=0.0; ph="roll"; vy=0.0; t=ts
    while t<ts+30:
        dr=1 if LVL[i][1]>0 else -1
        if ph=="roll":
            x+=dr*v*dt; ang+=dr*v*dt/13; y=surf(i,x)-13
            if (dr>0 and x>=505) or (dr<0 and x<=35):
                if i==4: tr.append((t,x,y,ang)); break
                ph="fall"; vy=0
        elif ph=="fall":
            vy+=900*dt; y+=vy*dt; x+=dr*14*dt; ang+=dr*dt*3
            if y>=surf(i+1,x)-13: i+=1; y=surf(i,x)-13; vy=-140; ph="bounce"
        else:
            vy+=900*dt; y+=vy*dt; x+=dr*14*dt; ang+=dr*dt*3
            if y>=surf(i,x)-13: y=surf(i,x)-13; ph="roll"
        tr.append((t,x,y,ang)); t+=dt
    return tr
SPAWN=[0.2,1.2,2.2]; TRAJ=[sim_barrel(s) for s in SPAWN]
def barrel_at(k,u):
    tr=TRAJ[k]
    if u<tr[0][0] or u>tr[-1][0]: return None
    j=min(len(tr)-1,int((u-tr[0][0])*60)); return tr[j]
def level_cross(k,lvl_y,x_t):
    best=None
    for t,x,y,a in TRAJ[k]:
        if abs(surf(3,x)-13-y)<2 and x<=x_t+1 and t>TRAJ[k][0][0]+1:
            if best is None and x<=x_t: best=t
    return best
JT=[level_cross(k,640,300) for k in range(3)]
def heroB(u):
    if u<1.2: x=400-239*sm(u/1.2); return x,surf(4,x),0,"walk",1
    if u<3.0:
        p=(u-1.2)/1.8; return 161,surf(4,161)+(surf(3,161)-surf(4,161))*p,0,"climb",p
    if u<5.4:
        p=sm((u-3.0)/2.4); x=161+139*p; y=surf(3,x)
    else: x=300; y=surf(3,300)
    j=0
    for tc in JT:
        if tc and abs(u-tc)<.38: j=max(j,56*(1-((u-tc)/.38)**2))
    return x,y-j,j,"walk" if u<5.4 else "idle",1
def ape(d,x,y,u,arms_up=0):
    c=(150,92,50); b=(98,58,30)
    shadow(d,x,y+52,56,8,70)
    d.E(x,y,52,46,b); d.E(x,y+8,38,32,c)
    pound=math.sin(u*10)*8*(1-arms_up)
    d.E(x-54,y+20+pound-arms_up*70,16,24,b); d.E(x+54,y+20-pound-arms_up*70,16,24,b)
    d.E(x,y-38,30,26,b); d.E(x,y-32,22,17,(230,190,150))
    for sg in(-1,1): d.E(x+sg*9,y-38,5,5,(255,255,255)); d.E(x+sg*9,y-38,2.4,2.4,(20,20,30)); d.E(x+sg*37,y-36,7,8,b)
    d.A(x,y-24,11,6,20,160,(70,30,20),2.5)
def barrel(d,x,y,r,ang):
    d.E(x+3,y+4,r,r*.9,(0,0,0,60))
    d.E(x,y,r,r,(170,108,52)); d.E(x,y,r*.7,r*.7,None,(90,50,20),2)
    for k in range(3):
        a=ang+k*2.09; d.L(x,y,x+math.cos(a)*r,y+math.sin(a)*r,(100,58,26),2)
    d.E(x-r*.3,y-r*.35,r*.35,r*.25,(255,255,255,50))
def girders(d,u):
    d.R(0,0,540,960,(8,8,20))
    for k in range(7): d.R(0,k*140,540,k*140+70,(255,255,255,4))
    for i,(y,sl) in enumerate(LVL):
        d.P([(20,y),(520,y+sl*500),(520,y+sl*500+22),(20,y+22)],(220,70,60))
        d.P([(20,y),(520,y+sl*500),(520,y+sl*500+6),(20,y+6)],(255,150,130))
        d.P([(20,y+22),(520,y+sl*500+22),(520,y+sl*500+30),(20,y+30)],(0,0,0,90))
        for k in range(24): xx=24+k*21; d.L(xx,y+22+sl*(xx-20),xx+12,y+6+sl*(xx-20),(120,30,40),2)
        for k in range(12): xx=30+k*42; d.E(xx,y+11+sl*(xx-20),2.2,2.2,(255,220,200))
    for x,y0,y1 in [(150,790,640),(380,640,490),(130,490,340),(400,340,200)]:
        y0=y0+ (0.02 if y0==790 else -0.02 if y0==640 else .02 if y0==490 else -.02)*(x-20)
        y1=y1+ (-.02 if y1==640 else .02 if y1==490 else -.02 if y1==340 else .02)*(x-20)
        d.L(x,y0,x,y1,(80,220,255),3); d.L(x+22,y0,x+22,y1,(80,220,255),3)
        for yy in range(int(min(y0,y1)),int(max(y0,y1)),14): d.L(x,yy,x+22,yy,(80,220,255),2.5)
def sceneB(u):
    im=new((8,8,20),(8,8,20)); d=D(im); girders(d,u)
    up=0
    for s in SPAWN:
        if s-.3<=u<s+.15: up=sm((u-(s-.3))/.25)*(1 if u<s else 1-(u-s)/.15)
    ape(d,130,150,u,up)
    # barril en las manos del mono antes de lanzarlo
    for s in SPAWN:
        if s-.3<=u<s: barrel(d,130+30,92,13,u*5)
    # bidon con fuego
    bevel(d,28,738,78,792,(50,90,200),4); d.R(28,756,78,762,(255,255,255,50)); 
    for k in range(5):
        fx=53+(k-2)*9; fh=22+10*math.sin(u*13+k*1.7); d.P([(fx-6,738),(fx,738-fh),(fx+6,738)],(255,150+k*12,40,230))
    # hero
    hx,hy,j,mode,p=heroB(u)
    cell=6.5; h=14*cell
    if mode=="climb": flip=int(p*8)%2==0
    else: flip=False
    shadow(d,hx,surf(3 if u>=3.0 else 4,hx)+2 if mode!="climb" else hy+2,28,5,80) if j==0 else None
    sprite(d,hx-6*cell,hy-h,cell,flip=flip,legs=(math.sin(u*14)*(.9 if mode=="walk" else .0) if mode!="climb" else (1 if int(p*8)%2 else -1)*.8))
    # barriles
    for k in range(3):
        b=barrel_at(k,u)
        if b: barrel(d,b[1],b[2],13,b[3])
    # scanlines + resplandor CRT
    for k in range(80): d.R(0,k*12,540,k*12+1,(0,0,0,60))
    return im
# ---------- C: sprite que se dibuja ----------
def sceneC(u):
    im=new((14,10,38),(30,14,56)); d=D(im)
    for k in range(30): d.E(rnd(k)*540,rnd(k,1)*960,1.2,1.2,(255,255,255,70))
    G=32; ox=54; oy=250
    bevel(d,ox-20,oy-20,ox+12*G+20,oy+15*G+20,(24,22,56),10)
    for r in range(15):
        for c in range(12): d.R(ox+c*G,oy+r*G,ox+c*G+G-2,oy+r*G+G-2,(32,30,72),2)
    rf=clamp(u/3.4)*NCELLS; reveal=int(rf)
    sprite(d,ox,oy,G,reveal=reveal,rf=rf)
    # cursor lapiz que se mueve celda a celda
    n=0; pos=None
    for r,row in enumerate(SPR):
        for c,ch in enumerate(row):
            if ch=='.': continue
            n+=1
            if n==reveal: pos=(ox+c*G+G/2,oy+r*G+G/2)
    if pos and u<3.5:
        px,py=pos; d.P([(px,py),(px+10,py-34),(px+22,py-26),(px+14,py+4)],(255,210,80)); d.P([(px,py),(px+4,py-12),(px+10,py-8)],(250,250,250)); d.E(px,py,5,5,(255,255,255,150))
    if u>3.6:
        a=int(160+90*math.sin(u*7))
        d.R(ox+2*G-6,oy-6,ox+11*G+6,oy+2*G+6,None,10,(255,160,60,a),4); d.R(ox+1*G-6,oy+2*G-6,ox+11*G+6,oy+6*G+6,None,10,(255,255,255,a),3)
    d.R(380,60,500,200,(20,18,50),8); d.R(380,60,500,66,(255,255,255,20),8)
    sprite(d,408,84,5,reveal=reveal)
    d.R(20,780,520,940,(20,18,50,200),10)
    for k in range(6): d.R(40+k*78,806,98+k*78,864,(40+k*14,50,120),4)
    return im
# ---------- D: el casero llega, llama y la puerta se abre ----------
def landlord(d,cx,feet,sc,u,walk=0,knock=0):
    cy=feet-196*sc; sw=math.sin(u*10)*walk
    shadow(d,cx,feet,52*sc,8*sc,70)
    for sg in(-1,1):
        lx=cx+sg*16*sc+sg*sw*10*sc; bevel(d,lx-12*sc,cy+130*sc,lx+12*sc,feet-8*sc,(76,52,40),6*sc); d.R(lx-14*sc,feet-12*sc,lx+16*sc,feet,(34,26,24),4*sc)
    bob=abs(math.sin(u*10))*3*sc*(1 if walk else 0); cy-=bob
    bevel(d,cx-44*sc,cy+38*sc,cx+44*sc,cy+138*sc,(124,84,52),22*sc)
    d.P([(cx-10*sc,cy+38*sc),(cx+10*sc,cy+38*sc),(cx,cy+70*sc)],(245,245,245)); d.R(cx-4*sc,cy+48*sc,cx+4*sc,cy+100*sc,(200,40,50),2*sc)
    d.R(cx-9*sc,cy+24*sc,cx+9*sc,cy+46*sc,SK2)
    bevel(d,cx-58*sc,cy+52*sc-sw*14*sc,cx-38*sc,cy+120*sc-sw*14*sc,(124,84,52),9*sc); d.E(cx-48*sc,cy+126*sc-sw*14*sc,10*sc,9*sc,SK)
    kx=knock*30*sc
    ax=cx+46*sc+kx; bevel(d,ax-10*sc,cy+44*sc-(knock>0)*18*sc,ax+10*sc,cy+104*sc-(knock>0)*18*sc,(124,84,52),9*sc); d.E(ax,cy+108*sc-(knock>0)*18*sc,10*sc,9*sc,SK)
    hair_front(d,cx,cy,sc,(190,190,200),0)
    face(d,cx,cy,sc,False,False,False)
    d.P([(cx-18*sc,cy+13*sc),(cx,cy+8*sc),(cx+18*sc,cy+13*sc),(cx+12*sc,cy+19*sc),(cx,cy+14*sc),(cx-12*sc,cy+19*sc)],(70,60,60))
    d.L(cx-18*sc,cy-10*sc,cx-5*sc,cy-6*sc,(60,50,50),3*sc); d.L(cx+18*sc,cy-10*sc,cx+5*sc,cy-6*sc,(60,50,50),3*sc)
    d.R(cx-70*sc,cy+120*sc,cx-30*sc,cy+160*sc,(250,250,240),3); d.L(cx-62*sc,cy+132*sc,cx-38*sc,cy+132*sc,(200,40,40),2)
def sceneD(u):
    im=new((250,150,100),(90,50,110)); d=D(im)
    d.E(400,230,70,70,(255,230,150,230)); d.E(400,230,120,120,(255,230,150,40))
    for k in range(3): d.E(100+k*140+(u*6)%30,150+k*30,50,16,(255,255,255,40))
    d.R(0,720,540,960,(70,60,76)); d.R(0,720,540,728,(255,255,255,24))
    for k in range(8): d.L(k*80-30,728,k*100-80,960,(0,0,0,30),2)
    bevel(d,40,240,500,720,(150,88,70),6)
    for r in range(19):
        for c in range(14):
            if (r+c)%2==0: d.R(42+c*32,242+r*25,42+c*32+30,242+r*25+23,(120,66,52,160),1)
    bevel(d,70,280,470,340,(60,50,80),4)
    for k in range(5): d.R(96+k*70,296,128+k*70,326,(255,230,120,160),2)
    for sg in(0,1):
        d.R(90+sg*130,440,170+sg*130,560,(40,50,90),4); d.R(94+sg*130,444,166+sg*130,556,(255,230,140,200),3); d.L(130+sg*130,444,130+sg*130,556,(40,50,90),3)
    # farola
    d.R(26,420,34,722,(40,40,60)); d.E(30,414,14,14,(255,240,170)); d.E(30,414,34,34,(255,240,170,50))
    # puerta que se abre (bisagra a la derecha)
    openp=sm((u-4.2)/1.4)
    d.R(314,430,466,722,(255,214,130,int(255*openp)) if openp>0 else (0,0,0,0),0)
    if openp>0:
        d.P([(314,722),(466,722),(466+0,722+ 160*openp),(314,722+160*openp)],(255,214,130,int(90*openp)))
        d.R(318,436,462,720,(255,226,160))
        d.R(330,640,450,720,(80,60,50,160)); d.R(360,560,420,640,(120,90,70,160))
    wdt=int(146*math.cos(openp*1.25))
    d.R(466-wdt,430,466,722,(80,54,40)); d.R(472-wdt+10,442,460,708,(60,40,32),4) if wdt>40 else None
    d.E(466-wdt+14,590,5,5,(240,200,80))
    # casero: camina, llama y espera
    if u<2.4: x=-90+330*sm(u/2.4); walk=1; kn=0
    else: x=240; walk=0; kn=(max(0,math.sin((u-2.5)*9)) if u<4.1 else 0)
    landlord(d,x,720,1.5,u,walk,kn)
    if kn>.8 and u<4.2:
        for k in range(2): d.A(x+110,520,20+k*14+ (u*30)%10,20+k*14+(u*30)%10,-50,50,(255,255,255,150-k*50),2)
    return im
# ---------- E: el equipo bautiza al personaje ----------
def sceneE(u):
    im=new((94,54,102),(38,26,64)); d=D(im)
    # pizarra con bocetos
    bevel(d,20,100,128,200,(240,240,236),4); d.L(32,118,100,118,(60,60,200),2); sprite(d,36,126,3); d.L(32,184,110,184,(0,0,0,70),2)
    d.R(412,110,500,222,(240,230,200),3); d.L(420,126,490,126,(0,0,0,60),2)
    for k in range(7): d.E(50+k*74,60+math.sin(u*3+k)*8,9,9,(255,220,120,120)); d.E(50+k*74,60+math.sin(u*3+k)*8,16,16,(255,220,120,40))
    d.R(0,640,540,960,(34,26,50)); d.R(0,640,540,646,(255,255,255,16))
    monitor(d,150,150,240,190,None,u)
    d.R(157,157,383,328,(40,60,110)); d.R(157,300,383,328,(70,150,70))
    # heroe en el monitor con gravedad: salta, vuelve a caer
    per=1.6; ph=(u%per)/per; hgt=64*4*ph*(1-ph)*1.0
    hx=190+ (u*38)%160
    sprite(d,hx,300-14*4-hgt,4,legs=math.sin(u*14)*.8)
    bevel(d,50,596,490,656,(88,62,100),10)
    tilt=math.sin(u*5)*3
    person_front(d,168,470,1.55,0,u,True); person_front(d,372,476,1.55,1,u+.4,True)
    b=sm((u-.6)/.35); ov=1+.18*math.sin(clamp((u-.6)/.5)*math.pi)
    bx,by=400,372
    d.R(bx-100*b*ov,by-34*b*ov,bx+100*b*ov,by+34*b*ov,(255,255,255,int(245*clamp(b))),18)
    d.P([(bx-60*b,by+30*b),(bx-30*b,by+30*b),(bx-48*b,by+64*b)],(255,255,255,int(245*clamp(b))))
    if b>.9: sprite(d,bx-24,by-26,4)
    for k in range(3):
        a=(u*2+k*.33)%1; d.A(80+k*30,250-a*50,12,10,0,360,(255,255,255,int(160*(1-a))),2)
    mug(d,270,568,u,(255,210,90))
    return im
# ---------- F: carpintero y fontanero (dos estaciones, camara viaja) ----------
def sceneF(u):
    im=new((24,18,60),(60,30,90)); d=D(im)
    for k in range(40): d.E(rnd(k)*540,rnd(k,1)*420,1.4,1.4,(255,255,255,140))
    d.R(0,740,540,960,(30,24,52)); d.R(0,740,540,746,(255,255,255,24))
    d.R(268,0,272,960,(255,255,255,0))
    # --- carpintero (izq) ---
    shadow(d,140,812,110,10,80)
    d.R(40,720,250,760,(150,100,50),4); d.R(40,720,250,726,(210,150,90),4)
    for sg in(60,230): d.R(sg-6,760,sg+6,812,(110,70,40),2)
    d.R(70,700,230,722,(190,140,80),3)
    hit=max(0,math.sin(u*7.0)); ang=-1.1+ (1.1+.0)*(hit**3)*1.0
    sprite(d,86,592,8,legs=0)
    px,py=190,640
    hm=rotpts([(px-4,py-80),(px+4,py-80),(px+4,py),(px-4,py)],px,py,-1.0+1.8*(1-hit)**2)
    d.P(hm,(160,110,60)); hd=rotpts([(px-18,py-92),(px+18,py-92),(px+18,py-76),(px-18,py-76)],px,py,-1.0+1.8*(1-hit)**2); d.P(hd,(190,190,205))
    d.R(176,696,184,722,(200,200,210),1)
    if hit>.9:
        for k in range(8): a=k*.8; d.L(184,700,184+math.cos(a)*22,700+math.sin(a)*14,(255,230,120),3)
    for k in range(8):
        t=(u*1.3+k*.37)%1; d.R(160+k*10+t*24,700+t*80-math.sin(t*3)*20*(1-t),164+k*10+t*24,704+t*80-math.sin(t*3)*20*(1-t),(220,170,100,int(220*(1-t))),1)
    # --- fontanero (der) ---
    shadow(d,400,812,110,10,80)
    d.R(300,730,500,748,(120,130,150),4); d.R(300,730,500,736,(190,200,220),4)
    d.R(310,690,324,730,(120,130,150),3); d.R(470,690,484,730,(120,130,150),3)
    d.R(330,640,478,672,(150,162,182),6); d.R(330,640,478,648,(255,255,255,60),6)
    d.R(328,634,340,678,(110,120,140),3); d.R(462,634,474,678,(110,120,140),3)
    sprite(d,340,590,8,flip=True,legs=0)
    rot=math.sin(u*5)*.35
    wr=rotpts([(400,610),(406,610),(406,660),(400,660)],403,656,rot); d.P(wr,(150,150,160))
    d.E(403,656,9,9,(190,190,200)); d.E(403,656,9,9,None,(90,90,100),2)
    # goteo con gravedad hacia el charco
    for k in range(5):
        t=((u*.9+k*.21)%1); y=672+ (t*t)*70
        if y<740: d.E(440+ (k%2)*8, y, 3.2,5,(120,200,255,220))
        else: d.E(440,742+ (t*10),5+(t-.7)*40,2,(120,200,255,120))
    d.E(445,746,24,5,(100,180,255,110)); 
    for k in range(3): d.E(445,746,10+((u*2+k*.33)%1)*28,2+((u*2+k*.33)%1)*4,None,(180,230,255,int(150*(1-((u*2+k*.33)%1)))),1.5)
    for k in range(4): d.E(360+k*18+math.sin(u*2+k)*4,610-((u*20+k*17)%50),8,6,(255,255,255,40))
    return im
# ---------- G: el escenario ----------
def sceneG(u):
    im=new((70,10,30),(20,6,30)); d=D(im)
    for k in range(16):
        a=k*math.pi/8+u*.5; d.P([(270,300),(270+math.cos(a-.09)*800,300+math.sin(a-.09)*800),(270+math.cos(a+.09)*800,300+math.sin(a+.09)*800)],(255,230,150,16))
    op=sm((u-.2)/1.4)
    d.R(0,780,540,960,(110,24,36)); d.R(0,780,540,788,(255,255,255,30))
    for k in range(9): d.R(k*60,800,k*60+8,960,(0,0,0,40))
    # foco que barre
    sx=270+math.sin(u*1.2)*60
    d.P([(sx-14,0),(sx+14,0),(sx+130,800),(sx-130,800)],(255,240,180,34)); d.E(sx,800,130,22,(255,240,180,60))
    s=.3+.7*sm(u/.9); br=math.sin(u*3)*2
    landlord(d,150,790,1.15*s,u,0,0)
    sprite(d,300,790-14*12*s+br,12*s+.01,legs=0)
    shadow(d,360,792,70,8,80)
    # cortinas
    for sg in(-1,1):
        w=170*(1-op)
        x0=0 if sg<0 else 540-w
        d.R(x0,0,x0+w,960,(150,24,40)); 
        for k in range(int(w/22)+1): d.R(x0+k*22,0,x0+k*22+8,960,(0,0,0,40))
    d.R(0,0,540,50,(120,16,30))
    for k in range(40):
        a=k*.21; t=((u-.9)*.5+rnd(k,4))%1; 
        x=270+(rnd(k,6)-.5)*500+math.sin(t*9+k)*14; y=-20+t*900
        if u>.9: d.R(x,y,x+7,y+4,[(255,220,80),(80,220,255),(255,100,150),(120,255,140)][k%4]+(230,),1)
    for k in range(20):
        x=270+math.cos(k*.31+u*.3)*210; y=330+math.sin(k*.31+u*.3)*150; 
        d.P([(x,y-8),(x+3,y-3),(x+8,y),(x+3,y+3),(x,y+8),(x-3,y+3),(x-8,y),(x-3,y-3)],(255,230,120,170))
    return im
SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
# ---------- camara cinematografica ----------
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx==0: return 1.0+.22*sm(p),270,470-60*sm(p)
    if idx==1:
        hx,hy,_,_,_=heroB(min(u,9.6)); return 1.1,270+(hx-270)*.5,clamp(420+(hy-420)*.6,300,720)
    if idx==2: return 1.65-.62*sm(clamp(u/4.2)),270+60*(1-sm(clamp(u/4.2))),430+60*(1-sm(clamp(u/4.2)))
    if idx==3: return 1.0+.35*sm(p),270+ 70*sm(p),480+60*sm(p)
    if idx==4: return 1.0+.12*sm(p),300-40*sm(p),460
    if idx==5:
        q=sm(clamp((u-2.4)/1.1)); return 1.55,140+ (400-140)*q,650
    if idx==6: return 1.5-.5*sm(clamp(u/3)),270,600-110*sm(clamp(u/3))
    return 1.22-.22*sm(p)+.0,270,430+40*sm(p)
def render_cam(idx,u,dur,t):
    im=SCN[idx](u); z,cx,cy=cam(idx,u,dur)
    cx+=math.sin(t*1.7)*1.6+math.sin(t*5.3)*.7; cy+=math.cos(t*1.3)*1.6+math.cos(t*4.1)*.7
    w,h=W/z,H/z; x0=clamp(cx-w/2,0,W-w); y0=clamp(cy-h/2,0,H-h)
    return im.crop((int(x0*S),int(y0*S),int((x0+w)*S),int((y0+h)*S))).resize(OUT,Image.LANCZOS)
_vig=None
def post(img,seed):
    global _vig
    a=np.asarray(img).astype(np.float32)
    # bloom
    small=img.resize((135,240),Image.BILINEAR)
    br=np.clip(np.asarray(small).astype(np.float32)-150,0,255)
    from PIL import ImageFilter
    bl=Image.fromarray(br.astype(np.uint8)).filter(ImageFilter.GaussianBlur(5)).resize(OUT,Image.BILINEAR)
    a=a+np.asarray(bl).astype(np.float32)*.9
    if _vig is None:
        yy,xx=np.mgrid[0:OUT[1],0:OUT[0]]; r=np.sqrt(((xx-540)/540.0)**2+((yy-960)/960.0)**2)
        _vig=(1-.38*np.clip(r-.45,0,1)**1.3*1.6)[:,:,None].astype(np.float32)
    a=a*_vig
    a[:,1:,0]=a[:,:-1,0]*0.5+a[:,1:,0]*0.5; a[:,:-1,2]=a[:,1:,2]*0.5+a[:,:-1,2]*0.5
    rng=np.random.default_rng(seed); a+=rng.normal(0,3.2,a.shape[:2])[:,:,None]
    return Image.fromarray(np.clip(a,0,255).astype(np.uint8))
def whip(prev,cur,p):
    A=np.asarray(prev); B=np.asarray(cur); wd=np.concatenate([A,B],axis=1)
    out=np.zeros_like(A,dtype=np.float32); n=7
    for k in range(n):
        off=int(p*OUT[0]+(k-n//2)*14*math.sin(p*math.pi)); off=max(0,min(OUT[0],off)); out+=wd[:,off:off+OUT[0]].astype(np.float32)
    return Image.fromarray((out/n).astype(np.uint8))
def glitch(im,amount,seed):
    a=np.array(im); rng=np.random.default_rng(seed); h=a.shape[0]
    for _ in range(int(14*amount)):
        y=int(rng.integers(0,h-60)); hh=int(rng.integers(20,160)); a[y:y+hh]=np.roll(a[y:y+hh],int(rng.integers(-180,180)),axis=1)
    a[:,:,0]=np.roll(a[:,:,0],int(14*amount),axis=1); a[:,:,2]=np.roll(a[:,:,2],-int(14*amount),axis=1)
    return Image.fromarray(a)
def frame(i):
    t=i/FPS; idx=0
    for k,s in enumerate(SC):
        if t>=s["start"]: idx=k
    s=SC[idx]; u=t-s["start"]; end=(SC[idx+1]["start"] if idx+1<len(SC) else TOTAL)
    dur=end-s["start"]
    f=render_cam(idx,u,dur,t)
    if idx>0 and u<.32:
        pp=SC[idx-1]; pd=s["start"]-pp["start"]
        prev=render_cam(idx-1,pd,pd,t); f=whip(prev,f,sm(u/.32))
    f=post(f,i)
    g=0
    if idx==0 and u<.5: g=1-u/.5
    if idx==7 and t>TOTAL-1.0: g=(t-(TOTAL-1.0))/1.0
    if g>0: f=glitch(f,g,i)
    f.save(f"fr/f{i:05d}.png",compress_level=1)
    return i
if __name__=="__main__":
    n=int(TOTAL*FPS)
    a=[int(x) for x in sys.argv[1:3]] if len(sys.argv)>2 else [0,n]
    import os; os.makedirs("fr",exist_ok=True)
    with Pool(4) as p:
        for _ in p.imap_unordered(frame,range(a[0],min(a[1],n)),chunksize=4): pass
