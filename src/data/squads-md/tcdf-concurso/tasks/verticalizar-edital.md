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
  - "[ ] status_fonte e observacao_fonte atualizados com a data e o numero da retificacao"
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

O conteudo programatico atual foi transcrito do **item 15 do edital de abertura**, ja com o Edital nº 2 – TCDF/ANACE, de 29/7/2026 (`status_fonte: VERIFICADO_NA_FONTE_OFICIAL`). Esta task existe para manter isso verdadeiro: a cada nova retificacao, o texto oficial volta para `scripts/edital.json` e os agentes se regeneram.

## Passos

1. Abrir o edital oficial e copiar integralmente a secao de **objetos de avaliacao / conteudo programatico**.
2. Colar aqui. O agente mapeia cada materia para uma entrada de `materias` em `scripts/edital.json`, preenchendo `ementa` com a transcricao literal.
3. Conferir `bloco` e `itens_estimados` contra a distribuicao oficial de itens.
4. Trocar `status_fonte` para `VERIFICADO_NA_FONTE_OFICIAL` e registrar a data.
5. Rodar os geradores — os agentes de materia e o `reitor-tcdf` sao reescritos com a ementa oficial:

```bash
python3 scripts/gerar_agentes.py
python3 scripts/gerar_progressao.py
python3 scripts/gerar_readme.py
python3 scripts/sync_app_registry.py
```

6. Se uma materia entrou ou saiu, encaixe-a em um grupo no `scripts/progressao.json` antes de rodar (o gerador acusa materia sem grupo).
7. Conferir com `--check`, rodar `npm run build` e commitar.

## Atencao

O `reitor-tcdf` e gerado e nao precisa de edicao manual. Os demais agentes de coordenacao (`estrategista-cebraspe`, `arquiteto-cronograma`, `redator-discursiva`, `mentor-desempenho`, `arbitro-da-progressao`) sao escritos a mao: se a retificacao mexer em estrutura de prova, duracao, minimos ou criterios da discursiva, revise esses arquivos manualmente.
