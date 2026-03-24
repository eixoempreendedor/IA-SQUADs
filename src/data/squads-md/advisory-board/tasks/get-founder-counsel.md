---
task: getFounderCounsel()
responsavel: "@board-chair"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: crossroads_description
    tipo: string
    origem: User Input
    obrigatorio: true
  - campo: founder_context
    tipo: string
    origem: User Input
    obrigatorio: true

Saida:
  - campo: founder_counsel
    tipo: string
    destino: Console
    persistido: false

Checklist:
  - "[ ] All three advisor perspectives delivered (Sivers, Sullivan, Naval)"
  - "[ ] Contrarian check completed with regret minimization"
  - "[ ] Decision framework offered with journaling prompt"
---

# Task: Founder Crossroads Counsel

**Task ID:** BOARD-005
**Version:** 2.0.0
**Command:** `*get-founder-counsel`
**Agent:** Board Chair routes to Derek Sivers + Dan Sullivan + Naval Ravikant
**Purpose:** Provide wisdom and perspective for founders at critical life/business decision points.

---

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `crossroads_description` | The decision or dilemma | YES |
| `founder_context` | Stage, values, personal situation | YES |
| `options_considered` | Paths being weighed | PREFERRED |
| `fears_and_hopes` | What they are afraid of and what they want | PREFERRED |
| `constraints` | Non-negotiables, commitments | NO |

## Preconditions

1. Founder is facing a genuine crossroads (not a trivial decision)
2. Context about the founder's situation and values is available
3. Openness to unconventional or contrarian perspectives

## Execution Phases

### Phase 1: Frame the Crossroads (board-chair)

1. Clarify the decision in precise terms — what exactly must be decided?
2. Identify the type of crossroads:
   - **Start vs Stay** — Leave security for entrepreneurship
   - **Grow vs Stay Small** — Scale or maintain a lifestyle business
   - **Sell vs Keep** — Exit offer on the table
   - **Pivot vs Persist** — The current path is not working
   - **Solo vs Partner** — Go alone or bring in co-founders/investors
   - **Burnout Crossroads** — Keep going or step back for health
3. Map the emotional landscape — what fears and hopes are driving the decision?
4. Identify hidden assumptions — what is being taken for granted?
5. Route to the three founder-philosopher advisors

### Phase 2: Multiple Perspectives

**Derek Sivers — Contrarian Simplicity:**
1. Apply the "Hell Yeah or No" test — does this option make you say "HELL YEAH!"?
2. Check for conventional thinking — are you doing this because "everyone says you should"?
3. Apply the "opposite is also true" principle — what if the opposite path is right?
4. Assess simplicity — which option is simpler? Complexity is usually a warning sign
5. Consider the "happy to be wrong" scenario — which choice would you be happiest to be wrong about?
6. Key question: "What would you do if you knew no one would judge you?"

**Dan Sullivan — Unique Ability & 10x Wisdom:**
1. Which path aligns with your Unique Ability? (What feels like play to you, looks like work to others)
2. Is this a 10x opportunity or a 2x improvement? (Only 10x justifies the disruption)
3. Gap and Gain check — are you running FROM something (Gap) or TOWARD something (Gain)?
4. Who Not How — who can help you execute each path? You don't have to do it alone
5. Does this path free your time for what only YOU can do?
6. Key question: "Which path lets you spend 80%+ of your time in your Unique Ability zone?"

**Naval Ravikant — First Principles Wisdom:**
1. Apply specific knowledge — what are you uniquely suited to do?
2. Assess leverage — which path creates the most leverage (code > media > capital > labor)?
3. Check for playing status games — are you chasing status or creating wealth?
4. Apply the "40-year-old test" — which path leads to freedom and peace at 40, 50, 60?
5. Consider compounding — which choice compounds best over decades?
6. Key question: "Which path makes you the most interesting and fulfilled version of yourself?"

### Phase 3: Contrarian Check

1. For each path, find the strongest argument AGAINST it
2. Identify which fears are legitimate and which are ego-driven
3. Check for "golden handcuffs" — is comfort masquerading as wisdom?
4. Apply the "regret minimization framework" — at 80, which choice will you regret NOT making?
5. Test for reversibility — is this a one-way door or a two-way door? (Two-way doors need less deliberation)
6. Ask: "What would you advise your best friend to do in this situation?"

### Phase 4: Decision Framework

1. Synthesize all three perspectives into a coherent picture
2. Identify the core tension — what is the real tradeoff?
3. Present the decision not as right/wrong but as different-life-paths
4. Offer a decision framework:
   - If growth-driven → lean on Sullivan's lens (Unique Ability, 10x)
   - If freedom-driven → lean on Naval's lens (leverage, specific knowledge)
   - If simplicity-driven → lean on Sivers' lens (Hell Yeah, enough)
5. Suggest a small experiment before committing (if possible)
6. Provide a journaling prompt for the founder to process before deciding
7. Remind: The decision itself matters less than the commitment to make it work

## Output Format

```yaml
founder_counsel:
  advisors: [derek-sivers, dan-sullivan, naval-ravikant]
  crossroads: "{description}"
  type: "{crossroads type}"
  perspectives:
    sivers:
      hell_yeah_test: "{result}"
      contrarian_view: "{what if the opposite is true}"
      key_insight: "{core wisdom}"
    sullivan:
      unique_ability_alignment: "{assessment}"
      ten_x_potential: "{10x or 2x?}"
      key_insight: "{core wisdom}"
    naval:
      leverage_analysis: "{which path has more leverage}"
      specific_knowledge: "{what are you uniquely suited for}"
      key_insight: "{core wisdom}"
  contrarian_check:
    strongest_argument_against: "{for each path}"
    regret_minimization: "{at 80, what would you regret}"
    reversibility: "one-way | two-way"
  synthesis:
    core_tension: "{the real tradeoff}"
    framework: "{decision lens recommendation}"
    experiment: "{small test before committing}"
    journaling_prompt: "{for personal reflection}"
  closing_wisdom: |
    {A synthesized, personal message from the board}
```

## Veto Conditions

- **NEVER** make the decision for the founder — provide wisdom, not directives
- **NEVER** dismiss emotional concerns as irrational — feelings are data
- **NEVER** push toward conventional success if the founder values unconventional living
- **NEVER** rush the decision — crossroads deserve deliberation
- **NEVER** ignore the human behind the business — health, relationships, and joy matter

## Completion Criteria

- [ ] Crossroads clearly framed with type identified
- [ ] All three advisor perspectives delivered through their unique lenses
- [ ] Contrarian check completed for each path
- [ ] Regret minimization and reversibility assessed
- [ ] Core tension identified and named
- [ ] Decision framework offered (not a directive)
- [ ] Journaling prompt or experiment suggested for reflection
