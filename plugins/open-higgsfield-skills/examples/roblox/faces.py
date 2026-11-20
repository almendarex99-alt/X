from PIL import Image, ImageDraw, ImageFont
import os
os.makedirs("faces",exist_ok=True); os.makedirs("tex",exist_ok=True)
N=512; B=(25,20,25,255); W=(255,255,255,255); C=N//2
AN=[0]
def eyes_open(d,y=190,r=34,dx=105):
    if AN[0]: r=48
    for s in(-1,1):
        if AN[0]:
            d.ellipse([C+s*dx-r,y-r*1.3,C+s*dx+r,y+r*1.3],fill=(38,24,46,255)); d.ellipse([C+s*dx-r*.55,y-r*.95,C+s*dx+r*.05,y-r*.25],fill=W); d.ellipse([C+s*dx+r*.1,y+r*.35,C+s*dx+r*.45,y+r*.7],fill=(255,255,255,210))
        else:
            d.ellipse([C+s*dx-r,y-r*1.25,C+s*dx+r,y+r*1.25],fill=B); d.ellipse([C+s*dx-r*.35+4,y-r*.8,C+s*dx+r*.25+4,y-r*.2],fill=W)
def smile(d): eyes_open(d); d.arc([C-110,250,C+110,400],20,160,fill=B,width=20)
def grin(d):
    eyes_open(d); d.pieslice([C-120,250,C+120,420],0,180,fill=B); d.pieslice([C-95,250,C+95,300],0,180,fill=W); d.ellipse([C-45,350,C+45,400],fill=(210,80,90,255))
def shock(d):
    for s in(-1,1):
        d.ellipse([C+s*105-52,140,C+s*105+52,250],fill=W,outline=B,width=10); d.ellipse([C+s*105-14,175,C+s*105+14,215],fill=B)
        d.line([C+s*105-55,110,C+s*105+55,95-s*10],fill=B,width=14)
    d.ellipse([C-45,300,C+45,420],fill=B)
def angry(d):
    eyes_open(d,200,28); d.line([C-150,120,C-50,165],fill=B,width=24); d.line([C+150,120,C+50,165],fill=B,width=24); d.arc([C-100,320,C+100,430],200,340,fill=B,width=20)
def smug(d):
    for s in(-1,1): d.arc([C+s*105-45,150,C+s*105+45,230],200,340,fill=B,width=18); d.chord([C+s*105-45,185,C+s*105+45,230],180,360,fill=B)
    d.line([C-90,300,C+50,300],fill=B,width=18); d.arc([C-20,260,C+130,350],0,90,fill=B,width=18)
def worry(d):
    eyes_open(d,200); d.line([C-150,140,C-55,115],fill=B,width=14); d.line([C+150,140,C+55,115],fill=B,width=14); d.arc([C-90,330,C+90,420],200,340,fill=B,width=20)
def closed(d):
    for s in(-1,1): d.arc([C+s*105-50,160,C+s*105+50,260],20,160,fill=B,width=18)
    d.arc([C-90,330,C+90,420],200,340,fill=B,width=20)
EX=dict(smile=smile,grin=grin,shock=shock,angry=angry,smug=smug,worry=worry,closed=closed)
KITS={
 "Tito":dict(glasses=2,blush=1),
 "Lola":dict(anime=1,blush=1),
 "Max":dict(blush=1,brow=1),
 "Profe":dict(mustache=1,glasses=1,bags=1),
}
def overlay(d,k):
    if k.get("blush"):
        for s in(-1,1): d.ellipse([C+s*165-38,255,C+s*165+38,300],fill=(255,110,140,150))
    if k.get("lashes"):
        for s in(-1,1):
            for a in(-1,0,1): d.line([C+s*105+s*30,170,C+s*105+s*(52+a*8),150+a*14],fill=B,width=9)
    if k.get("freckles"):
        import random; r=random.Random(3)
        for s in(-1,1):
            for _ in range(6): x=C+s*(120+r.randint(-20,40)); y=250+r.randint(-8,30); d.ellipse([x-5,y-5,x+5,y+5],fill=(150,80,50,230))
    if k.get("bags"):
        for s in(-1,1): d.arc([C+s*105-45,215,C+s*105+45,260],20,160,fill=(120,90,80,200),width=7)
    if k.get("mustache"):
        d.pieslice([C-95,262,C,320],180,360,fill=(130,130,135,255)); d.pieslice([C,262,C+95,320],180,360,fill=(130,130,135,255))
    if k.get("glasses")==2:
        for s in(-1,1): d.ellipse([C+s*105-66,120,C+s*105+66,260],outline=(15,15,20,255),width=11)
        d.line([C-40,185,C+40,185],fill=(15,15,20,255),width=10)
    elif k.get("glasses"):
        for s in(-1,1): d.ellipse([C+s*105-62,125,C+s*105+62,255],outline=(40,40,50,255),width=12); d.ellipse([C+s*105-62,125,C+s*105+62,255],fill=(190,230,255,45))
        d.line([C-45,185,C+45,185],fill=(40,40,50,255),width=12)
