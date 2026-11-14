"""Módulo F — diagramas de Geopolítica: linha do tempo das ordens mundiais e estrutura da ONU."""
from svgkit import Fig, FULL, HALF, INK, MUTED, wrap
from common import save_svg


def timeline():
    H = 180
    f = Fig(FULL, H, "timeline_ordens", "Linha do tempo das ordens mundiais (1945–2026)")
    W = FULL
    x0, x1 = 14, W - 14
    X = lambda y: x0 + (y - 1945) / (2026 - 1945) * (x1 - x0)
    ya = 90
    bands = [(1947, 1991, "#1F2A44", "BIPOLAR (Guerra Fria)"), (1991, 2008, "#7B3FA0", "TRANSIÇÃO: hegemonia dos EUA"), (2008, 2026, "#E65100", "MULTIPOLAR e COMPETITIVA")]
    f.rect(X(1945), ya - 7, X(1947) - X(1945) - 1.5, 14, fill="#9AA3B2", rx=3)
    for a_, b_, c, t in bands:
        f.rect(X(a_), ya - 7, X(b_) - X(a_) - 1.5, 14, fill=c, rx=3)
        f.text((X(a_) + X(b_)) / 2, ya, t, 6.2, 800, "#FFFFFF", "middle", valign="mid")
    # faixas de texto: a2 = acima (alto), a1 = acima (baixo), b1 = abaixo (perto), b2 = abaixo (longe)
    tr = {"a2": (-1, 62), "a1": (-1, 34), "b1": (1, 20), "b2": (1, 48)}
    ev = [(1945, "ONU criada;\nfim da II Guerra", "a2", "start"), (1947, "Doutrina Truman;\nPlano Marshall", "b2", "start"), (1949, "OTAN;\nRevolução Chinesa", "a1", "start"),
          (1955, "Pacto de Varsóvia;\nBandung", "b1", "middle"), (1961, "Muro de\nBerlim", "a2", "middle"), (1962, "Crise dos\nmísseis", "b2", "middle"),
          (1979, "URSS no\nAfeganistão", "a1", "middle"), (1989, "Queda do\nMuro", "b1", "middle"), (1991, "Fim da\nURSS", "a2", "middle"),
          (2001, "11 de\nsetembro", "b2", "middle"), (2008, "Crise\nfinanceira", "a1", "middle"), (2014, "Crimeia", "b1", "middle"),
          (2022, "Invasão da\nUcrânia", "a2", "middle"), (2025, "Tarifas;\nEUA–China", "b2", "end")]
    for y, t, trk, anc in ev:
        x = X(y)
        sgn, d = tr[trk]
        yt = ya + sgn * d
        f.line(x, ya + sgn * 8, x, ya + sgn * (d - 2), "#37474F", 1)
        if sgn < 0:
            f.text(x, yt - 20, str(y), 6.3, 800, "#1F2A44", anc)
            f.text(x, yt - 9, t, 6.0, 700, INK, anc, lh=1.15)
        else:
            f.text(x, yt, str(y), 6.3, 800, "#1F2A44", anc)
            f.text(x, yt + 10, t, 6.0, 700, INK, anc, lh=1.15)
    f.text(W / 2, H - 8, "Datas aproximadas e simplificadas; a periodização das ordens é interpretativa e varia entre autores.", 5.9, 600, MUTED, "middle")
    save_svg("timeline_ordens", f.render())


def onu():
    H = 228
    f = Fig(FULL, H, "estrutura_onu", "Estrutura da ONU")
    W = FULL
    f.rect(0, 0, W, 26, fill="#1F2A44", rx=6)
    f.text(W / 2, 13, "ONU — Carta de São Francisco (1945) · 193 Estados-membros · sede em Nova York", 7.8, 800, "#FFFFFF", "middle", valign="mid")
    cols = [("Assembleia Geral", "Todos os membros; um país, um voto. Debate e faz recomendações (não vinculantes na maioria dos temas).", "#1565C0"),
            ("Conselho de Segurança", "15 membros. Decisões obrigatórias sobre paz e segurança (sanções, missões de paz). Aprovação exige 9 votos e nenhum veto.", "#C62828"),
            ("Secretariado", "Chefiado pelo secretário-geral; administra a organização e a diplomacia preventiva.", "#546E7A"),
            ("Corte Internacional de Justiça", "Haia; julga disputas entre Estados (se aceitarem a jurisdição) e emite pareceres.", "#7B3FA0"),
            ("Conselho Econômico e Social", "Coordena temas econômicos e sociais e as agências especializadas.", "#E65100"),
            ("Conselho de Tutela", "Supervisionava territórios sob tutela; suspenso desde 1994.", "#9AA3B2")]
    cw, gap = 109, 11.2
    for i, (t, d, c) in enumerate(cols):
        x = i * (cw + gap)
        f.rect(x, 36, cw, 100, fill="#FFFFFF", stroke=c, sw=1.4, rx=5)
        f.rect(x, 36, cw, 26, fill=c, rx=5)
        f.para(x + 4, 41, cw - 8, t, 6.5, 800, "#FFFFFF", "middle", lh=1.12)
        f.para(x + 6, 68, cw - 12, d, 6.1, 500, INK, lh=1.2)
    # P5
    x = 1 * (cw + gap)
    f.rect(x, 142, cw, 52, fill="#FDECEC", stroke="#C62828", sw=1, rx=4)
    f.text(x + cw / 2, 146, "5 permanentes com veto", 6.0, 800, "#8E1B1B", "middle")
    f.para(x + 4, 158, cw - 8, "EUA · Rússia · China · Reino Unido · França\n+ 10 rotativos (2 anos)", 5.9, 600, INK, "middle", lh=1.2)
    # agências
    x = 4 * (cw + gap)
    f.rect(x, 142, cw + gap + cw, 52, fill="#FFF3E6", stroke="#E65100", sw=1, rx=4)
    f.text(x + (2 * cw + gap) / 2, 146, "Agências e programas", 6.0, 800, "#B23C00", "middle")
    f.para(x + 5, 158, 2 * cw + gap - 10, "OMS · FAO · UNESCO · OIT · FMI e Banco Mundial (agências especializadas) · UNICEF · ACNUR · PNUD · PNUMA", 5.9, 600, INK, "middle", lh=1.2)
    f.rect(0, 200, W, 26, fill="#F5F7FA", rx=4)
    f.para(8, 204, W - 16, "**Atenção:** a OMC não é agência da ONU (organização autônoma). Palestina e Santa Sé são Estados observadores, não membros. Reforma do Conselho de Segurança: o Brasil (G4, com Alemanha, Índia e Japão) pleiteia assento permanente.", 6.0, 600, "#37474F", "middle", lh=1.2)
    save_svg("estrutura_onu", f.render())


def build():
    timeline()
    onu()
