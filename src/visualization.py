"""Visualizações do pipeline."""

from typing import Mapping, Optional

import matplotlib.pyplot as plt
import numpy as np


def show_images(
    images: Mapping[str, np.ndarray],
    *,
    cols: int = 3,
    figsize: Optional[tuple[float, float]] = None,
):
    """Exibe um dicionário título → imagem."""
    names = list(images.keys())
    values = list(images.values())
    n = len(values)
    rows = (n + cols - 1) // cols

    fig, axes = plt.subplots(
        rows,
        cols,
        figsize=figsize or (5 * cols, 4 * rows),
        squeeze=False,
    )

    for index, (name, image) in enumerate(zip(names, values)):
        ax = axes[index // cols][index % cols]
        ax.imshow(image, cmap="gray")
        ax.set_title(name)
        ax.axis("off")

    for index in range(n, rows * cols):
        axes[index // cols][index % cols].axis("off")

    plt.tight_layout()
    return fig


def plot_histogram(image: np.ndarray, bins: int = 256):
    """Exibe o histograma dos níveis de cinza."""
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(np.asarray(image).ravel(), bins=bins, range=(0, 255))
    ax.set_title("Histograma dos tons de cinza")
    ax.set_xlabel("Intensidade")
    ax.set_ylabel("Quantidade de pixels")
    ax.grid(alpha=0.2)
    plt.tight_layout()
    return fig


def overlay_mask(
    image: np.ndarray,
    mask: np.ndarray,
    *,
    alpha: float = 0.35,
):
    """Sobrepõe máscara binária à imagem para inspeção visual."""
    base = np.stack([image, image, image], axis=-1).astype(np.float32)
    overlay = base.copy()
    positive = np.asarray(mask) > 0
    overlay[positive, 0] = 255
    overlay[positive, 1] *= 0.35
    overlay[positive, 2] *= 0.35
    blended = (1 - alpha) * base + alpha * overlay
    return np.clip(blended, 0, 255).astype(np.uint8)
