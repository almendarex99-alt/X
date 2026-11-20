import bpy, math, json, sys, os, random
random.seed(7)
from mathutils import Vector, Quaternion, Euler
A=sys.argv[sys.argv.index("--")+1:]
OUT=A[0]; F0=int(A[1]); F1=int(A[2]); RES=float(A[3]); SAMP=int(A[4]); STEP=int(A[5]) if len(A)>5 else 1
FPS=24
TL=json.load(open("timeline.json")); S0=[s["start"] for s in TL["scenes"]]; TOTAL=TL["total"]
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene
sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=SAMP; sc.cycles.use_denoising=True
sc.cycles.max_bounces=3; sc.cycles.diffuse_bounces=2; sc.cycles.glossy_bounces=2; sc.cycles.transmission_bounces=2
sc.render.resolution_x=int(540*RES); sc.render.resolution_y=int(960*RES); sc.render.fps=FPS
sc.view_settings.view_transform='Standard'
sc.render.image_settings.file_format='PNG'

# ---------- utilidades ----------
def sm(x): x=max(0,min(1,x)); return x*x*(3-2*x)
def K(t,pts):
    """interpola suave entre claves [(t,valor)] valor numero o tupla"""
    if t<=pts[0][0]: return pts[0][1]
    if t>=pts[-1][0]: return pts[-1][1]
    for (a,va),(b,vb) in zip(pts,pts[1:]):
        if a<=t<=b:
            u=sm((t-a)/(b-a))
            if isinstance(va,(tuple,list)): return tuple(x+(y-x)*u for x,y in zip(va,vb))
            return va+(vb-va)*u
MATS={}
def mat(c,rough=.45,emit=0,alpha=1,name=None):
    k=(c,rough,emit,alpha)
    if k in MATS: return MATS[k]
    m=bpy.data.materials.new("m"); m.use_nodes=True; b=m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value=(*c,1); b.inputs["Roughness"].default_value=rough
    if emit:
        b.inputs["Emission Color"].default_value=(*c,1); b.inputs["Emission Strength"].default_value=emit
    if alpha<1: b.inputs["Alpha"].default_value=alpha
    MATS[k]=m; return m
def lin(h): # hex -> linear rgb
    h=h.lstrip('#'); c=[int(h[i:i+2],16)/255 for i in(0,2,4)]
    return tuple(((x+0.055)/1.055)**2.4 if x>0.04045 else x/12.92 for x in c)
def box(name,loc,size,m,parent=None,bev=.08,rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(location=loc); o=bpy.context.object; o.name=name
    o.scale=(size[0]/2,size[1]/2,size[2]/2); o.rotation_euler=rot
    bpy.ops.object.transform_apply(scale=True)
    if bev>0:
        md=o.modifiers.new("b","BEVEL"); md.width=bev; md.segments=3; md.limit_method='ANGLE'
    o.data.materials.append(m)
    if parent: o.parent=parent
    return o
def cyl(name,loc,r,h,m,parent=None,rot=(0,0,0),v=32):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v,radius=r,depth=h,location=loc,rotation=rot); o=bpy.context.object; o.name=name
    o.data.materials.append(m); bpy.ops.object.shade_smooth()
    if parent: o.parent=parent
    return o
def sph(name,loc,r,m,parent=None,scale=(1,1,1)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=r,location=loc); o=bpy.context.object; o.name=name; o.scale=scale
    o.data.materials.append(m); bpy.ops.object.shade_smooth()
    if parent: o.parent=parent
    return o
def empty(name,loc=(0,0,0),parent=None):
    o=bpy.data.objects.new(name,None); bpy.context.collection.objects.link(o); o.location=loc
    if parent: o.parent=parent
    return o

# ---------- mundo / luz ----------
w=bpy.data.worlds.new("w"); sc.world=w; w.use_nodes=True
bg=w.node_tree.nodes["Background"]; bg.inputs[0].default_value=(*lin("#bfe3ff"),1); bg.inputs[1].default_value=1.1
bpy.ops.object.light_add(type='SUN',location=(-6,8,14)); sun=bpy.context.object
sun.data.energy=4.2; sun.data.color=(1,.95,.85); sun.rotation_euler=(math.radians(50),math.radians(15),math.radians(-35)); sun.data.angle=math.radians(8)
bpy.ops.object.light_add(type='AREA',location=(0,-2,9)); fill=bpy.context.object; fill.data.energy=900; fill.data.size=14; fill.data.color=(1,.97,.92)

# ---------- aula ----------
floor_m=mat(lin("#c99a62"),.55); wall_m=mat(lin("#9fd8c4"),.9); wall2=mat(lin("#f3e7c8"),.9)
box("floor",(0,0,-.25),(30,26,.5),floor_m,bev=0)
for i in range(-6,7): box("plank",(i*2.2,0,.003),(.06,26,.01),mat(lin("#a87b48"),.7),bev=0)
box("wallB",(0,-11,9),(30,.5,18),wall_m,bev=0)      # fondo (atras de los alumnos)
box("wallF",(0,12,9),(30,.5,18),wall2,bev=0)        # pizarra
box("wallL",(-13,0,9),(.5,26,18),wall2,bev=0)
box("wallR",(13,0,9),(.5,26,18),wall2,bev=0)
box("zocalo",(0,-10.7,.6),(30,.4,1.2),mat(lin("#5aa58c"),.8),bev=0)
# pizarra
box("pizarra",(0,11.6,6),(11,.3,5),mat(lin("#2f5b4a"),.8),bev=.1); box("marco",(0,11.5,6),(11.6,.2,5.6),mat(lin("#8a5a2b"),.6),bev=.1)
box("tiza",(2,11.35,3.45),(.8,.2,.12),mat(lin("#f5f5f5"),.9),bev=0)
for i,(x,z,wd) in enumerate([(-3,6.9,3),(-2,6.2,4.4),(1.5,6.9,2.5),(-3.2,5.4,2),(2.5,5.6,3)]):
    box("garabato",(x,11.42,z),(wd,.05,.14),mat(lin("#f0f0f0"),.9,emit=.3),bev=0)
