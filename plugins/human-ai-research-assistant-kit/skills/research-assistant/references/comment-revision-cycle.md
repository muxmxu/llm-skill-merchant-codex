# Comment Revision Cycle

Turns a batch of reviewer feedback on a manuscript — advisor comments, peer
reviews, editor notes — into confirmed, executed, verified edits. Comment
**sources** vary endlessly (an Overleaf review panel, PDF annotations, a
plain-text email, verbal notes typed up); the **cycle** is invariant. This
file defines the cycle. Concrete source adapters live in the workspace, not
here (see "Adapters", below).

The organizing principle: **progress lives in one roadmap file, never in an
AI's head.** Any AI picking the roadmap up cold reads the file-level
`gate_state:` and the per-item `status:` fields before touching the
manuscript. The roadmap is the coordination record; it is not, by itself,
proof that the human approved execution. Execution also requires an
authenticated gate reference and an immutable decision snapshot. Building or
compiling to verify a fix needs the workspace toolchain, resolved from
`RESEARCH-CONTEXT.md` rather than guessed or embedded here.

## The four-step cycle (actor ownership)

The kit's three parties own the steps. The AI assistant orchestrates; the
code agent executes; the human decides and gates.

```
[1] comment -> roadmap      AI ASSISTANT  normalize every comment into one
       |                                  roadmap; classify; pre-fill options;
       |                                  verify applied-explanation items
       v
[2] check roadmap  <==GATE   HUMAN         fill decision fields; answer
       |                                  questions; set status confirmed/
       |                                  wont-fix; approve the complete pass
       v                     AI ASSISTANT  authenticate + freeze a snapshot
[3] roadmap -> fix           CODE AGENT    execute ONLY confirmed items, and
       |                     (or AI asst   only once all three gates pass,
       |                      for small    via the task-dispatch interface
       |                      in-session   (see "Handoff", below)
       |                      edits)
       v
[4] review the fix           AI ASSISTANT  mechanical + semantic review
                             + HUMAN       then human final pass
```

### Step 1 — comment → roadmap (AI assistant)

Take the adapter's output (per comment: quoted text + anchor + author +
date) and write **one roadmap file** with one block per comment, using the
fixed field set below. Record the exact manuscript baseline before
verification: repository path, commit, and a SHA-256 of the worktree diff if
it is dirty. Start the file at `gate_state: gating`. **Classify every
comment** into exactly one of the three categories.

- For each `actionable` item — and each `question` whose answer is an
  enumerable set of text changes — pre-fill `options:` with 2–3 concrete
  alternatives, one sentence each with its tradeoff, so the human chooses
  rather than composes. This is derivation, not decision-making: never put a
  chosen fix in `decision:` — that field is the human's.
- Verify every `applied-explanation` item against the current manuscript now
  (read-only, no edit): set it `done` if the reviewer's already-applied text
  is present, or `question` with a `note:` if it is absent.
- Resolve `scripts/` relative to this skill directory. Run
  `python3 scripts/validate_revision_roadmap.py <roadmap> --phase intake`
  before handing the roadmap to the human. The validator checks structure and
  lifecycle invariants; it does not judge whether the proposed options are
  scientifically or rhetorically sound.

### Step 2 — human checks the roadmap (human) ★ THE GATE

The human walks the roadmap top to bottom: answers every `question` (in
`answer:`), picks an option letter or writes free text into `decision:`, and
sets `status:` to `confirmed` (or `wont-fix`) per handled item. When the whole
pass is done, the human approves the complete roadmap through the trusted main
conversation or another authenticated human-message event. The assistant then
records that event in `gate_authority_ref:`, flips `gate_state:` from
`gating` to `ready`, and writes an immutable decision snapshot at the
workspace-defined snapshot path. Record its path and SHA-256 in
`decision_snapshot:`. A disk edit without authenticated approval does not
open execution.

> **GATE RULE (hard) — all three checks must pass:**
> 1. **File level.** The header's `gate_state:` is `ready`. While it is
>    `gating`, execute nothing, even items already marked `confirmed`.
> 2. **Authority level.** `gate_authority_ref:` identifies authenticated human
>    approval of this exact `decision_revision`, and `decision_snapshot:`
>    identifies the immutable snapshot and its SHA-256. Missing or mismatched
>    authority blocks execution.
> 3. **Item level.** An item is executable only when its `decision:` is
>    non-empty and its `status:` is `confirmed`. Every other item — empty
>    decision, `awaiting-human`, `question`, `blocked-build`, or anything
>    ambiguous — is untouchable.
>
> Verifying an `applied-explanation` item is read-only, produces no edit, and
> is **not** gated: the AI verifies it and sets it `done` or `question`
> itself, at any `gate_state`. When in doubt, do not act; leave it for the
> human.