for ch,k in KITS.items():
    AN[0]=k.get('anime',0)
    for n,f in EX.items():
        im=Image.new("RGBA",(N,N),(0,0,0,0)); d=ImageDraw.Draw(im); f(d); overlay(d,k); im.save(f"faces/{ch}_{n}.png")
# ---- texturas de ropa (torso 2x2) ----
def tex(name,fn):
    im=Image.new("RGBA",(N,N),(0,0,0,0)); d=ImageDraw.Draw(im); fn(d); im.save(f"tex/{name}.png")
fb=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",190)
def heart(d,cx,cy,s,c):
    d.ellipse([cx-s,cy-s,cx,cy],fill=c); d.ellipse([cx,cy-s,cx+s,cy],fill=c); d.polygon([(cx-s,cy-s*.35),(cx+s,cy-s*.35),(cx,cy+s*1.05)],fill=c)
def lola(d):
    d.ellipse([C-120,-60,C+120,70],fill=(215,60,125,255))                       # capucha
    d.ellipse([C-90,-30,C+90,50],fill=(255,150,195,255))
    for x in(-45,45): d.line([C+x,50,C+x*1.1,170],fill=W,width=12); d.ellipse([C+x*1.1-10,165,C+x*1.1+10,190],fill=W)
    heart(d,C,260,60,(255,255,255,255)); heart(d,C,262,42,(230,40,100,255))
    d.rounded_rectangle([C-130,340,C+130,440],radius=22,outline=(215,60,125,255),width=8,fill=(255,100,160,255))
    d.rectangle([0,470,N,N],fill=(215,60,125,255))
def max_(d):
    d.rectangle([0,185,N,325],fill=(255,255,255,255)); d.rectangle([0,205,N,225],fill=(30,58,138,255)); d.rectangle([0,285,N,305],fill=(30,58,138,255))
    d.text((C,255),"7",font=fb,fill=(220,60,20,255),anchor="mm")
    d.pieslice([C-95,-60,C+95,110],0,180,fill=(255,255,255,255)); d.pieslice([C-65,-60,C+65,75],0,180,fill=(240,150,70,255)) 
    d.rectangle([0,465,N,N],fill=(30,58,138,255)); d.rectangle([C-26,470,C+26,N-4],fill=(250,200,40,255)); d.rectangle([C-14,482,C+14,N-18],fill=(30,58,138,255))
def profe(d):
    d.polygon([(0,0),(150,0),(C,330),(N-150,0),(N,0),(N,N),(0,N)],fill=(30,130,70,255))     # chaleco verde
    d.polygon([(150,0),(C,330),(C-50,0)],fill=(255,255,255,255)); d.polygon([(N-150,0),(C,330),(C+50,0)],fill=(255,255,255,255))   # cuello camisa
    d.polygon([(C-26,40),(C+26,40),(C+34,300),(C,370),(C-34,300)],fill=(210,35,45,255)); d.polygon([(C-26,40),(C+26,40),(C+16,85),(C-16,85)],fill=(150,20,30,255))   # corbata
    for y in(340,400): d.ellipse([C-9,y,C+9,y+18],fill=(240,240,240,255))
    d.rounded_rectangle([60,300,150,380],radius=6,fill=(25,110,60,255),outline=(15,80,40,255),width=5)
    for x,c in((80,(30,60,200,255)),(104,(200,30,30,255)),(128,(20,20,20,255))): d.rectangle([x,265,x+10,320],fill=c)
    d.rectangle([0,470,N,N],fill=(60,45,35,255)); d.rectangle([C-34,474,C+34,N-4],fill=(250,200,40,255)); d.rectangle([C-20,486,C+20,N-18],fill=(60,45,35,255))
