// Copia fontes (Source Serif 4 / Source Sans 3) e KaTeX de node_modules para assets/ (projeto autocontido).
import fs from 'fs'; import path from 'path';
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const nm = (p) => path.join(root, 'node_modules', p);
const out = path.join(root, 'assets');

// ---- KaTeX (apenas woff2) ----
fs.mkdirSync(path.join(out, 'katex/fonts'), { recursive: true });
let css = fs.readFileSync(nm('katex/dist/katex.min.css'), 'utf8');
css = css.replace(/,url\(fonts\/[^)]+\.woff\) format\("woff"\),url\(fonts\/[^)]+\.ttf\) format\("truetype"\)/g, '');
fs.writeFileSync(path.join(out, 'katex/katex.min.css'), css);
for (const f of fs.readdirSync(nm('katex/dist/fonts'))) if (f.endsWith('.woff2')) fs.copyFileSync(nm('katex/dist/fonts/' + f), path.join(out, 'katex/fonts', f));

// ---- Fontes (subconjuntos latin, latin-ext, greek) ----
const wanted = [
  ['source-serif-4', [['400', 'normal'], ['400', 'italic'], ['600', 'normal'], ['600', 'italic'], ['700', 'normal'], ['700', 'italic']]],
  ['source-sans-3', [['400', 'normal'], ['400', 'italic'], ['600', 'normal'], ['700', 'normal'], ['800', 'normal']]],
];
let fontCss = '/* gerado por scripts/vendor.mjs — Source Serif 4 e Source Sans 3 (SIL OFL 1.1) */\n';
for (const [pkg, variants] of wanted) {
  for (const [w, st] of variants) {
    const cssFile = nm(`@fontsource/${pkg}/${w}${st === 'italic' ? '-italic' : ''}.css`);
    if (!fs.existsSync(cssFile)) { console.warn('ausente:', cssFile); continue; }
    const blocks = fs.readFileSync(cssFile, 'utf8').split('/*').slice(1).map((b) => '/*' + b);
    for (const b of blocks) {
      const m = b.match(/\/\* ([\w-]+) \*\//); if (!m) continue;
      const name = m[1];
      if (!/-(latin|latin-ext|greek)-\d+-(normal|italic)$/.test(name)) continue;
      const file = `${name}.woff2`;
      fs.copyFileSync(nm(`@fontsource/${pkg}/files/${file}`), path.join(out, 'fonts', file));
      fontCss += b.replace(/src:[^;]+;/, `src: url(./${file}) format('woff2');`).replace('font-display: swap', 'font-display: block') + '\n';
    }
  }
}
fs.writeFileSync(path.join(out, 'fonts/fonts.css'), fontCss);
console.log('vendor ok:', fs.readdirSync(path.join(out, 'fonts')).length, 'arquivos de fonte;', fs.readdirSync(path.join(out, 'katex/fonts')).length, 'fontes KaTeX');
