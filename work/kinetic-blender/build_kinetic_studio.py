"""Reference-driven, editable Kinetic Studio proof; run with Blender --background.

All scene geometry and graphics are authored procedurally. No Spline source is changed.
The camera is an inferred anchor fit, not a measured reconstruction of the concept art.
"""
import bpy
import math
import random
import json
import time
import hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent.parent
random.seed(271026)
START = time.time()
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1
scene.render.engine = 'CYCLES'
scene.cycles.samples = 24
scene.cycles.use_denoising = True
scene.cycles.adaptive_threshold = .035
scene.cycles.max_bounces = 8
scene.cycles.diffuse_bounces = 3
scene.cycles.glossy_bounces = 4
scene.cycles.transmission_bounces = 6
scene.render.resolution_x = 960
scene.render.resolution_y = 270
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGB'
scene.render.film_transparent = False
scene.render.threads_mode = 'FIXED'
scene.render.threads = 12
scene.view_settings.view_transform = 'AgX'
scene.view_settings.exposure = .35
try:
    scene.view_settings.look = 'AgX - Medium High Contrast'
except TypeError:
    pass

devices = []
prefs = bpy.context.preferences.addons['cycles'].preferences
for mode in ['OPTIX', 'CUDA']:
    try:
        prefs.compute_device_type = mode
        prefs.get_devices()
        for d in prefs.devices:
            d.use = d.type != 'CPU'
        if any(d.use for d in prefs.devices):
            devices = [{'name':d.name, 'type':d.type, 'enabled':bool(d.use)} for d in prefs.devices]
            scene.cycles.device = 'GPU'
            break
    except Exception as exc:
        print('DEVICE_CANDIDATE_UNAVAILABLE', mode, str(exc))
else:
    scene.cycles.device = 'CPU'

world = bpy.data.worlds.new('Blue hour ambient')
world.use_nodes = True
world.node_tree.nodes['Background'].inputs['Color'].default_value = (.22,.32,.58,1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value = .16
scene.world = world

COL = None
def collection(name):
    global COL
    COL = bpy.data.collections.new(name)
    scene.collection.children.link(COL)
    return COL

def move_to_collection(obj):
    for c in list(obj.users_collection): c.objects.unlink(obj)
    COL.objects.link(obj)
    return obj

def finish(obj, name, mat=None):
    obj.name = name
    if mat: obj.data.materials.append(mat)
    return obj

def material(name, color, rough=.45, metal=0, emission=0, transmission=0):
    m=bpy.data.materials.new(name); m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Roughness'].default_value=rough
    p.inputs['Metallic'].default_value=metal
    p.inputs['Transmission Weight'].default_value=transmission
    p.inputs['IOR'].default_value=1.46
    if emission:
        p.inputs['Emission Color'].default_value=(*color,1)
        p.inputs['Emission Strength'].default_value=emission
    return m

def tactile(m, scale, strength=.15, distance=.001, stretch=None):
    nt=m.node_tree; n=nt.nodes; l=nt.links
    tex=n.new('ShaderNodeTexCoord'); noise=n.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value=scale
    noise.inputs['Detail'].default_value=3
    if stretch:
        v=n.new('ShaderNodeVectorMath');v.operation='MULTIPLY';v.inputs[1].default_value=stretch
        l.new(tex.outputs['Generated'],v.inputs[0]);l.new(v.outputs[0],noise.inputs['Vector'])
    else: l.new(tex.outputs['Generated'],noise.inputs['Vector'])
    bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=strength;bump.inputs['Distance'].default_value=distance
    l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs['Normal'],n['Principled BSDF'].inputs['Normal'])
    return noise

black=material('Graphite powder coat',(.023,.029,.035),.36,.72)
tactile(black,170,.15,.0005)
dark=material('Near-black architectural paint',(.028,.034,.039),.68)
walnut=material('Oiled walnut cabinetry',(.17,.077,.035),.35)
grain=tactile(walnut,5,.2,.001,(6,.15,4))
nt=walnut.node_tree;r=nt.nodes.new('ShaderNodeValToRGB')
r.color_ramp.elements[0].color=(.045,.017,.007,1);r.color_ramp.elements[1].color=(.25,.12,.05,1)
nt.links.new(grain.outputs['Fac'],r.inputs[0]);nt.links.new(r.outputs[0],nt.nodes['Principled BSDF'].inputs['Base Color'])
floor_mats=[]
for i in range(8):
    m=walnut.copy();m.name=f'Floor walnut plank variation {i+1:02}'
    ramp=next(n for n in m.node_tree.nodes if n.type=='VALTORGB')
    factor=.77+i*.065
    ramp.color_ramp.elements[0].color=(.055*factor,.026*factor,.012*factor,1)
    ramp.color_ramp.elements[1].color=(.28*factor,.155*factor,.073*factor,1)
    m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.29+i*.015
    floor_mats.append(m)
