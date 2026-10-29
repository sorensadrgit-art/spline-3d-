import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import ts from "typescript";
import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { CameraMotion, route } from "../src/state.ts";
import { zones, anchors } from "../src/tour.ts";

// The app entry is not written to be imported by a test: it mounts itself and
// imports CSS. Earlier this harness rewrote that source text with regular
// expressions that encoded the file's exact formatting, so a single reformat
// silently turned the import into a crash. The replacements below act on module
// specifiers instead of on formatting, which lets the file be reformatted freely.

const entry = new URL("../src/main.tsx", import.meta.url);
const entrySource = readFileSync(entry, "utf8");

const domClientShim =
  "data:text/javascript,export const createRoot=()=>({render(){}});export const hydrateRoot=createRoot;";
const canvasStub =
  "Promise.resolve({ default: () => null, clearFailedSkyCache: () => {} })";

const resolveTo = (id: string) => JSON.stringify(import.meta.resolve(id));

const transpiled = ts.transpileModule(
  'import React from "react";\n' + entrySource,
  {
    compilerOptions: {
      jsx: ts.JsxEmit.React,
      module: ts.ModuleKind.ESNext,
      target: ts.ScriptTarget.ES2022,
    },
  },
).outputText;

const moduleSource =
  transpiled
    // CSS is a side effect with no meaning in Node.
    .replace(/import\s*"\.\/style\.css";?/g, "")
    // Mounting is replaced by a no-op root, so importing the entry is inert.
    .replace(/from\s*"react-dom\/client"/g, `from ${JSON.stringify(domClientShim)}`)
    .replace(/from\s*"react"/g, `from ${resolveTo("react")}`)
    .replace(
      /from\s*"\.\/(tour|state)\.ts"/g,
      (_match, name: string) =>
        `from ${JSON.stringify(new URL(`../src/${name}.ts`, import.meta.url).href)}`,
    )
    // Data URLs cannot resolve bare or relative specifiers, so the lazily
    // imported canvas is replaced by an inert module.
    .replace(/import\("\.\/StudioCanvas\.tsx"\)/g, canvasStub) +
  // AppShell is a plain function declaration; exporting it after transpile
  // avoids editing the source to make it importable.
  "\nexport { AppShell };\n";

const { AppShell, GraphicsBoundary } = await import(
  "data:text/javascript;base64," + Buffer.from(moduleSource).toString("base64")
);

test("harness loads the real entry without mounting it", () => {
  assert.equal(typeof AppShell, "function");
  assert.equal(typeof GraphicsBoundary, "function");
  // Documented coupling: the harness relies on exactly one manual mount call.
  assert.equal((entrySource.match(/createRoot\(/g) ?? []).length, 1);
});

test("GraphicsBoundary error handling lifecycle and fallback UI rendering", () => {
  assert.deepEqual(GraphicsBoundary.getDerivedStateFromError(), { failed: true });

  let failureMessage = "";
  const boundary = new GraphicsBoundary({
    onFailure: (message: string) => {
      failureMessage = message;
    },
    children: React.createElement("div", null, "Canvas Child"),
  });

  assert.deepEqual(boundary.state, { failed: false });
  assert.equal(renderToStaticMarkup(boundary.render()), " Canvas Child ");

  boundary.componentDidCatch();
  assert.equal(
    failureMessage,
    "3D is unavailable. Image navigation remains ready.",
  );

  boundary.state = GraphicsBoundary.getDerivedStateFromError();
  assert.equal(boundary.render(), null);
});

for (const zone of zones) {
  test(`${zone.id}: UI enables 3D, selects its image and details, has no pending label`, () => {
    const original = Object.getOwnPropertyDescriptor(globalThis, "location");
    Object.defineProperty(globalThis, "location", {
      configurable: true,
      value: { hash: "#" + zone.id },
    });
    try {
      const html = renderToStaticMarkup(React.createElement(AppShell));
      const button = html.match(/<button[^>]*id="mode"[^>]*>/)?.[0];
      assert.ok(button, zone.id + " must render the 3D mode control");
      assert.ok(
        !button.includes("disabled"),
        zone.id + " must be eligible for actual GLB navigation",
      );
      assert.ok(html.includes('data-zone="' + zone.id + '"'));
      assert.ok(html.includes("/media/" + zone.image + ".webp"));
      assert.ok(!html.includes("pending"));
      for (const [title] of zone.details) assert.ok(html.includes(title));
      assert.equal(route("#" + zone.id), zone);
      assert.equal(anchors[zone.id].length, zone.details.length);
      assert.equal(new Set(anchors[zone.id].map((p) => p.join(","))).size, 3);
    } finally {
      if (original) Object.defineProperty(globalThis, "location", original);
      else delete globalThis.location;
    }
  });
}

test("every ordered zone pair retargets continuously and reaches the exact pose", () => {
  for (const from of zones)
    for (const to of zones) {
      const motion = new CameraMotion(from);
      motion.select(to, 100);
      const middle = motion.sample(550, false);
      motion.select(from, 550);
      assert.deepEqual(motion.sample(550, false), middle);
      assert.deepEqual(motion.sample(1900, false), {
        position: from.position,
        target: from.target,
      });
      motion.select(to, 2000, true);
      assert.deepEqual(motion.sample(2000, true), {
        position: to.position,
        target: to.target,
      });
    }
});
