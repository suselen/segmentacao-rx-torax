"""Métricas para avaliação de máscaras binárias."""

import numpy as np


def _as_bool(mask: np.ndarray) -> np.ndarray:
    arr = np.asarray(mask)
    if arr.ndim != 2:
        raise ValueError("A máscara deve possuir duas dimensões.")
    return arr > 0


def intersection_over_union(reference: np.ndarray, prediction: np.ndarray) -> float:
    """Calcula IoU. Duas máscaras vazias resultam em 1.0."""
    ref = _as_bool(reference)
    pred = _as_bool(prediction)

    if ref.shape != pred.shape:
        raise ValueError("As máscaras devem possuir a mesma dimensão.")

    intersection = np.logical_and(ref, pred).sum()
    union = np.logical_or(ref, pred).sum()

    return 1.0 if union == 0 else float(intersection / union)


def dice_coefficient(reference: np.ndarray, prediction: np.ndarray) -> float:
    """Calcula Dice. Duas máscaras vazias resultam em 1.0."""
    ref = _as_bool(reference)
    pred = _as_bool(prediction)

    if ref.shape != pred.shape:
        raise ValueError("As máscaras devem possuir a mesma dimensão.")

    intersection = np.logical_and(ref, pred).sum()
    denominator = ref.sum() + pred.sum()

    return 1.0 if denominator == 0 else float((2.0 * intersection) / denominator)
