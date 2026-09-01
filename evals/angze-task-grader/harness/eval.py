#!/usr/bin/env python3
"""Synthetic evaluation harness for angze-task-grader."""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time
from typing import Any, Iterable


EVAL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = EVAL_ROOT.parents[1]
SKILL_SOURCE = REPO_ROOT / "skills" / "angze-task-grader"
CODE_STYLE_SKILL_SOURCE = REPO_ROOT / "skills" / "angze-code-style"
CODE_STYLE_FIXTURES_ROOT = REPO_ROOT / "evals" / "angze-code-style" / "fixtures"
CASES_ROOT = EVAL_ROOT / "cases"
FIXTURES_ROOT = EVAL_ROOT / "fixtures"
RESULTS_ROOT = EVAL_ROOT / "results"

TIER_NAMES = {
    "T0": "Mechanical",
    "T1": "Localized Patch",
    "T2": "Bounded Feature or Subsystem Audit",
    "T3": "High-Risk Change",
    "T4": "Release, Destructive, or Critical",
}
TIER_RANK = {tier: rank for rank, tier in enumerate(TIER_NAMES)}
CONTRACT_TYPES: dict[str, type] = {
    "tier": str,
    "tier_name": str,
    "risk_overrides": list,
    "reasons": list,
    "inspection_budget": list,
    "patch_budget": dict,
    "abstraction_budget": str,
    "validation_floor": list,
    "validation_ceiling": list,
    "documentation_budget": str,
    "review_requirement": str,
    "subagent_policy": str,
    "commit_strategy": str,
    "stop_condition": str,
    "escalation_triggers": list,
}
PATCH_BUDGET_TYPES = {"expected_scope": str, "file_guidance": str}
ALLOWED_RISK_OVERRIDES = {
    "scientific/numerical",
    "data/destructive",
    "compatibility/cross-platform",
    "uncertainty",
}
REQUIRED_LIST_FIELDS = {
    "reasons",
    "inspection_budget",
    "validation_floor",
    "validation_ceiling",
    "escalation_triggers",
}
RELEASE_GRADE_VALIDATION_PATTERNS = (
    re.compile(r"\bfull (?:repository |test )?suite\b", re.IGNORECASE),
    re.compile(r"\b(?:package build|build (?:the )?package)\b", re.IGNORECASE),
    re.compile(r"\bclean(?:-room)? install\b", re.IGNORECASE),
    re.compile(r"\brelease matrix\b", re.IGNORECASE),
)
NEGATION_PATTERN = re.compile(r"\b(?:do not|don't|no|not|never|without|avoid)\b", re.IGNORECASE)
ACTIONABLE_STOP_PATTERN = re.compile(
    r"^(?:stop\b|complete (?:only )?when\b|finish (?:only )?when\b|end (?:only )?when\b)",
    re.IGNORECASE,
)
TIER_COMPARISON_PATTERN = re.compile(
    r"\b(?:T[0-4]|Tier\s+[0-3])\b.{0,100}"
    r"\b(?:equivalent(?:\s+to)?|same\s+as|maps?\s+to|translates?\s+to|"
    r"higher\s+than|lower\s+than|outranks?|equals?)\b.{0,100}"
    r"\b(?:T[0-4]|Tier\s+[0-3])\b",
    re.IGNORECASE | re.DOTALL,
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def run(command: list[str], cwd: Path, *, timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=False,
    )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_contract(contract: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(contract, dict):
        return ["contract is not a JSON object"]
    expected_keys = set(CONTRACT_TYPES)
    actual_keys = set(contract)
    if actual_keys != expected_keys:
        missing = sorted(expected_keys - actual_keys)
        extra = sorted(actual_keys - expected_keys)
        errors.append(f"contract keys differ; missing={missing}, extra={extra}")
    for key, expected_type in CONTRACT_TYPES.items():
        if key in contract and not isinstance(contract[key], expected_type):
            errors.append(f"{key} must be {expected_type.__name__}")
    for key, value in contract.items():
        if key in CONTRACT_TYPES and isinstance(value, str) and not value.strip():
            errors.append(f"{key} must not be empty")
        if key in CONTRACT_TYPES and isinstance(value, list):
            if key in REQUIRED_LIST_FIELDS and not value:
                errors.append(f"{key} must contain at least one item")
            if any(not isinstance(item, str) or not item.strip() for item in value):
                errors.append(f"{key} entries must be non-empty strings")
    tier = contract.get("tier")
    if tier not in TIER_NAMES:
        errors.append(f"tier must be one of {sorted(TIER_NAMES)}")
    elif contract.get("tier_name") != TIER_NAMES[tier]:
        errors.append("tier_name does not match tier")
    overrides = contract.get("risk_overrides")
    if isinstance(overrides, list):
        unknown = sorted({item for item in overrides if isinstance(item, str)} - ALLOWED_RISK_OVERRIDES)
        if unknown:
            errors.append(f"unknown risk_overrides: {unknown}")
        if len(overrides) != len(set(item for item in overrides if isinstance(item, str))):
            errors.append("risk_overrides must not contain duplicates")
    patch_budget = contract.get("patch_budget")
    if isinstance(patch_budget, dict):
        if set(patch_budget) != set(PATCH_BUDGET_TYPES):
            errors.append("patch_budget keys differ from the stable schema")
        for key, expected_type in PATCH_BUDGET_TYPES.items():
            if key in patch_budget and not isinstance(patch_budget[key], expected_type):
                errors.append(f"patch_budget.{key} must be {expected_type.__name__}")
            elif key in patch_budget and not patch_budget[key].strip():
                errors.append(f"patch_budget.{key} must not be empty")
    stop_condition = contract.get("stop_condition")
    if isinstance(stop_condition, str) and stop_condition.strip() and not ACTIONABLE_STOP_PATTERN.match(stop_condition.lstrip()):
        errors.append("stop_condition must start with an actionable stop or completion condition")
    return errors


def output_schema() -> dict[str, Any]:
    properties: dict[str, Any] = {}
    for key, expected_type in CONTRACT_TYPES.items():
        if expected_type is str:
            properties[key] = {"type": "string", "minLength": 1}
        elif expected_type is list:
            properties[key] = {"type": "array", "items": {"type": "string", "minLength": 1}}
            if key in REQUIRED_LIST_FIELDS:
                properties[key]["minItems"] = 1
        elif key == "patch_budget":
            properties[key] = {
                "type": "object",
                "additionalProperties": False,
                "required": list(PATCH_BUDGET_TYPES),
                "properties": {name: {"type": "string", "minLength": 1} for name in PATCH_BUDGET_TYPES},
            }
    properties["tier"]["enum"] = list(TIER_NAMES)
    properties["tier_name"]["enum"] = list(TIER_NAMES.values())
    properties["risk_overrides"]["items"]["enum"] = sorted(ALLOWED_RISK_OVERRIDES)
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": list(CONTRACT_TYPES),
        "properties": properties,
    }


def validate_case_contract(case: dict[str, Any], contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if case["expected_tier"] not in {"T0", "T1"}:
        return errors
    ceiling = contract.get("validation_ceiling")
    if not isinstance(ceiling, list):
        return errors
    for item in ceiling:
        if not isinstance(item, str) or NEGATION_PATTERN.search(item):
            continue
        if any(pattern.search(item) for pattern in RELEASE_GRADE_VALIDATION_PATTERNS):
            errors.append(f"low-risk validation ceiling is release-grade: {item!r}")
    return errors


def score_contract(case: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    schema_errors = validate_contract(contract)
    semantic_errors = validate_case_contract(case, contract)
    actual = contract.get("tier")
    acceptable = {case["expected_tier"]}
    if case.get("acceptable_adjacent_tier"):
        acceptable.add(case["acceptable_adjacent_tier"])
    expected_overrides = (
        set(case["expected_risk_overrides"])
        if actual == case["expected_tier"]
        else set()
    )
    actual_overrides = set(contract.get("risk_overrides", [])) if isinstance(contract.get("risk_overrides"), list) else set()
    forbidden_undergrade = actual in set(case["forbidden_undergrade"])
    return {
        "schema_ok": not schema_errors,
        "schema_errors": schema_errors,
        "semantic_ok": not semantic_errors,
        "semantic_errors": semantic_errors,
        "tier_ok": actual in acceptable,
        "expected_tier": case["expected_tier"],
        "acceptable_tiers": sorted(acceptable),
        "actual_tier": actual,
        "overrides_ok": expected_overrides.issubset(actual_overrides),
        "missing_overrides": sorted(expected_overrides - actual_overrides),
        "forbidden_undergrade": forbidden_undergrade,
        "accepted": not schema_errors and not semantic_errors and actual in acceptable and expected_overrides.issubset(actual_overrides) and not forbidden_undergrade,
    }


def summarize_grading(results: list[dict[str, Any]]) -> dict[str, Any]:
    scored = [item for item in results if "score" in item]
    accepted = sum(bool(item["score"]["accepted"]) for item in scored)
    hard_gate_failures = []
    for item in scored:
        case = item["case"]
        score = item["score"]
        actual = score["actual_tier"]
        if actual not in TIER_RANK:
            continue
        expected = case["expected_tier"]
        canonical_t4_undergrade = expected == "T4" and TIER_RANK[actual] < TIER_RANK["T4"]
        protected_t3_undergrade = expected == "T3" and bool(case["required_hard_trigger"]) and TIER_RANK[actual] < TIER_RANK["T3"]
        if canonical_t4_undergrade or protected_t3_undergrade or score["forbidden_undergrade"]:
            hard_gate_failures.append(case["case_id"])
    accuracy = accepted / len(scored) if scored else 0.0
    return {
        "scored_cases": len(scored),
        "accepted_cases": accepted,
        "agreement": accuracy,
        "agreement_gate_passed": bool(scored) and accuracy >= 0.90,
        "hard_gate_failures": hard_gate_failures,
        "hard_gates_passed": not hard_gate_failures,
    }


def validate_case_files() -> None:
    grading = load_json(CASES_ROOT / "grading_cases.json")
    required_grading = {
        "case_id",
        "task_prompt",
        "fixture",
        "fixture_context_summary",
        "expected_tier",
        "acceptable_adjacent_tier",
        "required_hard_trigger",
        "expected_risk_overrides",
        "forbidden_undergrade",
        "expected_validation_ceiling",
        "rationale",
    }
    require(len(grading) >= 25, "grading suite must contain at least 25 cases")
    require(len({item["case_id"] for item in grading}) == len(grading), "grading case IDs must be unique")
    for item in grading:
        require(set(item) == required_grading, f"grading case {item.get('case_id')} has an unstable schema")
        require(item["expected_tier"] in TIER_NAMES, f"invalid tier in {item['case_id']}")
        require((FIXTURES_ROOT / item["fixture"]).is_dir(), f"missing fixture for {item['case_id']}")
        require(set(item["expected_risk_overrides"]) <= ALLOWED_RISK_OVERRIDES, f"unknown override in {item['case_id']}")
        require(item["expected_validation_ceiling"].strip(), f"empty validation ceiling in {item['case_id']}")
    counts = Counter(item["expected_tier"] for item in grading)
    minimums = {"T0": 4, "T1": 6, "T2": 6, "T3": 5, "T4": 4}
    for tier, minimum in minimums.items():
        require(counts[tier] >= minimum, f"{tier} needs at least {minimum} grading cases")
    require(any("scientific/numerical" in item["expected_risk_overrides"] for item in grading), "missing scientific override case")
    require(any("data/destructive" in item["expected_risk_overrides"] for item in grading), "missing data override case")
    require(any("uncertainty" in item["expected_risk_overrides"] for item in grading), "missing uncertainty override case")
    require(sum(item["required_hard_trigger"] == "de-escalation" for item in grading) >= 2, "missing de-escalation cases")

    routing = load_json(CASES_ROOT / "routing_cases.json")
    require(len({item["case_id"] for item in routing}) == len(routing), "routing case IDs must be unique")
    require(sum(item["should_trigger"] for item in routing) >= 6, "routing suite needs at least six positives")
    require(sum(not item["should_trigger"] for item in routing) >= 7, "routing suite needs at least seven negatives")
    for item in routing:
        require(set(item) == {"case_id", "should_trigger", "prompt", "reason"}, f"routing case {item.get('case_id')} has an unstable schema")

    implementations = load_json(CASES_ROOT / "implementation_cases.json")
    required_implementation = {
        "case_id",
        "fixture",
        "task_prompt",
        "expected_tier",
        "expected_overrides",
        "allowed_paths",
        "acceptance_command",
        "expected_baseline_exit",
    }
    require(4 <= len(implementations) <= 6, "bounded implementation suite must contain four to six cases")
    for item in implementations:
        require(set(item) == required_implementation, f"implementation case {item.get('case_id')} has an unstable schema")
        require((FIXTURES_ROOT / item["fixture"]).is_dir(), f"missing implementation fixture {item['fixture']}")

    composition = load_json(CASES_ROOT / "composition_cases.json")
    required_composition = {
        "case_id",
        "source_fixture",
        "target_path",
        "seed_replacement",
        "task_prompt",
        "expected_task_tiers",
        "expected_worktree_changed",
        "required_response_term_groups",
    }
    require(len(composition) == 1, "composition suite must contain exactly one canonical case")
    item = composition[0]
    require(set(item) == required_composition, "composition case has an unstable schema")
    require(set(item["seed_replacement"]) == {"from", "to"}, "composition seed replacement has an unstable schema")
    require(item["expected_task_tiers"] and set(item["expected_task_tiers"]) <= {"T0", "T1"}, "composition task must be low effort")
    require(item["expected_worktree_changed"] is False, "composition case must require an unchanged worktree")
    source = CODE_STYLE_FIXTURES_ROOT / item["source_fixture"]
    require(source.is_file(), "composition source fixture is missing")
    notebook = load_json(source)
    require(notebook.get("metadata", {}).get("generated", {}).get("generator"), "composition notebook must identify its generator")
    require(all(cell.get("metadata", {}).get("editable") is False for cell in notebook.get("cells", [])), "composition notebook cells must be non-editable")
    source_bytes = source.read_bytes()
    require(source_bytes.count(item["seed_replacement"]["from"].encode()) == 1, "composition seed marker must occur exactly once")
    require(item["required_response_term_groups"] and all(group for group in item["required_response_term_groups"]), "composition response terms must be grouped")


def validate_fixture_seeds() -> None:
    manifest = load_json(CASES_ROOT / "fixture_manifest.json")
    names = {item["fixture"] for item in manifest}
    required = {
        "docs_only",
        "tiny_python_cli",
        "parser_project",
        "scientific_numeric",
        "notebook_tutorial",
        "schema_project",
        "file_locking",
        "release_package",
    }
    require(names == required, "fixture manifest must cover the eight required fixtures")
    for item in manifest:
        source = FIXTURES_ROOT / item["fixture"]
        require((source / "README.md").is_file(), f"{item['fixture']} must identify itself as synthetic")
        require(not (source / ".git").exists(), f"canonical fixture {item['fixture']} must not contain .git")
        with tempfile.TemporaryDirectory(prefix=f"task-grader-{item['fixture']}-") as tmp:
            work = Path(tmp) / item["fixture"]
            shutil.copytree(source, work)
            completed = run(item["check"], work, timeout=30)
            require(
                completed.returncode == item["expected_baseline_exit"],
                f"{item['fixture']} seed check returned {completed.returncode}, expected {item['expected_baseline_exit']}",
            )


def sample_contract(tier: str, overrides: list[str] | None = None) -> dict[str, Any]:
    return {
        "tier": tier,
        "tier_name": TIER_NAMES[tier],
        "risk_overrides": overrides or [],
        "reasons": ["synthetic test"],
        "inspection_budget": ["target"],
        "patch_budget": {"expected_scope": "bounded", "file_guidance": "target only"},
        "abstraction_budget": "none",
        "validation_floor": ["focused regression"],
        "validation_ceiling": ["affected tests"],
        "documentation_budget": "affected docs only",
        "review_requirement": "focused diff",
        "subagent_policy": "none",
        "commit_strategy": "one commit if requested",
        "stop_condition": "Stop when acceptance passes.",
        "escalation_triggers": ["new persistent-data risk"],
    }


def validate_internal_scoring() -> None:
    require(not validate_contract(sample_contract("T1")), "valid sample contract failed schema validation")
    invalid = sample_contract("T1")
    invalid["extra"] = True
    require(validate_contract(invalid), "extra contract key was not rejected")
    invalid_override = sample_contract("T1", ["invented-category"])
    require(validate_contract(invalid_override), "unknown override was not rejected")
    for override in ALLOWED_RISK_OVERRIDES:
        require(
            not validate_contract(sample_contract("T1", [override])),
            f"allowed override was rejected: {override}",
        )
    empty_field = sample_contract("T1")
    empty_field["review_requirement"] = ""
    require(validate_contract(empty_field), "empty required string was not rejected")
    empty_list = sample_contract("T1")
    empty_list["reasons"] = []
    require(validate_contract(empty_list), "empty required list was not rejected")
    non_actionable_stop = sample_contract("T1")
    non_actionable_stop["stop_condition"] = "Acceptance passes."
    require(validate_contract(non_actionable_stop), "non-actionable stop condition was not rejected")
    alternate_stop = sample_contract("T4")
    alternate_stop["stop_condition"] = "Complete only when every required gate passes."
    require(not validate_contract(alternate_stop), "actionable completion condition was rejected")
    cases = load_json(CASES_ROOT / "grading_cases.json")
    synthetic_results = []
    for case in cases:
        contract = sample_contract(case["expected_tier"], case["expected_risk_overrides"])
        synthetic_results.append({"case": case, "score": score_contract(case, contract)})
    summary = summarize_grading(synthetic_results)
    require(summary["agreement_gate_passed"], "perfect synthetic grading did not pass the agreement gate")
    require(summary["hard_gates_passed"], "perfect synthetic grading did not pass hard gates")
    t4_case = next(case for case in cases if case["expected_tier"] == "T4")
    undergraded = {"case": t4_case, "score": score_contract(t4_case, sample_contract("T3"))}
    require(not summarize_grading([undergraded])["hard_gates_passed"], "T4 undergrade did not fail hard gate")
    t3_case = next(case for case in cases if case["expected_tier"] == "T3" and case["required_hard_trigger"])
    undergraded = {"case": t3_case, "score": score_contract(t3_case, sample_contract("T2"))}
    require(not summarize_grading([undergraded])["hard_gates_passed"], "T3 hard-trigger undergrade did not fail hard gate")
    low_risk_case = next(case for case in cases if case["expected_tier"] == "T1")
    overbroad = sample_contract("T1")
    overbroad["validation_ceiling"] = ["Run the full repository suite and clean-room install."]
    require(not score_contract(low_risk_case, overbroad)["semantic_ok"], "release-grade T1 ceiling was not rejected")
    proportional = sample_contract("T1")
    proportional["validation_ceiling"] = ["Run the focused regression; do not run the full repository suite."]
    require(score_contract(low_risk_case, proportional)["semantic_ok"], "negated broad validation limit was rejected")
    adjacent_case = next(
        case
        for case in cases
        if case["expected_risk_overrides"] and case["acceptable_adjacent_tier"]
    )
    adjacent = sample_contract(adjacent_case["acceptable_adjacent_tier"])
    require(
        score_contract(adjacent_case, adjacent)["overrides_ok"],
        "accepted adjacent tier inherited the expected tier's override",
    )


def validate_all() -> None:
    validate_case_files()
    validate_fixture_seeds()
    validate_internal_scoring()
    print("PASS case schemas and tier distribution")
    print("PASS eight synthetic fixture seeds fail only their intended acceptance gates")
    print("PASS contract vocabulary, non-empty fields, stop conditions, proportional ceilings, scoring, and T3/T4 hard gates")


def commit_disposable_baseline(destination: Path) -> None:
    for command in (
        ["git", "init", "-q"],
        ["git", "config", "user.name", "Synthetic Evaluator"],
        ["git", "config", "user.email", "synthetic@example.invalid"],
        ["git", "add", "."],
        ["git", "commit", "-q", "-m", "synthetic fixture baseline"],
    ):
        completed = run(command, destination)
        if completed.returncode:
            raise RuntimeError(f"failed to initialize disposable fixture: {' '.join(command)}\n{completed.stderr}")
    (destination / ".git" / "info" / "exclude").write_text(".agents/\n.codex/\n", encoding="utf-8")


def init_disposable_repo(source: Path, destination: Path) -> None:
    shutil.copytree(source, destination)
    commit_disposable_baseline(destination)


def install_repo_scoped_skill(work: Path, skill_name: str = "angze-task-grader") -> None:
    sources = {
        "angze-task-grader": SKILL_SOURCE,
        "angze-code-style": CODE_STYLE_SKILL_SOURCE,
    }
    require(skill_name in sources, f"unknown repo-scoped skill: {skill_name}")
    target = work / ".agents" / "skills" / skill_name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(sources[skill_name], target)


def codex_version() -> str:
    completed = run(["codex", "--version"], REPO_ROOT)
    if completed.returncode:
        return "unavailable"
    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    return lines[-1] if lines else "unknown"


def walk_values(value: Any) -> Iterable[tuple[str, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield key, child
            yield from walk_values(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_values(child)


def parse_event_evidence(jsonl: str) -> dict[str, Any]:
    event_types: Counter[str] = Counter()
    commands: list[str] = []
    token_metrics: dict[str, int | float] = {}
    parsed_lines = 0
    for line in jsonl.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        parsed_lines += 1
        event_type = event.get("type")
        if isinstance(event_type, str):
            event_types[event_type] += 1
        for key, value in walk_values(event):
            lowered = key.lower()
            if lowered in {"command", "cmd"} and isinstance(value, str) and value not in commands:
                commands.append(value)
            if "token" in lowered and isinstance(value, (int, float)):
                token_metrics[key] = value
    return {
        "parsed_event_lines": parsed_lines,
        "event_types": dict(sorted(event_types.items())),
        "commands": commands,
        "token_metrics": token_metrics or None,
        "skill_event_evidence": "angze-task-grader" in jsonl.lower() and "skill" in jsonl.lower(),
    }


def run_codex(
    work: Path,
    prompt: str,
    output_dir: Path,
    label: str,
    *,
    model: str | None,
    output_contract: bool,
    timeout: int,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    last_message = output_dir / f"{label}.final.txt"
    events_path = output_dir / f"{label}.events.jsonl"
    stderr_path = output_dir / f"{label}.stderr.txt"
    command = [
        "codex",
        "exec",
        "--ephemeral",
        "--json",
        "--color",
        "never",
        "--approve-for-me",
        "-C",
        str(work),
        "--output-last-message",
        str(last_message),
    ]
    if model:
        command.extend(["--model", model])
    if output_contract:
        schema_path = output_dir / "execution-contract.schema.json"
        write_json(schema_path, output_schema())
        command.extend(["--output-schema", str(schema_path)])
    command.append(prompt)
    started_at = utc_now()
    start = time.monotonic()
    try:
        completed = run(command, work, timeout=timeout)
        timed_out = False
    except subprocess.TimeoutExpired as error:
        completed = subprocess.CompletedProcess(command, 124, error.stdout or "", error.stderr or "timed out")
        timed_out = True
    wall_seconds = round(time.monotonic() - start, 3)
    stdout = completed.stdout or ""
    stderr = completed.stderr or ""
    events_path.write_text(stdout, encoding="utf-8")
    stderr_path.write_text(stderr, encoding="utf-8")
    final = last_message.read_text(encoding="utf-8") if last_message.exists() else ""
    evidence = parse_event_evidence(stdout)
    return {
        "label": label,
        "command": command[:-1] + ["<prompt>"],
        "model": model or "inherited",
        "reasoning_effort": "inherited",
        "speed_mode": "inherited",
        "sandbox": "workspace-write via --approve-for-me",
        "approval_policy": "automatic review via --approve-for-me",
        "codex_version": codex_version(),
        "started_at": started_at,
        "ended_at": utc_now(),
        "wall_seconds": wall_seconds,
        "exit_status": completed.returncode,
        "timed_out": timed_out,
        "final_response": final,
        "event_evidence": evidence,
        "stderr": stderr,
    }


def selected_cases(path: Path, requested: list[str]) -> list[dict[str, Any]]:
    cases = load_json(path)
    if not requested or "all" in requested:
        return cases
    by_id = {item["case_id"]: item for item in cases}
    missing = sorted(set(requested) - set(by_id))
    require(not missing, f"unknown case IDs: {missing}")
    return [by_id[case_id] for case_id in requested]


def grade_cases(args: argparse.Namespace) -> int:
    cases = selected_cases(CASES_ROOT / "grading_cases.json", args.case)
    run_dir = RESULTS_ROOT / f"grading-{timestamp()}"
    results = []
    for repeat in range(1, args.repeats + 1):
        for case in cases:
            label = f"{case['case_id']}-r{repeat}"
            print(f"RUN {label}", flush=True)
            with tempfile.TemporaryDirectory(prefix="task-grader-grade-") as tmp:
                work = Path(tmp) / "fixture"
                init_disposable_repo(FIXTURES_ROOT / case["fixture"], work)
                install_repo_scoped_skill(work)
                prompt = (
                    "Use $angze-task-grader.\n"
                    "TASK-GRADER EVAL MODE\n"
                    f"Synthetic fixture context: {case['fixture_context_summary']}\n"
                    f"Task to grade: {case['task_prompt']}"
                )
                result = run_codex(
                    work,
                    prompt,
                    run_dir,
                    label,
                    model=args.model,
                    output_contract=True,
                    timeout=args.timeout,
                )
                status = run(["git", "status", "--short"], work)
                result["worktree_changed"] = bool(status.stdout.strip())
                result["case"] = case
                try:
                    contract = json.loads(result["final_response"])
                    result["contract"] = contract
                    result["score"] = score_contract(case, contract)
                except json.JSONDecodeError as error:
                    result["score"] = {
                        "schema_ok": False,
                        "schema_errors": [f"final response is not valid JSON: {error}"],
                        "tier_ok": False,
                        "actual_tier": None,
                        "overrides_ok": False,
                        "forbidden_undergrade": False,
                        "accepted": False,
                    }
                if result["worktree_changed"]:
                    result["score"]["accepted"] = False
                    result["score"]["schema_errors"].append("evaluation mode modified the worktree")
                results.append(result)
    summary = summarize_grading(results)
    payload = {"kind": "grading", "generated_at": utc_now(), "summary": summary, "results": results}
    write_json(run_dir / "summary.json", payload)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["agreement_gate_passed"] and summary["hard_gates_passed"] else 1


def routing_fixture(prompt: str) -> str:
    lowered = prompt.lower()
    if "release" in lowered:
        return "release_package"
    if "schema" in lowered or "migration" in lowered:
        return "schema_project"
    if "notebook" in lowered:
        return "notebook_tutorial"
    if "scientific" in lowered or "orca" in lowered or "cp2k" in lowered:
        return "scientific_numeric"
    if "parser" in lowered:
        return "parser_project"
    if "cli" in lowered or "ci" in lowered:
        return "tiny_python_cli"
    return "docs_only"


def route_cases(args: argparse.Namespace) -> int:
    cases = selected_cases(CASES_ROOT / "routing_cases.json", args.case)
    run_dir = RESULTS_ROOT / f"routing-{timestamp()}"
    results = []
    for case in cases:
        print(f"RUN {case['case_id']}", flush=True)
        with tempfile.TemporaryDirectory(prefix="task-grader-route-") as tmp:
            work = Path(tmp) / "fixture"
            init_disposable_repo(FIXTURES_ROOT / routing_fixture(case["prompt"]), work)
            install_repo_scoped_skill(work)
            result = run_codex(
                work,
                case["prompt"],
                run_dir,
                case["case_id"],
                model=args.model,
                output_contract=False,
                timeout=args.timeout,
            )
            direct = any(
                ".agents/skills/angze-task-grader/SKILL.md" in command
                for command in result["event_evidence"]["commands"]
            )
            result["case"] = case
            result["observed_triggered"] = direct
            result["outcome_correct"] = direct is case["should_trigger"]
            result["routing_evidence"] = (
                "direct skill-file read in Codex JSON command evidence"
                if direct
                else "no task-grader skill-file read observed in Codex JSON command evidence"
            )
            results.append(result)
    positives = [item for item in results if item["case"]["should_trigger"]]
    negatives = [item for item in results if not item["case"]["should_trigger"]]
    summary = {
        "cases": len(results),
        "positive_cases": len(positives),
        "negative_cases": len(negatives),
        "positive_outcomes": sum(item["outcome_correct"] for item in positives),
        "negative_outcomes": sum(item["outcome_correct"] for item in negatives),
        "false_negatives": [item["case"]["case_id"] for item in positives if not item["observed_triggered"]],
        "false_positives": [item["case"]["case_id"] for item in negatives if item["observed_triggered"]],
        "observed_correct": sum(item["outcome_correct"] for item in results),
        "observation_method": "presence or absence of a task-grader SKILL.md read in emitted Codex JSON commands",
        "limitation": "This measures observed skill-file reads in the current Codex event stream, not general production routing performance.",
    }
    write_json(run_dir / "summary.json", {"kind": "routing", "generated_at": utc_now(), "summary": summary, "results": results})
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


def init_composition_repo(case: dict[str, Any], destination: Path) -> bytes:
    source = CODE_STYLE_FIXTURES_ROOT / case["source_fixture"]
    destination.mkdir(parents=True)
    target = destination / case["target_path"]
    target.parent.mkdir(parents=True, exist_ok=True)
    source_bytes = source.read_bytes()
    old = case["seed_replacement"]["from"].encode()
    new = case["seed_replacement"]["to"].encode()
    require(source_bytes.count(old) == 1, "composition seed marker must occur exactly once")
    protected_bytes = source_bytes.replace(old, new, 1)
    target.write_bytes(protected_bytes)
    commit_disposable_baseline(destination)
    return protected_bytes


def composition_cases(args: argparse.Namespace) -> int:
    cases = selected_cases(CASES_ROOT / "composition_cases.json", args.case)
    require(len(cases) == 1, "composition execution must run the one canonical case")
    run_dir = RESULTS_ROOT / f"composition-{timestamp()}"
    results = []
    for case in cases:
        print(f"RUN {case['case_id']}", flush=True)
        with tempfile.TemporaryDirectory(prefix="task-grader-compose-") as tmp:
            work = Path(tmp) / "fixture"
            protected_bytes = init_composition_repo(case, work)
            install_repo_scoped_skill(work, "angze-task-grader")
            install_repo_scoped_skill(work, "angze-code-style")
            prompt = (
                "Use both $angze-task-grader and $angze-code-style.\n"
                "This is a synthetic dual-skill composition evaluation. State whether the task-grader "
                "classifies the requested correction as T0 or T1, but do not compare or translate the "
                "two skills' numeric tier systems. Apply both skills' constraints.\n"
                f"Task: {case['task_prompt']}"
            )
            result = run_codex(
                work,
                prompt,
                run_dir,
                case["case_id"],
                model=args.model,
                output_contract=False,
                timeout=args.timeout,
            )
            target = work / case["target_path"]
            response = result["final_response"]
            response_lower = response.lower()
            term_groups_ok = all(
                any(term.lower() in response_lower for term in group)
                for group in case["required_response_term_groups"]
            )
            tier_evidence = [
                tier
                for tier in case["expected_task_tiers"]
                if re.search(rf"\b{tier}\b", response, re.IGNORECASE)
            ]
            comparisons = TIER_COMPARISON_PATTERN.findall(response)
            files = changed_files(work)
            protected_unchanged = target.is_file() and target.read_bytes() == protected_bytes
            accepted = (
                result["exit_status"] == 0
                and not files
                and protected_unchanged
                and bool(tier_evidence)
                and term_groups_ok
                and not comparisons
            )
            result["case"] = case
            result["composition_score"] = {
                "accepted": accepted,
                "worktree_changed": bool(files),
                "changed_files": files,
                "protected_artifact_unchanged": protected_unchanged,
                "task_tier_evidence": tier_evidence,
                "preservation_constraint_evidence": term_groups_ok,
                "tier_comparisons": comparisons,
            }
            results.append(result)
    summary = {
        "cases": len(results),
        "accepted_cases": sum(item["composition_score"]["accepted"] for item in results),
        "protected_artifacts_unchanged": sum(
            item["composition_score"]["protected_artifact_unchanged"] for item in results
        ),
        "tier_comparison_failures": sum(
            bool(item["composition_score"]["tier_comparisons"]) for item in results
        ),
    }
    write_json(
        run_dir / "summary.json",
        {"kind": "composition", "generated_at": utc_now(), "summary": summary, "results": results},
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["accepted_cases"] == len(results) else 1


def changed_files(work: Path) -> list[str]:
    completed = run(["git", "status", "--porcelain", "-z"], work)
    paths: list[str] = []
    chunks = completed.stdout.split("\0")
    for chunk in chunks:
        if not chunk:
            continue
        path = chunk[3:] if len(chunk) > 3 else chunk
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if not path.startswith((".agents/", ".codex/")):
            paths.append(path)
    return sorted(set(paths))


def diff_metrics(diff: str) -> dict[str, int]:
    added = 0
    removed = 0
    for line in diff.splitlines():
        if line.startswith("+++") or line.startswith("---"):
            continue
        if line.startswith("+"):
            added += 1
        elif line.startswith("-"):
            removed += 1
    return {"lines_added": added, "lines_removed": removed}


def command_metrics(commands: list[str]) -> dict[str, Any]:
    normalized = [re.sub(r"\s+", " ", command.strip()) for command in commands]
    counts = Counter(normalized)
    broad_patterns = ("check_all_skills", "pytest", "tox", "nox", "build", "pip install")
    skill_loads = [command for command in normalized if ".agents/skills/angze-task-grader/" in command]
    task_commands = [command for command in normalized if command not in skill_loads]
    validation_commands = []
    validation_operation_count = 0
    for command in task_commands:
        operations = 0
        if "unittest" in command or "pytest" in command:
            operations += 1
        if "compile(" in command or "compileall" in command or "py_compile" in command:
            operations += 1
        if "diff --check" in command:
            operations += 1
        if re.search(r"git diff -- (?!check)", command):
            operations += 1
        if re.search(r"(?:^|[ /])check\.py(?:[ '\"]|$)", command):
            operations += 1
        if operations:
            validation_commands.append(command)
            validation_operation_count += operations
    return {
        "command_count": len(normalized),
        "skill_load_command_count": len(skill_loads),
        "task_command_count": len(task_commands),
        "validation_command_count": validation_operation_count,
        "validation_commands": validation_commands,
        "repeated_commands": sorted(command for command, count in counts.items() if count > 1),
        "potentially_broad_validation": [command for command in normalized if any(pattern in command for pattern in broad_patterns)],
    }


def collect_arm_state(work: Path, case: dict[str, Any]) -> dict[str, Any]:
    diff = run(["git", "diff", "--no-ext-diff", "--binary", "HEAD"], work).stdout
    files = changed_files(work)
    acceptance = run(case["acceptance_command"], work, timeout=120)
    allowed = set(case["allowed_paths"])
    return {
        "files_changed": files,
        "changed_file_count": len(files),
        "unrelated_files": sorted(set(files) - allowed),
        "diff": diff,
        "diff_metrics": diff_metrics(diff),
        "acceptance": {
            "command": case["acceptance_command"],
            "exit_status": acceptance.returncode,
            "passed": acceptance.returncode == 0,
            "stdout": acceptance.stdout,
            "stderr": acceptance.stderr,
        },
    }


def smoke_ab(args: argparse.Namespace) -> int:
    cases = selected_cases(CASES_ROOT / "implementation_cases.json", args.case)
    require(len(cases) <= 6, "smoke A/B is limited to six cases")
    run_dir = RESULTS_ROOT / f"smoke-ab-{timestamp()}"
    results = []
    for case in cases:
        for arm in ("baseline", "treatment"):
            label = f"{case['case_id']}-{arm}"
            print(f"RUN {label}", flush=True)
            with tempfile.TemporaryDirectory(prefix="task-grader-ab-") as tmp:
                work = Path(tmp) / "fixture"
                init_disposable_repo(FIXTURES_ROOT / case["fixture"], work)
                prompt = case["task_prompt"]
                if arm == "treatment":
                    install_repo_scoped_skill(work)
                    prompt = f"Use $angze-task-grader.\n{prompt}"
                result = run_codex(
                    work,
                    prompt,
                    run_dir,
                    label,
                    model=args.model,
                    output_contract=False,
                    timeout=args.timeout,
                )
                result["case"] = case
                result["arm"] = arm
                result["state"] = collect_arm_state(work, case)
                result["command_metrics"] = command_metrics(result["event_evidence"]["commands"])
                results.append(result)
    comparisons = []
    for case in cases:
        by_arm = {item["arm"]: item for item in results if item["case"]["case_id"] == case["case_id"]}
        baseline = by_arm["baseline"]
        treatment = by_arm["treatment"]
        comparisons.append(
            {
                "case_id": case["case_id"],
                "both_correct": baseline["state"]["acceptance"]["passed"] and treatment["state"]["acceptance"]["passed"],
                "treatment_correctness_regression": baseline["state"]["acceptance"]["passed"] and not treatment["state"]["acceptance"]["passed"],
                "unrelated_file_delta": len(treatment["state"]["unrelated_files"]) - len(baseline["state"]["unrelated_files"]),
                "changed_file_delta": treatment["state"]["changed_file_count"] - baseline["state"]["changed_file_count"],
                "validation_command_delta": treatment["command_metrics"]["validation_command_count"] - baseline["command_metrics"]["validation_command_count"],
                "task_command_delta": treatment["command_metrics"]["task_command_count"] - baseline["command_metrics"]["task_command_count"],
                "human_review_required": True,
            }
        )
    summary = {
        "cases": len(cases),
        "arms": len(results),
        "correctness_regressions": sum(item["treatment_correctness_regression"] for item in comparisons),
        "increased_unrelated_files": sum(item["unrelated_file_delta"] > 0 for item in comparisons),
        "token_savings_claimed": False,
        "human_review_required": True,
    }
    write_json(
        run_dir / "summary.json",
        {"kind": "smoke-ab", "generated_at": utc_now(), "summary": summary, "comparisons": comparisons, "results": results},
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["correctness_regressions"] == 0 and summary["increased_unrelated_files"] == 0 else 1


def score_saved(args: argparse.Namespace) -> int:
    payload = load_json(Path(args.result))
    require(payload.get("kind") == "grading", "score accepts a grading summary.json")
    current_cases = {
        case["case_id"]: case for case in load_json(CASES_ROOT / "grading_cases.json")
    }
    rescored = []
    for item in payload["results"]:
        case_id = item["case"]["case_id"]
        require(case_id in current_cases, f"saved result references unknown case {case_id}")
        case = current_cases[case_id]
        contract = item.get("contract", {})
        rescored.append({"case": case, "score": score_contract(case, contract)})
    summary = summarize_grading(rescored)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["agreement_gate_passed"] and summary["hard_gates_passed"] else 1


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    subparsers = root.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate", help="run deterministic case, fixture, schema, and scoring checks")

    for name, help_text in (
        ("grade", "run controlled evaluation-mode grading cases"),
        ("route", "run separate implicit-routing probes"),
        ("composition", "run the canonical dual-skill preservation case"),
        ("smoke-ab", "run bounded synthetic behavioral A/B arms"),
    ):
        command = subparsers.add_parser(name, help=help_text)
        command.add_argument("--case", action="append", default=[], help="case ID; repeat or use all")
        command.add_argument("--model", help="optional model passed through the supported --model flag")
        command.add_argument("--timeout", type=int, default=900, help="per Codex invocation timeout in seconds")
        if name == "grade":
            command.add_argument("--repeats", type=int, default=1, choices=range(1, 4))

    score = subparsers.add_parser("score", help="rescore a saved grading summary")
    score.add_argument("result")
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "validate":
            validate_all()
            return 0
        if args.command == "grade":
            return grade_cases(args)
        if args.command == "route":
            return route_cases(args)
        if args.command == "composition":
            return composition_cases(args)
        if args.command == "smoke-ab":
            return smoke_ab(args)
        if args.command == "score":
            return score_saved(args)
    except (ValueError, RuntimeError) as error:
        print(f"ERROR {error}")
        return 1
    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())
