"""Isolated follow-up run; reuse unchanged nine-group functions at port 4182."""
import importlib.util,json,time,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('baseline_qa',ROOT.parent/'browser_qa.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
b.SESSION='kinetic-sky-parity-20261028-isolated';b.E=ROOT
original_run=b.run
def run(*args):
 return original_run(*(x.replace('127.0.0.1:4180','127.0.0.1:4182') if isinstance(x,str) else x for x in args))
b.run=run
if __name__=='__main__':
 try:
  run('set','viewport','1920','1080');run('set','media','dark','no-reduced-motion')
  if '--suite' in sys.argv:
   for name,fn in [('image/history/keyboard/skip',b.basic),('model/camera/rapid/wheel/reset/Escape',b.three),('reduced-motion/drag/focus',b.reduced_and_drag),('mobile',b.mobile),('model failure/retry',b.failure),('sky failure/retry',b.sky_failure),('timeout',b.timeout),('no WebGL',b.no_webgl),('context loss',b.loss)]:b.check(name,fn)
  b.open_home();b.click('#mode');b.wait_mode('three');time.sleep(1.5)
  poses={}
  for zone in ['home','motion']:
   b.click('nav [data-zone='+zone+']');time.sleep(1.6)
   poses[zone]=b.ev('({position:document.querySelector("canvas").dataset.position,target:document.querySelector("canvas").dataset.target,markers:[...document.querySelectorAll("#hotspots button")].map(e=>{const s=getComputedStyle(e);return {label:e.textContent,color:s.color,background:s.backgroundColor,opacity:s.opacity,hidden:e.hidden,ancestors:[...function*(n){while(n){yield n;n=n.parentElement}}(e)].map(n=>{const c=getComputedStyle(n);return {tag:n.tagName,id:n.id,opacity:c.opacity,filter:c.filter,mixBlendMode:c.mixBlendMode}})}})})')
   b.shot('after-'+zone+'-3d.png')
  (ROOT/'live-observations.json').write_text(json.dumps(poses,indent=2),encoding='utf-8')
  for cmd in ['errors','console','a11y']:
   (ROOT/(('suite-' if '--suite' in sys.argv else 'clean-')+cmd+'.json')).write_text(json.dumps(run(cmd),indent=2),encoding='utf-8')
 finally:run('close')
