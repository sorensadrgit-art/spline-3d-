# Kinetic Studio — first Blender proof

Publication note: this checkout contains the current v006 packed master. Earlier binary checkpoints and raw downloaded assets remain in the original local archive. Historical scripts and acceptance checks below can require those omitted inputs; see the root README before rebuilding them.

## Latest delivery: v006 cinematic master

`kinetic-studio-proof-v006.blend` is the current editable master. `kinetic-studio-proof-v006.png` is its 3840 × 1080, 128-sample Cycles proof from the preserved hero camera. The four `kinetic-studio-<zone>-v006.png` files are 1600 × 1000 zone proofs. Native text, geometry, shaders, modifiers, lighting and all five cameras remain editable. All 20 file images are packed.

The scene now includes slimmer signage, cabinet returns and drawer construction, glazing details, organized workstation cables, audio hardware, richer instrument props, an articulated engineering concept, more detailed illustrative study graphics, project pin-ups, woven seating accents and fuller linked foliage. The warm interior and blue-hour direction remain intact.

The web bake exposed inward normals in 1,347 authored closed box meshes. `correct_surface_normals.py` corrects those surfaces in a new v006 source and preserves v005. `verify_kinetic_studio.py v006` independently reopens the result and checks outward box normals, all five renders, the original camera, editable structure, packed texture/provenance records, references and unchanged v004 files. Its receipt is `acceptance-v006.json`.

`export_tour.py` creates separate decimated meshes with Cycles lighting atlases and standard glTF unlit materials. It does not overwrite the master. `../kinetic-tour/README.md` explains the adaptive image/3D tour, controls, local launch and evidence. `../kinetic-splat/pilot-report.json` documents the separate experimental single-zone Gaussian reconstruction from preserved v005.

The source remains a design refinement, not final photoreal acceptance. Camera calibration, geography, anatomy and screen data retain the limits noted below. No new GUI-launch claim is made.

## Historical refinement: v004

`kinetic-studio-proof-v004.blend` and `kinetic-studio-proof-v004.png` are the current editable scene and visually reviewed 1920 x 540, 128-sample Cycles render. Earlier scene and image versions remain intact.

The refinement adds photographed leather response, softer sofa cushions and editable piping, a curved woven ergonomic chair back, a detailed leather lounge chair, scanned broadleaf foliage and succulents, procedural palm fronds, real-scale stoneware planters, photographed wood roughness, a licensed dusk HDRI, and three editable rugged alpine terrain meshes. The monitor landscapes are genuine renders of that new exterior. The hero camera and all four original zone collections are preserved.

Six Poly Haven CC0 assets are included: Potted Plant 02, Potted Plant 04, Mid Century Lounge Chair, Qwantani Dusk 2 Pure Sky, Brown Leather, and Wood Cabinet Worn Long. Source URLs, author metadata, verified download checksums, and local SHA-256 hashes are in `assets/asset-provenance.json`. All 20 file images used by the saved scene are packed into the blend. No Spline AI was used.

`refine_photoreal.py` creates v003 from v002. `balance_refinement.py` creates v004 from v003 after correcting the oversized terracotta planters and overly soft terrain observed in v003. `verify_kinetic_studio.py v004` reopens the source and checks the camera against v002, zone visibility, editable structure, packed textures, licensed asset hashes, image validity, original references, and preservation of the v002 source and PNG. Results are in `acceptance-v004.json` and `proof-verification-v004.json`.

Remaining limitations: the anatomy and technical graphics are schematic, the landscape is an artistic alpine reconstruction, and the initial camera fit is approximate. This is a refinement pass rather than final photoreal acceptance. The Windows GUI launcher issue described below was not re-tested during this refinement.

## Historical first proof: v002

- `kinetic-studio-proof-v002.blend`: editable Blender 4.5.3 LTS scene.
- `kinetic-studio-proof-v002.png`: visually reviewed 1600 x 450 Cycles proof, 64 samples.
- `acceptance-v002.json`: independent source reopening and image checks.
- `proof-verification.json`: render device, camera assumptions, reference hashes, provenance, and remaining limitations.

The scene contains 2,464 objects in ten named collections, including separate architecture, workstation, four zones, lounge/plants, exterior, lighting, and cameras. Geometry, native text, materials, lights, and modifiers remain editable. The four original Spline zones and warm lighting direction are represented. The original Spline source and supplied reference images were not modified.

## Camera and reference boundary

The hero camera is an inferred frontal fit to the upper panoramic panel of `The Kinetic Studio Concept Board-2.png`. Its 27 mm lens, assumed 23 m room width, 3.05 m eye height, and projected anchors are documented in the verification report. These are design assumptions rather than surveyed camera calibration. The supplementary four-zone board informed furniture and lighting.

## Build and verification

`build_kinetic_studio.py` creates and renders v001. `refine_proof.py` opens v001, applies the corrections observed in its actual render, and saves/renders v002. `verify_kinetic_studio.py v002` independently reopens v002 and checks source structure, editable signage/modifiers, lighting, reference preservation, and image content. Its successful marker is `KINETIC_EDITABLE_PROOF_PASS`.

The first proof had excessive flat fill and embedded platform LED strips. The refined revision reduced helper light illumination and visibility, exposed the LED strips beyond the platform faces, and reduced the meeting partition's grazing reflections. Earlier v001 files are retained for comparison.

The verified runtime is Blender's official `bpy==4.5.3` Python module, isolated at `<local-toolchain>\bpy-runtime`, using the bundled Python 3.11 executable in the portable Blender directory. The RTX 4070 Laptop GPU was selected through Cycles device discovery. The 64-sample refined render took approximately 38 seconds.

The portable Windows Blender GUI launchers encountered a bundled `blender.crt` side-by-side runtime error. The editable blend was instead created, rendered, and reopened using Blender's official Python module. GUI launching on this machine remains unverified; open the blend in a functioning Blender 4.5-compatible installation for interactive editing.

## First-proof provenance and remaining work

In v002 all geometry, shaders, foliage, and screen graphics were directly authored with Blender scripting. That first proof used no Spline AI, generated-image substitute, third-party asset library, or external texture dependency. The supplied concept boards remain unchanged; their SHA-256 hashes were checked after delivery. Later licensed additions are documented under the current revision above.

This is the first composition-and-lighting proof, not final photoreal acceptance. The anatomy model and display graphics are schematic, foliage and equipment need finer geometry, upholstery needs richer surface detail, and the exterior uses editable layered silhouettes and simplified city geometry. The render keeps those limitations visible. Native Spline interactions were not rebuilt or tested in Blender, and the separate Spline navigation task was not changed.
