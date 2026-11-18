import bpy, math, random, sys
from mathutils import Vector
OUT=sys.argv[sys.argv.index("--")+1]; F0=int(sys.argv[sys.argv.index("--")+2]); F1=int(sys.argv[sys.argv.index("--")+3]); RES=float(sys.argv[sys.argv.index("--")+4])
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene
sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=40; sc.cycles.use_denoising=True
sc.render.resolution_x=int(1280*RES); sc.render.resolution_y=int(720*RES); sc.render.fps=24
sc.frame_start=1; sc.frame_end=120
sc.view_settings.view_transform='Standard'
def mat(c,rough=.35,spec=.4,coat=0.0):
    m=bpy.data.materials.new("m"); m.use_nodes=True; b=m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value=(*c,1); b.inputs["Roughness"].default_value=rough
    try: b.inputs["Specular IOR Level"].default_value=spec
    except: pass
    try: b.inputs["Coat Weight"].default_value=coat
    except: pass
    return m
def sph(name,loc,scale,m,seg=48):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=seg//2,location=loc); o=bpy.context.object
    o.scale=scale; o.name=name; o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o
# world
w=bpy.data.worlds.new("w"); sc.world=w; w.use_nodes=True
bg=w.node_tree.nodes["Background"]; bg.inputs[0].default_value=(.45,.72,1,1); bg.inputs[1].default_value=1.1
# ground & hills
bpy.ops.mesh.primitive_plane_add(size=80,location=(0,0,0)); g=bpy.context.object; g.data.materials.append(mat((.35,.78,.28),.8))
for x,y,s,c in((-14,18,9,(.4,.8,.32)),(10,22,12,(.3,.72,.3)),(24,10,7,(.38,.78,.3))):
    sph("hill",(x,y,-s*.45),(s*1.4,s*1.2,s),mat(c,.9),32)
# puddle
bpy.ops.mesh.primitive_cylinder_add(radius=2.4,depth=.04,location=(0,0,.02),vertices=96); p=bpy.context.object
p.scale=(1,.7,1); p.data.materials.append(mat((.25,.55,.95),.05,.8,1)); bpy.ops.object.shade_smooth()
# ripples
rip=[]
for i in range(3):
    bpy.ops.mesh.primitive_torus_add(major_radius=1,minor_radius=.025,location=(0,0,.05),major_segments=64,minor_segments=8)
    r=bpy.context.object; r.data.materials.append(mat((.95,.98,1),.2)); rip.append(r)
# flowers
fl=[(-4.2,-1.2,(1,.45,.65)),(-3.0,1.5,(1,1,1)),(3.8,-.5,(1,.65,.2)),(4.6,1.6,(1,.45,.65)),(-5.2,.4,(1,.65,.2)),(2.9,2.2,(1,1,1))]
flw=[]
for x,y,c in fl:
    bpy.ops.mesh.primitive_cylinder_add(radius=.04,depth=.7,location=(x,y,.35)); s=bpy.context.object; s.data.materials.append(mat((.2,.6,.2),.7))
    for k in range(6):
        a=k*math.pi/3
        sph("p",(x+.17*math.cos(a),y+.17*math.sin(a),.72),(.14,.14,.05),mat(c,.4),16)
    sph("c",(x,y,.74),(.1,.1,.08),mat((1,.85,.2),.4),16)
# duck
yel=mat((1,.82,.12),.4,.5,.3); yel2=mat((1,.88,.25),.4,.5,.3); org=mat((1,.5,.1),.35); red=mat((.9,.12,.18),.35,.5,.4)
dk=bpy.data.objects.new("duck",None); sc.collection.objects.link(dk)
def child(o,par=dk):
    o.parent=par; return o
body=child(sph("body",(0,0,.95),(.95,.85,.9),yel))
head=child(sph("head",(0,-.05,2.1),(.85,.8,.78),yel2))
for s in(-1,1):
    child(sph("cheek",(s*.55,-.55,1.95),(.17,.08,.11),mat((1,.55,.5),.5),16))
    ey=child(sph("eye",(s*.3,-.68,2.25),(.14,.1,.2),mat((.02,.02,.04),.1,1,1),24))
    child(sph("hl",(s*.3+.03,-.77,2.33),(.05,.04,.06),mat((1,1,1),.1),12))
    child(sph("foot",(s*.4,-.35,.1),(.3,.4,.1),org,24))
