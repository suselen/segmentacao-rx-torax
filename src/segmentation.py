"""Segmentação anatômica.

A v0.1 contém apenas uma linha de base exploratória. Ela não deve ser usada
como resultado clínico. A v0.2 substituirá esta etapa por máscaras validadas
e, posteriormente, por modelo treinado.
"""

import cv2
import numpy as np


def exploratory_lung_candidate_mask(image: np.ndarray) -> np.ndarray:
    """
    Produz candidatos escuros internos ao tórax por limiarização e morfologia.

    Limitações:
    - não garante a separação correta dos pulmões;
    - pode incluir fundo, abdome, ar externo e artefatos;
    - serve apenas para demonstrar o pipeline de PDI.
    """
    if image.ndim != 2:
        raise ValueError("A imagem deve estar em tons de cinza.")

    blurred = cv2.GaussianBlur(image, (7, 7), 0)
    _, binary = cv2.threshold(
        blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    h, w = image.shape
    roi = np.zeros_like(binary)
    cv2.rectangle(
        roi,
        (int(0.10 * w), int(0.08 * h)),
        (int(0.90 * w), int(0.92 * h)),
        255,
        -1,
    )
    binary = cv2.bitwise_and(binary, roi)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel)

    count, labels, stats, _ = cv2.connectedComponentsWithStats(cleaned, 8)
    candidates = []

    for label in range(1, count):
        area = int(stats[label, cv2.CC_STAT_AREA])
        x = int(stats[label, cv2.CC_STAT_LEFT])
        y = int(stats[label, cv2.CC_STAT_TOP])
        bw = int(stats[label, cv2.CC_STAT_WIDTH])
        bh = int(stats[label, cv2.CC_STAT_HEIGHT])

        touches_border = x <= 1 or y <= 1 or x + bw >= w - 1 or y + bh >= h - 1
        if not touches_border and area > 0.01 * h * w:
            candidates.append((area, label))

    candidates.sort(reverse=True)
    selected_labels = {label for _, label in candidates[:2]}

    mask = np.zeros_like(binary)
    for label in selected_labels:
        mask[labels == label] = 255

    return mask


def segment_heart(*args, **kwargs):
    """Reservado para a v0.2."""
    raise NotImplementedError(
        "A segmentação cardíaca será implementada na v0.2 com máscara validada."
    )
