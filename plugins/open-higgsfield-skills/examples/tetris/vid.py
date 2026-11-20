import sys; sys.path.insert(0,"..")
import core, math, random
from core import *
COL={'I':(0,225,240),'O':(255,220,40),'T':(176,80,235),'S':(84,222,92),'Z':(242,62,72),'J':(64,104,244),'L':(255,150,44)}
SH={'I':[(0,0),(0,1),(0,2),(0,3)],'O':[(0,0),(0,1),(1,0),(1,1)],'T':[(0,1),(1,0),(1,1),(1,2)],'S':[(0,1),(0,2),(1,0),(1,1)],'Z':[(0,0),(0,1),(1,1),(1,2)],'J':[(0,0),(1,0),(1,1),(1,2)],'L':[(0,2),(1,0),(1,1),(1,2)]}
def norm(c):
    mr=min(r for r,_ in c); mc=min(x for _,x in c); return sorted((r-mr,x-mc) for r,x in c)
def rots(k):
    out=[norm(SH[k])]
    for _ in range(3):
        n=norm([(x,-r) for r,x in out[-1]])
        if n not in out: out.append(n)
    return out
RO={k:rots(k) for k in SH}
def fits(b,cells,y,x):
    for r,c in cells:
        yy,xx=y+r,x+c
        if xx<0 or xx>=10 or yy>=20: return False
        if yy>=0 and b[yy][xx]: return False
    return True
def drop(b,cells,x):
    y=-2
    if not fits(b,cells,y,x): return None
    while fits(b,cells,y+1,x): y+=1
    return y
def place(b,cells,y,x,k):
    nb=[row[:] for row in b]
    for r,c in cells: nb[y+r][x+c]=k
    return nb
def score(b):
    hs=[]; holes=0
    for c in range(10):
        h=0
        for r in range(20):
            if b[r][c]: h=20-r; break
        hs.append(h)
        seen=False
        for r in range(20):
            if b[r][c]: seen=True
            elif seen: holes+=1
    bump=sum(abs(hs[i]-hs[i+1]) for i in range(9))
    return -0.51*sum(hs)-0.36*holes-0.18*bump,hs
def clear(b):
    full=[r for r in range(20) if all(b[r])]
    nb=[row for i,row in enumerate(b) if i not in full]
    nb=[[None]*10 for _ in full]+nb
    return nb,full
def simulate(seed,n,rate=11.0):
    rnd_=random.Random(seed); bag=[]; b=[[None]*10 for _ in range(20)]; t=0.0; P=[]; lines=0
    for i in range(n):
        if not bag: bag=list(SH); rnd_.shuffle(bag)
        k=bag.pop(); best=None
        for ri,cells in enumerate(RO[k]):
            w=max(c for _,c in cells)+1
            for x in range(10-w+1):
                y=drop(b,cells,x)
                if y is None: continue
                nb=place(b,cells,y,x,k); ncl,full=clear(nb); s,_=score(ncl); s+=0.76*len(full)*3
                if best is None or s>best[0]: best=(s,ri,x,y,nb,ncl,full)
        if best is None: b=[[None]*10 for _ in range(20)]; continue
        s,ri,x,y,nb,ncl,full=best; dx=abs(x-3); tf=max(y/rate,.2+.08*dx+.1,.08*ri+.1)+.08
        P.append(dict(k=k,ri=ri,x=x,y=y,t0=t,tl=t+tf,before=[r[:] for r in b],lock=nb,after=ncl,full=full,lines=lines,rate=rate))
        lines+=len(full); b=ncl; t=t+tf+(.55 if full else .1)
    return P
def block(d,x,y,s,col,a=255):
    d.R(x,y,x+s,y+s,col+(a,),3); d.R(x+1,y+1,x+s-1,y+s*.45,(255,255,255,70),3); d.R(x+1,y+s*.6,x+s-1,y+s-1,(0,0,0,70),3); d.R(x+s*.18,y+s*.18,x+s*.46,y+s*.34,(255,255,255,120),2)
def board_state(P,t):
    # indice de la pieza actual
    i=0
    for k,p in enumerate(P):
        if t>=p["t0"]: i=k
    return i
