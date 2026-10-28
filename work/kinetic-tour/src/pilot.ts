import * as pc from 'playcanvas';
const button=document.querySelector<HTMLButtonElement>('#load')!;
const canvas=document.querySelector<HTMLCanvasElement>('#pilot')!;
const status=document.querySelector<HTMLParagraphElement>('#status')!;
let app:pc.Application|undefined;
const compressed=new URLSearchParams(location.search).has('sog');
button.addEventListener('click',()=>{
  button.disabled=true;status.textContent='Loading the experimental Gaussian scene…';
  try{
    canvas.hidden=false;
    app=new pc.Application(canvas,{graphicsDeviceOptions:{alpha:false,antialias:false}});
    app.graphicsDevice.maxPixelRatio=1;
    app.setCanvasFillMode(pc.FILLMODE_NONE,canvas.clientWidth,canvas.clientHeight);app.setCanvasResolution(pc.RESOLUTION_AUTO);
    const camera=new pc.Entity('Pilot camera');camera.addComponent('camera',{clearColor:new pc.Color(.04,.06,.07),fov:43,nearClip:.05,farClip:100});app.root.addChild(camera);
    let yaw=0,pitch=0;
    const pose=()=>{camera.setPosition(4.95+Math.sin(yaw)*3.5,1.85+pitch,-4.3+Math.cos(yaw)*3.5);camera.lookAt(4.95,1.75,-4.3);};pose();
    app.assets.loadFromUrl(compressed?'/models/engineering-pilot.sog':'/models/engineering-pilot.ply','gsplat',(error,asset)=>{
      if(error||!asset){status.textContent='The Gaussian viewer could not load. The comparison remains available.';app?.destroy();app=undefined;canvas.hidden=true;button.disabled=false;return;}
      const entity=new pc.Entity('Engineering trained Gaussians');entity.addComponent('gsplat',{asset:asset});
      // SuperSplat exports include its file-space Z flip; raw Brush PLY uses Blender Z-up.
      entity.setLocalEulerAngles(...(compressed?[0,0,180]:[-90,0,0]) as [number,number,number]);
      app!.root.addChild(entity);app!.start();status.textContent=`Experimental ${compressed?'compressed SOG':'Gaussian'} scene loaded. Drag to inspect.`;
    });
    let drag:{x:number;y:number;yaw:number;pitch:number}|undefined;
    canvas.style.touchAction='none';canvas.addEventListener('pointerdown',e=>{drag={x:e.clientX,y:e.clientY,yaw,pitch};canvas.setPointerCapture(e.pointerId);});
    canvas.addEventListener('pointermove',e=>{if(drag){yaw=Math.max(-.3,Math.min(.3,drag.yaw+(e.clientX-drag.x)*.001));pitch=Math.max(-.3,Math.min(.3,drag.pitch+(e.clientY-drag.y)*.002));pose();}});
    canvas.addEventListener('pointerup',()=>drag=undefined);canvas.addEventListener('pointercancel',()=>drag=undefined);
    new ResizeObserver(()=>app?.resizeCanvas(canvas.parentElement!.clientWidth,innerHeight*.65)).observe(canvas.parentElement!);
  }catch(error){status.textContent='Graphics support is unavailable. The comparison remains available.';canvas.hidden=true;button.disabled=false;app?.destroy();app=undefined;console.warn(error);}
});
window.addEventListener('pagehide',()=>app?.destroy());
