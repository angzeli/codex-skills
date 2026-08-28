---
name: scientific-code-documenter
description: Document, prune, refactor, or review scientific code and Jupyter notebooks while preserving scientific, data, interface, execution-state, and artifact contracts. Use for evidence-backed comments, docstrings, notebook Markdown, units, shapes, schemas, ordering, missing-value conventions, assumptions, numerical choices, or readability work that must not change analysis semantics. Do not trigger for ordinary notebook execution, data analysis, debugging, performance work, methodology changes, output regeneration, dependency updates, or feature implementation.
---

# Scientific Code Documenter

Improve scientific and technical code without obscuring its logic or silently changing its behavior. Match the repository's established conventions when they are coherent and intentional.

## Core workflow

1. Inspect before editing.
   - Read applicable `AGENTS.md` files and repository instructions.
   - Inspect the repository structure and the requested files.
   - Find formatting, linting, type-checking, testing, and documentation configuration.
   - Read nearby code to learn naming, layout, docstring, and comment conventions.
   - Identify generated and vendored files that should remain untouched.
   - Check the working tree and preserve unrelated user changes.
   - If a tracked target already has documentation or readability changes, treat them as user or prior-pass work. Do not refine, replace, or stack another pass unless the user explicitly asks to continue from those existing changes.
2. Classify the operating mode and treat review-only or no-edit language as a hard boundary.
3. Build a compact contract inventory for the requested scope. Classify each relevant item as `evidence-backed`, `observable-only`, or `unknown`.
4. For notebooks, classify the artifact role as `source`, `tutorial`, `analysis artifact`, `generated`, or `unknown` before deciding whether an edit is safe.
5. Grade the proposed work from Tier 0 through Tier 3 and perform only the authorized, protectable tier.
6. Define the smallest coherent scope and apply repository-specific conventions before general preferences.
7. Treat documentation that already satisfies the requested contracts as complete. Do not create a diff merely to rephrase, expand, rename local variables, or apply another plausible cleanup.
8. Preserve public interfaces, calculations, numerical behavior, outputs, notebook state, and file formats unless the user explicitly authorizes and protects a change.
9. Run the narrowest relevant validation. Fail closed on unexplained contract changes and report exactly what ran.

### Treat operating mode as a hard boundary

- Before acting, classify the request as editing, review only, explanation only, recommendations only, or planning only. Treat explicit scope and no-edit instructions as overriding all documentation, readability, cleanup, formatting, and refactoring preferences in this skill, including validation that would modify files.
- In any non-editing mode, inspect and report inaccurate, stale, unsupported, or missing documentation; explain its impact and location; and propose concrete replacement wording when useful. Do not apply the replacement, edit, rename, reformat, or restructure source files, or run formatters, fixers, or other commands that modify files. Use read-only validation when useful, and verify that the working tree remains unchanged before finishing.
- Report a stale or dangerous comment as a high-priority issue when warranted, but do not treat its seriousness as authorization to edit.

## Inventory scientific and artifact contracts

Before editing, record only the contract items relevant to the target. Consider scientific meaning, units, shapes, schemas, ordering, missing values, state dependencies, public and filesystem interfaces, expected outputs, stored outputs, notebook structure, and notebook role.

- `evidence-backed`: supported by tests, schemas, types, authoritative code or documentation, or user instructions. Document it precisely.
- `observable-only`: visible in the implementation, but its scientific intent is not established. Describe only the observed operation.
- `unknown`: insufficient evidence exists. Preserve the behavior and request or recommend expert confirmation.

Do not infer a scientific contract from domain familiarity or an arithmetic pattern. Consult [references/scientific-contracts.md](references/scientific-contracts.md) when units, schemas, ordering, missing values, state, or interface boundaries need detailed treatment.

## Grade risk before acting

- **Tier 0 — review/planning only:** make no changes when the request is non-editing, intent is too uncertain, the artifact is generated or unknown, or preservation cannot be verified.
- **Tier 1 — documentation only:** edit comments, docstrings, or Markdown; prune redundant or misleading commentary; document only evidence-backed contracts. Do not change behavior.
- **Tier 2 — local readability refactoring:** refactor only when explicitly requested, locally protectable, and free of Tier-3 effects. Require targeted behavior checks.
- **Tier 3 — protected/high risk:** report by default. This includes numerical evaluation order, public interfaces, notebook structure or identity, execution state, stored outputs, metadata, and artifact contracts. Edit only with explicit authorization and suitable protection.

