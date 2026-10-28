"""Build review artifact and record manual screenshot paint checks for visible markers."""
import hashlib,json,math,statistics
from pathlib import Path
from PIL import Image
E=Path(__file__).resolve().parent
zones=['home','motion','clinical','engineering','projects']
html=['<!doctype html><meta charset="utf-8"><title>Kinetic M3 locked-camera review</title><style>body{background:#11191b;color:#f3eee4;font:16px Arial;margin:24px}section{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-bottom:36px}img{width:100%;height:auto}h2{grid-column:1/-1}a{color:#ddbd96}figure{margin:0}figcaption{padding:8px} @media(max-width:900px){section{grid-template-columns:1fr}}</style><h1>M3 five-zone review</h1><p>1920×1080, exact original cameras. Click full captures. PlayCanvas remains authoritative. GLB views have baked/simple geometry and differ from Cycles; this is not photoreal acceptance.</p>']
for z in zones:
 html.append('<section><h2>'+z.title()+'</h2>')
 for label,name in [('Fresh PlayCanvas',f'legacy-{z}-3d.png'),('M3 real GLB',f'{z}-3d.png'),('Original Cycles image in M3 UI',f'{z}-image.png')]:html.append(f'<figure><a href="{name}"><img src="{name}" alt="{z} {label}"></a><figcaption>{label}</figcaption></figure>')
 html.append('</section>')
html.append('<p>Emulated mobile: <a href="mobile-projects-image.png">image-first</a>, <a href="mobile-projects-3d.png">lighter GLB</a>. No physical-phone test.</p>')
(E/'comparison.html').write_text('\n'.join(html),encoding='utf-8')

def luminance(rgb):
 c=[x/255 for x in rgb];c=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in c];return sum(a*b for a,b in zip(c,[.2126,.7152,.0722]))
fg=(243,238,228);bg=(21,35,36);ratio=(luminance(fg)+.05)/(luminance(bg)+.05)
views=json.loads((E/'five-views.json').read_text(encoding='utf-8'));out={}
for z in zones:
 im=Image.open(E/(z+'-3d.png')).convert('RGB');assert im.size==(1920,1080)
 marks=[]
 for m in views[z]['markers']:
  if m['hidden']:continue
  x,y=round(m['x']),round(m['y']);pixels=[im.getpixel((x+dx,y+dy)) for dx in range(-15,-9) for dy in range(-4,5)]
  sampled=tuple(statistics.median(p[c] for p in pixels) for c in range(3));assert sampled==bg,(z,m,sampled)
  marks.append({'label':m['label'],'paintedFillMedianRGB':sampled,'computedTextRGB':fg,'declaredContrast':ratio,'physicallyClickable':m['hit']})
 out[z]=marks
(E/'manual-contrast.json').write_text(json.dumps({'method':'Screenshot left interior fill strip, outside text/border; computed opaque text color; screenshots visually inspected. Scope: locked desktop anchors only. Axe incomplete retained, not suppressed.','textToFillRatio':ratio,'markers':out},indent=2),encoding='utf-8')
print('COMPARISON_AND_PAINT_CHECK_PASS',ratio)
