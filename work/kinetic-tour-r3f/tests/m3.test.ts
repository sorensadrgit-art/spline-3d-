import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import ts from 'typescript';
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { CameraMotion, route } from '../src/state.ts';
import { zones, anchors } from '../src/tour.ts';

// Exercise the real AppShell initial render without mounting a browser root.
// TypeScript is already a pinned build dependency; no test runtime is added.
const source = readFileSync(new URL('../src/main.tsx', import.meta.url), 'utf8')
  .replace(/import \{ createRoot \} from "react-dom\/client";/, '')
  .replace(/import "\.\/style.css";/, '')
  .replace(/createRoot\(document.getElementById\("root"\)!\)\.render\(<AppShell \/>\);/, '')
  .replace('function AppShell()', 'export function AppShell()');
let js = ts.transpileModule('import React from "react";' + source, { compilerOptions: { jsx: ts.JsxEmit.React, module: ts.ModuleKind.ESNext, target: ts.ScriptTarget.ES2022 } }).outputText;
js = js.replace(/from "react"/g, 'from ' + JSON.stringify(import.meta.resolve('react')))
  .replace(/from "\.\/(tour|state)\.ts"/g, (_, name) => 'from ' + JSON.stringify(new URL('../src/' + name + '.ts', import.meta.url).href));
const { AppShell } = await import('data:text/javascript;base64,' + Buffer.from(js).toString('base64'));

for (const z of zones) {
  test(z.id + ': actual UI enables 3D, selects its image/details and has no pending label', () => {
    const original = Object.getOwnPropertyDescriptor(globalThis, 'location');
    Object.defineProperty(globalThis, 'location', { configurable: true, value: { hash: '#' + z.id } });
    try {
      const html = renderToStaticMarkup(React.createElement(AppShell));
      const button = html.match(/<button[^>]*id="mode"[^>]*>/)?.[0];
      assert.ok(button);
      assert.ok(!button.includes('disabled'), z.id + ' must be eligible for actual GLB navigation');
      assert.ok(html.includes('data-zone="' + z.id + '"'));
      assert.ok(html.includes('/media/' + z.image + '.webp'));
      assert.ok(!html.includes('pending'));
      for (const [title] of z.details) assert.ok(html.includes(title));
      assert.equal(route('#' + z.id), z);
      assert.equal(anchors[z.id].length, z.details.length);
      assert.equal(new Set(anchors[z.id].map(p => p.join(','))).size, 3);
    } finally {
      if (original) Object.defineProperty(globalThis, 'location', original);
      else delete globalThis.location;
    }
  });
}

test('every ordered zone pair retargets continuously and reaches exact position and target', () => {
  for (const from of zones) for (const to of zones) {
    const c = new CameraMotion(from);
    c.select(to, 100);
    const mid = c.sample(550, false);
    c.select(from, 550);
    assert.deepEqual(c.sample(550, false), mid);
    assert.deepEqual(c.sample(1900, false), { position: from.position, target: from.target });
    c.select(to, 2000, true);
    assert.deepEqual(c.sample(2000, true), { position: to.position, target: to.target });
  }
});
