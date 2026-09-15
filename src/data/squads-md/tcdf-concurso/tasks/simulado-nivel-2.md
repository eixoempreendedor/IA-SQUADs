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
  - "[ ] Pre-requisito conferido: 70% do peso dos topicos do grupo vencido no Nivel 1 — abaixo disso, roda o lote de rampa"
  - "[ ] Lote no tamanho do grupo (50 ou 60) e na proporcao definida, com no minimo 2 questoes por topico"
  - "[ ] Composicao do dia conferida em data/status-atual.md (oficial ou rampa)"
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

## Antes de tudo: o grupo ja chegou aos 70%?

O simulado oficial so decide quando o grupo tem pelo menos **70% do seu peso vencido no Nivel 1**. Abaixo disso, 50 questoes sobre um grupo estudado pela metade medem sorteio: reprovariam o grupo por conteudo que ainda nem foi visto.

Por isso a manha nunca fica vazia — ela roda em **modo rampa**:

| | Simulado oficial | Lote de rampa |
|---|---|---|
| Quando | grupo com 70%+ do peso vencido | grupo abaixo de 70% |
| Escopo | todos os topicos do grupo | so os topicos ja estudados |
| Tamanho | 50 ou 60 | ~4 questoes por topico estudado (minimo 10, teto no lote oficial) |
| Meta | 90% — decide | 90% — referencia |
| Efeito | grupo VENCIDO ou repete | nenhum no mapa: gera a lista de reforco do dia |

A rampa cresce sozinha: cada topico novo estudado entra nela na semana seguinte, ate o grupo passar dos 70% e a manha virar o simulado oficial. A composicao exata de cada dia (oficial ou rampa) sai calculada em [`data/status-atual.md`](../data/status-atual.md).

Num topico estudado pela metade, a rampa reduz a cota na proporcao do que ja foi visto — nao adianta sortear questoes de subtopico que ainda nao foi aberto.

## Fluxo

1. Conferir a cota do dia em [`data/grupos-de-conteudo.md`](../data/grupos-de-conteudo.md) (lote oficial) ou em [`data/status-atual.md`](../data/status-atual.md) (lote de rampa, enquanto o grupo estiver abaixo de 70%).
2. Montar o simulado no Gran com essa composicao exata — a tabela traz a cota de cada topico, com piso de 2 questoes.
3. Resolver cronometrado (70 ou 85 minutos), pela manha, antes de qualquer conteudo novo.
4. `arbitro-da-progressao` apura o **bruto** (decide) e o **liquido** (projeta), total e por topico.
5. **>= 90% bruto (45/50 ou 54/60)**: grupo VENCIDO — todos os seus topicos entram no pool do Nivel 3; o dia passa a rodar manutencao quinzenal e o tempo liberado vai para os grupos ainda pendentes.
6. **< 90% bruto**: repete no mesmo dia da semana seguinte. Os topicos com pior desempenho recebem revisao dirigida com o `<materia>-revisor` e novos lotes de Nivel 1.
7. **< 70%**: recuo — volta ao Nivel 1 nos topicos piores antes de novo simulado do grupo.
8. **Lote de rampa**: o arbitro apura bruto e liquido e devolve a lista de reforco, sem veredito de grupo. O resultado entra em `scripts/progresso.json` com `"escopo": "rampa"` e `"gate": false`.

## Revisao dirigida (mesma manha)

Depois da apuracao, cada erro vira linha no [diario de erros](../templates/diario-de-erros.md) e cada topico com 2+ erros volta para o revisor da materia no mesmo dia. Simulado sem revisao no mesmo dia perde a maior parte do seu valor.
