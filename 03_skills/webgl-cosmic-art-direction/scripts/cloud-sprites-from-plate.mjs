// @ts-check
/**
 * cloud-sprites-from-plate.mjs: cuts drifting cloud sprites from a painted plate's OWN clouds
 * (see the section "Preserve texture and control movement" in references/PLATE_STYLE_SPEC.md).
 * A development tool, not part of a site build: plates usually live outside the repo, so commit
 * the sprites together with the clouds.json provenance this writes.
 *
 * For each crop: greyscale, a median filter that removes the painted stars (they must never drift),
 * a level map from the plate's own ground to its brightest cloud, a soft elliptical feather, and
 * that luminance becomes the ALPHA of a flat fill colour. CSS shows the result at low opacity on a
 * light strip, so the sprite carries the shape and the page carries the tint.
 *
 * Needs Node 18+ and `npm install sharp` in your project. Pick crops with wide, star-free cloud
 * structure in your own plates, then pass one --crop per sprite:
 *
 *   node cloud-sprites-from-plate.mjs --plates-dir ~/path/to/plates --out src/assets/clouds \
 *     --fill 808080 --crop a:plate-a.jpg:100:100:640:160 --crop b:plate-b.jpg:200:400:640:160
 *
 * --crop     id:file:left:top:width:height (repeatable; required). Pixels, in the plate's own size.
 * --plates-dir  folder that holds the plate images (default: the current folder).
 * --out      output folder (default: src/assets/clouds).
 * --fill     fill colour as 6 hex digits, no '#' (default: 808080, a neutral grey; use your own token).
 * (Node does not expand '~' itself; your shell does, when the path is unquoted as above.)
 * Writes OUT/cloud-<id>.webp + OUT/clouds.json.
 */
import { writeFileSync, mkdirSync, statSync } from 'node:fs';
import { resolve, join } from 'node:path';

const USAGE = 'usage: node cloud-sprites-from-plate.mjs --crop id:file:left:top:width:height [--crop ...] [--plates-dir DIR] [--out DIR] [--fill RRGGBB]';

/** @param {string[]} argv */
function parseArgs(argv) {
  const opts = { platesDir: '.', out: 'src/assets/clouds', fill: '808080', crops: /** @type {string[]} */ ([]) };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    const next = () => {
      const v = argv[++i];
      if (v === undefined) throw new Error(`${a} needs a value`);
      return v;
    };
    if (a === '--crop') opts.crops.push(next());
    else if (a === '--plates-dir') opts.platesDir = next();
    else if (a === '--out') opts.out = next();
    else if (a === '--fill') opts.fill = next();
    else if (a === '--help' || a === '-h') { console.log(USAGE); process.exit(0); }
    else throw new Error(`unknown argument: ${a}`);
  }
  return opts;
}

/** @param {string} spec */
function parseCrop(spec) {
  const parts = spec.split(':');
  if (parts.length !== 6) throw new Error(`--crop must be id:file:left:top:width:height, got "${spec}"`);
  const [id, plate, ...nums] = parts;
  const [left, top, width, height] = nums.map((n) => Number.parseInt(n, 10));
  if (!/^[A-Za-z0-9_-]+$/.test(id)) throw new Error(`crop id must be letters, digits, '-' or '_': "${id}"`);
  if ([left, top, width, height].some((n) => !Number.isInteger(n) || n < 0) || width < 2 || height < 2) {
    throw new Error(`crop numbers must be whole pixels (width and height at least 2): "${spec}"`);
  }
  return { id, plate, left, top, width, height };
}

/** @param {string} hex */
function parseFill(hex) {
  if (!/^[0-9A-Fa-f]{6}$/.test(hex)) throw new Error(`--fill must be 6 hex digits without '#', got "${hex}"`);
  return [0, 2, 4].map((k) => Number.parseInt(hex.slice(k, k + 2), 16));
}

let opts;
let crops;
let FILL;
try {
  opts = parseArgs(process.argv.slice(2));
  if (opts.crops.length === 0) throw new Error('give at least one --crop');
  crops = opts.crops.map(parseCrop);
  FILL = parseFill(opts.fill);
} catch (err) {
  console.error(`${err instanceof Error ? err.message : err}\n${USAGE}`);
  process.exit(2);
}

const { default: sharp } = await import('sharp');
const PLATES = resolve(opts.platesDir);
const OUT = resolve(opts.out);
mkdirSync(OUT, { recursive: true });

/** @param {number} e0 @param {number} e1 @param {number} x */
const smooth = (e0, e1, x) => {
  const t = Math.min(1, Math.max(0, (x - e0) / (e1 - e0)));
  return t * t * (3 - 2 * t);
};

const manifest = [];
for (const c of crops) {
  const src = join(PLATES, c.plate);
  const { data, info } = await sharp(src)
    .extract({ left: c.left, top: c.top, width: c.width, height: c.height })
    .greyscale()
    .median(13)
    .blur(4)
    .raw()
    .toBuffer({ resolveWithObject: true });
  const n = info.width * info.height;
  const sorted = Array.from(data).sort((p, q) => p - q);
  const lo = sorted[Math.floor(n * 0.35)];
  const hi = sorted[Math.floor(n * 0.995)];
  const rgba = Buffer.alloc(n * 4);
  for (let y = 0; y < info.height; y++) {
    for (let x = 0; x < info.width; x++) {
      const i = y * info.width + x;
      const level = Math.min(1, Math.max(0, (data[i] - lo) / Math.max(1, hi - lo))) ** 0.85;
      const dx = (x / (info.width - 1)) * 2 - 1;
      const dy = (y / (info.height - 1)) * 2 - 1;
      const feather = 1 - smooth(0.55, 1, Math.hypot(dx, dy * 1.05));
      rgba[i * 4] = FILL[0];
      rgba[i * 4 + 1] = FILL[1];
      rgba[i * 4 + 2] = FILL[2];
      rgba[i * 4 + 3] = Math.round(255 * level * feather);
    }
  }
  const file = join(OUT, `cloud-${c.id}.webp`);
  await sharp(rgba, { raw: { width: info.width, height: info.height, channels: 4 } })
    .webp({ quality: 80, alphaQuality: 95, effort: 6 })
    .toFile(file);
  manifest.push({ ...c, file: `cloud-${c.id}.webp`, bytes: statSync(file).size, level: { lo, hi } });
}
writeFileSync(join(OUT, 'clouds.json'), `${JSON.stringify({ fill: opts.fill, note: 'derived by cloud-sprites-from-plate.mjs; regenerate when the plates change', sprites: manifest }, null, 1)}\n`);
console.error(manifest.map((m) => `[clouds] ${m.file} ${m.width}x${m.height} ${m.bytes} B (level ${m.level.lo}-${m.level.hi})`).join('\n'));