def draw_board(d,P,t,x0,y0,cell,total_t=None,mono=False,frame=True):
    CC=(lambda k:{'I':(15,56,15),'O':(48,98,48),'T':(15,56,15),'S':(48,98,48),'Z':(15,56,15),'J':(48,98,48),'L':(15,56,15)}[k]) if mono else (lambda k:COL[k])
    if total_t is None: total_t=P[-1]["tl"]
    t=t%(total_t+.3) if t>total_t else t
    i=board_state(P,t); p=P[i]
    if frame:
        d.R(x0-6,y0-6,x0+10*cell+6,y0+20*cell+6,(18,20,44),8); d.R(x0,y0,x0+10*cell,y0+20*cell,(6,8,22))
        for r in range(21): d.L(x0,y0+r*cell,x0+10*cell,y0+r*cell,(255,255,255,10),1)
        for c in range(11): d.L(x0+c*cell,y0,x0+c*cell,y0+20*cell,(255,255,255,10),1)
    if t<p["tl"]: b=p["before"]
    else:
        b=p["lock"]
    dt=t-p["tl"]
    full=p["full"]
    for r in range(20):
        for c in range(10):
            k=b[r][c]
            if not k: continue
            if t>=p["tl"] and full:
                if r in full:
                    if dt<.3:
                        if int(dt*20)%2==0: block(d,x0+c*cell,y0+r*cell,cell,(255,255,255))
                        else: block(d,x0+c*cell,y0+r*cell,cell,CC(k))
                        continue
                    else: continue
                else:
                    sh=sum(1 for f in full if f>r)
                    if dt>=.3: 
                        q=sm((dt-.3)/.2)
                        block(d,x0+c*cell,y0+(r+sh*q)*cell,cell,CC(k)); continue
            block(d,x0+c*cell,y0+r*cell,cell,CC(k))
    if t<p["tl"]:
        cells=RO[p["k"]][p["ri"]]
        w=max(c for _,c in cells)+1
        ru=min(p["ri"],int((t-p["t0"])/.08)); cr=RO[p["k"]][ru]
        step=int(max(0,t-p["t0"]-.2)/.08); tx=p["x"]; sx=3
        cx=sx+max(-step,min(step,tx-sx)) if tx!=sx else sx
        yy=min(p["y"],(t-p["t0"])*p["rate"])
        # sombra de aterrizaje
        for r,c in cells: d.R(x0+(p["x"]+c)*cell+2,y0+(p["y"]+r)*cell+2,x0+(p["x"]+c+1)*cell-2,y0+(p["y"]+r+1)*cell-2,None,3,CC(p["k"])+(120,),1.5)
        for r,c in cr: block(d,x0+(cx+c)*cell,y0+(yy+r)*cell,cell,CC(p["k"]))
    if full and 0<=dt<.45:
        for j,r in enumerate(full):
            for c in range(10):
                a=dt*3; d.E(x0+c*cell+cell/2+math.cos(c*1.7+j)*dt*90,y0+r*cell+cell/2+math.sin(c*2.3)*dt*40+ dt*dt*160,cell*.2,cell*.2,(255,240,150,int(255*(1-dt/.45))))
    return i,p
SIM=simulate(7,70)
SIMF=simulate(11,90,rate=14.0)
def seg7(d,x,y,w,h,digit,col):
    S7={0:"abcdef",1:"bc",2:"abdeg",3:"abcdg",4:"bcfg",5:"acdfg",6:"acdefg",7:"abc",8:"abcdefg",9:"abcdfg"}[digit]
    t=w*.18
    seg={'a':(x+t,y,x+w-t,y+t),'b':(x+w-t,y+t,x+w,y+h/2-t/2),'c':(x+w-t,y+h/2+t/2,x+w,y+h-t),'d':(x+t,y+h-t,x+w-t,y+h),'e':(x,y+h/2+t/2,x+t,y+h-t),'f':(x,y+t,x+t,y+h/2-t/2),'g':(x+t,y+h/2-t/2,x+w-t,y+h/2+t/2)}
    for k,(a,b,c,e) in seg.items(): d.R(a,b,c,e,col+((255,) if k in S7 else (40,)),1.5)
