#!/usr/bin/env bash
# Simple script to create GitHub Issues from `BACKLOG.csv` using the GitHub CLI (`gh`).
# Usage: `scripts/create_issues.sh` (requires `gh` authenticated and repository remote set)

set -euo pipefail

CSV_FILE="$(dirname "$0")/../BACKLOG.csv"
if [ ! -f "$CSV_FILE" ]; then
  echo "ERROR: $CSV_FILE not found"
  exit 1
fi

echo "Reading $CSV_FILE and creating/updating issues (one per row). Press Ctrl+C to cancel."

# Ensure the 'backlog' label exists (create if missing)
if ! gh label view backlog >/dev/null 2>&1; then
  echo "Label 'backlog' not found — creating it."
  if gh label create backlog --color "0e8a16" --description "Sprint backlog tasks" >/dev/null 2>&1; then
    echo "✓ Label 'backlog' created"
    USE_LABEL=true
  else
    echo "Warning: failed to create label 'backlog'. Issues will be created without that label." >&2
    USE_LABEL=false
  fi
else
  USE_LABEL=true
fi

# Parse CSV header to determine fields
HEADER=$(head -n1 "$CSV_FILE")

# Determine whether labels and assignees columns exist
HAS_LABELS=false
HAS_ASSIGNEES=false
if echo "$HEADER" | grep -q "labels"; then HAS_LABELS=true; fi
if echo "$HEADER" | grep -q "assignees"; then HAS_ASSIGNEES=true; fi

# Iterate rows
tail -n +2 "$CSV_FILE" | while IFS=, read -r id task owner status issue_link labels assignees; do
  id=$(echo "$id" | xargs)
  task=$(echo "$task" | xargs)
  owner=$(echo "$owner" | xargs)
  status=$(echo "$status" | xargs)
  labels=$(echo "${labels:-}" | xargs)
  assignees=$(echo "${assignees:-}" | xargs)

  title="$id: $task"
  body="Owner: $owner\nStatus: $status\n\nSource: BACKLOG.md"

  echo "Processing: $title"

  # Check if an issue with this exact title already exists
  existing_number=$(gh issue list --search "$title" --limit 1 --json number,title --jq '.[0].number' 2>/dev/null || true)

  if [ -n "$existing_number" ] && [ "$existing_number" != "null" ]; then
    echo "  Updating existing issue #$existing_number"
    # Add backlog label if available
    if [ "${USE_LABEL}" = true ]; then
      gh issue edit "$existing_number" --add-label backlog >/dev/null 2>&1 || true
    fi
    # Add any CSV labels
    if [ "$HAS_LABELS" = true ] && [ -n "$labels" ]; then
      # split labels by semicolon or pipe or comma
      IFS=';|' read -ra LAB_ARR <<< "$labels"
      for l in "${LAB_ARR[@]}"; do
        l=$(echo "$l" | xargs)
        [ -n "$l" ] && gh issue edit "$existing_number" --add-label "$l" >/dev/null 2>&1 || true
      done
    fi
    # Add assignees if provided
    if [ "$HAS_ASSIGNEES" = true ] && [ -n "$assignees" ]; then
      IFS=';|' read -ra ASS_ARR <<< "$assignees"
      for a in "${ASS_ARR[@]}"; do
        a=$(echo "$a" | xargs)
        [ -n "$a" ] && gh issue edit "$existing_number" --add-assignee "$a" >/dev/null 2>&1 || true
      done
    fi
    # Update issue body to include status/owner (overwrite body)
    gh issue edit "$existing_number" --body "$body" >/dev/null 2>&1 || true
  else
    echo "  Creating new issue"
    CMD=(gh issue create --title "$title" --body "$body")
    if [ "${USE_LABEL}" = true ]; then
      CMD+=(--label backlog)
    fi
    if [ "$HAS_LABELS" = true ] && [ -n "$labels" ]; then
      # allow comma/semicolon-separated labels in the CSV cell
      IFS=';|' read -ra LAB_ARR <<< "$labels"
      for l in "${LAB_ARR[@]}"; do
        l=$(echo "$l" | xargs)
        [ -n "$l" ] && CMD+=(--label "$l")
      done
    fi
    if [ "$HAS_ASSIGNEES" = true ] && [ -n "$assignees" ]; then
      IFS=';|' read -ra ASS_ARR <<< "$assignees"
      for a in "${ASS_ARR[@]}"; do
        a=$(echo "$a" | xargs)
        [ -n "$a" ] && CMD+=(--assignee "$a")
      done
    fi
    # Execute creation
    "${CMD[@]}" >/dev/null 2>&1 || { echo "Failed to create issue for row $id" >&2; exit 2; }
  fi
  sleep 0.2
done

echo "All done."
