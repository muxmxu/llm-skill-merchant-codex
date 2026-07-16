# Task: <Short imperative title>

## Metadata
- task_id: `YYYY-MM-DD_<snake_case_title>`
- revision: `1`
- stage: `<Stage I | Stage II | Stage III | project-defined stage | n/a>`
- status: `active`
- owner: `code_agent`
- parent_authority_kind: `<log | progress | decision | human_instruction>`
- parent_authority_ref: `<exact path | authenticated-event-id>`
- parent_authority_revision: `<positive integer | n/a>`
- parent_authority_sha256: `<64-character lowercase hex>`
- supersedes: `<task_id@revision | none>`

## Objective
<One sentence. What the agent must achieve, not how.>

## Context
<2-5 sentences of relevant background. Link the parent authority or references. Do not re-explain material that the agent can read from linked refs.>

## Scope
**In scope**
- <concrete bullet>

**Out of scope**
- <concrete bullet>

## Inputs
Files the agent must read (priority order, strongest first):

1. `<path/to/ref.md>` — <one-line why>
2. `<path/to/ref.md>` — <one-line why>

Files the agent must inspect (codebase):
- `<source/.../file.py>`

Checkpoints / artifacts:
- `<path/to/artifact>` — <purpose>

## Deliverables
Exact paths and contents the agent must produce:

- `<path/to/output.md>` — <required sections or content>
- `<path/to/output.json>` — <schema hint>
- `<path/to/script.py>` — <purpose and reproducibility requirement>

## Procedure
Ordered steps. Each step is a self-contained unit; agent reports completion per step.

1. **<Step name>** — <what to do, what to output>
2. **<Step name>** — <what to do, what to output>
3. **<Step name>** — <what to do, what to output>

## Acceptance Criteria
Objective, checkable conditions. Every item must be verifiable from the deliverables alone.

- [ ] <condition 1>
- [ ] <condition 2>
- [ ] <condition 3>

## Constraints
- <hard constraint>

## Open Questions / Assumptions
- Assumption: <what the agent may take as given>
- Question: <what the agent must answer in deliverables>
