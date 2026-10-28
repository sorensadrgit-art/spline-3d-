# Launch Antigravity collaboration for Kinetic Studio

This repository branch contains instructions only; the Antigravity runtime has **not** been started from ChatGPT. Source implementation of the React/Three.js pilot has **not** begun.

## 1. Open the collaboration branch locally

The working Git checkout is `C:\Users\soren\OneDrive\Desktop\spline-3d-`. It is distinct from the original `splinepro` archive. In PowerShell:

```powershell
Set-Location "C:\Users\soren\OneDrive\Desktop\spline-3d-"
git status --short
git fetch origin
git switch collab/kinetic-antigravity-20261028
git lfs install
git lfs pull
```

If `git status --short` shows local changes, do not discard them; instead use a separate clone/worktree or reconcile first. Verify the displayed branch and read `AGENTS.md` and `docs/KINETIC_ANTIGRAVITY_COLLAB.md`.

## 2. Recommended: Antigravity App or CLI Teamwork

Google Antigravity supports `/teamwork-preview` on eligible paid plans in its **App and CLI**. Open this checkout as the workspace and paste the command below in the Antigravity conversation (not into PowerShell):

```text
/teamwork-preview Create an Antigravity engineering collaboration for Kinetic Studio, working from branch collab/kinetic-antigravity-20261028 of https://github.com/sorensadrgit-art/spline-3d-. Read AGENTS.md, docs/KINETIC_ANTIGRAVITY_COLLAB.md, the root README, work/kinetic-tour/README.md, src/main.ts, src/tour.ts and existing tests first. The source of truth is the editable Blender v006 master; keep the published PlayCanvas tour operational and the original splinepro archive untouched. Plan, independently critique alternatives, and after accepting the implementation plan execute an isolated React 19 + React Three Fiber 9 + Three.js pilot under work/kinetic-tour-r3f, reusing existing GLBs, images, camera anchors and zone data. Use GSAP only where it improves cinematic camera/UI choreography. Include workstation/Home and four zones, 1.35s camera retarget with rapid-click correctness, reduced motion, semantic image fallback, keyboard 0–4/Home/Escape, Back/Forward, reset/drag/wheel, model-load timeout, mobile image-first and graphics-loss handling. Preserve lighting direction and composition. Work in isolated worktrees with exclusive file ownership, coordinate via GitHub issue/PR, run real baseline tests and prototype tests, perform browser screenshot comparisons, and report actual performance evidence. Use the SOREN Understand -> Investigate -> Rederive -> Plan Forge -> Plan Acceptance -> Execute -> Result Acceptance contract. Spawn exploratory/read-only, UX/implementation and independent audit tracks as appropriate. Keep port 4177 and original Blender files untouched, never deploy publicly, and never merge to main. Produce a Plan artifact for review, then milestone commits, QA receipts, visual Walkthrough and a draft implementation PR; clearly mark missing physical-phone acceptance.
```

Antigravity will scope the request and present its own prompt/plan artifact for approval. Approve that artifact in Antigravity before autonomous implementation. Any external Codex collaborator should review via GitHub PR/comments; do not simulate a connected Codex agent.

## 3. Fallback: Antigravity IDE or no Teamwork entitlement

In the IDE's agent prompt, use:

```text
/plan Read AGENTS.md and docs/KINETIC_ANTIGRAVITY_COLLAB.md. Architect a reversible work/kinetic-tour-r3f proof with acceptance criteria, ownership, artifacts and rollback. Do not modify the Blender master or existing tour. After the Implementation Plan is approved, implement only M2 (Home + Motion vertical slice), run tests, capture browser evidence, and open a draft PR; do not deploy or merge to main.
```

Antigravity IDE supports structured `/plan`, but `/teamwork-preview` is an App/CLI feature. Continue remaining milestones only after evaluating M2 evidence.

## 4. Coordination rules

- Shared plan: `docs/KINETIC_ANTIGRAVITY_COLLAB.md`
- Persistent agent rules: `AGENTS.md`
- Antigravity-specific execution skill: `.agents/skills/kinetic-studio-collab/SKILL.md`
- Dedicated feature branch for React proof: `feat/kinetic-r3f-pilot`, based on collaboration branch.
- Review everything through GitHub draft PRs; no auto-merge.
- Existing preview: `http://127.0.0.1:4177/` (verify live before reuse). Prototype should use an available different port (4180 proposed).
- Baseline checks: `npm ci`, `npm test`, `node tests/validate-models.mjs`, `npm run build` from `work/kinetic-tour`.

## 5. What a successful first handoff contains

Antigravity returns (1) alternatives and an accepted plan, (2) a file ownership matrix, (3) actual M2 source changes on its feature branch, (4) observed tests and screenshots, (5) remaining issues, (6) a draft PR for Codex/independent QA review. Existing PlayCanvas continues to work.

Official references:
- https://antigravity.google/docs/teamwork/
- https://www.antigravity.google/docs/plan/
- https://www.antigravity.google/docs/skills/
