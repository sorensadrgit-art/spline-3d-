---
name: kinetic-studio-collab
description: Coordinates Antigravity and Codex planning, React Three Fiber experiments, Blender-source preservation, and evidence-based acceptance for Kinetic Studio. Use when modifying Kinetic Studio or executing the R3F collaboration plan.
---

# Kinetic Studio agent collaboration skill

Read `AGENTS.md` and `docs/KINETIC_ANTIGRAVITY_COLLAB.md` before making project edits. The published checkout is separate from the user's original `splinepro` workspace.

## Mandatory gate sequence

- **Understand:** state exact task, branch/base commit, affected files, Blender v006 hash and permissions. Current collaboration branch is not production authorization.
- **Investigate:** read `work/kinetic-tour/src/main.ts`, `src/tour.ts`, project README and existing QA receipts; run baseline tests if connected. Do not treat historical JSON as fresh proof.
- **Rederive:** compare PlayCanvas retention, parallel R3F, and Spline runtime. Identify trade-offs and rollback.
- **Plan Forge:** issue a reviewable artifact with ownership, sequence, dependency list, integration hazards and measurable success gates.
- **Plan Acceptance:** present one reviewable plan. Do not start multi-file implementation until this gate is accepted.
- **Execute:** isolated new directory `work/kinetic-tour-r3f/`; React/R3F proof, five zones, media fallback, transitions, history, accessible controls, performance. Do not alter the v006 .blend, original archive, baked GLBs or working PlayCanvas tour.
- **Result Acceptance:** independent QA and side-by-side visual evidence, explicit PASS/FAIL/UNVERIFIED, go/no-go, detailed changed files and rollback.

## Exclusive roles

1. Explorer: read-only codebase and dependency investigation; findings with file/line references.
2. Antigravity implementation lead: React/R3F code and unit tests in new directory only, coordinated worktree.
3. Codex/independent QA: review and verification via GitHub issue/PR; never claim external agent started without evidence.
4. Blender Studio: only if separately scoped source modification is approved; never invoke the Architect workflow.
5. Auditor: test logs, visual and performance report, exact branch+SHA.

Never have multiple agents write the same files concurrently. Record milestones in PR comments. Keep changes reversible, no Spline AI, no public deployment or main merge.

## First deliverable

M2 vertical slice must show Home and Motion Systems using existing GLB, the same semantic image tour if WebGL is unavailable, 1.35s/reduced-motion camera behavior, browser history, basic controls, test logs and two comparison screenshots. Only then expand to the remaining zones.
