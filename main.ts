/**
 * main.ts — entry point for "The World in One Day — Monday 23 November 2026".
 *
 * Copies the finished poster (entry.png, sitting next to this file)
 * into the output directory named by MAKEFUN_OUTPUT_DIR (default
 * /output), creating the directory when needed, and reports how many
 * bytes were written. The poster itself is drawn by poster.py with
 * Pillow; this entry point only ships the finished PNG.
 *
 * Standard library only, no network access. Running it twice writes
 * byte-identical output: it is a plain file copy.
 */
import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

if (!existsSync(source)) {
  console.error(`entry.png not found next to main.ts (${here})`);
  process.exit(1);
}

const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output");
mkdirSync(outDir, { recursive: true });

const target = join(outDir, "entry.png");
copyFileSync(source, target);
const bytes = statSync(target).size;
console.log(`wrote ${target} (${bytes} bytes)`);
