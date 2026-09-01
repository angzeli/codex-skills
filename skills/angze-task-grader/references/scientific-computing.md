# Scientific-computing risk guide

Apply this guide when code can affect scientific results, numerical meaning, structures, workflow provenance, or expensive calculations. Increase validation depth without automatically increasing patch size.

## General contract

- Establish units, signs, reference states, array shapes, axis order, indexing, tolerances, and provenance from code, tests, schemas, documentation, or user instructions.
- Preserve the distinction between process success and scientific validity.
- Prefer minimized, synthetic, or already-authorized fixtures.
- Never launch expensive scientific calculations without explicit authorization.
- Treat plausible-looking output as insufficient. Check invariants and authoritative expectations.
- Keep the implementation localized when the defect is localized, even when validation is T3-depth.

## ORCA output parsing

- Distinguish normal program termination from optimization convergence, frequency validity, and the requested calculation target.
- Match parsed artifacts to the intended attempt, input, method, charge, multiplicity, and geometry lineage.
- Test truncated output, restarted jobs, multiple termination markers, failed optimization, missing sections, locale/spacing variants, and scientific notation where relevant.
- Do not infer that one electronic-structure method is higher level solely from a label or ordering.
- Use small synthetic output excerpts; do not run ORCA unless explicitly authorized.

## Multiwfn workflows

- Preserve menu/input sequencing, file selection, working-directory assumptions, output naming, and failure detection.
- Distinguish successful process exit from scientifically complete output.
- Validate expected artifact identity and provenance with synthetic or authorized small inputs.
- Do not assume interactive defaults are stable across versions.

## ASE structures and units

- Verify whether coordinates are Cartesian or fractional, the cell and periodic boundary conditions, atom ordering, constraints, and length/energy units.
- Preserve array shapes, indices, component identity, and coordinate frames.
- Test rigid transformations with distance and orientation invariants, not visual plausibility alone.
- Do not infer charge, spin, bonding, or molecular identity from geometry unless explicitly established.

## VASP inputs and defaults

- Treat defaults affecting functional, cutoff, k-points, smearing, spin, charge, convergence, symmetry, dispersion, or restart behavior as scientific hard triggers.
- Compare resolved inputs, not only source templates.
- Validate units, default precedence, restart artifacts, and compatibility with existing workflows.
- Never launch a production calculation merely to validate input generation.

## Energies and sign conventions

- Write the defining equation beside test fixtures.
- Identify the reference state and whether a reported value is interaction, binding, adsorption, association, deformation, reaction, or formation energy.
- Test a hand-computable synthetic example with a sign-sensitive expected value.
- Preserve unit conversions and energy-reference provenance.
- Do not rename an energy quantity to a familiar convention without evidence.

## Geometry and coordinate transformations

- Specify origin, frame, handedness, rotation convention, angle units, axis order, and whether transformations are active or passive.
- Test distances, centroids, determinant/orthogonality, periodic wrapping, and round trips as applicable.
- Preserve atom ordering and constraints.

## Convergence and thresholds

- Distinguish parser-detected termination, algorithmic convergence, and scientific acceptance.
- Treat changes to tolerances, thresholds, iteration limits, and defaults as scientific risk.
- Test values just below, at, and above thresholds using explicit comparison semantics.
- Avoid exact equality for floating-point behavior unless the contract requires it.

## Spin, charge, and multiplicity

- Require caller-supplied or source-backed metadata when these values affect a converter or workflow.
- Validate consistency constraints and surface requested versus resolved choices.
- Do not infer formal charge or multiplicity from element counts or geometry.

## Numerical tolerances

- Choose absolute, relative, or combined tolerances based on the established scale and algorithm.
- Record why a tolerance protects the contract; do not loosen it merely to pass a test.
- Include zero, sign change, boundary, large/small magnitude, and non-finite cases when relevant.
- Preserve evaluation order when floating-point reproducibility matters.

## Provenance, paths, and restarts

- Treat source identity, input/output paths, attempt IDs, hashes when truly required, restart files, resolved defaults, software versions, and parameter lineage as part of correctness.
- Verify that an output belongs to the requested target and attempt before accepting it.
- Keep active queues and in-progress calculations under their current owner; do not hot-swap inputs.
- Use hashes only when identity or immutable provenance is part of the task.

## Expensive calculations

- Separate code correctness, process health, and scientific validity.
- Prefer unit tests, minimized fixtures, dry runs, input validation, and previously authorized outputs.
- State clearly when production-scale numerical validation remains unrun.
- Request authorization before consuming meaningful compute, replacing live inputs, resuming a campaign, or writing to external scientific systems.
