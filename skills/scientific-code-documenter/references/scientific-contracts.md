# Scientific contract inventory

Use this reference when documentation depends on data meaning, units, shapes, schemas, ordering, missing values, state, or interfaces. Record only items relevant to the requested scope.

## Evidence classes

### Evidence-backed

Repository evidence establishes the contract:

```python
def absorbance(intensity: np.ndarray) -> np.ndarray:
    """Return dimensionless absorbance in the input wavelength order."""
```

Use this wording only when tests, schemas, labels, types, documentation, or authoritative nearby code establish both the quantity and ordering.

### Observable-only

The operation is visible, but the scientific intent is not:

```python
# Preserve the configured scaling operation; the source and target units are not documented.
scaled = signal * scale_factor
```

Do not turn multiplication by a familiar factor into an unsupported unit conversion.

### Unknown

No reliable contract can be established. Preserve the behavior, state the gap, and request expert confirmation. Do not invent units, physical roles, value ranges, sentinel meanings, or provenance.

## Contract checklist

- **Scientific meaning:** measured, calculated, fitted, simulated, raw, processed, absolute, or relative only when established.
- **Units:** record source and target units and the conversion point. If either is unknown, document only the operation.
- **Shapes:** include rank, axis order, and alignment rules where evidence supports them.
- **Schemas:** preserve column names, types, optional fields, and serialization order.
- **Ordering:** preserve row, column, iteration, and output ordering when positional consumers or tests depend on it.
- **Missing values:** distinguish rejection, propagation, imputation, and sentinel handling only from evidence.
- **State dependencies:** identify required prior calls, cells, mutable globals, seeds, files, environment variables, and working directories.
- **Interfaces:** preserve public symbols, exceptions, files, paths, formats, side effects, and output artifacts.

## Safe wording patterns

```python
"""Return values with the same shape and row order as `samples`."""
```

Use when shape and ordering are tested.

```python
# Values equal to the configured sentinel follow the existing exclusion branch.
```

Use when the effect is observable but the sentinel's scientific meaning is unknown.

```python
# Expert confirmation required: the repository does not identify this factor's units or provenance.
```

Use in a review finding, not as a noisy inline comment, when no safe code wording is needed.
