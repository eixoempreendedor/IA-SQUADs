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
  - "[ ] 20 questoes do tema (banco do Gran ou lote do examinador)"
  - "[ ] Cronometro de 30 minutos"
  - "[ ] Liquido apurado pelo arbitro-da-progressao"
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

Fechar o ciclo estudo → questao no mesmo dia: 20 questoes sobre **um topico numerado da ementa**, meta de 90% liquido. Aprovou, o topico entra vencido no grupo a que pertence e conta para liberar o simulado de Nivel 2 daquele dia.

Qual topico pertence a qual dia esta no `MAPA DE TOPICOS` do agente professor da materia e em [`data/grupos-de-conteudo.md`](../data/grupos-de-conteudo.md). Atencao: a mesma materia pode ter topicos em dias diferentes — Direito Administrativo, por exemplo, aparece em quatro dias.

## Fluxo

1. `<materia>-professor` da a aula do tema.
2. 20 questoes do tema no Gran (ou lote do `<materia>-examinador` quando o banco nao cobrir o recorte).
3. `arbitro-da-progressao` apura: `(acertos - erros) / 20`.
4. **>= 90%**: tema VENCIDO no mapa.
5. **< 90%**: reforco com o professor + novo lote de 20 em 48h. Na segunda falha, revisao completa do tema com o `<materia>-revisor` antes de nova tentativa.

## Observacao

20 questoes e uma amostra pequena: 18 acertos e 90%, 17 e 85%. Um unico erro bobo reprova o tema — e essa e a ideia. Se o tema reprovar duas vezes por desatencao e nao por conteudo, o encaminhamento e para o `estrategista-cebraspe`, nao para o professor.