def tito(d):
    pts=[]; import math
    for i in range(10): a=-math.pi/2+i*math.pi/5; r=70 if i%2==0 else 30; pts.append((380+r*math.cos(a),150+r*math.sin(a)))
    d.polygon(pts,fill=(250,200,40,255),outline=(160,110,10,255)); d.rectangle([0,470,N,N],fill=(25,70,150,255))
def lola2(d):
    d.polygon([(0,0),(110,0),(160,60),(C,95),(N-160,60),(N-110,0),(N,0),(N,N),(0,N)],fill=(255,255,255,0))
    d.rectangle([108,0,190,N],fill=(28,24,34,255)); d.rectangle([N-190,0,N-108,N],fill=(28,24,34,255))     # tirantes
    d.polygon([(108,200),(N-108,200),(N-90,N),(90,N)],fill=(28,24,34,255))                                    # peto negro
    for y in range(230,480,60): d.rectangle([C-8,y,C+8,y+34],fill=(255,255,255,255))
    heart(d,C,330,26,(255,150,190,255))
    for x in(150,N-150):
        for y in range(215,470,40): d.line([x-10,y,x+10,y+14],fill=(255,255,255,255),width=6)
    d.polygon([(C,70),(C-85,20),(C-85,115)],fill=(20,18,24,255)); d.polygon([(C,70),(C+85,20),(C+85,115)],fill=(20,18,24,255)); d.ellipse([C-24,45,C+24,95],fill=(40,36,46,255))   # lazo cuello
    d.rectangle([0,478,N,N],fill=(255,255,255,255))
def tito2(d):
    d.polygon([(70,0),(190,0),(C,150),(N-190,0),(N-70,0),(C,230)],fill=(235,235,240,255)); d.polygon([(190,0),(C,150),(C-30,0)],fill=(255,255,255,255))
    d.polygon([(C-22,30),(C+22,30),(C+30,330),(C,380),(C-30,330)],fill=(20,20,26,255)); d.ellipse([C-14,10,C+14,40],fill=(20,20,26,255)); d.rectangle([C-5,200,C+5,240],fill=(235,235,240,255))
    d.rectangle([108,0,150,N],fill=(22,22,28,255)); d.rectangle([N-150,0,N-108,N],fill=(22,22,28,255))
    for x in(129,N-129): d.rectangle([x-12,430,x+12,455],fill=(150,150,160,255))
    d.rounded_rectangle([N-175,255,N-95,330],radius=6,outline=(190,190,200,255),width=4); d.rectangle([0,478,N,N],fill=(20,20,24,255)); d.rectangle([C-26,482,C+26,N-4],fill=(200,200,205,255))
def max2(d):
    d.polygon([(130,0),(N-130,0),(C,260)],fill=(244,205,160,255))                                            # V de piel
    d.polygon([(0,0),(130,0),(C,260),(C-10,N),(0,N)],fill=(238,226,205,255)); d.polygon([(N-130,0),(N,0),(N,N),(C+10,N),(C,260)],fill=(238,226,205,255))
    d.line([130,0,C,260],fill=(200,186,160,255),width=6); d.line([N-130,0,C,260],fill=(200,186,160,255),width=6)
    for x,s in((C-60,-1),(C+60,1)): d.line([x,60,x+s*20,300],fill=(150,150,158,255),width=10); d.ellipse([x+s*20-10,295,x+s*20+10,325],fill=(120,120,128,255))
    for y in(300,360,420): d.ellipse([C-8,y,C+8,y+16],fill=(190,176,150,255))
    d.rectangle([0,470,N,N],fill=(50,50,56,255)); d.rectangle([C-26,474,C+26,N-4],fill=(190,190,200,255))
tex("Lola",lola2); tex("Max",max2); tex("Profe",profe); tex("Tito",tito2)
for nm,fn in(("bow",None),):
    im=Image.new("RGBA",(256,256),(0,0,0,0)); dd=ImageDraw.Draw(im); dd.polygon([(128,128),(30,70),(30,186)],fill=(15,15,20,255)); dd.polygon([(128,128),(226,70),(226,186)],fill=(15,15,20,255)); dd.ellipse([108,108,148,148],fill=(35,35,45,255)); im.save("tex/bow.png")