# ventana grande a la izquierda
box("vent_m",(-12.7,2,6.5),(.3,7.4,5.4),mat(lin("#8a5a2b"),.6),bev=.05)
box("vent_c",(-12.55,2,6.5),(.1,7,5),mat(lin("#8fd0ff"),.3,emit=2.2),bev=0)
box("vent_a",(-12.4,2,6.5),(.12,.25,5),mat(lin("#8a5a2b"),.6),bev=0)
# reloj
cyl("reloj",(6,-10.6,8.6),1.3,.3,mat(lin("#ffffff"),.4),rot=(math.radians(90),0,0))
cyl("reloj_a",(6,-10.45,8.6),1.3,.1,mat(lin("#dd3333"),.4),rot=(math.radians(90),0,0),v=3) if False else None
box("man1",(6,-10.4,8.9),(.14,.1,.9),mat(lin("#111111"),.5),bev=0); box("man2",(6.3,-10.4,8.6),(.7,.1,.14),mat(lin("#111111"),.5),bev=0)
# posters
box("poster1",(-6,-10.6,7.5),(3,.1,3.8),mat(lin("#ffb347"),.8),bev=0); box("pc",(-6,-10.5,7.6),(2,.05,2),mat(lin("#3b82f6"),.8),bev=0)
sph("planeta",(-6,-10.4,7.6),.8,mat(lin("#ff6b6b"),.5))
box("poster2",(9,-10.6,5.2),(2.4,.1,3.2),mat(lin("#c084fc"),.8),bev=0); sph("p2",(9,-10.5,5.3),.7,mat(lin("#fde047"),.5))
# techo (no tapa el sol)
ce=box("techo",(0,0,18.3),(30,26,.5),mat(lin("#f6f1e4"),.9,emit=.3),bev=0); ce.visible_shadow=False
# estante
box("estante",(11.3,2,2.2),(2,6,4.4),mat(lin("#8a5a2b"),.6),bev=.05)
for i,c in enumerate(["#ef4444","#3b82f6","#22c55e","#eab308","#a855f7","#f97316"]):
    box("libro",(10.5,.0+i*.8,4.65),(.8,.6,1),mat(lin(c),.6),bev=.03)
# globo terraqueo / planta
cyl("maceta",(-10.5,-8,.7),.9,1.4,mat(lin("#d97706"),.6)); sph("planta",(-10.5,-8,2.4),1.3,mat(lin("#22c55e"),.6)); sph("planta2",(-10.2,-7.6,3.2),.9,mat(lin("#16a34a"),.6))

def desk(x,y,mm="#e0a85f"):
    box("mesa",(x,y,3.0),(4,2.4,.28),mat(lin(mm),.45),bev=.05)
    for sx in(-1.75,1.75):
        for sy in(-1,1): box("pata",(x+sx,y+sy*.9,1.45),(.2,.2,2.9),mat(lin("#7f8aa0"),.35),bev=.03)
def chair(x,y):
    box("asiento",(x,y,1.65),(2.2,2.2,.25),mat(lin("#3b82f6"),.5),bev=.06)
    box("resp",(x,y-1.0,2.7),(2.2,.22,1.8),mat(lin("#3b82f6"),.5),bev=.06)
    for sx in(-.9,.9):
        for sy in(-.9,.9): box("pch",(x+sx,y+sy,.8),(.14,.14,1.6),mat(lin("#6b7280"),.35),bev=.02)

# ---------- personajes (estilo Roblox) ----------
FACES={}
def imgmat(path,rough=.6):
    if path in FACES: return FACES[path]
    img=bpy.data.images.load(os.path.abspath(path)); img.alpha_mode='STRAIGHT'
    m=bpy.data.materials.new("i"); m.use_nodes=True; nt=m.node_tree; b=nt.nodes["Principled BSDF"]
    t=nt.nodes.new("ShaderNodeTexImage"); t.image=img; t.interpolation='Linear'
    nt.links.new(t.outputs["Color"],b.inputs["Base Color"]); nt.links.new(t.outputs["Alpha"],b.inputs["Alpha"]); b.inputs["Roughness"].default_value=rough
    FACES[path]=m; return m
def decal(parent,path,loc,size,rot=(math.radians(90),0,0)):
    bpy.ops.mesh.primitive_plane_add(size=size,location=loc,rotation=rot); p=bpy.context.object; p.data.materials.append(imgmat(path)); p.parent=parent; return p
class Char: pass
def blob(name,loc,sc,m,parent,seg=20):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=12,location=loc); o=bpy.context.object; o.name=name; o.scale=sc; o.data.materials.append(m); bpy.ops.object.shade_smooth(); o.parent=parent; return o
def cone(loc,rot,r,h,m,parent):
    bpy.ops.mesh.primitive_cone_add(vertices=12,radius1=r,radius2=0,depth=h,location=loc,rotation=rot); o=bpy.context.object; o.data.materials.append(m); bpy.ops.object.shade_smooth(); o.parent=parent; return o
