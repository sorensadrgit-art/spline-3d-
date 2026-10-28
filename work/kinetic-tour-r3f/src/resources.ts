import type { Object3D, Mesh, Material, Texture, BufferGeometry } from "three";
/** Dispose shared GLB resources once; caller retains ownership of the scene. */
export function disposeScene(scene: Object3D) {
  const geometries = new Set<BufferGeometry>(),
    materials = new Set<Material>(),
    textures = new Set<Texture>();
  scene.traverse((object) => {
    const mesh = object as Mesh;
    if (mesh.geometry) geometries.add(mesh.geometry);
    const list = Array.isArray(mesh.material) ? mesh.material : [mesh.material];
    for (const material of list) {
      if (!material) continue;
      materials.add(material);
      for (const value of Object.values(material))
        if (value?.isTexture) textures.add(value);
    }
  });
  const images = new Set<unknown>();
  for (const texture of textures) {
    const image = texture.source?.data;
    if (image && !images.has(image)) {
      images.add(image);
      if (typeof image.close === "function") image.close();
    }
    texture.dispose();
  }
  for (const material of materials) material.dispose();
  for (const geometry of geometries) geometry.dispose();
}
