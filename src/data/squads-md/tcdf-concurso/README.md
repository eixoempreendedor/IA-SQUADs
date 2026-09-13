# TCDF Concurso Squad 🎓

**68 agentes de IA para aprovacao no concurso de Analista Administrativo de Controle Externo do TCDF (Cebraspe, 2026).**

Sao **3 agentes para cada uma das 21 materias do edital** — um professor, um examinador e um revisor — mais **5 agentes de coordenacao** que cuidam de estrategia de prova, cronograma, discursiva e desempenho.

| | |
|---|---|
| **Orgao** | Tribunal de Contas do Distrito Federal (TCDF) |
| **Cargo** | Analista Administrativo de Controle Externo — Área de Gestão — Serviços Técnico-Administrativos (ANACE) |
| **Banca** | Cebraspe |
| **Vagas** | 10 vagas imediatas + cadastro de reserva |
| **Remuneracao inicial** | R$ 14,9 mil |
| **Escolaridade** | Nível superior em qualquer área de formação |
| **Provas** | 22/11/2026 — Brasília/DF (4 horas (objetivas)) |
| **Formato** | Certo/Errado (C/E) com penalidade: cada erro anula um acerto |

## ⚠️ Status da fonte do edital

**`NAO_VERIFICADO_NA_FONTE_OFICIAL`**

O CDN do Cebraspe estava bloqueado pela politica de rede da sessao em que este squad foi gerado. A estrutura de provas e a lista de materias foram reconstruidas a partir de fontes secundarias (Cebraspe/TCDF, Estrategia, Gran, Nova Concursos, Folha Dirigida/Qconcursos). As ementas por materia sao ementas-padrao da banca para o tipo de cargo, NAO transcricoes do edital. Rode a task verticalizar-edital.md colando o texto oficial antes de confiar 100% no mapa.

Antes de usar o squad para decisoes finas de conteudo, rode a task [`tasks/verticalizar-edital.md`](tasks/verticalizar-edital.md): cole o conteudo programatico oficial, atualize `scripts/edital.json` e regenere os agentes. A estrutura do squad ja esta pronta para isso — a ementa e dado, nao codigo.

## Estrutura das provas

| Prova | Conteudo | Itens | Minimo |
|---|---|---|---|
| P1 | Conhecimentos Basicos | 35 | 7,00 pontos |
| P2 | Conhecimentos Especificos | 45 | 13,00 pontos |
| P3 | Conhecimentos Especializados | 70 | 21,00 pontos |
| P4 | Prova Discursiva | — | 50,00 pontos no total: questao discursiva de ate 20 linhas (15,00) + peca tecnica tipo Informacao de ate 50 linhas (35,00), no padrao do Manual de Redacao Oficial do TCDF (2a edicao) |

Minimo global nas objetivas: **45 pontos no conjunto das provas objetivas**.

## Os 3 papeis por materia

| Papel | O que faz | Quando acionar |
|---|---|---|
| 🧑‍🏫 **Professor** | Ensina o topico no recorte exato da banca: conceito, exemplo, tabela comparativa, pegadinhas, resumo e 3 itens de fixacao | Conteudo novo, duvida conceitual, montar resumo ou mapa mental |
| 🎯 **Examinador** | Escreve itens Certo/Errado no padrao Cebraspe, aplica simulado cronometrado e comenta o gabarito com o mecanismo de erro usado | Treinar, simular, entender por que errou |
| 🔁 **Revisor** | Revisao espacada (R1/R7/R30), flashcards, diario de erros e revisao de vespera | Manter vivo o que ja foi aprendido |

## Agentes de coordenacao

| Agente | Funcao |
|---|---|
| 🎓 `reitor-tcdf` | Orquestrador e porta de entrada: diagnostica, prioriza pelo peso do edital e roteia |
| ♟️ `estrategista-cebraspe` | Tecnica de prova C/E, politica de chute, gestao de tempo, recursos |
| 🗓️ `arquiteto-cronograma` | Ciclo de estudos ponderado pelo edital, revisoes embutidas, plano de reta final |
| ✍️ `redator-discursiva` | P4: questao discursiva e peca tecnica tipo Informacao, com espelho de correcao |
| 📈 `mentor-desempenho` | Metricas, diario de erros, projecao por bloco e ajuste de rota semanal |

