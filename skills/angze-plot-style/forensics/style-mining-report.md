# Angze plotting style: Phase 1 forensic mining report

Analysis date: 2026-08-12
Bundle starting HEAD: `cd45210acbc6fc405620f0fa5e0e13eec6682869`

This is an evidence report, not a plotting specification. “Observed” means a value is present in tracked source. “Inferred” means the interpretation combines frequency, cross-repository recurrence, recency, independence, context, and authorship confidence. No value is recommended because it is a common publication default.

## 1. Executive summary

Discovery located 35 Git repositories under the bounded Desktop and Documents roots. A token and context screen reduced these to 15 plausible plotting candidates. Ten repositories were mined and five were excluded after provenance/context review. The static corpus contains 90 plotting-bearing files, 302 distinct function/notebook-cell plotting contexts, and 4,288 granular observations.

The strongest inferred fingerprint is unusually consistent across independent research, coursework, and tooling repositories:

- Arial-first sans-serif text where a family is explicitly controlled;
- 22 pt bold axis labels;
- 14 pt bold tick labels;
- 18 pt bold titles when titles are shown;
- complete black boxed axes with 1.8 pt spines;
- inward major ticks, usually 1.8 pt wide;
- white figure/axes backgrounds with black foreground text and axes;
- framed, bold legends, most often 10 pt;
- an approximately 8 × 6 inch single-panel canvas;
- `tight_layout()` for ordinary figures and constrained layout for dense/multipanel figures;
- `bbox_inches="tight"` and a white, opaque raster background.

One high-confidence base/publication family exists. A smaller-text diagnostic family is supported at MEDIUM confidence by the XPS workbench and BO Forge. A compact multipanel family and a presentation family are visible but remain LOW confidence because their exact values are concentrated in one repository or do not agree closely enough across repositories.

Overall confidence is HIGH for the core typographic, spine, background, legend-frame, figure-geometry, and bounding-box fingerprint; MEDIUM for line/marker defaults, error bars, annotations, and context variants; and UNRESOLVED for global font size, tick length, minor ticks, top/right tick placement, marker-edge width, alpha, raster DPI, vector transparency, and exact math fontset.

## 2. Repository corpus

“Plotting evidence” reports plotting-bearing tracked files; for included repositories it also gives the curated mined subset. Recency is the latest commit touching the relevant candidate/mined paths, not the repository’s wall-clock modification time.

| Repository | Path | Recency | Plotting evidence | User-authored? | Included? | Notes |
|---|---|---:|---:|---|---|---|
| pdi-calculation | `~/Desktop/Tsinghua 2026 Summer/pdi_h2o2_production/calculation` | 2026-08-12 | 20; 14 mined | High | Yes | Recent manuscript analysis, notebooks, and explicit shared helpers; tests excluded. |
| pdi-data | `~/Desktop/Tsinghua 2026 Summer/pdi_h2o2_production/data` | 2026-08-04 | 19; 18 mined | High | Yes | Independent experimental techniques sharing a repeated publication template; one test excluded. |
| xps-workbench | `~/Desktop/squiddy tools/xps-fitting-workbench` | 2026-08-09 | 32; 15 mined | High | Yes | Current workbench; explicit `angze_publication`, diagnostic, multipanel, and presentation themes. |
| bo-forge | `~/Desktop/bo_forge` | 2026-08-09 | 28; 15 mined | High | Yes | Shared report-ready helper, diagnostics, and source notebooks; tests and app UI excluded. |
| ising-coursework | `~/Desktop/Imperial/Year 25-26/26 Summer/imperial-complab-monte-carlo-simulations-of-a-2d-ising-model` | 2026-06-08 | 11; 11 mined | High | Yes | Independent scientific project with `ILplot_style.py`. |
| pdi-theory-demo | `~/Desktop/Tsinghua 2026 Summer/pdi_h2o2_production/pdi-theory-demo` | 2026-07-18 | 9; 9 mined | Medium | Yes | Tracked tutorial/analysis notebooks only; active untracked work excluded. |
| fyp-zis-photocatalysis | `~/Desktop/Imperial/Year 25-26/26 Summer/fyp-zis-photocatalysis` | 2026-06-07 | 1; 1 mined | High | Yes | One Gaussian report generator, treated as one independent source. |
| tdqms-coursework | `~/Desktop/Imperial/Year 25-26/26 Spring/Time-dependent Quantum Mechanics and Spectroscopy/Coursework` | 2026-05-05 | 4; 2 mined | High | Yes | Local helper plus its consuming notebook. |
| opentrons-screening | `~/Desktop/Imperial/Year 25-26/26 Summer/Emerging Technologies/Opentrons OT-2 liquid handling platform/opentrons_macrocycle_screening` | 2026-05-13 | 1; 1 mined | High | Yes | Two related calibration figures in one notebook; one independent file. |
| pytorch-to-bo | `~/Desktop/Experiences/from-pytorch-to-bayesian-optimisation` | 2026-06-13 | 44; 4 mined | Medium | Yes, downweighted | Only four advanced source tutorials were sampled; worked copies were excluded as non-independent duplicates. |
| ase-learning | `~/Desktop/Experiences/ase_learning` | 2026-08-10 | 15; 0 mined | Low for style | No | Files explicitly identify as official ASE tutorials; personal-style provenance is weak. |
| qchem-workbench | `~/Desktop/Experiences/qchem_workbench` | 2026-06-29 | 4; 0 mined | High | No | Near-default Matplotlib is intentionally used for utilitarian library output, not a personal final-figure style. |
| data-foundations | `~/Desktop/squiddy tools/data-foundations-with-numpy-and-pandas` | 2026-06-22 repository head | No material plotting code cells | Medium | No | Plot references are teaching/data-preparation examples, not final visual identity. |
| market-criticism-index | `~/Desktop/squiddy tools/market-criticism-index` | 2026-06-03 | 1; 0 mined | High | No | One finance diagnostic uses a grid and 160 dpi; insufficient recurrence and outside the scientific target. |
| xps-workbench-older-copy | `~/Desktop/squiddy tools/experimental_data_analysis/xps-fitting-workbench` | 2026-07-22 | 28; 0 mined | High | No | Older duplicate lineage; counting it would inflate recurrence without independence. |

