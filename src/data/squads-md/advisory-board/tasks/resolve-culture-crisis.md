---
task: resolveCultureCrisis()
responsavel: "@board-chair"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: crisis_description
    tipo: string
    origem: User Input
    obrigatorio: true
  - campo: symptoms
    tipo: string
    origem: User Input
    obrigatorio: true

Saida:
  - campo: culture_resolution
    tipo: string
    destino: Console
    persistido: false

Checklist:
  - "[ ] All three diagnostic frameworks applied"
  - "[ ] Root cause identified with causal chain mapped"
  - "[ ] Implementation plan with quick wins and measurement criteria"
---

# Task: Culture & Team Dysfunction Resolution

**Task ID:** BOARD-003
**Version:** 2.0.0
**Command:** `*resolve-culture-crisis`
**Agent:** Board Chair routes to Patrick Lencioni + Simon Sinek + Marshall Goldsmith
**Purpose:** Diagnose and resolve organizational culture dysfunction or team breakdown.

---

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `crisis_description` | User prompt | YES |
| `team_size` | Number of people affected | PREFERRED |
| `symptoms` | Observable behaviors and problems | YES |
| `duration` | How long has this been happening | PREFERRED |
| `previous_interventions` | What has been tried already | NO |
| `organizational_context` | Company stage, industry, values | NO |

## Preconditions

1. Culture or team dysfunction is acknowledged
2. Observable symptoms are described (not just a vague feeling)
3. Willingness to address root causes, not just symptoms

## Execution Phases

### Phase 1: Diagnose Dysfunction

**Patrick Lencioni — Five Dysfunctions Assessment:**
1. **Absence of Trust** — Do team members hide weaknesses and mistakes?
2. **Fear of Conflict** — Do they avoid difficult conversations?
3. **Lack of Commitment** — Do they fail to buy into decisions?
4. **Avoidance of Accountability** — Do they avoid calling out peers?
5. **Inattention to Results** — Do they prioritize individual status over team goals?
6. Identify which dysfunction is the primary root (they cascade from trust downward)
7. Assess severity: early warning, established pattern, or crisis

**Marshall Goldsmith — Leadership Behavioral Assessment:**
1. Is the leader's behavior the root cause or a symptom?
2. Which of the 20 bad habits is most present? (winning too much, adding too much value, etc.)
3. What Got You Here Won't Get You There — is a past strength now a weakness?
4. Feedforward from the team — what ONE behavior change would they most appreciate?
5. Does the leader model the trust and accountability they expect from the team?

**Simon Sinek — Purpose Alignment Check:**
1. Is the WHY clear and shared across the team?
2. Has the organization drifted from its founding purpose?
3. Are people playing a finite game (winning) or infinite game (sustaining)?
4. Is there a just cause that inspires the team?
5. Are leaders serving the people, or are people serving the leaders?

### Phase 2: Identify Root Cause

1. Cross-reference all three diagnostic frameworks
2. Identify the deepest root — usually trust or purpose, not the visible symptom
3. Trace the causal chain: root cause → cascade → visible symptoms
4. Determine if this is a people problem, process problem, or leadership problem
5. Assess whether leadership is part of the cause or part of the solution
6. Identify the one intervention that would have the highest leverage

### Phase 3: Design Intervention

**For Trust Deficit (Lencioni lead):**
1. Personal histories exercise — build vulnerability-based trust
2. Behavioral profiling — understand each other's working styles
3. Team effectiveness exercise — open discussion of strengths and weaknesses
4. Leader goes first — vulnerability must come from the top

**For Leadership Deficit (Goldsmith lead):**
1. Identify leader's ONE behavior to change — highest leverage behavioral shift
2. Install Daily Questions — "Did I do my BEST to make my team feel safe today?"
3. Feedforward protocol — team provides future-focused suggestions (not past-focused feedback)
4. Establish norms for direct, compassionate communication

**For Purpose Deficit (Sinek lead):**
1. Rediscover the WHY — what originally inspired the team/company?
2. Find the Just Cause — what is the long-term vision worth fighting for?
3. Establish infinite game mindset — shift from "beating competitors" to "advancing the cause"
4. Identify worthy rivals — learn from others instead of trying to destroy them

### Phase 4: Implementation Plan

1. Sequence interventions — address root cause first, then downstream effects
2. Define quick wins — what can improve within 1 week?
3. Define structural changes — what needs 30-90 days?
4. Assign leadership responsibilities — who drives each intervention?
5. Set measurement criteria — how will you know it is working?
6. Plan check-ins — weekly for first month, then bi-weekly
7. Define escalation triggers — what signals the intervention is not working?

## Output Format

```yaml
culture_resolution:
  advisors: [patrick-lencioni, simon-sinek, marshall-goldsmith]
  diagnosis:
    lencioni_dysfunction: "{primary dysfunction}"
    goldsmith_leadership: "{leader behavior assessment}"
    sinek_purpose: "{alignment assessment}"
    root_cause: "{deepest root}"
    causal_chain: "{root → cascade → symptoms}"
    severity: "early_warning | established | crisis"
  intervention:
    primary: "{highest leverage intervention}"
    trust_building: ["{specific exercises}"]
    leader_behavior_change: ["{specific practices}"]
    purpose_alignment: ["{specific actions}"]
  implementation:
    week_1: ["{quick wins}"]
    month_1: ["{structural changes}"]
    month_3: ["{sustained practices}"]
    measurement: ["{success indicators}"]
    escalation_triggers: ["{warning signs}"]
```

## Veto Conditions

- **NEVER** blame individuals — focus on systems, patterns, and leadership
- **NEVER** skip the trust assessment — trust is the foundation of everything
- **NEVER** recommend surface-level fixes (team building events) without addressing root cause
- **NEVER** ignore the role of leadership in the dysfunction
- **NEVER** rush the process — culture change takes time and consistent effort

## Completion Criteria

- [ ] All three diagnostic frameworks applied
- [ ] Root cause identified with causal chain mapped
- [ ] Severity assessed (early warning / established / crisis)
- [ ] Intervention designed addressing root cause first
- [ ] Implementation plan with quick wins and structural changes
- [ ] Measurement criteria defined
- [ ] Escalation triggers established
