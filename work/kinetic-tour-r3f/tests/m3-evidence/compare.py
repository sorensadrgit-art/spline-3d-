"""Same actual browser/hardware/viewport comparison; intervals are NOT GPU FPS."""
import importlib.util,json,time
from pathlib import Path
E=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('m3',E/'browser.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
b=m.b;b.SESSION='kinetic-m3-comparison-20261028';run=m.run
probe="""new Promise(resolve=>{const zones=['home','motion','clinical','engineering','projects'];let times=[],last=performance.now(),start=last,step=-1;function tick(now){times.push(now-last);last=now;const n=Math.floor((now-start)/650);if(n!==step){step=n;document.querySelector('nav [data-zone='+zones[n%5]+']').click()}if(now-start<3900)requestAnimationFrame(tick);else{times=times.slice(2).sort((a,b)=>a-b);resolve({samples:times.length,meanMs:times.reduce((a,b)=>a+b,0)/times.length,medianMs:times[Math.floor(times.length/2)],p95Ms:times[Math.floor(times.length*.95)]})}}requestAnimationFrame(tick)})"""
results={}
try:
 run('set','viewport','1920','1080');run('set','media','dark','no-reduced-motion')
 for name,port in [('legacy',4184),('r3f',4183)]:
  run('open',f'http://127.0.0.1:{port}/#home');run('reload');run('wait','#mode:not([disabled])');run('snapshot','-i');run('click','#mode')
  run('wait','--fn','!!document.querySelector("canvas")?.dataset.position && !document.querySelector("canvas").hidden')
  if name=='r3f':b.wait_mode('three')
  time.sleep(1.5)
  item={'viewportHardware':b.ev('({userAgent:navigator.userAgent,viewport:[innerWidth,innerHeight],dpr:devicePixelRatio,hardwareConcurrency:navigator.hardwareConcurrency,deviceMemory:navigator.deviceMemory,heap:performance.memory?.usedJSHeapSize})'),
    'navigation':b.ev('performance.getEntriesByType("navigation").map(e=>({duration:e.duration,domContentLoaded:e.domContentLoadedEventEnd,transferSize:e.transferSize}))'),
    'modelResources':b.ev('performance.getEntriesByType("resource").filter(e=>e.name.endsWith(".glb")).map(e=>({name:e.name,duration:e.duration,transferSize:e.transferSize,encodedBodySize:e.encodedBodySize}))'),
    'gpu':b.ev('(()=>{const gl=document.querySelector("canvas").getContext("webgl2");const e=gl?.getExtension("WEBGL_debug_renderer_info");return {vendor:e?gl.getParameter(e.UNMASKED_VENDOR_WEBGL):null,renderer:e?gl.getParameter(e.UNMASKED_RENDERER_WEBGL):null}})()')}
  for zone in m.Z:
   b.click('nav [data-zone='+zone+']')
   if name=='r3f':m.settled(zone)
   else:time.sleep(1.5)
   pose=b.ev('({position:document.querySelector("canvas").dataset.position,target:document.querySelector("canvas").dataset.target})')
   assert all(abs(float(a)-float(v))<1e-10 for key in ['position','target'] for a,v in zip(pose[key].split(','),m.Z[zone][key].split(','))),pose
   if name=='legacy':b.shot('legacy-'+zone+'-3d.png')
  item['rafSchedulingIntervals']=b.ev(probe)
  results[name]=item;(E/'performance.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(name,json.dumps(item),flush=True)
 # Both mobile modes; all five images remain usable; mobile DPR confirmed from real renderer.
 run('set','viewport','390','844');b.open_home()
 mobile={'imageFirst':b.ev('!document.querySelector("canvas") && !performance.getEntriesByType("resource").some(e=>e.name.endsWith(".glb"))')}
 for zone in m.Z:
  b.click('nav [data-zone='+zone+']');b.ev('document.querySelector("#poster").decode().then(()=>true)');assert b.ev('document.documentElement.scrollWidth<=innerWidth')
 b.shot('mobile-projects-image.png');b.click('#mode');b.wait_mode('three');m.settled('projects');run('scroll','up','3000');b.shot('mobile-projects-3d.png')
 mobile['actual']=m.inspect('projects');assert mobile['actual']['dpr']==1;assert any(x.endswith('studio-mobile.glb') for x in mobile['actual']['resources'])
 mobile['overflow']=b.ev('document.documentElement.scrollWidth>innerWidth');assert not mobile['overflow']
 (E/'mobile.json').write_text(json.dumps(mobile,indent=2),encoding='utf-8')
 run('set','viewport','1920','1080');b.open_home();b.click('#mode');b.wait_mode('three');m.settled('home');time.sleep(.5)
 # Keep full session diagnostics; probe deliberately logs context loss on temporary context.
 for cmd in ['errors','console']:(E/('comparison-'+cmd+'.json')).write_text(json.dumps(run(cmd),indent=2),encoding='utf-8')
 run('errors','--clear');run('console','--clear')
 for zone in m.Z:b.click('nav [data-zone='+zone+']');m.settled(zone)
 for cmd in ['errors','console']:(E/('steady-success-'+cmd+'.json')).write_text(json.dumps(run(cmd),indent=2),encoding='utf-8')
finally:run('close')
