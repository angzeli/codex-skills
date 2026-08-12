#!/usr/bin/env python3
"""Extract traceable Matplotlib style evidence from a curated local corpus.

The extractor is deliberately static: it reads tracked Python and notebook code,
never imports project modules, and never executes plotting or scientific code.
"""

from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
from datetime import date
import fnmatch
import json
from pathlib import Path
import re
import subprocess
from typing import Any, Iterable


PLOT_TOKENS = (
    "matplotlib",
    "seaborn",
    "plt.",
    ".plot(",
    ".scatter(",
    ".errorbar(",
    ".bar(",
    "savefig",
    "figsize",
    "tick_params",
    "rcparams",
)


@dataclass(frozen=True)
class RepositorySpec:
    name: str
    home_relative_path: str
    included: bool
    include_globs: tuple[str, ...] = ("*.py", "*.ipynb", "**/*.py", "**/*.ipynb")
    exclude_globs: tuple[str, ...] = ()
    provenance: str = "likely-user-authored"
    context: str = "scientific"
    notes: str = ""

    @property
    def path(self) -> Path:
        return Path.home() / self.home_relative_path

    @property
    def display_path(self) -> str:
        return f"~/{self.home_relative_path}"


REPOSITORIES = (
    RepositorySpec(
        "pdi-calculation",
        "Desktop/Tsinghua 2026 Summer/pdi_h2o2_production/calculation",
        True,
        exclude_globs=("**/tests/**",),
        provenance="high",
        context="manuscript-analysis",
        notes="Recent research analysis; tracked plotting notebooks and shared helpers.",
    ),
    RepositorySpec(
        "pdi-data",
        "Desktop/Tsinghua 2026 Summer/pdi_h2o2_production/data",
        True,
        exclude_globs=("**/test_*.py",),
        provenance="high",
        context="manuscript-experimental",
        notes="Independent experimental techniques with a repeated publication template.",
    ),
    RepositorySpec(
        "xps-workbench",
        "Desktop/squiddy tools/xps-fitting-workbench",
        True,
        include_globs=(
            "src/xps_fitting/plotting/*.py",
            "src/xps_fitting/publication.py",
            "examples/plot_pdi_h_cooh_c1s_publication.py",
            "xps_vgd_utils.py",
        ),
        provenance="high",
        context="publication-tooling",
        notes="Current non-duplicate workbench with an explicit angze_publication theme.",
    ),
    RepositorySpec(
        "bo-forge",
        "Desktop/bo_forge",
        True,
        include_globs=(
            "bo_forge/plot_style.py",
            "bo_forge/diagnostics.py",
            "notebooks/*.ipynb",
        ),
        provenance="high",
        context="diagnostic-tutorial",
        notes="Shared report-ready helper plus campaign diagnostics; tests and app UI excluded.",
    ),
    RepositorySpec(
        "ising-coursework",
        "Desktop/Imperial/Year 25-26/26 Summer/imperial-complab-monte-carlo-simulations-of-a-2d-ising-model",
        True,
        include_globs=("python_script/*.py",),
        provenance="high",
        context="scientific-coursework",
        notes="Independent scientific project with a local publication-style helper.",
    ),
    RepositorySpec(
        "pdi-theory-demo",
        "Desktop/Tsinghua 2026 Summer/pdi_h2o2_production/pdi-theory-demo",
        True,
        include_globs=("analysis/*.ipynb",),
        provenance="medium",
        context="scientific-tutorial",
        notes="Tracked analysis notebooks only; active untracked work was not mined.",
    ),
    RepositorySpec(
        "fyp-zis-photocatalysis",
        "Desktop/Imperial/Year 25-26/26 Summer/fyp-zis-photocatalysis",
        True,
        include_globs=("gaussian/scripts/visualise_gaussian_results.py",),
        provenance="high",
        context="diagnostic-report",
        notes="One user-authored Gaussian report generator; treated as one independent source.",
    ),
    RepositorySpec(
        "tdqms-coursework",
        "Desktop/Imperial/Year 25-26/26 Spring/Time-dependent Quantum Mechanics and Spectroscopy/Coursework",
        True,
        include_globs=("tdqms_plotting.py", "TDQMS_notebook_part_2.ipynb"),
        provenance="high",
        context="scientific-coursework",
        notes="Local plotting helper and its consuming notebook.",
    ),
    RepositorySpec(
        "opentrons-screening",
        "Desktop/Imperial/Year 25-26/26 Summer/Emerging Technologies/Opentrons OT-2 liquid handling platform/opentrons_macrocycle_screening",
        True,
        include_globs=("calibration/calibration_curve.ipynb",),
        provenance="high",
        context="experimental-calibration",
        notes="Two related calibration plots in one notebook; counted as one independent file.",
    ),
    RepositorySpec(
        "pytorch-to-bo",
        "Desktop/Experiences/from-pytorch-to-bayesian-optimisation",
        True,
        include_globs=("part_6/tutorial_*.ipynb",),
        exclude_globs=("**/worked/**",),
        provenance="medium",
        context="tutorial",
        notes="Only the four advanced source tutorials; worked duplicates excluded.",
    ),
    RepositorySpec(
        "ase-learning",
        "Desktop/Experiences/ase_learning",
        False,
        provenance="low",
        context="external-tutorial",
        notes="Excluded: files explicitly identify as official ASE tutorials; personal-style provenance is weak.",
    ),
    RepositorySpec(
        "qchem-workbench",
        "Desktop/Experiences/qchem_workbench",
        False,
        provenance="high",
        context="generic-library-output",
        notes="Excluded: plotting functions intentionally use near-default Matplotlib for utilitarian output.",
    ),
    RepositorySpec(
        "data-foundations",
        "Desktop/squiddy tools/data-foundations-with-numpy-and-pandas",
        False,
        provenance="medium",
        context="teaching-example",
        notes="Excluded: plotting snippets teach data preparation rather than define final visual identity.",
    ),
    RepositorySpec(
        "market-criticism-index",
        "Desktop/squiddy tools/market-criticism-index",
        False,
        provenance="high",
        context="one-off-finance-diagnostic",
        notes="Excluded: one plotting function, grid enabled, 160 dpi; insufficient scientific-style recurrence.",
    ),
    RepositorySpec(
        "xps-workbench-older-copy",
        "Desktop/squiddy tools/experimental_data_analysis/xps-fitting-workbench",
        False,
        provenance="high",
        context="duplicate-repository",
        notes="Excluded: older duplicate lineage of the current XPS workbench; not independent evidence.",
    ),
)


