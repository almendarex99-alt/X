import sys; sys.path.insert(0,"..")
import core, math, random
from core import *
import json,os
_T=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"skins.json")))
def crop(a,r0,r1,c0,c1): return [[tuple(px) for px in row[c0:c1]] for row in a[r0:r1]]
FR=_T["steve"]["front"]; BK=_T["steve"]["back"]; SRV=_T["steve"]["right"]
STV=dict(head=dict(front=crop(FR,0,8,4,12),side=crop(SRV,0,8,0,8),top=[[tuple(BK[j%2][4+i]) for i in range(8)] for j in range(8)]),
  body=dict(front=crop(FR,8,20,4,12),side=crop(FR,8,20,4,8),top=None),
  armL=dict(front=crop(FR,8,20,0,4),side=crop(SRV,8,20,2,6),top=None),armR=dict(front=crop(FR,8,20,12,16),side=crop(SRV,8,20,2,6),top=None),
  legL=dict(front=crop(FR,20,32,4,8),side=crop(SRV,20,32,2,6),top=None),legR=dict(front=crop(FR,20,32,8,12),side=crop(SRV,20,32,2,6),top=None))
CF=["........","........","..XX.XX.","..XX.XX.","...XX...","..XXXX..","..XXXX..","..X..X.."]
_C=_T["creeper"]
def _face(arr):
    out=[[tuple(p) for p in row] for row in arr]
    for j,row in enumerate(CF):
        for i,ch in enumerate(row):
            if ch=='X': out[j][i]=(4,10,4)
    return out
CRT=dict(head=dict(front=_face(_C["seg2"]),side=[[tuple(p) for p in r] for r in _C["seg3"]],top=[[tuple(p) for p in r] for r in _C["top"]]),
  body=dict(front=crop(_C["body"],0,12,4,12),side=crop(_C["body"],0,12,12,16),top=None),
  leg=dict(front=crop(_C["body"],0,6,0,4),side=crop(_C["body"],6,12,12,16),top=None))
def _shade(c,k): return tuple(int(clamp(v*k,0,255)) for v in c)
def tbox(d,x,y,w,h,dp,tex,a=255,dark=1.0):
    ox,oy=dp*.55,-dp*.45
    F=tex["front"]; ny=len(F); nx=len(F[0])
    side=tex.get("side") or [[_shade(F[j][-1],.72) for _ in range(4)] for j in range(ny)]
    top=tex.get("top") or [[_shade(F[0][i],1.15) for i in range(nx)] for _ in range(4)]
    sh=len(side); sw=len(side[0]); th=len(top); tw=len(top[0])
    for j in range(th):      # tapa superior (en perspectiva)
        for i in range(tw):
            p=[(x+i*w/tw+ox*j/th,y+oy*j/th),(x+(i+1)*w/tw+ox*j/th,y+oy*j/th),(x+(i+1)*w/tw+ox*(j+1)/th,y+oy*(j+1)/th),(x+i*w/tw+ox*(j+1)/th,y+oy*(j+1)/th)]
            d.P(p,_shade(top[j][i],1.12*dark)+(a,))
    for i in range(sw):      # cara lateral derecha
        for j in range(sh):
            p=[(x+w+ox*i/sw,y+oy*i/sw+j*h/sh),(x+w+ox*(i+1)/sw,y+oy*(i+1)/sw+j*h/sh),(x+w+ox*(i+1)/sw,y+oy*(i+1)/sw+(j+1)*h/sh+.4),(x+w+ox*i/sw,y+oy*i/sw+(j+1)*h/sh+.4)]
            d.P(p,_shade(side[j][i],.78*dark)+(a,))
    for j in range(ny):
        for i in range(nx):
            d.R(x+i*w/nx,y+j*h/ny,x+(i+1)*w/nx+.4,y+(j+1)*h/ny+.4,_shade(F[j][i],dark)+(a,),0)
    d.L(x,y,x+w,y,(255,255,255,30),1.2)
