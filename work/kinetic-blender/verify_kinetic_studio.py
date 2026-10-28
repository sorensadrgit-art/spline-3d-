"""Reopen the saved Blender source and check the delivered image and invariants."""
import bpy
import json
import hashlib
import struct
import sys
from pathlib import Path
import numpy as np

root=Path(__file__).resolve().parent
version=sys.argv[-1] if sys.argv[-1].startswith('v00') else 'v001'
blend=root/f'kinetic-studio-proof-{version}.blend'
png=root/f'kinetic-studio-proof-{version}.png'
assert blend.is_file() and blend.stat().st_size>100000, 'Missing editable Blender source'
assert png.is_file() and png.stat().st_size>1000, 'Missing proof image'
raw=png.read_bytes()
assert raw[:8]==b'\x89PNG\r\n\x1a\n', 'Invalid PNG header'
width,height=struct.unpack('>II',raw[16:24])
assert width>=960 and height>=270
baseline_camera=None
if version in ['v003','v004','v005','v006']:
    bpy.ops.wm.open_mainfile(filepath=str(root/'kinetic-studio-proof-v002.blend'),load_ui=False)
    baseline_camera=([list(row) for row in bpy.context.scene.camera.matrix_world],bpy.context.scene.camera.data.lens)
bpy.ops.wm.open_mainfile(filepath=str(blend),load_ui=False)
scene=bpy.context.scene
required=['03_ZONE_01_MOTION_SYSTEMS','04_ZONE_02_CLINICAL_THINKING','05_ZONE_03_CREATIVE_ENGINEERING','06_ZONE_04_PROJECTS']
assert all(n in bpy.data.collections and len(bpy.data.collections[n].objects)>10 for n in required)
assert all(not bpy.data.collections[n].hide_render for n in required)
assert scene.camera and scene.camera.name=='CAM_Hero_Reference_Fit'
assert len([o for o in scene.objects if o.type=='CAMERA'])==5
assert len([o for o in scene.objects if o.type=='MESH'])>300
assert sum(bool(o.modifiers) for o in scene.objects)>100
assert sum(o.type=='FONT' for o in scene.objects)>=9, 'Zone signage must remain editable text'
assert any(o.type=='LIGHT' and o.data.color[0]>o.data.color[2]*1.3 for o in scene.objects)
assert scene.unit_settings.system=='METRIC'
assert scene['native_spline_preserved']
if baseline_camera:
    assert all(abs(a-b)<1e-6 for ra,rb in zip(baseline_camera[0],scene.camera.matrix_world) for a,b in zip(ra,rb)), 'Hero camera transform changed'
    assert abs(scene.camera.data.lens-baseline_camera[1])<1e-6, 'Hero lens changed'
    missing=[im.name for im in bpy.data.images if im.source=='FILE' and not im.packed_file and not Path(bpy.path.abspath(im.filepath)).is_file()]
    assert not missing, 'Missing external textures: '+str(missing)
    assert all(im.packed_file for im in bpy.data.images if im.source=='FILE' and im.filepath), 'File textures must be packed'
    provenance=json.loads((root/'assets/asset-provenance.json').read_text(encoding='utf-8'))
    assert provenance['license']=='CC0'
    for asset in provenance['assets'].values():
        for entry in asset['files']:
            assert hashlib.sha256((root/'assets'/entry['path']).read_bytes()).hexdigest()==entry['sha256'], 'Asset bytes changed'
    prior=json.loads((root/'acceptance-v002.json').read_text(encoding='utf-8'))
    assert hashlib.sha256((root/'kinetic-studio-proof-v002.blend').read_bytes()).hexdigest()==prior['blend_sha256'], 'Previous editable source changed'
    assert hashlib.sha256((root/'kinetic-studio-proof-v002.png').read_bytes()).hexdigest()==prior['png_sha256'], 'Previous render changed'
