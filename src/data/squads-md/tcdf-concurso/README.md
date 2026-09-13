# TCDF Concurso Squad 🎓

**54 agentes de IA para aprovacao no concurso de Analista Administrativo de Controle Externo do TCDF (Cebraspe, 2026).**

Sao **3 agentes para cada uma das 16 materias do edital** — um professor, um examinador e um revisor — mais **6 agentes de coordenacao** que cuidam de estrategia de prova, cronograma, discursiva, desempenho e progressao por niveis.

| | |
|---|---|
| **Orgao** | Tribunal de Contas do Distrito Federal (TCDF) |
| **Cargo** | Analista Administrativo de Controle Externo — Área de Gestão — Serviços Técnico-Administrativos (ANACE) |
| **Banca** | Cebraspe |
| **Vagas** | 10 vagas imediatas (5 ampla concorrência, 2 PcD, 2 negros, 1 hipossuficiente) + cadastro de reserva |
| **Remuneracao inicial** | R$ 14.990,41 (Lei Distrital nº 7.860/2026) |
| **Escolaridade** | Nível superior em qualquer área de formação |
| **Provas** | 22/11/2026 — objetivas pela manhã, discursiva à tarde |
| **Duracao** | 4 horas para as provas objetivas e 4 horas para a prova discursiva |
| **Formato** | Certo/Errado: +1,00 ponto por acerto, -1,00 ponto por erro, 0,00 em branco ou marcação dupla |

## Fonte do conteudo

**`VERIFICADO_NA_FONTE_OFICIAL`** — Conteúdo programático transcrito do item 15 (Dos objetos de avaliação) do edital de abertura, já com as alterações do Edital nº 2 – TCDF/ANACE, de 29 de julho de 2026. Verificado em 13/9/2026.

Se houver nova retificacao, rode a task [`tasks/verticalizar-edital.md`](tasks/verticalizar-edital.md): o conteudo programatico e dado (`scripts/edital.json`), nao codigo, e os agentes se regeneram com um comando.

## Estrutura das provas

| Prova | Conteudo | Itens | Minimo |
|---|---|---|---|
| P1 | Conhecimentos Básicos | 35 | 7,00 pontos |
| P2 | Conhecimentos Específicos | 45 | 13,00 pontos |
| P3 | Conhecimentos Especializados | 70 | 21,00 pontos |
| P4 | Prova Discursiva | — | 50,00 pontos no total: questão discursiva de até 20 linhas (15,00) + peça de natureza técnica (Informação) de até 50 linhas (35,00), na estrutura do padrão unificado de apresentação de atos oficiais do Manual de Redação Oficial do TCDF (2ª edição) |

Minimo global nas objetivas: **45,00 pontos na soma de P1 + P2 + P3**. Só é corrigida a discursiva dos mais bem classificados nas objetivas: 120 na ampla concorrência, 48 PcD, 48 negros e 24 hipossuficientes.

## Os 3 papeis por materia

| Papel | O que faz | Quando acionar |
|---|---|---|
| 🧑‍🏫 **Professor** | Ensina o topico no recorte exato da banca: conceito, exemplo, tabela comparativa, pegadinhas, resumo e 3 itens de fixacao | Conteudo novo, duvida conceitual, resumo ou mapa mental |
| 🎯 **Examinador** | Escreve itens Certo/Errado no padrao Cebraspe, aplica simulado cronometrado e comenta o gabarito com o mecanismo de erro usado | Treinar, simular, entender por que errou |
| 🔁 **Revisor** | Revisao espacada (R1/R7/R30), flashcards, diario de erros e revisao de vespera | Manter vivo o que ja foi aprendido |

## Agentes de coordenacao

| Agente | Funcao |
|---|---|
| 🎓 `reitor-tcdf` | Orquestrador e porta de entrada: diagnostica, prioriza pelo peso do edital e roteia |
| ♟️ `estrategista-cebraspe` | Tecnica de prova C/E, politica de chute, gestao de tempo, recursos |
| 🗓️ `arquiteto-cronograma` | Ciclo de estudos ponderado pelo edital, revisoes embutidas, reta final |
| ✍️ `redator-discursiva` | P4: questao discursiva e peca tecnica Informacao, com espelho de correcao |
| 📈 `mentor-desempenho` | Metricas, diario de erros, projecao por bloco e ajuste de rota semanal |
| ⚖️ `arbitro-da-progressao` | Apura cada simulado, aplica o criterio de 90% e declara avanco, repeticao ou regressao |

## Mapa das materias

