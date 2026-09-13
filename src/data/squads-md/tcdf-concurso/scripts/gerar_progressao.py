#!/usr/bin/env python3
"""Gera a documentacao do sistema de progressao por niveis e valida a consistencia.

Os grupos de conteudo sao formados por TOPICOS do edital, nao por materias:
uma materia pode aparecer em mais de um dia. A validacao garante que cada
topico do edital pertence a exatamente um grupo.

Le scripts/progressao.json + scripts/edital.json e escreve:
  - data/grupos-de-conteudo.md      (os 6 grupos, seg a sab, com topicos e cotas)
  - templates/mapa-de-progressao.md (folha de acompanhamento por topico)

Uso:
    python3 scripts/gerar_progressao.py
    python3 scripts/gerar_progressao.py --check   # so valida
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import cotas

RAIZ = Path(__file__).resolve().parent.parent
PROG = RAIZ / "scripts" / "progressao.json"
EDITAL = RAIZ / "scripts" / "edital.json"


def curto(texto: str, limite: int = 90) -> str:
    t = re.sub(r"^\d+\s+", "", texto)
    return t if len(t) <= limite else t[: limite - 3].rstrip() + "..."


def pesos(materia: dict) -> dict:
    return {t["n"]: t["peso"] for t in materia["ementa"]}


def peso_do_bloco(bloco: dict, materias: dict) -> int:
    p = pesos(materias[bloco["id"]])
    return sum(p[n] for n in bloco["topicos"])


def peso_do_grupo(grupo: dict, materias: dict) -> int:
    return sum(peso_do_bloco(b, materias) for b in grupo["materias"])


def validar(prog: dict, materias: dict) -> list[str]:
    erros: list[str] = []
    vistos: list[tuple[str, str]] = []
    for g in prog["grupos"]:
        try:
            r = cotas.resumo(g, materias)
        except (ValueError, KeyError) as e:
            erros.append(f"{g['id']}: nao foi possivel calcular as cotas ({e})")
            r = None
        if r:
            if sum(r["por_topico"].values()) != r["total"]:
                erros.append(f"{g['id']}: cotas por topico somam {sum(r['por_topico'].values())}, esperado {r['total']}")
            magros = [f"{mid} #{n} ({q}q)" for (mid, n), q in r["por_topico"].items() if q < cotas.COTA_MINIMA]
            if magros:
                erros.append(f"{g['id']}: topicos abaixo do piso de {cotas.COTA_MINIMA} questoes: " + ", ".join(magros))
        for b in g["materias"]:
            if b["id"] not in materias:
                erros.append(f"{g['id']}: materia inexistente '{b['id']}'")
                continue
            validos = pesos(materias[b["id"]])
            for n in b["topicos"]:
                if n not in validos:
                    erros.append(f"{g['id']}/{b['id']}: topico {n} nao existe na ementa")
                else:
                    vistos.append((b["id"], n))

    todos = {(m["id"], t["n"]) for m in materias.values() for t in m["ementa"]}
    faltando = sorted(todos - set(vistos))
    duplicados = sorted({x for x in vistos if vistos.count(x) > 1})
    for mid, n in faltando:
        erros.append(f"topico sem grupo: {mid} #{n}")
    for mid, n in duplicados:
        erros.append(f"topico em mais de um grupo: {mid} #{n}")

    # Regra firme: materia nao se reparte entre dias.
    dias_por_materia: dict[str, set] = {}
    for g in prog["grupos"]:
        for b in g["materias"]:
            dias_por_materia.setdefault(b["id"], set()).add(g["dia"])
    for mid, dias in sorted(dias_por_materia.items()):
        if len(dias) > 1:
            erros.append(f"materia repartida entre dias: {mid} aparece em {', '.join(sorted(dias))}")
    for mid, m in materias.items():
        for g in prog["grupos"]:
            for b in g["materias"]:
                if b["id"] == mid and len(b["topicos"]) != len(m["ementa"]):
                    faltam = sorted({t["n"] for t in m["ementa"]} - set(b["topicos"]))
                    erros.append(f"{mid}: grupo {g['id']} nao leva a materia inteira (faltam os topicos {', '.join(faltam)})")

    soma = sum(peso_do_grupo(g, materias) for g in prog["grupos"])
    total_edital = sum(m["itens_estimados"] for m in materias.values())
    if soma != total_edital:
        erros.append(f"peso somado dos grupos ({soma}) != itens estimados do edital ({total_edital})")
    return erros


def doc_grupos(prog: dict, materias: dict) -> str:
    s = prog["sistema"]
    crit = s["criterio_de_aprovacao"]
    out = [
        "# Grupos de conteudo — progressao por niveis",
        "",
        "> GERADO por `scripts/gerar_progressao.py` a partir de `scripts/progressao.json`. Nao edite a mao.",
        "",
        f"Fonte das questoes: **{s['fonte_das_questoes']}**.",
        "",
        f"**Criterio de avanco: {crit['metrica']} >= {crit['meta']:.0%}** — `{crit['formula']}`. "
        f"{crit['regra_do_branco']}",
        "",
        f"**Metrica de acompanhamento ({crit['metrica_secundaria']['nome']}):** "
        f"`{crit['metrica_secundaria']['formula']}` — {crit['metrica_secundaria']['uso']}",
        "",
        crit["observacao"],
        "",
        f"**Como os grupos sao formados:** {s['estrutura_dos_grupos']}",
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

    out += ["", "## A semana", "",
            "| Dia | Grupo | Peso est. | Topicos | Simulado | Meta | Materias |", "|---|---|---|---|---|---|---|"]
    for g in prog["grupos"]:
        r = cotas.resumo(g, materias)
        lista = " · ".join(materias[b["id"]]["nome"] for b in g["materias"])
        out.append(f"| {g['dia']} | **{g['nome']}** | {r['peso']} | {r['topicos']} | "
                   f"**{r['total']}q** | {r['meta']}/{r['total']} | {lista} |")
    out.append("| Domingo | **Nivel 3 — simulado geral** | pool vencido | — | 200q | 180/200 | "
               "proporcional ao peso dos topicos vencidos |")
    out.append("")

    out += ["## Cada grupo em detalhe", ""]
    for g in prog["grupos"]:
        r = cotas.resumo(g, materias)
        out += [
            f"### {g['dia']} · {g['nome']} — {r['peso']} itens estimados · simulado de {r['total']} questoes "
            f"(meta {r['meta']})",
            "",
            f"*{g['tese']}*",
            "",
            "| Materia | Topicos | Peso est. | Questoes no simulado |",
            "|---|---|---|---|",
        ]
        for b in g["materias"]:
            out.append(
                f"| {materias[b['id']]['nome']} | {', '.join(b['topicos'])} | "
                f"{peso_do_bloco(b, materias)} | **{r['por_materia'][b['id']]}** |"
            )
        out += [
            f"| **Total** | — | **{r['peso']}** | **{r['total']}** |",
            "",
            "<details><summary>Topicos deste dia, um a um (cada um e uma unidade de Nivel 1)</summary>",
            "",
            "| Materia | # | Topico | Peso | Questoes no simulado |",
            "|---|---|---|---|---|",
        ]
        for b in g["materias"]:
            textos = {t["n"]: t["texto"] for t in materias[b["id"]]["ementa"]}
            pz = pesos(materias[b["id"]])
            for n in b["topicos"]:
                out.append(f"| {materias[b['id']]['nome']} | {n} | {curto(textos[n], 110)} | {pz[n]} | "
                           f"{r['por_topico'][(b['id'], n)]} |")
        out += ["", "</details>", ""]

    dim = s.get("dimensionamento_do_nivel_2", {})
    teto = s.get("teto_semanal", {})
    if dim:
        out += ["## Tamanho do simulado de Nivel 2", "",
                f"{dim['regra']}. Meta: **{dim['meta']}**.", "",
                f"Piso de **{dim['cota_minima_por_topico']} questoes por topico**. {dim['por_que']}", "",
                f"{dim['calculo']}.", ""]
    if teto:
        out += ["## Teto semanal", "",
                f"**{teto['questoes']} questoes por semana.** {teto['por_que']}", "",
                "Ordem de corte quando estourar:", ""]
        out += [f"- {x}" for x in teto["ordem_de_corte"]]
        out += ["", "Nunca cortar:", ""] + [f"- {x}" for x in teto["nunca_cortar"]]
        out += ["", teto["observacao"], ""]

    out += [
        "## Rotina",
        "",
        f"- **Manha (seg a sab):** {s['rotina_diaria']['manha']}",
        f"- **Tarde/noite (seg a sab):** {s['rotina_diaria']['tarde_noite']}",
        f"- **Domingo:** {s['rotina_diaria']['domingo']}",
        "",
        "Tempo-alvo: " + " · ".join(f"**Nivel {k[-1]}** {v}" for k, v in s["tempo_alvo"].items()),
        "",
        "## Regras de avanco e regressao",
        "",
    ]
    for n in s["niveis"]:
        out += [f"**Nivel {n['nivel']} — {n['nome']}**", ""]
        for chave, rotulo in [
            ("pre_requisito", "Pre-requisito"),
            ("composicao", "Composicao"),
            ("inicio", "Inicio"),
            ("aprovado_gera", f"Aprovado ({n['meta']:.0%}+)"),
            ("reprovado_gera", "Reprovado"),
            ("regressao", "Regressao"),
        ]:
            if n.get(chave):
                out.append(f"- {rotulo}: {n[chave]}")
        out.append("")
    return "\n".join(out) + "\n"


def mapa(prog: dict, materias: dict) -> str:
    total = sum(m["itens_estimados"] for m in materias.values())
    out = [
        "# Mapa de progressao — TCDF/ANACE",
        "",
        "> GERADO por `scripts/gerar_progressao.py`. Copie para onde voce acompanha (planilha, Notion, papel) "
        "e marque a cada simulado.",
        "",
        "Cada linha e uma unidade de Nivel 1 (20 questoes, 90% para vencer). Quando todos os topicos de um dia "
        "estiverem vencidos, o grupo daquele dia esta pronto para o simulado de Nivel 2.",
        "",
        "Status: `—` nao iniciado · `EM ESTUDO` · **`VENCIDO`** (>= 90% em 20 questoes) · `REFORCO` (reprovou uma vez) "
        "· `REVISAR` (reprovou duas vezes)",
        "",
        "| Dia | Grupo | Materia | # | Topico | Peso | Status | Data |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for g in prog["grupos"]:
        for b in g["materias"]:
            info = materias[b["id"]]
            textos = {t["n"]: t["texto"] for t in info["ementa"]}
            p = pesos(info)
            for n in b["topicos"]:
                out.append(
                    f"| {g['dia'][:3]} | {g['nome']} | {info['icone']} {info['nome']} | {n} | "
                    f"{curto(textos[n], 70)} | {p[n]} |  |  |"
                )
    out += [
        "",
        "## Nivel 2 — grupos",
        "",
        "| Dia | Grupo | Peso | Topicos vencidos | Melhor resultado | Status |",
        "|---|---|---|---|---|---|",
    ]
    for g in prog["grupos"]:
        n_top = sum(len(b["topicos"]) for b in g["materias"])
        out.append(f"| {g['dia']} | {g['nome']} | {peso_do_grupo(g, materias)} | 0 / {n_top} |  | — |")
    out += [
        "",
        "## Nivel 3 — pool",
        "",
        f"| Grupos vencidos | Peso somado | % do edital ({total}) | Questoes no domingo |",
        "|---|---|---|---|",
        "| 0 | 0 | 0% | — (minimo de 30 de peso para iniciar) |",
        "",
        "Cota de cada topico no simulado de 200: `200 x (peso do topico / peso somado do pool)`.",
        "",
        "## Registro dos domingos",
        "",
        "| Data | Grupos no pool | Questoes | Acertos | Erros | Liquido | % | Grupos abaixo de 90% |",
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

    n_top = sum(len(b["topicos"]) for g in prog["grupos"] for b in g["materias"])
    print(f"{len(prog['grupos'])} grupos cobrindo {n_top} topicos de {len(materias)} materias — consistente")
    if check:
        print("modo --check: nenhum arquivo foi escrito")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
