#!/usr/bin/env python3
"""Apura o estado da progressao a partir dos simulados registrados.

Le scripts/progresso.json (registros de lotes) + progressao.json + edital.json
e escreve data/status-atual.md com:
  - status de cada topico (Nivel 1)
  - prontidao de cada grupo para o Nivel 2, o lote de rampa de quem ainda nao chegou
    aos 70%, e quais grupos ja venceram
  - pool do Nivel 3 e a composicao do proximo simulado de domingo

Formato de cada registro em scripts/progresso.json:
  {"data": "2026-09-13", "nivel": 1, "materia": "direito-administrativo",
   "topico": "3", "total": 20, "acertos": 18, "erros": 2, "brancos": 0}
  Nivel 2 usa "grupo" no lugar de "materia"/"topico"; Nivel 3 usa "grupo" por linha.

So vale como tentativa oficial (gate) o lote que cobre UM topico INTEIRO e tem pelo
menos o tamanho do nivel. Lote parcial, misto ou curto e afericao diagnostica:
mede e orienta o reforco, mas nao marca VENCIDO nem queima tentativa. O registro
pode dizer isso explicitamente com "gate": false / "escopo": "parcial" | "misto".

Uso:
    python3 scripts/gerar_status.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))

import cotas  # noqa: E402

META = 0.90
QUESTOES_DO_NIVEL = {1: 20, 3: 50}
ESCOPOS_DIAGNOSTICOS = {"parcial", "misto", "diagnostico", "rampa"}


def subtopicos_do(n: str, texto: str) -> list[str]:
    """Subtopicos declarados na ementa do topico n ('1' -> ['1.1', '1.2', ...]).

    O recorte evita numeros de lei (4.320, 14.133, 32.598) exigindo que o prefixo
    seja o proprio numero do topico e que o sufixo tenha no maximo dois digitos.
    """
    achados = re.findall(rf"(?<![\d.]){re.escape(n)}\.\d{{1,2}}(?![\d./])", texto)
    vistos = []
    for a in achados:
        if a not in vistos:
            vistos.append(a)
    return vistos


def fracao_estudada(e: dict, n: str, texto: str) -> float:
    """Quanto do topico ja foi visto, entre 0 e 1."""
    if e.get("completo", True):
        return 1.0
    declarados = subtopicos_do(n, texto)
    vistos = [s for s in e.get("subtopicos", []) if s in declarados]
    if declarados and vistos:
        return len(vistos) / len(declarados)
    return 0.5


def curto(texto: str, limite: int = 70) -> str:
    t = re.sub(r"^\d+\s+", "", texto)
    return t if len(t) <= limite else t[: limite - 3].rstrip() + "..."


def bruto(r: dict) -> float:
    return r["acertos"] / r["total"] if r["total"] else 0.0


def liquido(r: dict) -> float:
    erros = r.get("erros", r["total"] - r["acertos"] - r.get("brancos", 0))
    return (r["acertos"] - erros) / r["total"] if r["total"] else 0.0


def placar(r: dict) -> str:
    return f"{r['acertos']}/{r['total']} ({bruto(r):.0%} bruto · {liquido(r):.0%} liq.)"


def topicos_do(r: dict) -> list[str]:
    if r.get("topicos"):
        return [str(t) for t in r["topicos"]]
    return [str(r["topico"])] if r.get("topico") is not None else []


def vale_como_gate(r: dict) -> bool:
    """Lote oficial: um topico inteiro, no tamanho do nivel. O resto e afericao."""
    if "gate" in r:
        return bool(r["gate"])
    if r.get("escopo", "completo") in ESCOPOS_DIAGNOSTICOS:
        return False
    if len(topicos_do(r)) > 1:
        return False
    return r["total"] >= QUESTOES_DO_NIVEL.get(r["nivel"], 0)


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


def ler_progresso(mats: dict) -> dict:
    """Estado declarado + apurado, na forma que os geradores consomem.

    tocados   topicos com algum estudo declarado
    completos topicos cuja ementa fechou (podem ir ao lote de 20)
    fracoes   quanto de cada topico ja foi visto (0 a 1)
    vencidos  topicos aprovados em lote oficial de Nivel 1
    """
    reg = json.loads((RAIZ / "scripts" / "progresso.json").read_text(encoding="utf-8"))
    estudo = {(e["materia"], str(e["topico"])): e for e in reg.get("estudados", [])}
    fracoes = {}
    for (mid, n), e in estudo.items():
        texto = {t["n"]: t["texto"] for t in mats[mid]["ementa"]}[n]
        fracoes[(mid, n)] = fracao_estudada(e, n, texto)
    vencidos = set()
    for r in reg["registros"]:
        if r["nivel"] == 1 and vale_como_gate(r) and bruto(r) >= META:
            vencidos |= {(r["materia"], n) for n in topicos_do(r)}
    return {
        "registros": reg["registros"],
        "estudo": estudo,
        "tocados": set(estudo),
        "completos": {k for k, e in estudo.items() if e.get("completo", True)},
        "fracoes": fracoes,
        "vencidos": vencidos,
    }


def main() -> int:
    ed = json.loads((RAIZ / "scripts" / "edital.json").read_text(encoding="utf-8"))
    prog = json.loads((RAIZ / "scripts" / "progressao.json").read_text(encoding="utf-8"))
    mats = {m["id"]: m for m in ed["materias"]}
    aulas_gran, marcadas_gran = carregar_gran()

    # ---- o que o candidato declara ter estudado ----
    estado = ler_progresso(mats)
    registros = estado["registros"]
    estudo, tocados = estado["estudo"], estado["tocados"]
    completos, fracoes = estado["completos"], estado["fracoes"]

    # ---- Nivel 1: lotes oficiais x afericoes ----
    n1_gate, n1_diag = {}, {}
    for r in (x for x in registros if x["nivel"] == 1):
        destino = n1_gate if vale_como_gate(r) else n1_diag
        for n in topicos_do(r):
            destino.setdefault((r["materia"], n), []).append(r)

    def status_topico(chave):
        lotes = n1_gate.get(chave)
        if lotes:
            melhor = max(lotes, key=bruto)
            if bruto(melhor) >= META:
                return "VENCIDO", melhor
            return ("REFORCO" if len(lotes) == 1 else "REVISAR"), melhor
        diag = n1_diag.get(chave)
        melhor_diag = max(diag, key=bruto) if diag else None
        if chave in completos:
            return "PRONTO P/ N1", melhor_diag
        if chave in tocados:
            return "EM ESTUDO", melhor_diag
        return "—", melhor_diag

    # ---- Nivel 2: grupos vencidos (so lote oficial decide) ----
    n2 = {}
    for r in (x for x in registros if x["nivel"] == 2 and vale_como_gate(r)):
        n2.setdefault(r["grupo"], []).append(r)

    out = ["# Status atual da progressao", "",
           "> GERADO por `scripts/gerar_status.py` a partir de `scripts/progresso.json`. Nao edite a mao.", "",
           f"Criterio de avanco: **bruto >= {META:.0%}** · branco conta como nao-acerto.", "",
           "Só fecha topico o lote que cobre **um topico inteiro** e tem o tamanho do nivel (20 no Nivel 1). "
           "Lote parcial ou misto entra como **afericao** — mede e orienta, nao marca VENCIDO nem queima tentativa.", ""]

    if not registros:
        out += ["Nenhum simulado registrado ainda.", "",
                "Para registrar, adicione entradas em `scripts/progresso.json` e rode "
                "`python3 scripts/gerar_status.py`.", ""]

    # ---- tabela por grupo ----
    pool_peso, pool_topicos, grupos_vencidos = 0, [], []
    rampas = []
    resumo = ["## Grupos", "",
              "| Dia | Grupo | Peso | Topicos vencidos | % do peso vencido | Manha do dia | Nivel 2 | Status |",
              "|---|---|---|---|---|---|---|---|"]
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
                         "PRONTO P/ N1": "pronto p/ N1", "EM ESTUDO": "em estudo"}.get(st, "—")
                lote = ""
                if melhor:
                    lote = placar(melhor) + ("" if vale_como_gate(melhor) else " · afericao")
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

        # manha do dia: lote oficial quando o grupo passou dos 70%, rampa antes disso
        oficial = cotas.tamanho_do_lote(n_top)
        if venceu:
            manha = "manutencao quinzenal"
        elif pct >= 0.70:
            manha = f"oficial: {oficial}q"
        else:
            cot = cotas.cotas_da_rampa(g, mats, tocados, fracoes)
            q = sum(cot.values())
            manha = f"rampa: {q}q" if q else "sem rampa (nada estudado)"
            if q:
                rampas.append((g, cot, q, pct))
        estado = "**VENCIDO**" if venceu else ("pronto para o Nivel 2" if pct >= 0.70 else "em Nivel 1")
        col2 = placar(melhor2) if melhor2 else "—"
        resumo.append(f"| {g['dia'][:3]} | {g['nome']} | {peso_total} | {n_venc}/{n_top} | {pct:.0%} | {manha} | {col2} | {estado} |")
        detalhe += linhas + [""]

    out += resumo + [""]

    # ---- modo rampa ----
    if rampas:
        out += ["## Modo rampa — a manha dos grupos que ainda nao chegaram a 70%", "",
                "Mesmo rito, mesmo cronometro, mesma meta de 90% — mas so com os topicos ja estudados "
                "(~4 questoes por topico, minimo de 10). **Nao aprova nem reprova o grupo**: produz a lista "
                "de reforco do dia. Quando o grupo passa dos 70% do peso vencido, a manha vira o simulado "
                "oficial de 50 ou 60 questoes.", ""]
        for g, cot, q, pct in rampas:
            out += [f"### {g['dia']} · {g['nome']} — {q} questoes ({pct:.0%} do peso vencido)", "",
                    "| Materia | # | Topico | Estudado | Questoes |", "|---|---|---|---|---|"]
            for (mid, n), qtd in sorted(cot.items(), key=lambda kv: (-kv[1], mats[kv[0][0]]["nome"], kv[0][1])):
                info = mats[mid]
                texto = {t["n"]: t["texto"] for t in info["ementa"]}[n]
                e = estudo[(mid, n)]
                subs = ", ".join(e.get("subtopicos", [])) or "topico inteiro"
                if not e.get("completo", True):
                    subs += " (parcial)"
                out.append(f"| {info['nome']} | {n} | {curto(texto, 50)} | {subs} | **{qtd}** |")
            out += [f"| **Total** | | | | **{q}** |", ""]

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
        cotas_n3 = [b[:5] for b in sorted(brutos, key=lambda b: (-b[3], b[0], b[1]))]
        for c in cotas_n3:
            out.append(f"| {c[0]} | {c[1]} | {c[2]} | {c[3]} | **{c[4]}** |")
        out += [f"| **Total** | | | **{pool_peso}** | **{sum(c[4] for c in cotas_n3)}** |", ""]

    # ---- filas de trabalho ----
    fila, abertos = [], []
    for g in prog["grupos"]:
        for b in g["materias"]:
            info = mats[b["id"]]
            pz = {t["n"]: t["peso"] for t in info["ementa"]}
            tx = {t["n"]: t["texto"] for t in info["ementa"]}
            for n in b["topicos"]:
                st, _ = status_topico((b["id"], n))
                aula = ", ".join(str(x) for x in aulas_gran.get((b["id"], n), []))
                if st == "PRONTO P/ N1":
                    fila.append((g["dia"], info["nome"], n, curto(tx[n]), pz[n], aula))
                elif st == "EM ESTUDO":
                    e = estudo[(b["id"], n)]
                    abertos.append((g["dia"], info["nome"], n, curto(tx[n], 50), pz[n],
                                    ", ".join(e.get("subtopicos", [])), e.get("observacao", "")))

    out += ["## Fila do Nivel 1 — topicos completos, aguardando o lote de 20", ""]
    if fila:
        out += [f"{len(fila)} lotes de 20 questoes = {len(fila) * 20} questoes.", "",
                "| Dia | Materia | # | Topico | Peso | Aula Gran |", "|---|---|---|---|---|---|"]
        out += [f"| {d[:3]} | {m} | {n} | {t} | {p} | {a or '—'} |" for d, m, n, t, p, a in
                sorted(fila, key=lambda f: -f[4])]
    else:
        out += ["Nada na fila: nenhum topico completo aguardando lote "
                "(preencha `estudados` em `scripts/progresso.json`).", ""]
    out += [""]

    out += ["## Em estudo — topicos abertos (falta parte da ementa)", ""]
    if abertos:
        out += ["Estes nao entram no lote de 20 enquanto nao fecharem: o lote de Nivel 1 cobre o topico inteiro.", "",
                "| Dia | Materia | # | Topico | Peso | Ja visto | Falta |", "|---|---|---|---|---|---|---|"]
        out += [f"| {d[:3]} | {m} | {n} | {t} | {p} | {v} | {o} |" for d, m, n, t, p, v, o in
                sorted(abertos, key=lambda f: -f[4])]
    else:
        out += ["Nenhum topico aberto.", ""]
    out += [""]

    # ---- afericoes diagnosticas ----
    diag = [r for r in registros if not vale_como_gate(r)]
    if diag:
        out += ["## Afericoes diagnosticas — medem, nao decidem", "",
                "| Data | Materia | Topico(s) | Escopo | Placar | Bruto | Liquido |",
                "|---|---|---|---|---|---|---|"]
        for r in sorted(diag, key=lambda r: r.get("data", "")):
            nome = mats[r["materia"]]["nome"] if r.get("materia") in mats else r.get("grupo", "—")
            out.append(f"| {r.get('data', '—')} | {nome} | {', '.join(topicos_do(r)) or '—'} | "
                       f"{r.get('escopo', 'parcial')} | {r['acertos']}/{r['total']} | "
                       f"{bruto(r):.1%} | {liquido(r):.1%} |")
        out += [""]

    out += detalhe
    (RAIZ / "data" / "status-atual.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    gates = sum(1 for r in registros if vale_como_gate(r))
    print(f"status gerado: {gates} lotes oficiais + {len(registros) - gates} afericoes, "
          f"{len(grupos_vencidos)} grupos vencidos, pool com peso {pool_peso}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
