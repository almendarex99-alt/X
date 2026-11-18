import bpy, math, sys, random
from mathutils import Vector, Euler
a=sys.argv[sys.argv.index("--")+1:]
OUT=a[0]; F0=int(a[1]); F1=int(a[2]); RES=float(a[3]); SAMP=int(a[4]) if len(a)>4 else 24
FPS=24; BX=40.0
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene
sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=SAMP; sc.cycles.use_denoising=True
sc.cycles.max_bounces=4; sc.cycles.glossy_bounces=3; sc.cycles.diffuse_bounces=2
sc.render.resolution_x=int(540*RES); sc.render.resolution_y=int(960*RES); sc.render.fps=FPS
sc.view_settings.view_transform='Filmic' if 'Filmic' in [i.identifier for i in sc.view_settings.bl_rna.properties['view_transform'].enum_items] else 'Standard'
sc.view_settings.look='None'
def mat(c,rough=.5,metal=0,em=None,emS=0,spec=.5):
    m=bpy.data.materials.new("m"); m.use_nodes=True; b=m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value=(*c,1); b.inputs["Roughness"].default_value=rough; b.inputs["Metallic"].default_value=metal
    try: b.inputs["Specular IOR Level"].default_value=spec
    except: pass
    if em: b.inputs["Emission Color"].default_value=(*em,1); b.inputs["Emission Strength"].default_value=emS
    return m
ALL={}
def reg(g,o): ALL.setdefault(g,[]).append(o); return o
def prim(kind,loc,scale,m,par=None,rot=(0,0,0),g=None,**kw):
    if kind=='sph': bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=16,location=loc)
    elif kind=='box': bpy.ops.mesh.primitive_cube_add(location=loc)
    elif kind=='cyl': bpy.ops.mesh.primitive_cylinder_add(vertices=24,location=loc,radius=kw.get('r',1),depth=kw.get('d',1))
    elif kind=='cone': bpy.ops.mesh.primitive_cone_add(vertices=32,location=loc,radius1=kw.get('r1',1),radius2=kw.get('r2',0),depth=kw.get('d',1))
    o=bpy.context.object; o.scale=scale; o.rotation_euler=rot; o.data.materials.append(m)
    if kind in('sph','cyl','cone'): bpy.ops.object.shade_smooth()
    if par: o.parent=par
    if g: reg(g,o)
    return o
def empty(loc,par=None,g=None):
    e=bpy.data.objects.new("e",None); sc.collection.objects.link(e); e.location=loc
    if par: e.parent=par
    if g: reg(g,e)
    return e
# ---------- world ----------
w=bpy.data.worlds.new("w"); sc.world=w; w.use_nodes=True
w.node_tree.nodes["Background"].inputs[0].default_value=(.004,.005,.012,1)
# ---------- materials ----------
wall=mat((.10,.22,.24),.85); wain=mat((.07,.045,.035),.5); wood=mat((.08,.045,.03),.18,0,spec=.6)
door=mat((.12,.07,.045),.5); ceil=mat((.55,.55,.5),.9); trim=mat((.5,.45,.38),.6)
skin=mat((.95,.72,.62),.55); skinP=mat((.82,.80,.78),.45)
black=mat((.005,.005,.006),.7)
# ---------- hallway ----------
HL=17
prim('box',(0,HL/2,-.05),(1.6,HL/2,.05),wood)
prim('box',(0,HL/2,3.05),(1.6,HL/2,.05),ceil)
for s in(-1,1):
    prim('box',(s*1.65,HL/2,1.5),(.05,HL/2,1.5),wall)
    prim('box',(s*1.6,HL/2,.45),(.03,HL/2,.45),wain)
    prim('box',(s*1.58,HL/2,.93),(.05,HL/2,.025),trim)
    prim('box',(s*1.58,HL/2,.05),(.05,HL/2,.05),trim)
    for y in(3.0,7.8,12.0):
        prim('box',(s*1.62,y,1.05),(.03,.5,1.05),door); prim('box',(s*1.59,y,1.05),(.02,.58,1.12),trim)
        prim('sph',(s*1.56,y+.38,1.0),(.03,.03,.03),mat((.7,.55,.2),.2,1),)
    for y in(5.4,10.0):
        prim('box',(s*1.6,y,1.7),(.02,.25,.32),mat((.03,.02,.02),.5)); prim('box',(s*1.595,y,1.7),(.01,.2,.27),mat((.35,.4,.38),.6))
