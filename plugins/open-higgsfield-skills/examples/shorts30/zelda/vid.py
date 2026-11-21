import sys; sys.path.insert(0,"..")
from art import *
GOLD=(255,214,70); GRN=(40,150,60)
def tri(d,x,y,s,col=GOLD,a=255): d.P([(x,y-s),(x-s*.9,y+s*.7),(x+s*.9,y+s*.7)],col+(a,))
def triforce(d,x,y,s,u=0.0,glow=1.0):
    d.E(x,y,s*2.2,s*2.0,GOLD+(int(40*glow),)); d.E(x,y,s*1.5,s*1.4,GOLD+(int(50*glow),))
    tri(d,x,y-s*.55,s*.5); tri(d,x-s*.5,y+s*.35,s*.5); tri(d,x+s*.5,y+s*.35,s*.5)
def field(d,u):
    gradient(d,0,520,(120,200,250),(220,240,255)); d.R(0,520,540,960,(70,170,70),0)
    for k in range(40): x=rnd(k)*540; y=540+rnd(k,1)*420; d.L(x,y,x+3,y-9,(40,130,50,200),2)
    d.P([(0,520),(110,430),(230,520)],(90,140,120)); d.P([(200,520),(340,400),(540,520)],(70,120,110))
    d.E(420,130,34,34,(255,244,190,230))
def link(d,x,y,sc,u,sword=True):
    shadow(d,x,y+4,40*sc,6*sc,80)
    for sg in(-1,1): d.R(x+sg*12*sc-8*sc,y-44*sc,x+sg*12*sc+8*sc,y,(120,80,50),3*sc)
    d.R(x-22*sc,y-110*sc,x+22*sc,y-40*sc,GRN,8*sc); d.R(x-22*sc,y-64*sc,x+22*sc,y-58*sc,(130,80,40),0)
    d.E(x,y-136*sc,22*sc,22*sc,SK); d.E(x-8*sc,y-136*sc,3*sc,3*sc,(30,20,20)); d.E(x+8*sc,y-136*sc,3*sc,3*sc,(30,20,20))
    d.P([(x-26*sc,y-130*sc),(x,y-176*sc),(x+26*sc,y-130*sc),(x+34*sc,y-100*sc),(x+12*sc,y-122*sc),(x-18*sc,y-122*sc)],GRN)
    d.R(x-26*sc,y-150*sc,x+26*sc,y-142*sc,(255,214,120),2*sc)
    d.R(x+24*sc,y-90*sc,x+40*sc,y-60*sc,SK,5*sc); d.R(x-38*sc,y-96*sc,x-22*sc,y-50*sc,(30,60,160),6*sc)
    if sword: d.R(x+34*sc,y-160*sc,x+40*sc,y-86*sc,(220,226,236),2*sc); d.R(x+28*sc,y-96*sc,x+46*sc,y-90*sc,(130,80,40),1)
def princess(d,x,y,sc,u):
    shadow(d,x,y+4,50*sc,6*sc,80)
    d.P([(x-18*sc,y-100*sc),(x+18*sc,y-100*sc),(x+46*sc,y),(x-46*sc,y)],(240,140,190)); d.R(x-20*sc,y-110*sc,x+20*sc,y-60*sc,(250,170,210),8*sc)
    d.E(x,y-130*sc,20*sc,20*sc,SK); d.E(x,y-142*sc,22*sc,14*sc,(230,190,80)); d.P([(x-14*sc,y-152*sc),(x-8*sc,y-166*sc),(x,y-152*sc),(x+8*sc,y-166*sc),(x+14*sc,y-152*sc)],GOLD)
    for sg in(-1,1): d.E(x+sg*8*sc,y-130*sc,3*sc,3*sc,(30,20,20)); d.R(x+sg*20*sc-3*sc,y-130*sc,x+sg*20*sc+3*sc,y-90*sc,(230,190,80),2*sc)
def cart(d,x,y,sc,u):
    d.R(x-60*sc,y-80*sc,x+60*sc,y+80*sc,(220,180,50),8*sc); d.R(x-60*sc,y-80*sc,x+60*sc,y-70*sc,(255,255,255,60),8*sc)
    d.R(x-44*sc,y-52*sc,x+44*sc,y+34*sc,(30,40,30),6*sc); triforce(d,x,y-10*sc,22*sc,u,.6)
    d.R(x-48*sc,y+46*sc,x+48*sc,y+72*sc,(160,126,30),4*sc)
