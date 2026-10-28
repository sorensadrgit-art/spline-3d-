import './style.css';
import './hotspots.css';
import {anchors, blend, zones, zoneFromHash, type Point, type Zone} from './tour.ts';
import type {Application, Entity} from 'playcanvas';

const $ = <T extends HTMLElement>(selector:string) => document.querySelector<T>(selector)!;
const canvas = $<HTMLCanvasElement>('#scene');
const poster = $<HTMLImageElement>('#poster');
const mode = $<HTMLButtonElement>('#mode');
const retry = $<HTMLButtonElement>('#retry');
const reset = $<HTMLButtonElement>('#reset');
const status = $('#status');
const reduced = matchMedia('(prefers-reduced-motion: reduce)');
const mobile = matchMedia('(max-width: 700px)');
let active = zoneFromHash(location.hash);
let app:Application|undefined, camera:Entity|undefined;
let ready=false, starting=false, interactive=false, destroyed=false;
let currentPosition:Point=[...active.position], currentTarget:Point=[...active.target];
let transition:{position:Point;target:Point;start:number}|undefined;
let orbit={yaw:0,pitch:0,distance:1};
let loadGeneration=0;
let frameCount=0, frameMs=0, slowSeconds=0;
let resizeObserver:ResizeObserver|undefined;
let frameRequest=0;
let projectPoint:((point:Point)=>{x:number;y:number;z:number})|undefined;

