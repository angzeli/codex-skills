# GENERATED FILE — DO NOT EDIT.
# Source schema: synthetic-api-v1

from __future__ import annotations


class SyntheticClient:
    def __init__(self, endpoint: str) -> None:
        self.endpoint = endpoint

    def get_run(self, run_id: str) -> dict[str, str]:
        return {"endpoint": self.endpoint, "run_id": run_id}
