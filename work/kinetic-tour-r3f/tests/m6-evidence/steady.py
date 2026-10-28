import importlib.util,json
from pathlib import Path
E=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('m6',E/'browser.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
b=m.b;run=m.run;b.SESSION='kinetic-m6-steady'
try:
 run('set','viewport','390','844');b.open_home();run('errors','--clear');run('console','--clear');b.click('#mode');b.wait_mode('three');m.settled('home');run('scroll','up','2000')
 result=b.ev("""new Promise(resolve=>{let frameCount=0,visibleFrames=0;const overlaps=[],start=performance.now();document.querySelector('nav [data-zone=clinical]').click();setTimeout(()=>document.querySelector('nav [data-zone=projects]').click(),180);function tick(){frameCount++;const v=[...document.querySelectorAll('#hotspots button:not([hidden])')].map(e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height}});if(v.length)visibleFrames++;for(let i=0;i<v.length;i++)for(let j=i+1;j<v.length;j++){const a=v[i],b=v[j];if(Math.abs(a.x-b.x)<48&&Math.abs(a.y-b.y)<48)overlaps.push({a,b})}if(performance.now()-start<1900)requestAnimationFrame(tick);else resolve({frameCount,visibleFrames,overlaps})}requestAnimationFrame(tick)})""")
 assert result['frameCount']>10 and result['visibleFrames']>0 and result['overlaps']==[],result
 result['errors']=run('errors');result['console']=run('console');(E/'steady-and-rapid-frames.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
finally:run('close')
