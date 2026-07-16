# Code Orchestration Mode for Codex

## Contents

- Scope and roles
- Activation and phases
- Orchestration ledger
- Module states
- Dispatch and authority
- Shared worktree and resources
- Interruptions, revisions, and retries
- Verification and integration
- Completion and reporting

## Scope and roles

This contract governs multi-agent work inside an AI Code Agent executing an
`impl` instruction.

- The **external tier-1 orchestrator** belongs to the Research Assistant side.
  After dispatch it supervises read-only and does not implement the task.
- The **internal implementation orchestrator** is the executor main session.
  It may perform authorized integration edits, validation, and reporting
  within the parent implementation scope.
- A **module agent** owns one bounded assignment. It never owns the parent
  task or its completion state.

Main-session ownership identifies the single integration owner. It grants no
new authority. This mode never authorizes staging, commit, push, remote
operations, scope expansion, or destructive cleanup.

## Activation and phases

Use this mode only when `impl` is active and an implementation has multiple
independent modules whose parallel execution saves meaningful time. Keep small
or tightly coupled work single-threaded.

Do not use this mode to launch training, run evaluation sweeps, change compute,
or operate remote systems. Name the mode switch and use `exp`, `eval`, or `ops`
under the applicable runbook and authorization rules.

Run these phases:

1. **Recon** — read repository rules and the accepted instruction; record the
   baseline tree, dirty inventory, applicable paths, and resource constraints.
2. **Decompose** — define modules, dependencies, ownership, acceptance, and
   validation before spawning writers.
3. **Implement** — run only ready modules with disjoint writes and resources.
4. **Verify** — bind semantic and mechanical evidence to exact attempts and
   code identities.
5. **Integrate** — stop writers, reconcile the final tree, and run current-tree
   module plus end-to-end checks.
6. **Report** — release `COMPLETE`, `BLOCKED`, or `INCOMPLETE` under the rules
   below.

## Orchestration ledger

Create a lightweight structured ledger before the first spawn. Use the
project-prescribed execution worklog when one exists. Otherwise keep it in the
main session and reproduce it in the final report. Do not create a repository
artifact solely for orchestration unless the parent instruction authorizes it.

Record the parent once:

- `parent_kind`: `task` or `human_instruction`;
- `parent_id`, `parent_revision`, and exact `parent_sha256`;
- parent `manifest_id` and `manifest_sha256` when dispatch supplied them;
- unique `run_id`;
- baseline commit/tree identity, dirty paths, and hashes for pre-existing
  in-scope changes.

For a direct instruction, use the trusted user-message event id when the
runtime exposes one. Otherwise create a run-local `parent_id`, set
`parent_revision: 1`, preserve the exact authenticated message bytes, and hash
those bytes. Later content changes increment the revision and replace the
hash. Do not mistake displayed terminal text for an authenticated message.

Record every module attempt with:

- `module_id`, monotonic `attempt_id`, and `required: true|false`;
- `owner_agent_id`, `writer_agent_id`, and `reviewer_agent_id` or `none`;
- scope, exact explicit and implicit allowed writes, and forbidden writes;
- dependency module identities and shared interface version or hash;
- resource locks, acceptance criteria, and validation commands;
- state, actual changed paths, partial writes, result identity, validation
  exit status, and evidence location;
- tree or diff identity against which implementation and review were judged.

The stable result key is the full parent identity plus `run_id`, `module_id`,
and `attempt_id`. Every assignment prompt and result must quote that key.
Append transitions; do not silently rewrite older attempts. A result with a
different, cancelled, or superseded key is stale and cannot release work.

## Module states

Use only:

```text
planned | ready | running | paused | succeeded | failed | blocked |
cancelled | superseded
```

Normal transitions are:

```text
planned -> ready -> running -> succeeded | failed | blocked | paused
paused -> running | cancelled | superseded
planned | ready | running | paused -> cancelled | superseded
succeeded | failed | blocked -> superseded
```

Mark `succeeded` only after the writer returns the full result key, actual
paths, validation results, and partial-write inventory. Crash, timeout,
interruption, missing identity, and partial output are never success. Record
them as `failed`, `blocked`, or `paused` according to the recoverable state.

Only a current `succeeded` attempt with satisfied release evidence may feed
integration. Predeclare optional modules during decomposition. Failure of a
required module blocks parent completion.

## Dispatch and authority

- Use runtime collaboration tools only for concrete, bounded modules that can
  proceed independently. Respect the live concurrency limit.
- Give each agent the full result key, exact scope, allowed writes, required
  repository instructions, dependencies, resource locks, acceptance,
  validation commands, and return schema.
