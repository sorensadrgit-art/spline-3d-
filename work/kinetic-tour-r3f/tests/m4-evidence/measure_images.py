from pathlib import Path
from PIL import Image,ImageStat
import json,colorsys
E=Path(__file__).resolve().parent
regions={'home':(1060,540,1100,565),'motion':(1000,540,1040,565),'clinical':(1000,540,1040,565),'engineering':(1000,540,1040,565),'projects':(1000,540,1040,565)}
def lum(rgb):
 v=[x/255 for x in rgb];v=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in v];return sum(a*b for a,b in zip(v,[.2126,.7152,.0722]))
out={}
for z,rect in regions.items():
 out[z]={}
 for label,path in [('legacy',E/('legacy-'+z+'-3d.png')),('m3-historical',E.parent/'m3-evidence'/(z+'-3d.png')),('m4',E/('r3f-'+z+'-3d.png'))]:
  im=Image.open(path).convert('RGB');assert im.size==(1920,1080);rgb=ImageStat.Stat(im.crop(rect)).mean;h,l,s=colorsys.rgb_to_hls(*[v/255 for v in rgb]);out[z][label]={'region':rect,'rgb':rgb,'relativeLuminance':lum(rgb),'hueDegrees':h*360,'saturation':s,'note':'Fixed central scene patch, not material/color accuracy or Cycles pixel parity'}
 fg=[243,238,228];bg=[21,35,36];out[z]['declaredMarkerContrast']=(lum(fg)+.05)/(lum(bg)+.05)
 # Check the marker paint at sampled ring interior only when fresh browser receipt gives visible center.
(E/'image-samples.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
html=['<!doctype html><meta charset="utf-8"><title>M4 five-zone comparison</title><style>body{background:#111;color:#eee;font:16px Arial}section{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}img{width:100%}h2{grid-column:1/-1}</style><h1>M4 five-zone comparison</h1><p>Actual 1920x1080 browser captures. M3 is labeled historical. M4 source unchanged: baseline equals candidate; no justified runtime tuning. Cycles is contextual, not pixel-matching.</p>']
for z in regions:
 ref='proof' if z=='home' else z
 html.append('<section><h2>'+z+'</h2><div>Fresh PlayCanvas<img src="legacy-'+z+'-3d.png"></div><div>Historical M3 before<img src="../m3-evidence/'+z+'-3d.png"></div><div>Fresh M4 retained candidate<img src="r3f-'+z+'-3d.png"></div><div>Cycles source<img src="../../../kinetic-blender/kinetic-studio-'+ref+'-v006.png"></div></section>')
(E/'comparison.html').write_text(''.join(html),encoding='utf-8');print('FIVE_VIEW_IMAGE_MEASUREMENTS_PASS')
