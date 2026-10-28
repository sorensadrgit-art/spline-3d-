# SOREN / CODEX EXECUTION BRIEF — KINETIC STUDIO × ANTIGRAVITY
Date: 2026-10-28. AgentZero Windows machine. This is a real engineering assignment, not a proposal-only brainstorming exercise.

## Your role and immediate mandate
You are Codex, technical lead and verifier for Kinetic Studio. START NOW. Coordinate honestly with Google Antigravity (already installed and running on AgentZero) and create a reversible React + Three.js refinement pilot without damaging completed assets. Execute the SOREN contract: Understand → Investigate → Rederive → Plan Forge → Plan Acceptance → Execute → Result Acceptance. Maintain durable shared state, actual test evidence, stage gates, and an auditable handoff to the user.

Begin by inventorying the branch and repo, evaluating the existing architecture, recording a detailed but bounded plan, then IMPLEMENT the isolated M2 vertical slice (Home + Motion Systems) if it meets the pre-agreed scope and objectively passes the plan-acceptance checklist below. This user message authorizes that bounded, reversible proof only. Ask for approval before material scope changes, replacement of PlayCanvas, Blender changes, external deployment, or merge into main. If a tool is blocked, continue the independent Codex portion and report the specific blocker instead of fabricating Antigravity output.

## Project identity and exact locations
Repository: https://github.com/sorensadrgit-art/spline-3d-
Published source baseline: main at c3f48b7694a70571987d14416ff30514efdb77fe
Collaboration plan branch: collab/kinetic-antigravity-20261028 (includes AGENTS.md, docs/KINETIC_ANTIGRAVITY_COLLAB.md, docs/ANTIGRAVITY_START.md, .agents/skills/kinetic-studio-collab/SKILL.md).
GitHub coordination issue: https://github.com/sorensadrgit-art/spline-3d-/issues/1
Draft collaboration plan PR: https://github.com/sorensadrgit-art/spline-3d-/pull/2

On AgentZero:
- HISTORICAL ARCHIVE: C:\Users\soren\OneDrive\Desktop\splinepro
- PUBLISHED CHECKOUT: C:\Users\soren\OneDrive\Desktop\spline-3d-
- Your task must run in a NEW isolated Codex clone/worktree, not either of those roots. Confirm actual cwd, branch and git state before editing.
- Antigravity desktop app location: C:\Users\soren\AppData\Local\Programs\antigravity\Antigravity.exe
- Antigravity CLI: C:\Users\soren\AppData\Local\agy\bin\agy.EXE (previously observed 1.4.8).
- Codex CLI: C:\Users\soren\AppData\Roaming\npm\codex.cmd (previously observed 0.164.0).
- A separate collaboration checkout may exist at C:\ProgramData\SentinelX\workspace\kinetic-antigravity-collab-20261028; DO NOT modify it because that is reserved for the Antigravity track.

Read these FIRST: AGENTS.md; docs/KINETIC_ANTIGRAVITY_COLLAB.md; docs/ANTIGRAVITY_START.md; .agents/skills/kinetic-studio-collab/SKILL.md; README.md; work/kinetic-tour/README.md; work/kinetic-tour/src/main.ts; work/kinetic-tour/src/tour.ts; work/kinetic-tour/tests; work/kinetic-blender/README.md; work/kinetic-studio-delivery.json. Do not assume a handoff statement is current; check live files.

## Source-of-truth invariants
- The *editable Blender v006 master* is work/kinetic-blender/kinetic-studio-proof-v006.blend, original SHA-256 8b121564f8895917a9a0f820f95da5d0ef8069ea2715e8312d51f1096e962cfe; preserve native geometry, materials, lights, modifiers, packed textures, text, cameras. The master is stored via Git LFS. Do not rebuild it or edit source Blender scripts without separate permission.
- Current browser viewer: work/kinetic-tour/ uses TypeScript/Vite/PlayCanvas with image-first fallback and desktop/mobile baked GLBs. It is COMPLETED, not a broken prototype. Do not overwrite or replace it.
- Four zones: Motion Systems, Clinical Thinking, Creative Engineering, Projects; plus central workstation/Home. Warm interior lights + blue-hour mountain exterior, correct composition and hero camera intent.
- Native cameras, five renders, original supplied concept boards, and authored scene direction must remain recognizable.
- Keep Gaussian SuperSplat pilot in work/kinetic-splat/ completely separate. Do not use Gaussian data as a substitute mesh master.
- No Spline AI. If native Blender refinement is ever needed, use SOREN Blender Studio without Architect workflow; it is OUT OF SCOPE for this first execution.
- No production deployment, domain/DNS changes, credential reads/exports, blanket license creation, broad cleanup, deletion, merge to main, or force push.