chrome=material('Brushed aluminum',(.38,.42,.46),.26,.95)
rubber=material('Rubber and cable jacket',(.012,.016,.019),.68)
fabric=material('Charcoal woven upholstery',(.065,.06,.052),.78)
tactile(fabric,210,.38,.001)
fabric.node_tree.nodes['Principled BSDF'].inputs['Sheen Weight'].default_value=.25
leather=material('Soft espresso leather',(.065,.041,.028),.4)
tactile(leather,115,.14,.0007)
rug=material('Warm charcoal woven rug',(.095,.087,.074),.95)
tactile(rug,240,.5,.004)
cream=material('Warm paper and bone',(.65,.58,.43),.48)
ceramic=material('Stoneware planter',(.28,.29,.27),.49)
tactile(ceramic,70,.14,.002)
soil=material('Planter soil',(.025,.016,.008),.98)
leaf=material('Leaf wax',(.045,.105,.028),.4)
leaf.node_tree.nodes['Principled BSDF'].inputs['Subsurface Weight'].default_value=.07
stemmat=material('Plant stems',(.04,.07,.018),.55)
glass=material('Architectural clear glass',(.94,.98,1),.025,0,0,1)
amber=material('Warm LED diffuser', (1,.51,.19),.28,0,5)
cyan=material('Motion cyan LED',(.025,.48,1),.25,0,4)
violet=material('Projects violet LED',(.43,.17,1),.3,0,3)
white=material('Warm lettering',(.83,.81,.71),.5,0,.8)
screenmat=material('Screen dark blue',(.009,.023,.055),.28,0,.65)
screenblue=material('Display cyan graphics',(.13,.56,.95),.45,0,1.8)
screenwhite=material('Display neutral graphics',(.55,.7,.8),.5,0,1.1)

def box(name, loc, dims, mat, bevel=0):
    x,y,z=[v/2 for v in dims]
    verts=[(-x,-y,-z),(-x,-y,z),(-x,y,-z),(-x,y,z),(x,-y,-z),(x,-y,z),(x,y,-z),(x,y,z)]
    faces=[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)]
    # Outward winding is required by lighting bakes and backface culling.
    faces=[tuple(reversed(face)) for face in faces]
    mesh=bpy.data.meshes.new(name+' mesh');mesh.from_pydata(verts,[],faces);mesh.update()
    obj=bpy.data.objects.new(name,mesh);COL.objects.link(obj);obj.location=loc
    finish(obj,name,mat)
    if bevel:
        mod=obj.modifiers.new('Editable edge radii','BEVEL');mod.width=bevel;mod.segments=3 if bevel>.018 else 2
        mod=obj.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL')
    return obj

def tube(name,a,b,radius,mat,radius2=None,vertices=16):
    a,b=Vector(a),Vector(b);d=b-a;length=d.length
    if length<1e-5:return None
    r2=radius if radius2 is None else radius2
    verts=[]
    for z,r in [(-length/2,radius),(length/2,r2)]:
        verts.extend([(r*math.cos(i*2*math.pi/vertices),r*math.sin(i*2*math.pi/vertices),z) for i in range(vertices)])
    faces=[tuple(range(vertices-1,-1,-1)),tuple(range(vertices,vertices*2))]
    faces.extend((i,(i+1)%vertices,(i+1)%vertices+vertices,i+vertices) for i in range(vertices))
    mesh=bpy.data.meshes.new(name+' mesh');mesh.from_pydata(verts,[],faces);mesh.update()
    obj=bpy.data.objects.new(name,mesh);COL.objects.link(obj);obj.location=(a+b)/2;obj.rotation_euler=d.to_track_quat('Z','Y').to_euler()
    finish(obj,name,mat)
    for p in mesh.polygons[2:]:p.use_smooth=True
    return obj

def ellipsoid(name,loc,scale,mat,seg=20,rings=12):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=rings,location=loc)
    o=move_to_collection(bpy.context.object);o.scale=scale;finish(o,name,mat)
    for p in o.data.polygons:p.use_smooth=True
    return o

def path(name,points,radius,mat,cyclic=False):
    data=bpy.data.curves.new(name+' editable path','CURVE');data.dimensions='3D';data.resolution_u=12
    data.bevel_depth=radius;data.bevel_resolution=3
    s=data.splines.new('BEZIER');s.bezier_points.add(len(points)-1)
    for p,co in zip(s.bezier_points,points):p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
    s.use_cyclic_u=cyclic
    o=bpy.data.objects.new(name,data);COL.objects.link(o);finish(o,name,mat);return o

def text(name,body,loc,size,mat=white,align='CENTER'):
    data=bpy.data.curves.new(name+' editable type','FONT');data.body=body;data.align_x=align;data.size=size;data.extrude=.0004
    o=bpy.data.objects.new(name,data);COL.objects.link(o);o.location=loc;o.rotation_euler=(math.pi/2,0,0);finish(o,name,mat);return o

def area(name,loc,target,power,color,size,size_y=None):
    data=bpy.data.lights.new(name,'AREA');data.energy=power;data.color=color
    data.shape='RECTANGLE';data.size=size;data.size_y=size if size_y is None else size_y
    o=bpy.data.objects.new(name,data);COL.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();return o

def assembly(name,loc,angle,builder):
    old=set(COL.objects);builder();new=set(COL.objects)-old
    root=bpy.data.objects.new(name,None);COL.objects.link(root)
    for o in new:
        if o.parent is None:o.parent=root
    root.location=loc;root.rotation_euler[2]=angle
    return root

def chair(name,loc,angle=0,meeting=False):
    def parts():
        upholstery=leather if meeting else fabric
        box('Sculpted seat',(0,0,.49),(.56,.53,.12),upholstery,.055)
        box('Lumbar cushion',(0,-.205,.83),(.52,.11,.52),upholstery,.055)
        if not meeting:
            box('Back mesh panel',(0,-.2,1.13),(.49,.07,.35),fabric,.04)
            box('Adjustable headrest',(0,-.22,1.42),(.34,.105,.17),rubber,.05)
            for side in [-1,1]:
                path('Chair back rail',[(side*.27,-.17,.56),(side*.27,-.26,1),(side*.21,-.23,1.32)],.018,black)
                tube('Arm support',(side*.34,.05,.52),(side*.34,.05,.73),.018,chrome)
                box('Arm pad',(side*.34,.015,.76),(.095,.3,.045),rubber,.018)
        tube('Chair gas lift',(0,0,.13),(0,0,.45),.034,chrome)
        for i in range(5):
            a=2*math.pi*i/5
            end=(.32*math.cos(a),.32*math.sin(a),.095)
            tube('Five spoke base',(0,0,.16),end,.022,black)
            ellipsoid('Chair castor',(end[0],end[1],.05),(.045,.032,.043),rubber,12,8)
    return assembly(name,loc,angle,parts)