| Materia | Bloco | Itens est. | Prioridade | Professor | Examinador | Revisor |
|---|---|---|---|---|---|---|
| 📝 **Língua Portuguesa** | P1 | 12 | alta | `lingua-portuguesa-professor` | `lingua-portuguesa-examinador` | `lingua-portuguesa-revisor` |
| 🏛️ **Lei Orgânica do Distrito Federal** | P1 | 6 | alta | `lei-organica-df-professor` | `lei-organica-df-examinador` | `lei-organica-df-revisor` |
| 🌆 **Conhecimentos do Distrito Federal e Política para Mulheres** | P1 | 4 | media | `conhecimentos-df-politica-mulheres-professor` | `conhecimentos-df-politica-mulheres-examinador` | `conhecimentos-df-politica-mulheres-revisor` |
| 🚑 **Noções de Primeiros Socorros** | P1 | 3 | baixa | `nocoes-primeiros-socorros-professor` | `nocoes-primeiros-socorros-examinador` | `nocoes-primeiros-socorros-revisor` |
| 🧮 **Raciocínio Lógico e Matemática Financeira** | P1 | 10 | alta | `raciocinio-logico-matematica-financeira-professor` | `raciocinio-logico-matematica-financeira-examinador` | `raciocinio-logico-matematica-financeira-revisor` |
| ⚖️ **Lei Orgânica do TCDF e Regimento Interno** | P2 | 10 | critica | `lei-organica-regimento-tcdf-professor` | `lei-organica-regimento-tcdf-examinador` | `lei-organica-regimento-tcdf-revisor` |
| 📜 **Direito Constitucional** | P2 | 10 | critica | `direito-constitucional-professor` | `direito-constitucional-examinador` | `direito-constitucional-revisor` |
| 🧓 **Direito Previdenciário** | P2 | 8 | alta | `direito-previdenciario-professor` | `direito-previdenciario-examinador` | `direito-previdenciario-revisor` |
| 📕 **Noções de Direito Civil** | P2 | 6 | media | `nocoes-direito-civil-professor` | `nocoes-direito-civil-examinador` | `nocoes-direito-civil-revisor` |
| 💰 **Noções de Direito Tributário** | P2 | 5 | media | `nocoes-direito-tributario-professor` | `nocoes-direito-tributario-examinador` | `nocoes-direito-tributario-revisor` |
| 🤖 **Análise de Dados, Noções de Estatística e Inteligência Artificial** | P2 | 6 | alta | `analise-dados-estatistica-ia-professor` | `analise-dados-estatistica-ia-examinador` | `analise-dados-estatistica-ia-revisor` |
| 🏢 **Direito Administrativo** | P3 | 22 | critica | `direito-administrativo-professor` | `direito-administrativo-examinador` | `direito-administrativo-revisor` |
| 📊 **Administração Financeira e Orçamentária** | P3 | 16 | critica | `administracao-financeira-orcamentaria-professor` | `administracao-financeira-orcamentaria-examinador` | `administracao-financeira-orcamentaria-revisor` |
| 🏗️ **Administração Geral e Pública** | P3 | 16 | critica | `administracao-geral-e-publica-professor` | `administracao-geral-e-publica-examinador` | `administracao-geral-e-publica-revisor` |
| 👤 **Regime Jurídico dos Servidores Públicos Civis do DF (LC 840/2011)** | P3 | 8 | alta | `regime-juridico-servidores-df-professor` | `regime-juridico-servidores-df-examinador` | `regime-juridico-servidores-df-revisor` |
| 📑 **Gestão de Contratos** | P3 | 8 | alta | `gestao-de-contratos-professor` | `gestao-de-contratos-examinador` | `gestao-de-contratos-revisor` |

> A distribuicao de itens por materia e **estimativa** ponderada pelo tamanho da ementa e pelo historico da banca: o edital fixa o total de cada bloco (35 / 45 / 70), nao o total por materia.

## Progressao por niveis (90% para avancar)

O estudo avanca por **resultado medido**, nao por tempo estudado. Questoes do **Gran Cursos (banco de questoes)**, criterio de **90% liquido** (`(acertos - erros) / total de questoes do lote`).

| Nivel | Unidade | Questoes | Quando | Aprovado gera |
|---|---|---|---|---|
| **1 — Tema** | Um topico da ementa da materia (ex.: Titulo 1 de Direito Constitucional, Ato Administrativo) | 20 | Logo apos estudar o tema, no mesmo dia | Tema marcado como VENCIDO e liberado para compor o simulado de Nivel 2 do grupo |
| **2 — Grupo de conteudo** | Um dos 6 grupos de conteudo (seg a sab) | 50 | Manha do dia fixo do grupo, antes de qualquer conteudo novo | Grupo marcado como VENCIDO e incluido no pool do Nivel 3; o dia passa a rodar manutencao quinzenal |
| **3 — Simulado geral** | Todas as materias ja vencidas no Nivel 2 | 200 | Domingo de manha, cronometrado | Materia confirmada no pool; segue em manutencao semanal sem voltar ao Nivel 2 |

### Grupos de conteudo (seg a sab)

