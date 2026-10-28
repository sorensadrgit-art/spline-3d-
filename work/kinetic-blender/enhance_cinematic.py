"""Versioned cinematic refinement. Run with the project's isolated official bpy runtime."""
import ast
import hashlib
import json
import math
import random
import time
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parent
random.seed(271028)
bpy.context.preferences.filepaths.use_scripts_auto_execute = False
source = ROOT / 'kinetic-studio-proof-v004.blend'
source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(source), load_ui=False)
scene = bpy.context.scene
scene.render.use_simplify = True
scene.render.simplify_subdivision_render = 1
scene.render.simplify_subdivision = 1
hero = scene.camera
hero_matrix = [list(row) for row in hero.matrix_world]
tree = ast.parse((ROOT / 'build_kinetic_studio.py').read_text(encoding='utf-8'))
helpers = {'box', 'tube', 'ellipsoid', 'path', 'finish', 'move_to_collection', 'material', 'area'}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in helpers], type_ignores=[]), 'existing_helpers', 'exec'))

def collection(name):
    global COL
    COL = bpy.data.collections.new(name)
    scene.collection.children.link(COL)
    return COL

def label(name, body, loc, size, mat, align='LEFT'):
    data = bpy.data.curves.new(name, 'FONT')
    data.body, data.size, data.align_x = body, size, align
    data.extrude = .00025
    ob = bpy.data.objects.new(name, data)
    COL.objects.link(ob)
    ob.location, ob.rotation_euler = loc, (math.pi / 2, 0, 0)
    ob.data.materials.append(mat)
    return ob

black = bpy.data.materials['Graphite powder coat']
walnut = bpy.data.materials['Oiled walnut cabinetry']
chrome = bpy.data.materials['Brushed aluminum']
rubber = bpy.data.materials['Rubber and cable jacket']
paper = bpy.data.materials['Warm paper and bone']
warm = material('V005 warm ivory lettering', (.62, .48, .31), .48)
copper = material('V005 brushed copper', (.32, .13, .055), .34, .78)
green = material('V005 circuit solder mask', (.012, .11, .065), .4)
fabric = material('V005 woven warm grey fabric', (.14, .13, .11), .83)
nt = fabric.node_tree
noise = nt.nodes.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value = 280
bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = .22; bump.inputs['Distance'].default_value = .0005
nt.links.new(noise.outputs['Fac'], bump.inputs['Height']); nt.links.new(bump.outputs[0], nt.nodes['Principled BSDF'].inputs['Normal'])
collection('15_CINEMATIC_ARCHITECTURE')

# Slim integrated wayfinding retains native text and the original four-zone order.
for i, (x, w, color) in enumerate([(-8.6, 5.2, 'cyan'), (-4.4, 2.75, 'warm'), (4.95, 4.45, 'warm'), (9.45, 3.85, 'violet')], 1):
    num = f'{i:02}'
    header = bpy.data.objects['Zone header ' + num]
    header.scale.z = .38; header.scale.x = .79; header.location.z = 3.69
    title = bpy.data.objects['Editable zone title ' + num]
    title.data.size = .092; title.location.z = 3.67
    number = bpy.data.objects['Editable zone number ' + num]
    number.data.size = .145; number.location.x = x - w * .38 + .15; number.location.z = 3.65
    accent = bpy.data.objects['Header accent ' + num]
    accent.scale.x = .58; accent.location.z = 3.59
for name in ['Workstation architectural header', 'Workstation header accent']:
    ob = bpy.data.objects[name]; ob.hide_render = True; ob.hide_set(True)
title = bpy.data.objects['Editable workstation title']
title.data.size = .105; title.location.z = 3.58

# Joints, soft reveal lines, and cabinet construction add depth at human scale.
for x, y, width in [(-4.38, 4.77, 2.7), (4.99, 4.73, 4.1)]:
    for dx in [-width / 2 + .035, width / 2 - .035]:
        box('Walnut cabinet return', (x + dx, y - .13, 1.72), (.065, .3, 3.4), walnut, .006)
    for z in [.18, .46, .70]:
        for col in range(3):
            xx = x - width / 2 + width / 6 + col * width / 3
            box('Inset walnut drawer front', (xx, y - .34, z), (width / 3 - .025, .05, .20), walnut, .005)
            box('Recessed copper drawer pull', (xx, y - .375, z + .035), (.21, .012, .009), copper, .003)
    box('Cabinet shadow toe kick', (x, y - .27, .08), (width - .16, .18, .10), black, .005)
