# Kinetic Studio — scene-only entry

This branch changes the **root URL** (`/`) into a fullscreen, auto-starting 3D viewer with no visible HTML website interface, headlines, zone cards, hotspots, menus, or buttons. The guided image/3D tour is preserved at `/tour.html#home`, and the experimental Gaussian pilot remains at `/pilot.html`.

## What the new viewer actually loads

The viewer uses the repository's **existing** baked desktop and mobile delivery assets:

- `public/models/studio-desktop.glb`
- `public/models/studio-mobile.glb`
- `public/models/blue-hour.jpg`
- `public/media/home.webp` as the non-text fallback

These assets are a Blender/PlayCanvas reconstruction, **not an export of the original Spline project**. The original Spline `.splinecode` or published scene URL was not found in this repository. No claim is made that the original Spline scene has been restored, and none of the protected 3D model, Blender, source images, or textures has been modified.

## Controls

- Open `/`: 3D initializes automatically. No "Explore in 3D" button.
- Drag: limited look-around rotation. Wheel: limited camera-distance adjustment.
- Keys `0`–`4`: invisible camera navigation among Home and the four existing zones.
- `Home`: return to the original authored overview camera.
- No visible controls or copy. Screen-reader announcements remain visually hidden.
- The overview image is displayed while loading and as a graceful graphics-error fallback; clicking the fallback image retries.

## Reproducible verification

From `work/kinetic-tour`:

```sh
npm ci
npm test
npm run build
npm run preview -- --port 4195 --strictPort
```

The legacy browser checks now target the preserved guided tour rather than the clean root; override its preview URL when testing on a nonstandard port:

```powershell
$env:KINETIC_TOUR_URL = 'http://127.0.0.1:4195/tour.html#home'
python tests/browser_qa.py
```

Recorded during isolated branch work on AgentZero:

- Unit tests: 14 of 14 PASS (including root-only visual contract and preserved tour).
- Production Vite/TypeScript build: PASS; existing PlayCanvas shared chunk warning remains.
- Existing guided-tour browser QA: 8 of 8 PASS.
- Scene-only desktop 1920×1080: WebGL canvas ready, 1920×1080, zero website-chrome elements, no browser errors.
- Scene-only mobile emulation 390×844: `studio-mobile.glb` ready, canvas exactly viewport size, no scrolling, zero website-chrome elements, no browser errors.
- Scene-only keyboard: the Motion view selected after the model loaded, camera reached [-8.4, 2.25, 5.2].
- Physical-phone performance, true original Spline parity, and production deployment: NOT VERIFIED.

The existing Codespaces URL is a separately running environment. A branch/PR does not automatically update its checked-out source or running preview. No `main` merge or public deployment is authorized by this patch.
