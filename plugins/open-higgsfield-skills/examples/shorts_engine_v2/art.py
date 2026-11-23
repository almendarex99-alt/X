import sys
import core, math, random
from core import *
# ---------------- utilidades ----------------
def lerp(a,b,t): return a+(b-a)*t
def mixc(a,b,t): return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))
def gradient(d,y0,y1,c0,c1,steps=24):
    for k in range(steps):
        t=k/(steps-1); y=y0+(y1-y0)*k/steps; d.R(0,y,540,y+(y1-y0)/steps+1,mixc(c0,c1,t),0)
def noise_static(d,x,y,w,h,u,a=200,cell=6):
    n=int(w/cell); m=int(h/cell); seed=int(u*30)
    for i in range(n):
        for j in range(m):
            v=int(60+170*rnd(i*131+j*17+seed*7)); d.R(x+i*cell,y+j*cell,x+i*cell+cell,y+j*cell+cell,(v,v,v,a),0)
def flicker(u,seed=0,rate=9): return 0.55+0.45*(math.sin(u*rate+seed)*math.sin(u*rate*2.3+seed*3)>-.2)
# ---------------- pasillo en perspectiva de un punto ----------------
HY=440
def planes(s): return 270-270*s, 270+270*s, HY-330*s, HY+330*s   # xl,xr,ytop,ybot
def depth(t): return 1.7/(1+0.62*t)
def corridor(d,u,speed=.5,wall=(60,70,80),floor=(40,36,34),ceil=(30,34,40),door=(90,70,50),light=(255,244,200),doors=True,lights=True,n=10,alt=0.0,pulse=1.0):
    near,far=depth(0),depth(n)
    xl,xr,yt,yb=planes(near); xl2,xr2,yt2,yb2=planes(far)
    d.P([(xl,yt),(xr,yt),(xr2,yt2),(xl2,yt2)],ceil+(255,)); d.P([(xl,yb),(xr,yb),(xr2,yb2),(xl2,yb2)],floor+(255,))
    d.P([(xl,yt),(xl2,yt2),(xl2,yb2),(xl,yb)],wall+(255,)); d.P([(xr,yt),(xr2,yt2),(xr2,yb2),(xr,yb)],tuple(int(c*.85) for c in wall)+(255,))
    d.R(xl2,yt2,xr2,yb2,(8,8,12),0)
    off=(u*speed+alt)%1.0
    for k in range(n,-1,-1):
        t=k+1-off; 
        if t<0.05: continue
        s=depth(t); s2=depth(t+.5); xa,xb,ya,yb_=planes(s); xc,xd,yc,yd=planes(s2)
        shade=clamp(1.1-(t/n))
        # lineas de cruce (cuadricula del suelo/techo)
        d.L(xa,yb_,xb,yb_,(0,0,0,int(60*shade)),2); d.L(xa,ya,xb,ya,(0,0,0,int(40*shade)),2)
        if doors and k%2==0:
            for side in(-1,1):
                if side<0: x1,x2=xa,xc
                else: x1,x2=xb,xd
                dh=250
                d.P([(x1,yb_),(x2,yd),(x2,yd-dh*s2),(x1,yb_-dh*s)],tuple(int(c*(.5+.5*shade)) for c in door)+(255,))
                d.P([(x1,yb_-dh*s),(x2,yd-dh*s2),(x2,yd-dh*s2+8*s2),(x1,yb_-dh*s+10*s)],(0,0,0,60))
        if lights:
            lw=70*s; d.P([(270-lw,ya+2),(270+lw,ya+2),(270+lw*.8,ya+8*s),(270-lw*.8,ya+8*s)],light+(int(255*shade*pulse),))
            d.E(270,ya+30*s,150*s,40*s,light+(int(36*shade*pulse),))
def silhouette(d,x,y,sc,col=(8,8,12),arms=True,head=1.0,lantern=False):
    d.E(x,y-148*sc,15*sc*head,17*sc*head,col+(255,)); d.R(x-20*sc,y-132*sc,x+20*sc,y-62*sc,col+(255,),10*sc)
    d.R(x-16*sc,y-66*sc,x-3*sc,y,col+(255,),5*sc); d.R(x+3*sc,y-66*sc,x+16*sc,y,col+(255,),5*sc)
    if arms: d.R(x-30*sc,y-130*sc,x-20*sc,y-76*sc,col+(255,),5*sc); d.R(x+20*sc,y-130*sc,x+30*sc,y-76*sc,col+(255,),5*sc)
