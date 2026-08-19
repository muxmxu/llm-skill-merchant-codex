#!/usr/bin/env python3
"""Validate a Comment Revision Cycle roadmap without external dependencies."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path


HEADER_FIELDS = (
    "roadmap_id",
    "decision_revision",
    "source",
    "manuscript",
    "manuscript_baseline",
    "date",
    "gate_state",
    "gate_authority_ref",
    "decision_snapshot",
)
SNAPSHOT_HEADER_FIELDS = tuple(
    field for field in HEADER_FIELDS if field != "decision_snapshot"
)
BLOCK_FIELDS = (
    "anchor",
    "comment",
    "author",
    "date",
    "category",
    "options",
    "decision",
    "answer",
    "status",
    "note",
    "last-touched-by",
)
FROZEN_BLOCK_FIELDS = (
    "anchor",
    "comment",
    "author",
    "date",
    "category",
    "options",
    "decision",
    "answer",
)
CATEGORIES = {"applied-explanation", "actionable", "question"}
STATUSES = {
    "awaiting-human",
    "confirmed",
    "in-progress",
    "done",
    "wont-fix",
    "question",
    "blocked-build",
}
ID_RE = re.compile(r"[A-Za-z0-9._-]{1,128}\Z")
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}\Z")
BASELINE_RE = re.compile(
    r".+;\s*worktree_diff_sha256=(?:clean|[0-9a-f]{64})\Z"
)
SNAPSHOT_RE = re.compile(r"(?P<path>.+)@sha256:(?P<hash>[0-9a-f]{64})\Z")
BLOCK_START_RE = re.compile(r"^### \[([^\]]+)\]\s*$")
HEADER_RE = re.compile(r"^([a-z][a-z0-9_-]*):\s*(.*)$")
FIELD_RE = re.compile(r"^- ([a-z][a-z0-9-]*):\s*(.*)$")
OPTION_RE = re.compile(r"(?m)^\s*[A-C]\)\s+\S")


@dataclass
class Block:
    item_id: str
    fields: dict[str, str]


@dataclass
class Roadmap:
    header: dict[str, str]
    blocks: list[Block]
    parse_errors: list[str]


def parse_roadmap(path: Path) -> Roadmap:
    lines = path.read_text(encoding="utf-8").splitlines()
    header: dict[str, str] = {}
    blocks: list[Block] = []
    errors: list[str] = []
    current: Block | None = None
    current_field: str | None = None

    for lineno, line in enumerate(lines, 1):
        block_match = BLOCK_START_RE.match(line)
        if block_match:
            item_id = block_match.group(1).strip()
            if any(block.item_id == item_id for block in blocks):
                errors.append(f"line {lineno}: duplicate item id [{item_id}]")
            current = Block(item_id=item_id, fields={})
            blocks.append(current)
            current_field = None
            continue

        if current is None:
            header_match = HEADER_RE.match(line)
            if header_match and header_match.group(1) in HEADER_FIELDS:
                key, value = header_match.groups()
                if key in header:
                    errors.append(f"line {lineno}: duplicate header field {key}")
                header[key] = value.strip()
            continue

        field_match = FIELD_RE.match(line)
        if field_match:
            key, value = field_match.groups()
            if key in current.fields:
                errors.append(
                    f"line {lineno}: item [{current.item_id}] duplicates field {key}"
                )
            current.fields[key] = value.rstrip()
            current_field = key
            continue

        if current_field and (line.startswith("    ") or not line.strip()):
            continuation = line.strip()
            if continuation:
                old = current.fields[current_field]
                current.fields[current_field] = (
                    f"{old}\n{continuation}" if old else continuation
                )

    return Roadmap(header=header, blocks=blocks, parse_errors=errors)


def is_placeholder(value: str) -> bool:
    stripped = value.strip().strip('"').strip()
    return stripped.startswith("<") and stripped.endswith(">")


def option_count(value: str) -> int:
    return len(OPTION_RE.findall(value))


def validate_structure(
    roadmap: Roadmap, *, snapshot: bool = False
) -> list[str]:
    errors = list(roadmap.parse_errors)
    required_headers = SNAPSHOT_HEADER_FIELDS if snapshot else HEADER_FIELDS

    for field in required_headers:
        if field not in roadmap.header:
            errors.append(f"missing header field: {field}")

    required_nonempty = {
        "roadmap_id",
        "decision_revision",
        "source",
        "manuscript",
        "manuscript_baseline",
        "date",
        "gate_state",
    }
    for field in required_nonempty:
        value = roadmap.header.get(field, "")
        if not value or is_placeholder(value):
            errors.append(f"header field {field} must have a concrete value")

    roadmap_id = roadmap.header.get("roadmap_id", "")
    if roadmap_id and not ID_RE.fullmatch(roadmap_id):
        errors.append("roadmap_id must match [A-Za-z0-9._-]{1,128}")

    revision = roadmap.header.get("decision_revision", "")
    if revision and (not revision.isdigit() or int(revision) < 1):
        errors.append("decision_revision must be a positive integer")

    date = roadmap.header.get("date", "")
    if date and not DATE_RE.fullmatch(date):
        errors.append("header date must use YYYY-MM-DD")

    baseline = roadmap.header.get("manuscript_baseline", "")
    if baseline and not is_placeholder(baseline) and not BASELINE_RE.fullmatch(baseline):
        errors.append(
            "manuscript_baseline must end with "
            "worktree_diff_sha256=clean or a lowercase SHA-256"
        )

    gate_state = roadmap.header.get("gate_state", "")
    if gate_state and gate_state not in {"gating", "ready"}:
        errors.append("gate_state must be gating or ready")

    if not roadmap.blocks:
        errors.append("roadmap must contain at least one comment block")

    for block in roadmap.blocks:
        if not ID_RE.fullmatch(block.item_id):
            errors.append(
                f"item [{block.item_id}] id must match [A-Za-z0-9._-]{{1,128}}"
            )
        missing = [field for field in BLOCK_FIELDS if field not in block.fields]
        extra = [field for field in block.fields if field not in BLOCK_FIELDS]
        if missing:
            errors.append(f"item [{block.item_id}] missing fields: {', '.join(missing)}")
        if extra:
            errors.append(f"item [{block.item_id}] unknown fields: {', '.join(extra)}")
        validate_block(block, errors)

    return errors


def validate_block(block: Block, errors: list[str]) -> None:
    fields = block.fields
    required_nonempty = (
        "anchor",
        "comment",
        "author",
        "date",
        "category",
        "status",
        "last-touched-by",
    )
    for field in required_nonempty:
        value = fields.get(field, "")
        if not value or is_placeholder(value):
            errors.append(f"item [{block.item_id}] field {field} needs a concrete value")

    date = fields.get("date", "")
    if date and not is_placeholder(date) and not DATE_RE.fullmatch(date):
        errors.append(f"item [{block.item_id}] date must use YYYY-MM-DD")

    category = fields.get("category", "")
    status = fields.get("status", "")
    options = fields.get("options", "").strip()
    decision = fields.get("decision", "").strip()
    answer = fields.get("answer", "").strip()

    for field in ("decision", "answer", "note"):
        value = fields.get(field, "").strip()
        if value and is_placeholder(value):
            errors.append(
                f"item [{block.item_id}] field {field} must be blank or concrete"
            )

    if category not in CATEGORIES:
        errors.append(f"item [{block.item_id}] has invalid category: {category}")
        return
    if status not in STATUSES:
        errors.append(f"item [{block.item_id}] has invalid status: {status}")

    if status in {"confirmed", "in-progress", "blocked-build"} and not decision:
        errors.append(f"item [{block.item_id}] status {status} requires decision")

    if category == "applied-explanation":
        if options != "verify-only":
            errors.append(
                f"item [{block.item_id}] applied-explanation requires options: verify-only"
            )
        if decision:
            errors.append(
                f"item [{block.item_id}] applied-explanation decision must stay empty"
            )
        if status not in {"done", "question"}:
            errors.append(
                f"item [{block.item_id}] applied-explanation status must be done or question"
            )
        return

    count = option_count(options)
    if re.search(r"<(?:option|tradeoff)\b", options, flags=re.IGNORECASE):
        errors.append(f"item [{block.item_id}] options still contain placeholders")
    if category == "actionable" and count not in {2, 3}:
        errors.append(f"item [{block.item_id}] actionable requires 2-3 A/B/C options")
    if category == "question" and options and count not in {2, 3}:
        errors.append(
            f"item [{block.item_id}] question options must be empty or contain 2-3 A/B/C options"
        )
    if category == "question" and status == "done" and not (answer or decision):
        errors.append(
            f"item [{block.item_id}] resolved question requires answer or decision"
        )
    if category == "actionable" and status == "done" and not decision:
        errors.append(f"item [{block.item_id}] completed actionable requires decision")


def snapshot_path_and_hash(roadmap_path: Path, value: str) -> tuple[Path, str] | None:
    match = SNAPSHOT_RE.fullmatch(value)
    if not match:
        return None
    snapshot_path = Path(match.group("path")).expanduser()
    if not snapshot_path.is_absolute():
        snapshot_path = roadmap_path.parent / snapshot_path
    return snapshot_path.resolve(), match.group("hash")


def verify_snapshot(roadmap_path: Path, roadmap: Roadmap) -> list[str]:
    errors: list[str] = []
    value = roadmap.header.get("decision_snapshot", "")
    parsed = snapshot_path_and_hash(roadmap_path, value)
    if parsed is None:
        return ["decision_snapshot must use <path>@sha256:<64-char lowercase hash>"]

    snapshot_path, expected_hash = parsed
    if not snapshot_path.is_file():
        return [f"decision snapshot does not exist: {snapshot_path}"]

    payload = snapshot_path.read_bytes()
    actual_hash = hashlib.sha256(payload).hexdigest()
    if actual_hash != expected_hash:
        errors.append(
            f"decision snapshot hash mismatch: expected {expected_hash}, got {actual_hash}"
        )

    snapshot = parse_roadmap(snapshot_path)
    errors.extend(f"snapshot: {error}" for error in validate_structure(snapshot, snapshot=True))
    if snapshot.header.get("gate_state") != "ready":
        errors.append("snapshot: gate_state must be ready")

    for field in SNAPSHOT_HEADER_FIELDS:
        if roadmap.header.get(field, "") != snapshot.header.get(field, ""):
            errors.append(f"snapshot differs from live roadmap header field: {field}")

    live_ids = [block.item_id for block in roadmap.blocks]
    snapshot_ids = [block.item_id for block in snapshot.blocks]
    if live_ids != snapshot_ids:
        errors.append("snapshot comment ids/order differ from live roadmap")
        return errors

    for live, frozen in zip(roadmap.blocks, snapshot.blocks):
        for field in FROZEN_BLOCK_FIELDS:
            if live.fields.get(field, "") != frozen.fields.get(field, ""):
                errors.append(
                    f"snapshot item [{live.item_id}] differs in frozen field: {field}"
                )
    return errors


def validate_phase(path: Path, roadmap: Roadmap, phase: str) -> list[str]:
    errors = validate_structure(roadmap)
    gate_state = roadmap.header.get("gate_state", "")
    authority = roadmap.header.get("gate_authority_ref", "")
    snapshot = roadmap.header.get("decision_snapshot", "")

    if phase == "intake":
        if gate_state != "gating":
            errors.append("intake phase requires gate_state: gating")
        if authority:
            errors.append("intake phase requires empty gate_authority_ref")
        if snapshot:
            errors.append("intake phase requires empty decision_snapshot")
        return errors

    if gate_state != "ready":
        errors.append(f"{phase} phase requires gate_state: ready")
    if not authority or is_placeholder(authority):
        errors.append(f"{phase} phase requires concrete gate_authority_ref")
    if not snapshot or is_placeholder(snapshot):
        errors.append(f"{phase} phase requires concrete decision_snapshot")
    else:
        errors.extend(verify_snapshot(path, roadmap))

    if phase == "execute":
        for block in roadmap.blocks:
            status = block.fields.get("status", "")
            if status in {"awaiting-human", "question"}:
                errors.append(
                    f"item [{block.item_id}] unresolved status {status} blocks execution"
                )
            if status == "blocked-build":
                errors.append(f"item [{block.item_id}] blocked-build halts the batch")
    elif phase == "complete":
        for block in roadmap.blocks:
            status = block.fields.get("status", "")
            if status not in {"done", "wont-fix"}:
                errors.append(
                    f"item [{block.item_id}] status {status} is not terminal for completion"
                )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roadmap", type=Path)
    parser.add_argument(
        "--phase", choices=("intake", "execute", "complete"), required=True
    )
    args = parser.parse_args()

    path = args.roadmap.expanduser().resolve()
    if not path.is_file():
        print(f"ERROR: roadmap does not exist: {path}", file=sys.stderr)
        return 2

    try:
        roadmap = parse_roadmap(path)
        errors = validate_phase(path, roadmap, args.phase)
    except (OSError, UnicodeError) as exc:
        print(f"ERROR: cannot read roadmap: {exc}", file=sys.stderr)
        return 2

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"FAIL: {len(errors)} validation error(s)", file=sys.stderr)
        return 1

    print(
        f"PASS: {path.name} is valid for phase={args.phase} "
        f"({len(roadmap.blocks)} item(s))"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
