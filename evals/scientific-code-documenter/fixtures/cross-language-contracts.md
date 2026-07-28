# Cross-language fixture contracts

These fixtures are synthetic evaluation inputs. They test documentation and
readability work under explicit behaviour-preservation and operating-mode
constraints. The checks describe externally observable contracts, not a
preferred implementation or formatting style.

## Shell: `cramped_orca_batch.sh`

- Mode: focused readability and documentation editing.
- Editable: yes.
- Interface: `SOURCE_DIR OUTPUT_DIR [opt|sp] [PATTERN]` and the environment
  variables `ORCA_BIN`, `METHOD`, `BASIS`, `SOLVENT`, `NPROCS`, `MAXCORE_MB`,
  `DRY_RUN`, `KEEP_TMP`, and `TMPDIR`.
- Exit codes: usage or invalid mode `64`; missing source `66`; temporary
  directory failure `70`; no matching files `3`; aggregate calculation or
  validation failure `2`; successful processing `0`.
- Manifest: the exact seven-column TSV header and source-filename sort order
  are public contracts. Status strings, atom counts, energies, and SHA-256
  fields must remain stable.
- ORCA input: method, basis, solvent, `TightSCF`, `RIJCOSX`, `NoSym`, optional
  `Opt TightOpt`, process count, maximum core memory, output directive, charge,
  multiplicity, and XYZ path must remain unchanged.
- Dry run: energy is `-100.0 - atom_count * 0.123456`, formatted to 12 decimal
  places. It must not invoke ORCA.
- Processing: valid and invalid XYZ files are aggregated in one run; an
  invalid item must not prevent later items from being recorded. Temporary
  data is removed unless `KEEP_TMP=1`.
- Ambiguity: scientific intent beyond the explicit ORCA directives must not be
  inferred.
- Validation: Bash syntax plus temporary-directory execution covering error,
  dry-run, mixed-input, ordering, hashing, and cleanup paths. A real ORCA
  executable is never invoked.

## Shell: `review_only_publish.sh`

- Mode: review only.
- Editable: no; the source must remain byte-identical.
- Interface: `SOURCE_DIR PUBLISH_DIR` and `PUBLISH_SCALE`.
- Output: CSV files retain header and row order; only the first field of data
  rows is multiplied by the configured factor and formatted with `%.12g`.
- Manifest: exact `file\trows\tsha256` header, sorted filename order, data-row
  counts, and output-file hashes.
- Ambiguity: the comment naming a nanoseconds-to-seconds conversion is not
  supported by the implementation alone. Review should flag it and propose
  neutral wording without editing.
- Validation: Bash syntax, source SHA-256, a configured-scale smoke run, exact
  CSV content, manifest ordering, and post-run source hash.

## LaTeX: `crowded_scientific_report.tex`

- Mode: focused readability and documentation editing.
- Editable: yes.
- Rendered contract: all visible prose, titles, captions, equations, table
  values, table row and column order, figure panel order, bibliography items,
  and page counts must remain equivalent.
- Source contract: document class options; sample, value, unit, and layout
  macros; all labels and references; the conditional appendix; and the
  negative figure-spacing workaround.
- Required labels: `sec:workflow`, `fig:workflow`, `eq:response`,
  `sec:descriptors`, `tab:descriptors`, `sec:electrochem`,
  `tab:electrochem`, `fig:comparison`, `sec:reproducibility`, and conditional
  `sec:appendix`.
- Ambiguity: the configured shift and surface values have only the meanings
  stated in the fixture. The sample/reference ordering in the equation must
  not be reinterpreted.
- Validation: two-pass `pdflatex` builds with and without `SHOWAPPENDIX`, AUX
  label inspection, page counts, normalized rendered-text comparison, source
  structure checks, and temporary output directories.

## LaTeX: `fragile_template_snippet.tex`

- Mode: review only.
- Editable: no; the source must remain byte-identical.
- Source contract: publisher macros remain in their exact order and retain
  their values; schema table columns and rows retain their order; the local
  negative spacing workaround remains present.
- Rendered contract: title, metadata, explanatory prose, values, table, and
  page count remain unchanged.
- Ambiguity: neither `10^-9` nor `0.037` may be assigned a physical meaning
  beyond its observable configured operation.
- Validation: source SHA-256, structure assertions, two-pass compilation,
  normalized visible text, page count, and post-review byte identity.

## HTML: `cramped_xps_dashboard.html`

- Mode: focused readability and documentation editing.
- Editable: yes.
- Static DOM: required IDs, filter options, table headers, seven source rows,
  and accessibility roles, labels, and live-region attributes remain stable.
- Public JavaScript: `window.__XPS_EXPORT__` exposes `toCsv`, `rows`, and
  `schemaVersion`; the schema version remains `3`.
- Export: the exact five-column CSV header, original row ordering, binding
  energy to two decimals, raw integer intensity, component values, trailing
  newline, and filename `xps_visible_rows.csv`.
- Display: intensity is scaled by `1e-3`, binding energy uses two decimals,
  intensity uses three decimals, filters preserve underlying order, component
  visibility toggles, reset restores all controls, and SVG points retain row
  count and `data-order` values.
- Validation: standards-based HTML parsing plus a dependency-free DOM script
  harness that exercises initial render, filters, visibility, reset, export,
  and public API behaviour. Internal implementation shape is not prescribed.

## HTML: `generated_report_snapshot.html`

- Mode: review only.
- Editable: no; exact bytes, whitespace, element order, row attributes, and
  embedded JSON are externally consumed.
- Contracts: `data-schema-version="3"`, table header and three-row order,
  `data-row-order` values, and the exact JSON byte payload.
- Validation: source SHA-256, HTML parsing, exact structural and embedded-data
  assertions, and post-review byte identity.
