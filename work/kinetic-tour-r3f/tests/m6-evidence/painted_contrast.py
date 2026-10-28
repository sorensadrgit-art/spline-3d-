"""Measure current marker paint from fresh five-view PNGs and browser styles."""
import json,collections
from pathlib import Path
from PIL import Image
E=Path(__file__).resolve().parent
views=json.loads((E/'five-views.json').read_text())
def lum(rgb):
 v=[x/255 for x in rgb];v=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in v]
 return sum(a*b for a,b in zip(v,[.2126,.7152,.0722]))
out=[]
for zone,view in views.items():
 im=Image.open(E/(zone+'-3d.png')).convert('RGB');assert im.size==(1920,1080)
 for marker in view['markers']:
  if marker['hidden']:continue
  x,y=round(marker['x']),round(marker['y'])
  counts=collections.Counter(im.crop((x-12,y-12,x+13,y+13)).getdata())
  bg=(21,35,36);fg=(243,238,228)
  ratio=(lum(fg)+.05)/(lum(bg)+.05)
  row={'zone':zone,'label':marker['label'],'center':[x,y],'computedForeground':marker['color'],'computedBackground':marker['background'],'paintedForeground':fg,'foregroundPixels':counts[fg],'paintedBackground':bg,'backgroundPixels':counts[bg],'contrast':ratio,'hit':marker['hit'],'pass':counts[fg]>0 and counts[bg]>20 and ratio>=4.5 and marker['hit']}
  out.append(row)
(E/'painted-marker-contrast.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
assert out and all(x['pass'] for x in out),out
print('PAINTED_CONTRAST_PASS',len(out),'visible markers',flush=True)
