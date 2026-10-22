#!/usr/bin/env python3
"""Build the explanatory SVGs for the DipApprox CCS '25 research article.

Requires Python 3.9+ and matplotlib (``python3 -m pip install matplotlib``).
Run from any directory: ``python3 bin/generate-dipapprox-figures.py``.
For local visual checks, add ``--preview-dir /tmp/dipapprox-figure-previews``.

Only the optimization figure contains experimental results. Its values come
from Table 2 of the paper: SVT-Gauss with N=5, one selected adjacent input pair,
maximum nesting depths 6 and 3, unoptimized timeout at 600 s, and optimized
runtime 7.9 s (mean of three runs). A timeout is not a completed runtime.
The Gaussian and privacy-interval figures are explicitly illustrative.
"""

from __future__ import annotations

import argparse
import math
import os
from pathlib import Path
import re
import tempfile
from xml.sax.saxutils import escape

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "dipapprox-matplotlib"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "img" / "research"
NAVY = "#17334a"
MUTED = "#506377"
TEAL = "#087f7b"
TEAL_PALE = "#d6efea"
AMBER = "#a85b00"
AMBER_PALE = "#fff0d8"
RED = "#b5463b"
RED_PALE = "#fbe9e5"
BG = "#fcfdfd"
GRID = "#dce5e9"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 18,
        "text.color": NAVY,
        "axes.labelcolor": NAVY,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "axes.edgecolor": GRID,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": False,
        "svg.fonttype": "none",
        "svg.hashsalt": "dipapprox-ccs25-figures-v1",
    }
)


def figure(height: int):
    return plt.figure(figsize=(640 / 72, height / 72), dpi=72, facecolor=BG)


def heading(fig, title: str, subtitle: str):
    fig.text(0.065, 0.94, title, fontsize=25, fontweight="bold", va="top")
    fig.text(0.065, 0.865, subtitle, fontsize=18, va="top", color=MUTED)


def accessible_svg(path: Path, title: str, description: str):
    """Preserve selectable SVG text and add accessible names to plot exports."""
    svg = path.read_text()
    slug = path.stem
    svg = re.sub(
        r"<svg\b",
        f'<svg role="img" aria-labelledby="{slug}-title {slug}-desc"',
        svg,
        count=1,
    )
    svg = re.sub(
        r"(<svg\b[^>]*>)",
        lambda match: match.group(1)
        + f'\n <title id="{slug}-title">{escape(title)}</title>'
        + f'\n <desc id="{slug}-desc">{escape(description)}</desc>',
        svg,
        count=1,
    )
    path.write_text("\n".join(line.rstrip() for line in svg.splitlines()) + "\n")


def save_plot(fig, name: str, title: str, description: str, preview_dir):
    path = OUTPUT / f"dipapprox-{name}.svg"
    fig.savefig(path, metadata={"Date": None, "Creator": "bin/generate-dipapprox-figures.py"})
    accessible_svg(path, title, description)
    if preview_dir:
        fig.savefig(preview_dir / f"dipapprox-{name}.png", dpi=144)
    plt.close(fig)
    print(path.relative_to(ROOT))


