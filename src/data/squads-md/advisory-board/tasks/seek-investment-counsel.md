---
task: seekInvestmentCounsel()
responsavel: "@board-chair"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: opportunity_description
    tipo: string
    origem: User Input
    obrigatorio: true
  - campo: financial_data
    tipo: string
    origem: User Input
    obrigatorio: false

Saida:
  - campo: investment_counsel
    tipo: string
    destino: Console
    persistido: false

Checklist:
  - "[ ] All three analyses (Cunningham, Munger, Naval) completed"
  - "[ ] Clear recommendation with terms or conditions"
  - "[ ] Kill criteria and monitoring framework defined"
---

# Task: Investment Committee Session

**Task ID:** BOARD-002
**Version:** 2.0.0
**Command:** `*seek-investment-counsel`
**Agent:** Board Chair routes to Keith Cunningham + Charlie Munger + Naval Ravikant
**Purpose:** Evaluate an investment or major financial decision through multiple analytical lenses optimized for PME context.

---

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `opportunity_description` | User prompt | YES |
| `financial_data` | Revenue, costs, projections | PREFERRED |
| `investment_amount` | Capital required | PREFERRED |
| `market_context` | Industry, competition, timing | PREFERRED |
| `risk_appetite` | Conservative, moderate, aggressive | NO |
| `time_horizon` | Short-term, medium, long-term | NO |

## Preconditions

1. Investment opportunity or financial decision is described
2. At least basic financial context is available
3. Decision-maker's constraints and values are understood

## Execution Phases

### Phase 1: Present Opportunity (board-chair)

1. Frame the opportunity in clear terms — what is being considered?
2. Summarize available financial data and projections
3. Identify the decision: invest/pass, amount, terms, timing
4. Map known risks and unknowns
5. Route to the investment committee: Cunningham, Munger, Naval

### Phase 2: Risk Analysis

**Keith Cunningham — Thinking Time Analysis:**
1. What is the REAL question behind this investment decision?
2. Pre-Mortem — imagine this investment failed in 12 months. What happened?
3. What is the Dumb Tax if this goes wrong? Can you afford it?
4. Am I making this decision as Owner (strategic) or Operator (reactive/emotional)?
5. What does my Business Machine need — does this investment serve it?
6. What am I NOT seeing? What would a smart person worry about?

**Charlie Munger — Mental Models Analysis:**
1. Apply inversion — what would make this fail? Work backwards from disaster
2. Check for cognitive biases — confirmation bias, FOMO, sunk cost, anchoring
3. Assess circle of competence — do you truly understand this domain?
4. Apply Lollapalooza effect — are multiple forces combining (for or against)?
5. Check the moat — what is the durable competitive advantage?
6. Apply the "newspaper test" — would you be proud of this decision on the front page?

**Naval Ravikant — Leverage & Compounding Analysis:**
1. Does this investment create leverage? (Code > Media > Capital > Labor)
2. Does it align with your specific knowledge? (What feels like play to you)
3. Will this compound over time or is it a one-time return?
4. Are you building an asset that earns while you sleep?
5. Productize Yourself check — does this help you package your unique abilities?
6. Long-term games with long-term people — is this partner/opportunity one you'd work with for decades?

### Phase 3: Cross-Analysis

1. Compile all three analyses side by side
2. Identify where all three agree (high-confidence signal)
3. Identify where they disagree (requires deeper analysis)
4. Apply second-order thinking — what happens AFTER the first move?
5. Calculate the asymmetry — is the upside much larger than the downside?
6. Run the pre-mortem — imagine it failed, what was the cause?

### Phase 4: Recommendation

1. Synthesize into a clear invest/pass/conditional recommendation
2. If invest: recommended terms, amount, and conditions
3. If pass: what would need to change to reconsider
4. If conditional: specific milestones or information needed
5. Define kill criteria — what triggers exiting the investment
6. Provide monitoring framework — what metrics to track

## Output Format

```yaml
investment_counsel:
  opportunity: "{description}"
  committee: [keith-cunningham, charlie-munger, naval-ravikant]
  analyses:
    cunningham:
      thinking_time: "{strategic analysis}"
      pre_mortem: "{failure scenarios}"
      dumb_tax: "{cost of getting it wrong}"
      verdict: "INVEST | PASS | CONDITIONAL"
    munger:
      mental_models_applied: ["{models used}"]
      inversion_result: "{failure scenarios}"
      bias_check: ["{biases identified}"]
      verdict: "INVEST | PASS | CONDITIONAL"
    naval:
      leverage_type: "{code | media | capital | labor}"
      specific_knowledge_fit: "{alignment assessment}"
      compounding_potential: "{assessment}"
      verdict: "INVEST | PASS | CONDITIONAL"
  synthesis:
    agreement: ["{convergence}"]
    disagreement: ["{divergence}"]
    asymmetry: "{upside vs downside}"
  recommendation:
    verdict: "INVEST | PASS | CONDITIONAL"
    terms: "{if invest}"
    conditions: "{if conditional}"
    kill_criteria: ["{exit triggers}"]
    monitoring: ["{key metrics}"]
```

## Veto Conditions

- **NEVER** recommend investing without stress-testing assumptions (Cunningham pre-mortem)
- **NEVER** skip the inversion exercise — always consider how it could fail (Munger)
- **NEVER** ignore cognitive biases in the analysis
- **NEVER** recommend based on FOMO or social proof alone
- **NEVER** present a recommendation without defining kill criteria

## Completion Criteria

- [ ] Opportunity framed with available financial data
- [ ] Cunningham's Thinking Time completed with pre-mortem and dumb tax
- [ ] Munger's mental models applied with inversion and bias check
- [ ] Naval's leverage and compounding analysis completed
- [ ] Analyses synthesized with agreement and disagreement mapped
- [ ] Clear recommendation with terms or conditions
- [ ] Kill criteria and monitoring framework defined