def sceneA(u,final=False):
    im=new((10,30,50),(30,60,70)); d=D(im); field(d,u)
    b=sm(u/1.0) if not final else 1.0
    triforce(d,270,400,70*(.8+.2*b),u,glow=.7+.3*math.sin(u*3))
    ptext(d,230,760,"?",14,(255,255,255))
    return im
def sceneB(u):
    im=new((30,30,44),(60,60,80)); d=D(im); d.R(0,780,540,960,(70,50,40),0)
    d.R(60,610,480,780,(70,70,76),10); d.R(60,610,480,630,(255,255,255,30),10); d.R(180,690,360,708,(20,20,24),4)
    cart(d,270,420+max(0,(1-sm(u/1.5)))*120,1.4,u)
    ptext(d,40,200,"1986",9,(255,255,255))
    return im
def sceneC(u):
    im=new((40,30,26),(80,60,48)); d=D(im); d.R(0,700,540,960,(110,76,50),0)
    # mesa de diseno con boceto de princesa y lista de nombres
    d.R(60,160,480,640,(240,236,220),8)
    princess(d,330,460,1.3,u)
    for i,n in enumerate(["NOMBRE 1","NOMBRE 2","NOMBRE 3"]):
        d.R(80,200+i*56,230,238+i*56,(255,255,255),4); ptext(d,90,212+i*56,n,2.6,(60,50,40));
        if i<2: d.L(80,219+i*56,230,219+i*56,(210,60,60),4)
    d.E(150,700,6,6,(0,0,0,0)); d.L(430,660,480,600,(240,200,60),10); d.P([(430,660),(424,676),(440,668)],(40,30,20))
    ptext(d,150,350,"?",10,(255,214,70))
    return im
def sceneD(u):
    im=new((24,20,30),(52,44,60)); d=D(im); d.R(0,760,540,960,(40,30,40),0)
    # libro y silueta de los anos 20 con cinta en la cabeza
    d.R(70,180,470,560,(60,40,80),10); d.R(70,180,100,560,(40,26,56),10); d.R(120,220,440,520,(236,220,180),6)
    ptext(d,140,260,"F. SCOTT",6,(60,40,30)); ptext(d,140,320,"FITZGERALD",5,(60,40,30)); d.L(140,400,420,400,(60,40,30,120),3)
    d.P([(220,700),(320,700),(340,960),(200,960)],(180,60,90)); d.E(270,640,40,46,(220,190,160)); d.R(232,610,308,622,(255,214,70),3); d.P([(270,602),(262,590),(278,590)],(255,214,70))
    d.R(250,690,290,710,(220,190,160),3); ptext(d,150,860,"ZELDA FITZGERALD",3.3,(255,255,255))
    return im
def sceneE(u):
    im=new((10,20,40),(30,50,80)); d=D(im); b=sm(u/1.0)
    for i,ch in enumerate("ZELDA"): ptext(d,50+i*92,360,ch,18,GOLD)
    for k in range(26): a=k*.5+u; d.E(270+math.cos(a)*(190+k*3),420+math.sin(a)*(160+k*4),3,3,(255,240,150,int(200*abs(math.sin(u*2+k)))))
    for k in range(6): d.A(270,600,60+k*38*(1-b*0)+0,40+k*20,0,360,(255,214,70,max(10,80-k*12)),2)
    ptext(d,60,800,"SUENA BIEN",7,(255,255,255))
    return im
def sceneF(u):
    im=new((60,140,200),(150,210,240)); d=D(im); field(d,u)
    link(d,160,800,2.2,u)
    princess(d,400,800,1.8,u)
    d.R(70,300,250,350,(0,0,0,150),8); ptext(d,84,313,"ESTE ES LINK",3.2,(255,255,255))
    d.R(310,300,490,350,(0,0,0,150),8); ptext(d,322,313,"ELLA ES ZELDA",2.8,(255,214,70))
    d.L(160,360,160,500,(255,255,255,160),4); d.L(400,360,400,520,(255,214,70,200),4)
    return im
def sceneG(u):
    im=new((60,140,200),(150,210,240)); d=D(im); field(d,u)
    triforce(d,270,300,52,u)
    link(d,270,830,1.8,u)
    for k in range(4):
        x=70+k*130; d.R(x-10,540,x+10,640,(60,50,50),0); ptext(d,x-12,580,"?",5,(255,255,255))
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx in(0,7,5): return 1.0,270,480
    return 1.0+.1*sm(p),270,480
core.CAM=cam
if __name__=="__main__": core.main()