prim('box',(0,HL,1.5),(1.65,.05,1.5),black)   # far darkness
# rug
prim('box',(0,6,.005),(.7,5.5,.006),mat((.35,.05,.07),.9))
# ceiling lamps
lampmat=mat((1,.7,.35),.3,0,(1,.62,.28),6)
prim('sph',(0,6,2.78),(.17,.17,.12),lampmat); prim('cyl',(0,6,2.95),(1,1,1),trim,r=.03,d=.3)
prim('sph',(0,12.5,2.78),(.12,.12,.1),mat((.3,.25,.2),.5))
bpy.ops.object.light_add(type='POINT',location=(0,6,2.6)); LH=bpy.context.object; LH.data.shadow_soft_size=.12; LH.data.color=(1,.62,.3)
bpy.ops.object.light_add(type='POINT',location=(0,9,2.4)); CH=bpy.context.object; CH.data.energy=12; CH.data.color=(.4,.55,1)
# ---------- character builders ----------
def girl(loc):
    r=empty(loc); P={}
    dress=mat((.68,.62,.85),.7); hair=mat((.06,.035,.025),.5); shoe=mat((.35,.1,.1),.4)
    P['root']=r
    for n,s in(('ll',-1),('rl',1)):
        p=empty((s*.065,0,.42),r); P[n]=p
        prim('cyl',(0,0,-.21),(1,1,1),skin,p,r=.035,d=.42); prim('sph',(0,-.03,-.42),(.05,.09,.04),shoe,p)
    prim('cone',(0,0,.64),(1,1,1),dress,r,r1=.2,r2=.09,d=.48)
    P['body']=r
    for n,s in(('la',-1),('ra',1)):
        p=empty((s*.12,0,.84),r); P[n]=p
        prim('cyl',(0,0,-.16),(1,1,1),dress,p,r=.032,d=.32); prim('sph',(0,0,-.33),(.035,.035,.035),skin,p)
    h=empty((0,0,.95),r); P['head']=h
    prim('sph',(0,0,.08),(.12,.12,.13),skin,h)
    prim('sph',(0,.025,.095),(.135,.13,.14),hair,h)
    prim('sph',(0,-.06,.15),(.125,.05,.07),hair,h)
    for s in(-1,1): prim('sph',(s*.045,-.105,.08),(.014,.01,.022),black,h)
    # teddy
    prim('sph',(-.12,-.22,.55),(.07,.06,.08),mat((.4,.22,.1),.9),P['body'])
    prim('sph',(-.12,-.22,.65),(.05,.05,.05),mat((.4,.22,.1),.9),P['body'])
    return P
def creature(loc,scale,g,hidden=False):
    r=empty(loc,g=g); r.scale=(scale,)*3; P={'root':r}
    cloak=mat((.006,.006,.008),.9); pale=mat((.78,.78,.74),.5)
    prim('cone',(0,0,.85),(1,1,1),cloak,r,r1=.42,r2=.1,d=1.7,g=g)
    h=empty((0,0,1.78),r,g=g); P['head']=h
    prim('sph',(0,0,.2),(.115,.125,.24),pale,h,g=g)
    for s in(-1,1): prim('sph',(s*.05,-.1,.27),(.032,.02,.05),black,h,g=g)
    prim('sph',(0,-.115,.1),(.06,.02,.018),black,h,g=g)
    jaw=prim('sph',(0,-.1,.06),(.05,.02,.045),black,h,g=g)
    for n,s in(('la',-1),('ra',1)):
        p=empty((s*.2,0,1.62),r,g=g); P[n]=p
        prim('cyl',(0,0,-.65),(1,1,1),cloak,p,r=.026,d=1.3,g=g)
        for k in(-1,0,1): prim('cyl',(k*.022,0,-1.43),(1,1,1),pale,p,r=.007,d=.2,g=g)
    return P
