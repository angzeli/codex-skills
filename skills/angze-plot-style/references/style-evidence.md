# Evidence and decision ledger

This ledger separates mined evidence from the user's Phase-2 canonical choices.
Future forensic re-mining may add or strengthen `FORENSIC` evidence, but it must
not erase or silently replace a `USER_DECISION`. Only an explicit later user
decision can supersede one.

Labels:

- `FORENSIC`: directly supported without resolving a meaningful conflict.
- `USER_DECISION`: an explicit Phase-2 choice, including a rule not established
  strongly enough by mining alone.
- `FORENSIC + USER_DECISION`: evidence supports a family or competing values,
  and the user selected the canonical value or scope.

## Canonical rule ledger

| Rule | Basis | Evidence or decision |
|---|---|---|
| Arial-first sans serif | `FORENSIC` | Explicit in 15 files across PDI calculation, PDI data, and XPS; the fallback stack preserves this preference when Arial is unavailable. |
| STIX Sans math | `FORENSIC + USER_DECISION` | Present in current PDI helpers; Phase 1 found competing math fontsets, and the user selected STIX Sans. |
| No global `font.size` | `FORENSIC + USER_DECISION` | Most repositories style roles directly; only XPS supplied a global 14. The user rejected a canonical global size. |
| Labels 22 bold | `FORENSIC + USER_DECISION` | 124 size uses across 30 files and 8 repositories; bold across 34 files and 9 repositories. |
| Ticks 14 bold | `FORENSIC + USER_DECISION` | 43 size uses across 30 files and 8 repositories, with broad explicit bold styling. |
| Titles 18 bold when present | `FORENSIC + USER_DECISION` | 61 size uses across 19 files and 7 repositories; title visibility was context-dependent. |
| Title absent by default | `USER_DECISION` | Mining split manuscript panels from diagnostic/tutorial titles; the user selected title-free default behavior while retaining the capability. |
| Legend 10 bold | `FORENSIC + USER_DECISION` | Size 10 was broadest; 11 and 12 were credible alternatives. The user selected 10. |
| Annotation 9–10 bold | `FORENSIC + USER_DECISION` | Compact bold annotations recurred across 25 files and 8 repositories; profile selects 10 base and 9 diagnostic. |
| White ground, black foreground | `FORENSIC + USER_DECISION` | Repeated current helpers explicitly force white figure/axes/export grounds and black axes/text. |
| Four visible black spines, 1.8 pt | `FORENSIC + USER_DECISION` | Width 1.8 appeared in 44 observations across all 10 mined repositories; explicit four-spine visibility was narrower but intentional. |
| Grid off | `FORENSIC + USER_DECISION` | Explicitly disabled by recent final-style helpers; Phase 1 classified avoidance as plausible negative evidence. The user made it canonical. |
| Inward major ticks, width 1.8 | `FORENSIC + USER_DECISION` | Inward direction recurred in 17 files/4 repositories and 1.8 width in 19 files/5 repositories. |
| Major length 4; bottom/left only | `USER_DECISION` | Phase 1 found lengths 4, 6, and 7 and conflicting top/right placement. The user selected 4 and disabled top/right ticks by default. |
| Minor ticks off | `USER_DECISION` | Presence and geometry were unresolved across spectra and electrochemistry. The user selected off with explicit caller override. |
| Figure size `(8, 6)` | `FORENSIC + USER_DECISION` | 31 occurrences across 18 files and 9 repositories; the user selected it as the default. |
| Prefer standalone figures | `USER_DECISION` | The user selected separate figures over a giant multipanel unless panels are required. |
| Tight simple / constrained dense | `FORENSIC + USER_DECISION` | Both layout patterns were recurring and context-linked; the user fixed their intended scopes. |
| Data line width 2.0 | `FORENSIC + USER_DECISION` | Broadest value: 25 uses across 14 files and 6 repositories; 2.2 and 2.4 remain context alternatives. |
| No universal alpha or scatter size | `FORENSIC + USER_DECISION` | Wide, role-dependent distributions; the user kept both context-controlled. |
| Error-bar caps 4; line 1.4 | `FORENSIC + USER_DECISION` | Caps 4 recurred in three repositories; 1.4 is the current PDI time-course value within the observed 1.4–1.5 band. |
| Neutral dashed reference lines | `FORENSIC + USER_DECISION` | Dashed neutral references recur broadly, but exact colour/width varies. The user selected the neutral dashed rule without a universal width. |
| Framed, opaque white legend | `FORENSIC + USER_DECISION` | Framed bold legends and white/black styling recur broadly; the user fixed opacity and the inside-axes placement order. |
| No legend when unnecessary | `USER_DECISION` | Scientific-content policy, not a scalar mining result. |
| PDI semantic colours | `FORENSIC + USER_DECISION` | The exact triad recurred in 7 files across the independent calculation and data repositories; the user restricted it to exact PDI identities. |
| Quantity plus units in parentheses | `FORENSIC + USER_DECISION` | Repeated scientific labels use parenthetical units, math super/subscripts, and direct degree/angstrom symbols; no universal precision rule. |
| PNG and PDF only, paired by default | `FORENSIC + USER_DECISION` | Paired output was established in PDI/XPS, while other formats and single-format diagnostics existed. The user excluded other formats by default. |
| 600 dpi, tight, opaque white | `FORENSIC + USER_DECISION` | Tight bounds and white opaque raster were strong; 300 versus 600 and vector transparency conflicted. The user selected 600 and opaque white for both outputs. |
| Base + manuscript policy + diagnostic override | `FORENSIC + USER_DECISION` | Base/publication and compact diagnostic families were supported; the user separated stable DNA from final-output policy and declined a broad presentation profile. |
| Specification-first dependency contract | `USER_DECISION` | `SKILL.md` is sufficient for normal self-contained Matplotlib generation. The Python asset is an optional reference implementation and validation fixture, not a cross-repository runtime dependency. |

