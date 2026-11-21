import sys; sys.path.insert(0,"..")
from art import *
from common import tv
G=[(224,248,208),(136,192,112),(52,104,86),(8,24,32)]   # paleta de la Game Boy
def gb_box(d,x,y,w,h):
    d.R(x,y,x+w,y+h,G[0]+(255,),0); d.R(x,y,x+w,y+h,None,0,G[3]+(255,),5)
def glitch_sprite(d,x,y,cell,u,seed=0,scramble=1.0):
    """bloque tipo MissingNo.: columna de teselas mezcladas"""
    w,h=6,14
    for r in range(h):
        for c in range(w):
            k=(r*7+c*13+seed)%11; sh=((r*3+c*5+int(u*10*scramble)*(1 if (r+c)%3==0 else 0))%4)
            if (r*w+c+seed)%5==0 and scramble>0: sh=int(rnd(r*w+c,int(u*6))*4)%4
            if c==0 and r>10: continue
            d.R(x+c*cell,y+r*cell,x+c*cell+cell,y+r*cell+cell,G[sh]+(255,),0)
def creature(d,x,y,cell):
    pat=["..####..",".######.","##.##.##","########","##.##.##",".######.","..#..#..",".##..##."]
    for r,row in enumerate(pat):
        for c,ch in enumerate(row):
            if ch=="#": d.R(x+c*cell,y+r*cell,x+c*cell+cell,y+r*cell+cell,G[3]+(255,),0)
def battle(d,u,txt="A WILD MISSINGNO. APPEARED!"):
    d.R(0,0,540,960,G[0]+(255,),0)
    glitch_sprite(d,300,120,18,u); d.R(40,230,230,250,G[2]+(255,),0); d.R(300,370,510,390,G[2]+(255,),0)
    # jugador de espaldas (silueta de pixeles)
    for r in range(8):
        for c in range(7): d.R(60+c*20,360+r*20,80+c*20,380+r*20,G[3]+(255,),0) if (r+c)%3 else None
    d.R(40,600,500,800,G[0]+(255,),0); d.R(40,600,500,800,None,0,G[3]+(255,),8); d.R(52,612,488,788,None,0,G[3]+(255,),3)
    ptext(d,70,640,txt[:18],4.0,G[3]); ptext(d,70,700,txt[18:],4.0,G[3])
def sceneA(u,final=False):
    im=new(G[0],G[0]); d=D(im); battle(d,u)
    return im
def sceneB(u):
    im=new((30,34,26),(60,70,50)); d=D(im)
    d.R(0,700,540,960,(40,48,34)); d.R(0,700,540,706,(255,255,255,24))
    # Game Boy y dos cartuchos (rojo/verde en Japon, rojo/azul fuera)
    shadow(d,270,880,150,12,80)
    bevel(d,150,420,390,820,(196,196,188),20); d.R(172,444,368,610,(80,80,100),14); d.R(190,462,350,590,G[1]+(255,),4)
    d.E(212,690,22,22,(180,40,90)); d.E(286,670,22,22,(180,40,90)); d.R(190,700,210,740,(40,40,52),3); d.R(180,712,220,728,(40,40,52),3)
    for k,(x,c,n) in enumerate([(30,(210,50,50),"RED"),(130,(60,160,90),"GREEN")]): d.R(x,150,x+90,300,(120,120,128),6); d.R(x+10,166,x+80,240,c,4); ptext(d,x+12,252,n,3.2,(255,255,255))
    for k,(x,c,n) in enumerate([(320,(210,50,50),"RED"),(420,(60,100,220),"BLUE")]): d.R(x,150,x+90,300,(120,120,128),6); d.R(x+10,166,x+80,240,c,4); ptext(d,x+12,252,n,3.2,(255,255,255))
    ptext(d,40,330,"JAPON",3.4,(255,255,255)); ptext(d,320,330,"MUNDO",3.4,(255,255,255)); ptext(d,200,90,"1996",6.0,(255,255,255))
    return im
def sceneC(u):
    im=new((70,140,200),(120,190,230)); d=D(im)
    # mapa simplificado: ciudad Verde arriba, isla en la esquina inferior con costa
    d.R(0,0,540,960,(70,140,200),0)
    d.P([(40,80),(420,60),(500,320),(380,520),(60,480)],(120,190,110)); d.R(150,120,230,180,(170,170,160),3)
    d.P([(300,620),(480,610),(500,820),(260,830)],(120,190,110)); d.R(380,700,430,750,(200,90,60),3)
    ptext(d,100,100,"VIRIDIAN",3.0,(20,20,20)); ptext(d,300,650,"CINNABAR",3.0,(20,20,20))
    step=int(clamp(u/5.0)*3)
    for k,(x,y,t) in enumerate([(190,150,"1"),(260,380,"2"),(520,720,"3")]):
        on=k<=step
        d.E(x,y,24,24,(255,230,90) if on else (255,255,255,160)); ptext(d,x-6,y-8,t,3.0,(20,20,20))
    d.L(190,150,260,380,(255,255,255,200),5); d.L(260,380,420,700,(255,255,255,200),5)
    # jugador surfeando junto a la costa
    sx=lerp(300,470,sm(u/5.0)); d.E(sx,770,16,12,(255,240,200)); d.R(sx-26,782,sx+26,792,(240,240,255),6)
    return im
