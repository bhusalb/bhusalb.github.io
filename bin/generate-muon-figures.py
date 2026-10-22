#!/usr/bin/env python3
"""Generate accessible SVG figures for the private-Muon clipping tutorial.

Requires Python 3.9+ and Matplotlib. Run from any directory with
``python3 bin/generate-muon-figures.py``. Add ``--preview-dir /tmp/muon-figures``
to also save PNGs for visual review.

All numbers come from assets/code/clipping_polar_geometry.py. These figures
show a deterministic teaching example, not training measurements or a private
optimizer. SVG output retains text, uses fixed identifiers, and omits dates.
"""

from __future__ import annotations

import argparse
import importlib.util
import math
import os
from pathlib import Path
import re
import sys
import tempfile
from xml.sax.saxutils import escape

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "muon-matplotlib"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "img" / "research"
SOURCE = ROOT / "assets" / "code" / "clipping_polar_geometry.py"
sys.dont_write_bytecode = True
SPEC = importlib.util.spec_from_file_location("clipping_polar_geometry", SOURCE)
GEOMETRY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GEOMETRY)

G1 = ((4.0, 0.0), (0.0, 0.0))
G2 = ((0.0, 1.0), (0.0, 1.0))
A = GEOMETRY.mean(G1, G2)
CLIPPED_G1, FACTOR1 = GEOMETRY.clip(G1, 1.0)
CLIPPED_G2, FACTOR2 = GEOMETRY.clip(G2, 1.0)
B = GEOMETRY.mean(CLIPPED_G1, CLIPPED_G2)

NAVY = "#17334a"
MUTED = "#53677a"
TEAL = "#087f7b"
TEAL_PALE = "#e7f4f1"
AMBER = "#a65b0a"
AMBER_PALE = "#fff2e0"
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
        "svg.fonttype": "none",
        "svg.hashsalt": "muon-clipping-figures-v1",
    }
)


def polar_angle(matrix):
    polar = GEOMETRY.polar_factor_2x2(matrix)
    return math.degrees(math.atan2(polar[1][0], polar[0][0]))


ANGLE_A = polar_angle(A)
ANGLE_B = polar_angle(B)


def figure(height):
    return plt.figure(figsize=(640 / 72, height / 72), dpi=72, facecolor=BG)


def heading(fig, title, subtitle):
    fig.text(0.0625, 0.94, title, fontsize=25, fontweight="bold", va="top")
    fig.text(0.0625, 0.875, subtitle, fontsize=18, color=MUTED, va="top")


def save(fig, name, title, description, preview_dir):
    path = OUTPUT / f"muon-{name}.svg"
    fig.savefig(path, metadata={"Date": None, "Creator": "bin/generate-muon-figures.py"})
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
    svg = svg.replace("'DejaVu Sans'", "'DejaVu Sans', Arial, sans-serif")
    svg = re.sub(r'width="([\d.]+)pt" height="([\d.]+)pt"', r'width="\1" height="\2"', svg, count=1)
    path.write_text("\n".join(line.rstrip() for line in svg.splitlines()) + "\n")
    if preview_dir:
        fig.savefig(preview_dir / f"muon-{name}.png", dpi=144)
    plt.close(fig)
    print(path.relative_to(ROOT))


def rounded_box(ax, x, y, width, height, color, edge):
    ax.add_patch(
        FancyBboxPatch(
            (x, y), width, height,
            boxstyle="round,pad=0,rounding_size=12",
            facecolor=color, edgecolor=edge, linewidth=1.1,
        )
    )


def matrix(ax, x, y, values, color=NAVY, decimal_places=None):
    """Draw a 2-by-2 matrix with selectable numeric labels and vector brackets."""
    for row in range(2):
        for column in range(2):
            value = values[row][column]
            label = f"{value:g}" if decimal_places is None else f"{value:.{decimal_places}f}".rstrip("0").rstrip(".")
            ax.text(x + 40 + column * 100, y + 21 + row * 43, label,
                    ha="center", va="center", fontsize=23, color=color)
    ax.plot([x + 5, x, x, x + 5], [y, y, y + 86, y + 86], color=color, linewidth=1.5)
    ax.plot([x + 175, x + 180, x + 180, x + 175], [y, y, y + 86, y + 86], color=color, linewidth=1.5)


