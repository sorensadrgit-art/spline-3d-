# M6 mobile projected hotspot repair

RESULT: PASS for the bounded R3F collision and resize repair. Release/adoption remains NO-GO pending owner visual acceptance and physical-device evidence. No merge or deployment.

## Understand / Investigate

Only isolated worktree `C:\ProgramData\SentinelX\workspace\kinetic-m6-mobile-markers-20261028`, branch `fix/kinetic-m6-mobile-hotspots-20261028`. Initial clean HEAD `6a7f4e57bee502e0d762dce5d68036891ac29d8d`; frozen main `44ad922826da34bbcaf7bb83646b24cd694d084c`. Fresh remote main query matched. PR #10 independently confirmed MERGED. Normal fetch materialized missing baseline commit for exact diff; no branch switch or main update.

Full M6 brief, AGENTS and collaboration contract read. Existing M3/M4/M5 browser logic inspected; M6 copies change output location/port/session without weakening inherited assertions. Owner's current request explicitly authorizes the bounded runtime repair. No Antigravity plan response or owner aesthetic approval is inferred.

Initial master was a 133-byte Git LFS pointer. Scoped `git lfs pull --include=work/kinetic-blender/kinetic-studio-proof-v006.blend` materialized 74,025,533bytes. Actual SHA256 `8b121564f8895917a9a0f820f95da5d0ef8069ea2715e8312d51f1096e962cfe` matches. All other manifest binaries matched before edits; final all 10 plus sky match. Historic source folders/other worktrees untouched.

## Rederive / Plan Forge / Plan Acceptance

[Plan Forge](CODEX_M6_PLAN_FORGE.md) was written before runtime edits. Retain authoritative PlayCanvas; repair sibling R3F visibility only. Spline replacement or fabricated projection shifts would change scope/semantics. Stable semantic-order collision rejection keeps true anchors and 44px targets with 4px clearance. Scoped owner execution request supplies repair authorization; Antigravity critique remains PENDING. Rollback is reverting only the M6 feature commit, preserving PlayCanvas.

## CHANGES / RED / GREEN / REFACTOR

- `src/hotspots.ts`: deterministic greedy selection of eligible projected44px rectangles with 4px separation. No coordinate mutation; invalid/ineligible targets cannot suppress valid ones.
- `src/StudioCanvas.tsx`: collect true projected points, apply visibility, transfer disappearing-marker focus to matching semantic detail (mode fallback). Invalidate after viewport-size commits so demand rendering refreshes resize projections. Camera owner,1350ms motion, exact poses, anchors, models, sky UV correction and styling remain unchanged.
- `tests/hotspots.test.ts`: recorded mobile geometry; exact spacing boundary; separated desktop and invalid/ineligible inputs.
- Only M6 documentation and `tests/m6-evidence/` scripts/logs/screenshots otherwise added. No dependency manifest/lock changes or protected-source changes.

Real browser RED: `python -u .../m6-evidence/mobile_markers.py` exited1 on actual390x844 Home overlaps. All targets44x44: shared center `(173,197.359375)`; material `(157.125,239.875)`; blue hour `(173,171.8125)`. Pairs center/material and center/blue-hour overlapped. All centers were independently hit-testable; all semantic details existed.

Unit RED: `node --experimental-strip-types --test .../tests/hotspots.test.ts` reported2assertion failures against pre-collision eligibility behavior: actual `[true,true,true]`, wanted `[true,false,false]`, plus insufficient-gap case. `red-unit.txt` retains actual assertions. GREEN full suite 18/18; behavior-preserving REFACTOR named separation 44+4, full suite 18/18 again.

Browser GREEN: same390x844 Home shared-center rectangle stays `(173,197.359375,44,44)`, center hit true. Material/blue-hour markers hidden, overlap[]; all three semantic detail buttons remain available and keyboard-operable. No fake anchor offsets.

Additional real RED: resize focus wait timed out. `focus-observation.json` showed390px canvas retaining marker x960 from prior1920px viewport, catching up one resize late. Post-size invalidation fixes it. `focus_green.py` checks independent projections after four sequential resizes and corresponding detail2focus; exit 0. Final matrix also verifies resize focus.

## VERIFICATION — actual commands and output

Commands run through approved native escalations where filesystem/network/browser permissions required. Node 24.19.0/npm 12.1.0/agent-browser 0.39.4/Chrome 155; desktop browser emulation only. Local built previews bind127.0.0.1:4192/4193. Ports4177–4191 were not rebound or terminated.

