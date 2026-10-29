import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

// src/tour.ts is protected by a byte-equality test in state.test.ts. The camera,
// orbit, breakpoint and timeout constants are NOT, because they live inside each
// app rather than in shared data. These tests read the authoritative PlayCanvas
// source as text and fail if the proof drifts from it, without editing the
// authoritative app.

const read = (relative: string) =>
  readFileSync(new URL(relative, import.meta.url), "utf8");

// Legacy writes `.9`; the proof writes `0.9`. Normalise the leading zero so a
// single literal comparison covers both spellings.
const normalise = (text: string) => text.replace(/(?<![\d.])\.(?=\d)/g, "0.");

const containsNumber = (text: string, literal: string) =>
  new RegExp(`(?<![\\d.])${literal.replace(/\./g, "\\.")}(?![\\d])`).test(text);

const invariants: Array<[string, string]> = [
  ["camera transition in milliseconds", "1350"],
  ["orbit yaw clamp in radians", "0.15"],
  ["orbit pitch clamp in radians", "0.35"],
  ["orbit minimum distance factor", "0.9"],
  ["orbit maximum distance factor", "1.12"],
  ["mobile breakpoint in pixels", "700"],
  ["3D load timeout in milliseconds", "45000"],
];

test("camera, orbit, breakpoint and timeout constants still match the authoritative tour", () => {
  const legacy = normalise(read("../../kinetic-tour/src/main.ts"));
  const proof = normalise(
    ["../src/state.ts", "../src/StudioCanvas.tsx", "../src/main.tsx"]
      .map(read)
      .join("\n"),
  );

  for (const [name, literal] of invariants) {
    assert.ok(
      containsNumber(legacy, literal),
      `the authoritative tour no longer contains ${name} (${literal}); rederive the proof before assuming parity`,
    );
    assert.ok(
      containsNumber(proof, literal),
      `the R3F proof drifted from ${name} (${literal}) in the authoritative tour`,
    );
  }
});

test("hotspot hit targets stay 44px in CSS with a 4px separation budget in logic", () => {
  const css = read("../src/style.css");
  const hotspots = read("../src/hotspots.ts");

  assert.match(
    css,
    /#hotspots button\s*\{[^}]*width:\s*44px/,
    "#hotspots button must keep its 44px hit target",
  );
  assert.match(
    css,
    /#hotspots button\s*\{[^}]*height:\s*44px/,
    "#hotspots button must keep its 44px hit target",
  );
  assert.match(
    hotspots,
    /44\s*\+\s*4/,
    "hotspots.ts must derive its centre separation from the 44px target plus 4px",
  );
});