def number(d,x,y,n,digits,w,h,col):
    s=str(int(n)).zfill(digits)
    for i,ch in enumerate(s): seg7(d,x+i*(w+8),y,w,h,int(ch),col)
def nextbox(d,x,y,k,cell=16):
    d.R(x,y,x+90,y+80,(18,20,44),8); cells=RO[k][0]
    for r,c in cells: block(d,x+14+c*cell,y+16+r*cell,cell,COL[k])
# ----- escenas -----
def sceneA(u,final=False):
    im=new((6,8,30),(30,10,58)); d=D(im)
    for k in range(14):
        kk=list(SH)[k%7]; x=(rnd(k)*500+20); y=(960-((u*30*(0.5+rnd(k,2))+rnd(k,3)*960)%1100)+60)
        for r,c in RO[kk][k%len(RO[kk])]: block(d,x+c*18,y+r*18,18,COL[kk],70)
    d.E(270,520,230,70,(80,60,255,40))
    t=u*1.0+ (6 if final else 0)
    d.R(24,150,516,850,(24,20,52),24); d.R(24,150,516,156,(255,255,255,24),24); d.R(24,150,516,850,None,24,(110,90,255,90),3)
    i,p=draw_board(d,SIM,t,84,200,30)
    lines=p["lines"]+(len(p["full"]) if t>=p["tl"] else 0)
    d.R(398,200,498,284,(18,20,44),8); number(d,404,218,lines*100,4,14,32,(80,255,140))
    nextbox(d,404,310,SIM[(i+1)%len(SIM)]["k"])
    shadow(d,270,880,180,14,80)
    return im
