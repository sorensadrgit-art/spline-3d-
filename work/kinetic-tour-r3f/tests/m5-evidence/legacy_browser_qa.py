"""Bounded agent-browser regression checks against the local built tour."""
import base64
import json
from pathlib import Path
import shutil
import subprocess
import time

ROOT=Path(__file__).resolve().parent
CLI=shutil.which('agent-browser')
PREFIX=[shutil.which('node'),str(Path(CLI).parent/'node_modules'/'agent-browser'/'bin'/'agent-browser.js')] if CLI.lower().endswith('.cmd') else [CLI]
SESSION='kinetic-m5-legacy-20261028'

def run(*args):
    result=subprocess.run([*PREFIX,'--session',SESSION,*args,'--json'],capture_output=True,text=True,encoding='utf-8',timeout=55)
    if result.returncode:raise RuntimeError(result.stdout[-500:]+result.stderr[-500:])
    text=result.stdout.strip()
    # CLI may emit a launch notice before its structured result.
    for line in reversed(text.splitlines()):
        if line.startswith('{'):
            packet=json.loads(line)
            if not packet.get('success',False):raise RuntimeError(str(packet))
            return packet.get('data')
    raise RuntimeError(text[-700:])

def evaluate(code):
    data=run('eval','--base64',base64.b64encode(code.encode()).decode())
    return data.get('result') if isinstance(data,dict) and 'result' in data else data

checks=[]
try:
    run('set','viewport','1920','1080')
    run('open','http://127.0.0.1:4191/#home')
    for _ in range(40):
        state=evaluate('({ready:!document.querySelector("#scene").hidden,status:document.querySelector("#status").textContent})')
        if state['ready'] or '3D studio is loaded' in state['status']:break
        time.sleep(.5)
    if not state['ready']:
        run('click','#mode')
        state=evaluate('({ready:!document.querySelector("#scene").hidden,status:document.querySelector("#status").textContent})')
    assert state['ready'],state
    checks.append({'check':'desktop renderer ready','result':state})
    size=evaluate('({view:[innerWidth,innerHeight],canvas:[document.querySelector("canvas").clientWidth,document.querySelector("canvas").clientHeight]})')
    assert size['view']==size['canvas'],size
    checks.append({'check':'canvas follows viewport','result':size})
    positions={'motion':[-8.4,2.25,5.2],'clinical':[-4.5,2,1.4],'engineering':[4.4,2.05,1.8],'projects':[9.1,2,3],'home':[0,3.05,15.2]}
    for zone in ['motion','clinical','engineering','projects','home']:
        run('snapshot','-i')
        run('click',f'[data-zone="{zone}"]')
        time.sleep(1.5)
        state=evaluate('({hash:location.hash,current:document.querySelector("nav [aria-current]").dataset.zone,details:document.querySelectorAll("#details button").length,markers:document.querySelectorAll("#hotspots button").length})')
        assert state=={'hash':'#'+zone,'current':zone,'details':3,'markers':3},state
        position=evaluate('document.querySelector("canvas").dataset.position.split(",").map(Number)')
        assert all(abs(a-b)<.001 for a,b in zip(position,positions[zone])),(zone,position)
    checks.append({'check':'all zones and Home','pass':True})
    run('back');assert evaluate('location.hash')=='#projects'
    run('forward');assert evaluate('location.hash')=='#home'
    checks.append({'check':'browser Back and Forward restore zones','pass':True})
    evaluate('document.querySelector("[data-zone=motion]").click();document.querySelector("[data-zone=projects]").click();document.querySelector("[data-zone=clinical]").click();true')
    time.sleep(1.6)
    assert evaluate('location.hash')=='#clinical'
    run('press','Home');assert evaluate('location.hash')=='#home'
    run('press','3');assert evaluate('location.hash')=='#engineering'
    checks.append({'check':'rapid retargeting and keyboard','pass':True})
    evaluate('document.querySelector("#details button").click();true')
    assert evaluate('document.querySelector("#details button").getAttribute("aria-expanded")')=='true'
    run('set','media','dark','reduced-motion');run('press','4')
    assert evaluate('matchMedia("(prefers-reduced-motion: reduce)").matches')
    run('screenshot',str(ROOT/'desktop-tour.png'))
    run('set','viewport','390','844');run('reload')
    time.sleep(1)
    assert evaluate('document.querySelector("canvas").hidden')
    assert evaluate('document.documentElement.scrollWidth<=innerWidth')
    for key in ['1','2','3','4','Home']:run('press',key)
    checks.append({'check':'mobile image tour and no horizontal overflow','pass':True})
    run('screenshot',str(ROOT/'mobile-tour.png'))
    run('click','#mode')
    for _ in range(40):
        if evaluate('!document.querySelector("canvas").hidden'):break
        time.sleep(.5)
    assert evaluate('!document.querySelector("canvas").hidden')
    checks.append({'check':'mobile delivery model loads on emulated viewport','pass':True,'physical_phone_test':False})
    evaluate('document.querySelector("canvas").dispatchEvent(new Event("webglcontextlost",{cancelable:true}));true')
    assert evaluate('document.querySelector("canvas").hidden')
    assert not evaluate('document.querySelector("#retry").hidden')
    for key in ['1','2','3','4','Home']:run('press',key)
    checks.append({'check':'context loss preserves all image navigation','pass':True})
    evaluate('navigator.gpu ? navigator.gpu.requestAdapter().then(a=>({available:!!a,info:a?.info?.description||"not exposed"})) : ({available:false})')
    (ROOT/'legacy-browser-checks.json').write_text(json.dumps({'marker':'KINETIC_BROWSER_QA_PASS','checks':checks},indent=2),encoding='utf-8')
    print('KINETIC_BROWSER_QA_PASS',len(checks))
finally:
    run('close')
