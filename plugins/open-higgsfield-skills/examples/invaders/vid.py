import sys; sys.path.insert(0,"..")
import core, math, random
from core import *
PALI={'#':(255,255,255)}
I1=[["...##...","..####..",".######.","##.##.##","########","..#..#..",".#.##.#.","#.#..#.#"],["...##...","..####..",".######.","##.##.##","########",".#.##.#.","#......#",".#....#."]]
I2=[["..#.....#..","...#...#...","..#######..",".##.###.##.","###########","#.#######.#","#.#.....#.#","...##.##..."],["..#.....#..","#..#...#..#","#.#######.#","###.###.###","###########",".#########.","..#.....#..",".#.......#."]]
I3=[["....####....",".##########.","############","###..##..###","############","...##..##...","..##.##.##..","##........##"],["....####....",".##########.","############","###..##..###","############","..###..###..",".##..##..##.","..##....##.."]]
CAN=["......#......","....#####....","....#####....","#############","#############","#############"]
UFO=["....######....","..##########..",".############.","##.##.##.##.##","##############","..###..###..","...#......#..."]
TINT=[(120,255,170),(255,120,220),(255,120,220),(110,200,255),(110,200,255)]
SPR=[I1,I2,I2,I3,I3]
PX=30; CELL=3.0
def sprite(d,x,y,rows,col,cell=3.0,a=255):
    for r,row in enumerate(rows):
        for c,ch in enumerate(row):
            if ch=='#': d.R(x+c*cell,y+r*cell,x+c*cell+cell+.3,y+r*cell+cell+.3,col+(a,),0)
BUNK=["...##############...","..################..",".##################.","####################","####################","####################","####################","####################","####################","#####..........#####","####............####","###..............###"]
def bunker_init(): return [[[1 if ch=='#' else 0 for ch in row] for row in BUNK] for _ in range(4)]
def erode(b,bi,cx,cy,rad=2):
    for r in range(len(BUNK)):
        for c in range(len(BUNK[0])):
            if (r-cy)**2+(c-cx)**2<=rad*rad: b[bi][r][c]=0
