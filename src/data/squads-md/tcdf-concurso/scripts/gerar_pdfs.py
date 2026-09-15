#!/usr/bin/env python3
"""Gera um PDF de checklist por dia da semana, a partir dos grupos de conteudo.

Cada PDF traz:
  - cabecalho do dia, o grupo e a meta do simulado de Nivel 2
  - registro de simulados do dia (data, total, acertos, % bruto, % liquido, veredito)
  - checklist com uma bolinha por topico e uma bolinha por subtopico,
    com campo para anotar o resultado do lote de Nivel 1 (__/20)
  - domingo recebe o PDF do Nivel 3 (registro geral e acompanhamento dos grupos)

Uso:
    python3 scripts/gerar_pdfs.py            # escreve em pdf/
"""
from __future__ import annotations

import json
import re
import unicodedata
import sys
from pathlib import Path

import cotas
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Flowable, Frame, KeepTogether, PageTemplate,
    Paragraph, Spacer, Table, TableStyle,
)

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "pdf"
sys.path.insert(0, str(RAIZ / "scripts"))

from gerar_status import ler_progresso  # noqa: E402

TINTA = colors.HexColor("#1a1a1a")
CINZA = colors.HexColor("#6b7280")
CLARO = colors.HexColor("#d1d5db")
LINHA = colors.HexColor("#e5e7eb")
DESTAQUE = colors.HexColor("#6d28d9")
FUNDO = colors.HexColor("#f5f3ff")

CORPO = ParagraphStyle("corpo", fontName="Helvetica", fontSize=9, leading=11.5,
                       textColor=TINTA, alignment=TA_LEFT)
TOPICO = ParagraphStyle("topico", parent=CORPO, fontSize=9.5, leading=12)
SUB = ParagraphStyle("sub", parent=CORPO, fontSize=8.2, leading=10.4, textColor=colors.HexColor("#374151"))
MATERIA = ParagraphStyle("materia", fontName="Helvetica-Bold", fontSize=10.5, leading=13,
                         textColor=DESTAQUE, spaceBefore=7, spaceAfter=3)
SECAO = ParagraphStyle("secao", fontName="Helvetica-Bold", fontSize=8.5, leading=11,
                       textColor=CINZA, spaceBefore=4, spaceAfter=3)
NOTA = ParagraphStyle("nota", fontName="Helvetica-Oblique", fontSize=7.6, leading=9.6, textColor=CINZA)
CABECA = ParagraphStyle("cabeca", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=colors.white)
CELULA = ParagraphStyle("celula", fontName="Helvetica", fontSize=8, leading=10, textColor=TINTA)


class Bolinha(Flowable):
    """Checkbox circular, desenhada para nao depender de glifo de fonte."""

    def __init__(self, raio=2.3 * mm, espessura=0.7, cor=colors.HexColor("#9ca3af"), cheia=False):
        super().__init__()
        self.raio, self.espessura, self.cor, self.cheia = raio, espessura, cor, cheia
        self.width = self.height = raio * 2

    def draw(self):
        c = self.canv
        c.setStrokeColor(self.cor)
        c.setLineWidth(self.espessura)
        c.circle(self.raio, self.raio - 0.6 * mm, self.raio, stroke=1, fill=0)
        if self.cheia:
            # Marcada ja na impressao: o que o candidato declarou em progresso.json
            c.setFillColor(self.cor)
            c.circle(self.raio, self.raio - 0.6 * mm, self.raio - 0.85, stroke=0, fill=1)


def slug(texto: str) -> str:
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def partes(texto: str):
    """Separa '4 Titulo: 4.1 um; 4.2 outro' em (numero, titulo, [subtopicos])."""
    m = re.match(r"^(\d+)\s+(.*)$", texto.strip(), re.S)
    numero, resto = (m.group(1), m.group(2)) if m else ("", texto)
    if ":" in resto:
        titulo, cauda = resto.split(":", 1)
        subs = [s.strip() for s in re.split(r";\s*(?=\d+\.\d)", cauda.strip()) if s.strip()]
        if len(subs) == 1 and not re.match(r"^\d+\.\d", subs[0]):
            return numero, resto.strip(), []
        return numero, titulo.strip(), subs
    return numero, resto.strip(), []


