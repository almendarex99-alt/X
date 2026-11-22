import sys; sys.path.insert(0,"..")
from art import *
from rig import *
GOLD=(255,214,70)
LINK=dict(skin=(244,200,160),hair=(214,170,80),hairstyle="short",hat="greencap",shirt=(40,150,60),pants=(240,236,220),shoes=(130,84,50),belt=(130,80,40),sleeve="short",brow=(120,80,30),eyes=(60,90,160))
ZELDA=dict(skin=(244,206,170),hair=(232,190,84),hairstyle="long",hat="crown",dress=True,shirt=(240,150,200),skirt_col=(244,170,214),sleeve="long",shoes=(200,160,60),eyes=(60,90,160),brow=(150,110,40))
DESIGNER=dict(skin=(230,190,150),hair=(30,24,20),hairstyle="short",glasses=True,shirt=(210,210,216),sleeve="long",pants=(60,64,80))
FLAPPER=dict(skin=(244,206,176),hair=(50,34,28),hairstyle="bob",hat="headband",dress=True,shirt=(190,60,100),skirt_col=(200,80,116),sleeve="none",shoes=(60,40,40),brow=(40,26,20))
WRITER=dict(skin=(236,196,160),hair=(70,56,40),hairstyle="short",shirt=(40,50,70),coat=(30,34,50),pants=(40,44,60),sleeve="long",shoes=(30,28,32))
KID=dict(skin=(226,176,140),hair=(40,26,20),hairstyle="short",shirt=(200,70,60),pants=(60,70,110),sleeve="short")
def tri(d,x,y,s,col=GOLD,a=255): d.P([(x,y-s),(x-s*.9,y+s*.7),(x+s*.9,y+s*.7)],col+(a,))
def triforce(d,x,y,s,u=0.0,glow=1.0):
    d.E(x,y,s*2.2,s*2.0,GOLD+(int(40*glow),)); d.E(x,y,s*1.5,s*1.4,GOLD+(int(50*glow),))
    tri(d,x,y-s*.55,s*.5); tri(d,x-s*.5,y+s*.35,s*.5); tri(d,x+s*.5,y+s*.35,s*.5)
def field(d,u):
    gradient(d,0,520,(120,200,250),(220,240,255)); d.R(0,520,540,960,(70,170,70),0)
    for k in range(40): x=rnd(k)*540; y=540+rnd(k,1)*420; d.L(x,y,x+3+math.sin(u*2+k)*3,y-9,(40,130,50,200),2)
    d.P([(0,520),(110,430),(230,520)],(90,140,120)); d.P([(200,520),(340,400),(540,520)],(70,120,110))
    d.E(420,130,34,34,(255,244,190,230))
    for k in range(3): x=((u*14+k*190)%700)-80; d.E(x,90+k*40,60,16,(255,255,255,170)); d.E(x+30,80+k*40,40,14,(255,255,255,170))
def sword_prop(dd,x,y,a,s): dd.R(x-3,y-82,x+3,y-8,(224,230,240),1); dd.R(x-13,y-10,x+13,y-4,(130,80,40),2); dd.R(x-3,y-4,x+3,y+16,(110,70,40),1)
def shield_prop(dd,x,y,a,s): dd.E(x-4,y,22,28,(30,70,170)); dd.E(x-4,y,16,22,(210,60,60)); dd.P([(x-4,y-14),(x-10,y+8),(x+2,y+8)],GOLD)
def sceneA(u,final=False):
    im=new((10,30,50),(30,60,70)); d=D(im); field(d,u)
    b=sm(u/1.0) if not final else 1.0
    triforce(d,270,300,64*(.8+.2*b),u,glow=.7+.3*math.sin(u*3))
    person(d,170,900,1.4,u,P_walk(u,2.2),LINK,props={"r":sword_prop,"l":shield_prop})
    person(d,380,900,1.4,u,P_idle(u,1),ZELDA)
    ptext(d,236,520,"?",12,(255,255,255))
    return im
def sceneB(u):
    im=new((30,30,44),(60,60,80)); d=D(im); d.R(0,780,540,960,(70,50,40),0)
    d.R(60,640,480,790,(70,70,76),10); d.R(60,640,480,660,(255,255,255,30),10); d.R(180,712,360,730,(20,20,24),4)
    def cart(dd,x,y,a,s):
        dd.R(x-34,y-44,x+34,y+44,(220,180,50),6); dd.R(x-26,y-30,x+26,y+16,(30,40,30),4); tri(dd,x,y-6,12)
    t=sm(u/1.5)
    person(d,270,1010,1.7,u,dict(al=(1.5,2.2),ar=(1.5,2.2),ll=(.05,.05),lr=(.05,.05),bob=math.sin(u*2),tilt=.05,look=(0,.5),mouth=0,curlL=.9,curlR=.9,hands_front=True),KID,props={"l":cart})
    ptext(d,40,200,"1986",9,(255,255,255))
    return im