Twenty additional discovered Git repositories had no plausible user-authored scientific Python plotting surface and were not promoted to the candidate table.

## 3. Methodology

### Discovery

Repository discovery was bounded to `~/Desktop` and `~/Documents`, with `.git` metadata used for recency. Virtual environments, dependency trees, caches, build outputs, and system paths were not traversed. Tracked `.py` and `.ipynb` files were screened for Matplotlib, seaborn, plotting calls, style configuration, and export calls.

### Provenance filtering

Git history was used to establish that the selected plotting surfaces were predominantly authored/adopted in the user’s repositories. Official tutorials, worked duplicates, tests that merely exercise arbitrary settings, generic default plotting, an older duplicate checkout, and untracked active work were excluded or downweighted. Personal author identity is intentionally not reproduced here.

### Extraction and normalisation

The intentionally reusable forensic extractor at `skills/angze-plot-style/forensics/extract_style_evidence.py` reads tracked Python source and notebook code cells only. It uses Python ASTs to resolve simple constants, dataclass theme defaults, `rcParams` mappings, style-helper calls, aliases such as `lw`/`linewidth` and `ms`/`markersize`, export options, semantic colour dictionaries, and function/cell locations. It never imports project code or executes plotting/scientific calculations. Numeric spellings such as `2` and `2.0` are merged for aggregation but preserved in individual observations.

### Weighting and confidence

Raw occurrences were not treated as votes. Inference considered frequency, independent files, repository count, recency, copied-template dependence, context, and authorship confidence. Nine PDI experimental utility modules, for example, provide strong within-repository consistency but count as one repository family for cross-repository confidence. Tutorial worked copies were excluded rather than counted repeatedly.

### Limitations

- Static extraction cannot resolve every runtime-derived value or data-dependent axis limit.
- One tracked notebook cell in `pdi-theory-demo/analysis/08_excitation_state_uv_vis_analysis.ipynb` contains an existing syntax error at cell 15, line 130. That cell was recorded as a parse limitation; other cells in the notebook were mined.
- Function-argument defaults and dynamically constructed export paths are supplemented by direct helper inspection, so the Markdown can cite evidence not represented as a scalar AST observation.
- A style explicitly adopted into a repository is treated as user-owned evidence even if an assistant may have helped write the code; the task is to recover the established codebase style, not reconstruct typing provenance.

## 4. High-confidence style fingerprint

Observed and suitable for likely canonicalisation:

> Arial-first sans serif on a white ground; very large bold axis labels (22), bold ticks (14), bold 18 pt titles when shown, full 1.8 pt black boxed spines, inward major ticks, framed bold legends, an 8 × 6-ish single-panel canvas, compact 2-ish-point data lines, and tight-bounded white exports.

This fingerprint is not a generic journal template. The 22/14/18 hierarchy and 1.8 pt box are substantially heavier/larger than many conventional defaults and are preserved because they recur in the user’s code.

Representative sources:

- `pdi-calculation:python/sterics/figure_style.py` — `apply_publication_theme`, `style_axes`, `style_legend`, `save_figure_bundle`.
- `pdi-data:cv/cv_utility.py` — `apply_plot_style`, `style_cv_axes`, `save_figure`.
- `xps-workbench:src/xps_fitting/plotting/themes.py` — `PlotTheme`, `rc_params`, `style_axes`.
- `bo-forge:bo_forge/plot_style.py` — module constants and finalisation helpers.
- `ising-coursework:python_script/ILplot_style.py` — independent publication helper.
- `tdqms-coursework:tdqms_plotting.py` and `opentrons-screening:calibration/calibration_curve.ipynb` cells 2/4 — older independent confirmations.

