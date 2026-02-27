# Test and Evaluation Guide

The `tests/agent-eval/` directory contains evaluation scenarios for Super_red_team_bot modules.

## Structure
- `recon-eval.json`         # Recon clustering evaluation criteria
- `secure-review-eval.json` # Secure code review evaluation criteria
- `triage-eval.json`        # Vulnerability triage evaluation criteria

## Adding Tests
- Add new JSON files for additional evaluation scenarios.
- Each file should specify the task and criteria for success.

## Running Tests
- Use the evaluation criteria to benchmark module performance.
- Automated test scripts can be added to this directory.

## Example
See the provided JSON files for evaluation structure.