| Dia | Grupo | Itens | Materias | Cotas no simulado de 50 |
|---|---|---|---|---|
| Segunda-feira | **Direito Administrativo e Contratações** | 30 | Direito Administrativo · Gestão de Contratos | 37 · 13 |
| Terça-feira | **Orçamento e Finanças Públicas** | 22 | Administração Financeira e Orçamentária · Lei Orgânica do Distrito Federal | 36 · 14 |
| Quarta-feira | **Constitucional e Institucional** | 20 | Direito Constitucional · Lei Orgânica do TCDF e Regimento Interno | 25 · 25 |
| Quinta-feira | **Gestão e Dados** | 22 | Administração Geral e Pública · Análise de Dados, Noções de Estatística e Inteligência Artificial | 36 · 14 |
| Sexta-feira | **Servidor e Direitos Complementares** | 27 | Regime Jurídico dos Servidores Públicos Civis do DF (LC 840/2011) · Direito Previdenciário · Noções de Direito Civil · Noções de Direito Tributário | 15 · 15 · 11 · 9 |
| Sábado | **Instrumentais e Distrito Federal** | 29 | Língua Portuguesa · Raciocínio Lógico e Matemática Financeira · Conhecimentos do Distrito Federal e Política para Mulheres · Noções de Primeiros Socorros | 21 · 17 · 7 · 5 |
| Domingo | **Nivel 3 — simulado geral** | pool vencido | Todas as materias vencidas | 200 proporcionais |

Composicao completa, regras de avanco e de regressao: [`data/grupos-de-conteudo.md`](data/grupos-de-conteudo.md). Acompanhamento: [`templates/mapa-de-progressao.md`](templates/mapa-de-progressao.md).

Para mudar grupos, cotas, meta ou metrica, edite `scripts/progressao.json` e rode `python3 scripts/gerar_progressao.py`.

## Como usar

```
@tcdf                                     # reitor-tcdf (diagnostico e rota)
@tcdf:direito-administrativo-professor    # aula de um topico
@tcdf:direito-administrativo-examinador   # lote de itens C/E
@tcdf:direito-administrativo-revisor      # revisao espacada e flashcards
@tcdf:arbitro-da-progressao               # apurar simulado e declarar avanco
@tcdf:arquiteto-cronograma                # montar o ciclo de estudos
@tcdf:redator-discursiva                  # treinar e corrigir a P4
```

Cada arquivo `.md` de agente e autossuficiente (persona, ementa oficial da materia, regras de comportamento e formato de saida), entao funciona tambem fora do app, colado direto em qualquer ferramenta de agentes.

## Fluxos prontos

| Workflow | Quando |
|---|---|
| [`wf-primeira-semana`](workflows/wf-primeira-semana.yaml) | Voce esta comecando agora |
| [`wf-ciclo-semanal`](workflows/wf-ciclo-semanal.yaml) | Rotina padrao de uma semana |
| [`wf-progressao-por-niveis`](workflows/wf-progressao-por-niveis.yaml) | Sistema de 90% para avancar |
| [`wf-reta-final`](workflows/wf-reta-final.yaml) | Ultimos 60 dias |

## Tasks

`aula-de-topico` · `corrigir-discursiva` · `diagnosticar-e-rotear` · `diagnostico-de-erros` · `gerar-simulado` · `montar-plano-de-estudos` · `revisao-do-dia` · `simulado-nivel-1` · `simulado-nivel-2` · `simulado-nivel-3` · `verticalizar-edital`

## Templates

[`mapa-de-progressao.md`](templates/mapa-de-progressao.md) · [`diario-de-erros.md`](templates/diario-de-erros.md) · [`folha-de-simulado.md`](templates/folha-de-simulado.md) · [`flashcards.md`](templates/flashcards.md)

## Regenerar

Os 48 agentes de materia e o `reitor-tcdf` sao **gerados** a partir de `scripts/edital.json`; os grupos e niveis, a partir de `scripts/progressao.json`.

```bash
python3 scripts/gerar_agentes.py        # agentes, squad.yaml, data/
python3 scripts/gerar_progressao.py     # grupos de conteudo e mapa de progressao
python3 scripts/gerar_readme.py         # este README
python3 scripts/sync_app_registry.py    # registra o squad em squads.ts e agents.ts
```

Os outros 5 agentes de coordenacao sao escritos a mao e nao sao sobrescritos.

Para adicionar uma materia: acrescente um objeto em `materias` no `edital.json`, encaixe-a em um grupo no `progressao.json` e rode os geradores — os 3 agentes nascem prontos e os documentos se atualizam.

## Estrutura de arquivos

```
tcdf-concurso/
├── squad.yaml                  # manifesto (gerado)
├── README.md                   # (gerado)
├── agents/                     # 54 agentes (.md)
├── tasks/                      # 11 tasks
├── workflows/                  # 4 workflows
├── checklists/                 # qualidade de item C/E, peca Informacao
├── templates/                  # mapa de progressao, diario de erros, simulado, flashcards
├── data/                       # edital verticalizado, grupos de conteudo, roteamento (gerados)
└── scripts/
    ├── edital.json             # FONTE DA VERDADE do conteudo
    ├── progressao.json         # FONTE DA VERDADE dos grupos e niveis
    └── *.py                    # geradores
```

## Limites

- Os agentes nao substituem a leitura do edital oficial nem do material de aula.
- Nenhum agente estima probabilidade de aprovacao ou nota de corte como certeza.
- Prazos, percentuais e quoruns devem ser conferidos na norma: os agentes sao instruidos a sinalizar quando nao tiverem certeza, mas a conferencia final e sua.