def sceneC(u):
    im=new((40,30,26),(80,60,48)); d=D(im); d.R(0,860,540,960,(110,76,50),0)
    d.R(220,520,500,820,(240,236,220),6)
    for i in range(3):
        d.R(236,540+i*34,380,568+i*34,(255,255,255),3)
        if i<2: d.L(236,554+i*34,380,554+i*34,(210,60,60),3)
    p=sm(u/3.0);
    def pencil(dd,x,y,a,s): dd.L(x,y-10,x+10,y+36,(240,200,60),6); dd.P([(x+10,y+36),(x+7,y+46),(x+13,y+46)],(40,30,20))
    person(d,150,1010,1.7,u,dict(al=(.5,.3),ar=(1.15+.08*math.sin(u*5),1.55+.2*math.sin(u*5)),ll=(.05,.05),lr=(.05,.05),bob=math.sin(u*2),tilt=.08,look=(.5,.6),mouth=0,curlL=.4,curlR=.8,hands_front=True),DESIGNER,props={"r":pencil})
    princess_scale=.5*p
    if p>.1: person(d,400,780,princess_scale+.05,u,P_idle(u),ZELDA)
    d.R(0,830,540,960,(110,76,50),0); d.R(0,830,540,838,(255,255,255,30),0)
    ptext(d,40,190,"NOMBRE",8,(255,255,255))
    return im
def sceneD(u):
    im=new((24,20,30),(52,44,60)); d=D(im); d.R(0,860,540,960,(40,30,40),0)
    for k in range(5): d.R(k*108,0,k*108+4,860,(0,0,0,30),0)
    d.R(60,200,250,420,(60,40,80),8); d.R(70,210,240,410,(236,220,180),4); ptext(d,84,240,"F. SCOTT",3.4,(60,40,30)); ptext(d,84,290,"FITZGERALD",2.9,(60,40,30)); d.L(84,340,226,340,(60,40,30,120),2)
    person(d,200,930,1.55,u,P_idle(u),WRITER)
    person(d,370,930,1.55,u,dict(P_wave(u,1),mouth=.4),FLAPPER)
    ptext(d,40,840,"ZELDA FITZGERALD",3.2,(255,255,255))
    return im
def sceneE(u):
    im=new((10,20,40),(30,50,80)); d=D(im); b=sm(u/1.0)
    for i,ch in enumerate("ZELDA"): ptext(d,50+i*92,300+math.sin(u*3+i)*8,ch,18,GOLD)
    for k in range(26): a=k*.5+u; d.E(270+math.cos(a)*(190+k*3),420+math.sin(a)*(160+k*4),3,3,(255,240,150,int(200*abs(math.sin(u*2+k)))))
    person(d,270,930,1.5,u,P_wave(u),ZELDA)
    ptext(d,60,150,"SUENA BIEN",7,(255,255,255))
    return im
def sceneF(u):
    im=new((60,140,200),(150,210,240)); d=D(im); field(d,u)
    sw=math.sin(u*3)
    person(d,150,930,1.7,u,dict(P_hold(u),ar=(1.2+.6*sw,2.3+.8*sw),curlR=1.0),LINK,props={"r":sword_prop,"l":shield_prop})
    person(d,400,930,1.6,u,P_wave(u),ZELDA)
    d.R(40,320,260,370,(0,0,0,150),8); ptext(d,54,333,"ESTE ES LINK",3.4,(255,255,255))
    d.R(290,320,510,370,(0,0,0,150),8); ptext(d,302,333,"ELLA ES ZELDA",3.0,(255,214,70))
    return im
def sceneG(u):
    im=new((60,140,200),(150,210,240)); d=D(im); field(d,u)
    triforce(d,270,260,52,u)
    person(d,270,930,1.6,u,P_walk(u,3.0),LINK,props={"r":sword_prop,"l":shield_prop})
    for k,(x,st) in enumerate(((70,KID),(160,DESIGNER),(380,WRITER),(470,FLAPPER))):
        person(d,x,780,.9,u+k,dict(P_point(u+k,dirx=1 if x<270 else -1),ar=(1.45,1.5)) if x<270 else dict(P_point(u+k,dirx=-1),ar=(.12,.2),al=(1.45,1.5)),st)
        ptext(d,x-12,430+(k%2)*60,"?",5,(255,255,255))
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx in(0,7): return 1.0+.1*sm(p),270,500
    return 1.0+.1*sm(p),270+16*math.sin(u*.8),480
core.CAM=cam
if __name__=="__main__": core.main()
