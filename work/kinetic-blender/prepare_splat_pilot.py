"""Render one bounded, known-pose synthetic dataset for the engineering splat pilot."""
import bpy
import hashlib
import json
import math
import numpy as np
import time
from pathlib import Path
from mathutils import Vector

ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'kinetic-splat'/'dataset-v005'
(OUT/'images').mkdir(parents=True,exist_ok=True)
source=ROOT/'kinetic-studio-proof-v005.blend'
bpy.context.preferences.filepaths.use_scripts_auto_execute=False
bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False)
scene=bpy.context.scene
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
for device in prefs.devices:device.use=device.type=='OPTIX'
scene.cycles.device='GPU' if any(d.use for d in prefs.devices) else 'CPU'
scene.cycles.samples=12;scene.cycles.use_denoising=True;scene.cycles.adaptive_threshold=.05
scene.render.use_persistent_data=True;scene.render.resolution_x=1024;scene.render.resolution_y=768;scene.render.resolution_percentage=100
scene.render.use_simplify=True;scene.render.simplify_subdivision_render=0
cam=bpy.data.objects['CAM_03_Creative_Engineering'];cam.data.lens=30;cam.data.sensor_width=36;cam.data.sensor_fit='HORIZONTAL';scene.camera=cam
target=Vector((4.95,4.3,1.75))
train=[];test=[];start=time.time()
poses=[(x,y,z) for z in [1.3,1.85,2.4] for y in np.linspace(.9,2.1,6) for x in np.linspace(3.35,6.65,8)]
for index,position in enumerate(poses):
    cam.location=position;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();bpy.context.view_layer.update()
    relative=f'images/{index:03}.png';scene.render.filepath=str(OUT/relative)
    frame={'file_path':relative,'transform_matrix':[list(row) for row in cam.matrix_world]}
    (test if index%12==5 else train).append(frame)
    if not (OUT/relative).is_file():bpy.ops.render.render(write_still=True)
    print('PILOT_FRAME',index+1,144,round(time.time()-start,1),flush=True)
focal=1024*cam.data.lens/cam.data.sensor_width
base={'camera_model':'OPENCV','w':1024,'h':768,'fl_x':focal,'fl_y':focal,'cx':512,'cy':384,'k1':0,'k2':0,'p1':0,'p2':0}
(OUT/'transforms_train.json').write_text(json.dumps(dict(base,frames=train,ply_file_path='init.ply'),indent=2),encoding='utf-8')
(OUT/'transforms_test.json').write_text(json.dumps(dict(base,frames=test),indent=2),encoding='utf-8')

# A real Gaussian initialization sampled from editable geometry, before image training.
# This is explicitly an initialization, never presented as a trained reconstruction.
rng=np.random.default_rng(271028);points=[];colors=[]
deps=bpy.context.evaluated_depsgraph_get()
for ob in scene.objects:
    if ob.type!='MESH' or ob.hide_render or any(c.hide_render for c in ob.users_collection):continue
    bounds=[ob.matrix_world@Vector(p) for p in ob.bound_box]
    center=sum(bounds,Vector())/8
    if not (2.6<center.x<7.4 and 2.6<center.y<5.3 and -.1<center.z<3.65):continue
    ev=ob.evaluated_get(deps);mesh=ev.to_mesh();mesh.calc_loop_triangles()
    count=min(600,max(10,len(mesh.loop_triangles)//3))
    for tri in rng.choice(len(mesh.loop_triangles),min(count,len(mesh.loop_triangles)),replace=False):
        face=mesh.loop_triangles[tri];a,b,c=[ob.matrix_world@mesh.vertices[i].co for i in face.vertices]
        u,v=rng.random(2)
        if u+v>1:u,v=1-u,1-v
        p=a+(b-a)*float(u)+(c-a)*float(v)
        points.append(tuple(p))
        material=mesh.materials[face.material_index] if len(mesh.materials)>face.material_index else None
        bsdf=material.node_tree.nodes.get('Principled BSDF') if material and material.use_nodes else None
        color=tuple(bsdf.inputs['Base Color'].default_value[:3]) if bsdf else (.18,.16,.12)
        colors.append(color)
    ev.to_mesh_clear()
if len(points)>24000:
    indices=rng.choice(len(points),24000,replace=False);points=[points[i] for i in indices];colors=[colors[i] for i in indices]
fields=['x','y','z','nx','ny','nz']+['f_dc_'+str(i) for i in range(3)]+['f_rest_'+str(i) for i in range(45)]+['opacity']+['scale_'+str(i) for i in range(3)]+['rot_'+str(i) for i in range(4)]
values=np.zeros((len(points),len(fields)),dtype='<f4');values[:,:3]=points;values[:,6:9]=(np.asarray(colors)-.5)/.2820947918
values[:,fields.index('opacity')]=0;values[:,fields.index('scale_0'):fields.index('scale_0')+3]=math.log(.025);values[:,fields.index('rot_0')]=1
header='ply\nformat binary_little_endian 1.0\nelement vertex '+str(len(points))+'\n'+''.join('property float '+field+'\n' for field in fields)+'end_header\n'
(OUT/'init.ply').write_bytes(header.encode()+values.tobytes())
report={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'train_frames':len(train),'held_out_frames':len(test),'resolution':[1024,768],'source_samples':12,'init_gaussians':len(points),'init_status':'geometry-sampled initialization, not trained','camera_convention':'Blender OpenGL camera-to-world, Nerfstudio transforms','seconds':round(time.time()-start,2)}
(OUT/'dataset-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
assert len(train)==132 and len(test)==12
print('KINETIC_SPLAT_DATASET_PASS',json.dumps(report),flush=True)