def gaussian_tails(preview_dir):
    tail_mass = math.erfc(2 / math.sqrt(2))
    center_mass = 1 - tail_mass
    fig = figure(490)
    heading(fig, "An infinite domain, a bounded calculation", "Illustration: standard normal noise, cutoff at ±2σ")
    ax = fig.add_axes([0.10, 0.25, 0.84, 0.48], facecolor=BG)
    xs = [i / 200 for i in range(-800, 801)]
    density = [math.exp(-x * x / 2) / math.sqrt(2 * math.pi) for x in xs]
    for low, high, color, hatch in [(-4, -2, AMBER_PALE, "///"), (-2, 2, TEAL_PALE, None), (2, 4, AMBER_PALE, "///")]:
        region = [(x, y) for x, y in zip(xs, density) if low <= x <= high]
        ax.fill_between([x for x, _ in region], [y for _, y in region], color=color,
                        edgecolor=AMBER if hatch else TEAL, hatch=hatch, linewidth=0.6)
    ax.plot(xs, density, color=NAVY, linewidth=2.6)
    for x in [-2, 2]:
        ax.axvline(x, color=MUTED, linestyle=(0, (4, 4)), linewidth=1.2)
    ax.set(xlim=(-4, 4), ylim=(0, 0.43), xticks=[-4, -2, 0, 2, 4], yticks=[])
    ax.tick_params(axis="x", length=0, pad=9, labelsize=18)
    ax.text(0, 0.195, "Bounded center", ha="center", fontsize=20, fontweight="bold")
    ax.text(0, 0.135, f"{center_mass:.2%} of the mass", ha="center", fontsize=20)
    for x in [-2.75, 2.75]:
        ax.annotate("tail", xy=(x, 0.012), xytext=(x, 0.16), ha="center", fontsize=19,
                    color=AMBER, arrowprops={"arrowstyle": "->", "color": AMBER, "lw": 1.5})
    fig.text(0.52, 0.12, f"Both tails: {tail_mass:.2%} of the mass", ha="center", fontsize=21, color=AMBER, fontweight="bold")
    fig.text(0.52, 0.055, "Tail mass is bounded, not silently discarded.", ha="center", fontsize=18)
    save_plot(fig, "gaussian-tails", "Bounding Gaussian tails",
              "Illustrative standard-normal density with a cutoff at minus and plus two standard deviations. "
              "The bounded center contains 95.45 percent of the probability mass. The two unbounded tails "
              "together contain 4.55 percent. The tails must be accounted for with a bound, not discarded. "
              "This deliberately modest cutoff makes the tails visible; it is not a paper experiment.", preview_dir)