Label Tier-3 findings with one or more reasons: `numerical-semantics`, `public-interface`, `notebook-structure`, `execution-state`, `stored-output`, `metadata`, or `artifact-contract`.

For review findings, report: location, issue, evidence, contract affected, confidence, behavior risk, proposed wording or action, and required expert confirmation. Separate established facts from inference.

## Adapt to the task

### Write new code

- Structure new code for scanning and maintenance from the start.
- Separate validation, computation, presentation, and persistence when practical.
- Document non-trivial functions and scientifically meaningful decisions.
- Add types, contracts, or schemas when they fit the language and repository.
- Avoid building abstractions that the requested scope does not need.

### Document existing code

- Add documentation without turning the task into a behavioral rewrite.
- Explain purpose, interpretation, assumptions, and non-obvious choices.
- Remove or correct stale, misleading, redundant, and obviously generated-sounding comments when confidence is high.
- Leave suspicious logic unchanged and flag it separately when its intended behavior is uncertain.
- Prefer deleting or consolidating stale, obvious, duplicated, or unsupported commentary over adding another explanation.

### Refactor for readability

- Simplify dense expressions, deep nesting, long functions, or opaque transformations only where understanding materially improves.
- Require a concrete current readability defect before applying a Tier-2 refactor. A broad readability request is not sufficient when the existing implementation and documentation already expose the relevant contracts.
- Use clear intermediate variables and coherent helpers.
- Preserve evaluation order, floating-point behavior, side effects, exception behavior, and data ordering unless change is requested.
- Keep public names stable. Treat symbol renaming and extraction across module boundaries as higher-risk changes.

### Review documentation and style

- Review without editing unless the user asks for fixes.
- Prioritize issues that affect correctness, scientific interpretation, reproducibility, or maintainability.
- Distinguish defects from preferences.
- Cite concrete files and tight line ranges, explain impact, and suggest the smallest remedy.
- State when no actionable issue is found.

## Make repeated invocation stable

Before editing, ask whether the current artifact already meets the request. If its high-value contracts are documented, unsupported meaning remains explicitly unknown, and no stale or redundant commentary remains, make no change and report that the existing documentation is sufficient.

Use the initial working-tree state as a preservation boundary. When the requested tracked file already contains in-scope documentation or readability changes, a generic request to improve that file is not permission to revise those changes. Inspect and validate them read-only, report any remaining concern separately, and leave the file unchanged unless the user explicitly authorizes building on the existing diff. In a controlled second pass, this existing diff is the prior candidate and must remain byte-identical.

Do not use a repeated invocation to:

- add lower-value detail omitted by a focused prior pass;
- rephrase accurate documentation without a demonstrated clarity defect;
- add more comments around already documented behavior;
- rename locals, expand formatting, or perform a new Tier-2 refactor merely because another form is possible;
- alternate between equivalent wording or representation choices.

Make the first accepted edit coherent enough that the same request against its result produces no tracked change. In an evaluation or release workflow, verify this with a fresh second pass and fail the candidate if content or notebook bytes drift.

## Readability rules

- Prefer descriptive names that convey scientific or computational meaning.
- Avoid unexplained abbreviations unless they are conventional in the field.
- Replace meaningful magic numbers with named constants when appropriate; do not alter unusual values without evidence.
- Prefer explicit intermediate values over deeply nested expressions and long transformation chains.
- Keep control flow shallow with early validation or returns when they clarify failure paths.
- Separate major logical stages with blank lines.
- Keep related operations together; do not isolate every trivial statement.
- Avoid dense one-line loops, conditionals, callbacks, and chained operations when they hide intent.
- Break long functions into coherent units only when the boundaries are real and useful.
- Use actionable validation errors rather than allowing obscure downstream failures.
- Avoid expanding code merely to increase line count.

## Documentation hierarchy

### Files and modules

Add a short module description only when the file has a distinct responsibility and the repository style supports it. Explain the role, main inputs and outputs, and important scientific or architectural context. Do not restate the filename.

### Functions, methods, and classes

Document every non-trivial function, method, and class with the language-appropriate convention. Scale detail to importance:

- Use one concise sentence for very small private helpers.
- Give public APIs and scientifically important routines fuller documentation.
- Describe purpose, important inputs, returned values, side effects, and meaningful failure conditions.
- Record units, shapes, dimensionality, axis order, coordinate systems, and value domains when relevant.
- Explain assumptions or conventions that a maintainer cannot infer from the signature.
- Do not mechanically repeat obvious names, types, or return annotations.

