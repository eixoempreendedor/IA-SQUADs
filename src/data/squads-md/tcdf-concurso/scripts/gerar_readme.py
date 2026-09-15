#!/usr/bin/env python3
"""Gera o README.md do squad a partir de edital.json e progressao.json.

Uso:
    python3 scripts/gerar_readme.py
"""
from __future__ import annotations

import json
import re
import unicodedata

import cotas
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def slug(texto: str) -> str:
    """Mesma regra de nomes de arquivo usada por gerar_pdfs.py."""
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
CORE = [
    ("🎓", "reitor-tcdf", "Orquestrador e porta de entrada: diagnostica, prioriza pelo peso do edital e roteia"),
    ("♟️", "estrategista-cebraspe", "Tecnica de prova C/E, politica de chute, gestao de tempo, recursos"),
    ("🗓️", "arquiteto-cronograma", "Ciclo de estudos ponderado pelo edital, revisoes embutidas, reta final"),
    ("✍️", "redator-discursiva", "P4: questao discursiva e peca tecnica Informacao, com espelho de correcao"),
    ("📈", "mentor-desempenho", "Metricas, diario de erros, projecao por bloco e ajuste de rota semanal"),
    ("⚖️", "arbitro-da-progressao", "Apura cada simulado, aplica o criterio de 90% e declara avanco, repeticao ou regressao"),
]


