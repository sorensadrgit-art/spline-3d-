"""M3 live GLB acceptance using the installed agent-browser CLI, isolated port/session."""
import importlib.util,json,time,sys,math
from pathlib import Path
E=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('m2_qa',E.parent/'browser_qa.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
b.SESSION='kinetic-m4-20261028-isolated';b.E=E
original_run=b.run
def run(*args):
 return original_run(*(x.replace('127.0.0.1:4180','127.0.0.1:4187') if isinstance(x,str) else x for x in args))
b.run=run
Z={
 'home':{'position':'0,3.05,15.2','target':'0,2.1,-2.3','titles':['The shared center','Material language','At blue hour']},
 'motion':{'position':'-8.4,2.25,5.2','target':'-8.55,1.55,-1.4','titles':['Capture rig','Calibration floor','Motion display']},
 'clinical':{'position':'-4.5,2,1.4','target':'-4.4,1.7,-4','titles':['Study model','Anatomy prints','Analysis desk']},
 'engineering':{'position':'4.4,2.05,1.8','target':'4.95,1.75,-4.2','titles':['Actuator study','Electronics bench','Tool wall']},
 'projects':{'position':'9.1,2,3','target':'9.45,1.6,-2.7','titles':['Materials table','Project wall','Shared seating']}}

STATE = "(()=>{let f=c[Object.keys(c).find(k=>k.startsWith('__reactFiber'))];while(f){for(let h=f.memoizedState;h;h=h.next){const o=h.memoizedState;if(o?.isObject3D&&o.__r3f?.root)return o.__r3f.root.getState()}f=f.return}throw Error('No mounted GLB state found')})()"
A={'home':[[0,1.6,-3],[-.6,.45,2.8],[0,3,-5.7]],'motion':[[-10.4,2.35,.4],[-8.55,.25,-1],[-7.3,1.5,-2.2]],'clinical':[[-5.39,1.3,-3.13],[-4.7,2.4,-4.79],[-4.3,.85,-3.78]],'engineering':[[5.6,1.3,-4],[5,.88,-3.86],[4.9,2.1,-4.7]],'projects':[[9.4,.88,-1.8],[10.55,2.5,-4.85],[8.6,.7,-.8]]}

def settled(zone):
 run('wait','--fn','document.querySelector("canvas")?.dataset.transition === "false" && document.querySelector("canvas").dataset.position === '+json.dumps(Z[zone]['position']))

def inspect(zone):
 d=b.ev(r'''(()=>{const c=document.querySelector('canvas');const r=c.getBoundingClientRect();const state=STATE_PLACEHOLDER;return {mode:document.querySelector('main').dataset.mode,zone:document.querySelector('main').dataset.zone,position:c.dataset.position,target:c.dataset.target,actualPosition:state.camera.position.toArray(),actualDirection:state.camera.getWorldDirection(new state.camera.position.constructor()).toArray(),fov:state.camera.fov,model:state.scene.children.filter(o=>o.type==='Group').map(o=>({type:o.type,meshes:(()=>{let n=0;o.traverse(x=>{if(x.isMesh)n++});return n})()})),dpr:state.viewport.dpr,markers:[...document.querySelectorAll('#hotspots button')].map(e=>({label:e.getAttribute('aria-label'),hidden:e.hidden,x:parseFloat(e.style.left),y:parseFloat(e.style.top),hit:(()=>{const r=e.getBoundingClientRect();return document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)===e})(),color:getComputedStyle(e).color,background:getComputedStyle(e).backgroundColor})),details:[...document.querySelectorAll('.details button span:first-of-type')].map(e=>e.textContent),expanded:document.querySelectorAll('.details [aria-expanded=true]').length,resources:performance.getEntriesByType('resource').filter(e=>/\.glb$/.test(e.name)).map(e=>e.name)}})()'''.replace('STATE_PLACEHOLDER', STATE))
 assert d['mode']=='three' and d['zone']==zone,d
 assert d['position']==Z[zone]['position'] and d['target']==Z[zone]['target'],d
 want=list(map(float,Z[zone]['position'].split(',')))
 assert all(abs(a-v)<1e-10 for a,v in zip(d['actualPosition'],want)),d
 target=list(map(float,Z[zone]['target'].split(',')));vec=[t-p for t,p in zip(target,want)];length=math.sqrt(sum(x*x for x in vec))
 assert all(abs(a-v/length)<1e-10 for a,v in zip(d['actualDirection'],vec)),d
 assert d['details']==Z[zone]['titles'],d
 assert [m['label'] for m in d['markers']]==['Inspect '+x for x in Z[zone]['titles']],d
 assert any(m['meshes']>=14 for m in d['model']),d
 assert len(d['resources'])==1,d
 projected=b.ev('(()=>{const c=document.querySelector("canvas");const s='+STATE+';return '+json.dumps(A[zone])+'.map(a=>{const p=s.camera.position.clone().set(...a).project(s.camera);return {x:(p.x+1)*s.size.width/2,y:(1-p.y)*s.size.height/2}})})()')
 for m,p in zip(d['markers'],projected):assert abs(m['x']-p['x'])<.01 and abs(m['y']-p['y'])<.01,(zone,m,p)
 assert all(m['hidden'] or m['hit'] for m in d['markers']),(zone,'visible marker covered by interface',d['markers'])
 d['independentProjections']=projected
 return d

def five_views():
 b.open_home();b.click('#mode');b.wait_mode('three');settled('home')
 views={}
 for zone in Z:
  b.click('nav [data-zone='+zone+']');settled(zone);views[zone]=inspect(zone)
  b.shot(zone+'-3d.png')
  run('snapshot','-i')
  # Exercise all semantic details, including projected markers where visible.
  for i in range(3):
   b.click('.details button[aria-controls=detail-'+str(i)+']')
   assert b.ev('document.querySelector("#detail-'+str(i)+'").hidden===false')
   b.click('.details button[aria-controls=detail-'+str(i)+']')
  visible=[i for i,m in enumerate(views[zone]['markers']) if not m['hidden'] and m['hit']]
  assert visible, (zone,'no physically clickable projected hotspot',views[zone])
  b.click('#hotspots button:nth-child('+str(visible[0]+1)+')')
  assert b.ev('document.activeElement.getAttribute("aria-expanded")==="true"')
  (E/('a11y-'+zone+'.json')).write_text(json.dumps(run('a11y'),indent=2),encoding='utf-8')
 # Details must close and canvas instance/model stay alive on zone changes.
 b.click('nav [data-zone=clinical]');settled('clinical');assert inspect('clinical')['expanded']==0
 run('back');settled('projects');run('forward');settled('clinical')
 for i,zone in enumerate(Z):run('press',str(i));settled(zone)
 run('press','Home');settled('home')
 (E/'five-views.json').write_text(json.dumps(views,indent=2),encoding='utf-8')
 return {z:{'actualPosition':v['actualPosition'],'target':v['target'],'clickableMarkers':sum(m['hit'] and not m['hidden'] for m in v['markers'])} for z,v in views.items()}

def images_and_hash():
 run('press','Escape');b.wait_mode('images')
 for zone in Z:
  b.click('nav [data-zone='+zone+']');b.ev('document.querySelector("#poster").decode().then(()=>true)');b.shot(zone+'-image.png')
  assert b.ev('!document.querySelector("canvas") && document.querySelector("#poster").naturalWidth>0 && !document.querySelector("#mode").disabled')
  run('reload');run('wait','#poster');assert b.ev('document.querySelector("main").dataset.zone')==zone
 (E/'a11y-images.json').write_text(json.dumps(run('a11y'),indent=2),encoding='utf-8')
 return {'allFiveImages':True,'reloadHashes':True}

def rapid_and_reduced():
 b.open_home();b.click('#mode');b.wait_mode('three');settled('home')
 result=b.ev('''new Promise(resolve=>{const c=document.querySelector('canvas'),start=performance.now();document.querySelector('nav [data-zone=clinical]').click();const samples=[];setTimeout(()=>{samples.push(c.dataset.position);document.querySelector('nav [data-zone=engineering]').click()},350);setTimeout(()=>{samples.push(c.dataset.position);document.querySelector('nav [data-zone=projects]').click()},600);setTimeout(()=>resolve({sameCanvas:c===document.querySelector('canvas'),samples,end:c.dataset.position,totalMs:performance.now()-start}),2100)})''')
 assert result['sameCanvas'] and result['end']==Z['projects']['position'],result
 run('set','media','dark','reduced-motion')
 for i,zone in enumerate(Z):
  run('press',str(i));settled(zone);d=inspect(zone);assert b.ev('document.querySelector("canvas").dataset.transition')=='false'
 run('set','media','dark','no-reduced-motion')
 return result

def stale_load():
 b.open_home();b.ev('''window.origFetch=fetch;window.releaseModel=null;window.fetch=(u,o)=>String(u).includes('studio-desktop.glb')?new Promise(resolve=>window.releaseModel=()=>window.origFetch(u).then(resolve)):window.origFetch(u,o);true''')
 b.click('#mode');run('wait','--fn','!!window.releaseModel');run('press','Escape');b.wait_mode('images');b.click('nav [data-zone=projects]')
 b.ev('window.releaseModel();true');time.sleep(1)
 assert b.ev('document.querySelector("main").dataset.mode==="images" && !document.querySelector("canvas") && location.hash==="#projects"')
 return {'lateModelCannotReopen':True}

def inspected_navigation():
 b.open_home();b.click('#mode');b.wait_mode('three');settled('home')
 b.ev("document.querySelector('canvas').dispatchEvent(new WheelEvent('wheel',{deltaY:100000,cancelable:true}));true")
 run('wait','--fn','JSON.parse(document.querySelector("canvas").dataset.orbit).distance===1.12')
 result=b.ev('new Promise(resolve=>{const c=document.querySelector("canvas"),s='+STATE+';const before=s.camera.position.toArray();document.querySelector("nav [data-zone=clinical]").click();requestAnimationFrame(()=>resolve({before,after:s.camera.position.toArray(),from:c.dataset.position}))})')
 jump=math.dist(result['before'],result['after']);assert jump<.08,result
 settled('clinical');result['firstFrameDisplacement']=jump
 b.click('#reset');settled('clinical');return result

def focus_routes():
 b.open_home();b.click('#mode');b.wait_mode('three');settled('home')
 run('focus','.details button[aria-controls=detail-0]');run('press','4');settled('projects')
 after_key=b.ev('({tag:document.activeElement.tagName,zone:document.activeElement.dataset.zone,controls:document.activeElement.getAttribute("aria-controls")})')
 assert after_key['tag']=='BUTTON',after_key
 b.ev('document.querySelector("#hotspots button:not([hidden])").focus();true');run('press','Escape');b.wait_mode('images')
 after_escape=b.ev('document.activeElement.id');assert after_escape=='mode',after_escape
 return {'afterKey':after_key,'afterEscape':after_escape}

if __name__=='__main__':
 try:
  run('set','viewport','1920','1080');run('set','media','dark','no-reduced-motion')
  if '--captures-only' not in sys.argv:
   for name,fn in [('baseline image/history/keys/skip',b.basic),('1350ms/model/rapid/wheel/reset/Escape',b.three),('reduced/native drag/focus',b.reduced_and_drag),('mobile image/model/overflow',b.mobile),('model failure/retry',b.failure),('sky failure/retry',b.sky_failure),('accelerated timeout',b.timeout),('no WebGL',b.no_webgl),('synthetic context loss',b.loss),('cancelled stale load',stale_load)]:b.check(name,fn)
  # Fresh page and cleared diagnostics separate deliberate failure messages.
  b.open_home();run('errors','--clear');run('console','--clear')
  b.check('five real destinations/cameras/hotspots/details/history/keys',five_views)
  b.check('five images and restored hashes',images_and_hash)
  b.check('cross-zone rapid retarget and all reduced cuts',rapid_and_reduced)
  b.check('inspection continuity',inspected_navigation)
  b.check('focus after keyboard navigation and Escape',focus_routes)
  (E/'clean-errors.json').write_text(json.dumps(run('errors'),indent=2),encoding='utf-8')
  (E/'clean-console.json').write_text(json.dumps(run('console'),indent=2),encoding='utf-8')
 finally:
  (E/'browser-checks.json').write_text(json.dumps(b.checks,indent=2),encoding='utf-8')
  run('close')
