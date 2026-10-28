"""M5 fresh verification; receipts confined to this directory."""
import hashlib,json,os,subprocess
from pathlib import Path
E=Path(__file__).resolve().parent
R=E.parents[3]
BASE='16d2a6b20bc5d29ef777bd3bf81dc8e16af9218f'
commands=[]
def command(name,args,cwd=R):
 p=subprocess.run(args,cwd=cwd,capture_output=True,text=True,encoding='utf-8',env={**os.environ,'PYTHONUTF8':'1'})
 (E/(name+'.txt')).write_text(p.stdout+p.stderr,encoding='utf-8')
 commands.append({'name':name,'command':args,'cwd':str(cwd),'exit':p.returncode})
 (E/'commands.json').write_text(json.dumps(commands,indent=2),encoding='utf-8')
 print(name,'exit',p.returncode,p.stdout[-1200:],p.stderr[-500:],flush=True)
 assert p.returncode==0,name
for app in ['kinetic-tour','kinetic-tour-r3f']:
 for label,args in [('install',['npm.cmd','ci']),('unit',['npm.cmd','test']),('build',['npm.cmd','run','build'])]:
  command(app+'-'+label,args,R/'work'/app)
manifest=json.loads((R/'work/kinetic-studio-delivery.json').read_text())['artifacts']
out={}
for name,want in manifest.items():
 p=R/'work'/name;actual=hashlib.sha256(p.read_bytes()).hexdigest()
 out[name]={'expected':want,'actual':{'bytes':p.stat().st_size,'sha256':actual},'pass':actual==want['sha256'] and p.stat().st_size==want['bytes']}
sky=R/'work/kinetic-tour/public/models/blue-hour.jpg'
out['sky']={'sha256':hashlib.sha256(sky.read_bytes()).hexdigest(),'pass':hashlib.sha256(sky.read_bytes()).hexdigest()=='c45d164f9ebcc307feb66f9adcdd19182e1701e8ec2f51e1099cb0aaf7e8bc40'}
original=(R/'work/kinetic-tour/public/models/studio-mobile.glb').read_bytes()
tampered=bytearray(original);tampered[-1]^=1
expected=manifest['kinetic-tour\\public\\models\\studio-mobile.glb']['sha256']
out['negativeProtection']={'method':'in-memory copy only; flip final byte, reject altered digest','originalAccepted':hashlib.sha256(original).hexdigest()==expected,'tamperedRejected':hashlib.sha256(tampered).hexdigest()!=expected,'pass':hashlib.sha256(original).hexdigest()==expected and hashlib.sha256(tampered).hexdigest()!=expected}
(E/'protected-hashes.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
assert all(x['pass'] for x in out.values())
command('protected-diff',['git','diff',BASE,'--','work/kinetic-tour','work/kinetic-blender','work/kinetic-splat'])
assert not (E/'protected-diff.txt').read_text().strip()
# Use existing validator logic verbatim except module/asset paths and receipt location.
source=(R/'work/kinetic-tour/tests/validate-models.mjs').read_text()
source=source.replace("from 'gltf-validator'","from '../../../kinetic-tour/node_modules/gltf-validator/index.js'")
source=source.replace('../public/models/','../../../kinetic-tour/public/models/')
(E/'validate-models.mjs').write_text(source,encoding='utf-8')
command('validator',['node',str(E/'validate-models.mjs')])
command('provenance',['git','diff','--name-status',BASE,'HEAD'])
print('M5_SOURCE_AND_BUILD_PASS',flush=True)