beak=child(sph("beak",(0,-.78,2.0),(.34,.3,.14),org,24))
child(sph("mouth",(0,-.86,1.95),(.22,.14,.07),mat((.7,.2,.2),.5),16))
wings=[child(sph("wing",(s*.95,0,1.0),(.2,.45,.5),mat((1,.72,.1),.4,.5,.3),24)) for s in(-1,1)]
hat=child(sph("hat",(0,-.05,2.55),(.78,.75,.5),red))
bpy.ops.mesh.primitive_cylinder_add(radius=1.0,depth=.07,location=(0,-.12,2.5),vertices=64); br=bpy.context.object; br.data.materials.append(red); bpy.ops.object.shade_smooth(); child(br)
child(sph("pom",(0,-.05,3.05),(.13,.13,.13),mat((1,1,1),.5),16))
# drops
random.seed(5); drops=[]
dm=mat((.75,.9,1),.05,.9,1)
for i in range(40):
    d=sph("d",(0,0,-5),(.09,.09,.12),dm,12); a=random.uniform(0,2*math.pi)
    drops.append((d,a,random.uniform(1.0,2.4),random.uniform(3.5,6.0),random.uniform(0,.04)))
# sun light + sun
bpy.ops.object.light_add(type='SUN',location=(5,-6,10)); L=bpy.context.object; L.data.energy=3.0; L.rotation_euler=(math.radians(48),math.radians(10),math.radians(35)); L.data.angle=.08
bpy.ops.object.light_add(type='AREA',location=(-4,-6,4)); A=bpy.context.object; A.data.energy=140; A.data.size=6; A.rotation_euler=(math.radians(70),0,math.radians(-30))
sun=sph("sun",(9,25,12),(2.2,2.2,2.2),bpy.data.materials.new("e"))
sm=sun.data.materials[0]; sm.use_nodes=True; n=sm.node_tree.nodes; n.clear(); em=n.new("ShaderNodeEmission"); em.inputs[0].default_value=(1,.85,.2,1); em.inputs[1].default_value=3; o=n.new("ShaderNodeOutputMaterial"); sm.node_tree.links.new(em.outputs[0],o.inputs[0])
# clouds
clouds=[]
for cx,cy,cz in((-8,16,8),(2,20,10),(12,14,7)):
    root=bpy.data.objects.new("cl",None); sc.collection.objects.link(root)
    for dx,dz,r in((0,0,1.6),(-1.5,-.2,1.2),(1.5,-.2,1.3),(.3,.8,1.1)):
        o=sph("c",(dx,0,dz),(r*1.1,r*.8,r*.8),mat((1,1,1),.9),24); o.parent=root
    root.location=(cx,cy,cz); clouds.append((root,cx))
# camera
bpy.ops.object.camera_add(location=(0,-12.5,3.4)); C=bpy.context.object; C.data.lens=30
C.rotation_euler=(math.radians(86),0,0); sc.camera=C
for fr in range(F0,F1+1):
    t=(fr-1)/24; sc.frame_set(fr)
    cyc=(t*1.6)%1; hop=abs(math.sin(cyc*math.pi)); z=hop*1.5
    sq=1-.2*(1-min(hop*5,1))
    dk.location=(0,0,z); dk.scale=(1/math.sqrt(sq),1/math.sqrt(sq),sq)
    dk.rotation_euler=(0,math.sin(t*3.2)*.08,math.sin(t*1.6*math.pi)*.12)
    for i,w_ in enumerate(wings): w_.rotation_euler=(0,(1 if i else -1)*(.5+math.sin(t*16)*.45),0)
    head.location=(0,-.05,2.1+math.sin(t*3.2*math.pi)*.04)
    for k,r in enumerate(rip):
        ph=((t*1.6)+k/3)%1; s=.5+ph*1.9; r.scale=(s,s*.7,1); r.location.z=.05
        r.data.materials[0].diffuse_color=(1,1,1,1-ph)
    land=(t*1.6)%1
    for d,a,vh,vz,j in drops:
        tt=land*.625
        if land<.7:
            d.location=(math.cos(a)*vh*tt*1.6,math.sin(a)*vh*tt*.9,.1+vz*tt-9.8*tt*tt*.6)
            if d.location.z<.05: d.location.z=-5
        else: d.location=(0,0,-5)
    for root,cx in clouds: root.location.x=((cx+t*.9)+22)%44-22
    for ob in bpy.data.objects:
        pass
    sc.render.filepath=f"{OUT}/f{fr:04d}.png"; sc.render.image_settings.file_format='PNG'
    bpy.ops.render.render(write_still=True)
