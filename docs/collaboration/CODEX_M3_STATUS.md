# M3 result acceptance - 2026-10-28

RESULT: PASS for the owner-authorized five-zone functional R3F proof. Visual/adoption acceptance remains PENDING; NO-GO for replacing PlayCanvas. Antigravity PENDING. No deployment or merge.

Branch: `feat/kinetic-r3f-five-zones-20261028-codex`. Immutable base: `96f13b29a152cd9c6b5400796e56cbcfb13d5538`. Delivery SHA is the commit containing this evidence (publication receipt below / Git log); production source hashes are in implemented-source-hashes.json.

## Understand / Investigate / Rederive / Plan Forge / Plan Acceptance

Read complete M3 execution brief, project AGENTS, collaboration contract, CODEX_EXECUTION_PROMPT, CODEX_PLAN_FORGE, CODEX_STATUS, CODEX_SKY_PARITY_RESULT, R3F README/source/tests and legacy main/tour source. Verified exact branch/HEAD. Initially only the supplied M3 brief and backup were untracked; both preserved unstaged. Native LFS filter present; master was a 133-byte pointer. Materialized only the recorded LFS master using git lfs pull; actual 74,025,533 bytes matches manifest. No Blender editing.

All five typed zone/anchor/detail records already existed byte-identically to legacy (CRLF checkout preserved); AppShell restricted 3D eligibility. Retain PlayCanvas authoritative; extend existing R3F sidecar. Spline embed would add a runtime/conversion dependency and cannot preserve this renderer/control implementation. Asset rebuild is unnecessary and outside scope. CODEX_M3_PLAN_FORGE.md was written before production coding. Owner's brief/current request explicitly accepts narrow Codex M3; independent result/Antigravity/visual/device gates remain distinct.

## Execute / changes

- `src/main.tsx`: all five destinations retain the same lazy canvas/load generation; removed pending labels and 3D eligibility restriction; zone-specific messages/details; restore focus to selected nav/mode when keyboard/history/Escape removes focused controls.
- `src/state.ts`, `src/StudioCanvas.tsx`: travel/reset starts from displayed inspected position and last target before clearing orbit. Single 1350ms smoothstep owner, reduced cut and retarget remain. Hide UI-covered 44px markers while preserving exact anchors/projections; all three semantic details stay available even when a marker is hidden.
- Tests: actual rendered AppShell eligibility/image/content for each route, 25 ordered camera pairs/rapid/reduced cuts, inspected-pose regression, live five-zone camera/mesh/projection/hit/focus/history checks. Existing sibling browser test adds timing receipt before unchanged timing assertions.
- README, M3 plan/status, Antigravity handoff and scoped evidence only. No assets/libraries/lockfiles/lighting changes. Sky RepeatWrapping / repeat.x=-1 / offset.x=1 retained.

## RED GREEN REFACTOR

Real RED before eligibility change: 5 failures, 9 passes. GREEN 14/14. Independent reviewer found inherited orbital jump; additional RED 1 failure /15, then GREEN15/15. Focus RED (BODY after key4) and covered-marker RED were reproduced in the browser, fixed and retested. Obsolete eligibility state/branches removed instead of adding renderer variants. Full details in tests/m3-evidence/red-green-notes.md and RED receipts.

One final-suite attempt failed the reused camera endpoint/1550ms sampling assertion. Unchanged diagnostic run reached exact endpoint at 1372.6ms. Added timing evidence; subsequent full suite passed without relaxing assertions. Earlier failure remains documented as a scheduling/flakiness risk, not silently converted to PASS.

## Verification - fresh commands and observed exits

`npm ci --prefix work/kinetic-tour-r3f`: exit0, 45 packages, audit0. `npm ci --prefix work/kinetic-tour`: exit0,21 packages,audit0. Actual commands executed under normal scoped escalation review; no permission bypass.

Final serial `python work/kinetic-tour-r3f/tests/m3-evidence/final.py`: exit0, FINAL_M3_VERIFICATION_PASS. final-commands.json retains exact subprocesses/cwd/exits:

| Check | Observed |
| --- | --- |
| R3F npm test | exit0;15/15 |
| R3F npm run build | exit0;tsc + Vite; lazy chunk-size warning retained |
| PlayCanvas npm test | exit0;3/3 |
| PlayCanvas npm run build | exit0;existing chunk-size warning |
| Copied GLB validator | exit0;desktop/mobile14 meshes,14 materials,9 images;zero errors/warnings |
| Protected hashes |13/13;all10 manifest artifacts + exact sky + untouched source comparisons |
| Browser suite |exit0;15 groups, actual installed agent-browser, own session/port4183 |
| Comparison/mobile |exit0;fresh unchanged legacy on4184;same browser/hardware/viewport |
| Sky comparator |exit0;Home/Motion blue-left to violet-right maintained |

Production timeout remains45s; browser test accelerates only its timer to1200ms. Context-loss event is synthetic; actual GPU reset UNVERIFIED. Late model completion after Escape cannot reopen canvas. Failure/retry tests deliberately inject errors; separate steady success console and errors are empty. The temporary WebGL support probe can log informational `THREE.WebGLRenderer: Context Lost.` during initialization; no success-path warnings/page errors observed. Negative-suite logs are not clean-success receipts.

Exact live camera endpoints and actual camera look direction checked with numerical tolerance1e-10; DOM dataset endpoints exact. GLB scene independently inspected through mounted R3F store:14 actual meshes; one desktop GLB resource across five destinations. Independent literal anchor projections match DOM coordinates within0.01px. All currently visible markers pass actual elementFromPoint hit testing; UI-covered markers are hidden.

| Space | Position | Target |
| --- | --- | --- |
| Home |0,3.05,15.2|0,2.1,-2.3|
| Motion | -8.4,2.25,5.2|-8.55,1.55,-1.4|
| Clinical | -4.5,2,1.4|-4.4,1.7,-4|
| Engineering |4.4,2.05,1.8|4.95,1.75,-4.2|
| Projects |9.1,2,3|9.45,1.6,-2.7|

Measured final normal transition settled at 1460.3ms, including browser scheduling. Inspection navigation first-frame measured displacement0.0; eventual exact endpoints pass. Camera easing code duration remains1350ms.

## Visual evidence

[Full three-column comparison](../../work/kinetic-tour-r3f/tests/m3-evidence/comparison.html) includes five fresh PlayCanvas anchors, five fresh R3F GLB anchors and five matching image views. All desktop screenshots1920x1080. Mobile390x844 is emulation only.

- Home: [3D](../../work/kinetic-tour-r3f/tests/m3-evidence/home-3d.png), [image](../../work/kinetic-tour-r3f/tests/m3-evidence/home-image.png), [legacy](../../work/kinetic-tour-r3f/tests/m3-evidence/legacy-home-3d.png).
- Motion: [3D](../../work/kinetic-tour-r3f/tests/m3-evidence/motion-3d.png), [image](../../work/kinetic-tour-r3f/tests/m3-evidence/motion-image.png), [legacy](../../work/kinetic-tour-r3f/tests/m3-evidence/legacy-motion-3d.png).
- Clinical: [3D](../../work/kinetic-tour-r3f/tests/m3-evidence/clinical-3d.png), [image](../../work/kinetic-tour-r3f/tests/m3-evidence/clinical-image.png), [legacy](../../work/kinetic-tour-r3f/tests/m3-evidence/legacy-clinical-3d.png).
- Engineering: [3D](../../work/kinetic-tour-r3f/tests/m3-evidence/engineering-3d.png), [image](../../work/kinetic-tour-r3f/tests/m3-evidence/engineering-image.png), [legacy](../../work/kinetic-tour-r3f/tests/m3-evidence/legacy-engineering-3d.png).
- Projects: [3D](../../work/kinetic-tour-r3f/tests/m3-evidence/projects-3d.png), [image](../../work/kinetic-tour-r3f/tests/m3-evidence/projects-image.png), [legacy](../../work/kinetic-tour-r3f/tests/m3-evidence/legacy-projects-3d.png).

Manual visual review: warm cabinetry/workstation and distinct rigs, skeleton/prints, engineering bench/actuator and project table are present. Exact framing corresponds to legacy. R3F is darker/higher contrast than washed/gray PlayCanvas; sky more saturated violet, exterior/tree geometry angular/simplified relative to Cycles, baked lighting/reflections lack Cycles detail. Typography/right-panel differences intentionally retained. No photoreal or pixel parity claim. Independent reviewer actually viewed new-zone/Projects reference images and agrees these remain limitations.

## Accessibility / mobile / performance