## 5. Typography

Counts are `occurrences / independent files / repositories`.

| Property | Candidate or conflict | Count | Recency/context | Confidence | Representative evidence |
|---|---|---:|---|---|---|
| Font family | Arial-first sans serif | 15 / 15 / 3 explicit Arial-first declarations | 2026-08 PDI calculation/data and XPS | HIGH | `pdi-data:cv/cv_utility.py::apply_plot_style`; `pdi-calculation:python/sterics/figure_style.py::apply_publication_theme`; `xps-workbench:src/xps_fitting/plotting/themes.py::PlotTheme.font_family` |
| Global font size | 14 only in XPS base theme; other repositories style roles directly | 1 / 1 / 1 | XPS only | UNRESOLVED | `xps-workbench:src/xps_fitting/plotting/themes.py::PlotTheme.font_size` |
| Axis-label size | 22 | 124 / 30 / 8 | 2026-05 to 2026-08; research, coursework, tools | HIGH | BO `AXIS_LABEL_SIZE`; Ising `LABEL_SIZE`; PDI utilities; TDQMS helper |
| Axis-label weight | bold | 138 / 34 / 9 | Broadest typographic recurrence | HIGH | Same helpers plus Gaussian report `style_plot_axes` |
| Tick-label size | 14 | 43 / 30 / 8 | Base/publication contexts | HIGH | BO `TICK_LABEL_SIZE`; Ising `TICK_SIZE`; PDI utilities |
| Tick-label weight | bold | 40 / 29 / 8 explicit resolved uses | Cross-repository | HIGH | `pdi-data:cv/cv_utility.py` and `pdi-data:eis/eis_utility.py` tick loops; `xps-workbench:src/xps_fitting/plotting/themes.py::style_axes` |
| Title size | 18 when present | 61 / 19 / 7 | Diagnostics/tutorials and titled analyses | HIGH | BO `TITLE_LABEL_SIZE`; Ising `TITLE_SIZE`; PDI theory notebook style cells |
| Title weight | bold | 95 / 26 / 8 | Cross-repository | HIGH | BO, PDI, XPS, Gaussian helpers |
| Title visibility | shown in diagnostic/tutorial; suppressed in some final manuscript panels | explicit conflict | Context split | MEDIUM | XPS `show_title=False`; H2O2 helper describes “title-free” axes; BO diagnostics set titles |
| Legend size | 10 base; 12 and 11 credible alternatives | 10: 46 / 17 / 8; 12: 8 / 8 / 4; 11: 2 / 2 / 2 | 10 broadest; 12 experimental/TDQMS; 11 XPS | MEDIUM | BO/Ising/sterics use 10; PDI CV/XPS/TDQMS use 12; XPS theme uses 11 |
| Legend weight | bold | 48 / 24 / 8 | Broad | HIGH | `prop={"size": ..., "weight": "bold"}` and legend styling helpers |
| Panel labels | `(a)`, `(b)`, …, bold, left title position | explicit in XPS only | Multipanel XPS | LOW | `xps-workbench:src/xps_fitting/plotting/themes.py::panel_label_template`; `xps-workbench:src/xps_fitting/plotting/sample_panel.py` line-style title call |

The small 5–8 pt typography values in dimer overview montages are outliers tied to very dense panels, not evidence against the 22/14/18 base.

## 6. Axes and spines

| Property | Observed values | Interpretation | Confidence |
|---|---|---|---|
| Spine visibility | all spines explicitly visible: 20 / 17 / 4; XPS base has top/right `True` | Complete boxed axes are intentional. Occasional hidden spines belong to specialized orbital/montage panels. | HIGH |
| Spine width | 1.8: 44 / 33 / all 10 mined repositories; 1.2 and 1.0 are sparse/local | 1.8 is the strongest single numerical rule in the corpus. | HIGH |
| Spine colour | repeated explicit black in style helpers | Black box on white ground. | HIGH |
| Grid | explicit `False` in 3 independent repositories and `axes.grid=False` in recent helpers; no included final-style helper enables a grid | Grid avoidance is plausible, but absence was not converted into explicit votes. | MEDIUM / plausible negative |
| Axis limits | usually explicit and science-driven | Do not globalise limits. Spectra often invert or tightly bind the physical domain; bar/time plots often start y at zero. | HIGH that this is context-dependent |
| Horizontal padding | `margins(x=0)` appears 6 / 6 / 2, mainly spectra/XPS | Zero x padding is a spectral convention, not a universal axis rule. | MEDIUM, spectral only |
| Vertical headroom | explicit 6–18% examples; XPS theme uses 10% | Add label/curve headroom when annotations need it, but exact padding is unresolved. | MEDIUM |

