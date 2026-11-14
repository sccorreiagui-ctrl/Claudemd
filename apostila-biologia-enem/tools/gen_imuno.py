o=''
o+='<line x1="30" y1="14" x2="30" y2="156" class="nf s-k sw12" marker-end="url(#ar-k)"/><line x1="30" y1="156" x2="326" y2="156" class="nf s-k sw12" marker-end="url(#ar-k)"/>'
o+='<text x="2" y="12" class="t8 g">anticorpos</text><text x="326" y="172" class="t8 g e">dias</text>'
o+='<path d="M30 156 H59 C70 156 84 118 106 116 C120 118 130 136 154 138" class="nf s-la sw3 rc"/>'
o+='<path d="M154 138 C160 138 166 76 178 40 C190 32 220 38 250 54 C280 68 306 86 320 96" class="nf s-vm sw3 rc"/>'
o+='<line x1="30" y1="22" x2="30" y2="156" class="nf" style="display:none"/>'
for x,t in ((30,'1ª exposição'),(154,'2ª exposição')):
    o+=f'<path d="M{x} 176 V160" class="nf s-ro sw2" marker-end="url(#ar-ro)" style="display:none"/>'
o+='<line x1="30" y1="156" x2="30" y2="160" class="nf s-k"/><line x1="154" y1="26" x2="154" y2="156" class="nf s-g sw1 dt"/>'
o+='<text x="34" y="170" class="t8 b tx-ro">1ª exposição</text><text x="158" y="170" class="t8 b tx-ro">2ª exposição</text>'
o+='<text x="96" y="104" class="t8 c b tx-la">resposta primária</text><text x="96" y="114" class="t7 c g">lenta, baixa (IgM)</text>'
o+='<text x="236" y="40" class="t8 c b tx-vm">resposta secundária</text><text x="236" y="26" class="t7 c g" style="display:none"></text><text x="268" y="52" class="t7 g" style="display:none"></text>'
o+='<text x="190" y="108" class="t7 b tx-vm" style="display:none"></text>'
o+='<text x="236" y="88" class="t8 b tx-vm">rápida, intensa (IgG),</text><text x="236" y="98" class="t8 b tx-vm">duradoura</text><text x="236" y="112" class="t7 g">memória imunológica</text>'
open('src/svg/respostas.svg','w').write(f'<svg viewBox="0 0 335 182">{o}</svg>')
# vacina x soro: proteção no tempo
o=''
o+='<line x1="30" y1="14" x2="30" y2="146" class="nf s-k sw12" marker-end="url(#ar-k)"/><line x1="30" y1="146" x2="326" y2="146" class="nf s-k sw12" marker-end="url(#ar-k)"/>'
o+='<text x="2" y="12" class="t8 g">proteção</text><text x="326" y="162" class="t8 g e">tempo após a aplicação</text>'
o+='<path d="M30 146 C60 146 90 140 130 100 C170 62 200 54 320 52" class="nf s-ve sw3 rc"/><text x="214" y="46" class="t8 b tx-ve">VACINA: lenta, duradoura</text>'
o+='<path d="M30 146 C32 70 34 40 40 36 C80 44 120 100 180 138 C210 144 260 146 320 146" class="nf s-vm sw3 rc"/><text x="50" y="38" class="t8 b tx-vm">SORO: imediato, passageiro</text>'
o+='<text x="140" y="124" class="t7 g">anticorpos prontos</text><text x="140" y="133" class="t7 g">são consumidos</text>'
open('src/svg/vacsoro.svg','w').write(f'<svg viewBox="0 0 335 168">{o}</svg>')
print('ok')