def desk(name,x,y,width=2.3,depth=.85):
    box(name+' walnut top',(x,y,.79),(width,depth,.055),walnut,.018)
    for side in [-1,1]:
        sx=x+side*(width/2-.24)
        box(name+' drawer pedestal',(sx,y+.05,.38),(.42,depth-.12,.73),dark,.009)
        for z in [.16,.38,.60]:
            box('Drawer face',(sx,y-depth/2-.009,z),(.395,.027,.19),black,.004)
            box('Drawer pull',(sx,y-depth/2-.027,z+.055),(.18,.025,.012),chrome,.004)
    tube('Rear cable tray',(x-width*.37,y+.25,.63),(x+width*.37,y+.25,.63),.035,black)

def monitor(name,x,y,z,w,h,graphic='data'):
    box(name+' housing',(x,y,z),(w,.075,h),black,.025)
    box(name+' glass',(x,y-.041,z),(w-.035,.009,h-.035),screenmat,.007)
    tube(name+' stand',(x,y+.015,.84),(x,y+.015,z-h/2),.025,black)
    box(name+' foot',(x,y-.02,.823),(.33,.25,.018),black,.008)
    left=x-w*.44;right=x+w*.44;bottom=z-h*.39;top=z+h*.36;front=y-.052
    if graphic=='landscape':
        palettes=[(.035,.06,.15),(.045,.08,.20),(.065,.12,.22),(.12,.19,.28)]
        for layer,col in enumerate(palettes):
            m=material(name+f' mountain tone {layer}',col,.6,0,.8)
            points=[(left,bottom)]
            for i in range(25):
                xx=left+(right-left)*i/24
                zz=bottom+(top-bottom)*(.35+.12*math.sin(i*1.7+layer)+.08*random.random()+layer*.11)
                points.append((xx,zz))
            points.append((right,bottom))
            poly(name+' layered mountain',points,front-.001*layer,m)
    elif graphic=='skeleton':
        cx=x;cz=z+.10
        # Editable diagram, deliberately schematic rather than a medical illustration.
        ring=[(cx+.07*math.cos(a),front-.002,cz+.56+.095*math.sin(a)) for a in [i*math.tau/24 for i in range(24)]]
        path('Display skeleton head',ring,.005,screenblue,True)
        for pts in [[(cx,cz+.45),(cx,cz+.04)],[(cx-.19,cz+.37),(cx+.19,cz+.37)],[(cx-.19,cz+.37),(cx-.24,cz+.12),(cx-.26,cz-.12)],[(cx+.19,cz+.37),(cx+.24,cz+.12),(cx+.26,cz-.12)],[(cx,cz+.04),(cx-.11,cz-.04),(cx-.12,cz-.38),(cx-.13,cz-.69)],[(cx,cz+.04),(cx+.11,cz-.04),(cx+.12,cz-.38),(cx+.13,cz-.69)]]:
            path('Display skeletal joint chain',[(xx,front-.002,zz) for xx,zz in pts],.006,screenblue)
        for i in range(6):
            zz=cz+.13+i*.045
            path('Display rib',[(cx-.12,front-.004,zz+.03),(cx,front-.004,zz),(cx+.12,front-.004,zz+.03)],.003,screenwhite)
    else:
        for row in range(3):
            zz=bottom+(top-bottom)*(.2+row*.28)
            pts=[(left+(right-left)*i/55,front,zz+.025*math.sin(i*.65+row)+.014*math.cos(i*1.8)) for i in range(56)]
            path('Editable signal trace',pts,.0025,screenblue if row%2 else screenwhite)
            tube('Display graph baseline',(left,front,zz-.045),(right,front,zz-.045),.001,screenwhite)
    return None

def poly(name,xz,y,mat):
    mesh=bpy.data.meshes.new(name+' mesh');mesh.from_pydata([(x,y,z) for x,z in xz],[],[tuple(range(len(xz)))]);mesh.update()
    obj=bpy.data.objects.new(name,mesh);COL.objects.link(obj);finish(obj,name,mat);return obj

def plant(name,x,y,h=1.7):
    pot=h*.23
    tube(name+' stoneware pot',(x,y,.04),(x,y,pot),h*.12,ceramic,h*.145,32)
    tube(name+' soil',(x,y,pot-.025),(x,y,pot-.015),h*.135,soil,vertices=24)
    for stalk in range(7):
        a=stalk*2.399;reach=h*(.12+.13*random.random())
        top=(x+math.cos(a)*reach,y+math.sin(a)*reach,h*(.65+.35*random.random()))
        path(name+' stem',[(x,y,pot),(x+math.cos(a)*reach*.3,y+math.sin(a)*reach*.3,h*.5),top],.007,stemmat)
        for j in range(4):
            t=.45+j*.16
            base=Vector((x+(top[0]-x)*t,y+(top[1]-y)*t,pot+(top[2]-pot)*t))
            az=a+j*2.1;length=h*(.14+.06*random.random());width=length*.25
            d=Vector((math.cos(az),math.sin(az),.27));side=Vector((-math.sin(az),math.cos(az),0))
            verts=[]
            for k in range(7):
                u=k/6;mid=base+d*(u*length);mid.z+=math.sin(u*math.pi)*length*.25
                ww=math.sin(u*math.pi)*width
                verts.extend([tuple(mid-side*ww),tuple(mid+Vector((0,0,.012))),tuple(mid+side*ww)])
            faces=[]
            for k in range(6):
                n=k*3;faces.extend([(n,n+3,n+4,n+1),(n+1,n+4,n+5,n+2)])
            mesh=bpy.data.meshes.new(name+' leaf mesh');mesh.from_pydata(verts,[],faces);mesh.update()
            ob=bpy.data.objects.new(name+' waxy leaf',mesh);COL.objects.link(ob);finish(ob,ob.name,leaf)
            for f in mesh.polygons:f.use_smooth=True

