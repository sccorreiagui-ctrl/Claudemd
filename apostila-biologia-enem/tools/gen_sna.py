rows=[('👁️','Pupila','dilata (midríase)','contrai (miose)'),
('🫀','Coração','↑ frequência e força (taquicardia)','↓ frequência (bradicardia)'),
('🫁','Brônquios','dilatam (mais ar)','contraem'),
('🍽️','Tubo digestório','↓ peristaltismo e secreções','↑ peristaltismo e secreções'),
('💧','Glândulas salivares','pouca saliva (boca seca)','muita saliva'),
('🩸','Fígado e glicose','glicogenólise: ↑ glicemia','armazena glicogênio'),
('🚽','Bexiga','relaxa (retém urina)','contrai (micção)'),
('🔴','Vasos da pele e vísceras','vasoconstrição (sangue ao músculo)','pouca ação direta')]
o=''
o+='<rect x="0" y="0" width="690" height="38" rx="8" fill="#fff" stroke="#98a2b6" stroke-width="1" style="display:none"/>'
o+='<rect x="190" y="0" width="236" height="44" rx="8" fill="#d4287c"/><text x="308" y="17" class="t11 c xb w">SIMPÁTICO</text><text x="308" y="32" class="t8 c w">“luta ou fuga” · noradrenalina e adrenalina</text>'
o+='<rect x="436" y="0" width="254" height="44" rx="8" fill="#475a73"/><text x="563" y="17" class="t11 c xb w">PARASSIMPÁTICO</text><text x="563" y="32" class="t8 c w">“repouso e digestão” · acetilcolina</text>'
y=52
for i,(e,n,s,p) in enumerate(rows):
    fill='#f8f9fc' if i%2==0 else '#fff'
    o+=f'<rect x="0" y="{y}" width="690" height="30" fill="{fill}"/>'
    o+=f'<text x="22" y="{y+22}" class="t16 c em">{e}</text><text x="44" y="{y+19}" class="t10 xb">{n}</text>'
    o+=f'<text x="196" y="{y+19}" class="t9" style="fill:#86144f">{s}</text><text x="442" y="{y+19}" class="t9" style="fill:#2c3b50">{p}</text>'
    y+=32
o+=f'<line x1="186" y1="44" x2="186" y2="{y}" class="nf s-g sw1"/><line x1="432" y1="44" x2="432" y2="{y}" class="nf s-g sw1"/>'
o+=f'<text x="0" y="{y+16}" class="t8 g">Anatomia: simpático = gânglios perto da medula (fibras pré curtas, pós longas); parassimpático = gânglios perto dos órgãos (nervo vago).</text>'
open('src/svg/sna.svg','w').write(f'<svg viewBox="0 0 690 {y+24}">{o}</svg>')
# arco reflexo
o=''
o+='<ellipse cx="130" cy="96" rx="60" ry="46" fill="#f1ece4" stroke="#8a7a60" stroke-width="2"/><path d="M130 62 C110 54 94 66 100 84 C104 96 116 98 130 96 C144 98 156 96 160 84 C166 66 150 54 130 62 Z" fill="#c9c1b0" stroke="#8a7a60"/><path d="M130 100 C112 100 96 112 104 126 C112 136 124 130 130 126 C136 130 148 136 156 126 C164 112 148 100 130 100Z" fill="#c9c1b0" stroke="#8a7a60"/>'
o+='<text x="6" y="170" class="t8 b" style="fill:#5a4a30">medula espinhal (corte transversal)</text>'
o+='<path d="M230 22 C190 22 166 40 140 70" class="nf s-ro sw3" marker-end="url(#ar-ro)"/><circle cx="248" cy="22" r="12" class="l-rs s-rs sw2"/><text x="268" y="26" class="t8 b tx-rs">receptor (pele)</text>'
o+='<text x="190" y="46" class="t8 b tx-ro">neurônio sensitivo</text>'
o+='<circle cx="130" cy="82" r="5" class="f-ro"/><text x="40" y="76" class="t8 b tx-ro e" style="display:none"></text><text x="74" y="86" class="t8 b tx-ro e">neurônio</text><text x="74" y="96" class="t8 b tx-ro e">associativo</text>'
o+='<path d="M136 118 C170 144 200 150 236 144" class="nf s-vm sw3" marker-end="url(#ar-vm)"/><text x="196" y="168" class="t8 b tx-vm">neurônio motor</text>'
o+='<rect x="240" y="130" width="88" height="28" rx="8" fill="#f3b6b6" stroke="#b34747" stroke-width="1.6"/><text x="284" y="148" class="t9 c xb" style="fill:#7a2020">músculo (efetor)</text>'
o+='<text x="250" y="86" class="t8 g" style="display:none"></text>'
open('src/svg/arco.svg','w').write(f'<svg viewBox="0 0 335 176">{o}</svg>')
# sinapse
o=''
o+='<path d="M10 10 H160 Q176 10 176 26 V54 Q176 70 160 70 H10 Z" fill="#ece0f8" stroke="#7b43b8" stroke-width="2"/><text x="14" y="26" class="t8 b tx-ro">terminal do axônio</text>'
for (x,y) in [(40,44),(70,38),(100,48),(130,40)]: o+=f'<circle cx="{x}" cy="{y}" r="8" fill="#fff" stroke="#1f78c8" stroke-width="1.8"/><circle cx="{x-2}" cy="{y-1}" r="2" class="f-rs"/><circle cx="{x+3}" cy="{y+2}" r="2" class="f-rs"/>'
o+='<rect x="10" y="102" width="166" height="62" rx="8" fill="#fbe0e0" stroke="#d83a3a" stroke-width="2" style="display:none"/>'
o+='<path d="M10 106 H176 Q190 106 190 120 V150 Q190 164 176 164 H10 Z" fill="#fde9ef" stroke="#c9778f" stroke-width="2"/><text x="14" y="122" class="t8 b" style="fill:#86144f">célula pós-sináptica</text>'
o+='<rect x="30" y="97" width="12" height="9" rx="2" class="f-az"/><rect x="74" y="97" width="12" height="9" rx="2" class="f-az"/><rect x="118" y="97" width="12" height="9" rx="2" class="f-az"/>'
o+='<text x="100" y="92" class="t8 c b tx-sl">fenda sináptica</text>'
for x in (36,80,124): o+=f'<path d="M{x} 62 V92" class="nf s-rs sw1 dt"/><circle cx="{x}" cy="88" r="2.4" class="f-rs"/>'
o+='<g class="t8">'
steps=['1  potencial de ação chega','2  Ca²⁺ entra no terminal','3  vesículas liberam o','    neurotransmissor','4  receptores abrem canais','    iônicos (pós-sináptica)','5  neurotransmissor removido']
for i,t in enumerate(steps): o+=f'<text x="196" y="{22+i*12}" class="{"b" if t[0].isdigit() else ""}">{t}</text>'
o+='</g>'
o+='<text x="196" y="116" class="t8 b tx-vm">Potencial de ação:</text><text x="196" y="127" class="t8">Na⁺ entra (despolariza);</text><text x="196" y="138" class="t8">K⁺ sai (repolariza);</text><text x="196" y="149" class="t8">bomba Na⁺/K⁺ (gasta ATP).</text>'
open('src/svg/sinapse.svg','w').write(f'<svg viewBox="0 0 335 176">{o}</svg>')
print('ok')
