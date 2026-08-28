# Jupyter Notebook handling

Use this reference before editing or reviewing an `.ipynb` file.

## Classify notebook role

- `source`: maintained input to the analysis workflow.
- `tutorial`: intentionally explanatory and usually editable within its teaching contract.
- `analysis artifact`: committed state or results whose stored outputs may be evidentiary.
- `generated`: produced by a pipeline, exporter, benchmark, or cache; normally review only.
- `unknown`: insufficient repository evidence; default to review only.

Repository documentation, generators, build rules, paths, headers, and version-control policy are stronger evidence than the mere fact that a notebook is committed.

## Protected fields

Preserve by default:

- `nbformat` and `nbformat_minor`;
- notebook metadata;
- cell count, order, IDs, types, and metadata;
- execution counts and code-cell outputs;
- Markdown attachments;
- untouched cell source;
- source representation, JSON formatting, key order, Unicode escaping, and trailing-newline behavior where the editing mechanism permits.

Unexpected changes are hard failures. Do not waive them because the notebook still opens.

## Choose documentation location

- Use existing Markdown for workflow purpose, scientific context shared by several cells, and state dependencies visible to readers.
- Use code comments for a local numerical convention, ordering constraint, or implementation safeguard.
- Avoid repeating the same explanation in adjacent Markdown and code.
- Prune narration that merely restates the next statement.

## Hidden state and stale outputs

Report reliance on prior-cell namespace, mutable globals, working directories, files, environment variables, random state, package versions, display hooks, or services. Do not silently reorder or merge cells to remove the dependency.

When source is edited without execution, preserve outputs and execution counts. Disclose that the notebook was not executed and that displayed outputs were not recomputed from the modified source.

## Serialization locality

Use a structure-aware, locality-preserving editing mechanism. A small source edit should have a small diff. If a tool would normalize the whole JSON document, metadata, source arrays, or escaping, stop and report the limitation.

Validate both:

1. semantic structural preservation; and
2. textual diff locality.

## Generated and review-only notebooks

Do not edit a generated, cached, benchmark, result, publication, or unknown-role notebook without explicit source-edit authorization and a protection plan. Report the finding and direct changes to the authoritative source or generator when known.

## Behavioral probes

Do not execute the original notebook by default. Repository-designed fixture code may be extracted and run in an isolated deterministic probe to compare limited numerical, ordering, missing-value, or serialization behavior. Describe this accurately as additional fixture evidence, never as general notebook equivalence.
