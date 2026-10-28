import bpy,json
from pathlib import Path
from mathutils import Vector
root=Path(__file__).resolve().parent
bpy.context.preferences.filepaths.use_scripts_auto_execute=False
result={}
for name in ['potted_plant_02','potted_plant_04','mid_century_lounge_chair']:
    with bpy.data.libraries.load(str(root/'assets'/name/(name+'_1k.blend')),link=False) as (source,target):
        target.objects=source.objects
    objects=[o for o in target.objects if o and o.type=='MESH']
    result[name]=[{'name':o.name,'dimensions':list(o.dimensions),'location':list(o.location),'rotation':list(o.rotation_euler),'vertices':len(o.data.vertices),'materials':[m.name for m in o.data.materials if m]} for o in objects]
print(json.dumps(result,indent=2))
(root/'assets'/'asset-structure.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