def make_char(name,skin,shirt,pants,hairc,hair,pos,yaw,seated,extra=None,sleeves="short",shoe=None,sole=None,skirt=False,sockbow=False,baggy=1.0,cuff=None):
    c=Char(); c.name=name; c.skin=mat(lin(skin),.4); c.root=empty(name+"_root",pos); c.yaw=yaw; c.base=Vector(pos); c.seated=seated
    shm=mat(lin(shirt),.5); pm=mat(lin(pants),.5); hm=mat(lin(hairc),.35)
    c.torso_p=empty(name+"_torso",(0,0,2),c.root)           # origen en las caderas
    box("torso",(0,0,1),(2,1,2),shm,c.torso_p,bev=.06)
    if os.path.exists(f"tex/{name}.png"): decal(c.torso_p,f"tex/{name}.png",(0,-.513,1),2.0)
    # espalda lisa con costura
    c.shirt=shm
    c.neck=empty(name+"_neck",(0,0,2),c.torso_p)
    cyl("cabeza",(0,0,.64),.67,1.24,c.skin,c.neck); 
    md=bpy.context.object.modifiers.new("b","BEVEL"); md.width=.16; md.segments=4; md.limit_method='ANGLE'
    c.head=c.neck
    # ---- pelo (accesorios tipo Roblox) ----
    if hair=="long":      # Lola: melena larga con flequillo lateral y mono rosa
        blob("cap",(0,.05,.98),(.72,.72,.5),hm,c.neck); blob("cap2",(0,.18,.82),(.76,.74,.62),hm,c.neck)
        box("espalda",(0,.55,-.35),(1.5,.5,2.5),hm,c.neck,bev=.2)
        for sx in(-1,1): box("mecha",(sx*.7,-.05,.25),(.34,.7,1.8),hm,c.neck,bev=.12)
        box("fleco1",(-.1,-.64,1.14),(1.1,.2,.26),hm,c.neck,bev=.1); box("fleco2",(.6,-.6,1.0),(.3,.22,.4),hm,c.neck,bev=.1)
        pk=mat(lin("#ff4f9a"),.35); blob("lazoA",(.52,-.2,1.42),(.3,.14,.22),pk,c.neck); blob("lazoB",(.86,-.2,1.42),(.3,.14,.22),pk,c.neck); blob("lazoC",(.69,-.2,1.42),(.14,.14,.14),mat(lin("#e11d74"),.35),c.neck)
    elif hair=="spiky":   # Max: pelo naranja de puas
        blob("cap",(0,.05,1.0),(.74,.74,.5),hm,c.neck); box("nuca",(0,.5,.72),(1.45,.4,.9),hm,c.neck,bev=.15)
        box("fleco",(0,-.6,1.08),(1.4,.2,.3),hm,c.neck,bev=.08)
        for i,(x,y,z,rx,ry) in enumerate([(-.5,-.1,1.4,0,-.5),(-.2,-.2,1.55,-.25,-.2),(.15,-.2,1.6,-.2,.1),(.5,-.1,1.42,0,.5),(0,.2,1.55,.3,0),(-.55,.2,1.2,0,-.9),(.55,.2,1.2,0,.9)]):
            cone((x,y,z),(rx,ry,0),.2,.75,hm,c.neck)
    elif hair=="twin":    # Lola gotica-kawaii: coletas negras con mechas rosas, flequillo recto, lazo grande
        pk=mat(lin("#ff8fc0"),.4)
        blob("cap",(0,.05,.98),(.74,.74,.52),hm,c.neck); blob("cap2",(0,.2,.8),(.76,.74,.6),hm,c.neck)
        box("espalda",(0,.55,.25),(1.45,.45,1.5),hm,c.neck,bev=.2); box("flequillo",(0,-.67,1.02),(1.42,.2,.44),hm,c.neck,bev=.1)
        for sx in(-1,1):
            box("mecha",(sx*.72,-.02,.2),(.26,.62,1.6),hm,c.neck,bev=.1)
            box("cola",(sx*1.02,.25,-.25),(.5,.5,2.7),hm,c.neck,bev=.2); box("rayo",(sx*1.02,.0,-.25),(.14,.14,2.5),pk,c.neck,bev=.04)
            box("rayo2",(sx*.7,-.68,.82),(.12,.14,.9),pk,c.neck,bev=.03)
            blob("bollo",(sx*.78,.15,1.18),(.34,.3,.34),mat(lin("#f6c9dc"),.5),c.neck); blob("liga",(sx*1.0,.25,.9),(.2,.2,.2),mat(lin("#ffffff"),.5),c.neck)
        kb=mat(lin("#14121a"),.4); blob("lazoA",(-.4,.0,1.5),(.34,.14,.26),kb,c.neck); blob("lazoB",(.4,.0,1.5),(.34,.14,.26),kb,c.neck); blob("lazoC",(0,.0,1.5),(.15,.15,.15),mat(lin("#2a2733"),.4),c.neck)
    elif hair=="messyblack":   # Tito: pelo negro revuelto con flequillo
        blob("cap",(0,.05,.98),(.74,.74,.5),hm,c.neck); box("nuca",(0,.5,.6),(1.4,.4,.95),hm,c.neck,bev=.15)
        for i,(x,zz,h,rz) in enumerate([(-.55,1.0,.55,.35),(-.28,1.02,.48,.12),(0,1.04,.62,-.05),(.28,1.02,.5,-.15),(.55,1.0,.55,-.35)]):
            box("fl",(x,-.66,zz),(.34,.16,h),hm,c.neck,bev=.05,rot=(0,0,rz))
        for sx in(-1,1): box("pat",(sx*.68,-.2,.62),(.16,.5,.75),hm,c.neck,bev=.05)
        for (x,z,rx,ry) in[(-.45,1.5,0,-.4),(0,1.55,-.2,0),(.4,1.5,0,.45)]: cone((x,.0,z),(rx,ry,0),.2,.5,hm,c.neck)
    elif hair=="swoosh":   # Max: pelo castano peinado de lado
        blob("cap",(0,.05,1.0),(.74,.74,.5),hm,c.neck); box("nuca",(0,.52,.65),(1.42,.38,.9),hm,c.neck,bev=.15)
        box("fleco",(.18,-.64,1.1),(1.2,.2,.36),hm,c.neck,bev=.08,rot=(0,math.radians(-14),0)); box("lado",(-.66,-.35,.8),(.22,.5,.7),hm,c.neck,bev=.06)
        for (x,z,rx,ry) in[(-.3,1.45,.1,-.3),(.15,1.5,-.1,.1),(.5,1.35,0,.5)]: cone((x,-.05,z),(rx,ry,0),.2,.55,hm,c.neck)
    elif hair=="canas":   # Profe: calvo arriba, canas a los lados
        for sx in(-1,1): blob("lado",(sx*.6,.1,.55),(.2,.38,.38),hm,c.neck)
        box("nuca",(0,.52,.55),(1.35,.25,.6),hm,c.neck,bev=.1)
        for sx in(-1,1): blob("ceja",(sx*.28,-.66,.82),(.22,.08,.07),hm,c.neck)
    c.faces={}
    for n in ["smile","grin","shock","angry","smug","worry","closed"]:
        bpy.ops.mesh.primitive_plane_add(size=1.12,location=(0,-.672,.62),rotation=(math.radians(90),0,0)); pl=bpy.context.object; pl.name="cara_"+n
        pl.data.materials.append(imgmat(f"faces/{name}_{n}.png")); pl.parent=c.neck; c.faces[n]=pl
    # brazos
    c.armL=empty(name+"_armL",(-1.5,0,1.9),c.torso_p); c.armR=empty(name+"_armR",(1.5,0,1.9),c.torso_p)
    for p in(c.armL,c.armR):
        p.rotation_mode='QUATERNION'; box("brazo",(0,0,-1),(1,1,2),c.skin,p,bev=.08)
        if sleeves=="long": box("manga",(0,0,-.78),(1.05,1.05,1.58),shm,p,bev=.06); box("puno",(0,0,-1.55),(1.08,1.08,.14),mat(lin("#ffffff"),.5),p,bev=.03)
        else: box("manga",(0,0,-.4),(1.05,1.05,.84),shm,p,bev=.06)
    c.legL=empty(name+"_legL",(-.5,0,0),c.torso_p); c.legR=empty(name+"_legR",(.5,0,0),c.torso_p)
    for p in(c.legL,c.legR):
        box("pierna",(0,0,-1),(1*baggy,1*baggy,2),pm,p,bev=.08)
        if shoe:
            box("zapato",(0,-.08,-1.78),(1.06,1.2,.44),mat(lin(shoe),.45),p,bev=.1)
            box("suela",(0,-.08,-1.97),(1.1,1.24,.12),mat(lin(sole or "#ffffff"),.5),p,bev=.04)
    if sockbow:
        for p in(c.legL,c.legR):
            decal(p,"tex/bow.png",(0,-.505,-.55),.55); cyl("volante",(0,0,-1.55),.64,.2,mat(lin("#ffffff"),.6),p); cyl("volante2",(0,0,-1.68),.62,.1,mat(lin("#e9e4ee"),.6),p)
    if skirt:
        kb=mat(lin("#1c1922"),.6)
        sk=cone((0,0,-.15),(math.radians(180),0,0),1.5,.9,kb,c.torso_p); sk.name="falda"
        sk2=cone((0,0,-.55),(math.radians(180),0,0),1.75,.5,mat(lin("#26222d"),.6),c.torso_p)
        cyl("encaje",(0,0,-.78),1.76,.08,mat(lin("#f4f0f6"),.7),c.torso_p)
    c.root.rotation_euler=(0,0,yaw)
    if extra: extra(c)
    return c
