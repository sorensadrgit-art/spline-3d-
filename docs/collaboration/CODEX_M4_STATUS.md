# M4 result acceptance — 2026-10-28

STAGE: Understand / Investigate / Rederive / Plan Forge / narrow Plan Acceptance / Execute / independent Result Review.
RESULT: bounded investigation and evidence complete; retain R3F runtime without forced source fixes. Adoption remains NO-GO. Antigravity and physical-device acceptance PENDING. No merge/deployment.

BRANCH + SHA: feat/kinetic-r3f-m4-visual-20261028, starting HEAD d7f2e26f542ba2e5c75e7abc64cbe07e3ebd2e97; git fetch --deepen=30 verified ancestry from specified M3 merge c6a1367ac72c88b809fbd5f27a8df75f53d2c46e. Clean isolated checkout at start. Final delivery SHA is the commit containing this report; publication receipt follows separately.

CHANGES: only M4 collaboration documents and work/kinetic-tour-r3f/tests/m4-evidence. No production source, dependency, lockfile, renderer, camera, sky, content or asset changes. Plan Forge written before executing candidate selection. Owner brief explicitly authorizes narrow R3F refinement; no objective defect justified production changes. Potential focus loss on resize was probed and not reproduced. RED/GREEN: NOT APPLICABLE (no demonstrated application defect/no source fix); infrastructure/script failures are not labeled application RED tests.

## Verification — fresh commands and observed output

- npm ci --prefix work/kinetic-tour-r3f: exit0,45 packages,audit0. Legacy equivalent: exit0,21 packages,audit0.
- npm test from R3F: exit0,15/15; npm test legacy: exit0,3/3. npm run build from both: exit0. Exact commands/cwd/exits in tests/m4-evidence/commands.json; full outputs retained.
- node work/kinetic-tour-r3f/tests/m4-evidence/validate-models.mjs: exit0; desktop/mobile14 meshes,14 materials,9 images;0 errors/0 warnings. Outputs confined to M4 evidence.
- Protected hashes:9 delivered binary artifacts and sky match manifest/recorded bytes. Blender master is an unchanged133-byte LFS pointer with correct declared OID8b121564f8895917a9a0f820f95da5d0ef8069ea2715e8312d51f1096e962cfe and size74025533. Actual master binary hash UNVERIFIED; no fetch/materialization or Blender write performed. protected-hashes.json deliberately preserves pointer mismatch rather than claiming10/10.
- Final python tests/m4-evidence/browser.py: exit0,15/15 scenario groups. final-browser-run.txt and browser-checks.json record all results. Exact five cameras/directions checked at1e-10; projected anchors/hit tests/details checked. Normal transition observed1368.3ms with code1350ms. Rapid retarget, drag/wheel/reset, reduced cuts, 0–4/Home/Escape/history, inspected continuity, generation/stale completion, failure/retry/timeout/mobile/synthetic-loss all pass. Inspected first-frame displacement0.0.
- Earlier first run failed waiting for3D load; next run passed10 groups then daemon outcome_unknown/error10060. Both receipts preserved. Final serial pass did not relax app/test thresholds.
- Measurement-script failures: missing local canvas variable; warm same-URL navigation retained prior resource entries; daemon EOF/cleanup timeout. Corrected local measurement scripts and fresh runs retained final records. These do not demonstrate an application defect.

## Five-view visual evidence and alternatives

[Actual four-column comparison](../../work/kinetic-tour-r3f/tests/m4-evidence/comparison.html): fresh matching1920x1080 PlayCanvas/R3F Home, Motion, Clinical, Engineering, Projects; historical M3 before labeled; authoritative Cycles references contextual. Source unchanged, so retained baseline equals candidate; no fabricated before/after improvement. image-samples.json records fixed unobscured scene RGB/luminance/hue patches. No pixel-matching/Cycles-equivalence claim.

Home retains central workstation/all-zone overview; Motion capture rig/calibration/display; Clinical skeleton/prints/desk; Engineering bench/actuator; Projects presentation table. Large serif upper-left hero, right panel, warm walnut/graphite and blue-left/magenta-right exterior preserved. All actual R3F/legacy frames reviewed independently. R3F darker and more saturated than gray-lifted PlayCanvas; baked KHR_materials_unlit export lacks Cycles reflections/foliage/soft light. A preserve direction is selected over B speculative exposure/color tuning; C postprocessing/regeneration rejected for GPU cost and immutable assets. Spline runtime would add conversion/runtime uncertainty. Rollback: discard scoped M4 evidence commit; working PlayCanvas remains authoritative.

