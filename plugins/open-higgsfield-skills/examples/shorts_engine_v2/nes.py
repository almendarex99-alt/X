"""Graficos estilo NES / Game Boy / Atari dibujados con pixeles reales (para las pantallas de los televisores y consolas)."""
import math
from PIL import Image, ImageDraw
from art import F35
SKYC=(92,148,252); BRK=(200,76,12); BRK2=(252,152,56); GRN=(0,168,0); GRN2=(0,88,0); WHT=(252,252,252); CYN=(60,188,252)
SH=["....##....##....","...####..####...","..############..",".##############.","################","################","################",".##############."]
def sprite(d,x,y,fill,outline,sc=2,shade=None):
    for oy,row in enumerate(SH):
        for ox,c in enumerate(row):
            if c=="#":
                for (dx,dy) in((-1,0),(1,0),(0,-1),(0,1)): d.rectangle([x+(ox+dx)*sc,y+(oy+dy)*sc,x+(ox+dx+1)*sc-1,y+(oy+dy+1)*sc-1],fill=outline)
    for oy,row in enumerate(SH):
        for ox,c in enumerate(row):
            if c=="#": d.rectangle([x+ox*sc,y+oy*sc,x+(ox+1)*sc-1,y+(oy+1)*sc-1],fill=fill)
    if shade:
        for ox in (3,4,5,7,8,9,10,11,12): d.rectangle([x+ox*sc,y+6*sc,x+(ox+1)*sc-1,y+7*sc-1],fill=shade)
def text(d,x,y,s,col=WHT,cell=1):
    for i,ch in enumerate(s.upper()):
        for r,row in enumerate(F35.get(ch,F35[" "])):
            for c,v in enumerate(row):
                if v=="#": d.rectangle([x+(i*4+c)*cell,y+r*cell,x+(i*4+c+1)*cell-1,y+(r+1)*cell-1],fill=col)
def level(off=0.0,mode=0.0,u=0.0,hl=0.0):
    """pantalla 256x240 de un nivel: nubes y arbustos usan EL MISMO sprite; mode 0=colores normales, 1=todo nube(blanco), 2=todo arbusto(verde)"""
    im=Image.new("RGB",(256,240),SKYC); d=ImageDraw.Draw(im)
    for (x,y) in((22,40),(116,28),(198,56),(300,36)):
        xx=(x-off*.3)%330-40; c=WHT if mode!=2 else GRN; o=CYN if mode!=2 else GRN2; sprite(d,xx,y,c,o,2,shade=(200,220,252) if mode!=2 else (0,120,0))
    for (x,w,h) in((-16,80,40),(160,60,28),(270,80,40)):
        xx=(x-off)%340-50; d.polygon([(xx,184),(xx+w*.22,184-h*.7),(xx+w*.38,184-h),(xx+w*.62,184-h),(xx+w*.78,184-h*.7),(xx+w,184)],fill=GRN)
        d.polygon([(xx+w*.08,184),(xx+w*.26,184-h*.62),(xx+w*.38,184-h*.85),(xx+w*.3,184)],fill=GRN2)
    for x in(70,190,290):
        xx=(x-off)%340-50; c=GRN if mode!=1 else WHT; o=GRN2 if mode!=1 else CYN; sprite(d,xx,168,c,o,2,shade=(0,120,0) if mode!=1 else (200,220,252))
    qx=(120-off)%340-30; d.rectangle([qx,110,qx+16,126],fill=(252,168,56)); d.rectangle([qx+2,112,qx+14,124],fill=(200,120,20)); text(d,qx+6,114,"?",WHT,2)
    d.rectangle([0,184,255,240],fill=BRK)
    for r in range(4):
        for c in range(-1,18):
            x=c*16+((r%2)*8)-int(off)%16; y=184+r*14
            d.rectangle([x,y,x+15,y+13],fill=BRK); d.line([x,y,x+15,y],fill=BRK2); d.line([x,y,x,y+13],fill=BRK2); d.line([x+15,y,x+15,y+13],fill=(100,30,0)); d.line([x,y+13,x+15,y+13],fill=(100,30,0))
    text(d,16,8,"MARIO",WHT,1); text(d,16,16,"000000",WHT,1); text(d,100,16,"x00",WHT,1); text(d,140,8,"WORLD",WHT,1); text(d,146,16,"1-1",WHT,1); text(d,204,8,"TIME",WHT,1); text(d,208,16,str(max(0,400-int(u*2))).zfill(3),WHT,1)
    # heroe (silueta generica de fontanero: gorra roja, mono azul)
    px=100; py=152+int(math.sin(u*8)*1.5); d.rectangle([px,py,px+11,py+3],fill=(216,40,0)); d.rectangle([px+1,py+4,px+10,py+8],fill=(252,188,152)); d.rectangle([px,py+9,px+11,py+15],fill=(0,88,248)); d.rectangle([px+1,py+16,px+4,py+19],fill=(110,44,0)); d.rectangle([px+7,py+16,px+10,py+19],fill=(110,44,0))
    return im
