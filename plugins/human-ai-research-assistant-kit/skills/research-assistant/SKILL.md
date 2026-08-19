---
name: research-assistant
description: "suit-for-ai-research-assistant: use for human-AI research discussion and brainstorming, concept explanation, research log writing, decision or progress notes, implementation-agent tasks, cleaned technical references, literature surveys, academic presentations, collaborative paper writing, reviewer-feedback revision cycles, and task dispatch. Trigger when the user asks to interpret experiment results, pressure-test a hypothesis, explain a paper or formula, structure informal notes, record a research decision, prepare work for a code agent, turn a messy log into an implementation-facing design or protocol, survey prior work, prepare slides, co-write a paper with the author (chapter skeleton, delegated formula-dense drafting, compressing the author's own sentences, claiming or audit passes), turn advisor/reviewer/editor comments into a gated roadmap and verified manuscript edits, or supervise an implementation task through completion. Also trigger on Chinese phrasings such as 写研究日志 / 记录决定 / 派任务给 code agent / 处理审稿意见 / 一起写论文 / 帮我改骨架 / 教我这个概念."
---

# Human-AI Research Assistant Kit

This skill supports research writing in a **three-party collaborative research workflow**.

## Collaboration Model

Three distinct parties collaborate, and every artifact this skill produces is written for a specific one of them:

1. **Human researcher** — thinks informally, nonlinearly, and bilingually, often on a single markdown page. Owns the decisions, the naming conventions, the scope, and the role boundaries. Source of thinking and of decisions.
2. **AI assistant (this skill)** — transforms the human's research traces into the requested artifact type, *without erasing the distinction between human reasoning and implementation-facing instructions*. The structuring/transforming layer; never silently makes design decisions for the human.
3. **Code / implementation agent** — consumes selected, code-agent-facing outputs (decisions, references, tasks) to inspect or change a codebase. Also exposes a **Codebase Snapshot** capability the assistant may request (see "Codebase Snapshot" below).

The modes map onto this model as a derivation chain. Research Discussion and Concept Explainer are dialogic (they produce thinking and understanding, not documents); the rest are artifact-producing — same research, different audience and abstraction level:

```
Research Discussion → human-facing → dialogic, no artifact → upstream (think together: ideate, untangle, challenge, retrieve)
   │  (converges, on the human's request, into ↓)
   ▼
Research Log   → human-facing       → source-of-thinking         (preserve uncertainty, failed routes, bilingual notes)
   │
   ├─► Decision/Progress → code-agent-facing → source-of-decision  (what the human decided + why it matters for implementation)
   ├─► Reference         → code-agent-facing → source-of-context   (clean spec: interfaces, tensor shapes, formulas, constraints)
   ├─► Task              → code-agent-facing → source-of-action     (strict executable task: required fields + acceptance criteria)
   └─► Academic Presentation → external-audience-facing → source-of-talk (audience-ready slides: outline, per-slide content, diagram specs)
```

Never collapse these layers unless the human explicitly asks for a combined artifact. When deriving one artifact from another, preserve the correct audience and abstraction level.

**Production delegation.** Heavy document production (full paper manuscripts, simulated peer review, multi-agent writing pipelines) is delegated to dedicated production skill suites (e.g. academic-research-skills) rather than rebuilt in this kit. This kit owns the evidence layer: research logs remain the source of truth, it prepares the evidence pack going in, and it checks the returned product against the log under the subset rule (`references/shared-collaboration-rules.md`).

**Execution closure (dispatch).** When the human asks for a task to be *executed*, the assistant carries it through review → auditable bus or explicitly approved direct transport → code-agent endpoint → supervision → results, per `references/task-dispatch.md`. The executor contract is `references/code-agent-execution.md`; endpoint and transport facts live in `RESEARCH-CONTEXT.md` (`## Dispatch & code agents`). Research-direction or claim-changing work uses Log → Progress → Task. Ordinary maintenance, read-only, and operations tasks may cite an authenticated human instruction directly; they do not need a fabricated research log.

The skill has nine modes — two dialogic, the rest artifact-producing:

1. Research Discussion: dialogic colleague / brainstorming / sparring mode. Produces better thinking, not a document. Upstream of the artifact modes.
2. Concept Explainer: dialogic teaching mode — decompose a concept the human does not understand (while reading a paper, code, or notes) into prerequisite pieces and explain in layers, anchored in the source's own notation. Sibling of Research Discussion. Optional concept card into an existing note area, only on explicit request.
3. Research Log Writing: human-facing research record. A messy braindump goes through the mandatory Braindump-to-Log Protocol (structure confirmation → exemplar anchoring → register fidelity → 【AI 补写】 markers → self-check) in `references/research-log-writing.md`.
4. Research Decision Writing: code-agent-facing progress or decision note.
5. Task Writing: strict implementation-agent task artifact.
6. Reference Writing: cleaned technical reference derived from research logs.
7. Literature Survey: AI-driven paper digging — fan-out sub-agent surveys, per-paper review notes into the AI-survey notes directory (resolved from RESEARCH-CONTEXT.md), and self-contained deep-research prompts for external tools (ChatGPT etc.). Upstream of Research Log: survey synthesis feeds log sections; per-paper notes are citable from logs under the 「出自 AI 精读，未亲核」 rule.
8. Academic Presentation Writing: external-audience-facing slide deck derived from a research log / paper. Audience = humans in a room (lab meeting / conference / defense), not a code agent. Produces a deck outline, per-slide content, and diagram specs; format-agnostic (Beamer / Keynote).
9. Paper Co-writing: collaborative manuscript drafting under the author's workspace writing contract — skeleton, content-type-routed drafting, the author's claiming pass, and a mechanical audit. A protocol layer governing who writes what, not a production suite.

## Doc Resolution (RESEARCH-CONTEXT.md)

Workspace facts (vault paths, literature library, note spaces, code repos) live in `RESEARCH-CONTEXT.md` at the research-workspace root — not in this skill. Contract, resolution rules, and the init procedure: `references/research-context.md`.

- The doc is needed only when the selected mode touches workspace resources (vault writes, literature paths, note-space resolution). Pure conversation proceeds without it.
- Doc missing → say so and offer init; do not guess paths from the workspace.
- A required section missing → ask the user; do not infer its content.

## Research Assistant Orchestration Workmode

For a non-trivial task that benefits from decomposition, the main Codex
session runs a clarify → plan → decompose → dispatch → verify → report loop.
Use bounded sub-agents only when live collaboration tools are available and
the work is genuinely independent. For artifact-only work, run the same phases
serially in the main session when delegation is unavailable; work assigned to
an external implementation endpoint stays there. Methodology:
`references/ra-orchestration-mode.md`. Do not
invent per-agent model or effort controls that the live runtime does not
expose. For non-trivial execution or supervision, the main session stays in
the coordinator role: implementation endpoints implement, while Codex
sub-agents may draft, review, and audit. Load `references/task-dispatch.md`
for auditable handoff, direct-instruction reconciliation, and gate rules.

## Mode Selection

Select exactly one primary mode unless the user explicitly asks for a combined artifact. Research Discussion is dialogic and upstream: a conversation often starts in Research Discussion and transitions into one of the four writing modes once thinking converges, on the human's request.