def books(x,y,z,count=10):
    bookcolors=[(.12,.13,.12),(.24,.12,.065),(.31,.28,.20),(.06,.09,.13),(.16,.19,.16)]
    for i in range(count):
        w=random.uniform(.035,.07);h=random.uniform(.19,.31)
        m=material('Book linen '+str(len(bpy.data.materials)),random.choice(bookcolors),.85)
        box('Book bound spine',(x,y,z+h/2),(w,.18,h),m,.003)
        tube('Book spine rule',(x-w*.25,y-.092,z+h*.8),(x+w*.25,y-.092,z+h*.8),.001,cream)
        x+=w+.009

collection('01_ARCHITECTURE')
box('Foundation slab',(0,0,-.10),(23.2,12,.18),dark,.01)
for ix in range(96):
    x=-11.4+ix*.24
    offset=(ix%3)*.72
    for j in range(7):
        y=-6.5+j*2.12+offset
        if -5.95<y<6.6:
            box('Separate walnut floor plank',(x,y,.003),(.237,2.115,.032),random.choice(floor_mats),.002)
for x in [-11.5,11.5]:
    box('Side perimeter sill',(x,0,.08),(.09,12,.14),black,.006)
    for y in [-3,0,3,5.8]:
        box('Side glazed mullion',(x,y,2.65),(.09,.09,5.3),black,.004)
    box('Side glass',(x,1,2.65),(.015,9.5,5.2),glass)
for x in [-11.5,-9.6,-7.7,-5.8,-3.9,-2.7,-.9,.9,2.7,4.7,6.8,8.8,10.6,11.5]:
    box('Rear window mullion',(x,5.7,2.65),(.07,.105,5.3),black,.004)
box('Rear glass wall',(0,5.75,2.65),(23,.016,5.3),glass)
for z in [.12,3.55,5.15]:box('Rear transom',(0,5.69,z),(23,.09,.065),black,.004)
for x in [-11.5,-5.9,-2.8,2.8,7.3,11.5]:
    box('Architectural column',(x,3.25,2.4),(.16,.23,4.8),dark,.008)
    box('Ceiling beam',(x,.5,4.82),(.22,10.8,.28),walnut,.008)
box('Rear ceiling lintel',(0,5.35,4.84),(23,.55,.32),dark,.01)
for x,w,label,num,accent in [(-8.6,5.2,'MOTION SYSTEMS','01',cyan),(-4.4,2.75,'CLINICAL THINKING','02',amber),(4.95,4.45,'CREATIVE ENGINEERING','03',amber),(9.45,3.85,'PROJECTS','04',violet)]:
    box('Zone header '+num,(x,3.12,3.85),(w,.18,.54),dark,.008)
    text('Editable zone title '+num,label,(x+.15,3.017,3.86),.145)
    text('Editable zone number '+num,num,(x-w/2+.34,3.012,3.78),.27,accent)
    box('Header accent '+num,(x,3.01,3.65),(w*.7,.01,.014),accent)
box('Workstation architectural header',(0,3.14,3.85),(5.4,.18,.54),dark,.008)
text('Editable workstation title','CENTRAL WORKSTATION',(0,3.035,3.77),.17)
box('Workstation header accent',(0,3.03,3.64),(1,.012,.014),cyan)

collection('02_CENTRAL_WORKSTATION')
box('Workstation woven area rug',(0,1.8,.032),(5.25,3.3,.024),rug,.008)
desk('Central workstation',0,2.65,4.7,.94)
monitor('Panoramic hero monitor',0,3.02,1.66,2.85,.97,'landscape')
monitor('Left analysis display',-1.12,2.43,1.06,.96,.38)
monitor('Right analysis display',1.12,2.43,1.06,.96,.38)
box('Desk pad',(0,2.31,.83),(1.42,.42,.006),rubber,.018)
box('Keyboard',(0,2.34,.852),(.68,.19,.025),black,.009)
for row in range(4):
    for k in range(17):box('Separate keyboard key',(-.30+k*.037,2.27+row*.044,.871),(.031,.034,.008),dark,.002)
ellipsoid('Mouse',(.53,2.27,.85),(.045,.065,.025),black)
for side in [-1,1]:
    sx=side*1.92;box('Nearfield speaker',(sx,2.99,1.02),(.22,.25,.37),black,.018)
    for zz,rr in [(.965,.07),(1.125,.035)]:tube('Speaker driver',(sx,2.854,zz),(sx,2.846,zz),rr,rubber,vertices=32)
chair('Central ergonomic chair',(0,1.50,.04))
path('Visible monitor cable',[(-1.1,3.04,.95),(-1.1,3.12,.73),(-.6,3.10,.63),(-.4,3,.4)],.007,rubber)
box('Desk notebook',(-1.63,2.27,.841),(.26,.19,.025),cream,.004)
tube('Desk pen',(-1.75,2.32,.865),(-1.5,2.34,.865),.004,black)
tube('Ceramic mug',(1.61,2.35,.82),(1.61,2.35,.92),.042,ceramic,vertices=28)
for r,z,mat in [(1.22,4.56,black),(1.16,4.515,amber)]:
    pts=[(r*math.cos(i*math.tau/96),1.8+r*math.sin(i*math.tau/96),z) for i in range(96)]
    path('Ring pendant housing' if mat==black else 'Ring pendant diffuser',pts,.065 if mat==black else .021,mat,True)