- Require every writer to read applicable `AGENTS.md`, `ROLE.txt`, task,
  development rules, protected-zone rules, and runbooks before its first write;
  list the paths read in its result.
- Fork only necessary context. Do not invent unavailable model or effort
  controls.
- Module agents may not stage, commit, push, operate remote resources, expand
  scope, claim parent completion, or delegate again by default. Nested
  delegation requires the executor main to register another bounded module
  identity, ownership set, resource set, and authority that is no broader than
  the parent.
- Follow-up instructions that change content create a new attempt identity;
  never mutate an active assignment in place.

For adversarial verification, give the reviewer raw artifacts and the
acceptance contract. Do not leak the implementer's intended answer or the main
session's suspected finding unless the check specifically targets it.

## Shared worktree and resources

- Snapshot repository status before dispatch. Preserve all pre-existing and
  user changes; never claim, stage, revert, or overwrite them as task output.
- Allocate disjoint explicit and implicit writes. Include generated files,
  lockfiles, snapshots, caches, format outputs, and shared metadata that a
  command may rewrite.
- Check ownership before the first write and again before integration. If a
  user or unrelated process changes an owned path, pause that module and
  report the conflict; do not auto-merge it.
- Serialize commands that can rewrite repository-wide state, even when their
  nominal source paths differ.
- Lock every exclusive resource, including GPUs, ports, databases, build
  caches, test fixtures, generated directories, and mutable external services.
- Treat unowned changes that appear during execution as external. Preserve
  them, exclude them from task attribution and staging, and block integration
  when their interaction cannot be proven safe.

## Interruptions, revisions, and retries

When the user pauses or changes the parent instruction:

1. Freeze new dispatch.
2. Pause affected work at reversible boundaries and inventory running states,
   partial writes, and external processes.
3. Do not delete partial work or stop external processes without separate
   authority and the applicable safety contract.
4. If task content changed, record a new parent revision/hash and mark affected
   old attempts `superseded`. Unaffected results may survive only when their
   dependency and interface identities remain exact.
5. Resume through new `ready` or `running` records. Reject late stale results.

A correction or retry always receives a new `attempt_id`. Before dispatch,
inspect residual diffs and record what will be retained, repaired, or left
untouched. Never blindly rerun a non-idempotent codemod, migration, generator,
or external action. Safety, authorization, protected-zone, and project-hard-
rule conflicts block immediately; they do not consume a retry round. After two
failed correction attempts on the same issue, report the blocker unless the
authenticated parent instruction explicitly authorizes another bounded try.

## Verification and integration

- Record each validation command, exit status, evidence location, module
  attempt, dependency/interface identities, and exact tree or diff identity.
- Call a check **independent** only when `reviewer_agent_id` differs from the
  writer for that attempt. If no such reviewer exists, record `self-review` or
  `NOT RUN`; neither is an independent `PASS`.
- Invalidate prior verification whenever relevant files, generated outputs,
  dependencies, shared interfaces, or validation configuration changes.
- A semantic review checks behavior, interfaces, scope, failure modes, and
  missing tests. Mechanical checks run the repository-required formatter,
  linter, type checker, and tests.
- Stop all writers before final integration. The executor main is the only
  integration writer. Recheck path ownership, inspect the complete diff, rerun
  affected module checks on the final tree, then run end-to-end checks.
- Never integrate a stale attempt, an unverified required module, or an
  unowned/unauthorized change.

## Completion and reporting

Report `COMPLETE` only when all of these are true:

- every required module has a current `succeeded` attempt;
- module acceptance and every required independent check pass against current
  identities, or a parent-manifest check has a valid canonical waiver;
- final-tree module and end-to-end checks pass;
- no unresolved owned-path conflict, unowned task attribution, unauthorized
  change, or unwaived required `FAIL` or `NOT RUN` remains.

When the parent came through `task-dispatch`, its gate and waiver protocol is
canonical. Preserve the original `FAIL` or `NOT RUN` and record the valid
waiver; never relabel it `PASS`. Internal checks that are not declared
waivable parent gates remain non-waivable.

Otherwise report `BLOCKED` when progress requires new authority, a decision,
or external-state change. Report `INCOMPLETE` when authorized work or checks
remain. Do not hide either state under a completion narrative.

The final report includes the parent/run identities, complete module ledger,
owners and attempts, actual changed paths, validation commands and exits,
evidence identities, deviations, unresolved risks, and repository status. A
sub-agent result is internal evidence, not the user-facing completion report.
When the parent came through `task-dispatch`, only the executor main writes the
declared completion report and emits the parent result signal.

Integration ownership still does not authorize staging, commit, or push. Run
`impl check` on the final tree before an explicitly authorized commit. Commit
and push each require separate authenticated authority.
