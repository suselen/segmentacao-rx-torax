"""Funções para desidentificação de DICOM e mascaramento de pixels."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Iterable, Sequence, Tuple, Union
import hashlib

import cv2
import numpy as np
import pydicom
from pydicom.uid import generate_uid


Rectangle = Tuple[int, int, int, int]


REMOVE_KEYWORDS = {
    "PatientName",
    "PatientID",
    "OtherPatientIDs",
    "OtherPatientNames",
    "PatientAddress",
    "PatientTelephoneNumbers",
    "AccessionNumber",
    "InstitutionName",
    "InstitutionAddress",
    "ReferringPhysicianName",
    "PerformingPhysicianName",
    "OperatorsName",
    "StudyID",
    "MedicalRecordLocator",
    "IssuerOfPatientID",
}

DATE_KEYWORDS = {
    "PatientBirthDate",
    "StudyDate",
    "SeriesDate",
    "AcquisitionDate",
    "ContentDate",
    "InstanceCreationDate",
}

TIME_KEYWORDS = {
    "StudyTime",
    "SeriesTime",
    "AcquisitionTime",
    "ContentTime",
    "InstanceCreationTime",
}


def _stable_code(value: str, salt: str) -> str:
    raw = f"{salt}|{value}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:12].upper()


def deidentify_dataset(
    dataset: pydicom.dataset.Dataset,
    *,
    preserve_sex: bool = True,
    preserve_birth_year: bool = False,
    salt: str = "troque-este-salt",
) -> pydicom.dataset.Dataset:
    """
    Cria cópia desidentificada do dataset.

    Por padrão:
    - preserva PatientSex;
    - remove data de nascimento completa;
    - remove datas e horários;
    - substitui identificadores e UIDs.

    A função é uma base acadêmica e não declara conformidade regulatória.
    """
    ds = deepcopy(dataset)

    original_patient_id = str(getattr(ds, "PatientID", "SEM_ID"))
    project_code = _stable_code(original_patient_id, salt)

    birth_year = ""
    birth_date = str(getattr(ds, "PatientBirthDate", ""))
    if preserve_birth_year and len(birth_date) >= 4:
        birth_year = birth_date[:4]

    for keyword in REMOVE_KEYWORDS:
        if hasattr(ds, keyword):
            setattr(ds, keyword, "")

    for keyword in DATE_KEYWORDS:
        if hasattr(ds, keyword):
            setattr(ds, keyword, "")

    for keyword in TIME_KEYWORDS:
        if hasattr(ds, keyword):
            setattr(ds, keyword, "")

    ds.PatientName = "ANONIMO"
    ds.PatientID = f"PROJ-{project_code}"

    if preserve_sex:
        ds.PatientSex = str(getattr(dataset, "PatientSex", ""))
    elif hasattr(ds, "PatientSex"):
        ds.PatientSex = ""

    if preserve_birth_year and birth_year:
        ds.PatientBirthDate = f"{birth_year}0101"
    else:
        ds.PatientBirthDate = ""

    # Novos UIDs evitam manter identificadores internos do exame original.
    for keyword in (
        "StudyInstanceUID",
        "SeriesInstanceUID",
        "SOPInstanceUID",
        "FrameOfReferenceUID",
    ):
        if hasattr(ds, keyword):
            setattr(ds, keyword, generate_uid())

    if hasattr(ds, "file_meta") and hasattr(ds.file_meta, "MediaStorageSOPInstanceUID"):
        ds.file_meta.MediaStorageSOPInstanceUID = getattr(ds, "SOPInstanceUID", generate_uid())

    if hasattr(ds, "remove_private_tags"):
        ds.remove_private_tags()

    return ds


def save_deidentified_dicom(
    dataset: pydicom.dataset.Dataset,
    output_path: Union[str, Path],
    **kwargs,
) -> Path:
    """Desidentifica e salva uma cópia DICOM."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    ds = deidentify_dataset(dataset, **kwargs)
    ds.save_as(str(output))
    return output


def mask_pixel_regions(
    image: np.ndarray,
    rectangles: Iterable[Rectangle],
    value: int = 0,
) -> np.ndarray:
    """
    Cobre regiões retangulares da imagem.

    Cada retângulo usa o formato (x, y, largura, altura).
    Essa abordagem é adequada quando nome/ID estão gravados nos pixels.
    """
    result = np.asarray(image).copy()

    if result.ndim not in {2, 3}:
        raise ValueError("A imagem deve possuir duas ou três dimensões.")

    height, width = result.shape[:2]

    for x, y, w, h in rectangles:
        x1 = max(0, int(x))
        y1 = max(0, int(y))
        x2 = min(width, x1 + max(0, int(w)))
        y2 = min(height, y1 + max(0, int(h)))

        if x2 > x1 and y2 > y1:
            result[y1:y2, x1:x2] = value

    return result


def default_corner_masks(image: np.ndarray, fraction: float = 0.14) -> Sequence[Rectangle]:
    """
    Gera máscaras de segurança nos quatro cantos.

    Deve ser revisado visualmente: textos identificadores podem estar em outras áreas.
    """
    h, w = image.shape[:2]
    fw = max(1, int(w * fraction))
    fh = max(1, int(h * fraction))
    return [
        (0, 0, fw, fh),
        (w - fw, 0, fw, fh),
        (0, h - fh, fw, fh),
        (w - fw, h - fh, fw, fh),
    ]