GB=[(15,56,15),(48,98,48),(139,172,15),(155,188,15)]
def gb_screen(w=160,h=144):
    return Image.new("RGB",(w,h),GB[3])
GBC=[(15,56,15),(48,98,48),(139,172,15),(155,188,15)]
def _gbimg(): return Image.new("RGB",(160,144),GBC[3])
def gb_overworld(u):
    im=_gbimg(); d=ImageDraw.Draw(im)
    for ty in range(9):
        for tx in range(10):
            x=tx*16; y=ty*16; water=(tx<3) or (ty>6 and tx<6)
            if water:
                d.rectangle([x,y,x+15,y+15],fill=GBC[2])
                for k in range(3): d.line([x+1+((k*5+int(u*6))%10),y+3+k*5,x+6+((k*5+int(u*6))%10),y+3+k*5],fill=GBC[1])
            else:
                d.rectangle([x,y,x+15,y+15],fill=GBC[3])
                if (tx+ty)%2: d.rectangle([x+4,y+4,x+5,y+5],fill=GBC[2]); d.rectangle([x+10,y+9,x+11,y+10],fill=GBC[2])
    for (hx,hy) in((70,24),(110,40),(86,70)): d.rectangle([hx,hy,hx+18,hy+14],fill=GBC[1]); d.rectangle([hx+2,hy+2,hx+16,hy+6],fill=GBC[0]); d.rectangle([hx+7,hy+8,hx+11,hy+14],fill=GBC[0])
    d.rectangle([48,0,60,144],fill=GBC[2]); 
    py=int(20+(u*14)%110); d.rectangle([52,py,58,py+9],fill=GBC[0]); d.rectangle([53,py+1,57,py+3],fill=GBC[3])
    d.rectangle([20,60,26,70],fill=GBC[1]); d.rectangle([21,61,25,63],fill=GBC[3])
    d.rectangle([4,108,155,140],fill=GBC[3],outline=GBC[0],width=2); text(d,10,114,"ANCIANO: ",GBC[0],1); text(d,10,124,"TE ENSENO A",GBC[0],1); text(d,10,132,"CAPTURAR?",GBC[0],1)
    return im
def gb_dex(u):
    im=_gbimg(); d=ImageDraw.Draw(im); d.rectangle([0,0,159,16],fill=GBC[0]); text(d,6,6,"POKEDEX",GBC[3],1)
    rows=[1,2,3,0,4,5,6]
    for k,n in enumerate(rows):
        y=22+k*17; sel=(k==3)
        d.rectangle([4,y,155,y+14],fill=GBC[0] if sel else GBC[3],outline=GBC[0]); c=GBC[3] if sel else GBC[0]
        text(d,10,y+5,("NO.%03d"%n) if n else "NO.???",c,1); d.rectangle([80,y+3,88,y+11],fill=c) if n else d.text((82,y+2),"?",fill=c)
    return im
def gb_glitch(u):
    im=_gbimg(); d=ImageDraw.Draw(im); import random
    rnd=random.Random(int(u*8)); cell=6; ox,oy=50,30
    for gy in range(14):
        for gx in range(10):
            v=rnd.random(); c=GBC[0] if v<.34 else GBC[1] if v<.5 else GBC[3] if v<.8 else GBC[2]
            d.rectangle([ox+gx*cell,oy+gy*cell,ox+gx*cell+cell-1,oy+gy*cell+cell-1],fill=c)
    text(d,40,120,"MISSINGNO.",GBC[0],1); d.rectangle([4,4,155,139],outline=GBC[0],width=2)
    return im
def gb_items(u):
    n=min(128,int(1+u*40)); im=_gbimg(); d=ImageDraw.Draw(im); d.rectangle([0,0,159,16],fill=GBC[0]); text(d,6,6,"MOCHILA",GBC[3],1)
    items=[("POCION",5),("BALL",9),("CARAMELO RARO",n),("ANTIDOTO",3)]
    for k,(nm,c) in enumerate(items):
        y=24+k*24; d.rectangle([4,y,155,y+20],outline=GBC[0],fill=GBC[3] if k!=2 else GBC[2]); text(d,10,y+7,nm,GBC[0],1); text(d,116,y+7,"x%d"%c,GBC[0],1)
    return im
