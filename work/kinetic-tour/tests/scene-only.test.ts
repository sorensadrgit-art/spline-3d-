import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {resolve} from 'node:path';
import test from 'node:test';

const root = fileURLToPath(new URL('../', import.meta.url));
const read = (name: string) => readFileSync(resolve(root, name), 'utf8');

test('root entry is just a fullscreen 3D scene, without visible website chrome', () => {
  const html = read('index.html');
  assert.match(html, /<canvas\s+id="scene"/);
  assert.match(html, /src="\/src\/scene-only\.ts"/);
  assert.doesNotMatch(html, /<(?:header|nav|footer|section|aside|button|h[1-6]|a)\b/i);
  assert.doesNotMatch(html, /id="(?:zone-content|zone-title|mode|reset|hotspots|details)"/);
});

test('the previous image-first guided tour is preserved at tour.html', () => {
  const html = read('tour.html');
  assert.match(html, /id="mode"/);
  assert.match(html, /id="zone-content"/);
  assert.match(html, /src="\/src\/main\.ts"/);
});

test('scene-only viewer automatically loads the existing 3D delivery assets', () => {
  const source = read('src/scene-only.ts');
  assert.match(source, /studio-desktop\.glb/);
  assert.match(source, /studio-mobile\.glb/);
  assert.match(source, /void startScene\(\)/);
  assert.doesNotMatch(source, /getElementById\(['"]mode['"]\)/);
});

test('scene-only CSS covers the viewport and hides page scrolling', () => {
  const css = read('src/scene-only.css');
  assert.match(css, /100dvh/);
  assert.match(css, /overflow:\s*hidden/);
  assert.match(css, /position:\s*absolute/);
});

test('Vite builds both the clean root and the preserved guided tour', () => {
  const config = read('vite.config.ts');
  assert.match(config, /studio:\s*'index\.html'/);
  assert.match(config, /tour:\s*'tour\.html'/);
});

test('legacy browser regression targets the preserved guided tour URL', () => {
  const qa = read('tests/browser_qa.py');
  assert.match(qa, /tour\.html#home/);
});
