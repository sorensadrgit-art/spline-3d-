# M5 bounded browser measurement

Eight sequential measurements in performance.json: both engines, desktop1920×1080/emulated390×844, cold-browser/warm-browser. Exact resources, navigation timings, heap samples and rAF distributions retained. Same Windows host/i9-14900HX, HeadlessChrome155, active Intel UHD ANGLE/D3D11. Node24.19/npm12.1, agent-browser0.39.4. Local loopback4190/4191 only.

active-performance-and-steady-diagnostics.json records active-camera rAF scheduling medians18.1ms legacy and12.1ms R3F, p9530.2ms/18.3ms. This is not GPU render duration/FPS. GPU extension/renderer details are in browser-capabilities-and-timeline.json; timer support is true, measurement false. No OS/driver reset. Empty success-only console/errors for both engines.

One sample/cell, fixed engine order, uncontrolled OS/filesystem cache, GC, background/thermal state. No causal speed superiority, sustained phone performance or leak-free conclusion. Legacy keeps a hidden canvas; initial.imageFirst=false in this helper is not auto3D. Its initial raw resource objects serialize as [{}]; use named resource arrays. Dedicated R3F mobile regression verifies no GLB before opt-in and the lower-detail model after opt-in.

Both builds warn about chunks above500kB. R3F initial JS202.37kB plus lazy894.98kB; legacy studio11.47kB plus engine2498.25kB (uncompressed). No source optimization or dependency change was justified by this audit. Physical phone remains PENDING.
