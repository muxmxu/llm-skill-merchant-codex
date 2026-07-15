# Code Orchestration Mode for Codex

## Activation

Use this mode when `impl` is active and a task has multiple independent
modules whose parallel execution saves meaningful time. This skill reference
authorizes sub-agent orchestration for such large tasks unless a
higher-priority instruction forbids it. Keep small or tightly coupled tasks
in the normal single-thread workflow.

## Phases

1. **Decompose** - define bounded modules, owner paths, shared interfaces,
   acceptance criteria, and dependencies before dispatch.
2. **Implement** - dispatch only modules that can proceed independently.
3. **Verify** - review each module's semantics, scope, edge cases, and cheap
   mechanical checks independently of its implementer.
4. **Integrate** - the main session performs one pass over the combined
   working tree, resolves cross-module issues, and runs end-to-end checks.
5. **Report** - the main session sends one completion report covering all
   modules, validation, deviations, and unresolved decisions.

Implementation and verification may pipeline after decomposition. Integration
is deliberately single-owner and happens only after all required modules have
settled.

## Codex dispatch discipline

- Use the live collaboration tools exposed by the runtime. Spawn an agent only
  for a concrete, bounded task that can run independently alongside useful
  work. Respect the runtime's concurrency limit; never assume a fixed number
  of slots.
- Give each agent a self-contained prompt: scope, exact source paths, allowed
  writes, constraints, acceptance criteria, validation commands, and expected
  return format. Fork only the context needed for that task.
- Use follow-up messages to correct or extend an active assignment. Wait for
  required results before integration. Interrupt an agent only when its work
  is obsolete, unsafe, or blocking the task.
- Do not invent per-agent model or effort controls. If the live dispatch tool
  exposes no such fields, all assignments use the runtime-selected agent
  configuration. Assign roles by task, not by assumed model tier.
- For adversarial verification, give the reviewer raw artifacts and the
  acceptance contract. Do not leak the implementer's intended answer or the
  main session's suspected finding unless the check specifically requires it.

## Shared-worktree discipline

- Codex agents share the filesystem. Give concurrent writers disjoint files
  or directories. If two tasks must touch the same file, serialize them.
- Treat changes that appear while agents run as shared work. Inspect and
  integrate them; never revert or overwrite another agent's or the user's
  changes blindly.
- The main session owns cross-module edits, final validation, staging, commits,
  and pushes unless the user explicitly assigns those operations elsewhere.
- GPU and other exclusive resources remain serial. Parallelize CPU-bound
  inspection, implementation, tests, and documentation only when they do not
  contend for the same resource.
- Repository-local `AGENTS.md`, `ROLE.txt`, task artifacts, protected zones,
  experiment launch rules, and operations runbooks bind every sub-agent.
  Parallel work never relaxes them.

## Verification and reporting

- A semantic review checks behavior, interfaces, scope, failure modes, and
  missing tests. Mechanical checks run the repository's required formatter,
  linter, type checker, and tests where applicable.
- Rework stays bounded. After two failed correction rounds on the same issue,
  the main session reports the disagreement or blocker instead of looping.
- Sub-agent messages are internal evidence. Only the main session reports to
  the user, and it reports verified repository state rather than agent claims.