def linha_topico(numero, titulo, peso, com_campo=True, q_n2=None, aulas=None,
                 estudado=False, vencido=False):
    marca = f" <font size=7 color='#6d28d9'>[Gran {', '.join(str(a) for a in aulas)}]</font>" if aulas else ""
    direita = f"peso {peso} · N2: {q_n2}q<br/>N1: ____ / 20" if com_campo else f"peso {peso}"
    t = Table([[
        Bolinha(cor=colors.HexColor("#c4b5fd"), cheia=estudado),
        Bolinha(cheia=vencido),
        Paragraph(f"<b>{numero}.</b> {titulo}{marca}", TOPICO),
        Paragraph(direita, NOTA),
    ]], colWidths=[6.5 * mm, 7 * mm, 112.5 * mm, 32 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
        ("ALIGN", (3, 0), (3, 0), "RIGHT"),
        ("LINEABOVE", (0, 0), (-1, 0), 0.4, LINHA),
    ]))
    return t


def legenda_bolinhas():
    """Cabecalho das duas colunas de marcacao, alinhado com linha_topico."""
    t = Table([[
        Paragraph("<font size=6.5 color='#6d28d9'><b>ESTUDEI</b></font>", NOTA),
        Paragraph("<font size=6.5 color='#374151'><b>VENCI</b></font>", NOTA),
        Paragraph("", NOTA),
    ]], colWidths=[13.5 * mm, 17 * mm, 127.5 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def linha_sub(texto, sugerido=False, cheia=False):
    estilo = SUB if not sugerido else ParagraphStyle("subsug", parent=SUB, textColor=CINZA)
    cor = colors.HexColor("#c4b5fd") if cheia else CLARO
    t = Table([[Bolinha(raio=1.7 * mm, cor=cor, cheia=cheia), Paragraph(texto, estilo)]],
              colWidths=[13.5 * mm, 144.5 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, 0), 14.5),
        ("LEFTPADDING", (1, 0), (1, 0), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 1.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
    ]))
    return t


def tabela_registro(titulo_extra="", linhas=10, escopo=False, rotulo_escopo="Grupo / escopo"):
    cabecalho = ["Data", "Total", "Acertos", "Erros", "% Bruto", "% Líq.", "Veredito"]
    larguras = [22 * mm, 16 * mm, 18 * mm, 16 * mm, 20 * mm, 18 * mm, 48 * mm]
    if escopo:
        cabecalho.insert(1, rotulo_escopo)
        larguras = [20 * mm, 40 * mm, 14 * mm, 16 * mm, 14 * mm, 18 * mm, 16 * mm, 20 * mm]
    dados = [[Paragraph(c, CABECA) for c in cabecalho]] + [[""] * len(cabecalho) for _ in range(linhas)]
    t = Table(dados, colWidths=larguras, rowHeights=[7 * mm] + [7.5 * mm] * linhas, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DESTAQUE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.4, LINHA),
        ("BOX", (0, 0), (-1, -1), 0.7, CLARO),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fafafa")]),
    ]))
    return t