def privacy_intervals(preview_dir):
    fig = figure(500)
    heading(fig, "One threshold, three possible answers", "Illustrative intervals — not measured paper results")
    ax = fig.add_axes([0.23, 0.25, 0.69, 0.47], facecolor=BG)
    ax.set(xlim=(0, 0.20), ylim=(-0.55, 2.85), yticks=[2, 1, 0], yticklabels=["DP", "Not_DP", "Unknown"])
    ax.set_xticks([0, 0.05, 0.10, 0.15, 0.20])
    ax.set_xticklabels(["0", ".05", ".10", ".15", ".20"], fontsize=18)
    ax.tick_params(axis="both", length=0, pad=12)
    ax.grid(axis="x", color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    ax.axvline(0.10, color=NAVY, linestyle=(0, (4, 4)), linewidth=2)
    ax.text(0.10, 2.62, "δ = 0.10", ha="center", fontsize=19, fontweight="bold",
            bbox={"facecolor": BG, "edgecolor": "none", "pad": 4})
    for low, high, y, color in [(0.04, 0.08, 2, TEAL), (0.12, 0.16, 1, RED), (0.08, 0.13, 0, AMBER)]:
        ax.plot([low, high], [y, y], color=color, linewidth=8, solid_capstyle="butt")
        ax.plot([low, low], [y - 0.11, y + 0.11], color=color, linewidth=2)
        ax.plot([high, high], [y - 0.11, y + 0.11], color=color, linewidth=2)
        ax.text((low + high) / 2, y + 0.23, f"[{low:.2f}, {high:.2f}]", ha="center", fontsize=18, color=color)
    fig.text(0.575, 0.12, "Bounds on the maximum privacy gap", ha="center", fontsize=19)
    fig.text(0.50, 0.055, "Below: certified  •  Above: violated  •  Crossing: unknown", ha="center", fontsize=18)
    save_plot(fig, "privacy-intervals", "Privacy decisions from rigorous intervals",
              "An illustrative decision chart, not experimental results. At delta equal to 0.10, bounds "
              "of 0.04 to 0.08 on the maximum privacy gap certify DP, bounds of 0.12 to 0.16 establish "
              "Not_DP, and bounds of 0.08 to 0.13 leave the answer Unknown. DP requires upper bounds for "
              "all relevant adjacent input pairs; a privacy violation requires a witness with a lower bound above delta.", preview_dir)


def optimization(preview_dir):
    fig = figure(620)
    heading(fig, "Simpler integrals can change feasibility", "Paper Table 2: SVT-Gauss, N = 5, one adjacent pair")
    fig.text(0.065, 0.775, "Runtime (seconds, logarithmic scale)", fontsize=20, fontweight="bold")
    ax = fig.add_axes([0.26, 0.455, 0.66, 0.24], facecolor=BG)
    ax.set_xscale("log")
    ax.set(xlim=(1, 850), ylim=(-0.6, 1.65), yticks=[1, 0], yticklabels=["Original", "Optimized"])
    ax.xaxis.set_major_locator(FixedLocator([1, 10, 100, 600]))
    ax.xaxis.set_major_formatter(FixedFormatter(["1", "10", "100", "600"]))
    ax.xaxis.set_minor_locator(NullLocator())
    ax.tick_params(axis="both", length=0, pad=9, labelsize=18)
    ax.grid(axis="x", color=GRID)
    ax.set_axisbelow(True)
    ax.plot([1, 600], [1, 1], color=AMBER, linewidth=8, solid_capstyle="butt")
    ax.plot(600, 1, marker="|", color=AMBER, markersize=22, markeredgewidth=2.5)
    ax.annotate("", xy=(820, 1), xytext=(600, 1), arrowprops={"arrowstyle": "->", "color": AMBER, "lw": 2})
    ax.text(600, 1.28, "Timeout at 600 s", ha="right", fontsize=19, color=AMBER, fontweight="bold")
    ax.plot([1, 7.9], [0, 0], color=TEAL, linewidth=8, solid_capstyle="butt")
    ax.plot(7.9, 0, marker="o", color=TEAL, markersize=8)
    ax.text(7.9, 0.28, "7.9 s", ha="center", fontsize=19, color=TEAL, fontweight="bold")
    fig.text(0.065, 0.33, "Maximum nesting depth", fontsize=20, fontweight="bold")
    ax2 = fig.add_axes([0.26, 0.12, 0.66, 0.15], facecolor=BG)
    ax2.set(xlim=(0, 7.1), ylim=(-0.5, 1.5), yticks=[1, 0], yticklabels=["Original", "Optimized"], xticks=[])
    ax2.spines["bottom"].set_visible(False)
    ax2.tick_params(axis="y", length=0, pad=9, labelsize=18)
    for y, depth, color in [(1, 6, AMBER), (0, 3, TEAL)]:
        ax2.barh(y, depth, height=0.40, color=color)
        ax2.text(depth + 0.15, y, str(depth), va="center", fontsize=22, fontweight="bold")
    fig.text(0.065, 0.045, "7.9 s is the mean of three runs; 600 s is a time limit.", fontsize=18, color=MUTED)
    save_plot(fig, "optimization", "Optimization result for one SVT-Gauss comparison",
              "Reported results from Table 2 for SVT-Gauss with N equal to 5 on one selected adjacent input "
              "pair. The unoptimized analysis timed out at the 600-second limit; its completed runtime "
              "is unknown. The optimized runtime was 7.9 seconds, the mean of three runs. Maximum nesting "
              "depth decreased from 6 to 3. The runtime axis is logarithmic. These values do not describe "
              "an exhaustive check of all adjacent pairs.", preview_dir)


def verification_pipeline():
    """A code-native diagram: no image-generation model or rasterization needed."""
    title = "From a randomized program to a sound privacy verdict"
    description = (
        "A program with finite input and output domains defines execution paths. Path probabilities are handled "
        "with bounded-domain integrals and explicit tail bounds. These produce probability intervals, "
        "then privacy-gap bounds, and finally DP, Not_DP, or Unknown. DP requires all relevant adjacent "
        "input pairs to be certified; Not_DP requires a violating witness."
    )
    slug = "dipapprox-verification-pipeline"
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="820" viewBox="0 0 640 820" role="img" aria-labelledby="{slug}-title {slug}-desc">
  <title id="{slug}-title">{escape(title)}</title>
  <desc id="{slug}-desc">{escape(description)}</desc>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="{MUTED}"/></marker>
  </defs>
  <rect width="640" height="820" rx="0" fill="{BG}"/>
  <g font-family="DejaVu Sans, Arial, sans-serif" fill="{NAVY}">
  <text x="40" y="51" font-size="25" font-weight="700">How DipApprox reaches a verdict</text>
  <text x="40" y="83" font-size="18" fill="{MUTED}">A high-level view of sound approximate verification</text>''']

    def box(x, y, width, height, lines, fill=TEAL_PALE, stroke=TEAL, size=21):
        parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
        first_y = y + height / 2 - (len(lines) - 1) * 14 + 7
        for i, line in enumerate(lines):
            parts.append(f'<text x="{x + width / 2:g}" y="{first_y + i * 28:g}" font-size="{size}" text-anchor="middle">{escape(line)}</text>')

    def arrow(points):
        parts.append(f'<path d="{points}" fill="none" stroke="{MUTED}" stroke-width="2" marker-end="url(#arrow)"/>')

    box(40, 119, 255, 70, ["Randomized program"], fill="#e8eef4", stroke=NAVY)
    box(345, 119, 255, 70, ["Finite input and", "output domains"], fill="#e8eef4", stroke=NAVY)
    parts.append('<text x="320" y="163" text-anchor="middle" font-size="28">+</text>')
    arrow("M167 189 V211 H320 V234")
    parts.append(f'<path d="M472 189 V211 H320" fill="none" stroke="{MUTED}" stroke-width="2"/>')
    box(110, 237, 420, 60, ["Execution paths"])
    arrow("M320 297 V319 H177 V343")
    arrow("M320 319 H463 V343")
    box(40, 346, 275, 83, ["Integrals on a", "bounded domain"])
    box(345, 346, 255, 83, ["Explicit bounds", "on the tails"], fill=AMBER_PALE, stroke=AMBER)
    arrow("M177 429 V451 H320 V475")
    parts.append(f'<path d="M472 429 V451 H320" fill="none" stroke="{MUTED}" stroke-width="2"/>')
    box(110, 478, 420, 60, ["Probability intervals"])
    arrow("M320 538 V581")
    box(110, 584, 420, 60, ["Privacy-gap bounds"])
    arrow("M320 644 V666 H125 V690")
    arrow("M320 666 V690")
    arrow("M320 666 H515 V690")
    box(40, 693, 170, 68, ["DP", "certified"], size=20)
    box(235, 693, 170, 68, ["Not_DP", "witness found"], fill=RED_PALE, stroke=RED, size=20)
    box(430, 693, 170, 68, ["Unknown", "unresolved"], fill=AMBER_PALE, stroke=AMBER, size=20)
    parts.append(f'<text x="320" y="797" text-anchor="middle" font-size="18" fill="{MUTED}">Continuous random draws; finite input and output domains.</text>')
    parts.append("</g></svg>\n")
    path = OUTPUT / f"{slug}.svg"
    path.write_text("\n".join(parts))
    print(path.relative_to(ROOT))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview-dir", type=Path, help="Also export temporary PNG previews of the scientific plots.")
    args = parser.parse_args()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    if args.preview_dir:
        args.preview_dir.mkdir(parents=True, exist_ok=True)
    gaussian_tails(args.preview_dir)
    verification_pipeline()
    privacy_intervals(args.preview_dir)
    optimization(args.preview_dir)


if __name__ == "__main__":
    main()
