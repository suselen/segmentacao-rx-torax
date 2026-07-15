"""Geração de tabela e rascunho técnico estruturado."""

from typing import Dict, Optional

import pandas as pd


def metrics_table(
    intensity_stats: Dict[str, float],
    *,
    dice: Optional[float] = None,
    iou: Optional[float] = None,
) -> pd.DataFrame:
    """Transforma as métricas em tabela."""
    rows = [
        ("Intensidade mínima", intensity_stats["mínimo"]),
        ("Intensidade máxima", intensity_stats["máximo"]),
        ("Intensidade média", intensity_stats["média"]),
        ("Mediana", intensity_stats["mediana"]),
        ("Desvio-padrão", intensity_stats["desvio_padrão"]),
        ("Percentil 5", intensity_stats["percentil_05"]),
        ("Percentil 95", intensity_stats["percentil_95"]),
    ]

    if dice is not None:
        rows.append(("Dice", dice))
    if iou is not None:
        rows.append(("IoU", iou))

    return pd.DataFrame(rows, columns=["Métrica", "Valor"])


def technical_draft(
    *,
    image_shape: tuple[int, int],
    stats: Dict[str, float],
    edge_pixel_percentage: float,
    segmentation_status: str = "não avaliada",
) -> str:
    """
    Gera descrição técnica, sem afirmar diagnóstico.

    O texto descreve processamento e medidas computacionais.
    """
    height, width = image_shape

    return (
        "Radiografia de tórax processada para fins acadêmicos. "
        f"A imagem analisada possui {width} colunas e {height} linhas. "
        f"A intensidade média foi {stats['média']:.2f}, com desvio-padrão "
        f"de {stats['desvio_padrão']:.2f}. "
        f"Os pixels classificados como borda corresponderam a "
        f"{edge_pixel_percentage:.2f}% da imagem. "
        f"O estado da segmentação anatômica foi: {segmentation_status}. "
        "Foram produzidas versões com realce local de contraste, suavização "
        "e detecção de bordas para comparação visual. "
        "Este resultado é quantitativo e experimental, não constituindo "
        "interpretação radiológica ou laudo médico."
    )
