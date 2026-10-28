"""Success-only browser capabilities and transition timeline; no OS GPU reset."""
import importlib.util,json,time
from pathlib import Path
E=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('m5',E/'browser.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
b=m.b;b.SESSION='kinetic-m5-supplement-20261028';run=m.run
try:
 run('set','viewport','1920','1080');b.open_home();b.click('#mode');b.wait_mode('three');m.settled('home')
 run('errors','--clear');run('console','--clear')
 gpu=b.ev("""(()=>{const c=document.querySelector('canvas'),gl=c.getContext('webgl2'),d=gl.getExtension('WEBGL_debug_renderer_info');return {ua:navigator.userAgent,viewport:[innerWidth,innerHeight],dpr:devicePixelRatio,vendor:d?gl.getParameter(d.UNMASKED_VENDOR_WEBGL):null,renderer:d?gl.getParameter(d.UNMASKED_RENDERER_WEBGL):null,version:gl.getParameter(gl.VERSION),extensions:gl.getSupportedExtensions(),timerSupported:!!gl.getExtension('EXT_disjoint_timer_query_webgl2'),timerMeasured:false,hardwareResetPerformed:false}})()""")
 timeline=b.ev("""new Promise(resolve=>{const c=document.querySelector('canvas'),start=performance.now();let started=false,done=null,samples=[];document.querySelector('nav [data-zone=motion]').click();function tick(){const t=performance.now()-start,transition=c.dataset.transition,position=c.dataset.position;if(transition==='true')started=true;if(samples.length<110)samples.push({t,transition,position});if(started&&transition==='false'&&position==='-8.4,2.25,5.2'&&done===null)done=t;if(t<1800)requestAnimationFrame(tick);else resolve({started,done,samples})}requestAnimationFrame(tick)})""")
 out={'gpu':gpu,'transition':timeline,'errors':run('errors'),'console':run('console'),'timingMeaning':'rAF-observed transition completion, not GPU frame duration or FPS'}
 (E/'browser-capabilities-and-timeline.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
 assert timeline['started'] and 1200<timeline['done']<1550,timeline
 print('M5_BROWSER_SUPPLEMENT_PASS',timeline['done'],gpu['renderer'],flush=True)
finally:run('close')