def set_face(c,n):
    for k,o in c.faces.items(): o.hide_render=(k!=n); o.hide_viewport=(k!=n)
def aimq(c,pivot,wdir,w,pitch=0):
    q0=Quaternion((1,0,0),pitch)
    if w<=0 or wdir is None: pivot.rotation_quaternion=q0; return
    d=Vector(wdir).normalized(); d=Quaternion((0,0,1),-c.yaw)@d     # a espacio local
    q1=Vector((0,0,-1)).rotation_difference(d)
    pivot.rotation_quaternion=q0.slerp(q1,min(1,w))

# desk + silla de cada alumno (miran hacia +y)
for (x,y) in[(-3,0),(3,0),(0,-4.5)]:
    desk(x,y+2.1,"#e0a85f"); chair(x,y-.1)

def hat(c):
    c.hat=empty("hatE",(0,0,1.32),c.neck)
    cyl("ala",(0,0,0),1.05,.08,mat(lin("#6b4423"),.6),c.hat); cyl("copa",(0,0,.28),.62,.5,mat(lin("#7c4f2a"),.6),c.hat); cyl("cinta",(0,0,.14),.64,.12,mat(lin("#222222"),.5),c.hat)
def lupa(c):
    c.lupa=empty("lupaE",(0,-.2,-1.9),c.armL); c.lupa.rotation_euler=(math.radians(-90),0,0)
    cyl("mango",(0,0,-.35),.1,.9,mat(lin("#222222"),.5),c.lupa,rot=(math.radians(90),0,0)) if False else None
    cyl("mango2",(0,0,0),.09,1.0,mat(lin("#222222"),.5),c.lupa,rot=(math.radians(90),0,0))
    # aro + cristal
    bpy.ops.mesh.primitive_torus_add(major_radius=.55,minor_radius=.09,location=(0,-.95,0),rotation=(0,0,0)); t=bpy.context.object
    t.data.materials.append(mat(lin("#d4a017"),.3)); t.parent=c.lupa
    g=cyl("cristal",(0,-.95,0),.5,.04,mat(lin("#bfe8ff"),.1,emit=.8),c.lupa,rot=(math.radians(0),0,0))
