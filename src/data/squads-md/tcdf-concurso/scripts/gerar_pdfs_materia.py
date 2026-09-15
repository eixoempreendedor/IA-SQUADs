#!/usr/bin/env python3
"""Gera um PDF por materia: a ementa inteira cruzada com os filtros do Gran.

Duas folhas em pe (A4 retrato):

  FOLHA 1 — MAPA DA EMENTA x FILTROS. Cada topico e cada subtopico do edital em
  uma linha, com a aula do curso ao lado e uma bolinha em cada coluna de filtro.
  O nome do filtro vai escrito a mao, em pe, no cabecalho da coluna; as bolinhas
  marcadas dizem o que aquele filtro esta sorteando.

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
    CABECA, CELULA, CLARO, DESTAQUE, LINHA, NOTA, SECAO,
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
        self.l_filtro = min(7 * mm, max(5.6 * mm, 0.62 * mm * escala))
        self.l_aula = max(9 * mm, 0.85 * mm * escala)
        self.l_coluna = (LARGURA_UTIL - CALHA) / 2 if colunas == 2 else LARGURA_UTIL
        self.l_texto = self.l_coluna - self.l_aula - N_FILTROS * self.l_filtro
        self.larguras = [self.l_texto, self.l_aula] + [self.l_filtro] * N_FILTROS
        self.raio = min(2.3 * mm, self.l_filtro * 0.28)
        self.padding = max(PADDING_MINIMO, escala * 0.14)
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


def aulas_da_materia(gran: dict, mid: str) -> dict[str, list[int]]:
    saida: dict[str, list[int]] = {}
    for a in gran["materias"].get(mid, []):
        for n in a["topicos"]:
            saida.setdefault(n, []).append(a["aula"])
    return saida


def linhas_da_materia(materia, aulas, estado):
    """[(e_topico, texto, aula, bolinha_cheia)] na ordem da ementa."""
    saida = []
    for t in materia["ementa"]:
        n = t["n"]
        numero, titulo, subs = partes(t["texto"])
        e = estado["estudo"].get((materia["id"], n), {})
        vistos = set(e.get("subtopicos", []))
        ag = ", ".join(str(x) for x in aulas.get(n, [])) or "—"
        saida.append((True, f"<b>{numero or n}.</b> {titulo}", ag,
                      bool(e) and e.get("completo", True)))
        for s in subs:
            saida.append((False, s, "", s.split()[0] in vistos))
        for s in t.get("subtopicos_sugeridos", []):
            saida.append((False, f"{s} <font size=5.5>(sugerido)</font>", "", False))
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
    caixas = ["", ""] + [CaixaDoFiltro(m.l_filtro) for _ in range(N_FILTROS)]
    rotulos = [Paragraph("TÓPICO E SUBTÓPICO DO EDITAL", MINI), Paragraph("AULA", MINI)] + \
              [Paragraph(f"F{i}", MINI) for i in range(1, N_FILTROS + 1)]
    dados, marcas, zebra = [caixas, rotulos], [], []

    for i, (e_topico, texto, aula, cheia) in enumerate(linhas):
        if e_topico and len(dados) > 2:
            marcas.append(("LINEABOVE", (0, len(dados)), (-1, len(dados)), 0.5, CLARO))
        if i % 2:
            zebra.append(("BACKGROUND", (0, len(dados)), (-1, len(dados)), ZEBRA))
        dados.append([Paragraph(texto, m.topico if e_topico else m.sub),
                      Paragraph(aula, m.aula)] +
                     [Bolinha(raio=m.raio, cheia=cheia) for _ in range(N_FILTROS)])

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
        ("TOPPADDING", (0, 2), (-1, -1), m.padding + respiro),
        ("BOTTOMPADDING", (0, 2), (-1, -1), m.padding + respiro),
        ("LINEBEFORE", (2, 1), (2, -1), 0.7, CLARO),
        ("BOX", (0, 1), (-1, -1), 0.7, CLARO),
    ] + zebra + marcas))
    return t


def nota_de_uso():
    return Paragraph(
        "Escreva o nome do filtro em pé na caixa tracejada e marque a bolinha de cada tópico e "
        "subtópico que ele sorteia — a coluna vira o retrato do filtro, e linha sem bolinha "
        "nenhuma é conteúdo que filtro nenhum testa. <b>AULA</b> = videoaula do Gran que cobre o "
        "tópico (o curso reordena o programa, não segue a numeração do edital).", NOTA)


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


def folha_do_mapa(linhas, m: Medidas, respiro=0.0, linhas_pautadas=0):
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
    saida = [nota_de_uso(), Spacer(1, 5), corpo]
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
        Paragraph(
            "Uma linha por lote resolvido. <b>Bruto</b> = acertos ÷ total, é ele que decide o "
            "avanço; <b>líquido</b> = (acertos − erros) ÷ total, é a régua da prova, onde cada erro "
            "anula um acerto. Branco conta como erro: responda o lote inteiro. Em <i>filtro</i>, "
            "repita o nome que você escreveu na coluna da folha 1; no <i>veredito</i>, anote se o "
            "lote foi tentativa oficial de Nível 1 (tópico inteiro, 20 questões) ou aferição.", NOTA),
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
