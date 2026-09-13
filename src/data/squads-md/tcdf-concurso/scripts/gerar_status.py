#!/usr/bin/env python3
"""Apura o estado da progressao a partir dos simulados registrados.

Le scripts/progresso.json (registros de lotes) + progressao.json + edital.json
e escreve data/status-atual.md com:
  - status de cada topico (Nivel 1)
  - prontidao de cada grupo para o Nivel 2 e quais ja venceram
  - pool do Nivel 3 e a composicao do proximo simulado de domingo

Formato de cada registro em scripts/progresso.json:
  {"data": "2026-09-13", "nivel": 1, "materia": "direito-administrativo",
   "topico": "3", "total": 20, "acertos": 18, "erros": 2, "brancos": 0}
  Nivel 2 usa "grupo" no lugar de "materia"/"topico"; Nivel 3 usa "grupo" por linha.

Uso:
    python3 scripts/gerar_status.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
META = 0.90


def curto(texto: str, limite: int = 70) -> str:
    t = re.sub(r"^\d+\s+", "", texto)
    return t if len(t) <= limite else t[: limite - 3].rstrip() + "..."


def bruto(r: dict) -> float:
    return r["acertos"] / r["total"] if r["total"] else 0.0


def liquido(r: dict) -> float:
    return (r["acertos"] - r.get("erros", r["total"] - r["acertos"] - r.get("brancos", 0))) / r["total"] if r["total"] else 0.0


def carregar_gran() -> tuple[dict, dict]:
    """(materia, topico) -> [aulas do curso]; e quais dessas aulas estao marcadas na plataforma."""
    arq = RAIZ / "scripts" / "gran.json"
    if not arq.exists():
        return {}, {}
    gran = json.loads(arq.read_text(encoding="utf-8"))
    aulas, marcadas = {}, {}
    for mid, lista in gran["materias"].items():
        for a in lista:
            for n in a["topicos"]:
                aulas.setdefault((mid, n), []).append(a["aula"])
                if a.get("marcado_na_plataforma"):
                    marcadas.setdefault((mid, n), []).append(a["aula"])
    return aulas, marcadas


def main() -> int:
    ed = json.loads((RAIZ / "scripts" / "edital.json").read_text(encoding="utf-8"))
    prog = json.loads((RAIZ / "scripts" / "progressao.json").read_text(encoding="utf-8"))
    reg = json.loads((RAIZ / "scripts" / "progresso.json").read_text(encoding="utf-8"))
    mats = {m["id"]: m for m in ed["materias"]}
    registros = reg["registros"]
    estudados = {(e["materia"], str(e["topico"])) for e in reg.get("estudados", [])}
    aulas_gran, marcadas_gran = carregar_gran()

    # ---- Nivel 1: status por topico ----
    n1 = {}
    for r in (x for x in registros if x["nivel"] == 1):
        chave = (r["materia"], str(r["topico"]))
        n1.setdefault(chave, []).append(r)

    def status_topico(chave):
        lotes = n1.get(chave)
        if not lotes:
            return ("PRONTO P/ N1" if chave in estudados else "—"), None
        melhor = max(lotes, key=bruto)
        if bruto(melhor) >= META:
            return "VENCIDO", melhor
        return ("REFORCO" if len(lotes) == 1 else "REVISAR"), melhor

    # ---- Nivel 2: grupos vencidos ----
    n2 = {}
    for r in (x for x in registros if x["nivel"] == 2):
        n2.setdefault(r["grupo"], []).append(r)

    out = ["# Status atual da progressao", "",
           "> GERADO por `scripts/gerar_status.py` a partir de `scripts/progresso.json`. Nao edite a mao.", "",
           f"Criterio de avanco: **bruto >= {META:.0%}** · branco conta como nao-acerto.", ""]

    if not registros:
        out += ["Nenhum simulado registrado ainda.", "",
                "Para registrar, adicione entradas em `scripts/progresso.json` e rode "
                "`python3 scripts/gerar_status.py`.", ""]

    # ---- tabela por grupo ----
    pool_peso, pool_topicos, grupos_vencidos = 0, [], []
    resumo = ["## Grupos", "", "| Dia | Grupo | Peso | Topicos vencidos | % do peso vencido | Nivel 2 | Status |",
              "|---|---|---|---|---|---|---|"]
    detalhe = ["## Topicos", ""]

    for g in prog["grupos"]:
        peso_total = peso_venc = 0
        n_top = n_venc = 0
        linhas = [f"### {g['dia']} · {g['nome']}", "",
                  "| Materia | # | Topico | Peso | Aula Gran | Marcado | Status | Melhor lote |",
                  "|---|---|---|---|---|---|---|---|"]
        for b in g["materias"]:
            info = mats[b["id"]]
            pesos = {t["n"]: t["peso"] for t in info["ementa"]}
            textos = {t["n"]: t["texto"] for t in info["ementa"]}
            for n in b["topicos"]:
                st, melhor = status_topico((b["id"], n))
                peso_total += pesos[n]
                n_top += 1
                if st == "VENCIDO":
                    peso_venc += pesos[n]
                    n_venc += 1
                marca = {"VENCIDO": "**VENCIDO**", "REFORCO": "REFORCO", "REVISAR": "REVISAR",
                         "PRONTO P/ N1": "pronto p/ N1"}.get(st, "—")
                lote = f"{melhor['acertos']}/{melhor['total']} ({bruto(melhor):.0%})" if melhor else ""
                ag = ", ".join(str(x) for x in aulas_gran.get((b["id"], n), [])) or "—"
                mg = "sim" if (b["id"], n) in marcadas_gran else ""
                linhas.append(f"| {info['nome']} | {n} | {curto(textos[n])} | {pesos[n]} | {ag} | {mg} | {marca} | {lote} |")
        pct = peso_venc / peso_total if peso_total else 0
        lotes2 = n2.get(g["id"], [])
        melhor2 = max(lotes2, key=bruto) if lotes2 else None
        venceu = bool(melhor2 and bruto(melhor2) >= META)
        if venceu:
            grupos_vencidos.append(g["id"])
            pool_peso += peso_total
            pool_topicos += [(b["id"], n) for b in g["materias"] for n in b["topicos"]]
        estado = "**VENCIDO**" if venceu else ("pronto para o Nivel 2" if pct >= 0.70 else "em Nivel 1")
        col2 = f"{melhor2['acertos']}/{melhor2['total']} ({bruto(melhor2):.0%})" if melhor2 else "—"
        resumo.append(f"| {g['dia'][:3]} | {g['nome']} | {peso_total} | {n_venc}/{n_top} | {pct:.0%} | {col2} | {estado} |")
        detalhe += linhas + [""]

    out += resumo + [""]

    # ---- Nivel 3 ----
    total_edital = sum(m["itens_estimados"] for m in mats.values())
    out += ["## Nivel 3 — pool do domingo", "",
            f"Grupos vencidos: **{len(grupos_vencidos)}/6** · peso no pool: **{pool_peso}** de {total_edital} "
            f"({pool_peso / total_edital:.0%} do edital)", ""]
    if pool_peso == 0:
        out += ["Nenhum grupo vencido ainda: o simulado de domingo comeca no primeiro grupo aprovado no Nivel 2.", ""]
    else:
        tamanho = 200 if pool_peso >= 30 else max(50, round(200 * pool_peso / total_edital / 10) * 10)
        out += [f"Tamanho do proximo simulado: **{tamanho} questoes**", "",
                "| Materia | # | Topico | Peso | Questoes |", "|---|---|---|---|---|"]
        # Apportionment por maior resto (Hamilton): fecha exatamente em `tamanho`
        # sem jogar todo o erro de arredondamento num unico topico.
        brutos = []
        for mid, n in pool_topicos:
            info = mats[mid]
            peso = {t["n"]: t["peso"] for t in info["ementa"]}[n]
            texto = {t["n"]: t["texto"] for t in info["ementa"]}[n]
            exato = tamanho * peso / pool_peso
            brutos.append([info["nome"], n, curto(texto), peso, int(exato), exato - int(exato)])
        sobra = tamanho - sum(b[4] for b in brutos)
        for b in sorted(brutos, key=lambda b: -b[5])[:sobra]:
            b[4] += 1
        cotas = [b[:5] for b in sorted(brutos, key=lambda b: (-b[3], b[0], b[1]))]
        for c in cotas:
            out.append(f"| {c[0]} | {c[1]} | {c[2]} | {c[3]} | **{c[4]}** |")
        out += [f"| **Total** | | | **{pool_peso}** | **{sum(c[4] for c in cotas)}** |", ""]

    # fila de trabalho: o que ja foi estudado e ainda nao passou pelo lote de 20
    fila = []
    for g in prog["grupos"]:
        for b in g["materias"]:
            info = mats[b["id"]]
            pz = {t["n"]: t["peso"] for t in info["ementa"]}
            tx = {t["n"]: t["texto"] for t in info["ementa"]}
            for n in b["topicos"]:
                if status_topico((b["id"], n))[0] == "PRONTO P/ N1":
                    fila.append((g["dia"], info["nome"], n, curto(tx[n]), pz[n],
                                 ", ".join(str(x) for x in aulas_gran.get((b["id"], n), []))))
    out += ["## Fila do Nivel 1 — topicos ja estudados, aguardando o lote de 20", ""]
    if fila:
        out += [f"{len(fila)} lotes de 20 questoes = {len(fila) * 20} questoes.", "",
                "| Dia | Materia | # | Topico | Peso | Aula Gran |", "|---|---|---|---|---|---|"]
        out += [f"| {d[:3]} | {m} | {n} | {t} | {p} | {a} |" for d, m, n, t, p, a in
                sorted(fila, key=lambda f: -f[4])]
    else:
        out += ["Nada na fila: nenhum topico foi declarado estudado ainda "
                "(preencha `estudados` em `scripts/progresso.json`).", ""]
    out += [""]

    out += detalhe
    (RAIZ / "data" / "status-atual.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"status gerado: {len(registros)} lotes registrados, {len(grupos_vencidos)} grupos vencidos, pool com peso {pool_peso}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
