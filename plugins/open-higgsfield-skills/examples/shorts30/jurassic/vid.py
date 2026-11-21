import sys; sys.path.insert(0,"..")
from art import *
def trex(d,x,y,sc,u,open_=1.0,col=(70,96,60)):
    dark=tuple(int(c*.6) for c in col)
    d.E(x,y+60*sc,90*sc,50*sc,col+(255,)); d.P([(x-90*sc,y+40*sc),(x-60*sc,y-60*sc),(x+20*sc,y-100*sc),(x+110*sc,y-50*sc),(x+130*sc,y+20*sc),(x+30*sc,y+60*sc)],col+(255,))
    # mandibula abierta
    jy=y+20*sc+open_*50*sc
    d.P([(x+10*sc,y+30*sc),(x+160*sc,y+20*sc),(x+150*sc,jy+10*sc),(x+30*sc,jy+40*sc)],(160,40,50))
    d.P([(x+10*sc,y+30*sc),(x+170*sc,y+16*sc),(x+160*sc,y+30*sc),(x+30*sc,y+50*sc)],col)
    d.P([(x+20*sc,jy+30*sc),(x+150*sc,jy+6*sc),(x+160*sc,jy+30*sc),(x+30*sc,jy+60*sc)],dark)
    for k in range(7): d.P([(x+34*sc+k*17*sc,y+32*sc),(x+42*sc+k*17*sc,y+32*sc),(x+38*sc+k*17*sc,y+50*sc)],(244,240,224))
    for k in range(6): d.P([(x+44*sc+k*17*sc,jy+10*sc),(x+52*sc+k*17*sc,jy+10*sc),(x+48*sc+k*17*sc,jy-6*sc)],(244,240,224))
    d.E(x+30*sc,y-34*sc,11*sc,9*sc,(255,210,60)); d.E(x+32*sc,y-34*sc,4*sc,7*sc,(10,10,10))
    d.E(x+120*sc,y+2*sc,5*sc,4*sc,(20,30,20))
    for k in range(3): d.A(x-10*sc,y+0*sc,30*sc+k*18*sc,22*sc+k*14*sc,200,340,(0,0,0,50),3*sc)
def sound(d,x,y,u,n=5,col=(255,210,120),r0=50):
    for k in range(n): t=((u*.6+k/n)%1); d.A(x,y,r0+t*220,r0*.8+t*200,-50,50,col+(int(200*(1-t)),),5)
def elephant(d,x,y,sc,u):
    shadow(d,x,y+4,70*sc,8*sc,80); col=(150,154,164)
    d.E(x,y-60*sc,62*sc,44*sc,col+(255,));
    for sg in(-1,1): d.R(x+sg*34*sc-10*sc,y-40*sc,x+sg*34*sc+10*sc,y,col+(255,),4*sc)
    d.E(x+60*sc,y-92*sc,32*sc,30*sc,col+(255,)); d.E(x+38*sc,y-88*sc,18*sc,26*sc,(130,134,144)); d.R(x+78*sc,y-84*sc,x+92*sc,y-30*sc,col+(255,),6*sc); d.E(x+72*sc,y-98*sc,3*sc,3*sc,(10,10,10))
def tiger(d,x,y,sc,u):
    shadow(d,x,y+4,70*sc,8*sc,80); col=(236,140,40)
    d.E(x,y-52*sc,64*sc,32*sc,col+(255,));
    for sg in(-1,1): d.R(x+sg*36*sc-7*sc,y-38*sc,x+sg*36*sc+7*sc,y,col+(255,),3*sc)
    d.E(x+66*sc,y-72*sc,24*sc,22*sc,col+(255,)); d.E(x+66*sc,y-62*sc,12*sc,8*sc,(250,240,220)); d.E(x+72*sc,y-78*sc,3*sc,3*sc,(10,10,10))
    d.L(x-62*sc,y-60*sc,x-96*sc,y-30*sc,col+(255,),6*sc)
    for k in range(6): d.L(x-40*sc+k*16*sc,y-82*sc,x-34*sc+k*16*sc,y-48*sc,(30,20,10),3*sc)
def croc(d,x,y,sc,u):
    shadow(d,x,y+4,80*sc,6*sc,80); col=(70,120,60)
    d.R(x-80*sc,y-30*sc,x+80*sc,y-4*sc,col+(255,),12*sc); d.P([(x+60*sc,y-26*sc),(x+130*sc,y-18*sc),(x+130*sc,y-6*sc),(x+60*sc,y-4*sc)],col)
    d.P([(x-80*sc,y-24*sc),(x-130*sc,y-6*sc),(x-80*sc,y-8*sc)],col)
    for k in range(8): d.P([(x+66*sc+k*8*sc,y-8*sc),(x+70*sc+k*8*sc,y-8*sc),(x+68*sc+k*8*sc,y-16*sc)],(244,240,224))
    d.E(x+70*sc,y-34*sc,5*sc,5*sc,(255,210,60))
    for sg in(-1,1): d.R(x+sg*40*sc-5*sc,y-6*sc,x+sg*40*sc+5*sc,y+8*sc,col+(255,),2*sc)
