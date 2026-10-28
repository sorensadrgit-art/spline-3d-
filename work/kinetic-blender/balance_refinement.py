"""Correct the plant scale and landscape softness observed in the v003 render."""
import bpy,math,json,time,ast,random
from pathlib import Path
from mathutils import Vector,Matrix,noise
ROOT=Path(__file__).resolve().parent
bpy.context.preferences.filepaths.use_scripts_auto_execute=False
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'kinetic-studio-proof-v003.blend'),load_ui=False)
scene=bpy.context.scene;hero=scene.camera
tree=ast.parse((ROOT/'build_kinetic_studio.py').read_text(encoding='utf-8'))
helpers={'finish','tube','path','material'}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in helpers],type_ignores=[]),'scene_helpers','exec'))
COL=bpy.data.collections['12_REFINED_PLANTS'];ceramic=bpy.data.materials['Stoneware planter'];soil=bpy.data.materials['Planter soil']
heights=[1.7,1.55,1.85,1.95,1.65,1.8]
for i,root in enumerate(sorted([o for o in scene.objects if o.type=='EMPTY' and o.name.startswith('Broadleaf floor plant')],key=lambda o:o.name)):
    leaves=None
    for child in root.children:
        if 'leaves' in child.name:leaves=child
        else:child.hide_render=True;child.hide_set(True)
    assert leaves is not None
    points=[leaves.matrix_world@Vector(c) for c in leaves.bound_box]
    lo=Vector(tuple(min(p[a] for p in points) for a in range(3)));hi=Vector(tuple(max(p[a] for p in points) for a in range(3)))
    center=Vector(((lo.x+hi.x)/2,(lo.y+hi.y)/2,lo.z))
    x,y,z=root.location
    target_h=heights[i]-.54;target_w=.88 if i in [2,3] else .76
    scale=Matrix.Diagonal((target_w/(hi.x-lo.x),target_w/(hi.y-lo.y),target_h/(hi.z-lo.z),1))
    leaves.matrix_world=Matrix.Translation((x,y,.54))@scale@Matrix.Translation(-center)@leaves.matrix_world
    tube('Slim stoneware floor planter',(x,y,.035),(x,y,.55),.19,ceramic,.235,48)
    tube('Real-scale planter soil',(x,y,.53),(x,y,.538),.222,soil,vertices=40)
    path('Stoneware planter rim',[(x+.232*math.cos(a*math.tau/64),y+.232*math.sin(a*math.tau/64),.548) for a in range(64)],.007,ceramic,True)

# Sharper ridged terrain retains real mesh depth, snow breakup, and editable vertices.
for layer,ob in enumerate(sorted([o for o in scene.objects if o.name.startswith('Editable alpine range')],key=lambda o:o.name)):
    ys=[v.co.y for v in ob.data.vertices];center=(max(ys)+min(ys))/2;span=max(ys)-min(ys)
    values=[]
    for vertex in ob.data.vertices:
        x,y=vertex.co.x,vertex.co.y
        value=noise.ridged_multi_fractal(Vector((x*.034,y*.049,layer*3.173)),.85,2.1,5,1,2)
        values.append(value)
    low,high=min(values),max(values)
    amp=[27,19,12][layer];base=[-8,-8,-7][layer]
    for vertex,value in zip(ob.data.vertices,values):
        x,y=vertex.co.x,vertex.co.y
        normalized=(value-low)/(high-low)
        envelope=math.exp(-((y-center)/(span*.34))**2)
        alpine_peaks=.10*math.exp(-((x-7)/16)**2)+.07*math.exp(-((x+46)/12)**2)
        vertex.co.z=base+amp*envelope*(.18+.82*normalized+alpine_peaks)
    ob.data.update()
    # Keep snow restricted to the high fractured ridges of the distant range.
    nt=ob.data.materials[0].node_tree
    for node in nt.nodes:
        if node.type=='MAP_RANGE':
            node.inputs['From Min'].default_value=8 if layer==0 else 15
            node.inputs['From Max'].default_value=11 if layer==0 else 18

