"""Pré-processamento clássico de radiografias."""

from dataclasses import dataclass

import cv2
import numpy as np


@dataclass(frozen=True)
class PreprocessingResult:
    original: np.ndarray
    clahe: np.ndarray
    gaussian: np.ndarray
    median: np.ndarray
    bilateral: np.ndarray
    sobel: np.ndarray
    canny: np.ndarray


def apply_clahe(
    image: np.ndarray,
    clip_limit: float = 2.0,
    tile_grid_size: tuple[int, int] = (8, 8),
) -> np.ndarray:
    """Realce local de contraste com CLAHE."""
    clahe = cv2.createCLAHE(
        clipLimit=float(clip_limit),
        tileGridSize=tuple(tile_grid_size),
    )
    return clahe.apply(image)


def sobel_magnitude(image: np.ndarray) -> np.ndarray:
    """Magnitude do gradiente de Sobel."""
    gx = cv2.Sobel(image, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(image, cv2.CV_32F, 0, 1, ksize=3)
    magnitude = cv2.magnitude(gx, gy)
    return cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)


def preprocess(
    image: np.ndarray,
    *,
    clip_limit: float = 2.0,
    gaussian_kernel: int = 5,
    median_kernel: int = 5,
    canny_low: int = 50,
    canny_high: int = 150,
) -> PreprocessingResult:
    """Executa o pipeline CLAHE → filtros → bordas."""
    if image.ndim != 2:
        raise ValueError("A imagem deve estar em tons de cinza.")

    if gaussian_kernel % 2 == 0 or gaussian_kernel < 1:
        raise ValueError("gaussian_kernel deve ser ímpar e positivo.")
    if median_kernel % 2 == 0 or median_kernel < 1:
        raise ValueError("median_kernel deve ser ímpar e positivo.")

    clahe_img = apply_clahe(image, clip_limit=clip_limit)
    gaussian = cv2.GaussianBlur(clahe_img, (gaussian_kernel, gaussian_kernel), 0)
    median = cv2.medianBlur(clahe_img, median_kernel)
    bilateral = cv2.bilateralFilter(clahe_img, d=7, sigmaColor=50, sigmaSpace=50)
    sobel = sobel_magnitude(gaussian)
    canny = cv2.Canny(gaussian, canny_low, canny_high)

    return PreprocessingResult(
        original=image,
        clahe=clahe_img,
        gaussian=gaussian,
        median=median,
        bilateral=bilateral,
        sobel=sobel,
        canny=canny,
    )
