import {
  lazy,
  Suspense,
  useCallback,
  useEffect,
  useRef,
  useState,
  Component,
  type ReactNode,
} from "react";
import { createRoot } from "react-dom/client";
import { zones, type Zone } from "./tour.ts";
import { route, loadState, type LoadState } from "./state.ts";
import "./style.css";
const StudioCanvas = lazy(() => import("./StudioCanvas.tsx"));
class GraphicsBoundary extends Component<
  { children: ReactNode; onFailure: (message: string) => void },
  { failed: boolean }
> {
  state = { failed: false };
  static getDerivedStateFromError() {
    return { failed: true };
  }
  componentDidCatch() {
    void import("./StudioCanvas.tsx").then(module => module.clearFailedSkyCache());
    this.props.onFailure("3D is unavailable. Image navigation remains ready.");
  }
  render() {
    return this.state.failed ? null : this.props.children;
  }
}
const names = [
  "Home",
  "Motion Systems",
  "Clinical Thinking",
  "Creative Engineering",
  "Projects",
];
function AppShell() {
  const [zone, setZone] = useState(() => route(location.hash));
  const [load, setLoad] = useState<LoadState>({
    generation: 0,
    mode: "images",
  });
  const [message, setMessage] = useState(
    "Image tour ready. Five connected studio spaces.",
  );
  const [detail, setDetail] = useState<number | null>(null);
  const [reset, setReset] = useState(0);
  const loadRef = useRef(load);
  loadRef.current = load;
  const select = useCallback((z: Zone, push = true) => {
    // A key/history change can remove the focused zone-specific control.
    if (document.activeElement?.closest(".details, #hotspots"))
      requestAnimationFrame(() =>
        document.querySelector<HTMLButtonElement>("nav [data-zone=" + z.id + "]")
          ?.focus({ preventScroll: true }),
      );
    setZone(z);
    setDetail(null);
    if (push && location.hash !== "#" + z.id)
      history.pushState(null, "", "#" + z.id);
    setMessage(names[zones.indexOf(z)] + " selected.");
  }, []);
  const images = useCallback((text = "Image tour ready.") => {
    if (document.activeElement?.closest("#hotspots, .canvas-layer, .controls button"))
      requestAnimationFrame(() =>
        document.getElementById("mode")?.focus({ preventScroll: true }),
      );
    setLoad((s) => loadState(s, "dismiss"));
    setMessage(text);
  }, []);
  useEffect(() => {
    const historyChanged = () => select(route(location.hash), false);
    const key = (e: KeyboardEvent) => {
      if (
        e.altKey ||
        e.ctrlKey ||
        e.metaKey ||
        (e.target instanceof HTMLElement &&
          (e.target.isContentEditable ||
            /INPUT|TEXTAREA|SELECT/.test(e.target.tagName)))
      )
        return;
      if (e.key === "Escape") {
        images();
        return;
      }
      if (e.key === "Home" || /^[0-4]$/.test(e.key)) {
        e.preventDefault();
        select(zones[e.key === "Home" ? 0 : Number(e.key)]);
      }
    };
    addEventListener("popstate", historyChanged);
    addEventListener("hashchange", historyChanged);
    addEventListener("keydown", key);
    return () => {
      removeEventListener("popstate", historyChanged);
      removeEventListener("hashchange", historyChanged);
      removeEventListener("keydown", key);
    };
  }, [select, images]);
  useEffect(() => {
    if (load.mode !== "loading") return;
    const token = load.generation;
    const timer = setTimeout(() => {
      if (
        loadRef.current.generation === token &&
        loadRef.current.mode === "loading"
      )
        images("3D loading timed out. Image navigation remains ready.");
    }, 45000);
    return () => clearTimeout(timer);
  }, [load, images]);
  const failed = useCallback((m: string) => images(m), [images]);
  const ready = useCallback((token: number) => {
    setLoad((s) => loadState(s, "ready", token));
    if (loadRef.current.generation === token)
      setMessage("3D ready. Drag to inspect; wheel adjusts distance.");
  }, []);
  return (
    <>
      <a
        className="skip"
        href="#content"
        onClick={(e) => {
          e.preventDefault();
          document.getElementById("content")?.focus();
        }}
      >
        Skip to studio details
      </a>
      <main id="studio" data-mode={load.mode} data-zone={zone.id}>
        <div className="scene" role="group" aria-label="Studio view">
          <img
            id="poster"
            src={"/media/" + zone.image + ".webp"}
            alt={
              zone.id === "home"
                ? "Warm walnut Kinetic Studio with four connected work zones and blue-hour mountain windows."
                : names[zones.indexOf(zone)] +
                  " in the warm Kinetic Studio, rendered from the editable Blender master."
            }
            hidden={load.mode === "three"}
          />
          {load.mode !== "images" && (
            <GraphicsBoundary key={load.generation} onFailure={failed}>
              <Suspense fallback={null}>
                <StudioCanvas
                  zone={zone}
                  reset={reset}
                  generation={load.generation}
                  onReady={ready}
                  onFailure={failed}
                  onDetail={(i) => {
                    setDetail(i);
                    requestAnimationFrame(() =>
                      document
                        .querySelector<HTMLButtonElement>(
                          "[aria-controls=detail-" + i + "]",
                        )
                        ?.focus({ preventScroll: true }),
                    );
                  }}
                />
              </Suspense>
            </GraphicsBoundary>
          )}
        </div>
        <header>
          <a
            className="wordmark"
            href="#home"
            onClick={(e) => {
              e.preventDefault();
              select(zones[0]);
            }}
          >
            KINETIC<span>STUDIO / R3F PROOF</span>
          </a>
          <p className="edition">MOVEMENT · INVESTIGATION · MAKING</p>
        </header>
        <section className="intro" id="content" tabIndex={-1}>
          <p className="eyebrow">{zone.number}</p>
          <h1 dangerouslySetInnerHTML={{ __html: zone.title }} />
          <p className="description">{zone.description}</p>
          <p className="proof-note">
            Five connected spaces / isolated R3F proof
          </p>
        </section>
        <aside className="details" aria-label="Studio details">
          <h2>Inside this space</h2>
          {zone.details.map(([title, body], i) => (
            <div key={zone.id + i}>
              <button
                aria-expanded={detail === i}
                aria-controls={"detail-" + i}
                onClick={() => setDetail(detail === i ? null : i)}
              >
                {String(i + 1).padStart(2, "0")} <span>{title}</span>
                <span aria-hidden="true">{detail === i ? "−" : "+"}</span>
              </button>
              <p id={"detail-" + i} hidden={detail !== i}>
                {body}
              </p>
            </div>
          ))}
        </aside>
        <footer>
          <div className="controls">
            <button
              id="mode"
              aria-pressed={load.mode === "three"}
              disabled={load.mode === "loading"}
              onClick={() =>
                load.mode === "three"
                  ? images()
                  : setLoad((s) => loadState(s, "start"))
              }
            >
              {load.mode === "loading"
                ? "Loading 3D…"
                : load.mode === "three"
                  ? "View cinematic images"
                  : "Explore in 3D"}
            </button>
            {load.mode === "loading" && (
              <button onClick={() => images()}>Use images</button>
            )}
            {load.mode === "three" && (
              <button id="reset" onClick={() => setReset((n) => n + 1)}>
                Reset view
              </button>
            )}
            <p id="status" role="status">
              {message}
            </p>
          </div>
          <nav aria-label="Studio spaces">
            {zones.map((z, i) => (
              <button
                key={z.id}
                data-zone={z.id}
                aria-current={z.id === zone.id ? "page" : undefined}
                onClick={() => select(z)}
              >
                <span className="nav-number">0{i}</span>
                {names[i]}
              </button>
            ))}
          </nav>
          <p className="keys">
            0–4 select a space · Home returns · Escape opens images
          </p>
        </footer>
      </main>
    </>
  );
}
createRoot(document.getElementById("root")!).render(<AppShell />);
