import sys; sys.path.insert(0,"..")
from art import *
from common import tv
def ps4(d,x,y,sc,u):
    shadow(d,x,y+4,120*sc,10*sc,80)
    d.P([(x-120*sc,y),(x+100*sc,y),(x+120*sc,y-60*sc),(x-100*sc,y-60*sc)],(26,26,32)); d.P([(x-100*sc,y-60*sc),(x+120*sc,y-60*sc),(x+110*sc,y-70*sc),(x-90*sc,y-70*sc)],(46,46,56))
    d.P([(x-110*sc,y-28*sc),(x+110*sc,y-28*sc),(x+112*sc,y-34*sc),(x-108*sc,y-34*sc)],(60,120,255,230)); d.E(x+80*sc,y-12*sc,4*sc,4*sc,(80,160,255))
def tile(d,x,y,w,h,col,inner=None,sel=False,a=255):
    d.R(x,y,x+w,y+h,col+(a,),8)
    if inner: inner(d,x,y,w,h)
    if sel: d.R(x-4,y-4,x+w+4,y+h+4,None,10,(255,255,255,int(230*a/255)),3)
def hall_img(d,x,y,w,h):
    d.R(x,y,x+w,y+h,(22,16,14)); d.P([(x+w*.1,y),(x+w*.9,y),(x+w*.62,y+h*.36),(x+w*.38,y+h*.36)],(120,92,70)); d.P([(x,y+h),(x+w,y+h),(x+w*.62,y+h*.52),(x+w*.38,y+h*.52)],(50,34,24))
    d.R(x+w*.38,y+h*.36,x+w*.62,y+h*.52,(6,6,8)); d.E(x+w*.5,y+h*.1,w*.14,h*.05,(255,226,160,150)); ptext(d,x+w*.5-24,y+h*.58,'P.T.',4.0,(255,255,255),230)
def store(d,u,vanish=0.0):
    gradient(d,0,960,(14,40,96),(8,16,52))
    for k in range(5): 
        pts=[(x,260+math.sin(x/70+u*.8+k)*28+k*70) for x in range(-10,560,20)]
        for i in range(len(pts)-1): d.L(pts[i][0],pts[i][1],pts[i+1][0],pts[i+1][1],(255,255,255,18),6)
    d.R(0,0,540,100,(8,20,56),0)
    for k in range(5): d.R(30+k*60,38,70+k*60,60,(255,255,255,60+ (80 if k==1 else 0)),6)
    cols=[(60,100,200),(180,70,90),(80,160,120),(200,160,60),(120,80,180),(60,160,200)]
    # rejilla de mosaicos; el de P.T. (indice 1) se esfuma
    k=0
    for r in range(3):
        for c in range(2):
            x=36+c*236; y=160+r*210; idx=r*2+c
            if idx==1:
                a=1.0-vanish
                tile(d,x,y,220,180,(30,30,36),hall_img,sel=True,a=int(255*a))
                if vanish>0:
                    d.E(x+110,y+90,40*vanish,40*vanish,None,(255,255,255,int(255*vanish)),5)
                    d.L(x+84,y+64,x+136,y+116,(240,70,70,int(255*vanish)),9); d.L(x+136,y+64,x+84,y+116,(240,70,70,int(255*vanish)),9)
            else: tile(d,x,y,220,180,cols[idx%6])

def pt_details(d,u,lap=0):
    """pasillo de P.T.: empapelado floral, rodapie, cuadros, lampara colgante y radio sobre una mesa"""
    for side in(-1,1):
        for k in range(1,18):
            t=k*.5; s=depth(t); xl,xr,yt,yb=planes(s); x=xl+ (14*s if side<0 else -14*s) if side<0 else xr-14*s
            for r in range(5):
                y=HY-250*s+r*95*s
                d.E(x,y,5*s*2.2,5*s*2.2,(120,92,72,150)); d.E(x,y,2*s*2.2,2*s*2.2,(190,160,120,150))
    near,far=depth(0),depth(10)
    for t in (1.6,3.5,5.2):
        s1,s2=depth(t),depth(t+.6); xa=planes(s1)[0]; xb=planes(s2)[0]
        yt1,yb1=HY-120*s1,HY+30*s1; yt2,yb2=HY-120*s2,HY+30*s2
        d.P([(xa,yt1),(xb,yt2),(xb,yb2),(xa,yb1)],(60,42,30)); d.P([(xa+4*s1,yt1+8*s1),(xb-2*s2,yt2+6*s2),(xb-2*s2,yb2-6*s2),(xa+4*s1,yb1-8*s1)],(150,160,170))
    s=depth(2.2); d.L(270,HY-330*s,270,HY-210*s,(40,34,30),4*s*2); d.E(270,HY-204*s,10*s*2,12*s*2,(255,238,180)); d.E(270,HY-204*s,60*s*2,60*s*2,(255,238,180,int(60*(0.8+0.2*math.sin(u*9+lap)))))
    s=depth(6.8); xr=planes(s)[1]; yy=HY+90*s
    d.R(xr-70*s*2,yy,xr-10*s*2,yy+16*s*2,(40,30,24),2); d.R(xr-62*s*2,yy-26*s*2,xr-22*s*2,yy,(24,24,28),2*s*2); d.L(xr-30*s*2,yy-26*s*2,xr-18*s*2,yy-50*s*2,(200,200,210),2*s*2)
    d.E(xr-54*s*2,yy-8*s*2,2.4*s*2,2.4*s*2,(255,70,60) if int(u*3)%2==0 else (90,30,24))
    noise_static(d,0,0,540,960,u,22,6)
