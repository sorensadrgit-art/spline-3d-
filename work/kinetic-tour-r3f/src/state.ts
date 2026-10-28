import { blend, zones, type Zone, type Point } from "./tour.ts";
export const route = (hash: string) =>
  zones.find((z) => "#" + z.id === hash) ?? zones[0];
export const boundedOrbit = (yaw: number, pitch: number, distance: number) => ({
  yaw: Math.max(-0.15, Math.min(0.15, yaw)),
  pitch: Math.max(-0.35, Math.min(0.35, pitch)),
  distance: Math.max(0.9, Math.min(1.12, distance)),
});
type Pose = { position: Point; target: Point };
export class CameraMotion {
  from: Pose;
  destination: Zone;
  start = 0;
  current: Pose;
  constructor(zone: Zone) {
    this.destination = zone;
    this.from = { position: [...zone.position], target: [...zone.target] };
    this.current = this.from;
  }
  select(zone: Zone, now: number, reduced = false, displayed?: Pose) {
    // Inspection offsets live in CameraDirector; preserve the last painted pose
    // when that owner starts a trip or resets the view.
    const from = displayed ?? this.sample(now, reduced);
    this.from = { position: [...from.position], target: [...from.target] };
    this.destination = zone;
    this.start = now;
  }
  sample(now: number, reduced: boolean): Pose {
    const t = reduced ? 1 : (now - this.start) / 1350;
    if (t >= 1) {
      this.current = {
        position: [...this.destination.position],
        target: [...this.destination.target],
      };
      return this.current;
    }
    this.current = {
      position: blend(this.from.position, this.destination.position, t),
      target: blend(this.from.target, this.destination.target, t),
    };
    return this.current;
  }
}
export type LoadState = {
  generation: number;
  mode: "images" | "loading" | "three";
};
export function loadState(
  s: LoadState,
  event: "start" | "ready" | "failure" | "dismiss",
  generation = s.generation,
): LoadState {
  if (event === "start")
    return { generation: s.generation + 1, mode: "loading" };
  if (event === "dismiss" || event === "failure")
    return { generation: s.generation + 1, mode: "images" };
  return generation === s.generation && s.mode === "loading"
    ? { ...s, mode: "three" }
    : s;
}