for a in [0,2.094,4.189]:tube('Pendant suspension',(1.1*math.cos(a),1.8+1.1*math.sin(a),4.58),(1.1*math.cos(a),1.8+1.1*math.sin(a),5.45),.003,black)

collection('03_ZONE_01_MOTION_SYSTEMS')
def motion():
    box('Capture platform',(0,0,.115),(4.5,3.8,.20),black,.025)
    box('Capture rubber surface',(0,0,.223),(4.38,3.68,.02),rubber,.006)
    for xx in [-2.23,2.23]:box('Platform cyan side',(xx,0,.15),(.014,3.7,.025),cyan)
    for yy in [-1.88,1.88]:box('Platform cyan front rear',(0,yy,.15),(4.45,.014,.025),cyan)
    for xx in [-1.85,1.85]:
        for yy in [-1.45,1.45]:
            tube('Capture frame upright',(xx,yy,.24),(xx,yy,2.85),.04,black)
            box('Capture base plate',(xx,yy,.26),(.25,.25,.04),black,.008)
            for dx in [-.08,.08]:
                for dy in [-.08,.08]:tube('Anchor bolt',(xx+dx,yy+dy,.28),(xx+dx,yy+dy,.30),.012,chrome,vertices=6)
            tube('Frame locking collar',(xx,yy,2.65),(xx,yy,2.73),.058,black)
            box('Capture camera',(xx,yy-.12,2.35),(.19,.16,.13),black,.009)
            tube('Capture lens',(xx,yy-.205,2.35),(xx,yy-.26,2.35),.043,chrome,vertices=24)
            tube('Lens glass',(xx,yy-.26,2.35),(xx,yy-.263,2.35),.033,screenmat,vertices=24)
        tube('Capture upper side rail',(xx,-1.45,2.85),(xx,1.45,2.85),.04,black)
    for yy in [-1.45,1.45]:tube('Capture top crossbar',(-1.85,yy,2.85),(1.85,yy,2.85),.04,black)
    for xx in [-.7,.7]:
        for yy in [-.75,.75]:box('Calibration floor marker',(xx,yy,.237),(.085,.085,.001),cream)
    monitor('Motion tall display',1.25,1.20,1.46,.88,2.24,'skeleton')
    for row in range(2):
        points=[(.91+i*.012,1.143,.45+row*.1+.025*math.sin(i*.7)) for i in range(55)]
        path('Motion signal trace',points,.002,screenwhite)
    text('Motion screen caption','KINETIC / LIVE',(1.25,1.142,2.46),.052,screenwhite)
    for xx,yy in [(-1.4,.6),(-.3,1.2)]:
        for a in [0,2.094,4.189]:tube('Tripod leg',(xx,yy,1.22),(xx+.35*math.cos(a),yy+.35*math.sin(a),.25),.012,chrome)
        tube('Tripod mast',(xx,yy,.7),(xx,yy,1.66),.019,black)
        box('Tripod sensor',(xx,yy,1.72),(.17,.11,.10),black,.008)
assembly('Motion capture station',(-8.55,1.05,0),0,motion)

collection('04_ZONE_02_CLINICAL_THINKING')
box('Clinical walnut back wall',(-4.38,4.95,1.80),(2.82,.12,3.58),walnut,.007)
desk('Clinical desk',-4.30,3.78,2.55,.75)
chair('Clinical desk chair',(-4.28,2.93,.035),-.07,True)
monitor('Clinical analysis display',-4.35,4.00,1.15,.70,.45)
for sx in [-5.15,-4.23]:
    box('Framed anatomy print',(sx,4.84,2.38),(.72,.06,1.03),black,.012)
    box('Print warm paper',(sx,4.80,2.38),(.66,.01,.97),cream)
    for xoff in [-.13,0,.13]:
        path('Anatomy print line',[(sx+xoff,4.786,2.66),(sx+xoff*.3,4.786,2.37),(sx+xoff*1.1,4.786,2.10)],.004,walnut)
    text('Clinical print caption','HUMAN / STUDY',(sx,4.779,1.99),.035,dark)
for z in [1.17,1.72,2.31,2.93]:
    box('Clinical display shelf',(-3.28,4.43,z),(.51,.56,.035),walnut,.007)
    box('Clinical shelf LED',(-3.28,4.24,z-.022),(.45,.015,.012),amber)