def tallman(d,x,y,sc,u,suit=(10,10,14),tie=(150,20,28)):
    """figura alta sin rostro, de traje"""
    d.E(x,y-262*sc,15*sc,19*sc,(226,224,218)); 
    d.R(x-18*sc,y-244*sc,x+18*sc,y-104*sc,suit+(255,),9*sc); d.P([(x-5*sc,y-244*sc),(x+5*sc,y-244*sc),(x,y-196*sc)],(230,230,236)); d.R(x-3*sc,y-230*sc,x+3*sc,y-170*sc,tie,2*sc)
    d.R(x-14*sc,y-110*sc,x-3*sc,y,suit+(255,),4*sc); d.R(x+3*sc,y-110*sc,x+14*sc,y,suit+(255,),4*sc)
    d.R(x-28*sc,y-240*sc,x-18*sc,y-86*sc,suit+(255,),4*sc); d.R(x+18*sc,y-240*sc,x+28*sc,y-86*sc,suit+(255,),4*sc)
def fogband(d,u,y0,y1,col=(150,160,175),a=40,n=9):
    for k in range(n):
        x=(rnd(k,2)*700+u*(10+k*3)*(1 if k%2 else -1))%700-80; y=y0+(y1-y0)*rnd(k,3)
        d.E(x,y,190+rnd(k,4)*120,28+rnd(k,5)*28,col+(a,))
def flashlight(d,x,y,tx,ty,spread=.38,L=520,a=90,col=(255,244,200)):
    ang=math.atan2(ty-y,tx-x)
    for k in range(4):
        sp=spread*(1-k*.18); 
        d.P([(x,y),(x+math.cos(ang-sp)*L,y+math.sin(ang-sp)*L),(x+math.cos(ang+sp)*L,y+math.sin(ang+sp)*L)],col+(int(a*(.35+k*.2)),))
def forest(d,u,sky=(16,22,40),sky2=(40,50,74),ground=(10,14,12),fog=(150,170,190),dense=14,moon=True,sway=1.0):
    gradient(d,0,600,sky,sky2)
    if moon: d.E(410,150,40,40,(236,240,226,230)); d.E(410,150,86,86,(236,240,226,40))
    stars(d,u,40,300)
    d.R(0,600,540,960,ground+(255,),0)
    for layer in range(3):
        sc=.55+layer*.3; base=560+layer*80
        for i in range(dense):
            x=(i*(540/dense*1.1)+rnd(i,layer)*40)%560-10; w=14*sc*(1+rnd(i,3)); h=(520+layer*160)
            col=mixc((18,26,24),(4,6,6),layer/2.0)
            sw=math.sin(u*.8+i)*3*sway
            d.P([(x-w,base),(x+w,base),(x+w*.6+sw,base-h),(x-w*.6+sw,base-h)],col+(255,))
            for b in range(3):
                by=base-h*(.35+.18*b); d.L(x,by,x+(40+b*10)*(1 if (i+b)%2 else -1)*sc,by-30*sc,col+(255,),3*sc)
        fogband(d,u,base-200,base-20,fog,22+layer*10)
def cctv(d,x,y,w,h,u,inner=None,rec=True,static=.15):
    bevel(d,x,y,x+w,y+h,(34,34,40),6); d.R(x+6,y+6,x+w-6,y+h-6,(8,10,10),3)
    if inner: inner(d,x+6,y+6,w-12,h-12)
    for k in range(int((h-12)/5)): d.R(x+6,y+6+k*5,x+w-6,y+7+k*5,(0,0,0,60))
    if static>0: noise_static(d,x+6,y+6,w-12,h-12,u,int(255*static),4)
    if rec and int(u*2)%2==0: d.E(x+w-18,y+16,4,4,(240,40,40))
