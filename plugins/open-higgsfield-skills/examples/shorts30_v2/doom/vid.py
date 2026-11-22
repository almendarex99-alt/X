import sys; sys.path.insert(0,"..")
from art import *
from rig import *
from common import ps1f
CLAY=(150,98,70)
IMP=dict(skin=CLAY,hairstyle="bald",horns=True,claws=True,tail=CLAY,shirt=shade(CLAY,1.08),pants=shade(CLAY,.7),shoes=(60,36,26),bulk=1.55,sleeve="none",eyes=(255,210,60),ear=False,brow=(30,10,10),mouth_col=(60,10,10),height=1.05)
ARTIST=dict(skin=(226,184,150),hair=(54,36,26),hairstyle="short",beard=True,glasses=True,shirt=(190,190,196),coat=(120,84,60),sleeve="long",pants=(56,60,76))
def imp_deco(d,hx,hy,sc):
    for sg in(-1,1): d.E(hx+sg*8.5*sc,hy-3*sc,13*sc,11*sc,(255,210,60,60))
def imp(d,x,y,sc,u,pose=None,ph=0.0,**kw):
    st=dict(IMP); st.update(kw.pop("style",{}))
    return person(d,x,y,sc,u,pose or P_walk(u,2.6,ph),st,deco=imp_deco,**kw)
def lump(d,x,y,sc):
    d.E(x,y,90*sc,40*sc,(120,78,54)); d.E(x-20*sc,y-12*sc,50*sc,18*sc,(160,108,78,160))
def hell_bg(d,u):
    gradient(d,0,520,(24,4,6),(120,22,12)); d.R(0,520,540,960,(36,14,12),0)
    for k in range(10): x=rnd(k)*540; d.E(x,520+rnd(k,1)*20,60+rnd(k,2)*60,10,(255,100,30,40))
    for k in range(5): d.L(0,540+k*70,540,540+k*70,(255,90,30,40),2)
    for k in range(34): d.E((rnd(k,5)*540+u*20)%540,(rnd(k,6)*900-u*50)%900,2,2,(255,150,60,160))
def pistol(d,x,y,a,s):
    d.R(x-7,y-12,x+7,y+40,(70,70,78),3); d.R(x-5,y-48,x+5,y-8,(110,110,120),2); d.R(x-3,y-60,x+3,y-46,(60,60,66),1)
def sceneA(u,final=False):
    im=new((24,4,6),(120,22,12)); d=D(im); hell_bg(d,u)
    z=sm(u/2.4) if not final else 1.0
    imp(d,270,900,1.0+.55*z,u,pose=dict(P_walk(u,2.4),mouth=1.0,al=(.8,1.9),ar=(.8,1.9),curlL=.6,curlR=.6,spreadL=1.0,spreadR=1.0))
    return im
def sceneB(u):
    im=new((30,24,20),(60,50,44)); d=D(im)
    corridor(d,u,speed=.35,wall=(90,80,70),floor=(60,46,36),ceil=(40,40,44),door=(100,70,40),light=(255,224,160),n=9,doors=True)
    imp(d,270,450,.34+.1*math.sin(u*.5),u,pose=P_walk(u,3.4))
    d.R(0,800,540,960,(110,96,86),0); d.R(0,800,540,808,(60,50,44),0)
    d.R(40,820,500,950,(80,70,64),6); d.E(270,885,34,38,(222,176,140)); d.E(257,877,4,4,(40,20,10)); d.E(283,877,4,4,(40,20,10)); d.R(262,896,278,900,(120,40,40),1)
    d.R(70,834,200,872,(20,10,10),4); ptext(d,82,842,"100",5,(240,60,40)); d.R(340,834,470,872,(20,10,10),4); ptext(d,352,842,"050",5,(240,200,60))
    rc=max(0,math.sin(u*5))*14
    # brazo en primera persona: antebrazo desde abajo, mano con 5 dedos sujetando la pistola
    d.L(400,990,340,780-rc*.5,(70,90,60,255),44); d.L(400,990,350,800,(70,90,60,255),40)
    hand(d,340,770-rc,.35,1,2.1,(226,176,140),curl=.95,spread=.3,prop=lambda dd,x,y,a,s: pistol(dd,x,y-10,a,s))
    if rc>9: d.E(330,690,40,30,(255,240,160,200))
    ptext(d,40,200,"1993",8,(255,255,255))
    return im
