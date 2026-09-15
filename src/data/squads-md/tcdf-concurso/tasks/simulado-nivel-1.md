---
task: simuladoNivel1()
responsavel: "@<materia>-examinador"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: tema
    tipo: string
    origem: User Input (topico numerado da ementa oficial, recem-estudado)
    obrigatorio: true
  - campo: resultado_gran
    tipo: string
    origem: User Input (acertos, erros, brancos, tempo)
    obrigatorio: false

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
  - "[ ] Topico INTEIRO estudado (todos os subtopicos da ementa) — se faltou parte, o lote e afericao, nao tentativa"
  - "[ ] 20 questoes do tema (banco do Gran ou lote do examinador)"
  - "[ ] Cronometro de 30 minutos"
  - "[ ] Bruto e liquido apurados pelo arbitro-da-progressao (o bruto decide)"
  - "[ ] Tema marcado como vencido ou encaminhado para reforco"
---

# Task: Simulado de Nivel 1 — Tema

## Metadata

| Campo | Valor |
|---|---|
| Task ID | `tcdf-concurso:simulado-nivel-1` |
| Comando | `@tcdf:<materia>-examinador` → `@tcdf:arbitro-da-progressao` |
| Quando | Tarde/noite, logo apos estudar o tema |

## Objetivo

Fechar o ciclo estudo → questao no mesmo dia: 20 questoes sobre **um topico numerado da ementa**, meta de **90% bruto** (18 acertos em 20). Aprovou, o topico entra vencido no grupo a que pertence e conta para liberar o simulado de Nivel 2 daquele dia.

Qual topico pertence a qual dia esta no `MAPA DE TOPICOS` do agente professor da materia e em [`data/grupos-de-conteudo.md`](../data/grupos-de-conteudo.md). Cada materia fica inteira em um unico dia, entao todo topico de uma materia cai sempre no mesmo grupo.

## A unidade e o topico INTEIRO

O lote de 20 cobre **um topico numerado da ementa com todos os seus subtopicos**. AFO, topico 1, e "Orcamento publico: 1.1 conceito; 1.2 tecnicas orcamentarias; 1.3 principios; 1.4 ciclo; 1.5 processo orcamentario" — estudar 1.1 e 1.2 nao fecha o topico.

Enquanto a ementa do topico nao fecha, o que se resolve e **afericao diagnostica**:

| | Tentativa de Nivel 1 | Afericao |
|---|---|---|
| Escopo | um topico inteiro | parte de um topico, ou varios topicos juntos |
| Tamanho | 20 questoes | o que der (10, 20, 24...) |
| Meta | 90% decide | 90% e referencia, nao decide |
| Se passar | topico VENCIDO | nada muda no mapa |
| Se nao passar | reforco + novo lote em 48h | so aponta o que revisar; **nao conta como tentativa perdida** |

A afericao e util e nao deve ser evitada: e ela que diz, no dia do estudo, se o entendimento pegou. So nao serve para fechar topico — para isso, termine a ementa e faca o lote de 20. As afericoes ficam registradas em `scripts/progresso.json` com `"gate": false` e aparecem em [`data/status-atual.md`](../data/status-atual.md).

## Fluxo

1. `<materia>-professor` da a aula do tema.
2. 20 questoes do tema no Gran (ou lote do `<materia>-examinador` quando o banco nao cobrir o recorte).
3. `arbitro-da-progressao` apura `acertos / 20` (decide) e `(acertos - erros) / 20` (projeta a prova real).
4. **>= 90% bruto (18/20)**: topico VENCIDO no mapa.
5. **< 90% bruto**: reforco com o professor + novo lote de 20 em 48h. Na segunda falha, revisao completa do topico com o `<materia>-revisor` antes de nova tentativa.
6. **Topico ainda aberto** (a ementa nao fechou): o lote e registrado como afericao. O `arbitro-da-progressao` da o numero e o reforco, o topico continua "em estudo" e entra na fila do lote de 20 quando fechar.

## Observacao

20 questoes e uma amostra pequena: 18 acertos e 90%, 17 e 85%. Dois erros ja reprovam o topico — e essa e a ideia. Se o topico reprovar duas vezes por desatencao e nao por conteudo, o encaminhamento e para o `estrategista-cebraspe`, nao para o professor.
