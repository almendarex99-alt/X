import sys; sys.path.insert(0,"..")
from art import *
GRN=(110,255,150)
def ghost(d,x,y,sc,u,a=150,eyes=True):
    w=math.sin(u*2)*8*sc
    d.E(x,y-110*sc,40*sc,48*sc,(230,240,255,a)); d.R(x-40*sc,y-110*sc,x+40*sc,y-10*sc,(230,240,255,a),0)
    for k in range(5): d.E(x-32*sc+k*16*sc,y-8*sc+math.sin(u*3+k)*5*sc,10*sc,16*sc,(230,240,255,a))
    d.R(x-58*sc+w,y-90*sc,x-38*sc+w,y-40*sc,(230,240,255,int(a*.8)),8*sc); d.R(x+38*sc-w,y-90*sc,x+58*sc-w,y-40*sc,(230,240,255,int(a*.8)),8*sc)
    d.E(x,y-100*sc,70*sc,80*sc,(200,220,255,int(a*.25)))
    if eyes:
        for sg in(-1,1): d.E(x+sg*14*sc,y-118*sc,6*sc,9*sc,(10,12,20,255))
        d.E(x,y-92*sc,7*sc,10*sc,(10,12,20,255))
def house_room(d,u):
    gradient(d,0,560,(6,8,16),(16,20,34)); d.R(0,560,540,960,(30,24,26),0)
    for k in range(7): d.L(0,590+k*50,540,590+k*50,(0,0,0,60),2)
    d.R(0,540,540,560,(10,8,10),0)
    d.R(40,150,200,410,(10,12,22),6); d.R(40,150,200,410,None,6,(70,60,50),8); d.L(120,150,120,410,(70,60,50),6)
    d.E(120,230,50,70,(200,220,255,int(20+10*math.sin(u))))
    d.R(330,360,490,640,(24,18,20),6); d.R(330,360,490,640,None,6,(70,60,50),6)
def flash(d,x,y,tx,ty,u): flashlight(d,x,y,tx,ty,spread=.3,L=700,a=70)
def emf(d,x,y,sc,lvl):
    d.R(x-36*sc,y-90*sc,x+36*sc,y+90*sc,(40,44,50),10*sc)
    for k in range(5): d.R(x-20*sc,y+60*sc-k*28*sc,x+20*sc,y+78*sc-k*28*sc,((60,230,90) if k<2 else (240,220,60) if k<4 else (240,60,50)) if k<lvl else (30,32,36),3*sc)
def mic(d,x,y,sc):
    d.R(x-20*sc,y-60*sc,x+20*sc,y+20*sc,(70,74,82),20*sc)
    for k in range(5): d.L(x-18*sc,y-50*sc+k*14*sc,x+18*sc,y-50*sc+k*14*sc,(30,32,36),2*sc)
    d.A(x,y+10*sc,34*sc,34*sc,0,180,(130,134,142),4*sc); d.L(x,y+44*sc,x,y+90*sc,(130,134,142),5*sc); d.L(x-24*sc,y+90*sc,x+24*sc,y+90*sc,(130,134,142),5*sc)
def waves(d,x,y,u,col=GRN,n=4,r0=40):
    for k in range(n): t=((u*.6+k/n)%1); d.A(x,y,r0+t*190,r0*.9+t*170,-60,60,col+(int(200*(1-t)),),4); d.A(x,y,r0+t*190,r0*.9+t*170,120,240,col+(int(200*(1-t)),),4)
def sceneA(u,final=False):
    im=new((6,8,16),(16,20,34)); d=D(im); house_room(d,u)
    b=sm(u/1.0) if not final else 1.0
    ghost(d,270,740,1.7,u,a=int(110*b+40))
    mic(d,110,860,.8); waves(d,110,820,u)
    return im
def sceneB(u):
    im=new((4,6,14),(12,16,30)); d=D(im); stars(d,u,40,380); d.E(420,120,30,30,(235,235,245,220))
    d.R(110,380,430,700,(16,14,20),0); d.P([(90,380),(270,260),(450,380)],(12,10,16))
    for (x,y) in ((150,450),(330,450),(150,580),(330,580)): d.R(x,y,x+60,y+70,(255,210,120,int(180*flicker(u,x,4))) if (x+y)%3 else (20,20,28),2)
    d.R(230,600,310,700,(30,22,22),2); d.R(0,700,540,960,(14,18,16),0)
    ptext(d,40,200,"2020",9,(255,255,255))
    return im
def sceneC(u):
    im=new((10,12,20),(22,24,36)); d=D(im); d.R(0,640,540,960,(50,38,30),0); d.R(0,640,540,650,(255,255,255,20),0)
    emf(d,110,520,1.1,int(1+u*1.2)%6);
    d.R(220,380,280,640,(220,220,226),14); d.R(236,400,264,580,(30,40,56),6); d.E(250,610,22,22,(220,60,60)); d.R(242,540,258,600,(80,150,255),4)
    d.R(330,500,490,620,(34,34,40),10); d.E(410,560,40,40,(16,16,22)); d.E(410,560,26,26,(80,110,160)); d.E(400,550,7,7,(255,255,255,200))
    for k,t in enumerate(["EMF","TEMP","CAMARA"]): ptext(d,60+k*160,700,t,3.6,(255,255,255))
    return im
def sceneD(u):
    im=new((6,8,16),(14,18,30)); d=D(im); mic(d,270,500,2.6); waves(d,270,460,u,n=5,r0=90)
    for k in range(22):
        h=10+abs(math.sin(k*.8+u*7))*70*sm(u/1.0); d.R(40+k*22,860-h,40+k*22+12,860+h,GRN+(180,),2)
    ptext(d,40,190,"VOZ",12,(255,255,255))
    return im
def sceneE(u):
    im=new((6,8,16),(16,20,34)); d=D(im); house_room(d,u)
    ghost(d,370,740,1.6,u,a=120); silhouette(d,130,820,1.5,(30,34,48))
    t=sm((u-.6)/.8); d.R(40,300,290,380,(255,255,255,int(230*t)),10); ptext(d,54,320,"ESTAS AQUI?",3.4,(20,20,30,int(255*t)) if False else (20,20,30))
    t2=sm((u-2.8)/.8); d.R(260,420,500,500,(180,200,255,int(230*t2)),10); ptext(d,276,442,"...",8,(10,10,20))
    return im
def sceneF(u):
    im=new((6,8,16),(14,18,30)); d=D(im); house_room(d,u)
    near=clamp(u/6.0); ghost(d,lerp(420,300,near),760,lerp(1.2,2.2,near),u,a=int(120+80*near))
    # barra de cordura bajando
    d.R(40,120,500,150,(255,255,255,40),8); d.R(40,120,40+460*(1-.7*near),150,GRN+(230,),8); ptext(d,40,160,"CORDURA",3.4,(255,255,255))
    return im
def sceneG(u):
    im=new((6,8,16),(14,18,30)); d=D(im); house_room(d,u)
    mic(d,150,780,1.2); waves(d,150,720,u,n=4,r0=60)
    ghost(d,380,760,1.5,u,a=150)
    d.A(380,520,60,70,-40,40,(230,240,255,160),4); d.A(380,520,90,100,-40,40,(230,240,255,100),4)
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx in(0,7,3): return 1.0,270,480
    return 1.0+.1*sm(p),270,500
core.CAM=cam
if __name__=="__main__": core.main()
