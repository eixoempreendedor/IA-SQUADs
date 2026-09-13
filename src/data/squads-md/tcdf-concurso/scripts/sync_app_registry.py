#!/usr/bin/env python3
"""Sincroniza o TCDF Concurso Squad com os registros do app Next.js.

Atualiza (de forma idempotente, entre marcadores):
  - src/data/squads.ts  -> entrada do squad no catalogo
  - src/data/agents.ts  -> os 68 agentes no catalogo de agentes

Uso:
    python3 scripts/sync_app_registry.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
APP_DATA = RAIZ.parent.parent  # src/data
SQUADS_TS = APP_DATA / "squads.ts"
AGENTS_TS = APP_DATA / "agents.ts"

SQUAD_ID = "tcdf-concurso"
SQUAD_NOME = "TCDF Concurso Squad"
COR = "#7c3aed"

INI = f"  // >>> {SQUAD_ID} (gerado por squads-md/{SQUAD_ID}/scripts/sync_app_registry.py)"
FIM = f"  // <<< {SQUAD_ID}"

CORE = [
    ("reitor-tcdf", "Reitor TCDF", "🎓", "Orquestrador do TCDF Concurso Squad"),
    ("estrategista-cebraspe", "Estrategista Cebraspe", "♟️", "Tecnica de prova Certo/Errado"),
    ("arquiteto-cronograma", "Arquiteto de Cronograma", "🗓️", "Ciclo de estudos e reta final"),
    ("redator-discursiva", "Redator da Discursiva", "✍️", "Prova P4 e peca tecnica Informacao"),
    ("mentor-desempenho", "Mentor de Desempenho", "📈", "Diagnostico, metricas e ajuste de rota"),
]


def ts(texto: str) -> str:
    return '"' + texto.replace("\\", "\\\\").replace('"', '\\"') + '"'


def substituir_bloco(conteudo: str, bloco: str, ancora: str) -> str:
    """Troca o bloco entre INI/FIM; se nao existir, insere antes da ancora."""
    padrao = re.compile(re.escape(INI) + r".*?" + re.escape(FIM) + r"\n", re.DOTALL)
    if padrao.search(conteudo):
        return padrao.sub(bloco, conteudo)
    idx = conteudo.index(ancora)
    return conteudo[:idx] + bloco + conteudo[idx:]


def main() -> int:
    edital = json.loads((RAIZ / "scripts" / "edital.json").read_text(encoding="utf-8"))
    mats = edital["materias"]
    total_agentes = len(CORE) + len(mats) * 3
    tasks = len(list((RAIZ / "tasks").glob("*.md")))
    wfs = len(list((RAIZ / "workflows").glob("*.yaml")))

    # ---------------- squads.ts ----------------
    desc = (
        f"Squad de {total_agentes} agentes para o concurso de Analista do TCDF (Cebraspe): "
        f"professor, examinador e revisor para cada uma das {len(mats)} materias do edital, "
        "mais orquestrador, estrategista de prova, cronograma, discursiva e desempenho."
    )
    bloco_squad = "\n".join([
        INI,
        "  {",
        f'    id: "{SQUAD_ID}",',
        f"    name: {ts(SQUAD_NOME)},",
        f"    description: {ts(desc)},",
        '    version: "v1.0.0",',
        f"    agents: {total_agentes},",
        f"    tasks: {tasks},",
        f"    workflows: {wfs},",
        '    tags: ["concurso-publico", "tcdf", "cebraspe", "controle-externo", "estudos", '
        '"questoes-certo-errado", "revisao-espacada", "discursiva", "cronograma", "direito"],',
        f'    color: "{COR}",',
        "  },",
        FIM,
        "",
    ])
    squads_src = SQUADS_TS.read_text(encoding="utf-8")
    squads_src = substituir_bloco(squads_src, bloco_squad, "];\n\nexport const inactiveSquads")
    SQUADS_TS.write_text(squads_src, encoding="utf-8")

    # ---------------- agents.ts ----------------
    linhas = [INI]
    for aid, nome, icone, titulo in CORE:
        linhas.append(
            f"  {{ id: {ts(aid)}, name: {ts(nome)}, icon: {ts(icone)}, title: {ts(titulo)}, "
            f'squadId: "{SQUAD_ID}", squadName: {ts(SQUAD_NOME)} }},'
        )
    papeis = [
        ("professor", "Professor de {nome}", "{icone}", "Teoria e aulas de {nome} ({bloco})"),
        ("examinador", "Examinador de {nome}", "🎯", "Itens Certo/Errado de {nome} ({bloco})"),
        ("revisor", "Revisor de {nome}", "🔁", "Revisao espacada de {nome} ({bloco})"),
    ]
    for m in mats:
        for papel, nome_tpl, icone_tpl, titulo_tpl in papeis:
            ctx = {"nome": m["nome"], "icone": m["icone"], "bloco": m["bloco"]}
            linhas.append(
                f'  {{ id: {ts(m["id"] + "-" + papel)}, name: {ts(nome_tpl.format(**ctx))}, '
                f"icon: {ts(icone_tpl.format(**ctx))}, title: {ts(titulo_tpl.format(**ctx))}, "
                f'squadId: "{SQUAD_ID}", squadName: {ts(SQUAD_NOME)} }},'
            )
    linhas += [FIM, ""]
    bloco_agentes = "\n".join(linhas)

    agents_src = AGENTS_TS.read_text(encoding="utf-8")
    agents_src = substituir_bloco(agents_src, bloco_agentes, "  // agentes-de-ferias (inactive)")
    AGENTS_TS.write_text(agents_src, encoding="utf-8")

    print(f"squads.ts e agents.ts sincronizados: {total_agentes} agentes, {tasks} tasks, {wfs} workflows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
