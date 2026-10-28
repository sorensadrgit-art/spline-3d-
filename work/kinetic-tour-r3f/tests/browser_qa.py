"""Real agent-browser regression; isolated session, failure receipts retained."""
import base64,json,shutil,subprocess,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; E=ROOT/'tests/evidence'; E.mkdir(exist_ok=True)
CLI=shutil.which('agent-browser');PREFIX=[shutil.which('node'),str(Path(CLI).parent/'node_modules/agent-browser/bin/agent-browser.js')] if CLI.lower().endswith('.cmd') else [CLI]
SESSION='kinetic-codex-m2-20261028';checks=[]
def run(*args):
 p=subprocess.run([*PREFIX,'--session',SESSION,*args,'--json'],capture_output=True,text=True,encoding='utf-8',timeout=60)
 if p.returncode:raise RuntimeError(p.stdout[-1200:]+p.stderr[-1200:])
 for line in reversed(p.stdout.splitlines()):
  if line.startswith('{'):
   d=json.loads(line)
   if not d.get('success'):raise RuntimeError(str(d))
   return d.get('data')
 raise RuntimeError(p.stdout)
def ev(s):
 d=run('eval','--base64',base64.b64encode(s.encode()).decode());return d.get('result') if isinstance(d,dict) and 'result' in d else d