ALIASES = {
    "lw": "linewidth",
    "ms": "markersize",
    "mew": "markeredgewidth",
    "ls": "linestyle",
}

CONSTANT_PARAMETERS = {
    "FIGSIZE": "figure_size",
    "SINGLE_PANEL_SIZE": "figure_size.single_panel",
    "TWO_PANEL_STACK_SIZE": "figure_size.two_panel_stack",
    "THREE_PANEL_STACK_SIZE": "figure_size.three_panel_stack",
    "FOUR_PANEL_GRID_SIZE": "figure_size.four_panel_grid",
    "AXIS_LABEL_SIZE": "axis_label_fontsize",
    "LABEL_SIZE": "axis_label_fontsize",
    "TICK_LABEL_SIZE": "tick_label_fontsize",
    "TICK_SIZE": "tick_label_fontsize",
    "TITLE_LABEL_SIZE": "title_fontsize",
    "TITLE_SIZE": "title_fontsize",
    "LEGEND_FONT_SIZE": "legend_fontsize",
    "LEGEND_SIZE": "legend_fontsize",
    "SPINE_WIDTH": "spine_width",
    "LINE_WIDTH": "line_width",
    "MARKER_SIZE": "marker_size",
    "MARKER_EDGE_WIDTH": "marker_edge_width",
    "BAR_EDGE_WIDTH": "bar_edge_width",
    "COLORBAR_LABEL_SIZE": "colorbar_label_fontsize",
    "COLORBAR_TICK_SIZE": "colorbar_tick_fontsize",
}

THEME_FIELD_PARAMETERS = {
    "font_family": "font_family",
    "font_size": "global_fontsize",
    "axis_label_size": "axis_label_fontsize",
    "tick_label_size": "tick_label_fontsize",
    "tick_label_weight": "tick_label_fontweight",
    "title_size": "title_fontsize",
    "spine_width": "spine_width",
    "tick_width": "tick_width",
    "tick_length": "tick_length",
    "minor_tick_width": "minor_tick_width",
    "minor_tick_length": "minor_tick_length",
    "tick_direction": "tick_direction",
    "marker_size": "marker_size",
    "marker_edge_width": "marker_edge_width",
    "fit_line_width": "fit_line_width",
    "background_line_width": "background_line_width",
    "background_line_style": "background_line_style",
    "component_line_width": "component_line_width",
    "component_alpha": "component_alpha",
    "legend_frame": "legend_frameon",
    "legend_font_size": "legend_fontsize",
    "legend_font_weight": "legend_fontweight",
    "legend_frame_alpha": "legend_framealpha",
    "legend_frame_linewidth": "legend_frame_linewidth",
    "legend_fancybox": "legend_fancybox",
    "legend_spacing": "legend_spacing",
    "axis_padding": "axis_labelpad",
    "figure_size": "figure_size",
    "vertical_headroom": "vertical_headroom_fraction",
    "dpi": "export_dpi",
    "panel_label_template": "panel_label_template",
    "show_title": "show_title",
    "top_spine": "top_spine_visible",
    "right_spine": "right_spine_visible",
    "raster_transparent": "raster_transparent",
    "vector_transparent": "vector_transparent",
}


def run_git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.rstrip("\n")


def tracked_code_files(spec: RepositorySpec) -> list[Path]:
    names = run_git(spec.path, "ls-files", "*.py", "*.ipynb").splitlines()
    return [spec.path / name for name in names]