def sceneB(u):
    im=new((10,14,36),(40,50,86)); d=D(im)
    # ventana nevada con ciudad
    bevel(d,50,60,490,330,(60,50,60),12); d.R(62,72,478,318,(28,40,86))
    stars(d,u,30,300)
    d.E(420,110,24,24,(250,244,220,230))
    for k,(x,h,w) in enumerate([(70,120,50),(130,170,40),(180,100,56),(250,150,36),(300,210,60),(380,130,48),(430,100,40)]):
        d.R(62+x-60,318-h,62+x-60+w,318,(16,20,44)); 
        for r in range(int(h/26)):
            for c in range(int(w/16)):
                if rnd(k*9+r*3+c)>.5: d.R(66+x-60+c*16,324-h+r*26,74+x-60+c*16,334-h+r*26,(255,220,120,220),1)
    # cupulas estilo ruso (siluetas)
    for x,hh in((196,70),(246,92),(296,66)):
        d.R(x-9,318-60-hh*.5,x+9,318,(110,84,124)); dc=[(200,50,60),(60,150,90),(230,190,70)][int(x/50)%3]; d.E(x,318-60-hh*.5,18,24,dc)
        for kk in range(4): d.A(x,318-60-hh*.5,18,24,200+kk*30,230+kk*30,(255,255,255,90),2)
        d.L(x,318-60-hh*.5-26,x,318-60-hh*.5-44,(230,200,90),3)
    d.R(0,330,540,960,(40,32,56))
    for k in range(60):
        x=(rnd(k,5)*560+math.sin(u*1.3+k)*14+u*18)%560-10; y=(rnd(k,6)*300+u*(30+rnd(k,7)*30))%300+70
        d.E(x,y,2.2,2.2,(255,255,255,200))
    # radiador, estantes, reloj
    d.R(20,560,120,720,(70,66,90),6)
    for k in range(7): d.R(28+k*13,568,36+k*13,712,(100,96,124),3)
    d.E(450,420,28,28,(240,238,230)); d.E(450,420,28,28,None,(60,50,40),3); ang=u*.4
    d.L(450,420,450+math.cos(ang)*18,420+math.sin(ang)*18,(40,30,30),3); d.L(450,420,450+math.cos(ang*12)*24,420+math.sin(ang*12)*24,(40,30,30),2)
    # escritorio y monitor verde
    bevel(d,40,640,500,700,(110,74,52),6); d.R(60,700,80,860,(80,52,38),3); d.R(460,700,480,860,(80,52,38),3)
    box=crt(d,140,392,260,214,(2,18,8),(196,188,160))
    x0,y0,x1,y1=box; G=(90,255,130)
    cw,ch=11,12; bx=x0+(x1-x0)/2-5*cw; by=y0+14
    def br(x,y,col=G):
        d.R(x+1,y+1,x+3,y+ch-1,col+(255,),0); d.R(x+1,y+1,x+5,y+3,col+(255,),0); d.R(x+1,y+ch-3,x+5,y+ch-1,col+(255,),0)
        d.R(x+cw-3,y+1,x+cw-1,y+ch-1,col+(255,),0); d.R(x+cw-5,y+1,x+cw-1,y+3,col+(255,),0); d.R(x+cw-5,y+ch-3,x+cw-1,y+ch-1,col+(255,),0)
    for r in range(13):
        d.R(bx-9,by+r*ch,bx-7,by+r*ch+ch-2,G+(255,),0); d.R(bx-5,by+r*ch+2,bx-3,by+r*ch+ch-4,G+(255,),0)
        d.R(bx+10*cw+5,by+r*ch,bx+10*cw+7,by+r*ch+ch-2,G+(255,),0); d.R(bx+10*cw+1,by+r*ch+2,bx+10*cw+3,by+r*ch+ch-4,G+(255,),0)
    for c in range(10): d.R(bx+c*cw+2,by+13*ch+1,bx+c*cw+cw-2,by+13*ch+4,G+(255,),0)
    stack=[(12,0),(12,1),(12,2),(12,3),(12,5),(12,6),(12,7),(12,8),(12,9),(11,1),(11,2),(11,3),(11,6),(11,7),(11,8),(10,2),(10,7)]
    for r,c in stack: br(bx+c*cw,by+r*ch)
    kk=["T","L","S","J"][int(u*.5)%4]; yy=int((u*3.2)%10)
    for r,c in RO[kk][int(u*1.3)%len(RO[kk])]: br(bx+(3+c)*cw,by+(yy+r)*ch)
    d.R(x0+8,y0+8,x0+14,y0+14,G+(255,),0)
    crt_fx(d,box)
    d.R(150,640,390,664,(176,168,142),4); d.R(150,640,390,646,(255,255,255,40),4)
    for r in range(2):
        for c in range(16): d.R(160+c*14,648+r*8,170+c*14,654+r*8,(60,56,70),1)
    mug(d,420,610,u,(220,230,250))
    # programador de espaldas con gafas (se ve el perfil)
    person_back(d,270,640,1.25,0,u)
    # papeles
    d.R(66,620,110,642,(250,248,238),2); d.L(70,628,104,628,(0,0,0,60),2); d.L(70,634,96,634,(0,0,0,60),2)
    return im
def sceneC(u):
    im=new((14,10,40),(34,16,62)); d=D(im)
    stars(d,u,40,300)
    keys=list(SH); 
    for n,k in enumerate(keys):
        col=n%4; row=n//4; cx=90+col*120; cy=240+row*260
        # cuatro cuadrados vuelan y se ensamblan
        for j,(r,c) in enumerate(RO[k][0]):
            ts=n*.7+j*.12; p=sm((u-ts)/.5)
            sx=cx+(rnd(n*5+j)-.5)*500; sy=-60-rnd(n*5+j,3)*100
            tx=cx+c*34-34; ty=cy+r*34-20 + (0 if u<n*.7+1.2 else 0)
            rot=(1-p)*4
            x=sx+(tx-sx)*p; y=sy+(ty-sy)*p; 
            if p>=1: y+=math.sin((u-ts-.5)*10)*3*max(0,1-(u-ts-.5)*1.5)
            block(d,x,y,34,COL[k])
    for r in range(30): d.L(0,r*32,540,r*32,(255,255,255,7),1)
    for c in range(18): d.L(c*32,0,c*32,960,(255,255,255,7),1)
    a=sm((u-5.0)/1.5)
    for r,c in [(0,0),(0,3),(1,0),(1,3),(2,0),(2,1),(2,2),(2,3),(3,3),(4,3)]:
        xx=96+c*84; yy=560+r*66; cc=(255,255,255)
        if a>0: block(d,xx,yy,76,[(0,225,240),(255,220,40),(176,80,235),(84,222,92),(242,62,72)][(r+c)%5],int(235*a))
    return im