## SOREN phased collaboration protocol
**S0 Understand.** Confirm repo root, branch, HEAD, clean state, source hashes, local runtimes, constraints. Note whether Antigravity and Codex are actually reachable. Do not infer a connection from executable presence alone.

**S1 Investigate.** Read code and tests; run fresh existing baseline checks from work/kinetic-tour: npm ci, npm test, node tests/validate-models.mjs, npm run build. Use the existing healthy preview on 127.0.0.1:4177 only for viewing; verify its owner before use, never kill/rebind it. If it is unavailable, use a nonconflicting port. Capture command output and failures. Record which evidence was historical versus freshly generated.

**S2 Rederive.** Compare (A) keeping PlayCanvas, (B) parallel React/React Three Fiber + Three.js proof, (C) Spline runtime/embedding. Select based on measurable cinematic camera control, maintainability, accessibility, asset fidelity, mobile/device performance and reversibility. Do NOT decree R3F is better without measurement.

**S3 Plan Forge.** Create docs/collaboration/CODEX_PLAN_FORGE.md on your feature branch with scope, source references, component tree, motion system, file ownership, independent Antigravity/Codex workstreams, RED/GREEN tests, acceptance matrix, risks, rollback, and next gates. Use exact existing camera coordinates from work/kinetic-tour/src/tour.ts. Publish plan and stage results as status evidence in docs/collaboration/CODEX_STATUS.md; each section must include RESULT, CHANGES, VALIDATION, BLOCKERS, NEXT GATE.

**S4 Plan Acceptance.** Evaluate the plan against all invariants and the existing collaboration contract. The user's instruction authorizes starting an M2 proof in a **new isolated directory only**. If the plan is inside that scope, record a PASS for that narrow gate and proceed; if not, STOP and request owner decision. Do not call migration to production 'accepted'. Antigravity plan approval is a separate gate and must not be invented.

**S5 Execute M2.** Implement only the working vertical slice described below, applying test-driven development (test fails first, then pass, then refactor). Keep all implementation and test files under work/kinetic-tour-r3f/ except the new docs/collaboration status artifacts. Work from a new branch feat/kinetic-r3f-pilot-20261028-codex based on the collaboration branch. No changes in the existing tour directory. Do not share an editing worktree with Antigravity.

**S6 Result Acceptance.** Independent inspection of code/diff and actual browser comparison. Record exact commands and exit codes, screenshots and source file hashes, regressions, accessibility, and what is unverified. M2 is accepted only if basic parity passes; do not extrapolate to all four zones or a physical phone. If complete and permitted, publish a feature branch and DRAFT PR only, linked to issue #1; no auto-merge.

## Antigravity collaboration: actual participation, not simulation
Treat Antigravity as visual/UX and R3F implementation collaborator, Codex as orchestration/integration/QA. Look for the already-running Antigravity App on AgentZero and its native supported interaction path. Its CLI may require interactive read_file/command permission in headless mode; prior attempts were DENIED. DO NOT use --dangerously-skip-permissions, change Antigravity global permission policies or attempt to impersonate its model output. Prefer authorized interactive permission prompts or create a structured handoff in GitHub issue #1 and docs/collaboration/ANTIGRAVITY_HANDOFF.md. Record a real response from Antigravity only if an actual call succeeded. If not, proceed with the Codex-only vertical slice in your own branch and mark Antigravity PENDING.

Ownership:
- Antigravity: non-overlapping design/UX critique, future polish, review of five-view navigation and cinematic style, possible independent feature branch.
- Codex: M0–M2 execution in isolated Codex feature branch, deterministic data/state architecture, TDD, integration test harness, QA evidence.
- Independent reviewer: inspect screen captures, build logs, perf and diff; never mark a gate PASS on narrative assertions alone.
- Shared state: GitHub issue #1 + docs/collaboration. Do not silently overwrite other agents' changes.

