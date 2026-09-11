// Builds photos.json from whatever is in images/.
// Filenames drive the captions, so bulk-dropping files is enough:
//   images/dinners/2026-09-06-cacio-e-pepe.jpg   -> "Cacio e pepe", 6 Sep 2026
//   images/design/2026-ferment--Identity.jpg     -> "Ferment", 2026, Identity
// Anything in captions.json overrides the filename-derived text.
import { readdirSync, readFileSync, writeFileSync, existsSync } from "node:fs";
import { join } from "node:path";

const EXT = /\.(jpe?g|png|webp|avif|gif)$/i;
const titleCase = s => s.replace(/[-_]+/g, " ").trim().replace(/^./, c => c.toUpperCase());

const overrides = existsSync("captions.json")
  ? JSON.parse(readFileSync("captions.json", "utf8"))
  : {};

const list = dir => existsSync(dir)
  ? readdirSync(dir).filter(f => EXT.test(f) && !f.startsWith(".")).sort()
  : [];

const dinners = list("images/dinners").map(file => {
  const src = `images/dinners/${file}`;
  const base = file.replace(EXT, "");
  const m = base.match(/^(\d{4}-\d{2}-\d{2})[-_]?(.*)$/);
  return {
    src,
    date: m ? m[1] : "",
    title: titleCase(m ? m[2] : base) || "Untitled",
    note: "",
    ...(overrides[src] || {}),
  };
}).sort((a, b) => (b.date || "").localeCompare(a.date || ""));

const design = list("images/design").map(file => {
  const src = `images/design/${file}`;
  const base = file.replace(EXT, "");
  const [namePart, kindPart] = base.split("--");
  const m = namePart.match(/^(\d{4})[-_]?(.*)$/);
  return {
    src,
    year: m ? m[1] : "",
    title: titleCase(m ? m[2] : namePart) || "Untitled",
    kind: kindPart ? titleCase(kindPart) : "",
    note: "",
    ...(overrides[src] || {}),
  };
}).sort((a, b) => (b.year || "").localeCompare(a.year || ""));

writeFileSync("photos.json", JSON.stringify({ dinners, design }, null, 2) + "\n");
console.log(`photos.json: ${dinners.length} dinners, ${design.length} projects`);