The most representative boxed-axis implementations are `pdi-data:cv/cv_utility.py::style_cv_axes`, `pdi-calculation:python/sterics/figure_style.py::style_axes`, `xps-workbench:src/xps_fitting/plotting/themes.py::style_axes`, and `fyp-zis-photocatalysis:gaussian/scripts/visualise_gaussian_results.py::style_plot_axes`.

## 7. Ticks

| Property | Values and counts | Interpretation | Confidence |
|---|---|---|---|
| Direction | inward: 30 / 17 / 4 | Recent PDI and XPS styles agree. | HIGH |
| Major width | 1.8: 22 / 19 / 5 | Usually matches the spine width. | HIGH |
| Major length | 7: 9 / 8 / 1; 6: 6 / 5 / 2; 4: 2 / 2 / 2 | PDI experimental uses 7; sterics/Ising use 6; XPS uses 4. No single base length is justified. | UNRESOLVED |
| Minor width | 1.2: 8 / 8 / 2; 1.4: 2 / 2 / 2 | 1.2 is a candidate when minor ticks are enabled. | MEDIUM |
| Minor length | 3.5: 7 / 7 / 1; 2.5: 1 / 1 / 1; 4: one PDI case | Exact minor geometry is context-specific. | UNRESOLVED |
| Minor presence | electrochemical quantitative axes often use `AutoMinorLocator(2)`; broad UV–Vis/IR spectra deliberately use `NullLocator()` | Presence depends on plot density and physical axis. | UNRESOLVED |
| Top/right ticks | PDI experimental helpers explicitly set both `False`; XPS maps ticks to visible top/right spines | Boxed spines are stable, tick placement is not. | UNRESOLVED |
| Tick decimals | `.1f`, `.2f`, `.3f`, integer locators, and adaptive scientific formats all occur | Formatting follows measurement precision; no global decimal rule. | UNRESOLVED |

## 8. Lines, markers, scatter, error bars

### Lines and markers

| Property | Main values | Interpretation | Confidence |
|---|---|---|---|
| Data-line width | 2.0: 25 / 14 / 6; 2.2: 7 / 4 / 3; 2.4: 6 / 4 / 2; 2.5 concentrated in tutorial families | 2.0 is the broad base candidate. 2.2 is spectral; 2.4 is the current sterics profile. | MEDIUM |
| Marker size | 6: 13 / 7 / 5; 4: 7 / 3 / 3; 5.5: 3 / 3 / 2; 7: 3 / 2 / 2 | 6 is a general candidate; smaller markers support dense XPS/sterics and larger ones experimental time courses. | MEDIUM |
| Marker edge width | 0.4, 0.45, 0.5, 0.6, 0.8, 0.9, 1.8 | Filled, open, and highlighted markers intentionally differ. | UNRESOLVED |
| Line alpha | 0.55, 0.65, 0.8, 0.82 in different roles | No single alpha. | UNRESOLVED |

Recent final PDI figures often use coloured lines with round caps, filled or white-centred circular markers, and contrasting white/black edges. This is a recurring construction, but edge treatment depends on whether the marker is raw data, a highlighted minimum, or a fitted point.

### Scatter

Scatter size has no dominant global value. `s=45` recurs across 5 files/3 repositories, while 50, 55, 70, 80, 90, 120, and 150 are all credible context values. Edge widths of 0.8 (7 files/4 repositories) and 0.5 (3 files/3 repositories) recur, but tutorial and highlight scatters use 1.0–1.8. Scatter alpha ranges from faint diagnostic clouds (0.08–0.55) to nearly opaque scientific points (0.85–0.92). The evidence supports semantic scatter styling, not one canonical scatter preset.

### Error bars

| Property | Values | Interpretation | Confidence |
|---|---|---|---|
| Capsize | 4: 7 occurrences / 3 files / 3 repositories; 2–3 compact; 5 emphasized | `capsize=4` is the best general candidate. | MEDIUM |
| Error-line width | 1.4 in PDI time courses; 1.5 in Opentrons calibration | 1.4–1.5 band. | MEDIUM |
| Cap thickness | 1.4 in PDI time courses | Insufficient cross-repository evidence. | LOW |
| Error marker size | 6–6.5 in experimental plots; 2.5–4 in compact Ising panels; 8 in one sterics plot | Context-dependent. | UNRESOLVED |

### Bars

Black bar edges recur at 1.2 (5 files/3 repositories) and 0.8 (3 files/2 repositories). Bars are often labelled with bold values and deliberate y headroom. Alpha 0.75 in the Gaussian report and 0.85–0.88 in BO diagnostics is not cross-context stable.