def tex_color(base,i,j,var=22,seed=0):
    h=((i*73856093)^(j*19349663)^(seed*83492791))&0xffff; v=(h%1000)/1000.0-.5
    return tuple(int(clamp(c+v*var,0,255)) for c in base)
def box(d,x,y,w,h,dp,base,cells=(8,8),seed=0,face=None,top=None,side=None,a=255):
    """caja en proyeccion oblicua: frente (x,y,w,h), profundidad dp"""
    ox,oy=dp*.55,-dp*.45
    tcol=top or tuple(min(255,int(c*1.18)) for c in base); scol=side or tuple(int(c*.72) for c in base)
    d.P([(x,y),(x+w,y),(x+w+ox,y+oy),(x+ox,y+oy)],tcol+(a,))
    d.P([(x+w,y),(x+w+ox,y+oy),(x+w+ox,y+h+oy),(x+w,y+h)],scol+(a,))
    nx,ny=cells
    for i in range(nx):
        for j in range(ny):
            c=tex_color(base,i,j,22,seed)
            d.R(x+i*w/nx,y+j*h/ny,x+(i+1)*w/nx+.4,y+(j+1)*h/ny+.4,c+(a,),0)
    if face:
        for j,row in enumerate(face[0]):
            for i,ch in enumerate(row):
                if ch!='.' : 
                    d.R(x+i*w/len(row),y+j*h/len(face[0]),x+(i+1)*w/len(row)+.4,y+(j+1)*h/len(face[0])+.4,face[1][ch]+(a,),0)
    d.L(x,y,x+w,y,(255,255,255,30),1.2)
CF=["........","........","..XX.XX.","..XX.XX.","...XX...","..XXXX..","..XXXX..","..X..X.."]
PF=["........","........","..E..E..","........","........","........","........","........"]
GRN=(78,178,64); PINK=(244,160,170)
def lerpc(a,b,t): return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))
def creature(d,cx,gy,sc,t,u,flash=0.0,walk=0.0,stretch=1.0):
    """t=0 cerdo (cuerpo 10x8x16), t=1 creeper con la skin real (cuerpo 8x12x4, patas 4x6x4). Cabeza 8x8x8"""
    col=lerpc((240,162,166),(76,172,62),t)
    if flash>0: col=lerpc(col,(255,255,255),flash)
    legh=6*sc*stretch; bw=(10+(8-10)*t)*sc; bh=(8+(12-8)*t)*sc*stretch; bd=(16+(4-16)*t)*sc
    ld=4*sc; hw=8*sc
    sw=math.sin(walk)*1.6*sc
    kc=clamp((t-.35)/.3); kp=1-kc
    hy_pig=gy-legh-hw*1.12; hy_cr=gy-legh-bh-hw; hy=hy_pig+(hy_cr-hy_pig)*t
    shadow(d,cx+6*sc,gy+4,max(bw,bd)*.8,5*sc,70)
    fl=1.0+flash*1.6
    legs=[(-bw/2,sw,True),(bw/2-ld,-sw,True),(-bw/2,-sw,False),(bw/2-ld,sw,False)]
    if kp>0.01:
        for k,(dx,off,back) in enumerate(legs):
            pc=tuple(int(c*(.8 if back else 1)) for c in col); box(d,cx+dx,gy-legh-off*.15,ld,legh+off*.15,ld,pc,(2,3),seed=k+3,a=int(255*kp))
        box(d,cx-bw/2,gy-legh-bh,bw,bh,bd,col,(max(4,int(bw/sc)),max(4,int(bh/sc))),seed=11,a=int(255*kp))
        box(d,cx-hw/2,hy,hw,hw,hw,col,(8,8),seed=7,face=(PF,{'E':(34,24,30)}),a=int(255*kp))
        box(d,cx-hw*.25,hy+hw*.52,hw*.5,hw*.32,hw*.18,(250,196,204),(4,3),seed=2,a=int(255*kp))
    if kc>0.01:
        A=int(255*kc)
        for k,(dx,off,back) in enumerate(legs):
            tbox(d,cx+dx,gy-legh-off*.15,ld,legh+off*.15,ld,CRT["leg"],A,dark=(.82 if back else 1.0)*fl)
        tbox(d,cx-bw/2,gy-legh-bh,bw,bh,bd,CRT["body"],A,dark=fl)
        tbox(d,cx-hw/2,hy,hw,hw,hw,CRT["head"],A,dark=fl)
    return hy