def lerp(a,b,t): return a+(b-a)*max(0,min(1,t))
def sm(t): t=max(0,min(1,t)); return t*t*(3-2*t)
# hallway cast
MIA=girl((0.1,3,0)); CR=creature((0,15,0),1.0,'hallcr')
# ---------- bedroom ----------
prim('box',(BX,2.5,-.05),(3,3.1,.05),wood); prim('box',(BX,2.5,2.85),(3,3.1,.05),ceil)
bw=mat((.17,.12,.14),.85)
prim('box',(BX,5.05,1.4),(3,.05,1.4),bw); prim('box',(BX-3.05,2.5,1.4),(.05,3.1,1.4),bw); prim('box',(BX+3.05,2.5,1.4),(.05,3.1,1.4),bw)
prim('box',(BX,-.65,1.4),(3,.05,1.4),bw)
# mirror
prim('box',(BX,4.97,1.3),(.85,.02,1.05),mat((.8,.82,.85),.0,1.0))
prim('box',(BX,5.0,1.3),(.93,.015,1.13),mat((.05,.03,.02),.4,0,))
prim('box',(BX,5.0,.12),(.9,.15,.1),mat((.06,.04,.03),.5))  # dresser
# bed (left)
prim('box',(BX-1.8,3.2,.3),(.9,1.3,.25),mat((.12,.07,.05),.6)); prim('box',(BX-1.8,3.2,.6),(.85,1.25,.12),mat((.55,.5,.55),.9))
prim('box',(BX-1.8,4.95,.9),(.9,.06,.5),mat((.1,.06,.04),.6))
# nightstand + lamp + photo
prim('box',(BX+1.6,2.2,.3),(.35,.3,.3),mat((.1,.06,.04),.5))
prim('cone',(BX+1.6,2.2,.8),(1,1,1),mat((1,.78,.5),.7,0,(1,.7,.35),2.5),r1=.18,r2=.1,d=.28)
prim('cyl',(BX+1.6,2.2,.64),(1,1,1),mat((.2,.15,.1),.4),r=.03,d=.1)
prim('box',(BX+1.35,2.12,.66),(.1,.01,.14),mat((.02,.02,.02),.4)); prim('box',(BX+1.35,2.115,.66),(.075,.008,.115),mat((.5,.45,.4),.8))
prim('box',(BX+1.35,2.1,.8),(.12,.012,.02),black)
# chair (rocking) + rocker pivot
rock=empty((BX,3.2,0))
cw=mat((.1,.055,.035),.5)
prim('box',(0,0,.45),(.38,.34,.03),cw,rock); prim('box',(0,-.32,.72),(.38,.03,.22),cw,rock)
for sx in(-.34,.34):
    prim('box',(sx,0,.22),(.025,.38,.025),cw,rock); prim('box',(sx,.3,.24),(.025,.025,.22),cw,rock); prim('box',(sx,-.3,.24),(.025,.025,.22),cw,rock)
# mother (real), faces +Y
mother=empty((0,0,.48),rock); mother.rotation_euler=(0,0,math.pi)
gown=mat((.05,.06,.1),.8); hairM=mat((.04,.03,.035),.35)
prim('cone',(0,0,.32),(1,1,1),gown,mother,r1=.3,r2=.15,d=.6,g='mom'); [reg('mom',o) for o in []]
mh=empty((0,0,.7),mother); 
prim('sph',(0,0,.1),(.13,.13,.15),skin,mh,g='mom')
prim('sph',(0,.045,.06),(.16,.15,.3),hairM,mh,g='mom'); prim('sph',(0,-.02,.2),(.16,.14,.1),hairM,mh,g='mom')
MA={}
for n,s in(('la',-1),('ra',1)):
    p=empty((s*.18,0,.55),mother); MA[n]=p
    prim('cyl',(0,0,-.2),(1,1,1),gown,p,r=.04,d=.4,g='mom'); prim('sph',(0,0,-.41),(.04,.04,.04),skin,p,g='mom')
# mirror-only creature
CR2=creature((0,0,.5),.78,'mircr'); CR2['root'].parent=rock; CR2['root'].location=(0,0,.5); CR2['root'].rotation_euler=(0,0,math.pi)
for o in ALL['mircr']: 
    o.visible_camera=False; o.visible_shadow=False
for o in ALL['mom']:
    o.visible_glossy=False