def caixa(texto_html, fundo=FUNDO, borda=DESTAQUE, largura=158 * mm):
    t = Table([[Paragraph(texto_html, CORPO)]], colWidths=[largura])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), fundo),
        ("BOX", (0, 0), (-1, -1), 0.8, borda),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def documento(caminho, titulo: str, subtitulo: str, rodape: str, margem=26 * mm,
              tamanho=A4, faixa=20 * mm, topo=30 * mm, base=18 * mm):
    larg, alt = tamanho
    # `caminho` pode ser um buffer em memoria (o medidor de paginas usa BytesIO).
    # str() num buffer devolve "<_io.BytesIO object at 0x...>", que o reportlab
    # aceita como NOME DE ARQUIVO e grava no disco — foi assim que milhares de
    # arquivos de lixo entraram no repositorio.
    destino = caminho if isinstance(caminho, str) or hasattr(caminho, "write") else str(caminho)
    doc = BaseDocTemplate(destino, pagesize=tamanho,
                          leftMargin=margem, rightMargin=margem,
                          topMargin=topo, bottomMargin=base,
                          title=titulo, author="TCDF Concurso Squad")

    def moldura(canvas, _doc):
        canvas.saveState()
        canvas.setFillColor(DESTAQUE)
        canvas.rect(0, alt - faixa, larg, faixa, stroke=0, fill=1)
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 13)
        canvas.drawString(margem, alt - faixa * 0.675, titulo)
        canvas.setFont("Helvetica", 8.5)
        canvas.drawRightString(larg - margem, alt - faixa * 0.65, subtitulo)
        canvas.setFillColor(CINZA)
        canvas.setFont("Helvetica", 7.5)
        canvas.drawString(margem, base * 0.61, rodape)
        canvas.drawRightString(larg - margem, base * 0.61, f"pág. {canvas.getPageNumber()}")
        canvas.setStrokeColor(LINHA)
        canvas.setLineWidth(0.4)
        canvas.line(margem, base * 0.78, larg - margem, base * 0.78)
        canvas.restoreState()

    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="corpo")
    doc.addPageTemplates([PageTemplate(id="padrao", frames=[frame], onPage=moldura)])
    return doc