def clipping_matrices(preview_dir):
    fig = figure(650)
    heading(fig, "Clipping changes the mixture", "The same threshold gives two different weights: C = 1")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=(0, 640), ylim=(650, 0))
    ax.axis("off")

    for x, name, gradient, norm, factor in [
        (40, "G₁", G1, "4", "1/4 = 0.25"),
        (340, "G₂", G2, "√2", "1/√2 ≈ 0.707"),
    ]:
        rounded_box(ax, x, 122, 260, 229, "#f0f4f7", GRID)
        ax.text(x + 130, 153, name, ha="center", va="center", fontsize=23, fontweight="bold")
        matrix(ax, x + 40, 176, gradient)
        ax.text(x + 130, 289, f"Frobenius norm: {norm}", ha="center", va="center", fontsize=18)
        ax.text(x + 130, 325, f"Weight: {factor}", ha="center", va="center", fontsize=19, fontweight="bold")

    ax.text(320, 390, "Compare the two averages", ha="center", va="center", fontsize=21, fontweight="bold")
    for x, title, name, mean, color, pale in [
        (40, "Before clipping", "A", A, TEAL, TEAL_PALE),
        (340, "After clipping", "B", B, AMBER, AMBER_PALE),
    ]:
        rounded_box(ax, x, 418, 260, 168, pale, color)
        ax.text(x + 130, 449, f"{title}  ·  {name}", ha="center", va="center", fontsize=20, color=color, fontweight="bold")
        matrix(ax, x + 40, 478, mean, color=color, decimal_places=3 if name == "B" else None)
    ax.text(320, 621, "Unequal weights can change more than the overall size.",
            ha="center", va="center", fontsize=18, color=MUTED)
    save(fig, "clipping-matrices", "Per-example clipping changes the average matrix",
         "Deterministic teaching example with clipping threshold C equal to 1. G1 is [[4, 0], [0, 0]], "
         "has Frobenius norm 4, and receives weight 1/4. G2 is [[0, 1], [0, 1]], has norm square root "
         "of 2, and receives weight 1 divided by square root of 2. Their original mean A is "
         "[[2, 0.5], [0, 0.5]]. Their clipped mean B is [[0.5, 0.353553...], [0, 0.353553...]], "
         "shown rounded to three decimal places. These are illustrative matrices, not measured training results.", preview_dir)


def polar_rotation(preview_dir):
    fig = figure(500)
    heading(fig, "Clipping rotates this polar factor", "Compare unit directions: Q(A)e₁ and Q(B)e₁")
    ax = fig.add_axes([0.09, 0.24, 0.85, 0.51])
    ax.set(xlim=(-0.08, 1.18), ylim=(-0.52, 0.07), aspect="equal")
    ax.axis("off")
    ax.add_patch(FancyArrowPatch((0, 0), (1.12, 0), arrowstyle="-|>", mutation_scale=14,
                                color=MUTED, linewidth=1.2, linestyle=(0, (4, 3))))
    ax.text(1.15, 0.014, "e₁", fontsize=21, va="center", ha="center", color=MUTED)
    ax.plot(0, 0, "o", color=NAVY, markersize=5, zorder=6)
    ax.add_patch(Arc((0, 0), 2, 2, theta1=-29, theta2=2, linewidth=1.3, color=GRID))
    for matrix_value, color, style in [(A, TEAL, "-"), (B, AMBER, "-")]:
        polar = GEOMETRY.polar_factor_2x2(matrix_value)
        endpoint = (polar[0][0], polar[1][0])
        ax.add_patch(FancyArrowPatch((0, 0), endpoint, arrowstyle="-|>", mutation_scale=20,
                                    color=color, linewidth=3, linestyle=style))
    ax.text(0.69, -0.068, f"Original  {ANGLE_A:.2f}°", ha="center", va="center", fontsize=20, color=TEAL, fontweight="bold")
    ax.text(0.72, -0.445, f"Clipped  {ANGLE_B:.2f}°", ha="center", va="center", fontsize=20, color=AMBER, fontweight="bold")
    ax.add_patch(Arc((0, 0), 1.16, 1.16, theta1=ANGLE_B, theta2=ANGLE_A,
                     linewidth=2.3, color=NAVY))
    mid_angle = math.radians((ANGLE_A + ANGLE_B) / 2)
    ax.annotate(f"{abs(ANGLE_B - ANGLE_A):.2f}° clockwise", xy=(0.58 * math.cos(mid_angle), 0.58 * math.sin(mid_angle)),
                xytext=(0.12, -0.39), fontsize=19, ha="left", va="center",
                arrowprops={"arrowstyle": "-", "color": MUTED, "lw": 1.2, "connectionstyle": "angle,angleA=0,angleB=-90,rad=5"})
    fig.text(0.5, 0.145, "Common positive scaling keeps the direction:",
             ha="center", fontsize=19, color=MUTED)
    fig.text(0.5, 0.075, "Q(αA) = Q(A), for every α > 0", ha="center", fontsize=22, fontweight="bold", color=TEAL)
    save(fig, "polar-rotation", "Polar-factor rotation caused by unequal clipping",
         "Unit directions obtained by applying the orthogonal polar factors to e1, the first coordinate "
         "unit vector. Q(A)e1 makes an angle of minus 11.309932 degrees with e1. Q(B)e1 makes an angle "
         "of minus 22.5 degrees, a clockwise change of 11.190068 degrees. Multiplying A by any positive "
         "scalar leaves its polar factor Q(A) unchanged. These arrows depict columns of the polar factors, "
         "not columns of the mean matrices. This is a deterministic teaching example, not a training result.", preview_dir)


