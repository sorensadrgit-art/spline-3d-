import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { CameraMotion, route, boundedOrbit, loadState } from "../src/state.ts";
import { zones } from "../src/tour.ts";
test("camera data has no drift from delivered tour", () =>
  assert.equal(
    readFileSync(new URL("../src/tour.ts", import.meta.url), "utf8"),
    readFileSync(
      new URL("../../kinetic-tour/src/tour.ts", import.meta.url),
      "utf8",
    ),
  ));
test("1350ms transition reaches target and clamps", () => {
  const c = new CameraMotion(zones[0]);
  c.select(zones[1], 100);
  assert.deepEqual(c.sample(100, false).position, zones[0].position);
  assert.notDeepEqual(c.sample(775, false).position, zones[1].position);
  assert.deepEqual(c.sample(1450, false).position, zones[1].position);
});
test("rapid retarget samples actual pose without jump", () => {
  const c = new CameraMotion(zones[0]);
  c.select(zones[1], 0);
  const p = c.sample(300, false);
  c.select(zones[0], 300);
  assert.deepEqual(c.sample(300, false), p);
  assert.deepEqual(c.sample(1650, false).position, zones[0].position);
});
test("reduced motion immediately cuts and reset restores destination", () => {
  const c = new CameraMotion(zones[0]);
  c.select(zones[1], 0);
  assert.deepEqual(c.sample(1, true).position, zones[1].position);
  c.select(zones[0], 2);
  assert.deepEqual(c.sample(2, true).position, zones[0].position);
});
test("unknown route returns Home and five destinations remain discoverable", () => {
  assert.equal(route("#missing").id, "home");
  for (const z of zones) assert.equal(route("#" + z.id).id, z.id);
});
test("orbit clamps drag and wheel to original safe bounds", () =>
  assert.deepEqual(boundedOrbit(9, -9, 30), {
    yaw: 0.15,
    pitch: -0.35,
    distance: 1.12,
  }));
test("late load cannot reopen a failed or dismissed generation", () => {
  const a = loadState({ generation: 1, mode: "loading" }, "failure", 1);
  assert.equal(a.mode, "images");
  assert.equal(loadState(a, "ready", 1).mode, "images");
  assert.equal(
    loadState({ generation: 2, mode: "loading" }, "ready", 1).mode,
    "loading",
  );
  assert.equal(
    loadState({ generation: 2, mode: "loading" }, "ready", 2).mode,
    "three",
  );
});
