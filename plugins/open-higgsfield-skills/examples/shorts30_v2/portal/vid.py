import sys; sys.path.insert(0,"..")
from art import *
from rig import *
from creatures import claw_arm
BLU=(60,170,255); ORG=(255,150,40)
SUBJ=dict(skin=(226,176,140),hair=(70,44,30),hairstyle="ponytail",shirt=(236,236,236),sleeve="none",pants=(240,120,30),shoes=(60,60,68),brow=(50,30,20),belt=(200,200,206))
ACTRESS=dict(skin=(236,196,160),hair=(120,70,40),hairstyle="long",shirt=(90,60,130),hat="headphones",sleeve="long",pants=(50,50,70))
SINGER=dict(skin=(226,186,150),hair=(80,60,40),hairstyle="short",glasses=True,shirt=(60,110,90),sleeve="long",pants=(60,60,70),beard=False)
def chamber(d,u,tint=(224,228,232)):
    d.R(0,0,540,960,tint,0)
    for r in range(12):
        for c in range(7): d.R(c*80+2,r*80+2,c*80+78,r*80+78,(236,240,244),2); d.R(c*80+2,r*80+2,c*80+78,r*80+6,(255,255,255,90),2)
    d.R(0,0,540,960,(0,0,0,26),0)
def ring(d,x,y,rx,ry,col,u=0.0):
    for k in range(4): d.E(x,y,rx*(1.2-k*.1),ry*(1.12-k*.08),col+(60+k*30,))
    d.E(x,y,rx,ry,col+(255,)); d.E(x,y,rx*.78,ry*.8,(10,14,24))
    for q in range(10): a=q*.63+u*2; d.E(x+math.cos(a)*rx*.9,y+math.sin(a)*ry*.9,3,3,(255,255,255,170))
def glados(d,x,y,sc,u,glow=1.0,arms=True):
    for sg in(-2,-1,0,1,2): d.L(x+sg*12*sc,0,x+sg*20*sc,y-50*sc,(40,40,46),4*sc)
    if arms:
        for k,sg in enumerate((-1,1)):
            claw_arm(d,x+sg*40*sc,y-30*sc,sg*(1.0+.25*math.sin(u*2+k)),sg*(.2+.4*math.sin(u*2.6+k*2)),sc*.8,l1=90,l2=80,open_=.5+.3*math.sin(u*3+k))
    d.E(x,y,52*sc,46*sc,(232,232,238)); d.E(x-14*sc,y-14*sc,28*sc,18*sc,(255,255,255,120)); d.E(x,y+24*sc,44*sc,14*sc,(190,190,198))
    d.R(x-22*sc,y+28*sc,x+22*sc,y+54*sc,(210,210,218),6*sc)
    d.E(x,y+2*sc,20*sc,20*sc,(20,20,24)); d.E(x,y+2*sc,13*sc,13*sc,(255,200,60,int(255*glow))); d.E(x,y+2*sc,30*sc,30*sc,(255,200,60,int(60*glow)))
    d.E(x,y+2*sc,4*sc,4*sc,(255,255,255,int(255*glow)))
def cake(d,x,y,sc,u,candle=True):
    shadow(d,x,y+4,90*sc,9*sc,80)
    d.R(x-70*sc,y-60*sc,x+70*sc,y,(120,70,50),6*sc); d.R(x-70*sc,y-90*sc,x+70*sc,y-58*sc,(250,244,236),8*sc)
    for k in range(7): d.E(x-60*sc+k*20*sc,y-58*sc,8*sc,10*sc,(250,244,236))
    d.R(x-70*sc,y-62*sc,x+70*sc,y-56*sc,(180,40,50),0); d.R(x-4*sc,y-120*sc,x+4*sc,y-90*sc,(230,230,240),1)
    if candle: d.E(x,y-130*sc,6*sc,10*sc+math.sin(u*9)*2*sc,(255,180,50)); d.E(x,y-130*sc,12*sc,16*sc,(255,200,80,50))
def cube(d,x,y,sc):
    d.R(x-34*sc,y-68*sc,x+34*sc,y,(150,150,158),6*sc); d.R(x-34*sc,y-68*sc,x+34*sc,y-58*sc,(210,210,218),6*sc)
    d.R(x-24*sc,y-58*sc,x+24*sc,y-10*sc,(110,110,118),4*sc)
    d.E(x-8*sc,y-42*sc,9*sc,9*sc,(255,120,170)); d.E(x+8*sc,y-42*sc,9*sc,9*sc,(255,120,170)); d.P([(x-17*sc,y-38*sc),(x+17*sc,y-38*sc),(x,y-20*sc)],(255,120,170))
def note(d,x,y,sc,col):
    d.E(x,y,9*sc,7*sc,col); d.R(x+7*sc,y-40*sc,x+10*sc,y,col,0); d.P([(x+10*sc,y-40*sc),(x+24*sc,y-28*sc),(x+10*sc,y-30*sc)],col)
def mic(d,x,y,sc):
    d.R(x-18*sc,y-56*sc,x+18*sc,y+18*sc,(70,74,82),18*sc)
    for k in range(5): d.L(x-16*sc,y-46*sc+k*13*sc,x+16*sc,y-46*sc+k*13*sc,(30,32,36),2*sc)
    d.A(x,y+8*sc,30*sc,30*sc,0,180,(130,134,142),4*sc); d.L(x,y+38*sc,x,y+170*sc,(130,134,142),5*sc); d.L(x-26*sc,y+170*sc,x+26*sc,y+170*sc,(130,134,142),5*sc)
