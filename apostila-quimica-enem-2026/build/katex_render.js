// Renderiza fórmulas matemáticas (apenas matemática; a química usa build/chem.py).
// Entrada (stdin): JSON [{tex, display}, ...]   Saída (stdout): JSON [html, ...]
const path = require('path');
const katex = require(path.join(__dirname, '..', 'node_modules', 'katex'));

let input = '';
process.stdin.on('data', d => (input += d));
process.stdin.on('end', () => {
  const items = JSON.parse(input);
  const out = items.map(it => katex.renderToString(it.tex, {
    displayMode: !!it.display,
    output: 'html',
    throwOnError: true,
    strict: 'error',
    trust: false,
  }));
  process.stdout.write(JSON.stringify(out));
});
