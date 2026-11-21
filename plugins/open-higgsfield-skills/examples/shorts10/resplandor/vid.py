import sys; sys.path.insert(0,"..")
from art import *

HEX=[(196,84,36),(122,52,30),(232,220,200),(168,40,40),(210,150,60)]
def hex_floor(d,u):
    """alfombra hexagonal del hotel: hexagonos en perspectiva sobre el suelo del pasillo"""
    for i in range(14,0,-1):
        t=i*.62; s_=depth(t); xl,xr,yt,yb=planes(s_); m=7; wc=(xr-xl)/m
        for k in range(m):
            cx=xl+(k+.5)*wc+(wc*.5 if i%2 else 0)
            if cx>xr: continue
            col=HEX[(k+i)%5]; rw=wc*.52; rh=wc*.2
            pts=[(cx-rw,yb),(cx-rw*.5,yb-rh),(cx+rw*.5,yb-rh),(cx+rw,yb),(cx+rw*.5,yb+rh),(cx-rw*.5,yb+rh)]
            d.P(pts,col+(235,))
            d.P([(cx-rw*.5,yb),(cx-rw*.25,yb-rh*.5),(cx+rw*.25,yb-rh*.5),(cx+rw*.5,yb),(cx+rw*.25,yb+rh*.5),(cx-rw*.25,yb+rh*.5)],HEX[(k+i+2)%5]+(235,))
def twins(d,x,y,sc):
    for dx in(-14,14):
        d.E(x+dx*sc,y-86*sc,8*sc,9*sc,(230,200,170)); d.E(x+dx*sc,y-92*sc,9*sc,6*sc,(60,44,34))
        d.P([(x+dx*sc-12*sc,y-76*sc),(x+dx*sc+12*sc,y-76*sc),(x+dx*sc+16*sc,y-22*sc),(x+dx*sc-16*sc,y-22*sc)],(110,170,220))
        d.R(x+dx*sc-9*sc,y-22*sc,x+dx*sc-3*sc,y,(236,236,240),2*sc); d.R(x+dx*sc+3*sc,y-22*sc,x+dx*sc+9*sc,y,(236,236,240),2*sc)
    d.L(x-6*sc,y-62*sc,x+6*sc,y-62*sc,(230,200,170),3*sc)
def stairs_hotel(d,x0,y0,x1,y1,n):
    # pared de madera con ventana luminosa al fondo y barandilla tallada
    d.R(0,0,540,960,(58,38,28,255),0)
    for k in range(9): d.R(k*66,0,k*66+4,960,(0,0,0,50),0)
    wx,wy=x1-70,y1-300
    d.R(wx-6,wy-6,wx+120,wy+190,(44,28,20),3); d.R(wx,wy,wx+114,wy+184,(255,236,190),3); d.L(wx+57,wy,wx+57,wy+184,(120,90,60),4); d.L(wx,wy+92,wx+114,wy+92,(120,90,60),4)
    d.P([(wx,wy+184),(wx+114,wy+184),(wx+260,y1+160),(wx-120,y1+160)],(255,236,190,26))
    stairs(d,x0,y0,x1,y1,n)
def hedge_maze(d,u):
    gradient(d,0,440,(10,18,44),(34,52,90))
    d.E(410,150,40,40,(236,240,250,230)); d.E(410,150,90,90,(236,240,250,36))
    corridor(d,u,speed=.06,wall=(26,70,46),floor=(226,232,244),ceil=(14,24,56),door=(20,50,34),light=(200,220,255),doors=False,lights=False,n=10,alt=0.0)
    xl,xr,yt,yb=planes(depth(0))
    for i in range(12):
        t=i*.8+.3; s_=depth(t); xa,xb,ya,yb2=planes(s_)
        d.R(xa-4,yb2-300*s_,xa+10*s_,yb2-296*s_,(240,246,255,230),1); d.R(xb-10*s_,yb2-300*s_,xb+4,yb2-296*s_,(240,246,255,230),1)
    d.R(0,0,0,0,(0,0,0,0),0)
def stairs(d,x0,y0,x1,y1,n,col=(120,86,60),rail=True):
    for k in range(n):
        x=x0+(x1-x0)*k/n; y=y0+(y1-y0)*k/n; w=(x1-x0)/n; h=(y0-y1)/n
        d.R(x,y-h,x+w*1.05,y+80,tuple(int(c*(.55+.4*k/n)) for c in col),0); d.R(x,y-h,x+w*1.05,y-h+6,(255,255,255,50),0)
        d.R(x,y,x+w*1.05,y+80,(0,0,0,50),0)
    if rail:
        d.L(x0,y0-90,x1,y1-90,(60,44,30),8)
        for k in range(0,n+1,2): x=x0+(x1-x0)*k/n; y=y0+(y1-y0)*k/n; d.L(x,y-90,x,y-6,(60,44,30),5)