function announce(message:string) { status.textContent=message; }
function resizeCanvas() {
  if(!app)return;
  const parent=canvas.parentElement!;
  app.resizeCanvas(parent.clientWidth,parent.clientHeight);
  requestRender();
}
function select(zone:Zone, updateHistory=true) {
  active=zone;
  if(updateHistory && location.hash !== '#'+zone.id) history.pushState(null,'','#'+zone.id);
  $('#zone-number').textContent=zone.number;
  $('#zone-title').innerHTML=zone.title;
  $('#zone-description').textContent=zone.description;
  poster.src='/media/'+zone.image+'.webp';
  poster.dataset.zone=zone.id;
  poster.alt=zone.id==='home' ? 'Overview of the warm four-zone Kinetic Studio at blue hour.' : `${zone.id} zone of Kinetic Studio, rendered from the editable Blender master.`;
  document.querySelectorAll<HTMLButtonElement>('[data-zone]').forEach(button=>{
    if(button.dataset.zone===zone.id) button.setAttribute('aria-current','page');
    else button.removeAttribute('aria-current');
  });
  $('#details').replaceChildren(...zone.details.map(([title,body],i)=>{
    const wrapper=document.createElement('div');
    const button=document.createElement('button');
    button.textContent=title;button.setAttribute('aria-expanded','false');
    const content=document.createElement('p');content.id=`detail-${zone.id}-${i}`;content.textContent=body;content.hidden=true;
    button.setAttribute('aria-controls',content.id);
    button.addEventListener('click',()=>{
      const expanded=button.getAttribute('aria-expanded')==='true';
      button.setAttribute('aria-expanded',String(!expanded));content.hidden=expanded;
    });
    wrapper.append(button,content);return wrapper;
  }));
  transition={position:[...currentPosition],target:[...currentTarget],start:performance.now()};
  $('#hotspots').replaceChildren(...zone.details.map(([title],i)=>{
    const marker=document.createElement('button');marker.textContent=String(i+1);
    marker.setAttribute('aria-label',title);marker.title=title;
    marker.addEventListener('click',()=>{
      const button=$<HTMLButtonElement>(`[aria-controls="detail-${zone.id}-${i}"]`);
      if(button.getAttribute('aria-expanded')==='false')button.click();
      button.focus({preventScroll:true});
    });
    return marker;
  }));
  orbit={yaw:0,pitch:0,distance:1};
  announce(`${zone.id==='home'?'Workstation':zone.id+' zone'} selected. ${interactive?'Drag to explore.':'Image tour ready.'}`);
  requestRender();
}
function showImages(message='Image tour ready. Choose a space to continue.') {
  interactive=false;canvas.hidden=true;poster.hidden=false;
  mode.setAttribute('aria-pressed','false');mode.innerHTML='Explore in 3D <span aria-hidden="true">↗</span>';
  document.body.classList.remove('interactive');reset.hidden=true;
  $('#view-label').textContent='CINEMATIC IMAGE TOUR';announce(message);
  if(app) app.autoRender=false;
}
function show3D() {
  if(!ready||!app)return;
  interactive=true;canvas.hidden=false;poster.hidden=true;
  mode.setAttribute('aria-pressed','true');mode.textContent='View cinematic images';
  document.body.classList.add('interactive');reset.hidden=false;
  $('#view-label').textContent='LIVE 3D / DRAG TO EXPLORE';
  resizeCanvas();requestRender();
  announce(`${active.id==='home'?'Workstation':active.id} ready in 3D. Drag to look around; choose a zone to travel.`);
}
function requestRender() {
  if(!frameRequest && !destroyed) frameRequest=requestAnimationFrame(tick);
}
function tick(now:number) {
  frameRequest=0;
  if(transition) {
    const t=reduced.matches?1:(now-transition.start)/1350;
    currentPosition=blend(transition.position,active.position,t);
    currentTarget=blend(transition.target,active.target,t);
    if(t>=1)transition=undefined;
  }
  if(camera && interactive && app) {
    const [dx,dy,dz]=currentPosition.map((n,i)=>n-currentTarget[i]);
    const radius=Math.hypot(dx,dz)*orbit.distance;
    const theta=Math.atan2(dx,dz)+orbit.yaw;
    camera.setPosition(currentTarget[0]+Math.sin(theta)*radius,currentTarget[1]+dy*orbit.distance+orbit.pitch,currentTarget[2]+Math.cos(theta)*radius);
    camera.lookAt(...currentTarget);
    canvas.dataset.position=currentPosition.join(',');
    canvas.dataset.target=currentTarget.join(',');
    app.renderNextFrame=true;
    if(projectPoint)$('#hotspots').querySelectorAll<HTMLButtonElement>('button').forEach((marker,i)=>{
      const screen=projectPoint!(anchors[active.id][i]);
      marker.style.left=screen.x+'px';marker.style.top=screen.y+'px';
      marker.hidden=screen.z<0||screen.x<30||screen.x>canvas.clientWidth-30||screen.y<80||screen.y>canvas.clientHeight-160;
    });
  }
  if(transition)requestRender();
}
async function start3D(open=true) {
  if(starting)return;
  if(ready){show3D();return;}
  starting=true;retry.hidden=true;mode.disabled=true;
  announce('Loading the studio. The image tour remains available.');
  const generation=++loadGeneration;
  const timeout=setTimeout(()=>{
    if(!ready && generation===loadGeneration) {
      ++loadGeneration;starting=false;mode.disabled=false;retry.hidden=false;
      showImages('3D loading took too long. The complete image tour is available. Retry when ready.');
      app?.destroy();app=undefined;camera=undefined;
    }
  },45000);
  try {
    const pc=await import('playcanvas');
    if(generation!==loadGeneration||destroyed)return;
    app=new pc.Application(canvas,{graphicsDeviceOptions:{alpha:false,antialias:!mobile.matches,powerPreference:'high-performance',preserveDrawingBuffer:true}});
    app.autoRender=false;
    app.graphicsDevice.maxPixelRatio=mobile.matches?1:Math.min(devicePixelRatio,1.5);
    app.setCanvasFillMode(pc.FILLMODE_NONE,canvas.parentElement!.clientWidth,canvas.parentElement!.clientHeight);
    app.setCanvasResolution(pc.RESOLUTION_AUTO);
    app.scene.ambientLight=new pc.Color(.3,.3,.3);
    camera=new pc.Entity('Tour camera');
    camera.addComponent('camera',{clearColor:new pc.Color(.025,.035,.055),fov:mobile.matches?65:46,nearClip:.05,farClip:350,toneMapping:pc.TONEMAP_LINEAR});
    app.root.addChild(camera);
    projectPoint=(point:Point)=>camera!.camera!.worldToScreen(new pc.Vec3(...point));
    const src=mobile.matches?'/models/studio-mobile.glb':'/models/studio-desktop.glb';
    const asset=await new Promise<import('playcanvas').Asset>((resolve,reject)=>{
      app!.assets.loadFromUrl(src,'container',(error,asset)=> error||!asset ? reject(new Error(String(error||'Missing studio asset'))) : resolve(asset));
    });
    if(generation!==loadGeneration||destroyed){asset.unload();return;}
    const entity=(asset.resource as import('playcanvas').ContainerResource).instantiateRenderEntity({castShadows:false,receiveShadows:false});
    app.root.addChild(entity);
    resizeObserver=new ResizeObserver(resizeCanvas);
    resizeObserver.observe(canvas.parentElement!);
    app.on('update',(dt:number)=>{
      if(!interactive||document.hidden)return;
      frameCount++;frameMs+=dt*1000;
      if(frameCount>=120){
        const average=frameMs/frameCount;
        canvas.dataset.frameMs=average.toFixed(2);
        slowSeconds=average>50?slowSeconds+frameMs/1000:0;
        if(slowSeconds>5)showImages('This device is rendering slowly. Switched to the complete image tour.');
        frameCount=0;frameMs=0;
      }
    });
    canvas.addEventListener('webglcontextlost',event=>{event.preventDefault();ready=false;showImages('Graphics connection lost. The image tour is still available.');retry.hidden=false;app?.destroy();app=undefined;camera=undefined;});
    app.start();ready=true;
    const sky=await new Promise<import('playcanvas').Asset|undefined>(resolve=>{
      app!.assets.loadFromUrl('/models/blue-hour.jpg','texture',(error,asset)=>resolve(error?undefined:asset));
    });
    if(sky && generation===loadGeneration && app){
      const dome=new pc.Entity('Licensed blue-hour sky');dome.addComponent('render',{type:'sphere',castShadows:false,receiveShadows:false});
      const material=new pc.StandardMaterial();material.useLighting=false;material.diffuse=new pc.Color(0,0,0);material.emissive=new pc.Color(1,1,1);material.emissiveMap=sky.resource as import('playcanvas').Texture;material.cull=pc.CULLFACE_FRONT;material.update();
      dome.render!.meshInstances.forEach(mesh=>mesh.material=material);dome.setLocalScale(280,280,280);dome.setLocalEulerAngles(0,92,0);app.root.addChild(dome);
    }
    if(open)show3D();else announce('Image tour ready. The 3D studio is loaded when you want to explore.');
  } catch(error) {
    if(generation!==loadGeneration)return;
    console.warn('Studio 3D unavailable:',error);
    app?.destroy();app=undefined;camera=undefined;ready=false;
    showImages('3D is unavailable in this browser. All five cinematic views remain available.');retry.hidden=false;
  } finally {
    clearTimeout(timeout);
    if(generation===loadGeneration){starting=false;mode.disabled=false;}
  }
}
document.querySelectorAll<HTMLButtonElement>('[data-zone]').forEach(button=>button.addEventListener('click',()=>select(zones.find(z=>z.id===button.dataset.zone)!)));
mode.addEventListener('click',()=>interactive?showImages():void start3D());
retry.addEventListener('click',()=>void start3D());
reset.addEventListener('click',()=>select(active,false));
window.addEventListener('popstate',()=>select(zoneFromHash(location.hash),false));
window.addEventListener('hashchange',()=>select(zoneFromHash(location.hash),false));
document.addEventListener('keydown',event=>{
  if(event.altKey||event.ctrlKey||event.metaKey||/INPUT|TEXTAREA|SELECT/.test((event.target as HTMLElement).tagName))return;
  const index=event.key==='Home'?0:Number(event.key);
  if(/^[0-4]$/.test(event.key)||event.key==='Home'){event.preventDefault();select(zones[index]);}
  if(event.key==='Escape'&&interactive)showImages();
});
let pointer:{x:number;y:number;yaw:number;pitch:number}|undefined;
canvas.addEventListener('pointerdown',event=>{
  if(!interactive||transition)return;
  pointer={x:event.clientX,y:event.clientY,yaw:orbit.yaw,pitch:orbit.pitch};canvas.setPointerCapture(event.pointerId);
});
canvas.addEventListener('pointermove',event=>{
  if(!pointer)return;
  orbit.yaw=Math.max(-.15,Math.min(.15,pointer.yaw+(event.clientX-pointer.x)*.001));
  orbit.pitch=Math.max(-.35,Math.min(.35,pointer.pitch+(event.clientY-pointer.y)*.002));requestRender();
});
for(const type of ['pointerup','pointercancel','lostpointercapture'])canvas.addEventListener(type,()=>{pointer=undefined;});
canvas.addEventListener('wheel',event=>{if(interactive&&!transition){event.preventDefault();orbit.distance=Math.max(.9,Math.min(1.12,orbit.distance+event.deltaY*.0003));requestRender();}},{passive:false});
reduced.addEventListener('change',()=>requestRender());
document.addEventListener('visibilitychange',()=>{if(!document.hidden)requestRender();});
window.addEventListener('pagehide',()=>{destroyed=true;++loadGeneration;cancelAnimationFrame(frameRequest);resizeObserver?.disconnect();app?.destroy();});
select(active,false);
// Lower-memory devices start in the complete image tour, with 3D available on request.
if(!mobile.matches && !(navigator as Navigator & {connection?:{saveData:boolean}}).connection?.saveData) void start3D(false);
