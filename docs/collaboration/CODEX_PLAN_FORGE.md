# Codex Plan Forge — bounded M2
Date: 2026-10-28. Source HEAD b6968bbb54b8fd85a9fb6c6845fa90e4f2513630; feature branch feat/kinetic-r3f-pilot-20261028-codex.

## Scope and acceptance
Implement Home + Motion Systems only in work/kinetic-tour-r3f. Preserve Blender master, all delivered assets, PlayCanvas, splat, archive, main and port 4177. No deployment or adoption approval. Other destinations remain visible, labeled future proof, with honest image access only.

## Investigation and alternatives
A: Keep PlayCanvas authoritative: existing complete tour, smallest adoption risk, proven existing interactions. B: sibling React 19 / R3F 9 / Three.js proof: composable semantic UI and testable camera owner; adds runtime/bundle cost and material fidelity risk. C: Spline embed adds conversion/service dependency and uncertain asset fidelity; reject for this bounded reuse task. Choose B only as experiment; A stays authoritative until measured parity and independent acceptance.

## Architecture and ownership
AppShell owns navigation/history, image/3D mode, detail selection and fallback message. TourData is a byte-for-byte copy of existing tour.ts with provenance test against source. StudioCanvas is lazy, initializes only on explicit request (especially mobile), owns model lifecycle and context loss. CameraDirector exclusively owns camera pose plus bounded orbit, with demand rendering. DOM Hotspots project existing anchors and hide points outside the frustum. DetailPanel uses semantic buttons and aria-expanded. No GSAP: one monotonic camera owner suffices. CSS preserves warm walnut/graphite and blue hour with legible overlays.

Codex owns this feature directory and new collaboration documents. Antigravity is requested for read-only critique, no overlapping edits. Separate independent audit required; no invented Antigravity acceptance.

## Exact camera references
Home position [0,3.05,15.2], target [0,2.1,-2.3]. Motion position [-8.4,2.25,5.2], target [-8.55,1.55,-1.4]. All five original anchors and source data retained without coordinate drift. Legacy desktop FOV 46, mobile 65; near .05 far 350. Camera intent remains inferred 27 mm, not recalibrated.

## Sequence / RED GREEN
1. Fresh legacy install/test/build; validator copied to isolated evidence directory because it writes receipts. Verify delivered hashes before/after.
2. Tests first: deterministic route, 1350ms interpolation, retarget sampled actual pose, reduced-motion cut, bounded orbit, fallback generation/timeout, exact camera data. Observe failures; implement; rerun.
3. Semantic image UI and lazy R3F model loader using read-only publicDir ../kinetic-tour/public. Browser behavior tests written before UI execution; failures recorded honestly.
4. Browser Home/Motion image and 3D, history, rapid retarget, reset, keyboard, reduced motion, mobile model opt-in/overflow, failed model/timeout/context loss, focus/landmarks. Capture locked comparison screenshots on same viewport.
5. Build/typecheck/full tests, compare JS/assets and measured browser frame intervals/load timings. Record software renderer and physical-device limits.

## Acceptance matrix
Each check records PASS/FAIL/UNVERIFIED with exact command/exit and evidence: Home+Motion images/model; timing+rapid retarget; reset+bounded drag/wheel; history+keys; mobile image-first; model/error/timeout/context fallback; semantics+focus; matching camera screenshots; clean build/tests; frozen source hashes. No narrative-only pass.

## Risks / rollback / gates
Three unlit color management and sky orientation may differ; compare screenshots. Headless GPU timings are not physical-phone measurements. React/R3F adds bundle cost; measure. Asset parsing cannot be assumed cancellable: generation guard and disposal required. Timeout must keep image navigation usable. Rollback removes only sibling proof and new docs on feature branch.

S4 narrow plan acceptance: PASS against explicit docs/CODEX_EXECUTION_PROMPT.md S4 user authorization for reversible Codex-only M2. This does not accept Antigravity's absent artifact, full migration, other zones, production or merge. Antigravity gate PENDING. M2 result remains UNVERIFIED until real checks.