| Command / check | Observed final result |
| --- | --- |
| Both apps `npm ci` | exit 0; zero reported vulnerabilities |
| R3F `npm test` | exit 0,18/18, including final resize source |
| PlayCanvas `npm test` | exit 0,3/3 |
| Both `npm run build` | exit 0; existing >500kB chunk warnings retained |
| `run_check.py browser` | exit 0,15/15; final retarget1363.7ms; first-frame inspected displacement0 |
| `run_check.py matrix` | exit 0,20/20: five zones at320/390/430x844 and1920x1080 |
| `run_check.py focus_green` | exit 0,four sequential resize projections/focus correct |
| `run_check.py legacy_browser_qa` | exit 0,8/8 against protected PlayCanvas build |
| Copied existing GLB validator | exit 0; each14meshes,14materials,9images,0errors/0warnings |
| `run_check.py final_integrity` | exit 0; all 10 manifest binaries+sky match; protected-source diff empty; whitespace clean |
| `run_check.py painted_contrast` | exit 0;8visible markers,painted13.994:1, all hit-testable |
| `run_check.py steady` | exit 0;312real frames,278with visible targets, no overlaps; success-only errors/messages[] |

Matrix asserts true independent projections, label/title identity, >=44px visible targets, center elementFromPoint, >=4px rectangle separation (0.02px CSS rounding tolerance), no horizontal overflow, actual mobile GLB and DPR1, all semantic details via keyboard Enter. All five desktop marker visibility arrays match historical M5:8visible total, no unrelated desktop suppression. Camera/sky/orbit data unchanged. Keyboard0–4/Home/Escape,history,rapid retarget,reset,drag/wheel clamps,reduced motion,late load,network/sky retry,timeout, noWebGL and synthetic context loss pass in the full browser suite.

Axe 4.12.1:11 fresh audits (five desktop 3D, five 390 mobile 3D,one image mode), zero confirmed violations. Each 3D audit has one incomplete contrast rule; image audit has none. Painted marker contrast supplements axe; it does not resolve every scene-text contrast question or certify WCAG compliance. Manual screen reader PENDING.

## VISUAL EVIDENCE

[Before390Home](../../work/kinetic-tour-r3f/tests/m6-evidence/before-mobile-home.png) and [after390Home](../../work/kinetic-tour-r3f/tests/m6-evidence/after-mobile-home.png) retain scene/composition/typography with corrected marker visibility. `320-*.png`,`390-*.png`,`430-*.png`,`1920-*.png` capture all 20zone/viewports. Five desktop 3D/image pairs and real browser rectangles/projections are in the same evidence directory. Reviewer independently viewed before/after and 320engineering. No photoreal/Cycles parity claim.

## Failed attempts and retries

All retained, none counted as final passes: initial browser ERR_ABORTED; verification wrapper cp1252 UnicodeEncodeError after successful legacy tests (rerun PYTHONUTF8=1); R3F npm ci EPERM native-module unlink while own dev preview held it (stop only own PID53676,successful reinstall); first matrix selected already-hidden desktop marker2 (fixed fixture to observed visible marker3); second matrix revealed real stale-size bug; concurrent final browser/matrix CLI timeouts60s/outcome_unknown10060 (doctor offline quick8 pass / 1 warn / 0 fail, no destructive repair; sequential fresh-session runs pass). Final integrity summarizer initially matched its own summary JSON list (TypeError), fixed explicit exclusion and reran successfully. Contrast script reports a Pillow getdata deprecation warning. Existing build chunk warnings remain. No permissions,thresholds,dependencies or global configurations weakened.

## RISKS / BLOCKERS / NEXT GATE

Physical-phone FPS/sustained thermals PENDING; Antigravity design critique PENDING; manual screen-reader and real hardware GPU-reset PENDING. Synthetic context-loss test is not a hardware reset; none attempted. Baked material/lighting limitations and bundle-size warnings remain. Independent Codex review is separate from Antigravity and cannot grant owner visual acceptance.

NEXT GATE: owner reviews draft PR/evidence, obtains physical-phone and Antigravity/visual acceptance before any adoption decision. Keep PlayCanvas authoritative. No merge,deploy,production/domain/account/credential changes authorized or performed.

Skills actually read: kinetic-studio-collab,TDD and writing-good-tests,agent-browser and installedCLIcore,caveman,chisle,soren-learning-loop,router,threejs-scene-setup,soren-universal-deployment plus read-onlypreflight,github-outside-sandbox. SOREN/OpenDesign MCP tools were not exposed; no routing call claimed. Lightswind is not applicable to this bounded bug fix. Learning recall returned no relevant records; no memory/configuration writes.

Independent reviewer receipt: `work/kinetic-tour-r3f/tests/m6-evidence/independent-review.md`. Publication is a feature-branch DRAFT PR linked to issue #1 and merged PR #10; never merge/deploy.

Publication preparation: staged whitespace check found trailing spaces emitted by build/test tools. Review text copies were normalized; raw-command-output.json preserves original strings/digests. Initial git commit failed because the isolated checkout had no author identity; no commit was created by that attempt. Identity resolution uses authenticated GitHub public identity for this commit only, without global or repository configuration changes.

## Publication receipt

Tested source/evidence commit `29c15e086caf08822d3944675f74629d8865863e` pushed only to `fix/kinetic-m6-mobile-hotspots-20261028`. DRAFT PR [#11](https://github.com/sorensadrgit-art/spline-3d-/pull/11) targets main and links issue #1 and merged PR #10. Fresh `gh pr view 11` verified OPEN, isDraft=true, base=main and matching source SHA before this documentation-only receipt. No merge or deployment.