Axe4.12.1: zero violations across all five3D views and images;3D retains one incomplete contrast rule (pseudo-element compositing and non-text +/- indicator). Images have zero incomplete. Manual locked desktop checks visually inspected currently visible marker numbers; screenshot fill samples equal opaque RGB21,35,36 and declared text RGB243,238,228 gives13.9939965:1. All visible markers physically hit their own buttons after overlap fix. This is scoped desktop evidence, not blanket accessibility/screen-reader certification.

Mobile390x844: image-first, no GLB until opt-in, all five images usable/no overflow; actual studio-mobile.glb selected, actual renderer DPR1 verified, Projects screenshot plus baseline Home mobile evidence. Desktop cap1.5 preserved; observed DPR1 on this monitor. No physical phone connected/tested; sustained phone FPS/thermals UNVERIFIED.

legacy: rAF scheduling mean 13.92ms / median 12.10ms / p95 24.30ms, 280 samples; navigation 423.8ms; GLB resource 186.7ms.

r3f: rAF scheduling mean 7.06ms / median 6.10ms / p95 12.20ms, 553 samples; navigation 15.0ms; GLB resource 93.1ms.

Same actual HeadlessChrome155, Windows10, Intel UHD ANGLE/D3D11,1920x1080,DPR1. Final measurement serial after browser suite; no parallel test render. One sequential loopback run with mixed browser/OS/cache state; navigation/heap samples are not controlled cold-load/leak evidence. rAF scheduling intervals are NOT GPU frame durations or FPS. No speed superiority/adoption conclusion. R3F JS202.37KB initial +894.98KB lazy (gzip64.89+238.83); legacy studio11.47KB +2498.25KB PlayCanvas (gzip5.31+642.67); compare loading policy before drawing conclusions.

## Result Acceptance / risks / blockers / next gate

A five actual GLB cameras/details/hotspots PASS; B five independent images/mobile opt-in PASS; C controls/history/keys/rapid/reset/orbit/reduced/stale/error/timeout/synthetic-loss PASS; D sky direction PASS, full visual parity PENDING; E tests/build/validators/hashes PASS; F actual browser/screenshots/manual desktop/a11y PASS within disclosed limits, phone/real GPU reset/owner review PENDING; G protected diff empty/no merge/deploy PASS.

Real independent native reviewer source/unit/screenshot findings drove3 fixes; receipt independent-review.md. Antigravity was NOT contacted in this run (no callable agy/antigravity in PATH); installed desktop binaries are not evidence of critique. ANTIGRAVITY_M3_HANDOFF.md contains concrete inspection tasks; status PENDING.

No implementation blocker remains. Risks: timing-check scheduling sensitivity (one failed run disclosed), conservative marker hiding, substantial lazy chunk, darker/more saturated/simple visual response, no sustained leak/device testing. Next gate: owner/Antigravity review draft stacked PR and side-by-side captures; actual phone and real GPU-reset acceptance before any proposal to replace PlayCanvas. No adoption/production authorization inferred.

## Source / tool provenance

Master SHA2568b121564f8895917a9a0f820f95da5d0ef8069ea2715e8312d51f1096e962cfe; desktop6a586e3d2115d226664a042c021f9432672f324b37cb9f29e50b27855a96c913; mobile d0c5fc11b5d7ac0b24523aed651e66d1d8df5aedfa53c639f4b77110911451e9; sky c45d164f9ebcc307feb66f9adcdd19182e1701e8ec2f51e1099cb0aaf7e8bc40. source-hashes.json distinguishes binary byte comparison from CRLF-normalized source comparison. implemented-source-hashes.json records current production source bytes.

Actually read local skill files: using-superpowers, soren-learning-loop, soren-plan-forge, kinetic-studio-collab, router, threejs-react-three-fiber, test-driven-development + writing-good-tests, agent-browser + installed CLI core, ui-skills-root, soren-universal-deployment, github-outside-sandbox, verification-before-completion. Guidance targeting newer Three APIs did not trigger upgrades; pinned r180/R3F9.4 retained. Deployment read-only preflight detected Vite/npm with no configuration issue; previews local only. Remote SOREN/Open Design/Lightswind tools not exposed; no MCP actions claimed. Caveman/chisle not found in installed skill roots; no configuration altered. Learning recall returned no matching lessons; no global memory/skill promotion. No external API behavior/research needed for locally grounded bounded changes.
