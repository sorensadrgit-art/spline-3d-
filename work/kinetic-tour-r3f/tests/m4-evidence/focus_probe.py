import importlib.util,json,time
from pathlib import Path
E=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('m4',E/'browser.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);b=m.b;b.SESSION='kinetic-m4-focus-20261028';run=m.run
try:
 run('set','viewport','1920','1080');b.open_home();b.click('#mode');b.wait_mode('three');m.settled('home')
 before=b.ev('(()=>{let e=document.querySelector("#hotspots button:not([hidden])");e.focus();window.m4focused=e;return {label:e.getAttribute("aria-label"),focus:document.activeElement===e}})()')
 run('set','viewport','800','600');time.sleep(.5)
 after=b.ev('({hidden:window.m4focused.hidden,active:document.activeElement.tagName,activeLabel:document.activeElement.getAttribute("aria-label"),visibleFocus:document.activeElement!==document.body&&!document.activeElement.hidden})')
 (E/'focus-probe.json').write_text(json.dumps({'before':before,'after':after},indent=2),encoding='utf-8');print(before,after)
 assert not after['hidden'] or after['visibleFocus'],'Focused marker became hidden without visible focus restoration'
finally:run('close')
