<!-- runbook-contract: research-context v1 -->
# Research Context

<!-- AI-agnostic resource map for this research workspace: static,
     human-approved facts only. Every AI reads this file to locate
     resources; per-AI instruction files (CLAUDE.md, ...) keep identity +
     style + a pointer here. Skills navigate by the exact H2 headings below
     — do not rename them. Dynamic session state does NOT belong here: the
     AI-maintained brief lives at tmp/latest-brief.md. -->

## Workspace overview

<!-- What this research project is, in a paragraph. What the workspace is
     for (discussion-only / code-included). Language conventions if any. -->

## Research logs

<!-- Where research logs live; the frontmatter a log must carry to be picked
     up by dashboards; naming/date conventions; the TOC/dashboard; storage
     caveats (e.g. cloud-synced, possibly unmaterialized files). -->

## Literature

<!-- Reference-manager library: path, lock/access notes, collections that
     matter. AI-survey notes dir. Human-read notes dir + boundary (AI never
     writes there). PDF storage dir + naming. Dashboard/TOC. -->

## Note spaces

<!-- Inventory of other note areas (study notes, tech notes, ...), each with
     its local conventions (frontmatter or none, language, granularity).
     Consumers pick a fitting existing area — creating new directories is
     forbidden. -->

## Papers & presentations

<!-- Each paper/presentation project: location, link mechanism (symlink to
     an independent git repo?), and what editing a linked path really
     edits. -->

## Code & compute

<!-- Each code repo: local path/symlink, remote host + access command,
     evidence discipline (read-only by default), pointer to the repo's own
     runbooks (EXPERIMENTS.md, OPERATIONS.md, ...). Index, don't
     duplicate. -->

## Discussion archive

<!-- Where multi-agent/human discussions are archived; per-agent file
     conventions. -->

## Dispatch & code agents

<!-- Optional; required only when dispatch is used.

Contracts:
- dispatch contract path
- executor contract path

Delivery modes:
- bus repo + remote, if used
- authenticated human-approved direct transports + allowed roots/APIs

Handoff ledger:
- append-only dispatch-manifest location + manifest-id convention

Endpoints:
- endpoint id; address/session; transport; harness; assignment state

Authentication:
- trusted main-conversation or authenticated human-message event references

Artifact paths:
- ACK, completion report, gate record, and result-signal conventions for each mode

Safe kickoff:
- native argv or structured API that carries only the allowlisted payload from
  task-dispatch.md; never shell source

Watcher:
- watcher-owner convention
- structured/literal-input nudge transport + allowlisted token ids
- readiness source proving the pane is an agent prompt, never a shell

Execution workspace:
- batch-directory and branch conventions
-->
