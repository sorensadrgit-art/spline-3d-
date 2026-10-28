# M2 sky-parity correction — 2026-10-28

RESULT: PASS for bounded horizontal sky orientation; full visual/adoption acceptance PENDING. PlayCanvas remains authoritative. No M3, merge or deployment.

Branch: `fix/kinetic-r3f-sky-parity-20261028`. Parent `9b960ee0de9b230761340b9ee99c4f5bcf2594e4`. Verified implementation/evidence commit `a025ba11a0560133cade087b63041fb22bc5d077`; subsequent receipt commit adds this report and strips one trailing space from captured build output (first diff whitespace check reported it; corrected before publication). Source rendering code is identical to the verified implementation commit.

## Understand → Investigate → Rederive → Plan Forge → Acceptance

Read complete follow-up, AGENTS, collaboration contract, status, independent review and sibling README. Used only the assigned isolated checkout. PlayCanvas inward/front-culled sphere and Three BackSide sphere both use 92° yaw, but their U direction differs. Locked Home/Motion captures confirm reversal. Keep PlayCanvas authoritative; a parallel R3F correction is bounded/reversible. Spline embed or asset/model rebuild would not address this local mapping defect and would expand scope.

Authorized plan: reproduce failure from committed locked captures before source edits; reflect sky U only; capture full 1920×1080 matching anchors; rerun unit/build/nine browser groups and hashes; independently audit, report and publish draft stacked PR. The follow-up explicitly authorizes this bounded correction under the existing parent plan. Antigravity plan/result participation is not claimed; review remains PENDING.

## Changes

Only production change: `work/kinetic-tour-r3f/src/StudioCanvas.tsx`, five added lines: RepeatWrapping import plus sky `wrapS=RepeatWrapping`, `repeat.x=-1`, `offset.x=1`, comment. This reflects U to 1-U without changing sky bytes, sphere yaw, camera, geometry, material brightness or controls. No runtime dependency change.

New files: this report and `work/kinetic-tour-r3f/tests/sky-parity/` (scripts, README, full captures, command/test/error/a11y/contrast/hash receipts, independent audit and comparison HTML). Exact paths in `git show --stat a025ba1` and the stacked PR diff. Original follow-up brief and its backup were pre-existing untracked inputs, deliberately unstaged and preserved. No protected tracked paths changed. LFS materialization fetched the recorded master, without authoring it.

## RED → GREEN → REFACTOR evidence

Before source edits, ran from repository root:

```powershell
python work/kinetic-tour-r3f/tests/sky-parity/check.py --receipt work/kinetic-tour-r3f/tests/sky-parity/red.json
```

Exit 1, meaningful orientation failure at both anchors. Median sky-only sRGB boxes: Home L (300,110)-(340,140), R (1500,110)-(1540,140); Motion L same, R (1550,200)-(1590,225), exclusive right/bottom. No foreground/text in these boxes. Hue 240° means blue, 300° magenta. Direction = right R/B minus left R/B; require >0.10 in legacy and candidate. Ratios reduce effects of left UI scrim but do not prove exact color parity.

| View | Legacy RGB L / R | Before RGB L / R | After RGB L / R | Direction legacy / before / after |
| --- | --- | --- | --- | --- |
| Home | 27,35,97 / 99,96,205 | 78,68,123 / 37,45,117 | 24,31,67 / 149,122,237 | +.204576 / -.317907 / +.270483 |
| Motion | 25,32,79 / 104,83,142 | 87,65,101 / 34,37,88 | 21,27,55 / 142,94,146 | +.415939 / -.475023 / +.590785 |

After minimal rendering correction:

```powershell
python work/kinetic-tour-r3f/tests/sky-parity/check.py --candidate work/kinetic-tour-r3f/tests/sky-parity --prefix after --receipt work/kinetic-tour-r3f/tests/sky-parity/green.json
```

Exit 0, both orientation assertions pass. Refined evidence tool to avoid deprecated Pillow getdata and distinguish CRLF checkout text from LF Git blobs. No further production refactor needed. Python/Pillow and agent-browser were already installed; no new environment tooling installed.

## Actual verification

- `npm ci` in sibling: exit 0, 45 packages, audit 0 vulnerabilities.
- `npm test` in sibling: exit 0, 8/8, before and after correction.
- `npm run build` in sibling: exit 0, TypeScript + Vite 8.3.5; existing >500 KB lazy chunk warning retained (894.64 KB, gzip 238.68 KB).
- `npm test` in legacy: exit 0, 3/3. Legacy full browser/build/validator were not rerun for this sky-only follow-up; parent receipts remain historical.
- Socket connect to 4182 initially returned Windows 10061 (no listener). Started only this checkout using `npm run preview -- --port 4182`; old ports/processes/sessions untouched.
- `python work/kinetic-tour-r3f/tests/sky-parity/verify.py`: unit/build/browser/sky commands each exit 0; first wrapper exit 1 on provenance because master was an LFS pointer and text used CRLF. Did not mask this failure. `git lfs pull --include=work/kinetic-blender/kinetic-studio-proof-v006.blend` exit 0; `verify.py --hash-only` then exit 0, SOURCE_HASHES_PASS 13. Byte comparisons for all binaries; LF-normalized comparison only for untouched TypeScript.
- Nine browser groups passed with existing agent-browser CLI, isolated session `kinetic-sky-parity-20261028-isolated`, closed afterward. Images/history/keys/skip; actual model/1350ms camera/rapid retarget/wheel/reset/Escape; reduced motion/native drag/stale gesture/focus; mobile image-first/mobile GLB/overflow; model failure/retry; sky failure/retry; accelerated timeout; no WebGL; synthetic context loss. Measured transition settled at 1363ms including scheduling.
- `browser.py` without --suite: exit 0, fresh clean captures/error/console/a11y. Clean errors and console messages are both empty. Negative-suite error receipt retains deliberately aborted sky load.
- Final computed sky comparator: exit 0. Exact commands/exits in tests/sky-parity/commands.json; logs in unit.txt/build.txt/browser.txt/sky.txt. Build log whitespace normalized only.

