"""Fresh mobile marker hit/overlap observation, separately from the 15-group suite."""
import importlib.util,json,time
from pathlib import Path
E=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('m5',E/'browser.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
b=m.b;b.SESSION='kinetic-m5-mobile-markers-20261028';run=m.run
try:
 run('set','viewport','390','844');b.open_home();b.click('#mode');b.wait_mode('three');m.settled('home');run('scroll','up','2000');time.sleep(.5)
 d=b.ev("""(()=>{const nodes=[...document.querySelectorAll('#hotspots button')],markers=nodes.map(e=>{const r=e.getBoundingClientRect();return {label:e.getAttribute('aria-label'),hidden:e.hidden,rect:{x:r.x,y:r.y,width:r.width,height:r.height},centerHit:!e.hidden&&document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)===e}});const overlap=[];for(let i=0;i<markers.length;i++)for(let j=i+1;j<markers.length;j++){const a=markers[i],b=markers[j];if(!a.hidden&&!b.hidden&&Math.min(a.rect.x+a.rect.width,b.rect.x+b.rect.width)>Math.max(a.rect.x,b.rect.x)&&Math.min(a.rect.y+a.rect.height,b.rect.y+b.rect.height)>Math.max(a.rect.y,b.rect.y))overlap.push([a.label,b.label])}return {viewport:[innerWidth,innerHeight],markers,overlap,semanticDetails:[...document.querySelectorAll('.details button')].map(e=>e.textContent),modelResources:performance.getEntriesByType('resource').filter(e=>e.name.endsWith('.glb')).map(e=>e.name)}})()""")
 b.shot('mobile-markers-probe.png');d['status']='FAIL' if d['overlap'] or any(not x['centerHit'] for x in d['markers'] if not x['hidden']) else 'PASS'
 (E/'mobile-marker-probe.json').write_text(json.dumps(d,indent=2),encoding='utf-8');print('MOBILE_MARKER_PROBE',json.dumps(d),flush=True)
finally:run('close')
