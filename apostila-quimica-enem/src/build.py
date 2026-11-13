import importlib, subprocess, sys, os, glob
sys.path.insert(0, os.path.dirname(__file__))
import lib, fonts
fonts.build(os.path.join(os.path.dirname(__file__), '..', 'build', 'fonts'))
MODS = ['p00_intro', 'pA', 'pB', 'pC', 'pD', 'pE', 'pF', 'pG', 'pH', 'pI', 'pJ', 'pK', 'pR']
for m in MODS:
    if os.path.exists(os.path.join(os.path.dirname(__file__), m + '.py')):
        importlib.import_module(m)
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
out_html = os.path.join(root, 'build', 'apostila.html')
open(out_html, 'w', encoding='utf-8').write(lib.render_pages())
pdf = os.path.join(root, 'Apostila_Visual_Quimica_ENEM.pdf')
subprocess.run(['node', os.path.join(root, 'build', 'render.js'), out_html, pdf], check=True)
print('PDF:', pdf, os.path.getsize(pdf)//1024, 'KB')

open(os.path.join(root, 'build', 'qc_log.txt'), 'w', encoding='utf-8').write('\n'.join(lib.QC))
print('QC checks:', len(lib.QC))
