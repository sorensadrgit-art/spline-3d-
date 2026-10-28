import {test} from 'node:test';
import assert from 'node:assert/strict';
import {zones,zoneFromHash,blend} from '../src/tour.ts';
test('all five destinations have distinct poses and three factual details',()=>{
  assert.equal(new Set(zones.map(z=>z.id)).size,5);
  for(const zone of zones){assert.equal(zone.details.length,3);assert.ok(zone.position.every(Number.isFinite));assert.notDeepEqual(zone.position,zone.target);}
});
test('unknown hashes return Home and browser history hashes map deterministically',()=>{
  assert.equal(zoneFromHash('#missing').id,'home');
  for(const zone of zones)assert.equal(zoneFromHash('#'+zone.id),zone);
});
test('camera interpolation clamps and can retarget from its actual intermediate pose',()=>{
  assert.deepEqual(blend([0,0,0],[10,4,2],-2),[0,0,0]);
  assert.deepEqual(blend([0,0,0],[10,4,2],4),[10,4,2]);
  const middle=blend([0,0,0],[10,4,2],.5);
  assert.deepEqual(middle,[5,2,1]);assert.deepEqual(blend(middle,[-2,1,3],0),middle);
});