### Logical implementation blocks

Add a short comment before a major stage in a multi-stage routine, such as input validation, data cleaning, baseline correction, model construction, optimization, post-processing, plotting, or export. Identify the stage's purpose without narrating its statements.

### Inline comments

Use inline comments sparingly for:

- the reason for a non-obvious implementation;
- a scientific assumption or convention;
- a numerical-stability precaution;
- an indexing, axis, or coordinate convention;
- an unusual edge case or compatibility constraint;
- a deliberate deviation from the obvious approach.

Do not translate syntax into English. Prefer `# Skip the metadata row before reading numerical values.` over `# Increment the index.`

## Preserve scientific meaning

When relevant, make these details explicit near the code they govern:

- physical units and conversion points;
- array, tensor, image, or table shapes and axis order;
- coordinate systems, reference electrodes, sign conventions, and energy references;
- basis sets, computational methods, boundary conditions, and normalization conventions;
- wavelength, frequency, time, spatial, or energy domains;
- whether values are measured or calculated, raw or processed, fitted or simulated, absolute or relative;
- numerical tolerances, convergence criteria, initial guesses, stopping rules, and expected precision;
- exclusions, interpolation, smoothing, uncertainty handling, and random seeds;
- provenance of empirical parameters or constants when a source is already known.

Name scientifically meaningful thresholds when doing so improves interpretation. Explain why a threshold exists when its value is not self-evident. Do not invent citations, provenance, or intent.

Maintain distinctions that affect interpretation, including measured versus calculated values, association versus interaction energies, gas-phase versus solution-phase quantities, and internal versus literature-standard conventions.

## Write comments like a human maintainer

- Use direct, neutral, domain-appropriate sentences.
- Prefer concrete verbs and specific nouns.
- Keep paragraphs short and use consistent tense and punctuation.
- Use concise stage labels only when the repository already favors them.
- Explain why, constraints, or interpretation rather than obvious mechanics.
- Avoid tutorial narration, second-person instructions, decorative banners, and speculative claims.
- Avoid stock phrases such as “This function is responsible for,” “This block handles,” “Here, we,” and “It is important to note that.”
- Avoid vague praise such as “robust,” “seamless,” “comprehensive,” or “efficient” unless technically defined.
- Avoid repeatedly stating “This ensures that” when the consequence is already evident.
- Remove comments that narrate syntax, duplicate nearby Markdown, contradict the code, or bury the important contract.
- Replace or remove an unsupported scientific claim only when repository evidence establishes the correction or the claim is clearly redundant. Otherwise report the ambiguity and require expert confirmation, even when editing is authorized.

Consult [references/comment-examples.md](references/comment-examples.md) when concrete wording examples would help. Do not load it when the repository's own conventions already settle the choice.

### Require evidence before assigning scientific meaning

Do not infer units, physical roles, sentinel meanings, or conversion
semantics from arithmetic patterns, input position, or domain familiarity
alone.

Treat an interpretation as established only when it is supported by one
or more of the following:

- explicit variable or field names;
- data schemas;
- tests;
- repository documentation;
- user instructions;
- authoritative nearby comments;
- output labels that unambiguously define the quantity.

In particular:

- Do not describe multiplication by `1e-n` as a unit conversion unless
  both the source and target units are established.
- Do not assign sample/reference, measured/calculated,
  reactant/product, or similar physical roles to generic input series
  without supporting evidence.
- Do not assign a physical meaning to a sentinel, correction, offset, or
  threshold beyond its observable effect in the implementation.
- Do not turn a plausible domain interpretation into a documented fact.

When scientific semantics remain uncertain:

1. preserve the calculation;
2. use neutral terminology;
3. document only the observable computational operation;
4. report the ambiguity in the completion summary.

Prefer “Scale the input values by the configured factor” over “Convert
nanoseconds to seconds” when the units are not documented.

## Respect refactoring boundaries

- Do not silently fix scientific assumptions or numerical constants.
- Do not rename public symbols, change schemas, or alter output ordering unless requested.
- Preserve side effects, exception behavior, and generated file structure.
- Update nearby documentation whenever implementation changes make it stale.
- Delete commented-out dead code only when it is clearly obsolete; retain it only with a concrete justification.
- Describe a valuable but risky refactor separately instead of applying it during documentation work.
- Do not add TODO or FIXME comments unless they name a concrete unresolved action, its importance, and any condition needed to resolve it.

## Apply language-specific conventions

### Jupyter Notebook

