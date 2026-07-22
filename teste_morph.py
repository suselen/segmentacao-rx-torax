import numpy as np

from third_party import morph
from third_party.morph import mm


def main() -> None:
    """Testa as operações básicas da versão incorporada."""

    image = np.array(
        [
            [10, 20, 30, 40],
            [50, 60, 70, 80],
            [90, 100, 110, 120],
            [130, 140, 150, 160],
        ],
        dtype=np.uint8,
    )

    binary = mm.threshold(image, 80)
    gaussian = mm.gaussian(image, N=3)
    sobel = mm.sobel(image)

    print("Versão da morph:", morph.__version__)

    print("\nImagem original:")
    print(image)

    print("\nLimiarização:")
    print(binary)

    print("\nFiltro Gaussiano:")
    print(gaussian)

    print("\nSobel:")
    print(sobel)


if __name__ == "__main__":
    main()