def sceneC(u):
    im=new((40,30,26),(70,56,48)); d=D(im)
    for k in range(5): d.R(k*108,0,k*108+4,700,(0,0,0,30),0)
    d.R(40,150,200,330,(60,50,44),4)
    for k in range(3): d.R(54,166+k*50,186,200+k*50,(120,90,70),2)
    p=sm(u/5.5); t=u*3
    person(d,270,1010,1.9,u,dict(al=(.42+.12*math.sin(t),.22),ar=(.42-.12*math.sin(t),.22),ll=(.05,.05),lr=(.05,.05),bob=math.sin(u*2)*1,tilt=.06*math.sin(u*1.4),look=(0,.8),mouth=0,curlL=.55,curlR=.55,hands_front=True),ARTIST)
    d.R(0,830,540,960,(90,60,40),0); d.R(0,830,540,838,(255,255,255,30),0)
    lump(d,270,832,.9)
    imp(d,270,830,.15+.4*p,u,pose=P_idle(u),style=dict(shirt=(130,86,60),pants=(110,76,54),skin=(140,92,66)))
    ptext(d,40,190,"A MANO",8,(255,220,140))
    return im
def sceneD(u):
    im=new((20,18,22),(46,40,44)); d=D(im); d.R(0,700,540,960,(70,56,46),0)
    ang=u*1.4
    d.E(380,780,100,16,(110,96,86)); imp(d,380,775,.9,u,pose=dict(P_idle(u),mouth=.4))
    def cam_l(dd,x,y,a,s): dd.R(x-18,y-14,x+18,y+22,(34,34,40),6); dd.E(x,y+4,10,10,(80,110,160))
    def cam_r(dd,x,y,a,s): dd.R(x-14,y-10,x+14,y+18,(34,34,40),6)
    fl=math.sin(u*5)>.7
    o=person(d,150,900,1.7,u,dict(al=(1.6,2.3),ar=(1.6,2.3),ll=(.05,.05),lr=(.05,.05),bob=math.sin(u*2),tilt=0,look=(.8,0),mouth=0,curlL=.8,curlR=.8,hands_front=True),dict(ARTIST,coat=None,shirt=(70,90,130)),props={"l":cam_l,"r":cam_r})
    if fl: d.E(o["hand_l"][0]+16,o["hand_l"][1],90,90,(255,255,230,100))
    for q in range(8):
        x=22+q*62; d.R(x,860,x+54,950,(236,236,236,230),3); imp(d,x+27,945,.19,u+q*.4,pose=P_walk(u*0+q*.9,0.0,q),style=dict(horns=True))
    ptext(d,40,190,"FOTOS",8,(255,220,140))
    return im
def sceneE(u):
    im=new((24,24,32),(50,50,64)); d=D(im)
    for r in range(3):
        for c in range(3):
            x=100+c*170; y=360+r*190; d.R(x-70,y-90,x+70,y+90,(0,0,0,70),6)
            imp(d,x,y+82,.5,u+r*.2+c*.1,pose=P_walk(u,3.0,c*1.1+r*.6))
    ptext(d,40,190,"SPRITES",8,(255,255,255))
    return ps1f(im,block=9)
def sceneF(u):
    im=new((30,10,10),(100,30,18)); d=D(im); hell_bg(d,u)
    imp(d,270,900,1.7,u,pose=dict(P_cheer(u),mouth=1.0),style=dict(eyes=(255,230,90)))
    ptext(d,40,190,"VOLUMEN",8,(255,220,140))
    return im
def sceneG(u):
    im=new((34,26,24),(70,56,48)); d=D(im)
    for k in range(5): d.R(k*108,0,k*108+4,640,(0,0,0,30),0)
    d.R(0,740,540,960,(90,60,40),0)
    o=person(d,150,860,1.5,u,P_hold(u,r=(1.3,2.7),grip=.5),ARTIST)
    hx,hy=o["hand_r"]; imp(d,hx,hy-14,.3+.02*math.sin(u*3),u,pose=P_wave(u))
    lump(d,90,745,.7)
    d.R(330,590,500,740,(34,34,40),10); d.E(415,665,36,36,(80,110,160)); d.E(405,655,8,8,(255,255,255,200))
    imp(d,420,920,1.0,u,pose=P_walk(u,2.4))
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx==0 or idx==7: return 1.0+.12*sm(p),270,480+30*sm(p)
    if idx==5: return 1.05+.12*sm(p),270,560-40*sm(p)
    return 1.0+.1*sm(p),270+14*math.sin(u*.7),480
core.CAM=cam
if __name__=="__main__": core.main()
