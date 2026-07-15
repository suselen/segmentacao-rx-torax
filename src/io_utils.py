"""Leitura e conversão de imagens radiográficas."""

from pathlib import Path
from typing import Tuple, Union

import cv2
import numpy as np
import pydicom


PathLike = Union[str, Path]


def normalize_to_uint8(image: np.ndarray) -> np.ndarray:
    """Normaliza uma matriz numérica para o intervalo [0, 255]."""
    arr = np.asarray(image).astype(np.float32)

    finite = np.isfinite(arr)
    if not finite.any():
        raise ValueError("A imagem não possui valores numéricos válidos.")

    min_value = float(arr[finite].min())
    max_value = float(arr[finite].max())

    if max_value <= min_value:
        return np.zeros(arr.shape, dtype=np.uint8)

    normalized = (arr - min_value) / (max_value - min_value)
    return np.clip(normalized * 255.0, 0, 255).astype(np.uint8)


def read_raster(path: PathLike) -> np.ndarray:
    """Lê PNG/JPG/TIFF e devolve imagem em tons de cinza uint8."""
    image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Não foi possível ler a imagem: {path}")
    return image


def read_dicom(path: PathLike) -> Tuple[np.ndarray, pydicom.dataset.FileDataset]:
    """Lê DICOM, aplica rescale e devolve imagem uint8 e dataset."""
    dataset = pydicom.dcmread(str(path))
    image = dataset.pixel_array.astype(np.float32)

    slope = float(getattr(dataset, "RescaleSlope", 1.0))
    intercept = float(getattr(dataset, "RescaleIntercept", 0.0))
    image = image * slope + intercept

    photometric = str(getattr(dataset, "PhotometricInterpretation", ""))
    image = normalize_to_uint8(image)

    if photometric == "MONOCHROME1":
        image = 255 - image

    return image, dataset


def read_image(path: PathLike):
    """Seleciona automaticamente a leitura por extensão."""
    suffix = Path(path).suffix.lower()
    if suffix in {".dcm", ".dicom"}:
        image, dataset = read_dicom(path)
        return image, dataset
    return read_raster(path), None