## Mapa completo das materias

| Materia | Bloco | Itens est. | Prioridade | Professor | Examinador | Revisor |
|---|---|---|---|---|---|---|
| 📝 **Lingua Portuguesa** | P1 | 12 | alta | `lingua-portuguesa-professor` | `lingua-portuguesa-examinador` | `lingua-portuguesa-revisor` |
| 🧮 **Raciocinio Logico e Matematica Financeira** | P1 | 8 | alta | `raciocinio-logico-matematica-financeira-professor` | `raciocinio-logico-matematica-financeira-examinador` | `raciocinio-logico-matematica-financeira-revisor` |
| 🏛️ **Lei Organica do Distrito Federal** | P1 | 6 | alta | `lei-organica-df-professor` | `lei-organica-df-examinador` | `lei-organica-df-revisor` |
| 🌆 **Conhecimentos sobre o Distrito Federal e Politicas para Mulheres** | P1 | 6 | media | `conhecimentos-df-politicas-mulheres-professor` | `conhecimentos-df-politicas-mulheres-examinador` | `conhecimentos-df-politicas-mulheres-revisor` |
| 🚑 **Nocoes de Primeiros Socorros** | P1 | 3 | baixa | `nocoes-primeiros-socorros-professor` | `nocoes-primeiros-socorros-examinador` | `nocoes-primeiros-socorros-revisor` |
| ⚖️ **Lei Organica e Regimento Interno do TCDF** | P2 | 10 | critica | `lei-organica-regimento-tcdf-professor` | `lei-organica-regimento-tcdf-examinador` | `lei-organica-regimento-tcdf-revisor` |
| 📜 **Direito Constitucional** | P2 | 10 | critica | `direito-constitucional-professor` | `direito-constitucional-examinador` | `direito-constitucional-revisor` |
| 🧓 **Direito Previdenciario** | P2 | 8 | alta | `direito-previdenciario-professor` | `direito-previdenciario-examinador` | `direito-previdenciario-revisor` |
| 📕 **Nocoes de Direito Civil** | P2 | 6 | media | `nocoes-direito-civil-professor` | `nocoes-direito-civil-examinador` | `nocoes-direito-civil-revisor` |
| 💰 **Nocoes de Direito Tributario** | P2 | 6 | media | `nocoes-direito-tributario-professor` | `nocoes-direito-tributario-examinador` | `nocoes-direito-tributario-revisor` |
| 🤖 **Analise de Dados, Nocoes de Estatistica e Inteligencia Artificial** | P2 | 5 | alta | `analise-dados-estatistica-ia-professor` | `analise-dados-estatistica-ia-examinador` | `analise-dados-estatistica-ia-revisor` |
| 🏢 **Direito Administrativo** | P3 | 14 | critica | `direito-administrativo-professor` | `direito-administrativo-examinador` | `direito-administrativo-revisor` |
| 📊 **Administracao Financeira e Orcamentaria (AFO)** | P3 | 10 | critica | `administracao-financeira-orcamentaria-professor` | `administracao-financeira-orcamentaria-examinador` | `administracao-financeira-orcamentaria-revisor` |
| 🏗️ **Administracao Geral e Publica** | P3 | 8 | alta | `administracao-geral-e-publica-professor` | `administracao-geral-e-publica-examinador` | `administracao-geral-e-publica-revisor` |
| 👥 **Gestao de Pessoas** | P3 | 8 | alta | `gestao-de-pessoas-professor` | `gestao-de-pessoas-examinador` | `gestao-de-pessoas-revisor` |
| 🔄 **Gestao de Processos** | P3 | 6 | media | `gestao-de-processos-professor` | `gestao-de-processos-examinador` | `gestao-de-processos-revisor` |
| 📌 **Gestao de Projetos** | P3 | 6 | media | `gestao-de-projetos-professor` | `gestao-de-projetos-examinador` | `gestao-de-projetos-revisor` |
| 📦 **Administracao de Recursos Materiais** | P3 | 5 | media | `administracao-recursos-materiais-professor` | `administracao-recursos-materiais-examinador` | `administracao-recursos-materiais-revisor` |
| 🗂️ **Arquivologia** | P3 | 5 | media | `arquivologia-professor` | `arquivologia-examinador` | `arquivologia-revisor` |
| 📒 **Contabilidade Publica** | P3 | 5 | alta | `contabilidade-publica-professor` | `contabilidade-publica-examinador` | `contabilidade-publica-revisor` |
| 🏷️ **Administracao Patrimonial** | P3 | 3 | baixa | `administracao-patrimonial-professor` | `administracao-patrimonial-examinador` | `administracao-patrimonial-revisor` |

