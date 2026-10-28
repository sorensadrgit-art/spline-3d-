# Sky parity follow-up

Port 4182 only; never use/stop 4177, 4180 or 4181. Start the built sibling with `npm run preview -- --port 4182` from its root. Existing Python/Pillow and agent-browser required; no new runtime dependencies.

From checkout root:

```powershell
python work/kinetic-tour-r3f/tests/sky-parity/check.py --receipt work/kinetic-tour-r3f/tests/sky-parity/red.json
# Expected exit 1: compares locked parent before captures, deliberately reproduces defect.
python work/kinetic-tour-r3f/tests/sky-parity/verify.py
# Expected exit 0: unit/build/nine-group browser/live sky/hashes.
python work/kinetic-tour-r3f/tests/sky-parity/browser.py
# Optional clean capture without injected-failure logs; same isolated session closed on exit.
```

`comparison.html` preserves full reference/before/after captures. `red.json` was created before source edits; `green.json` is fresh live evidence. `commands.json` contains actual unit/build/browser/sky command exits. `suite-*` logs retain expected injected sky failure; `clean-*` is a separate clean browser run. `verify.py --hash-only` reruns immutable provenance checks without repeating successful functional tests.

Sky-only boxes (exclusive right/bottom) are Home L (300,110)-(340,140), R (1500,110)-(1540,140); Motion L same, R (1550,200)-(1590,225). Median sRGB pixels, hue 240 blue/300 magenta. Direction is right R/B minus left R/B; require >.10 in reference and candidate. The wrong U orientation makes the score negative at both locked anchors. Left UI scrim affects exact RGB, so no pixel-perfect or exact hue parity claim. Tests do not crop the delivered comparisons. Existing source captures remain unchanged.