Home camera: position 0,3.05,15.2; target 0,2.1,-2.3. Motion: -8.4,2.25,5.2; target -8.55,1.55,-1.4. Both exact anchors recorded by live browser.

## Visual evidence and independent audit

[Full three-column comparison](../../work/kinetic-tour-r3f/tests/sky-parity/comparison.html).

| View | Committed PlayCanvas | Committed R3F before | Fresh R3F after |
| --- | --- | --- | --- |
| Home | [reference](../../work/kinetic-tour-r3f/tests/evidence/legacy-home-3d.png) | [before](../../work/kinetic-tour-r3f/tests/evidence/prototype-home-3d.png) | [after](../../work/kinetic-tour-r3f/tests/sky-parity/after-home-3d.png) |
| Motion | [reference](../../work/kinetic-tour-r3f/tests/evidence/legacy-motion-3d.png) | [before](../../work/kinetic-tour-r3f/tests/evidence/prototype-motion-3d.png) | [after](../../work/kinetic-tour-r3f/tests/sky-parity/after-motion-3d.png) |

All six complete images were visually inspected by lead and separate read-only native sky_audit session. Auditor independently recomputed patch values, confirmed sky-only patches, blue-left → violet/magenta-right after, and empty protected-path diff. Receipt: tests/sky-parity/independent-audit.md. Auditor did not run browser/unit/build or claim Antigravity involvement.

Remaining material/sky differences: stronger magenta/saturation and darker/more contrasty geometry than PlayCanvas; cloud/gradient alignment and absolute colors are not pixel-exact. No geometry darkening was introduced by this fix. Separate intentional UI difference: R3F oversized upper-left serif hero and right detail panel versus compact lower-left legacy hero and inline details. Preserved unchanged; no redesign authorized.

## Hotspot contrast

Live computed foreground rgb(243,238,228), opaque background rgb(21,35,36), opacity 1 for all three markers at both anchors. Ancestors observed opacity 1, filter none, blend normal. Existing CSS puts hotspots z2 above the scene pseudo overlay z1. WCAG sRGB linearization and relative luminance gives **13.9939965:1**, exceeding 4.5:1 for text against button fill. Formula and values in contrast.json, computed styles in live-observations.json.

Axe 4.12.1 still reports 0 violations and 1 incomplete color-contrast rule covering 3 markers because of pseudo-element compositing. Keep **MANUAL REVIEW** visible for actual painted/composited visibility and overlap; ratio is proven only for declared opaque text/fill. No blanket accessibility PASS or issue suppression.

## Source provenance

All ten manifest artifacts match expected SHA-256 after LFS materialization; sky exact bytes and parent tour/camera data also verified. Full values in tests/sky-parity/source-hashes.json.

- Blender v006: `8b121564f8895917a9a0f820f95da5d0ef8069ea2715e8312d51f1096e962cfe` (74,025,533 bytes), LFS filter verified.
- Desktop GLB: `6a586e3d2115d226664a042c021f9432672f324b37cb9f29e50b27855a96c913`.
- Mobile GLB: `d0c5fc11b5d7ac0b24523aed651e66d1d8df5aedfa53c639f4b77110911451e9`.
- Sky: `c45d164f9ebcc307feb66f9adcdd19182e1701e8ec2f51e1099cb0aaf7e8bc40`.

## Risks, blockers and next gate

Physical-phone performance/thermals and actual GPU reset **UNVERIFIED**; synthetic loss and desktop mobile emulation do not prove either. No new performance superiority claim. Antigravity review **PENDING**. Accept the bounded orientation correction for draft stacked review; retain PlayCanvas and defer adoption/full visual parity/M3 until owner and Antigravity review.

Local skill bodies actually read: kinetic-studio-collab, test-driven-development and writing-good-tests, soren-learning-loop, router, threejs-textures (guidance targets newer r186; used installed r180 API), agent-browser plus CLI core, soren-universal-deployment plus actual read-only preflight, verification-before-completion, github-outside-sandbox. No callable soren-skills/Open Design tools were exposed; no registrations changed. Requested caveman/chisle skills were absent from local skill roots. Normal scoped escalation review approved writes; no permission bypass.

## Publication receipt

Draft stacked PR: https://github.com/sorensadrgit-art/spline-3d-/pull/5, targeting `feat/kinetic-r3f-pilot-20261028-codex`, linked to PR #4 and issue #1. Branch push and draft creation exit 0. Verified source commit `a025ba11a0560133cade087b63041fb22bc5d077`; report commits follow. A receipt append encountered Windows cp1252 decoding failure; corrected with explicit UTF-8 and repaired document punctuation before final delivery. Rendering source/evidence are unchanged. Final delivery SHA is the PR head and git log. No merge/deployment. Pre-existing untracked brief/backup remain unstaged and preserved.
