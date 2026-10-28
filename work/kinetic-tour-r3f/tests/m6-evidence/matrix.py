"""M6 actual rectangles, grounded projections, semantic access and focus regression."""
import importlib.util,json,time
from pathlib import Path
E=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('m6',E/'browser.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
b=m.b;run=m.run;b.SESSION='kinetic-m6-final-matrix'
rows=[]
def measure():
 return b.ev("""(()=>{const nodes=[...document.querySelectorAll('#hotspots button')];return {viewport:[innerWidth,innerHeight],overflow:document.documentElement.scrollWidth>innerWidth,markers:nodes.map(e=>{const r=e.getBoundingClientRect();return {label:e.getAttribute('aria-label'),hidden:e.hidden,x:r.x,y:r.y,w:r.width,h:r.height,hit:!e.hidden&&document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)===e}})}})()""")
def validate(d):
 assert not d['overflow'],d
 visible=[x for x in d['markers'] if not x['hidden']]
 assert visible,d
 for a in visible:assert a['w']>=44 and a['h']>=44 and a['hit'] and a['label'].startswith('Inspect '),d
 for i,a in enumerate(visible):
  for z in visible[i+1:]:
   dx=max(z['x']-(a['x']+a['w']),a['x']-(z['x']+z['w']))
   dy=max(z['y']-(a['y']+a['h']),a['y']-(z['y']+z['h']))
   assert max(dx,dy)>=3.98,('spacing',d)
try:
 for width,height in [(320,844),(390,844),(430,844),(1920,1080)]:
  run('set','viewport',str(width),str(height));b.open_home()
  assert b.ev('!document.querySelector("canvas") && !performance.getEntriesByType("resource").some(x=>x.name.endsWith(".glb"))')
  b.click('#mode');b.wait_mode('three');m.settled('home');run('scroll','up','2000')
  for zone in m.Z:
   b.click('nav [data-zone='+zone+']');m.settled(zone);run('scroll','up','2000')
   view=m.inspect(zone);d=measure();d.update(zone=zone,dpr=view['dpr'],resources=view['resources'],projections=view['independentProjections'])
   validate(d)
   if width<700:assert d['dpr']==1 and d['resources'][0].endswith('studio-mobile.glb'),d
   # Keyboard Enter must open every semantic detail, including hidden marker equivalents.
   for i in range(3):
    run('focus','.details button[aria-controls=detail-'+str(i)+']');run('press','Enter')
    assert b.ev('document.querySelector("#detail-'+str(i)+'").hidden===false && document.activeElement.getAttribute("aria-controls")==="detail-'+str(i)+'"')
    run('press','Enter')
   run('scroll','up','2000');b.shot(str(width)+'-'+zone+'.png');rows.append(d)
   if width==390:(E/('mobile-a11y-'+zone+'.json')).write_text(json.dumps(run('a11y'),indent=2))
   (E/'marker-matrix.json').write_text(json.dumps(rows,indent=2))
  print('MATRIX_PASS',width,len(rows),flush=True)
 # A genuine visible marker loses eligibility on resize: focus must survive on its semantic equivalent.
 b.click('nav [data-zone=home]');m.settled('home')
 run('focus','#hotspots button:nth-child(3)');assert b.ev('document.activeElement===document.querySelectorAll("#hotspots button")[2]')
 run('set','viewport','390','844');run('wait','--fn','document.querySelectorAll("#hotspots button")[2].hidden')
 focus=b.ev('({controls:document.activeElement.getAttribute("aria-controls"),tag:document.activeElement.tagName})')
 assert focus=={'controls':'detail-2','tag':'BUTTON'},focus
 (E/'resize-focus.json').write_text(json.dumps(focus,indent=2))
 # Check intermediate rapid retarget frames rather than only settled views.
 run('scroll','up','2000')
 samples=b.ev("""new Promise(resolve=>{const samples=[],start=performance.now();document.querySelector('nav [data-zone=clinical]').click();setTimeout(()=>document.querySelector('nav [data-zone=projects]').click(),180);function tick(){const v=[...document.querySelectorAll('#hotspots button:not([hidden])')].map(e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height}});for(let i=0;i<v.length;i++)for(let j=i+1;j<v.length;j++){const a=v[i],b=v[j];if(Math.abs(a.x-b.x)<48&&Math.abs(a.y-b.y)<48)samples.push({elapsed:performance.now()-start,a,b})}if(performance.now()-start<1800)requestAnimationFrame(tick);else resolve(samples)}requestAnimationFrame(tick)})""")
 assert samples==[],samples
 (E/'rapid-frame-overlaps.json').write_text(json.dumps(samples))
 print('M6_MATRIX_PASS',len(rows),'focus',focus,flush=True)
finally:run('close')
