---
name: magi
description: "<suit-for-ai-research-assistant> convene a MAGI decision council on a decision the human is facing — whether to run an experiment, adopt an approach, cut scope, spend a budget, submit to a venue, or abandon a line of work. Several mutually orthogonal lenses deliberate on a shared bound-facts pack, every reason is audited back to its source and struck if it does not hold, a unanimous vote is red-teamed before it stands, and the result is reported as a ruling with a vote tally, the surviving reasons for and against, the cost of not acting, and each vote's flip condition. Trigger on 'should we do X', 'is X worth it', 'X or Y', and on an explicit ask for MAGI. Not a brainstorm and not a debate: open-ended thinking belongs in research discussion, and designing the how belongs in planning."
---

# MAGI — decision council

A decision, not a discussion. The input is one decidable proposition; the
output is a ruling report with a vote tally, the reasons that survived audit,
and the conditions that would flip them.

What this is not:

- **Not brainstorming.** Generating options is research-discussion work. MAGI
  runs after the options exist.
- **Not design.** "How should we build X" is a planning question. MAGI
  answers "should we".
- **Not a debate.** The lenses should not see each other's first-round output.
  Disagreement is resolved by audit and tally, not by argument.
- **Not an executor.** The council reports; the human rules. Convening the
  council is not permission to act on its ruling.

## Stage 0 — Frame the proposition

The main Codex session does this itself. Do not delegate it: everything
downstream inherits the framing.

**0.1 Reduce to one decidable proposition.** Binary (do / do not) or at most
four mutually exclusive options. State the default explicitly: what happens if
the ruling is "no". Write it as a single sentence.

**0.2 Refuse if it is not decidable.** Say what is missing, ask the one
question that would fix it, and stop. Refuse when:

- the question is a "how", not a "whether" — that is planning work;
- neither side has any checkable evidence, so every vote would be intuition;
- the human has already decided and is asking for validation.

**0.3 Assemble the bound-facts pack.** Enumerate every fact whose mistake
would change the ruling. For each one, pin a precise value or name exactly
where to get it. Cover at minimum:

- the state being decided about — run, checkpoint, manuscript, dataset,
  deadline;
- existing evidence — log paths, code paths, papers, measured numbers;
- hard constraints — compute, person-hours, budget, dependencies, dates;
- the cost of being wrong in each direction.

An item that is neither pinned nor sourced blocks the council. Every seat
receives the same complete pack and nothing private.

## Stage 1 — Seat the council

Default three seats. The human's choice of lenses overrides this default.
Seats must be mutually orthogonal: if the same evidence moves two seats in
the same direction, merge them and choose a different lens.

Default triad:

- **MELCHIOR — evidence and method.** Does the evidence bear the weight?
  Would the proposed work answer the question it claims to answer?
- **BALTHASAR — cost and survival.** Compute, person-hours, deadlines, and
  reversibility. What does not doing it cost?
- **CASPER — outside evaluation.** How will a reviewer, advisor, or reader
  receive it? Where will it be attacked?

When another lens is needed, name it by the question it asks. Candidates and
the orthogonality test are in `references/lens-library.md`.

## Stage 2 — Independent deliberation

Use one bounded Codex collaboration assignment per seat when such facilities
are available. Keep the first round blind: no seat sees another seat's output.
If no seat-level collaboration is available, run the seats serially from the
same bound-facts pack and label the report as serial; do not claim stronger
independence than was actually obtained.

Each seat receives the proposition and default, the complete bound-facts pack,
its mandate, and this output schema:

```jsonc
{
  "stance": "for" | "against" | "abstain",
  "confidence": "low" | "medium" | "high",
  "reasons": [
    {
      "claim": "one sentence",
      "label": "observation" | "data" | "claim-from-source" | "hypothesis",
      "source": "a checkable pointer: file path + line, log name, commit, number origin, or paper location",
      "weight": "decisive" | "supporting" | "minor"
    }
  ],
  "cost_of_not_doing": "what this seat sees going wrong if the ruling is no",
  "flip_condition": "what would have to be true for this seat to change its vote",
  "cheapest_probe": "the smallest check that would resolve this seat's uncertainty"
}
```

A reason without a checkable source does not count. A seat that cannot produce
one must abstain. Do not report a hypothesis as an observation. Stay inside
the mandate. `cost_of_not_doing` is mandatory even for a vote against.

## Stage 3 — Audit every reason

Audit per reason, not per seat. The auditor must be distinct from the seat and
must check each reason against its source:

- **upheld** — the source exists and supports the claim as stated;
- **downgraded** — the source supports only a weaker claim; relabel and reduce
  weight as needed;
- **struck** — the source is absent, contradictory, numerically wrong, or the
  reason does not bear on this proposition.

If all of a seat's reasons are struck, or the surviving reasons no longer
support its stance, that seat becomes `abstain (grounds did not hold)`.
Struck reasons remain visible in the report so the same unsupported argument
does not return later.

## Stage 4 — Red-team a unanimous vote

If every valid vote points the same way, including when only one valid vote
remains, run a red-team assignment. Its only job is to break the consensus by
finding counter-evidence, an omitted bound fact, or a shared wrong premise.

- Counter-evidence that survives audit → the result is **hold**.
- Red team fails → the consensus stands and the report says it was red-teamed.

A unanimous vote that has not been red-teamed does not produce a ruling.

## Stage 5 — Tally and report

The main session does this itself.

- Majority, red-teamed where required → **carried** or **rejected**.
- Tie, fewer than two valid votes, or all seats abstaining → **hold** with the
  missing evidence and cheapest probe.
- The tally is not the ruling. The human decides; do not begin execution.

Report in the conversation language:

```markdown
# MAGI ruling: <proposition>
Verdict: carried / rejected / hold  (for N : against M, abstain K)
Red team: passed / not triggered / broke the consensus
Date: YYYY-MM-DD

## Proposition and default path
## Bound facts (the one input every seat received)
## Reasons for (survived audit)
1. [label] claim — source, seat
## Reasons against (survived audit)
1. [label] claim — source, seat
## Cost of not acting
## Flip conditions
## Cheapest way to resolve what is still open
## Audit record (struck and downgraded reasons)
## Ruling
The decision belongs to the human. <name>'s ruling: <left blank until given>
```

**Persistence.** Write the report to the current task directory as
`magi-<slug>.md` and append the tally to that directory's `worklog.md`,
unless the human explicitly asked for no file. Use the `agent-workspace`
convention for the directory.

## Codex execution boundary

The Claude-side `/magi:ask` command and Workflow `pipeline` wrapper are not
part of this Codex port. Invoke this skill conversationally. Use available
Codex collaboration facilities for seat and audit assignments; if they are
unavailable, follow the serial fallback above and record that limitation.

Resolve any model or effort assignment from the workspace's `ORCHESTRATION.md`
using the research-assistant contract-directory resolution order. Stage 0 and
Stage 5 remain with the main session, and no seat or auditor may silently
inherit tier-1's role when the workspace specifies a different assignment.
