import argparse
from dataclasses import dataclass
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter

matplotlib.use("Agg")


DEFAULT_OUTPUT = Path(__file__).resolve().parents[1] / "public" / "page-topography-fixed.svg"


@dataclass(frozen=True)
class ContourConfig:
    output: Path
    seed: int = 23
    grid_width: int = 480
    grid_height: int = 270
    levels: int = 16
    line_width: float = 1.6
    alpha: float = 0.10
    color: str = "#686868"
    smooth_sigma: float = 1.2
    noise_scale: float = 1.0
    flow_scale: float = 1.0
    feature_scale: float = 1.0
    figure_width: float = 19.2
    figure_height: float = 10.8


def parse_args() -> ContourConfig:
    parser = argparse.ArgumentParser(
        description="Generate a topographic contour SVG for the blog page background."
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--seed", type=int, default=23)
    parser.add_argument("--grid-width", type=int, default=480)
    parser.add_argument("--grid-height", type=int, default=270)
    parser.add_argument("--levels", type=int, default=16)
    parser.add_argument("--line-width", type=float, default=1.6)
    parser.add_argument("--alpha", type=float, default=0.10)
    parser.add_argument("--color", default="#686868")
    parser.add_argument("--smooth-sigma", type=float, default=1.2)
    parser.add_argument(
        "--noise-scale",
        type=float,
        default=1.0,
        help="Scale layered noise strength up or down.",
    )
    parser.add_argument(
        "--flow-scale",
        type=float,
        default=1.0,
        help="Scale directional flow strength up or down.",
    )
    parser.add_argument(
        "--feature-scale",
        type=float,
        default=1.0,
        help="Scale peaks and basins up or down.",
    )
    parser.add_argument("--figure-width", type=float, default=19.2)
    parser.add_argument("--figure-height", type=float, default=10.8)
    args = parser.parse_args()

    return ContourConfig(
        output=args.output,
        seed=args.seed,
        grid_width=args.grid_width,
        grid_height=args.grid_height,
        levels=args.levels,
        line_width=args.line_width,
        alpha=args.alpha,
        color=args.color,
        smooth_sigma=args.smooth_sigma,
        noise_scale=args.noise_scale,
        flow_scale=args.flow_scale,
        feature_scale=args.feature_scale,
        figure_width=args.figure_width,
        figure_height=args.figure_height,
    )


def build_field(config: ContourConfig) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(config.seed)
    x = np.linspace(-1.0, 1.0, config.grid_width)
    y = np.linspace(-1.0, 1.0, config.grid_height)
    xx, yy = np.meshgrid(x, y)

    field = np.zeros((config.grid_height, config.grid_width), dtype=float)

    # Layered smooth noise for continuous landform-like variation.
    for sigma, weight in (
        (4, 0.55),
        (8, 0.75),
        (16, 0.9),
        (30, 1.15),
        (54, 1.35),
    ):
        noise = rng.normal(size=(config.grid_height, config.grid_width))
        field += config.noise_scale * weight * gaussian_filter(noise, sigma=sigma, mode="wrap")

    # A broad directional flow to avoid isolated "blob islands".
    field += config.flow_scale * 0.35 * np.sin(1.8 * xx - 1.25 * yy)
    field += config.flow_scale * 0.28 * np.cos(1.1 * xx + 2.0 * yy)
    field += config.flow_scale * 0.18 * np.sin(2.6 * (xx + yy))

    # Peaks and basins shape recognizable relief zones.
    features = (
        (-0.72, 0.38, 1.7, 0.22, 0.30),
        (-0.28, -0.15, -1.25, 0.32, 0.22),
        (0.08, 0.10, 1.15, 0.26, 0.18),
        (0.42, -0.28, -1.05, 0.24, 0.24),
        (0.74, 0.34, 1.45, 0.20, 0.28),
    )

    for cx, cy, amplitude, sx, sy in features:
        field += config.feature_scale * amplitude * np.exp(
            -(((xx - cx) / sx) ** 2 + ((yy - cy) / sy) ** 2)
        )

    field = gaussian_filter(field, sigma=config.smooth_sigma, mode="nearest")
    return xx, yy, field


def render_svg(config: ContourConfig) -> None:
    xx, yy, field = build_field(config)
    levels = np.linspace(field.min(), field.max(), config.levels)

    fig = plt.figure(
        figsize=(config.figure_width, config.figure_height),
        dpi=100,
        facecolor="none",
    )
    ax = fig.add_axes((0, 0, 1, 1), facecolor="none")
    ax.set_axis_off()
    ax.set_xlim(xx.min(), xx.max())
    ax.set_ylim(yy.min(), yy.max())
    ax.set_aspect("auto")

    ax.contour(
        xx,
        yy,
        field,
        levels=levels,
        colors=[config.color],
        linewidths=config.line_width,
        alpha=config.alpha,
        antialiased=True,
    )

    fig.savefig(config.output, format="svg", transparent=True, bbox_inches="tight", pad_inches=0)
    plt.close(fig)


if __name__ == "__main__":
    config = parse_args()
    config.output.parent.mkdir(parents=True, exist_ok=True)
    render_svg(config)
