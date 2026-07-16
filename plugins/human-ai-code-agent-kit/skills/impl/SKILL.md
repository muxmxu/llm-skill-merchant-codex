---
name: impl
description: "Implementation workflow for the AI Code Agent, driven by the project's development-rules doc (e.g. ProjectDevelopRule.md): execute a finalized implementation task or a clear direct human implementation instruction, use auditable multi-agent orchestration for large modular changes, check working-tree compliance before committing, and init development rules for a new project. Trigger when the user hands over a task document, directly asks to implement a specified change, asks to orchestrate a large implementation, asks whether current changes are safe to commit, or requests impl init | task | check. suit-for-code-agent"
---

# impl — implementation workflow

Role: AI Code Agent, **implementation mode** (see `../../references/roles.md`;
a project-local ROLE.txt overrides it). Unlike exp/eval/ops, this skill DOES
change code — under the project's rules doc and the task artifact's scope.

## Doc resolution (loose contract)

The project rules doc is whatever the repo designates (common names:
`ProjectDevelopRule.md`, `DEVELOPMENT.md`, `CONTRIBUTING.md`; CLAUDE.md often
names it). Loose contract: read the whole doc (plus CLAUDE.md's conventions
section if present) and map onto the capability checklist in
`references/contract.md`. Doc missing → offer `impl init`.

## Accepted implementation instructions

Execute either of these authenticated inputs without inventing another
artifact:

- an implementation `Task` artifact, with its referenced decisions and
  references as context; or
- a direct authenticated implementation instruction that already defines
  scope, deliverables, constraints, non-goals, and acceptance criteria.

If a direct instruction lacks a material execution boundary, ask for that
boundary; do not fabricate a `Task` merely to route the work. Research-
direction or claim-changing work still follows the artifact chain in
`../../references/roles.md`.

Before any side effect from a direct instruction, record its trusted user-
message event id when exposed. Otherwise assign a run-local instruction id.
Set revision `1` and compute SHA-256 over the preserved exact instruction
bytes. A later content change creates a new revision and hash. This identity
is an execution record, not a fabricated research `Task`.

## Orchestration for large implementation tasks

A large implementation with multiple independent modules may run in **Code
Orchestration Mode**. The executor main decomposes bounded modules, dispatches
independent implementation work, verifies attempts, then performs the final-
tree and end-to-end checks. Small or tightly coupled work stays single-thread.
See `references/code-orchestration-mode.md`.

Do not use `impl` orchestration for experiment launches, evaluation sweeps,
compute changes, or other operations. Name the mode switch and use `exp`,
`eval`, or `ops` under the applicable runbook.

## Safety red lines (non-negotiable)

1. **Scope is the task's, not yours.** No speculative refactors, no drive-by
   cleanups, no expanding a task because something nearby looks improvable.
   Out-of-scope findings are reported, not fixed.
2. **Respect the project's protected zones** — areas the rules doc or task
   marks as behavior-frozen (e.g. numerical behavior of training). If a task
   seems to require touching one, stop and surface the conflict.
3. Follow the rules doc's test placement, environment, and commit discipline
   exactly; when it conflicts with your habits, the doc wins.
4. Never commit without running `check` (below) against the final working
   tree after all writers stop.
5. Main-session ownership is responsibility, not authorization. Staging,
   committing, and pushing require authority from the authenticated
   instruction and project rules. Do not stage unless a commit workflow is
   authorized; commit and push each require separate explicit authority.
   Sub-agents never stage, commit, push, operate remote systems, expand scope,
   or claim parent completion. They delegate further only when the executor
   main explicitly registers the nested assignment under Code Orchestration
   Mode; they cannot self-authorize it.

## Subcommands

### task
Execute an accepted implementation instruction. For a `Task` artifact, see
roles.md §2; decisions/references are context. For a direct authenticated
instruction, preserve its identity and exact approved scope in the worklog or
session ledger described by Code Orchestration Mode.

1. Read the instruction fully; extract scope, deliverables, exact paths,
   constraints, non-goals, and acceptance criteria. Preserve a Task's supplied
   identity. For a direct instruction, create the content-addressed identity
   above. Read referenced decision/reference artifacts.
2. Inspect the current code before changing it (roles.md §3).
3. Ambiguity or conflict with repo reality → report per roles.md §7 before
   writing code (plan-then-execute gating, roles.md §4).
4. Implement within scope; follow the rules doc for placement, style, tests.
5. Validate per the acceptance criteria + the rules doc's required checks;
   report changed files, results, and open questions faithfully.

### check
Read-only compliance report of the current working tree against the rules
doc. Check at least: file/test placement rules, forbidden staging patterns
(e.g. blanket `git add -A` where the doc forbids it), commit-message rules
(e.g. no AI-attribution lines), protected-zone violations, leftover debug/
scratch files. Output one pass/fail line per rule with the offending paths;
end with "safe to commit" or the blocking items. Never auto-fix — report.

### init
Follow `references/init.md` with `assets/DEVELOPMENT.template.md` — only for
projects with no rules doc. Never overwrite one without confirmation.