books(-3.49,4.38,1.20,7)
books(-3.48,4.38,2.34,6)
def skeleton():
    tube('Skeleton display base',(0,0,.03),(0,0,.065),.23,black,vertices=40)
    tube('Skeleton stand',(0,.08,.06),(0,.08,1.5),.012,chrome)
    skull=ellipsoid('Schematic skull',(0,0,1.66),(.09,.075,.11),cream)
    box('Skeleton mandible',(0,-.018,1.585),(.11,.085,.045),cream,.018)
    for xx in [-.035,.035]:ellipsoid('Skull eye socket',(xx,-.067,1.68),(.021,.011,.022),dark,12,8)
    for i in range(12):ellipsoid('Separate vertebra',(0,.018,1.01+i*.043),(.028,.024,.020),cream,12,8)
    for side in [-1,1]:
        ellipsoid('Pelvis iliac wing',(side*.072,.015,.99),(.078,.047,.083),cream)
        tube('Clavicle',(0,0,1.46),(side*.18,0,1.45),.016,cream)
        for i in range(7):
            z=1.15+i*.039;w=.11+.055*math.sin(i/7*math.pi)
            path('Separate rib',[(0,.036,z+.02),(side*w,.012,z+.025),(side*w,-.055,z),(side*.025,-.072,z-.025)],.009,cream)
        tube('Humerus',(side*.18,0,1.43),(side*.22,-.015,1.14),.019,cream,.014)
        for offset in [-.011,.011]:tube('Forearm bone',(side*.22+offset,-.015,1.12),(side*.24+offset,-.04,.88),.009,cream)
        ellipsoid('Skeletal hand',(side*.24,-.04,.835),(.025,.016,.06),cream)
        tube('Femur',(side*.075,.015,.95),(side*.10,.01,.55),.024,cream,.018)
        ellipsoid('Patella',(side*.10,-.017,.53),(.025,.018,.026),cream)
        tube('Tibia',(side*.10,.012,.52),(side*.105,.018,.13),.018,cream,.012)
        tube('Fibula',(side*.13,.02,.52),(side*.135,.025,.13),.009,cream)
        ellipsoid('Foot bones',(side*.11,-.045,.105),(.035,.10,.025),cream)
assembly('Editable schematic anatomy model',(-5.39,3.13,.04),0,skeleton)

collection('05_ZONE_03_CREATIVE_ENGINEERING')
box('Engineering walnut back wall',(4.99,4.94,1.81),(4.3,.14,3.6),walnut,.008)
desk('Engineering workbench',4.98,4.07,3.95,.83)
box('Tool pegboard',(4.98,4.80,2.02),(3.84,.065,1.75),dark,.006)
# Pegboard holes are dark recessed discs, separately editable and regular in scale.
for ix in range(38):
    for iz in range(14):
        tube('Pegboard perforation',(3.17+ix*.098,4.761,1.37+iz*.105),(3.17+ix*.098,4.755,1.37+iz*.105),.007,rubber,vertices=8)
for z in [1.29,2.91,3.33]:
    box('Engineering timber shelf',(4.98,4.54,z),(4.0,.56,.047),walnut,.009)
    box('Engineering shelf diffuser',(4.98,4.30,z-.03),(3.90,.018,.014),amber)
for i in range(10):
    xx=3.30+i*.365;zz=2.05+(i%3)*.19
    path('Pegboard tool hook',[(xx,4.747,zz+.11),(xx,4.68,zz+.11),(xx,4.66,zz)],.008,chrome)
    if i%3==0:
        tube('Camera lens equipment',(xx,4.68,zz-.04),(xx,4.49,zz-.04),.08,black,vertices=32)
        tube('Lens focus ring',(xx,4.57,zz-.04),(xx,4.54,zz-.04),.085,rubber,vertices=32)
    elif i%3==1:
        tube('Tool metal shaft',(xx,4.63,zz),(xx,4.63,zz-.30),.012,chrome)
        box('Tool grip',(xx,4.63,zz-.25),(.065,.065,.15),black,.015)
    else:
        box('Hung camera body',(xx,4.65,zz-.09),(.20,.10,.13),black,.008)
        tube('Camera lens',(xx,4.59,zz-.09),(xx,4.51,zz-.09),.045,chrome,vertices=24)
monitor('Engineering laptop display',4.0,4.02,1.08,.66,.42)
box('Engineering laptop keyboard',(4.0,3.78,.83),(.66,.30,.02),black,.008)
for i in range(6):
    box('Workbench storage bin',(3.3+i*.55,4.5,3.04),(.35,.28,.20),black,.009)
chair('Engineering task chair',(5.52,3.06,.04),.08)
path('Articulated lamp arm',[(6.25,3.9,.83),(6.25,3.9,1.1),(6.0,3.86,1.42),(5.76,3.80,1.30)],.018,black)
box('Engineering lamp shade',(5.76,3.80,1.29),(.30,.13,.04),black,.02)
box('Prototype electronics mat',(4.95,3.88,.825),(.52,.32,.006),rubber,.005)
for i in range(5):box('Prototype component',(4.79+i*.07,3.86,.85),(.045,.10,.035),chrome,.004)

collection('06_ZONE_04_PROJECTS')
for yy in [-.3,2.0,4.3]:
    box('Meeting glass partition post',(7.43,yy,1.78),(.055,.055,3.56),black,.003)
    if yy<4:box('Meeting partition glass',(7.43,yy+1.12,1.78),(.012,2.15,3.5),glass)
box('Projects woven rug',(9.45,1.65,.036),(3.9,4.2,.03),rug,.008)
box('Meeting table walnut top',(9.45,1.8,.80),(2.9,1.15,.065),walnut,.035)
for xx in [8.45,10.45]:
    for yy in [1.4,2.2]:tube('Meeting table leg',(xx,yy,.06),(xx,yy,.77),.032,black)
for xx in [8.6,9.45,10.3]:
    chair('Meeting chair south',(xx,.80,.045),math.pi,True)
    chair('Meeting chair north',(xx,2.8,.045),0,True)
monitor('Projects presentation screen',9.45,4.55,1.85,2.35,1.3,'landscape')
for xx in [8.6,10.1]:
    box('Meeting notebook',(xx,1.80,.842),(.22,.17,.025),cream,.003)
    tube('Meeting mug',(xx+.2,1.8,.837),(xx+.2,1.8,.93),.038,ceramic,vertices=24)
for z,r in [(3.25,.60),(3.225,.55)]:
    path('Meeting pendant rim',[(9.45+r*math.cos(i*math.tau/64),1.8+r*.6*math.sin(i*math.tau/64),z) for i in range(64)],.032,black if z>3.24 else amber,True)
