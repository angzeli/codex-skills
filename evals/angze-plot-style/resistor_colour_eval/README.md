# Resistor colour-policy A/B evaluation

The source is `../data/resistor_repeats5_20260122_201801.csv`: one shared
51-point `Voltage (V)` column followed by five repeat-current columns and their
average, all in mA. Source order is retained as Run 1, Run 2, Run 3, Run 4,
Run 5, and Average (`S1`–`S6`). The numerical data are plotted without
smoothing, interpolation, normalization, offset, baseline correction, or
rescaling.

- **A**: ordinary Matplotlib with no plotting skill.
- **B**: self-contained Matplotlib using only
  `skills/angze-plot-style/SKILL.md` as the plotting-style treatment.

Scenario 1 plots all six source series as unrelated categories. Scenario 2
plots the unchanged non-contiguous identities S1, S3, S5, and S6. Scenario 3
reuses the same six numerical series as evaluation-only `Level 1` through
`Level 6` values of one identity; these are not claimed to be real ordered
experimental conditions. Every figure includes the explicitly requested
`y = 0` reference line.

## Rerun

From the repository root, using a Python environment with Matplotlib:

```bash
python_bin=${ANGZE_PLOT_STYLE_PYTHON:-python3}
for renderer in categorical6 subset4 ordered6; do
    MPLBACKEND=Agg "$python_bin" \
        "evals/angze-plot-style/resistor_colour_eval/renderers/baseline/${renderer}.py"
done
for renderer in categorical6 subset4 ordered6; do
    MPLBACKEND=Agg "$python_bin" \
        "evals/angze-plot-style/resistor_colour_eval/renderers/skill/${renderer}.py"
done
"$python_bin" evals/angze-plot-style/resistor_colour_eval/prepare_comparison.py
```

Condition outputs are in `outputs/A_baseline/` and `outputs/B_skill/`; the six
primary review copies are in `outputs/comparison/`. Outputs are ignored by Git
but remain local. B does not import the optional Python helper or depend on the
skill references, assets, or forensics.

Isolation limitation: the surrounding conversation had already exposed and
maintained `angze-plot-style` in earlier tasks. A was nevertheless completed
and hash-frozen before `SKILL.md` was reopened during this evaluation run, but
the experiment is not strictly blinded.
