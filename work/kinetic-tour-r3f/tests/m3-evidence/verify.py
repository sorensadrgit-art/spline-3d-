"""Fresh command receipts; protected binaries checked against delivery manifest."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[4]; P=R/'work/kinetic-tour-r3f'; E=Path(__file__).resolve().parent
commands=[]
def command(name,args,cwd=R):
 p=subprocess.run(args,cwd=cwd,capture_output=True,text=True,encoding='utf-8',env={**os.environ,'PYTHONUTF8':'1'})
 (E/(name+'.txt')).write_text(p.stdout+p.stderr,encoding='utf-8')
 commands.append({'name':name,'command':args,'cwd':str(cwd),'exit':p.returncode})
 (E/'commands.json').write_text(json.dumps(commands,indent=2),encoding='utf-8')
 print(name,'exit',p.returncode,p.stdout[-2000:],p.stderr[-600:],flush=True)
 assert p.returncode==0,name
if '--hash-only' not in sys.argv:
 for name,args,cwd in [('unit',['npm.cmd','test'],P),('build',['npm.cmd','run','build'],P),('legacy-unit',['npm.cmd','test'],R/'work/kinetic-tour'),('legacy-build',['npm.cmd','run','build'],R/'work/kinetic-tour'),('validator',['node',str(E/'validate-models.mjs')],R)]:command(name,args,cwd)
manifest=json.loads((R/'work/kinetic-studio-delivery.json').read_text(encoding='utf-8'))['artifacts'];out={}
for name,want in manifest.items():
 p=R/'work'/name; actual=hashlib.sha256(p.read_bytes()).hexdigest();out[name]={'expected':want['sha256'],'actual':actual,'matches':actual==want['sha256'],'bytes':p.stat().st_size}
for name in ['work/kinetic-tour/public/models/blue-hour.jpg','work/kinetic-tour/src/main.ts','work/kinetic-tour-r3f/src/tour.ts']:
 p=R/name;current=p.read_bytes();original=subprocess.run(['git','show','96f13b2:'+name],cwd=R,capture_output=True,check=True).stdout
 normalized=current.replace(b'\r\n',b'\n') if p.suffix=='.ts' else current
 out[name]={'actual':hashlib.sha256(current).hexdigest(),'baseline':hashlib.sha256(original).hexdigest(),'comparison':'LF-normalized for TS; exact binary bytes','matches':normalized==original}
protected=subprocess.run(['git','diff','--name-only','96f13b2','--','work/kinetic-tour','work/kinetic-blender','work/kinetic-splat'],cwd=R,capture_output=True,text=True,check=True).stdout
(E/'protected-diff.txt').write_text(protected,encoding='utf-8');assert not protected.strip(),protected
(E/'source-hashes.json').write_text(json.dumps(out,indent=2),encoding='utf-8');assert all(x['matches'] for x in out.values()),out
print('SOURCE_HASHES_PASS',len(out),flush=True)