image=bpy.data.images.load(str(png),check_existing=False)
pixels=np.asarray(image.pixels[:],dtype=np.float32).reshape(height,width,4)[:,:,:3]
assert np.isfinite(pixels).all()
assert pixels.std()>.035, 'Blank or nearly solid render'
assert (pixels.max(axis=2)>.2).mean()>.1, 'Render too dark to review'
report_path=root/f'proof-verification-{version}.json'
if not report_path.exists():report_path=root/'proof-verification.json'
report=json.loads(report_path.read_text(encoding='utf-8-sig'))
reference_hashes=report.get('source_hashes') or json.loads((root/'proof-verification-v004.json').read_text(encoding='utf-8'))['source_hashes']
for name,expected in reference_hashes.items():
    assert hashlib.sha256((root.parent.parent/name).read_bytes()).hexdigest()==expected, 'Reference source changed'
if version in ['v005','v006']:
    prior=json.loads((root/'acceptance-v004.json').read_text(encoding='utf-8'))
    assert hashlib.sha256((root/'kinetic-studio-proof-v004.blend').read_bytes()).hexdigest()==prior['blend_sha256']
    assert hashlib.sha256((root/'kinetic-studio-proof-v004.png').read_bytes()).hexdigest()==prior['png_sha256']
    assert [width,height]==[3840,1080]
    for zone in ['motion','clinical','engineering','projects']:
        path=root/f'kinetic-studio-{zone}-{version}.png'
        zone_image=bpy.data.images.load(str(path),check_existing=False)
        assert list(zone_image.size)==[1600,1000]
        zone_pixels=np.asarray(zone_image.pixels[:],dtype=np.float32)
        assert np.isfinite(zone_pixels).all() and zone_pixels.std()>.035
    if version=='v006':
        import bmesh
        for ob in scene.objects:
            if ob.type=='MESH' and len(ob.data.vertices)==8 and len(ob.data.polygons)==6:
                mesh=bmesh.new();mesh.from_mesh(ob.data)
                assert mesh.calc_volume(signed=True)>-1e-10, 'Inward box normals: '+ob.name
                mesh.free()
result={
    'marker':'KINETIC_EDITABLE_PROOF_PASS','version':version,
    'blend_reopened':True,'png_dimensions':[width,height],
    'objects':len(scene.objects),'materials':len(bpy.data.materials),
    'mesh_objects':sum(o.type=='MESH' for o in scene.objects),
    'zone_objects':{n:len(bpy.data.collections[n].objects) for n in required},
    'image_rgb_std':float(pixels.std()),'image_rgb_mean':float(pixels.mean()),
    'blend_sha256':hashlib.sha256(blend.read_bytes()).hexdigest(),
    'png_sha256':hashlib.sha256(raw).hexdigest(),
    'source_references_unchanged':True,
    'hero_camera_matches_v002':baseline_camera is not None,
    'packed_file_images':sum(bool(im.packed_file) for im in bpy.data.images),
    'limits':'Software and image checks do not establish final photoreal quality, exact camera calibration, or Spline interchange fidelity.'
}
(root/f'acceptance-{version}.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
if version=='v004':
    report.update(status='rendered-visually-reviewed-and-source-reopened',objects=result['objects'],mesh_objects=result['mesh_objects'],materials=result['materials'])
    report['asset_provenance']='Authored studio and terrain plus six selected Poly Haven CC0 assets; source URLs, author metadata, and file hashes are recorded in assets/asset-provenance.json.'
    report['refinement']['packed_file_images']=result['packed_file_images']
    report['visual_review']='Compared v002, v003, and v004 actual PNGs. Corrected oversized terracotta planters and soft mountain ridges in v003. v004 preserves the hero camera and four-zone order, with warmer interior contrast, a blue-hour HDR sky, rugged editable terrain, photographed plant detail, and leather furniture detail.'
    report.pop('devices',None)
    report['render_device_selection']={'backend':'OPTIX','device':'NVIDIA GeForce RTX 4070 Laptop GPU','evidence':'balance_refinement.py enabled only OPTIX devices immediately before the final render; source retains Cycles GPU selection.'}
    report.pop('total_seconds',None)
    report_path.write_text(json.dumps(report,indent=2),encoding='utf-8')
print('KINETIC_EDITABLE_PROOF_PASS',json.dumps(result))
