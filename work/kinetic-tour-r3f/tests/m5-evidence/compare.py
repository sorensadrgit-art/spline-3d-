"""Sequential same-browser cold/warm measurements; rAF is scheduling, not GPU time."""
import importlib.util,json,time,sys
from pathlib import Path
E=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('m4',E/'browser.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
b=m.b;b.SESSION='kinetic-m5-comparison-20261028';run=m.run
probe="""new Promise(resolve=>{let a=[],last=performance.now(),start=last;function tick(t){a.push(t-last);last=t;if(t-start<2500)requestAnimationFrame(tick);else{a=a.slice(2).sort((x,y)=>x-y);resolve({samples:a.length,median:a[Math.floor(a.length*.5)],p95:a[Math.floor(a.length*.95)],mean:a.reduce((x,y)=>x+y,0)/a.length})}}requestAnimationFrame(tick)})"""
results=json.loads((E/'performance.json').read_text()) if '--mobile-only' in sys.argv else []
try:
 for width,height,label in ([(390,844,'emulated-mobile')] if '--mobile-only' in sys.argv else [(1920,1080,'desktop'),(390,844,'emulated-mobile')]):
  for name,port in [('legacy',4191),('r3f',4190)]:
   b.SESSION='kinetic-m5-perf-'+name+'-'+label+'-20261028';run('set','viewport',str(width),str(height))
   # A fresh owned session/origin is browser-cache cold; OS/filesystem cache uncontrolled.
   for cache in ['cold-browser','warm-browser']:
    run('open',f'http://127.0.0.1:{port}/#home')
    if cache=='warm-browser':run('reload')
    run('wait','#mode:not([disabled])')
    b.ev("window.m4long=[];window.m4obs=new PerformanceObserver(l=>window.m4long.push(...l.getEntries().map(e=>({start:e.startTime,duration:e.duration}))));window.m4obs.observe({type:'longtask',buffered:true});true")
    image=b.ev('({imageFirst:!document.querySelector("canvas"),modelBeforeOptIn:performance.getEntriesByType("resource").filter(e=>e.name.endsWith(".glb"))})')
    b.click('#mode');run('wait','--fn','!!document.querySelector("canvas")?.dataset.position && !document.querySelector("canvas").hidden')
    if name=='r3f':b.wait_mode('three')
    time.sleep(1.6)
    item={'name':name,'viewport':label,'cache':cache,'initial':image,'environment':b.ev('({ua:navigator.userAgent,viewport:[innerWidth,innerHeight],dpr:devicePixelRatio,cores:navigator.hardwareConcurrency,memory:navigator.deviceMemory})'),'heapBefore':b.ev('performance.memory?.usedJSHeapSize')}
    if cache=='warm-browser' and label=='desktop':
     for zone in m.Z:
      b.click('nav [data-zone='+zone+']');time.sleep(1.6)
      if name=='r3f':m.settled(zone);m.inspect(zone)
      b.shot(name+'-'+zone+'-3d.png')
    if label=='emulated-mobile' and cache=='warm-browser':b.shot(name+'-mobile-3d.png')
    item['rafSchedulingIntervalsMs']=b.ev(probe)
    item['navigation']=b.ev('performance.getEntriesByType("navigation").map(e=>e.toJSON())')
    item['resources']=b.ev('performance.getEntriesByType("resource").map(e=>({name:e.name,duration:e.duration,transferSize:e.transferSize,encodedBodySize:e.encodedBodySize,decodedBodySize:e.decodedBodySize,initiatorType:e.initiatorType}))')
    item['longTasks']=b.ev('window.m4long');item['heapAfter']=b.ev('performance.memory?.usedJSHeapSize')
    if name=='r3f':item['renderer']=b.ev('(()=>{const c=document.querySelector("canvas"),s='+m.STATE+';return {render:s.gl.info.render,memory:s.gl.info.memory,programs:s.gl.info.programs.length,dpr:s.viewport.dpr}})()')
    results.append(item);(E/'performance.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(name,label,cache,item['rafSchedulingIntervalsMs'],flush=True)
    b.click('#mode');time.sleep(.4)
   run('close')
 # Preserve baseline/candidate identical if no objective fix selected.
 html=['<!doctype html><meta charset="utf-8"><title>M5 five-zone comparison</title><style>body{background:#111;color:#eee;font:16px Arial}section{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}img{width:100%}h2{grid-column:1/-1}</style><h1>M5 actual five-zone comparison</h1><p>Fresh legacy and R3F at 1920x1080. Cycles references are contextual, not pixel parity. No runtime change selected yet.</p>']
 for zone in m.Z:
  ref='proof' if zone=='home' else zone
  html.append('<section><h2>'+zone+'</h2><div>PlayCanvas<img src="legacy-'+zone+'-3d.png"></div><div>R3F<img src="r3f-'+zone+'-3d.png"></div><div>Cycles source<img src="../../../kinetic-blender/kinetic-studio-'+ref+'-v006.png"></div></section>')
 (E/'comparison.html').write_text(''.join(html),encoding='utf-8')
finally:run('close')