def ex_tito(c): hat(c); lupa(c)
tito=make_char("Tito","#f3d2b8","#ffffff","#16161c","#14131a","messyblack",(-3,0,-.2),math.radians(180),True,ex_tito,shoe="#f2f2f4",sole="#ffffff",baggy=1.2)
lola=make_char("Lola","#f7ece8","#f7f2f5","#f4f0f6","#14121a","twin",(3,0,-.2),math.radians(180),True,sleeves="long",shoe="#2a2124",sole="#111111",skirt=True,sockbow=True)
max_=make_char("Max","#f1c58f","#eee2cd","#6c6f7a","#8a5a3a","swoosh",(0,-4.5,-.2),math.radians(180),True,sleeves="long",shoe="#2b2326",sole="#d9d5c8",baggy=1.12)
profe=make_char("Profe","#e8c0a0","#fafafa","#3d4452","#a5a8b0","canas",(6.5,5.5,0),math.radians(160),False,sleeves="long",shoe="#1b1b1b",sole="#0a0a0a")
# cosas: tarteras, sandwich, galletas, migas, mayonesa
loncheraM=mat(lin("#ef4444"),.4)
lunch=box("fiambrera",(-3,2.1,3.33),(1.6,1.0,.4),loncheraM,bev=.06); lid=box("tapa",(-3,2.75,3.8),(1.6,.12,1.0),loncheraM,bev=.04,rot=(math.radians(-15),0,0))
wrap=box("papel",(-3,2.1,3.18),(1.3,.8,.04),mat(lin("#fafafa"),.8),bev=0)
mig=[box("miga",(-3+random.uniform(-.5,.5),2.1+random.uniform(-.3,.3),3.57),(.1,.1,.08),mat(lin("#d9a45c"),.8),bev=0) for _ in range(4)]
# galletas (Lola)
for o in mig: pass
cookieM=mat(lin("#b5651d"),.7)
cookie=empty("cookie",(0,-.2,-2.1),lola.armR);
cyl("galleta",(0,0,0),.6,.18,cookieM,cookie,rot=(math.radians(90),0,0))
for (x,z) in[(-.2,.15),(.2,-.1),(.05,.28),(-.25,-.2)]: sph("chip",(x,-.1,z),.09,mat(lin("#3b1d08"),.6),cookie)
crumbs=[sph("migaL",(random.uniform(-.4,.4),random.uniform(-.7,-.25),-1.8+random.uniform(-.2,.2)),.07,mat(lin("#d9a45c"),.8),lola.armL) for _ in range(7)]
# sandwich asqueroso (Max)
sand=empty("sandwich",(0,-.3,-2.0),max_.armR)
for i,(c,h,wd) in enumerate([("#e2b872",.28,1.5),("#6bc24a",.14,1.7),("#e0463a",.14,1.45),("#f4d35e",.1,1.6),("#7a3b2e",.28,1.35),("#9be15d",.16,1.75),("#e2b872",.28,1.5)]):
    box("cap",(0,0,-.9+sum([.3,.15,.15,.1,.3,.17][:i])+h/2-0.3),(wd,1.1,h),mat(lin(c),.6),sand,bev=.06)
sand.rotation_euler=(math.radians(-90),0,0)
mayo=[sph("mayo",p,r,mat(lin("#fff8e1"),.25),tito.neck,scale=(1,.4,1)) for p,r in[((-.35,-.72,.38),.19),((.28,-.72,.34),.15),((.0,-.72,.2),.2),((.42,-.72,.52),.1),((-.48,-.72,.56),.11)]]
# signos ! ?
def txt(s,col,size=1.3):
    bpy.ops.object.text_add(); o=bpy.context.object; o.data.body=s; o.data.size=size; o.data.extrude=.15; o.data.align_x='CENTER'
    o.data.materials.append(mat(lin(col),.4,emit=.6)); o.rotation_euler=(math.radians(90),0,math.radians(180)); return o
sig={}
def add_sign(k,s,col,where,size=1.6):
    o=txt(s,col,size); o.parent=where; o.location=(0,0,2.1); o.rotation_euler=(math.radians(90),0,0); sig[k]=o
