# Comment and docstring examples

These synthetic examples illustrate comment quality, not a mandatory house style. Follow coherent repository conventions first.

## Python docstrings, units, and shapes

Prefer a concise contract that records scientific meaning:

```python
def absorbance(transmitted: np.ndarray, incident: np.ndarray) -> np.ndarray:
    """Return base-10 absorbance for paired intensity samples.

    Args:
        transmitted: Detector intensity in counts, shape `(n_wavelengths,)`.
        incident: Reference intensity in counts with the same shape.

    Returns:
        Dimensionless absorbance values in input wavelength order.

    Raises:
        ValueError: If shapes differ or either array contains non-positive values.
    """
```

Avoid padding the contract with syntax narration:

```python
def absorbance(transmitted, incident):
    """This function is responsible for taking two arrays and returning an array."""
```

## Logical stages and inline decisions

Prefer comments that expose intent or a constraint:

```python
# Convert wavelengths to metres before evaluating the photon-energy relation.
wavelength_m = wavelength_nm * 1e-9

# Keep input row order because spectrum labels are positional downstream.
selected = samples.loc[accepted_mask]
```

Avoid narrating individual statements:

```python
# Multiply by one billion.
wavelength_nm = wavelength_m * 1e9
# Create a mask.
accepted_mask = residuals < limit
```

## Unknown scientific meaning

Do not guess at an undocumented correction:

```python
# Apply the legacy correction exactly; its physical basis is not documented here.
corrected = signal - 0.037 * reference
```

Do not invent provenance or interpretation:

```python
# Remove the calibrated solvent contribution reported by Smith et al.
corrected = signal - 0.037 * reference
```

## Protected thresholds

An unusual, test-protected value may deserve a named constant without changing it:

```python
# Preserve the historical acceptance boundary used by archived campaign outputs.
MAX_RELATIVE_RESIDUAL = 0.073
```

Do not round it to a more familiar value or claim a statistical basis that is absent.

## HTML structure

Use a structural comment only when it helps navigate a substantial region:

```html
<!-- Calibration summary shared by screen and print layouts. -->
<section class="calibration-summary" aria-labelledby="calibration-heading">
```

Avoid commenting every element:

```html
<!-- Heading -->
<h2>Calibration</h2>
<!-- Paragraph -->
<p>Reference scan complete.</p>
```

## Shell workflow

Document assumptions and major stages:

```sh
# Run from the campaign directory; the solver writes relative checkpoint paths.
cd "$campaign_dir"

# Resume each independent temperature job from its matching checkpoint.
for checkpoint in checkpoints/*.chk; do
    solver --resume "$checkpoint" --output results/
done
```

Avoid comments that merely translate shell syntax, and do not add strict mode without checking its effect on optional commands and pipelines.

## LaTeX macros and template constraints

Explain a non-obvious compatibility workaround:

```tex
% The publisher class measures captions before applying the final column width.
% Delay the width override until the figure environment is active.
\newcommand{\setfigurewidth}{\setlength{\figwidth}{\linewidth}}
```

Do not annotate ordinary commands such as `\section`, `\label`, or `\cite`.

## Trivial code and repetitive voice

This helper is clear without a long docstring or inline comments:

```python
def kelvin_to_celsius(temperature_k: float) -> float:
    """Convert kelvin to degrees Celsius."""
    return temperature_k - 273.15
```

Avoid repetitive generated-sounding prose such as “This function is responsible for,” “This block handles,” “Here, we,” and repeated “This ensures that” statements.
