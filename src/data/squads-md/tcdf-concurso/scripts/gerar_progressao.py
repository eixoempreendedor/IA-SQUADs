#!/usr/bin/env python3
"""Gera a documentacao do sistema de progressao por niveis e valida a consistencia.

Le scripts/progressao.json + scripts/edital.json e escreve:
  - data/grupos-de-conteudo.md   (tabela dos 6 grupos, seg a sab, com as cotas de questoes)
  - templates/mapa-de-progressao.md  (folha de acompanhamento com as 21 materias)

Uso:
    python3 scripts/gerar_progressao.py
    python3 scripts/gerar_progressao.py --check   # so valida
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PROG = RAIZ / "scripts" / "progressao.json"
EDITAL = RAIZ / "scripts" / "edital.json"


def blocos(grupo: dict) -> list:
    """Um grupo simples rende um bloco; um grupo com rotacao rende um por variante."""
    return [grupo] if "materias" in grupo else grupo["variantes"]


def validar(prog: dict, materias: dict) -> list[str]:
    erros, vistas = [], []
    for g in prog["grupos"]:
        soma_itens = 0
        for b in blocos(g):
            total_q = sum(m["questoes_n2"] for m in b["materias"])
            if total_q != prog["sistema"]["niveis"][1]["questoes"]:
                erros.append(f"{g['id']}/{b.get('id', '-')}: questoes_n2 somam {total_q}, esperado 50")
            for m in b["materias"]:
                vistas.append(m["id"])
                soma_itens += m["itens"]
                if m["id"] not in materias:
                    erros.append(f"{m['id']}: materia inexistente no edital.json")
                elif materias[m["id"]]["itens_estimados"] != m["itens"]:
                    erros.append(
                        f"{m['id']}: itens {m['itens']} divergem do edital "
                        f"({materias[m['id']]['itens_estimados']})"
                    )
        if soma_itens != g["itens_edital"]:
            erros.append(f"{g['id']}: itens_edital {g['itens_edital']} != soma das materias {soma_itens}")
    faltando = sorted(set(materias) - set(vistas))
    duplicadas = sorted({x for x in vistas if vistas.count(x) > 1})
    if faltando:
        erros.append("materias sem grupo: " + ", ".join(faltando))
    if duplicadas:
        erros.append("materias em mais de um grupo: " + ", ".join(duplicadas))
    return erros


def doc_grupos(prog: dict, materias: dict) -> str:
    s = prog["sistema"]
    crit = s["criterio_de_aprovacao"]
    out = [
        "# Grupos de conteudo — progressao por niveis",
        "",
        "> GERADO por `scripts/gerar_progressao.py` a partir de `scripts/progressao.json`. Nao edite a mao.",
        "",
        f"Fonte das questoes: **{s['fonte_das_questoes']}**. "
        f"Criterio de aprovacao: **{crit['metrica']}** = `{crit['formula']}` >= **{crit['meta']:.0%}**.",
        "",
        crit["observacao"],
        "",
        "## Os tres niveis",
        "",
        "| Nivel | Unidade | Questoes | Quando | Meta | Aprovado gera |",
        "|---|---|---|---|---|---|",
    ]
    for n in s["niveis"]:
        out.append(
            f"| **{n['nivel']} — {n['nome']}** | {n['unidade']} | {n['questoes']} | "
            f"{n['quando']} | {n['meta']:.0%} | {n['aprovado_gera']} |"
        )
    out += ["", "## Semana", "", "| Dia | Grupo | Itens no edital | Materias |", "|---|---|---|---|"]
    for g in prog["grupos"]:
        for b in blocos(g):
            nome = g["nome"] if "materias" in g else f"{g['nome']} — variante {b['id']} ({b['nome']}, semanas {b['semanas']})"
            nomes = ", ".join(materias[m["id"]]["nome"] for m in b["materias"])
            out.append(f"| {g['dia']} | **{nome}** | {g['itens_edital']} | {nomes} |")
    out += ["| Domingo | **Nivel 3 — simulado geral** | pool vencido | Todas as materias ja vencidas no Nivel 2 |", ""]
    out += ["## Composicao de cada simulado de Nivel 2 (50 questoes)", ""]
    for g in prog["grupos"]:
        for b in blocos(g):
            titulo = g["nome"] if "materias" in g else f"{g['nome']} — variante {b['id']}: {b['nome']}"
            out += [f"### {g['dia']} · {titulo}", ""]
            if "materias" in g:
                out += [f"*{g['tese']}*", ""]
            out += ["| Materia | Itens no edital | Questoes no simulado |", "|---|---|---|"]
            for m in b["materias"]:
                out.append(f"| {materias[m['id']]['nome']} | {m['itens']} | **{m['questoes_n2']}** |")
            out += [f"| **Total** | **{sum(m['itens'] for m in b['materias'])}** | **{sum(m['questoes_n2'] for m in b['materias'])}** |", ""]
    out += [
        "## Rotina",
        "",
        f"- **Manha (seg a sab):** {s['rotina_diaria']['manha']}",
        f"- **Tarde/noite (seg a sab):** {s['rotina_diaria']['tarde_noite']}",
        f"- **Domingo:** {s['rotina_diaria']['domingo']}",
        "",
        "Tempo-alvo: "
        + " · ".join(f"**Nivel {k[-1]}** {v}" for k, v in s["tempo_alvo"].items()),
        "",
        "## Regras de avanco e regressao",
        "",
    ]
    for n in s["niveis"]:
        out += [f"**Nivel {n['nivel']} — {n['nome']}**", ""]
        if n.get("pre_requisito"):
            out.append(f"- Pre-requisito: {n['pre_requisito']}")
        if n.get("composicao"):
            out.append(f"- Composicao: {n['composicao']}")
        if n.get("inicio"):
            out.append(f"- Inicio: {n['inicio']}")
        out.append(f"- Aprovado ({n['meta']:.0%}+): {n['aprovado_gera']}")
        if n.get("reprovado_gera"):
            out.append(f"- Reprovado: {n['reprovado_gera']}")
        if n.get("regressao"):
            out.append(f"- Regressao: {n['regressao']}")
        out.append("")
    return "\n".join(out) + "\n"


def mapa(prog: dict, materias: dict) -> str:
    out = [
        "# Mapa de progressao — TCDF/ANACE",
        "",
        "> GERADO por `scripts/gerar_progressao.py`. Copie para onde voce acompanha (planilha, Notion, papel) e atualize a cada simulado.",
        "",
        "Status: `—` nao iniciado · `N1` temas em andamento · `N1 OK` todos os temas vencidos · "
        "`N2` em simulado de grupo · **`VENCIDA`** aprovada com 90% e no pool do Nivel 3 · `REGREDIU` voltou ao Nivel 2.",
        "",
        "| Dia | Grupo | Materia | Itens | Temas vencidos (N1) | Melhor N2 | Status | Ultimo N3 |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for g in prog["grupos"]:
        for b in blocos(g):
            rotulo = g["nome"] if "materias" in g else f"{g['nome']} ({b['id']})"
            for m in b["materias"]:
                info = materias[m["id"]]
                temas = len(info["ementa"])
                out.append(
                    f"| {g['dia']} | {rotulo} | {info['icone']} {info['nome']} | {m['itens']} | "
                    f"0 / {temas} |  | — |  |"
                )
    out += [
        "",
        "## Pool do Nivel 3",
        "",
        "| Materias vencidas | Itens somados | % da prova | Questoes no domingo |",
        "|---|---|---|---|",
        "| 0 | 0 | 0% | — (minimo de 30 itens para iniciar) |",
        "",
        "A cota de cada materia no simulado de 200 questoes e proporcional: "
        "`questoes = 200 x (itens da materia / itens somados do pool)`.",
        "",
        "## Registro semanal",
        "",
        "| Domingo | Materias no pool | Questoes | Acertos | Erros | Liquido | % | Materias abaixo de 90% |",
        "|---|---|---|---|---|---|---|---|",
        "|  |  |  |  |  |  |  |  |",
        "",
    ]
    return "\n".join(out) + "\n"


def main() -> int:
    check = "--check" in sys.argv
    prog = json.loads(PROG.read_text(encoding="utf-8"))
    materias = {m["id"]: m for m in json.loads(EDITAL.read_text(encoding="utf-8"))["materias"]}

    erros = validar(prog, materias)
    for e in erros:
        print("ERRO:", e)
    if erros:
        return 1

    if not check:
        (RAIZ / "data" / "grupos-de-conteudo.md").write_text(doc_grupos(prog, materias), encoding="utf-8")
        (RAIZ / "templates" / "mapa-de-progressao.md").write_text(mapa(prog, materias), encoding="utf-8")

    n_grupos = len(prog["grupos"])
    n_blocos = sum(len(blocos(g)) for g in prog["grupos"])
    print(f"{n_grupos} grupos ({n_blocos} variantes de simulado) cobrindo {len(materias)} materias — consistente")
    if check:
        print("modo --check: nenhum arquivo foi escrito")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
