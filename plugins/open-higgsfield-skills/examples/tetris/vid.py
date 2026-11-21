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

GBP=[(155,188,15),(139,172,15),(48,98,48),(15,56,15)]
FONT={"A":["###","#.#","###","#.#","#.#"],"C":["###","#..","#..","#..","###"],"E":["###","#..","##.","#..","###"],"I":["###",".#.",".#.",".#.","###"],"L":["#..","#..","#..","#..","###"],"N":["#.#","###","###","###","#.#"],"O":["###","#.#","#.#","#.#","###"],"R":["##.","#.#","##.","#.#","#.#"],"S":["###","#..","###","..#","###"],"T":["###",".#.",".#.",".#.",".#."],"V":["#.#","#.#","#.#","#.#",".#."],"X":["#.#","#.#",".#.","#.#","#.#"],"0":["###","#.#","#.#","#.#","###"],"1":[".#.","##.",".#.",".#.","###"],"2":["###","..#","###","#..","###"],"3":["###","..#","###","..#","###"],"4":["#.#","#.#","###","..#","..#"],"5":["###","#..","###","..#","###"],"6":["###","#..","###","#.#","###"],"7":["###","..#","..#","..#","..#"],"8":["###","#.#","###","#.#","###"],"9":["###","#.#","###","..#","###"]," ":["...","...","...","...","..."]}
def gb_text(d,x,y,txt,cell,col=GBP[3]):
    for i,ch in enumerate(txt):
        for r,row in enumerate(FONT.get(ch,FONT[" "])):
            for c,v in enumerate(row):
                if v=="#": d.R(x+(i*4+c)*cell,y+r*cell,x+(i*4+c)*cell+cell,y+r*cell+cell,col+(255,),0)
def gb_wall(d,x,y,w,h,cell):
    for r in range(int(h/cell)):
        for c in range(int(w/cell)):
            xx=x+c*cell; yy=y+r*cell
            d.R(xx,yy,xx+cell,yy+cell,GBP[2] if (r+c)%2==0 else GBP[1],0); d.R(xx+cell*.25,yy+cell*.25,xx+cell*.75,yy+cell*.75,GBP[3] if (r+c)%2==0 else GBP[2],0)
def gb_screen(d,P,t,lines,sc=1.15,Y0=190):
    """pantalla tipo Game Boy (Type A): muros decorados, campo 10x18, panel NEXT / LEVEL / LINES / SCORE; 4 tonos de verde"""
    cell=22*sc; X0=30
    d.R(0,0,540,960,GBP[0]+(255,),0)
    gb_wall(d,0,0,540,66,22); gb_wall(d,0,894,540,66,22)
    gb_wall(d,X0,Y0,2*cell,20*cell,cell); gb_wall(d,X0+2*cell+10*cell,Y0,2*cell,20*cell,cell)
    gb_wall(d,X0,Y0+18*cell,14*cell,2*cell,cell)
    d.R(X0+2*cell,Y0,X0+12*cell,Y0+18*cell,GBP[0]+(255,),0)
    draw_board(d,P,t,X0+2*cell,Y0,cell,mono=True,frame=False)
    px=X0+14*cell+10; pw=540-px-14
    d.R(px,Y0,px+pw,Y0+96,GBP[1]+(255,),0); d.R(px,Y0,px+pw,Y0+96,None,0,GBP[3]+(255,),4)
    gb_text(d,px+12,Y0+8,"NEXT",3.4,GBP[3])
    nk=P[(board_state(P,t)+1)%len(P)]["k"]
    for r,c in RO[nk][0]: d.R(px+22+c*15,Y0+40+r*15,px+22+c*15+14,Y0+40+r*15+14,GBP[3]+(255,),2)
    gb_text(d,px,Y0+150,"LEVEL",3.4,GBP[3]); gb_text(d,px,Y0+176,"00",4.4,GBP[3])
    gb_text(d,px,Y0+240,"LINES",3.4,GBP[3]); gb_text(d,px,Y0+266,str(lines).zfill(3),4.4,GBP[3])
    gb_text(d,px,Y0+330,"SCORE",3.4,GBP[3]); gb_text(d,px,Y0+356,str(lines*100).zfill(6),3.4,GBP[3])
