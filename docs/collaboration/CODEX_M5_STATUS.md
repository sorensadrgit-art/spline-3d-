# M5 merged-main release-readiness audit

RESULT: PARTIAL ACCEPTANCE — release/adoption NO-GO. Fresh source, asset, build and functional gates pass. Owner visual approval and physical-device evidence remain pending. Evidence only; no deployment/adoption authorization.

## Understand / Investigate

Work performed only in C:\ProgramData\SentinelX\workspace\kinetic-m5-main-qa-20261028 on feat/kinetic-m5-release-readiness-20261028. Initial HEAD 9ba41ff4a2210e1fa67242ece3cf826c59e512bb is a direct child of remote merged main 16d2a6b20bc5d29ef777bd3bf81dc8e16af9218f. Fresh git ls-remote confirmed main. Normal depth-2 fetch materialized the missing shallow baseline object; git diff shows only the M5 brief differs between those commits. App source/assets therefore match main. Initial tracked state clean. The old desktop clone and M4 worktrees were not touched; the brief's old desktop c3f48b7 remains a historical claim, not a fresh query.

Blender initially was the 133-byte LFS pointer declaring OID 8b121564f8895917a9a0f820f95da5d0ef8069ea2715e8312d51f1096e962cfe and size 74025533. Normal git lfs pull succeeded. Actual materialized master size 74,025,533 bytes and SHA256 match. All ten delivery artifacts plus sky match; negative protection rejects an in-memory byte-flipped mobile GLB without changing any asset. See protected-hashes.json. Protected-folder diff from main is empty.

## Rederive / Plan Forge / Plan Acceptance

Retaining PlayCanvas preserves the authoritative tour. The merged R3F sibling supports isolated comparison and rollback. Spline conversion adds asset/runtime uncertainty without a demonstrated need. Plan artifact: CODEX_M5_PLAN_FORGE.md, written before fetch/LFS/install mutations. The user's complete M5 assignment authorizes evidence execution; no runtime implementation was proposed or needed. No replacement/adoption is inferred from PR #9.

## Execute — verification

Fresh npm ci, npm test and npm run build executed in both app directories; all exit 0. PlayCanvas 3/3 tests; R3F 15/15. Both builds warn about chunks above 500 kB; warnings are retained, not treated as failures. Installs report zero vulnerabilities at execution time. Existing validator logic redirected only its module/asset paths and outputs into M5: desktop/mobile 14 meshes, 14 materials, nine images each, zero errors/warnings. Exact commands, cwd, exit statuses and full install/test/build logs: work/kinetic-tour-r3f/tests/m5-evidence/commands.json and adjacent logs. Source remains unchanged.

Fresh browser command: python -u work/kinetic-tour-r3f/tests/m5-evidence/browser.py, exit 0, 15/15 groups. Unique kinetic-m5-20261028-regression session. Actual local preview listeners bind 127.0.0.1:4190 (R3F) and :4191 (legacy); no public exposure or old listener termination. All five real GLB positions/directions match at 1e-10 tolerance; semantic details, projected anchors/hit tests, keyboard 0–4/Home/Escape, history, rapid retarget, reset, drag/wheel clamps, reduced motion, accelerated 45s timeout, stale completion, network/sky failure/retry, image-first mobile/mobile GLB and synthetic context loss pass. Inspected-pose first-frame displacement 0.0. Passing transition 1379.7ms.

First browser attempt failed the inherited timing assertion: firstDone 119.8ms while the later midpoint was still intermediate. first-browser-failure.json is retained. The helper can mistake initial idle dataset.transition=false for completion before motion starts. The second full run passed unchanged 1200–1550ms thresholds. An additional started-state transition probe is provided; this is an evidence-harness issue, not a demonstrated application bug. No runtime fix or fabricated RED/GREEN claim.

## Accessibility / visual evidence

Fresh 1920×1080 zone-3d captures and five-views.json inspect actual cameras and all semantic detail controls, including details whose projected markers are hidden by UI. Eight visible markers pass hit tests and current painted foreground/background pixel checks. Colors RGB243,238,228 / RGB21,35,36 yield approximately 13.994:1; measured samples and computed styles retained in painted-marker-contrast.json. Axe 4.12.1 reports zero confirmed violations across five 3D views and image mode; each 3D view has an incomplete contrast rule. This is not blanket WCAG certification. Keyboard focus and an error/retry path pass. Manual screen reader UNVERIFIED.

Matched legacy/R3F captures and comparison.html are the owner review artifact. Warm walnut/graphite interior, serif hero/right panel, all zones and blue-left/magenta-right exterior are retained. Baked unlit exports have darker/flat surfaces and faceted/blurred detail; no Cycles pixel parity or owner aesthetic approval is claimed. Mobile captures are desktop emulation at 390×844 only.

## Acceptance matrix

