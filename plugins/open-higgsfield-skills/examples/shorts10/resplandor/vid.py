import sys; sys.path.insert(0,"..")
from art import *
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
    for r in range(12): d.R(0,r*80,540,r*80+78,(60,40,30) if r%2 else (70,48,36),0)
    d.R(0,0,540,960,(0,0,0,90),0)
    stairs(d,20,820,420,320,12)
    bat_woman(d,300-(u*.0),520-12*0,1.5,u,swing=math.sin(u*3)*.3)
    silhouette(d,120,740,1.5,(6,6,8),arms=True)
    n=int(clamp(u/3.6)*127) if not final else 127
    slate_counter(d,380,170,n,.8,u)
    return im
def sceneB(u):
    im=new((14,10,12),(40,26,22)); d=D(im)
    corridor(d,u,speed=0.0,wall=(120,70,50),floor=(80,34,34),ceil=(50,36,30),door=(90,56,40),light=(255,232,190),pulse=1.0,n=9,doors=True)
    film_camera(d,150,860,1.0,u); clapper(d,400,880,.9,open_=(math.sin(u*3)>.4)*1.0)
    silhouette(d,270,870,1.3,(8,8,12)); d.R(250,740,290,770,(8,8,12),6)   # director con barba (silueta)
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
    for r in range(12): d.R(0,r*80,540,r*80+78,(60,40,30) if r%2 else (70,48,36),0)
    stairs(d,20,820,420,320,12)
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
    stairs(d,40,900,420,560,10,(110,80,56),False)
    # silueta sentada en la escalera, cansada
    sx,sy=250,740; d.E(sx,sy-90,16,18,(8,8,10)); d.R(sx-20,sy-74,sx+20,sy-10,(8,8,10),10); d.R(sx-36,sy-14,sx-8,sy+60,(8,8,10),6); d.R(sx+8,sy-14,sx+36,sy+60,(8,8,10),6)
    for k in range(3): 
        t=(u*.8+k*.33)%1; d.A(sx+60+k*16,sy-110-t*60,10,10,0,300,(255,255,255,int(200*(1-t))),3)
    return im
def sceneG(u):
    im=new((10,16,28),(24,40,64)); d=D(im)
    stairs(d,20,900,420,380,12,(70,90,120))
    bat_woman(d,260,520,1.5,u,swing=math.sin(u*3)*.3)
    for k in range(70):
        x=(rnd(k)*560+math.sin(u*1.3+k)*20)%560; y=(rnd(k,2)*960+u*(40+rnd(k,3)*50))%960; d.E(x,y,2+rnd(k,4)*2.4,2+rnd(k,4)*2.4,(235,244,255,180))
    d.R(0,0,540,960,(120,170,240,26),0)
    for k in range(5): d.A(60+k*110,60,40,18,0,180,(235,244,255,120),3)
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
