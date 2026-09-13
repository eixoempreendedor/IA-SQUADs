---
task: simuladoNivel2()
responsavel: "@arbitro-da-progressao"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: grupo
    tipo: string
    origem: data/grupos-de-conteudo.md (grupo do dia)
    obrigatorio: true
  - campo: resultado_gran
    tipo: string
    origem: User Input (acertos, erros, brancos, tempo, por materia)
    obrigatorio: true

Saida:
  - campo: veredito
    tipo: markdown
    destino: Console
    persistido: false
  - campo: mapa_atualizado
    tipo: markdown
    destino: templates/mapa-de-progressao.md
    persistido: true

Checklist:
  - "[ ] Pre-requisito conferido: 70% do peso dos topicos do grupo vencido no Nivel 1"
  - "[ ] Lote no tamanho do grupo (50 ou 60) e na proporcao definida, com no minimo 2 questoes por topico"
  - "[ ] Cronometro (70 min no lote de 50, 85 min no de 60), pela manha, antes de conteudo novo"
  - "[ ] Resultado apurado por materia e por topico, nao so no total"
  - "[ ] Revisao dirigida dos erros feita no mesmo dia"
---

# Task: Simulado de Nivel 2 — Grupo de Conteudo

## Metadata

| Campo | Valor |
|---|---|
| Task ID | `tcdf-concurso:simulado-nivel-2` |
| Comando | `@tcdf:arbitro-da-progressao` |
| Quando | Manha do dia fixo do grupo (seg a sab) |

## Objetivo

Decidir se o grupo de conteudo do dia esta vencido. Lote de **50 ou 60 questoes** conforme o numero de topicos do grupo (50 ate 14 topicos, 60 de 15 em diante), meta de **90% bruto** — 45/50 ou 54/60.

## Fluxo

1. Conferir a cota do dia em [`data/grupos-de-conteudo.md`](../data/grupos-de-conteudo.md).
2. Montar o simulado no Gran com essa composicao exata — a tabela traz a cota de cada topico, com piso de 2 questoes.
3. Resolver cronometrado (70 ou 85 minutos), pela manha, antes de qualquer conteudo novo.
4. `arbitro-da-progressao` apura o **bruto** (decide) e o **liquido** (projeta), total e por topico.
5. **>= 90% bruto (45/50 ou 54/60)**: grupo VENCIDO — todos os seus topicos entram no pool do Nivel 3; o dia passa a rodar manutencao quinzenal e o tempo liberado vai para os grupos ainda pendentes.
6. **< 90% bruto**: repete no mesmo dia da semana seguinte. Os topicos com pior desempenho recebem revisao dirigida com o `<materia>-revisor` e novos lotes de Nivel 1.
7. **< 70%**: recuo — volta ao Nivel 1 nos topicos piores antes de novo simulado do grupo.

## Revisao dirigida (mesma manha)

Depois da apuracao, cada erro vira linha no [diario de erros](../templates/diario-de-erros.md) e cada topico com 2+ erros volta para o revisor da materia no mesmo dia. Simulado sem revisao no mesmo dia perde a maior parte do seu valor.
