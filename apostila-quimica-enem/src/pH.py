# -*- coding: utf-8 -*-
from lib import *
from figs import *
from chk import num
import math

def energia_fig():
    s = Svg(340, 280)
    ax = Axes(s, 46, 14, 280, 214, (0, 10), (0, 120))
    s.line(ax.x0, ax.y0, ax.x0, ax.y0+ax.h, INK, 1.6); s.line(ax.x0, ax.y0+ax.h, ax.x0+ax.w, ax.y0+ax.h, INK, 1.6)
    s.text(ax.x0-32, ax.y0+ax.h/2, 'Energia (kJ)', 10, INK, 'middle', 700, rot=-90); s.text(ax.x0+ax.w/2, ax.y0+ax.h+22, 'Caminho (progresso) da reação', 10, INK, 'middle', 700)
    def curve(peak, col, sw, dash=None):
        d = f'M{ax.X(0)},{ax.Y(40)} L{ax.X(1.6)},{ax.Y(40)} C{ax.X(3.4)},{ax.Y(40)} {ax.X(3.4)},{ax.Y(peak)} {ax.X(5)},{ax.Y(peak)} C{ax.X(6.6)},{ax.Y(peak)} {ax.X(6.6)},{ax.Y(20)} {ax.X(8.4)},{ax.Y(20)} L{ax.X(10)},{ax.Y(20)}'
        s.path(d, stroke=col, sw=sw, dash=dash)
    curve(100, INK, 2.8); curve(70, ORANGE, 2.8, '6 4')
    s.line(ax.X(0), ax.Y(40), ax.X(1.6), ax.Y(40), GRAY, 1, '2 2')
    s.text(ax.X(0.2), ax.Y(40)-6, 'reagentes', 9.6, INK, 'start', 800); s.text(ax.X(8.2), ax.Y(20)+13, 'produtos', 9.6, INK, 'start', 800)
    s.label(ax.X(5), ax.Y(100)-12, 'complexo ativado (sem catalisador)', 9, INK, '#fff', 800)
    s.label(ax.X(5), ax.Y(70)+22, 'com catalisador', 9.4, ORANGE_D, '#fff', 800)
    s.line(ax.X(1.3), ax.Y(40), ax.X(1.3), ax.Y(100), RED, 1.6, marker='red'); s.line(ax.X(1.3), ax.Y(100), ax.X(1.3), ax.Y(40), RED, 1.6, marker='red'); s.label(ax.X(1.3)+22, ax.Y(70), 'Eₐ', 11, RED_D, '#fff', 900)
    s.line(ax.X(2.4), ax.Y(40), ax.X(2.4), ax.Y(70), ORANGE, 1.6, marker='orange'); s.label(ax.X(2.4)+12, ax.Y(56), "Eₐ'", 10, ORANGE_D, '#fff', 900)
    s.line(ax.X(9.4), ax.Y(40), ax.X(9.4), ax.Y(20), GREEN, 1.8, marker='green'); s.text(ax.X(9.4)-4, ax.Y(30)+3, 'ΔH', 10.5, GREEN_D, 'end', 900)
    s.line(ax.X(8.6), ax.Y(40), ax.X(10), ax.Y(40), GRAY, 1, '2 2')
    return s.render()

def dist_fig():
    s = Svg(330, 190)
    ax = Axes(s, 42, 12, 276, 130, (0, 10), (0, 1.1))
    ax.frame(None, None, 'Energia cinética das moléculas', 'nº de moléculas', size=9, ylabel_dx=18, xlabel_dy=26)
    def f(x, T): k = 1.0/T; return (x**1.0) * math.exp(-x*k*1.0)
    def pts(T, norm):
        return [(x/10*10, norm*(x/ T) * math.exp(-x/T)) for x in [i*0.2 for i in range(0, 51)]]
    for T, col, lab in ((1.6, BLUE, 'T baixa'), (2.6, ORANGE, 'T alta')):
        d = [(x, (x/T)*math.exp(-x/T)/0.368*0.78*(1.6/T)**0.45) for x in [i*0.2 for i in range(0, 51)]]
        ax.line(d, col, 2.4)
    EA = 5.4
    ax.s.line(ax.X(EA), ax.Y(0), ax.X(EA), ax.Y(0.95), RED, 1.8, '4 3'); ax.s.text(ax.X(EA)+4, ax.Y(0.95)+2, 'Eₐ', 10.5, RED_D, 'start', 900)
    ax.s.text(ax.X(1.6), ax.Y(0.88), 'T baixa', 9.6, BLUE_D, 'middle', 800); ax.s.text(ax.X(4.0), ax.Y(0.62), 'T alta', 9.6, ORANGE_D, 'middle', 800)
    ax.s.text(ax.X(6.0), ax.Y(0.80), 'só as moléculas com', 9, INK, 'start', 700); ax.s.text(ax.X(6.0), ax.Y(0.70), 'E ≥ Eₐ reagem;', 9, INK, 'start', 700); ax.s.text(ax.X(6.0), ax.Y(0.60), '↑T → mais delas', 9, INK, 'start', 700)
    return s.render()

def surf_fig():
    s = Svg(330, 110)
    s.rect(14, 28, 56, 56, '#E7E9EE', INK, 2, 2); s.text(42, 100, 'bloco', 9.6, INK, 'middle', 800); s.text(42, 14, '6 faces expostas', 8.8, GRAY, 'middle', 600)
    s.arrow(84, 56, 126, 56, 'orange', 2.4)
    import random; rnd = random.Random(2)
    for _ in range(40): s.rect(150 + rnd.uniform(0, 150), 34 + rnd.uniform(0, 48), 6, 6, '#E7E9EE', INK, 1, 1.1)
    s.text(228, 100, 'pó: muito mais área de contato', 9.6, INK, 'middle', 800); s.text(228, 14, 'mesma massa, mais superfície → mais rápido', 8.8, GRAY, 'middle', 600)
    return s.render()