def click(selector):run('snapshot','-i');run('click',selector)
def check(name,fn):
 try:
  result=fn();checks.append({'name':name,'pass':True,'observed':result});print('PASS',name,json.dumps(result),flush=True)
 except Exception as e:
  checks.append({'name':name,'pass':False,'error':str(e)});print('FAIL',name,str(e),flush=True);raise
 finally:(E/'prototype-browser-checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
def assert_(value):
 if not value:raise AssertionError(value)
 return value
def wait_mode(mode,timeout=35):
 until=time.monotonic()+timeout
 while time.monotonic()<until:
  s=ev('({mode:document.querySelector("main").dataset.mode,status:document.querySelector("#status").textContent})')
  if s['mode']==mode:return s
  time.sleep(.3)
 raise AssertionError(s)
def shot(name):run('screenshot',str(E/name))
def open_home():
 run('open','http://127.0.0.1:4180/#home');run('reload');run('wait','#poster');ev('document.querySelector("#poster").decode().then(()=>true)')
def basic():
 open_home();assert_(ev('document.querySelector("main").dataset.mode==="images" && document.querySelector("#poster").naturalWidth>0 && !document.querySelector("canvas")'))
 click('[data-zone=motion]');assert_(ev('location.hash==="#motion" && document.querySelector("#poster").src.endsWith("motion.webp")'));shot('prototype-motion-image.png')
 # regression: skip never changes selected zone or hash
 run('focus','.skip');run('press','Enter');assert_(ev('location.hash==="#motion" && document.activeElement.id==="content"'))
 click('[data-zone=home]');run('back');assert_(ev('location.hash==="#motion"'));run('forward');assert_(ev('location.hash==="#home"'))
 run('press','1');assert_(ev('location.hash==="#motion"'));run('press','Home');assert_(ev('location.hash==="#home"'));run('press','0');
 shot('prototype-home-image.png');return {'images':2,'history':True,'skipFocus':True,'keyboard':True}
def three():
 click('#mode');wait_mode('three');time.sleep(1.5);shot('prototype-home-3d.png')
 assert_(ev('document.querySelector("canvas").dataset.position==="0,3.05,15.2"'))
 result=ev('''new Promise(resolve=>{const start=performance.now();document.querySelector('[data-zone=motion]').click();let firstDone=null,mid=null;function tick(){const elapsed=performance.now()-start;const c=document.querySelector('canvas');if(elapsed>=500&&!mid)mid=c.dataset.position;if(c.dataset.transition==='false'&&elapsed>100&&!firstDone)firstDone=elapsed;if(elapsed>1550)resolve({firstDone,mid,end:c.dataset.position});else requestAnimationFrame(tick);}requestAnimationFrame(tick);})''')
 assert_(result['end']=='-8.4,2.25,5.2');assert_(1200<result['firstDone']<1550);shot('prototype-motion-3d.png')
 # select repeatedly while moving, then verify actual last destination
 ev('document.querySelector("[data-zone=home]").click();setTimeout(()=>document.querySelector("[data-zone=motion]").click(),120);true');time.sleep(1.7)
 assert_(ev('document.querySelector("canvas").dataset.position==="-8.4,2.25,5.2"'))
 # real DOM input listeners, extreme drag and wheel are clamped
 ev('''(()=>{const c=document.querySelector('canvas');c.dispatchEvent(new WheelEvent('wheel',{deltaY:100000,bubbles:true,cancelable:true}));return true;})()''');time.sleep(.1)
 assert_(ev('JSON.parse(document.querySelector("canvas").dataset.orbit).distance===1.12'))
 click('#reset');time.sleep(1.5);assert_(ev('JSON.parse(document.querySelector("canvas").dataset.orbit).distance===1'))
 run('press','Escape');wait_mode('images');return result
def reduced_and_drag():
 open_home();click('#mode');wait_mode('three');time.sleep(1.5)
 run('set','media','dark','reduced-motion');run('press','1')
 assert_(ev('matchMedia("(prefers-reduced-motion: reduce)").matches && document.querySelector("canvas").dataset.position==="-8.4,2.25,5.2" && document.querySelector("canvas").dataset.transition==="false"'))
 # native pointer events exercise the DOM listeners with a real pointer capture target
 ev("document.querySelector('canvas').dataset.beforeDrag=document.querySelector('canvas').dataset.orbit;true")
 run('mouse','move','1100','550');run('mouse','down');run('mouse','move','1500','700');run('mouse','up')
 o=ev('JSON.parse(document.querySelector("canvas").dataset.orbit)');assert_(abs(o['yaw'])<=.15 and abs(o['pitch'])<=.35);assert_(o['yaw']!=0 or o['pitch']!=0)
 # A key selection cancels a gesture captured in the previous view.
 run('mouse','move','1100','550');run('mouse','down');run('press','Home');run('mouse','move','1500','700');run('mouse','up')
 assert_(ev('JSON.parse(document.querySelector("canvas").dataset.orbit).yaw===0'))
 # Hotspot activation moves focus to its expanded semantic detail control.
 ev('document.querySelector("#hotspots button:not([hidden])").click();true')
 assert_(ev('document.activeElement.getAttribute("aria-expanded")==="true" && document.activeElement.hasAttribute("aria-controls")'))
 run('set','media','dark','no-reduced-motion');run('press','Escape');return {'reducedMotionCut':True,'boundedDrag':o,'staleDragCancelled':True,'hotspotFocus':True}
def mobile():
 run('set','viewport','390','844');open_home();assert_(ev('!document.querySelector("canvas") && document.documentElement.scrollWidth<=innerWidth && !performance.getEntriesByType("resource").some(x=>x.name.endsWith(".glb"))'))
 shot('prototype-mobile-image.png');click('#mode');wait_mode('three');assert_(ev('performance.getEntriesByType("resource").some(x=>x.name.endsWith("studio-mobile.glb"))'));run('scroll','up','2000');time.sleep(1);shot('prototype-mobile-3d.png');run('press','Escape');run('set','viewport','1920','1080');return {'imageFirst':True,'mobileModel':True,'overflow':False}
def failure():
 open_home();ev('window.originalFetch=window.fetch;window.fetch=(input,options)=>String(input?.url||input).includes("studio-desktop.glb")?Promise.reject(new Error("QA model network failure")):window.originalFetch(input,options);true');click('#mode');s=wait_mode('images');assert_('unavailable' in s['status']);click('[data-zone=motion]');assert_(ev('location.hash==="#motion"'))
 ev('window.fetch=window.originalFetch;true');click('#mode');return wait_mode('three')
def sky_failure():
 open_home();run('network','route','**/models/blue-hour.jpg','--abort');click('#mode');wait_mode('images')
 run('network','unroute','**/models/blue-hour.jpg');click('#mode');return wait_mode('three',12)
def timeout():
 open_home();ev('window.originalFetch=window.fetch;window.fetch=(input,options)=>String(input?.url||input).includes("studio-desktop.glb")?new Promise(()=>{}):window.originalFetch(input,options);window.originalTimeout=window.setTimeout;window.setTimeout=(fn,ms,...args)=>window.originalTimeout(fn,ms===45000?1200:ms,...args);true');click('#mode');s=wait_mode('images');assert_('timed out' in s['status']);click('[data-zone=motion]');return s
def no_webgl():
 open_home();ev('window.originalContext=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(type,...args){return /webgl/.test(type)?null:window.originalContext.call(this,type,...args)};true');click('#mode');return wait_mode('images',10)
def loss():
 open_home();click('#mode');wait_mode('three');ev('document.querySelector("canvas").dispatchEvent(new Event("webglcontextlost",{cancelable:true}));true');s=wait_mode('images');click('[data-zone=motion]');assert_(ev('location.hash==="#motion"'));return s
if __name__=='__main__':
 try:
  run('set','viewport','1920','1080')
  check('Home/Motion images, history, keyboard, skip focus',basic)
  check('real model, 1350ms camera, rapid retarget, wheel, reset, Escape',three)
  check('reduced motion and native bounded drag',reduced_and_drag)
  check('mobile image-first, lighter model, no overflow',mobile)
  check('model error retains navigation and retry succeeds',failure)
  check('sky asset failure recovers on retry',sky_failure)
  check('asset timeout retains navigation (timer accelerated)',timeout)
  check('no WebGL returns to images immediately',no_webgl)
  check('context loss retains image navigation',loss)
 except Exception:traceback.print_exc();raise
 finally:
  (E/'prototype-browser-checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
