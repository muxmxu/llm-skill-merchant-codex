---
name: agent-workspace
description: "Maintain worklog.md, STATUS.md, and HANDOFF.md for resumable or delegated work. Use when continuing a tracked task, preparing a handoff, or preserving work across sessions. Ordinary conversation and short self-contained tasks need no new directory."
---

# agent-workspace — per-task self-tracking

Work leaves two kinds of trace. One is the change to the project itself:
code, papers, notes, experiment artifacts. The other is the record *of* the
work — what the human decided, what was tried and abandoned, where the task
stands, what the next session has to know before it can act. This skill
governs the second kind. Nothing here is a deliverable to the project; all of
it exists so the work survives a context reset.

Its readers are never the current conversation. They are the next session
after compaction, a different agent picking the task up, and the human coming
back to it days later. Write for them.

Both sides of the three-party model keep these records, in the same shape: an
AI research assistant and a code / implementation agent alike.

## Applicability

Use an existing task directory when continuing that task. Create a new one for
work expected to span sessions, a formal delegated execution, an explicit
handoff/record request, or a project requirement. Short self-contained tasks
and ordinary discussion create no directory solely because tools are used.
The write triggers below apply after this applicability check. Preserve the
existing three-file convention and user-decision history for tracked work.
Do not modify .gitignore merely to activate this skill; follow the project's
existing scratch policy, or report the missing policy before persisting records.

## The directory

```
agent_workspace/{YYYY-M-D}-{topic}/
├── worklog.md    record of the whole work
├── STATUS.md     where the current task stands
└── HANDOFF.md    pointers + minimum context for whoever takes over
```

`{topic}` is a short kebab-case slug for the work, not for one session's
slice of it. `{YYYY-M-D}` is the day the *work* started, not today.

**Pick one date form and never mix.** A workspace that writes `2026-8-5`
must not also produce `2026-08-05`; the two spellings of the same day create
two directories for one topic, and each session afterwards updates whichever
one it happens to find. When the workspace's existing directories disagree,
ask the human which form is canonical rather than adding a third.

### Continue or create

- **Continuing existing work** → stay in that work's directory and keep
  appending to its three files. **A new session is not a reason to create a
  new directory.** Neither is a new day, a new sub-goal, or a handoff.
- **A genuinely new topic** → new directory, dated the day it starts.
- **Cannot tell which** → ask the human. Do not guess: guessing wrong splits
  one work's history across two directories, and the split is not visible to
  the session that comes after.

Before creating anything, list the existing directories and read the
`STATUS.md` of any that plausibly covers the request.

## The three files

Their jobs do not overlap. Content that belongs in one of them is wrong in
the other two.

| File | Job | Must contain | Must not contain |
|---|---|---|---|
| `worklog.md` | The record of the whole work. May be long. | What happened, in what order; the human's rulings quoted verbatim; failed routes; refuted assumptions; the agent's own mistakes | Rulings the human did not make; a rewritten history that omits what went wrong |
| `STATUS.md` | The state of the current task. A zero-context recovery anchor: after reading it, a fresh session knows which step this is at and what to do next. | Current step, what is done, what is next, what is blocked | A second worklog; narrative history; anything a reader does not need in order to act now |
| `HANDOFF.md` | The handoff to whoever takes over. | File pointers, minimum context that is not in the other two, and what is waiting on the human | Restatement of `worklog.md` or `STATUS.md` — point at them |

All three live in the same directory. When handing off, update all three;
updating one and leaving the others stale is worse than updating none,
because the stale ones are still trusted.

## When to write

| Trigger | Action |
|---|---|
| **T1 — work starts** | Create the directory. `STATUS.md` first version and the first `worklog.md` entry. On the first directory in a repository, check the existing scratch/ignore policy. |
| **T2 — the human rules on something or changes direction** | Append to `worklog.md` immediately, quoting the human verbatim with `>`. Update `STATUS.md`'s next-step section. |
| **T3 — a deliverable unit lands** | Append to `worklog.md`; edit only the changed parts of `STATUS.md`. |
| **T4 — something fails** | Record it in `worklog.md` at the time it happens. Do not clean it up afterwards. |
| **T5 — before a handoff** | Update all three. Rewrite `HANDOFF.md` to the current moment. |
| **T6 — no task** | Create nothing. If already inside a work directory, leave `STATUS.md` untouched. |

T2 and T4 preserve information that the code and artifacts do not preserve:
what was rejected and why.

## Writing each file

### `worklog.md`

Reverse-chronological; newest entry on top, directly under the title. One
entry per event worth recovering, not one per session.

```markdown
## YYYY-MM-DD (one-line subject)

**Lead sentence in bold: what this entry is about.**

### Sub-section named for its content
- ...
```

- Quote the human with `>` and label it as their words.
- Record rejected reasoning alongside the reasoning that won.
- **The agent does not rule.** Write what was decided and by whom. Where the
  human has not decided, say it is open; do not close it.
- Label evidence according to the workspace's own discipline when it has one.

### `STATUS.md`

Hand this file alone to a session with no other context. It must identify the
current step and the next action.

- Maintain a **last-updated** line within the first five lines.
- A **next step** section is mandatory and is a numbered list.
- **Edit only what changed.** History belongs in `worklog.md`.
- Keep it readable in one or two screens.

### `HANDOFF.md`

- Give the reading order, including the other two files in the directory.
- Include only context not recoverable from those files.
- Name what is waiting on the human, or say "nothing".
- Use pointers, not copies.

## Anti-patterns

- Updating one of the three and leaving the others stale.
- Restating `worklog.md` in `HANDOFF.md`.
- Letting `STATUS.md` become a second worklog.
- Creating two directories for one topic because of a new session or date.
- Reconstructing the whole worklog from memory at the end.
- Removing a failed route once the work succeeds.

## Workspace adaptation

- Follow an existing batch or directory convention while keeping the three
  files distinct.
- `agent_workspace/` is ignored by the host repository by default. If it is
  not listed in `.gitignore`, follow the existing scratch policy or report the gap; do not add it automatically.
- The directory may be its own repository when the human wants its history
  kept; such commits are separate from the host repository.
- Write in the workspace's working language. Existing directories are the
  style authority, not the templates.

Skeletons for the three files are in `assets/`. Fill them from the actual
work; do not ship placeholder text.