for x in [-11.5, -5.9, -2.8, 2.8, 7.3, 11.5]:
    box('Steel column base shoe', (x, 3.25, .12), (.23, .3, .24), black, .009)
    for z in [.08, 4.68]:
        for dx in [-.07, .07]: tube('Architectural exposed fixing', (x+dx, 3.115, z), (x+dx, 3.10, z), .009, chrome, vertices=6)
for x in [-9.6, -7.7, -3.9, -.9, .9, 4.7, 6.8, 8.8, 10.6]:
    box('Rear glazing rubber gasket', (x+.044, 5.638, 2.65), (.012, .014, 5.12), rubber, .002)

collection('16_CINEMATIC_WORKSTATION')
box('Workstation underdesk cable tray', (0, 2.91, .66), (2.3, .18, .065), black, .009)
for i in range(6):
    path('Organized workstation cable', [(-.9+i*.34, 2.99, 1.26), (-.9+i*.34, 3.13, .8), (-.6+i*.22, 2.99, .66)], .0045, rubber)
for side in [-1, 1]:
    sx = side * 1.82
    box('Speaker isolation foam', (sx, 2.99, .835), (.24, .25, .024), rubber, .008)
    tube('Speaker tweeter trim', (side*1.92, 2.842, 1.125), (side*1.92, 2.834, 1.125), .038, copper, vertices=40)
for x in [-.30, .30]:
    tube('Monitor arm upright', (x, 3.14, .84), (x, 3.14, 1.44), .022, black)
    tube('Monitor VESA joint', (x, 3.14, 1.4), (x, 3.04, 1.49), .035, chrome)
box('Audio interface', (.95, 2.27, .875), (.27, .18, .075), chrome, .007)
for x in [.87, .95, 1.03]: tube('Audio interface knob', (x, 2.173, .875), (x, 2.16, .875), .013, black, vertices=24)
for x in [-.20, .20]:
    box('Workstation chair arm pad detail', (x, 1.49, .75), (.075, .26, .035), rubber, .014)
path('Desk task light arm', [(-1.55, 3.02, .86), (-1.55, 3.02, 1.22), (-1.30, 2.88, 1.5), (-1.0, 2.81, 1.49)], .014, black)
tube('Desk light hinge', (-1.55, 3, 1.22), (-1.55, 3.04, 1.22), .028, copper)
box('Desk task light head', (-.98, 2.81, 1.48), (.34, .06, .035), black, .01)

collection('17_CINEMATIC_ZONE_DETAILS')
# Motion: recognizable lenses, calibration targets, connection cables, and a storage case.
box('Motion instrument road case', (-10.0, 2.5, .42), (.9, .54, .38), black, .026)
for x in [-10.33, -9.67]:
    box('Road case latch', (x, 2.216, .43), (.045, .02, .07), chrome, .006)
    for y in [2.29, 2.71]: ellipsoid('Road case corner protector', (x, y, .59), (.038, .038, .025), chrome)
for x in [-10.40, -6.70]:
    path('Motion sensor data cable', [(x, -.40, 2.35), (x+.05, -.39, 1.7), (x+.05, -.39, .33), (x+.23, .3, .25)], .006, rubber)
for x, y in [(-9.8, .4), (-8.4, 1.4), (-7.7, .1)]:
    for i in [-1, 1]: box('Capture floor calibration cross', (x, y, .241), (.14 if i==1 else .014, .014 if i==1 else .14, .002), paper)
label('Motion illustrative caption', 'ILLUSTRATIVE MOTION STUDY', (-7.70, 2.184, .36), .032, warm)

# Clinical: detailed skeletal study, not a clinical/anatomical certification claim.
skeleton = bpy.data.objects['Editable schematic anatomy model']
skull = bpy.data.objects.get('Schematic skull')
if skull:
    skull.scale.x *= .88; skull.scale.z *= 1.06
for child in skeleton.children:
    if 'Skeletal hand' in child.name:
        child.scale *= .5
for side in [-1, 1]:
    for j in range(5):
        x = side * (.24 + (j-2)*.010)
        for k in range(3):
            ob = tube('Separate finger phalanx', (x, -.044, .856-k*.018), (x+side*.002, -.047, .842-k*.018), .0038, paper, .003)
            ob.parent = skeleton
    for joint in [(side*.18, 0, 1.43), (side*.22, -.015, 1.13), (side*.075, .015, .95), (side*.10, .01, .54)]:
        ob=ellipsoid('Skeletal articular epiphysis', joint, (.027,.027,.032), paper); ob.parent=skeleton
    for j in range(5):
        ob=tube('Separate foot metatarsal', (side*.11+(j-2)*.009, -.02, .10), (side*.11+(j-2)*.011, -.125, .09), .0045, paper); ob.parent=skeleton
