"""Bake a separate glTF delivery copy. Never save over the editable master."""
import bpy
import hashlib
import json
import math
import struct
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'kinetic-tour'/'public'/'models'
OUT.mkdir(parents=True,exist_ok=True)
BAKES=ROOT/'tour-bakes';BAKES.mkdir(exist_ok=True)
SOURCE=ROOT/'kinetic-studio-proof-v006.blend'
source_hash=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
bpy.context.preferences.filepaths.use_scripts_auto_execute=False
bpy.ops.wm.open_mainfile(filepath=str(SOURCE),load_ui=False)
scene=bpy.context.scene
scene.render.use_simplify=True;scene.render.simplify_subdivision=0;scene.render.simplify_subdivision_render=0
scene.cycles.samples=16;scene.cycles.use_denoising=True
scene.cycles.use_adaptive_sampling=True
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='OPTIX'
scene.cycles.device='GPU' if any(d.use for d in prefs.devices) else 'CPU'

def visible(ob):
    return not ob.hide_render and any(not c.hide_render for c in ob.users_collection)

def group_for(ob):
    names=[c.name for c in ob.users_collection]
    if any('PLANT' in n for n in names):return 'plants'
    if any('EXTERIOR' in n for n in names):return 'exterior'
    if any('LOUNGE' in n or 'FURNITURE' in n for n in names):return 'lounge'
    if any('WORKSTATION' in n for n in names):return 'workstation'
    for key,part in [('motion','ZONE_01'),('clinical','ZONE_02'),('engineering','ZONE_03'),('projects','ZONE_04')]:
        if any(part in n for n in names):return key
    if any('ZONE_DETAILS' in n for n in names):
        x=ob.matrix_world.translation.x
        return 'motion' if x<-6 else 'clinical' if x<-2.8 else 'projects' if x>7.3 else 'engineering'
    return 'architecture'

originals=list(scene.objects)
for ob in originals:
    if ob.type in {'MESH','CURVE','FONT'}:
        for mod in ob.modifiers:
            if mod.type=='SUBSURF':mod.levels=0;mod.render_levels=0
            if mod.type=='BEVEL':mod.segments=1
        if ob.type=='CURVE':ob.data.bevel_resolution=0;ob.data.resolution_u=3
bpy.context.view_layer.update()
deps=bpy.context.evaluated_depsgraph_get()
groups={};glass=[]
collection=bpy.data.collections.new('WEB_DELIVERY_COPY');scene.collection.children.link(collection)
for ob in originals:
    if ob.type not in {'MESH','CURVE','FONT'} or not visible(ob):continue
    if ob.name.startswith(('Pegboard perforation','Separate keyboard key','Distant city window')):continue
    evaluated=ob.evaluated_get(deps)
    mesh=bpy.data.meshes.new_from_object(evaluated,preserve_all_data_layers=True,depsgraph=deps)
    if not mesh or not mesh.polygons:continue
    copy=bpy.data.objects.new(ob.name+' delivery',mesh);collection.objects.link(copy)
    copy.matrix_world=ob.matrix_world.copy()
    is_glass=any(m and ('glass' in m.name.lower() or 'glazing' in m.name.lower()) for m in mesh.materials)
    if is_glass:glass.append(copy)
    else:groups.setdefault(group_for(ob),[]).append(copy)
for ob in originals:
    if ob.type not in {'LIGHT','CAMERA'}:bpy.data.objects.remove(ob,do_unlink=True)
