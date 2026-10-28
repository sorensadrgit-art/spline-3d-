"""Inspect trained Gaussian output and compare the reserved synthetic views."""
import hashlib
import json
import math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parent
dataset=ROOT/'dataset-v005';run=ROOT/'pilot-v005'
ply=run/'engineering_3000.ply'
raw=ply.read_bytes();header=raw[:raw.index(b'end_header')+10].decode('ascii')
for required in ['f_dc_0','opacity','scale_0','rot_0']:assert 'property float '+required in header
count=int(next(line.split()[-1] for line in header.splitlines() if line.startswith('element vertex')))
frames=json.loads((dataset/'transforms_test.json').read_text())['frames']
results=[];sheet=Image.new('RGB',(1280,4*270),(15,21,23));draw=ImageDraw.Draw(sheet)
for i,frame in enumerate(frames):
    source=dataset/frame['file_path'];output=run/'eval_3000'/source.name
    expected=Image.open(source).convert('RGB');actual=Image.open(output).convert('RGB')
    assert expected.size==actual.size
    a=np.asarray(expected,dtype=np.float32)/255;b=np.asarray(actual,dtype=np.float32)/255
    mse=float(np.square(a-b).mean());psnr=-10*math.log10(max(mse,1e-12))
    results.append({'view':source.name,'psnr_db':round(psnr,3),'rgb_rmse':round(math.sqrt(mse),5)})
    if i in [0,3,6,9]:
        row=[0,3,6,9].index(i);expected.thumbnail((620,238));actual.thumbnail((620,238))
        sheet.paste(expected,(10,row*270+28));sheet.paste(actual,(650,row*270+28))
        draw.text((10,row*270+8),'CYCLES SOURCE / '+source.name,fill=(230,218,196))
        draw.text((650,row*270+8),f'TRAINED GAUSSIANS / {psnr:.2f} dB',fill=(230,218,196))
sheet.save(ROOT/'pilot-comparison.jpg',quality=91)
mean=float(np.mean([r['psnr_db'] for r in results]))
report={'trainer':'Brush v0.3.0, local Windows CLI','training_steps':3000,'training_frames':132,'held_out_frames':12,'gaussians':count,'source_scene':'v005 (preserved cinematic checkpoint, before v006 normal correction)','ply':str(ply),'ply_bytes':len(raw),'ply_sha256':hashlib.sha256(raw).hexdigest(),'mean_held_out_psnr_db':round(mean,3),'min_held_out_psnr_db':min(r['psnr_db'] for r in results),'views':results,'status':'bounded-pilot-trained-awaiting-visual-and-viewer-review','limitations':'Synthetic single-zone views. Pixel metrics do not establish full-room coverage, thin-edge quality or physical-phone performance. v006 remains the editable master.'}
(ROOT/'pilot-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('KINETIC_SPLAT_PILOT_CHECK_PASS',json.dumps(report),flush=True)