def sceneA(u,final=False):
    im=new((155,188,15),(155,188,15)); d=D(im)
    t=u*1.0+(6 if final else 0)
    i=board_state(SIM,t); p=SIM[i]; lines=p["lines"]+(len(p["full"]) if t>=p["tl"] else 0)
    gb_screen(d,SIM,t,lines)
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
# ---------- D: tenis en perspectiva (camara de retransmision) ----------
YN,YF=890,560
def tsc(t): return 1.0/(1.0+t)                       # escala por profundidad (t=0 linea cercana, t=1 linea lejana)
def ty(t): return YN-(YN-YF)*(1-tsc(t))/0.5
def tx(x,t): return 270+x*250*tsc(t)                 # x en [-1,1] a lo ancho de la pista
def ellpoly(cx,cy,rx,ry,ang,n=28):
    ca,sa=math.cos(ang),math.sin(ang)
    return [(cx+rx*math.cos(k*2*math.pi/n)*ca-ry*math.sin(k*2*math.pi/n)*sa, cy+rx*math.cos(k*2*math.pi/n)*sa+ry*math.sin(k*2*math.pi/n)*ca) for k in range(n)]
def racket(d,hx,hy,ang,sc):
    """raqueta bien formada: mango, garganta en V, marco oval y cuerdas. ang = direccion del mango->cabeza"""
    ca,sa=math.cos(ang),math.sin(ang); px,py=-sa,ca
    H=lambda L:(hx+ca*L*sc,hy+sa*L*sc)
    d.L(hx,hy,H(34)[0],H(34)[1],(40,40,48),5*sc)                          # mango
    d.L(H(34)[0]+px*2*sc,H(34)[1]+py*2*sc,H(50)[0]+px*8*sc,H(50)[1]+py*8*sc,(230,230,236),3*sc)   # garganta en V
    d.L(H(34)[0]-px*2*sc,H(34)[1]-py*2*sc,H(50)[0]-px*8*sc,H(50)[1]-py*8*sc,(230,230,236),3*sc)
    cx,cy=H(72)
    rx,ry=22*sc,17*sc
    # cuerdas (dentro del ovalo, alineadas con el eje de la raqueta)
    for k in range(-4,5):
        o=k*ry/4.5; h=rx*math.sqrt(max(0,1-(o/ry)**2))
        d.L(cx-ca*h+px*o,cy-sa*h+py*o,cx+ca*h+px*o,cy+sa*h+py*o,(240,240,200,150),1.1*sc)
    for k in range(-5,6):
        o=k*rx/5.5; h=ry*math.sqrt(max(0,1-(o/rx)**2))
        d.L(cx+ca*o-px*h,cy+sa*o-py*h,cx+ca*o+px*h,cy+sa*o+py*h,(240,240,200,150),1.1*sc)
    pts=ellpoly(cx,cy,rx,ry,ang)
    for i in range(len(pts)): 
        p,q=pts[i],pts[(i+1)%len(pts)]; d.L(p[0],p[1],q[0],q[1],(230,60,70),3.6*sc)
def tplayer(d,px,py,sc,back,shirt,hit_t,swing_dir,u):
    """jugador: py = pies. back=True (de espaldas, cerca). Brazo -> mano -> raqueta unidos."""
    H=150*sc
    shadow(d,px,py+2,30*sc,6*sc,80)
    for sg in(-1,1):
        d.R(px+sg*9*sc-7*sc,py-60*sc,px+sg*9*sc+7*sc,py-6*sc,(236,200,170),4*sc)
        d.R(px+sg*9*sc-9*sc,py-8*sc,px+sg*9*sc+9*sc,py,(245,245,245),4*sc)
    d.R(px-22*sc,py-86*sc,px+22*sc,py-52*sc,(250,250,250) if back else (40,50,90),8*sc)   # pantalon corto
    d.R(px-24*sc,py-124*sc,px+24*sc,py-82*sc,shirt,10*sc)
    d.R(px-24*sc,py-124*sc,px+24*sc,py-118*sc,(255,255,255,50),10*sc)
    # cabeza
    d.E(px,py-140*sc,15*sc,17*sc,(236,200,170)); d.E(px,py-148*sc,16*sc,10*sc,(70,48,34) if back else (50,34,24))
    if not back:
        for sg in(-1,1): d.E(px+sg*6*sc,py-140*sc,1.8*sc,2.2*sc,(30,30,40))
        d.A(px,py-133*sc,5*sc,3*sc,20,160,(120,50,50),1.6*sc)
    # brazo libre (equilibrio)
    fx=-swing_dir
    d.L(px+fx*26*sc,py-118*sc,px+fx*40*sc,py-92*sc,(236,200,170),7*sc)
    # brazo con raqueta: hombro -> mano -> raqueta, angulo segun fase del golpe
    ph=clamp((u-hit_t+.35)/.7)            # 0 preparacion .. .5 impacto .. 1 final
    sh=(px+swing_dir*24*sc,py-116*sc)
    ang=(-2.5+3.1*sm(ph)) if swing_dir>0 else (math.pi+2.5-3.1*sm(ph))
    if not back: ang=ang+0  # igual convencion
    ha=ang-.35*swing_dir
    hand=(sh[0]+math.cos(ha)*34*sc,sh[1]+math.sin(ha)*34*sc+8*sc)
    d.L(sh[0],sh[1],hand[0],hand[1],(236,200,170),7.5*sc)
    d.E(hand[0],hand[1],5*sc,5*sc,(236,200,170))
    racket(d,hand[0],hand[1],ang,sc)
