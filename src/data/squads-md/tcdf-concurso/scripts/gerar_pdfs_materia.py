#!/usr/bin/env python3
"""Gera um PDF por materia: a ementa inteira cruzada com os filtros do Gran.

Duas folhas em pe (A4 retrato):

  FOLHA 1 — MAPA DA EMENTA x FILTROS. Cada topico e cada subtopico do edital em
  uma linha, com a aula do curso ao lado e uma bolinha em cada coluna de filtro.
  O nome do filtro vai escrito a mao, em pe, no cabecalho da coluna; as bolinhas
  marcadas dizem o que aquele filtro esta sorteando.

  A ultima coluna e fixa: GERAL N2. A bolina grande dela marca o conteudo que ja
  venceu — o que sai da fila de estudo e passa a entrar no filtro geral, aquele
  que alimenta os simulados de grupo e as revisoes de tudo que ja esta vencido.

  FOLHA 2 — REGISTRO DOS SIMULADOS. Uma linha por lote resolvido: filtro, data,
  total, acertos, erros, bruto, liquido e veredito.

A materia inteira cabe na folha 1, qualquer que seja o tamanho dela: o corpo do
texto encolhe so o quanto for preciso, e o que sobra de altura vira respiro
entre as linhas e, depois, pauta de anotacao — folha cheia em qualquer caso.

Uso:
    python3 scripts/gerar_pdfs_materia.py                      # todas as materias
    python3 scripts/gerar_pdfs_materia.py direito-administrativo
"""
from __future__ import annotations

import json
import math
import re
import sys
from io import BytesIO
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import Flowable, PageBreak, Paragraph, Spacer, Table, TableStyle
from reportlab.platypus.doctemplate import LayoutError

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))

from gerar_pdfs import (  # noqa: E402
    CABECA, CELULA, CLARO, DESTAQUE, FUNDO, LINHA, SECAO,
    Bolinha, documento, partes, slug,
)
from gerar_status import ler_progresso  # noqa: E402

SAIDA = RAIZ / "pdf" / "materias"
PAGINA = A4
MARGEM = 12 * mm
FAIXA = 14 * mm
TOPO = 20 * mm
BASE = 10 * mm
CALHA = 7 * mm

N_FILTROS = 8
LARGURA_UTIL = PAGINA[0] - 2 * MARGEM
ALTURA_UTIL = PAGINA[1] - TOPO - BASE

# O respiro minimo entre as linhas acompanha o corpo: em 12pt sobra folga, em
# 7pt cada ponto fixo de padding custa 2 mm de folha ao longo de 55 linhas.
PADDING_MINIMO = 0.8
PADDING_MAXIMO = 6.0
H_CAIXA = 15 * mm
ZEBRA = colors.HexColor("#fafafa")

# Corpos tentados, do mais confortavel ao mais apertado. Em retrato a coluna
# unica e a unica opcao: partir a folha em duas deixaria 45 mm de texto, estreito
# demais para o enunciado de um subtopico.
LAYOUTS = [(1, c) for c in (12.0, 11.0, 10.0, 9.2, 8.6, 8.0, 7.6, 7.2,
                            6.9, 6.6, 6.3, 6.0, 5.8)]

MINI = CABECA.clone("mini", fontSize=6, leading=7)
LINHAS_DO_HISTORICO = 12


