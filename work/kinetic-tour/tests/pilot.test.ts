import {test} from 'node:test';
import assert from 'node:assert/strict';
import * as pc from 'playcanvas';

function setupMockCreateDevice() {
  pc.Application.prototype.createDevice = function(canvas: any) {
    const device = new pc.EventHandler() as any;
    device.canvas = canvas;
    device.maxPixelRatio = 1;
    device.clientRect = { width: 800, height: 600 };
    device.gpuProfiler = new pc.EventHandler();
    device._shaderStats = {};
    device._vram = { tex: 0, vb: 0, ib: 0, ub: 0, sb: 0 };
    device.destroy = () => {};
    device.resizeCanvas = () => {};
    device.init = () => {};
    device.attributes = { alpha: false };
    device.scope = { resolve: () => ({ set: () => {}, setValue: () => {} }) };
    device.createTextureImpl = () => ({ destroy: () => {}, loseContext: () => {}, propertyChanged: () => {} });
    device.createRenderTargetImpl = () => ({ destroy: () => {}, loseContext: () => {}, initialized: true });
    device.createVertexBufferImpl = () => ({ destroy: () => {}, loseContext: () => {} });
    device.createIndexBufferImpl = () => ({ destroy: () => {}, loseContext: () => {} });
    device.createShaderImpl = () => ({ destroy: () => {}, loseContext: () => {} });
    device.onTextureDestroyed = () => {};
    device.onShaderDestroyed = () => {};
    device.targets = new Set();
    device.buffers = new Set();
    device.textures = new Set();
    device.shaders = new Set();
    device.on = () => {};
    device.off = () => {};
    device.fire = () => {};
    this.graphicsDevice = device;
    return device;
  };
}

class MockElement {
  listeners: Record<string, Array<(e?: any) => void>> = {};
  style: Record<string, string> = {};
  parentElement: { clientWidth: number } = { clientWidth: 800 };
  hidden = false;
  disabled = false;
  textContent = '';
  clientWidth = 800;
  clientHeight = 600;
  capturedPointerId?: number;

  addEventListener(event: string, listener: (e?: any) => void) {
    if (!this.listeners[event]) this.listeners[event] = [];
    this.listeners[event].push(listener);
  }
  dispatch(event: string, data: Record<string, any> = {}) {
    const list = this.listeners[event] || [];
    for (const fn of list) fn({ ...data, clientX: data.clientX || 0, clientY: data.clientY || 0 });
  }
  setPointerCapture(id: number) { this.capturedPointerId = id; }
}

function createDOMMock(search = '') {
  const mockButton = new MockElement();
  const mockCanvas = new MockElement();
  const mockStatus = new MockElement();
  const windowListeners: Record<string, Array<() => void>> = {};

  let resizeCallback: () => void = () => {};

  (globalThis as any).document = {
    querySelector: (sel: string) => {
      if (sel === '#load') return mockButton;
      if (sel === '#pilot') return mockCanvas;
      if (sel === '#status') return mockStatus;
      return null;
    },
    addEventListener: () => {},
    removeEventListener: () => {},
    body: {}
  };
  (globalThis as any).location = { search };
  (globalThis as any).innerHeight = 1000;
  (globalThis as any).window = {
    addEventListener(event: string, listener: () => void) {
      if (!windowListeners[event]) windowListeners[event] = [];
      windowListeners[event].push(listener);
    },
    dispatch(event: string) {
      for (const fn of windowListeners[event] || []) fn();
    }
  };
  (globalThis as any).ResizeObserver = class {
    constructor(cb: () => void) { resizeCallback = cb; }
    observe() {}
  };

  return {
    mockButton,
    mockCanvas,
    mockStatus,
    triggerResize: () => resizeCallback(),
    triggerWindow: (event: string) => (globalThis as any).window.dispatch(event)
  };
}

test('load button initializes PlayCanvas and loads default PLY Gaussian asset', async () => {
  const dom = createDOMMock('');
  setupMockCreateDevice();

  let loadedUrl = '';
  let loadedType = '';
  let loadCallback: any;

  pc.AssetRegistry.prototype.loadFromUrl = function(url: string, type: string, cb: any) {
    loadedUrl = url;
    loadedType = type;
    loadCallback = cb;
  };

  let appStarted = false;
  const origStart = pc.Application.prototype.start;
  pc.Application.prototype.start = function() {
    appStarted = true;
  };

  await import(`../src/pilot.ts?case=ply_${Date.now()}`);

  dom.mockButton.dispatch('click');

  assert.equal(dom.mockButton.disabled, true);
  assert.equal(dom.mockCanvas.hidden, false);
  assert.equal(dom.mockStatus.textContent, 'Loading the experimental Gaussian scene…');
  assert.equal(loadedUrl, '/models/engineering-pilot.ply');
  assert.equal(loadedType, 'gsplat');

  // Simulate successful asset load
  const mockAsset = new pc.Asset('engineering-pilot', 'gsplat');
  loadCallback(null, mockAsset);

  assert.equal(appStarted, true);
  assert.equal(dom.mockStatus.textContent, 'Experimental Gaussian scene loaded. Drag to inspect.');

  pc.Application.prototype.start = origStart;
});

