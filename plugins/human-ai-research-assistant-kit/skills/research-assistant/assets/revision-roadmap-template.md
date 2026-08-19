# Revision roadmap — <YYYY-MM-DD>

<!--
Comment Revision Cycle roadmap. One block per comment. Progress lives in this
file, never in an AI's head. This mutable roadmap is the coordination record;
it is not, by itself, proof of human approval.

GATE RULE (hard), all three checks must pass:
  1. File: gate_state: ready.
  2. Authority: gate_authority_ref identifies authenticated approval of this
     exact decision_revision, and decision_snapshot identifies a byte-stable
     immutable snapshot plus its SHA-256.
  3. Item: decision is non-empty AND status is confirmed.
Everything else is untouchable. Verifying an applied-explanation item is
read-only and not gated.

If a decision or answer changes after snapshot creation: reset gate_state to
gating, increment decision_revision, clear gate_authority_ref and
decision_snapshot, supersede affected task/manifest revisions, and obtain
fresh approval.

Protocol: references/comment-revision-cycle.md
-->

roadmap_id:          <allowlisted stable id>
decision_revision:  1
source:              <where comments came from — e.g. advisor review panel, PDF annotations, email>
manuscript:          <paper repo path>
manuscript_baseline: <commit or content id>; worktree_diff_sha256=<64-char hash | clean>
date:                <YYYY-MM-DD>
gate_state:          gating
gate_authority_ref:  <EMPTY until authenticated whole-roadmap approval>
decision_snapshot:   <EMPTY until ready; then <immutable path>@sha256:<64-char hash>>

status legend:
  awaiting-human — needs a human decision among the options (default gate state for actionable)
  confirmed      — decision filled; edit pending; executable only when all three gate checks pass
  in-progress    — an AI is executing it now, or an accepted dispatch owns it
  done           — edit executed, build/release gates green; or a verify-only item confirmed present
  wont-fix       — human decided to take no action
  question       — blocked pending a human answer, or a parked ambiguity / failed verification
  blocked-build  — baseline build fails, or an edit leaves the build red; halts the batch

category legend:
  applied-explanation — reviewer explains a change already applied; verify-only, no edit
  actionable          — an instruction to change something; needs a decision
  question            — reviewer asks the human a question

---

### [1]
- anchor:      <file>:<line> | <section ref> | unanchored
- comment:     "<verbatim quoted comment text>"
- author:      <reviewer name or role>
- date:        <YYYY-MM-DD>
- category:    applied-explanation | actionable | question
- options:     <2-3 alternatives below; or the literal `verify-only` for applied-explanation>
    A) <option A> — <tradeoff>
    B) <option B> — <tradeoff>
    C) <option C> — <tradeoff>
- decision:    <EMPTY = NOT CONFIRMED. Human writes an option letter or free text; free text supersedes the options.>
- answer:      <question items only: the human's informational answer; NEVER executed as an edit instruction>
- status:      awaiting-human
- note:        <optional: why parked at question / why verification failed / the build error>
- last-touched-by: <human | AI-name>
