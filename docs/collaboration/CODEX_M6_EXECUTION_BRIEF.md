# SOREN Kinetic Studio M6 — mobile hotspot collision fix
Date: 2026-10-28. Requested: RESUME after completed M5. Task: fix a reproduced R3F mobile interaction defect in an isolated branch. Not authorized to deploy, merge main, or modify PlayCanvas/Blender.

## Source and constraints
Repo: https://github.com/sorensadrgit-art/spline-3d-
Git main frozen baseline: 44ad922826da34bbcaf7bb83646b24cd694d084c
Branch: fix/kinetic-m6-mobile-hotspots-20261028
AgentZero isolated checkout: C:\ProgramData\SentinelX\workspace\kinetic-m6-mobile-markers-20261028
Read AGENTS.md; docs/KINETIC_ANTIGRAVITY_COLLAB.md; docs/collaboration/CODEX_M5_STATUS.md; work/kinetic-tour-r3f/src/StudioCanvas.tsx, src/main.tsx, src/style.css; tests/m5-evidence/mobile-marker-probe.json and mobile_markers.py; M3/M4 browser suites and relevant test-driven-development skill before coding.

M5 FAIL evidence: at 390x844 mobile emulation, image-first Home 3D opt-in uses studio-mobile.glb but three projected 44x44 DOM hotspot buttons overlap. Measured rectangles:
- Inspect The shared center x173 y197.359 width44 height44
- Inspect Material language x157.125 y239.875 width44 height44
- Inspect At blue hour x173 y171.8125 width44 height44
Overlap pairs: center/material and center/blue hour. Centers were individually clickable, and all three semantic detail buttons remained available. The failure is visual/touch target collision. CameraDirector currently hides markers when out of frustum or UI-covered but lacks inter-marker collision detection.

## Execute actual SOREN gates
Understand > Investigate > Rederive > Plan Forge > Plan Acceptance > Execute TDD RED/GREEN/REFACTOR > Result Acceptance.
1. Verify exact branch SHA and clean state, immutable asset hashes and availability of Node/npm, test framework, browser CLI, free local ports. Write docs/collaboration/CODEX_M6_PLAN_FORGE.md with alternatives, acceptance thresholds and rollback BEFORE editing runtime.
2. Reproduce actual failing 390x844 Home mobile 3D overlap on a separately running preview (prefer free localhost 4192), using existing probe or copied task-local equivalent. Record real before screenshot, marker rectangle overlaps and failing exit code; don't simulate RED.
3. Write a new failing regression unit test around a deterministic geometry/collision helper, plus browser tests measuring pairwise overlap, center elementFromPoint, labels and keyboard focus. Demonstrate RED before source fix; no unconditional/weak assertions.
4. Implement ONLY a minimal R3F-sidecar fix: deterministic collision prioritization or clustering that preserves true 3D anchor projections and the 44px visual/touch target with nonoverlapping visible rectangles (aim >=4px spacing); hiding lower-priority colliding markers is preferable to fake projection shifts. All original semantic details in zone details panel MUST stay accessible even if 3D markers are hidden. Address marker focus if it becomes hidden (transfer to corresponding semantic detail or safe fallback), rapid camera motion and viewport resize. Avoid hiding unrelated desktop hotspots.
5. Verify GREEN: mobile Home and all five zones at 320/390/430 widths as feasible, desktop 1920x1080; measure pairwise overlaps, visual rectangles, click hit tests, 44px minimum and mobile screenshots before/after. Ensure image-first, actual lower-detail GLB, DPR1, no overflow, semantic details, keyboard/focus, history, reduced motion, 1350ms retarget, sky UV correction and all exact camera poses are retained. Do not change model assets or animation owner.
6. Rerun full existing R3F unit test suite (prior 15/15), 15 browser groups, PlayCanvas 3/3 unit tests, legacy 8 browser checks, both Vite builds and GLB validator; record failures and retries truthfully. Verify all 10 manifest binary artifacts including materialized Git LFS Blender, plus sky SHA. No protected-source drift. Screenshot comparison should show corrected marker separation without visual-direction changes.
7. Axe and painted contrast plus semantic/touch access: record confirmed and incomplete findings separately; manual screen-reader, real phone, GPU reset and Antigravity design critique remain pending unless actually performed. No unsafe OS GPU reset. Don't claim an Antigravity response based on CLI presence; prior attempts timed out.
8. Save docs/collaboration/CODEX_M6_STATUS.md, task-local tests/m6-evidence scripts/screenshots/logs and independent reviewer receipt if real. Publish only this M6 feature branch and open DRAFT PR against main linking issue #1 and merged M5 PR #10, never merge or deploy. Stop with blocker if fix requires asset reauthoring or weakens 3D semantic UX.

## Non-negotiable
Protected: work/kinetic-blender/kinetic-studio-proof-v006.blend SHA256 8b121564f8895917a9a0f820f95da5d0ef8069ea2715e8312d51f1096e962cfe (74,025,533 B), PlayCanvas work/kinetic-tour, work/kinetic-splat, both original GLBs, sky JPG, all original renders, current desktop clone and historic splinepro archive. Do not touch other agents' worktrees or loopback 4177-4191. Prefer unused 4192/4193, verify before binding. No Spline AI, global permission overrides, credential operations, merge main, public deploy or replacement of authoritative PlayCanvas.

Report exact branch/SHA, source changes, real RED/GREEN overlap rectangles and 44px target, screenshots, all actual command exits, Antigravity/physical-device/real GPU-reset limits, draft PR URL and next owner acceptance gate. Start the scoped implementation now, not just a generic plan.