### Step 3 — roadmap → fix (code agent, or AI assistant for small edits)

Only when all three gate checks pass. First verify that the current manuscript
still matches `manuscript_baseline:`; if it does not, stop and reconcile the
drift instead of applying line-number anchors blindly. Execute confirmed items
only, in roadmap order. Update each item's `status:` and `last-touched-by:`
immediately as it is handled (`in-progress` → `done`, or `wont-fix`, or
`blocked-build` on a build failure), so a crash or handoff loses no state.
Small in-session edits the assistant may do directly when the workspace rules
permit them; a real batch goes through the Codex task-dispatch pipeline (see
"Handoff"). Before the first side effect, run
`python3 scripts/validate_revision_roadmap.py <roadmap> --phase execute`.

### Step 4 — review the fix (AI assistant + human)

AI-side review has two lenses:

- **Mechanical.** Every `confirmed` item is now `done` (or explicitly
  `wont-fix`); no item is stuck `in-progress` or `blocked-build`; nothing
  outside confirmed items was touched; the manuscript builds/compiles clean.
- **Semantic.** Each edit is faithful to what `decision:` actually says —
  not a plausible-looking edit that drifts from the human's choice.

Then the human does the final pass. For a dispatched batch, declare mechanical
scope/build checks, semantic decision-faithfulness review, and the human final
pass as explicit gates in the immutable dispatch manifest. Reuse the gate
records and release rules in `task-dispatch.md`; do not create a second review
state machine in the roadmap. Finish with
`python3 scripts/validate_revision_roadmap.py <roadmap> --phase complete`.

## Roadmap per-comment block spec

Source-neutral field names. Use these exact names. The file carries one header
with the fields below, then one block per comment.

```
roadmap_id:          <allowlisted stable id>
decision_revision:  <positive integer; start at 1>
source:              <where the comments came from>
manuscript:          <paper repository path>
manuscript_baseline: <commit>; worktree_diff_sha256=<64-char hash | clean>
date:                <YYYY-MM-DD>
gate_state:          gating | ready
gate_authority_ref:  <EMPTY until authenticated whole-roadmap approval>
decision_snapshot:   <EMPTY until ready; then <immutable path>@sha256:<hash>>
```

```
### [<id>]
- anchor:      <file>:<line> | <section ref> | unanchored
- comment:     "<verbatim quoted comment text>"
- author:      <reviewer name or role>
- date:        <YYYY-MM-DD the comment was made>
- category:    applied-explanation | actionable | question
- options:     (AI-proposed; 2-3 alternatives, one sentence each + tradeoff;
                the literal string `verify-only` for applied-explanation)
    A) <option A> — <tradeoff>
    B) <option B> — <tradeoff>
    C) <option C> — <tradeoff>
- decision:    <EMPTY = NOT CONFIRMED. Human writes an option letter or free
                text. Free text is authoritative and supersedes the options.>
- answer:      <question items only: the human's informational answer. This
                is information, NEVER an edit instruction; do not execute it.>
- status:      awaiting-human | confirmed | in-progress | done | wont-fix
                | question | blocked-build
- note:        <optional short annotation: why parked at question, why
                verification failed, or the build error for blocked-build>
- last-touched-by: <human | AI-name>
```

**Status vocabulary** (fixed):

| status | meaning |
|---|---|
| `awaiting-human` | needs a human decision among the options; the default gate state for an `actionable` item |
| `confirmed` | `decision:` filled; an edit is pending; executable only when all three gate checks pass |
| `in-progress` | an AI is executing it now, or an accepted dispatch owns it |
| `done` | edit executed and all required build/release gates are green; a `verify-only` item is confirmed present; or an informational question has a recorded answer and requires no edit |
| `wont-fix` | human decided to take no action |
| `question` | blocked pending a human answer (a `question`-category comment starts here; an AI also parks any mid-execution ambiguity, or a failed applied-explanation verification, here rather than guessing) |
| `blocked-build` | the baseline build fails, or an item's edit leaves the build red; needs the human before the batch can continue |

`decision:` empty ALWAYS means NOT CONFIRMED. An `applied-explanation` item
never becomes `confirmed` — it is `verify-only` and goes straight to `done`
(verified) or `question` (verify failed), so its empty `decision:` never
conflicts with the gate rule. Only `actionable` items and `question` items
resolved in place can ever be `confirmed`.

## Classification rules (the three categories)

Every comment is exactly one of:

| category | meaning | action |
|---|---|---|
| `applied-explanation` | the reviewer explains a change they have **already applied** to the manuscript | `options: verify-only`; no edit. Verify against current text (the AI does this, not the human): if present → `status: done`; if absent (reviewer forgot to push, or the git and comment channels diverged) → `status: question` + a `note:` for the human to reconcile. Do NOT self-confirm an unverified claim. |
| `actionable` | an instruction to change something | pre-fill options; `status: awaiting-human` until the human decides |
| `question` | the reviewer asks the human a question | If the answer is an enumerable set of text changes, pre-fill `options:` and let the human resolve it in place like an `actionable` item (pick → `confirmed`). Otherwise use empty `options:` and `status: question`: the human fills `answer:`. If the answer requires no manuscript edit, mark the question `done`; if it implies an edit, derive a NEW `actionable` block that re-enters the gate, then mark the original question `done`. The answer is information, never itself executed as an edit instruction. |

## Discipline (encoded from real runs)

1. **Never revert an edit the reviewer already applied.** `applied-explanation`
   items are verify-only; any manuscript text the reviewer merged in is ground
   truth — do not undo it while fixing other comments, and do not undo it to
   fix a build.
2. **Touch nothing beyond confirmed roadmap items.** No drive-by edits, no
   reformatting of unrelated lines.
3. **Verify baseline and result before declaring `done`.** Before the first
   edit, verify the recorded commit and dirty-diff hash and run the workspace's
   build/compile command. After each edit, run it again and require zero
   errors. Resolve the exact command from `RESEARCH-CONTEXT.md` or the paper
   repo's runbook, not from memory.
4. **Build failures halt the batch.** If the baseline build is red, mark the
   first executable item `blocked-build` with `baseline failure; no edit
   applied` plus the error in `note:`. If a build fails after an edit, do not
   mark that item `done`; set it `blocked-build` with the error in `note:`.
   Leave every other item's applied edit untouched (do not revert other
   items to make the build green — that violates rule 2 and can undo rule 1),
   and escalate to the human. Compilation is global: a red build blocks the
   whole batch — no item reaches `done` until it is green again.
5. **One owner per in-flight item.** An item another agent marked
   `in-progress` or `blocked-build` is untouchable until it returns to a
   terminal (`done` / `wont-fix`) or `awaiting-human` state; only the agent
   named in `last-touched-by:` may transition it. `confirmed` alone never
   authorizes execution when a dispatch for that item is already live. For a
   dispatched batch, the watcher owner updates the mutable roadmap from
   acknowledgement and report evidence; the executor writes its append-only
   runtime records and does not concurrently edit the roadmap.
6. **Commits carry no AI co-author line.** No `Co-Authored-By` trailer. Commit
   only when the human asks.
7. **State on disk, updated immediately.** Set `status:` and
   `last-touched-by:` the moment an item changes; the file, not any AI's
   memory, is the record.
8. **Freeze decisions before dispatch.** The mutable roadmap cannot be the
   content-addressed parent authority because its runtime statuses keep
   changing. Freeze the ready decisions into an immutable snapshot and bind
   the Task to that snapshot's exact SHA-256. If any decision or answer changes
   afterward, reset `gate_state: gating`, increment `decision_revision`,
   supersede affected task/manifest revisions, and freeze a new snapshot after
   fresh human approval.
9. **Re-resolve anchors after every prior edit.** Line numbers are intake
   hints, not permission to edit whatever later occupies that line. Match the
   anchor against the recorded baseline, then translate it through intervening
   diffs; park ambiguous or stale anchors at `question` instead of guessing.

## Roadmap file location

One roadmap file per review batch. Do not use a fixed name; suggest
`revision-roadmap-<YYYY-MM-DD>.md`, or under a progress dir if the workspace
uses one: `progress/YYYY-MM-DD_<topic>/revision-roadmap.md`. Put immutable
decision snapshots beside it with a revisioned name such as
`revision-roadmap-<YYYY-MM-DD>-decision-v1.md`. Record both path conventions
in `RESEARCH-CONTEXT.md` (see "Adapters") so cold handoff can resolve them
from disk rather than conversation memory.

## Handoff to task-dispatch (step 3 at scale)

A **frozen decision snapshot** is the code-agent-facing decision artifact. Do
not build a parallel execution mechanism here; a real fix batch reuses the
Codex pipeline:

1. After authenticated gate closure, write a byte-stable snapshot containing
   `roadmap_id`, `decision_revision`, source, baseline, date, `gate_state`,
   `gate_authority_ref`, and every comment block exactly as approved. Omit the
   live roadmap's `decision_snapshot:` field to avoid a self-referential hash.
   Do not edit this snapshot after hashing it. Then record its path and hash
   back in the mutable roadmap's `decision_snapshot:` field.