def faders(d,x,y,w,u):
    d.R(x,y,x+w,y+170,(40,42,50),10)
    for k in range(8):
        px=x+18+k*((w-36)/7); d.R(px-3,y+20,px+3,y+150,(14,14,18),2); fy=y+30+(math.sin(u*1.6+k*1.4)*.5+.5)*100; d.R(px-11,fy,px+11,fy+16,(200,200,210),3); d.E(px,y+10,4,4,(80,230,120) if k%2 else (240,200,60))
def sceneA(u,final=False):
    im=new((6,14,10),(20,40,26)); d=D(im); d.R(0,740,540,960,(20,30,18),0)
    b=sm(u/.9) if not final else 1.0
    trex(d,140,520,1.9,u,open_=b)
    sound(d,350,540,u,n=5)
    return im
def sceneB(u):
    im=new((24,16,8),(120,70,20)); d=D(im); d.E(270,420,160,200,(230,140,30)); d.E(270,420,130,170,(250,180,60)); d.E(220,360,40,60,(255,255,255,40))
    d.E(270,430,16,8,(30,20,10)); d.L(270,430,244,414,(30,20,10),2); d.L(270,430,296,414,(30,20,10),2); d.L(270,430,252,452,(30,20,10),2); d.L(270,430,288,452,(30,20,10),2)
    ptext(d,40,200,"1993",9,(255,255,255)); ptext(d,40,690,"JURASSIC PARK",5,(255,214,120))
    return im
def sceneC(u):
    im=new((14,16,24),(30,34,48)); d=D(im); d.R(0,700,540,960,(40,34,34),0)
    faders(d,60,400,420,u)
    d.R(210,190,330,330,(60,62,70),20); d.A(270,260,86,86,200,340,(120,124,134),10)
    d.R(40,640,500,700,(30,32,38),8)
    d.E(270,820,10,10,(240,60,60));
    ptext(d,60,780,"?",8,(255,255,255)); ptext(d,420,780,"?",8,(255,255,255))
    return im
def sceneD(u):
    im=new((14,22,16),(34,52,36)); d=D(im); d.R(0,700,540,960,(48,56,40),0)
    a=sm((u-.6)/.8); b=sm((u-1.8)/.8); c=sm((u-3.0)/.8)
    if a>.05: elephant(d,130,520,1.2*a,u)
    if b>.05: tiger(d,360,520,1.2*b,u)
    if c>.05: croc(d,270,800,1.3*c,u)
    ptext(d,215,470,"+",12,(255,255,255),200); ptext(d,215,700,"+",12,(255,255,255),200)
    return im
def sceneE(u):
    im=new((14,22,16),(34,52,36)); d=D(im); d.R(0,700,540,960,(48,56,40),0)
    # raptor silueta + tortuga + caballo
    d.E(130,540,60,70,(80,100,60)); d.R(100,540,160,620,(80,100,60),10); d.R(120,620,140,720,(80,100,60),4)
    d.E(180,470,26,18,(80,100,60)); d.E(190,466,4,4,(255,210,60))
    d.P([(60,560),(10,580),(60,590)],(80,100,60))
    d.E(360,700,60,34,(110,120,70)); d.E(360,690,50,24,(140,150,90)); d.E(420,700,14,10,(110,120,70))
    d.E(370,500,60,44,(130,86,56)); d.R(420,430,450,520,(130,86,56),8); d.E(440,430,24,18,(130,86,56));
    ptext(d,40,235,"SE CUENTA",5,(255,214,120))
    return im
def sceneF(u):
    im=new((6,10,8),(14,28,20)); d=D(im);
    for k in range(30):
        h=14+abs(math.sin(k*.6+u*6))*190*(1-abs(k-15)/18); d.R(30+k*16,480-h,30+k*16+10,480+h,(255,210,120,255),2)
    trex(d,160,780,1.0,u,open_=1.0)
    return im
def sceneG(u):
    im=new((14,10,6),(40,28,14)); d=D(im); b=sm(u/1.0)
    d.E(270,470,130,130,(255,214,70,60)); d.R(250,400,290,640,(250,200,50),12); d.E(270,360,40,44,(250,200,50)); d.R(220,640,320,720,(40,32,20),6); d.R(190,720,350,780,(30,24,14),6)
    d.E(270,360,16,16,(255,255,255,60))
    for k in range(30): a=k*.5+u; d.E(270+math.cos(a)*(150+k*3),470+math.sin(a)*(160+k*3),2.5,2.5,(255,230,140,int(220*abs(math.sin(u*2+k)))))
    ptext(d,40,235,"OSCAR",9,(255,214,70))
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx in(0,7,3,4): return 1.0,270,480
    return 1.0+.1*sm(p),270,480
core.CAM=cam
if __name__=="__main__": core.main()
