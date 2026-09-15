---
task: montarPlanoDeEstudos()
responsavel: "@arquiteto-cronograma"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: horas_disponiveis
    tipo: string
    origem: User Input
    obrigatorio: true
  - campo: data_alvo
    tipo: string
    origem: User Input
    obrigatorio: true
  - campo: nivel_por_bloco
    tipo: string
    origem: User Input
    obrigatorio: false

Saida:
  - campo: ciclo_de_estudos
    tipo: markdown
    destino: Arquivo/Console
    persistido: true

Checklist:
  - "[ ] Horas liquidas calculadas (80% do declarado)"
  - "[ ] Fatias proporcionais ao peso do edital"
  - "[ ] Revisoes R1/R7/R30 agendadas"
  - "[ ] Slots fixos de revisao, questoes mistas e discursiva definidos"
  - "[ ] Plano de recuperacao para atraso incluido"
---

# Task: Montar Plano de Estudos

## Metadata

| Campo | Valor |
|---|---|
| Task ID | `tcdf-concurso:montar-plano-de-estudos` |
| Comando | `@tcdf-concurso:arquiteto-cronograma` |
| Versao | 1.0.0 |

## Objetivo

Produzir um ciclo de estudos executavel, ponderado pelo peso das 21 materias do edital, com revisao espacada embutida e fases ate a data da prova.

## Passos

1. Levantar horas reais e aplicar o fator de realidade (80%).
2. Converter peso de cada materia (itens/150) em fatia do ciclo.
3. Montar blocos de 50/10 com divisao 60% teoria / 40% questoes.
4. Fixar os slots semanais: revisao geral, questoes mistas e (a partir de D-60) discursiva.
5. Gerar calendario de revisoes e de simulados.
6. Definir a regra de recalculo em caso de atraso.

## Saida esperada

Tabela do ciclo + slots fixos + calendario de revisoes + marcos por fase + regra de ajuste.
