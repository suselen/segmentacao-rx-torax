"""Estatísticas e medições quantitativas."""

from typing import Dict, Optional

import numpy as np


def intensity_statistics(
    image: np.ndarray,
    mask: Optional[np.ndarray] = None,
) -> Dict[str, float]:
    """Calcula estatísticas globais ou dentro de uma máscara."""
    arr = np.asarray(image)

    if arr.ndim != 2:
        raise ValueError("A imagem deve possuir duas dimensões.")

    if mask is not None:
        selected = arr[np.asarray(mask) > 0]
    else:
        selected = arr.ravel()

    if selected.size == 0:
        raise ValueError("Nenhum pixel foi selecionado.")

    return {
        "mínimo": float(np.min(selected)),
        "máximo": float(np.max(selected)),
        "média": float(np.mean(selected)),
        "mediana": float(np.median(selected)),
        "desvio_padrão": float(np.std(selected)),
        "percentil_05": float(np.percentile(selected, 5)),
        "percentil_25": float(np.percentile(selected, 25)),
        "percentil_75": float(np.percentile(selected, 75)),
        "percentil_95": float(np.percentile(selected, 95)),
    }


def mask_area_percentage(mask: np.ndarray) -> float:
    """Percentual de pixels positivos da máscara."""
    arr = np.asarray(mask) > 0
    return float(100.0 * arr.sum() / arr.size)


def cardiothoracic_ratio(
    cardiac_width_pixels: float,
    thoracic_width_pixels: float,
) -> float:
    """Calcula a razão cardiotorácica a partir de larguras já determinadas."""
    if thoracic_width_pixels <= 0:
        raise ValueError("A largura torácica deve ser maior que zero.")
    if cardiac_width_pixels < 0:
        raise ValueError("A largura cardíaca não pode ser negativa.")
    return float(cardiac_width_pixels / thoracic_width_pixels)
