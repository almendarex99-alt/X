import sys; sys.path.insert(0,"..")
from art import *
from rig import *
RED=(190,30,30); GRN=(30,120,50)
FRED=dict(skin=(150,110,100),hair=(30,24,20),hairstyle="bald",hat="fedora",shirt=RED,shirt2=GRN,pants=(110,90,70),shoes=(60,40,30),sleeve="long",coat=None,face=False,height=1.0,belt=(70,50,40))
TEEN=dict(skin=(236,196,160),hair=(120,70,40),hairstyle="short",shirt=(70,110,170),pants=(60,64,90),shoes=(240,240,244),sleeve="short")
TEENF=dict(skin=(240,200,168),hair=(200,150,70),hairstyle="long",shirt=(200,120,160),pants=(70,70,100),shoes=(220,220,230),sleeve="short")
BULLY=dict(skin=(226,176,140),hair=(40,28,20),hairstyle="short",shirt=(80,80,90),pants=(50,50,70),shoes=(30,30,34),sleeve="long",height=1.05,bulk=1.2)
def blades(d,hand,sc,u,col=(206,212,222)):
    x,y=hand
    for k in range(4):
        a=.12*(k-1.5)+.05*math.sin(u*6); d.P([(x-3*sc+k*6*sc-9*sc,y+8*sc),(x+3*sc+k*6*sc-9*sc,y+8*sc),(x+k*6*sc-9*sc+math.sin(a)*70*sc,y+8*sc+math.cos(a)*70*sc)],col+(255,))
def fred(d,x,y,sc,u,pose=None,ph=0.0):
    o=person(d,x,y,sc,u,pose or dict(P_walk(u,2.4,ph),ar=(.9,.9)),FRED,deco=lambda dd,hx,hy,s: dd.E(hx,hy-1*s,17*s,15*s,(20,14,14,200)))
    blades(d,o["hand_r"],sc,u); return o
def room(d,u,frost=0.0):
    gradient(d,0,560,(18,14,30),(40,30,56)); d.R(0,560,540,960,(30,22,30),0)
    for k in range(7): d.L(0,590+k*50,540,590+k*50,(0,0,0,50),2)
    d.R(330,110,500,360,(16,20,40),6); d.R(330,110,500,360,None,6,(100,80,70),8); d.L(415,110,415,360,(100,80,70),6); d.E(415,200,18,18,(240,240,250,200))
def bed(d,x,y,sc):
    d.R(x-150*sc,y-30*sc,x+150*sc,y+60*sc,(110,90,110),10*sc); d.R(x-150*sc,y-110*sc,x-128*sc,y+70*sc,(70,50,40),4*sc); d.R(x+128*sc,y-80*sc,x+150*sc,y+70*sc,(70,50,40),4*sc)
    d.R(x-132*sc,y-60*sc,x-50*sc,y-26*sc,(230,230,240),8*sc)
def sleeper(d,x,y,sc,u):
    """persona tumbada: cabeza sobre la almohada, cuello, torso bajo la manta y un brazo con mano fuera"""
    b=math.sin(u*1.6)*2*sc; hx=x-96*sc; hy=y-48*sc
    d.E(hx-8*sc,hy-4*sc,30*sc,28*sc,(120,70,40)); d.R(hx-2*sc,hy+4*sc,hx+16*sc,hy+24*sc,(220,180,146),3*sc)
    d.E(hx,hy,20*sc,22*sc,(236,196,160)); d.E(hx-8*sc,hy-10*sc,21*sc,14*sc,(120,70,40))
    d.L(hx-8*sc,hy-2*sc,hx-2*sc,hy-2*sc,(30,20,20),2*sc); d.L(hx+6*sc,hy-2*sc,hx+12*sc,hy-2*sc,(30,20,20),2*sc); d.A(hx+4*sc,hy+12*sc,6*sc,3*sc,20,160,(150,70,70),1.5*sc)
    d.R(x-82*sc,y-34*sc+b,x+120*sc,y+8*sc+b,(70,70,120),14*sc); d.R(x-82*sc,y-34*sc+b,x+120*sc,y-26*sc+b,(255,255,255,40),8*sc)
    hand(d,x-40*sc,y-24*sc,1.55,1,sc*.9,(236,196,160),curl=.4,spread=.7)
    d.L(x-62*sc,y-30*sc,x-40*sc,y-24*sc,(70,110,170),9*sc)
def sceneA(u,final=False):
    im=new((18,14,30),(40,30,56)); d=D(im); room(d,u); bed(d,200,740,1.3); sleeper(d,200,730,1.25,u)
    fogband(d,u,520,820,(150,120,170),50,10)
    b=sm(u/1.2) if not final else 1.0
    fred(d,400,860,1.4*b+.01,u,dict(P_idle(u),ar=(.9,1.0)))
    return im
def sceneB(u):
    im=new((14,14,24),(34,34,52)); d=D(im); d.R(0,700,540,960,(24,26,28),0)
    d.R(180,260,360,700,(40,36,44),0); d.P([(160,260),(270,150),(380,260)],(30,28,34))
    d.R(230,480,310,700,(70,50,40),2); d.R(200,300,260,380,(255,210,130,int(200*flicker(u,3,5))),2)
    person(d,110,950,1.4,u,P_walk(u,2.6),TEEN); person(d,420,950,1.4,u,P_walk(u,2.6,1.5),TEENF)
    d.R(40,720,500,790,(0,160,90),6); ptext(d,60,738,"ELM STREET",8,(255,255,255))
    ptext(d,40,200,"1984",9,(255,255,255))
    return im
