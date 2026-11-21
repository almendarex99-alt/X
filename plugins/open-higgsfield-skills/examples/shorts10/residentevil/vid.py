import sys; sys.path.insert(0,"..")
from art import *
from PIL import Image, ImageOps
import numpy as np
WOOD=(92,58,42); GOLD=(214,170,72)

_BAY=np.array([[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]],dtype=np.float32)
def ps1f(im,block=6):
    """aspecto PlayStation 1996: baja resolucion, colores reducidos con trama (dither) y pixeles grandes"""
    w,h=im.size; sm_=im.resize((w//block,h//block),Image.BOX)
    a=np.array(sm_).astype(np.float32)
    bay=np.tile(_BAY,(a.shape[0]//4+1,a.shape[1]//4+1))[:a.shape[0],:a.shape[1]]
    a=a+(bay[...,None]-7.5)*1.4
    a=np.clip(np.round(a/16.0)*16.0,0,255).astype(np.uint8)
    return Image.fromarray(a).resize((w,h),Image.NEAREST)
def foyer(d,u,light=1.0):
    gradient(d,0,640,(34,22,20),(70,44,36))
    for k in range(9): d.R(k*66,230,k*66+60,600,(0,0,0,40),3); d.R(k*66+4,236,k*66+56,594,(255,255,255,10),3)
    d.R(0,224,540,234,(190,150,70),0); d.R(0,596,540,606,(190,150,70),0)
    # suelo de baldosas y alfombra
    d.R(0,606,540,960,(70,60,52),0)
    for r in range(8):
        for c in range(14):
            if (r+c)%2==0: d.R(c*40,606+r*50,c*40+40,606+r*50+50,(116,100,84),0)
    # escalera central con alfombra roja
    for k in range(10):
        x0=120+k*8; x1=420-k*8; y=606-k*28
        d.R(x0,y-28,x1,y,(98,64,48),0); d.R(x0,y-28,x1,y-22,(150,110,80),0); d.R(x0+30,y-28,x1-30,y,(150,30,36),0)
    d.R(100,252,440,282,(66,44,36),0)
    for k in range(10): d.R(104+k*34,224+0,112+k*34,282,(40,26,22),0)
    # puerta del rellano y puertas laterales
    d.R(236,150,304,252,(38,24,20),2); d.R(242,156,298,252,(110,70,48),2); d.E(270,150,34,22,(38,24,20))
    for x in(30,440): d.R(x,330,x+70,606,(44,28,22),3); d.R(x+6,336,x+64,606,(104,66,46),3); d.E(x+50,470,3,3,(220,180,80))
    # lampara de arana con velas
    d.E(270,96,70,18,(200,160,70)); d.L(270,0,270,80,(120,100,60),4)
    for k in range(8):
        a=k*math.pi/4; cx=270+math.cos(a)*62; cy=96+math.sin(a)*14
        d.R(cx-3,cy-20,cx+3,cy,(244,240,226),1); d.P([(cx-3,cy-20),(cx+3,cy-20),(cx,cy-34-(math.sin(u*9+k)*3))],(255,200,80,int(255*light)))
    d.E(270,120,160,70,(255,214,140,int(34*light)))
def door_wood(d,cx,by,w,h,openp):
    d.R(cx-w-10,by-h-12,cx+w+10,by,(44,30,24),4); d.R(cx-w,by-h,cx+w,by,(4,4,6),0)
    if openp>0: d.R(cx-w,by-h,cx+w,by,(255,214,140,int(210*openp)),0)
    for sg,hx in((1,cx-w),(-1,cx+w)):
        ww=w*max(.07,math.cos(openp*1.38)); sk=h*.05*math.sin(openp*1.38); x2=hx+sg*ww
        d.P([(hx,by-h),(x2,by-h+sk),(x2,by-sk),(hx,by)],(96,58,36))
        for q in range(14): 
            yy=by-h+q*h/14; d.L(hx,yy,x2,yy+ (sk if q%2 else -sk*.2),(60,34,22,160),3)
        for q in range(2):
            y_=by-h*(.30+.42*q); d.P([(hx+sg*ww*.16,y_-h*.15),(hx+sg*ww*.84,y_-h*.15+sk*.5),(hx+sg*ww*.84,y_+h*.12),(hx+sg*ww*.16,y_+h*.12)],(64,38,26))
        d.E(hx+sg*ww*.86,by-h*.46,6,6,(226,184,80))
def zombie(d,x,y,sc,u,col=(10,8,10)):
    sw=math.sin(u*2.2)*5*sc
    d.E(x+8*sc+sw*.4,y-146*sc,15*sc,17*sc,col+(255,)); d.R(x-18*sc+sw*.3,y-130*sc,x+22*sc+sw*.3,y-62*sc,col+(255,),9*sc)
    d.R(x-14*sc,y-66*sc,x-2*sc,y,col+(255,),4*sc); d.R(x+4*sc,y-66*sc,x+16*sc,y,col+(255,),4*sc)
    for sg in(-1,1): d.P(rotpts([(x+sg*14*sc,y-126*sc),(x+sg*24*sc,y-126*sc),(x+sg*28*sc,y-70*sc),(x+sg*18*sc,y-70*sc)],x+sg*14*sc,y-126*sc,-1.25*sg*0+(-1.1 if sg>0 else 1.1)*0+ (math.pi/2.6)*(-sg)*0),col+(255,))
    d.R(x-34*sc+sw,y-128*sc,x-24*sc+sw,y-92*sc,col+(255,),4*sc); d.R(x+22*sc+sw,y-128*sc,x+32*sc+sw,y-92*sc,col+(255,),4*sc)
def leaf(d,hx,by,w,h,openp,hinge=1,col=(104,66,46)):
    ww=w*max(.07,math.cos(openp*1.38)); sk=h*.05*math.sin(openp*1.38)
    x2=hx+hinge*ww
    d.P([(hx,by-h),(x2,by-h+sk),(x2,by-sk),(hx,by)],col+(255,))
    d.P([(hx,by-h),(x2,by-h+sk),(x2,by-h+sk+10),(hx,by-h+10)],(255,255,255,30))
    for q in range(2):
        yy=by-h*(.30+.40*q); d.P([(hx+hinge*ww*.18,yy-h*.14),(hx+hinge*ww*.82,yy-h*.14+sk*.5),(hx+hinge*ww*.82,yy+h*.12),(hx+hinge*ww*.18,yy+h*.12)],(70,42,30,255))
    d.E(hx+hinge*ww*.86,by-h*.46,4,4,GOLD)
def double_door(d,cx,by,w,h,openp,light=(255,214,140)):
    d.R(cx-w-10,by-h-12,cx+w+10,by,(44,30,24),4); d.R(cx-w,by-h,cx+w,by,(4,4,6),0)
    if openp>0: d.R(cx-w,by-h,cx+w,by,light+(int(210*openp),),0)
    leaf(d,cx-w,by,w,h,openp,1); leaf(d,cx+w,by,w,h,openp,-1)
    d.P([(cx-w-10,by-h-12),(cx+w+10,by-h-12),(cx,by-h-52)],(60,40,32))
def mansion(d,u,speed=.12,door_open=0.0,light=1.0,zomb=None):
    corridor(d,u,speed=speed,wall=(96,60,44),floor=(70,32,36),ceil=(40,26,24),door=(70,44,32),light=(255,214,140),pulse=light,doors=True,n=8)
    # puerta doble al fondo
    s=depth(8.3); cx=270
    double_door(d,cx,HY+300*s-10,170*s,330*s,door_open)
    if zomb is not None: zombie(d,cx+zomb[0]*s,HY+300*s-10,zomb[1]*s*2.4,u)
def ps1(d,x,y,sc,u):
    shadow(d,x,y+4,120*sc,12*sc,80)
    bevel(d,x-110*sc,y-70*sc,x+110*sc,y,(178,178,184),10*sc)
    d.R(x-110*sc,y-30*sc,x+110*sc,y-26*sc,(0,0,0,50),0)
    d.E(x,y-70*sc,64*sc,12*sc,(150,150,158)); d.E(x,y-74*sc,36*sc,8*sc,(210,210,218))
    d.E(x+70*sc,y-18*sc,7*sc,7*sc,(90,255,140)); d.E(x-70*sc,y-18*sc,7*sc,7*sc,(255,90,90))
def tv(d,x,y,w,h,inner,u):
    bevel(d,x,y,x+w,y+h,(62,60,70),14); d.R(x+10,y+10,x+w-10,y+h-18,(4,6,10),8)
    inner(d,x+10,y+10,w-20,h-28); 
    for k in range(int((h-28)/5)): d.R(x+10,y+10+k*5,x+w-10,y+11+k*5,(0,0,0,50))
    d.E(x+w-24,y+h-9,3,3,(80,255,140))
def sceneA(u,final=False):
    im=new((34,22,20),(70,44,36)); d=D(im)
    foyer(d,u,flicker(u,1,5))
    pxp=270+math.sin(u*.5)*30; silhouette(d,pxp,820,1.3,(8,6,8))
    return ps1f(im)
def sceneB(u):
    im=new((26,22,40),(60,50,70)); d=D(im)
    d.R(0,640,540,960,(54,40,40)); d.R(0,640,540,646,(255,255,255,24))
    def inner(d_,x,y,w,h):
        d_.R(x,y,x+w,y+h,(30,14,14)); d_.R(x+8,y+h*.4,x+w-8,y+h-6,(70,36,30))
        double_door(d_,x+w/2,y+h-8,w*.14,h*.46,0)
    tv(d,90,330,360,330,inner,u)
    ps1(d,270,760,1.0,u)
    # mando con cable
    bevel(d,330,800,450,850,(178,178,184),20); d.R(346,816,360,834,(60,60,70),2); d.R(340,822,366,828,(60,60,70),2)
    for k,c in enumerate([(70,200,110),(230,90,160),(230,60,60),(70,110,230)]): d.E(404+(k%2)*18-9,820+(k//2)*16-8,5,5,c)
    d.L(390,800,320,740,(60,60,70),3)
    # calendario 1996 y director
    d.R(40,120,200,290,(244,240,230),6); d.R(40,120,200,150,(200,50,60),6)
    for r in range(3):
        for c in range(4): d.R(52+c*34,164+r*38,76+c*34,190+r*38,(210,210,220) if (r*4+c)!=int(u*1.2)%12 else (255,210,80),2)
    person_back(d,420,900,1.1,0,u) if False else None
    return im
def sceneC(u):
    im=new((10,14,24),(24,30,50)); d=D(im)
    for r in range(30): d.L(0,r*32,540,r*32,(255,255,255,8),1)
    for c in range(18): d.L(c*32,0,c*32,960,(255,255,255,8),1)
    # plano de la mansion (habitaciones)
    rooms=[(30,150,140,110),(180,150,150,110),(340,150,170,110),(30,280,100,150),(140,280,200,150),(350,280,160,150),(30,440,160,110),(200,440,140,110),(350,440,160,110)]
    cur=int((u*.8)%9)
    loaded=[i for i in range(9) if i<=cur+0]
    for i,(x,y,w,h) in enumerate(rooms):
        on=(i==cur)
        d.R(x,y,x+w,y+h,(30,44,80) if not on else (60,120,255),4); d.R(x,y,x+w,y+h,None,4,(150,180,255,200) if on else (80,100,150,120),2.5)
        if on: d.R(x+4,y+4,x+w-4,y+h-4,(120,170,255,40),4)
    px,py=rooms[cur][0]+rooms[cur][2]/2,rooms[cur][1]+rooms[cur][3]/2
    d.E(px,py,10,10,(255,230,120)); d.E(px,py,22+4*math.sin(u*6),22+4*math.sin(u*6),(255,230,120,60))
    # memoria de la consola: barra que se desbordaria si se cargara todo
    ptext(d,30,596,'PLAYSTATION RAM: 2 MB',3.2,(255,255,255))
    d.R(30,640,510,690,(14,18,34),10); 
    used=clamp((cur+1)/9.0*.28+.04+.07*math.sin(u*3))
    d.R(36,646,36+468*used,684,(80,200,140),8)
    d.L(36+468*.35,634,36+468*.35,696,(255,255,255,160),2)
    # mansion completa que no cabe: barra roja imaginaria
    t=sm((u-3.0)/2.5); d.R(36,716,36+468*min(1.0,.9*t+.1),752,(240,70,70,int(255*t)),8) if t>0 else None
    if t>.8: 
        d.R(36,716,504,752,None,8,(255,255,255,int(160+90*math.sin(u*10))),3)
    return im
def sceneD(u):
    im=new((14,8,8),(34,18,16)); d=D(im)
    op=sm((u-1.0)/4.8)
    door_wood(d,270,860,236,700,op)
    d.R(70,886,470,922,(14,10,10),8); d.R(76,892,76+388*op,916,(236,200,110),6)
    for k in range(6): d.E(110+k*60,940,4,4,(236,200,110,int(255*clamp(math.sin(u*5+k)*.5+.5))))
    return ps1f(im,5)
def sceneE(u):
    im=new((14,8,8),(30,16,16)); d=D(im)
    mansion(d,u,speed=.0,door_open=sm((u-.6)/3.5),light=flicker(u,2,6),zomb=(0,1.0) if u>3.2 else None)
    silhouette(d,270,HY+400,1.9,(4,4,6))
    # indicador de salud estilo RE: caja con ECG y estado
    st=0 if u<3.2 else (1 if u<4.6 else 2); col=[(90,230,90),(236,210,60),(240,70,60)][st]; name=['FINE','CAUTION','DANGER'][st]
    d.R(300,820,520,930,(0,0,0,210),4); d.R(300,820,520,930,None,4,(255,255,255,200),2)
    ptext(d,314,832,name,4.2,col)
    pts=[]
    for x in range(0,540,6):
        t=(x/540.0*3+u*1.6)%1
        y=900-(60 if .45<t<.50 else -26 if .50<t<.54 else 12 if .54<t<.60 else 0)
        pts.append((x,y))
    for i in range(len(pts)-1):
        if pts[i][0]>306: d.L(pts[i][0],pts[i][1]+(-20),pts[i+1][0],pts[i+1][1]+(-20),col+(240,),3)
    return ps1f(im,5)
def sceneF(u):
    im=new((16,14,26),(44,36,58)); d=D(im)
    # mapa con dos zonas: Japon y Occidente + sello de marca registrada
    d.R(30,120,510,520,(30,40,80),14)
    for k in range(10): d.E(60+rnd(k)*420,150+rnd(k,1)*340,30+rnd(k,2)*40,20+rnd(k,3)*24,(70,110,90,200))
    d.E(430,260,38,48,(220,70,70,230)); d.E(120,280,80,70,(90,140,230,230))
    d.A(270,300,150,80,200,340,(255,255,255,200),4); d.P([(412,254),(424,276),(398,276)],(255,255,255))
    # simbolo de riesgo biologico (referencia al nombre japones) y sello ®
    def biohazard(cx,cy,r,col):
        d.E(cx,cy,r,r,None,col,5)
        for k in range(3):
            a=k*2.094+u*.3; d.E(cx+math.cos(a)*r*.62,cy+math.sin(a)*r*.62,r*.34,r*.34,None,col,4)
        d.E(cx,cy,r*.12,r*.12,col)
    biohazard(430,260,26,(40,10,12)); ptext(d,52,150,'BIOHAZARD',3.4,(255,255,255)); ptext(d,36,540,'RESIDENT EVIL',3.4,(255,255,255))
    d.R(60,580,480,760,(244,240,226),10); d.L(80,620,300,620,(0,0,0,90),4); d.L(80,660,340,660,(0,0,0,90),4); d.L(80,700,260,700,(0,0,0,90),4)
    s=sm((u-1.2)/.35); sz=70*(1+.5*(1-s))
    d.E(400,690,sz,sz,None,(200,40,50,int(255*s)),9); d.A(400,690,sz*.5,sz*.5,0,360,(200,40,50,int(255*s)),6) if s>0 else None
    d.L(400-sz*.6,690+sz*.6,400+sz*.6,690-sz*.6,(200,40,50,int(255*s)),7) if s>0 else None
    return im
def sceneG(u):
    im=new((20,10,10),(60,26,24)); d=D(im)
    for k in range(18):
        a=k*math.pi/9+u*.3; d.P([(270,430),(270+math.cos(a-.07)*800,430+math.sin(a-.07)*800),(270+math.cos(a+.07)*800,430+math.sin(a+.07)*800)],(255,214,140,16))
    b=sm(u/.8)
    double_door(d,270,700,120*b,420*b,.55+.1*math.sin(u*2),(255,214,140))
    ps1(d,270,880,1.1,u)
    for k in range(24): a=k*.27+u*.4; r=300+rnd(k,3)*40; d.E(270+math.cos(a)*r,430+math.sin(a)*r*.7,4,4,(255,230,140,200))
    return ps1f(im,6)
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx==0: return 1.0+.25*sm(p),270,500
    if idx==1: return 1.05+.2*sm(p),270,520
    if idx==2: return 1.0,270,480
    if idx==3: return 1.0+.25*sm(p),270,520
    if idx==4: return 1.0+.5*sm(p),270,560-40*sm(p)
    if idx==5: return 1.0+.1*sm(p),270,480
    if idx==6: return 1.3-.3*sm(p),270,470
    return 1.25-.25*sm(p),270,500
core.CAM=cam
if __name__=="__main__": core.main()