def notebook_code(path: Path) -> list[tuple[int, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [
        (index, "".join(cell.get("source", [])))
        for index, cell in enumerate(data.get("cells", []))
        if cell.get("cell_type") == "code"
    ]


def file_plot_source(path: Path) -> tuple[str, list[tuple[int | None, str]]]:
    if path.suffix == ".ipynb":
        cells = notebook_code(path)
        return "notebook", cells
    return "python", [(None, path.read_text(encoding="utf-8"))]


def is_plotting_source(source: str) -> bool:
    lower = source.lower()
    return any(token in lower for token in PLOT_TOKENS)


def selected(spec: RepositorySpec, relative: str) -> bool:
    included = any(fnmatch.fnmatch(relative, pattern) for pattern in spec.include_globs)
    excluded = any(fnmatch.fnmatch(relative, pattern) for pattern in spec.exclude_globs)
    return included and not excluded


def literal(node: ast.AST, constants: dict[str, Any]) -> tuple[Any, bool]:
    if isinstance(node, ast.Name) and node.id in constants:
        return constants[node.id], True
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
        value, resolved = literal(node.operand, constants)
        if resolved and isinstance(value, (int, float)):
            return (-value if isinstance(node.op, ast.USub) else value), True
    if isinstance(node, (ast.Constant, ast.Tuple, ast.List, ast.Set, ast.Dict)):
        try:
            return ast.literal_eval(node), True
        except (ValueError, TypeError):
            pass
    try:
        return ast.unparse(node), False
    except Exception:
        return "<unresolved>", False


def collect_constants(tree: ast.AST) -> dict[str, Any]:
    constants: dict[str, Any] = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            value_node = node.value
            if value_node is None:
                continue
            value, resolved = literal(value_node, constants)
            if not resolved:
                continue
            for target in targets:
                if isinstance(target, ast.Name):
                    constants[target.id] = value
    return constants


def call_name(node: ast.Call) -> str:
    try:
        return ast.unparse(node.func)
    except Exception:
        return "<call>"


def clean_notebook_source(source: str) -> str:
    lines = []
    for line in source.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("%", "!", "?")):
            lines.append("pass")
        else:
            lines.append(line)
    return "\n".join(lines)


def normalized_parameter(call: str, original: str, call_keywords: dict[str, Any]) -> str:
    name = call.split(".")[-1]
    key = ALIASES.get(original, original)
    if name in {"set_xlabel", "set_ylabel"}:
        return {"fontsize": "axis_label_fontsize", "fontweight": "axis_label_fontweight", "labelpad": "axis_labelpad"}.get(key, f"axis_label.{key}")
    if name in {"set_title", "suptitle"}:
        return {"fontsize": "title_fontsize", "fontweight": "title_fontweight", "weight": "title_fontweight", "pad": "title_pad"}.get(key, f"title.{key}")
    if name == "tick_params":
        which = str(call_keywords.get("which", "major"))
        prefix = "minor_tick" if which == "minor" else "tick"
        return {
            "labelsize": "tick_label_fontsize",
            "width": f"{prefix}_width",
            "length": f"{prefix}_length",
            "direction": "tick_direction",
            "pad": "tick_pad",
            "top": "top_ticks_visible",
            "right": "right_ticks_visible",
        }.get(key, f"tick_params.{key}")
    if name == "legend":
        return {
            "fontsize": "legend_fontsize",
            "frameon": "legend_frameon",
            "fancybox": "legend_fancybox",
            "framealpha": "legend_framealpha",
            "loc": "legend_location",
            "facecolor": "legend_facecolor",
            "edgecolor": "legend_edgecolor",
            "labelspacing": "legend_labelspacing",
            "handlelength": "legend_handlelength",
            "borderpad": "legend_borderpad",
            "columnspacing": "legend_columnspacing",
            "ncols": "legend_ncols",
        }.get(key, f"legend.{key}")
    if name in {"subplots", "figure"}:
        return {"figsize": "figure_size", "constrained_layout": "constrained_layout", "facecolor": "figure_facecolor"}.get(key, f"figure.{key}")
    if name == "savefig":
        return {"dpi": "export_dpi", "bbox_inches": "export_bbox_inches", "transparent": "export_transparent", "facecolor": "export_facecolor", "edgecolor": "export_edgecolor", "format": "export_format"}.get(key, f"export.{key}")
    if name in {"plot", "semilogx", "semilogy", "loglog"}:
        return {"linewidth": "line_width", "markersize": "marker_size", "markeredgewidth": "marker_edge_width", "alpha": "line_alpha", "color": "line_color", "linestyle": "line_style", "marker": "marker"}.get(key, f"line.{key}")
    if name == "scatter":
        return {"s": "scatter_size", "linewidth": "scatter_edge_width", "linewidths": "scatter_edge_width", "alpha": "scatter_alpha", "color": "scatter_color", "c": "scatter_color", "edgecolor": "scatter_edgecolor", "edgecolors": "scatter_edgecolor", "marker": "scatter_marker", "cmap": "scatter_cmap"}.get(key, f"scatter.{key}")
    if name == "errorbar":
        return {"linewidth": "errorbar_line_width", "markersize": "errorbar_marker_size", "markeredgewidth": "errorbar_marker_edge_width", "capsize": "errorbar_capsize", "elinewidth": "errorbar_elinewidth", "capthick": "errorbar_capthick", "alpha": "errorbar_alpha", "fmt": "errorbar_format", "color": "errorbar_color", "ecolor": "errorbar_ecolor"}.get(key, f"errorbar.{key}")
    if name in {"axhline", "axvline"}:
        return {"linewidth": "reference_line_width", "linestyle": "reference_line_style", "color": "reference_line_color", "alpha": "reference_line_alpha"}.get(key, f"reference_line.{key}")
    if name in {"annotate", "text"}:
        return {"fontsize": "annotation_fontsize", "fontweight": "annotation_fontweight", "weight": "annotation_fontweight", "ha": "annotation_horizontal_alignment", "va": "annotation_vertical_alignment", "arrowprops": "annotation_arrowprops"}.get(key, f"annotation.{key}")
    if name == "bar":
        return {"linewidth": "bar_edge_width", "edgecolor": "bar_edgecolor", "alpha": "bar_alpha", "color": "bar_color", "width": "bar_width"}.get(key, f"bar.{key}")
    if name in {"grid"}:
        return f"grid.{key}"
    if name in {"margins"}:
        return f"axis_margin.{key}"
    return key


class EvidenceVisitor(ast.NodeVisitor):
    def __init__(
        self,
        *,
        repository: RepositorySpec,
        relative_file: str,
        source_type: str,
        cell: int | None,
        constants: dict[str, Any],
    ) -> None:
        self.repository = repository
        self.relative_file = relative_file
        self.source_type = source_type
        self.cell = cell
        self.constants = constants
        self.symbols: list[str] = []
        self.observations: list[dict[str, Any]] = []

    @property
    def symbol(self) -> str | None:
        return ".".join(self.symbols) if self.symbols else None

    def add(
        self,
        node: ast.AST,
        *,
        call: str,
        parameter: str,
        original_parameter: str,
        value: Any,
        resolved: bool,
    ) -> None:
        self.observations.append(
            {
                "repository": self.repository.name,
                "file": self.relative_file,
                "source_type": self.source_type,
                "cell": self.cell,
                "line": getattr(node, "lineno", None),
                "symbol": self.symbol,
                "call": call,
                "parameter": parameter,
                "original_parameter": original_parameter,
                "value": value,
                "resolved": resolved,
                "context": self.repository.context,
                "provenance_confidence": self.repository.provenance,
                "independence_group": f"{self.repository.name}:{self.relative_file}",
            }
        )

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.symbols.append(node.name)
        self.generic_visit(node)
        self.symbols.pop()

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.symbols.append(node.name)
        if node.name == "PlotTheme":
            for item in node.body:
                if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name) and item.value is not None:
                    parameter = THEME_FIELD_PARAMETERS.get(item.target.id)
                    if parameter:
                        value, resolved = literal(item.value, self.constants)
                        self.add(
                            item,
                            call="PlotTheme.default",
                            parameter=parameter,
                            original_parameter=item.target.id,
                            value=value,
                            resolved=resolved,
                        )
        self.generic_visit(node)
        self.symbols.pop()

    def visit_Assign(self, node: ast.Assign) -> None:
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in CONSTANT_PARAMETERS:
                value, resolved = literal(node.value, self.constants)
                self.add(
                    node,
                    call="constant",
                    parameter=CONSTANT_PARAMETERS[target.id],
                    original_parameter=target.id,
                    value=value,
                    resolved=resolved,
                )
            if isinstance(target, ast.Name):
                value, resolved = literal(node.value, self.constants)
                colour_name = target.id.upper()
                if resolved and isinstance(value, str) and re.fullmatch(r"#[0-9A-Fa-f]{6}", value):
                    if "COLOR" in colour_name or "COLOUR" in colour_name:
                        self.add(
                            node,
                            call="colour_constant",
                            parameter=f"semantic_colour.{target.id}",
                            original_parameter=target.id,
                            value=value.upper(),
                            resolved=True,
                        )
                if resolved and isinstance(value, dict) and ("COLOR_MAP" in colour_name or "COLOUR_MAP" in colour_name):
                    self._add_colour_map(node, target.id, value)
        self.generic_visit(node)

    def _add_colour_map(self, node: ast.AST, name: str, value: dict[Any, Any], prefix: str = "") -> None:
        for key, item in sorted(value.items(), key=lambda pair: str(pair[0])):
            semantic_key = f"{prefix}.{key}" if prefix else str(key)
            if isinstance(item, dict):
                self._add_colour_map(node, name, item, semantic_key)
            elif isinstance(item, str) and re.fullmatch(r"#[0-9A-Fa-f]{6}", item):
                self.add(
                    node,
                    call="colour_map",
                    parameter=f"semantic_colour.{semantic_key}",
                    original_parameter=name,
                    value=item.upper(),
                    resolved=True,
                )

    def visit_Call(self, node: ast.Call) -> None:
        name = call_name(node)
        short = name.split(".")[-1]
        keyword_values: dict[str, Any] = {}
        for keyword in node.keywords:
            if keyword.arg is None:
                continue
            value, resolved = literal(keyword.value, self.constants)
            keyword_values[keyword.arg] = value
            parameter = normalized_parameter(name, keyword.arg, keyword_values)
            if short in {
                "set_xlabel", "set_ylabel", "set_title", "suptitle", "tick_params",
                "legend", "subplots", "figure", "savefig", "plot", "semilogx",
                "semilogy", "loglog", "scatter", "errorbar", "axhline", "axvline",
                "annotate", "text", "bar", "grid", "margins",
            }:
                self.add(
                    keyword,
                    call=name,
                    parameter=parameter,
                    original_parameter=keyword.arg,
                    value=value,
                    resolved=resolved,
                )

        if name.endswith("rcParams.update") and node.args:
            mapping, mapping_ok = literal(node.args[0], self.constants)
            if mapping_ok and isinstance(mapping, dict):
                for key, value in sorted(mapping.items(), key=lambda pair: str(pair[0])):
                    if not isinstance(key, str):
                        continue
                    self.add(
                        node,
                        call=name,
                        parameter=f"rcParams.{key}",
                        original_parameter=key,
                        value=value,
                        resolved=True,
                    )

        if short == "legend" and "prop" in keyword_values and isinstance(keyword_values["prop"], dict):
            prop = keyword_values["prop"]
            if "size" in prop:
                self.add(node, call=name, parameter="legend_fontsize", original_parameter="prop.size", value=prop["size"], resolved=True)
            if "weight" in prop:
                self.add(node, call=name, parameter="legend_fontweight", original_parameter="prop.weight", value=prop["weight"], resolved=True)

        lowered_context = f"{name} {self.symbol or ''}".lower()
        fontweight_parameter = "text_fontweight"
        fontsize_parameter = "text_fontsize"
        if "axis_label" in lowered_context or "xaxis.label" in lowered_context or "yaxis.label" in lowered_context:
            fontweight_parameter = "axis_label_fontweight"
            fontsize_parameter = "axis_label_fontsize"
        elif "title" in lowered_context or "suptitle" in lowered_context:
            fontweight_parameter = "title_fontweight"
            fontsize_parameter = "title_fontsize"
        elif "tick" in lowered_context or (
            (self.symbol or "").split(".")[-1] in {"style_axes", "style_axis", "style_xaxis", "style_yaxis"}
            and name.startswith("label.")
        ):
            fontweight_parameter = "tick_label_fontweight"
            fontsize_parameter = "tick_label_fontsize"
        elif "legend" in lowered_context:
            fontweight_parameter = "legend_fontweight"
            fontsize_parameter = "legend_fontsize"
        positional_map: dict[str, str] = {
            "set_linewidth": "spine_width" if "spine" in name.lower() else "line_width",
            "set_fontweight": fontweight_parameter,
            "set_fontsize": fontsize_parameter,
            "set_visible": "spine_visible" if "spine" in name.lower() else "visible",
            "grid": "grid.enabled",
        }
        if short in positional_map and node.args:
            value, resolved = literal(node.args[0], self.constants)
            self.add(
                node,
                call=name,
                parameter=positional_map[short],
                original_parameter="positional[0]",
                value=value,
                resolved=resolved,
            )

        if short in {"tight_layout", "set_tight_layout"}:
            self.add(
                node,
                call=name,
                parameter="tight_layout",
                original_parameter="call",
                value=True,
                resolved=True,
            )

        if short == "with_suffix" and node.args:
            suffix, resolved = literal(node.args[0], self.constants)
            if resolved and isinstance(suffix, str) and suffix.lower() in {".png", ".pdf", ".svg"}:
                self.add(
                    node,
                    call=name,
                    parameter="export_format",
                    original_parameter="suffix",
                    value=suffix.lower().lstrip("."),
                    resolved=True,
                )

        if short == "savefig" and node.args:
            path_value, resolved = literal(node.args[0], self.constants)
            if resolved and isinstance(path_value, str):
                suffix = Path(path_value).suffix.lower().lstrip(".")
                if suffix in {"png", "pdf", "svg"}:
                    self.add(
                        node,
                        call=name,
                        parameter="export_format",
                        original_parameter="path suffix",
                        value=suffix,
                        resolved=True,
                    )

        self.generic_visit(node)