def sceneD(u):
    im=new((90,170,230),(190,230,255)); d=D(im)
    d.E(430,120,46,46,(255,240,170)); d.E(430,120,86,86,(255,240,170,50))
    for k in range(3): d.E(90+k*150+(u*8)%40,110+k*36,52,16,(255,255,255,190))
    d.R(0,600,540,960,(52,150,92)); d.R(0,600,540,606,(255,255,255,30))
    d.R(0,640,540,900,(40,110,170)); d.R(0,640,540,646,(255,255,255,60))
    for k in range(9): d.L(0,660+k*26,540,660+k*26,(255,255,255,26),2)
    d.R(20,858,520,864,(255,255,255,200)); d.R(262,770,278,862,(230,230,230,255),2); 
    d.R(150,776,262,862,(240,240,240,40),2); d.R(278,776,390,862,(240,240,240,40),2)
    d.R(150,770,390,778,(255,255,255,235),3)
    for k in range(7): d.L(150,778+k*12,390,778+k*12,(40,40,40,110),1.4)
    for k in range(20): d.L(150+k*12,778,150+k*12,862,(40,40,40,110),1.4)
    # pelota con fisica: parabolas entre los dos jugadores con rebote en el suelo
    per=2.4; ph=(u%per)/per; leg=int(u/per)%2
    x0,x1=110,430
    if leg: x0,x1=x1,x0
    bx=x0+(x1-x0)*ph
    # primera mitad: vuelo hacia el suelo, rebote, segunda mitad
    if ph<.5: q=ph/.5; by=800-0*q-math.sin(q*math.pi)*0; by=700+ (860-700)*q*q-60*math.sin(q*math.pi)*0
    g=858; 
    if ph<.5:
        q=ph/.5; by=450+(g-450)*q*q
    else:
        q=(ph-.5)/.5; by=g-(g-380)*(1-(1-q)**2)*1.0 if False else g-(g-470)*4*q*(1-q)*2*(1-0)
        by=g-(g-420)*(1-(2*q-1)**2)
    shadow(d,bx,872,18,4,60)
    for tt in range(5): 
        qq=ph-tt*.012; 
    d.E(bx,by,15,15,(215,240,60)); d.A(bx,by,15,15,-40,70,(255,255,255),3); d.A(bx,by,15,15,140,250,(255,255,255),3)
    # jugadores con raqueta
    for side,px in((0,70),(1,470)):
        hit=abs(ph-(0 if (leg==0)==(side==0) else 0))<0
        sw=math.sin(ph*math.pi*2)*0
        shirt=(230,80,100) if side==0 else (70,120,220)
        shadow(d,px,872,30,5,70)
        d.R(px-24,740,px+24,830,shirt,12); d.E(px,716,20,22,SK); d.E(px,706,23,13,(60,40,30)); d.E(px-7,716,2.6,3,(30,30,40)); d.E(px+7,716,2.6,3,(30,30,40)); d.A(px,724,6,4,20,160,(110,40,40),2)
        d.R(px-20,826,px-5,866,(60,60,90),4); d.R(px+5,826,px+20,866,(60,60,90),4); d.R(px-24,860,px-3,870,(240,240,240),4); d.R(px+3,860,px+24,870,(240,240,240),4)
        sgn=1 if side==0 else -1
        swing=0
        if (side==0 and ((leg==0 and ph<.08) or (leg==1 and ph>.92))) or (side==1 and ((leg==1 and ph<.08) or (leg==0 and ph>.92))): swing=1
        ang=-.6+swing*1.2
        ra=rotpts([(px+sgn*30,690),(px+sgn*36,690),(px+sgn*36,780),(px+sgn*30,780)],px+sgn*20,780,ang*sgn); d.P(ra,(80,60,40))
        hx=px+sgn*20+(px+sgn*33-(px+sgn*20))*math.cos(ang*sgn)-(690-780)*math.sin(ang*sgn)*0
        d.E(px+sgn*33,672,18,26,None,(235,235,245),4)
    # cuatro cuadrados que caen y forman la pieza (el nombre)
    a=sm((u-4.0)/1.0)
    for j,(r,c) in enumerate(RO['T'][0]):
        y=-60+(330-(-60)+r*40)*clamp((u-3.6-j*.15)/.7)**2; 
        if u>3.6: block(d,60+c*40,y,40,COL['T'])
    return im