BX=[54+i*114 for i in range(4)]; BY=640; BC=3.6
def simulate(seed,T,dt=1/60.0):
    rg=random.Random(seed)
    alive=[[1]*11 for _ in range(5)]; offx=0.0; offy=150.0; dr=1; tt=0.0; frame=0
    ufo=None; ut=2.5; cx=270.0; cool=0.0; pb=None; eb=[]; efire=0.5; boom=[]; bunk=bunker_init(); snaps=[]; t=0.0; kills=0
    while t<T:
        n=sum(sum(r) for r in alive)
        if ufo is None:
            ut-=dt
            if ut<=0: ufo=[-40.0 if rg.random()<.5 else 560.0,0]; ufo[1]=1 if ufo[0]<0 else -1; ut=13.0
        else:
            ufo[0]+=ufo[1]*110*dt
            if ufo[0]<-60 or ufo[0]>600: ufo=None
        if n==0:
            alive=[[1]*11 for _ in range(5)]; offx=0.0; offy=150.0; dr=1; n=55; boom=[]
            bunk=bunker_init(); pb=None; eb=[]
        interval=0.018+0.0165*n
        tt+=dt
        if tt>=interval:
            tt=0; frame^=1; xs=[c for c in range(11) for r in range(5) if alive[r][c]]
            lo=PX+offx+min(xs)*36; hi=PX+offx+max(xs)*36+33
            if (dr>0 and hi+8>510) or (dr<0 and lo-8<30): offy+=14; dr=-dr
            else: offx+=8*dr
        # objetivo del cañon: invasores cuya columna de tiro esta libre de bunker
        def free(x):
            for bi in range(4):
                if BX[bi]<=x<BX[bi]+20*BC:
                    c=int((x-BX[bi])/BC)
                    if 0<=c<20 and any(bunk[bi][r][c] for r in range(12)): return False
            return True
        tg=None
        for r in range(4,-1,-1):
            for c in range(11):
                if alive[r][c]:
                    x=PX+offx+c*36+16
                    if free(x) and (tg is None or abs(x-cx)<abs(tg-cx)): tg=x
            if tg is not None: break
        if tg is None:
            for r in range(4,-1,-1):
                for c in range(11):
                    if alive[r][c]:
                        x=PX+offx+c*36+16
                        if tg is None or abs(x-cx)<abs(tg-cx): tg=x
        if tg is not None:
            # esquivar balas
            for ex,ey,_a in eb:
                if 690<ey<775 and abs(ex-cx)<22: tg=cx+(-1 if ex>=cx else 1)*60
            sp=300*dt; 
            if abs(tg-cx)>sp: cx+=sp*(1 if tg>cx else -1)
            cx=max(PX+20,min(510-20,cx))
        cool-=dt
        if pb is None and cool<=0 and tg is not None and abs(tg-cx)<7:
            pb=[cx,770.0]; cool=.12
        if pb:
            pb[1]-=820*dt; hit=False
            for bi in range(4):
                if BX[bi]<=pb[0]<BX[bi]+20*BC and BY<=pb[1]<BY+12*BC:
                    c=int((pb[0]-BX[bi])/BC); r=int((pb[1]-BY)/BC)
                    if 0<=r<12 and 0<=c<20 and bunk[bi][r][c]: erode(bunk,bi,c,r,2); hit=True
            if not hit:
                for r in range(5):
                    for c in range(11):
                        if alive[r][c]:
                            sw=len(SPR[r][0][0])*CELL; x=PX+offx+c*36+(36-sw)/2-1; y=offy+r*34
                            if x<=pb[0]<=x+sw and y<=pb[1]<=y+24: alive[r][c]=0; boom.append([pb[0],pb[1],0.0]); hit=True; kills+=1; break
                    if hit: break
            if hit or pb[1]<60: pb=None
        efire-=dt
        if efire<=0 and n>0:
            efire=.8+rg.random()*.6; cols=[c for c in range(11) if any(alive[r][c] for r in range(5))]
            if cols:
                c=rg.choice(cols); r=max(rr for rr in range(5) if alive[rr][c]); eb.append([PX+offx+c*36+16,offy+r*34+24,0.0])
        ne=[]
        for b in eb:
            b[1]+=210*dt; b[2]+=dt; ok=True
            for bi in range(4):
                if BX[bi]<=b[0]<BX[bi]+20*BC and BY<=b[1]<BY+12*BC:
                    c=int((b[0]-BX[bi])/BC); r=int((b[1]-BY)/BC)
                    if 0<=r<12 and 0<=c<20 and bunk[bi][r][c]: erode(bunk,bi,c,r,2); ok=False; boom.append([b[0],b[1],0.0])
            if b[1]>790: ok=False
            if ok: ne.append(b)
        eb=ne
        for e in boom: e[2]+=dt
        boom=[e for e in boom if e[2]<.3]
        t+=dt
        if int(round(t*60))%2==0:
            snaps.append(dict(ufo=ufo[:] if ufo else None,kills=kills,alive=[r[:] for r in alive],offx=offx,offy=offy,frame=frame,cx=cx,pb=pb[:] if pb else None,eb=[b[:] for b in eb],boom=[e[:] for e in boom],bunk=[[row[:] for row in bb] for bb in bunk],n=n,interval=interval,t=t))
    return snaps
