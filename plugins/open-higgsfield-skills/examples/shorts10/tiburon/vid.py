import sys; sys.path.insert(0,"..")
from art import *
def boat(d,x,y,sc,u):
    by=y+math.sin(u*1.4)*3*sc; ang=math.sin(u*1.1)*.03
    d.E(x,by+16*sc,120*sc,10*sc,(0,0,0,60))
    d.P([(x-120*sc,by-30*sc),(x+130*sc,by-30*sc),(x+96*sc,by+18*sc),(x-96*sc,by+18*sc)],(96,52,40)); d.P([(x-120*sc,by-30*sc),(x+130*sc,by-30*sc),(x+126*sc,by-42*sc),(x-116*sc,by-42*sc)],(236,230,220))
    d.R(x-34*sc,by-96*sc,x+40*sc,by-42*sc,(226,220,208),4*sc); d.R(x-26*sc,by-84*sc,x+32*sc,by-60*sc,(30,60,90),3*sc)
    d.L(x+74*sc,by-42*sc,x+74*sc,by-150*sc,(60,60,70),4*sc); d.L(x+74*sc,by-150*sc,x+112*sc,by-60*sc,(60,60,70),2*sc)
def shark_mech(d,x,y,sc,u,mouth=.3):
    top=(98,118,140); bel=(226,230,234); lat=(170,184,198)
    shadow(d,x,y+44*sc,160*sc,10*sc,60)
    body=[(x-120*sc,y-6*sc),(x-50*sc,y-62*sc),(x+64*sc,y-62*sc),(x+150*sc,y-20*sc),(x+168*sc,y+4*sc),(x+110*sc,y+30*sc),(x+10*sc,y+44*sc),(x-100*sc,y+22*sc)]
    d.P(body,top+(255,))
    d.P([(x-100*sc,y+4*sc),(x-20*sc,y+14*sc),(x+80*sc,y+10*sc),(x+168*sc,y+4*sc),(x+110*sc,y+30*sc),(x+10*sc,y+44*sc),(x-100*sc,y+22*sc)],bel+(255,))
    d.L(x-100*sc,y,x+150*sc,y-6*sc,lat+(255,),3*sc)
    d.P([(x-118*sc,y-6*sc),(x-200*sc,y-74*sc),(x-176*sc,y-4*sc),(x-204*sc,y+58*sc)],mixc(top,(40,50,62),.3))
    d.P([(x-20*sc,y-58*sc),(x+40*sc,y-58*sc),(x+8*sc,y-140*sc)],mixc(top,(60,76,94),.3))
    d.P([(x+26*sc,y+26*sc),(x+92*sc,y+22*sc),(x+44*sc,y+84*sc)],mixc(top,(60,70,82),.4))
    d.E(x+122*sc,y-12*sc,7*sc,7*sc,(8,8,10)); d.E(x+120*sc,y-14*sc,2.6*sc,2.6*sc,(255,255,255))
    for k in range(5): d.L(x+104*sc+k*4*sc,y-2*sc,x+104*sc+k*4*sc+2*sc,y+10*sc,(40,50,60),2*sc)
    # boca abierta con filas de dientes
    mo=mouth*18*sc
    d.P([(x+86*sc,y+14*sc),(x+170*sc,y+6*sc+mo),(x+168*sc,y+36*sc+mo),(x+84*sc,y+34*sc)],(120,18,26))
    for row,off in enumerate((0,6,12)):
        for k in range(9): d.P([(x+90*sc+k*8*sc,y+12*sc+off*sc*.0),(x+94*sc+k*8*sc,y+22*sc+off*.6*sc),(x+98*sc+k*8*sc,y+12*sc)],(250,250,244))
        for k in range(9): d.P([(x+88*sc+k*8*sc,y+34*sc+mo),(x+92*sc+k*8*sc,y+24*sc+mo),(x+96*sc+k*8*sc,y+34*sc+mo)],(244,244,238))
    # corrosion: manchas de sal blanca y verdin
    for k in range(18):
        a=rnd(k)*6.28; r=rnd(k,1)*110*sc; d.E(x+math.cos(a)*r*1.1,y+math.sin(a)*r*.34,(4+rnd(k,2)*8)*sc,(3+rnd(k,3)*5)*sc,(255,255,255,150) if k%3 else (96,150,96,150))
