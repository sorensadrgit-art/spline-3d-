import hashlib,json,subprocess
from pathlib import Path
E=Path(__file__).resolve().parent;R=E.parents[3]
out={}
for name,want in json.loads((R/'work/kinetic-studio-delivery.json').read_text())['artifacts'].items():
 p=R/'work'/name;actual={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()};out[name]={'expected':want,'actual':actual,'pass':want==actual}
sky=R/'work/kinetic-tour/public/models/blue-hour.jpg';digest=hashlib.sha256(sky.read_bytes()).hexdigest();out['sky']={'sha256':digest,'pass':digest=='c45d164f9ebcc307feb66f9adcdd19182e1701e8ec2f51e1099cb0aaf7e8bc40'}
assert all(v['pass'] for v in out.values()),out
for name,args in [('final-protected-diff',['git','diff','44ad922826da34bbcaf7bb83646b24cd694d084c','--','work/kinetic-tour','work/kinetic-blender','work/kinetic-splat']),('final-diff-check',['git','diff','--check'])]:
 p=subprocess.run(args,cwd=R,capture_output=True,text=True,encoding='utf-8');(E/(name+'.txt')).write_text(p.stdout+p.stderr,encoding='utf-8');assert p.returncode==0 and not p.stdout and not p.stderr,(name,p.stdout,p.stderr)
(E/'final-protected-hashes.json').write_text(json.dumps(out,indent=2));print('FINAL_IMMUTABLE_PASS',len(out),'protected-source-diff empty')
a=[]
for f in sorted([*E.glob('a11y-*.json'),*E.glob('mobile-a11y-*.json')]):
 if f.name=='a11y-summary.json':continue
 d=json.loads(f.read_text());assert d['counts']['violations']==0;a.append({'file':f.name,'axe':d['axeVersion'],'counts':d['counts'],'incompleteRules':[x['id'] for x in d['incomplete']]})
(E/'a11y-summary.json').write_text(json.dumps(a,indent=2));print('AXE_ZERO_CONFIRMED',len(a))
