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
| 📜 **Direito Constitucional** | P2 | 12 | critica | `direito-constitucional-professor` | `direito-constitucional-examinador` | `direito-constitucional-revisor` |
| 🧓 **Direito Previdenciário** | P2 | 8 | alta | `direito-previdenciario-professor` | `direito-previdenciario-examinador` | `direito-previdenciario-revisor` |
| 📕 **Noções de Direito Civil** | P2 | 6 | media | `nocoes-direito-civil-professor` | `nocoes-direito-civil-examinador` | `nocoes-direito-civil-revisor` |
| 💰 **Noções de Direito Tributário** | P2 | 4 | media | `nocoes-direito-tributario-professor` | `nocoes-direito-tributario-examinador` | `nocoes-direito-tributario-revisor` |
| 🤖 **Análise de Dados, Noções de Estatística e Inteligência Artificial** | P2 | 5 | alta | `analise-dados-estatistica-ia-professor` | `analise-dados-estatistica-ia-examinador` | `analise-dados-estatistica-ia-revisor` |
| 🏢 **Direito Administrativo** | P3 | 25 | critica | `direito-administrativo-professor` | `direito-administrativo-examinador` | `direito-administrativo-revisor` |
| 📊 **Administração Financeira e Orçamentária** | P3 | 15 | critica | `administracao-financeira-orcamentaria-professor` | `administracao-financeira-orcamentaria-examinador` | `administracao-financeira-orcamentaria-revisor` |
| 🏗️ **Administração Geral e Pública** | P3 | 15 | critica | `administracao-geral-e-publica-professor` | `administracao-geral-e-publica-examinador` | `administracao-geral-e-publica-revisor` |
| 👤 **Regime Jurídico dos Servidores Públicos Civis do DF (LC 840/2011)** | P3 | 8 | alta | `regime-juridico-servidores-df-professor` | `regime-juridico-servidores-df-examinador` | `regime-juridico-servidores-df-revisor` |
| 📑 **Gestão de Contratos** | P3 | 7 | alta | `gestao-de-contratos-professor` | `gestao-de-contratos-examinador` | `gestao-de-contratos-revisor` |

> O edital fixa o total de itens por bloco (35/45/70), não por matéria nem por tópico. Os pesos por tópico são estimativa própria, usada para dimensionar grupos de estudo e cotas de simulado.

> O edital tem **87 topicos numerados** no total. Cada um e uma unidade de Nivel 1 e pertence a exatamente um grupo de conteudo.

## Progressao por niveis (90% para avancar)

O estudo avanca por **resultado medido**, nao por tempo estudado. Questoes do **Gran Cursos (banco de questoes)**.

**Avanca com 90% bruto** (`acertos / total de questões do lote`). Questão deixada em branco conta como não-acerto no denominador. O lote precisa ser respondido inteiro — senão bastaria responder só o que se sabe para bater a meta.

O **líquido** (`(acertos - erros) / total de questões do lote`) e apurado sempre ao lado, mas nao decide avanco: ele e o placar da prova real, em que cada erro anula um acerto.

| Nivel | Unidade | Questoes | Quando | Aprovado gera |
|---|---|---|---|---|
| **1 — Tema** | Um tópico numerado da ementa oficial (ex.: Direito Administrativo, tópico 3 — Ato administrativo) | 20 | Logo apos estudar o tema, no mesmo dia | Tópico marcado como VENCIDO e liberado para compor o simulado de Nível 2 do grupo a que ele pertence |
| **2 — Grupo de conteudo** | Um dos 6 grupos de conteúdo (conjunto de tópicos de matérias diferentes que se estudam juntos) | 50 ou 60, conforme o número de tópicos do grupo | Manhã do dia fixo do grupo, antes de qualquer conteúdo novo | Grupo marcado como VENCIDO e incluido no pool do Nivel 3; o dia passa a rodar manutencao quinzenal |
| **3 — Simulado geral** | Todos os tópicos dos grupos já vencidos no Nível 2 | 200 | Domingo de manha, cronometrado | Grupo confirmado no pool; segue em manutenção semanal sem voltar ao Nível 2 |

