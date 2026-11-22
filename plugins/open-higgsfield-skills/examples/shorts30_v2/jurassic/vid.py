import sys; sys.path.insert(0,"..")
from art import *
from rig import *
from creatures import *
ENG=dict(skin=(230,188,150),hair=(90,70,50),hairstyle="short",beard=True,glasses=True,shirt=(120,150,170),pants=(60,64,80),hat="headphones",sleeve="short")
DIRX=dict(skin=(234,194,160),hair=(70,56,44),hairstyle="short",beard=True,glasses=True,shirt=(200,70,60),coat=(80,100,70),hat="cap",cap_col=(40,50,90),pants=(70,80,100),sleeve="long")
GOLDM=dict(skin=(250,200,50),hair=(250,200,50),hairstyle="bald",shirt=(250,200,50),pants=(250,200,50),shoes=(220,170,40),face=False,ear=False,sleeve="none",hands_col=(250,200,50),neck_col=(240,190,50))
def jungle(d,u,top=(6,14,10),bot=(20,40,26)):
    gradient(d,0,740,top,bot); d.R(0,740,540,960,(20,30,18),0)
    for k in range(8):
        x=k*80+20; d.R(x-8,300,x+8,760,(14,30,18),0)
        for q in range(4): d.E(x+math.sin(u+k+q)*8,300+q*30,60,24,(18,46,26,230))
def sound(d,x,y,u,n=5,col=(255,210,120),r0=50):
    for k in range(n): t=((u*.6+k/n)%1); d.A(x,y,r0+t*220,r0*.8+t*200,-50,50,col+(int(200*(1-t)),),5)
def faders(d,x,y,w,u):
    d.R(x,y,x+w,y+120,(40,42,50),10)
    for k in range(8):
        px=x+18+k*((w-36)/7); d.R(px-3,y+14,px+3,y+104,(14,14,18),2); fy=y+20+(math.sin(u*1.6+k*1.4)*.5+.5)*64; d.R(px-11,fy,px+11,fy+14,(200,200,210),3); d.E(px,y+8,4,4,(80,230,120) if k%2 else (240,200,60))
def sceneA(u,final=False):
    im=new((6,14,10),(20,40,26)); d=D(im); jungle(d,u)
    b=sm(u/.9) if not final else 1.0
    trex(d,lerp(230,170,sm(u/2.0)),880,1.4,u,jaw=b,facing=1)
    sound(d,470,560,u,n=5)
    return im
def sceneB(u):
    im=new((24,16,8),(120,70,20)); d=D(im); d.E(270,420,160,200,(230,140,30)); d.E(270,420,130,170,(250,180,60)); d.E(220,360,40,60,(255,255,255,40))
    d.E(270,430,16,8,(30,20,10)); d.L(270,430,244,414,(30,20,10),2); d.L(270,430,296,414,(30,20,10),2); d.L(270,430,252,452,(30,20,10),2); d.L(270,430,288,452,(30,20,10),2)
    ptext(d,40,200,"1993",9,(255,255,255));
    def mega(dd,x,y,a,s): dd.P([(x-12,y-8),(x+12,y-8),(x+34,y-30),(x+34,y+18)],(200,200,210)); dd.R(x-16,y-8,x-8,y+16,(60,60,70),2)
    person(d,150,980,1.6,u,dict(P_hold(u,r=(1.5,1.9),l=(.3,.4)),mouth=.5+.5*math.sin(u*8)),DIRX,props={"r":mega})
    ptext(d,40,820,"JURASSIC PARK",5,(255,214,120))
    return im
def sceneC(u):
    im=new((14,16,24),(30,34,48)); d=D(im); d.R(0,820,540,960,(40,34,34),0)
    person(d,270,1015,1.9,u,dict(al=(.5+.2*math.sin(u*1.6),.3),ar=(.5-.2*math.sin(u*1.6),.3),ll=(.05,.05),lr=(.05,.05),bob=math.sin(u*2),tilt=.07*math.sin(u*1.3),look=(0,.8),mouth=0,curlL=.5,curlR=.5,hands_front=True),ENG)
    d.R(30,895,510,960,(40,42,50),10); faders(d,50,885,440,u)
    ptext(d,60,300,"?",8,(255,255,255)); ptext(d,440,300,"?",8,(255,255,255))
    return im
def sceneD(u):
    im=new((14,22,16),(34,52,36)); d=D(im); d.R(0,700,540,960,(48,56,40),0)
    for k in range(10): d.E(rnd(k)*540,740+rnd(k,1)*200,26,5,(34,44,30))
    elephant(d,150+math.sin(u)*20,640,.8,u)
    tiger(d,400+math.sin(u*1.1)*20,640,.8,u,facing=-1)
    croc(d,270+math.sin(u*.8)*20,900,.9,u)
    ptext(d,236,500,"+",12,(255,255,255),200); ptext(d,236,700,"+",12,(255,255,255),200)
    return im
def sceneE(u):
    im=new((14,22,16),(34,52,36)); d=D(im); d.R(0,700,540,960,(48,56,40),0)
    raptor(d,150,720,1.3,u,facing=1)
    horse(d,380,720,.8,u,facing=-1)
    tortoise(d,270,900,1.5,u,facing=1)
    ptext(d,40,235,"SE CUENTA",5,(255,214,120))
    return im
def sceneF(u):
    im=new((6,10,8),(14,28,20)); d=D(im)
    for k in range(30):
        h=14+abs(math.sin(k*.6+u*6))*190*(1-abs(k-15)/18); d.R(30+k*16,420-h,30+k*16+10,420+h,(255,210,120,255),2)
    trex(d,95,900,.95,u,jaw=.7)
    person(d,420,960,1.4,u,dict(P_idle(u),al=(1.0,2.6),mouth=.3,look=(-.5,0)),ENG)
    return im
def sceneG(u):
    im=new((14,10,6),(40,28,14)); d=D(im); b=sm(u/1.0)
    d.E(270,470,150,150,(255,214,70,60))
    def oscar(dd,x,y,a,s):
        o=person(dd,x,y+80,.52,u,dict(al=(.05,.1),ar=(.05,.1),ll=(.05,.05),lr=(.05,.05),bob=0,tilt=0,look=(0,0),mouth=0),GOLDM)
    o=person(d,270,980,1.7,u,dict(P_hold(u,r=(2.2,2.9),grip=.9),mouth=.6),ENG,props={"r":oscar})
    for k in range(30): a=k*.5+u; d.E(270+math.cos(a)*(150+k*3),470+math.sin(a)*(160+k*3),2.5,2.5,(255,230,140,int(220*abs(math.sin(u*2+k)))))
    ptext(d,40,235,"OSCAR",9,(255,214,70))
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx in(0,7): return 1.0+.12*sm(p),270,560
    return 1.0+.1*sm(p),270+14*math.sin(u*.9),480
core.CAM=cam
if __name__=="__main__": core.main()
