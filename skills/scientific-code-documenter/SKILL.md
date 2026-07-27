---
name: scientific-code-documenter
description: Write, refactor, document, or review scientific and technical code for readable structure, concise human-sounding comments and docstrings, and explicit units, shapes, assumptions, conventions, and numerical choices while preserving behavior. Use when users ask to add or improve comments or docstrings, clean up cramped code, improve scientific-code readability, document units, dimensions, array or table shapes, scientific assumptions, or numerical conventions, remove excessive or AI-like comments, or review documentation quality. Do not trigger for ordinary debugging, dependency updates, test execution, or feature implementation that does not request documentation or readability work.
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
2. Classify the request as new code, documentation, readability refactoring, or review. Perform only the requested mode or modes.
3. Define the smallest coherent scope. Prefer focused edits over repository-wide style churn.
4. Apply repository-specific conventions first. Improve local inconsistency only when the existing pattern is unclear, cramped, or misleading.
5. Preserve public interfaces, calculations, numerical behavior, outputs, and file formats unless the user explicitly requests a behavioral change.
6. Run the most relevant available validation and report exactly what ran.

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

### Refactor for readability

- Simplify dense expressions, deep nesting, long functions, or opaque transformations only where understanding materially improves.
- Use clear intermediate variables and coherent helpers.
- Preserve evaluation order, floating-point behavior, side effects, exception behavior, and data ordering unless change is requested.
- Keep public names stable. Treat symbol renaming and extraction across module boundaries as higher-risk changes.

### Review documentation and style

- Review without editing unless the user asks for fixes.
- Prioritize issues that affect correctness, scientific interpretation, reproducibility, or maintainability.
- Distinguish defects from preferences.
- Cite concrete files and tight line ranges, explain impact, and suggest the smallest remedy.
- State when no actionable issue is found.

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

Never claim a check passed unless it ran successfully. If a check cannot run, name it and explain why.

Finish with a concise report that states:

- which files changed;
- what documentation or readability improved;
- whether behavior was intentionally preserved;
- which validation commands ran and their outcomes;
- any unresolved ambiguity, scientific assumption, or suspicious logic left unchanged.