- Treat `.ipynb` as a structured artifact, not ordinary JSON. Classify its role before editing; generated, cached, result, publication, and unknown-role notebooks are normally Tier 0.
- Preserve `nbformat`, `nbformat_minor`, notebook and cell metadata, cell count and order, cell IDs and types, execution counts, outputs, attachments, and untouched source by default.
- Do not execute, clear or regenerate outputs, normalize JSON or metadata, convert to a script, add or remove cells, reorder cells, or repair hidden state unless explicitly requested and protected.
- Change only the minimum existing Markdown or code-cell source needed. Prefer one authoritative explanation instead of duplicated Markdown and comments.
- Require both structural preservation and a focused textual diff. If the editing mechanism would rewrite unrelated serialization, report the limitation and do not edit.
- Report hidden or prior-state dependencies without silently restructuring the notebook.
- When source changes but stored outputs remain, say the notebook was not executed and do not imply that displayed outputs were recomputed.
- Use a dependency-free structural comparison or repository validator when available. A deterministic fixture probe may add evidence, but it does not prove general notebook equivalence.

Consult [references/jupyter-notebooks.md](references/jupyter-notebooks.md) before editing a notebook or reviewing notebook state, serialization, generated status, or stale outputs.

### Python

- Follow repository formatter and lint settings; otherwise use PEP 8-compatible, Black-like readability.
- Use the existing docstring convention; otherwise use concise Google-style docstrings.
- Add type hints to new or substantially modified public functions when practical, without churning untouched code.
- Document NumPy-style shapes, dtypes, units, and axis meanings when relevant.
- Prefer named helpers over dense lambdas or anonymous transformations.
- Keep scientific computation separate from plotting and file I/O when practical.
- Raise explicit exceptions with actionable messages.

### JavaScript and TypeScript

- Follow repository formatter and lint rules.
- Use JSDoc or TSDoc for public or non-trivial interfaces when it adds information beyond TypeScript types.
- Break long promise chains, callbacks, JSX expressions, and transformations into named steps.
- Document browser, runtime, DOM, and framework assumptions.
- Prefer semantic names over `data2`, `tmp`, or `res` when a precise name is available.

### HTML and CSS

- Use semantic structure and keep nesting controlled.
- Preserve accessibility attributes and add them for new interactive elements.
- Comment only meaningful page regions or unusual layout constraints.
- Prefer role-based class names and avoid large unexplained inline-style blocks.
- Group related CSS declarations consistently with the project.

### Shell

- Use readable multi-line commands when a command has several options or stages.
- Quote variables unless intentional splitting is required.
- Document required executables, environment variables, paths, and working directories.
- Comment major stages and non-obvious shell behavior.
- Do not add `set -e`, `set -u`, or `set -o pipefail` blindly; first evaluate behavior changes.
- Keep destructive operations explicit and narrowly scoped.
- Prefer ShellCheck-compatible patterns when available.

### TeX and LaTeX

- Organize packages, macros, structure, figures, tables, and bibliography settings coherently.
- Explain non-obvious package choices, macros, counters, spacing workarounds, and template constraints.
- Use semantic macros for recurring scientific notation when appropriate.
- Preserve journal or institutional template requirements.
- Do not reformat generated bibliography or template code unless requested.

### Configuration and data formats

- Preserve schema, key order, column order, and machine-generated structure when required.
- Group configuration keys logically.
- Add comments only where the format supports them.
- Put explanations in nearby documentation rather than introducing invalid JSON, CSV, or other syntax.
- Do not modify generated files unless the request explicitly includes them.

## Validate and report

Run the narrowest relevant checks available, such as the formatter, linter, type checker, unit or integration tests, syntax compiler, TeX build, ShellCheck, or a targeted smoke test. For documentation-only edits, still check parsing, compilation, or rendered structure when practical.

For notebook edits, validate protected structure and intended source allowances without executing the original notebook. Treat validator errors, ambiguous results, unexpected source changes, and protected-field changes as failures. When the task is repeatable, check that a second identical documentation pass converges to no meaningful diff.

Never claim a check passed unless it ran successfully. If a check cannot run, name it and explain why.

Finish with a concise report that states:

- which files changed;
- what documentation or readability improved;
- whether behavior was intentionally preserved;
- which validation commands ran and their outcomes;
- any unresolved ambiguity, scientific assumption, or suspicious logic left unchanged.
- for notebooks, the apparent role, whether execution occurred, and whether stored outputs were preserved rather than regenerated.
