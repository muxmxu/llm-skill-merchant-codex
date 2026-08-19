#!/usr/bin/env bash
# Validate and print a safe DISPATCH / NUDGE kickoff line (Codex dispatch grammar).
# Usage:
#   validate-kickoff.sh DISPATCH <task_id> <revision> <task_sha256> <manifest_id> <manifest_sha256>
#   validate-kickoff.sh NUDGE    <task_id> <revision> <manifest_id> <manifest_sha256> <stall_epoch> <token_id>
# Prints the single-line payload on stdout iff every field passes the
# whitelist; exits non-zero otherwise. Send the output through a native
# argv or structured send API — never build the line by shell interpolation.
set -euo pipefail
ID_RE='^[A-Za-z0-9._-]{1,128}$'
UINT_RE='^[1-9][0-9]*$'
HEX_RE='^[0-9a-f]{64}$'
kind="${1:?kind (DISPATCH|NUDGE) required}"
case "$kind" in
  DISPATCH)
    task_id="${2:?}"; revision="${3:?}"; task_sha="${4:?}"; man_id="${5:?}"; man_sha="${6:?}"
    [[ "$task_id" =~ $ID_RE ]]   || { echo "invalid task_id" >&2; exit 1; }
    [[ "$revision" =~ $UINT_RE ]] || { echo "invalid revision" >&2; exit 1; }
    [[ "$task_sha" =~ $HEX_RE ]]  || { echo "invalid task_sha256" >&2; exit 1; }
    [[ "$man_id" =~ $ID_RE ]]     || { echo "invalid manifest_id" >&2; exit 1; }
    [[ "$man_sha" =~ $HEX_RE ]]   || { echo "invalid manifest_sha256" >&2; exit 1; }
    printf 'DISPATCH task_id=%s revision=%s task_sha256=%s manifest_id=%s manifest_sha256=%s\n' \
      "$task_id" "$revision" "$task_sha" "$man_id" "$man_sha" ;;
  NUDGE)
    task_id="${2:?}"; revision="${3:?}"; man_id="${4:?}"; man_sha="${5:?}"; stall="${6:?}"; token="${7:?}"
    [[ "$task_id" =~ $ID_RE ]]   || { echo "invalid task_id" >&2; exit 1; }
    [[ "$revision" =~ $UINT_RE ]] || { echo "invalid revision" >&2; exit 1; }
    [[ "$man_id" =~ $ID_RE ]]     || { echo "invalid manifest_id" >&2; exit 1; }
    [[ "$man_sha" =~ $HEX_RE ]]   || { echo "invalid manifest_sha256" >&2; exit 1; }
    [[ "$stall" =~ $UINT_RE ]]    || { echo "invalid stall_epoch" >&2; exit 1; }
    [[ "$token" =~ $ID_RE ]]      || { echo "invalid token_id" >&2; exit 1; }
    printf 'NUDGE task_id=%s revision=%s manifest_id=%s manifest_sha256=%s stall_epoch=%s token_id=%s\n' \
      "$task_id" "$revision" "$man_id" "$man_sha" "$stall" "$token" ;;
  *) echo "kind must be DISPATCH or NUDGE" >&2; exit 1 ;;
esac
