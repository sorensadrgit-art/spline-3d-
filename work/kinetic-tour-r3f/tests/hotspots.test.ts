import { test } from "node:test";
import assert from "node:assert/strict";
import { visibleMarkers } from "../src/hotspots.ts";

// Removing inter-marker rejection must fail this recorded mobile geometry case.
test("keeps first grounded target and rejects both colliding mobile Home targets", () => {
  const points = [{ x:195, y:219.359375, eligible:true }, { x:179.125, y:261.875, eligible:true }, { x:195, y:193.8125, eligible:true }];
  const before = structuredClone(points);
  assert.deepEqual(visibleMarkers(points), [true, false, false]);
  assert.deepEqual(points, before);
});
test("keeps separated desktop targets and accepts exactly four pixels of space", () => {
  assert.deepEqual(visibleMarkers([{x:100,y:100,eligible:true},{x:148,y:100,eligible:true},{x:100,y:148,eligible:true}]), [true,true,true]);
  assert.deepEqual(visibleMarkers([{x:100,y:100,eligible:true},{x:147.99,y:147.99,eligible:true}]), [true,false]);
});
test("ineligible or invalid targets cannot suppress later valid anchors", () => {
  assert.deepEqual(visibleMarkers([{x:100,y:100,eligible:false},{x:100,y:100,eligible:true},{x:NaN,y:100,eligible:true},{x:148,y:100,eligible:true}]), [false,true,false,true]);
});
