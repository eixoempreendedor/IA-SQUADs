---
task: corrigirDiscursiva()
responsavel: "@redator-discursiva"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: enunciado
    tipo: string
    origem: User Input
    obrigatorio: true
  - campo: texto_do_candidato
    tipo: string
    origem: User Input
    obrigatorio: true

Saida:
  - campo: espelho_de_correcao
    tipo: markdown
    destino: Console
    persistido: false
  - campo: nota_estimada
    tipo: markdown
    destino: Console
    persistido: false

Checklist:
  - "[ ] Espelho com quesitos montado antes da correcao"
  - "[ ] Limite de linhas verificado"
  - "[ ] Estrutura da peca conferida contra o padrao de atos oficiais do TCDF"
  - "[ ] Quesitos ausentes apontados com o local onde caberiam"
  - "[ ] Trecho-modelo reescrito entregue"
---

# Task: Corrigir Discursiva (P4)

## Metadata

| Campo | Valor |
|---|---|
| Task ID | `tcdf-concurso:corrigir-discursiva` |
| Comando | `@tcdf-concurso:redator-discursiva` |
| Versao | 1.0.0 |

## Objetivo

Corrigir a questao discursiva (ate 20 linhas / 15,00 pontos) e a peca tecnica tipo Informacao (ate 50 linhas / 35,00 pontos) com espelho, nota por criterio e reescrita modelo.

## Criterios de correcao

Estrutura da peca · dominio do conteudo · fundamentacao normativa · coesao e coerencia · correcao gramatical · limite de linhas.
