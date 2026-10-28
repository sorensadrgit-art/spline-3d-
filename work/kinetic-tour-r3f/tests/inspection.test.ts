import { test } from 'node:test';
import assert from 'node:assert/strict';
import { CameraMotion } from '../src/state.ts';
import { zones } from '../src/tour.ts';

test('navigation and reset start from the displayed inspected pose', () => {
  const displayed = { position: [2.9289873965, 3.514, 17.0799131275], target: [0, 2.1, -2.3] };
  const motion = new CameraMotion(zones[0]);
  motion.select(zones[2], 2000, false, displayed);
  assert.deepEqual(motion.sample(2000, false), displayed);
  assert.deepEqual(motion.sample(3350, false), { position: zones[2].position, target: zones[2].target });
  motion.select(zones[0], 4000, true, displayed);
  assert.deepEqual(motion.sample(4000, true), { position: zones[0].position, target: zones[0].target });
});