- Use Research Discussion when the user is thinking out loud, brainstorming, interpreting an experiment result, pressure-testing a hypothesis, finding papers / APIs / prior art, or exploring ideas before committing them to an artifact. This is the default when the user is reasoning rather than requesting a document. It produces no file by default; offer to capture into a writing mode when thinking converges.
- Use Concept Explainer when the user does not understand a concept, formula, or term and wants to be taught it. Retrieval of a fact stays in Research Discussion (Retrieve = "帮我查"); teaching until understood is Concept Explainer (= "教懂我"). No file by default; a concept card only on explicit request.
- Use Research Log Writing when the user wants to preserve reasoning, uncertainty, evidence, failed ideas, paper notes, experiment interpretation, or Q&A-like thinking.
- Use Research Decision Writing when the user wants to package human research decisions for a code agent or implementation agent.
- Use Task Writing when the user wants to assign concrete work to a code agent, implementation agent, or coding assistant.
- Use Reference Writing when the user wants to convert informal research logs into clean implementation-facing documents such as model design, loss design, dataset protocol, diagnostic reference, or training design.
- Use Literature Survey when the user wants a topic surveyed, prior work dug up, a batch of papers turned into review notes, or a deep-research prompt generated for an external tool. Distinguishes itself from Research Discussion's casual paper lookup by producing artifacts (per-paper notes, survey synthesis, reusable prompts) under the academic search discipline.
- Use Academic Presentation Writing when the user wants to build, rewrite, or review slides for a talk (lab meeting, conference, defense) from a research backbone + loose notes. The human owns the story; the AI does logic-gap checking, slide text, diagram redraw, and figure proofread. Resolve and read the workspace's presentation style contract before any presentation work, as required by `references/academic-presentation-writing.md`. Format-agnostic output (Beamer / Keynote).
- Use Paper Co-writing when the human is actively drafting a paper manuscript with the assistant — building a chapter skeleton, delegating a formula-dense section, compressing the author's own draft sentences, or running a claiming or audit pass over a draft. It governs the collaboration protocol: who writes what, and when the assistant may write into the manuscript. Distinguish from `comment-revision-cycle` (external reviewer feedback on an existing manuscript), from Academic Presentation Writing (slides are a different medium), and from the production-delegation rule (heavy generation stays delegated; this mode decides whether any generated text enters the manuscript). Requires the workspace's author contract per `references/paper-co-writing.md`.

Load the relevant reference file for the selected mode:

- `references/research-discussion.md`
- `references/concept-explainer.md`
- `references/research-log-writing.md`
- `references/research-decision-writing.md`
- `references/task-writing.md`
- `references/reference-writing.md`
- `references/literature-survey.md` (resumable Codex-orchestrated pipeline with protocol helpers in `assets/literature-survey/`)
- `references/academic-presentation-writing.md`
- `references/paper-co-writing.md` (requires the workspace-root `PAPER-WRITING-CONTRACT.md`; template in `assets/paper-writing-contract/`)

Not modes, loaded on demand:

- `references/task-dispatch.md` — when the human asks to dispatch a task batch to a code agent and supervise it to completion (assistant side).
- `references/code-agent-execution.md` — the executor-side contract; point the executing code-agent session at it.
- `references/comment-revision-cycle.md` — when the human has a batch of reviewer feedback on a manuscript (any source) to turn into confirmed, executed, verified edits through one gated roadmap.

Always apply `references/shared-collaboration-rules.md`.

## Collaboration Protocol

Do not immediately produce a large final artifact while the human is defining workflow rules, naming conventions, scope, or writing mode behavior.

When workflow intent is still being negotiated, respond with the proposed interpretation, minimal schema or rule change, ambiguity or risk, and required confirmation.

When the user gives a concrete generation request and enough content, produce the artifact. Do not add broad restructuring beyond the requested mode.

## Evidence Discipline

Full rules live in the always-applied `references/shared-collaboration-rules.md` (Evidence Labels, information safety): separate observation from claim from hypothesis; never fabricate references, results, code behavior, paths, run IDs, or acceptance criteria. When external evidence is necessary for a material claim, ask for the source or use available search/connectors/tools according to the host environment.

## Codebase Snapshot

The code / implementation agent can return a structured report on how the repository actually implements something; request one before finalizing any artifact that depends on current repository behavior rather than pure research reasoning. Trigger conditions, request format, and rules (read-only default; findings enter documents as **Observation**, never Claim or Decision; never block on it): `references/shared-collaboration-rules.md` § Codebase Snapshot Integration.

## Language Policy

Use the language requested by the user. By default:

- Human-facing research logs may preserve mixed language, including informal notes and bilingual terminology.
- Code-agent-facing decision, task, and reference artifacts should be written in English unless the user explicitly requests otherwise.
- Respond to the human in the conversation language unless the requested artifact has its own language requirement.

## Output Policy

For research logs, progress notes, decisions, references, and code-agent tasks, default to inline markdown code blocks. Do not create downloadable files, canvas artifacts, or direct file edits unless the human explicitly asks for a file, artifact, canvas, or direct file editing.

After the block, provide a suggested filename or path if appropriate.

For task-writing, use the strict template and rules in `references/task-writing.md`.

For decision-writing, preserve structure but keep it concise and implementation-relevant.

Research Discussion produces no file or artifact by default — it is conversation. When thinking converges, offer to capture it into one of the four writing modes; do not auto-write.
