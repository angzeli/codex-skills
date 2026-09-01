# Synthetic file-locking fixture

`counter.py` deliberately performs a non-atomic read/modify/write against a shared text file. Repair lost updates with a lock covering the complete critical section. Keep the fixture local and deterministic; it contains no real user data.