test('loads compressed SOG asset when sog search parameter is set', async () => {
  const dom = createDOMMock('?sog');
  setupMockCreateDevice();

  let loadedUrl = '';
  let loadCallback: any;

  pc.AssetRegistry.prototype.loadFromUrl = function(url: string, _type: string, cb: any) {
    loadedUrl = url;
    loadCallback = cb;
  };

  await import(`../src/pilot.ts?case=sog_${Date.now()}`);

  dom.mockButton.dispatch('click');

  assert.equal(loadedUrl, '/models/engineering-pilot.sog');

  const mockAsset = new pc.Asset('engineering-pilot', 'gsplat');
  loadCallback(null, mockAsset);

  assert.equal(dom.mockStatus.textContent, 'Experimental compressed SOG scene loaded. Drag to inspect.');
});

test('handles asset loading error gracefully', async () => {
  const dom = createDOMMock('');
  setupMockCreateDevice();

  let loadCallback: any;
  pc.AssetRegistry.prototype.loadFromUrl = function(_url: string, _type: string, cb: any) {
    loadCallback = cb;
  };

  await import(`../src/pilot.ts?case=err_${Date.now()}`);

  dom.mockButton.dispatch('click');

  // Simulate load error
  loadCallback(new Error('Network error'), null);

  assert.equal(dom.mockStatus.textContent, 'The Gaussian viewer could not load. The comparison remains available.');
  assert.equal(dom.mockCanvas.hidden, true);
  assert.equal(dom.mockButton.disabled, false);
});

test('handles graphics device initialization failure via fallback', async () => {
  const dom = createDOMMock('');

  // Force Application creation failure
  pc.Application.prototype.createDevice = function() {
    throw new Error('WebGL not supported');
  };

  const warnings: any[] = [];
  const origWarn = console.warn;
  console.warn = (...args: any[]) => warnings.push(args);

  await import(`../src/pilot.ts?case=webgl_fail_${Date.now()}`);

  dom.mockButton.dispatch('click');

  assert.equal(dom.mockStatus.textContent, 'Graphics support is unavailable. The comparison remains available.');
  assert.equal(dom.mockCanvas.hidden, true);
  assert.equal(dom.mockButton.disabled, false);
  assert.equal(warnings.length, 1);

  console.warn = origWarn;
});

test('supports pointer dragging, camera pose updates, resize observer, and pagehide cleanup', async () => {
  const dom = createDOMMock('');
  setupMockCreateDevice();

  let loadCallback: any;
  pc.AssetRegistry.prototype.loadFromUrl = function(_url: string, _type: string, cb: any) {
    loadCallback = cb;
  };

  let resizedArgs: [number, number] | undefined;
  const origResizeCanvas = pc.Application.prototype.resizeCanvas;
  pc.Application.prototype.resizeCanvas = function(w: number, h: number) {
    resizedArgs = [w, h];
  };

  let appDestroyed = false;
  const origDestroy = pc.Application.prototype.destroy;
  pc.Application.prototype.destroy = function() {
    appDestroyed = true;
  };

  await import(`../src/pilot.ts?case=interactive_${Date.now()}`);

  dom.mockButton.dispatch('click');
  loadCallback(null, new pc.Asset('engineering-pilot', 'gsplat'));

  // Pointer interaction testing
  dom.mockCanvas.dispatch('pointerdown', { pointerId: 42, clientX: 100, clientY: 100 });
  assert.equal(dom.mockCanvas.capturedPointerId, 42);

  // Small drag
  dom.mockCanvas.dispatch('pointermove', { clientX: 150, clientY: 120 });
  // Large drag beyond limits (yaw clamped to [-0.3, 0.3], pitch clamped to [-0.3, 0.3])
  dom.mockCanvas.dispatch('pointermove', { clientX: 1000, clientY: -1000 });

  dom.mockCanvas.dispatch('pointerup');

  // Pointer move after pointerup should be ignored (drag is undefined)
  dom.mockCanvas.dispatch('pointermove', { clientX: 50, clientY: 50 });

  // Test pointercancel
  dom.mockCanvas.dispatch('pointerdown', { pointerId: 43, clientX: 100, clientY: 100 });
  dom.mockCanvas.dispatch('pointercancel');

  // ResizeObserver trigger
  dom.triggerResize();
  assert.deepEqual(resizedArgs, [800, 650]); // clientWidth 800, innerHeight 1000 * 0.65 = 650

  // Window pagehide cleanup
  dom.triggerWindow('pagehide');
  assert.equal(appDestroyed, true);

  pc.Application.prototype.resizeCanvas = origResizeCanvas;
  pc.Application.prototype.destroy = origDestroy;
});
