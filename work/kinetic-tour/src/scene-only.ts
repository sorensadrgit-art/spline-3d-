import './scene-only.css';
import {blend, zones, type Point, type Zone} from './tour.ts';
import type {Application, Asset, Entity} from 'playcanvas';

const canvas = document.querySelector<HTMLCanvasElement>('#scene')!;
const poster = document.querySelector<HTMLImageElement>('#poster')!;
const status = document.querySelector<HTMLElement>('#status')!;
const mobile = matchMedia('(max-width: 700px)');
const reduced = matchMedia('(prefers-reduced-motion: reduce)');

let app: Application | undefined;
let camera: Entity | undefined;
let active: Zone = zones[0];
let currentPosition: Point = [...active.position];
let currentTarget: Point = [...active.target];
let transition: {position: Point; target: Point; start: number} | undefined;
let orbit = {yaw: 0, pitch: 0, distance: 1};
let pointer: {x: number; y: number; yaw: number; pitch: number} | undefined;
let frameRequest = 0;
let loadGeneration = 0;
let destroyed = false;
let resizeObserver: ResizeObserver | undefined;

function requestRender() {
  if (!frameRequest && !destroyed) frameRequest = requestAnimationFrame(renderFrame);
}

function renderFrame(now: number) {
  frameRequest = 0;
  if (document.hidden || !app || !camera) return;

  if (transition) {
    const t = reduced.matches ? 1 : (now - transition.start) / 1350;
    currentPosition = blend(transition.position, active.position, t);
    currentTarget = blend(transition.target, active.target, t);
    if (t >= 1) transition = undefined;
  }

  const dx = currentPosition[0] - currentTarget[0];
  const dz = currentPosition[2] - currentTarget[2];
  const radius = Math.hypot(dx, dz) * orbit.distance;
  const theta = Math.atan2(dx, dz) + orbit.yaw;
  camera.setPosition(
    currentTarget[0] + Math.sin(theta) * radius,
    currentTarget[1] + (currentPosition[1] - currentTarget[1]) * orbit.distance + orbit.pitch,
    currentTarget[2] + Math.cos(theta) * radius
  );
  camera.lookAt(...currentTarget);
  canvas.dataset.position = currentPosition.join(',');
  canvas.dataset.target = currentTarget.join(',');
  app.renderNextFrame = true;
  if (transition) requestRender();
}

function resizeCanvas() {
  if (!app) return;
  const bounds = canvas.parentElement!;
  app.resizeCanvas(bounds.clientWidth, bounds.clientHeight);
  requestRender();
}

function setZone(zone: Zone) {
  if (!app || !camera) return;
  active = zone;
  transition = {position: [...currentPosition], target: [...currentTarget], start: performance.now()};
  orbit = {yaw: 0, pitch: 0, distance: 1};
  requestRender();
}

function showPoster(message: string) {
  ++loadGeneration;
  status.textContent = message;
  canvas.hidden = true;
  poster.hidden = false;
  canvas.dataset.ready = 'false';
  resizeObserver?.disconnect();
  resizeObserver = undefined;
  app?.destroy();
  app = undefined;
  camera = undefined;
}

