---
name: slack-message-drafting
description: "Draft or revise Slack messages using workspace recipient tone rules. Use for Slack drafting, replies, or requested file and clipboard export. Never send, post, or schedule messages."
---

# Slack Message Drafting

Draft Slack messages for the user to paste and send themselves. The core
problem is recipient-specific register: an advisor may demand a short answer
while a peer expects context and reasoning. Register rules are workspace-local
facts, not skill content.

## Hard rule: drafting only

Never send, schedule, or post a message through any Slack tool. The deliverable
is always text the user sends manually.

## Tone resolution

1. Read the workspace's `SLACK-MESSAGE-TONE.md`. Look first at
   `merchant_skill_contract/SLACK-MESSAGE-CONTRACT/SLACK-MESSAGE-TONE.md`, then
   the workspace root as a legacy location. Its recipient profiles and shared
   formatting rules override the defaults below.
2. If the file exists at neither location, say so. Offer to create it from
   `assets/SLACK-MESSAGE-TONE.template.md`; for the current draft ask only for
   the recipient, language, expected length, and politeness.

## Audience resolution

Precedence: explicit user designation > an unambiguous tone-file profile > ask
the user. Never silently choose between plausible profiles.

## Modes

- **From-scratch**: order the user's points per the profile, keeping their
  uncertainty markers visible.
- **Reply**: address every point or question in the incoming message. If the
  user supplied no stance on one point, flag the gap instead of inventing one.

## Drafting rules

- Plain-text-safe by default. Slack's default composer does not parse pasted
  markup. Do not use `*bold*`, backticks, Markdown headings, or tables unless
  the profile explicitly says `Markup: mrkdwn allowed`.
- Follow the profile's language, length, opening, closing, and question form.
- Convey only what the user stated. Do not add facts, opinions, commitments,
  or deadlines. Use `[…]` for missing material and point it out.
- Short-register recipients get a main message plus an optional thread
  follow-up when details are needed.
- Put each draft in its own fenced code block, followed by at most two lines
  noting the profile and any omitted or placeholder material.

## Tone file maintenance

When a recipient's real reaction reveals a durable rule, propose adding that
evidence-backed rule to the tone file. Edit it only with the user's consent.

## Codex delivery boundary

This Codex port provides drafting only. The Claude-side `/slack-message:tof`
and `/slack-message:cp` command wrappers are intentionally not copied because
Codex does not use Claude command files. Save or copy a confirmed draft only
when the user explicitly requests that separate action.