def enzima_fig():
    s = Svg(330, 150)
    s.path('M20,60 C20,20 60,20 78,48 L100,48 L100,58 L78,58 C60,78 20,90 20,60 Z', '#DDF3E4', GREEN, 2); s.text(52, 66, 'enzima', 9.6, GREEN_D, 'middle', 900)
    s.poly([(96, 46), (112, 46), (112, 60), (96, 60)], '#fff', INK, 0, close=True)
    s.rect(108, 45, 30, 16, ORANGE_L, ORANGE, 3, 2); s.text(123, 56.5, 'S', 10, ORANGE_D, 'middle', 900); s.arrow(160, 53, 180, 53, 'ink', 1.8)
    s.text(100, 80, 'sítio ativo', 8.8, GREEN_D, 'middle', 800); s.text(123, 38, 'substrato', 8.8, ORANGE_D, 'middle', 800)
    s.rect(190, 45, 14, 16, ORANGE_L, ORANGE, 3, 1.8); s.rect(208, 45, 14, 16, ORANGE_L, ORANGE, 3, 1.8); s.text(206, 78, 'produtos', 8.8, ORANGE_D, 'middle', 800)
    ax = Axes(s, 262, 20, 62, 70, (0, 10), (0, 1.1))
    s.line(262, 90, 324, 90, INK, 1.4); s.line(262, 20, 262, 90, INK, 1.4)
    d = [(x, math.exp(-((x-5.4)/2.2)**2)) for x in [i*0.2 for i in range(0, 51)]]
    s.poly([(262+x*6.2, 90-y*62) for x, y in d], stroke=GREEN, sw=2.4)
    s.text(293, 106, '37 °C ótima', 8.8, GREEN_D, 'middle', 800); s.text(293, 118, 'T → desnatura', 8.4, GRAY, 'middle', 600)
    s.text(266, 18, 'atividade', 8.4, INK, 'start', 700)
    s.text(8, 142, 'chave-fechadura: o substrato encaixa no sítio ativo (alta especificidade)', 9, GRAY, 'start', 700)
    return s.render()

def p_H1():
    return f'''
<div class="cols2" style="grid-template-columns:340px 1fr; align-items:start">
  <div><h2>Gráfico energia × caminho da reação</h2>{energia_fig()}</div>
  <div><h2>Como ler</h2>
  <ul><li><b>Eₐ</b> (energia de ativação): barreira que as moléculas precisam vencer para formar o <b>complexo ativado</b>.</li><li><b>Catalisador</b>: abre outro caminho, com <b>Eₐ menor</b>. Aumenta a velocidade, é regenerado, e <b>não altera ΔH</b>, nem o rendimento de equilíbrio.</li><li><b>ΔH</b>: diferença entre produtos e reagentes (aqui, <b>exotérmica</b>: produtos mais baixos).</li><li>Velocidade = quantas colisões <b>efetivas</b> por segundo (energia suficiente e orientação correta).</li></ul>
  {box('red','Erros comuns','<ul><li>“O catalisador diminui a energia da reação (ΔH).” <b>Não</b>: diminui a <b>barreira</b>.</li><li>“Temperatura alta ⇒ Eₐ menor.” <b>Não</b>: Eₐ não muda; <b>mais moléculas</b> a superam.</li><li>Reação rápida ≠ reação favorável (ΔH ou equilíbrio).</li></ul>')}</div>
</div>
<div class="cols2" style="grid-template-columns:330px 1fr; align-items:start">
  <div><h2>Temperatura: a cauda da distribuição</h2>{dist_fig()}</div>
  <div><h2>Os fatores, em uma tabela</h2>
  <table><tr><th>Fator</th><th>↑ velocidade porque…</th></tr>
  <tr><td><b>Concentração</b> / pressão (gases)</td><td>mais partículas por volume → mais colisões</td></tr>
  <tr><td><b>Temperatura</b></td><td>maior fração de colisões com E ≥ Eₐ</td></tr>
  <tr><td><b>Superfície de contato</b></td><td>mais área exposta ao reagente</td></tr>
  <tr><td><b>Catalisador</b></td><td>caminho com menor Eₐ</td></tr>
  <tr><td><b>Natureza do reagente</b>, luz</td><td>ligações mais fracas ou energia radiante</td></tr></table>
  <div style="margin-top:1mm">{surf_fig()}</div></div>
</div>
<div class="cols2" style="grid-template-columns:340px 1fr; align-items:start">
  <div><h2>Enzimas: catalisadores biológicos</h2>{enzima_fig()}</div>
  <div>{box('green','Aplicações: biológicas, industriais e ambientais','<ul><li><b>Enzimas</b>: amilase (digere amido), lipase, catalase (H₂O₂ → H₂O + ½ O₂); detergentes enzimáticos. Acima da T ótima, a enzima <b>desnatura</b>.</li><li><b>Geladeira</b>: T baixa retarda a decomposição.</li><li><b>Panela de pressão</b>: ↑ pressão → ↑ T de ebulição → cozimento mais rápido.</li><li><b>Conversor catalítico</b> (Pt, Pd, Rh): 2 CO + 2 NO → 2 CO₂ + N₂.</li></ul>')}
  {quiz([('Em um gráfico [produto] × tempo, qual curva indica reação mais rápida?', 'A de maior inclinação inicial (mais produto por unidade de tempo).'), ('Por que moer o comprimido acelera a ação?', 'Maior superfície de contato com o solvente.')])}</div>
</div>'''
page('H', 'Módulo H · 1 de 1', 'Cinética química: o que faz uma reação ser rápida', p_H1(), key='H1')