def rig(d,x,y,sc):
    d.R(x-10*sc,y-160*sc,x+10*sc,y+4*sc,(96,100,110),2*sc); d.R(x-90*sc,y-170*sc,x+10*sc,y-150*sc,(96,100,110),3*sc)
    for k in range(4): d.L(x-84*sc+k*24*sc,y-170*sc,x-72*sc+k*24*sc,y-150*sc,(60,64,72),2*sc)
    for k in range(3):
        pts=[(x-70*sc+k*14*sc,y-150*sc),(x-20*sc+k*30*sc,y-120*sc),(x+60*sc+k*20*sc,y-60*sc),(x+150*sc,y-20*sc+k*4*sc)]
        for i in range(len(pts)-1): d.L(pts[i][0],pts[i][1],pts[i+1][0],pts[i+1][1],(20,20,24),4*sc)
    d.E(x-10*sc,y-150*sc,12*sc,12*sc,(150,154,164)); d.E(x-10*sc,y-150*sc,5*sc,5*sc,(60,64,72))
def sceneA(u,final=False):
    im=new((250,160,90),(255,214,150)); d=D(im)
    ocean(d,u,hz=520,sky=(246,150,80),sky2=(255,214,150),sea=(40,84,110),sea2=(10,28,50))
    d.E(270,470,70,70,(255,236,170,230)); d.E(270,470,150,150,(255,236,170,50))
    for k,(x,y) in enumerate([(120,820),(410,860)]): barrel(d,x,y,1.4+.1*k,u)
    p=sm(u/4.0) if not final else 1.0
    fin(d,150+p*220,640+p*0+math.sin(u*2)*2,1.0+p*1.6,u)
    return im
def sceneB(u):
    im=new((90,150,210),(210,232,248)); d=D(im)
    ocean(d,u,hz=470); glints(d,u,470,50)
    d.R(0,430,100,470,(90,110,70),0); d.E(40,440,90,30,(90,110,70))
    boat(d,300,640,1.7,u)
    # equipo de rodaje en la cubierta: camara, director y claqueta
    film_camera(d,180,640,.52,u)
    silhouette(d,250,630,.55,(34,34,44)); silhouette(d,340,632,.55,(60,40,34))
    d.R(246,520,264,536,(230,60,70),2)
    clapper(d,430,560,.45,open_=(math.sin(u*3)>0.4)*1.0)
    return im
def sceneC(u):
    im=new((90,150,210),(210,232,248)); d=D(im)
    ocean(d,u,hz=470)
    # plataforma con el tiburon mecanico saliendo del agua, fallando
    d.R(40,560,500,600,(110,112,122),4)
    for k in range(10): d.L(40+k*46,560,60+k*46,600,(70,72,82),3)
    sh=sin_=math.sin(u*3)
    y=720+math.sin(u*2.2)*10
    shark_mech(d,290,y,1.3,u,mouth=(1+math.sin(u*5))*.5)
    rig(d,120,y+10,1.4)
    # chispas y sal blanca (el agua salada estropea los mecanismos)
    for k in range(24):
        t=(u*1.4+rnd(k))%1; x=210+rnd(k,2)*260; yy=y-30-t*90
        d.E(x,yy,3,3,(255,255,255,int(230*(1-t))))
    for k in range(6):
        t=(u*2+k*.33)%1; d.L(250+k*22,y-40,250+k*22+rnd(k,3)*30-15,y-40-t*60,(255,220,90,int(255*(1-t))),3)
    # aviso de error
    if int(u*2)%2==0: d.E(430,200,48,48,(230,60,70)); d.R(424,176,436,214,(255,255,255),3); d.E(430,228,6,6,(255,255,255))
    for k in range(3): d.E(80+k*40,190-((u*30+k*20)%70),14+k*6,10+k*4,(220,220,230,90))
    return im
def sceneD(u):
    im=new((26,24,36),(52,44,60)); d=D(im)
    d.R(0,640,540,960,(40,34,44)); d.R(0,640,540,646,(255,255,255,24))
    # guion grafico: tiburon completo tachado frente a barriles y agua
    d.R(30,160,250,330,(244,240,226),6); shark_mech(d,140,260,.5,u)
    d.L(40,170,240,320,(220,50,60),9); d.L(240,170,40,320,(220,50,60),9)
    d.R(290,160,510,330,(244,240,226),6)
    for k in range(3): barrel(d,330+k*60,260,.9,u)
    d.L(300,310,500,310,(60,100,160),6)
    # director con idea
    silhouette(d,270,720,1.6,(30,30,40)); gl=.7+.3*math.sin(u*6); d.E(270,560,56,56,(255,230,120,int(60*gl))); d.E(270,560,24,28,(255,236,140)); d.R(262,580,278,594,(150,150,160),3)
    clapper(d,420,720,.9,open_=sm(math.sin(u*2)))
    return im
