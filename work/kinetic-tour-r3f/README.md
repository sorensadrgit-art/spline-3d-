# Kinetic Studio — five-zone R3F proof

This sibling experiment leaves `../kinetic-tour` authoritative. React 19.2, R3F 9.4, Three.js r180 and Vite 8.3.5 are pinned in package-lock.json. Node 24.19/npm 12.1 were used for the checks.

```powershell
npm ci
npm test
npm run build
npm run preview
```

Preview: http://127.0.0.1:4180/. The port is strict; never stop or rebind the existing 4177 listener. `publicDir: '../kinetic-tour/public'` reuses existing assets read-only; Vite copies them into ignored dist during builds. No asset bytes are authored here. There are no accounts or backend.

Home, Motion Systems, Clinical Thinking, Creative Engineering and Projects have image and real GLB 3D destinations with the original exact cameras, anchors and details. All devices begin with images; mobile 3D opt-in uses studio-mobile.glb and DPR 1. Desktop DPR is capped at 1.5. Use keys 0–4/Home/Escape, browser Back/Forward, drag, wheel, Reset, semantic details and projected DOM hotspots. Reduced motion cuts immediately. Network, 45-second timeout and graphics-loss failures preserve image navigation.

CameraMotion has one authoritative pose owner, 1350ms smoothstep transitions and retargeting from the displayed pose, including inspection offsets. UI-covered projected markers are hidden; every detail remains accessible in the side panel. Keyboard navigation preserves focus when zone controls are replaced. R3F uses demand rendering. No GSAP, orbit library or extra effects compete for camera transforms. Model fetch is abortable; late parse results and shared geometry/materials/textures are explicitly disposed. The static sky texture is reused through R3F's loader cache.

## Verification

```powershell
python tests/browser_qa.py
python tests/compare.py
```

Requires the already installed agent-browser CLI. Scripts use named task sessions, snapshots before actions and direct Python subprocess calls. `compare.py` additionally requires the freshly built legacy tour on 4181 (`npm run preview -- --port 4181` from the legacy folder). The copied legacy test and validator in tests/evidence redirect only session/port/output paths; the original files stay unchanged.

See tests/evidence/prototype-browser-checks.json, legacy-browser-checks.json, source-hashes.json, commands.json, performance.json and a11y-*.json. [Visual comparison](tests/evidence/comparison.html) places actual legacy and prototype captures alongside each other.

## Limits

This is a bounded proof, not adoption approval. Camera coordinates match; renderer/sky/color response and UI placement differ visibly from PlayCanvas and Cycles. Headless Windows Chromium on Intel UHD is not a physical phone. Performance captures report requestAnimationFrame scheduling intervals during camera movement, not GPU render duration or an FPS guarantee. Navigation/load cache states were mixed; no controlled cold-load conclusion is supported. Heap snapshots are single samples, not leak certification. Five-zone functional checks pass in M3. Physical-phone performance, sustained thermals and final visual acceptance remain pending.

Historical M2 process: state and disposal tests were written before implementation; initial failures and endpoint correction were observed. UI automation was added after the first UI implementation, so this run does not claim a fully test-first UI process. Independent review found and drove fixes for skip navigation, retry, no-WebGL, stale drag, hotspot focus and cleanup. M2 review acceptance is recorded in docs/collaboration/CODEX_STATUS.md. M3 adds test-first rendered eligibility, all-pairs camera coverage and the inspected-pose regression; see its RED/GREEN notes and final receipts.

Rollback removes only this sibling folder and the new collaboration artifacts from the feature branch. Keep the existing PlayCanvas tour and Blender master.


## M3 evidence

Run `python tests/m3-evidence/browser.py` against this branch on unused port 4183 (`npm run preview -- --port 4183`). It reuses the existing browser regression plus all five real-camera/mesh/projection/detail checks, history/hash, reduced cuts, stale loads, inspection continuity and focus. `python tests/m3-evidence/verify.py` records unit/build/legacy/validator/hash results without editing protected sources. `python tests/m3-evidence/compare.py` additionally needs the unchanged legacy build served on free port 4184. These scripts use isolated agent-browser sessions and close only their own browser.

See [M3 comparison](tests/m3-evidence/comparison.html) and [status](../../docs/collaboration/CODEX_M3_STATUS.md). This is a functional proof, not permission to replace PlayCanvas or deploy. Physical-phone performance, actual GPU-reset recovery, Antigravity critique and owner visual acceptance remain separate gates.
