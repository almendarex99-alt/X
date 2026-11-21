import sys; sys.path.insert(0,"..")
from art import *
from PIL import Image, ImageOps
# ---------- elementos del juego ----------
def bonnie(d,x,y,sc,u,glow=0.0):
    pu=(110,70,160); sh=(78,48,118)
    shadow(d,x,y+4,50*sc,7*sc,90)
    d.R(x-40*sc,y-160*sc,x+40*sc,y-40*sc,pu+(255,),26*sc); d.E(x,y-96*sc,26*sc,40*sc,(150,110,190))
    for sg in(-1,1): d.R(x+sg*44*sc-12*sc,y-150*sc,x+sg*44*sc+12*sc,y-84*sc,pu+(255,),9*sc); d.R(x+sg*20*sc-14*sc,y-46*sc,x+sg*20*sc+14*sc,y,sh+(255,),8*sc)
    hy=y-208*sc
    for sg in(-1,1): d.E(x+sg*22*sc,hy-52*sc,13*sc,46*sc,pu+(255,)); d.E(x+sg*22*sc,hy-52*sc,7*sc,36*sc,(180,120,210))
    d.E(x,hy,40*sc,40*sc,pu+(255,)); d.E(x,hy+14*sc,24*sc,17*sc,(150,110,190))
    for sg in(-1,1): d.E(x+sg*15*sc,hy-6*sc,9*sc,9*sc,(20,16,24)); d.E(x+sg*15*sc,hy-6*sc,4*sc,4*sc,(200,60,200)); 
    d.A(x,hy+14*sc,12*sc,7*sc,10,170,(30,16,36),3*sc)
    d.P([(x-18*sc,y-168*sc),(x,y-160*sc),(x-18*sc,y-150*sc)],(190,30,40)); d.P([(x+18*sc,y-168*sc),(x,y-160*sc),(x+18*sc,y-150*sc)],(190,30,40)); d.E(x,y-160*sc,5*sc,5*sc,(190,30,40))
    d.L(x+50*sc,y-90*sc,x+90*sc,y-150*sc,(120,60,36),6*sc); d.E(x+92*sc,y-156*sc,14*sc,10*sc,(214,40,60))   # guitarra
def chica(d,x,y,sc,u,glow=0.0):
    ye=(236,204,60); sh=(200,160,40)
    shadow(d,x,y+4,50*sc,7*sc,90)
    d.R(x-42*sc,y-160*sc,x+42*sc,y-40*sc,ye+(255,),26*sc); d.R(x-30*sc,y-150*sc,x+30*sc,y-90*sc,(244,244,248),12*sc)
    for sg in(-1,1): d.R(x+sg*46*sc-12*sc,y-150*sc,x+sg*46*sc+12*sc,y-84*sc,ye+(255,),9*sc); d.R(x+sg*20*sc-14*sc,y-46*sc,x+sg*20*sc+14*sc,y,(240,150,40),8*sc)
    hy=y-206*sc
    for k in range(3): d.E(x+(k-1)*14*sc,hy-44*sc,7*sc,14*sc,ye+(255,))
    d.E(x,hy,42*sc,40*sc,ye+(255,)); d.E(x,hy+10*sc,26*sc,12*sc,(240,150,40)); d.E(x,hy+20*sc,18*sc,9*sc,(240,110,30))
    for sg in(-1,1): d.E(x+sg*16*sc,hy-8*sc,10*sc,10*sc,(250,250,250)); d.E(x+sg*16*sc,hy-8*sc,4*sc,4*sc,(130,40,150))
def stage_view(d,x,y,w,h,u,k=0,bear_vis=True):
    gradient_local(d,x,y,w,h*.7,(60,22,72),(120,40,96))
    for i in range(7): d.R(x+i*w/7,y,x+(i+1)*w/7,y+h*.7,[(120,30,60,120),(150,40,70,120)][i%2])
    d.R(x,y+h*.7,x+w,y+h,(70,52,46)); d.R(x,y+h*.7,x+w,y+h*.7+4,(255,255,255,40))
    for i in range(6): d.E(x+10+i*w/5.4,y+8,3,3,(255,220,120,200))
    d.R(x+w*.08,y+h*.18,x+w*.92,y+h*.26,(236,226,120,200),3)
    if bear_vis:
        sc=h/560.0*1.65; by=y+h*.94
        bonnie(d,x+w*.2,by,sc,u); chica(d,x+w*.8,by,sc,u); bear(d,x+w/2,by+4,sc*1.12,u,eyes=(130,190,240),glow=.5)