def pdf_do_grupo(grupo, mats, ordem, sistema, outros, gran=None, estado=None):
    gran = gran or {}
    estado = estado or {"tocados": set(), "completos": set(), "fracoes": {}, "vencidos": set(), "estudo": {}}
    r = cotas.resumo(grupo, mats)
    peso_total, n_top = r["peso"], r["topicos"]
    lote, meta = r["total"], r["meta"]
    minutos = 70 if lote == 50 else 85

    arq = SAIDA / f"{ordem}-{slug(grupo['dia'])}-{slug(grupo['nome'])}.pdf"
    doc = documento(arq, grupo["dia"].upper(), grupo["nome"],
                    "TCDF / ANACE 2026 · checklist de estudo — avanca com 90% bruto")
    hist = []

    hist.append(caixa(
        f"<b>{grupo['nome']}</b> — {peso_total} itens estimados do edital · {n_top} tópicos<br/>"
        f"<b>Simulado de Nível 2 deste dia:</b> {lote} questões · meta <b>{meta}/{lote} (90% bruto)</b> · "
        f"{minutos} minutos, pela manhã<br/>"
        f"<font size=8 color='#6b7280'>{grupo['tese']}</font>"))
    hist.append(Spacer(1, 7))

    # A manha so vira simulado oficial quando 70% do peso do grupo esta vencido.
    # Antes disso o dia roda o lote de rampa, com os topicos ja estudados.
    do_grupo = [(b["id"], n) for b in grupo["materias"] for n in b["topicos"]]
    pesos_top = {(b["id"], n): {t["n"]: t["peso"] for t in mats[b["id"]]["ementa"]}[n]
                 for b in grupo["materias"] for n in b["topicos"]}
    peso_venc = sum(p for k, p in pesos_top.items() if k in estado["vencidos"])
    pct = peso_venc / peso_total if peso_total else 0
    rampa = cotas.cotas_da_rampa(grupo, mats, estado["tocados"], estado["fracoes"]) if pct < 0.70 else {}

    if pct < 0.70:
        q_rampa = sum(rampa.values())
        if q_rampa:
            itens = "<br/>".join(
                f"&nbsp;&nbsp;{mats[mid]['nome']}, tópico {n} — <b>{q}q</b> "
                f"<font size=7.5 color='#6b7280'>({', '.join(estado['estudo'][(mid, n)].get('subtopicos', [])) or 'tópico inteiro'}"
                f"{'' if estado['estudo'][(mid, n)].get('completo', True) else ', parcial'})</font>"
                for (mid, n), q in sorted(rampa.items(), key=lambda kv: -kv[1]))
            corpo = (f"<b>A MANHÃ DE HOJE: LOTE DE RAMPA — {q_rampa} QUESTÕES</b><br/>"
                     f"O grupo tem <b>{pct:.0%}</b> do peso vencido; o simulado oficial de {lote} questões só "
                     f"decide a partir de 70%. Até lá a manhã roda só o que já foi estudado:<br/>{itens}<br/>"
                     "<font size=8 color='#6b7280'>Mesma meta de 90% e mesmo cronômetro, mas este lote "
                     "<b>não aprova nem reprova o grupo</b>: ele aponta o reforço do dia. A rampa cresce sozinha "
                     "a cada tópico novo estudado.</font>")
        else:
            corpo = (f"<b>A MANHÃ DE HOJE: NADA AINDA</b><br/>"
                     f"Nenhum tópico deste grupo foi declarado estudado, então não há lote de rampa. "
                     f"A manhã começa a rodar no primeiro tópico estudado; o simulado oficial de {lote} questões "
                     f"entra quando o grupo passar de 70% do peso vencido.<br/>"
                     "<font size=8 color='#6b7280'>Declare o que estudou em scripts/progresso.json "
                     "e rode scripts/gerar_pdfs.py para esta folha sair com a rampa do dia.</font>")
        hist.append(caixa(corpo, fundo=colors.HexColor("#fffbeb"), borda=colors.HexColor("#b45309")))
        hist.append(Spacer(1, 7))

    composicao = " · ".join(f"{mats[b['id']]['nome']}: <b>{r['por_materia'][b['id']]}q</b>" for b in grupo["materias"])
    hist.append(Paragraph(f"COMPOSIÇÃO DAS {lote} QUESTÕES", SECAO))
    hist.append(Paragraph(composicao, CORPO))
    hist.append(Paragraph(
        f"Cada tópico entra com pelo menos {cotas.COTA_MINIMA} questões — a coluna <i>N2</i> do checklist diz "
        "quantas cabem a cada um. Monte o lote no Gran seguindo essa distribuição.", NOTA))
    hist.append(Spacer(1, 9))

    hist.append(Paragraph("REGISTRO DOS SIMULADOS DESTE DIA", SECAO))
    hist.append(Paragraph(
        f"Na coluna <i>escopo</i>, diga o que o lote cobriu: <b>N2</b> ({lote} questões do grupo, meta {meta}), "
        "<b>rampa</b> (só os tópicos já estudados), <b>N1 tópico N</b> (20 questões de um tópico inteiro, meta 18) "
        "ou <b>aferição</b> (parte de um tópico, ou vários tópicos juntos). Só N2 e N1 decidem avanço — rampa e "
        "aferição medem e orientam. Branco conta como erro: responda o lote inteiro.", NOTA))
    hist.append(Spacer(1, 4))
    hist.append(tabela_registro(linhas=8, escopo=True, rotulo_escopo="Escopo"))
    hist.append(Spacer(1, 12))

    hist.append(Paragraph("CHECKLIST DE CONTEÚDO", SECAO))
    hist.append(Paragraph(
        "Cada tópico do edital tem <b>duas marcações</b>: a primeira bolinha (<font color='#6d28d9'>ESTUDEI</font>) "
        "é o conteúdo visto; a segunda (VENCI) só é marcada quando o lote de 20 questões daquele tópico fecha em "
        "18/20 — e esse lote só vale com o <b>tópico inteiro</b> estudado, todos os subtópicos marcados. Ver a "
        "aula não vence o tópico, e lote sobre meio tópico é aferição, não tentativa. As bolinhas menores são os "
        "subtópicos: elas dizem quando o tópico fechou. "
        "<font color='#6d28d9'>[Gran N]</font> = número da aula no curso que cobre aquele tópico — o curso fatia e "
        "reordena o programa, então a numeração das aulas não é a do edital.",
        NOTA))

    for b in grupo["materias"]:
        info = mats[b["id"]]
        textos = {t["n"]: t for t in info["ementa"]}
        hist.append(Paragraph(
            f"{info['nome']} <font size=8 color='#6b7280'>· {info['bloco']} · "
            f"{r['por_materia'][b['id']]} questões no simulado</font>", MATERIA))
        hist.append(legenda_bolinhas())
        fora = [t["n"] for t in info["ementa"] if t["n"] not in b["topicos"]]
        if fora:
            onde = sorted({outros[(info["id"], n)] for n in fora})
            hist.append(Paragraph(
                f"Os tópicos {', '.join(fora)} desta matéria são estudados em outro dia ({'; '.join(onde)}) — "
                "por isso a numeração abaixo tem saltos.", NOTA))
        for n in b["topicos"]:
            t = textos[n]
            numero, titulo, subs = partes(t["texto"])
            # Nenhuma bolinha sai marcada: a folha impressa e para a caneta.
            bloco = [linha_topico(numero or n, titulo, t["peso"],
                                  q_n2=r["por_topico"][(b["id"], n)],
                                  aulas=gran.get((b["id"], n)))]
            for s in subs:
                bloco.append(linha_sub(s))
            for s in t.get("subtopicos_sugeridos", []):
                bloco.append(linha_sub(f"{s} <font size=7>(subdivisão sugerida)</font>", sugerido=True))
            hist.append(KeepTogether(bloco))

    doc.build(hist)
    return arq, peso_total, n_top