## M2 vertical slice — precise technical work
Create work/kinetic-tour-r3f/ as a sibling of work/kinetic-tour/, using compatible React 19, React Three Fiber 9, Three.js, Vite, TypeScript, CSS/Tailwind as suitable; use GSAP only for clear benefit and never create dual control of camera transforms. Keep dependencies minimal and pin/test versions. Reuse delivered studio-desktop.glb, studio-mobile.glb and zone renders; prefer a read-only Vite publicDir pointing at existing tour/public or a documented reproducible asset-copy process that leaves original bytes unchanged.

Component contract:
- AppShell: layered cinematic UI, strong typography, semantic landmark navigation.
- TourData: typed zone ids, target and position arrays, hotspot anchors ported from existing tour.ts without drift.
- CameraDirector: cancellable/retargetable 1350ms camera transition, monotonic single state owner, reduced-motion immediate cut, safe rapid consecutive selections.
- StudioCanvas: low-overhead R3F model loader and camera, bounded pointer drag/orbit plus wheel/Reset without disorientation, lighting/baked colors close to original.
- ZoneNavigation and DetailPanel: Home and Motion Systems as functional target screens; all five navigation destinations shown as appropriate but unfinished sections clearly labeled, not fake completed.
- ImageTour/LoadFallback: complete semantic Home + Motion navigation when WebGL fails, context lost, asset timeout, or user selects images. Mobile starts in image mode, can opt into lighter model; preserve navigation.
- Hotspots: keyboard and screenreader accessible DOM buttons tied to grounded 3D anchor coordinates, safe screen projection.
- History: hash routing / Back/Forward, keyboard 0–4/Home/Escape, Tab order, Escape image mode, and visible focus states.

Motion/art direction:
- Cinematic but restrained: composition-first, warm tungsten cabinetry and cool exterior, walnut/graphite/brushed metal, gentle parallax and depth, 1.35-second smooth camera dolly with retargeting. Avoid spinning camera, gratuitous particles, excessive bloom, unnecessary postprocessing, fixed desktop-only canvas, scrolljacking, or inaccessible custom controls.
- Desktop should preserve hero camera character and compare with v006 3840×1080 and zone render. On small screens, maintain legible overlays, avoid layout overflow, start image mode, only initialize WebGL on request.
- Performance: compare same device/viewport and the legacy viewer. Record warm/cold load, average/median frame time (not invented FPS), asset sizes, JS bundle and memory where available; cap pixel ratio and degrade gracefully. Do not state "60fps" without measured evidence.

## M2 acceptance tests (minimum)
1. Home image and Home R3F scene render with existing model.
2. Motion Systems image and 3D view render and navigate correctly from Home and back.
3. 1.35 s transition, fast double-click retarget, reduced motion and camera reset.
4. Keyboard Home/0/1/Escape and browser Back/Forward restore views.
5. Mobile image-first, opt-in lower-detail GLB, no horizontal overflow.
6. Asset error, timeout, no-WebGL/context loss lead to still usable image navigation.
7. Landmarks, keyboard focus, meaningful alt text, aria-expanded/pressed and reduced-motion support.
8. Browser screenshots of locked Home and Motion camera side-by-side against legacy. Document unavoidable bake/material differences.
9. Build/typecheck/test pass; legacy test suite remains green. Run browser automation through existing local agent-browser CLI when available and preserve actual output.
10. No changes to Blender .blend, exported GLBs, PlayCanvas app, SuperSplat pilot or supplied concept references.

Use a test-first RED → GREEN → REFACTOR loop for each behavior; never mark unexecuted tests as passing. Add failure-path tests, not just happy paths.

## Delivery format and finish line
Create/maintain:
- docs/collaboration/CODEX_PLAN_FORGE.md
- docs/collaboration/CODEX_STATUS.md
- docs/collaboration/ANTIGRAVITY_HANDOFF.md
- work/kinetic-tour-r3f/ with clean build/test scripts, README, source, tests and test evidence (bounded text/screenshots; don't commit secrets, caches or unlicensed assets).
- Draft feature PR linked to issue #1 when changes are verified and repository authorization is available.

Report at the end of this run:
STAGE / RESULT; exact branch + SHA; Antigravity contact status with evidence or blocker; implementation summary and changed files; baseline and prototype tests with observed outputs; screenshots; performance evidence and unverified items; PR/issue links; any required user approval. The current request is to BEGIN, not to falsely claim full migration. Start by checking repository state immediately; do not give me another generic plan and stop.

IMPORTANT: Don't interrupt other Codex sessions or background processes. Do not kill the existing Node preview on port 4177. Never use dangerous bypass flags. Do not deploy.
