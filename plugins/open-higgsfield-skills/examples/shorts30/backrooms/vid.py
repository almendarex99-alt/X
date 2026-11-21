import sys; sys.path.insert(0,"..")
from art import *
YEL=(206,188,92)
def yroom(d,u,speed=.25,pulse=1.0,alt=0.0):
    corridor(d,u,speed=speed,wall=YEL,floor=(150,126,70),ceil=(214,208,176),door=(170,150,80),light=(255,250,220),n=11,doors=False,pulse=pulse,alt=alt)
    # franjas verticales del papel pintado
    for k in range(14): d.R(k*40,0,k*40+4,0,(0,0,0,0),0)
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
def sceneA(u,final=False):
    im=new((206,188,92),(150,126,70)); d=D(im); yroom(d,u,.2,pulse=flicker(u,3,3))
    b=sm(u/1.0) if not final else 1.0
    d.R(0,0,540,960,(0,0,0,int(90*(1-b))),0)
    d.R(10,10,530,950,None,0,(255,255,255,60),3)
    return im
def sceneB(u):
    im=new((24,24,28),(48,48,56)); d=D(im)
    # fotografia polaroid de una oficina vacia
    d.R(60,170,480,720,(244,242,236),6); d.R(80,190,460,620,(40,40,44),2); office(d,80,190,460,620)
    d.R(60,170,480,176,(255,255,255,70),6)
    ptext(d,90,640,"INTERNET",5,(60,60,60)); ptext(d,90,690,"2019",5,(60,60,60))
    d.L(0,0,60,170,(255,255,255,0),1)
    return im
def sceneC(u):
    im=new((30,28,18),(70,60,32)); d=D(im); d.R(0,600,540,960,(150,126,70),0)
    for k in range(6): d.L(0,630+k*50,540,630+k*50,(0,0,0,40),2)
    p=sm(u/3.5)
    silhouette(d,270,640+p*220,1.5-p*.5,(20,20,24))
    for k in range(10): a=k*.62; d.L(270,720,270+math.cos(a)*(80+p*90),720+math.sin(a)*(20+p*30),(0,0,0,150),3)
    d.E(270,740,60+p*150,14+p*30,(0,0,0,int(120*p)))
    ptext(d,40,190,"NOCLIP",9,(255,255,255))
    return im
def sceneD(u):
    im=new((206,188,92),(150,126,70)); d=D(im); yroom(d,u,.18,alt=.5)
    maze_top(d,300,100,200,300); ptext(d,300,420,"INFINITO",3.4,(255,255,255))
    d.R(0,0,540,960,(0,0,0,40),0)
    return im
def sceneE(u):
    im=new((20,20,26),(40,38,46)); d=D(im)
    nodes=[(270,300,"BACKROOMS"),(110,520,"NIVELES"),(270,620,"ENTIDADES"),(430,520,"REGLAS")]
    for (x,y,t) in nodes[1:]: d.L(270,300,x,y,(255,230,120,120),3)
    for i,(x,y,t) in enumerate(nodes):
        r=sm((u-i*.5)/.7); w=len(t)*4*3.4/2+14
        d.R(x-w*r,y-26*r,x+w*r,y+26*r,YEL+(255,),8);
        if r>.8: ptext(d,x-len(t)*4*3.4/2+3,y-8,t,3.4,(40,34,12))
    for k in range(24): a=k*.4+u*.3; d.E(270+math.cos(a)*(200+k*4),600+math.sin(a)*(240+k*3),2,2,YEL+(120,))
    return im
def sceneF(u):
    im=new((10,10,14),(24,24,30)); d=D(im)
    d.R(80,280,460,640,(10,10,12),10); office(d,90,290,450,630)
    d.R(80,280,460,640,None,10,(255,255,255,60),3)
    if int(u*1.2)%2==0: d.E(112,312,9,9,(240,40,40))
    ptext(d,130,304,"REC",3.4,(240,240,240)); ptext(d,330,304,"02:%02d"%(int(u*6)%60),3.4,(240,240,240))
    # boton de reproduccion
    d.R(190,720,350,820,(240,30,30),24); d.P([(240,740),(240,800),(300,770)],(255,255,255))
    ptext(d,40,190,"2022",9,(255,255,255))
    return im
def sceneG(u):
    im=new((206,188,92),(150,126,70)); d=D(im); yroom(d,u,.15,pulse=flicker(u,2,4))
    d.R(60,200,480,620,(244,242,236),6); d.R(78,218,462,602,(40,40,44),2); office(d,78,218,462,602)
    d.R(0,0,540,960,(0,0,0,50),0)
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx in(0,7,1,4,5): return 1.0,270,480
    return 1.0+.1*sm(p),270,480
core.CAM=cam
if __name__=="__main__": core.main()