for o in ALL['mom']: pass
# Mia in bedroom (second girl)
MIA2=girl((BX+.4,-.6,0))
# bedroom lights
bpy.ops.object.light_add(type='POINT',location=(BX+1.45,2.2,.95)); BL=bpy.context.object; BL.data.color=(1,.65,.33); BL.data.shadow_soft_size=.15
bpy.ops.object.light_add(type='AREA',location=(BX-2.9,2.5,2.3)); MN=bpy.context.object; MN.data.energy=90; MN.data.color=(.45,.6,1); MN.data.size=2.5; MN.rotation_euler=(0,math.radians(-70),0)
bpy.ops.object.light_add(type='POINT',location=(BX,.4,2.3)); FL=bpy.context.object; FL.data.energy=10; FL.data.color=(.5,.6,1)
# camera
bpy.ops.object.camera_add(); C=bpy.context.object; C.data.lens=24; C.data.sensor_width=36; C.data.sensor_fit='VERTICAL'; C.data.sensor_height=36; sc.camera=C
C.data.dof.use_dof=True; C.data.dof.aperture_fstop=3.2
def look(cam,pos,tgt,roll=0):
    cam.location=pos; d=Vector(tgt)-Vector(pos); cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler(); cam.rotation_euler.rotate_axis('Z',roll)
def dark(t,wins):
    for a,b in wins:
        if a<=t<b: return True
    return False
HW=[(1.2,1.35),(2.5,2.68),(3.6,3.74),(4.3,4.48),(4.9,5.12)]
def pose_girl(P,phase,amp,swing):
    P['ll'].rotation_euler=(math.sin(phase)*amp,0,0); P['rl'].rotation_euler=(-math.sin(phase)*amp,0,0)
    P['la'].rotation_euler=(-math.sin(phase)*swing,0,0); P['ra'].rotation_euler=(math.sin(phase)*swing,0,0)