## 9. Layout and figure geometry

### Figure sizes

| Size (inches) | Occurrences / files / repositories | Aspect | Context |
|---|---:|---:|---|
| 8 × 6 | 31 / 18 / 9 | 1.333 | Strong base/single-panel geometry. |
| 9 × 6 | 6 / 4 / 4 | 1.5 | Wider categories or labels. |
| 8 × 5 | 14 / 9 / 3 | 1.6 | Wide diagnostics/tutorial figures. |
| 8.4 × 6.4 | explicit recent sterics constant/calls | 1.313 | Current PDI manuscript single panel. |
| 14 × 5 | 7 / 4 / 1 | 2.8 | Wide BO tutorial panels. |
| 7.2 × 4.8 | 3 / 3 / 1 | 1.5 | Compact Ising analysis. |
| stacked 7.2–8 × 7.2–11 | repeated Ising | variable | Vertical shared-x scientific panels. |
| 13 × 3.8, 13 × 5.8, 13 × 10.5 | recent PDI/XPS families | variable | Four-panel/wide or grid compositions. |

The evidence supports 8 × 6 as the base, with geometry selected by panel count rather than forcing one aspect ratio everywhere.

### Layout engine and spacing

- `tight_layout()` appears 79 times across 33 files and 9 repositories: HIGH evidence for ordinary finalisation.
- `constrained_layout=True` appears 42 times across 12 files and 3 repositories, concentrated in recent BO, Ising, and PDI dense figures: MEDIUM evidence for a dense/multipanel override.
- Recent sterics figures use `tight_layout(w_pad=2.0)` for horizontal panels.
- Dense BO layouts use small explicit engine pads (`w_pad=0.08`, `h_pad=0.2`, `wspace=0.06`).
- ORR/dimer montages use hand-tuned `subplots_adjust` values. These are figure-specific and must not become global defaults.

## 10. Legends and annotations

### Legends

Framed bold legends are HIGH confidence: `frameon=True` appears in 21 files/8 repositories and bold legend text in 24 files/8 repositories. Face white and edge black recur through BO, PDI, TDQMS, and XPS helpers. Square corners (`fancybox=False`) and frame alpha 0.95–1.0 occur in PDI/XPS publication code.

Legend location is deliberately data-dependent:

- upper left: 7 files/4 repositories;
- upper right: 8 files/3 repositories;
- best: 4 files/3 repositories;
- upper centre: 4 files/2 repositories;
- outside lower centre: an XPS multipanel case.

No canonical legend location is justified. Frame padding, handle length, label spacing, and column count are configured only in particular dense figures; leave these context-controlled.

### Annotations

Bold annotations recur 57 times across 25 files and 8 repositories. Sizes 9 (17 occurrences/8 files/3 repositories) and 10 (11/6/5) form the best base band. Eight-point text is used for compact diagnostics; 12–14 for more prominent values. Axes-relative placement, explicit horizontal/vertical alignment, white-backed text boxes, and offset-point annotations are common. Arrow/leader widths range roughly 0.7–1.4 and are context-dependent.

Panel labels are only explicitly standardised by XPS as `(a)`, `(b)`, … in a bold, left-aligned title position. This is traceable but LOW confidence as an Angze-wide convention.

## 11. Colour and semantic colour conventions

### Fixed recurring semantic palette

The following palette is HIGH confidence only for PDI compound comparisons:

| Semantic identity | Colour | Evidence |
|---|---|---|
| PDI-Me-COOH | `#D55E00` | 7 independent files across pdi-calculation and pdi-data |
| PDI-H-COOH | `#0072B2` | 7 independent files across the same two repositories |
| PDI-OMe-COOH | `#7A5195` | 7 independent files across the same two repositories |

Representative definitions: `pdi-calculation:python/sterics/config.py::COLOUR_MAP`, `pdi-data:eis/eis_utility.py::COLOUR_MAP`, plus independent IR, IT, UV–Vis, XRD, CV, and H2O2 uses. The meaning is compound identity/performance ordering, not generic blue/orange/purple series order.

### Context-specific semantic colours

- Ising: blue energy, green magnetisation, red heat capacity, purple susceptibility, orange own result, near-black reference.
- BO: slate raw observations, blue group means, viridis for objective-coloured two-dimensional scatter, and additional task-specific colours.
- XPS: neutral raw/fit colours plus component-assignment colours supplied by chemistry-aware configuration.
- Gaussian report: blue/red/green for related orbital or status categories.

These palettes do not agree enough to infer one general Angze palette. Neutral black/grey is consistently used for reference lines, outlines, raw points, and fit scaffolding.

## 12. Export conventions