def sceneD(u):
    im=new(G[0],G[0]); d=D(im)
    d.R(0,0,540,960,G[0]+(255,),0)
    ptext(d,60,60,"POKEDEX",5.0,G[3]); 
    for k in range(8):
        n=[1,2,3,0,4,5,6,7][k]
        ptext(d,60,150+k*52,"NO."+str(n).zfill(3) if n!=0 else "NO.000",3.6,G[3]); 
        d.R(280,150+k*52,480,154+k*52,G[2]+(255,),0)
    d.R(60,150+3*52-6,490,150+4*52-6,None,0,G[3]+(255,),4)
    glitch_sprite(d,380,580,16,u,scramble=.6)
    ptext(d,60,860,"MISSINGNO.",5.0,G[3])
    return im
def sceneE(u):
    im=new(G[0],G[0]); d=D(im)
    d.R(0,0,540,960,G[0]+(255,),0)
    sc=clamp(u/5.0)
    cell=22
    # criatura normal cuyas teselas se mezclan poco a poco
    for r in range(8):
        for c in range(8):
            pat=["..####..",".######.","##.##.##","########","##.##.##",".######.","..#..#..",".##..##."]
            ch=pat[r][c]
            rr,cc=r,c
            if rnd(r*8+c,3)<sc:
                rr=int(rnd(r*8+c,int(u*3)+1)*8)%8; cc=int(rnd(r*8+c,int(u*3)+7)*8)%8; ch=pat[rr][cc]
            if ch=="#": d.R(110+c*cell*2.2,200+r*cell*2.2,110+c*cell*2.2+cell*2.2,200+r*cell*2.2+cell*2.2,G[3]+(255,),0)
            elif rnd(r*8+c,9)<sc*.5: d.R(110+c*cell*2.2,200+r*cell*2.2,110+c*cell*2.2+cell*2.2,200+r*cell*2.2+cell*2.2,G[2]+(255,),0)
    ptext(d,60,60,"LOS PIXELES",4.0,G[3]); ptext(d,60,760,"SE MEZCLAN",4.0,G[3])
    return im
def sceneF(u):
    im=new(G[0],G[0]); d=D(im)
    d.R(0,0,540,960,G[0]+(255,),0)
    d.R(40,120,500,760,G[0]+(255,),0); d.R(40,120,500,760,None,0,G[3]+(255,),8)
    ptext(d,70,150,"ITEMS",5.0,G[3])
    items=["POTION","POKE BALL","ANTIDOTE","ESCAPE ROPE","REPEL","RARE CANDY"]
    for k,n in enumerate(items):
        y=240+k*84; ptext(d,80,y,n,3.4,G[3])
        q=1 if k<5 else 1+int(clamp((u-1.0)/3.0)*127)
        ptext(d,360,y+30,"X"+str(q),3.4,G[3])
    d.P([(60,240+5*84),(60,240+5*84+24),(76,240+5*84+12)],G[3]+(255,))
    d.R(40,800,500,880,None,0,G[3]+(int(255*(abs(math.sin(u*5)))),),5)
    return im
def sceneG(u):
    im=new((130,190,240),(220,240,250)); d=D(im)
    d.R(0,640,540,960,(110,170,90)); d.R(0,640,540,646,(255,255,255,30))
    d.E(430,120,40,40,(255,240,170)); 
    for k in range(12): d.L(k*50,540,k*50,690,(120,120,130),4)
    d.L(0,560,540,560,(120,120,130),6); d.L(0,660,540,660,(120,120,130),6)
    # ninos pasandose una consola de mano
    xs=[90,250,410]
    for i,x in enumerate(xs):
        c=[(220,70,80),(70,120,220),(240,200,70)][i]; silhouette(d,x,780,1.0,c)
        hy=780-96; gx=x+30; d.R(gx,hy,gx+26,hy+36,(196,196,188),4); d.R(gx+4,hy+4,gx+22,hy+20,G[1]+(255,),2)
    t=(u*.5)%2; px=lerp(110,430,sm(t if t<1 else 2-t)); d.R(px,640,px+26,676,(196,196,188),4); d.R(px+4,644,px+22,660,G[1]+(255,),2)
    for k,(x,y) in enumerate([(120,420),(300,360),(440,440)]):
        a=sm((u-.5-k*.8)/.4)
        if a>0: d.R(x,y,x+110,y+60,(255,255,255,int(240*a)),14); ptext(d,x+10,y+18,"MISSINGNO",2.6,(20,20,20),int(255*a))
    return im
core.SCN=[lambda u:sceneA(u),sceneB,sceneC,sceneD,sceneE,sceneF,sceneG,lambda u:sceneA(u,True)]
def cam(idx,u,dur):
    p=clamp(u/max(.01,dur))
    if idx in (0,7): return 1.0,270,480
    return 1.0+.1*sm(p),270,480
core.CAM=cam
if __name__=="__main__": core.main()
