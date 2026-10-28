# KINETIC STUDIO — Antigravity + Codex collaboration and execution contract

**Prepared:** 2026-10-28 (America/New_York)
**Project:** Kinetic Studio / Splinepro
**GitHub:** https://github.com/sorensadrgit-art/spline-3d-
**Frozen source baseline:** main at `c3f48b7694a70571987d14416ff30514efdb77fe`
**Collaboration branch:** `collab/kinetic-antigravity-20261028`
**Status:** Collaboration scaffold created; live Antigravity team NOT launched; React prototype NOT implemented; public deployment NOT authorized.

## 1. Mandate and success definition

Build a reversible, production-minded **React + React Three Fiber + Three.js tour prototype**, using the existing exported desktop/mobile GLBs, existing approved renders and established zone/camera data. Preserve the working PlayCanvas tour and native Blender master. Evaluate whether R3F materially improves cinematic quality, motion control, maintainability and accessibility without unacceptable mobile performance or visual regressions.

This is a **parallel proof**, NOT automatic approval to replace PlayCanvas or deploy the site.

### Preserve exactly
- Four navigable zones: Motion Systems, Clinical Thinking, Creative Engineering, Projects.
- Central workstation/Home and five distinct views.
- Warm interior lighting / cool blue-hour mountain backdrop, based on v006 Cycles proofs.
- Back/Forward, rapid navigation retargeting, 1.35-second ease, bounded drag/wheel controls, reset, keys 0–4/Home/Escape, reduced motion.
- Image-first access and complete semantic navigation when GLB/WebGL is unavailable, slow, lost or user-selected.
- Source editability and provenance; native Blender v006 is authoritative.
- Pilot SuperSplat remains separate and experimental.
- No Spline AI and no SOREN Blender Architect workflow.

## 2. Verified baseline and known limitations

Current published files:
- `work/kinetic-blender/kinetic-studio-proof-v006.blend`: native packed editable master via Git LFS.
- `work/kinetic-tour/src/main.ts`: PlayCanvas application, UI and lifecycle.
- `work/kinetic-tour/src/tour.ts`: typed zones, camera positions and hotspot anchors.
- `work/kinetic-tour/public/models/studio-desktop.glb`: baked delivery model.
- `work/kinetic-tour/public/models/studio-mobile.glb`: lighter mobile delivery model.
- `work/kinetic-tour/tests/browser-checks.json`: historical browser QA receipt.
- `work/kinetic-studio-delivery.json`: primary artifact hashes and sizes.

The handoff reports three unit tests, a Vite/TypeScript build, two zero-error/warning Khronos GLB validations, eight browser checks and clean publication; these are **prior-run evidence** and must be rerun where practical. Physical-phone FPS, sustained thermals and final photoreal review were NOT checked. Blender GUI launching on this Windows setup previously failed; official isolated `bpy` worked. GUI repair is outside this phase.

Local Windows roots (not guaranteed online):
- Archive: `C:\Users\soren\OneDrive\Desktop\splinepro`
- Published checkout: `C:\Users\soren\OneDrive\Desktop\spline-3d-`
- Current legacy preview reported at `http://127.0.0.1:4177/`; verify process before reuse.

## 3. Ownership and collaboration protocol

| Role | Owns | Cannot claim without evidence |
| --- | --- | --- |
| Antigravity Planner / UX Lead | Architectural comparison, interaction/visual specification, implementation plan artifact | User accepted direction / fresh test results |
| Antigravity Frontend Worker | New `work/kinetic-tour-r3f/` code, camera system, UI, fallback and interaction tests | Migration complete / existing tour replaced |
| Codex Integration / QA | Independent inspection, GLB identity/validator review, regression matrix, browser QA, performance analysis | Physical device result without a device |
| SOREN Blender Studio (only if needed) | Explicitly scoped native Blender edits and export updates | Rebuilt v006 without source+hash verification |
| Independent Auditor | Cross-check code diff, plan, tests, visual evidence, performance measurements | Acceptance based only on agent prose |
| Owner | Accepts plan, authorizes adoption/production changes | No change to authorization can be inferred |

**Git isolation:** Antigravity creates `feat/kinetic-r3f-pilot` *from the collaboration branch* in a separate Git worktree. Codex reviews from a separate checkout/worktree. Do not both edit the same paths concurrently. Never write prototype code into `work/kinetic-tour/` during the proof. Keep `main` untouched until explicit merge acceptance.

**Progress bus:** The GitHub draft PR contains proposed instructions and is the durable discussion thread. Each execution PR must link its plan version, baseline commit, screenshot/recording evidence and test results. Use issue comments for status and blockers, not unsupported assertions.

## 4. SOREN phases and gates

### M0 — Understand + Investigate: collaboration setup
Status: **SET UP** (docs branch), with remote live execution still blocked.
- Read original project docs and listed tests. Verify base commit and branch.
- Freeze master v006 and existing tour; snapshot delivered SHA-256 hashes.
- Confirm machine access, existing preview port owner and Antigravity App/CLI availability before spawning workers.
- **Gate M0:** no source/binary changes; repo branch and plan exist; no unverified 'agent running' claim.

