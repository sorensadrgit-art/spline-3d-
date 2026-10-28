import { test } from "node:test";
import assert from "node:assert/strict";
import { BoxGeometry, MeshBasicMaterial, Texture, Mesh, Group } from "three";
import { disposeScene } from "../src/resources.ts";
test("shared model resources dispose once, including bitmap source", () => {
  const group = new Group();
  const geometry = new BoxGeometry();
  let closes = 0;
  const texture = new Texture({
    close() {
      closes++;
    },
  } as any);
  const material = new MeshBasicMaterial({ map: texture });
  let g = 0,
    m = 0,
    t = 0;
  geometry.addEventListener("dispose", () => g++);
  material.addEventListener("dispose", () => m++);
  texture.addEventListener("dispose", () => t++);
  group.add(new Mesh(geometry, material), new Mesh(geometry, material));
  disposeScene(group);
  assert.deepEqual({ g, m, t, closes }, { g: 1, m: 1, t: 1, closes: 1 });
});
