---
task: verticalizarEdital()
responsavel: "@reitor-tcdf"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: texto_oficial_do_edital
    tipo: string
    origem: User Input (colar o conteudo programatico oficial)
    obrigatorio: true

Saida:
  - campo: edital_atualizado
    tipo: json
    destino: scripts/edital.json
    persistido: true
  - campo: agentes_regenerados
    tipo: markdown
    destino: agents/
    persistido: true

Checklist:
  - "[ ] Cada materia do texto oficial tem entrada em scripts/edital.json"
  - "[ ] Ementa transcrita na integra, sem resumo"
  - "[ ] Blocos (P1/P2/P3) e itens conferidos com o edital"
  - "[ ] status_fonte alterado para VERIFICADO_NA_FONTE_OFICIAL"
  - "[ ] python3 scripts/gerar_agentes.py executado"
  - "[ ] squad.yaml e README atualizados se o numero de materias mudou"
---

# Task: Verticalizar o Edital (fonte da verdade)

## Metadata

| Campo | Valor |
|---|---|
| Task ID | `tcdf-concurso:verticalizar-edital` |
| Comando | `@tcdf-concurso:reitor-tcdf` |
| Versao | 1.0.0 |

## Por que esta task existe

O squad foi gerado quando o CDN do Cebraspe estava inacessivel pela politica de rede da sessao. A estrutura de provas e a lista de materias vieram de fontes secundarias; as ementas sao ementas-padrao da banca para o perfil do cargo, **nao transcricoes oficiais**.

## Passos

1. Abrir o edital oficial e copiar integralmente a secao de **objetos de avaliacao / conteudo programatico**.
2. Colar aqui. O agente mapeia cada materia para uma entrada de `materias` em `scripts/edital.json`, preenchendo `ementa` com a transcricao literal.
3. Conferir `bloco` e `itens_estimados` contra a distribuicao oficial de itens.
4. Trocar `status_fonte` para `VERIFICADO_NA_FONTE_OFICIAL` e registrar a data.
5. Rodar `python3 scripts/gerar_agentes.py` — os 63 agentes de materia sao reescritos com a ementa oficial.
6. Conferir `python3 scripts/gerar_agentes.py --check` e commitar.

## Atencao

Se o edital for retificado (ja houve retificacao sobre a prova discursiva), repita esta task. Os agentes de coordenacao (`reitor-tcdf`, `estrategista-cebraspe`, `arquiteto-cronograma`, `redator-discursiva`, `mentor-desempenho`) sao escritos a mao e devem ser editados manualmente.
