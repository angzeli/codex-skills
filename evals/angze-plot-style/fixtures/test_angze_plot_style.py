"""Regression checks for the reusable Angze Matplotlib helper."""

from __future__ import annotations

import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path

import matplotlib as mpl

mpl.use("Agg", force=True)

import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba


REPO_ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = (
    REPO_ROOT
    / "skills"
    / "angze-plot-style"
    / "assets"
    / "angze_plot_style.py"
)
MODULE_SPEC = importlib.util.spec_from_file_location("angze_plot_style", MODULE_PATH)
if MODULE_SPEC is None or MODULE_SPEC.loader is None:
    raise RuntimeError(f"Could not load plotting helper from {MODULE_PATH}")
style = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(style)


class RecordingFigure:
    """Capture savefig calls without depending on encoded file bytes."""

    def __init__(self) -> None:
        self.calls: list[tuple[Path, dict[str, object]]] = []

    def savefig(self, output: str | Path, **kwargs: object) -> None:
        self.calls.append((Path(output), dict(kwargs)))


class AngzePlotStyleRegressionTests(unittest.TestCase):
    def tearDown(self) -> None:
        plt.close("all")

    def test_create_figure_styles_future_artists(self) -> None:
        ambient = {
            "lines.linewidth": 0.25,
            "axes.labelsize": 7.0,
            "axes.labelweight": "normal",
            "axes.titlesize": 8.0,
            "axes.titleweight": "normal",
        }
        with mpl.rc_context(rc=ambient):
            with style.create_figure(profile="manuscript") as (fig, ax):
                line = ax.plot([0.0, 1.0], [0.0, 1.0])[0]
                ax.set_xlabel("Time (s)")
                title = ax.set_title("Response")

                self.assertEqual(tuple(fig.get_size_inches()), (8.0, 6.0))
                self.assertEqual(line.get_linewidth(), 2.0)
                self.assertEqual(ax.xaxis.label.get_fontsize(), 22.0)
                self.assertEqual(ax.xaxis.label.get_fontweight(), "bold")
                self.assertEqual(title.get_fontsize(), 18.0)
                self.assertEqual(title.get_fontweight(), "bold")

    def test_create_figure_restores_rcparams_after_exception(self) -> None:
        profile_keys = tuple(style.rc_params())
        with mpl.rc_context(rc={"lines.linewidth": 0.25, "axes.labelsize": 7.0}):
            before = {
                key: copy.deepcopy(mpl.rcParams[key])
                for key in profile_keys
            }
            with self.assertRaisesRegex(RuntimeError, "intentional probe"):
                with style.create_figure() as (_fig, ax):
                    self.assertEqual(ax.plot([0, 1], [0, 1])[0].get_linewidth(), 2.0)
                    raise RuntimeError("intentional probe")

            for key, expected in before.items():
                with self.subTest(rcparam=key):
                    self.assertEqual(mpl.rcParams[key], expected)

    def test_style_legend_restores_frame(self) -> None:
        fig, ax = plt.subplots()
        ax.plot([0, 1], [0, 1], label="series")
        legend = ax.legend(frameon=False)

        returned = style.style_legend(legend)

        self.assertIs(returned, legend)
        self.assertTrue(legend.get_frame_on())
        self.assertTrue(legend.get_frame().get_visible())
        self.assertEqual(legend.get_frame().get_facecolor(), to_rgba("white"))
        self.assertEqual(legend.get_frame().get_edgecolor(), to_rgba("black"))
        self.assertEqual(legend.get_frame().get_alpha(), 1.0)
        self.assertEqual(legend.get_texts()[0].get_fontsize(), 10.0)
        self.assertEqual(legend.get_texts()[0].get_fontweight(), "bold")
        plt.close(fig)

    def test_style_axes_disables_major_and_minor_grids(self) -> None:
        fig, ax = plt.subplots()
        ax.minorticks_on()
        ax.grid(True, which="both")

        style.style_axes(ax, minor_ticks=True, grid=False)
        fig.canvas.draw()

        major_gridlines = [*ax.get_xgridlines(), *ax.get_ygridlines()]
        minor_gridlines = [
            *(tick.gridline for tick in ax.xaxis.get_minor_ticks()),
            *(tick.gridline for tick in ax.yaxis.get_minor_ticks()),
        ]
        self.assertFalse(any(line.get_visible() for line in major_gridlines))
        self.assertFalse(any(line.get_visible() for line in minor_gridlines))
        plt.close(fig)

    def test_style_axes_styles_all_title_locations(self) -> None:
        fig, ax = plt.subplots()
        titles = [
            ax.set_title("Left", loc="left", fontsize=7, fontweight="normal", color="red"),
            ax.set_title("Center", loc="center", fontsize=7, fontweight="normal", color="red"),
            ax.set_title("Right", loc="right", fontsize=7, fontweight="normal", color="red"),
        ]

        style.style_axes(ax)

        for title in titles:
            with self.subTest(title=title.get_text()):
                self.assertEqual(title.get_fontsize(), 18.0)
                self.assertEqual(title.get_fontweight(), "bold")
                self.assertEqual(to_rgba(title.get_color()), to_rgba("black"))
        plt.close(fig)

    def test_mathtext_default_remains_caller_controlled(self) -> None:
        with mpl.rc_context(rc={"mathtext.default": "it", "mathtext.fontset": "dejavusans"}):
            with style.angze_plot_context():
                self.assertEqual(mpl.rcParams["mathtext.fontset"], "stixsans")
                self.assertEqual(mpl.rcParams["mathtext.default"], "it")

            self.assertEqual(mpl.rcParams["mathtext.fontset"], "dejavusans")
            self.assertEqual(mpl.rcParams["mathtext.default"], "it")

    def test_save_bundle_applies_policy_and_writes_both_formats(self) -> None:
        with tempfile.TemporaryDirectory(prefix="angze-plot-style-") as temp_dir:
            temp_root = Path(temp_dir)
            recording = RecordingFigure()
            recorded_outputs = style.save_figure_bundle(
                recording,
                temp_root / "recorded",
            )

            self.assertEqual(
                recorded_outputs,
                (temp_root / "recorded.png", temp_root / "recorded.pdf"),
            )
            self.assertEqual(len(recording.calls), 2)
            for output, kwargs in recording.calls:
                with self.subTest(format=output.suffix):
                    self.assertEqual(kwargs["dpi"], 600)
                    self.assertEqual(kwargs["bbox_inches"], "tight")
                    self.assertEqual(kwargs["facecolor"], "white")
                    self.assertEqual(kwargs["edgecolor"], "white")
                    self.assertIs(kwargs["transparent"], False)

            with style.create_figure(figsize=(2.0, 1.5)) as (fig, ax):
                ax.plot([0.0, 1.0], [0.0, 1.0])
                real_outputs = style.save_figure_bundle(fig, temp_root / "smoke")
                plt.close(fig)

            self.assertEqual(
                real_outputs,
                (temp_root / "smoke.png", temp_root / "smoke.pdf"),
            )
            for output in real_outputs:
                with self.subTest(output=output.name):
                    self.assertTrue(output.is_file())
                    self.assertGreater(output.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