class Medidas:
    """Larguras e raios de um layout — tudo deriva do corpo do texto."""

    def __init__(self, colunas: int, escala: float):
        self.colunas, self.escala = colunas, escala
        self.l_filtro = min(7 * mm, max(5.2 * mm, 0.62 * mm * escala))
        self.l_aula = max(9 * mm, 0.85 * mm * escala)
        self.l_coluna = (LARGURA_UTIL - CALHA) / 2 if colunas == 2 else LARGURA_UTIL
        # A coluna do GERAL N2 e mais larga e leva a bolina: ela decide se o
        # conteudo entrou no bolo que os simulados de grupo e as revisoes usam.
        self.l_geral = min(11 * mm, max(7.6 * mm, 0.95 * mm * escala))
        self.l_texto = (self.l_coluna - self.l_aula - N_FILTROS * self.l_filtro
                        - self.l_geral)
        self.larguras = ([self.l_texto, self.l_aula] + [self.l_filtro] * N_FILTROS
                         + [self.l_geral])
        # O raio tambem acompanha o corpo: a bolinha e o piso da altura da linha
        # (um circulo de 3 mm nao cabe em linha de 2,7 mm), entao raio fixo trava a
        # folha e faz reduzir a fonte nao adiantar nada.
        self.raio = min(2.3 * mm, self.l_filtro * 0.28, max(1.05 * mm, 0.19 * mm * escala))
        self.padding = max(PADDING_MINIMO, escala * 0.14)
        # A bolina e maior que as outras, mas nunca a ponto de esticar a linha:
        # numa materia de 55 linhas, meio milimetro a mais por linha custa a folha.
        self.raio_geral = min(3.4 * mm, self.l_geral * 0.34, self.raio * 1.5,
                              (escala * 1.2 + 2 * self.padding) / 2 * 0.95)
        item = CELULA.clone("item", fontSize=escala, leading=escala * 1.2)
        self.topico = item.clone("topico", fontName="Helvetica-Bold")
        self.sub = item.clone("sub", fontSize=escala - 0.4, leading=escala * 1.17,
                              leftIndent=escala * 0.9, textColor=colors.HexColor("#374151"))
        self.aula = item.clone("aula", fontSize=escala - 1.1, leading=escala, textColor=DESTAQUE)


class CaixaDoFiltro(Flowable):
    """Cabecalho da coluna: caixa alta e vazia, para escrever o nome do filtro em pe."""

    def __init__(self, largura):
        super().__init__()
        self.width, self.height = largura - 1.2 * mm, H_CAIXA - 2 * mm

    def draw(self):
        c = self.canv
        c.setStrokeColor(CLARO)
        c.setLineWidth(0.5)
        c.setDash(1.2, 1.6)
        c.rect(0, 0, self.width, self.height, stroke=1, fill=0)
        c.setDash()


class RotuloGeral(Flowable):
    """Cabecalho da coluna fixa: GERAL N2 escrito em pe, ja impresso."""

    def __init__(self, largura):
        super().__init__()
        self.width, self.height = largura - 1.2 * mm, H_CAIXA - 2 * mm

    def draw(self):
        c = self.canv
        c.setFillColor(FUNDO)
        c.setStrokeColor(DESTAQUE)
        c.setLineWidth(0.6)
        c.rect(0, 0, self.width, self.height, stroke=1, fill=1)
        c.setFillColor(DESTAQUE)
        c.setFont("Helvetica-Bold", 7)
        c.saveState()
        c.translate(self.width / 2 + 2.5, 3)
        c.rotate(90)
        c.drawString(0, 0, "GERAL N2")
        c.restoreState()


def aulas_da_materia(gran: dict, mid: str) -> dict[str, list[int]]:
    saida: dict[str, list[int]] = {}
    for a in gran["materias"].get(mid, []):
        for n in a["topicos"]:
            saida.setdefault(n, []).append(a["aula"])
    return saida


def linhas_da_materia(materia, aulas, estado):
    """[(e_topico, texto, aula, estudado, vencido)] na ordem da ementa.

    `vencido` so e lido na linha do topico: e o topico inteiro que vence, num lote
    de 20, e e ele que entra ou nao no filtro GERAL N2.
    """
    saida = []
    for t in materia["ementa"]:
        n = t["n"]
        numero, titulo, subs = partes(t["texto"])
        e = estado["estudo"].get((materia["id"], n), {})
        venceu = (materia["id"], n) in estado["vencidos"]
        vistos = set(e.get("subtopicos", []))
        ag = ", ".join(str(x) for x in aulas.get(n, [])) or "—"
        saida.append((True, f"<b>{numero or n}.</b> {titulo}", ag,
                      bool(e) and e.get("completo", True), venceu))
        for s in subs:
            saida.append((False, s, "", s.split()[0] in vistos, venceu))
        for s in t.get("subtopicos_sugeridos", []):
            saida.append((False, f"{s} <font size=5.5>(sugerido)</font>", "", False, venceu))
    return saida


def altura_estimada(linha, m: Medidas) -> float:
    """Altura da celula em pontos — mede a largura real da string na fonte usada."""
    e_topico, texto = linha[0], re.sub(r"<[^>]+>", "", linha[1])
    fonte = "Helvetica-Bold" if e_topico else "Helvetica"
    corpo = m.escala if e_topico else m.escala - 0.4
    util = m.l_texto - 3 - (0 if e_topico else m.escala * 0.9)
    n = max(1, math.ceil(stringWidth(texto, fonte, corpo) / util))
    return n * corpo * 1.2 + 2 * m.padding