SIM=simulate(5,100)
def snap(t): return SIM[min(len(SIM)-1,max(0,int(t*30)))]
DIG={0:['###','#.#','#.#','#.#','###'],1:['.#.','##.','.#.','.#.','###'],2:['###','..#','###','#..','###'],3:['###','..#','###','..#','###'],4:['#.#','#.#','###','..#','..#'],5:['###','#..','###','..#','###'],6:['###','#..','###','#.#','###'],7:['###','..#','..#','..#','..#'],8:['###','#.#','###','#.#','###'],9:['###','#.#','###','..#','###']}
def draw_game(d,s,x0,y0,sc=1.0,tint=True):
    # rejilla coherente: todo se dibuja en coordenadas de juego y se traslada
    def X(x): return x0+x*sc
    def Y(y): return y0+y*sc
    for r in range(5):
        for c in range(11):
            if s["alive"][r][c]:
                sw=len(SPR[r][0][0])*CELL; x=PX+s["offx"]+c*36+(36-sw)/2-1; y=s["offy"]+r*34
                sprite(d,X(x),Y(y),SPR[r][s["frame"]],(255,255,255) if y<590 else (120,255,140),CELL*sc)
    for bi in range(4):
        for r in range(12):
            for c in range(20):
                if s["bunk"][bi][r][c]: d.R(X(BX[bi]+c*BC),Y(BY+r*BC),X(BX[bi]+c*BC+BC)+.3,Y(BY+r*BC+BC)+.3,(90,230,110,255),0)
    sprite(d,X(s["cx"]-19.5),Y(770),CAN,(120,255,140),CELL*sc)
    if s["ufo"]: sprite(d,X(s["ufo"][0]),Y(52),UFO,(255,70,80),CELL*sc*.95)
    sc_=str(int(s["kills"]*10)).zfill(4)
    for i,ch in enumerate(sc_):
        for rr,row in enumerate(DIG[int(ch)]):
            for cc,v in enumerate(row):
                if v=='#': d.R(X(PX+4+i*14+cc*3),Y(14+rr*3),X(PX+4+i*14+cc*3+3)+.3,Y(14+rr*3+3)+.3,(255,255,255),0)
    for l in range(3): sprite(d,X(PX+260+l*50),Y(826),CAN,(120,255,140),2.0*sc)
    d.R(X(PX),Y(814),X(510),Y(818),(90,230,110),0)
    if s["pb"]: d.R(X(s["pb"][0]-1.5),Y(s["pb"][1]-10),X(s["pb"][0]+1.5),Y(s["pb"][1]),(255,255,255),0)
    for b in s["eb"]:
        z=int(b[2]*12)%2
        for k in range(5): d.R(X(b[0]+(-2 if (k+z)%2 else 2)),Y(b[1]+k*4),X(b[0]+(-2 if (k+z)%2 else 2)+3),Y(b[1]+k*4+4),(255,255,255),0)
    for e in s["boom"]:
        a=1-e[2]/.3; rr=8+e[2]*50
        for k in range(8): ang=k*math.pi/4; d.R(X(e[0]+math.cos(ang)*rr),Y(e[1]+math.sin(ang)*rr),X(e[0]+math.cos(ang)*rr+4),Y(e[1]+math.sin(ang)*rr+4),(255,230,120,int(255*a)),0)
def arcade_frame(d,top=120):
    d.R(0,0,540,960,(4,4,10))
    for r in range(60): d.R(0,r*16,540,r*16+1,(0,0,0,70))
def sceneA(u,final=False):
    im=new((6,4,22),(24,10,48)); d=D(im); stars(d,u,40,300)
    # sala de recreativos: neon y suelo brillante
    for k,(x,c) in enumerate([(40,(255,60,190)),(500,(60,220,255))]):
        d.R(x-4,80,x+4,700,c+(220,),3); d.E(x,390,50,320,c+(30,))
    floor(d,870,(22,14,38)); d.E(270,900,220,22,(255,80,200,46))
    shadow(d,270,880,200,14,100)
    bevel(d,90,40,450,880,(14,14,24),14)
    d.R(90,40,104,880,(255,60,150)); d.R(436,40,450,880,(60,220,255))
    for k in range(4):
        sprite(d,116,300+k*130,I1[0],(255,80,160,),2.6,90); sprite(d,396,300+k*130,I3[0],(80,220,255),2.2,90)
    bevel(d,110,52,430,150,(30,16,60),8)
    for k in range(5): sprite(d,128+k*60,76,[I1,I2,I3,I2,I1][k][int(u*2)%2],[(255,255,255),(120,255,140),(255,120,200),(120,200,255),(255,230,90)][k],4.0)
    bevel(d,104,160,436,652,(30,30,44),10); d.R(118,176,422,640,(2,2,6),6)
    s_=snap(u*1.0+(30 if final else 0)); draw_game(d,s_,121,169,.55)
    for k in range(40): d.R(118,176+k*12,422,177+k*12,(0,0,0,60))
    d.P([(126,182),(260,182),(190,634),(126,634)],(255,255,255,12))
    d.R(118,176,422,640,None,6,(120,255,170,int(30+20*math.sin(u*5))),2)
    bevel(d,104,656,436,740,(38,30,56),8)
    for k,x in enumerate([180,270,360]): d.E(x,700,17,17,(24,24,30)); d.E(x,697,13,13,[(240,70,70),(70,70,240),(255,220,80)][k])
    d.R(236,770,304,826,(24,24,34),5); d.R(262,780,278,812,(255,220,80,int(120+100*(int(u*2)%2))),2)
    for k in range(8): d.R(116+k*40,846,140+k*40,852,(0,0,0,70),2)
    return im
