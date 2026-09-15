#!/usr/bin/env python3
"""Gera um PDF por materia: a ementa inteira cruzada com os filtros do Gran.

A folha de cada materia tem tres partes:

  1. MAPA DA EMENTA x FILTROS — cada topico e cada subtopico do edital em uma
     linha, com a aula do curso ao lado e uma bolinha em cada coluna de filtro.
     O nome do filtro vai escrito a mao no cabecalho da coluna; as bolinhas
     marcadas dizem o que aquele filtro esta sorteando.
  2. RESULTADO DE CADA FILTRO — no pe das mesmas colunas, data, total, acertos
     e percentual do ultimo lote daquele filtro.
  3. REGISTRO DOS SIMULADOS — historico corrido: filtro, data, total, acertos,
     erros, bruto e liquido.

Uso:
    python3 scripts/gerar_pdfs_materia.py                      # todas as materias
    python3 scripts/gerar_pdfs_materia.py direito-administrativo
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import Flowable, KeepTogether, Paragraph, Spacer, Table, TableStyle

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))

from gerar_pdfs import (  # noqa: E402
    CABECA, CELULA, CINZA, CLARO, DESTAQUE, FUNDO, LINHA, NOTA, SECAO,
    Bolinha, caixa, documento, partes, slug,
)
from gerar_status import ler_progresso  # noqa: E402

SAIDA = RAIZ / "pdf" / "materias"
MARGEM = 18 * mm
N_FILTROS = 8

L_TEXTO = 104 * mm
L_AULA = 14 * mm
L_FILTRO = 7 * mm
LARGURAS = [L_TEXTO, L_AULA] + [L_FILTRO] * N_FILTROS
LARGURA_TOTAL = sum(LARGURAS)

ITEM = CELULA.clone("item", fontSize=8.6, leading=10.8)
ITEM_TOP = ITEM.clone("itemtop", fontName="Helvetica-Bold")
ITEM_SUB = ITEM.clone("itemsub", fontSize=8, leading=10, textColor=colors.HexColor("#374151"),
                      leftIndent=9)
AULA = CELULA.clone("aula", fontSize=7.4, leading=9, textColor=DESTAQUE)
MINI = CABECA.clone("mini", fontSize=6.5, leading=8)


class CaixaDoFiltro(Flowable):
    """Cabecalho da coluna: caixa alta e vazia, para escrever o nome do filtro em pe."""

    def __init__(self, largura=L_FILTRO - 1.4 * mm, altura=27 * mm):
        super().__init__()
        self.width, self.height = largura, altura

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


def linha(texto, estilo, aula="", cheia=False):
    return [Paragraph(texto, estilo), Paragraph(aula, AULA)] + \
           [Bolinha(raio=2.0 * mm, cheia=cheia) for _ in range(N_FILTROS)]


def tabela_caixas_de_filtro():
    """Faixa onde o nome de cada filtro e escrito em pe, alinhada com as colunas do mapa."""
    dados = [[Paragraph("Escreva aqui, em pé, o nome de cada filtro que você montar no Gran  →",
                        NOTA), ""] + [CaixaDoFiltro() for _ in range(N_FILTROS)]]
    t = Table(dados, colWidths=LARGURAS, rowHeights=[29 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (1, 0), "BOTTOM"),
        ("VALIGN", (2, 0), (-1, 0), "MIDDLE"),
        ("ALIGN", (0, 0), (1, 0), "RIGHT"),
        ("ALIGN", (2, 0), (-1, 0), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, 0), 0),
        ("RIGHTPADDING", (0, 0), (1, 0), 6),
        ("RIGHTPADDING", (2, 0), (-1, 0), 0),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 4),
    ]))
    return t


def tabela_mapa(materia, aulas, estado):
    rotulos = [Paragraph("TÓPICO E SUBTÓPICO DO EDITAL", CABECA), Paragraph("AULA", CABECA)] + \
              [Paragraph(f"F{i}", MINI) for i in range(1, N_FILTROS + 1)]
    dados, estilos = [rotulos], []
    alturas = [6.5 * mm]

    for t in materia["ementa"]:
        n = t["n"]
        numero, titulo, subs = partes(t["texto"])
        e = estado["estudo"].get((materia["id"], n), {})
        vistos = set(e.get("subtopicos", []))
        ag = ", ".join(str(x) for x in aulas.get(n, [])) or "—"
        if len(dados) > 1:
            estilos.append(("LINEABOVE", (0, len(dados)), (-1, len(dados)), 0.6, CLARO))
        dados.append(linha(f"<b>{numero or n}.</b> {titulo}", ITEM_TOP, ag,
                           cheia=bool(e) and e.get("completo", True)))
        alturas.append(None)
        for s in subs:
            dados.append(linha(s, ITEM_SUB, cheia=s.split()[0] in vistos))
            alturas.append(None)
        for s in t.get("subtopicos_sugeridos", []):
            dados.append(linha(f"{s} <font size=6.5>(sugerido)</font>", ITEM_SUB))
            alturas.append(None)

    t = Table(dados, colWidths=LARGURAS, rowHeights=alturas, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DESTAQUE),
        ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),
        ("VALIGN", (0, 1), (-1, -1), "TOP"),
        ("ALIGN", (2, 0), (-1, -1), "CENTER"),
        ("ALIGN", (1, 1), (1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (0, -1), 4),
        ("LEFTPADDING", (1, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 1), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 2.5),
        ("LINEBEFORE", (2, 0), (2, -1), 0.8, CLARO),
        ("BOX", (0, 0), (-1, -1), 0.8, CLARO),
    ] + estilos))
    return t


def tabela_resultado_por_filtro():
    """Pe das colunas: o ultimo lote de cada filtro, alinhado com o mapa acima."""
    rotulos = ["Nome do filtro", "Data do último lote", "Total de questões",
               "Acertos", "% bruto (meta 90%)"]
    dados = [[Paragraph(f"<b>{r}</b>" if i == 0 else r, CELULA), ""] + [""] * N_FILTROS
             for i, r in enumerate(rotulos)]
    dados.insert(0, [Paragraph("RESULTADO DE CADA FILTRO", CABECA), ""] +
                 [Paragraph(f"F{i}", MINI) for i in range(1, N_FILTROS + 1)])
    t = Table(dados, colWidths=LARGURAS,
              rowHeights=[6.5 * mm] + [7.5 * mm] * len(rotulos), repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DESTAQUE),
        ("SPAN", (0, 0), (1, 0)),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (2, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (0, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.4, LINHA),
        ("BOX", (0, 0), (-1, -1), 0.8, CLARO),
        ("SPAN", (0, 1), (1, 1)),
        ("SPAN", (0, 2), (1, 2)),
        ("SPAN", (0, 3), (1, 3)),
        ("SPAN", (0, 4), (1, 4)),
        ("SPAN", (0, 5), (1, 5)),
        ("ROWBACKGROUNDS", (0, 1), (1, -1), [FUNDO, colors.white]),
    ]))
    return t


def tabela_registro(linhas=12):
    cab = ["Filtro", "Data", "Total", "Acertos", "Erros", "% Bruto", "% Líq.", "Veredito"]
    larguras = [46 * mm, 20 * mm, 15 * mm, 18 * mm, 15 * mm, 18 * mm, 16 * mm, 26 * mm]
    dados = [[Paragraph(c, CABECA) for c in cab]] + [[""] * len(cab) for _ in range(linhas)]
    t = Table(dados, colWidths=larguras, rowHeights=[7 * mm] + [7.5 * mm] * linhas, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DESTAQUE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.4, LINHA),
        ("BOX", (0, 0), (-1, -1), 0.7, CLARO),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fafafa")]),
    ]))
    return t


def pdf_da_materia(materia, gran, estado, dia):
    aulas = aulas_da_materia(gran, materia["id"])
    n_top = len(materia["ementa"])
    peso = sum(t["peso"] for t in materia["ementa"])
    arq = SAIDA / f"{slug(materia['nome'])}.pdf"
    doc = documento(arq, materia["nome"].upper(),
                    f"{materia['bloco']} · {dia}",
                    "TCDF / ANACE 2026 · mapa da ementa por filtro do Gran — meta 90% bruto",
                    margem=MARGEM)

    hist = [caixa(largura=LARGURA_TOTAL, texto_html=(
        f"<b>{materia['nome']}</b> — {n_top} tópicos · {materia['itens_estimados']} itens estimados "
        f"do edital · bloco {materia['bloco']} · estudada na <b>{dia}</b><br/><br/>"
        "<b>Como usar:</b> monte o filtro no Gran, escreva o nome dele em pé no cabeçalho de uma "
        "coluna (F1, F2, …) e marque a bolinha de cada tópico e subtópico que aquele filtro está "
        "sorteando. A coluna passa a ser o retrato do filtro: o que ele cobre e o que ele deixa de "
        "fora.<br/>"
        "<font size=8 color='#6b7280'>A coluna <i>AULA</i> traz o número da aula do curso que cobre "
        "o tópico — o Gran fatia e reordena o programa, então a numeração das aulas não é a do "
        "edital. Um tópico sem bolinha marcada em nenhuma coluna é conteúdo que nenhum filtro seu "
        "está testando.</font>"))]
    hist.append(Spacer(1, 8))
    hist.append(Paragraph("MAPA DA EMENTA × FILTROS", SECAO))
    hist.append(tabela_caixas_de_filtro())
    hist.append(tabela_mapa(materia, aulas, estado))
    hist.append(Spacer(1, 10))
    hist.append(KeepTogether(tabela_resultado_por_filtro()))
    hist.append(Spacer(1, 12))

    hist.append(KeepTogether([
        Paragraph("REGISTRO DOS SIMULADOS DESTA MATÉRIA", SECAO),
        Paragraph(
            "Uma linha por lote resolvido. <b>Bruto</b> = acertos ÷ total, é ele que decide o "
            "avanço; <b>líquido</b> = (acertos − erros) ÷ total, é a régua da prova, onde cada "
            "erro anula um acerto. Branco conta como erro: responda o lote inteiro. No "
            "<i>veredito</i>, anote se o lote foi tentativa oficial de Nível 1 (tópico inteiro, "
            "20 questões) ou aferição.", NOTA),
        Spacer(1, 4),
        tabela_registro(),
    ]))

    doc.build(hist)
    return arq, n_top, peso


def main() -> int:
    ed = json.loads((RAIZ / "scripts" / "edital.json").read_text(encoding="utf-8"))
    prog = json.loads((RAIZ / "scripts" / "progressao.json").read_text(encoding="utf-8"))
    gran = json.loads((RAIZ / "scripts" / "gran.json").read_text(encoding="utf-8"))
    mats = {m["id"]: m for m in ed["materias"]}
    estado = ler_progresso(mats)
    dia = {b["id"]: g["dia"] for g in prog["grupos"] for b in g["materias"]}

    alvos = sys.argv[1:] or list(mats)
    SAIDA.mkdir(parents=True, exist_ok=True)
    for mid in alvos:
        if mid not in mats:
            print(f"materia desconhecida: {mid}")
            return 1
        arq, n_top, peso = pdf_da_materia(mats[mid], gran, estado, dia.get(mid, "—"))
        print(f"{arq.relative_to(RAIZ)}: {n_top} topicos, peso {peso}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
