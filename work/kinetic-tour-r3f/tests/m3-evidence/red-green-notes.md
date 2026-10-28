# M3 RED / GREEN / REFACTOR and failure log

Before implementation: real AppShell was transpiled with the pinned TypeScript dependency and server-rendered for each route. Initial test harness missed the React JSX import (ReferenceError); corrected the harness before counting RED. Genuine RED: 5 failed / 9 passed; Home/Motion failed pending-label check, Clinical/Engineering/Projects failed enabled-3D check. `red.txt` preserves this result. Removing the UI eligibility restriction and pending labels produced 14/14 GREEN (`green.txt`).

Independent review found orbital discontinuity. New real CameraMotion regression failed 1 / 15 with actual [0,3.05,15.2] versus displayed inspected position; `orbit-red.txt`. Director now passes the last painted camera position/target before clearing orbit; 15/15 GREEN, plus live first-frame displacement check. This retains one animation owner.

Browser focus RED showed BODY after focused details then key4 (`focus-red.json`). Added focus restoration to selected nav or mode on removed controls; live GREEN records projects nav and #mode. Reviewer confirmed source logic.

Browser hotspot RED (`hotspot-red.json`) proved visible Home material-language marker hit false; Projects shared seating also covered by nav. Batched UI-rectangle reads now hide overlapping 44px markers without changing anchor projections. Every visible desktop marker must pass elementFromPoint; semantic side panel still exposes all details. Conservative hiding can leave only one projected marker in some zones.

One final-suite attempt failed the legacy reused 1550ms camera sample assertion with only boolean False, before timing was persisted. No failed assertion was relaxed. Diagnostic unchanged movement run reached the exact endpoint and ended at 1372.6ms; per-frame data in timing-investigation.json. Added timing receipt before the existing assertions in sibling browser_qa.py. Subsequent final command receipts state the actual final outcome. This earlier failure remains an acknowledged scheduling/flakiness limitation; it was not proven to be a rendering defect.

Other harness corrections: read the actual mounted GLB's R3F store through React fiber, rather than nonexistent canvas.__r3f; legacy pose comparisons allow 1e-10 numerical tolerance for 5.199999999999999 versus 5.2 (R3F authored dataset endpoints still exact strings). An exploratory browser invocation used the default small viewport; rerun at the required 1920x1080 before counting hotspot RED. A PowerShell nested-quote diagnostic failed to parse; replaced with a literal Python heredoc. No production behavior changed for these harness errors.

Refactor: removed obsolete eligibility state/branching instead of adding zone-specific renderer paths. No new runtime/test libraries or assets. No camera, geometry, sky byte or lighting changes. All final claims are tied to final-commands.json, fresh screenshots and hashes, rather than historical or intermediate receipts.