### Grupos de conteudo (seg a sab)

Cada matéria do edital fica INTEIRA em um único dia — nenhuma matéria é repartida entre dias. Os grupos reúnem matérias que compartilham norma ou vocabulário, de modo que estudar uma adianta a outra. Dentro do dia, a unidade de Nível 1 continua sendo o tópico numerado do edital.

| Dia | Grupo | Peso est. | Simulado | Materias — cota |
|---|---|---|---|---|
| Segunda-feira | **Orçamento e Tributação** | 19 | **50q** (meta 45) | Administração Financeira e Orçamentária 39q · Noções de Direito Tributário 11q |
| Terça-feira | **Direito Administrativo e Contratações** | 32 | **60q** (meta 54) | Direito Administrativo 51q · Gestão de Contratos 9q |
| Quarta-feira | **Controle Externo e Organização do Estado** | 28 | **60q** (meta 54) | Direito Constitucional 30q · Lei Orgânica do TCDF e Regimento Interno 14q · Lei Orgânica do Distrito Federal 16q |
| Quinta-feira | **Gestão e Dados** | 20 | **50q** (meta 45) | Administração Geral e Pública 35q · Análise de Dados, Noções de Estatística e Inteligência Artificial 15q |
| Sexta-feira | **Servidores, Previdência e Direito Civil** | 22 | **50q** (meta 45) | Regime Jurídico dos Servidores Públicos Civis do DF (LC 840/2011) 12q · Direito Previdenciário 20q · Noções de Direito Civil 18q |
| Sábado | **Instrumentais e Distrito Federal** | 29 | **60q** (meta 54) | Língua Portuguesa 23q · Raciocínio Lógico e Matemática Financeira 23q · Conhecimentos do Distrito Federal e Política para Mulheres 10q · Noções de Primeiros Socorros 4q |
| Domingo | **Nivel 3 — simulado geral** | pool vencido | 200q (meta 180) | proporcional ao peso dos topicos vencidos |

Tamanho do lote de Nivel 2: lote de 50 questões para grupos com até 14 tópicos e de 60 para grupos com 15 ou mais, de modo que todo dia fique entre 3,5 e 4,5 questões por tópico, com piso de 2 questoes por topico. Teto de **450 questoes por semana** — acima disso o `arquiteto-cronograma` corta primeiro a manutencao dos grupos ja vencidos, nunca o Nivel 1 do conteudo novo.

Composicao completa, regras de avanco e de regressao: [`data/grupos-de-conteudo.md`](data/grupos-de-conteudo.md). Estado atual, apurado dos simulados ja feitos: [`data/status-atual.md`](data/status-atual.md).

Para registrar um simulado, acrescente uma linha em `scripts/progresso.json` e rode `python3 scripts/gerar_status.py` — ele recalcula topicos vencidos, prontidao de cada grupo, pool do Nivel 3 e a composicao do proximo simulado de domingo.

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

## Checklists em PDF

Um PDF por dia da semana, para imprimir: checklist com uma bolinha por topico e por subtopico do edital, campo para o resultado do lote de Nivel 1 de cada topico, e a tabela de registro dos simulados daquele dia. Domingo traz o registro geral do Nivel 3 e a projecao por bloco.

| Dia | Arquivo |
|---|---|
| Segunda-feira | [`pdf/1-segunda-feira-orcamento-e-tributacao.pdf`](pdf/1-segunda-feira-orcamento-e-tributacao.pdf) |
| Terça-feira | [`pdf/2-terca-feira-direito-administrativo-e-contratacoes.pdf`](pdf/2-terca-feira-direito-administrativo-e-contratacoes.pdf) |
| Quarta-feira | [`pdf/3-quarta-feira-controle-externo-e-organizacao-do-estado.pdf`](pdf/3-quarta-feira-controle-externo-e-organizacao-do-estado.pdf) |
| Quinta-feira | [`pdf/4-quinta-feira-gestao-e-dados.pdf`](pdf/4-quinta-feira-gestao-e-dados.pdf) |
| Sexta-feira | [`pdf/5-sexta-feira-servidores-previdencia-e-direito-civil.pdf`](pdf/5-sexta-feira-servidores-previdencia-e-direito-civil.pdf) |
| Sábado | [`pdf/6-sabado-instrumentais-e-distrito-federal.pdf`](pdf/6-sabado-instrumentais-e-distrito-federal.pdf) |
| Domingo | [`pdf/7-domingo-nivel-3.pdf`](pdf/7-domingo-nivel-3.pdf) |

