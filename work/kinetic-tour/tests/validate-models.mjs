import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import validator from 'gltf-validator';

const results={};
for(const profile of ['desktop','mobile']){
  const path=new URL(`../public/models/studio-${profile}.glb`,import.meta.url);
  const bytes=await fs.readFile(path);
  assert.equal(bytes.toString('ascii',0,4),'glTF');
  assert.equal(bytes.readUInt32LE(4),2);assert.equal(bytes.readUInt32LE(8),bytes.length);
  const doc=JSON.parse(bytes.toString('utf8',20,20+bytes.readUInt32LE(12)).trim());
  assert.equal(doc.meshes.filter(m=>m.primitives.length).length>=9,true);
  assert.ok(doc.materials.some(m=>m.extensions?.KHR_materials_unlit));
  assert.ok(doc.images.length>=9);
  assert.ok(doc.meshes.every(m=>m.primitives.every(p=>p.attributes.POSITION!==undefined)));
  for(const mesh of doc.meshes)for(const primitive of mesh.primitives){
    if(doc.materials[primitive.material]?.pbrMetallicRoughness?.baseColorTexture)assert.notEqual(primitive.attributes.TEXCOORD_0,undefined);
  }
  const report=await validator.validateBytes(new Uint8Array(bytes),{uri:`studio-${profile}.glb`,maxIssues:100});
  assert.equal(report.issues.numErrors,0,JSON.stringify(report.issues));
  await fs.writeFile(new URL(`./validator-${profile}.json`,import.meta.url),JSON.stringify(report,null,2));
  results[profile]={bytes:bytes.length,sha256:crypto.createHash('sha256').update(bytes).digest('hex'),meshes:doc.meshes.length,materials:doc.materials.length,images:doc.images.length,errors:report.issues.numErrors,warnings:report.issues.numWarnings,extensions:doc.extensionsUsed};
}
await fs.writeFile(new URL('./model-checks.json',import.meta.url),JSON.stringify(results,null,2));
console.log('KINETIC_GLTF_VALIDATION_PASS',JSON.stringify(results));
