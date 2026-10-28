# SOREN KINETIC STUDIO — M4 Visual Fidelity & Acceptance

Prepared: 2026-10-28
Source: `feat/kinetic-r3f-pilot-20261028-codex` at `c6a1367ac72c88b809fbd5f27a8df75f53d2c46e`, after M3 PR #7 merged.
Execution branch: `feat/kinetic-r3f-m4-visual-20261028`.
Tracker: [Issue #1](https://github.com/sorensadrgit-art/spline-3d-/issues/1). Prior evidence: PRs #4, #5, #7.
Status at preparation: **PLAN PREPARED**, not launched on AgentZero. This file does **not** indicate Antigravity approval, real-phone testing, GPU testing, deployment, or implementation completion.

## Goal, decision and authority

The user said **"resume"** following verified M3 five-zone completion. Continue the next reversible phase: review and improve **cinematic visual fidelity, accessible interactions, and measured performance** of the five-zone React Three Fiber sidecar, without replacing the working PlayCanvas experience or changing 3D source assets.

The original Blender v006 packed editable master remains authoritative, with its recorded SHA-256 `8b121564f8895917a9a0f820f95da5d0ef8069ea2715e8312d51f1096e962cfe`. All ten prior delivery assets (master, Cycles renders, GLBs, splat) and the sky texture remain immutable. Current Web GLB assets are baked approximations and **cannot be assumed Cycles-equivalent**. Do not use Spline AI or Blender Architect. Retain the approved R3F hero typography, side-panel structure, navigation language and the corrected blue-left / magenta-right sky orientation.

This is scoped M4 work; no authorization to deploy, replace PlayCanvas, merge to main, change accounts, credentials, DNS, remote permissions, or rebuild Blender/glTF. No automatic main-branch merges.

## SOREN stage contract

**S0 Understand:** verify exact working branch/base, read project `AGENTS.md`, all collaboration plans and `docs/collaboration/CODEX_M3_STATUS.md`, list current assets/hashes, and confirm the five 3D destinations and M3 15/15 unit and 15 browser group acceptance receipts. Distinguish historical receipts from fresh execution.

**S1 Investigate:** independently inspect each of the five `tests/m3-evidence` PlayCanvas/R3F/Cycles locked camera frames, actual style/renderer controls, scene gradients, overlay occlusion, markers, sky/textures, and bundle/performance receipts. Identify at most 3 high-confidence, measurable visual/interaction defects that can be fixed **within R3F source only**. Do not infer every R3F-vs-PlayCanvas difference is a defect: document intentional design changes versus asset baked-render limitations.

**S2 Rederive:** compare (A) no change / preserve approved direction, (B) minimal runtime color or composition tuning, and (C) heavy postprocessing and scene regeneration. Prefer A/B. Reject changes that require reauthoring Blender assets, geometry or source GLBs. Document contrast, GPU cost, and rollback.

**S3 Plan Forge:** create `docs/collaboration/CODEX_M4_PLAN_FORGE.md`, a test/measurement matrix and objective before/after threshold for each selected correction; cap scope, ensure no duplicate camera or animation owner. Put proposed changes and constraints before edits.

**S4 Plan Acceptance:** user authorized continuing bounded refinement, not radical UI redesign. If proposed change preserves existing visual direction, improves an objectively evidenced issue, is reversible, and affects only the sibling R3F sidecar, record a narrow approval and proceed. If the issue requires aesthetics to be reinterpreted, extra 3D assets, production operation, or global tools/permissions, **stop with a review brief**, not an assumption of approval.

**S5 Execute:** fix each selected issue with RED → GREEN → REFACTOR tests first, using a single exclusive M4 worktree. Preserve the current functionality for all five zones (Home, Motion, Clinical, Engineering, Projects), exact cameras/anchors/content, single 1350 ms camera owner, rapid retarget, Orbit/Reset, reduced motion, keyboard 0–4/Home/Escape, history, image fallback, mobile image-first and lighter GLB, model/sky retry, accelerated timeout, generation/disposal, and synthetic context-loss behavior. Avoid adding GSAP/postprocessing unless a measurable, reviewed improvement justifies the cost. Keep the corrected `RepeatWrapping`, negative sky U repeat, offset and 92° yaw.

**S6 Result Acceptance:** independent read-only code/browser/visual audit, accurate report and draft PR. No claims beyond actual fresh measurements.

## Visual review and acceptance

1. Capture or reuse **matching 1920×1080** screenshots from one real browser and locked camera positions for all five zones. Include the baseline PlayCanvas screenshots and the source Cycles renders for context, not pixel-matching assertions. Produce a concise before/after HTML comparison and objective RGB/luminance/contrast/hue samples from regions clear of overlays.
2. Preserve exterior sky direction from M2 sky fix. If correcting over-saturation or room darkness, document exact CSS/renderer/material parameter changes, isolate the sky from geometry changes, and show all five visual comparisons. No silent correction of original source assets.
3. Preserve approved large serif hero, premium graphite/walnut palette, upper-left headline and right details panel; ensure readable text against scene, avoid overlap/scroll overflow; preserve visible keyboard focus and readable projected hotspot labels. Do not invent new content or change anatomical/clinical illustration truth claims.
4. Inspect marker hiding over UI, keyboard focus restoration and detail access. Axe automated 0 violations with composited marker contrast incomplete is **not blanket accessibility certification**. Verify painted/opaque foreground/background and actual visibility in screenshots, report manual screen reader as untested if no session.
5. Keep mobile 390×844 image-first / lighter GLB opt-in. Benchmark across at least a desktop 1920×1080 and emulated mobile viewport; clearly label emulation. If a physical phone can be reached through an explicitly authorized test path, measure real load, thermals, interaction and WebGL recovery; otherwise mark **PHYSICAL PHONE UNVERIFIED** and produce reproducible on-device instructions without inventing results.

## Performance evidence

- Repeat baseline and candidate sequentially on same hardware/browser/viewport; collect nav timing, model bytes, JS chunks, response resources, memory snapshots, long tasks, and rAF interval distribution. Include cold vs warm cache distinction. Current prior rAF scheduling medians: legacy 12.10 ms vs R3F 6.10 ms; **these are not GPU frame duration/FPS**.
- Existing R3F lazy chunk ~895 KB minified. Diagnose tree-shaking, splitting, unneeded imports, and only make a bounded dependency optimization if real bytes improve and all interaction tests pass. No unproven 60 fps claims; no disabling accessibility controls for speed.
- No real GPU reset can be inferred from synthetic `webglcontextlost`; mark a real reset explicitly unverified without hardware evidence.

## Required test & evidence gates

- Preserve or strengthen **15/15 R3F unit tests** and **15 browser scenario groups**; rerun legacy **3/3** and both builds, both GLB validators and all protected source hashes. Capture fresh baseline tests where possible.
- Demonstrate at least one failing RED check for each new code defect, then passing GREEN with unchanged regression requirements. If no justified defect exists, produce a read-only audit and stop; don't force edits.
- Verify exact all-five camera endpoints, navigation from inspected pose, graceful fallback, touch/mobile, a11y/contrast, memory/disposal and no errors in steady-state console.
- Save M4 receipts, screenshots, independent audit and a report at `work/kinetic-tour-r3f/tests/m4-evidence/` and `docs/collaboration/CODEX_M4_STATUS.md`. Keep generated `dist`, node_modules, caches and credentials untracked. Keep port 4177 (original), 4180–4184 (old tests/servers) untouched; find a free port such as 4185 before launching an isolated preview and use a uniquely named agent-browser session.

## Antigravity partner handoff

Antigravity desktop was observed on AgentZero; previous headless CLI conversations required file/terminal approval or timed out without a real reply. Ask Antigravity for **read-only independent five-view design critique** through the installed, authorized interactive interface when available. Use the existing plan in `docs/ANTIGRAVITY_START.md` and new M4 review question. Do **not** use `--dangerously-skip-permissions`, modify global Antigravity policies, simulate a critique, or share a writable worktree.

If Antigravity unavailable, record PENDING in `docs/collaboration/ANTIGRAVITY_M4_HANDOFF.md`, include the concrete review instructions and actual failure. Codex's own reviewer can verify separate items but must be labeled **Codex independent review**, not Antigravity.

## Git strategy / source protection

- Create an isolated AgentZero checkout/worktree from `feat/kinetic-r3f-m4-visual-20261028` only, never use the old `splinepro` archive or the authoritative worktree.
- Commit ONLY new M4 documents, evidence and scoped `work/kinetic-tour-r3f/` source/tests if justified. No protected source changes, no force push.
- When validated, open a **DRAFT** PR targeting `feat/kinetic-r3f-pilot-20261028-codex` (the corrected M3 feature branch) and link issue #1, M3 PR #7. Do not merge or deploy until owner reviews comparisons and device acceptance.
- If AgentZero inaccessible, do not claim a running CodeX process. Leave this branch and plan ready, with the connection blocker recorded on issue #1.

## Completion report shape

`STAGE | RESULT | BRANCH + SHA | CHANGED FILES | TEST RED/GREEN | FIVE-VIEW COMPARISON | ACCESSIBILITY | PERFORMANCE (REAL VS EMULATED) | ANTIGRAVITY STATUS | UNVERIFIED | DRAFT PR | NEXT GATE`.

**Begin with a fresh ground-truth check, not a generic brainstorm.**