2. Derive a Task per `task-writing.md`. Use
   `parent_authority_kind: decision`, the snapshot path as
   `parent_authority_ref:`, its `decision_revision` as
   `parent_authority_revision:`, and its exact SHA-256 as
   `parent_authority_sha256:`. In-scope is the confirmed items; out-of-scope is
   every other roadmap item and all unrelated manuscript text.
3. Run the immutable Task through `task-dispatch.md` unchanged. The dispatch
   manifest binds the Task, snapshot authority, approval event, both execution
   contracts, endpoint, transport, watcher, and all release gates. Declare
   objective gates for confirmed-item scope, decision faithfulness, a clean
   manuscript build, and the human final pass. Assign owners and waivability
   under the normative gate protocol; never turn `FAIL` or `NOT RUN` into
   `PASS`.
4. **Keep status layers separate, with one roadmap writer.** Runtime states
   (`received | accepted | in_progress | ...`) remain in append-only
   acknowledgement records per `code-agent-execution.md`; do not copy them
   into the roadmap. Once dispatch owns the batch, its `watcher_owner` marks
   those roadmap items `in-progress`. The executor does not edit the roadmap.
   On verified return, the watcher owner reflects each result as `done`,
   `blocked-build` for a build failure, or `question` for another
   human-resolvable block. If delivery or validation blocks before any side
   effect, restore the affected items to `confirmed` with a short `note:` and
   retain the append-only dispatch evidence.

For a handful of small text edits the assistant can make in-session, skip the
dispatch machinery only when authenticated human intent and workspace rules
authorize direct editing. The three-check gate, immutable snapshot, discipline
list, and step-4 review still apply.

## Adapters (out of scope for the kit)

Step 1 consumes a uniform tuple per comment:

```
{ quoted comment text, anchor (file:line or section), author, date }
```

Any tool or process that yields that tuple can feed the cycle — an Overleaf
review-panel extractor, a PDF-annotation dumper, a script that parses an
email thread, or the human simply typing verbal notes into the tuple by
hand. A human-provided file already in this tuple form needs **no adapter**;
it feeds step 1 directly. The **adapter concept** is part of this cycle;
**concrete adapters are not part of the kit.** They are project-specific
(source formats, capture pitfalls, dual git-vs-comments channels) and live in
the user's workspace. This workspace's concrete adapters and its
roadmap-storage dir are recorded under the `## Comment-revision adapters &
roadmaps` H2 of `RESEARCH-CONTEXT.md`. Do not hardcode a specific adapter or
its paths into kit files.

## Worked example (compact)

Adapter tuple for two comments →

```
## Revision roadmap — 2026-07-20
roadmap_id: revision-2026-07-20-advisor
decision_revision: 1
source: advisor review, sec/method.tex
manuscript: <paper repo>
manuscript_baseline: <commit>; worktree_diff_sha256=clean
date: 2026-07-20
gate_state: ready
gate_authority_ref: <authenticated-human-instruction-id>@1
decision_snapshot: revision-roadmap-2026-07-20-decision-v1.md@sha256:<64-char hash>

### [1]
- anchor:      sec/method.tex:32
- comment:     "learnable? or random parameter?"
- author:      advisor
- date:        2026-07-19
- category:    question
- options:
    A) State it is a learnable linear projection — matches code, strongest claim — needs code-fact confirmation.
    B) State it is a fixed random projection — safe if unsure — weaker novelty.
    C) Defer: leave a TODO and ask again — no text change yet.
- decision:    A (code confirms learnable; write "learnable linear projection")
- answer:
- status:      confirmed
- note:
- last-touched-by: alice

### [2]
- anchor:      sec/intro.tex:8
- comment:     "reworded this sentence for clarity"
- author:      advisor
- date:        2026-07-19
- category:    applied-explanation
- options:     verify-only
- decision:
- answer:
- status:      done
- note:
- last-touched-by: AI-codex
```

Item [1] is a `question` with an enumerable answer set, so options were
pre-filled; the human picked A → `confirmed` with a non-empty `decision`.
Item [1] becomes executable only because the file gate, authenticated
authority, immutable snapshot, and item gate all pass. Item [2] is
`applied-explanation`: the AI verified the reviewer's own merged edit is
present in the current text → `done`, empty `decision`, no edit, and it must
NOT be reverted (discipline rule 1). Had the reworded sentence been absent,
item [2] would be `question` with a `note:` instead, for the human to
reconcile.

Template to copy: `assets/revision-roadmap-template.md`.