def bat_woman(d,x,y,sc,u,swing=0.0):
    silhouette(d,x,y,sc,(10,10,14),arms=False)
    sh=(x+22*sc,y-120*sc); ang=-1.2+swing
    d.L(x-24*sc,y-118*sc,x-34*sc,y-90*sc,(10,10,14),7*sc)
    d.L(sh[0],sh[1],sh[0]+30*sc,sh[1]-18*sc,(10,10,14),7*sc)
    hand=(sh[0]+30*sc,sh[1]-18*sc); pts=rotpts([(hand[0]-4*sc,hand[1]-90*sc),(hand[0]+4*sc,hand[1]-90*sc),(hand[0]+6*sc,hand[1]+6*sc),(hand[0]-6*sc,hand[1]+6*sc)],hand[0],hand[1],ang+1.2)
    d.P(pts,(160,110,70))
def slate_counter(d,x,y,n,sc=1.0,u=0):
    clapper(d,x,y,sc*1.4,open_=(math.sin(u*6)>.5)*1.0)
    d.R(x-62*sc*1.4,y+24*sc*1.4,x+62*sc*1.4,y+78*sc*1.4,(20,20,24),4)
    for i,ch in enumerate(str(int(n)).zfill(3)): seg7(d,x-48*sc*1.4+i*32*sc*1.4,y+30*sc*1.4,26*sc*1.4,42*sc*1.4,int(ch),(255,255,255),(30,30,34))
def sceneA(u,final=False):
    im=new((20,14,12),(52,36,28)); d=D(im)
    stairs_hotel(d,20,820,420,320,12)
    bat_woman(d,300-(u*.0),520-12*0,1.5,u,swing=math.sin(u*3)*.3)
    silhouette(d,120,740,1.5,(6,6,8),arms=True)
    n=int(clamp(u/3.6)*127) if not final else 127
    slate_counter(d,380,170,n,.8,u); noise_static(d,0,0,540,960,u,16,6)
    return im
def sceneB(u):
    im=new((14,10,12),(40,26,22)); d=D(im)
    corridor(d,u,speed=0.0,wall=(120,70,50),floor=(80,34,34),ceil=(50,36,30),door=(90,56,40),light=(255,232,190),pulse=1.0,n=9,doors=True)
    hex_floor(d,u)
    s_=depth(9.2); twins(d,270,HY+300*s_,1.25)
    film_camera(d,150,860,1.0,u); clapper(d,400,880,.9,open_=(math.sin(u*3)>.4)*1.0)
    silhouette(d,270,880,1.3,(8,8,12)); d.R(250,750,290,780,(8,8,12),6)
    d.R(0,220,540,372,(0,0,0,225),0); ptext(d,46,262,"THE SHINING",5.6,(240,240,244))
    return im
def sceneC(u):
    im=new((10,12,18),(24,30,44)); d=D(im)
    n=int(clamp(u/5.0)*127); cols=11; 
    for k in range(min(n,132)):
        r,c=k//cols,k%cols; x=24+c*46; y=140+r*52
        d.R(x,y,x+40,y+30,(24,24,28),3); 
        for q in range(4): d.R(x+2+q*9,y+2,x+8+q*9,y+8,(255,255,255,230),1)
        if k==n-1: d.R(x-3,y-3,x+43,y+33,None,4,(255,214,90),3)
    number(d,150,800,n,3,56,110,(255,255,255)); 
    for k in range(2): 
        cx=60+k*420; cy=860; d.E(cx,cy,40,40,(40,42,52)); d.E(cx,cy,40,40,None,(120,124,140),3)
        for q in range(3): a=u*5+q*2.09+k; d.L(cx,cy,cx+math.cos(a)*34,cy+math.sin(a)*34,(190,194,204),3)
    return im
def sceneD(u):
    im=new((20,14,12),(52,36,28)); d=D(im)
    stairs_hotel(d,20,820,420,320,12)
    # copias fantasma de la misma escena repetida (tomas)
    for k in range(5):
        t=((u*.4+k*.2)%1.0)
        x=120+t*260; y=760-t*300; d.E(x,y,0,0,(0,0,0,0))
        bat_woman(d,x,y,1.4-.2*t,u+k,swing=math.sin((u+k)*3)*.3) if False else None
    cyc=(u*.55)%1.0
    x=140+cyc*220; y=740-cyc*260
    for g in range(4): 
        gx=140+((cyc-g*.08)%1.0)*220; gy=740-((cyc-g*.08)%1.0)*260
        silhouette(d,gx,gy,1.2,(10,10,14),arms=False); 
    bat_woman(d,x+40,y-6,1.3,u,swing=math.sin(u*4)*.4)
    silhouette(d,100,780,1.4,(6,6,8))
    n=int(clamp(u/6.0)*127); slate_counter(d,390,170,n,.8,u)
    return im