for k in range(16):
    ob=ellipsoid('Study model vertebral process', (0,.045,1.02+k*.031), (.010,.030,.009), paper,12,8); ob.parent=skeleton
for x in [-5.15,-4.23]:
    for ob in list(scene.objects):
        if ob.name.startswith('Anatomy print line'):
            ob.hide_render=True
    label('Educational anatomy print title', 'KINEMATIC STUDY', (x-.27,4.775,2.79), .045, black)
    for i in range(20):
        z=2.65-i*.023
        ellipsoid('Illustrative vertebral print detail',(x+.013*math.sin(i*.4),4.779,z),(.023,.0015,.008),walnut,12,6)
    for side in [-1,1]:
        for i in range(8):
            z=2.59-i*.029; w=.08+.055*math.sin(i*.4)
            path('Illustrative rib print',[(x,4.775,z+.01),(x+side*w,4.775,z),(x+side*.025,4.775,z-.023)],.0017,walnut)
    label('Illustrative print footer','FORM / RANGE / MOTION',(x-.25,4.775,2.06),.026,black)
label('Clinical model disclosure','ILLUSTRATIVE STUDY MODEL',(-5.68,3.02,.12),.026,warm)

# Engineering: one coherent instrument prototype instead of anonymous repeated blocks.
box('Engineering prototype PCB', (5.0,3.86,.865), (.40,.29,.018), green,.004)
for i in range(7):
    x=4.84+i*.045
    box('PCB surface mount component',(x,3.82,.883),(.022,.045,.018),black,.003)
    for y in [3.78,3.86]:box('PCB copper connection',(x,y,.88),(.012,.012,.004),copper)
for j in range(5):path('PCB conductor trace',[(4.83,3.76+j*.04,.878),(5.05,3.76+j*.04,.878),(5.15,3.80+j*.03,.878)],.0012,copper)
box('Prototype actuator base',(5.77,4.0,.91),(.35,.3,.15),chrome,.014)
arm_points=[(5.77,4,1.0),(5.77,4,1.25),(5.53,3.96,1.53),(5.31,3.89,1.38)]
for a,b in zip(arm_points,arm_points[1:]):tube('Editable prototype actuator link',a,b,.037,black,.027,24)
for p in arm_points:ellipsoid('Actuator copper joint',p,(.055,.05,.055),copper)
for side in [-1,1]:tube('Prototype gripper',(5.31,3.89,1.38),(5.31+side*.045,3.89,1.27),.009,chrome)
path('Actuator wiring loom',[(5.78,4.03,.92),(5.83,4.03,1.25),(5.56,4.0,1.58),(5.29,3.92,1.40)],.007,rubber)
for i in range(4):
    x=3.5+i*.13
    tube('Engineering precision driver',(x,4.63,2.15),(x,4.63,1.85),.008,chrome)
    tube('Precision driver copper grip',(x,4.63,1.96),(x,4.63,1.85),.020,copper,vertices=24)
box('Engineering sample caliper rail',(6.43,4.64,2.06),(.30,.025,.018),chrome,.002)
for x in [6.34,6.48]:box('Engineering caliper jaw',(x,4.64,2.09),(.018,.025,.10),chrome,.002)
label('Prototype desk identifier','KS / ACTUATOR 01',(5.52,3.829,.98),.028,warm)

# Projects: physical pin-up boards and presentation material with honest example labels.
for x in [8.35,10.55]:
    box('Projects pin-up frame',(x,4.9,2.45),(.65,.055,.9),black,.007)
    box('Projects warm pin-up paper',(x,4.865,2.45),(.61,.008,.86),paper)
    label('Projects printed heading','DESIGN / STUDY',(x-.25,4.855,2.77),.045,black)
    for i in range(4):
        box('Projects diagram rule',(x,4.85,2.6-i*.07),(.47,.003,.004),walnut)
    label('Projects sample caption','CONCEPT ITERATION',(x-.25,4.85,2.15),.026,black)
for x in [8.6,9.45,10.3]:
    for y in [.80,2.8]:
        box('Meeting chair woven seat',(x,y,.49),(.43,.42,.045),fabric,.035)
        for dx in [-.22,.22]:tube('Meeting chair polished arm support',(x+dx,y,.49),(x+dx,y,.69),.012,chrome)
        box('Meeting chair padded arm',(x-.22,y,.70),(.045,.29,.026),rubber,.01)
