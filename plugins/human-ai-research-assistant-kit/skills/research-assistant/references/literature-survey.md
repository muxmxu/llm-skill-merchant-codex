# Literature Survey Mode (AI-Dug Papers)

Use when the human asks to survey a topic, dig prior work, or build a reading list — typically via fan-out sub-agents, or via an external deep-research tool (see "Deep-research prompt generation"). Three deliverable types, all or some per request:

1. **Survey synthesis** — convergent findings, delivered in chat and/or folded into a research log section.
2. **Per-paper review notes** — written into the AI-survey notes directory declared in RESEARCH-CONTEXT.md `## Literature` (NOT the human-read notes directory, which is reserved for the human's own reading).
3. **Deep-research prompt** — a self-contained prompt for ChatGPT Deep Research or similar.

Path resolution: every workspace location this mode writes to (notes dir, PDF dir, dashboard) comes from RESEARCH-CONTEXT.md `## Literature` — contract and resolution rules in `references/research-context.md`. Doc missing → offer init; do not guess.

## Search discipline (academic rules — apply to every agent and every prompt)

1. **Source hierarchy**: peer-reviewed venue (journal / conference proceedings) > arXiv preprint > workshop paper > technical blog. Preprints must be labeled as preprints; check whether a published version exists and cite that instead. Blogs are background only — never citable evidence.
2. **Verify venue and year from the paper itself** (PDF header / official venue page), never from search snippets or secondary citations.
3. **Read before claiming**: every number, equation, or recipe detail in a note must come from the PDF actually read. If a paper is paywalled or unreadable, mark the entry LOW-CONFIDENCE and do not cite implementation details from it.
4. **Originals over surveys**: claims cite the original paper; survey papers are for mapping the field only.
5. **Dedupe first**: before writing a note, check the reference-manager library and both note directories (AI-survey and human-read, per RESEARCH-CONTEXT.md `## Literature`) for an existing entry; update rather than duplicate.
6. **Negative results are first-class**: reported failures, instabilities, and "we switched away from X because" findings are explicitly in scope and often the most valuable output.
7. **Convergence rule**: a synthesis claim may be called "convergent" only with ≥ 2 independent sources; otherwise attribute it to its single source.
8. **Lineage tracing**: for methods, note what the field later replaced them with and why — a method's abandonment history is evidence.
9. **Record code and data availability** per paper.
10. **Every entry carries**: title, venue + year, arXiv ID / DOI, URL.

## Per-paper note format

- Location: the AI-survey notes directory from RESEARCH-CONTEXT.md `## Literature`, in a `<YYYY-MM>/` subfolder; filename `<YYYY - Title>.md` (year, " - ", title with ":" replaced by " - ").
- Frontmatter (ZoteroImport-derived contract — dashboards depend on these fields):

```yaml
---
type: paper
citekey: "<authorKeywordYear>"
title: "<full title>"
authors: "<comma-separated>"
publication: "<venue>"
year: "<YYYY>"
date: "<YYYY-MM-DD>"
url: "<arxiv abs / venue url>"
zotero_link: ""            # empty until imported to Zotero
pdf_link: "[<pdf file>](file://<absolute local path>)"
status: reading            # AI NEVER sets read — read means the human personally read it
origin: ai-survey
tags:
  - research
  - AI-dug
  - <topical tags>
---
```

- Body sections (match the human's own paper-review note style): Abstract callout (verbatim) → `#### Summary` (核心问题 / 方法（配方细节）/ 实验与关键数字) → `#### 杂谈 + 思考 + 批判` (genuine critique + relevance to the current project) → `#### Relation` (link the project note and sibling reviews).
- Writing rules: Chinese plain short sentences; expand abbreviations at first use; math in LaTeX `$...$`; no metaphor pile-ups; no AI attribution inside the note body.
- PDFs: download to the PDF storage directory from RESEARCH-CONTEXT.md `## Literature` (topic-subfoldered) with naming `YYYY-Venue-Author-Keyword-<arxivId>.pdf`; `pdf_link` points there.
- Dashboard: the notes dashboard declared in RESEARCH-CONTEXT.md `## Literature` picks notes up automatically if the frontmatter contract is respected.

## Citing AI-dug papers in research logs

- Link normally: `[[YYYY - Title]]`.
- A claim taken from an AI note the human has not personally read carries the marker 「出自 AI 精读，未亲核」. Drop the marker once the note's status flips to `read`.
- Any claim a design decision rests on must be re-verified by the human in the PDF, or explicitly accepted as AI-verified in the log.

## Fan-out orchestration (sub-agent surveys)

1. Split by **theme angle** (3-5 agents with distinct perspectives: e.g. by application domain / by method family / by failure-mode focus), not by paper count.
2. Each agent prompt must include: the search-discipline rules (condensed); the project-relevance paragraph (so critique sections judge applicability, write it fresh per survey); the full intended note-filename list (so cross-links resolve); the note template; instruction to read the PDF before writing and to return only a one-line-per-file final message.
3. The orchestrator (not the agents) writes the synthesis: convergent findings with source counts, contradictions flagged, then folds it into the research log. Per-paper detail stays in the notes.
4. Long-running fan-outs: run agents in background; if an agent dies (session limit, errors), the orchestrator re-launches its share — keep a written spec of assignments so relaunching is mechanical.

## Codex-orchestrated survey (the heavy pipeline)

For a large survey, use bounded Codex sub-agent batches plus filesystem
checkpoints. The protocol skeleton and deterministic helpers live in
`assets/literature-survey/`. The pipeline must remain resumable even when a
session ends and no agent state survives.

Four phases (see `assets/literature-survey/MISSION-template.md`):

1. **Search** — split by angle and dispatch one read-only search task per
   angle, up to the live concurrency limit. Each task writes only its own
   `findings-<angle>.md` and returns the path.
2. **Dedupe + download** — the main session deduplicates, excludes already
   owned papers, builds `review-manifest.md`, and runs `download.sh`. The
   manifest table is `# | Title | Venue+Year | Primary angle | PDF filename |
   Note filename`.
3. **Deep-read** — assign no more than four papers per agent. Give agents
   disjoint note files. Each agent reads the PDF before claiming, checks for a
   complete target note first, and skips completed work.
4. **Verify → digest → synthesize → report** — dispatch independent
   verification tasks per note or small note batch. Reviewers re-read PDFs and
   return `FIXED`, `PASS`, or `FLAG`. After verification settles, dispatch one
   digest task per angle. The main session writes `synthesis-draft.md`, updates
   the research log, and runs the final link check.

Codex agents share the filesystem. Never assign the same note to concurrent
writers. Respect the runtime's available slots and do not assume per-agent
model selection. If collaboration tools are unavailable, run the same batches
serially.

**Resume after interruption — checkpoint is the filesystem.** Every completed
note is independent of session memory. Run `bash check-progress.sh`, rebuild
assignments only for missing notes, and repeat the idempotent deep-read phase.
Always verify before digest.

## Deep-research prompt generation (ChatGPT etc.)

When the human asks for a deep-research prompt instead of (or in addition to) a sub-agent survey, emit ONE self-contained prompt block containing, in order:

1. **Context** — project background written fresh for a zero-context reader (no internal jargon without definition).
2. **Research questions** — 3-7, ranked by priority, each answerable by literature.
3. **Search constraints** — the search-discipline rules above, condensed to a numbered list (source hierarchy, verify venues, originals over surveys, negative results in scope, convergence rule).
4. **Required output format** — per-paper structured entries (title | venue+year | arXiv/DOI | method recipe | hyperparameters | verification protocol | one-line takeaway) + a synthesis section with convergence counts + an explicit "not found / uncertain" section.
5. **Exclusion list** — papers already reviewed (titles), so the tool digs new ground.

Deliver inline in chat, and save a copy under the project root (e.g. `deep_research_prompt_<topic>.md`) when the human wants to reuse it. Results coming back from the external tool are treated as UNVERIFIED leads: before any claim enters a note or log, fetch and read the actual paper per the search discipline above.