for xx in [9.05,9.85]:tube('Meeting pendant cable',(xx,1.8,3.28),(xx,1.8,4.9),.003,black)
box('Projects ceiling accent',(9.4,4.8,3.52),(3.6,.025,.012),violet)

collection('07_LOUNGE_AND_PLANTS')
box('Lounge woven rug',(-.6,-2.65,.035),(7.4,3.5,.025),rug,.01)
def sofa():
    box('Sofa upholstered base',(0,0,.32),(3.4,1.02,.36),leather,.14)
    box('Sofa back',(0,.37,.65),(3.38,.25,.68),leather,.115)
    for side in [-1,1]:box('Sofa arm',(side*1.59,0,.55),(.28,.98,.57),leather,.12)
    for i in [-1,0,1]:
        box('Sofa separate seat cushion',(i*.98,-.10,.53),(.95,.79,.17),leather,.075)
        box('Sofa separate back cushion',(i*.98,.24,.78),(.95,.18,.50),leather,.07)
    for xx in [-1.35,1.35]:
        for yy in [-.3,.3]:tube('Sofa foot',(xx,yy,.04),(xx,yy,.20),.025,black)
assembly('Foreground leather sofa',(-3.4,-3.25,.04),-.06,sofa)
def loungechair():
    box('Lounge seat',(0,0,.39),(1.06,1.0,.23),leather,.13)
    back=box('Lounge reclining back',(0,.36,.85),(1.05,.27,.98),leather,.14);back.rotation_euler[0]=-.13
    for side in [-1,1]:box('Lounge arm',(side*.48,.02,.59),(.19,.9,.35),leather,.09)
    for xx in [-.36,.36]:tube('Lounge chair foot',(xx,-.35,.05),(xx,.30,.32),.024,black)
assembly('Foreground lounge chair',(4.9,-3.45,.04),-.45,loungechair)
tube('Oval coffee table top',(-.3,-2.8,.36),(-.3,-2.8,.41),1.0,black,vertices=80).scale.y=.55
for xx in [-.9,.3]:tube('Coffee table leg',(xx,-2.8,.05),(xx,-2.8,.36),.025,black)
for i in range(3):box('Coffee table art book',(-.60+i*.20,-2.8,.43+i*.025),(.40,.28,.025),cream if i==1 else dark,.005)
for x,y,h in [(-11.0,-.8,1.65),(-6.03,2.85,1.5),(-2.75,3.8,1.7),(2.74,3.45,1.8),(7.15,3.75,1.75),(11.15,-.5,1.65),(-3.15,4.25,.68),(6.7,4.3,.72),(.58,-2.85,.43)]:plant('Studio plant',x,y,h)

collection('08_EXTERIOR')
sky=bpy.data.materials.new('Blue hour vertical sky gradient');sky.use_nodes=True
nt=sky.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission')
coord=nt.nodes.new('ShaderNodeTexCoord');sep=nt.nodes.new('ShaderNodeSeparateXYZ');ramp=nt.nodes.new('ShaderNodeValToRGB')
stops=[(0,(.7,.24,.14,1)),(.18,(.38,.15,.25,1)),(.29,(.16,.17,.36,1)),(.5,(.055,.105,.28,1)),(1,(.012,.029,.08,1))]
cr=ramp.color_ramp;cr.elements.remove(cr.elements[1]);cr.elements[0].position=0;cr.elements[0].color=stops[0][1]
for pos,col in stops[1:]:cr.elements.new(pos).color=col
nt.links.new(coord.outputs['Generated'],sep.inputs[0]);nt.links.new(sep.outputs['Z'],ramp.inputs[0]);nt.links.new(ramp.outputs[0],em.inputs['Color']);em.inputs['Strength'].default_value=.65;nt.links.new(em.outputs[0],out.inputs['Surface'])
box('Distant sky backdrop',(0,115,25),(260,.1,90),sky)
for layer,(yy,base,amp,col) in enumerate([(87,4.5,7,(.17,.20,.32)),(67,2.9,5.0,(.10,.15,.25)),(46,1.4,3.2,(.055,.09,.15))]):
    mat=material('Atmospheric mountain layer '+str(layer),col,.95,0,.35)
    pts=[(-80,-5)]
    for i in range(81):
        x=-80+i*2
        height=base+amp*(.34+.34*math.sin(i*.85+layer)+.17*math.sin(i*2.3)+.15*random.random())
        pts.append((x,height))
    pts.append((80,-5));poly('Editable distant mountain silhouette',pts,yy,mat)
citymat=material('Distant city buildings',(.031,.047,.07),.9,0,.16)
citylight=material('Distant warm city windows',(.95,.55,.25),.6,0,2.5)
for i in range(90):
    x=random.uniform(-43,43);y=random.uniform(19,37);h=random.uniform(.35,2.65);w=random.uniform(.25,.75)
    box('Distant city building',(x,y,h/2-.35),(w,.45,h),citymat)
    for j in range(random.randint(2,5)):
        zz=.05+j*.32
        if zz<h-.35:box('Distant city window',(x,y-.23,zz),(.055,.005,.075),citylight)
box('Exterior terrace',(0,8,-.055),(28,5,.12),dark)

collection('09_LIGHTING')
area('Large soft warm interior',(0,-.2,4.65),(0,1,0),1150,(1,.74,.48),8,4)
area('Camera-side soft bounce',(0,-7,4.3),(0,2.5,1),750,(1,.8,.62),9,4)
area('Cool evening window source',(0,8,5.6),(0,1.8,1.2),1700,(.28,.45,1),12,4)
area('Ring pendant downlight',(0,1.8,4.47),(0,1.8,.3),230,(1,.57,.28),2.2)
for x,y,w,energy in [(-4.4,4.2,2.4,210),(4.95,4.25,3.8,370),(9.45,1.8,3,170)]:
    area('Warm zone task light',(x,y,3.20),(x,y-.35,.6),energy,(1,.59,.29),w,.4)
