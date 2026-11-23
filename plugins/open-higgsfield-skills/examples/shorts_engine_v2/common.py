from PIL import Image, ImageOps
import numpy as np
from art import *
def zombie(d,x,y,sc,u,col=(10,8,10)):
    sw=math.sin(u*2.2)*5*sc
    d.E(x+8*sc+sw*.4,y-146*sc,15*sc,17*sc,col+(255,)); d.R(x-18*sc+sw*.3,y-130*sc,x+22*sc+sw*.3,y-62*sc,col+(255,),9*sc)
    d.R(x-14*sc,y-66*sc,x-2*sc,y,col+(255,),4*sc); d.R(x+4*sc,y-66*sc,x+16*sc,y,col+(255,),4*sc)
    for sg in(-1,1): d.P(rotpts([(x+sg*14*sc,y-126*sc),(x+sg*24*sc,y-126*sc),(x+sg*28*sc,y-70*sc),(x+sg*18*sc,y-70*sc)],x+sg*14*sc,y-126*sc,-1.25*sg*0+(-1.1 if sg>0 else 1.1)*0+ (math.pi/2.6)*(-sg)*0),col+(255,))
    d.R(x-34*sc+sw,y-128*sc,x-24*sc+sw,y-92*sc,col+(255,),4*sc); d.R(x+22*sc+sw,y-128*sc,x+32*sc+sw,y-92*sc,col+(255,),4*sc)
def ps1(d,x,y,sc,u):
    shadow(d,x,y+4,120*sc,12*sc,80)
    bevel(d,x-110*sc,y-70*sc,x+110*sc,y,(178,178,184),10*sc)
    d.R(x-110*sc,y-30*sc,x+110*sc,y-26*sc,(0,0,0,50),0)
    d.E(x,y-70*sc,64*sc,12*sc,(150,150,158)); d.E(x,y-74*sc,36*sc,8*sc,(210,210,218))
    d.E(x+70*sc,y-18*sc,7*sc,7*sc,(90,255,140)); d.E(x-70*sc,y-18*sc,7*sc,7*sc,(255,90,90))
def tv(d,x,y,w,h,inner,u):
    bevel(d,x,y,x+w,y+h,(62,60,70),14); d.R(x+10,y+10,x+w-10,y+h-18,(4,6,10),8)
    inner(d,x+10,y+10,w-20,h-28); 
    for k in range(int((h-28)/5)): d.R(x+10,y+10+k*5,x+w-10,y+11+k*5,(0,0,0,50))
    d.E(x+w-24,y+h-9,3,3,(80,255,140))

_BAY=np.array([[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]],dtype=np.float32)
def ps1f(im,block=6):
    """aspecto PlayStation 1996: baja resolucion, colores reducidos con trama (dither) y pixeles grandes"""
    w,h=im.size; sm_=im.resize((w//block,h//block),Image.BOX)
    a=np.array(sm_).astype(np.float32)
    bay=np.tile(_BAY,(a.shape[0]//4+1,a.shape[1]//4+1))[:a.shape[0],:a.shape[1]]
    a=a+(bay[...,None]-7.5)*1.4
    a=np.clip(np.round(a/16.0)*16.0,0,255).astype(np.uint8)
    return Image.fromarray(a).resize((w,h),Image.NEAREST)