| Gate | Status | Evidence / limit |
| --- | --- | --- |
| Merged-main source and full LFS master | PASS | provenance and byte checks |
| Both installs/unit tests/builds | PASS | 3/3, 15/15, exit 0 builds |
| GLB validation / negative hash protection | PASS | zero validator errors/warnings; tampered copy rejected |
| R3F browser regression | PASS | fresh 15/15; earlier timing failure disclosed |
| Painted markers / keyboard / recovery | PASS | eight visible markers; semantic details; focus/error tests |
| Axe | PASS with limits | zero violations; incomplete 3D contrast disclosed |
| Five-view capture comparison | PASS with limits | ten matched desktop frames reviewed; owner signoff separate |
| Mobile marker separation | FAIL | fresh 390×844 Home marker rectangles overlap; all centers still hit |
| Bounded browser performance/GPU capabilities | PASS with limits | eight sequential records, active rAF and renderer/extension receipts; no GPU duration claim |
| Physical phone / sustained thermals | UNVERIFIED | PENDING; emulation does not qualify |
| Manual screen reader / hardware GPU reset | UNVERIFIED | not performed; no OS reset attempted |
| Antigravity / owner visual signoff | UNVERIFIED | PENDING; paste-ready handoff |
| Release/adoption | FAIL / NO-GO | separate owner authorization required |

## Changes / risks / blockers / next gate

Only M5 documentation and tests/m5-evidence are intended for publication. No runtime, dependency manifests/locks, PlayCanvas, original assets, global settings, production, domain or permission policies changed. Independent read-only Codex review runs separately from Antigravity; its receipt will be included. No objective runtime bug reproduced.

RISKS: baked visual limitations; browser timing/cache/hardware variation; large chunks; no sustained-device, screen-reader or real graphics-reset evidence. BLOCKERS: physical-device access and owner/Antigravity acceptance. NEXT GATE: owner reviews five-view comparison, tests a physical smartphone, supplies visual signoff, and optionally obtains genuine desktop Antigravity critique. See ANTIGRAVITY_M5_HANDOFF.md. Keep PlayCanvas authoritative.

Skills actually read: kinetic-studio-collab, soren-learning-loop, caveman, chisle, agent-browser and installed CLI core, soren-universal-deployment (read-only preflight), router, threejs-performance, github-outside-sandbox. SOREN router/Open Design MCP tools were not exposed and no such calls are claimed. No Lightswind route applies to evidence-only QA.

## Result Acceptance — final fresh evidence

Independent native Codex reviewer /root/m5_audit inspected source, fresh receipts, ten desktop GLB frames and two mobile screenshots. It verified source/asset/build/functional gates, retained baked visual limitations and identified mobile Home marker overlap. A fresh mobile-marker-probe.json confirms overlapping rectangles at 390×844; all three centers remain clickable and all semantic details exist. This is a FAIL for marker separation, not a failure of the narrower image-first/model-selection group. No runtime changes were made in this evidence-only audit. Next sidecar implementation gate should address mobile projected-marker separation with this reproduction, then rerun acceptance before adoption. Owner aesthetic approval remains separate.

Fresh copied legacy browser regression also passed 8/8; receipts stay outside legacy paths. Focus resize probe passed. Supplemental started-state transition observed 1480ms within unchanged bounds. Its success-only errors/messages are empty. Inherited clean-errors.json contains the deliberately induced sky failure and clean-console.json includes synthetic-loss information; these filenames do not mean clean steady state. Separate active-performance-and-steady-diagnostics.json reports empty success-only errors/messages for both engines.

Performance: Windows/i9-14900HX, HeadlessChrome155, agent-browser0.39.4, active Intel UHD ANGLE/D3D11 (OS inventory also lists RTX4070; not evidence it rendered the page). Eight sequential browser cold/warm records cover desktop1920×1080 and emulated390×844, one sample per cell. Active camera rAF medians: legacy18.1ms/p9530.2ms; R3F12.1ms/p9518.3ms. These are scheduling intervals, not GPU frame duration/FPS or causal renderer superiority. OS cache, GC, fixed renderer order and thermal conditions are uncontrolled. Legacy hidden canvas makes the helper's initial.imageFirst=false ambiguous; it does not mean legacy automatically enters3D. Raw resource entries [{}] in initial.modelBeforeOptIn are not a count/identity proof; use the named resources array and R3F dedicated mobile assertion. No leak-free or sustained-device claim. GPU disjoint timer extension is supported but no timer query was measured; no OS GPU reset.

Additional infrastructure observation: the first mobile-marker probe launch received agent-browser outcome_unknown/os10060 at viewport setup; a normal retry succeeded. No permissions, browser policy, installed tools or test thresholds changed. No Antigravity response was requested or claimed. Physical phone, manual screen reader and hardware reset remain UNVERIFIED.
