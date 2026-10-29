# CLAUDE.md

Repository guide for agent sessions. `AGENTS.md` is the binding collaboration contract; `docs/KINETIC_ANTIGRAVITY_COLLAB.md` is the execution contract. Read both before non-trivial edits. This file is an orientation map, not an authority that overrides them.

## What this repo is

**Kinetic Studio** — a four-zone Blender studio scene (Motion Systems, Clinical Thinking, Creative Engineering, Projects, plus a central workstation/Home, warm interior, blue-hour alpine exterior) shipped three ways:

1. `work/kinetic-blender/` — the editable Blender 4.5.3 master + Cycles proof renders + assets/provenance.
2. `work/kinetic-tour/` — the **authoritative** browser tour (Vite + TypeScript + PlayCanvas 2.23.3, image-first with baked GLB).
3. `work/kinetic-tour-r3f/` — a **sibling experimental** React 19 + React Three Fiber 9 + Three.js r180 proof. Not adopted, not deployed.
4. `work/kinetic-splat/` — separate experimental Gaussian/SuperSplat pilot. Never swap into the tour.

No backend, no accounts, no deployment. Everything is loopback-only.

## Commands

Legacy (authoritative) tour — `work/kinetic-tour`:

```sh
npm ci
npm test                              # node --experimental-strip-types --test tests/*.test.ts
node tests/validate-models.mjs        # Khronos glTF validator against both GLBs
npm run build                         # tsc --noEmit && vite build
npm run preview                       # 127.0.0.1:4177
python tests/browser_qa.py            # needs agent-browser CLI + running preview
```

R3F proof — `work/kinetic-tour-r3f`:

```sh
npm ci
npm test                              # unit tests (state, hotspots, resources, inspection, m3)
npm run build
npm run preview                       # 127.0.0.1:4180 --strictPort
python tests/browser_qa.py
python tests/compare.py               # also needs the legacy build on 4181
```

Node 24.19 / npm 12.1 / agent-browser 0.39.4 were the delivery versions. Git LFS is required for the `.blend`: `git lfs install && git lfs pull`, or the master appears as a 133-byte pointer file.

Port discipline: never stop, kill or rebind the existing `127.0.0.1:4177` listener. Use a free port (4180+, 4192/4193 were used for evidence runs) and isolated named agent-browser sessions; close only your own session.

## Protected artifacts — do not modify

- `work/kinetic-blender/kinetic-studio-proof-v006.blend` (SHA-256 `8b121564f8895917a9a0f820f95da5d0ef8069ea2715e8312d51f1096e962cfe`) and its native geometry, text, materials, modifiers, cameras, lights, packed textures.
- `work/kinetic-tour/public/models/studio-desktop.glb` and `studio-mobile.glb`, the zone renders in `public/media/`, and the supplied concept boards (`*.png` at repo root).
- `work/kinetic-tour/` source at all — the PlayCanvas tour stays authoritative and working.
- `work/kinetic-splat/` — separate pilot, never merged into the main tour.
- Never: push/merge to `main`, deploy, change domains/DNS/credentials, force push, broad cleanup or deletion, Spline AI, SOREN Blender "Architect" workflow, `--dangerously-skip-permissions`.
- Never silently sync or overwrite the historical archive `C:\Users\soren\OneDrive\Desktop\splinepro`.

`work/kinetic-studio-delivery.json` records byte counts and SHA-256 for the ten primary artifacts. Verify before and after touching any delivered binary.

## Source map

`work/kinetic-tour/src`
- `main.ts` — PlayCanvas app, state machine, hash routing, load/timeout/context-loss handling, 3D-anchor → 2D projection.
- `tour.ts` — typed `Zone` list, camera `position`/`target`, hotspot `anchors`, `blend()` smoothstep.
- `pilot.ts` — isolated `/pilot.html` loader (`?sog` for the compressed export).
- `style.css`, `hotspots.css`, `env.d.ts`.

