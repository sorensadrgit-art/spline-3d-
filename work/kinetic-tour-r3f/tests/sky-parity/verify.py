"""Repeatable bounded verification, with command exit codes and immutable hashes."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[4];P=R/'work/kinetic-tour-r3f';E=P/'tests/sky-parity'
commands=[]
for args,cwd in [(['npm.cmd','test'],P),(['npm.cmd','run','build'],P),([sys.executable,str(E/'browser.py'),'--suite'],R),([sys.executable,str(E/'check.py'),'--candidate',str(E),'--prefix','after','--receipt',str(E/'green.json')],R)]:
 if '--hash-only' in sys.argv:break
 p=subprocess.run(args,cwd=cwd,capture_output=True,text=True,encoding='utf-8',env={**os.environ,'PYTHONUTF8':'1'})
 name=['unit','build','browser','sky'][len(commands)];(E/(name+'.txt')).write_text(p.stdout+p.stderr,encoding='utf-8')
 commands.append({'command':args,'cwd':str(cwd),'exit':p.returncode});print(name,'exit',p.returncode,p.stdout[-1600:],p.stderr[-500:],flush=True)
 (E/'commands.json').write_text(json.dumps(commands,indent=2),encoding='utf-8')
 if p.returncode:sys.exit(p.returncode)
manifest=json.loads((R/'work/kinetic-studio-delivery.json').read_text())['artifacts'];out={}
for name,expected in manifest.items():
 path=R/'work'/Path(name);actual=hashlib.sha256(path.read_bytes()).hexdigest();out[name]={'expected':expected['sha256'],'actual':actual,'matches':actual==expected['sha256'],'bytes':path.stat().st_size}
for name in ['work/kinetic-tour/public/models/blue-hour.jpg','work/kinetic-tour/src/main.ts','work/kinetic-tour-r3f/src/tour.ts']:
 path=R/name;current=hashlib.sha256(path.read_bytes()).hexdigest();original=subprocess.run(['git','show','9b960ee:'+name],cwd=R,capture_output=True,check=True).stdout
 normalized=path.read_bytes().replace(b'\r\n',b'\n') if path.suffix=='.ts' else path.read_bytes()
 out[name]={'actual':current,'parent':hashlib.sha256(original).hexdigest(),'comparison':'LF-normalized for TypeScript; exact bytes for binary','matches':normalized==original}
(E/'source-hashes.json').write_text(json.dumps(out,indent=2),encoding='utf-8');assert all(x['matches'] for x in out.values());print('SOURCE_HASHES_PASS',len(out),flush=True)