def sceneD(u):
    im=new((110,170,235),(200,225,250)); d=D(im)
    d.E(430,100,40,40,(255,240,170)); d.E(430,100,76,76,(255,240,170,50))
    for k in range(3): d.E(90+k*160+(u*8)%40,90+k*30,50,15,(255,255,255,190))
    # gradas y valla de fondo (detras de la linea lejana)
    d.R(0,300,540,YF-20,(60,70,96)); 
    for r in range(8):
        for c in range(54):
            if rnd(r*54+c)>.25: d.R(c*10,308+r*17,c*10+8,308+r*17+10,[(220,90,90),(90,140,230),(240,210,90),(230,230,230),(110,200,130)][(r+c)%5]+(210,),2)
    d.R(0,YF-34,540,YF-8,(34,110,80)); d.R(0,YF-34,540,YF-30,(255,255,255,60))
    # suelo exterior y pista azul en perspectiva
    d.R(0,YF-8,540,960,(48,128,92))
    court=[(tx(-1.0,0),ty(0)),(tx(1.0,0),ty(0)),(tx(1.0,1),ty(1)),(tx(-1.0,1),ty(1))]
    d.P(court,(46,110,190))
    for k in range(10):
        t=k/10.0; d.L(tx(-1,t),ty(t),tx(1,t),ty(t),(255,255,255,10),1.5)
    LW=(255,255,255)
    def seg(x0,t0,x1,t1,w=3.2): d.L(tx(x0,t0),ty(t0),tx(x1,t1),ty(t1),LW,w*tsc((t0+t1)/2))
    seg(-1,0,1,0); seg(-1,1,1,1); seg(-1,0,-1,1); seg(1,0,1,1)
    seg(-.82,0,-.82,1,2.6); seg(.82,0,.82,1,2.6)
    seg(-.82,.23,.82,.23); seg(-.82,.77,.82,.77); seg(0,.23,0,.77,2.6)
    # --- red: poste, malla y cinta en perspectiva correcta (plano frontal al espectador) ---
    tn=.5; yn=ty(tn); sn=tsc(tn); nh=75*sn; xl=tx(-1.08,tn); xr=tx(1.08,tn)
    for k in range(-1,16):
        xx=xl+(xr-xl)*k/14.0
        if xl<=xx<=xr: d.L(xx,yn-nh,xx,yn,(240,240,240,150),1.2)
    for k in range(0,8): d.L(xl,yn-nh+k*nh/7.0,xr,yn-nh+k*nh/7.0,(240,240,240,150),1.2)
    d.R(xl-2,yn-nh-3,xr+2,yn-nh+4,(250,250,250),2); 
    for xx in(xl,xr): d.R(xx-3,yn-nh-6,xx+3,yn+4,(40,40,50),1)
    d.R(xl,yn,xr,yn+3,(0,0,0,40),0)
    # --- pelota con trayectoria fisica: bote y sombra ---
    per=1.35; leg=int(u/per); ph=(u%per)/per; far_to_near=(leg%2==1)
    tt=.05+.9*ph
    if far_to_near: tt=1.0-tt
    # altura en px a escala cercana: dos arcos (antes y despues del bote)
    hit=80.0
    def zf(pp):
        if pp<.75: tau=pp/.75; return hit*(1-tau)+4*190*tau*(1-tau)
        tau=(pp-.75)/.25; return 4*52*tau*(1-tau)+hit*tau
    pp=ph; z=zf(pp)
    bx=tx(.08*math.sin(leg*2.1)*(1-2*abs(ph-.5)),tt); by=ty(tt); sc=tsc(tt)
    d.E(bx,by+1,10*sc,3.5*sc,(0,0,0,90))
    d.E(bx,by-z*sc,12*sc,12*sc,(214,240,60)); d.A(bx,by-z*sc,12*sc,12*sc,-40,70,(255,255,255),2.2*sc); d.A(bx,by-z*sc,12*sc,12*sc,140,250,(255,255,255),2.2*sc)
    # --- jugadores (cercano de espaldas, lejano de frente) con golpe sincronizado ---
    near_hits=[k*per for k in range(0,10) if k%2==0]; far_hits=[k*per for k in range(1,10) if k%2==1]
    nh_t=min(near_hits,key=lambda t:abs(t-u)); fh_t=min(far_hits,key=lambda t:abs(t-u))
    tplayer(d,tx(-.05,.96),ty(.99),tsc(.99),False,(40,110,200),fh_t,1,u)
    tplayer(d,tx(.05,0.0)+0,YN+10,1.0,True,(222,70,90),nh_t,-1,u)
    # --- cuatro cuadrados que caen y forman la pieza (el nombre) ---
    for j,(r,c) in enumerate(RO['T'][0]):
        yy=-60+(260-(-60)+r*40)*clamp((u-1.0-j*.18)/.8)**2
        if u>1.0: block(d,60+c*40+160,yy,40,COL['T'])
    return im