| Property | Evidence | Interpretation | Confidence |
|---|---|---|---|
| Bounding box | `tight`: 73 / 30 / 9 | Canonical candidate. | HIGH |
| Raster background | white face colour: 29 / 16 / 6; explicit transparent false in multiple helpers | White opaque raster output. | HIGH |
| Formats | paired PDF+PNG in PDI calculation/data and XPS; PNG-only Ising; PDF-only calibration/Gaussian paths | Pair PDF+PNG for final manuscript figures, but do not require pairs for diagnostics. | MEDIUM |
| DPI | 300: at least 17 direct saves/12 files/3 repos plus BO/Ising defaults; 600: 11/11/2 | Both are recent and intentional. | UNRESOLVED |
| PDF fonts | `pdf.fonttype=42` in 16 files across PDI calculation/data; XPS theme also uses 42 | TrueType embedding is a strong PDI/XPS publication convention. | MEDIUM-HIGH |
| SVG | Ising sets `svg.fonttype="none"`, but its save helper emits PNG; routine final SVG export is not established | Do not create an SVG default yet. | LOW / insufficient |
| Vector transparency | XPS default `True`; PDI helpers force white output | Context conflict. | UNRESOLVED |

Observed naming is descriptive and snake_case, usually one logical figure stem shared by PDF and PNG. No evidence supports a globally mandated file prefix or numbering scheme.

## 13. Scientific formatting conventions

Recurring observed patterns:

- Axis labels normally use `Quantity or descriptor (unit)`.
- Degree and angstrom symbols are usually rendered directly as `°` and `Å`.
- Powers and inverse units use math text: `s$^{-1}$`, `Å$^2$`, or `\mathregular{C^{-2}\ (10^9\,F^{-2}\,cm^4)}`.
- The recent sterics energy unit is deliberately bold in the exponent: `kJ mol$^{\mathbf{-1}}$`.
- Chemical species use subscripts, charges, and radical bullets in math text; the Gaussian report deliberately bolds formulas with `\mathbf{...}`.
- `a.u.` is used for arbitrary units; electron-volt labels use `eV`; electrochemical labels specify reference electrode where needed.
- Peak and fit values use context-specific precision: XPS peak energies commonly two decimals, CV current can use three decimals, and bar labels use adaptive precision/scientific notation for small values.

Inference: unit placement and mathematical superscript/subscript handling are MEDIUM confidence style rules. Decimal places and scientific-notation thresholds are measurement-specific and remain UNRESOLVED.

## 14. Context-dependent variants

### Base/publication — HIGH

Supported by PDI calculation/data, XPS, BO, Ising, TDQMS, and Opentrons:

- Arial-first sans serif;
- axis labels 22 bold;
- ticks 14 bold;
- titles 18 bold when present;
- complete 1.8 pt boxed spines;
- inward ticks;
- framed bold legend;
- white/black ground;
- approximately 8 × 6 inches;
- tight layout/bounding box.

### Compact diagnostic — MEDIUM

Two independent explicit profiles are close enough to form a family:

- XPS diagnostic: global 10, axis 13, tick 10, title 14, legend 9, 5.8 × 4.4.
- BO high-dimensional: axis 14, tick 10, title 16, legend 9, colourbar label 12, figure geometry driven by dimension count.

Difference from base: smaller typography and data-dependent geometry. Exact axis/title size should remain a bounded range, not be silently averaged.

### Compact multipanel — LOW

XPS explicitly uses axis 10, ticks 9, title 9, legend 9 for multipanels. Dense PDI dimer panels also reduce typography to roughly 8–10. The direction is coherent, but exact values are not independently stable enough for automatic Phase-2 encoding.

### Presentation — LOW

XPS defines a presentation profile (axis 17, ticks 13, title 18, line 3, 8 × 5, titles shown). No independent repository exposes a matching named presentation style, so this remains an XPS-local profile rather than an Angze-wide convention.

## 15. Negative conventions

### Strong

- Top/right spines are normally retained; removing them is not the established base style.
- Bold titles, axis labels, tick labels, annotations, and legend text are not avoided; bold typography is central to the style.
- Legends are normally not frameless.
- Raster figures are not normally transparent or dark-background dependent.

### Plausible

- Final scientific figures normally avoid grids. This is explicitly enforced in three independent styles and consistent with default-reset helpers elsewhere, but absence was not counted as equivalent to `grid(False)`.
- The codebase prefers Matplotlib directly. No seaborn import/theme/context call was found in the included corpus.
- Routine SVG delivery is not established; PDF and PNG dominate.

### Insufficient evidence

- Whether top/right ticks should accompany the retained spines.
- Whether all figures should omit titles.
- Whether minor ticks should always be enabled.
- Whether one marker fill/edge treatment should apply to all scatter/errorbar roles.

## 16. Existing reusable helpers