def bear(d,x,y,sc,u,eyes=(255,255,255),glow=0.0,arms_up=0.0,tint=(124,82,52)):
    """oso animatronico original: cuerpo, cabeza con orejas, hocico, sombrero de copa y pajarita"""
    sh=tuple(int(c*.7) for c in tint)
    shadow(d,x,y+4,60*sc,8*sc,90)
    d.R(x-48*sc,y-170*sc,x+48*sc,y-40*sc,tint+(255,),30*sc); d.E(x,y-100*sc,34*sc,48*sc,(200,160,120))
    for sg in(-1,1): d.R(x+sg*48*sc-14*sc,y-160*sc-arms_up*70*sc,x+sg*48*sc+14*sc,y-84*sc-arms_up*70*sc,tint+(255,),10*sc)
    for sg in(-1,1): d.R(x+sg*22*sc-16*sc,y-48*sc,x+sg*22*sc+16*sc,y,sh+(255,),8*sc)
    hy=y-222*sc
    for sg in(-1,1): d.E(x+sg*40*sc,hy-30*sc,18*sc,18*sc,tint+(255,)); d.E(x+sg*40*sc,hy-30*sc,10*sc,10*sc,(60,36,24))
    d.E(x,hy,46*sc,44*sc,tint+(255,)); d.E(x,hy+14*sc,28*sc,20*sc,(214,176,136))
    d.E(x,hy+8*sc,7*sc,5*sc,(20,14,12))
    for sg in(-1,1):
        d.E(x+sg*17*sc,hy-8*sc,10*sc,10*sc,(20,20,24)); d.E(x+sg*17*sc,hy-8*sc,4*sc,4*sc,eyes)
        if glow>0: d.E(x+sg*17*sc,hy-8*sc,20*sc,20*sc,eyes+(int(70*glow),))
    d.A(x,hy+16*sc,14*sc,8*sc,10,170,(30,20,18),3*sc)
    d.R(x-30*sc,hy-62*sc,x+30*sc,hy-44*sc,(18,18,22),4*sc); d.R(x-20*sc,hy-100*sc,x+20*sc,hy-60*sc,(18,18,22),4*sc); d.R(x-20*sc,hy-70*sc,x+20*sc,hy-62*sc,(30,30,36),2*sc)
    d.P([(x-20*sc,y-170*sc),(x,y-160*sc),(x-20*sc,y-150*sc)],(14,14,18)); d.P([(x+20*sc,y-170*sc),(x,y-160*sc),(x+20*sc,y-150*sc)],(14,14,18)); d.E(x,y-160*sc,5*sc,5*sc,(30,30,36))
# ---------------- mar / cine ----------------
def ocean(d,u,hz=470,sky=(120,170,220),sky2=(200,225,245),sea=(18,70,110),sea2=(6,28,56)):
    gradient(d,0,hz,sky,sky2); gradient(d,hz,960,sea,sea2)
    d.E(400,hz-120,40,40,(255,246,200,230)); d.E(400,hz-120,80,80,(255,246,200,60))
    for k in range(18):
        y=hz+6+k*k*1.55; amp=3+k*.9; per=34+k*7
        pts=[(x,y+math.sin(x/per*2+u*1.6+k)*amp) for x in range(-20,580,18)]
        for i in range(len(pts)-1): d.L(pts[i][0],pts[i][1],pts[i+1][0],pts[i+1][1],(255,255,255,int(20+k*5)),1.5+k*.12)
def glints(d,u,hz,n=60,col=(255,255,235)):
    for k in range(n):
        x=(rnd(k)*560+u*10*(1+rnd(k,3)))%560; y=hz+14+rnd(k,1)*(960-hz-30)*rnd(k,4)
        t=.5+.5*math.sin(u*5+k*1.7)
        if t>.55: d.L(x,y,x+8+rnd(k,5)*16,y,col+(int(210*t),),1.6+y/500.0)
def wave_y(x,u,y,amp,per,k=0): return y+math.sin(x/per*2+u*1.6+k)*amp
def barrel(d,x,y,sc,u):
    by=y+math.sin(u*1.7+x)*3*sc; d.E(x,by+16*sc,22*sc,6*sc,(0,0,0,70))
    d.R(x-16*sc,by-22*sc,x+16*sc,by+16*sc,(236,190,30),8*sc); d.R(x-16*sc,by-8*sc,x+16*sc,by-2*sc,(190,140,20),0); d.R(x-16*sc,by+6*sc,x+16*sc,by+12*sc,(190,140,20),0)
    d.R(x-12*sc,by-20*sc,x-6*sc,by+14*sc,(255,255,255,70),3*sc)
def fin(d,x,y,sc,u,col=(60,66,76)):
    d.P([(x-18*sc,y),(x+22*sc,y),(x+4*sc,y-60*sc)],col+(255,)); d.P([(x-18*sc,y),(x-6*sc,y-40*sc),(x+4*sc,y-60*sc),(x+10*sc,y)],(86,92,104))
    for k in range(3): d.E(x-30*sc-k*26*sc,y+4*sc,36*sc,5*sc,(255,255,255,70-k*18))
