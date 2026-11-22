import sys; sys.path.insert(0,"..")
from art import *
from rig import *
YEL=(206,188,92)
W1=dict(skin=(226,184,150),hair=(60,44,32),hairstyle="short",shirt=(200,200,206),pants=(70,90,130),shoes=(236,236,240),sleeve="short")
W2=dict(skin=(214,170,130),hair=(30,24,20),hairstyle="long",shirt=(150,60,70),pants=(40,44,56),shoes=(40,36,36),sleeve="long")
W3=dict(skin=(240,200,160),hair=(190,140,60),hairstyle="ponytail",shirt=(70,120,100),pants=(80,80,90),shoes=(50,46,46),sleeve="short")
CAP=dict(skin=(226,184,150),hair=(60,44,32),hairstyle="short",hat="cap",cap_col=(40,40,60),shirt=(60,60,80),pants=(50,50,60),shoes=(30,30,34),sleeve="long")
def yroom(d,u,speed=.25,pulse=1.0,alt=0.0):
    corridor(d,u,speed=speed,wall=YEL,floor=(150,126,70),ceil=(214,208,176),door=(170,150,80),light=(255,250,220),n=11,doors=False,pulse=pulse,alt=alt)
def office(d,x0,y0,x1,y1):
    d.R(x0,y0,x1,y1,YEL,0)
    for k in range(10): d.R(x0+k*((x1-x0)/10),y0,x0+k*((x1-x0)/10)+4,y1,(170,150,70,120),0)
    d.R(x0,y1-(y1-y0)*.3,x1,y1,(150,126,70),0); d.R(x0,y0,x1,y0+(y1-y0)*.12,(220,214,184),0)
    for k in range(3): d.R(x0+(x1-x0)*(.1+k*.3),y0+3,x0+(x1-x0)*(.3+k*.3),y0+(y1-y0)*.1,(255,252,230),1)
def maze_top(d,x,y,w,h,col=(60,52,20)):
    d.R(x,y,x+w,y+h,(236,220,140),4)
    for r in range(8):
        for c in range(5):
            if rnd(r*7+c)>.45: d.R(x+c*(w/5)+3,y+r*(h/8)+3,x+(c+1)*(w/5)-3,y+r*(h/8)+10,col,1)
            if rnd(r*5+c+40)>.5: d.R(x+c*(w/5)+3,y+r*(h/8)+3,x+c*(w/5)+10,y+(r+1)*(h/8)-3,col,1)
def walker(d,x,y,sc,u,st,ph=0.0): return person(d,x,y,sc,u,P_walk(u,3.0,ph),st,facing="back")
def sceneA(u,final=False):
    im=new((206,188,92),(150,126,70)); d=D(im); yroom(d,u,.2,pulse=flicker(u,3,3))
    b=sm(u/1.0) if not final else 1.0
    walker(d,270,720-u*8,1.25-.05*u,u,W1)
    d.R(0,0,540,960,(0,0,0,int(90*(1-b))),0); d.R(10,10,530,950,None,0,(255,255,255,60),3)
    return im
def sceneB(u):
    im=new((24,24,28),(48,48,56)); d=D(im)
    def pol(dd,x,y,a,s): pass
    o=person(d,270,1010,1.8,u,dict(al=(1.7,2.5),ar=(1.7,2.5),ll=(.05,.05),lr=(.05,.05),bob=math.sin(u*2),tilt=.04,look=(0,.3),mouth=0,curlL=.5,curlR=.5,hands_front=True),W1)
    cx=(o["hand_l"][0]+o["hand_r"][0])/2; cy=(o["hand_l"][1]+o["hand_r"][1])/2
    d.R(cx-90,cy-70,cx+90,cy+60,(244,242,236),5); d.R(cx-80,cy-60,cx+80,cy+22,(40,40,44),2); office(d,cx-80,cy-60,cx+80,cy+22)
    d.R(cx-90,cy-70,cx+90,cy-65,(255,255,255,70),5)
    # los dedos sujetan la foto: se redibujan sobre el borde
    for hp in (o["hand_l"],o["hand_r"]): d.E(hp[0],hp[1],10,10,(226,184,150,255))
    ptext(d,cx-76,cy+30,"INTERNET 2019",2.4,(60,60,60))
    return im