def office_desk(d,x0,x1,ytop,col=(112,78,56)):
    bevel(d,x0,ytop,x1,ytop+24,col,5); d.R(x0+10,ytop+24,x0+24,ytop+130,tuple(int(c*.72) for c in col),3); d.R(x1-24,ytop+24,x1-10,ytop+130,tuple(int(c*.72) for c in col),3)
def small_crt(d,x,y,w,h,u,k=0):
    box=crt(d,x,y,w,h,(2,14,8),(190,182,158)); x0,y0,x1,y1=box
    for r in range(int((y1-y0-12)/9)):
        ww=10+rnd(r+k*5,3)*(x1-x0-30); d.R(x0+8,y0+8+r*9,x0+8+ww,y0+13+r*9,(90,255,130,200),1)
    crt_fx(d,box)
def sceneB(u):
    im=new((40,34,58),(74,66,92)); d=D(im)
    # --- pared, zocalo y techo con fluorescentes ---
    d.R(0,0,540,40,(46,40,62)); 
    for k in range(3): 
        d.R(30+k*180,14,170+k*180,28,(255,252,228)); d.E(100+k*180,32,120,30,(255,252,228,36))
    d.R(0,470,540,640,(58,52,78)); d.R(0,470,540,476,(255,255,255,24))
    # --- ventana con la ciudad de noche (persianas) ---
    bevel(d,22,70,206,320,(64,54,66),8); d.R(32,80,196,310,(18,24,64))
    for k,(x,h,w) in enumerate([(36,110,30),(70,150,26),(100,90,34),(138,130,28),(170,100,24)]):
        d.R(x,310-h,x+w,310,(14,18,46))
        for r in range(int(h/18)):
            for c in range(int(w/10)):
                if rnd(k*9+r*3+c)>.45: d.R(x+3+c*10,314-h+r*18,x+8+c*10,322-h+r*18,(255,222,130,230),1)
    d.E(170,110,12,12,(250,244,220,230))
    for k in range(9): d.R(32,80+k*26,196,86+k*26,(70,62,72,150),0)
    # --- corcho con bocetos de invasores ---
    bevel(d,330,84,516,300,(158,112,72),6)
    for k in range(6):
        px=344+(k%3)*58; py=100+(k//3)*92
        d.R(px,py,px+50,py+80,(246,244,232),2); d.E(px+25,py+6,3,3,(220,60,60))
        sprite(d,px+6,py+16,[I1,I2,I3][k%3][int(u*2)%2],(50,50,60),3.6)
        d.L(px+6,py+66,px+44,py+66,(0,0,0,60),1.5)
    # reloj de pared
    d.E(270,100,26,26,(244,242,232)); d.E(270,100,26,26,None,(70,60,50),3)
    d.L(270,100,270+math.cos(u*.4)*17,100+math.sin(u*.4)*17,(40,30,30),3); d.L(270,100,270+math.cos(u*4.8)*22,100+math.sin(u*4.8)*22,(40,30,30),2)
    # armario de cintas (mainframe de la epoca) con bobinas girando
    bevel(d,456,320,528,560,(182,176,152),6)
    for k in range(2):
        cx=476+k*34; cy=368; d.E(cx,cy,14,14,(40,40,50)); 
        for q in range(3): a_=u*3+q*2.09+k; d.L(cx,cy,cx+math.cos(a_)*12,cy+math.sin(a_)*12,(210,210,220),2)
    for k in range(6): d.E(470+k*10,430+(k%2)*10,3,3,[(255,70,70),(80,255,120),(255,220,80)][k%3]+(int(120+120*math.sin(u*6+k)),))
    # --- suelo con baldosas ---
    d.R(0,640,540,960,(52,46,72)); d.R(0,640,540,646,(255,255,255,18))
    for k in range(10): d.L(k*60-20,646,k*80-110,960,(0,0,0,40),2)
    for k in range(6): d.L(0,660+k*50,540,660+k*50,(0,0,0,30),2)
    # --- fila trasera: dos escritorios con compañeros trabajando (mas lejos, mas pequeños) ---
    office_desk(d,34,210,560,(108,74,54)); small_crt(d,78,450,96,84,u,1)
    office_desk(d,330,452,560,(108,74,54)); small_crt(d,346,450,96,84,u,2)
    person_back(d,122,586,.62,1,u); person_back(d,392,590,.62,0,u+.7)
    for x in (110,396): mug(d,x+34,540,u,(240,240,248))
    # --- espectadores de pie junto a la pantalla principal ---
    person_front(d,78,470,.78,0,u,False); person_front(d,462,478,.78,1,u+.5,False)
    # --- escritorio principal: ordenador central con Space Invaders ---
    office_desk(d,40,500,676,(118,82,58)); d.R(40,676,500,682,(255,255,255,26),5)
    box=crt(d,150,360,240,262,(2,8,10),(190,182,158)); x0,y0,x1,y1=box
    d.R(x0,y0,x1,y1,(0,0,0))
    sn=snap(u*1.2+10); sc_=.255
    draw_game(d,sn,x0+(x1-x0-480*sc_)/2-30*sc_+8,y0+4,sc_)
    crt_fx(d,box); d.E((x0+x1)/2,y1+20,0,0,(0,0,0))
    # cables, teclado, placa y tazas
    for k in range(3): d.A(150-20+k*6,640,40,24,60,300,(30,30,40),3)
    keyboard(d,196,654,150,32)
    d.R(54,660,156,702,(16,90,52),4)
    for k in range(7): d.R(62+k*13,668,70+k*13,676,(24,24,30),2); d.L(62+k*13,684,70+k*13,696,(210,180,60,230),2)
    d.R(360,664,452,700,(248,246,234),2); d.L(366,672,444,672,(0,0,0,60),2); d.L(366,680,430,680,(0,0,0,60),2); d.L(366,688,438,688,(0,0,0,60),2)
    mug(d,470,650,u,(255,240,200)); d.R(0,0,0,0,(0,0,0,0),0)
    # --- diseñador principal, sentado frente al ordenador (centro de la escena) ---
    person_back(d,270,740,1.45,0,u)
    # papeles volando suavemente
    for k in range(3):
        px=(120+k*150+math.sin(u*1.3+k)*12); py=240+k*30+math.sin(u*.9+k*2)*6
        d.R(px,py,px+18,py+24,(250,248,238,200),1); d.L(px+3,py+7,px+15,py+7,(0,0,0,50),1)
    return im
def sceneC(u):
    im=new((6,14,30),(10,26,56)); d=D(im)
    for r in range(30): d.L(0,r*32,540,r*32,(255,255,255,8),1)
    for c in range(18): d.L(c*32,0,c*32,960,(255,255,255,8),1)
    # chip central
    bevel(d,160,60,380,230,(30,30,40),8)
    for k in range(10): d.R(150,76+k*16,160,86+k*16,(190,190,200),1); d.R(380,76+k*16,390,86+k*16,(190,190,200),1)
    d.R(176,76,364,214,(14,14,24),4)
    pulse=int(120+100*math.sin(u*9)); d.R(186,88,354,204,None,4,(120,255,170,pulse),2)
    for k in range(5): d.L(190,100+k*22,350,100+k*22,(120,255,170,50),1.5)
    d.E(270,146,16,16,(120,255,170,pulse))
    # cuadricula de invasores que se destruyen en el tiempo: n baja linealmente
    n=max(3,int(55-u*7.2)); order=list(range(55)); random.Random(3).shuffle(order)
    alive=set(order[:n]); idx=0
    cy0=300; draw_pos=[]
    for r in range(5):
        for c in range(11):
            k=r*11+c
            if k in alive: sprite(d,30+c*44,cy0+r*54,SPR[r][int(u*3)%2],TINT[r],3.6)
    # cursor de dibujo
    rem=[k for k in range(55) if k in alive]
    interval=0.018+0.0165*len(rem)
    ph=(u%max(.2,interval*2))/max(.2,interval*2)
    ci=int(ph*len(rem)) if rem else 0
    if rem:
        k=rem[min(ci,len(rem)-1)]; r,c=k//11,k%11
        d.R(30+c*44-5,cy0+r*54-5,30+c*44+44,cy0+r*54+34,None,4,(255,255,255,230),3)
        d.L(270,230,30+c*44+20,cy0+r*54-5,(120,255,170,150),2)
    # reloj/velocimetro: aguja proporcional a 1/intervalo
    cx,cy=270,740; R=130
    d.E(cx,cy,R+8,R+8,(30,30,50)); d.E(cx,cy,R,R,(10,14,34))
    for k in range(11):
        a=math.pi*(1+k/10); d.L(cx+math.cos(a)*(R-14),cy+math.sin(a)*(R-14),cx+math.cos(a)*R,cy+math.sin(a)*R,(255,255,255,160),3)
    d.A(cx,cy,R-6,R-6,180,360,(120,255,170,220),8)
    d.A(cx,cy,R-6,R-6,300,360,(255,80,90,220),8)
    speed=clamp((1/interval-1.0)/55.0)
    a=math.pi*(1+speed)
    d.L(cx,cy,cx+math.cos(a)*(R-24),cy+math.sin(a)*(R-24),(255,255,255),6); d.E(cx,cy,10,10,(255,255,255))
    d.R(cx-60,cy+30,cx+60,cy+70,(10,14,34),6); number_=int(len(rem))
    bar=clamp(1-len(rem)/55); d.R(40,880,500,904,(10,14,34),6); d.R(40,880,40+460*bar,904,(120,255,170),6)
    return im
def sceneD(u):
    im=new((4,4,14),(12,10,34)); d=D(im); stars(d,u,40,960)
    bevel(d,126,92,414,532,(40,36,60),16); d.R(138,104,402,520,(2,3,10),8)
    t0=min(77.0,u*10.5)
    s=snap(t0); draw_game(d,s,135,108,.5)
    for k in range(35): d.R(138,104+k*12,402,105+k*12,(0,0,0,60))
    # grafica de velocidad (derivada de la simulacion real)
    d.R(30,560,510,880,(10,12,30),10); d.R(30,560,510,566,(255,255,255,18),10)
    for k in range(6): d.L(40,600+k*50,500,600+k*50,(255,255,255,18),1)
    pts=[]
    k=0
    while k*.6<=t0:
        sn=snap(k*.6); pts.append((50+k*.6/78*440,860-clamp((1/sn["interval"])/28.0)*270)); k+=1
    for i in range(len(pts)-1): d.L(pts[i][0],pts[i][1],pts[i+1][0],pts[i+1][1],(255,120,140),4)
    if pts: d.E(pts[-1][0],pts[-1][1],9,9,(255,255,255)); d.E(pts[-1][0],pts[-1][1],18,18,(255,120,140,90))
    # contador de invasores
    d.R(380,574,500,616,(0,0,0,150),6)
    n=s["n"]
    for i,ch in enumerate(str(n).zfill(2)): pass
    return im
def sceneE(u):
    im=new((70,46,92),(26,22,54)); d=D(im)
    for k in range(7): d.E(50+k*74,60+math.sin(u*3+k)*6,8,8,(255,220,120,120))
    d.R(0,660,540,960,(30,24,48)); d.R(0,660,540,666,(255,255,255,18))
    bevel(d,40,620,500,680,(88,62,100),10)
    box=crt(d,140,230,260,200,(2,10,24),(70,66,84)); s=snap(30+u*.4); draw_game(d,s,box[0]+2,box[1]+6,.42); crt_fx(d,box)
    person_front(d,160,520,1.35,0,u,False); person_front(d,400,524,1.35,1,u+.3,False)
    b=sm((u-.5)/.4)
    bubble(d,100,170,340,90,200,262,int(255*clamp(b)))
    # bichito (error) -> check
    sw=sm((u-3.0)/.6)
    if sw<1:
        cx,cy=270,215; sc=1-sw
        d.E(cx,cy,24*sc,18*sc,(190,50,60,int(255*clamp(b)))); 
        for k in range(3): d.L(cx-20*sc,cy-8*sc+k*8*sc,cx-34*sc,cy-14*sc+k*14*sc,(60,30,30,int(255*clamp(b))),2*sc); d.L(cx+20*sc,cy-8*sc+k*8*sc,cx+34*sc,cy-14*sc+k*14*sc,(60,30,30,int(255*clamp(b))),2*sc)
        d.E(cx,cy-18*sc,9*sc,9*sc,(60,30,30,int(255*clamp(b))))
    if sw>0:
        cx,cy=270,215; r=30*sw; d.E(cx,cy,r,r,(40,200,100)); d.L(cx-14*sw,cy+2*sw,cx-4*sw,cy+12*sw,(255,255,255),5*sw); d.L(cx-4*sw,cy+12*sw,cx+16*sw,cy-10*sw,(255,255,255),5*sw)
    return im
def sceneF(u):
    im=new((14,2,6),(40,8,18)); d=D(im)
    shake=(math.sin(u*70)*3,math.cos(u*55)*3) if u>0 else (0,0)
    bevel(d,40,100,500,880,(40,24,30),16); d.R(54,114,486,866,(2,2,8),8)
    # tramo final de la simulacion: queda un solo invasor, gran velocidad
    tr=next((i/30.0 for i,sn in enumerate(SIM) if i>300 and sn["n"]==55),80.0)
    base=tr-5.6
    s=snap(min(base+u*1.0,tr-.15)); draw_game(d,s,54+shake[0],114+shake[1],.9)
    for k in range(60): d.R(54,114+k*13,486,115+k*13,(0,0,0,60))
    v=int(70+70*abs(math.sin(u*3.2))); d.R(0,0,540,960,(255,0,30,int(v*.35)))
    # latido
    d.R(54,114,486,866,None,8,(255,60,70,int(120+120*abs(math.sin(u*3.2)))),4)
    return im
def sceneG(u):
    im=new((10,6,30),(46,12,70)); d=D(im); stars(d,u,60,960)
    for k in range(16):
        a=k*math.pi/8+u*.4; d.P([(270,430),(270+math.cos(a-.07)*800,430+math.sin(a-.07)*800),(270+math.cos(a+.07)*800,430+math.sin(a+.07)*800)],(255,230,150,12))
    b=sm(u/.8)*(1+.06*math.sin(u*4))
    d.E(270,430,200*b,200*b,(255,255,255,18)); sprite(d,270-132*b*.9,430-96*b*.9,I2[int(u*2)%2],(120,255,170),24*b*.9)
    ux=(u*80)%700-80; sprite(d,ux,120,UFO,(255,90,100),5.0)
    for k in range(26): a=k*.24+u*.4; r=250+rnd(k,3)*40; d.E(270+math.cos(a)*r,430+math.sin(a)*r*.8,4,4,(255,230,120,220))
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx==0: return 1.0+.9*sm(p),270,500-100*sm(p)
    if idx==1: return 1.0+.65*sm(p),270,560-60*sm(p)
    if idx==2: return 1.0+.1*sm(p),270,480
    if idx==3: return 1.0,270,480
    if idx==4: return 1.0+.3*sm(p),270,430
    if idx==5: return 1.0+.25*sm(p),270,480
    if idx==6: return 1.4-.4*sm(clamp(u/3)),270,470
    return 1.9-.9*sm(p),270,400+80*sm(p)
core.CAM=cam
if __name__=="__main__": core.main()
