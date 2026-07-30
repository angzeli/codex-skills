# scientific-code-documenter v0.3.0 validation

## Version status

- Version: `scientific-code-documenter` v0.3.0
- Release status: experimental release candidate
- Accepted runtime snapshot SHA-256: `3a58a55702bde8061fb3db226173da80e6f0336049ca679e4a70eb312069312e`
- Deterministic manifest SHA-256: `c55d3a7cb122b2b253f0d7c56edef349b13c75fdd08ffef1abd53f9563e79c4e`
- Runtime change from v0.2.0: none

v0.3.0 expands real-repository validation evidence without changing the v0.2.0 runtime. The tagged v0.2.0 runtime, live runtime, and immutable acceptance snapshot are byte-identical.

## Real ORCA Shell repository

Acceptance used a frozen, remote-free snapshot of an authorized production-style ORCA calculation repository. Nine relevant Shell scripts totaling 4,319 lines were reviewed. The selected scripts represented:

- `run_ground_states.sh` (801 lines): multi-stage ground-state orchestration, generated optimization/frequency/single-point inputs, watchdogs, retries, and resume behavior;
- `dimer_workflow_common.sh` (733 lines): sourced workflow helpers, provenance-aware checkpoints, failure classification, archival, and process-count fallback;
- `generate_esp_cubes.sh` (497 lines): parallel density/electrostatic-potential cube post-processing, staged publication, cleanup, and aggregate failure.

A fresh skill-enabled review inspected all nine scripts and produced twelve prioritized findings while changing zero tracked or untracked files. Facts, uncertain interpretations, and changes requiring scientific approval remained distinct.

No real ORCA, `orca_plot`, Multiwfn, scheduler, or expensive scientific calculation was launched. Validation used syntax checks, missing-executable preflight probes, source-only helper probes, and isolated deterministic mocks.

A pre-existing calculation continued advancing ignored checkpoints in the live repository while evidence was captured. The activity began before the evaluation and was recorded separately: branch, HEAD, remotes, tracked, staged, unstaged, and untracked source state remained unchanged, as did the immutable evaluated inputs. Because candidate sessions used frozen snapshots and never wrote to the live source tree, the external activity did not affect acceptance validity.

## A/B results

Each pair started from the same detached neutral commit. Baseline sessions exposed zero user skills; skill sessions exposed exactly the immutable `scientific-code-documenter` snapshot and recorded its `SKILL.md` read. Prompt bodies, model, reasoning effort, CLI, sandbox, repository context, and independent validation were otherwise identical. A zero-skill blind judge scored anonymous candidates from complete scripts, diffs, context, and contract outputs.

| Script | Baseline | Skill | Outcome | Baseline diff | Skill diff |
| --- | ---: | ---: | --- | ---: | ---: |
| `run_ground_states.sh` | 27/30 | 29/30 | Skill win | +92/-92 | +96/-55 |
| `dimer_workflow_common.sh` | 26/30 | 30/30 | Skill win | +73/-73 | +42/-42 |
| `generate_esp_cubes.sh` | 27/30 | 30/30 | Skill win | +71/-71 | +45/-45 |
| **Total** | **80/90** | **89/90** | **3 wins, 0 ties, 0 losses** |  |  |

All six candidates passed `bash -n`, target-only scope checks, and independent dynamic equivalence. ShellCheck was unavailable. The skill candidates were all judged proportionate, operationally safe, scientifically accurate, and reasonably approvable.

The ground-state harness compared generated optimization, frequency, and single-point ORCA inputs; success, resume, invalid-argument, and frequency-failure behavior; traces; exit codes; output trees; and scratch cleanup. The helper harness compared sourcing errors, success and checkpoint reuse, process-count fallback, scientific-failure classification, generated input, traces, archival, logs, and outputs. The cube harness compared three-system command traces, worker limits, successful publication, rerun skips, one-job failure aggregation, filenames, output hashes, and scratch cleanup.

Thus the tested functional, basis, solvent, charge, multiplicity, PAL/process, `%maxcore`, SCF, optimization, frequency, and cube/property directives remained unchanged. CLI and environment variables, command order, parallelism, failure semantics, restart behavior, traps, cleanup, logging, filenames, stdout, stderr, exit codes, and output structures also remained equivalent.

## Aggregate result

| Category average | Baseline | Skill |
| --- | ---: | ---: |
| Readability | 2.00 | 3.00 |
| Function and section documentation | 3.00 | 3.00 |
| Scientific-context accuracy | 3.00 | 3.00 |
| Comment quality | 2.00 | 3.00 |
| Behavior and output preservation | 3.00 | 3.00 |
| Scope discipline | 3.00 | 3.00 |
| Shell convention adherence | 3.00 | 3.00 |
| Scientific and operational restraint | 2.67 | 3.00 |
| Maintainability and refactoring quality | 2.00 | 2.67 |
| ORCA workflow reproducibility | 3.00 | 3.00 |

Every skill behavior-preservation score and scientific/operational-restraint score was 3/3. No skill candidate lost through over-refactoring, unsupported interpretation, or Shell-semantic damage.

One skill-enabled ESP attempt was excluded before scoring because its evaluator supplied a relative snapshot symlink, leaving the skill undiscoverable. The failed attempt was preserved, the harness invocation was corrected to an absolute immutable-snapshot path, and the arm was rerun from the neutral commit. The valid rerun recorded exactly one discoverable skill and a `SKILL.md` read.

## Existing evidence retained

The unchanged runtime retains the [v0.2.0 controlled evidence](scientific-code-documenter-v0.2.0.md): a 159/162 skill score versus 145/162 baseline across Shell, LaTeX, and HTML editing/restraint fixtures, complete trigger and boundary gates, and the earlier scientific Python real-repository acceptance. No full Python A/B rerun was required because the runtime and manifest hashes remain identical.

## Limitations

- Real Shell acceptance was performed on one ORCA-oriented source tree.
- No expensive production calculation was launched.
- Mock and dry-run equivalence cannot prove every HPC, MPI, scheduler, cluster, or operating-system interaction.
- ShellCheck was unavailable during this run.
- Human scientific and maintainer review remains required before accepting generated changes.
- The skill remains experimental and does not guarantee correctness in every project.