def clapper(d,x,y,sc,open_=0.0,txt=0):
    d.R(x-60*sc,y-30*sc,x+60*sc,y+50*sc,(24,24,28),4*sc); d.R(x-60*sc,y-30*sc,x+60*sc,y-22*sc,(255,255,255,40),4*sc)
    for k in range(4): d.R(x-54*sc+k*28*sc,y+6*sc,x-30*sc+k*28*sc,y+8*sc,(255,255,255,200),1)
    # pala articulada
    ang=-open_*.5
    pts=[(x-60*sc,y-30*sc),(x+60*sc,y-30*sc),(x+60*sc,y-52*sc),(x-60*sc,y-52*sc)]
    pts=rotpts(pts,x-60*sc,y-30*sc,ang); d.P(pts,(24,24,28))
    for k in range(6):
        q=[(x-60*sc+k*20*sc,y-30*sc),(x-60*sc+k*20*sc+10*sc,y-30*sc),(x-60*sc+k*20*sc+10*sc+6*sc,y-52*sc),(x-60*sc+k*20*sc+6*sc,y-52*sc)]
        d.P(rotpts(q,x-60*sc,y-30*sc,ang),(240,240,240))
def film_camera(d,x,y,sc,u):
    shadow(d,x,y+3,70*sc,8*sc,70)
    for sg in(-1,1): d.L(x,y-120*sc,x+sg*60*sc,y,(50,50,58),7*sc)
    d.L(x,y-120*sc,x,y,(60,60,68),7*sc)
    bevel(d,x-50*sc,y-210*sc,x+44*sc,y-130*sc,(40,42,50),8*sc)
    for k,(rx,ry) in enumerate([(-22,-246),(16,-246)]):
        d.E(x+rx*sc,y+ry*sc,28*sc,28*sc,(30,32,40)); d.E(x+rx*sc,y+ry*sc,28*sc,28*sc,None,(80,84,96),2*sc)
        for q in range(3): a=u*4+q*2.09+k; d.L(x+rx*sc,y+ry*sc,x+rx*sc+math.cos(a)*22*sc,y+ry*sc+math.sin(a)*22*sc,(190,194,204),2*sc)
    d.R(x+44*sc,y-196*sc,x+86*sc,y-150*sc,(24,26,32),5*sc); d.E(x+88*sc,y-173*sc,14*sc,22*sc,(20,22,30)); d.E(x+88*sc,y-173*sc,8*sc,13*sc,(90,120,170))
def film_strip(d,y,u,h=90,col=(18,18,22),a=255):
    d.R(0,y,540,y+h,col+(a,),0)
    for k in range(-1,10):
        x=k*64+(u*60)%64; d.R(x+6,y+8,x+20,y+22,(230,230,230),3); d.R(x+6,y+h-22,x+20,y+h-8,(230,230,230),3)
    for k in range(-1,6): 
        x=k*110+(u*60)%110; d.R(x+16,y+26,x+104,y+h-26,(60,66,80),2)
def door_swing(d,cx,by,w,h,openp,col=(90,60,40),light=(255,220,150)):
    d.R(cx-w/2-8,by-h-8,cx+w/2+8,by,(30,24,20),3)
    d.R(cx-w/2,by-h,cx+w/2,by,(10,8,10),0)
    if openp>0: d.R(cx-w/2,by-h,cx+w/2,by,light+(int(180*openp),),0)
    ww=w*max(.06,math.cos(openp*1.35)); sk=h*0.06*math.sin(openp*1.35)
    d.P([(cx-w/2,by-h),(cx-w/2+ww,by-h+sk),(cx-w/2+ww,by-sk),(cx-w/2,by)],col+(255,))
    d.E(cx-w/2+ww*.84,by-h*.46,4,4,(230,200,100))
def shower(d,u,bw=True):
    d.R(0,0,540,960,(176,176,176)); 
    for r in range(24):
        for c in range(14): d.R(c*40,r*40,c*40+38,r*40+38,(204,204,204),2); d.R(c*40,r*40,c*40+38,r*40+4,(255,255,255,60),2)
    d.R(0,0,540,960,(0,0,0,60),0)
    d.R(210,36,330,60,(120,120,126),8); d.R(262,0,278,40,(120,120,126),0); d.E(270,64,50,12,(150,150,156))
    for k in range(40):
        x=210+rnd(k)*120; ty=(u*620+rnd(k,2)*900)%900; d.L(x,70+ty,x-2,86+ty,(255,255,255,190),2)