# Keep HDR sky detail while restoring the reference's cool evening hue.
nt=scene.world.node_tree
hdr=next(n for n in nt.nodes if n.type=='TEX_ENVIRONMENT')
backgrounds=[n for n in nt.nodes if n.type=='BACKGROUND']
lightbg,visiblebg=backgrounds
lightbg.inputs['Strength'].default_value=.035
visiblebg.inputs['Strength'].default_value=.30
tint=nt.nodes.new('ShaderNodeMixRGB');tint.blend_type='MULTIPLY';tint.inputs[0].default_value=1;tint.inputs[2].default_value=(.26,.39,.78,1)
nt.links.new(hdr.outputs['Color'],tint.inputs[1]);nt.links.new(tint.outputs[0],visiblebg.inputs['Color'])
ray=next(n for n in nt.nodes if n.type=='LIGHT_PATH');mix=next(n for n in nt.nodes if n.type=='MIX_SHADER')
ray_union=nt.nodes.new('ShaderNodeMath');ray_union.operation='MAXIMUM';nt.links.new(ray.outputs['Is Camera Ray'],ray_union.inputs[0]);nt.links.new(ray.outputs['Is Transmission Ray'],ray_union.inputs[1]);nt.links.new(ray_union.outputs[0],mix.inputs[0])
scene.world['art_direction']='Cool blue-hour grading of licensed dusk HDRI; warm architectural fixtures retained.'
bpy.data.objects['Large soft warm interior'].data.energy=320
bpy.data.objects['Camera-side soft bounce'].data.energy=120
rug=bpy.data.materials['Warm charcoal woven rug']
for node in rug.node_tree.nodes:
    if node.type=='VALTORGB':
        node.color_ramp.elements[0].color=(.015,.019,.020,1);node.color_ramp.elements[1].color=(.065,.069,.068,1)

prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='OPTIX'
scene.cycles.device='GPU' if any(d.use for d in prefs.devices) else 'CPU'
artcam=bpy.data.objects['Landscape artwork source camera']
visibility={c.name:c.hide_render for c in scene.collection.children}
for c in scene.collection.children:
    if c.name not in ['08_EXTERIOR','13_REFINED_EXTERIOR','14_SCREEN_ARTWORK']:c.hide_render=True
scene.camera=artcam;scene.render.resolution_x=1024;scene.render.resolution_y=384;scene.cycles.samples=32
scene.render.filepath=str(ROOT/'screen-landscape-v004.png');bpy.ops.render.render(write_still=True)
for name,state in visibility.items():bpy.data.collections[name].hide_render=state
scene.camera=hero
art=bpy.data.images.load(str(ROOT/'screen-landscape-v004.png'),check_existing=False);art.colorspace_settings.name='sRGB'
for node in bpy.data.materials['Rendered mountain landscape display'].node_tree.nodes:
    if node.type=='TEX_IMAGE':node.image=art
bpy.data.objects.remove(artcam,do_unlink=True)
scene.render.resolution_x=1920;scene.render.resolution_y=540;scene.cycles.samples=128;scene.cycles.adaptive_threshold=.012
scene.render.filepath=str(ROOT/'kinetic-studio-proof-v004.png');scene['refinement_revision']='v004'
scene['proof_limitations']='Anatomy and technical screens remain schematic. Terrain is artist-authored. Hero camera remains an inferred fit, not measured calibration.'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'kinetic-studio-proof-v004.blend'))
t=time.time();bpy.ops.render.render(write_still=True)
report=json.loads((ROOT/'proof-verification-v003.json').read_text(encoding='utf-8'))
report.update(revision='v004',status='rendered-awaiting-visual-review',render_seconds=round(time.time()-t,2),samples=128,objects=len(scene.objects),materials=len(bpy.data.materials),blend=str(ROOT/'kinetic-studio-proof-v004.blend'),render=scene.render.filepath)
report['collections']={c.name:len(c.objects) for c in scene.collection.children}
report['mesh_objects']=sum(o.type=='MESH' for o in scene.objects)
report['asset_provenance']='Authored studio and terrain plus selected Poly Haven CC0 assets; see assets/asset-provenance.json for source URLs, authors, and checksums.'
report['devices']=[{'name':d.name,'type':d.type,'enabled':bool(d.use)} for d in prefs.devices]
report.pop('total_seconds',None)
report['refinement']['packed_file_images']=sum(bool(i.packed_file) for i in bpy.data.images)
report['refinement']['corrections_after_v003']=['Fit licensed broadleaf foliage to slim stoneware planters with credible dimensions.','Sharpened alpine ridge geometry and snow breakup.','Graded the dusk sky toward blue-hour through glazing and retained warm interior fixtures.']
report['limitations']=scene['proof_limitations']
(ROOT/'proof-verification-v004.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('KINETIC_REFINEMENT_V004_RENDERED',report['render_seconds'],len(scene.objects),flush=True)