def sceneA(u,final=False):
    im=new((8,8,12),(22,22,30)); d=D(im)
    glados(d,270,400,2.4,u,glow=.7+.3*math.sin(u*3))
    for k in range(5): t=(u*.45+k*.2)%1; note(d,80+k*90+math.sin(u+k)*10,860-t*420,1.3,(255,200,60,int(220*(1-t))))
    return im
def sceneB(u):
    im=new((200,206,212),(226,230,236)); d=D(im); chamber(d,u)
    ring(d,110,610,60,130,BLU,u); ring(d,440,470,60,130,ORG,u)
    t=clamp(u/3.4)
    if t<1: person(d,lerp(300,140,sm(t)),800,1.3*(1-.25*sm(clamp((t-.7)/.3))),u,P_walk(u,3.2),SUBJ,facing="front")
    else: person(d,lerp(400,300,sm(clamp((u-3.4)/1.6))),800 if u<4.6 else 800,1.3,u,P_walk(u,3.2) if u<5 else P_idle(u),SUBJ)
    d.R(120,860,420,950,(255,150,30),10); d.R(120,860,420,892,(40,40,48),10); ptext(d,136,866,"THE ORANGE BOX",3.0,(255,255,255)); ptext(d,136,904,"2007",5,(30,20,10))
    return im
def sceneC(u):
    im=new((190,194,200),(214,218,224)); d=D(im); chamber(d,u,tint=(204,206,212))
    d.R(50,200,490,420,(40,40,46),8)
    for k in range(60): d.L(60+rnd(k)*420,210+rnd(k,1)*200,70+rnd(k)*420,214+rnd(k,1)*200,(255,255,255,18),1)
    ptext(d,66,250,"LA TARTA ES",7,(255,60,60)); ptext(d,66,320,"MENTIRA",7,(255,60,60))
    person(d,150,930,1.5,u,P_point(u,dirx=1),SUBJ)
    d.R(220,800,500,830,(150,150,158),6); d.R(240,830,260,930,(120,120,128),0); d.R(460,830,480,930,(120,120,128),0)
    cake(d,380,800,1.3,u)
    return im
def sceneD(u):
    im=new((8,8,12),(26,26,34)); d=D(im)
    glados(d,380,260,1.6,u,glow=1.0)
    d.R(0,820,540,960,(24,24,30),0)
    o=person(d,170,900,1.6,u,dict(P_talk(u),ar=(.5,.4),mouth=.5+.5*math.sin(u*9)),ACTRESS)
    mic(d,300,640,1.1)
    ptext(d,40,190,"ELLEN MCLAIN",4.2,(255,255,255))
    return im
def sceneE(u):
    im=new((4,6,10),(10,16,26)); d=D(im)
    ptext(d,60,260,"STILL ALIVE",8,(120,230,150))
    for k in range(4): t=(u*.5+k*.25)%1; note(d,60+k*130,760-t*400,1.6,(255,200,60,int(220*(1-t))))
    for k in range(22):
        h=14+abs(math.sin(k*.7+u*6))*70; d.R(30+k*22,420-h*.8,30+k*22+14,420+h*.8,(120,230,150,170),2)
    # cantautor con guitarra: las manos sujetan el mastil y rasgan las cuerdas
    def hl(dd,x,y,a,s): dd.R(x-8,y-6,x+8,y+14,(150,100,60),3)
    o=person(d,270,950,1.6,u,dict(al=(1.15,2.5),ar=(.5+.2*math.sin(u*8),.6),ll=(.05,.05),lr=(.05,.05),bob=math.sin(u*2),tilt=.05,look=(0,0),mouth=.5+.5*math.sin(u*8),curlL=.7,curlR=.4,hands_front=True),SINGER,props={"l":hl})
    d.E(o["hip"][0]+10,o["hip"][1]-20,42,48,(190,120,60)); d.E(o["hip"][0]+10,o["hip"][1]-20,12,12,(30,20,14)); d.P([(o["hip"][0]-30,o["hip"][1]-60),(o["hip"][0]-170,o["hip"][1]-170),(o["hip"][0]-166,o["hip"][1]-180),(o["hip"][0]-22,o["hip"][1]-70)],(120,80,44))
    ptext(d,40,820,"JONATHAN COULTON",3.2,(255,255,255))
    return im
def sceneF(u):
    im=new((4,8,10),(10,22,26)); d=D(im)
    for r in range(18):
        y=((u*70)+r*52)%900+30; w=160+rnd(r)*260; d.R(40,y,40+w,y+14,(120,230,150,int(200*(1-abs(y-450)/500))),2)
    d.R(0,0,540,120,(4,8,10),0)
    ptext(d,40,190,"HUMOR NEGRO",5,(255,255,255))
    def cb(dd,x,y,a,s): pass
    o=person(d,300,950,1.6,u,dict(P_walk(u,3.0),al=(1.0,2.3),ar=(1.0,2.3),curlL=1.0,curlR=1.0,hands_front=True),SUBJ)
    cx=(o["hand_l"][0]+o["hand_r"][0])/2; cy=(o["hand_l"][1]+o["hand_r"][1])/2
    cube(d,cx,cy+34,.95)
    return im
def sceneG(u):
    im=new((200,206,212),(226,230,236)); d=D(im); chamber(d,u)
    ring(d,100,420,56,120,BLU,u); ring(d,450,640,56,120,ORG,u)
    person(d,270,930,1.5,u,P_cheer(u),SUBJ)
    cake(d,420,950,.7,u,candle=False)
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx in(0,7): return 1.0+.14*sm(p),270,440
    return 1.0+.1*sm(p),270+14*math.sin(u*.8),480
core.CAM=cam
if __name__=="__main__": core.main()
