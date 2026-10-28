# M4 performance: measured scope

Hardware observed: Intel Core i9-14900HX; Windows reports RTX4070 Laptop and Intel UHD adapters. Adapter listing does not identify active WebGL adapter. Browser HeadlessChrome155, DPR1. Local loopback preview, same machine/browser installation, sequential fixed legacy-first order.

One browser-cache cold and warm navigation per renderer/viewport. OS/filesystem caches uncontrolled. Warm resources revalidated (300-byte transfer entries); cache status must be read per resource. No source candidate change selected.

|Runtime|Viewport|Cache|Navigation DCL ms|Idle rAF median/p95 ms|Heap before/after bytes|Long tasks|
|---|---|---|---:|---|---|---:|
|legacy|desktop|cold-browser|91.5|12.10/24.30|36936290/37231097|2|
|legacy|desktop|warm-browser|243.0|6.10/12.10|36610997/36011487|1|
|r3f|desktop|cold-browser|298.2|6.10/12.10|31067199/31160795|1|
|r3f|desktop|warm-browser|43.2|6.10/12.10|43748590/18264683|1|
|legacy|emulated-mobile|cold-browser|188.8|6.10/24.30|25165237/23076160|1|
|legacy|emulated-mobile|warm-browser|41.1|6.10/12.10|36392029/36829726|0|
|r3f|emulated-mobile|cold-browser|367.3|6.10/6.20|25022906/24235117|1|
|r3f|emulated-mobile|warm-browser|42.8|6.10/12.10|35859726/30090677|1|

Intervals above are idle scheduling, not GPU render times, active camera frame cost or FPS. No speed superiority conclusion. Heap snapshots depend on GC and do not prove absence of leaks. Long-task observer uses buffered navigation entries and records start/duration, not attribution.

Desktop GLB 12,023,904 bytes; mobile 5,972,736 bytes. No model request before image-mode opt-in in measured entries. R3F initial JS202.37KB + lazy894.98KB (gzip64.89+238.83); legacy studio11.47KB + engine2498.25KB. Different lazy-loading policies prevent naive byte-to-runtime comparisons.

Bundle diagnosis: existing direct named Three imports, explicit GLTFLoader addon and lazy StudioCanvas preserve renderer/loader dependency boundary. Initial shell excludes lazy renderer; renderer necessarily includes Three/R3F and GLTF parsing. No demonstrated unused-import or duplicate-package saving justifies dependency changes. No postprocessing/GSAP added.

Physical phone, thermals, manual screen reader, hardware GPU timing/reset and sustained leak test UNVERIFIED. See on-device-instructions.md.

Separate active camera probe: legacy median12.1ms/p9524.2ms/314 samples; R3F median6.1ms/p9512.2ms/523 samples over3900ms with650ms retargets. Scheduling intervals only, not GPU duration/FPS. Both actual WebGL adapters Intel UHD ANGLE/D3D11. Separate fresh steady-success errors/messages arrays empty after all-five navigation. Legacy daemon close timed out after saving valid measurement; R3F-only continuation completed. See active-performance-and-steady-diagnostics.json.