def sceneE(u):
    im=new((8,16,36),(16,30,64)); d=D(im)
    for r in range(30): d.L(0,r*32,540,r*32,(255,255,255,8),1)
    for c in range(18): d.L(c*32,0,c*32,960,(255,255,255,8),1)
    nodes=[(120,500),(250,360),(250,660),(400,250),(420,520),(400,780),(480,380)]
    edges=[(0,1),(0,2),(1,3),(1,4),(2,4),(2,5),(4,6)]
    d.L(330,60,330,900,(255,230,120,140),3)
    for a,b in edges: d.L(nodes[a][0],nodes[a][1],nodes[b][0],nodes[b][1],(255,255,255,40),2)
    # propagacion
    arr={0:0.0}
    for a,b in edges:
        pass
    when={0:0.0,1:1.6,2:2.0,3:3.4,4:3.8,5:4.2,6:5.2}
    for i,(x,y) in enumerate(nodes):
        on=u>=when[i]; pulse=max(0,1-(u-when[i])*1.2) if on else 0
        d.E(x,y,34+pulse*30,34+pulse*30,(80,255,160,int(60*pulse)))
        s=1.3 if i==0 else 1
        bevel(d,x-24*s,y-20*s,x+24*s,y+14*s,(70,70,100) if not on else (60,150,110),4); d.R(x-19*s,y-15*s,x+19*s,y+8*s,(10,30,24) if on else (10,12,30),3)
        d.R(x-14*s,y+14*s,x+14*s,y+20*s,(50,50,70),2)
        if on: 
            for k,kk in enumerate(("T","L")): 
                for r,c in RO[kk][0]: d.R(x-10*s+c*6*s+k*0,y-12*s+r*6*s+k*0,x-5*s+c*6*s,y-6*s+r*6*s,COL[kk]+(255,),1) if k==(int(u*2)%2) else None
    def disk(x,y,rot=0):
        d.R(x-15,y-15,x+15,y+15,(30,30,36),3); d.R(x-15,y-15,x+15,y-12,(255,255,255,30),3)
        d.E(x,y,9,9,(225,225,232)); d.E(x,y,5.5,5.5,(20,20,26)); d.R(x-3,y+6,x+3,y+13,(225,225,232),1)
        d.R(x+11,y-6,x+15,y-1,(10,10,14),0); d.R(x-12,y-13,x-4,y-9,(240,240,235),1)
    for a,b in edges:
        ts=when[b]-1.0
        if ts<=u<ts+1.0:
            p=sm((u-ts)/1.0); xa,ya=nodes[a]; xb,yb=nodes[b]
            cx=(xa+xb)/2+ (ya-yb)*.12; cy=(ya+yb)/2+(xb-xa)*.12-30
            x=(1-p)**2*xa+2*(1-p)*p*cx+p*p*xb; y=(1-p)**2*ya+2*(1-p)*p*cy+p*p*yb
            disk(x,y)
    return im
