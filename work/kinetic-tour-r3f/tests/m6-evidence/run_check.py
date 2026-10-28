import subprocess,sys,json,os
from pathlib import Path
E=Path(__file__).resolve().parent
name=sys.argv[1]
p=subprocess.run([sys.executable,'-u',str(E/(name+'.py'))],capture_output=True,text=True,encoding='utf-8',env={**os.environ,'PYTHONUTF8':'1'})
(E/(name+'-run.txt')).write_text(p.stdout+p.stderr,encoding='utf-8')
(E/(name+'-exit.json')).write_text(json.dumps({'command':[sys.executable,'-u',str(E/(name+'.py'))],'exit':p.returncode},indent=2))
print(p.stdout[-3000:]+p.stderr[-2000:]);sys.exit(p.returncode)