add_sign("t_exc","!","#ff3b30",tito.neck); add_sign("l_q","?","#facc15",lola.neck); add_sign("m_q","?","#facc15",max_.neck); add_sign("p_exc","!","#ff3b30",profe.neck); add_sign("l_exc","!","#ff3b30",lola.neck); add_sign("t_q","?","#facc15",tito.neck)
# vapor profe
vap=[sph("vapor",(0,0,0),.28,mat(lin("#ffffff"),.9,emit=.6),profe.neck) for _ in range(6)]
# estrella/confeti
conf=[box("conf",(0,0,0),(.2,.1,.35),mat(lin(random.choice(["#ef4444","#3b82f6","#22c55e","#eab308","#ec4899"])),.5,emit=.4),bev=0) for _ in range(40)]
cr=random.Random(4); confd=[(cr.uniform(-8,8),cr.uniform(-5,7),cr.uniform(.4,1.2),cr.uniform(0,6),cr.uniform(1,4)) for _ in conf]

# ---------- camara ----------
camd=bpy.data.cameras.new("cam"); cam=bpy.data.objects.new("cam",camd); bpy.context.collection.objects.link(cam); sc.camera=cam
camd.sensor_fit='HORIZONTAL'; camd.sensor_width=36; camd.dof.use_dof=False
tgt=empty("tgt"); tc=cam.constraints.new('TRACK_TO'); tc.target=tgt; tc.track_axis='TRACK_NEGATIVE_Z'; tc.up_axis='UP_Y'
S=S0+[TOTAL]
SHOTS=[ # t0,t1, locA,locB, tgtA,tgtB, lens
 (0,S[1]-.1, (-9.5,6.5,6.8),(-6,5,5.4), (0,0,3.4),(-3,0,4.0), 24),
 (S[1]-.1,S[2]-.1, (-3.5,6,5.4),(-.5,4.3,5.0), (2.5,0,3.8),(3,0,3.7), 28),
 (S[2]-.1,S[3]-.1, (2.6,3.8,5.6),(0.8,2.9,5.2), (0,-4.5,3.9),(0,-4.5,3.9), 30),
 (S[3]-.1,S[3]+2.3, (-7,5.2,6.2),(-5.3,4.4,5.9), (-3,0,4.2),(-3,0,4.6), 26),
 (S[3]+2.3,S[4]-.05, (-1,-1,6.5),(0.5,0.2,6), (6.5,5.5,4.4),(6.5,5.5,4.3), 30),
 (S[4]-.05,S[5]-.1, (1.2,2.3,5.3),(3.2,3.9,5.2), (6.5,5.5,4.4),(6.5,5.5,4.5), 36),
 (S[5]-.1,S[5]+1.9, (-1.2,5,5.3),(0.8,4.3,5.1), (3,0,4.0),(3,0,4.0), 30),
 (S[5]+1.9,S[6]-.1, (-4.2,4.5,5.6),(-3.4,3.2,5.4), (-3,0,4.3),(-3,0,4.3), 36),
 (S[6]-.1,S[6]+3.4, (-6.5,3.8,6),(-3.8,2.8,5.0), (-3,0,4.2),(-3,0,4.3), 28),
 (S[6]+3.4,S[7]-.1, (-5,7,8),(8,10,9.5), (0,0,3.2),(0,0,3.2), 22),
 (S[7]-.1,TOTAL+1, (0,8.5,6.8),(0,11.8,7.4), (0,-1,3.4),(0,-1,3.4), 23),
]
def cam_at(t):
    for (a,b,l0,l1,t0,t1,ln) in SHOTS:
        if a<=t<=b:
            u=sm((t-a)/(b-a)) if False else (t-a)/(b-a)
            u=u*u*(3-2*u)*.5+u*.5
            cam.location=tuple(x+(y-x)*u for x,y in zip(l0,l1)); tgt.location=tuple(x+(y-x)*u for x,y in zip(t0,t1)); camd.lens=ln; return
    a,b,l0,l1,t0,t1,ln=SHOTS[-1]; cam.location=l1; tgt.location=t1; camd.lens=ln

