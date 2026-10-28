# Execution failures and corrections — observed in this run

- First state test command exited 1 because src/state.ts did not exist. Initial implementation then produced 5/7 passing, with two exact endpoint assertions failing on 5.199999999999999 vs 5.2. Endpoint snapping fixed those failures; suite passed 7/7.
- Disposal test was executed before resources.ts existed (exit 1). Implementation using real Three resource dispose events passed; complete suite now 8/8.
- UI harness was added after initial UI implementation. It first failed because opening the same URL retained SPA mode, then because an offscreen skip link was clicked before focus. Actual reload and keyboard activation corrected harness setup.
- A real browser run failed because an effectful Canvas fallback unconditionally selected images even with WebGL support. Installed Fiber source showed fallback content mounts inside canvas. Explicit capability detection fixed the behavior. No-WebGL test now passes.
- Independent review identified skip-link routing, cached GLB retry, stale drag, hotspot focus and resource cleanup gaps. Real browser regressions were added and passed after fixes. Model loading was replaced with abortable fetch/parse and late-result disposal.
- Network interception initial command 'route' was rejected as unknown. Version-matched help showed 'network route'. Correct command reproduced failed sky cache retry after unroute. Lazy cache clear fixed this in the final ninth browser scenario.
- Initial compare script matched a hidden legacy poster via [data-zone=home]. Scoping to nav fixed the harness.
- Antigravity read-only CLI request returned only '[agy] print timeout after 45s with turn in progress; returning partial output' and exit 0. No collaborator response or acceptance was received.
- A first broad formatted hash output was unreadable; a later explicit hash showed an LFS pointer. This was corrected publicly, LFS materialized, and actual master plus all ten delivery artifacts verified.

No initial UI test-first claim, controlled physical-phone claim, visual-parity approval or Antigravity approval is made.
