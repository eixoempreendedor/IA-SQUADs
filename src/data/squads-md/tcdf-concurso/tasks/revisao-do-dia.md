---
task: revisaoDoDia()
responsavel: "@<materia>-revisor"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: topicos_pendentes
    tipo: string
    origem: User Input / cronograma
    obrigatorio: true
  - campo: ultima_revisao
    tipo: string
    origem: User Input
    obrigatorio: false

Saida:
  - campo: sessao_de_revisao
    tipo: markdown
    destino: Console
    persistido: false
  - campo: flashcards
    tipo: markdown
    destino: Arquivo
    persistido: true

Checklist:
  - "[ ] Sessao iniciada por recuperacao ativa, nao por releitura"
  - "[ ] Nivel de dominio atribuido a cada topico"
  - "[ ] Flashcards gerados para cada lacuna"
  - "[ ] Data da proxima revisao definida por topico"
---

# Task: Revisao do Dia

## Metadata

| Campo | Valor |
|---|---|
| Task ID | `tcdf-concurso:revisao-do-dia` |
| Comando | `@tcdf-concurso:<materia>-revisor` |
| Versao | 1.0.0 |

## Objetivo

Executar a revisao espacada do dia com recuperacao ativa e devolver a agenda atualizada de retorno de cada topico.

## Intervalos

R1 = 24h · R2 = 7 dias · R3 = 30 dias · R4 = reta final · Vespera = so critico.