def extract_file(spec: RepositorySpec, path: Path) -> tuple[list[dict[str, Any]], set[str], list[str]]:
    relative = path.relative_to(spec.path).as_posix()
    source_type, chunks = file_plot_source(path)
    observations: list[dict[str, Any]] = []
    contexts: set[str] = set()
    parse_errors: list[str] = []
    shared_constants: dict[str, Any] = {}
    for cell, source in chunks:
        if not is_plotting_source(source):
            continue
        parse_source = clean_notebook_source(source) if source_type == "notebook" else source
        try:
            tree = ast.parse(parse_source)
        except SyntaxError as exc:
            parse_errors.append(f"{spec.name}:{relative}:cell={cell}:line={exc.lineno}")
            continue
        shared_constants.update(collect_constants(tree))
        visitor = EvidenceVisitor(
            repository=spec,
            relative_file=relative,
            source_type=source_type,
            cell=cell,
            constants=shared_constants,
        )
        visitor.visit(tree)
        observations.extend(visitor.observations)
        symbols = {item["symbol"] or f"cell-{cell}" for item in visitor.observations}
        contexts.update(f"{spec.name}:{relative}:{symbol}" for symbol in symbols)
    return observations, contexts, parse_errors


def serial_value(value: Any) -> Any:
    if isinstance(value, tuple):
        return [serial_value(item) for item in value]
    if isinstance(value, list):
        return [serial_value(item) for item in value]
    if isinstance(value, set):
        return sorted(serial_value(item) for item in value)
    if isinstance(value, dict):
        return {str(key): serial_value(item) for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))}
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return repr(value)


def canonical_value(value: Any) -> Any:
    """Normalise equivalent numeric spellings for aggregation only."""
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, list):
        return [canonical_value(item) for item in value]
    if isinstance(value, tuple):
        return [canonical_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): canonical_value(item) for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))}
    return value


