---
task: diagnosticoDeErros()
responsavel: "@mentor-desempenho"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: resultados
    tipo: string
    origem: User Input / examinadores
    obrigatorio: true
  - campo: aderencia_ao_ciclo
    tipo: string
    origem: User Input
    obrigatorio: false

Saida:
  - campo: relatorio_semanal
    tipo: markdown
    destino: Arquivo
    persistido: true

Checklist:
  - "[ ] Liquido por materia e por bloco calculado"
  - "[ ] Projecao comparada aos minimos do edital (7 / 13 / 21 e 45 global)"
  - "[ ] Causa dominante do erro identificada"
  - "[ ] No maximo 3 ajustes propostos, com agente responsavel"
---

# Task: Diagnostico de Erros e Ajuste de Rota

## Metadata

| Campo | Valor |
|---|---|
| Task ID | `tcdf-concurso:diagnostico-de-erros` |
| Comando | `@tcdf-concurso:mentor-desempenho` |
| Versao | 1.0.0 |

## Objetivo

Converter resultados em decisao: o que muda na proxima semana, quem executa e como sera medido.

## Roteamento por causa de erro

| Causa | Destino |
|---|---|
| Desconhecimento | `<materia>-professor` |
| Esquecimento | `<materia>-revisor` (encurtar intervalo) |
| Desatencao / pressa | `estrategista-cebraspe` |
| Ma interpretacao | `lingua-portuguesa-professor` + `estrategista-cebraspe` |
| Baixa aderencia ao plano | `arquiteto-cronograma` |