## Como usar

```
@tcdf                               # cai no reitor-tcdf (diagnostico e rota)
@tcdf:direito-administrativo-professor    # aula de um topico
@tcdf:direito-administrativo-examinador   # lote de itens C/E
@tcdf:direito-administrativo-revisor      # revisao espacada e flashcards
@tcdf:arquiteto-cronograma                # montar o ciclo de estudos
@tcdf:redator-discursiva                  # treinar e corrigir a P4
```

Se voce usa os arquivos direto no Claude Code ou em outra ferramenta de agentes, basta abrir o `.md` do agente: cada arquivo e autossuficiente (persona, ementa da materia, regras de comportamento e formato de saida).

## Fluxos prontos

| Workflow | Quando |
|---|---|
| [`wf-primeira-semana`](workflows/wf-primeira-semana.yaml) | Voce esta comecando agora |
| [`wf-ciclo-semanal`](workflows/wf-ciclo-semanal.yaml) | Rotina padrao de uma semana |
| [`wf-reta-final`](workflows/wf-reta-final.yaml) | Ultimos 60 dias |

## Tasks

`diagnosticar-e-rotear` · `montar-plano-de-estudos` · `aula-de-topico` · `gerar-simulado` · `revisao-do-dia` · `corrigir-discursiva` · `diagnostico-de-erros` · `verticalizar-edital`

## Templates

[`diario-de-erros.md`](templates/diario-de-erros.md) · [`folha-de-simulado.md`](templates/folha-de-simulado.md) · [`flashcards.md`](templates/flashcards.md)

## Regenerar os agentes

Os 63 agentes de materia sao **gerados** a partir de `scripts/edital.json`. Editou a ementa, o peso ou as armadilhas de uma materia? Rode:

```bash
python3 scripts/gerar_agentes.py          # regenera agents/, data/ e squad.yaml
python3 scripts/gerar_agentes.py --check  # so valida, nao escreve
```

Os 5 agentes de coordenacao sao escritos a mao e **nao** sao sobrescritos (estao em `AGENTES_CORE` no script).

Para adicionar uma materia: acrescente um objeto em `materias` no `edital.json` (id, nome, bloco, icone, itens_estimados, prioridade, peso_justificativa, ementa, base_normativa, armadilhas, referencias) e rode o gerador — os 3 agentes nascem prontos.

## Estrutura de arquivos

```
tcdf-concurso/
├── squad.yaml                  # manifesto (gerado)
├── README.md
├── agents/                     # 68 agentes (.md)
├── tasks/                      # 8 tasks
├── workflows/                  # 3 workflows
├── checklists/                 # qualidade de item e peca Informacao
├── templates/                  # diario de erros, folha de simulado, flashcards
├── data/
│   ├── edital-verticalizado.md # edital legivel (gerado)
│   └── routing-catalog.yaml    # roteamento materia -> agentes (gerado)
└── scripts/
    ├── edital.json             # FONTE DA VERDADE
    └── gerar_agentes.py        # gerador
```

## Limites

- Os agentes nao substituem a leitura do edital oficial nem do material de aula.
- Nenhum agente estima probabilidade de aprovacao ou nota de corte como certeza.
- Numeros (prazos, percentuais, quoruns) devem ser conferidos na fonte — os agentes sao instruidos a sinalizar quando nao tiverem certeza, mas a conferencia final e sua.
