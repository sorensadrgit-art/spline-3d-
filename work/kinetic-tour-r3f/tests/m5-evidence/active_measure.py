import importlib.util,json,time,sys
from pathlib import Path
E=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('m4',E/'browser.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);b=m.b;run=m.run
results=json.loads((E/'active-performance-and-steady-diagnostics.json').read_text()) if '--r3f-only' in sys.argv else {}
for name,port in ([('r3f',4190)] if '--r3f-only' in sys.argv else [('legacy',4191),('r3f',4190)]):
 b.SESSION='kinetic-m5-active-'+name+'-20261028'
 try:
  run('set','viewport','1920','1080');run('open',f'http://127.0.0.1:{port}/#home');run('wait','#mode:not([disabled])');b.click('#mode');run('wait','--fn','!!document.querySelector("canvas")?.dataset.position && !document.querySelector("canvas").hidden')
  if name=='r3f':b.wait_mode('three')
  time.sleep(1.6);run('errors','--clear');run('console','--clear')
  probe="""new Promise(resolve=>{const zones=['home','motion','clinical','engineering','projects'];let a=[],last=performance.now(),start=last,step=-1;function tick(t){a.push(t-last);last=t;let n=Math.floor((t-start)/650);if(n!==step){step=n;document.querySelector('nav [data-zone='+zones[n%5]+']').click()}if(t-start<3900)requestAnimationFrame(tick);else{a=a.slice(2).sort((x,y)=>x-y);resolve({samples:a.length,median:a[Math.floor(a.length*.5)],p95:a[Math.floor(a.length*.95)],mean:a.reduce((x,y)=>x+y,0)/a.length})}}requestAnimationFrame(tick)})"""
  results[name]={'activeCameraRafSchedulingMs':b.ev(probe),'heap':b.ev('performance.memory?.usedJSHeapSize')}
  time.sleep(1.6)
  for zone in m.Z:
   b.click('nav [data-zone='+zone+']');time.sleep(1.5)
   if name=='r3f':m.settled(zone)
  gl="""(()=>{const gl=document.querySelector('canvas').getContext('webgl2'),e=gl?.getExtension('WEBGL_debug_renderer_info');return {vendor:e?gl.getParameter(e.UNMASKED_VENDOR_WEBGL):null,renderer:e?gl.getParameter(e.UNMASKED_RENDERER_WEBGL):null}})()"""
  results[name]['gpu']=b.ev(gl)
  results[name]['steadyErrors']=run('errors');results[name]['steadyConsole']=run('console')
  (E/'active-performance-and-steady-diagnostics.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(name,json.dumps(results[name]),flush=True)
 finally:
  try:run('close')
  except Exception as e:print('CLEANUP_FAILURE',str(e),flush=True)