| Repository | Helper/config | What it already encodes | Phase-2 relevance |
|---|---|---|---|
| pdi-calculation | `python/sterics/figure_style.py` | 22/14/10 hierarchy, 1.8 spines/ticks, 2.4 lines, 5.5 markers, framed legends, colourbars, bar labels, PDF+600-dpi PNG | Strongest recent manuscript helper; should inform but not be copied wholesale. |
| pdi-calculation | `python/dimer_analysis/notebook_reporting.py` | Report style, dense panel variants, constrained layout, semantic figures | Evidence for compact/multipanel exceptions. |
| pdi-data | technique `*_utility.py` modules | Repeated Arial template, inward ticks, boxed 1.8 spines, PDF+600-dpi PNG, technique-specific axes | Strong repeated experimental family; copied structure should be consolidated conceptually, not counted as nine repositories. |
| xps-workbench | `src/xps_fitting/plotting/themes.py` | Dataclass themes, `angze_publication`, diagnostic, multipanel, presentation, rc context | Best existing architecture reference; already separates contexts. |
| xps-workbench | `src/xps_fitting/plotting/export.py` | PNG/PDF validation, DPI, transparency, tight bounds, font application | Evidence for a separate export policy layer. |
| bo-forge | `bo_forge/plot_style.py` | White/black ground, 22/14/18/10, 1.8 spines, colourbar style, single/multi-axis finalisation | Strong independent base confirmation. |
| ising-coursework | `python_script/ILplot_style.py` | 22/14/18/10, 1.8 spines, 2.0 lines, 300 dpi | Independent compact scientific helper. |
| tdqms-coursework | `tdqms_plotting.py` | 8 × 6, 22/14/12, 1.8 spines, white/black ground, reference-line helper | Older independent confirmation. |

Phase 2 should consolidate patterns in the new skill rather than refactor or import these repositories. No source helper was modified in Phase 1.

## 17. Conflicts and unresolved questions

| Parameter | Competing evidence | Status / question |
|---|---|---|
| Global font size | 14 in XPS; role-specific only elsewhere | UNRESOLVED: should Phase 2 set `font.size`, or only role sizes? |
| Major tick length | 4 XPS, 6 sterics/Ising, 7 PDI experimental | UNRESOLVED; likely context-specific. |
| Minor ticks | off for broad spectra; 1.2 × 3.5 PDI; 1.2 × 2.5 XPS | UNRESOLVED. |
| Top/right ticks | off in PDI data; on with boxed XPS axes | UNRESOLVED. |
| Legend size | 10 broad base; 11 XPS; 12 experimental/TDQMS | MEDIUM base candidate with variants. |
| Line width | 2.0, 2.2, 2.4, 2.5 | MEDIUM base 2.0; preserve context alternatives. |
| Marker geometry | 4–7 pt; edge 0.4–1.8 pt | UNRESOLVED by artist role. |
| Layout | tight vs constrained | Context split, not a contradiction. |
| Raster DPI | 300 vs 600 | UNRESOLVED and should be reviewed before encoding. |
| Vector transparency | opaque white vs transparent PDF | UNRESOLVED/XPS-specific. |
| Title visibility | omitted manuscript titles vs present diagnostic titles | MEDIUM context split. |
| Math fontset | custom Arial vs STIX Sans vs STIX | UNRESOLVED. |
| Decimal precision | integers, 1–3 decimals, adaptive scientific notation | Must remain measurement-specific. |
| Legend location | upper left/right/centre/best/outside | Data-dependent; no canonical value. |

## 18. Outliers and one-offs

- Extremely small 5–8 pt labels in dense dimer overview/montage figures are panel-density adaptations.
- Very wide 14 × 5 BO tutorial canvases are educational multi-panel layouts, not base single-panel geometry.
- The Gaussian 11 × 8.5 text/table pages are report pages, not data-plot dimensions.
- One market-index plot with grid alpha 0.25 and 160 dpi was excluded as a one-off finance diagnostic.
- Qchem-workbench’s 6 × 4 near-default plots are utilitarian library output and were excluded from personal-style inference.
- ASE “official tutorial” notebooks were excluded despite recent activity.
- Pytorch worked notebooks were excluded so source/worked pairs could not double-count the same choices.
- Hidden spines in certain orbital/montage axes are special compositional decisions, not evidence for a general despined style.
- XPS vector transparency and the named presentation profile are legitimate local choices but not independently recurrent.

## 19. Candidate Phase-2 style profile

This table is provisional. `UNRESOLVED` means Phase 2 must not choose silently.