def sceneA(u,final=False):
    im=new((14,40,96),(8,16,52)); d=D(im)
    store(d,u,vanish=sm((u-1.6)/1.4) if not final else 1.0)
    return im
def sceneB(u):
    im=new((26,22,40),(60,50,70)); d=D(im)
    d.R(0,660,540,960,(40,34,44)); d.R(0,660,540,666,(255,255,255,24))
    tv(d,80,230,380,340,lambda d_,x,y,w,h:hall_img(d_,x,y,w,h),u)
    ps4(d,270,780,1.0,u)
    # mando con barra de luz
    d.P([(330,860),(450,860),(470,900),(310,900)],(30,30,36)); d.E(390,852,40,5,(60,120,255)); d.E(350,885,12,12,(20,20,26)); d.E(430,885,12,12,(20,20,26))
    d.R(40,100,200,200,(244,240,230),6); d.R(40,100,200,128,(200,50,60),6)
    d.R(80,150,160,170,(210,210,220),2)
    d.R(330,90,500,150,(60,200,120),12); d.R(340,100,490,140,None,10,(255,255,255,200),3)
    return im
def sceneC(u):
    lap=int(u/1.8); ph=(u%1.8)/1.8
    wall=[(150,126,98),(150,126,98),(124,96,84),(104,70,66),(70,44,48)][min(4,lap)]
    lt=[(255,236,190),(255,236,190),(255,214,150),(255,150,120),(230,60,50)][min(4,lap)]
    im=new((10,8,10),(20,16,18)); d=D(im)
    corridor(d,u,speed=.35,wall=wall,floor=(70,48,34),ceil=(46,38,36),door=(86,60,44),light=lt,pulse=flicker(u,1,8) if lap>=2 else 1.0,n=9)
    pt_details(d,u,lap)
    xl,xr,yt,yb=planes(depth(3))
    d.R(xl+6,HY-30,xl+60,HY+60,(244,240,230)); 
    d.R(xr-60,HY-30,xr-6,HY+60,(244,240,230)); 
    if lap>=1: d.R(xr-40,HY+100,xr-6,HY+130,(30,30,34),3); d.E(xr-22,HY+115,6,6,(255,60,60))
    s=depth(9.2)
    d.R(270-30*s*2,HY-60*s*2,270+30*s*2,HY+60*s*2,(4,4,6))
    if lap>=3: silhouette(d,270,HY+60*s*2,.55,(4,4,6))
    # marcador de vuelta e indicador de bucle
    d.R(24,36,210,100,(0,0,0,150),12)
    for i in range(5): d.E(46+i*34,68,10,10,(255,255,255,255) if i<=lap else (255,255,255,60))
    d.A(440,68,26,26,40,330,(255,255,255,230),6); d.P([(462,32),(484,52),(450,56)],(255,255,255))
    return im