Gerados por `python3 scripts/gerar_pdfs.py` — mudou grupo ou ementa, e so rodar de novo.

### Uma folha por materia: a ementa cruzada com os filtros do Gran

Em [`pdf/materias/`](pdf/materias/), um PDF por materia (16 no total), em **duas folhas A4 em pe**. A folha 1 e a materia inteira: cada topico e cada subtopico do edital em uma linha, a aula do curso ao lado e oito colunas de bolinhas. O nome de cada filtro montado no Gran e escrito em pe no cabecalho da coluna; as bolinhas marcadas dizem o que aquele filtro sorteia. A folha 2 e o registro dos simulados: filtro, data, total, acertos, erros, bruto, liquido e veredito.

A ultima coluna e fixa e se chama **GERAL N2**. A bolina grande dela, uma por topico, marca a materia vencida: o topico que fechou 18/20 sobre a ementa inteira sai da fila de estudo e passa a entrar no filtro geral do Gran — o que alimenta o simulado de Nivel 2 do grupo e as revisoes de tudo que ja esta vencido. Ela so aparece na linha do topico, porque e o topico inteiro que vence; subtopico sozinho nao fecha nada.

No pe da folha, **cada coluna de filtro fecha com uma bolona**: aquele filtro bateu a meta e pode ser jogado dentro do GERAL N2. A ultima bolona e a materia inteira.

A materia inteira cabe na folha 1 qualquer que seja o tamanho dela. O corpo do texto encolhe so o quanto for preciso — as curtas saem em 12pt e o que sobra vira pauta de anotacao; Direito Administrativo, a maior, fecha em 7,6pt com os 14 topicos e os 41 subtopicos.

A folha responde a pergunta que o mapa por dia nao responde: **qual pedaco da ementa cada filtro esta realmente cobrindo** — e, por eliminacao, o que nenhum filtro esta testando.

```bash
python3 scripts/gerar_pdfs_materia.py                      # todas as materias
python3 scripts/gerar_pdfs_materia.py direito-administrativo
```

## Templates

[`mapa-de-progressao.md`](templates/mapa-de-progressao.md) · [`diario-de-erros.md`](templates/diario-de-erros.md) · [`folha-de-simulado.md`](templates/folha-de-simulado.md) · [`flashcards.md`](templates/flashcards.md)

## Regenerar

Os 48 agentes de materia e o `reitor-tcdf` sao **gerados** a partir de `scripts/edital.json`; os grupos e niveis, a partir de `scripts/progressao.json`.

```bash
python3 scripts/gerar_agentes.py        # agentes, squad.yaml, data/
python3 scripts/gerar_progressao.py     # grupos de conteudo e mapa de progressao
python3 scripts/gerar_status.py         # status atual a partir dos simulados registrados
python3 scripts/gerar_pdfs.py           # os 7 PDFs de checklist (pdf/)
python3 scripts/gerar_pdfs_materia.py   # um PDF por materia: ementa x filtros (pdf/materias/)
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
    ├── progresso.json          # registro dos simulados feitos (memoria do sistema)
    └── *.py                    # geradores
```

## Limites

- Os agentes nao substituem a leitura do edital oficial nem do material de aula.
- Nenhum agente estima probabilidade de aprovacao ou nota de corte como certeza.
- Prazos, percentuais e quoruns devem ser conferidos na norma: os agentes sao instruidos a sinalizar quando nao tiverem certeza, mas a conferencia final e sua.
