---
task: aulaDeTopico()
responsavel: "@<materia>-professor"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: materia_id
    tipo: string
    origem: User Input
    obrigatorio: true
  - campo: topico
    tipo: string
    origem: User Input
    obrigatorio: true
  - campo: nivel_atual
    tipo: string
    origem: User Input
    obrigatorio: false

Saida:
  - campo: aula
    tipo: markdown
    destino: Console
    persistido: false

Checklist:
  - "[ ] Topico ancorado na ementa oficial da materia"
  - "[ ] Exemplo, contraexemplo e excecao apresentados"
  - "[ ] Tabela comparativa dos institutos confundiveis"
  - "[ ] Pegadinhas da banca listadas"
  - "[ ] Resumo de 5 linhas + 3 itens C/E de fixacao"
---

# Task: Aula de Topico

## Metadata

| Campo | Valor |
|---|---|
| Task ID | `tcdf-concurso:aula-de-topico` |
| Comando | `@tcdf-concurso:<materia>-professor` |
| Versao | 1.0.0 |

## Objetivo

Ensinar um topico especifico da ementa no recorte exato em que a Cebraspe cobra, terminando em fixacao imediata.

## Saida esperada

O que cai -> conceito -> destrinchamento -> tabela -> pegadinhas -> resumo -> 3 itens C/E comentados.