## Accessibility

Axe4.12.1:0 violations in all five3D views and image mode. Each3D view retains1 incomplete contrast rule; images0 incomplete. Not blanket certification. All8 visible markers across five locked frames pass hit tests and actual raster foreground/interior samples; opaque RGB21,35,36 and solid numeral RGB243,238,228 give13.994:1 (painted-marker-contrast.json). Hidden markers remain accessible through semantic side-panel controls. Browser focus checks pass after route/Escape; resize probe retained visible focused marker. Emulated390x844 remains image-first/no GLB before opt-in; lighter mobile GLB and DPR1 verified; no horizontal overflow. Manual screen reader UNTESTED.

## Performance and diagnostics

[Full performance report](../../work/kinetic-tour-r3f/tests/m4-evidence/performance-report.md) and performance.json retain8 sequential cold/warm records,1920x1080 and emulated390x844, same HeadlessChrome155/Windows/i9-14900HX machine. OS lists Intel UHD and RTX4070 Laptop; actual active adapter recorded separately. Navigation/resource durations, encoded/transfer bytes, heap snapshots, buffered long tasks and idle rAF distributions retained. Cold desktop GLB12,023,904B/mobile5,972,736B; warm transfer300B revalidation. No source candidate modification. One run/cell, fixed renderer order, OS cache/GC uncontrolled; no causal speed superiority or leak-free claim.

R3F202.37KB initial +894.98KB lazy JS(gzip64.89+238.83). Legacy11.47KB studio +2498.25KB engine. Existing named imports/lazy boundary inspected; no demonstrated unused dependency saving warrants speculative optimization. No GSAP/postprocessing/dependency changes.

Full-suite clean-errors.json contains the deliberately injected sky-load failure and clean-console.json informational Context Lost; filenames are inherited and MUST NOT be interpreted as clean steady-success proof. Separate active-performance-and-steady-diagnostics.json captures new success-only pages and active-camera scheduling; see that receipt for final observations. rAF intervals are NOT GPU frame duration or FPS. Synthetic loss is NOT a real GPU reset.

## Independent review / blockers / next gate

Actual read-only native reviewer /root/m4_audit reviewed source, all five fresh R3F and legacy images, Cycles references, commands and final15/15 browser/a11y receipts. independent-review.md distinguishes review from test execution and corrects diagnostic limitations. No source change justified.

Genuine Antigravity request used installed agy --mode plan --sandbox --print-timeout45s with read-only critique scope and normal permissions. Observed exit0 with timeout/turn-in-progress only, no critique. PENDING, not approval. No permission bypass/global policy changes. See ANTIGRAVITY_M4_HANDOFF.md.

BLOCKERS/UNVERIFIED: owner/Antigravity visual acceptance; physical phone/load/thermals; manual screen reader; hardware GPU timing/reset; full materialized Blender master hash; sustained leak evidence. on-device-instructions.md provides reproducible procedure. No remaining demonstrated runtime defect; no adoption recommendation. NEXT GATE: owner reviews comparisons/draft stacked PR, obtains real external/device acceptance before any proposal to replace PlayCanvas.

Tools/skills actually read: kinetic-studio-collab, soren-learning-loop, agent-browser plus installed CLI core, router, threejs-performance, soren-universal-deployment with read-only Vite/npm preflight, github-outside-sandbox, verification-before-completion. No exposed SOREN/Open Design/Lightswind MCP actions claimed; no React UI implementation selected. Caveman/chisle missing in installed skill roots. Only native independent reviewer was spawned; Antigravity timeout is separately labeled. No other tasks/main/old ports/production changed.

Final diagnostic supplement: separate fresh success-only errors/messages empty for both engines; active WebGL adapter Intel UHD ANGLE/D3D11. Active-camera scheduling legacy median12.1ms/p9524.2ms versus R3F6.1ms/p9512.2ms, no GPU/FPS claim. Fresh Home/Motion sky-direction comparator PASS.

Artifact note: r3f-mobile-3d.png is the actual scrolled detail/navigation viewport after opt-in; prototype-mobile-3d.png from the regression suite shows the upper scene. Captured logs have trailing whitespace/extra EOF blank lines normalized solely for git diff --check. Root .vite cache from an initial owned preview launch is excluded from staging.