async function startScene() {
  const generation = ++loadGeneration;
  let watchdog: ReturnType<typeof setTimeout> | undefined;
  try {
    const pc = await import('playcanvas');
    if (destroyed || generation !== loadGeneration) return;

    const instance = new pc.Application(canvas, {
      graphicsDeviceOptions: {
        alpha: false,
        antialias: !mobile.matches,
        powerPreference: 'high-performance',
        preserveDrawingBuffer: true
      }
    });
    app = instance;
    instance.autoRender = false;
    instance.graphicsDevice.maxPixelRatio = mobile.matches ? 1 : Math.min(devicePixelRatio, 1.5);
    instance.setCanvasFillMode(
      pc.FILLMODE_NONE,
      canvas.parentElement!.clientWidth,
      canvas.parentElement!.clientHeight
    );
    instance.setCanvasResolution(pc.RESOLUTION_AUTO);
    instance.scene.ambientLight = new pc.Color(.3, .3, .3);

    camera = new pc.Entity('Scene camera');
    camera.addComponent('camera', {
      clearColor: new pc.Color(.025, .035, .055),
      fov: mobile.matches ? 65 : 46,
      nearClip: .05,
      farClip: 350,
      toneMapping: pc.TONEMAP_LINEAR
    });
    instance.root.addChild(camera);

    watchdog = setTimeout(() => {
      if (generation === loadGeneration) showPoster('3D loading timed out. Scene preview shown.');
    }, 45000);

    const path = mobile.matches ? '/models/studio-mobile.glb' : '/models/studio-desktop.glb';
    const asset = await new Promise<Asset>((resolve, reject) => {
      instance.assets.loadFromUrl(path, 'container', (error, result) => {
        if (error || !result) reject(new Error(String(error || 'Studio model missing')));
        else resolve(result);
      });
    });
    if (destroyed || generation !== loadGeneration) {
      asset.unload();
      return;
    }
    const model = (asset.resource as import('playcanvas').ContainerResource)
      .instantiateRenderEntity({castShadows: false, receiveShadows: false});
    instance.root.addChild(model);

    resizeObserver = new ResizeObserver(resizeCanvas);
    resizeObserver.observe(canvas.parentElement!);
    instance.start();
    canvas.hidden = false;
    poster.hidden = true;
    canvas.dataset.ready = 'true';
    canvas.dataset.asset = path;
    status.textContent = '3D scene ready. Drag to explore.';
    resizeCanvas();

    // This is the preserved blue-hour environment from the existing delivery,
    // not a replacement shader, procedural ripple, or newly invented scene.
    instance.assets.loadFromUrl('/models/blue-hour.jpg', 'texture', (error, sky) => {
      if (error || !sky || generation !== loadGeneration || destroyed || app !== instance) return;
      const dome = new pc.Entity('Blue-hour sky');
      dome.addComponent('render', {type: 'sphere', castShadows: false, receiveShadows: false});
      const material = new pc.StandardMaterial();
      material.useLighting = false;
      material.diffuse = new pc.Color(0, 0, 0);
      material.emissive = new pc.Color(1, 1, 1);
      material.emissiveMap = sky.resource as import('playcanvas').Texture;
      material.cull = pc.CULLFACE_FRONT;
      material.update();
      dome.render!.meshInstances.forEach(mesh => { mesh.material = material; });
      dome.setLocalScale(280, 280, 280);
      dome.setLocalEulerAngles(0, 92, 0);
      instance.root.addChild(dome);
      requestRender();
    });
  } catch (error) {
    if (generation !== loadGeneration || destroyed) return;
    console.warn('Scene unavailable:', error);
    showPoster('3D is unavailable. Scene preview shown.');
  } finally {
    if (watchdog) clearTimeout(watchdog);
  }
}

canvas.addEventListener('webglcontextlost', event => {
  event.preventDefault();
  if (app) showPoster('Graphics context lost. Scene preview shown.');
});

canvas.addEventListener('pointerdown', event => {
  if (!app || transition) return;
  pointer = {x: event.clientX, y: event.clientY, yaw: orbit.yaw, pitch: orbit.pitch};
  canvas.setPointerCapture(event.pointerId);
});
canvas.addEventListener('pointermove', event => {
  if (!pointer || !app) return;
  orbit.yaw = Math.max(-.15, Math.min(.15, pointer.yaw + (event.clientX - pointer.x) * .001));
  orbit.pitch = Math.max(-.35, Math.min(.35, pointer.pitch + (event.clientY - pointer.y) * .002));
  requestRender();
});
for (const type of ['pointerup', 'pointercancel', 'lostpointercapture']) {
  canvas.addEventListener(type, () => { pointer = undefined; });
}
canvas.addEventListener('wheel', event => {
  if (!app || transition) return;
  event.preventDefault();
  orbit.distance = Math.max(.9, Math.min(1.12, orbit.distance + event.deltaY * .0003));
  requestRender();
}, {passive: false});

document.addEventListener('keydown', event => {
  if (event.altKey || event.ctrlKey || event.metaKey) return;
  const index = event.key === 'Home' ? 0 : Number(event.key);
  if (event.key === 'Home' || /^[0-4]$/.test(event.key)) {
    event.preventDefault();
    setZone(zones[index]);
  }
});
document.addEventListener('visibilitychange', () => {
  if (!document.hidden) requestRender();
});
reduced.addEventListener('change', requestRender);
window.addEventListener('pagehide', () => {
  destroyed = true;
  ++loadGeneration;
  cancelAnimationFrame(frameRequest);
  resizeObserver?.disconnect();
  app?.destroy();
});
poster.addEventListener('click', () => {
  if (!app && !destroyed) void startScene();
});

// The current scene starts automatically: there is no mode button or website UI.
void startScene();