## Targeted PDI marker audit

Audit snapshot: `pdi-calculation` at `1c02a841cce28ded67ed2afe0084d78ba10b4938`
and `pdi-data` at `b293c9b28f10be73f7a40e2d434320191fb5453a`.
Only tracked source was inspected; neither repository was modified.

The canonical general marker is `FORENSIC + USER_DECISION`: circle, 5.5 pt,
filled with the series colour, black 0.8 pt edge. The strongest reusable source
is `pdi-calculation:python/sterics/figure_style.py`, which centralizes
`MARKER_SIZE = 5.5` and `MARKER_EDGE_WIDTH = 0.8`. Final profile and branch
figures establish the circular filled geometry; branch series and the original
scan overlay explicitly use the black 0.8 pt edge, while one profile inherits a
same-colour edge. The user selected black as the deterministic general edge:

- `python/sterics/plot_steric_profiles.py::_profile_figure` (same-colour edge);
- `python/sterics/summarize_ome_branch_resolved.py::_plot_branch_series`;
- `python/sterics/summarize_ome_branch_resolved.py::render_figures`.

The following are intentional role alternatives, not votes against the general
default:

- `pdi-data:h2o2_production/h2o2_utility.py::plot_time_courses` uses 6.5 pt
  filled circles with white 0.7 pt edges for experimental error-bar series.
- The same function uses 7 pt white-centred circles with series-coloured 1.8 pt
  edges to distinguish open/control conditions.
- `pdi-data:eis/eis_utility.py::plot_eis` uses 4.5 pt circles with white 0.45 pt
  edges for dense impedance traces.
- `pdi-data:ms/ms_utility.py::plot_ms` uses similarly compact fit-point circles;
  diamond markers identify a distinct flat-band-potential role.
- Stars, triangles, squares, diamonds, and pentagons in steric figures encode
  minima, basins, branches, or descriptor roles and must remain caller-chosen.

Dense montages, diagnostic highlights, tests, and copied tutorial semantics were
not allowed to determine the general marker default.

## Phase-1 source

The granular observation trail remains in
`../forensics/style-evidence.json`; the narrative analysis remains in
`../forensics/style-mining-report.md`. Those files are evidence records, not
canonical runtime configuration.