def gradient_local(d,x,y,w,h,c0,c1,steps=10):
    for kk in range(steps): d.R(x,y+kk*h/steps,x+w,y+(kk+1)*h/steps+1,mixc(c0,c1,kk/(steps-1.0)),0)
def draw_beaver(d,x,y,sc,mood,u):
    """castor del juego familiar; mood 0 = tierno, 1 = inquietante (ojos pequenos y brillantes, sonrisa ancha)"""
    br=mixc((150,98,56),(70,44,30),mood); br2=mixc((196,140,90),(120,84,60),mood)
    shadow(d,x,y+4,60*sc,8*sc,80)
    d.E(x+52*sc,y-18*sc,46*sc,12*sc,mixc((96,60,40),(40,28,22),mood))
    d.E(x,y-60*sc,46*sc,58*sc,br); d.E(x,y-50*sc,28*sc,38*sc,br2)
    for sg in(-1,1): d.E(x+sg*40*sc,y-98*sc,14*sc,14*sc,br); d.E(x+sg*40*sc,y-98*sc,8*sc,8*sc,br2)
    d.E(x,y-116*sc,44*sc,40*sc,br)
    d.E(x,y-100*sc,26*sc,20*sc,br2)
    d.E(x,y-108*sc,8*sc,6*sc,(30,20,18))
    for sg in(-1,1):
        er=lerp(11,5,mood); d.E(x+sg*17*sc,y-128*sc,12*sc,12*sc,(250,250,250)); d.E(x+sg*17*sc,y-128*sc,er*sc,er*sc,(18,14,16))
        if mood<.5: d.E(x+sg*14*sc,y-131*sc,3*sc,3*sc,(255,255,255))
        else: d.E(x+sg*17*sc,y-128*sc,22*sc,22*sc,(255,255,255,int(70*mood)))
    w=lerp(9,24,mood)
    d.A(x,y-100*sc,w*sc,lerp(5,14,mood)*sc,10,170,(30,20,18),3*sc)
    d.R(x-6*sc,y-96*sc,x-1*sc,y-86*sc,(250,250,244),1*sc); d.R(x+1*sc,y-96*sc,x+6*sc,y-86*sc,(250,250,244),1*sc)
    d.E(x,y-146*sc,34*sc,12*sc,(236,190,40)); d.R(x-34*sc,y-146*sc,x+34*sc,y-138*sc,(236,190,40),3*sc)
def home_office(d,u,screen_fn,lamp=(255,200,120)):
    gradient(d,0,700,(24,20,42),(52,40,66))
    bevel(d,26,70,206,300,(56,46,56),8); d.R(36,80,196,290,(18,24,64)); d.E(160,120,14,14,(246,242,220)); stars(d,u,12,200) if False else None
    for k in range(7): d.R(36,80+k*30,196,85+k*30,(60,50,60,140),0)
    d.R(260,90,512,100,(110,76,54)); 
    for k,c in enumerate([(220,80,90),(90,150,230),(250,200,80),(120,200,140),(200,120,220)]): d.R(268+k*22,50,284+k*22,90,c,2)
    d.R(330,160,500,300,(244,240,226),3); d.E(414,224,34,34,(120,170,230)); d.L(340,280,490,280,(0,0,0,60),3)
    d.E(130,430,150,120,lamp+(26,))
    d.R(0,690,540,960,(40,30,40)); bevel(d,16,640,524,700,(116,78,56),6)
    box=crt(d,150,400,240,214,(2,10,14),(196,188,160)); screen_fn(d,*box); crt_fx(d,box)
    keyboard(d,190,664,160,30); mug(d,454,616,u,(255,240,220))
    person_back(d,270,742,1.45,0,u)
