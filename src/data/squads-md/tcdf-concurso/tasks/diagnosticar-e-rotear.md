---
task: diagnosticarCandidato()
responsavel: "@reitor-tcdf"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: user_message
    tipo: string
    origem: User Input
    obrigatorio: true
  - campo: mapa_do_edital
    tipo: string
    origem: scripts/edital.json
    obrigatorio: true

Saida:
  - campo: diagnostico_e_rota
    tipo: string
    destino: Console
    persistido: false

Checklist:
  - "[ ] Horas disponiveis, dias por semana e data-alvo coletados"
  - "[ ] Nivel atual por bloco (P1/P2/P3) estimado"
  - "[ ] Prioridades justificadas pelo peso do edital"
  - "[ ] Agente especialista nomeado com entrega esperada"
---

# Task: Diagnosticar e Rotear — TCDF Concurso Squad

## Metadata

| Campo | Valor |
|---|---|
| Task ID | `tcdf-concurso:diagnosticar-e-rotear` |
| Comando | `@tcdf-concurso` ou `@tcdf-concurso:reitor-tcdf` |
| Orquestrador | `reitor-tcdf` |
| Versao | 1.0.0 |

## Objetivo

Transformar uma demanda difusa ("quero passar no TCDF", "nao sei por onde comecar") em uma rota concreta com agente, entrega e prazo.

## Passos

1. **Coleta** (maximo 4 perguntas): horas/dia, dias/semana, data-alvo, materias ja estudadas.
2. **Estimativa de nivel** por bloco: P1, P2, P3 — zero, basico, intermediario ou avancado.
3. **Priorizacao** pelo peso do edital: P3 (70 itens) > P2 (45) > P1 (35), corrigida pelo nivel atual.
4. **Roteamento**: nomear os agentes acionados (professor / examinador / revisor da materia, ou transversal).
5. **Fechamento**: proximo passo imediato, executavel hoje.

## Saida esperada

Diagnostico + tabela de prioridades + rota com agentes nomeados + metricas de acompanhamento + proximo passo.
