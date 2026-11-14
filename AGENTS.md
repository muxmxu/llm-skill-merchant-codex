# Public skill authoring

When producing or editing a skill in this public repository, keep it abstract: describe roles, steps, and interfaces in generic terms. Do not include machine names, user names, host or network addresses, local paths, repository names, or other personal or environment-specific facts. Put those facts in the consuming workspace's private contract and have the skill read them through declared contract-interface placeholders. Before committing, check the diff for these literals.

# Repository maintenance

Keep `master` as the integration branch. Create a branch only when needed; integrate completed work and remove its local and remote branch promptly. Do not leave task branches unattended. Preserve unmerged work and check remote state before cleanup.
