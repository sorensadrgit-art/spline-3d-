# SOREN Kinetic Studio — M5 merged-main release-readiness verification

Prepared: October 28, 2026. **Authorization:** User requested "resume" after M4 evidence completion. Proceed with a reproducible, non-deploying acceptance audit of the now-merged repository `main`. This does **not** authorize replacing the working PlayCanvas tour, public exposure, release promotion, original-file modification, changing credentials, or changing permission policies.

## Verified starting state and immutable boundaries

- Repository: https://github.com/sorensadrgit-art/spline-3d-
- Source baseline: `main` at `16d2a6b20bc5d29ef777bd3bf81dc8e16af9218f` (merge PR #9 at 2026-10-28 13:51:55Z). PR #8 M4 evidence was merged into the R3F feature branch before PR #9.
- M5 review branch: `feat/kinetic-m5-release-readiness-20261028`; starts at the above `main` commit.
- Legacy authoritative browser tour: `work/kinetic-tour/` (PlayCanvas); R3F sidecar in `work/kinetic-tour-r3f/`; editable Blender master `work/kinetic-blender/kinetic-studio-proof-v006.blend`.
- The owner's **original desktop checkout** `C:\Users\soren\OneDrive\Desktop\spline-3d-` is still a clean, older `main` at `c3f48b7694a70571987d14416ff30514efdb77fe`. **Do not fetch/pull/rebase/modify it**. Operate only in the isolated M5 checkout.
- Frozen master SHA256 `8b121564f8895917a9a0f820f95da5d0ef8069ea2715e8312d51f1096e962cfe` and size 74,025,533 bytes. Desktop GLB `6a586e3d2115d226664a042c021f9432672f324b37cb9f29e50b27855a96c913`; mobile GLB `d0c5fc11b5d7ac0b24523aed651e66d1d8df5aedfa53c639f4b77110911451e9`; sky `c45d164f9ebcc307feb66f9adcdd19182e1701e8ec2f51e1099cb0aaf7e8bc40`.

### Why this gate exists

M2–M4 proved five-zone R3F functionality but did not prove physical-phone behavior, true hardware GPU reset, owner design signoff, or Antigravity participation. M4 also verified only the 133-byte Git LFS pointer for Blender, not the full materialized master. **GitHub merging source into `main` is not equivalent to deploying or adopting the sidecar.** Verify the merged main tree in isolation and publish the remaining release gates and evidence without inventing approvals.

## SOREN workflow and exact deliverables

Follow Understand → Investigate → Rederive → Plan Forge → Plan Acceptance → Execute → Result Acceptance. Read `AGENTS.md`, `README.md`, `docs/KINETIC_ANTIGRAVITY_COLLAB.md`, `docs/collaboration/CODEX_M3_STATUS.md`, `docs/collaboration/CODEX_M4_STATUS.md`, `docs/collaboration/ANTIGRAVITY_M4_HANDOFF.md`, and both tour READMEs plus their test scripts before beginning. Confirm exact branch, HEAD, clean tracked state and latest remote main. If different from the frozen SHA, reconcile rather than assuming.

1. Create `docs/collaboration/CODEX_M5_PLAN_FORGE.md` before any mutations, plus a stage-by-stage `CODEX_M5_STATUS.md` and device/Antigravity handoff. The acceptance matrix must label PASS, FAIL, UNVERIFIED distinctly.
2. Materialize Git LFS **only in the isolated checkout** using normal `git lfs pull` after recording LFS pointer OID; verify the actual 74,025,533-byte Blender master checksum with SHA256. Validate ALL ten recorded delivery artifacts from `work/kinetic-studio-delivery.json`, plus desktop/mobile GLBs and sky. If unavailable, record the LFS failure explicitly rather than substituting historical evidence.
3. Run reproducible tests on the **merged main checkout**: `npm ci` and `npm test` and `npm run build` for both `work/kinetic-tour` and `work/kinetic-tour-r3f`, the existing GLB model validator with receipts kept **outside legacy paths**, and a negative asset/hash protection check. Expect historically R3F 15/15 and legacy 3/3, but report actual fresh outcomes.
4. Run the already-proven **15-group browser regression** across all five exact camera positions, image and opted-in 3D modes, keyboard 0–4/Home/Escape, Back/Forward, detail navigation, rapid retarget/inspected camera pose, reset, reduced motion, 45s timeout (test timer accelerated), stale model load, asset failure/retry, mobile image-first and lower-detail GLB selection, and synthetic context loss. Use a uniquely named `agent-browser` session and **ports that are actually free** (prefer 4190 and 4191); never kill/rebind existing 4177–4188 listeners. Do not open public network ports or create an outside-facing preview.
5. Capture release-candidate snapshots for all five R3F GLB destinations at 1920×1080, matching legacy fixed-camera views and at least one emulated mobile 390×844. Verify corrected blue-left/magenta-right sky and retained premium visual direction. Use `tests/m5-evidence/` for command outputs, checks, screenshot comparison, source hashes, a11y and console logs; keep caches and large node_modules untracked.
6. Evaluate WCAG contrast of projected hotspot buttons in actual painted frames and browser computed styles; automated axe zero confirmed violations with 3D incomplete rule is **not** a blanket PASS. Test semantic detail access for markers hidden by overlays, keyboard focus and at least one error recovery path. Manual screen-reader session must be marked UNVERIFIED unless performed on a real accessibility setup.
7. Collect bounded real GPU *browser* capabilities (adapter/renderer strings, WebGL extensions and GPU timers only if actually supported and non-disruptive). **Never trigger an OS-level GPU/driver reset**; such a hardware test requires separate safe owner arrangements. Record GPU timing vs rAF scheduling accurately and sustained performance caveats. Desktop or emulated phone is **not** physical-phone verification. Enumerate attached phone evidence honestly; prepare a concise reproducible physical-phone test protocol with pass/fail fields. No automatic LAN exposure, USB pairing, or sign-in.
8. Antigravity: if a real authorized interactive channel can request a read-only design critique without bypassing permission approvals, obtain a genuine response and record it. Historical `agy` attempts timed out; don't repeat indefinitely or use `--dangerously-skip-permissions`. If no authorized interactive approval is possible, prepare exact concise copy/paste instructions for the Antigravity desktop app and label review PENDING. Do not impersonate another model.
9. Run an independent read-only Codex review of the source/evidence, distinct from Antigravity. DO NOT invent a defect or edit runtime solely to demonstrate coding. For a genuine source bug, write failing reproduction first, make only reversible sidecar changes, rerun all tests, keep old tour protected, and record exact fix and rollback.
10. Publish **only M5 evidence/docs and scoped reproducible tests** on this M5 branch. Open a **DRAFT review PR targeting main**, labelled in description "review evidence, no deployment/adoption authorization". Do not merge, deploy, change environment variables, rename domains, reconfigure approvals, or replace the running PlayCanvas tour.
11. Include a final owner-facing release gate summary with an explicit next action: review five-view comparison; physically test a smartphone; supply manual visual signoff; if desired approve a genuine Antigravity critique in its desktop app. Report each as PENDING until done. Reconcile the difference between remote main and untouched old desktop checkout; do not pull it automatically.

## Objective acceptance matrix

| Gate | What qualifies |
| --- | --- |
| Source/provenance | Actual merged-main SHA, all primary artifacts byte-verified including full LFS master, unchanged protected source folders |
| Functional | Both apps build and test; R3F 15 browser groups, all five actual GLB cameras/semantic details; no new regressions |
| Visual | Matched five fixed-camera captures with controlled sky/hue and explicit limitations; owner aesthetic signoff is separate |
| Accessibility | Axe with incomplete contrast disclosed; keyboard/focus and painted marker evidence; real screen-reader not inferred |
| Performance | Accurate exact hardware/viewport/cache/device method; GPU FPS vs rAF distinction, no invented leak-free conclusion |
| Physical phone | **PENDING** unless physical phone tested; emulation is not evidence |
| Hardware reset | **PENDING** unless real hardware-level test proven, and never cause OS disruption solely for this task |
| Antigravity | **PENDING** without actual independent result |
| Release | **NO-GO** on public deployment, merge/adoption, replacement of PlayCanvas until owner release approval |

### Output and stopping rule

Deliver `docs/collaboration/CODEX_M5_STATUS.md`, `CODEX_M5_PLAN_FORGE.md`, `ANTIGRAVITY_M5_HANDOFF.md`, `work/kinetic-tour-r3f/tests/m5-evidence/` (bounded log/screenshot/test receipts), draft PR and GitHub issue #1 checkpoint. Preserve earlier M4/M3 receipts and existing worktree. Finish with exact branch SHA and verified, pending and blocked items. If external access or host permissions fail, write an honest partial acceptance report and stop **without bypass**.

**Begin the verification on AgentZero immediately, not a generic plan-only discussion.**