def vh(d,u,a=40):
    for k in range(4): d.R(0,((u*80)+k*240)%960,540,((u*80)+k*240)%960+3,(255,255,255,a),0)

DIGS={0:"abcdef",1:"bc",2:"abdeg",3:"abcdg",4:"bcfg",5:"acdfg",6:"acdefg",7:"abc",8:"abcdefg",9:"abcdfg"}
def seg7(d,x,y,w,h,digit,col,off=(40,40,40)):
    S7=DIGS[digit]; t=w*.2
    seg={'a':(x+t,y,x+w-t,y+t),'b':(x+w-t,y+t,x+w,y+h/2-t/2),'c':(x+w-t,y+h/2+t/2,x+w,y+h-t),'d':(x+t,y+h-t,x+w-t,y+h),'e':(x,y+h/2+t/2,x+t,y+h-t),'f':(x,y+t,x+t,y+h/2-t/2),'g':(x+t,y+h/2-t/2,x+w-t,y+h/2+t/2)}
    for k,(a,b,c,e) in seg.items(): d.R(a,b,c,e,col+((255,) if k in S7 else (off[0],)),1.5)
def number(d,x,y,n,digits,w,h,col,gap=8):
    s=str(int(n)).zfill(digits)
    for i,ch in enumerate(s): seg7(d,x+i*(w+gap),y,w,h,int(ch),col)

F35={"+":["...",".#.","###",".#.","..."],"Q":["###","#.#","#.#","###","..#"],"$":[".#.","###","##.",".##","###"],"-":["...","...","###","...","..."],"!":[".#.",".#.",".#.","...",".#."],"?":["###","..#",".##","...",".#."],"Z":["###","..#",".#.","#..","###"],"J":["..#","..#","..#","#.#","###"],"A":["###","#.#","###","#.#","#.#"],"B":["##.","#.#","##.","#.#","##."],"C":["###","#..","#..","#..","###"],"D":["##.","#.#","#.#","#.#","##."],"E":["###","#..","##.","#..","###"],"F":["###","#..","##.","#..","#.."],"G":["###","#..","#.#","#.#","###"],"H":["#.#","#.#","###","#.#","#.#"],"I":["###",".#.",".#.",".#.","###"],"K":["#.#","#.#","##.","#.#","#.#"],"L":["#..","#..","#..","#..","###"],"M":["#.#","###","###","#.#","#.#"],"N":["##.","#.#","#.#","#.#","#.#"],"O":["###","#.#","#.#","#.#","###"],"P":["###","#.#","###","#..","#.."],"R":["##.","#.#","##.","#.#","#.#"],"S":["###","#..","###","..#","###"],"T":["###",".#.",".#.",".#.",".#."],"U":["#.#","#.#","#.#","#.#","###"],"V":["#.#","#.#","#.#","#.#",".#."],"W":["#.#","#.#","###","###","#.#"],"X":["#.#","#.#",".#.","#.#","#.#"],"Y":["#.#","#.#",".#.",".#.",".#."],"0":["###","#.#","#.#","#.#","###"],"1":[".#.","##.",".#.",".#.","###"],"2":["###","..#","###","#..","###"],"3":["###","..#","###","..#","###"],"4":["#.#","#.#","###","..#","..#"],"5":["###","#..","###","..#","###"],"6":["###","#..","###","#.#","###"],"7":["###","..#","..#","..#","..#"],"8":["###","#.#","###","#.#","###"],"9":["###","#.#","###","..#","###"],":":["...",".#.","...",".#.","..."],"%":["#.#","..#",".#.","#..","#.#"]," ":["...","...","...","...","..."],".":["...","...","...","...",".#."]}
def ptext(d,x,y,txt,cell,col=(255,255,255),a=255):
    for i,ch in enumerate(txt.upper()):
        for r,row in enumerate(F35.get(ch,F35[" "])):
            for c,v in enumerate(row):
                if v=="#": d.R(x+(i*4+c)*cell,y+r*cell,x+(i*4+c)*cell+cell,y+r*cell+cell,col+(a,),0)