| Candidate rule | Provisional value | Confidence | Scope |
|---|---|---|---|
| Font family | Arial-first sans-serif fallback stack | HIGH | Base |
| Global font size | no candidate | UNRESOLVED | Base |
| Axis labels | 22 pt, bold | HIGH | Base |
| Tick labels | 14 pt, bold | HIGH | Base |
| Titles | 18 pt, bold, only when shown | HIGH | Base |
| Title visibility | manuscript off / diagnostic on | MEDIUM | Context |
| Figure/axes ground | white; foreground black | HIGH | Base |
| Spines | all visible, black, 1.8 pt | HIGH | Base |
| Major ticks | inward, 1.8 pt wide | HIGH | Base |
| Major tick length | 4 / 6 / 7 by context | UNRESOLVED | Context |
| Minor ticks | context-dependent | UNRESOLVED | Context |
| Top/right ticks | context-dependent | UNRESOLVED | Context |
| Grid | off | MEDIUM | Base |
| Legend | framed, white, black edge, bold | HIGH | Base; square corners are MEDIUM |
| Legend size | 10 pt | MEDIUM | Base; 11/12 alternatives |
| Legend location | automatic/data-dependent | UNRESOLVED | Per figure |
| Single-panel size | 8 × 6 inches | HIGH | Base |
| Data-line width | 2.0 pt | MEDIUM | Base; 2.2/2.4 variants |
| Marker size | 6 pt | MEDIUM | Base |
| Marker edge width | no candidate | UNRESOLVED | Artist role |
| Alpha | no global candidate | UNRESOLVED | Artist role |
| Scatter | outlined markers; size/alpha context-dependent | LOW-MEDIUM | Artist role |
| Errorbar capsize | 4 pt | MEDIUM | Base error bars |
| Errorbar line/cap width | 1.4–1.5 pt | MEDIUM | Experimental |
| Reference lines | dashed, black/grey | HIGH | Base |
| Annotation text | 9–10 pt, bold | MEDIUM | Base |
| Panel labels | `(a)`, `(b)`, bold left title position | LOW | Multipanel |
| Ordinary layout | tight layout | HIGH | Single/simple |
| Dense layout | constrained layout | MEDIUM | Dense/multipanel |
| Export bounding box | tight | HIGH | All exports |
| Raster background | white, opaque | HIGH | Raster |
| Final formats | paired PDF + PNG | MEDIUM | Manuscript/final |
| Raster DPI | 300 or 600 | UNRESOLVED | Export context |
| PDF font type | 42 | MEDIUM-HIGH | Publication |
| SVG | no default | LOW / insufficient | Export |
| PDI semantic palette | Me `#D55E00`; H `#0072B2`; OMe `#7A5195` | HIGH | PDI comparisons only |
| General palette | no candidate | UNRESOLVED | Base |
| Units | quantity + units in parentheses; math superscripts/subscripts | MEDIUM | Scientific labels |
| Decimals/scientific notation | measurement-specific | UNRESOLVED | Per axis/annotation |

## 20. Recommended Phase-2 architecture

Use one `base-publication` profile plus one evidence-backed `compact-diagnostic` override. Keep multipanel geometry/layout as composable options rather than a fully canonical profile until the user reviews the LOW-confidence values.

Recommended separation of concerns:

1. **Base visual profile** — Arial-first font stack, 22/14/18 bold hierarchy, boxed 1.8 spines, inward ticks, white/black ground, framed bold legend, 8 × 6 geometry, grid off.
2. **Compact diagnostic override** — smaller 13–14 axis labels, 10 ticks, 14–16 titles, 9 legends; geometry remains caller-selected.
3. **Layout policy** — tight for ordinary figures, constrained for dense/multipanel figures; no hard-coded universal subplot spacing.
4. **Export policy** — tight bounds and opaque white raster are safe to encode. DPI must remain an explicit reviewed option (300 or 600). Paired PDF+PNG should be a final/manuscript option, not forced for every diagnostic.
5. **Semantic colour registry** — encode the PDI triad only behind explicit PDI identities. Do not invent or generalise a palette.
6. **Artist-role helpers** — reference lines and error bars may receive evidence-backed defaults; scatter alpha, marker edges, minor ticks, top/right ticks, and decimal formatting must remain caller/context controlled until reviewed.

Rules sufficiently supported for programmatic encoding now: Arial-first family, role font sizes/weights, white/black ground, all 1.8 pt spines, inward 1.8 pt major ticks, framed bold legends, 8 × 6 base size, grid off as a MEDIUM rule, tight layout/bounds, opaque white raster, dashed neutral reference lines, and the PDI semantic triad under a narrow scope.

Rules that Phase 2 must not silently encode: global font size, tick lengths, minor-tick presence/geometry, top/right ticks, one universal line/marker edge/alpha value, one universal DPI, vector transparency, universal title visibility, universal legend location, a general palette, or one decimal-formatting policy.

**Phase-1 verdict: READY FOR STYLE REVIEW.** Human review should resolve the explicit conflicts before any final `SKILL.md` or reusable plotting module is created.
