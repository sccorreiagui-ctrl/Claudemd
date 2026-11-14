o=''
o+='<rect x="0" y="22" width="440" height="84" rx="10" class="l-az"/><text x="8" y="36" class="t9 xb tx-az">ÁGUA PARADA (pneus, vasos, calhas, caixas)</text>'
# ovo
for dx in (0,8,16,24): o+=f'<ellipse cx="{50+dx}" cy="76" rx="4" ry="2.6" fill="#1b2236"/>'
o+='<text x="66" y="104" class="t9 c xb">1. Ovos</text><text x="66" y="114" class="t8 c g" style="display:none"></text>'
# larva
o+='<path d="M160 60 q-14 6 -4 16 q10 8 22 -2 q6 -6 -2 -12" class="nf s-sl sw3 rc"/><circle cx="186" cy="64" r="4" class="f-sl"/><text x="170" y="104" class="t9 c xb">2. Larva</text>'
# pupa
o+='<path d="M290 58 c14 -6 22 8 16 20 c-6 12 -22 6 -22 -4 c2 -6 6 -8 10 -6" class="nf s-sl sw3 rc"/><circle cx="294" cy="60" r="6" class="f-sl"/><text x="294" y="104" class="t9 c xb">3. Pupa</text>'
# adulto
o+='<text x="396" y="76" class="t30 c em">🦟</text><text x="396" y="104" class="t9 c xb">4. Adulto</text><text x="396" y="116" class="t8 c g">fêmea: sangue → ovos</text>'
o+='<g class="nf s-k sw2"><path d="M96 66 H128" marker-end="url(#ar-k)"/><path d="M212 66 H252" marker-end="url(#ar-k)"/><path d="M330 66 H360" marker-end="url(#ar-k)"/></g>'
# transmissão
o+='<g transform="translate(470 0)"><text x="0" y="14" class="t9 xb tx-vm">Ciclo de transmissão</text>'
o+='<text x="40" y="70" class="t26 c em">🧍</text><text x="160" y="70" class="t26 c em">🦟</text><text x="250" y="70" class="t26 c em" style="display:none"></text>'
o+='<path d="M60 52 C80 30 120 30 144 48" class="nf s-vm sw2" marker-end="url(#ar-vm)"/><text x="102" y="26" class="t8 c b tx-vm">fêmea pica pessoa infectada</text>'
o+='<path d="M144 82 C120 104 80 104 62 84" class="nf s-vm sw2" marker-end="url(#ar-vm)"/><text x="102" y="114" class="t8 c b tx-vm">após ≈ 1–2 semanas, transmite</text>'
o+='<text x="40" y="94" class="t8 c b">pessoa</text><text x="160" y="94" class="t8 c b">Aedes fêmea</text></g>'
open('src/svg/aedes.svg','w').write(f'<svg viewBox="0 0 690 122">{o}</svg>')
print('ok')
