# scientific-code-documenter v0.2.0

This experimental release candidate expands validated language coverage for the scientific code readability and documentation skill. It adds controlled Shell, LaTeX, HTML, CSS, and JavaScript evidence while keeping the accepted v0.1.0 runtime byte-identical.

Accepted runtime snapshot SHA-256: `3a58a55702bde8061fb3db226173da80e6f0336049ca679e4a70eb312069312e`

Deterministic manifest SHA-256: `c55d3a7cb122b2b253f0d7c56edef349b13c75fdd08ffef1abd53f9563e79c4e`

## Capabilities

- Review scientific and technical source without editing it.
- Improve source structure, comments, docstrings, and maintainability while preserving behavior.
- Document evidence-supported units, shapes, conventions, assumptions, interfaces, and numerical choices.
- Preserve Shell workflow and exit semantics, LaTeX rendered and template contracts, and HTML DOM and export contracts.
- Recognize fragile or generated files, keep them unchanged, and direct improvements to their owning source or generator.
- Refuse to turn plausible but unsupported scientific interpretations into documentation.

## Installation

From the collection checkout:

```sh
./scripts/install_skill.sh scientific-code-documenter --dry-run
./scripts/install_skill.sh scientific-code-documenter
```

The installer links only `skills/scientific-code-documenter/` into the per-user skills directory.

## Explicit and implicit usage

Explicit review-only invocation:

```text
$scientific-code-documenter
Review this file for readability and documentation accuracy. Do not modify it.
```

Explicit focused editing invocation:

```text
$scientific-code-documenter
Improve the readability and documentation of this source while preserving calculations, interfaces, parameters, rendered content, file formats, and externally consumed ordering.
```

Codex may select the skill implicitly for clearly scoped documentation or readability work in Python, Shell, LaTeX, HTML, CSS, JavaScript, and related technical sources. Ordinary debugging, compilation, deployment, dependency, feature, security, or test-execution requests should not load it merely because source code is involved.

## Validation overview

- New six-fixture controlled A/B: 159/162 with the skill versus 145/162 baseline; four wins, two ties, and no losses.
- All 12 candidates passed independent syntax or behavior contracts.
- Every skill behavior-preservation and restraint score was 3/3; all three review-only fixtures remained byte-identical.
- Shell coverage preserved exit codes, aggregate failure, deterministic order, manifests, hashes, cleanup, ORCA directives and parameters, and strict-mode restraint.
- LaTeX coverage preserved two-pass builds, page counts, normalized visible text, labels and references, macros and values, table order, conditional appendix behavior, and template workarounds.
- HTML coverage preserved parsing, accessible labels and live regions, DOM IDs, raw data and SVG order, scaling and formatting, public exports, exact CSV bytes, reset/filter behavior, and generated snapshots.
- Cross-language triggers: explicit 3/3, positive implicit 9/9, negative false triggers 0/6, and boundaries 6/6 with zero edits.
- Retained scientific Python evidence: five-fixture A/B at 112/120 versus 94/120 and authorized real-repository acceptance with behavior-preserving selected edits.

See the [sanitized v0.2.0 evaluation summary](../evaluations/scientific-code-documenter-v0.2.0.md) for methodology, per-fixture scores, category averages, and limitations.

## Compatibility with v0.1.0

The runtime files and their modes are unchanged from v0.1.0. v0.2.0 adds fixtures, deterministic contracts, trigger prompts, and release evidence only. No runtime behavior, invocation syntax, installation path, or public skill packaging changed.

## Limitations

- The release remains experimental and does not guarantee scientific correctness.
- Scientific Python is the only language with completed real-repository acceptance.
- Shell, LaTeX, HTML, CSS, and JavaScript validation is synthetic and contract-based.
- LaTeX validation compares normalized visible text, labels, structure, and page counts rather than byte-identical PDFs.
- HTML behavior uses the available dependency-free local DOM harness rather than a complete browser matrix.
- Human scientific and maintainer review is required before merging edits.