def partir(linhas, m: Medidas):
    """Divide a ementa em duas colunas, cortando sempre no inicio de um topico."""
    if m.colunas == 1:
        return linhas, []
    alturas = [altura_estimada(x, m) for x in linhas]
    total = sum(alturas)
    cortes = [i for i, x in enumerate(linhas) if x[0] and i > 0] or [len(linhas)]
    melhor = min(cortes, key=lambda i: abs(sum(alturas[:i]) - total / 2))
    return linhas[:melhor], linhas[melhor:]


def tabela_coluna(linhas, m: Medidas, respiro=0.0):
    caixas = ["", ""] + [CaixaDoFiltro(m.l_filtro) for _ in range(N_FILTROS)] + \
             [RotuloGeral(m.l_geral)]
    rotulos = [Paragraph("TÓPICO E SUBTÓPICO DO EDITAL", MINI), Paragraph("AULA", MINI)] + \
              [Paragraph(f"F{i}", MINI) for i in range(1, N_FILTROS + 1)] + \
              [Paragraph("VENCI", MINI)]
    dados, marcas, zebra = [caixas, rotulos], [], []

    for i, (e_topico, texto, aula, cheia, venceu) in enumerate(linhas):
        if e_topico and len(dados) > 2:
            marcas.append(("LINEABOVE", (0, len(dados)), (-1, len(dados)), 0.5, CLARO))
        if i % 2:
            zebra.append(("BACKGROUND", (0, len(dados)), (-1, len(dados)), ZEBRA))
        dados.append([Paragraph(texto, m.topico if e_topico else m.sub),
                      Paragraph(aula, m.aula)] +
                     [Bolinha(raio=m.raio, cheia=cheia) for _ in range(N_FILTROS)] +
                     # A bolina so existe na linha do topico: quem vence e o topico
                     # inteiro, num lote de 20 — subtopico sozinho nao fecha nada.
                     [Bolinha(raio=m.raio_geral, cor=DESTAQUE, espessura=1.1, cheia=venceu)
                      if e_topico else ""])

    t = Table(dados, colWidths=m.larguras,
              rowHeights=[H_CAIXA, 5 * mm] + [None] * len(linhas), hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 1), (-1, 1), DESTAQUE),
        ("VALIGN", (0, 0), (-1, 1), "MIDDLE"),
        ("VALIGN", (0, 2), (-1, -1), "TOP"),
        ("ALIGN", (2, 0), (-1, -1), "CENTER"),
        ("ALIGN", (1, 2), (1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (0, -1), 3),
        ("LEFTPADDING", (1, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (0, -1), 4),
        ("TOPPADDING", (0, 2), (-1, -1), m.padding + respiro),
        ("BOTTOMPADDING", (0, 2), (-1, -1), m.padding + respiro),
        # Celula vazia herda o corpo padrao da tabela (10pt) e infla a linha
        # inteira; nas linhas de subtopico isso custava 1,4 mm cada.
        ("FONTSIZE", (0, 2), (-1, -1), m.escala),
        ("LEADING", (0, 2), (-1, -1), m.escala * 1.2),
        ("LINEBEFORE", (2, 1), (2, -1), 0.7, CLARO),
        ("LINEBEFORE", (-1, 0), (-1, -1), 1.0, DESTAQUE),
        ("BOX", (0, 1), (-1, -1), 0.7, CLARO),
    ] + zebra + marcas + [("BACKGROUND", (-1, 2), (-1, -1), FUNDO)]))
    return t