# ---------- animacion ----------
def gt(i,off=0): return S[i]+off
def osc(t,f,a=1,ph=0): return math.sin((t*f+ph)*math.tau)*a
def pose(t):
    for c in(tito,lola,max_,profe):
        c.root.location=c.base; c.root.rotation_euler=(0,0,c.yaw)
        c.torso_p.rotation_euler=(0,0,0); c.neck.rotation_euler=(0,0,0); c.neck.location=(0,0,2)
        for p in(c.legL,c.legR): p.rotation_euler=(0,0,0)
        for p in(c.armL,c.armR): p.rotation_quaternion=(1,0,0,0)
        c.torso_p.location=(0,0,2)
        if c.seated:
            for p in(c.legL,c.legR): p.rotation_euler=(math.radians(-90),0,0)
            for p in(c.armL,c.armR): p.rotation_quaternion=Quaternion((1,0,0),math.radians(-80))
        c.torso_p.location=(0,0,2+osc(t,.8,.04,sum(map(ord,c.name))%7))
    for k,o in sig.items(): o.scale=(0,0,0)
    for o in vap: o.scale=(0,0,0)
    for o in conf: o.scale=(0,0,0)
    # ---------- TITO ----------
    T=tito
    stand=K(t,[(S[3]-.3,0),(S[3]+.5,1)])
    T.root.location=(-3,0-1.0*stand,-.2+stand*.2)
    for p in(T.legL,T.legR): p.rotation_euler=(math.radians(-90)*(1-stand),0,0)
    T.torso_p.location=(0,0,2)
    # detective: sombrero
    hs=K(t,[(2.0,0),(2.35,1.25),(2.6,1)]); T.hat.scale=(hs,hs,hs)
    # cara
    f="worry"
    if t>=gt(0,-.3): f="shock"
    if t>=2.0: f="smug"
    if t>=gt(1,2.2): f="worry"
    if t>=gt(2,.3): f="worry"
    if t>=gt(2,3.5): f="shock"
    if t>=gt(3): f="angry"
    if t>=gt(5,1.9): f="shock"
    if t>=gt(6,.9): f="worry"
    if t>=gt(6,3.6): f="closed"
    if t>=gt(7,.2): f="grin"
    set_face(T,f)
    # cabeza
    hy=K(t,[(0,0),(1.0,-.5),(3,.7),(3.8,0),(S[1]-.1,0),(S[1]+.5,-.9),(S[2],-.9),(S[2]+.4,0),(S[3]-.1,0),(S[3]+1,.4),(S[5]-.1,.4),(S[5]+2,0),(S[7],0)])
    hp=K(t,[(0,.5),(1.2,.45),(2.6,.0),(S[3],0),(S[6]+3,0),(S[6]+3.5,.7),(S[7]-.5,.7),(S[7]+.5,0)])
    T.neck.rotation_euler=(hp,0,hy)
    # brazos
    lp=K(t,[(0,-80),(3.0,-80),(3.5,-95),(S[1]-.1,-95),(S[1]+.5,-90),(S[2]+4.5,-90),(S[3]-.3,-80),(S[3]+.4,-130),(S[3]+2.2,-170),(S[3]+3.5,-15),(S[7]-.5,-15),(S[7]+.4,-60)])
    LA=K(t,[(S[1]-.1,0),(S[1]+.7,1),(S[2]+4.5,1),(S[2]+5.1,0)])  # lupa hacia Lola
    aimq(T,T.armL,(1,-.1,0.05),LA,math.radians(lp))
    # brazo derecho: apunta al profe en S3
    pr=K(t,[(0,-80),(S[3]-.3,-80),(S[3]+.5,-80)])
    PA=K(t,[(S[3]+.6,0),(S[3]+1.2,1),(S[4]+3.5,1),(S[4]+4,0)])
    aimq(T,T.armR,(9.5,5.5,.6),PA,math.radians(pr))
    if t>=gt(6,3.6): aimq(T,T.armR,None,0,math.radians(-150)); T.neck.rotation_euler=(.7,0,0)
    sw=K(t,[(S[7]-.3,0),(S[7]+.4,1)])
    if t>=gt(7,.2):
        T.armL.rotation_quaternion=Quaternion((1,0,0),math.radians(-15+osc(t,3,25))); T.armR.rotation_quaternion=Quaternion((1,0,0),math.radians(-15-osc(t,3,25)))
    # lupa visible solo hasta el giro
    T.lupa.scale=(1,1,1)
    # signos
    ex=K(t,[(.7,0),(1.0,1),(2.0,1),(2.2,0)]); sig["t_exc"].scale=(ex,ex,ex)
    q=K(t,[(S[2]+3.5,0),(S[2]+3.8,1),(S[3]-.4,1),(S[3]-.2,0)]); sig["t_q"].scale=(q,q,q)
    # mayo
    for o in mayo: o.hide_render=t<gt(5,1.6)
    for o in lunch.children: pass
    # ---------- LOLA ----------
    L=lola
    fl="smile"
    if t>=gt(1,.2): fl="smug"
    if t>=gt(1,2.3): fl="angry"
    if t>=gt(1,4): fl="grin"
    if t>=gt(2): fl="smile"
    if t>=gt(3): fl="shock"
    if t>=gt(5): fl="smug"
    if t>=gt(6,.5): fl="grin"
    if t>=gt(7): fl="grin"
    set_face(L,fl)
    ly=K(t,[(0,0),(S[1]-.1,0),(S[1]+.3,-.4),(S[1]+1.5,-.2),(S[2],0),(S[3],.4),(S[3]+1.4,-.5),(S[5],-.4),(S[5]+2,.5),(S[7],.5)])
    L.neck.rotation_euler=(0,0,ly)
    # brazo con migas levantado, luego galleta
    lP=K(t,[(S[1]+.1,-80),(S[1]+.7,-110),(S[1]+3,-110),(S[1]+3.6,-80)])
    L.armL.rotation_quaternion=Quaternion((1,0,0),math.radians(lP))
    gP=K(t,[(S[1]+3.3,-80),(S[1]+4,-100),(S[1]+5,-100),(S[1]+5.6,-80)])
    L.armR.rotation_quaternion=Quaternion((1,0,0),math.radians(gP))
    for o in crumbs: o.hide_render=not(S[1]-.1<=t<S[2]+1)
    cookie.scale=(1,1,1) if S[1]+3.3<=t<S[2]+1 else (0,0,0)
    # lola apunta a Tito en S5
    aimq(L,L.armL,(-3-3,0,.3),K(t,[(S[5]+.3,0),(S[5]+.9,1),(S[6]+.5,1),(S[6]+1,0)]),math.radians(-80))
    if t<S[5]+.3 or t>S[6]+1:
        L.armL.rotation_quaternion=Quaternion((1,0,0),math.radians(lP if S[1]-.1<=t<S[2] else -80))
    if t>=gt(7,.2): L.armL.rotation_quaternion=Quaternion((1,0,0),math.radians(-170+osc(t,3,15)))
    ex=K(t,[(S[5]+.2,0),(S[5]+.5,1.2),(S[5]+1.7,1.0),(S[5]+2,0)]); sig["l_exc"].scale=(ex,ex,ex)
    q=K(t,[(S[1]+.4,0),(S[1]+.7,1),(S[1]+2,1),(S[1]+2.3,0)]); sig["l_q"].scale=(q,q,q)
    L.root.location=(3,0,-.2+ (abs(osc(t,2.5,.35)) if t>=gt(7,.3) else 0))
    # ---------- MAX ----------
    M=max_
    fm="smile"
    if t>=gt(2,.2): fm="grin"
    if t>=gt(2,4.2): fm="smug"
    if t>=gt(3): fm="shock"
    if t>=gt(6,.6): fm="grin"
    if t>=gt(7): fm="grin"
    set_face(M,fm)
    M.neck.rotation_euler=(0,0,K(t,[(0,.2),(S[2]-.1,.2),(S[2]+.4,0),(S[3],-.3),(S[3]+1.6,.4),(S[5],0)]))
    sa=K(t,[(S[2]+.2,-80),(S[2]+.9,-115),(S[2]+4.5,-115),(S[2]+5.3,-80)])
    M.armR.rotation_quaternion=Quaternion((1,0,0),math.radians(sa))
    sand.scale=(1,1,1) if S[2]+.2<=t<S[3]+.7 else (0,0,0)
    # bocado
    if S[2]+2.2<=t<S[2]+4: M.neck.rotation_euler=(.3*abs(osc(t,2.5)),0,0)
    q=K(t,[(S[3]+.4,0),(S[3]+.7,1.2)])
    if t>=gt(7,.2): M.armL.rotation_quaternion=Quaternion((1,0,0),math.radians(-170+osc(t,3,20)))
    if t>=gt(7,.2): M.root.location=(0,-4.5,-.2+abs(osc(t,2.5,.35,.3)))
    sig["m_q"].scale=(0,0,0)
    # ---------- PROFE ----------
    P=profe
    fp="smile"
    if t>=gt(3,2.2): fp="shock"
    if t>=gt(4): fp="angry"
    if t>=gt(5,1.6): fp="worry"
    if t>=gt(6): fp="smug"
    if t>=gt(7): fp="grin"
    set_face(P,fp)
    # escribe en la pizarra al inicio
    wy=K(t,[(0,math.radians(170)),(S[3]+1.9,math.radians(170)),(S[3]+2.6,math.radians(300)),(S[7],math.radians(300))])
    P.root.rotation_euler=(0,0,wy); P.yaw=wy
    if t<S[3]+2.0:
        P.armR.rotation_quaternion=Quaternion((1,0,0),math.radians(-130+osc(t,1.5,14))); P.neck.rotation_euler=(0,0,osc(t,.5,.15))
    else:
        P.neck.rotation_euler=(0,0,0)
    ang=K(t,[(S[3]+2.3,0),(S[4],1),(S[4]+4,1),(S[4]+4.3,0)])
    if S[4]<=t<S[5]:
        shk=osc(t,12,.07)
        P.root.location=(6.5+shk,5.5,abs(osc(t,5,.2)))
        P.armL.rotation_quaternion=Quaternion((1,0,0),math.radians(-100+osc(t,5,25))); P.armR.rotation_quaternion=Quaternion((1,0,0),math.radians(-100-osc(t,5,25)))
        for i,o in enumerate(vap):
            u=(t*1.6+i/6.0)%1.0; s=sm(u*3)*(1-sm((u-.6)/.4))*1.2
            o.location=(((-1)**i)*(.9+u*.5),0,1.0+u*2.2); o.scale=(s,s,s)
    ex=K(t,[(S[3]+2.3,0),(S[3]+2.6,1.1),(S[3]+4,1),(S[3]+4.3,0)]); sig["p_exc"].scale=(ex,ex,ex)
    if t>=gt(7,.2):
        P.armL.rotation_quaternion=Quaternion((1,0,0),math.radians(-170+osc(t,3,15))); P.armR.rotation_quaternion=Quaternion((1,0,0),math.radians(-100))
    # rubor de ira del profe
    col=K(t,[(S[3]+2.3,0),(S[4]+.5,1),(S[5]-.5,1),(S[5]+.5,0)])
    bpy.ops.object.mode_set if False else None
    P.skin.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value=(*[a+(b-a)*col for a,b in zip(lin("#e8c0a0"),lin("#ff5a4a"))],1)
    # confeti en el final
    if t>=gt(7,.2):
        for i,o in enumerate(conf):
            x,y,sz,ph,sp=confd[i]; u=(t-gt(7,.2))
            o.location=(x,y,10-((u*sp+ph)%8)); o.rotation_euler=(u*3+ph,u*2,ph); o.scale=(1,1,1)
            o.hide_render=False
    for o in conf:
        if t<gt(7,.2): o.hide_render=True
    set_face_done=True

def render(f):
    t=f/FPS; pose(t); cam_at(t)
    sc.render.filepath=os.path.join(OUT,f"f{f:05d}.png"); bpy.ops.render.render(write_still=True)
if __name__=="__main__":
    os.makedirs(OUT,exist_ok=True)
    set_face(tito,"smile")
    for f in range(F0,F1+1,STEP):
        if os.path.exists(os.path.join(OUT,f"f{f:05d}.png")): continue
        render(f)