def hud(d,u,pw,hour):
    ptext(d,18,862,"POWER LEFT:",3.0,(255,255,255)); ptext(d,18,884,str(int(pw))+"%",5.0,(255,255,255))
    ptext(d,18,922,"USAGE:",3.0,(255,255,255))
    for k in range(4): d.R(104+k*14,922,114+k*14,936,[(90,220,90),(90,220,90),(230,220,60),(230,60,60)][k] if k<2+int(math.sin(u*.3)*.5+1) else (40,44,40),0)
    ptext(d,410,24,("12" if hour in(0,12) else str(hour))+" AM",5.0,(255,255,255)); ptext(d,420,70,"NIGHT 1",3.0,(255,255,255))
def office(d,u,power=.9,dl=0.0,dr=0.0,bearL=0.0,bearR=0.0,mon=None,pw=87,hour=12,zoom_mon=False):
    gradient(d,0,650,(14,18,22),(46,52,58))
    for k,(x,y,c) in enumerate([(176,96,(240,200,90)),(262,120,(120,200,240)),(344,92,(240,120,150))]):
        d.R(x,y,x+70,y+86,c+(230,),3); d.E(x+35,y+30,16,16,(255,255,255,200)); d.L(x+14,y+62,x+56,y+62,(0,0,0,70),3)
    for side,x0 in ((0,20),(1,400)):
        d.R(x0-8,226,x0+128,656,(24,20,30),4); d.R(x0,236,x0+120,656,(3,3,6),2)
        b=bearL if side==0 else bearR
        if b>0: bear(d,x0+60,656,.9,u,glow=1.0,tint=(104,70,46))
        f=dl if side==0 else dr
        if f>0:
            hh=(656-236)*f; d.R(x0,236,x0+120,236+hh,(66,70,82),2); 
            for k in range(int(hh/22)): d.R(x0,236+k*22,x0+120,238+k*22,(0,0,0,70),0)
            d.R(x0,236+hh-6,x0+120,236+hh,(255,200,60,140),0)
    d.R(0,650,540,960,(48,38,36)); d.R(0,650,540,656,(255,255,255,26))
    # panel de botones de las puertas
    for side,x0 in ((0,18),(1,430)):
        bevel(d,x0,700,x0+92,800,(50,52,60),6)
        f=dl if side==0 else dr
        d.E(x0+30,736,14,14,(220,60,60) if f>.5 else (90,30,30)); d.E(x0+62,736,14,14,(230,220,80) if f<.5 else (80,76,30)); d.R(x0+14,764,x0+78,780,(24,26,30),3)
    # monitor central
    bevel(d,150,690,390,860,(30,30,36),8); d.R(160,700,380,848,(4,8,8),4)
    if mon: mon(d,160,700,220,148)
    for k in range(30): d.R(160,700+k*5,380,701+k*5,(0,0,0,60))
    # ventilador
    d.E(466,760,36,36,(34,34,40)); d.E(466,760,5,5,(120,120,130)); 
    for k in range(3): a=u*14+k*2.094; d.P(rotpts([(466,760),(466+34,752),(466+34,768)],466,760,a),(150,154,162,200))
    d.R(458,792,474,830,(40,40,46),3)
    # lampara
    fl=flicker(u,2,6)
    d.E(110,640,120*fl,70*fl,(255,210,120,int(40*fl))); d.R(96,640,126,654,(60,54,60),3); d.L(110,654,86,742,(90,90,100),4); d.R(70,740,128,752,(60,60,70),4)
    hud(d,u,pw,hour)
def sceneA(u,final=False):
    im=new((10,8,20),(24,18,36)); d=D(im)
    office(d,u,mon=lambda d_,x,y,w,h:stage_view(d_,x,y,w,h,u),pw=99,hour=12,bearL=(1 if (u>1.2 and int(u*2)%2==0) else 0) if not final else 1)
    return im
def sceneB(u):
    im=new((24,20,42),(52,40,66)); d=D(im)
    def scr(d_,x0,y0,x1,y1):
        gradient(d_,y0,y0+120,(120,190,240),(200,230,250)) if False else None
        d_.R(x0,y0,x1,y1,(150,206,240)); d_.R(x0,y0+(y1-y0)*.66,x1,y1,(104,170,96))
        d_.R(x0+8,y0+(y1-y0)*.42,x0+80,y0+(y1-y0)*.7,(150,100,60),3); d_.P([(x0+4,y0+(y1-y0)*.43),(x0+44,y0+(y1-y0)*.28),(x0+84,y0+(y1-y0)*.43)],(190,60,60))
        for k in range(3): d_.R(x0+100+k*16,y0+(y1-y0)*.62,x0+112+k*16,y0+(y1-y0)*.7,(170,120,70),2)
        draw_beaver(d_,x0+(x1-x0)*.7+math.sin(u*2)*6,y0+(y1-y0)*.84,.52,0.0,u)
    home_office(d,u,scr)
    return im
