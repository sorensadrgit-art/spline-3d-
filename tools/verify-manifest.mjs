// Verifies the delivered binaries against work/kinetic-studio-delivery.json.
//
// The manifest is the repository's record of what was actually shipped. Until
// now nothing re-checked it after publication, so a regenerated GLB could drift
// silently. This script is read-only: it never writes, rewrites or repacks an
// artifact.
//
// Behaviour:
//   ok       - file present, byte count and SHA-256 match the manifest
//   LFS      - file is a Git LFS pointer (run `git lfs pull` to verify it)
//   MISSING  - manifest entry has no file in this checkout
//   FAIL     - file present but differs from the manifest
//
// Exit code is non-zero when anything reports MISSING or FAIL. A clone that has
// not pulled LFS still passes, because unverifiable is reported as unverifiable
// rather than as success.

import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const manifestPath = join(root, "work", "kinetic-studio-delivery.json");
const LFS_POINTER = "version https://git-lfs.github.com/spec/";

const manifest = JSON.parse(await readFile(manifestPath, "utf8"));
const artifacts = Object.entries(manifest.artifacts ?? {});

if (artifacts.length === 0) {
  console.error("verify-manifest: no artifacts listed in " + manifestPath);
  process.exit(1);
}

const rows = [];
let verified = 0;
let pointers = 0;
let problems = 0;

for (const [key, expected] of artifacts) {
  const relative = key.split("\\").join("/");
  let bytes;
  try {
    bytes = await readFile(join(root, "work", relative));
  } catch {
    problems++;
    rows.push(["MISSING", relative, "no such file in this checkout"]);
    continue;
  }

  if (bytes.subarray(0, LFS_POINTER.length).toString("utf8") === LFS_POINTER) {
    pointers++;
    rows.push(["LFS", relative, "pointer only - git lfs pull to verify"]);
    continue;
  }

  const sha256 = createHash("sha256").update(bytes).digest("hex");
  const sizeMatches = bytes.byteLength === expected.bytes;
  const hashMatches = sha256 === expected.sha256;

  if (sizeMatches && hashMatches) {
    verified++;
    rows.push(["ok", relative, `${bytes.byteLength} bytes`]);
    continue;
  }

  problems++;
  rows.push([
    "FAIL",
    relative,
    `${bytes.byteLength} bytes (expected ${expected.bytes}), sha256 ${sha256}`,
  ]);
}

const width = Math.max(...rows.map(([status]) => status.length));
for (const [status, relative, detail] of rows) {
  console.log(`${status.padEnd(width)}  ${relative}\n${" ".repeat(width)}  ${detail}`);
}

console.log(
  `\n${verified} verified, ${pointers} LFS pointer(s), ${problems} problem(s) of ${artifacts.length} manifest entries.`,
);

if (problems > 0) {
  console.error("verify-manifest: delivered artifact drift detected.");
  process.exit(1);
}
