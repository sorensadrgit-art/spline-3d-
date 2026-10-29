import { Suspense, useEffect, useRef, useState } from "react";
import { Canvas, useFrame, useLoader, useThree } from "@react-three/fiber";
import {
  BackSide,
  NoToneMapping,
  RepeatWrapping,
  SRGBColorSpace,
  TextureLoader,
  Vector3,
} from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import type { Object3D } from "three";
import { visibleMarkers } from "./hotspots.ts";
import { disposeScene } from "./resources.ts";
import { anchors, type Zone } from "./tour.ts";
import { boundedOrbit, CameraMotion } from "./state.ts";

// Class names covered by interface chrome. Hoisted so the frame loop does not
// rebuild the selector string on every rendered frame.
const OVERLAYS =
  "#studio header, #studio .intro, #studio .details, #studio footer";

// Overlay geometry only changes on resize, zone change or a detail toggle, so
// it is re-measured at this interval instead of once per frame.
const OVERLAY_TTL_MS = 400;

type Props = {
  zone: Zone;
  reset: number;
  generation: number;
  onReady: (generation: number) => void;
  onFailure: (message: string) => void;
  onDetail: (i: number) => void;
};

// The delivered GLB is 12.0 MB desktop and 6.0 MB mobile. Dismissing the canvas
// aborts the request and disposes the parsed scene, which is correct for GPU
// memory but means a slow re-download on every image/3D toggle. Retain only the
// most recent model's bytes; the parsed scene is still disposed.
let cachedBytes: { url: string; bytes: ArrayBuffer } | undefined;

async function loadModelBytes(url: string, signal: AbortSignal) {
  if (cachedBytes?.url === url) return cachedBytes.bytes;
  const response = await fetch(url, { signal });
  if (!response.ok) throw new Error("Model HTTP " + response.status);
  const bytes = await response.arrayBuffer();
  if (!signal.aborted) cachedBytes = { url, bytes };
  return bytes;
}

// Release the retained bytes when the page is torn down.
if (typeof addEventListener === "function")
  addEventListener("pagehide", () => {
    cachedBytes = undefined;
  });

function Model({
  scene,
  onReady,
  generation,
}: {
  scene: Object3D;
  onReady: Props["onReady"];
  generation: number;
}) {
  useEffect(() => {
    onReady(generation);
  }, [scene, onReady, generation]);
  return <primitive object={scene} dispose={null} />;
}

function Sky() {
  const texture = useLoader(TextureLoader, "/models/blue-hour.jpg");
  texture.colorSpace = SRGBColorSpace;
  // Match the inward PlayCanvas sphere UV direction without editing the sky asset.
  texture.wrapS = RepeatWrapping;
  texture.repeat.x = -1;
  texture.offset.x = 1;
  return (
    <mesh scale={140} rotation={[0, (92 * Math.PI) / 180, 0]}>
      <sphereGeometry args={[1, 40, 24]} />
      <meshBasicMaterial map={texture} side={BackSide} toneMapped={false} />
    </mesh>
  );
}