def sceneC(u,dur=7.0):
    m=sm(u/5.0); bgc=mixc((120,190,240),(14,10,18),m)
    im=new(bgc,mixc((200,230,250),(30,20,36),m)); d=D(im)
    for k in range(14): d.E(rnd(k)*540,rnd(k,1)*500,3,3,(255,255,255,int(80*(1-m))))
    d.R(0,720,540,960,mixc((104,170,96),(18,24,18),m)+(255,),0)
    draw_beaver(d,270,800,3.5,m,u)
    # comentarios que aparecen alrededor
    for k,(x,y,w) in enumerate([(24,150,200),(318,200,200),(30,330,180),(330,400,190)]):
        a=sm((u-.8-k*.9)/.4)
        if a>0:
            d.R(x,y,x+w,y+74,(255,255,255,int(235*a)),16); d.P([(x+30,y+72),(x+56,y+72),(x+36,y+96)],(255,255,255,int(235*a)))
            for q in range(3): d.E(x+34+q*34,y+36,8,8,(60,60,70,int(255*a)))
            d.R(x+w-52,y+14,x+w-14,y+34,(220,60,70,int(255*a)),6)
    return im
def sceneD(u):
    im=new((24,20,42),(52,40,66)); d=D(im)
    def scr(d_,x0,y0,x1,y1):
        d_.R(x0,y0,x1,y1,(244,240,226)); d_.L(x0+8,y0+10,x1-8,y0+10,(0,0,0,70),2)
        bear(d_,(x0+x1)/2,y1-8,.42,u,eyes=(30,30,30),glow=0,tint=(150,120,100))
    home_office(d,u,scr)
    # bombilla de idea sobre el desarrollador
    gl=.7+.3*math.sin(u*6); d.E(270,330,64,64,(255,230,120,int(60*gl))); d.E(270,330,26,30,(255,236,140)); d.R(262,352,278,368,(150,150,160),3)
    for k in range(8): a=k*math.pi/4; d.L(270+math.cos(a)*40,330+math.sin(a)*44,270+math.cos(a)*58,330+math.sin(a)*62,(255,236,140,200),3)
    # calendario: cinco noches
    d.R(330,170,500,290,(244,240,230),6); d.R(330,170,500,196,(200,50,60),6)
    for k in range(5):
        x=342+k*30; d.E(x+10,244,10,10,(34,40,80) if u>.8+k*.5 else (210,210,220)); 
        if u>.8+k*.5: d.A(x+10,244,6,6,200,340,(255,230,120),2)
    return im