def gameboy(d,cx,cy,sc,u,screen_fn):
    shadow(d,cx,cy+270*sc,150*sc,18*sc,90)
    bevel(d,cx-130*sc,cy-210*sc,cx+130*sc,cy+250*sc,(196,196,188),22*sc)
    d.R(cx-130*sc,cy-210*sc,cx-118*sc,cy+250*sc,(255,255,255,50),8); 
    d.R(cx-100*sc,cy-186*sc,cx+100*sc,cy-30*sc,(92,92,108),16*sc)
    for k,c in enumerate([(200,60,70),(60,60,200)]): d.R(cx-92*sc,cy-176*sc+k*3*sc,cx-70*sc,cy-173*sc+k*3*sc,c,1)
    d.R(cx-66*sc,cy-170*sc,cx+66*sc,cy-48*sc,(150,184,18),4*sc)
    d.E(cx-82*sc,cy-110*sc,4*sc,4*sc,(255,60,60,230))
    screen_fn(d,cx-66*sc,cy-170*sc,132*sc,122*sc)
    d.R(cx-66*sc,cy-170*sc,cx+66*sc,cy-48*sc,(255,255,255,0),4*sc)
    d.P([(cx-66*sc,cy-170*sc),(cx-6*sc,cy-170*sc),(cx-40*sc,cy-48*sc),(cx-66*sc,cy-48*sc)],(255,255,255,24))
    d.R(cx-70*sc,cy-24*sc,cx+10*sc,cy-8*sc,(70,60,150),3*sc)
    d.R(cx-88*sc,cy+31*sc,cx-48*sc,cy+43*sc,(40,40,52),3*sc); d.R(cx-74*sc,cy+17*sc,cx-62*sc,cy+57*sc,(40,40,52),3*sc); d.E(cx-68*sc,cy+37*sc,5*sc,5*sc,(30,30,40))
    d.E(cx+60*sc,cy+36*sc,15*sc,15*sc,(170,30,90)); d.E(cx+92*sc,cy+20*sc,15*sc,15*sc,(170,30,90))
    d.E(cx+58*sc,cy+32*sc,9*sc,6*sc,(255,255,255,70)); d.E(cx+90*sc,cy+16*sc,9*sc,6*sc,(255,255,255,70))
    for k,xx in enumerate([-44,-2]):
        pl=rotpts([(cx+xx*sc,cy+98*sc),(cx+(xx+34)*sc,cy+98*sc),(cx+(xx+34)*sc,cy+110*sc),(cx+xx*sc,cy+110*sc)],cx+xx*sc,cy+104*sc,-.45); d.P(pl,(122,122,132))
    for k in range(6): d.L(cx+30*sc+k*10*sc,cy+170*sc,cx+54*sc+k*10*sc,cy+226*sc,(130,130,140),2.5*sc)
def lcd_tetris(sim,t):
    P4=[(155,188,15),(139,172,15),(48,98,48),(15,56,15)]
    def f(d,x,y,w,h):
        cell=h/21.0
        draw_board(d,sim,t,x+(w-10*cell)/2,y+cell*.6,cell,mono=True,frame=False)
    return f
def sceneF(u):
    im=new((30,26,56),(14,12,34)); d=D(im)
    d.E(270,470,260,200,(255,230,160,26)); stars(d,u,40,300)
    for k in range(7):
        kk=list(SH)[k]; x=(rnd(k,9)*500+20); y=(rnd(k,8)*900-u*(14+k*3))%1000
        for r,c in RO[kk][0]: block(d,x+c*14,y+r*14,14,COL[kk],60)
    gameboy(d,270,470,1.65,u,lcd_tetris(SIM,u*1.0+8))
    return im
def sceneG(u):
    im=new((8,6,26),(54,12,72)); d=D(im)
    for k in range(18):
        a=k*math.pi/9+u*.3; d.P([(270,480),(270+math.cos(a-.07)*800,480+math.sin(a-.07)*800),(270+math.cos(a+.07)*800,480+math.sin(a+.07)*800)],(255,230,150,10))
    i,p=draw_board(d,SIMF,u*1.0,90,150,36)
    d.R(60,120,480,900,None,24,(255,220,120,int(120+100*math.sin(u*5))),3)
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx==0: return 1.0+.12*sm(p),270,470-30*sm(p)
    if idx==1: return 1.0+.5*sm(p),270+10*sm(p),520-110*sm(p)
    if idx==2: return 1.0+.12*sm(p),270,430+20*sm(p)
    if idx==3: return 1.25-.2*sm(p),150+240*sm(p),560
    if idx==4: return 1.1+.3*sm(p),250+80*sm(p),520
    if idx==5: return 1.0+.65*sm(p),270,470-40*sm(p)
    if idx==6: return 1.4-.4*sm(clamp(u/3)),270,560-110*sm(clamp(u/3))
    return 1.25-.2*sm(p),270,470
core.CAM=cam
if __name__=="__main__": core.main()
