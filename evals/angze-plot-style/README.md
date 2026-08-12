# Angze plot style spectral A/B evaluation

- **A**: ordinary Matplotlib with no plotting skill.
- **B**: ordinary self-contained Matplotlib using only
  `skills/angze-plot-style/SKILL.md` as the style treatment.

The inputs are `data/ir.csv`, `data/uv_vis.csv`, and `data/xrd.csv`. Each file
contains three paired PDI x/y series. The shared `common.py` fixes only parsing,
series identities, labels, and the conventional decreasing IR wavenumber axis.
No smoothing, normalization, offset, baseline correction, or peak annotation is
applied.

## Rerun

From the repository root, using a Python environment with Matplotlib:

```bash
MPLBACKEND=Agg python3 evals/angze-plot-style/renderers/baseline/render.py
MPLBACKEND=Agg python3 evals/angze-plot-style/renderers/skill/render.py
python3 evals/angze-plot-style/prepare_comparison.py
```

Condition outputs are under `outputs/A_baseline/` and `outputs/B_skill/`; the
six review PNGs are under `outputs/comparison/`. Generated outputs are ignored
by Git but remain local for inspection.

B does not import `angze_plot_style.py`, alter `sys.path`, or depend on the
skill references/assets/forensics. No other plotting skill was intentionally
read or used for this evaluation.

Isolation limitation: this evaluation was run in a conversation that had
already exposed `angze-plot-style` during earlier skill-development tasks.
Although A was completed and hash-frozen before `SKILL.md` was opened during
this evaluation run, the comparison is not strictly blinded.