bpy.context.view_layer.update()
joined=[];stats={};start=time.time()
for name,objects in groups.items():
    bpy.ops.object.select_all(action='DESELECT')
    for ob in objects:ob.hide_set(False);ob.select_set(True)
    bpy.context.view_layer.objects.active=objects[0];bpy.ops.object.join()
    ob=bpy.context.object;ob.name='Kinetic / '+name
    bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    tris=sum(len(p.vertices)-2 for p in ob.data.polygons)
    target=42000 if name=='plants' else 22000 if name=='lounge' else 18000 if name=='exterior' else 30000
    if tris>target:
        mod=ob.modifiers.new('Web delivery decimation','DECIMATE');mod.ratio=target/tris
        bpy.ops.object.modifier_apply(modifier=mod.name)
    # Each group has an independent light-and-color atlas. Geometry stays in meter units.
    bake_uv=ob.data.uv_layers.new(name='BakedLightingUV')
    ob.data.uv_layers.active_index=len(ob.data.uv_layers)-1
    bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=1.15192,island_margin=.003)
    bpy.ops.object.mode_set(mode='OBJECT')
    size=2048 if name in {'architecture','workstation','engineering','clinical','projects'} else 1024
    image=bpy.data.images.new('Baked '+name,width=size,height=size,alpha=False)
    image.colorspace_settings.name='sRGB'
    for material in ob.data.materials:
        if not material:continue
        material.use_nodes=True
        node=material.node_tree.nodes.new('ShaderNodeTexImage');node.name='WEB_BAKE_TARGET';node.image=image
        material.node_tree.nodes.active=node
    # Bake while every original shader is still present on all other groups.
    print('TOUR_BAKE_START',name,len(ob.data.polygons),flush=True)
    scene.render.bake.use_pass_direct=True;scene.render.bake.use_pass_indirect=True;scene.render.bake.use_pass_color=True
    scene.render.bake.use_pass_diffuse=True;scene.render.bake.use_pass_glossy=True;scene.render.bake.use_pass_transmission=False
    scene.render.bake.margin=3
    bpy.ops.object.bake(type='COMBINED',use_clear=True,uv_layer=bake_uv.name)
    image.filepath_raw=str(BAKES/(name+'.png'));image.file_format='PNG';image.save()
    stats[name]={'triangles':sum(len(p.vertices)-2 for p in ob.data.polygons),'atlas':str(image.filepath_raw),'resolution':size}
    joined.append((ob,image))

# Replace shaders only after every lighting bake completes.
for ob,image in joined:
    while len(ob.data.uv_layers)>1:ob.data.uv_layers.remove(ob.data.uv_layers[0])
    m=bpy.data.materials.new(ob.name+' baked unlit');m.use_nodes=True
    nt=m.node_tree;nt.nodes.clear()
    tex=nt.nodes.new('ShaderNodeTexImage');tex.image=image
    out=nt.nodes.new('ShaderNodeOutputMaterial')
    # The glTF exporter recognizes a color-to-surface connection as KHR_materials_unlit.
    nt.links.new(tex.outputs['Color'],out.inputs['Surface'])
    ob.data.materials.clear();ob.data.materials.append(m)
    for polygon in ob.data.polygons:polygon.material_index=0
for ob in glass:
    m=bpy.data.materials.new('Delivery clear glazing');m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.12,.18,.22,.045);p.inputs['Alpha'].default_value=.045;p.inputs['Roughness'].default_value=.25
    m.surface_render_method='DITHERED';ob.data.materials.clear();ob.data.materials.append(m)

def export(name):
    bpy.ops.object.select_all(action='DESELECT')
    for ob,_ in joined:ob.select_set(True)
    for ob in glass:ob.select_set(True)
    dest=OUT/name
    bpy.ops.export_scene.gltf(filepath=str(dest),export_format='GLB',use_selection=True,export_materials='EXPORT',export_image_format='JPEG',export_jpeg_quality=85,export_cameras=False,export_lights=False,export_animations=False,export_yup=True)
    raw=dest.read_bytes();magic,version,length=struct.unpack('<4sII',raw[:12]);assert magic==b'glTF' and version==2 and length==len(raw)
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}

desktop=export('studio-desktop.glb')
for ob,image in joined:
    if len(ob.data.polygons)>4000:
        bpy.context.view_layer.objects.active=ob
        mod=ob.modifiers.new('Mobile delivery detail','DECIMATE');mod.ratio=.5;bpy.ops.object.modifier_apply(modifier=mod.name)
    image.scale(512,512)
mobile=export('studio-mobile.glb')
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==source_hash
report={'source_sha256':source_hash,'desktop':desktop,'mobile':mobile,'groups':stats,'seconds':round(time.time()-start,2),'bake':'Cycles COMBINED diffuse, glossy, direct, indirect, color and emission; transmission excluded. glTF unlit atlases preserve static warm illumination.','source_editability':'Authoritative v006 unchanged. Delivery meshes are decimated, grouped, and baked.'}
(ROOT/'tour-export.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('KINETIC_TOUR_EXPORT_PASS',json.dumps(report),flush=True)