def clipping_sweep(preview_dir):
    fig = figure(550)
    heading(fig, "What happens as clipping gets looser?", "The same two gradients, with threshold C varied")
    ax = fig.add_axes([0.205, 0.265, 0.735, 0.50], facecolor=BG)
    thresholds = sorted({0.25 + i * (4.5 - 0.25) / 600 for i in range(601)} | {1.0, math.sqrt(2), 4.0})
    angles = []
    for threshold in thresholds:
        clipped1, _ = GEOMETRY.clip(G1, threshold)
        clipped2, _ = GEOMETRY.clip(G2, threshold)
        angles.append(polar_angle(GEOMETRY.mean(clipped1, clipped2)))
    ax.set(xlim=(0.25, 4.5), ylim=(-24, -9.8))
    ax.set_xticks([0.25, math.sqrt(2), 2.5, 4, 4.5], labels=["0.25", "√2", "2.5", "4", "4.5"])
    ax.set_yticks([-22.5, -17, ANGLE_A], labels=["−22.50", "−17", "−11.31"])
    ax.tick_params(axis="both", length=0, pad=9, labelsize=18)
    ax.set_ylabel("Polar rotation (degrees)", fontsize=19, labelpad=10)
    ax.set_xlabel("Clipping threshold C", fontsize=20, labelpad=14)
    ax.spines["left"].set_visible(False)
    ax.grid(axis="y", color=GRID, linewidth=0.9)
    ax.set_axisbelow(True)
    for threshold in [math.sqrt(2), 4]:
        ax.axvline(threshold, color=MUTED, linewidth=1.1, linestyle=(0, (3, 4)), alpha=0.65)
    ax.axhline(ANGLE_A, color=TEAL, linewidth=2, linestyle=(0, (5, 4)), label="Original mean")
    ax.plot(thresholds, angles, color=AMBER, linewidth=3.4, label="Clipped mean", zorder=3)
    ax.plot(1, ANGLE_B, "o", color=AMBER, markersize=8, markeredgecolor=BG, markeredgewidth=1.5, zorder=4)
    ax.annotate("C = 1: −22.50°", xy=(1, ANGLE_B), xytext=(0.46, -19.5), fontsize=19, color=AMBER,
                arrowprops={"arrowstyle": "-", "color": AMBER, "lw": 1.2})
    handles, labels = ax.get_legend_handles_labels()
    fig.legend([handles[1], handles[0]], [labels[1], labels[0]], loc="upper center",
               bbox_to_anchor=(0.53, 0.835), ncol=2, frameon=False, fontsize=18, handlelength=2.3,
               columnspacing=1.6)
    fig.text(0.5, 0.085, "0 < C ≤ √2: −22.5°  ·  C ≥ 4: original angle", ha="center", fontsize=18, color=MUTED)
    fig.text(0.5, 0.035, "A deterministic example, not measured training performance.", ha="center", fontsize=17, color=MUTED)
    save(fig, "clipping-sweep", "Polar rotation as the clipping threshold varies",
         "A deterministic threshold sweep for the tutorial's two gradient matrices, with C from 0.25 "
         "to 4.5. The clipped mean has polar angle minus 22.5 degrees when C is at most square root of 2. "
         "For square root of 2 less than C less than 4, the angle is minus arctangent of 1/(C + 1), in degrees. "
         "At C equal to 4 and above, neither example is clipped and the angle equals the original mean's "
         "minus 11.309932 degrees. A marker highlights C equal to 1. Vertical guides mark square root "
         "of 2 and 4, the two gradient norms. The dashed horizontal line is the original mean's angle. "
         "This plot contains no measured training results.", preview_dir)


def check_geometry():
    assert math.isclose(GEOMETRY.frobenius_norm(G1), 4)
    assert math.isclose(GEOMETRY.frobenius_norm(G2), math.sqrt(2))
    assert math.isclose(FACTOR1, 0.25)
    assert math.isclose(FACTOR2, 1 / math.sqrt(2))
    assert math.isclose(ANGLE_A, -math.degrees(math.atan(0.2)))
    assert math.isclose(ANGLE_B, -22.5)
    assert math.isclose(polar_angle(GEOMETRY.scale(A, 0.25)), ANGLE_A)
    for threshold in [0.25, 1, math.sqrt(2), 2, 3, 4, 4.5]:
        first, _ = GEOMETRY.clip(G1, threshold)
        second, _ = GEOMETRY.clip(G2, threshold)
        expected = -22.5 if threshold <= math.sqrt(2) else (
            ANGLE_A if threshold >= 4 else -math.degrees(math.atan(1 / (threshold + 1)))
        )
        assert math.isclose(polar_angle(GEOMETRY.mean(first, second)), expected)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview-dir", type=Path, help="Also export PNGs for visual review.")
    args = parser.parse_args()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    if args.preview_dir:
        args.preview_dir.mkdir(parents=True, exist_ok=True)
    check_geometry()
    clipping_matrices(args.preview_dir)
    polar_rotation(args.preview_dir)
    clipping_sweep(args.preview_dir)
    print(f"Polar angles: {ANGLE_A:.6f}°, {ANGLE_B:.6f}°; clockwise change: {ANGLE_A - ANGLE_B:.6f}°")


if __name__ == "__main__":
    main()
