import { zoneFromHash } from '../src/tour.ts';

const testHashes = [
  '#home',
  '#motion',
  '#clinical',
  '#engineering',
  '#projects',
  '#unknown_zone',
  'projects',
  ''
];

const ITERATIONS = 5_000_000;

console.log(`Running zoneFromHash benchmark (${ITERATIONS.toLocaleString()} iterations)...`);

const start = performance.now();
for (let i = 0; i < ITERATIONS; i++) {
  const hash = testHashes[i % testHashes.length];
  zoneFromHash(hash);
}
const end = performance.now();

const totalTimeMs = end - start;
const opsPerSec = (ITERATIONS / totalTimeMs) * 1000;

console.log(`Total time: ${totalTimeMs.toFixed(2)} ms`);
console.log(`Operations/sec: ${opsPerSec.toLocaleString(undefined, { maximumFractionDigits: 0 })} ops/s`);