box('Meeting materials sample tray',(9.4,1.8,.852),(.38,.28,.024),black,.009)
for i,mat in enumerate([walnut,chrome,copper]):box('Meeting material sample',(9.27+i*.12,1.8,.875),(.095,.21,.012),mat,.003)

collection('18_CINEMATIC_LOUNGE')
for loc,angle in [((-4.23,-3.03,.91),-.16),((-2.57,-3.09,.91),.21)]:
    ob=box('Woven sofa scatter cushion',loc,(.43,.19,.42),fabric,.065);ob.rotation_euler=(.11,0,angle)
for name in ['Large soft warm interior','Camera-side soft bounce']:
    light=bpy.data.objects[name].data;light.energy=430 if name.startswith('Large') else 230
area('Lounge photographic softbox',(-2,-3.8,3.8),(-2,-2.5,.5),200,(1,.72,.48),4,2)
area('Engineering equipment edge light',(6.1,3.6,3.1),(5.3,3.9,1.0),65,(1,.77,.56),1.2,.4)
area('Motion instrument soft edge',(-9.6,-.1,3.8),(-8.9,1.2,1.0),95,(.60,.72,1),2,.4)
# Larger softboxes are invisible to camera rays, but their illumination remains physical.
for ob in scene.objects:
    if ob.type=='LIGHT' and hasattr(ob,'visible_camera'):
        ob.visible_camera=False
        ob.visible_glossy=False
        ob.visible_transmission=False
for m in bpy.data.materials:
    if m.name.startswith('Alpine'):
        m['landscape_origin']='Artist-authored editable terrain; no geographic accuracy claim.'
for ob in scene.objects:
    if ob.name.startswith('Distant city building'):
        ob.scale.z*=random.uniform(.65,1.25);ob.scale.x*=random.uniform(.7,1.3)

prefs=bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type='OPTIX';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='OPTIX'
scene.cycles.device='GPU' if any(d.use for d in prefs.devices) else 'CPU'
scene.cycles.samples=128;scene.cycles.use_denoising=True
scene.cycles.adaptive_threshold=.015
scene.render.resolution_percentage=100
scene.camera=hero
scene.render.resolution_x=3840;scene.render.resolution_y=1080
scene.render.filepath=str(ROOT/'kinetic-studio-proof-v005.png')
scene['refinement_revision']='v005'
scene['proof_limitations']='Camera is inferred, landscape is artistic, anatomy and screen data are illustrative. Web copy is a separate delivery asset.'
assert hero_matrix==[list(row) for row in hero.matrix_world]
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'kinetic-studio-proof-v005.blend'))
render_start=time.time();bpy.ops.render.render(write_still=True)
outputs={'home':scene.render.filepath}
targets={
    'motion':('CAM_01_Motion_Systems',(-8.4,-5.2,2.25),(-8.55,1.4,1.55),30),
    'clinical':('CAM_02_Clinical_Thinking',(-4.5,-1.4,2.0),(-4.4,4.0,1.70),38),
    'engineering':('CAM_03_Creative_Engineering',(4.4,-1.8,2.05),(4.95,4.2,1.75),34),
    'projects':('CAM_04_Projects',(9.1,-3.0,2.0),(9.45,2.7,1.6),30),
}
camera_data={}
for key,(name,position,target,lens) in targets.items():
    cam=bpy.data.objects[name];cam.location=position;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=lens
    scene.camera=cam;scene.render.resolution_x=1600;scene.render.resolution_y=1000
    scene.render.filepath=str(ROOT/f'kinetic-studio-{key}-v005.png');scene.cycles.samples=96
    bpy.ops.render.render(write_still=True)
    outputs[key]=scene.render.filepath
    camera_data[key]={'position':list(position),'target':list(target),'lens':lens}
scene.camera=hero;scene.render.resolution_x=3840;scene.render.resolution_y=1080;scene.cycles.samples=128
scene.render.filepath=outputs['home']
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'kinetic-studio-proof-v005.blend'))
assert source_hash==hashlib.sha256(source.read_bytes()).hexdigest()
report={'revision':'v005','source_v004_sha256':source_hash,'hero_matrix':hero_matrix,'hero_lens':hero.data.lens,'render_seconds':round(time.time()-render_start,2),'outputs':outputs,'cameras':camera_data,'objects':len(scene.objects),'materials':len(bpy.data.materials),'device':[d.name for d in prefs.devices if d.use],'limitations':scene['proof_limitations']}
(ROOT/'proof-verification-v005.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('KINETIC_CINEMATIC_V005_RENDERED',json.dumps(report),flush=True)
