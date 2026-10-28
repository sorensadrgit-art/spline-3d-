import importlib.util,json,time
from pathlib import Path
E=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('m6',E/'browser.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
b=m.b;run=m.run;b.SESSION='kinetic-m6-focus-observe'
try:
 run('set','viewport','1920','1080');b.open_home();b.click('#mode');b.wait_mode('three');m.settled('home');run('focus','#hotspots button:nth-child(3)')
 out=[]
 for w,h in [(390,844),(320,600),(320,400),(430,844)]:
  run('set','viewport',str(w),str(h));time.sleep(.5)
  out.append(b.ev("""(()=>{const c=document.querySelector('canvas');return {viewport:[innerWidth,innerHeight],canvas:c.getBoundingClientRect().toJSON(),focus:document.activeElement.outerHTML,markers:[...document.querySelectorAll('#hotspots button')].map(e=>({hidden:e.hidden,rect:e.getBoundingClientRect().toJSON(),left:e.style.left,top:e.style.top}))}})()"""))
 (E/'focus-observation.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
finally:run('close')