def main() -> int:
    ed = json.loads((RAIZ / "scripts" / "edital.json").read_text(encoding="utf-8"))
    prog = json.loads((RAIZ / "scripts" / "progressao.json").read_text(encoding="utf-8"))
    c, mats = ed["concurso"], ed["materias"]
    nomes = {m["id"]: m for m in mats}
    total_agentes = len(mats) * 3 + len(CORE)
    tasks = sorted(p.name for p in (RAIZ / "tasks").glob("*.md"))
    wfs = sorted(p.name for p in (RAIZ / "workflows").glob("*.yaml"))
    crit = prog["sistema"]["criterio_de_aprovacao"]

    linhas = [f"# TCDF Concurso Squad {'🎓'}", "",
              f"**{total_agentes} agentes de IA para aprovacao no concurso de Analista Administrativo de "
              f"Controle Externo do TCDF (Cebraspe, 2026).**", "",
              f"Sao **3 agentes para cada uma das {len(mats)} materias do edital** — um professor, um examinador e "
              f"um revisor — mais **{len(CORE)} agentes de coordenacao** que cuidam de estrategia de prova, cronograma, "
              "discursiva, desempenho e progressao por niveis.", "",
              "| | |", "|---|---|",
              f"| **Orgao** | {c['orgao']} |",
              f"| **Cargo** | {c['cargo']} |",
              f"| **Banca** | {c['banca']} |",
              f"| **Vagas** | {c['vagas']} |",
              f"| **Remuneracao inicial** | {c['remuneracao_inicial']} |",
              f"| **Escolaridade** | {c['escolaridade']} |",
              f"| **Provas** | {c['data_provas']} |",
              f"| **Duracao** | {c['duracao_provas']} |",
              f"| **Formato** | {c['formato_itens']} |", "",
              "## Fonte do conteudo", "",
              f"**`{c['status_fonte']}`** — {c['observacao_fonte']}", "",
              "Se houver nova retificacao, rode a task [`tasks/verticalizar-edital.md`](tasks/verticalizar-edital.md): "
              "o conteudo programatico e dado (`scripts/edital.json`), nao codigo, e os agentes se regeneram com um comando.", "",
              "## Estrutura das provas", "",
              "| Prova | Conteudo | Itens | Minimo |", "|---|---|---|---|"]
    for p in c["provas"]:
        linhas.append(f"| {p['id']} | {p['nome']} | {p['itens'] or '—'} | {p['minimo']} |")
    linhas += ["", f"Minimo global nas objetivas: **{c['minimo_global_objetivas']}**. "
                   f"{c['corte_para_correcao_da_discursiva']}.", "",
               "## Os 3 papeis por materia", "",
               "| Papel | O que faz | Quando acionar |", "|---|---|---|",
               "| 🧑‍🏫 **Professor** | Ensina o topico no recorte exato da banca: conceito, exemplo, tabela comparativa, "
               "pegadinhas, resumo e 3 itens de fixacao | Conteudo novo, duvida conceitual, resumo ou mapa mental |",
               "| 🎯 **Examinador** | Escreve itens Certo/Errado no padrao Cebraspe, aplica simulado cronometrado e "
               "comenta o gabarito com o mecanismo de erro usado | Treinar, simular, entender por que errou |",
               "| 🔁 **Revisor** | Revisao espacada (R1/R7/R30), flashcards, diario de erros e revisao de vespera | "
               "Manter vivo o que ja foi aprendido |", "",
               "## Agentes de coordenacao", "", "| Agente | Funcao |", "|---|---|"]
    for icone, aid, desc in CORE:
        linhas.append(f"| {icone} `{aid}` | {desc} |")

    linhas += ["", "## Mapa das materias", "",
               "| Materia | Bloco | Itens est. | Prioridade | Professor | Examinador | Revisor |",
               "|---|---|---|---|---|---|---|"]
    for m in mats:
        linhas.append(
            f"| {m['icone']} **{m['nome']}** | {m['bloco']} | {m['itens_estimados']} | {m['prioridade']} | "
            f"`{m['id']}-professor` | `{m['id']}-examinador` | `{m['id']}-revisor` |"
        )
    linhas += ["", f"> {c['observacao_itens']}", "",
               f"> O edital tem **{sum(len(m['ementa']) for m in mats)} topicos numerados** no total. Cada um e uma "
               "unidade de Nivel 1 e pertence a exatamente um grupo de conteudo.", ""]

    linhas += ["## Progressao por niveis (90% para avancar)", "",
               f"O estudo avanca por **resultado medido**, nao por tempo estudado. Questoes do "
               f"**{prog['sistema']['fonte_das_questoes']}**.", "",
               f"**Avanca com {crit['meta']:.0%} {crit['metrica']}** (`{crit['formula']}`). "
               f"{crit['regra_do_branco']}", "",
               f"O **{crit['metrica_secundaria']['nome']}** (`{crit['metrica_secundaria']['formula']}`) e apurado "
               "sempre ao lado, mas nao decide avanco: ele e o placar da prova real, em que cada erro anula "
               "um acerto.", "",
               "| Nivel | Unidade | Questoes | Quando | Aprovado gera |", "|---|---|---|---|---|"]
    for n in prog["sistema"]["niveis"]:
        linhas.append(f"| **{n['nivel']} — {n['nome']}** | {n['unidade']} | {n['questoes']} | {n['quando']} | {n['aprovado_gera']} |")
    linhas += ["", "### Grupos de conteudo (seg a sab)", "",
               f"{prog['sistema']['estrutura_dos_grupos']}", "",
               "| Dia | Grupo | Peso est. | Simulado | Materias — cota |", "|---|---|---|---|---|"]
    for g in prog["grupos"]:
        r = cotas.resumo(g, nomes)
        lista = " · ".join(f"{nomes[b['id']]['nome']} {r['por_materia'][b['id']]}q" for b in g["materias"])
        linhas.append(f"| {g['dia']} | **{g['nome']}** | {r['peso']} | **{r['total']}q** (meta {r['meta']}) | {lista} |")
    linhas += ["| Domingo | **Nivel 3 — simulado geral** | pool vencido | 200q (meta 180) | proporcional ao peso dos topicos vencidos |", "",
               f"Tamanho do lote de Nivel 2: {prog['sistema']['dimensionamento_do_nivel_2']['regra'].lower()}, "
               f"com piso de {prog['sistema']['dimensionamento_do_nivel_2']['cota_minima_por_topico']} questoes por topico. "
               f"Teto de **{prog['sistema']['teto_semanal']['questoes']} questoes por semana** — acima disso o "
               "`arquiteto-cronograma` corta primeiro a manutencao dos grupos ja vencidos, nunca o Nivel 1 do "
               "conteudo novo.", "",
               "Composicao completa, regras de avanco e de regressao: [`data/grupos-de-conteudo.md`](data/grupos-de-conteudo.md). "
               "Estado atual, apurado dos simulados ja feitos: [`data/status-atual.md`](data/status-atual.md).", "",
               "Para registrar um simulado, acrescente uma linha em `scripts/progresso.json` e rode "
               "`python3 scripts/gerar_status.py` — ele recalcula topicos vencidos, prontidao de cada grupo, "
               "pool do Nivel 3 e a composicao do proximo simulado de domingo.", "",
               "Para mudar grupos, cotas, meta ou metrica, edite `scripts/progressao.json` e rode "
               "`python3 scripts/gerar_progressao.py`.", "",
               "## Como usar", "", "```",
               "@tcdf                                     # reitor-tcdf (diagnostico e rota)",
               "@tcdf:direito-administrativo-professor    # aula de um topico",
               "@tcdf:direito-administrativo-examinador   # lote de itens C/E",
               "@tcdf:direito-administrativo-revisor      # revisao espacada e flashcards",
               "@tcdf:arbitro-da-progressao               # apurar simulado e declarar avanco",
               "@tcdf:arquiteto-cronograma                # montar o ciclo de estudos",
               "@tcdf:redator-discursiva                  # treinar e corrigir a P4",
               "```", "",
               "Cada arquivo `.md` de agente e autossuficiente (persona, ementa oficial da materia, regras de "
               "comportamento e formato de saida), entao funciona tambem fora do app, colado direto em qualquer "
               "ferramenta de agentes.", "",
               "## Fluxos prontos", "", "| Workflow | Quando |", "|---|---|",
               "| [`wf-primeira-semana`](workflows/wf-primeira-semana.yaml) | Voce esta comecando agora |",
               "| [`wf-ciclo-semanal`](workflows/wf-ciclo-semanal.yaml) | Rotina padrao de uma semana |",
               "| [`wf-progressao-por-niveis`](workflows/wf-progressao-por-niveis.yaml) | Sistema de 90% para avancar |",
               "| [`wf-reta-final`](workflows/wf-reta-final.yaml) | Ultimos 60 dias |", "",
               "## Tasks", "", " · ".join(f"`{t[:-3]}`" for t in tasks), "",
               "## Checklists em PDF", "",
               "Um PDF por dia da semana, para imprimir: checklist com uma bolinha por topico e por subtopico do "
               "edital, campo para o resultado do lote de Nivel 1 de cada topico, e a tabela de registro dos "
               "simulados daquele dia. Domingo traz o registro geral do Nivel 3 e a projecao por bloco.", "",
               "| Dia | Arquivo |", "|---|---|"]
    for i, g in enumerate(prog["grupos"], 1):
        nome_pdf = f"{i}-{slug(g['dia'])}-{slug(g['nome'])}.pdf"
        linhas.append(f"| {g['dia']} | [`pdf/{nome_pdf}`](pdf/{nome_pdf}) |")
    linhas += ["| Domingo | [`pdf/7-domingo-nivel-3.pdf`](pdf/7-domingo-nivel-3.pdf) |", "",
               "Gerados por `python3 scripts/gerar_pdfs.py` — mudou grupo ou ementa, e so rodar de novo.", "",
               "### Uma folha por materia: a ementa cruzada com os filtros do Gran", "",
               f"Em [`pdf/materias/`](pdf/materias/), um PDF por materia ({len(mats)} no total), em **duas folhas A4 "
               "em pe**. A folha 1 e a materia inteira: cada topico e cada subtopico do edital em uma linha, a aula "
               "do curso ao lado e oito colunas de bolinhas. O nome de cada filtro montado no Gran e escrito em pe no "
               "cabecalho da coluna; as bolinhas marcadas dizem o que aquele filtro sorteia. A folha 2 e o registro "
               "dos simulados: filtro, data, total, acertos, erros, bruto, liquido e veredito.", "",
               "A ultima coluna e fixa e se chama **GERAL N2**. A bolina grande dela, uma por topico, marca a materia "
               "vencida: o topico que fechou 18/20 sobre a ementa inteira sai da fila de estudo e passa a entrar no "
               "filtro geral do Gran — o que alimenta o simulado de Nivel 2 do grupo e as revisoes de tudo que ja "
               "esta vencido. Ela so aparece na linha do topico, porque e o topico inteiro que vence; subtopico "
               "sozinho nao fecha nada.", "",
               "No pe da folha, **cada coluna de filtro fecha com uma bolona**: aquele filtro bateu a meta e pode "
               "ser jogado dentro do GERAL N2. A ultima bolona e a materia inteira.", "",
               "A materia inteira cabe na folha 1 qualquer que seja o tamanho dela. O corpo do texto encolhe so o "
               "quanto for preciso — as curtas saem em 12pt e o que sobra vira pauta de anotacao; Direito "
               "Administrativo, a maior, fecha em 7,6pt com os 14 topicos e os 41 subtopicos.", "",
               "A folha responde a pergunta que o mapa por dia nao responde: **qual pedaco da ementa cada filtro "
               "esta realmente cobrindo** — e, por eliminacao, o que nenhum filtro esta testando.", "",
               "```bash",
               "python3 scripts/gerar_pdfs_materia.py                      # todas as materias",
               "python3 scripts/gerar_pdfs_materia.py direito-administrativo",
               "```", "",
               "## Templates", "",
               "[`mapa-de-progressao.md`](templates/mapa-de-progressao.md) · "
               "[`diario-de-erros.md`](templates/diario-de-erros.md) · "
               "[`folha-de-simulado.md`](templates/folha-de-simulado.md) · "
               "[`flashcards.md`](templates/flashcards.md)", "",
               "## Regenerar", "",
               f"Os {len(mats) * 3} agentes de materia e o `reitor-tcdf` sao **gerados** a partir de "
               "`scripts/edital.json`; os grupos e niveis, a partir de `scripts/progressao.json`.", "", "```bash",
               "python3 scripts/gerar_agentes.py        # agentes, squad.yaml, data/",
               "python3 scripts/gerar_progressao.py     # grupos de conteudo e mapa de progressao",
               "python3 scripts/gerar_status.py         # status atual a partir dos simulados registrados",
               "python3 scripts/gerar_pdfs.py           # os 7 PDFs de checklist (pdf/)",
               "python3 scripts/gerar_pdfs_materia.py   # um PDF por materia: ementa x filtros (pdf/materias/)",
               "python3 scripts/gerar_readme.py         # este README",
               "python3 scripts/sync_app_registry.py    # registra o squad em squads.ts e agents.ts",
               "```", "",
               f"Os outros {len(CORE) - 1} agentes de coordenacao sao escritos a mao e nao sao sobrescritos.", "",
               "Para adicionar uma materia: acrescente um objeto em `materias` no `edital.json`, encaixe-a em um grupo "
               "no `progressao.json` e rode os geradores — os 3 agentes nascem prontos e os documentos se atualizam.", "",
               "## Estrutura de arquivos", "", "```", "tcdf-concurso/",
               "├── squad.yaml                  # manifesto (gerado)",
               "├── README.md                   # (gerado)",
               f"├── agents/                     # {total_agentes} agentes (.md)",
               f"├── tasks/                      # {len(tasks)} tasks",
               f"├── workflows/                  # {len(wfs)} workflows",
               "├── checklists/                 # qualidade de item C/E, peca Informacao",
               "├── templates/                  # mapa de progressao, diario de erros, simulado, flashcards",
               "├── data/                       # edital verticalizado, grupos de conteudo, roteamento (gerados)",
               "└── scripts/",
               "    ├── edital.json             # FONTE DA VERDADE do conteudo",
               "    ├── progressao.json         # FONTE DA VERDADE dos grupos e niveis",
               "    ├── progresso.json          # registro dos simulados feitos (memoria do sistema)",
               "    └── *.py                    # geradores", "```", "",
               "## Limites", "",
               "- Os agentes nao substituem a leitura do edital oficial nem do material de aula.",
               "- Nenhum agente estima probabilidade de aprovacao ou nota de corte como certeza.",
               "- Prazos, percentuais e quoruns devem ser conferidos na norma: os agentes sao instruidos a sinalizar "
               "quando nao tiverem certeza, mas a conferencia final e sua.", ""]

    (RAIZ / "README.md").write_text("\n".join(linhas), encoding="utf-8")
    print(f"README gerado: {total_agentes} agentes, {len(mats)} materias, {len(tasks)} tasks, {len(wfs)} workflows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
