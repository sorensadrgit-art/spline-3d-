"""Locked-camera sky direction check; RGB ratios resist the left UI scrim.
Patches are sky-only in both runtimes; hue 240=blue, 300=magenta.
Positive right-minus-left red/blue means the legacy blue-to-violet direction.
"""
import argparse, colorsys, json, statistics
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'evidence'
PATCHES={'home':[(300,110,340,140),(1500,110,1540,140)],'motion':[(300,110,340,140),(1550,200,1590,225)]}
def measure(path, zone):
 im=Image.open(path).convert('RGB'); assert im.size==(1920,1080), im.size
 patches=[]
 for box in PATCHES[zone]:
  crop=im.crop(box); pixels=[crop.getpixel((x,y)) for y in range(crop.height) for x in range(crop.width)]; rgb=[statistics.median(p[c] for p in pixels) for c in range(3)]
  h,s,v=colorsys.rgb_to_hsv(*(c/255 for c in rgb))
  patches.append({'box':box,'rgb':rgb,'hue':h*360,'redBlue':rgb[0]/rgb[2]})
 return {'path':str(path),'patches':patches,'direction':patches[1]['redBlue']-patches[0]['redBlue']}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--candidate',type=Path,default=BASE);p.add_argument('--prefix',default='prototype');p.add_argument('--receipt',type=Path,required=True);a=p.parse_args()
 results={}; ok=True
 for zone in PATCHES:
  ref=measure(BASE/f'legacy-{zone}-3d.png',zone); candidate=measure(a.candidate/f'{a.prefix}-{zone}-3d.png',zone)
  passed=ref['direction']>.10 and candidate['direction']>.10
  results[zone]={'reference':ref,'candidate':candidate,'pass':passed};ok &= passed
 a.receipt.write_text(json.dumps(results,indent=2),encoding='utf-8'); print(json.dumps(results,indent=2));raise SystemExit(0 if ok else 1)