def pdf_domingo(prog, mats, total_edital):
    arq = SAIDA / "7-domingo-nivel-3.pdf"
    doc = documento(arq, "DOMINGO", "Nível 3 — simulado geral",
                    "TCDF / ANACE 2026 · registro geral — avanca com 90% bruto")
    hist = [
        caixa("<b>Simulado de Nível 3</b> — 200 questões dos grupos já vencidos · meta <b>180/200 (90% bruto)</b> · "
              "4 horas, domingo de manhã<br/>"
              "Enquanto o pool somar menos de 30 de peso, rode simulado reduzido na mesma proporção (mínimo 50 questões).<br/>"
              "<font size=8 color='#6b7280'>Regressão: grupo abaixo de 90% em 2 domingos seguidos, ou abaixo de 80% "
              "em um único domingo, volta inteiro para o Nível 2.</font>"),
        Spacer(1, 10),
        Paragraph("REGISTRO DOS SIMULADOS DE DOMINGO", SECAO),
        tabela_registro(linhas=14, escopo=True),
        Spacer(1, 12),
        Paragraph("SITUAÇÃO DOS GRUPOS", SECAO),
        Paragraph("Marque o grupo quando ele passar no Nível 2 — a partir daí os tópicos dele entram no sorteio de domingo.", NOTA),
        Spacer(1, 4),
    ]

    linhas = [[Paragraph(c, CABECA) for c in
               ["", "Dia", "Grupo", "Peso", "Tópicos", "Questões no Nível 2", "Data em que venceu"]]]
    for g in prog["grupos"]:
        peso = 0
        for b in g["materias"]:
            p = {t["n"]: t["peso"] for t in mats[b["id"]]["ementa"]}
            peso += sum(p[n] for n in b["topicos"])
        n_top = sum(len(b["topicos"]) for b in g["materias"])
        linhas.append([Bolinha(), Paragraph(g["dia"][:3], CELULA), Paragraph(g["nome"], CELULA),
                       Paragraph(str(peso), CELULA), Paragraph(str(n_top), CELULA),
                       Paragraph("50", CELULA), ""])
    t = Table(linhas, colWidths=[9 * mm, 14 * mm, 62 * mm, 14 * mm, 17 * mm, 26 * mm, 26 * mm],
              rowHeights=[7 * mm] + [9 * mm] * len(prog["grupos"]))
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DESTAQUE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (1, -1), "CENTER"),
        ("ALIGN", (3, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.4, LINHA),
        ("BOX", (0, 0), (-1, -1), 0.7, CLARO),
    ]))
    hist += [t, Spacer(1, 12), Paragraph("PROJEÇÃO CONTRA O EDITAL", SECAO),
             Paragraph("O avanço é decidido pelo <b>bruto</b>, mas quem projeta a nota real é o <b>líquido</b> "
                       "(cada erro anula um acerto). Use esta tabela depois de cada simulado completo.", NOTA),
             Spacer(1, 4)]

    proj = [[Paragraph(c, CABECA) for c in ["Bloco", "Itens", "Mínimo", "% líquido", "Projeção", "Situação"]]]
    for bloco, itens, minimo in [("P1 — Conhecimentos Básicos", 35, "7,00"),
                                 ("P2 — Conhecimentos Específicos", 45, "13,00"),
                                 ("P3 — Conhecimentos Especializados", 70, "21,00"),
                                 ("TOTAL (NFPO)", 150, "45,00")]:
        proj.append([Paragraph(f"<b>{bloco}</b>" if bloco.startswith("TOTAL") else bloco, CELULA),
                     Paragraph(str(itens), CELULA), Paragraph(minimo, CELULA), "", "", ""])
    t2 = Table(proj, colWidths=[58 * mm, 16 * mm, 20 * mm, 22 * mm, 22 * mm, 30 * mm],
               rowHeights=[7 * mm] + [8.5 * mm] * 4)
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DESTAQUE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.4, LINHA),
        ("BOX", (0, 0), (-1, -1), 0.7, CLARO),
        ("BACKGROUND", (0, 4), (-1, 4), FUNDO),
    ]))
    hist += [t2, Spacer(1, 10),
             caixa("Referência rápida: <b>90% bruto ≈ 80% líquido ≈ 120 pontos</b> nas objetivas, contra o mínimo "
                   f"de 45,00. Pool completo = {total_edital} de peso (as 16 matérias do edital).",
                   fundo=colors.HexColor("#f9fafb"), borda=CLARO)]
    doc.build(hist)
    return arq