def sceneD(u):
    im=new((10,12,28),(30,18,48)); d=D(im)
    for k in range(14): d.E(rnd(k)*540,rnd(k,1)*400,2,2,(255,255,255,150))
    for r in range(4): fogband(d,u,560+r*50,640+r*50,(180,184,200),24,5)
    cards=[(30,"dir"),(190,"clap"),(350,"star")]
    for i,(x,kind) in enumerate(cards):
        a=sm((u-.5-i*1.2)/.5); 
        if a<=0: continue
        y=250+(1-a)*40
        d.R(x,y,x+160,y+240,(24,22,40,int(255*a)),16); d.R(x,y,x+160,y+240,None,16,(255,255,255,int(90*a)),2)
        cx,cy=x+80,y+110
        if kind=="dir":   # silla de director / megafono
            d.P([(cx-34,cy-20),(cx+34,cy-20),(cx+54,cy+30),(cx-54,cy+30)],(220,200,120,int(255*a))); d.R(cx-6,cy+30,cx+6,cy+70,(200,180,100,int(255*a)),2)
        elif kind=="clap": clapper(d,cx,cy+10,.8,open_=(math.sin(u*3)*.5+.5))
        else:
            pts=[]
            for k in range(10): r_=44 if k%2==0 else 18; ang=-math.pi/2+k*math.pi/5; pts.append((cx+math.cos(ang)*r_,cy+math.sin(ang)*r_))
            d.P(pts,(255,214,90,int(255*a)))
        ptext(d,x+14,y+186,['KOJIMA','DEL TORO','REEDUS'][i],3.2,(255,255,255),int(230*a))
    if u>4.2:
        b=sm((u-4.2)/.8); d.E(270,150,180*b,46*b,(190,194,210,int(90*b)))
        ptext(d,60,120,'SILENT HILLS',9.0,(235,238,244),int(255*b))
    return im
def sceneE(u):
    im=new((24,18,24),(52,36,44)); d=D(im)
    # calendario que pasa a 2015
    cx,cy=270,300
    d.R(130,150,410,420,(244,240,230),14); d.R(130,150,410,196,(200,50,60),14)
    for r in range(4):
        for c in range(6): d.R(146+c*42,222+r*46,174+c*42,254+r*46,(215,215,224),3)
    d.R(130,150,410,420,None,14,(0,0,0,60),3)
    flip=sm((u-1.2)/.5)
    d.R(130,420-270*flip,410,420,(255,255,255,0),0)
    # caja del juego con sello de cancelado
    d.R(130,520,410,780,(26,24,36),10); hall_img(d,142,534,256,170); d.R(142,712,398,764,(70,70,90),6)
    s=sm((u-2.6)/.4); sz=1.0+.8*(1-s)
    if s>0:
        d.L(120,510,420,790,(230,50,60,int(255*s)),14); d.L(420,510,120,790,(230,50,60,int(255*s)),14)
        d.E(270,650,150*sz,150*sz,None,(230,50,60,int(255*s)),10)
    return im
def sceneF(u):
    im=new((14,40,96),(8,16,52)); d=D(im)
    store(d,u,vanish=.0)
    # cambio: en la biblioteca, el mosaico se oscurece y aparece un candado
    g=sm((u-1.0)/2.0)
    tile(d,272,160,220,180,(30,30,36),hall_img,False,255)
    d.R(272,160,492,340,(20,20,28,int(200*g)),8)
    if g>.3:
        d.R(350,230,414,290,(200,200,210,int(255*g)),8); d.A(382,230,22,26,180,360,(200,200,210,int(255*g)),8); d.E(382,260,5,5,(40,40,50,int(255*g)))
    # flecha de descarga bloqueada
    d.R(60,820,480,880,(30,60,140),14); d.P([(150,836),(190,836),(170,866)],(255,255,255,90)); d.L(250,840,330,860,(255,255,255,60),6)
    d.L(130,826,214,874,(240,70,70,int(255*g)),7); d.L(214,826,130,874,(240,70,70,int(255*g)),7)
    # consola vacia
    return im
def sceneG(u):
    im=new((10,8,10),(24,18,20)); d=D(im)
    corridor(d,u,speed=.15,wall=(124,96,84),floor=(60,40,30),ceil=(40,32,32),door=(70,50,40),light=(255,226,170),pulse=flicker(u,2,7),n=9)
    pt_details(d,u,0)
    fade=sm(u/6.0); d.R(0,0,540,960,(8,6,8,int(200*fade)),0)
    for k in range(20): a=k*.31+u*.3; d.E(270+math.cos(a)*220,430+math.sin(a)*260,3,3,(255,236,190,int(120*(1-fade))))
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx==0: return 1.0+.3*sm(p),310,420
    if idx==1: return 1.0+.2*sm(p),270,500
    if idx==2: return 1.0+.45*sm(p),270,470
    if idx==3: return 1.0+.15*sm(p),270,480
    if idx==4: return 1.0+.25*sm(p),270,470
    if idx==5: return 1.0+.25*sm(p),330,320
    if idx==6: return 1.2-.2*sm(p),270,470
    return 1.3-.3*sm(p),310,430
core.CAM=cam
if __name__=="__main__": core.main()
