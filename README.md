# llm-skill-merchant-codex

Codex marketplace for mux's human-AI research collaboration skills.

This repository is the Codex counterpart of `llm-skill-merchant`. It preserves
the same role boundaries and document contracts while replacing Claude-only
metadata, Workflow scripts, and dispatch assumptions with Codex-compatible
plugins and collaboration rules.

## Install

```bash
codex plugin marketplace add LinhMuks-DFox/llm-skill-merchant-codex
codex plugin add human-ai-code-agent-kit@llm-skill-merchant-codex
codex plugin add human-ai-research-assistant-kit@llm-skill-merchant-codex
codex plugin add multi-agent-discussion@llm-skill-merchant-codex
```

For local development, register the checkout path instead of the GitHub source.
Reinstall an updated plugin so Codex refreshes its cached snapshot, then start a
new thread.

## Plugins

| Plugin | Skills | Purpose |
|---|---|---|
| `human-ai-code-agent-kit` | `impl`, `exp`, `eval`, `ops`, `codebase-snapshot` | Implementation, experiment lifecycle, evaluation, compute operations, and read-only code inspection. |
| `human-ai-research-assistant-kit` | `research-assistant` | Research discussion, explanation, logs, decisions, tasks, references, literature surveys, presentations, and gated reviewer-comment-to-manuscript revision. |
| `multi-agent-discussion` | `multi-agent-discussion` | File-based, multi-round research debate with human arbitration. |

Project-specific facts remain in project runbooks such as `ROLE.txt`,
`RESEARCH-CONTEXT.md`, `EXPERIMENTS.md`, `EVALUATION.md`, and `OPERATIONS.md`.

## Source relationship

The initial migration tracks Claude marketplace commit `2687b2f`; the
comment-revision cycle is ported from Claude commit `8b1cb4d`. Functional
content is preserved except where the host contract differs. Intentional Codex
adaptations include plugin manifests, role-tag syntax, collaboration-tool
orchestration, authenticated execution authority, immutable dispatch records,
shared-worktree rules, and the resumable literature-survey pipeline. Claude
Workflow JavaScript templates are not carried into this repo.

Sync 2026-08-19 tracks Claude marketplace commit `9dea1c1`: paper-co-writing
mode (9th) + author-contract template ported verbatim (host-agnostic); SKILL.md
renamed, deduplicated, and re-ordered to match; orphaned
`assets/code-agent-task-template.md` removed on both sides; a Codex-grammar
`validate-kickoff.sh` written against this repo's dispatch manifest fields
(not a copy of the Claude one).
