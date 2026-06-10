// Generates static social/share images from the MistLock logos:
// - public/og/default-og.png (1200x630, Open Graph default image)
// - public/apple-touch-icon.png (180x180, raster fallback of favicon.svg)
// Run manually with `node scripts/gen-og.js` and commit the PNGs.
import { readFileSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import sharp from 'sharp';

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const toDataUri = (file) =>
  `data:image/svg+xml;base64,${readFileSync(path.join(root, file)).toString('base64')}`;

const logoUri = toDataUri('src/assets/mistlock.svg');
const faviconUri = toDataUri('public/favicon.svg');

// Background matches the landing dark theme (--sl-color-black: hsl(224, 10%, 10%))
const ogSvg = `
<svg width="1200" height="630" xmlns="http://www.w3.org/2000/svg">
  <rect width="1200" height="630" fill="#17181c"/>
  <image href="${logoUri}" x="380" y="40" width="440" height="288"/>
  <text x="600" y="420" text-anchor="middle" font-family="Ubuntu, sans-serif"
        font-weight="bold" font-size="84" fill="#ffffff">MistLock</text>
  <text x="600" y="490" text-anchor="middle" font-family="Ubuntu, sans-serif"
        font-size="34" fill="#bf99f2">Catalog of Cloud dev environments</text>
  <text x="600" y="545" text-anchor="middle" font-family="Ubuntu, sans-serif"
        font-size="34" fill="#bf99f2">Free · Local-first · No accounts</text>
</svg>`;

// favicon.svg viewBox is 85x151 (tall): fit height with padding, center horizontally
const iconSvg = `
<svg width="180" height="180" xmlns="http://www.w3.org/2000/svg">
  <rect width="180" height="180" fill="#17181c"/>
  <image href="${faviconUri}" x="51" y="20" width="78" height="140"/>
</svg>`;

mkdirSync(path.join(root, 'public/og'), { recursive: true });
await sharp(Buffer.from(ogSvg)).png().toFile(path.join(root, 'public/og/default-og.png'));
await sharp(Buffer.from(iconSvg)).png().toFile(path.join(root, 'public/apple-touch-icon.png'));
console.log('Generated public/og/default-og.png and public/apple-touch-icon.png');
