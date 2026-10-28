"""Bounded corrections observed in the first actual proof render."""
import bpy
import time
import json
from pathlib import Path

root=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(root/'kinetic-studio-proof-v001.blend'),load_ui=False)
scene=bpy.context.scene
for o in scene.objects:
    if o.type=='LIGHT':
        o.visible_camera=False
        o.visible_glossy=False
        o.visible_transmission=False
    if o.name.startswith('Platform cyan side'):
        o.location.x=2.258 if o.location.x>0 else -2.258
    if o.name.startswith('Platform cyan front rear'):
        o.location.y=1.908 if o.location.y>0 else -1.908
    if o.name.startswith('Meeting partition glass'):
        old=o.data.materials[0]
        m=bpy.data.materials.get('Low-reflection meeting glass')
        if m is None:
            m=old.copy();m.name='Low-reflection meeting glass'
            nt=m.node_tree;p=nt.nodes.get('Principled BSDF');out=nt.nodes.get('Material Output')
            transparent=nt.nodes.new('ShaderNodeBsdfTransparent')
            mix=nt.nodes.new('ShaderNodeMixShader');mix.inputs[0].default_value=.32
            nt.links.new(transparent.outputs[0],mix.inputs[1]);nt.links.new(p.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],out.inputs['Surface'])
        o.data.materials[0]=m
energies={'Large soft warm interior':260,'Camera-side soft bounce':90,'Cool evening window source':520,'Ring pendant downlight':155,'Monitor spill':7}
for name,energy in energies.items():bpy.data.objects[name].data.energy=energy
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.055
scene.view_settings.exposure=.10
scene.cycles.samples=64
scene.cycles.adaptive_threshold=.02
scene.render.resolution_x=1600
scene.render.resolution_y=450
scene.render.filepath=str(root/'kinetic-studio-proof-v002.png')
bpy.ops.wm.save_as_mainfile(filepath=str(root/'kinetic-studio-proof-v002.blend'))
t=time.time();bpy.ops.render.render(write_still=True)
report=json.loads((root/'proof-verification.json').read_text(encoding='utf-8'))
report['status']='refined-render-awaiting-visual-review'
report['revision']='v002'
report['render_seconds']=round(time.time()-t,2)
report['samples']=scene.cycles.samples
report['resolution']=[scene.render.resolution_x,scene.render.resolution_y]
report['blend']=str(root/'kinetic-studio-proof-v002.blend')
report['render']=scene.render.filepath
report['materials']=len(bpy.data.materials)
report['observed_corrections']=['Moved embedded capture-platform diffusers outside opaque platform faces.','Reduced flat fill illumination and concealed helper light panels from camera/reflection/transmission rays.','Reduced grazing reflection of the meeting partition while retaining an editable glass shader.']
(root/'proof-verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('KINETIC_STUDIO_REFINED_PROOF_RENDERED',report['render_seconds'])