function CameraDirector({
  zone,
  reset,
  markers,
}: {
  zone: Zone;
  reset: number;
  markers: React.RefObject<(HTMLButtonElement | null)[]>;
}) {
  const { camera, gl, invalidate, size } = useThree();
  const motion = useRef(new CameraMotion(zone));
  const reduced = useRef(
    matchMedia("(prefers-reduced-motion: reduce)").matches,
  );
  const orbit = useRef({ yaw: 0, pitch: 0, distance: 1 });
  const deadline = useRef(0);
  const interactionEpoch = useRef(0);
  const point = useRef(new Vector3());
  // Serialising the orbit every frame allocated a string per frame; the value
  // is only written when an interaction actually changed it.
  const orbitRevision = useRef(0);
  const writtenRevision = useRef(-1);
  const overlays = useRef<DOMRect[]>([]);
  const overlaysAt = useRef(0);
  // Demand rendering needs a frame after React receives the new viewport size.
  useEffect(() => invalidate(), [size.width, size.height, invalidate]);
  useEffect(() => {
    interactionEpoch.current++;
    motion.current.select(zone, performance.now(), reduced.current, {
      position: camera.position.toArray(),
      target: [...motion.current.current.target],
    });
    deadline.current = performance.now() + 1350;
    orbit.current = { yaw: 0, pitch: 0, distance: 1 };
    orbitRevision.current++;
    // A new zone renders a different detail panel, so cached rects expire.
    overlaysAt.current = 0;
    invalidate();
  }, [zone, reset, camera, invalidate]);
  useEffect(() => {
    const mq = matchMedia("(prefers-reduced-motion: reduce)");
    const change = () => {
      reduced.current = mq.matches;
      invalidate();
    };
    mq.addEventListener("change", change);
    return () => mq.removeEventListener("change", change);
  }, [invalidate]);
  useEffect(() => {
    const el = gl.domElement;
    // Vertical page scrolling must keep working over the canvas on small
    // screens; horizontal drags still rotate the view.
    el.style.touchAction = "pan-y";
    let drag:
      | { x: number; y: number; yaw: number; pitch: number; epoch: number }
      | undefined;
    const down = (e: PointerEvent) => {
      if (performance.now() < deadline.current && !reduced.current) return;
      drag = {
        x: e.clientX,
        y: e.clientY,
        ...orbit.current,
        epoch: interactionEpoch.current,
      };
      el.setPointerCapture(e.pointerId);
    };
    const move = (e: PointerEvent) => {
      if (!drag) return;
      if (drag.epoch !== interactionEpoch.current) {
        drag = undefined;
        return;
      }
      orbit.current = boundedOrbit(
        drag.yaw + (e.clientX - drag.x) * 0.001,
        drag.pitch + (e.clientY - drag.y) * 0.002,
        orbit.current.distance,
      );
      orbitRevision.current++;
      invalidate();
    };
    const end = () => {
      drag = undefined;
    };
    const wheel = (e: WheelEvent) => {
      if (performance.now() < deadline.current && !reduced.current) return;
      const next = boundedOrbit(
        orbit.current.yaw,
        orbit.current.pitch,
        orbit.current.distance + e.deltaY * 0.0003,
      );
      // Claim the gesture only when the zoom actually moves. At the clamp limit
      // the page must still be able to scroll past the canvas.
      if (next.distance === orbit.current.distance) return;
      e.preventDefault();
      orbit.current = next;
      orbitRevision.current++;
      invalidate();
    };
    el.addEventListener("pointerdown", down);
    el.addEventListener("pointermove", move);
    el.addEventListener("pointerup", end);
    el.addEventListener("pointercancel", end);
    el.addEventListener("lostpointercapture", end);
    el.addEventListener("wheel", wheel, { passive: false });
    return () => {
      el.removeEventListener("pointerdown", down);
      el.removeEventListener("pointermove", move);
      el.removeEventListener("pointerup", end);
      el.removeEventListener("pointercancel", end);
      el.removeEventListener("lostpointercapture", end);
      el.removeEventListener("wheel", wheel);
    };
  }, [gl, invalidate]);
  useFrame(() => {
    const now = performance.now();
    const pose = motion.current.sample(now, reduced.current);
    const o = orbit.current;
    const dx = pose.position[0] - pose.target[0],
      dz = pose.position[2] - pose.target[2];
    const radius = Math.hypot(dx, dz) * o.distance;
    const theta = Math.atan2(dx, dz) + o.yaw;
    camera.position.set(
      pose.target[0] + Math.sin(theta) * radius,
      pose.target[1] +
        (pose.position[1] - pose.target[1]) * o.distance +
        o.pitch,
      pose.target[2] + Math.cos(theta) * radius,
    );
    camera.lookAt(...pose.target);
    camera.updateMatrixWorld();

    // Measure before writing. Reading layout after the dataset writes below
    // forces a synchronous style recalculation inside every animated frame.
    const el = gl.domElement;
    const bounds = el.getBoundingClientRect();
    if (now - overlaysAt.current > OVERLAY_TTL_MS || !overlays.current.length) {
      overlays.current = Array.from(
        document.querySelectorAll(OVERLAYS),
        (node) => node.getBoundingClientRect(),
      );
      overlaysAt.current = now;
    }
    const covered = overlays.current;
    const projected = anchors[zone.id].map((anchor) => {
      const p = point.current.set(...anchor).project(camera);
      const x = ((p.x + 1) * size.width) / 2;
      const y = ((1 - p.y) * size.height) / 2;
      const hidden = covered.some((r) =>
        x + bounds.left + 22 > r.left &&
        x + bounds.left - 22 < r.right &&
        y + bounds.top + 22 > r.top &&
        y + bounds.top - 22 < r.bottom,
      );
      return {
        x,
        y,
        eligible:
          !hidden &&
          p.z >= -1 &&
          p.z <= 1 &&
          Math.abs(p.x) <= 0.92 &&
          Math.abs(p.y) <= 0.82,
      };
    });
    const visible = visibleMarkers(projected);
    projected.forEach(({ x, y }, i) => {
      const marker = markers.current[i];
      if (!marker) return;
      // Move keyboard focus before hiding a target during orbit, resize or motion.
      if (!visible[i] && document.activeElement === marker) {
        const fallback = document.querySelector<HTMLButtonElement>(
          '.details button[aria-controls="detail-' + i + '"]',
        ) ?? document.getElementById("mode");
        fallback?.focus({ preventScroll: true });
      }
      marker.hidden = !visible[i];
      marker.style.left = x + "px";
      marker.style.top = y + "px";
    });

    el.dataset.position = pose.position.join(",");
    el.dataset.target = pose.target.join(",");
    el.dataset.transition = String(!reduced.current && now < deadline.current);
    if (writtenRevision.current !== orbitRevision.current) {
      el.dataset.orbit = JSON.stringify(o);
      writtenRevision.current = orbitRevision.current;
    }
    if (now < deadline.current && !reduced.current) invalidate();
  });
  return null;
}

