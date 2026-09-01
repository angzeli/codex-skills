"""Structural acceptance check for the synthetic notebook."""

import json
from pathlib import Path


notebook = json.loads(Path("tutorial.ipynb").read_text(encoding="utf-8"))
assert notebook["nbformat"] == 4
assert notebook["metadata"] == {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "synthetic": True,
}
markdown, code = notebook["cells"]
assert markdown["id"] == "instruction-cell"
assert markdown["metadata"] == {"synthetic": True}
assert markdown["source"] == ["Call `square(3)` to obtain 9.\n"]
assert code["id"] == "code-cell"
assert code["execution_count"] == 1
assert code["source"] == [
    "def square(value):\n",
    "    return value * value\n",
    "\n",
    "square(3)",
]
assert code["outputs"] == [
    {
        "data": {"text/plain": ["9"]},
        "execution_count": 1,
        "metadata": {},
        "output_type": "execute_result",
    }
]