def sceneC(u):
    im=new((30,28,18),(70,60,32)); d=D(im); d.R(0,600,540,960,(150,126,70),0)
    for k in range(6): d.L(0,630+k*50,540,630+k*50,(0,0,0,40),2)
    p=sm((u-.6)/3.2)
    d.E(270,760,40+p*160,12+p*34,(0,0,0,int(160*p)))
    person(d,270,720+p*60,1.3-p*.6,u,dict(P_scared(u),al=(.9+p,2.4),ar=(.9+p,2.4),bob=0),W2) if p<.95 else None
    d.R(0,760+p*60+16,540,960,(150,126,70),0)
    d.E(270,760,40+p*160,12+p*34,(0,0,0,int(140*p)))
    for k in range(10): a=k*.62; d.L(270,760,270+math.cos(a)*(60+p*150),760+math.sin(a)*(14+p*30),(0,0,0,150),3)
    ptext(d,40,190,"NOCLIP",9,(255,255,255))
    return im
def sceneD(u):
    im=new((206,188,92),(150,126,70)); d=D(im); yroom(d,u,.18,alt=.5)
    walker(d,270,740,1.25,u,W1,0)
    walker(d,250,600,.8,u,W2,1.2)
    walker(d,290,540,.5,u,W3,2.4)
    maze_top(d,330,100,180,270); ptext(d,330,380,"INFINITO",3.2,(255,255,255))
    d.R(0,0,540,960,(0,0,0,40),0)
    return im
def sceneE(u):
    im=new((20,20,26),(40,38,46)); d=D(im)
    nodes=[(270,300,"BACKROOMS"),(110,470,"NIVELES"),(270,540,"ENTIDADES"),(430,470,"REGLAS")]
    for (x,y,t) in nodes[1:]: d.L(270,300,x,y,(255,230,120,120),3)
    for i,(x,y,t) in enumerate(nodes):
        r=sm((u-i*.5)/.7); w=len(t)*4*3.4/2+14
        d.R(x-w*r,y-26*r,x+w*r,y+26*r,YEL+(255,),8)
        if r>.8: ptext(d,x-len(t)*4*3.4/2+3,y-8,t,3.4,(40,34,12))
    d.R(0,760,540,960,(40,34,24),0)
    for k,(x,st) in enumerate(((110,W1),(270,W2),(430,W3))):
        d.R(x-70,830,x+70,846,(60,60,70),4)
        o=person(d,x,1000,1.2,u,dict(al=(.5,.5),ar=(.5,.5),ll=(.05,.05),lr=(.05,.05),bob=0,tilt=.04,look=(0,.7),mouth=.3,curlL=.5,curlR=.5,hands_front=True),st)
        d.P([(x-60,836),(x+60,836),(x+50,760),(x-50,760)],(30,30,36,255)); d.R(x-62,836,x+62,842,(90,90,100),2)
    return im
def sceneF(u):
    im=new((10,10,14),(24,24,30)); d=D(im)
    d.R(70,300,470,560,(10,10,12),10); office(d,80,310,460,550); d.R(70,300,470,560,None,10,(255,255,255,60),3)
    if int(u*1.2)%2==0: d.E(112,332,9,9,(240,40,40))
    ptext(d,130,324,"REC",3.4,(240,240,240)); ptext(d,330,324,"02:%02d"%(int(u*6)%60),3.4,(240,240,240))
    def cm(dd,x,y,a,s): dd.R(x-26,y-18,x+30,y+20,(30,30,36),6); dd.E(x+34,y,12,12,(60,90,140)); dd.E(x-18,y-24,6,6,(240,50,50))
    person(d,270,1000,1.7,u,dict(al=(1.5,2.6),ar=(1.6,2.6),ll=(.05,.05),lr=(.05,.05),bob=math.sin(u*3)*1.5,tilt=.04*math.sin(u*2),look=(0,0),mouth=0,curlL=.8,curlR=.8,hands_front=True),CAP,props={"r":cm})
    d.R(190,800,350,860,(240,30,30),20); d.P([(240,812),(240,848),(300,830)],(255,255,255))
    ptext(d,40,235,"2022",9,(255,255,255))
    return im
def sceneG(u):
    im=new((206,188,92),(150,126,70)); d=D(im); yroom(d,u,.12,pulse=flicker(u,2,4))
    d.R(40,180,500,560,(244,242,236),6); d.R(60,200,480,540,(40,40,44),2); office(d,60,200,480,540); d.R(0,0,540,960,(0,0,0,50),0)
    person(d,140,980,1.7,u,dict(P_idle(u),ar=(1.6,2.6),look=(.7,-.4),curlR=.6,mouth=.2),W3)
    person(d,410,980,1.7,u,dict(P_idle(u,2),al=(1.6,2.6),look=(-.7,-.4),curlL=.6),W1)
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx in(0,7): return 1.0+.1*sm(p),270,500
    return 1.0+.1*sm(p),270+14*math.sin(u*.9),480
core.CAM=cam
if __name__=="__main__": core.main()