def rodape_do_geral(m: Medidas, n_topicos: int):
    """Pe da folha: uma bolona embaixo de cada coluna de filtro.

    A coluna diz, topico a topico, o que aquele filtro sorteia. A bolona do pe
    fecha a coluna: aquele filtro ja bateu a meta e pode ser jogado no GERAL N2,
    o filtro unico que junta a materia vencida e alimenta os simulados de grupo e
    as revisoes gerais. A ultima coluna e a materia inteira.
    """
    corpo = CELULA.clone("rodapegeral", fontSize=max(6.6, m.escala - 0.6),
                         leading=max(8.4, m.escala * 1.15))
    titulo = Paragraph(
        "ESTE FILTRO JÁ VENCEU? Bateu 90%, marque a bolona e jogue o filtro dentro do "
        "<b>GERAL N2</b> — o filtro único da matéria vencida, de onde saem os simulados de grupo "
        "e as revisões", CABECA)
    ficha = Paragraph(
        f"GERAL N2 · tópicos já dentro dele: ______ de {n_topicos} &nbsp;·&nbsp; "
        "atualizado em ______/______/__________ &nbsp;·&nbsp; última rodada: "
        "______/______/______ &nbsp;·&nbsp; questões ________ &nbsp;·&nbsp; acertos ________ "
        "&nbsp;·&nbsp; % bruto ________", corpo)
    raio = min(2.4 * mm, m.l_filtro * 0.36)

    dados = [
        [titulo] + [""] * N_FILTROS + [Paragraph("TUDO", MINI)],
        [Paragraph("<b>Entra no GERAL N2  →</b>", corpo)] +
        [Bolinha(raio=raio, cor=DESTAQUE, espessura=1.1) for _ in range(N_FILTROS)] +
        [Bolinha(raio=raio, cor=DESTAQUE, espessura=1.4)],
        [ficha] + [""] * N_FILTROS + [""],
    ]
    larguras = [sum(m.larguras[:2])] + m.larguras[2:]
    t = Table(dados, colWidths=larguras, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DESTAQUE),
        ("BACKGROUND", (0, 1), (-1, -1), FUNDO),
        ("SPAN", (0, 0), (-2, 0)),
        ("SPAN", (0, 2), (-1, 2)),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 1), (0, 1), "RIGHT"),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (0, -1), 5),
        ("LEFTPADDING", (1, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 1), (0, 1), 6),
        ("TOPPADDING", (0, 1), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 3.5),
        ("LINEBEFORE", (-1, 0), (-1, -1), 1.0, DESTAQUE),
        ("LINEBELOW", (0, 1), (-1, 1), 0.5, CLARO),
        ("BOX", (0, 0), (-1, -1), 0.8, CLARO),
    ]))
    return t


def pauta(linhas_pautadas: int):
    """Sobra da folha vira espaco pautado para anotar o que caiu no filtro."""
    dados = [[Paragraph("ANOTAÇÕES — o que o filtro cobrou e onde doeu", CABECA)]] + \
            [[""] for _ in range(linhas_pautadas)]
    t = Table(dados, colWidths=[LARGURA_UTIL],
              rowHeights=[6.5 * mm] + [7.5 * mm] * linhas_pautadas, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DESTAQUE),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (0, 1), (-1, -1), 0.4, LINHA),
        ("BOX", (0, 0), (-1, -1), 0.7, CLARO),
    ]))
    return t


def folha_do_mapa(linhas, m: Medidas, respiro=0.0, linhas_pautadas=0, n_topicos=0):
    esq, dir_ = partir(linhas, m)
    corpo = tabela_coluna(esq, m, respiro)
    if dir_:
        lado = Table([[corpo, tabela_coluna(dir_, m, respiro)]],
                     colWidths=[m.l_coluna, m.l_coluna + CALHA], hAlign="LEFT")
        lado.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (0, 0), 0),
            ("LEFTPADDING", (1, 0), (1, 0), CALHA),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        corpo = lado
    saida = [corpo, Spacer(1, 3),
             rodape_do_geral(m, n_topicos or sum(1 for x in linhas if x[0]))]
    if linhas_pautadas:
        saida += [Spacer(1, 10), pauta(linhas_pautadas)]
    return saida


def tabela_registro(linhas):
    cab = ["Filtro", "Data", "Total", "Acertos", "Erros", "% Bruto", "% Líq.", "Veredito"]
    proporcoes = [0.26, 0.09, 0.07, 0.08, 0.07, 0.09, 0.08, 0.26]
    dados = [[Paragraph(c, CABECA) for c in cab]] + [[""] * len(cab) for _ in range(linhas)]
    t = Table(dados, colWidths=[LARGURA_UTIL * p for p in proporcoes],
              rowHeights=[7 * mm] + [7.2 * mm] * linhas, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DESTAQUE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.4, LINHA),
        ("BOX", (0, 0), (-1, -1), 0.7, CLARO),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ZEBRA]),
    ]))
    return t


def folha_do_registro(linhas_do_historico=None):
    return [
        Paragraph("REGISTRO DOS SIMULADOS DESTA MATÉRIA", SECAO),
        Spacer(1, 4),
        tabela_registro(linhas_do_historico or LINHAS_DO_HISTORICO),
    ]