`work/kinetic-tour-r3f/src`
- `tour.ts` — **same data as the legacy tour, byte-identical `tour.ts`**; zone ids `home|motion|clinical|engineering|projects`, exact camera poses, anchors, `blend()`. Change it only in lockstep or not at all.
- `state.ts` — `route(hash)`, `boundedOrbit(yaw ±0.15, pitch ±0.35, distance 0.9–1.12)`, `CameraMotion` (single pose owner, 1350 ms smoothstep, retargeting from the *displayed* pose), `loadState` generation machine.
- `StudioCanvas.tsx` — R3F canvas, GLB load/abort/dispose, inspection offsets, projected hotspot collection, demand-render invalidation.
- `hotspots.ts` — greedy collision selection: 44 px targets with ≥4 px separation, semantic order preserved, coordinates never mutated.
- `resources.ts` — `disposeScene()`: dedupe geometries/materials/textures, close image bitmaps.
- `main.tsx` — app shell, navigation, detail panel, keyboard/history wiring. `style.css` — styling.

`docs/` — exec briefs (`CODEX_EXECUTION_PROMPT.md`, `ANTIGRAVITY_START.md`) and `docs/collaboration/` with per-milestone plans, statuses, handoffs and independent reviews (M2–M6). Read the latest milestone status before starting new work; historical receipts are prior evidence, not fresh proof.

`.agents/skills/kinetic-studio-collab/SKILL.md` — agent skill describing the same gates.

## Behavioral contract

- Five destinations: Home + four zones, each with an image view and a real 3D view, both navigable.
- Camera: 1350 ms smoothstep transition, retargetable mid-flight from the displayed pose; reduced motion cuts immediately; Reset restores the selected camera; bounded drag/wheel.
- Navigation: keys `0–4`, `Home`, `Escape`; browser Back/Forward via hash routing; semantic landmarks; visible focus; `aria-expanded`/`aria-pressed`; 44 px targets.
- Failure paths must degrade to usable image navigation: asset error, 45 s timeout, no WebGL, graphics context loss, late-arriving parse results.
- Mobile starts in image mode and opts into `studio-mobile.glb` at DPR 1; desktop DPR capped at 1.5. No horizontal overflow at 320/390/430 px.
- One and only one camera transform owner. Do not introduce GSAP, an orbit library, scrolljacking, spinning cameras, particles or heavy postprocessing.

## Conventions and gotchas

- Coordinates are glTF Y-up: Blender `(x, y, z)` → `(x, z, -y)`. Keep hero camera intent and the inferred 27 mm reference framing.
- `work/kinetic-tour-r3f/vite.config.ts` uses `publicDir: '../kinetic-tour/public'` — assets are reused read-only and copied into an ignored `dist`. Do not author asset bytes in the prototype.
- R3F uses demand rendering: after viewport size commits you must `invalidate()`, otherwise hotspot projections and focus lag one resize behind (real M6 bug).
- Hotspot collision rejection must keep true anchors; hiding a marker must transfer focus to the matching semantic detail button.
- Dependency versions are pinned and tested; do not bump without re-running the full suite.

## Verification and reporting

Every milestone report needs: **RESULT, CHANGES, VERIFICATION (exact commands + observed output), VISUAL EVIDENCE, RISKS, BLOCKERS, NEXT GATE**. Never mark an unexecuted test as passing; never claim another agent is running without an observed session; a desktop emulation is not a physical-phone result.

Known limits that stay unverified until evidenced: physical-phone FPS/sustained thermals, real hardware GPU-reset recovery, manual screen-reader pass, Antigravity design critique, owner visual acceptance, Cycles/PlayCanvas pixel parity, and the Windows Blender GUI launcher. PlayCanvas remains authoritative until all of those plus visual and feature parity are reviewed.

Publication style: feature branch → **draft** PR linked to issue #1. No merge, no deploy.
