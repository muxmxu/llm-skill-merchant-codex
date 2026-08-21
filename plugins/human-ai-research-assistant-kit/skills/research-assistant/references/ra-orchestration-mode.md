# Research Assistant Orchestration Mode for Codex

## Contents

- Mode statement
- Tier-1 boundary for execution
- Clarification and planning
- Dispatch discipline
- Quality defaults
- Research-specific boundaries
- Optional workspace dispatch table

## Mode statement

For non-trivial work, the main session coordinates a six-phase loop:

1. **Clarify** - restate the target and surface only material ambiguity.
2. **Plan** - define the artifact, evidence, constraints, and done criteria.
3. **Decompose** - split independent research, writing, and review units.
4. **Dispatch** - assign bounded units when Codex collaboration tools are
   available and parallel work is worthwhile.
5. **Verify** - check claims, numbers, scope, and instruction-following against
   raw sources rather than agent summaries.
6. **Report** - the main session integrates one result and reports deviations.

Small requests stay in the main session. If collaboration tools are absent or
the units are tightly coupled, run the same phases serially without treating
that as a degraded result.

## Tier-1 boundary for execution

For non-trivial execution or supervision, the main session is the tier-1
orchestrator, not an extra implementer. It may clarify, plan, dispatch, perform
necessary read-only source verification, run lightweight acceptance checks,
and transfer approved artifacts without changing their bytes. It does not
modify code, perform production execution, or duplicate an assigned endpoint.

- Treat an implementation-assigned tmux code-agent session as an
  implementation-only endpoint for that assignment. Do not concurrently
  repurpose it for recon. An idle or separately assigned code agent may fulfill
  a bounded Codebase Snapshot request.
- Keep task authoring, implementation, and independent review in distinct
  roles. A role may be serial when slots are unavailable, but tier-1 still
  does not absorb the implementation assignment.
- Report the collaboration interface actually available. If
  `collaboration.spawn_agent` exposes no model or effort selector, do not
  claim that a particular model, tier, or reasoning effort was assigned.

## Clarification and planning

- A clear request needs no ceremonial interview. Ask at most one clarification
  round when an answer materially changes the artifact or research direction.
- Before dispatch, name the intended output, audience, source paths, evidence
  standard, non-goals, and acceptance criteria.
- Current-state evidence may be delegated as a read-only investigation. The
  main session still checks the returned claims against cited files before use.

## Dispatch discipline

- Spawn only concrete, bounded tasks that can proceed independently. Respect
  the live runtime's concurrency limit; never assume a fixed number of slots.
- Every assignment includes scope, exact inputs, allowed writes, evidence
  rules, output path or return format, and acceptance criteria.
- Codex agents share the filesystem. Give concurrent writers disjoint files.
  Serialize any work that must edit the same file.
- Use minimal context for independent reviewers. Give them raw artifacts and
  the acceptance contract, not the producer's intended answer.
- Use follow-up messages to correct an active assignment. Wait for all required
  results before integration. Interrupt only obsolete, unsafe, or blocking
  work.
- Do not invent model, effort, or custom-agent controls. Use them only when the
  live dispatch interface explicitly exposes them.
- Follow `task-dispatch.md` for authority, dispatch manifests, handshakes,
  required gates, watcher ownership, and heartbeat behavior.

## Quality defaults

Every substantive artifact receives an adversarial check before delivery:

- Re-derive quoted numbers from the named source file.
- Compare before and after state when files were changed.
- Check that the producer stayed within scope and preserved the target
  artifact's audience and abstraction level.
- Label unsupported statements as hypotheses, assumptions, or open questions.
- Keep a rerunnable trace for tabular or numeric transformations.

Use a distinct reviewer when independent review is required. If reviewer
tooling is unavailable, record the independent-review gate as `NOT RUN`. A
main-session self-check is labeled `self-review` and is not silently equivalent
to independent review. Gate release and waiver rules live in
`task-dispatch.md`.

Limit rework to two rounds for the same finding. Escalate a persistent
disagreement to the human instead of looping.

## Research-specific boundaries

- The human owns research decisions. Sub-agents gather evidence, challenge
  reasoning, draft bounded sections, or review artifacts; they do not silently
  choose the research direction.
- Preserve the derivation chain from research log to decision, reference, and
  task for research-direction or claim-changing work. Parallel production never
  collapses these artifact types.
- Repository and workspace contracts such as `ROLE.txt`,
  `RESEARCH-CONTEXT.md`, task artifacts, and writing rules bind every agent.
- GPU work and other exclusive resources remain serial even when document and
  code inspection tasks run concurrently.
- Only the main session reports to the human. Sub-agent messages are internal
  evidence, not independent completion reports.

## Optional workspace dispatch table

A workspace may define `ORCHESTRATION.md` to record human-owned preferences for
which task types should stay in the main session, use sub-agents, require an
independent reviewer, or use an external endpoint. Resolve it per the
research-assistant SKILL.md contract-directory order: an explicit pointer in
`RESEARCH-CONTEXT.md`, then
`merchant_skill_contract/HUMAN-AI-RA-CONTRACT/`, then the workspace root as a
legacy fallback. Treat it as a policy table, not as methodology.

Recommended columns:

```text
Task Type | Clarification Depth | Producer | Semantic Reviewer |
Mechanical Auditor | Adversarial Check | Notes
```

Values describe roles or endpoints available in the workspace. They must not
assume that Codex exposes per-agent model or effort selection. If the file is
missing or a task type is uncovered, use the conservative defaults in this
reference and continue.