def aulas_do_gran() -> dict:
    """(materia, topico) -> [numeros das aulas do curso que cobrem o topico]."""
    arq = RAIZ / "scripts" / "gran.json"
    if not arq.exists():
        return {}
    gran = json.loads(arq.read_text(encoding="utf-8"))
    mapa: dict = {}
    for mid, aulas in gran["materias"].items():
        for a in aulas:
            for n in a["topicos"]:
                mapa.setdefault((mid, n), []).append(a["aula"])
    return mapa


def main() -> int:
    ed = json.loads((RAIZ / "scripts" / "edital.json").read_text(encoding="utf-8"))
    prog = json.loads((RAIZ / "scripts" / "progressao.json").read_text(encoding="utf-8"))
    mats = {m["id"]: m for m in ed["materias"]}
    total_edital = sum(m["itens_estimados"] for m in mats.values())

    # (materia, topico) -> dia em que ele cai, para avisar quando uma materia e repartida
    onde_estuda = {
        (b["id"], n): g["dia"]
        for g in prog["grupos"] for b in g["materias"] for n in b["topicos"]
    }
    gran = aulas_do_gran()
    estado = ler_progresso(mats)

    SAIDA.mkdir(exist_ok=True)
    for i, g in enumerate(prog["grupos"], 1):
        arq, peso, n_top = pdf_do_grupo(g, mats, i, prog["sistema"], onde_estuda, gran, estado)
        print(f"{arq.name}: {n_top} topicos, peso {peso}")
    arq = pdf_domingo(prog, mats, total_edital)
    print(f"{arq.name}: registro geral do Nivel 3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