for fr in range(F0,F1+1):
    t=(fr-1)/FPS
    for o in(MIA['root'],MIA2['root'],CR['root']): pass
    hall = t<6.0
    # visibility by shot
    for P in(MIA,): 
        for ob in bpy.data.objects:
            pass
    def vis(root,v):
        root.hide_render=not v
        for ch in root.children_recursive: ch.hide_render=not v
    vis(MIA['root'],hall); vis(CR['root'],hall); vis(MIA2['root'],not hall)
    LH.hide_render=not hall; CH.hide_render=not hall
    BL.hide_render=hall; MN.hide_render=hall; FL.hide_render=hall
    if hall:
        # lamp
        k=0.02 if dark(t,HW) else (0.9+0.1*math.sin(t*41)); LH.data.energy=300*k; lampmat.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value=6*k
        CH.data.energy=10
        # Mia
        mx=.1
        if t<4.4: my=3+.6*t; ph=t*5.2; pose_girl(MIA,ph,.45,.35); MIA['root'].rotation_euler=(0,0,math.pi); MIA['root'].location=(mx,my,abs(math.sin(ph))*.015)
        elif t<5.2:
            my=3+.6*4.4; MIA['root'].location=(mx,my,0); pose_girl(MIA,0,0,0); MIA['root'].rotation_euler=(0,0,math.pi)
            MIA['head'].rotation_euler=(0,0,0)
            # slight hunch + head tremor when figure arrives
            MIA['root'].location.x=mx+math.sin(t*60)*.004*(t>4.9)
        else:
            tt=t-5.2; MIA['root'].rotation_euler=(0,0,math.pi-math.pi*sm(tt/.22))
            run=max(0,tt-.15); my=3+.6*4.4-run*3.4; MIA['root'].location=(.1+ (.25*sm(run/.6)),my,abs(math.sin(run*11))*.04)
            pose_girl(MIA,tt*11,.85,.7)
        # creature steps
        pos=[(0,17,0,False),(0,14.8,0,True),(.0,12.0,0,True),(0,9.6,0,True),(0,8.0,0,True)]
        yy=None
        if t<1.2: CR['root'].hide_render=True; [setattr(c,'hide_render',True) for c in CR['root'].children_recursive]
        else:
            if t<2.5: yy=14.9
            elif t<3.6: yy=12.0
            elif t<4.3: yy=9.8
            elif t<4.9: yy=8.2
            else: yy=MIA['root'].location.y+1.15 if t>=5.0 else 8.2
            if t>=5.0: yy=3+.6*4.4+1.15
            CR['root'].location=(0.05+.12*math.sin(t*.7),yy,0); CR['root'].rotation_euler=(0,0,0)
            CR['head']['rotation_euler'] if False else None
            CR['head'].rotation_euler=(0,.0,math.sin(t*2.2)*.12+ (.18 if t<5 else .0)); 
            CR['la'].rotation_euler=(0,0,.05+.03*math.sin(t*3)); CR['ra'].rotation_euler=(0,0,-.05-.03*math.sin(t*3))
            for p in(CR['la'],CR['ra']): pass
        cy_=0 + (0.8*sm(t/4.4) if t<4.4 else .8)
        C.data.lens=34; look(C,(0,-.4+cy_*0.9,1.1+.03*math.sin(t*.9)),(0,8,1.25),roll=.015*math.sin(t*.5))
        C.data.dof.focus_distance=max(2,(MIA['root'].location.y+.4-C.location.y)) if t<5.2 else 3.0
    else:
        u=t-6.0
        # bedroom lamp
        wins=[(12.0,12.0),(18.0,18.28),(19.2,19.75)]
        k=0.03 if dark(t,wins) else (.92+.08*math.sin(t*23)); BL.data.energy=120*k
        MN.data.energy=80*(0.3 if dark(t,wins) else 1)
        FL.data.energy=8
        # Mia
        M=MIA2['root']
        if t<7.3:
            ph=u*11; pose_girl(MIA2,ph,.85,.7); M.rotation_euler=(0,0,math.pi); M.location=(BX+.42,-.5+u/1.3*3.1,abs(math.sin(ph))*.04)
        else:
            tt=t-7.3
            M.location=(BX+.42+.1*sm(tt/.5),2.55-.0*sm(tt/.4)+0.4*(1-1)*0,0)
            M.location.y=lerp(-.5+1.3/1.3*3.1*0+ (7.3-6.0)/1.3*3.1-.0,3.15,tt/.5)
            M.rotation_euler=(0,0,lerp(math.pi,1.5*math.pi,tt/.5))
            pose_girl(MIA2,0,0,0)
            arm=sm((tt-.4)/.5)
            MIA2['la'].rotation_euler=(-math.pi/2*arm,0,0); MIA2['ra'].rotation_euler=(-math.pi/2*arm,0,0)
            M.location.x=BX+lerp(.52,.47,tt/3)
        # rocking
        rock.rotation_euler=(math.sin(t*1.4)*.035,0,0)
        # mother arm embrace (world +x -> local -x so rotY=+)
        em=sm((t-8.2)/1.0)
        MA['la'].rotation_euler=(0,math.pi*.55*em,0)    # reaches toward +x side (flipped local)
        MA['ra'].rotation_euler=(0,0,0)
        mh=0
        # creature (mirror only): same embrace
        CR2['la'].rotation_euler=(0,math.pi*.5*em+ .1,0); CR2['ra'].rotation_euler=(math.pi*.1*em,0,0)
        CR2['head'].rotation_euler=(.12*math.sin(t*.7),0,.08*math.sin(t*.9))
        # mother vanishes
        mv = t>=18.0
        for o in ALL['mom']: o.hide_render=mv
        # creature approaches mirror end
        if t>=19.75: CR2['root'].parent=None; CR2['root'].location=(BX,4.55,.7); CR2['root'].rotation_euler=(0,0,math.pi); CR2['root'].scale=(.7,.7,.7); CR2['head'].rotation_euler=(.0,0,0)
        # Mia in mirror: show; she hugs air after vanish (nothing to change)
        # camera
        p=sm(u/14.0)
        C.data.lens=36; look(C,(BX+.02-.12*p+.01*math.sin(t*1.1),.2+ (1.75-.2)*p, 1.6-.12*p+.008*math.sin(t*.8)),(BX,5.0,1.38),roll=.01*math.sin(t*.6))
        C.data.dof.focus_distance=max(1.5,5.0-C.location.y+.5)
    sc.render.filepath=f"{OUT}/f{fr:04d}.png"; sc.render.image_settings.file_format='PNG'
    bpy.ops.render.render(write_still=True)
