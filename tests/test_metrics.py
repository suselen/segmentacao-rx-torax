import numpy as np

from src.metrics import dice_coefficient, intersection_over_union


def test_identical_masks():
    mask = np.array([[1, 0], [1, 0]], dtype=np.uint8)
    assert intersection_over_union(mask, mask) == 1.0
    assert dice_coefficient(mask, mask) == 1.0


def test_empty_masks():
    empty = np.zeros((2, 2), dtype=np.uint8)
    assert intersection_over_union(empty, empty) == 1.0
    assert dice_coefficient(empty, empty) == 1.0


def test_partial_overlap():
    reference = np.array([[1, 1], [0, 0]], dtype=np.uint8)
    prediction = np.array([[1, 0], [0, 0]], dtype=np.uint8)

    assert intersection_over_union(reference, prediction) == 0.5
    assert np.isclose(dice_coefficient(reference, prediction), 2 / 3)
