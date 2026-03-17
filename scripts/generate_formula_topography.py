from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter

matplotlib.use("Agg")


OUTPUT = Path(__file__).resolve().parents[1] / "public" / "formula-topography-fixed.svg"
SEED = 17
GRID_W = 480
GRID_H = 270


def build_field() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(SEED)
    x = np.linspace(-1.0, 1.0, GRID_W)
    y = np.linspace(-1.0, 1.0, GRID_H)
    xx, yy = np.meshgrid(x, y)

    field = np.zeros((GRID_H, GRID_W), dtype=float)

    # Layered smooth noise for continuous landform-like variation.
    for sigma, weight in (
        (4, 0.55),
        (8, 0.75),
        (16, 0.9),
        (30, 1.15),
        (54, 1.35),
    ):
        noise = rng.normal(size=(GRID_H, GRID_W))
        field += weight * gaussian_filter(noise, sigma=sigma, mode="wrap")

    # A broad directional flow to avoid isolated "blob islands".
    field += 0.35 * np.sin(1.8 * xx - 1.25 * yy)
    field += 0.28 * np.cos(1.1 * xx + 2.0 * yy)
    field += 0.18 * np.sin(2.6 * (xx + yy))

    # Peaks and basins shape recognizable relief zones.
    features = (
        (-0.72, 0.38, 1.7, 0.22, 0.30),
        (-0.28, -0.15, -1.25, 0.32, 0.22),
        (0.08, 0.10, 1.15, 0.26, 0.18),
        (0.42, -0.28, -1.05, 0.24, 0.24),
        (0.74, 0.34, 1.45, 0.20, 0.28),
    )

    for cx, cy, amplitude, sx, sy in features:
        field += amplitude * np.exp(-(((xx - cx) / sx) ** 2 + ((yy - cy) / sy) ** 2))

    field = gaussian_filter(field, sigma=1.2, mode="nearest")
    return xx, yy, field


def render_svg(output: Path) -> None:
    xx, yy, field = build_field()
    levels = np.linspace(field.min(), field.max(), 28)

    fig = plt.figure(figsize=(19.2, 10.8), dpi=100, facecolor="none")
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
        colors=["#686868"],
        linewidths=1.15,
        alpha=0.30,
        antialiased=True,
    )

    fig.savefig(output, format="svg", transparent=True, bbox_inches="tight", pad_inches=0)
    plt.close(fig)


if __name__ == "__main__":
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    render_svg(OUTPUT)
