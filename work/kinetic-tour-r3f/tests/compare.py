"""Same browser/viewport measurements: scheduling intervals, not GPU frame timings."""
import json,time
import browser_qa as b
b.SESSION='kinetic-codex-comparison-20261028'
E=b.E;results={};b.run('set','viewport','1920','1080');b.run('set','media','dark','no-reduced-motion')
probe='''new Promise(resolve=>{let samples=[],last=performance.now(),start=last,step=0;function tick(now){samples.push(now-last);last=now;const n=Math.floor((now-start)/650);if(n!==step){step=n;document.querySelector('nav [data-zone='+ (n%2?'motion':'home') +']').click();}if(now-start<2800)requestAnimationFrame(tick);else{samples=samples.slice(2).sort((a,b)=>a-b);resolve({samples:samples.length,averageMs:samples.reduce((a,b)=>a+b,0)/samples.length,medianMs:samples[Math.floor(samples.length/2)],p95Ms:samples[Math.floor(samples.length*.95)]});}}requestAnimationFrame(tick);})'''
for name,port in [('legacy',4181),('prototype',4180)]:
 item={};b.run('open',f'http://127.0.0.1:{port}/#home');time.sleep(.3)
 item['firstNavigation']=b.ev('performance.getEntriesByType("navigation").map(x=>({duration:x.duration,domContentLoaded:x.domContentLoadedEventEnd,transferSize:x.transferSize}))')
 b.run('snapshot','-i');b.run('click','#mode')
 for _ in range(50):
  ready=b.ev('!document.querySelector("canvas")?.hidden' if name=='legacy' else 'document.querySelector("main").dataset.mode==="three"')
  if ready and b.ev('!!document.querySelector("canvas")?.dataset.position'):break
  time.sleep(.3)
 else:raise AssertionError(name+' model unavailable')
 time.sleep(1.5)
 item['modelResources']=b.ev('performance.getEntriesByType("resource").filter(x=>x.name.endsWith(".glb")).map(x=>({name:x.name,duration:x.duration,transferSize:x.transferSize,encodedBodySize:x.encodedBodySize}))')
 item['browser']=b.ev('({userAgent:navigator.userAgent,viewport:[innerWidth,innerHeight],dpr:devicePixelRatio,memory:performance.memory?{usedJSHeapSize:performance.memory.usedJSHeapSize,totalJSHeapSize:performance.memory.totalJSHeapSize}:null})')
 item['gpu']=b.ev('(()=>{const gl=document.querySelector("canvas").getContext("webgl2");const e=gl?.getExtension("WEBGL_debug_renderer_info");return {vendor:e?gl.getParameter(e.UNMASKED_VENDOR_WEBGL):null,renderer:e?gl.getParameter(e.UNMASKED_RENDERER_WEBGL):null};})()')
 for zone in ['home','motion']:
  b.run('snapshot','-i');b.run('click','nav [data-zone='+zone+']');time.sleep(1.5);b.shot(name+'-'+zone+'-3d.png')
  item[zone+'Pose']=b.ev('({position:document.querySelector("canvas").dataset.position,target:document.querySelector("canvas").dataset.target})')
 item['transitionRafIntervals']=b.ev(probe)
 b.run('reload');time.sleep(.5);item['warmNavigation']=b.ev('performance.getEntriesByType("navigation").map(x=>({duration:x.duration,domContentLoaded:x.domContentLoadedEventEnd,transferSize:x.transferSize}))')
 results[name]=item;print(name,json.dumps(item),flush=True);(E/'performance.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
b.run('open','http://127.0.0.1:4180/#home');b.run('reload');b.run('snapshot','-i')
for mode in ['images','three']:
 if mode=='three':b.run('click','#mode');time.sleep(2)
 try:
  audit=b.run('a11y');(E/('a11y-'+mode+'.json')).write_text(json.dumps(audit,indent=2),encoding='utf-8');print('A11Y',mode,json.dumps(audit)[:3000],flush=True)
 except Exception as ex:print('A11Y ERROR',str(ex),flush=True)
(E/'clean-browser-errors.json').write_text(json.dumps(b.run('errors'),indent=2),encoding='utf-8')
(E/'clean-browser-console.json').write_text(json.dumps(b.run('console'),indent=2),encoding='utf-8')
b.run('close')