def sceneMoney(u):
    im=new((8,10,34),(30,26,64)); d=D(im); stars(d,u,40,300)
    d.R(0,740,540,960,(26,22,46)); d.R(0,740,540,746,(255,255,255,18))
    # edificio estatal (derecha): frontón, columnas y escalinata
    bx=290; 
    d.P([(bx-10,330),(bx+240,330),(bx+115,250)],(150,140,170)); d.R(bx-10,330,bx+240,350,(176,166,196),2)
    for k in range(6): d.R(bx+4+k*40,350,bx+20+k*40,700,(206,198,222),3); d.R(bx+4+k*40,350,bx+8+k*40,700,(255,255,255,70),3)
    d.R(bx-14,700,bx+244,720,(150,140,170),2); d.R(bx-24,720,bx+254,740,(130,120,150),2)
    d.R(bx+84,560,bx+150,700,(40,30,50),3); d.E(bx+117,560,33,26,(40,30,50))
    for k in range(5): d.R(bx+16+k*40,420,bx+34+k*40,500,(255,226,150,int(120+80*math.sin(u*3+k))),2)
    # programador (izquierda) con su monitor y un frasco vacio
    bevel(d,20,650,250,700,(112,76,52),6); d.R(36,700,54,860,(80,54,40),3); d.R(216,700,234,860,(80,54,40),3)
    box=crt(d,40,420,200,170,(2,18,8),(196,188,160)); x0,y0,x1,y1=box
    kk=["T","L","S","J"][int(u*.5)%4]; yy=(u*40)%90
    for r,c in RO[kk][0]: d.R(x0+60+c*14,y0+10+yy+r*14,x0+60+c*14+13,y0+10+yy+r*14+13,COL[kk]+(255,),2)
    crt_fx(d,box)
    person_back(d,150,690,1.1,0,u)
    d.R(196,598,236,650,(230,240,250,60),6); d.R(196,598,236,650,None,6,(230,240,250,180),2); d.R(200,590,232,600,(150,150,170),3)
    # monedas: salen del juego y viajan (parabola) hacia el edificio; el frasco sigue vacio
    for k in range(7):
        ts=(u*.9+k/7.0)%1.0
        sx,sy=240,520; ex,ey=bx+117,640
        x=sx+(ex-sx)*ts; y=sy+(ey-sy)*ts-math.sin(ts*math.pi)*170
        d.E(x,y,10,10,(255,205,70)); d.E(x,y,10,10,None,(190,140,30),2); d.E(x-3,y-3,3,3,(255,246,190))
        if ts>.92: d.E(ex,ey,20,20,(255,226,150,90))
    d.R(60,880,480,900,(0,0,0,0),0)
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
core.SCN=[lambda u:sceneA(u),sceneB,sceneD,sceneMoney,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx==0: return 1.0+.12*sm(p),270,470-30*sm(p)
    if idx==1: return 1.0+.5*sm(p),270+10*sm(p),520-110*sm(p)
    if idx==2: return 1.12-.08*sm(p),270,720-40*sm(p)
    if idx==3: return 1.0+.12*sm(p),270+20*sm(p),520
    if idx==4: return 1.1+.3*sm(p),250+80*sm(p),520
    if idx==5: return 1.0+.65*sm(p),270,470-40*sm(p)
    if idx==6: return 1.4-.4*sm(clamp(u/3)),270,560-110*sm(clamp(u/3))
    return 1.25-.2*sm(p),270,470
core.CAM=cam
if __name__=="__main__": core.main()
