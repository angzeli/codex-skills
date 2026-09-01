# Synthetic CSV migration

Migrate version-1 rows with columns `label,value` to version 2 with columns `sample_id,label,value_ev`.

- Preserve row order and every value byte.
- Generate `sample_id` as `row-001`, `row-002`, and so on.
- Write to a separate output path.
- Reject malformed input before creating or replacing output.
- Keep `read_v1` backward compatible.

All data is invented and public-safe.
