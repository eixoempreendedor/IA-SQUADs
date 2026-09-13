---
task: gerarSimulado()
responsavel: "@<materia>-examinador"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: escopo
    tipo: string
    origem: User Input
    obrigatorio: true
  - campo: quantidade_de_itens
    tipo: number
    origem: User Input
    obrigatorio: true
  - campo: nivel
    tipo: string
    origem: User Input
    obrigatorio: false

Saida:
  - campo: lote_de_itens
    tipo: markdown
    destino: Console
    persistido: false
  - campo: gabarito_comentado
    tipo: markdown
    destino: Console
    persistido: false

Checklist:
  - "[ ] Distribuicao 40/35/15/10 respeitada (lei seca / caso / comparacao / jurisprudencia)"
  - "[ ] Nenhum item ambiguo"
  - "[ ] Gabarito entregue apenas apos a resposta do candidato"
  - "[ ] Placar em liquido (acertos - erros) calculado"
  - "[ ] Erros classificados por causa"
---

# Task: Gerar Simulado / Lote de Itens

## Metadata

| Campo | Valor |
|---|---|
| Task ID | `tcdf-concurso:gerar-simulado` |
| Comando | `@tcdf-concurso:<materia>-examinador` |
| Versao | 1.0.0 |

## Objetivo

Treinar no formato real da prova: itens Certo/Errado, cronometrados, com placar liquido e diagnostico por causa de erro.

## Modos

| Modo | Escopo | Itens | Tempo |
|---|---|---|---|
| Flash | 1 topico | 10 | 15 min |
| Bloco | 1 materia | 20-30 | 40 min |
| Simulado de bloco | P1, P2 ou P3 inteiro | 35 / 45 / 70 | 50 / 65 / 100 min |
| Simulado completo | Prova inteira | 150 | 3h (+1h para P4) |

## Saida esperada

Itens -> (resposta do candidato) -> gabarito -> comentario item a item -> placar liquido -> topicos a retomar.