def sceneE(u):
    im=new((24,18,14),(60,44,34)); d=D(im)
    d.R(60,120,480,780,(236,226,200),10); d.R(60,120,480,780,None,10,(120,84,40),6)
    d.R(80,140,460,760,None,6,(150,110,60),2)
    for k in range(10): d.E(270+math.cos(k*.63)*120*0,0,0,0,(0,0,0,0))
    # laurel y sello con ciento veintisiete
    for sg in(-1,1):
        for k in range(8):
            a=.4+k*.2; d.E(270+sg*(110+math.cos(a)*30),360+k*26,16,8,(80,130,70))
    d.E(270,420,90,90,(214,170,72)); d.E(270,420,90,90,None,(150,110,30),6)
    number(d,196,380,127,3,34,70,(60,40,10))
    for k in range(6): d.R(110,590+k*24,430-(k%3)*50,602+k*24,(0,0,0,50),3)
    d.P([(220,520),(250,520),(250,640),(235,620),(220,640)],(200,40,50)); d.P([(290,520),(320,520),(320,640),(305,620),(290,640)],(200,40,50))
    for k in range(26): a=k*.24+u*.4; r=300+rnd(k,3)*50; d.P([(270+math.cos(a)*r,430+math.sin(a)*r*.8-7),(270+math.cos(a)*r+3,430+math.sin(a)*r*.8-2),(270+math.cos(a)*r+8,430+math.sin(a)*r*.8),(270+math.cos(a)*r+3,430+math.sin(a)*r*.8+2),(270+math.cos(a)*r,430+math.sin(a)*r*.8+7),(270+math.cos(a)*r-3,430+math.sin(a)*r*.8+2),(270+math.cos(a)*r-8,430+math.sin(a)*r*.8),(270+math.cos(a)*r-3,430+math.sin(a)*r*.8-2)],(255,230,120,210))
    return im
def sceneF(u):
    im=new((14,10,12),(30,22,24)); d=D(im)
    # calendario con paginas que pasan y reloj que corre
    d.R(40,100,260,360,(244,240,230),10); d.R(40,100,260,140,(200,50,60),10)
    pg=int(u*2)%20+1
    number(d,80,200,pg,2,46,86,(40,40,50))
    d.E(400,230,90,90,(244,244,240)); d.E(400,230,90,90,None,(40,40,46),6)
    for k in range(12): a=k*math.pi/6; d.L(400+math.cos(a)*76,230+math.sin(a)*76,400+math.cos(a)*86,230+math.sin(a)*86,(0,0,0),3)
    d.L(400,230,400+math.cos(u*14)*50,230+math.sin(u*14)*50,(0,0,0),6); d.L(400,230,400+math.cos(u*1.2)*34,230+math.sin(u*1.2)*34,(0,0,0),8)
    d.R(30,420,270,640,(244,242,230),4)
    for q in range(6): ptext(d,40,432+q*34,'ALL WORK AND NO PLAY',1.6,(30,30,34))
    stairs(d,40,900,420,560,10,(110,80,56),False)
    # silueta sentada en la escalera, cansada
    sx,sy=250,740; d.E(sx,sy-90,16,18,(8,8,10)); d.R(sx-20,sy-74,sx+20,sy-10,(8,8,10),10); d.R(sx-36,sy-14,sx-8,sy+60,(8,8,10),6); d.R(sx+8,sy-14,sx+36,sy+60,(8,8,10),6)
    for k in range(3): 
        t=(u*.8+k*.33)%1; d.A(sx+60+k*16,sy-110-t*60,10,10,0,300,(255,255,255,int(200*(1-t))),3)
    return im
def sceneG(u):
    im=new((10,16,28),(24,40,64)); d=D(im)
    hedge_maze(d,u)
    silhouette(d,270,HY+330,.9,(8,10,16))
    for k in range(70):
        x=(rnd(k)*560+math.sin(u*1.3+k)*20)%560; y=(rnd(k,2)*960+u*(40+rnd(k,3)*50))%960; d.E(x,y,2+rnd(k,4)*2.4,2+rnd(k,4)*2.4,(235,244,255,200))
    d.R(0,0,540,960,(120,170,240,24),0)
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx==0: return 1.0+.25*sm(p),270,500
    if idx==1: return 1.0+.35*sm(p),270,540
    if idx==2: return 1.0+.1*sm(p),270,480
    if idx==3: return 1.0+.2*sm(p),270,500
    if idx==4: return 1.0+.15*sm(p),270,470
    if idx==5: return 1.0+.1*sm(p),270,480
    if idx==6: return 1.3-.3*sm(p),270,500
    return 1.3-.3*sm(p),270,500
core.CAM=cam
if __name__=="__main__": core.main()