def sky(d,u,top=(110,170,255),bot=(200,230,255),sun=True):
    pass
def landscape(d,u,horizon=520,night=False):
    for k in range(2): pass
    # nubes de bloques
    for k,(x,y,w) in enumerate([(60,100,4),(260,150,5),(430,70,3)]):
        xx=(x+u*10*(k+1))%640-90
        for i in range(w): d.R(xx+i*36,y,xx+i*36+36,y+26,(255,255,255,235),0)
        for i in range(w-2): d.R(xx+36+i*36,y-26,xx+36+i*36+36,y,(255,255,255,235),0)
    if not night:
        d.R(400,200,468,268,(255,240,150),0); d.R(392,192,476,276,(255,240,150,60),0)
    # colinas de voxels (columnas)
    for i in range(18):
        h=70+int(60*math.sin(i*.6+1)+rnd(i)*50)//1
        for j in range(int(h/18)): d.R(i*34-10,horizon-j*18-18,i*34+24,horizon-j*18,tex_color((70,150,60) if j==int(h/18)-1 else (100,84,60),i,j,16,3)+(255,),0)
def tree(d,x,gy):
    for j in range(5): box(d,x,gy-(j+1)*26,26,26,18,(104,78,52),(3,3),seed=j)
    for (dx,dy,w) in [(-52,-190,130),(-26,-240,78)]:
        box(d,x+dx,gy+dy,w,52,18,(56,142,60),(int(w/16),3),seed=4)