def aggregate(observations: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for parameter in sorted({item["parameter"] for item in observations}):
        items = [item for item in observations if item["parameter"] == parameter and item["resolved"]]
        values: dict[str, list[dict[str, Any]]] = {}
        for item in items:
            key = json.dumps(canonical_value(serial_value(item["value"])), sort_keys=True, ensure_ascii=False)
            values.setdefault(key, []).append(item)
        rows = []
        for key, matches in values.items():
            rows.append(
                {
                    "value": json.loads(key),
                    "occurrence_count": len(matches),
                    "independent_file_count": len({match["independence_group"] for match in matches}),
                    "repository_count": len({match["repository"] for match in matches}),
                    "repositories": sorted({match["repository"] for match in matches}),
                    "observation_ids": [match["id"] for match in matches],
                }
            )
        rows.sort(key=lambda row: (-row["repository_count"], -row["independent_file_count"], -row["occurrence_count"], json.dumps(row["value"], sort_keys=True)))
        if rows:
            result[parameter] = rows
    return result


def _matching_observations(
    observations: list[dict[str, Any]], selectors: list[tuple[str, Any]]
) -> list[dict[str, Any]]:
    matches = []
    canonical_selectors = [(parameter, canonical_value(value)) for parameter, value in selectors]
    for item in observations:
        if not item["resolved"]:
            continue
        value = canonical_value(item["value"])
        if any(item["parameter"] == parameter and value == expected for parameter, expected in canonical_selectors):
            matches.append(item)
    return matches


def _representative_ids(matches: list[dict[str, Any]], limit: int = 14) -> list[str]:
    representatives = []
    seen_repositories = set()
    seen_files = set()
    for item in matches:
        if item["repository"] not in seen_repositories:
            representatives.append(item["id"])
            seen_repositories.add(item["repository"])
            seen_files.add(item["independence_group"])
    for item in matches:
        if len(representatives) >= limit:
            break
        if item["independence_group"] not in seen_files:
            representatives.append(item["id"])
            seen_files.add(item["independence_group"])
    return representatives[:limit]


def _rule(
    observations: list[dict[str, Any]],
    *,
    rule_id: str,
    parameter: str,
    candidate_value: Any,
    confidence: str,
    scope: str,
    interpretation: str,
    selectors: list[tuple[str, Any]],
    alternatives: list[Any] | None = None,
    representative_sources: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    matches = _matching_observations(observations, selectors)
    payload = {
        "id": rule_id,
        "parameter": parameter,
        "candidate_value": candidate_value,
        "confidence": confidence,
        "scope": scope,
        "interpretation": interpretation,
        "alternatives": alternatives or [],
        "evidence": {
            "occurrence_count": len(matches),
            "independent_file_count": len({item["independence_group"] for item in matches}),
            "repository_count": len({item["repository"] for item in matches}),
            "repositories": sorted({item["repository"] for item in matches}),
            "representative_observation_ids": _representative_ids(matches),
            "representative_sources": representative_sources or [],
        },
    }
    return payload


def curate_payload(payload: dict[str, Any]) -> None:
    observations = payload["observations"]
    payload["candidate_rules"] = [
        _rule(
            observations,
            rule_id="font-family",
            parameter="font.family",
            candidate_value="Arial-first sans-serif",
            confidence="HIGH",
            scope="base",
            interpretation="Use Arial as the requested face, with sans-serif fallbacks where availability matters.",
            selectors=[
                ("font_family", "Arial"),
                ("rcParams.font.family", "Arial"),
                ("rcParams.font.sans-serif", ["Arial"]),
                ("rcParams.font.sans-serif", ["Arial", "Helvetica", "DejaVu Sans"]),
            ],
            alternatives=["DejaVu Sans appears in a small tutorial subset"],
        ),
        _rule(
            observations,
            rule_id="axis-label-typography",
            parameter="axes.labels",
            candidate_value={"fontsize": 22, "fontweight": "bold"},
            confidence="HIGH",
            scope="base",
            interpretation="Large bold axis labels are the most stable cross-repository typographic choice.",
            selectors=[("axis_label_fontsize", 22), ("axis_label_fontweight", "bold")],
            alternatives=[{"fontsize": 13, "context": "compact XPS diagnostic"}, {"fontsize": 14, "context": "high-dimensional BO diagnostic"}],
        ),
        _rule(
            observations,
            rule_id="tick-label-typography",
            parameter="ticks.labels",
            candidate_value={"fontsize": 14, "fontweight": "bold"},
            confidence="HIGH",
            scope="base",
            interpretation="Bold 14 pt tick labels recur across recent research, coursework, and tooling.",
            selectors=[("tick_label_fontsize", 14), ("tick_label_fontweight", "bold")],
            alternatives=[{"fontsize": 10, "context": "diagnostic"}, {"fontsize": 9, "context": "compact multipanel"}],
        ),
        _rule(
            observations,
            rule_id="title-typography",
            parameter="axes.title",
            candidate_value={"fontsize": 18, "fontweight": "bold", "when_shown": True},
            confidence="HIGH",
            scope="base",
            interpretation="Titles are bold and usually 18 pt when present; final manuscript figures sometimes suppress them.",
            selectors=[("title_fontsize", 18), ("title_fontweight", "bold")],
            alternatives=[{"show_title": False, "context": "some manuscript figures"}],
        ),
        _rule(
            observations,
            rule_id="white-black-ground",
            parameter="figure-and-axes-colours",
            candidate_value={"figure_facecolor": "white", "axes_facecolor": "white", "foreground": "black"},
            confidence="HIGH",
            scope="base",
            interpretation="Plots explicitly force report-ready white grounds and black text/axes, often to override dark IDE themes.",
            selectors=[
                ("rcParams.figure.facecolor", "white"),
                ("rcParams.axes.facecolor", "white"),
                ("figure_facecolor", "white"),
                ("rcParams.text.color", "black"),
                ("rcParams.axes.edgecolor", "black"),
            ],
        ),
        _rule(
            observations,
            rule_id="boxed-spines",
            parameter="axes.spines",
            candidate_value={"all_visible": True, "linewidth": 1.8, "color": "black"},
            confidence="HIGH",
            scope="base",
            interpretation="Retain a complete black box around the axes rather than removing top/right spines.",
            selectors=[("spine_width", 1.8), ("spine_visible", True), ("top_spine_visible", True), ("right_spine_visible", True)],
        ),
        _rule(
            observations,
            rule_id="major-tick-direction-width",
            parameter="ticks.major",
            candidate_value={"direction": "in", "width": 1.8},
            confidence="HIGH",
            scope="base",
            interpretation="Inward major ticks matching the 1.8 pt spine width are well supported; length remains context-dependent.",
            selectors=[("tick_direction", "in"), ("tick_width", 1.8)],
            alternatives=[{"length": 7, "context": "PDI experimental"}, {"length": 6, "context": "sterics and Ising"}, {"length": 4, "context": "XPS"}],
        ),
        _rule(
            observations,
            rule_id="grid-off",
            parameter="axes.grid",
            candidate_value=False,
            confidence="MEDIUM",
            scope="base",
            interpretation="Grid-free final figures are explicit in several independent styles and implicit in many default-reset helpers; absence alone was not counted as explicit evidence.",
            selectors=[("grid.enabled", False), ("rcParams.axes.grid", False)],
        ),
        _rule(
            observations,
            rule_id="legend-frame-weight",
            parameter="legend",
            candidate_value={"frameon": True, "fontweight": "bold", "facecolor": "white", "edgecolor": "black"},
            confidence="HIGH",
            scope="base",
            interpretation="Legends are normally bold and framed, not frameless.",
            selectors=[("legend_frameon", True), ("legend_fontweight", "bold"), ("legend_facecolor", "white"), ("legend_edgecolor", "black")],
        ),
        _rule(
            observations,
            rule_id="legend-fontsize",
            parameter="legend.fontsize",
            candidate_value=10,
            confidence="MEDIUM",
            scope="base",
            interpretation="10 pt is the broadest base candidate, but 11 and 12 pt are credible publication alternatives.",
            selectors=[("legend_fontsize", 10)],
            alternatives=[11, 12],
        ),
        _rule(
            observations,
            rule_id="single-panel-geometry",
            parameter="figure.figsize",
            candidate_value=[8, 6],
            confidence="HIGH",
            scope="single-panel",
            interpretation="An approximately 4:3, 8 by 6 inch canvas recurs across nine independent repositories.",
            selectors=[("figure_size", [8, 6])],
            alternatives=[[8.4, 6.4], [9, 6]],
        ),
        _rule(
            observations,
            rule_id="line-width",
            parameter="lines.linewidth",
            candidate_value=2,
            confidence="MEDIUM",
            scope="base-data-lines",
            interpretation="2 pt is the broadest data-line candidate, while recent sterics figures intentionally use 2.4 pt and spectra often use 2.2 pt.",
            selectors=[("line_width", 2)],
            alternatives=[2.2, 2.4, 2.5],
        ),
        _rule(
            observations,
            rule_id="marker-size",
            parameter="lines.markersize",
            candidate_value=6,
            confidence="MEDIUM",
            scope="base",
            interpretation="6 pt is a recurring general marker size; dense XPS and sterics profiles use smaller 4-5.5 pt markers.",
            selectors=[("marker_size", 6)],
            alternatives=[4, 5.5, 6.5, 7],
        ),
        _rule(
            observations,
            rule_id="marker-edge-width",
            parameter="lines.markeredgewidth",
            candidate_value=None,
            confidence="UNRESOLVED",
            scope="base",
            interpretation="Observed values from 0.4 to 1.8 pt correlate with filled, open, and highlighted markers; no honest single default emerges.",
            selectors=[("marker_edge_width", 0.8), ("marker_edge_width", 0.9), ("marker_edge_width", 1.8)],
            alternatives=[0.4, 0.45, 0.5, 0.6, 0.7, 0.8, 0.9, 1.8],
        ),
        _rule(
            observations,
            rule_id="alpha",
            parameter="artist.alpha",
            candidate_value=None,
            confidence="UNRESOLVED",
            scope="base",
            interpretation="Alpha is semantic and artist-specific; lines, components, bars, and diagnostic scatters use different values.",
            selectors=[("line_alpha", 0.55), ("scatter_alpha", 0.9), ("component_alpha", 0.28), ("bar_alpha", 0.75)],
        ),
        _rule(
            observations,
            rule_id="ordinary-layout",
            parameter="figure.layout",
            candidate_value="tight_layout",
            confidence="HIGH",
            scope="ordinary-single-panel",
            interpretation="Tight layout is the general finalisation step; constrained layout is a coherent alternative for dense or multi-axis figures.",
            selectors=[("tight_layout", True)],
            alternatives=["constrained_layout for dense/multipanel figures"],
        ),
        _rule(
            observations,
            rule_id="dense-layout",
            parameter="figure.constrained_layout",
            candidate_value=True,
            confidence="MEDIUM",
            scope="dense-or-multipanel",
            interpretation="Recent BO, Ising, and dimer figures use constrained layout for dense compositions.",
            selectors=[("constrained_layout", True)],
        ),
        _rule(
            observations,
            rule_id="export-bounding-box",
            parameter="savefig.bbox_inches",
            candidate_value="tight",
            confidence="HIGH",
            scope="all-exported-figures",
            interpretation="Tight bounding boxes are nearly universal across the included corpus.",
            selectors=[("export_bbox_inches", "tight")],
        ),
        _rule(
            observations,
            rule_id="export-formats",
            parameter="savefig.formats",
            candidate_value=["pdf", "png"],
            confidence="MEDIUM",
            scope="final-manuscript",
            interpretation="Paired PDF and PNG output is established in PDI and XPS publication workflows; some diagnostics emit only one format.",
            selectors=[("export_format", "pdf"), ("export_format", "png")],
            alternatives=["PNG only for Ising diagnostic renderings", "PDF only in some calibration/report scripts"],
            representative_sources=[
                {"repository": "pdi-calculation", "file": "python/sterics/figure_style.py", "symbol": "save_figure_bundle"},
                {"repository": "pdi-data", "file": "cv/cv_utility.py", "symbol": "save_figure"},
                {"repository": "xps-workbench", "file": "src/xps_fitting/plotting/export.py", "symbol": "export_figure"},
            ],
        ),
        _rule(
            observations,
            rule_id="export-dpi",
            parameter="savefig.dpi",
            candidate_value=None,
            confidence="UNRESOLVED",
            scope="raster-export",
            interpretation="Both 300 and 600 dpi are established: 600 dominates PDI final figures; 300 dominates XPS, theory-demo, BO, and Gaussian reports.",
            selectors=[("export_dpi", 300), ("export_dpi", 600)],
            alternatives=[300, 600],
        ),
        _rule(
            observations,
            rule_id="opaque-raster",
            parameter="savefig.raster_background",
            candidate_value={"facecolor": "white", "transparent": False},
            confidence="HIGH",
            scope="raster-export",
            interpretation="White, opaque raster output is repeatedly forced for theme-independent reporting.",
            selectors=[("export_facecolor", "white"), ("export_transparent", False), ("raster_transparent", False), ("rcParams.savefig.transparent", False)],
            alternatives=[{"vector_transparent": True, "context": "XPS workbench only"}],
        ),
        _rule(
            observations,
            rule_id="reference-line-style",
            parameter="reference-lines",
            candidate_value={"linestyle": "--", "color": "black-or-grey"},
            confidence="HIGH",
            scope="reference-lines",
            interpretation="Dashed neutral reference lines recur broadly; linewidth varies by emphasis.",
            selectors=[("reference_line_style", "--"), ("reference_line_color", "black"), ("reference_line_color", "gray")],
            alternatives=[{"linewidth": 1.2}, {"linewidth": 1.8}],
        ),
        _rule(
            observations,
            rule_id="errorbar-caps",
            parameter="errorbar.capsize",
            candidate_value=4,
            confidence="MEDIUM",
            scope="general-errorbars",
            interpretation="4 pt caps recur independently, with 2-3 pt compact and 5 pt emphasized alternatives.",
            selectors=[("errorbar_capsize", 4)],
            alternatives=[2, 2.5, 3, 5],
        ),
        _rule(
            observations,
            rule_id="annotation-typography",
            parameter="annotations",
            candidate_value={"fontsize": "9-10", "fontweight": "bold"},
            confidence="MEDIUM",
            scope="data-annotations",
            interpretation="Annotations are generally bold and compact; exact size scales with panel density.",
            selectors=[("annotation_fontsize", 9), ("annotation_fontsize", 10), ("annotation_fontweight", "bold")],
        ),
        _rule(
            observations,
            rule_id="pdi-semantic-colours",
            parameter="semantic-colours.PDI",
            candidate_value={"PDI-Me-COOH": "#D55E00", "PDI-H-COOH": "#0072B2", "PDI-OMe-COOH": "#7A5195"},
            confidence="HIGH",
            scope="PDI-compound-comparisons-only",
            interpretation="This triad is stable across independent PDI calculation and experimental-data repositories; it is not a general-purpose palette.",
            selectors=[
                ("semantic_colour.PDI-Me-COOH", "#D55E00"),
                ("semantic_colour.PDI-H-COOH", "#0072B2"),
                ("semantic_colour.PDI-OMe-COOH", "#7A5195"),
            ],
            representative_sources=[
                {"repository": "pdi-calculation", "file": "python/sterics/config.py", "symbol": "COLOUR_MAP"},
                {"repository": "pdi-data", "file": "eis/eis_utility.py", "symbol": "COLOUR_MAP"},
            ],
        ),
        _rule(
            observations,
            rule_id="panel-labels",
            parameter="panel-labels",
            candidate_value="(a), (b), ...; bold; left-aligned title position",
            confidence="LOW",
            scope="multipanel",
            interpretation="Explicitly codified in XPS multipanels but not independently established elsewhere.",
            selectors=[("panel_label_template", "({label})")],
            representative_sources=[
                {"repository": "xps-workbench", "file": "src/xps_fitting/plotting/sample_panel.py", "symbol": "plot_sample_panel"},
                {"repository": "xps-workbench", "file": "src/xps_fitting/plotting/multipanel.py", "symbol": "plot_multipanel"},
            ],
        ),
        _rule(
            observations,
            rule_id="scientific-label-formatting",
            parameter="scientific-labels",
            candidate_value="quantity or descriptor followed by units in parentheses; math superscripts/subscripts where needed",
            confidence="MEDIUM",
            scope="scientific-axes",
            interpretation="Units consistently live in parentheses; chemical formulae, inverse powers, and molar exponents use math text, while degree and angstrom symbols are often Unicode.",
            selectors=[],
            representative_sources=[
                {"repository": "pdi-calculation", "file": "python/sterics/figure_style.py", "symbol": "ENERGY_UNIT_LABEL"},
                {"repository": "pdi-data", "file": "cv/cv_utility.py", "symbol": "style_cv_axes"},
                {"repository": "pdi-data", "file": "ms/ms_utility.py", "symbol": "style_ms_axes"},
                {"repository": "fyp-zis-photocatalysis", "file": "gaussian/scripts/visualise_gaussian_results.py", "symbol": "SPECIES_DISPLAY_LABELS"},
            ],
        ),
        _rule(
            observations,
            rule_id="global-fontsize",
            parameter="font.size",
            candidate_value=None,
            confidence="UNRESOLVED",
            scope="base",
            interpretation="A global 14 pt default is explicit only in the XPS theme; most other repositories style text roles directly.",
            selectors=[("global_fontsize", 14), ("rcParams.font.size", 14)],
        ),
        _rule(
            observations,
            rule_id="minor-ticks",
            parameter="ticks.minor",
            candidate_value=None,
            confidence="UNRESOLVED",
            scope="base",
            interpretation="Minor ticks are used for quantitative electrochemical axes but deliberately disabled for broad UV-vis/IR spectra; geometry also differs between PDI data and XPS.",
            selectors=[("minor_tick_width", 1.2), ("minor_tick_length", 3.5), ("minor_tick_length", 2.5)],
        ),
        _rule(
            observations,
            rule_id="top-right-ticks",
            parameter="ticks.top-right",
            candidate_value=None,
            confidence="UNRESOLVED",
            scope="base",
            interpretation="PDI experimental helpers retain boxed spines but turn top/right ticks off; the XPS publication theme places inward ticks on visible top/right spines.",
            selectors=[("top_ticks_visible", False), ("right_ticks_visible", False)],
            representative_sources=[
                {"repository": "pdi-data", "file": "cv/cv_utility.py", "symbol": "style_cv_axes"},
                {"repository": "xps-workbench", "file": "src/xps_fitting/plotting/themes.py", "symbol": "style_axes"},
            ],
        ),
    ]

    payload["conflicts"] = [
        {"parameter": "global font size", "values": [14, "role-specific only"], "status": "UNRESOLVED", "explanation": "Only XPS sets a global size."},
        {"parameter": "major tick length", "values": [4, 6, 7], "status": "UNRESOLVED", "explanation": "Correlates with XPS, sterics/Ising, and PDI experimental contexts."},
        {"parameter": "minor ticks", "values": ["off", {"width": 1.2, "length": 2.5}, {"width": 1.2, "length": 3.5}], "status": "UNRESOLVED", "explanation": "Presence and geometry depend on spectral density and plot type."},
        {"parameter": "top/right ticks", "values": [False, True], "status": "UNRESOLVED", "explanation": "Boxed spines are stable; tick placement is not."},
        {"parameter": "legend font size", "values": [10, 11, 12], "status": "MEDIUM", "explanation": "10 is broadest; 11 is XPS publication; 12 occurs in experimental single panels and TDQMS."},
        {"parameter": "data line width", "values": [2, 2.2, 2.4, 2.5], "status": "MEDIUM", "explanation": "Values correlate with base, spectra, sterics, and tutorial contexts."},
        {"parameter": "marker size and edge width", "values": ["4-7 pt markers", "0.4-1.8 pt edges"], "status": "UNRESOLVED", "explanation": "Dense, open, filled, and highlighted markers have different geometry."},
        {"parameter": "layout engine", "values": ["tight_layout", "constrained_layout"], "status": "MEDIUM", "explanation": "Tight is general; constrained is common for dense and multipanel plots."},
        {"parameter": "raster DPI", "values": [300, 600], "status": "UNRESOLVED", "explanation": "Both are recent and intentional in different publication workflows."},
        {"parameter": "vector transparency", "values": [False, True], "status": "UNRESOLVED", "explanation": "XPS permits transparent PDF while PDI helpers force white opaque output."},
        {"parameter": "title visibility", "values": [False, True], "status": "MEDIUM", "explanation": "Final manuscript panels often omit titles; diagnostics and tutorials use bold titles."},
        {"parameter": "math font set", "values": ["custom Arial", "stixsans", "stix"], "status": "UNRESOLVED", "explanation": "All preserve sans-oriented scientific text but differ by repository."},
    ]

    payload["variants"] = [
        {
            "name": "base-publication",
            "confidence": "HIGH",
            "evidence_repositories": ["pdi-calculation", "pdi-data", "xps-workbench", "bo-forge", "ising-coursework", "tdqms-coursework", "opentrons-screening"],
            "differences_from_base": {},
            "profile": "Arial-first sans serif; 22 pt bold axis labels; 14 pt bold ticks; 18 pt bold titles when shown; 1.8 pt boxed spines; inward ticks; white/black ground; framed bold legend; approximately 8 x 6 inches; tight export bounds.",
        },
        {
            "name": "compact-diagnostic",
            "confidence": "MEDIUM",
            "evidence_repositories": ["xps-workbench", "bo-forge"],
            "differences_from_base": {
                "axis_label_fontsize": "13-14",
                "tick_label_fontsize": 10,
                "title_fontsize": "14-16",
                "legend_fontsize": 9,
                "figure_size": "5.8 x 4.4 for compact XPS, larger dimension-driven BO grids",
            },
            "profile": "A coherent smaller-text diagnostic family exists, but geometry remains workload-dependent.",
        },
        {
            "name": "compact-multipanel",
            "confidence": "LOW",
            "evidence_repositories": ["xps-workbench", "pdi-calculation"],
            "differences_from_base": {
                "axis_label_fontsize": "8-10",
                "tick_label_fontsize": "8-9",
                "title_fontsize": "8-9",
                "legend_fontsize": 9,
            },
            "profile": "Dense panels reduce typography substantially, but exact values are not yet cross-repository stable.",
        },
        {
            "name": "presentation",
            "confidence": "LOW",
            "evidence_repositories": ["xps-workbench"],
            "differences_from_base": {"axis_label_fontsize": 17, "tick_label_fontsize": 13, "fit_line_width": 3, "figure_size": [8, 5], "show_title": True},
            "profile": "An explicit XPS presentation theme exists, but there is insufficient independent evidence to treat it as a general Angze profile.",
        },
    ]


def repository_record(spec: RepositorySpec) -> tuple[dict[str, Any], list[Path]]:
    files = tracked_code_files(spec)
    plotting_files = []
    for path in files:
        try:
            _, chunks = file_plot_source(path)
        except (OSError, json.JSONDecodeError, UnicodeDecodeError):
            continue
        if any(is_plotting_source(source) for _, source in chunks):
            plotting_files.append(path)
    selected_files = [
        path for path in plotting_files
        if spec.included and selected(spec, path.relative_to(spec.path).as_posix())
    ]
    relevant = selected_files if selected_files else plotting_files
    latest = ""
    if relevant:
        latest = run_git(spec.path, "log", "-1", "--format=%cI", "--", *[str(path.relative_to(spec.path)) for path in relevant])
    record = {
        "name": spec.name,
        "path": spec.display_path,
        "head": run_git(spec.path, "rev-parse", "HEAD"),
        "latest_relevant_commit": latest or None,
        "tracked_python_notebook_files": len(files),
        "plotting_bearing_files": len(plotting_files),
        "mined_files": len(selected_files),
        "included": spec.included,
        "context": spec.context,
        "provenance_confidence": spec.provenance,
        "notes": spec.notes,
        "path_exists_checked": spec.path.is_dir(),
    }
    return record, selected_files


def build_payload() -> dict[str, Any]:
    repository_rows = []
    observations: list[dict[str, Any]] = []
    contexts: set[str] = set()
    parse_errors: list[str] = []
    mined_files: set[str] = set()
    for spec in REPOSITORIES:
        record, selected_files = repository_record(spec)
        repository_rows.append(record)
        for path in selected_files:
            file_observations, file_contexts, file_errors = extract_file(spec, path)
            observations.extend(file_observations)
            contexts.update(file_contexts)
            parse_errors.extend(file_errors)
            mined_files.add(f"{spec.name}:{path.relative_to(spec.path).as_posix()}")

    observations.sort(
        key=lambda item: (
            item["repository"], item["file"], item["cell"] if item["cell"] is not None else -1,
            item["line"] or -1, item["parameter"], item["call"],
        )
    )
    for index, item in enumerate(observations, start=1):
        item["id"] = f"obs-{index:05d}"
        item["value"] = serial_value(item["value"])

    included_count = sum(row["included"] for row in repository_rows)
    payload = {
        "metadata": {
            "schema_version": 1,
            "analysis_date": date.today().isoformat(),
            "method": "Static AST extraction from tracked Python files and notebook code cells; no project code executed.",
            "candidate_repositories": len(repository_rows),
            "included_repositories": included_count,
            "excluded_repositories": len(repository_rows) - included_count,
            "mined_plotting_files": len(mined_files),
            "plotting_contexts": len(contexts),
            "observation_count": len(observations),
            "parse_errors": sorted(parse_errors),
        },
        "repositories": repository_rows,
        "observations": observations,
        "parameters": aggregate(observations),
        "candidate_rules": [],
        "conflicts": [],
        "variants": [],
        "exclusions": [
            {
                "repository": row["name"],
                "reason": row["notes"],
            }
            for row in repository_rows
            if not row["included"]
        ],
    }
    curate_payload(payload)
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="JSON output path under the forensic directory.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = build_payload()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(payload["metadata"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
