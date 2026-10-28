"""Final serial verification; keep stdout, stderr, exit codes and evidence source hashes."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
E=Path(__file__).resolve().parent;R=E.parents[3];results=[]
commands=[('verification',[sys.executable,str(E/'verify.py')]),('browser',[sys.executable,str(E/'browser.py')]),('comparison',[sys.executable,str(E/'compare.py')]),('sky',[sys.executable,str(E.parent/'sky-parity/check.py'),'--candidate',str(E),'--prefix','','--receipt',str(E/'sky-direction.json')])]
# Comparator uses prefix + '-' filename; M3 captures have no prefix.
commands[-1]=('sky',[sys.executable,'-c',"import importlib.util,json;from pathlib import Path;p=Path("+repr(str(E.parent/'sky-parity/check.py'))+");s=importlib.util.spec_from_file_location('sky',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);e=Path("+repr(str(E))+");r={z:{'legacy':m.measure(e/('legacy-'+z+'-3d.png'),z),'r3f':m.measure(e/(z+'-3d.png'),z)} for z in m.PATCHES};(e/'sky-direction.json').write_text(json.dumps(r,indent=2),encoding='utf-8');assert all(v['legacy']['direction']>.1 and v['r3f']['direction']>.1 for v in r.values());print('SKY_DIRECTION_PASS',json.dumps(r))"])
for name,args in commands:
 p=subprocess.run(args,cwd=R,capture_output=True,text=True,encoding='utf-8',env={**os.environ,'PYTHONUTF8':'1'})
 (E/('final-'+name+'.txt')).write_text(p.stdout+p.stderr,encoding='utf-8');results.append({'name':name,'command':args,'cwd':str(R),'exit':p.returncode})
 (E/'final-commands.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(name,'exit',p.returncode,p.stdout[-4000:],p.stderr[-1000:],flush=True)
 if p.returncode:raise SystemExit(p.returncode)
source={str(p.relative_to(R)):{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted((R/'work/kinetic-tour-r3f/src').glob('*')) if p.is_file()}
(E/'implemented-source-hashes.json').write_text(json.dumps(source,indent=2),encoding='utf-8')
print('FINAL_M3_VERIFICATION_PASS',flush=True)
