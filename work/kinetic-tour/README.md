# Kinetic Studio — cinematic master and adaptive tour

The editable source is `../kinetic-blender/kinetic-studio-proof-v006.blend`. The main tour uses separate baked delivery meshes. Source geometry, native text, modifiers, materials, lights and five cameras remain editable in Blender. v004 and v005 remain preserved checkpoints.

## Open the local tour

The current loopback preview uses port 4177. Open `http://127.0.0.1:4177/` in a browser. The experimental Gaussian page is `http://127.0.0.1:4177/pilot.html`.

For another local session, double-click `start-tour.cmd`. If dependencies are missing, run `npm ci` in this directory, then `npm run build` and `npm run preview`. Node 24.19.0 and npm 12.1.0 were used for this delivery. No hosting account or backend is required. Nothing was publicly deployed.

## Controls

- Choose any of the four zone buttons. Workstation or the Home key returns to the overview.
- Keys 0–4 select the overview and zones. Browser Back and Forward restore the selected zone.
- Choose **Explore in 3D** to enter the baked mesh tour. Drag to inspect within a bounded angle. The wheel adjusts distance slightly. **Reset view** restores the selected camera.
- Numbered 3D markers open the corresponding detail. The same descriptions are available as semantic HTML buttons in image mode.
- **View cinematic images** or Escape returns to the image tour. All five views work without graphics support.
- Reduced motion removes camera travel. Phones begin in image mode and can opt into the lighter 3D model.

The image tour is the initial presentation. Desktop browsers preload the 3D asset when data saving is off. Loading, graphics loss and errors retain usable image navigation. The pilot is explicitly separate and loads only on request.

## Files and evidence

| Artifact | Purpose |
| --- | --- |
| `public/models/studio-desktop.glb` | Baked desktop delivery scene |
| `public/models/studio-mobile.glb` | Lower-detail geometry and smaller atlases |
| `public/models/blue-hour.jpg` | Dusk sky derived from the licensed packed HDRI |
| `public/media/*.webp` | Real Cycles overview and four zone views |
| `src/tour.ts` | Typed zone content, camera anchors and points of interest |
| `tests/model-checks.json` | GLB identities and independent validation summary |
| `tests/validator-*.json` | Full Khronos validator reports |
| `tests/browser-checks.json` | Executed agent-browser acceptance checks |
| `../kinetic-blender/tour-export.json` | Bake parameters, geometry counts, source identity and file sizes |
| `../kinetic-splat/pilot-report.json` | Separate reconstruction experiment and held-out metrics |

Run `npm test`, `node tests/validate-models.mjs`, and `npm run build` for source/model checks. With the preview running, `python tests/browser_qa.py` runs the bounded agent-browser regression. Browser QA uses its own named session and closes only that session.

The installed versions are pinned in `package-lock.json`: PlayCanvas 2.23.3, Vite 8.3.5, TypeScript 7.0.2 and Khronos glTF Validator 2.0.0-dev.3.10.

## Source and rights

Geometry and illustrative studio graphics are authored for this project. Six existing Poly Haven CC0 assets supply scanned foliage, a lounge chair, leather, wood response and a dusk HDRI. Their author/source records and checksums remain in `../kinetic-blender/assets/asset-provenance.json`. No Spline AI or generated-image substitute was used. The original Spline scene and supplied reference boards were not modified.

## Limits

The hero camera remains an inferred concept-board fit. Terrain is artistic; anatomy, motion displays, instrument prototypes and project graphics are illustrative. Baked glTF lighting approximates the Cycles master and does not preserve live light editing. Edit lighting in Blender and rebuild delivery assets.

Desktop and mobile layouts were checked in a Windows Chromium browser. A small viewport is not a physical-phone performance test. Sustained device performance and final photographic quality remain review items. The Windows Blender GUI launcher issue from the earlier proof was not repaired; official isolated bpy reopened and verified the native sources.

The Gaussian pilot uses v005, 132 training views and 12 reserved views. It retains thin-edge and screen artifacts and was not promoted to the main tour. Do not treat its metric or load success as full-room reconstruction acceptance.

The native pilot project is `../kinetic-splat/kinetic-engineering-pilot-v001.ssproj`. It was created by SuperSplat 3.7.0 and reopened in a separate browser session. The layer count, Gaussian count, Y-up orientation and camera persisted. `../kinetic-splat/project-checks.json` records the file identity and checks. Browser file-input/download compatibility mode was used; a failed download transport was recovered from the editor's actual generated export blob.

The matching compressed `.sog` is in the same directory. `pilot.html?sog` loads that export independently. The trained PLY and compressed SOG were both visually inspected in the local viewer; the pilot retains the disclosed reconstruction artifacts.