def sceneE(u):
    im=new((24,60,92),(8,22,44)); d=D(im)
    ocean(d,u,hz=500,sky=(30,50,90),sky2=(120,140,180),sea=(10,44,76),sea2=(4,14,34))
    stars(d,u,30,300); glints(d,u,500,40,(255,255,255))
    # barco de pesca a lo lejos, persiguiendo a los barriles
    bx=380+math.sin(u*.4)*10; d.P([(bx-50,490),(bx+60,490),(bx+44,508),(bx-40,508)],(30,34,44)); d.R(bx-14,462,bx+22,490,(220,214,200),2); d.L(bx+34,490,bx+34,440,(40,44,54),2)
    pos=[(120,700),(280,740),(420,690)]
    for k,(x,y) in enumerate(pos):
        dip=sm((u-2.0-k*1.2)/.6)*(1 if k==1 else 0)
        # cuerda hacia el agua (arpon) y barril
        d.L(x,y+8,x+40,y+90,(150,120,80,200),3); 
        barrel(d,x,y+dip*70,1.5,u)
        if dip>0: d.E(x,y+10,50*dip,10*dip,None,(255,255,255,int(160*(1-dip))),3)
    for i in range(2):
        a=(math.sin(u*(2+u*.6)*1.0+i*math.pi)*.5+.5)
        d.R(190+i*90,860-a*80,250+i*90,900,(255,214,120,int(80+170*a)),8)
    return im
def sceneF(u):
    im=new((10,8,14),(24,16,30)); d=D(im)
    # pantalla de cine con mar y filas de espectadores de espaldas
    d.R(40,120,500,440,(18,22,30),6); 
    for k in range(10): d.R(40,120+k*32,500,152+k*32,mixc((90,140,200),(20,60,110),k/9.0),0)
    fin(d,250+math.sin(u*.5)*80,300,1.0+.2*u*0.1,u)
    d.R(40,120,500,440,None,6,(255,255,255,60),3)
    d.P([(270,60),(60,440),(480,440)],(255,255,255,14))
    for r in range(4):
        for c in range(7):
            x=40+c*75+(r%2)*30; y=560+r*90; sc=1.0+r*.3
            col=(10+r*6,8+r*6,14+r*6)
            d.E(x,y,22*sc,26*sc,col+(255,)); d.R(x-30*sc,y+20*sc,x+30*sc,y+80*sc,col+(255,),10*sc)
            if (r+c)%3==0 and u>2.0: d.R(x-26*sc,y+2*sc,x+26*sc,y+20*sc,col+(255,),5*sc)   # manos tapandose los ojos
            d.E(x,y,22*sc,26*sc,(90,140,200,int(40*(1-r*.2))))
    return im
def sceneG(u):
    im=new((190,226,246),(8,26,60)); d=D(im)
    for k in range(18): d.R(0,k*54,540,k*54+54,mixc((190,226,246),(4,14,38),(k/17.0)**.7),0)
    for k in range(10):
        a=-1.57+(k-5)*.16; d.P([(270,300),(270+math.cos(a-.04)*700,300+math.sin(a-.04)*700+400),(270+math.cos(a+.04)*700,300+math.sin(a+.04)*700+400)],(255,255,255,18))
    # superficie y nadadora
    d.R(0,280,540,292,(255,255,255,200),0)
    sx=270+math.sin(u*.8)*30; sy=262+math.sin(u*1.7)*3
    d.E(sx,sy,18,14,(20,24,34)); d.R(sx-44,sy-4,sx-16,sy+4,(20,24,34),3); d.R(sx+18,sy-4,sx+46,sy+4,(20,24,34),3)
    for k in range(3): d.L(sx-54+k*6,sy+10,sx-70+k*6,sy+24,(255,255,255,160),2)
    # tiburon enorme que sube desde abajo con la boca abierta
    rise=sm(u/2.0)
    shark_mech(d,270,1180-rise*420,2.1,u,mouth=1.0)
    d.R(0,0,540,960,(0,0,0,0),0)
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx==0: return 1.0+.45*sm(p),270,640
    if idx==1: return 1.0+.25*sm(p),270,560
    if idx==2: return 1.0+.2*sm(p),290,560
    if idx==3: return 1.0+.2*sm(p),270,520
    if idx==4: return 1.0+.35*sm(p),270,660
    if idx==5: return 1.0+.1*sm(p),270,480
    if idx==6: return 1.3-.3*sm(p),270,620
    return 1.5-.5*sm(p),270,660
core.CAM=cam
if __name__=="__main__": core.main()
