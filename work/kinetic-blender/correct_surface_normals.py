"""Correct the inverted authored box surfaces found by the actual web bake review."""
import bpy
import bmesh
import hashlib
import json
import math
from pathlib import Path
from mathutils import Matrix, Vector

ROOT=Path(__file__).resolve().parent
source=ROOT/'kinetic-studio-proof-v005.blend'
source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
bpy.context.preferences.filepaths.use_scripts_auto_execute=False
bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False)
scene=bpy.context.scene;hero=scene.camera
fixed=[];seen=set()
for ob in scene.objects:
    if ob.type!='MESH' or len(ob.data.vertices)!=8 or len(ob.data.polygons)!=6 or ob.data.name in seen:continue
    seen.add(ob.data.name)
    mesh=bmesh.new();mesh.from_mesh(ob.data)
    if mesh.calc_volume(signed=True)<-1e-10:
        bmesh.ops.reverse_faces(mesh,faces=list(mesh.faces));mesh.to_mesh(ob.data);ob.data.update();fixed.append(ob.name)
    mesh.free()
assert len(fixed)>500,'Expected to find the observed inverted-box source defect'

# Shared scan instances fill the formerly sparse broadleaf canopies without flattening them.
plants=bpy.data.collections['12_REFINED_PLANTS']
for root in [o for o in scene.objects if o.type=='EMPTY' and o.name.startswith('Broadleaf floor plant')]:
    for leaf in [c for c in root.children if 'leaves' in c.name and not c.hide_render]:
        origin=Vector((root.location.x,root.location.y,.55))
        copy=leaf.copy();copy.data=leaf.data;plants.objects.link(copy)
        copy.name='Additional broadleaf canopy / linked editable scan'
        copy.matrix_world=Matrix.Translation(origin)@Matrix.Rotation(math.radians(115),4,'Z')@Matrix.Diagonal((.88,.88,.94,1))@Matrix.Translation(-origin)@leaf.matrix_world
        copy.location.z+=.08

prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='OPTIX'
scene.cycles.device='GPU' if any(d.use for d in prefs.devices) else 'CPU'
scene.render.use_simplify=True;scene.render.simplify_subdivision_render=1
scene.cycles.samples=128;scene.render.resolution_x=3840;scene.render.resolution_y=1080
scene['refinement_revision']='v006'
scene['surface_correction']='Outward normals on authored closed box meshes; modifiers and native text retained.'
scene.render.filepath=str(ROOT/'kinetic-studio-proof-v006.png')
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'kinetic-studio-proof-v006.blend'))
bpy.ops.render.render(write_still=True)
for key,name in [('motion','CAM_01_Motion_Systems'),('clinical','CAM_02_Clinical_Thinking'),('engineering','CAM_03_Creative_Engineering'),('projects','CAM_04_Projects')]:
    scene.camera=bpy.data.objects[name];scene.render.resolution_x=1600;scene.render.resolution_y=1000;scene.cycles.samples=96
    scene.render.filepath=str(ROOT/f'kinetic-studio-{key}-v006.png');bpy.ops.render.render(write_still=True)
scene.camera=hero;scene.render.resolution_x=3840;scene.render.resolution_y=1080;scene.cycles.samples=128;scene.render.filepath=str(ROOT/'kinetic-studio-proof-v006.png')
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'kinetic-studio-proof-v006.blend'))
assert source_hash==hashlib.sha256(source.read_bytes()).hexdigest()
report=json.loads((ROOT/'proof-verification-v005.json').read_text(encoding='utf-8'))
report.update(revision='v006',source_v005_sha256=source_hash,corrected_closed_box_meshes=len(fixed),objects=len(scene.objects),normal_correction=fixed)
report.pop('render_seconds',None)
report['render_time_status']='v006 render duration was not separately recorded; v005 timing does not apply.'
report['outputs']={k:v.replace('v005','v006') for k,v in report['outputs'].items()}
(ROOT/'proof-verification-v006.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('KINETIC_V006_SURFACES_PASS',len(fixed),flush=True)