def sceneC(u):
    im=new((30,28,26),(62,58,52)); d=D(im); d.R(0,780,540,960,(90,66,46),0)
    d.R(230,160,490,640,(236,230,214),4); d.R(230,160,490,215,(60,56,50),4); ptext(d,246,176,"NOTICIA",6,(240,240,240))
    for k in range(3): d.R(246,240+k*50,340,280+k*50,(180,176,164),2)
    for k in range(9): d.R(352,240+k*24,476,248+k*24,(110,106,98),2)
    for k in range(5): d.R(246,420+k*24,340,428+k*24,(110,106,98),2)
    def paper(dd,x,y,a,s): pass
    person(d,110,1000,1.6,u,dict(al=(1.5,2.2),ar=(1.7,2.0),ll=(.05,.05),lr=(.05,.05),bob=math.sin(u*2),tilt=.06,look=(.8,0),mouth=.2,curlL=.7,curlR=.4,hands_front=True),dict(skin=(236,196,160),hair=(40,30,26),hairstyle="short",shirt=(110,100,90),pants=(60,56,60),coat=(80,70,64),sleeve="long"))
    return im
def sceneD(u):
    im=new((10,12,24),(26,30,52)); d=D(im); d.R(0,800,540,960,(40,30,30),0)
    d.E(110,420,70,70,(236,236,240)); d.E(110,420,70,70,None,(40,40,50),6)
    a=u*2.0; d.L(110,420,110+math.cos(a)*46,420+math.sin(a)*46,(30,30,36),5); d.L(110,420,110+math.cos(a*12)*58,420+math.sin(a*12)*58,(210,40,40),3)
    for k in range(3): d.R(330+k*58,700,368+k*58,758,(240,240,244),6); d.R(368+k*58,714,380+k*58,740,(240,240,244),4); d.E(349+k*58,686-(u*30+k*20)%40,8,12,(240,240,250,90))
    drop=.1*math.sin(u*1.4)+.3
    person(d,270,1000,1.6,u,dict(P_idle(u),al=(.25,.5),ar=(.9,1.9),tilt=.18*math.sin(u*1.2)+.05,look=(0,.5),mouth=.2*(math.sin(u*1.2)>0),curlR=.8,bob=math.sin(u*1.2)*3),TEEN,props={"r":lambda dd,x,y,a,s: (dd.R(x-9,y-6,x+9,y+22,(240,240,244),3),dd.E(x,y-10,6,3,(70,40,30)))})
    ptext(d,40,225,"NO DORMIR",7,(255,255,255))
    return im
def sceneE(u):
    im=new((24,10,28),(60,24,60)); d=D(im)
    corridor(d,u,speed=.22,wall=(70,44,60),floor=(34,30,34),ceil=(40,30,44),door=(90,60,50),light=(255,140,90),n=9,doors=False,pulse=flicker(u,3,5))
    fogband(d,u,520,820,(150,120,170),50,10)
    z=sm(u/6.0); fred(d,270,lerp(520,860,z),lerp(.45,1.5,z),u,dict(P_walk(u,2.6),ar=(.9,1.0)))
    person(d,140,960,1.3,u,dict(P_scared(u),mouth=1.0),TEEN)
    return im
def sceneF(u):
    im=new((30,26,22),(64,54,44)); d=D(im); d.R(0,800,540,960,(90,66,46),0)
    d.R(40,440,500,520,(160,120,80),6); d.R(70,520,92,760,(80,70,66),2); d.R(450,520,472,760,(80,70,66),2)
    d.R(90,456,280,486,(255,255,255,40),4); ptext(d,104,460,"FRED",8,(60,40,30))
    person(d,130,960,1.4,u,dict(P_scared(u),al=(.5,1.2),ar=(.5,1.2)),TEEN)
    person(d,400,960,1.5,u,dict(P_talk(u),ar=(.9,.9),al=(.9,.9),curlL=1.0,curlR=1.0,mouth=.8),BULLY)
    ptext(d,40,235,"EL COLEGIO",5,(255,255,255))
    return im
def sceneG(u):
    im=new((14,10,24),(34,24,50)); d=D(im)
    d.R(30,200,230,420,(236,230,214),6); d.R(30,200,230,240,(60,56,50),6)
    for k in range(5): d.R(46,260+k*30,214-((k*29)%50),270+k*30,(110,106,98),2)
    d.R(310,200,510,420,(160,120,80),6); ptext(d,330,290,"FRED",7,(60,40,30))
    fred(d,270,960,1.5,u,dict(P_idle(u),ar=(.9,1.0),al=(.3,.4)))
    ptext(d,40,125,"DOS MIEDOS",6,(255,255,255,0)) if False else None
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx in(0,7): return 1.0+.12*sm(p),270,500
    return 1.0+.1*sm(p),270+14*math.sin(u*.9),480
core.CAM=cam
if __name__=="__main__": core.main()