def doc_em_branco(destino, materia=None, dia=""):
    titulo = materia["nome"].upper() if materia else "medida"
    sub = (f"{materia['bloco']} · {dia} · {len(materia['ementa'])} tópicos · "
           f"{materia['itens_estimados']} itens estimados do edital") if materia else ""
    return documento(destino, titulo, sub,
                     "TCDF / ANACE 2026 · mapa da ementa por filtro do Gran — meta 90% bruto",
                     margem=MARGEM, tamanho=PAGINA, faixa=FAIXA, topo=TOPO, base=BASE)


def cabe_em_uma_folha(flowables) -> bool:
    doc = doc_em_branco(BytesIO())
    try:
        doc.build(flowables)
    except LayoutError:
        return False
    return doc.page == 1


def layout_da_materia(linhas):
    """Primeiro layout que fecha o mapa em uma folha, mais o respiro que sobra.

    Uma coluna alta demais estoura o frame como LayoutError em vez de paginar —
    a tabela de cada metade e indivisivel de proposito, para o mapa nao quebrar
    no meio. Nos dois casos a leitura e a mesma: nao coube, tenta o proximo.
    """
    for colunas, escala in LAYOUTS:
        m = Medidas(colunas, escala)
        if not cabe_em_uma_folha(folha_do_mapa(linhas, m)):
            continue
        respiro = 0.0
        while respiro < PADDING_MAXIMO:
            passo = round(respiro + 0.25, 2)
            if not cabe_em_uma_folha(folha_do_mapa(linhas, m, passo)):
                break
            respiro = passo
        # O que ainda sobra da folha vira pauta de anotacao, em vez de branco.
        pautadas = 0
        for n in range(14, 2, -1):
            if cabe_em_uma_folha(folha_do_mapa(linhas, m, respiro, n)):
                pautadas = n
                break
        return m, respiro, pautadas, True
    return Medidas(*LAYOUTS[-1]), 0.0, 0, False


def historico_que_cabe() -> int:
    """Maior numero de linhas do historico que ainda fecha a folha 2 em uma pagina."""
    for n in range(40, 5, -1):
        if cabe_em_uma_folha(folha_do_registro(n)):
            return n
    return 6


def pdf_da_materia(materia, gran, estado, dia):
    aulas = aulas_da_materia(gran, materia["id"])
    linhas = linhas_da_materia(materia, aulas, estado)
    m, respiro, pautadas, coube = layout_da_materia(linhas)
    arq = SAIDA / f"{slug(materia['nome'])}.pdf"
    doc = doc_em_branco(str(arq), materia, dia)
    doc.build(folha_do_mapa(linhas, m, respiro, pautadas) + [PageBreak()] + folha_do_registro())
    return arq, len(linhas), m, respiro, pautadas, doc.page, coube


def main() -> int:
    ed = json.loads((RAIZ / "scripts" / "edital.json").read_text(encoding="utf-8"))
    prog = json.loads((RAIZ / "scripts" / "progressao.json").read_text(encoding="utf-8"))
    gran = json.loads((RAIZ / "scripts" / "gran.json").read_text(encoding="utf-8"))
    mats = {m["id"]: m for m in ed["materias"]}
    estado = ler_progresso(mats)
    dia = {b["id"]: g["dia"] for g in prog["grupos"] for b in g["materias"]}

    global LINHAS_DO_HISTORICO
    LINHAS_DO_HISTORICO = historico_que_cabe()
    print(f"folha 2: {LINHAS_DO_HISTORICO} linhas de registro")

    alvos = sys.argv[1:] or list(mats)
    SAIDA.mkdir(parents=True, exist_ok=True)
    problemas = 0
    for mid in alvos:
        if mid not in mats:
            print(f"materia desconhecida: {mid}")
            return 1
        arq, n, m, respiro, pautadas, paginas, coube = pdf_da_materia(
            mats[mid], gran, estado, dia.get(mid, "—"))
        ok = coube and paginas == 2
        problemas += 0 if ok else 1
        print(f"{arq.name}: {n} linhas · {m.colunas} coluna(s) · corpo {m.escala}pt · "
              f"respiro {respiro:.2f}pt · pauta {pautadas} · "
              f"{paginas} folhas{'' if ok else '  <-- NAO FECHOU'}")
    return 1 if problemas else 0


if __name__ == "__main__":
    raise SystemExit(main())
