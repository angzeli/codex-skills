# angze-task-grader evaluation

This suite evaluates `angze-task-grader` only on tiny synthetic repositories. It never installs the skill globally and never targets active or private work.

## What is covered

- `cases/grading_cases.json`: 25 controlled `TASK-GRADER EVAL MODE` cases across T0-T4.
- `cases/routing_cases.json`: positive and negative implicit-invocation prompts.
- `cases/composition_cases.json`: one dual-skill generated-notebook preservation case.
- `cases/implementation_cases.json`: six bounded implementation cases for A/B comparison.
- `fixtures/`: public-safe seeded repositories with lightweight acceptance checks.
- `harness/eval.py`: one standard-library entry point for deterministic validation, grading runs, routing probes, behavioral A/B smoke runs, and summary scoring.

Generated JSONL, diffs, final messages, and machine-readable summaries go under `results/`, which is ignored. Committed reports contain only portable summaries.

## Deterministic checks

From the collection root:

```sh
./scripts/run_fixture_checks.sh angze-task-grader
```

Or run the harness directly:

```sh
python3 evals/angze-task-grader/harness/eval.py validate
```

Validation checks case schemas and tier counts, fixture safety and expected seeded failures, allowed override vocabulary, non-empty contract fields, actionable stop conditions, low-risk validation ceilings, score calculations, T3/T4 hard gates, and deterministic composition-fixture assumptions. Seeded fixture acceptance commands are expected to fail before an agent applies the requested fix.

## Model-backed grading

The grading runner makes a disposable copy of a synthetic fixture for every case, initializes a local Git repository, installs the skill only at `.agents/skills/angze-task-grader`, and invokes `codex exec` with the exact controlled trigger.

```sh
python3 evals/angze-task-grader/harness/eval.py grade --case all
```

Use `--model` only when pinning a supported model is necessary. The harness otherwise inherits the current model, reasoning effort, speed mode, sandbox, and authentication, and records those values as inherited when the event stream does not expose them.

## Behavioral A/B smoke

Run only the bounded six-case maximum unless the user explicitly authorizes a larger matrix:

```sh
python3 evals/angze-task-grader/harness/eval.py smoke-ab --case docs-typo --case cli-zero --case scientific-units --case parser-summary
```

Each arm starts from a fresh fixture copy and identical committed bytes. The baseline has no task-grader skill. The treatment receives the same task text plus explicit `$angze-task-grader` invocation and a repo-scoped skill copy. Results record available event evidence, commands, status, diff, changed files, acceptance results, and timing. Token metrics are recorded only if emitted by Codex.

## Implicit routing

```sh
python3 evals/angze-task-grader/harness/eval.py route --case all
```

The routing runner omits explicit invocation. It records a task-grader `SKILL.md` read in emitted Codex JSON commands as direct activation evidence and records when no such read is observed. This event-stream observation does not establish general production routing performance.

## Dual-skill composition

```sh
python3 evals/angze-task-grader/harness/eval.py composition --case all
```

The composition runner installs repo-scoped copies of both `angze-task-grader` and `angze-code-style` in a disposable repository. The one canonical case asks for a mechanically small correction to a generated, non-editable synthetic notebook whose upstream generator is unavailable. Passing requires a T0/T1 task-grade observation, no worktree change, byte-identical preservation, an explicit preservation/editability explanation, and no comparison or translation of the two skills' numeric tiers.

Synthetic evaluation establishes controlled behavioral evidence, not proof of performance on every real repository.