for xx in [-10.7,-6.4]:area('Motion strip bounce',(xx,1,.27),(xx,1,1.4),25,(.025,.36,1),.06,3.5)
area('Clinical skeleton task light',(-5.4,3.15,3.05),(-5.39,3.13,1),70,(1,.7,.4),.5)
area('Monitor spill',(0,2.9,1.65),(0,1.4,1.1),9,(.28,.5,1),2.5,.8)

collection('10_CAMERAS')
def camera(name,loc,target,lens=28):
    data=bpy.data.cameras.new(name);data.lens=lens;data.sensor_width=36;data.clip_end=300
    ob=bpy.data.objects.new(name,data);COL.objects.link(ob);ob.location=loc;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();return ob
hero=camera('CAM_Hero_Reference_Fit',(0,-15.2,3.05),(0,2.5,2.15),28)
hero.data.lens=27
scene.camera=hero
for name,loc,target,lens in [
    ('CAM_01_Motion_Systems',(-8.55,-5,2.35),(-8.55,1.7,1.5),34),
    ('CAM_02_Clinical_Thinking',(-4.35,-2.2,2.2),(-4.35,4.1,1.55),42),
    ('CAM_03_Creative_Engineering',(4.8,-2.7,2.2),(4.95,4.2,1.65),38),
    ('CAM_04_Projects',(9.3,-4,2.25),(9.45,2.6,1.45),35)]:camera(name,loc,target,lens)

# A deliberately small compositing contribution; geometry/light problems stay visible.
scene.use_nodes=True
nt=scene.node_tree;nt.nodes.clear();rl=nt.nodes.new('CompositorNodeRLayers');gl=nt.nodes.new('CompositorNodeGlare')
gl.glare_type='FOG_GLOW';gl.quality='MEDIUM';gl.threshold=2;gl.mix=-.96
out=nt.nodes.new('CompositorNodeComposite');nt.links.new(rl.outputs['Image'],gl.inputs['Image']);nt.links.new(gl.outputs['Image'],out.inputs['Image'])

scene['project']='Kinetic Studio / editable photoreal proof'
scene['source_method']='Direct procedural reconstruction from user concept boards; no Spline AI or image-generation substitute.'
scene['camera_fit']='Inferred frontal anchor fit. Dimensions and lens are design assumptions, not surveyed values.'
scene['proof_limitations']='First composition and lighting proof; schematic anatomy, procedural foliage, and layered exterior require later asset refinement.'
scene['native_spline_preserved']=True

anchors={
    'ring_center':(0,1.8,4.53),
    'workstation_center':(0,2.65,.82),
    'motion_center':(-8.55,1.05,.24),
    'clinical_center':(-4.38,3.78,.82),
    'engineering_center':(4.98,4.07,.82),
    'projects_center':(9.45,1.8,.84),
}
bpy.context.view_layer.update()
projected={}
for k,v in anchors.items():
    p=world_to_camera_view(scene,hero,Vector(v));projected[k]={'x':p.x,'y_from_top':1-p.y,'depth':p.z}
required=['03_ZONE_01_MOTION_SYSTEMS','04_ZONE_02_CLINICAL_THINKING','05_ZONE_03_CREATIVE_ENGINEERING','06_ZONE_04_PROJECTS']
assert all(len(bpy.data.collections[n].objects)>10 for n in required)
assert all(0<projected[k]['x']<1 for k in anchors)
assert scene.camera==hero

source_hashes={}
for name in ['The Kinetic Studio Concept Board-2.png','The Kinetic Studio_ Four-Zone Creative Hub-3.png']:
    p=PROJECT/name;source_hashes[name]=hashlib.sha256(p.read_bytes()).hexdigest()
report={
    'status':'built-awaiting-render',
    'blender_version':bpy.app.version_string,'devices':devices,'cycles_device':scene.cycles.device,
    'engine':scene.render.engine,'samples':scene.cycles.samples,'resolution':[scene.render.resolution_x,scene.render.resolution_y],
    'objects':len(scene.objects),'mesh_objects':sum(o.type=='MESH' for o in scene.objects),'materials':len(bpy.data.materials),
    'collections':{c.name:len(c.objects) for c in scene.collection.children},
    'camera':{'name':hero.name,'position':list(hero.location),'lens_mm':hero.data.lens,'anchor_projection':projected,
              'reference_assumptions':'Primary upper hero panel, approximate 3.56:1 crop; inferred room width 23 m and nominal eye height 3.05 m.'},
    'source_hashes':source_hashes,
    'asset_provenance':'All geometry, shaders, and display graphics directly authored by build_kinetic_studio.py; no third-party asset dependencies.',
    'limitations':scene['proof_limitations'],
}
ROOT.mkdir(parents=True,exist_ok=True)
blend=ROOT/'kinetic-studio-proof-v001.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(blend))
scene.render.filepath=str(ROOT/'kinetic-studio-proof-v001.png')
render_start=time.time()
bpy.ops.render.render(write_still=True)
report.update(status='rendered-awaiting-visual-review',render_seconds=round(time.time()-render_start,2),total_seconds=round(time.time()-START,2),blend=str(blend),render=scene.render.filepath)
(ROOT/'proof-verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('KINETIC_STUDIO_PROOF_RENDERED',json.dumps({'blend':str(blend),'png':scene.render.filepath,'objects':len(scene.objects),'seconds':report['render_seconds']}))