def ground(d,gy,u,rows=5):
    d.R(0,gy,540,960,(104,84,58))
    for r in range(rows):
        y=gy+r*(960-gy)/rows
        h=(960-gy)/rows
        for i in range(0,540,54):
            c=tex_color((84,170,64) if r==0 else (116,92,62) if r>0 else (84,170,64),i//54,r,18,9)
            d.R(i,y,i+54,y+h,c+(255,),0)
            d.L(i,y,i+54,y,(0,0,0,24),1.5)
    d.R(0,gy,540,gy+14,(98,200,76)); 
def dust(d,u,n=24,col=(255,255,255)):
    for k in range(n):
        x=(rnd(k,2)*540+u*8*(k%3+1))%540; y=(rnd(k,3)*960-u*12*(k%2+1))%960; d.R(x,y,x+3,y+3,col+(80,),0)
def person_blocky(d,cx,gy,v,u,walk=0.0,dirn=1):
    sw=math.sin(walk)*1.2*v
    shadow(d,cx,gy+4,9*v,5*v,70)
    tbox(d,cx-4*v,gy-12*v-abs(sw)*.2,4*v,12*v,4*v,STV["legL"]); tbox(d,cx,gy-12*v-abs(sw)*.2,4*v,12*v,4*v,STV["legR"])
    tbox(d,cx-4*v,gy-24*v,8*v,12*v,4*v,STV["body"])
    tbox(d,cx-8*v,gy-24*v-sw*.3,4*v,12*v,4*v,STV["armL"]); tbox(d,cx+4*v,gy-24*v+sw*.3,4*v,12*v,4*v,STV["armR"])
    tbox(d,cx-4*v,gy-32*v,8*v,8*v,8*v,STV["head"])
def sceneA(u,final=False):
    im=new((110,170,255),(200,230,255)); d=D(im)
    landscape(d,u,540)
    tree(d,90,640); tree(d,430,650)
    ground(d,620,u)
    z=1+.05*math.sin(u)
    walk=u*4
    cx=290+math.sin(u*.6)*10
    sc=8.0+.6*sm(u/4)
    creature(d,cx,810,sc,1.0,u,walk=walk)
    # siseo: ondas
    for k in range(3):
        ph=(u*.8+k*.33)%1; d.A(cx,590,90+ph*110,90+ph*110,200,340,(255,255,255,int(160*(1-ph))),3)
    dust(d,u)
    return im
def sceneB(u):
    im=new((60,50,86),(26,22,52)); d=D(im)
    # ventana con noche y luna cuadrada
    bevel(d,40,60,260,260,(70,56,70),10); d.R(52,72,248,248,(20,24,70))
    stars(d,u,30,240); d.R(190,92,220,122,(250,244,220))
    d.R(0,300,540,960,(36,28,52)); d.R(0,300,540,306,(255,255,255,18))
    # cartel con boceto del cerdo
    d.R(300,90,500,250,(248,244,230),3); 
    creature(d,400,232,3.2,0.0,u)
    for k in range(4): d.L(310+k*8,100,310+k*8,104,(0,0,0,60),2)
    bevel(d,30,700,510,760,(112,76,52),6); d.R(50,760,72,900,(82,56,40),3); d.R(470,760,492,900,(82,56,40),3)
    box_=crt(d,140,440,260,220,(10,16,30),(70,66,84))
    # el monitor muestra al cerdo en 3D girando
    x0,y0,x1,y1=box_
    d.R(x0,y0,x1,y1,(40,48,88)); 
    for k in range(10): d.L(x0,y0+k*22+120,x1,y0+k*22+120,(255,255,255,20),1)
    creature(d,(x0+x1)/2,y1-30,3.4,0.0,u,walk=u*3)
    crt_fx(d,box_)
    keyboard(d,180,690,170,36); mug(d,420,660,u,(240,240,250))
    person_back(d,270,690,1.3,0,u)
    return im
def sceneC(u):
    im=new((18,20,44),(34,24,70)); d=D(im)
    # editor 3D
    bevel(d,20,80,520,880,(32,34,64),16); d.R(34,94,506,866,(12,14,36),10)
    d.R(34,94,506,150,(24,26,56),10); 
    for k,c in enumerate([(255,90,90),(255,200,70),(90,220,110)]): d.E(60+k*26,122,7,7,c)
    # rejilla de piso
    for k in range(14): d.L(60,640+k*10,480,640+k*10,(255,255,255,16),1)
    for k in range(10): d.L(60+k*47,640,60+k*47-20,780,(255,255,255,16),1)
    t=sm((u-1.0)/3.6)
    cx=270; creature(d,cx,700,8.4,t,u,walk=0)
    # reglas de medida: altura/ancho (el error)
    legh=(4+(6-4)*t)*8.4; bh=(9+(14-9)*t)*8.4; bw=(11+(8-11)*t)*8.4
    top=700-legh-bh-8*8.4
    d.L(120,700,120,top,(255,255,255,160),3); d.L(112,top,128,top,(255,255,255,200),3); d.L(112,700,128,700,(255,255,255,200),3)
    d.L(cx-bw/2,740,cx+bw/2,740,(255,255,255,160),3); d.L(cx-bw/2,732,cx-bw/2,748,(255,255,255,200),3); d.L(cx+bw/2,732,cx+bw/2,748,(255,255,255,200),3)
    # deslizadores
    for k,(lab,val) in enumerate([("alto",t),("ancho",1-t)]):
        y=820+k*0; x0=60+k*230; d.R(x0,y,x0+190,y+10,(60,64,110),5); d.R(x0,y,x0+190*val,y+10,(255,200,70),5); d.E(x0+190*val,y+5,12,12,(255,255,255))
    return im
def sceneD(u):
    im=new((80,50,100),(30,24,60)); d=D(im)
    for k in range(7): d.E(50+k*74,60+math.sin(u*3+k)*6,8,8,(255,220,120,120))
    floor(d,720)
    # pedestales: cerdo y creeper
    for x,t in((150,0.0),(390,1.0)):
        bevel(d,x-80,740,x+80,780,(90,84,120),6); d.R(x-80,740,x+80,746,(255,255,255,30),6)
        creature(d,x,740,4.2,t,u,walk=math.sin(u*2)*0.0)
    # interrogaciones sobre el cerdo
    for k in range(3): 
        a=(u*.7+k*.33)%1; d.A(150+k*14-14,420-a*80,10,10,0,360,(255,255,255,int(200*(1-a))),2)
    person_front(d,270,480,1.0,0,u,False) if False else None
    bubble(d,60,200,420,84,270,300,int(255*sm((u-.3)/.4)))
    pxq_x=240
    # signo de interrogacion tipo bloque
    for r,row in enumerate(["..XXX..","XX...XX","....XX.","...XX..","...X...",".......","...X..."]):
        for c,ch in enumerate(row):
            if ch=='X': d.R(pxq_x+c*9,214+r*9,pxq_x+c*9+9,214+r*9+9,(255,200,70),0)
    return im
def sceneE(u):
    im=new((110,170,255),(200,230,255)); d=D(im)
    landscape(d,u,500); tree(d,70,610)
    ground(d,600,u)
    # crater (se elimina el terreno)
    boomt=u-4.0
    px=110+ (330*sm(clamp(u/1.6))*0)  # jugador quieto observando y luego se retira
    pxx=130-max(0,u-3.3)*90
    person_blocky(d,pxx,800,4.8,u,walk=(u*6 if (u<1.4 or u>3.3) else 0))
    # creeper se acerca
    x=430-clamp(u/3.0)*190 if u<3.0 else 240
    walk=u*5 if u<3.0 else 0
    fl=0
    if 3.0<=u<4.0: fl=(math.sin((u-3.0)*18)*.5+.5); sw=1+.25*clamp((u-3.0)/1.0)
    else: sw=1
    if u<4.0: creature(d,x,800,4.8*sw,1.0,u,flash=fl,walk=walk,stretch=sw)
    # crater: hueco oscuro en el suelo
    if u>=4.0:
        k=clamp(boomt/.3); d.E(x,800,150*k,34*k,(54,40,28)); d.E(x,800,100*k,22*k,(34,26,18))
        # escombros con gravedad y rebote
        for i in range(36):
            a=-math.pi*(.1+.8*rnd(i,1)); v=240+rnd(i,2)*340; vx=math.cos(a)*v*(1 if rnd(i,3)>.5 else -1); vy=math.sin(a)*v
            t=boomt; xx=x+vx*t*.5; yy=800+vy*t+520*t*t
            if yy>800: yy=800-abs(yy-800)*.35; 
            s_=10+rnd(i,4)*16; col=[(104,84,58),(84,170,64),(70,150,60),(128,100,70)][i%4]
            if boomt<2.4: box(d,xx,yy-s_,s_,s_,s_*.8,col,(2,2),seed=i)
        if boomt<.14: d.R(0,0,540,960,(255,255,255,int(255*(1-boomt/.14))))
        # destello y humo
        if boomt<.35: d.E(x,760,260*boomt/.35,260*boomt/.35,(255,240,160,int(220*(1-boomt/.35))))
        for i in range(14):
            a=clamp(boomt/2.2); sx=x+(rnd(i,5)-.5)*220*a; sy=770-a*170*(.4+rnd(i,6)); rr=22+a*40
            d.E(sx,sy,rr,rr,(240,240,240,int(170*(1-a))))
    dust(d,u,14)
    return im
def sceneF(u):
    im=new((8,14,12),(18,36,28)); d=D(im)
    # cueva con antorcha
    for r in range(8):
        for c in range(6): d.R(c*90,r*128,c*90+90,r*128+128,tex_color((46,54,50),c,r,18,2)+(255,),0)
    fl=.75+.25*math.sin(u*14)+.1*math.sin(u*31)
    d.E(90,300,240*fl,240*fl,(255,170,60,40)); d.E(90,300,120*fl,120*fl,(255,190,80,60))
    d.R(84,300,96,400,(104,78,52)); d.P([(90,250*1.0),(76,300),(104,300)],(255,140,40)); d.P([(90,265),(82,298),(98,298)],(255,230,120))
    # primer plano: cara del creeper a gran tamano
    z=1.0+.1*sm(u/5)
    cx,cy=330,500; s=24*z
    hw=8*s
    shadow(d,cx,cy+hw/2+40,hw*.55,20,80)
    tbox(d,cx-hw/2,cy-hw/2,hw,hw,hw*.6,CRT["head"])
    # silbido: ondas y chispas
    for k in range(4):
        ph=(u*1.2+k*.25)%1; d.A(cx,cy,hw*.6+ph*160,hw*.6+ph*160,200,340,(220,255,220,int(150*(1-ph))),4)
    for k in range(30):
        a=rnd(k)*6.28; r=hw*.55+((u*60+k*13)%140); d.R(cx+math.cos(a)*r,cy+math.sin(a)*r,cx+math.cos(a)*r+5,cy+math.sin(a)*r+5,(200,255,200,int(180*(1-(r-hw*.55)/140))),0)
    dust(d,u,20,(255,230,190))
    return im
def sceneG(u):
    im=new((40,10,60),(14,6,34)); d=D(im); stars(d,u,70,960)
    for k in range(16):
        a=k*math.pi/8+u*.4; d.P([(270,420),(270+math.cos(a-.07)*800,420+math.sin(a-.07)*800),(270+math.cos(a+.07)*800,420+math.sin(a+.07)*800)],(120,255,140,12))
    b=sm(u/.8)
    creature(d,330,760,8.2*b,1.0,u)
    creature(d,110,760,3.2,0.0,u)
    # regla con marca de medida
    d.R(40,820,500,832,(240,220,160),2)
    for k in range(24): d.R(48+k*19,832 if k%2 else 832,50+k*19,832+(14 if k%4==0 else 8),(60,40,20),0)
    d.E(430,150,60,60,(60,200,100)); d.L(404,152,424,174,(255,255,255),10); d.L(424,174,458,132,(255,255,255),10)
    for k in range(30):
        a=k*.21; t=(u*.5+rnd(k,4))%1; x=(rnd(k,6))*540; y=-20+t*980; d.R(x,y,x+8,y+8,[(120,255,140),(255,220,80),(255,255,255)][k%3]+(220,),0)
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx==0: return 1.0+.25*sm(p),270,560-60*sm(p)
    if idx==1: return 1.0+.45*sm(p),300-20*sm(p),520-50*sm(p)
    if idx==2: return 1.2-.12*sm(p),270,480
    if idx==3: return 1.3-.2*sm(p),150+120*sm(p),600
    if idx==4:
        sh=max(0,1-(u-4.0)/.9) if u>=4.0 else 0
        return 1.0+.1*sm(p)+.12*sh,270+(30 if u>4 else 0)+math.sin(u*70)*14*sh,600+math.cos(u*55)*14*sh
    if idx==5: return 1.0+.1*sm(p),300,480
    if idx==6: return 1.3-.3*sm(clamp(u/3)),270,560-80*sm(clamp(u/3))
    return 1.15-.15*sm(p),270,560
core.CAM=cam
if __name__=="__main__": core.main()
