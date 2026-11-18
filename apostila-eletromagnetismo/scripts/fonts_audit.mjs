// Audita quais fontes de plataforma realmente renderizam cada elemento (CDP). Sinaliza fallbacks inesperados.
import path from 'path'; import { createRequire } from 'module'; import { fileURLToPath } from 'url';
const require = createRequire(import.meta.url); const { chromium } = require('playwright');
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const browser = await chromium.launch(); const page = await browser.newPage();
await page.emulateMedia({ media: 'print' });
await page.goto('file://' + path.join(root, 'build/book.html'), { waitUntil: 'load' });
await page.evaluate(async () => { await document.fonts.ready; });
const cdp = await page.context().newCDPSession(page);
await cdp.send('DOM.enable'); await cdp.send('CSS.enable');
const { root: doc } = await cdp.send('DOM.getDocument', { depth: -1 });
const { nodeIds } = await cdp.send('DOM.querySelectorAll', { nodeId: doc.nodeId, selector: '.page *' });
const seen = new Map();
for (const id of nodeIds) {
  let fonts; try { ({ fonts } = await cdp.send('CSS.getPlatformFontsForNode', { nodeId: id })); } catch { continue; }
  for (const f of fonts) {
    if (/^(Source Serif|Source Sans|KaTeX_)/i.test(f.familyName)) continue;
    const { outerHTML } = await cdp.send('DOM.getOuterHTML', { nodeId: id });
    const key = f.familyName + ' | ' + f.postScriptName;
    if (!seen.has(key)) seen.set(key, { glyphs: 0, ex: outerHTML.slice(0, 160).replace(/\s+/g, ' ') });
    seen.get(key).glyphs += f.glyphCount;
  }
}
if (!seen.size) console.log('OK: somente Source Serif/Sans e KaTeX em uso.');
for (const [k, v] of seen) console.log('FALLBACK:', k, '| glifos:', v.glyphs, '\n   ex:', v.ex);
await browser.close();
