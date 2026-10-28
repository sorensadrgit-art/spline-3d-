# Kinetic Studio — collaboration rules for Codex and Antigravity

This file applies to agents working in the published Kinetic Studio Git checkout. Read `docs/KINETIC_ANTIGRAVITY_COLLAB.md` before changes.

## Authority, invariant assets, and scope
- The **editable Blender master** is `work/kinetic-blender/kinetic-studio-proof-v006.blend`. Preserve its geometry, native text, materials, cameras, editable modifiers, lights and packed textures. Its recorded SHA-256 is `8b121564f8895917a9a0f820f95da5d0ef8069ea2715e8312d51f1096e962cfe`. Never replace it with a Web GLB, Spline scene, or Gaussian data.
- The historical original is `C:\Users\soren\OneDrive\Desktop\splinepro`. The curated Git checkout is `C:\Users\soren\OneDrive\Desktop\spline-3d-`. They are separate folders; never silently synchronize, clean or overwrite the former.
- Preserve all four zones: Motion Systems, Clinical Thinking, Creative Engineering, Projects; central workstation/Home; warm interior and blue-hour mountain exterior. Keep five camera targets and the original 27 mm inferred reference-camera intent.
- Keep `work/kinetic-tour/` (existing Vite, TypeScript, PlayCanvas image-first tour) working and unchanged while developing the first React Three Fiber proof in a **sibling directory** `work/kinetic-tour-r3f/`.
- Keep `work/kinetic-splat/` as a separate experimental pilot. Do not swap it into the main tour.
- No Spline AI. Use SOREN Blender Studio without the Architect workflow for any explicitly authorized Blender refinement.
- No backend/accounts, production deployment, domain changes, pushing to main, auto-merge, credential changes or deletion of historic inputs without specific scope approval.

## Collaboration and file ownership
- Antigravity: architecture/UX proposal, React + React Three Fiber + Three.js proof, motion choreography, responsive behavior and initial unit tests under `work/kinetic-tour-r3f/`.
- Codex: baseline inventory, GLB/export checks, independent test review, browser and visual evidence, performance comparison, integration recommendations.
- Independent auditor: verify facts against commands, diffs, manifests and actual browser runs. No agent may mark another agent's work accepted on assertion alone.
- Use distinct branches/worktrees and non-overlapping file ownership; coordinate changed shared files via the GitHub PR rather than overwriting each other.
- Prefer existing `agent-browser` CLI on Windows for browser QA. Never kill/rebind the already healthy port 4177; use a distinct port for prototype preview.

## SOREN stage contract
1. Understand: identify request, canonical files, reference commit, immutable artifacts and scope.
2. Investigate: inspect code, existing QA and browser baseline; distinguish observed results from prior handoff claims.
3. Rederive: independently compare options (keep PlayCanvas, R3F sidecar, Spline embed). Document trade-offs.
4. Plan Forge: write a phased, reviewable plan and explicit acceptance tests. No unbounded rewrite.
5. Plan Acceptance: get the Antigravity plan artifact accepted before multi-file code implementation; bounded setup work may proceed.
6. Execute: implement one isolated milestone at a time. Run automated tests, capture browser evidence, and record every changed file.
7. Result Acceptance: independent review, failed/untested checks disclosed, explicit go/no-go for replacing the existing tour.

## Baseline checks
From `work/kinetic-tour`:
```sh
npm ci
npm test
node tests/validate-models.mjs
npm run build
```
If browser infrastructure is available: reuse healthy `http://127.0.0.1:4177/` or run preview from an unused port and execute `python tests/browser_qa.py` with `agent-browser` installed. Treat a historical acceptance JSON as prior evidence, not fresh execution.
Check `work/kinetic-studio-delivery.json` and SHA-256 before changing any original delivered binary; require Git LFS for the Blender master.

## Acceptance non-negotiables
Home and all four zones; camera retargeting (1.35 s default, reduced-motion shortcut), rapid clicks; drag/wheel limits; Reset; keyboard 0–4/Home/Escape; browser Back/Forward; semantic image navigation, image-first mobile, GLB fallback and graphics context-loss resilience. Use the same existing desktop/mobile GLBs for the first proof, not a full Blender rebuild.
A passing desktop emulation **does not** prove physical-phone performance. Keep the PlayCanvas tour authoritative until visual parity, feature parity, browser QA and actual device performance are evidenced and reviewed.

## Reporting
Every milestone must include: RESULT, CHANGES, VERIFICATION (commands + observed output), VISUAL EVIDENCE, RISKS, BLOCKERS, and NEXT GATE. When blocked, stop destructive work and report the exact failure. Do not claim Antigravity or Codex is running unless a real session was started and observed.