### M1 — Rederive + Plan Forge: parallel architecture review
Status: **PENDING ANTIGRAVITY SESSION**.
- Independently evaluate: (A) keep PlayCanvas; (B) sibling React/R3F prototype; (C) Spline runtime/embed.
- Compare camera fidelity, shader/material fidelity, asset load/performance, interactivity, accessibility, development velocity and reversibility.
- Recommend B only if it has testable benefits; this plan expresses a preference, not a predetermined verdict.
- Inventory `src/main.ts` state machine: history/hash, rapid retarget, interactive vs image mode, abort/timeout, context-loss behavior, resize, project 3D anchors to 2D.
- Propose React component tree (`AppShell`, `ZoneNav`, `StudioCanvas`, `CameraDirector`, `Hotspots`, `DetailsPanel`, `ImageTour`, `LoadFallback`) and shared zone data.
- Decide animation: GSAP timeline for orchestrated movement; keep camera state authoritative in one place. No unnecessary real-time postprocessing that compromises mobile.
- **Gate M1:** reviewed Implementation Plan + baseline evidence + explicit file ownership + tests + rollback; Antigravity plan artifact accepted before source implementation.

### M2 — Execute: isolated R3F vertical slice
Status: **NOT STARTED**.
- Add `work/kinetic-tour-r3f/` with React 19, React Three Fiber 9, Three.js, Vite/TypeScript and minimal supporting dependencies; use versions proven compatible at install time.
- Load existing GLBs; avoid duplicating large assets where practical. Keep source GLBs immutable, verify SHA-256.
- Implement workstation/Home and one zone (Motion Systems) first with camera retargeting, image fallback and semantic controls.
- Keep mobile image-first. Use a distinct local preview port (proposed `4180`, verify availability).
- **Gate M2:** fresh typecheck/build/tests; documented comparison screenshots, keyboard/back, reduced motion, and no regression in existing PlayCanvas suite.

### M3 — Execute: five-view functional parity
Status: **NOT STARTED**.
- Complete Clinical Thinking, Creative Engineering, Projects views, hotspots, details, and deterministic navigation.
- Implement reset, orbit limits, hash/history, Escape and 0–4/Home behavior, low-GPU/device handling, timeout and WebGL context-loss fallback.
- Test rapid repeated navigation and cleanup of event listeners/render loops.
- **Gate M3:** every legacy functional behavior passes for both image and interactive modes; one verified desktop browser test and emulated mobile layout/model test.

### M4 — Execute: cinematic visual refinement + measurement
Status: **NOT STARTED**.
- Produce locked-camera comparisons against current v006 overview and zone images. Preserve accurate composition and high-quality material response; honor baked lighting limitations.
- Add restrained GSAP transitions and accessible micro-interactions. Respect `prefers-reduced-motion`, keyboard, focus and semantic fallback.
- Measure bundle sizes, load times, rendering/frame-time under reproducible conditions and memory behavior; benchmark against legacy tour on identical equipment and viewport.
- **Gate M4:** side-by-side screenshots and timing/device information, no hidden console errors or unmeasured 'optimized' claims. Physical phone must be tested before recommending replacement; otherwise mark that gate unverified.

### M5 — Result Acceptance: adopt, revise or retain PlayCanvas
Status: **NOT STARTED**.
- Independent reviewer assesses each gate, project constraints, parity matrix, accessibility, performance, screenshots and rollback instructions.
- If evidence insufficient, retain the existing PlayCanvas tour. If superior, produce a separate, reviewable migration PR and ask for explicit merge decision.
- Do not deploy, change domain, publish production, or overwrite Blender sources under this contract.

## 5. Verification commands and evidence

Legacy baseline (from `work/kinetic-tour`):
```powershell
npm ci
npm test
node tests/validate-models.mjs
npm run build
```

Browser acceptance with healthy and correctly identified preview:
```powershell
python tests/browser_qa.py
```
Only run this when `agent-browser` is installed and its test session can use the desired preview. Avoid clobbering the existing listener on `127.0.0.1:4177`.

R3F prototype should add its own `npm test`, `npm run build`, browser QA and comparison script. This is a **required implementation output**, not a currently existing tool or test.

Reviewer evidence checklist:
- exact branch/commit SHA, file changes, binaries unchanged;
- commands, exit status and key output (not 'passed' without execution);
- five matching zone screenshots plus image and 3D mode;
- nav keyboard/history/rapid-click/reduced-motion/context-loss cases;
- desktop and emulated mobile; physical phone explicitly tested or flagged;
- original PlayCanvas baseline green;
- explicit go/no-go and rollback route.

## 6. Failure and recovery policy

- Port conflict: inspect PID/process and reuse healthy preview; never terminate PID 53128 solely from stale handoff text.
- No Antigravity paid teamwork feature: use `/plan` in Antigravity, review artifact, then execute a single bounded milestone in normal agent mode (or `/goal` where available); preserve the same checks.
- Remote Windows device offline: continue documentation/review through GitHub, but do not claim live desktop build, browser QA or Antigravity execution.
- LFS pointer rather than actual master: `git lfs install` and `git lfs pull` before Blender operations.
- Missing historical raw assets: do not attempt to replay Blender v001–v005 reconstruction from a clean published checkout.
- Acceptance fails: preserve PlayCanvas, revert only branch-scoped changes; report reason and smallest next action.

## 7. Handoff contract

At each milestone, post:
```text
STAGE:
RESULT: PASS / FAIL / BLOCKED
BASE COMMIT + BRANCH:
CHANGED FILES:
VALIDATION COMMANDS + OBSERVED OUTPUT:
SCREENSHOTS / ARTIFACTS:
PERFORMANCE DATA (device, resolution, median frame time, load):
REMAINING RISKS:
NEXT GATE:
```

Antigravity launch instructions and paste-ready request: `docs/ANTIGRAVITY_START.md`.
