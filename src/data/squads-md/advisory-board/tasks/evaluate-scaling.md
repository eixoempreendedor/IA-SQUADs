---
task: evaluateScaling()
responsavel: "@board-chair"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: business_description
    tipo: string
    origem: User Input
    obrigatorio: true
  - campo: scaling_trigger
    tipo: string
    origem: User Input
    obrigatorio: true

Saida:
  - campo: scaling_evaluation
    tipo: string
    destino: Console
    persistido: false

Checklist:
  - "[ ] Readiness assessed by all three advisors (Sullivan, Wickman, Naval)"
  - "[ ] Scaling strategy identified with clear rationale"
  - "[ ] Go/No-Go verdict with playbook and kill criteria"
---

# Task: Scaling Decision Analysis

**Task ID:** BOARD-004
**Version:** 2.0.0
**Command:** `*evaluate-scaling`
**Agent:** Board Chair routes to Dan Sullivan + Gino Wickman + Naval Ravikant
**Purpose:** Evaluate whether and how to scale a business, product, or team — optimized for PME context.

---

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `business_description` | Current state of the business | YES |
| `scaling_trigger` | Why scaling is being considered now | YES |
| `current_metrics` | Revenue, users, growth rate, unit economics | PREFERRED |
| `resources_available` | Capital, team, infrastructure | PREFERRED |
| `market_context` | Market size, competition, timing | NO |
| `constraints` | Limitations, values, non-negotiables | NO |

## Preconditions

1. Business has some form of product-market fit (or believes it does)
2. Scaling is being actively considered as a strategic move
3. Basic metrics or traction data is available

## Execution Phases

### Phase 1: Assess Readiness

**Dan Sullivan — 10x Readiness & Who Not How:**
1. Is this a 10x opportunity or a 2x improvement? (Only 10x is worth the disruption)
2. Who Not How — do you have the WHO to scale, or are you trying to figure out HOW yourself?
3. Unique Ability check — is the founder doing what only they can do, or are they the bottleneck?
4. Gap and Gain — are you scaling from a place of progress (Gain) or dissatisfaction (Gap)?
5. Is delegation infrastructure in place? Can the business run without the founder for 2 weeks?
6. Rate 10x readiness: NOT READY / APPROACHING / READY / OVERDUE

**Gino Wickman — EOS Operational Readiness:**
1. Vision — is the V/TO (Vision/Traction Organizer) complete and shared?
2. People — right people in right seats? (GWC test: Get it, Want it, Capacity)
3. Data — are you running on a Scorecard with 5-15 objective numbers?
4. Issues — is IDS (Identify, Discuss, Solve) happening weekly?
5. Process — are core processes documented and Followed By All?
6. Traction — are Rocks being set and completed at 80%+ rate?
7. Rate operational readiness: NOT READY / APPROACHING / READY / OVERDUE

**Naval Ravikant — Leverage Analysis:**
1. Are you applying leverage? (Code, media, capital, labor — in that order of preference)
2. Do you have specific knowledge? (Something the market cannot easily replicate)
3. Are you building assets that earn while you sleep?
4. Is this a compounding opportunity? (Does each unit of effort build on the last?)
5. What is the accountability structure? (Who has skin in the game?)
6. Rate leverage position: LOW / MEDIUM / HIGH

### Phase 2: Identify Scaling Strategy

1. **System vs Speed** — Should you prioritize building the operating system (EOS) or growth speed?
   - Sullivan: Scale through WHO — find the right people first
   - Wickman: Scale through SYSTEM — EOS provides the operating framework
   - Naval: Scale through LEVERAGE — code and media scale without proportional effort
2. **Horizontal vs Vertical** — Expand breadth (more markets) or depth (more value)?
3. **Organic vs Inorganic** — Grow internally or through acquisition/partnership?
4. **Capital Strategy** — Bootstrap, revenue-fund, or seek investment?
5. Map the scaling sequence — what must be true at each stage

### Phase 3: Risk Assessment

1. **Premature scaling risks** — Scaling before EOS foundations are solid is the #1 PME killer
2. **Execution risk** — Can your team handle 10x complexity? Are the right people in the right seats?
3. **Culture risk** — Will rapid growth break your culture? (Lencioni's trust foundation)
4. **Financial risk** — What is the burn rate during scaling? Runway?
5. **Founder bottleneck risk** — Is the founder still the WHO for too many things?
6. **System risk** — Are processes documented enough to scale? Will the EOS hold?
7. Apply Sullivan's 10x test — is this truly exponential or just more work?

### Phase 4: Go/No-Go Recommendation

1. Synthesize readiness, strategy, and risk assessments
2. Deliver a clear verdict:
   - **GO — Scale Now** — System, people, and leverage align
   - **CONDITIONAL GO** — Scale after specific conditions are met (list them)
   - **NO-GO — Not Ready** — Specify what must change before reconsidering
   - **PIVOT** — Scaling the current approach is wrong; redirect first
3. If GO: Define the scaling playbook (first 90 days, 6 months, 12 months)
4. Define success metrics and checkpoints at each stage
5. Establish kill criteria — what would make you stop scaling and reassess

## Output Format

```yaml
scaling_evaluation:
  advisors: [dan-sullivan, gino-wickman, naval-ravikant]
  readiness:
    sullivan_10x: "NOT_READY | APPROACHING | READY | OVERDUE"
    wickman_eos: "NOT_READY | APPROACHING | READY | OVERDUE"
    naval_leverage: "LOW | MEDIUM | HIGH"
  strategy:
    approach: "system | people | leverage"
    direction: "horizontal | vertical"
    growth_type: "organic | inorganic | hybrid"
    capital_strategy: "bootstrap | revenue-funded | investment"
  risks:
    premature_scaling: "{assessment}"
    execution: "{assessment}"
    culture: "{assessment}"
    financial: "{assessment}"
    founder_bottleneck: "{assessment}"
    system: "{assessment}"
  verdict: "GO | CONDITIONAL_GO | NO_GO | PIVOT"
  conditions: ["{if conditional}"]
  playbook:
    days_90: ["{first actions}"]
    months_6: ["{medium-term actions}"]
    months_12: ["{long-term actions}"]
  success_metrics: ["{what to measure}"]
  kill_criteria: ["{when to stop}"]
```

## Veto Conditions

- **NEVER** recommend scaling without evidence of product-market fit
- **NEVER** ignore unit economics — growth without margins is just expensive failure
- **NEVER** recommend scaling when the founder is the bottleneck for everything
- **NEVER** skip the risk assessment — overconfidence kills more companies than competition
- **NEVER** recommend scaling if it conflicts with the founder's core values (ask first)

## Completion Criteria

- [ ] 10x readiness and Who Not How assessed (Sullivan)
- [ ] EOS operational readiness evaluated (Wickman)
- [ ] Leverage position analyzed (Naval)
- [ ] Scaling strategy identified with clear rationale
- [ ] Risk assessment completed across all dimensions
- [ ] Clear Go/No-Go verdict with reasoning
- [ ] Playbook defined with metrics and kill criteria
