// Audita quais fontes de plataforma realmente renderizam cada elemento-folha (CDP). Sinaliza fallbacks inesperados.
import path from 'path'; import { createRequire } from 'module'; import { fileURLToPath } from 'url';
const require = createRequire(import.meta.url); const { chromium } = require('playwright');
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const browser = await chromium.launch(); const page = await browser.newPage();
await page.emulateMedia({ media: 'print' });
await page.goto('file://' + path.join(root, 'build/book.html'), { waitUntil: 'load' });
await page.evaluate(async () => {
  await document.fonts.ready;
  // marca elementos-folha (sem filhos-elemento) que contêm texto
  for (const el of document.querySelectorAll('.page *')) {
    if (el.children.length === 0 && el.textContent.trim().length) el.setAttribute('data-leaf', '1');
  }
});
const cdp = await page.context().newCDPSession(page);
await cdp.send('DOM.enable'); await cdp.send('CSS.enable');
const { root: doc } = await cdp.send('DOM.getDocument', { depth: -1 });
const { nodeIds } = await cdp.send('DOM.querySelectorAll', { nodeId: doc.nodeId, selector: '[data-leaf]' });
const seen = new Map(); let nLeaves = 0;
for (const id of nodeIds) {
  let fonts; try { ({ fonts } = await cdp.send('CSS.getPlatformFontsForNode', { nodeId: id })); } catch { continue; }
  nLeaves++;
  for (const f of fonts) {
    if (/^(Source Serif|Source Sans|KaTeX_)/i.test(f.familyName)) continue;
    const { outerHTML } = await cdp.send('DOM.getOuterHTML', { nodeId: id });
    const pg = await page.evaluate((nid) => null, id).catch(() => null);
    const { object } = await cdp.send('DOM.resolveNode', { nodeId: id });
    const where = await cdp.send('Runtime.callFunctionOn', { objectId: object.objectId, returnByValue: true, functionDeclaration: "function(){ const p=this.closest('.page'); const par=this.parentElement; return (p?p.id:'?')+' < '+(par?par.className:'')+' < '+(par&&par.parentElement?par.parentElement.className.slice(0,30):''); }" });
    const txt = outerHTML.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim() + ' @' + where.result.value;
    const key = f.familyName + ' | ' + f.postScriptName;
    if (!seen.has(key)) seen.set(key, { glyphs: 0, ex: [] });
    const r = seen.get(key); r.glyphs += f.glyphCount;
    if (r.ex.length < 6) r.ex.push(txt.slice(0, 70));
  }
}
console.log('elementos-folha auditados:', nLeaves);
if (!seen.size) console.log('OK: somente Source Serif/Sans e KaTeX em uso.');
for (const [k, v] of seen) console.log('FALLBACK:', k, '| glifos:', v.glyphs, '\n   ex:', v.ex.join(' ¦ '));
await browser.close();
