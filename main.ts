import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// "THE WORLD - ONE DAY": a broadsheet front page summing up the world news
// of Tuesday 24 November 2026. The image is drawn at build time by gen.py
// (PIL) and shipped as entry.png; this program only copies it to the output
// directory. Node stdlib only, no network, no other files read.
const FILE_NAME = "entry.png";

function main(): void {
  const scriptDir = dirname(fileURLToPath(import.meta.url));
  const source = join(scriptDir, FILE_NAME);
  if (!existsSync(source)) {
    throw new Error(`${FILE_NAME} not found next to main.ts: ${source}`);
  }
  const outDir =
    process.env.MAKEFUN_OUTPUT_DIR || process.argv[2] || "/output";
  mkdirSync(outDir, { recursive: true });
  copyFileSync(source, join(outDir, FILE_NAME));
}

main();
