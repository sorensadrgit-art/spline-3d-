"""Independent native-project and compressed-archive checks after browser reopening."""
import hashlib
import json
from pathlib import Path
import zipfile
import numpy as np

def gaussian_values(raw):
    end=raw.index(b'end_header\n')+len(b'end_header\n')
    header=raw[:end].decode('ascii')
    assert 'format binary_little_endian 1.0' in header
    count=int(next(line.split()[-1] for line in header.splitlines() if line.startswith('element vertex')))
    properties=[line.split()[-1] for line in header.splitlines() if line.startswith('property float ')]
    assert len(properties)>=14
    values=np.frombuffer(raw[end:],dtype='<f4').reshape(count,len(properties))
    assert np.isfinite(values).all()
    return {name:values[:,i] for i,name in enumerate(properties)}

ROOT=Path(__file__).resolve().parent
report=json.loads((ROOT/'pilot-report.json').read_text(encoding='utf-8'))
ply=ROOT/'pilot-v005/engineering_3000.ply'
assert hashlib.sha256(ply.read_bytes()).hexdigest()==report['ply_sha256']
project=ROOT/'kinetic-engineering-pilot-v001.ssproj'
with zipfile.ZipFile(project) as archive:
    assert archive.testzip() is None
    assert {'document.json','resource_0.ply','instances_0.bin'}<=set(archive.namelist())
    document=json.loads(archive.read('document.json'))
    assert len(document['splats'])==1 and document['resources'][0]['numRows']==21516
    assert abs(document['splats'][0]['rotation'][0]+2**-.5)<1e-6
    assert document['camera']['fov']==70 and document['camera']['focalPoint']==[4.95,1.75,-4.3]
    native=gaussian_values(archive.read('resource_0.ply'));source=gaussian_values(ply.read_bytes())
    # Native serialization reorders rows; compare the complete coordinate sets independently.
    native_xyz=np.column_stack([native[axis] for axis in ['x','y','z']])
    source_xyz=np.column_stack([source[axis] for axis in ['x','y','z']])
    native_order=np.lexsort(native_xyz.T[::-1]);source_order=np.lexsort(source_xyz.T[::-1])
    assert np.allclose(native_xyz[native_order],source_xyz[source_order],atol=1e-5)
sog=ROOT/'kinetic-engineering-pilot-v001.sog'
with zipfile.ZipFile(sog) as archive:
    assert archive.testzip() is None
    metadata=json.loads(archive.read('meta.json'))
    assert metadata['version']==2 and metadata['count']==21516
    for name in archive.namelist():
        if name.endswith('.webp'):
            raw=archive.read(name);assert raw[:4]==b'RIFF' and raw[8:12]==b'WEBP'
result={'marker':'KINETIC_NATIVE_EXPORTS_PASS','gaussians':21516,'native_project_sha256':hashlib.sha256(project.read_bytes()).hexdigest(),'sog_sha256':hashlib.sha256(sog.read_bytes()).hexdigest(),'original_trained_ply_preserved':True,'project_reopen_receipt':'project-checks.json','raw_and_compressed_browser_views':'pilot-browser.png and compressed-pilot-browser.png'}
(ROOT/'native-export-checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print('KINETIC_NATIVE_EXPORTS_PASS')