function ContextGuard({ onFailure }: { onFailure: Props["onFailure"] }) {
  const gl = useThree((s) => s.gl);
  useEffect(() => {
    const lost = (e: Event) => {
      e.preventDefault();
      onFailure("Graphics context lost. Image navigation remains ready.");
    };
    gl.domElement.addEventListener("webglcontextlost", lost);
    return () => gl.domElement.removeEventListener("webglcontextlost", lost);
  }, [gl, onFailure]);
  return null;
}

function Unavailable({ onFailure }: { onFailure: Props["onFailure"] }) {
  useEffect(
    () => onFailure("WebGL unavailable. Image navigation remains ready."),
    [onFailure],
  );
  return null;
}

export default function StudioCanvas(props: Props) {
  const mobile = useRef(matchMedia("(max-width: 700px)").matches).current;
  const markers = useRef<(HTMLButtonElement | null)[]>([]);
  const model = mobile
    ? "/models/studio-mobile.glb"
    : "/models/studio-desktop.glb";
  const [supported] = useState(() => {
    try {
      const probe = document.createElement("canvas");
      const context = probe.getContext("webgl2");
      context?.getExtension("WEBGL_lose_context")?.loseContext();
      return Boolean(context);
    } catch {
      return false;
    }
  });
  const [scene, setScene] = useState<Object3D | null>(null);
  useEffect(() => {
    if (!supported) return;
    const abort = new AbortController();
    let owned: Object3D | undefined;
    void (async () => {
      try {
        const bytes = await loadModelBytes(model, abort.signal);
        if (abort.signal.aborted) return;
        const gltf = await new GLTFLoader().parseAsync(bytes, "/models/");
        if (abort.signal.aborted) {
          disposeScene(gltf.scene);
          return;
        }
        owned = gltf.scene;
        setScene(owned);
      } catch {
        if (!abort.signal.aborted)
          props.onFailure("3D is unavailable. Image navigation remains ready.");
      }
    })();
    return () => {
      abort.abort();
      if (owned) disposeScene(owned);
    };
  }, [model, supported, props.onFailure]);
  if (!supported) return <Unavailable onFailure={props.onFailure} />;
  return (
    <div className="canvas-layer">
      <Canvas
        frameloop="demand"
        flat
        dpr={mobile ? 1 : [1, 1.5]}
        camera={{
          position: props.zone.position,
          fov: mobile ? 65 : 46,
          near: 0.05,
          far: 350,
        }}
        gl={{
          antialias: !mobile,
          powerPreference: "high-performance",
          preserveDrawingBuffer: true,
          toneMapping: NoToneMapping,
        }}
        fallback={<p>Graphics unavailable. Use images to continue.</p>}
      >
        <color attach="background" args={["#111923"]} />
        <ContextGuard onFailure={props.onFailure} />
        <CameraDirector
          zone={props.zone}
          reset={props.reset}
          markers={markers}
        />
        <Suspense fallback={null}>
          <>
            {scene && (
              <Model
                scene={scene}
                onReady={props.onReady}
                generation={props.generation}
              />
            )}
          </>
        </Suspense>
        <Suspense fallback={null}>
          <Sky />
        </Suspense>
      </Canvas>
      <div id="hotspots" role="group" aria-label="Points in this space">
        {props.zone.details.map(([title], i) => (
          <button
            hidden
            ref={(el) => {
              markers.current[i] = el;
            }}
            key={props.zone.id + i}
            aria-label={"Inspect " + title}
            onClick={() => props.onDetail(i)}
          >
            {i + 1}
          </button>
        ))}
      </div>
    </div>
  );
}

// Clear only the failed sky entry on graphics-boundary failure; keep successful reuse.
export function clearFailedSkyCache() {
  useLoader.clear(TextureLoader, "/models/blue-hour.jpg");
}
