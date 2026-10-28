# Kinetic Studio — bounded Gaussian pilot

This is a separate reconstruction experiment for the Creative Engineering zone. The editable authoritative studio remains `../kinetic-blender/kinetic-studio-proof-v006.blend`.

## Deliverables

- `kinetic-engineering-pilot-v001.ssproj`: native SuperSplat 3.7.0 project, saved and reopened in a separate session. It preserves one layer, 21,516 Gaussians, the corrected Y-up orientation and an authored inspection camera.
- `kinetic-engineering-pilot-v001.sog`: native SuperSplat compressed export, 957,256 bytes. It was loaded and visually reviewed in the actual local PlayCanvas viewer. Its file-space convention includes the standard export Z flip, handled in the viewer.
- `pilot-v005/engineering_3000.ply`: original trained Gaussian PLY, 5,079,326 bytes. This remains unchanged.
- `pilot-comparison.jpg`: paired source/held-out reconstruction views.
- `native-project-reopened.png`, `pilot-browser.png`, `compressed-pilot-browser.png`: inspected evidence from real editors/viewers.
- `pilot-report.json` and `project-checks.json`: identities, metrics, inspection and reopen checks.

Open the `.ssproj` in SuperSplat to edit the Gaussian layer. Open `http://127.0.0.1:4177/pilot.html` with the tour preview running for the raw PLY view. Add `?sog` for the compressed comparison. The scene loads only after clicking its explicit button. The source-image comparison works without graphics support.

## Reconstruction

`../kinetic-blender/prepare_splat_pilot.py` creates 144 deterministic, known-pose 1024 × 768 Cycles images from preserved v005. The dataset has 132 training images and 12 held-out views. The initialization is sampled from actual editable geometry and is explicitly recorded as an initialization, not a trained result.

The checksum-verified official Brush v0.3.0 Windows CLI trained the scene locally for 3,000 steps. The run capped Gaussians at 200,000, stopped growth at step 2,200, saved output every 1,000 steps and wrote the held-out evaluation images to disk. No paid service or public upload was used for training.

`check_pilot.py` independently reads the Gaussian properties and calculates held-out pixel errors. Mean PSNR is 24.577 dB; minimum is 21.965 dB. The compressed SOG is 81.15% smaller than the trained PLY. That size reduction is a file measurement, not a frame-rate or visual-fidelity claim.

The SuperSplat browser imported the actual trained file. It saved the native project with its standard file-input/download compatibility path. The automated browser's download transport failed; the same native generated export blob was saved without modifying its bytes. ZIP contents and hashes were checked, then the `.ssproj` was reopened in a separate SuperSplat session. The SOG export received the same transport treatment and was tested independently in a viewer.

## Decision

Keep the pilot experimental. The bench, lighting and actuator are recognizable, but thin edges, foliage and monitor traces have reconstruction artifacts. Full-room training was not attempted. The main adaptive tour uses baked meshes and the complete Cycles image fallback. Source mesh editability and live light authoring remain in Blender; Gaussian editability is a separate representation.

No physical-phone performance, surveyed scale, medical/anatomical accuracy, or final photographic acceptance is established by this pilot.