def sceneE(u):
    im=new((10,8,20),(24,18,36)); d=D(im)
    pw=max(60,int(99-u*5.2)); hour=12 if u<1.5 else int(1+ (u-1.5)//1.7)
    dr=sm((u-2.4)/.35); dl=sm((u-4.3)/.35)
    bR=1 if (1.5<u<2.6 or (u>5.4 and dr>0)) else 0
    bL=1 if (3.4<u<4.5) else 0
    office(d,u,pw=pw,hour=hour if hour>0 else 12,dl=dl,dr=dr,bearL=bL,bearR=bR,mon=lambda d_,x,y,w,h:stage_view(d_,x,y,w,h,u,bear_vis=(u%3>1)))
    return im
def sceneF(u):
    im=new((8,10,10),(16,20,22)); d=D(im)
    cut=int(u/1.6); ph=(u%1.6)
    sc=[.9,1.25,1.75,2.4][min(3,cut)]
    corridor(d,u,speed=0.0,wall=(120,124,120),floor=(150,150,150),ceil=(90,92,90),door=(80,70,80),light=(255,255,240),pulse=flicker(u,3,8),alt=cut*.15)
    # suelo de tablero blanco y negro
    near,far=depth(0),depth(10)
    for kk in range(10):
        s1,s2=depth(kk),depth(kk+1); xa,xb,ya,yb=planes(s1); xc,xd,yc,yd=planes(s2)
        for j in range(6):
            if (kk+j)%2==0:
                fa=j/6.0; fb=(j+1)/6.0
                d.P([(xa+(xb-xa)*fa,yb),(xa+(xb-xa)*fb,yb),(xc+(xd-xc)*fb,yd),(xc+(xd-xc)*fa,yd)],(20,20,22,230))
    bear(d,270,HY+130+sc*92,sc,u,eyes=(255,255,255),glow=1.0)
    im2=ImageOps.grayscale(im).convert("RGB"); im2=Image.blend(im2,Image.new("RGB",im2.size,(70,120,100)),.18)
    d=D(im2)
    for k in range(int(960/5)): d.R(0,k*5,540,k*5+1,(0,0,0,70))
    noise_static(d,0,0,540,960,u*.5,34,12)
    if ph<.16: noise_static(d,0,0,540,960,u,int(255*(1-ph/.16)),9)
    # interfaz de camaras: etiqueta y mapa con botones
    ptext(d,18,26,"CAM 2A",4.0,(255,255,255)); ptext(d,18,56,"WEST HALL",3.0,(255,255,255))
    if int(u*2)%2==0: d.E(500,40,9,9,(240,40,40))
    d.R(330,700,516,926,(20,24,20,210),4); d.R(330,700,516,926,None,4,(255,255,255,200),2)
    for (rx,ry,rw,rh) in[(344,712,60,40),(420,712,86,60),(344,770,40,100),(398,800,40,70),(446,790,60,70)]: d.R(rx,ry,rx+rw,ry+rh,(120,130,120,150),2)
    for i,(bx,by_) in enumerate([(350,716),(430,716),(350,790),(404,820),(452,806)]):
        on=(i==min(3,cut)); d.R(bx,by_,bx+26,by_+14,(80,230,80) if on else (60,80,60),2)
    ptext(d,340,900,"YOU",3.0,(255,255,255))
    return im2
def sceneG(u):
    im=new((14,10,24),(30,18,44)); d=D(im); stars(d,u,40,300)
    # rejilla de miniaturas de videos con reacciones
    for r in range(5):
        for c in range(3):
            x=24+c*170; y=120+r*150-(u*18)%150; k=r*3+c
            d.R(x,y,x+154,y+116,(26,22,40),8); d.R(x,y,x+154,y+6,(255,255,255,24),8)
            d.R(x+6,y+6,x+148,y+110,(8,10,14),5)
            bear(d,x+104,y+112,.28,u,eyes=(255,255,255),glow=.5)
            fx=x+42; fy=y+72; d.E(fx,fy,24,26,(236,196,160)); d.E(fx-8,fy-6,6,7,(255,255,255)); d.E(fx+8,fy-6,6,7,(255,255,255)); d.E(fx-8,fy-6,2.4,2.4,(20,20,20)); d.E(fx+8,fy-6,2.4,2.4,(20,20,20))
            d.E(fx,fy+12,8,11+3*math.sin(u*9+k),(90,20,30)); d.E(fx-22,fy-26,10,10,(60,40,30))
            d.P([(x+66,y+44),(x+66,y+68),(x+84,y+56)],(255,255,255,90))
    # contador de reproducciones
    n=int(1000*(1.0+u*3.2)**6)
    d.R(40,28,500,92,(0,0,0,160),10)
    for i,ch in enumerate(str(n).zfill(8)[-8:]): seg7(d,56+i*52,40,40,40,int(ch),(255,80,80))
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx==0: return 1.0+.7*sm(p),270,520+60*sm(p)
    if idx==1: return 1.0+.5*sm(p),270,520-30*sm(p)
    if idx==2: return 1.1-.05*sm(p),270,500
    if idx==3: return 1.0+.4*sm(p),300,420
    if idx==4: return 1.0+.12*sm(p),270,560
    if idx==5: return 1.0+.1*sm(p),270,470
    if idx==6: return 1.3-.3*sm(p),270,420
    return 1.7-.7*sm(p),270,590-80*sm(p)
core.CAM=cam
if __name__=="__main__": core.main()
