---
task: simuladoNivel3()
responsavel: "@arbitro-da-progressao"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: pool_vencido
    tipo: string
    origem: templates/mapa-de-progressao.md
    obrigatorio: true
  - campo: resultado_gran
    tipo: string
    origem: User Input (acertos, erros, brancos e tempo por materia)
    obrigatorio: true

Saida:
  - campo: apuracao
    tipo: markdown
    destino: Console
    persistido: false
  - campo: relatorio_semanal
    tipo: markdown
    destino: Arquivo
    persistido: true

Checklist:
  - "[ ] Composicao proporcional calculada a partir do pool vencido"
  - "[ ] 200 questoes (ou reduzido proporcional enquanto o pool < 30 itens)"
  - "[ ] Cronometro de 4 horas, domingo de manha"
  - "[ ] Liquido apurado por grupo e por topico"
  - "[ ] Regressoes declaradas e reencaixadas no dia do grupo"
  - "[ ] Relatorio do mentor-desempenho gerado a tarde"
---

# Task: Simulado de Nivel 3 — Domingo

## Metadata

| Campo | Valor |
|---|---|
| Task ID | `tcdf-concurso:simulado-nivel-3` |
| Comando | `@tcdf:arbitro-da-progressao` |
| Quando | Domingo de manha, cronometrado |

## Objetivo

Provar que o que foi vencido continua vencido, sob carga e sob tempo de prova real.

## Composicao

```
Para cada topico do pool (topicos dos grupos ja vencidos):
  questoes = arredondar(200 x peso_do_topico / soma_dos_pesos_do_pool)
Ajuste o topico de maior peso para fechar exatamente 200.
```

Enquanto o pool somar menos de 30 de peso, rode simulado reduzido na mesma proporcao (minimo 50 questoes). O rito de domingo comeca no primeiro grupo vencido — so o tamanho cresce.

## Fluxo

1. `arbitro-da-progressao` calcula a composicao a partir do mapa.
2. Montar no Gran e resolver em ate 4 horas, sem pausa longa — o objetivo tambem e resistencia.
3. Apurar liquido **por materia**.
4. **Grupo >= 90%** (somados os seus topicos): mantem no pool.
5. **Grupo < 90% em 2 domingos seguidos** ou **< 80% em um domingo**: REGRIDE inteiro para o Nivel 2 e reentra no seu dia da semana.
6. A tarde, `mentor-desempenho` gera o relatorio semanal com a projecao por bloco (P1/P2/P3) contra os minimos do edital.

## Leitura obrigatoria do resultado

O indice do Nivel 3 e o melhor preditor que voce tem. Compare sempre com os minimos reais: P1 >= 7,00 · P2 >= 13,00 · P3 >= 21,00 · conjunto >= 45,00. Um pool com 90% liquido mas concentrado em grupos leves nao diz muito sobre a prova — o `mentor-desempenho` aponta essa distorcao.
