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
  - "[ ] Pre-requisito conferido: 70% dos temas do grupo vencidos no Nivel 1"
  - "[ ] 50 questoes na proporcao definida para o grupo"
  - "[ ] Cronometro de 70 minutos, pela manha, antes de conteudo novo"
  - "[ ] Resultado apurado por materia, nao so no total"
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

Decidir se o grupo de conteudo do dia esta vencido. 50 questoes na proporcao do grupo, meta de 90% liquido.

## Fluxo

1. Conferir a cota do dia em [`data/grupos-de-conteudo.md`](../data/grupos-de-conteudo.md).
2. Montar o simulado no Gran com essa composicao exata.
3. Resolver cronometrado (70 minutos), pela manha, antes de qualquer conteudo novo.
4. `arbitro-da-progressao` apura o liquido **total e por materia**.
5. **>= 90%**: grupo VENCIDO, entra no pool do Nivel 3; o dia passa a rodar manutencao quinzenal e o tempo liberado vai para os grupos ainda pendentes.
6. **< 90%**: repete no mesmo dia da semana seguinte. As materias com pior liquido recebem revisao dirigida com o `<materia>-revisor` e novos lotes de Nivel 1 nos temas fracos.
7. **< 70%**: recuo — volta ao Nivel 1 nos temas piores antes de novo simulado do grupo.

## Revisao dirigida (mesma manha)

Depois da apuracao, cada erro vira linha no [diario de erros](../templates/diario-de-erros.md) e cada tema com 2+ erros volta para o revisor da materia no mesmo dia. Simulado sem revisao no mesmo dia perde a maior parte do seu valor.
