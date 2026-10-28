export type ProjectedMarker = { x: number; y: number; eligible: boolean };

// 44px targets plus a 4px gap, in CSS pixels.
const separation = 44 + 4;

// Stable semantic order wins collisions; never move a projected 3D anchor.
export function visibleMarkers(points: readonly ProjectedMarker[]): boolean[] {
  const accepted: ProjectedMarker[] = [];
  return points.map(point => {
    if (!point.eligible || !Number.isFinite(point.x) || !Number.isFinite(point.y)) return false;
    if (accepted.some(other => Math.abs(point.x - other.x) < separation && Math.abs(point.y - other.y) < separation)) return false;
    accepted.push(point);
    return true;
  });
}
